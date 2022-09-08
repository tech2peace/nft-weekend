from svglib.svglib import svg2rlg
import numpy as np
from reportlab.graphics.shapes import Line, Circle, Image


def lerp(t, locs, vals):
    x0, x1 = locs
    q0, q1 = vals
    length = (x1 - x0)
    c = (t - x0) / length * q0 + (x1 - t) / length * q1
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


def extract_background(drawing):
    bg = find_by_id(drawing, "Background")
    if len(bg.contents) > 0:
        return bg.contents[0]
    return None

def unpack_drawing(drawing, offset_stroke=None):
    words = find_by_id(drawing, "Words")

    word_forms = []
    forms_langs = []
    # Fixed cases where svgid causes another layer of grouping
    # Extract lang from svgid
    for i, wordform in enumerate(words.contents):
        forms_langs.append(wordform.svgid)
        if len(wordform.contents) > 1:
            word_forms.append(wordform.contents)
        else:
            word_forms.append(wordform.contents[0].contents)
            words.contents[i] = wordform.contents[0]
    # Unpack letters

    letters_forms = zip(*word_forms)

    P = [[LetterForm(letter_form) for letter_form in letter_forms] for letter_forms in letters_forms]

    if offset_stroke:
        # Keep two word forms
        words.contents = words.contents[:2]
        return words.contents[1], P, forms_langs, words.contents[0]
    else:
        # Keep only one word form
        words.contents = words.contents[:1]
        return words.contents[0], P, forms_langs, None


class LetterForm:

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
            sc = letter_form.strokeColor
            self.stroke_color = np.asarray(
                [sc.red, sc.green, sc.blue])
            self.stroke_width = letter_form.strokeWidth
        else:
            for letter_part in letter_form.contents:
                if hasattr(letter_part, "contents"):
                    letter_part = letter_part.contents[0]
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
        self.strokes = np.asarray(self.strokes, dtype=object)

    def __mul__(self, scalar):
        s, sc, sw = self.strokes * scalar, self.stroke_color * scalar, self.stroke_width * scalar
        return LetterForm(s, sc, sw)

    def __rmul__(self, scalar):
        s, sc, sw = self.strokes * scalar, self.stroke_color * scalar, self.stroke_width * scalar
        return LetterForm(s, sc, sw)

    def __truediv__ (self, scalar):
        s, sc, sw = self.strokes / scalar, self.stroke_color / scalar, self.stroke_width / scalar
        return LetterForm(s, sc, sw)

    def __add__(self, other):
        return LetterForm(self.strokes + other.strokes, self.stroke_color + other.stroke_color, self.stroke_width + other.stroke_width)


class SpectrumWord:

    def __init__(self, input_path, offset_stroke=None):
        self.drawing = svg2rlg(input_path)
        # P is a list of letters, each letter has F forms, each form has the same amount of bezier curves,
        # the curves has the same amount of control points
        if offset_stroke:
            self.offset_stroke_color, self.offset_stroke_width = offset_stroke
        self.word, self.letters, self.forms_langs, self.offset_stroke = unpack_drawing(self.drawing, offset_stroke)
        self.forms_count = len(self.forms_langs)
        self.locs = [-1, 1] if self.forms_count == 2 else np.asarray([(-1, -1), (1, -1), (-1, 1), (1, 1)])

        self.bg = extract_background(self.drawing)
        return

    def set_background_image(self, path):
        if self.bg:
            curr_bg = self.bg.contents[0]
            new_bg = Image(curr_bg.x, curr_bg.y, curr_bg.width, curr_bg.height, path)
            self.bg.contents[0] = new_bg
        pass

    def set_drawing_points(self, letter_parts, points, color, width):
        for p, g in zip(points, letter_parts.contents):
            if hasattr(g, "contents"):
                g = g.contents[0]
            if type(g) == Line:
                g.x1, g.x2, g.y1, g.y2 = p.tolist()
            elif type(g) == Circle:
                g.cx, g.cy = p.tolist()
            else:
                g.strokeColor.red, g.strokeColor.green, g.strokeColor.blue = color
                g.strokeWidth = width
                g.points = p.tolist()

    def sample(self, T):
        assert len(self.letters) == len(T)

        # P is a list of letters, each letter has F forms, each form has the same amount of bezier curves,
        # the curves has the same amount of control points
        for i, (t, letter_forms) in enumerate(zip(T, self.letters)):

            # ith letter
            # linear interpolation
            if self.forms_count == 2:
                cp = lerp(t, self.locs, letter_forms)
                cp = cp[0]
            # bilinear interpolation
            if self.forms_count == 4:
                points = list(zip(*self.locs.T, letter_forms))
                cp = bilinear_interpolation(*t, points)

            if self.offset_stroke:
                self.set_drawing_points(self.offset_stroke.contents[i], cp.strokes, self.offset_stroke_color, cp.stroke_width + self.offset_stroke_width)
            self.set_drawing_points(self.word.contents[i], cp.strokes, cp.stroke_color, cp.stroke_width)
        return self.drawing

    def calculate_ar_heb_percentages(self, centers):
        Ar = [100 if lang.startswith("Ar") else 0  for lang in self.forms_langs]
        ar_vals = []
        for c in centers:
            if self.forms_count == 2:
                ar_vals.append(lerp(c, self.locs, Ar))
            if self.forms_count == 4:
                points = list(zip(*self.locs.T, Ar))
                ar_vals.append(bilinear_interpolation(*c, points))
        ar_percentage = round(np.average(ar_vals), 2)
        return (ar_percentage, 100 - ar_percentage)