
from svglib.svglib import svg2rlg
import numpy as np
from reportlab.graphics.shapes import Line, Circle

def lerp(t, l0, l1):
    c = t * l0 + (1 - t) * l1
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
    P = []
    for letter_forms in letters:
        letter_parts = []
        for letter_form in letter_forms:
            l = []
            if type(letter_form) == Line:
                points = [ letter_form.x1, letter_form.x2, letter_form.y1, letter_form.y2 ]
                l = [points,]
            else:
                for letter_part in letter_form.contents:
                    if hasattr(letter_part, "contents"):
                        points = letter_part.contents[0].points
                    else:
                        if type(letter_part) == Line:
                            points = [letter_part.x1, letter_part.x2, letter_part.y1, letter_part.y2]
                        elif type(letter_part) == Circle:
                            points = [letter_part.cx, letter_part.cy]
                        else:
                            points = letter_part.points
                    l.append(np.asarray(points))
            letter_parts.append(l)
            # letter_parts.append([np.asarray(letter_part.contents[0].points) for letter_part in letter_form.contents])
        P.append(letter_parts)

    # Keep only one word form
    words.contents = words.contents[:1]
    return words.contents[0], P, len(word_forms)

class SpectrumWord():

    def __init__(self, input_path):
        self.drawing = svg2rlg(input_path)
        # P is a list of letters, each letter has F forms, each form has the same amount of bezier curves,
        # the curves has the same amount of control points
        self.word, self.P, self.forms_count = unpack_drawing(self.drawing)
        return

    def set_drawing_points(self, i, points):
        for p, g in zip(points, self.word.contents[i].contents):
            if hasattr(g, "contents"):
                g.contents[0].points = p.tolist()
            else:
                if type(g) == Line:
                    g.x1, g.x2, g.y1, g.y2 = p.tolist()
                elif type(g) == Circle:
                    g.cx, g.cy = p.tolist()
                else:
                    g.points = p.tolist()

    def sample(self, T):
        assert len(self.P) == len(T)
        locs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        # P is a list of letters, each letter has F forms, each form has the same amount of bezier curves,
        # the curves has the same amount of control points
        for i, (t, L) in enumerate(zip(T, self.P)):
            # ith letter
            L = np.asarray(L)
            # linear interpolation
            if len(L) == 2:
                print(i, [len(x) for x in L[0]], [len(x) for x in L[1]])
                c = lerp(t, *L)

            # bilinear interpolation
            if len(L) == 4:
                l0, l1, l2, l3 = L[0], L[1], L[2], L[3]
                #c = old_quad_lerp(t, *L)
                c = bilinear_interpolation(*t,
                                       [(*locs[0], l0),
                                        (*locs[1], l2),
                                        (*locs[2], l1),
                                        (*locs[3], l3)])

            self.set_drawing_points(i, list(c))
        return self.drawing

