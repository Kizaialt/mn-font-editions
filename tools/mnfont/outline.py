"""Outline access and measurement helpers.

All geometry is in font units. A "contour" is a list of (x, y, on_curve)
tuples in TrueType point order (quadratic B-splines, implied on-curve
points between consecutive off-curve points). A "shape" is a list of
contours.
"""
from __future__ import annotations

import math
from functools import lru_cache

from fontTools.pens.recordingPen import DecomposingRecordingPointPen
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.varLib.iup import iup_delta
from fontTools.varLib.models import supportScalar


# --------------------------------------------------------------------------
# Locations / masters
# --------------------------------------------------------------------------

def loc_key(loc: dict) -> tuple:
    """Hashable key for a normalized location (drops zero coordinates)."""
    return tuple(sorted((k, round(v, 6)) for k, v in loc.items() if v))


def master_locations(font, glyph_names) -> list[dict]:
    """Default + the peak of every gvar tuple used by `glyph_names`.

    Returned as normalized location dicts, default ({}) first.
    """
    gvar = font["gvar"]
    seen = {(): {}}
    for name in glyph_names:
        for tv in gvar.variations.get(name, []):
            loc = {ax: peak for ax, (lo, peak, hi) in tv.axes.items() if peak}
            seen.setdefault(loc_key(loc), loc)
    return list(seen.values())


class GlyphSets:
    """Caches decomposed glyph outlines per normalized location."""

    def __init__(self, font):
        self.font = font
        self._sets = {}
        self._cache = {}

    def glyphset(self, loc):
        key = loc_key(loc)
        if key not in self._sets:
            if key:
                self._sets[key] = self.font.getGlyphSet(location=dict(loc), normalized=True)
            else:
                self._sets[key] = self.font.getGlyphSet()
        return self._sets[key]

    def shape(self, name, loc) -> list[list[tuple]]:
        """Decomposed contours of `name` at `loc` (floats, unrounded)."""
        key = (name, loc_key(loc))
        if key not in self._cache:
            gs = self.glyphset(loc)
            pen = DecomposingRecordingPointPen(gs)
            gs[name].drawPoints(pen)
            contours, cur = [], None
            for op, args, kw in pen.value:
                if op == "beginPath":
                    cur = []
                elif op == "addPoint":
                    (x, y), seg = args[0], args[1]
                    cur.append((float(x), float(y), seg is not None))
                elif op == "endPath":
                    contours.append(cur)
            self._cache[key] = contours
        return [list(c) for c in self._cache[key]]

    def advance(self, name, loc) -> float:
        return float(self.glyphset(loc)[name].width)


def full_coords(font, name, loc) -> GlyphCoordinates:
    """Raw point coordinates (incl. the 4 phantom points) of glyph `name` at a
    normalized location, exactly as a TrueType-gvar rasterizer computes them
    (same algorithm as fontTools' glyph set).  For composites the "points"
    are the component offsets."""
    glyf = font["glyf"]
    hm = font["hmtx"].metrics
    vm = font["vmtx"].metrics if "vmtx" in font else None
    coords, controls = glyf._getCoordinatesAndControls(name, hm, vm)
    coords = GlyphCoordinates(coords)
    if not loc or "gvar" not in font:
        return coords
    orig = GlyphCoordinates(coords)
    endPts = controls[1] if controls[0] >= 1 else list(range(len(controls[1])))
    for tv in font["gvar"].variations.get(name, []):
        scalar = supportScalar(loc, tv.axes)
        if not scalar:
            continue
        delta = tv.coordinates
        if None in delta:
            delta = iup_delta(delta, orig, endPts)
        coords += GlyphCoordinates(delta) * scalar
    return coords


# --------------------------------------------------------------------------
# Geometry utilities
# --------------------------------------------------------------------------

def flatten_contour(contour, steps=24):
    """TrueType quadratic contour -> closed polyline [(x, y), ...]."""
    pts = contour
    n = len(pts)
    if n == 0:
        return []
    if all(not p[2] for p in pts):  # all off-curve: insert implied on-curves
        start = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2, True)
        pts = [start] + pts
        n = len(pts)
    # rotate so we start on an on-curve point
    k = next(i for i, p in enumerate(pts) if p[2])
    pts = pts[k:] + pts[:k]
    out = [(pts[0][0], pts[0][1])]
    i = 1
    cur = pts[0]
    offs = []

    def emit_quad(p0, c, p1):
        for s in range(1, steps + 1):
            t = s / steps
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]
            out.append((x, y))

    seq = pts[1:] + [pts[0]]
    for p in seq:
        if p[2]:
            if not offs:
                out.append((p[0], p[1]))
            else:
                for j, c in enumerate(offs):
                    if j < len(offs) - 1:
                        nxt = offs[j + 1]
                        end = ((c[0] + nxt[0]) / 2, (c[1] + nxt[1]) / 2)
                    else:
                        end = (p[0], p[1])
                    emit_quad(cur, c, end)
                    cur = end
                offs = []
            cur = (p[0], p[1])
        else:
            offs.append(p)
    if out[-1] == out[0]:
        out.pop()
    return out


