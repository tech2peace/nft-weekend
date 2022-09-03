
from svglib.svglib import svg2rlg
import numpy as np
from reportlab.graphics.shapes import Line, Circle

def lerp(t, locs, vals):
    x0, x1 = locs
    q0, q1 = vals
    length = (x1 - x0)
    c = (t - x0) / length * q0 + (x1 - t) / length * q1
    return c

def old_quad_lerp(t, l0, l1, l2, l3):
    a0 = t * l0 + (1 - t) * l1
    a1 = t * l1 + (1 - t) * l2
    a2 = t * l2 + (1 - t) * l3
    b0 = t * a0 + (1 - t) * a1
    b1 = t * a1 + (1 - t) * a2
    c = t * b0 + (1 - t) * b1
    return c

def bilinear_interpolation(x, y, points):
    '''Interpolate (x,y) from values associated with four points.

    The four points are a list of four triplets:  (x, y, value).
    The four points can be in any order.  They should form a rectangle.

        >>> bilinear_interpolation(12, 5.5,
        ...                        [(10, 4, 100),
        ...                         (20, 4, 200),
        ...                         (10, 6, 150),
        ...                         (20, 6, 300)])
        165.0

    '''
    # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)

def find_by_id(drawing, id):
    if not hasattr(drawing, "contents"):
        return None
    for group in drawing.contents:
        if hasattr(group, "svgid"):
            if group.svgid == id:
                return group
        res = find_by_id(group, id)
        if res:
            return res
    return None

def unpack_drawing(drawing):
    words = find_by_id(drawing, "Words")

    word_forms = words.contents
    # Unpack letters
    letters = zip(*[wordform.contents for wordform in word_forms])
    P = [[LetterForm(letter_form) for letter_form in letter_forms] for letter_forms in letters]

    # Keep only one word form
    words.contents = words.contents[:1]
    return words.contents[0], P, len(word_forms)

class LetterForm():

    # constructor overloading
    # based on args
    def __init__(self, *args):

        # if arg is an integer
        # square the arg
        if len(args) == 1:
            self.from_drawing(*args)

        # if arg is string
        # Print with hello
        elif len(args) == 3:
            self.from_parameters(*args)

    def from_parameters(self, strokes, stroke_color, stroke_width):
        self.strokes = strokes
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    def from_drawing(self, letter_form):
        self.strokes = []
        if type(letter_form) == Line:
            control_points = [letter_form.x1, letter_form.x2, letter_form.y1, letter_form.y2]
            self.strokes.append(np.asarray(control_points))
        else:
            for letter_part in letter_form.contents:
                if hasattr(letter_part, "contents"):
                    control_points = letter_part.contents[0].points
                else:
                    sc = letter_part.strokeColor
                    self.stroke_color = np.asarray(
                        [sc.red, sc.green, sc.blue])
                    self.stroke_width = letter_part.strokeWidth
                    if type(letter_part) == Line:
                        control_points = [letter_part.x1, letter_part.x2, letter_part.y1, letter_part.y2]
                    elif type(letter_part) == Circle:
                        control_points = [letter_part.cx, letter_part.cy]
                    else:
                        control_points = letter_part.points
                self.strokes.append(np.asarray(control_points))
        self.strokes = np.asarray(self.strokes)

    def __mul__(self, scalar):
        print('__mul__')
        s, sc, sw = self.strokes * scalar, self.stroke_color * scalar, self.stroke_width * scalar
        return LetterForm(s, sc, sw)

    def __rmul__(self, scalar):
        print('__rmul__')
        s, sc, sw = self.strokes * scalar, self.stroke_color * scalar, self.stroke_width * scalar
        return LetterForm(s, sc, sw)
    def __add__(self, other):
        print('__add__')
        return LetterForm(self.strokes + other.strokes, self.stroke_color + other.stroke_color, self.stroke_width + other.stroke_width)

class SpectrumWord():

    def __init__(self, input_path):
        self.drawing = svg2rlg(input_path)
        # P is a list of letters, each letter has F forms, each form has the same amount of bezier curves,
        # the curves has the same amount of control points
        self.word, self.P, self.forms_count = unpack_drawing(self.drawing)
        return

    def set_drawing_points(self, i, points, color, width):
        for p, g in zip(points, self.word.contents[i].contents):
            if hasattr(g, "contents"):
                g.contents[0].points = p.tolist()
            else:
                if type(g) == Line:
                    g.x1, g.x2, g.y1, g.y2 = p.tolist()
                elif type(g) == Circle:
                    g.cx, g.cy = p.tolist()
                else:
                    g.strokeColor.red, g.strokeColor.green, g.strokeColor.blue = color
                    g.strokeWidth = width
                    g.points = p.tolist()

    def sample(self, T):
        assert len(self.P) == len(T)

        # P is a list of letters, each letter has F forms, each form has the same amount of bezier curves,
        # the curves has the same amount of control points
        for i, (t, letter_forms) in enumerate(zip(T, self.P)):
            locs = [-1, 1]
            # ith letter
            #L = np.asarray(L)
            # linear interpolation
            if len(letter_forms) == 2:
                #print(i, [len(x) for x in L[0]], [len(x) for x in L[1]])
                cp = lerp(t, locs, letter_forms)
                # control_points0, color0, width0 = L[0]
                # control_points1, color1, width1 = L[1]
                # cp = lerp(t, locs, [np.asarray(control_points0), np.asarray(control_points1)])
                # colors = np.asarray([color0, color1])
                # color = lerp(t, locs, colors)
                # width = lerp(t, locs, [width0, width1])

            # bilinear interpolation
            if len(letter_forms) == 4:
                locs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
                l0, l1, l2, l3 = L[0], L[1], L[2], L[3]
                cp = bilinear_interpolation(*t,
                                       [(*locs[0], l0),
                                        (*locs[1], l2),
                                        (*locs[2], l1),
                                        (*locs[3], l3)])

            self.set_drawing_points(i, cp[0].strokes, cp[0].stroke_color, cp[0].stroke_width)
        return self.drawing