def flatten(shape, steps=24):
    return [flatten_contour(c, steps) for c in shape if c]


def _crossings(polys, coord, axis):
    """Crossings of the line {axis == coord} with polygon edges.
    axis=1: horizontal line y=coord -> returns [(x, winding_dir)]
    axis=0: vertical line   x=coord -> returns [(y, winding_dir)]"""
    res = []
    o = 1 - axis
    for poly in polys:
        m = len(poly)
        for i in range(m):
            a, b = poly[i], poly[(i + 1) % m]
            a1, b1 = a[axis], b[axis]
            if a1 == b1:
                continue
            if (a1 <= coord < b1) or (b1 <= coord < a1):
                t = (coord - a1) / (b1 - a1)
                res.append((a[o] + t * (b[o] - a[o]), 1 if b1 > a1 else -1))
    res.sort()
    return res


def ink_intervals(shape_or_polys, coord, axis, flattened=False):
    """Non-zero-winding ink intervals along a horizontal (axis=1, y=coord)
    or vertical (axis=0, x=coord) line."""
    polys = shape_or_polys if flattened else flatten(shape_or_polys)
    cr = _crossings(polys, coord, axis)
    out, w, start = [], 0, None
    for pos, d in cr:
        nw = w + d
        if w == 0 and nw != 0:
            start = pos
        elif w != 0 and nw == 0:
            out.append((start, pos))
        w = nw
    # merge touching intervals
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] < 0.5:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def bounds(shape):
    pts = [p for poly in flatten(shape) for p in poly]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def on_bounds(shape):
    """Bounds of on-curve + off-curve points (control box)."""
    xs = [p[0] for c in shape for p in c]
    ys = [p[1] for c in shape for p in c]
    return min(xs), min(ys), max(xs), max(ys)


def signed_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return a / 2.0


def is_clockwise(contour):
    """TrueType outer contours are clockwise (negative signed area, y-up)."""
    return signed_area(flatten_contour(contour)) < 0


def _winding(polys, x, y):
    w = 0
    for poly in polys:
        m = len(poly)
        for i in range(m):
            (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % m]
            if y0 <= y < y1 or y1 <= y < y0:
                xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                if xi > x:
                    w += 1 if y1 > y0 else -1
    return w


def orientation_problems(shape, eps=1.5):
    """TrueType convention check that also works for holes and overlapping
    contours: walking along a correctly oriented contour, the ink is always
    on the RIGHT-hand side.  Returns indices of contours where most sampled
    edges have no ink on their right."""
    polys = flatten(shape)
    bad = []
    for ci, poly in enumerate(polys):
        m = len(poly)
        ok = tot = 0
        for i in range(m):
            (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % m]
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 4 * eps:
                continue
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            rx, ry = (y1 - y0) / L, -(x1 - x0) / L      # right-hand normal (y up)
            tot += 1
            ok += _winding(polys, mx + rx * eps, my + ry * eps) != 0
        if tot and ok < tot / 2:
            bad.append(ci)
    return bad


def line_x_at_y(p0, p1, y):
    (x0, y0), (x1, y1) = p0, p1
    if y1 == y0:
        raise ValueError("horizontal line")
    return x0 + (y - y0) * (x1 - x0) / (y1 - y0)


def line_y_at_x(p0, p1, x):
    (x0, y0), (x1, y1) = p0, p1
    if x1 == x0:
        raise ValueError("vertical line")
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def rect(x0, y0, x1, y1):
    """Clockwise rectangle contour starting top-left (TrueType outer)."""
    return [(x0, y1, True), (x1, y1, True), (x1, y0, True), (x0, y0, True)]


def round_shape(shape):
    return [[(int(round(x)), int(round(y)), on) for x, y, on in c] for c in shape]


def nearest_interval(intervals, target):
    """Interval containing target, else the closest one."""
    best, bd = None, math.inf
    for a, b in intervals:
        d = 0 if a <= target <= b else min(abs(a - target), abs(b - target))
        if d < bd:
            best, bd = (a, b), d
    return best


def pair_clearance(gs, left, right, kern, loc, step=5):
    """Smallest horizontal white gap between the ink of `left` and the ink
    of `right` when set side by side with `kern` units of kerning, scanning
    horizontal lines every `step` units.  Returns (gap, y_at_min)."""
    a, b = flatten(gs.shape(left, loc)), flatten(gs.shape(right, loc))
    shift = gs.advance(left, loc) + kern
    ys = [p[1] for poly in a + b for p in poly]
    best = (math.inf, None)
    y = math.floor(min(ys))
    while y <= max(ys):
        ia = ink_intervals(a, y + 0.5, 1, flattened=True)
        ib = ink_intervals(b, y + 0.5, 1, flattened=True)
        if ia and ib:
            g = ib[0][0] + shift - ia[-1][1]
            if g < best[0]:
                best = (g, y)
        y += step
    return best
