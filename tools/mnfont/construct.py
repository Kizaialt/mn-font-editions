"""Glyph constructors.

Every constructor works per *master location* (normalized), measuring the
font's own outlines at that location and building the new outline from
them, so the result interpolates like its neighbours.  A constructor
returns a `Built` record; `varglyph.py` turns it into glyf/gvar/hmtx/HVAR
data.

Methods (selected per glyph in the family JSON):
  component   new glyph = TrueType composite of an existing glyph
  barred_o    Cyrillic barred O: re-use an existing full-bar glyph (e.g. Latin
              U+019F/U+0275) if it checks out, else O + horizontal bar
  straight_u  Cyrillic straight u (U+04AF): the font's v whose outer arm edges
              run straight into a lowercase stem down to the descender
              (polygonal v only - kept for Unbounded MN)
  straight_u_p  same idea for any single-contour v (curved vertex, italic):
              stem width, depth and bottom terminal copied from p / р
  tugrik      tugrik sign: the font's T + two parallel diagonal strokes
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .outline import (GlyphSets, bounds, ink_intervals, line_y_at_x, loc_key,
                      nearest_interval, rect, round_shape, orientation_problems)


@dataclass
class Built:
    name: str
    kind: str                     # "simple" | "composite"
    metrics_base: str             # advance / HVAR / phantom points copied from here
    shapes: dict = field(default_factory=dict)       # loc_key -> rounded shape
    components: list = field(default_factory=list)   # [(glyphName, dx, dy)]
    overlap: bool = False
    notes: list = field(default_factory=list)
    measurements: dict = field(default_factory=dict)  # loc_key -> {label: value}
    tracks: list = None           # [base glyph, [[new point index, base point index], ...]] for verification


def _fmt_loc(loc):
    return ",".join(f"{k}={v:+.2f}" for k, v in sorted(loc.items())) or "default"


# --------------------------------------------------------------------------
# italic helpers: work in "deslanted" space (x' = x - k*y, k = tan(slant))
# --------------------------------------------------------------------------

def deslant(shape, k):
    if not k:
        return shape
    return [[(x - k * y, y, on) for x, y, on in c] for c in shape]


def reslant(contour, k):
    if not k:
        return contour
    return [(x + k * y, y, on) for x, y, on in contour]


# --------------------------------------------------------------------------
# measurements
# --------------------------------------------------------------------------

def measure_hbar(gs: GlyphSets, name, loc, k=0.0):
    """Horizontal crossbar of e.g. H / н: vertical ray through the glyph's
    horizontal centre; returns (bottom, top) of the ink run nearest the
    vertical centre.  k = italic slant (measured in deslanted space)."""
    shape = deslant(gs.shape(name, loc), k)
    x0, y0, x1, y1 = bounds(shape)
    iv = ink_intervals(shape, (x0 + x1) / 2, axis=0)
    return nearest_interval(iv, (y0 + y1) / 2)


def measure_descender_stem(gs: GlyphSets, name, loc):
    """Stem of e.g. p: horizontal ray half-way down the descender.
    Returns ((left, right), descender_y)."""
    shape = gs.shape(name, loc)
    x0, y0, x1, y1 = bounds(shape)
    if y0 >= 0:
        raise ValueError(f"{name} has no descender")
    iv = ink_intervals(shape, y0 / 2, axis=1)
    return iv[0], y0


def measure_t(gs: GlyphSets, name, loc, k=0.0):
    """T-like glyph: stem (left, right), crossbar (bottom, top), x extent
    (in deslanted space when k != 0)."""
    return measure_t_shape(deslant(gs.shape(name, loc), k))


def measure_t_shape(shape):
    x0, y0, x1, y1 = bounds(shape)
    iv = ink_intervals(shape, y0 + 0.25 * (y1 - y0), axis=1)
    stem = nearest_interval(iv, (x0 + x1) / 2)
    xm = (x0 + stem[0]) / 2
    bar_iv = ink_intervals(shape, xm, axis=0)
    bar = max(bar_iv, key=lambda ab: ab[1])
    return dict(stem=stem, bar=bar, x0=x0, x1=x1, y0=y0, y1=y1)


# --------------------------------------------------------------------------
# component
# --------------------------------------------------------------------------

def build_component(gs: GlyphSets, locs, name, spec):
    base = spec["base"]
    if base not in gs.font.getGlyphOrder():
        raise KeyError(f"{name}: component base {base} missing")
    b = Built(name, "composite", metrics_base=base, components=[(base, 0, 0)])
    b.notes.append(f"composite of '{base}' (offset 0,0)")
    return b


# --------------------------------------------------------------------------
# barred O
# --------------------------------------------------------------------------

def check_barred_candidate(gs, locs, cand, base, tol=2.0):
    """A candidate (e.g. Latin Ɵ) is acceptable for Cyrillic Ө if at every
    master it has the base's outline extent and advance, and a horizontal
    line through the optical centre crosses ONE continuous ink run from the
    left wall to the right wall (= bar joined to both walls)."""
    order = gs.font.getGlyphOrder()
    if cand not in order:
        return False, f"{cand} not in font"
    for loc in locs:
        bs, cs = gs.shape(base, loc), gs.shape(cand, loc)
        bb, cb = bounds(bs), bounds(cs)
        if any(abs(a - c) > tol for a, c in zip(bb, cb)):
            return False, f"{cand} extent differs from {base} at {_fmt_loc(loc)}"
        if abs(gs.advance(base, loc) - gs.advance(cand, loc)) > 0.5:
            return False, f"{cand} advance differs at {_fmt_loc(loc)}"
        cy = (bb[1] + bb[3]) / 2
        iv = ink_intervals(cs, cy, axis=1)
        biv = ink_intervals(bs, cy, axis=1)
        if len(iv) != 1 or abs(iv[0][0] - biv[0][0]) > tol or abs(iv[0][1] - biv[-1][1]) > tol:
            return False, (f"{cand} bar does not join both walls at {_fmt_loc(loc)} "
                           f"(ink runs at y={cy:.0f}: {[(round(a), round(b)) for a, b in iv]})")
    return True, "ok"


def construct_barred_o(gs, locs, name, spec):
    base, bar_ref = spec["base"], spec["bar_ref"]
    shift = spec.get("bar_shift", 0.0)  # fraction of height, + = up
    b = Built(name, "simple", metrics_base=base, overlap=True)
    for loc in locs:
        shape = gs.shape(base, loc)
        x0, y0, x1, y1 = bounds(shape)
        lo, hi = measure_hbar(gs, bar_ref, loc, spec.get("_slant", 0.0))
        t = hi - lo
        cy = (y0 + y1) / 2 + shift * (y1 - y0)
        # keep both half-counters open: each >= min_counter_ratio x bar thickness
        # (designers thin the bar at heavy weights; e.g. Unbounded Black Ɵ bar
        # is 174 vs H crossbar 228)
        vc = ink_intervals(shape, (x0 + x1) / 2, axis=0)
        if len(vc) >= 2:
            counter_h = vc[-1][0] - vc[0][1]
            r = spec.get("min_counter_ratio", 0.6)
            t = min(t, counter_h / (1 + 2 * r))
        yb, yt = cy - t / 2, cy + t / 2
        lefts, rights = [], []
        for y in (yb, cy, yt):
            iv = ink_intervals(shape, y, axis=1)
            if len(iv) < 2:
                raise ValueError(f"{name}: {base} has no counter at y={y:.0f}")
            lefts.append(iv[0])
            rights.append(iv[-1])
        # bar ends hidden in the middle of each wall over the whole bar band
        lo_l, hi_l = max(a for a, _ in lefts), min(b_ for _, b_ in lefts)
        lo_r, hi_r = max(a for a, _ in rights), min(b_ for _, b_ in rights)
        if lo_l >= hi_l or lo_r >= hi_r:
            raise ValueError(f"{name}: bar ends cannot be hidden in the walls of {base} at {_fmt_loc(loc)}")
        xl, xr = (lo_l + hi_l) / 2, (lo_r + hi_r) / 2
        bar = rect(xl, yb, xr, yt)
        b.shapes[loc_key(loc)] = round_shape([bar] + shape)
        b.measurements[loc_key(loc)] = dict(bar_thickness=round(t, 1), bar_center=round(cy, 1),
                                            bar_x=(round(xl), round(xr)))
    npts = sum(len(c) for c in gs.shape(base, {}))
    b.tracks = [base, [[4 + i, i] for i in range(npts)]]
    d = b.measurements[()]
    b.notes.append(f"'{base}' + bar from {bar_ref} crossbar: thickness {d['bar_thickness']}, "
                   f"centre y={d['bar_center']}, x {d['bar_x'][0]}..{d['bar_x'][1]} (default)")
    return b


def build_barred_o(gs, locs, name, spec):
    for cand in spec.get("prefer_component", []):
        ok, why = check_barred_candidate(gs, locs, cand, spec["base"])
        if ok:
            b = Built(name, "composite", metrics_base=cand, components=[(cand, 0, 0)])
            b.notes.append(f"composite of '{cand}': verified at every master to be "
                           f"'{spec['base']}' + a full-width bar joined to both walls")
            # cross-check the generic constructor against the designer's glyph
            try:
                ref = construct_barred_o(gs, locs, name, spec)
                cmp = []
                for loc in locs:
                    cs = gs.shape(cand, loc)
                    bar_iv = ink_intervals(cs, (bounds(cs)[0] + bounds(cs)[2]) / 2, axis=0)
                    m = ref.measurements[loc_key(loc)]
                    cmp.append(f"{_fmt_loc(loc)}: designer bar "
                               f"{[(round(a), round(c)) for a, c in bar_iv]} vs constructed "
                               f"centre {m['bar_center']} thick {m['bar_thickness']}")
                b.notes.append("cross-check (generic constructor vs designer glyph, vertical ray "
                               "through centre): " + " | ".join(cmp))
            except Exception as e:  # informative only
                b.notes.append(f"cross-check failed: {e}")
            return b
        b_note = f"candidate {cand} rejected: {why}"
        spec.setdefault("_rejected", []).append(b_note)
    b = construct_barred_o(gs, locs, name, spec)
    b.notes = spec.get("_rejected", []) + b.notes
    return b


# --------------------------------------------------------------------------
# straight u (U+04AF) from v
# --------------------------------------------------------------------------

def build_straight_u(gs, locs, name, spec):
    base, stem_ref = spec["base"], spec["stem_ref"]
    dshape = gs.shape(base, {})
    if len(dshape) != 1 or not all(p[2] for p in dshape[0]):
        raise ValueError(f"{name}: '{base}' must be a single straight-sided contour "
                         f"for method straight_u (got {len(dshape)} contours)")
    c0 = dshape[0]
    n = len(c0)
    ymin = min(p[1] for p in c0)
    run = [i for i, p in enumerate(c0) if p[1] <= ymin + 1.0]
    runset = set(run)
    start = next(i for i in run if (i - 1) % n not in runset)
    if any((start + k) % n not in runset for k in range(len(run))):
        raise ValueError(f"{name}: bottom points of '{base}' are not consecutive")
    # rotate only if the bottom run wraps around the contour start
    rot = start if (0 in runset and (n - 1) in runset) else 0
    b = Built(name, "simple", metrics_base=base, overlap=True)
    for loc in locs:
        c = gs.shape(base, loc)[0]
        c = c[rot:] + c[:rot] if rot else c
        idx = [(i - rot) % n for i in run]
        idx.sort()
        i0, i1 = idx[0], idx[-1]
        (sl, sr), desc = measure_descender_stem(gs, stem_ref, loc)
        if "descender" in spec:
            desc = spec["descender"]
        s = (sr - sl) * spec.get("stem_scale", 1.0)
        bx = [c[i][0] for i in idx]
        cx = (min(bx) + max(bx)) / 2
        prev, first, last, nxt = c[i0 - 1], c[i0], c[i1], c[(i1 + 1) % n]
        if first[0] >= last[0]:
            xf, xl_ = cx + s / 2, cx - s / 2
        else:
            xf, xl_ = cx - s / 2, cx + s / 2
        j1 = (xf, line_y_at_x(prev[:2], first[:2], xf))
        j2 = (xl_, line_y_at_x(last[:2], nxt[:2], xl_))
        crotch = min(p[1] for i, p in enumerate(c) if i not in idx and p[1] > ymin + 1)
        if not (desc + s / 4 < j1[1] < crotch and desc + s / 4 < j2[1] < crotch):
            raise ValueError(f"{name}: stem join out of range at {_fmt_loc(loc)} "
                             f"(join y {j1[1]:.0f}/{j2[1]:.0f}, crotch {crotch:.0f})")
        new = (c[:i0] + [(j1[0], j1[1], True), (xf, desc, True), (xl_, desc, True),
                         (j2[0], j2[1], True)] + c[i1 + 1:])
        b.shapes[loc_key(loc)] = round_shape([new])
        b.measurements[loc_key(loc)] = dict(stem=round(s, 1), stem_x=(round(min(xf, xl_)), round(max(xf, xl_))),
                                            join_y=round((j1[1] + j2[1]) / 2, 1), descender=round(desc, 1),
                                            v_bottom_width=round(max(bx) - min(bx), 1))
    nn = len(c0)
    pairs = [[i, i] for i in range(idx[0])] + [[i + 4 - len(idx), i] for i in range(idx[-1] + 1, nn)]
    b.tracks = [base, pairs] if not rot else None
    d = b.measurements[()]
    b.notes.append(f"'{base}' outline with its bottom replaced by a straight stem: stem width "
                   f"{d['stem']} (= '{stem_ref}' descender stem), x {d['stem_x'][0]}..{d['stem_x'][1]}, "
                   f"down to y={d['descender']} ('{stem_ref}' descender); outer arm edges extended "
                   f"to meet the stem at y={d['join_y']} ('{base}' bottom flat was {d['v_bottom_width']} wide)")
    return b


# --------------------------------------------------------------------------
# tugrik (U+20AE) from T
# --------------------------------------------------------------------------

def measure_internal_gaps(gs, refs, loc, k=0.0, min_gap=None):
    """Tightest white gap between two ink runs (a closed or semi-closed
    counter such as the space between the bars of ₸ € ¥ or the eye of e),
    measured on one vertical ray per reference glyph.  refs: list of
    {"glyph": name, "x": fraction of the glyph's ink width}."""
    out = {}
    order = set(gs.font.getGlyphOrder())
    if min_gap is None:      # ignore slivers where a ray grazes a curve
        min_gap = 0.02 * gs.font["head"].unitsPerEm
    for r in refs:
        g = r["glyph"]
        if g not in order:
            continue
        shape = deslant(gs.shape(g, loc), k)       # italic: rays along the slant
        x0, y0, x1, y1 = bounds(shape)
        iv = ink_intervals(shape, x0 + r["x"] * (x1 - x0), axis=0)
        gaps = [b[0] - a[1] for a, b in zip(iv, iv[1:]) if b[0] - a[1] >= min_gap]
        if gaps:
            out[g] = round(min(gaps), 1)
    return out


def _parse_loc(key):
    """'wght=1' / 'wght=+1.0,wdth=-1' -> loc_key tuple."""
    if key in ("default", ""):
        return ()
    d = {}
    for part in key.split(","):
        a, v = part.split("=")
        d[a.strip()] = float(v)
    return loc_key(d)


def _angle_search(p, avail, hs, reserve, t_target, t_min):
    """Walk the angle down from angle_deg to angle_min_deg until strokes of
    at least t_min fit in `avail` with `reserve` units of whitespace.
    Returns (angle, thickness) or (None, last_fit)."""
    a = p["angle_deg"]
    t_fit = 0.0
    while a >= p["angle_min_deg"] - 1e-9:
        th = math.radians(a)
        rh = hs * math.tan(th)
        t_fit = (avail - 2 * rh - reserve(a)) / 2 * math.cos(th)
        if t_fit >= t_target:
            return a, t_target
        if t_fit >= t_min:
            return a, t_fit
        a -= 0.25
    return None, t_fit


def build_tugrik(gs, locs, name, spec):
    """₮ = T + two parallel diagonal strokes (vertical end cuts) centred on
    the stem.

    Light/regular masters: target thickness / angle / span, whitespace split
    by `whitespace_split`.  Heaviest master (largest crossbar): the strokes
    yield to the whitespace instead - internal gaps (between the strokes,
    and under the crossbar) >= heavy_gap_factor x the family's own tightest
    internal gap (measured on `heavy_gap_refs`, e.g. the bars of ₸ € ¥ and
    the eye of e), bottom gap >= bottom_gap_ratio x that, and the stroke
    ends protrude >= min_protrusion x stem past the stem.
    `master_overrides` {"wght=1": {angle, thickness, x_span, gap_bottom,
    gap_between}} pins reviewed values for one master; the rule is still
    evaluated and a warning is logged if the pinned values break it."""
    base = spec["base"]
    p = dict(angle_deg=20.0, angle_min_deg=14.0, span=0.68, thickness_ratio=0.78,
             thickness_min_ratio=0.5, whitespace_ratio=1.0, whitespace_split=(0.25, 0.40, 0.35),
             min_protrusion=0.55, heavy_gap_factor=1.2, bottom_gap_ratio=0.45,
             heavy_gap_refs=[], heavy_rule=True)
    p.update({k: v for k, v in spec.items() if k in p})
    overrides = {_parse_loc(k): v for k, v in spec.get("master_overrides", {}).items()
                 if not k.startswith("_")}
    k_sl = spec.get("_slant", 0.0)      # italic: construct upright, then re-slant the strokes
    meas = {loc_key(l): measure_t(gs, base, l, k_sl) for l in locs}
    # absolute floor for the stroke thickness: the font's lightest crossbar
    # across masters (variable fonts), or an explicit "min_stroke" in units
    if "min_stroke" in spec:
        hairline = spec["min_stroke"]
    elif len(locs) > 1:
        hairline = min(m["bar"][1] - m["bar"][0] for m in meas.values())
    else:
        hairline = 0
    heaviest = max(meas, key=lambda k: meas[k]["bar"][1] - meas[k]["bar"][0])
    if len(locs) == 1 and not spec.get("static_is_heavy", False):
        heaviest = None   # a lone static master is "heavy" only if the family says so
    sb, sg, st = p["whitespace_split"]
    tot = sb + sg + st
    b = Built(name, "simple", metrics_base=base, overlap=True)
    for loc in locs:
        k = loc_key(loc)
        m = meas[k]
        shape = gs.shape(base, loc)
        sl, sr = m["stem"]
        cx, s = (sl + sr) / 2, sr - sl
        cb_lo, cb_hi = m["bar"]
        h = cb_hi - cb_lo
        L = m["x1"] - m["x0"]
        base_y = m["y0"]
        avail = cb_lo - base_y
        t_target = max(p["thickness_ratio"] * h, hairline)
        t_min = max(p["thickness_min_ratio"] * h, hairline)
        heavy = bool(p["heavy_rule"]) and k == heaviest
        extra, G = {}, 0.0
        if heavy:
            fam = measure_internal_gaps(gs, p["heavy_gap_refs"], loc, k_sl)
            if fam:
                G = p["heavy_gap_factor"] * min(fam.values())
            extra.update(family_gaps=fam, min_internal_gap=round(G, 1))
        if k in overrides:
            o = overrides[k]
            theta, t = o["angle"], o["thickness"]
            hs = o["x_span"] / 2
            th = math.radians(theta)
            vt, rh = t / math.cos(th), hs * math.tan(th)
            m_b, g = o["gap_bottom"], o["gap_between"]
            W = avail - 2 * vt - 2 * rh
            mode = "override"
        elif heavy:
            hs = max(p["span"] * L / 2, s / 2 + p["min_protrusion"] * s)
            hs = min(hs, 0.97 * L / 2)         # stay within the crossbar width
            reserve = (2 + p["bottom_gap_ratio"]) * G
            theta, t = _angle_search(p, avail, hs, lambda a: reserve, t_target, t_min)
            if theta is None:   # the whitespace rule wins over thickness_min_ratio
                theta = p["angle_min_deg"]
                th = math.radians(theta)
                t = (avail - 2 * hs * math.tan(th) - reserve) / 2 * math.cos(th)
                b.notes.append(f"note: heaviest-master strokes thinned to {t:.1f} "
                               f"({t / h:.2f} x crossbar) to keep internal gaps >= {G:.1f}")
            th = math.radians(theta)
            vt, rh = t / math.cos(th), hs * math.tan(th)
            W = avail - 2 * vt - 2 * rh
            spare = max(W - reserve, 0.0)
            m_b = p["bottom_gap_ratio"] * G + spare * sb / tot
            g = G + spare * sg / tot
            mode = "heavy rule"
        else:
            hs = p["span"] * L / 2
            wr = p["whitespace_ratio"]
            # whitespace reserve proportional to the stroke's vertical thickness
            a = p["angle_deg"]
            theta = t = None
            while a >= p["angle_min_deg"] - 1e-9:
                th = math.radians(a)
                rh = hs * math.tan(th)
                t_fit = (avail - 2 * rh) / (2 + wr) * math.cos(th)
                if t_fit >= t_target:
                    theta, t = a, t_target
                    break
                if t_fit >= t_min:
                    theta, t = a, t_fit
                    break
                a -= 0.25
            if theta is None:
                theta, t = p["angle_min_deg"], max(t_fit, 0.35 * h)
                b.notes.append(f"WARNING: tugrik strokes forced below thickness_min at {_fmt_loc(loc)}")
            th = math.radians(theta)
            vt, rh = t / math.cos(th), hs * math.tan(th)
            W = avail - 2 * vt - 2 * rh
            m_b, g = W * sb / tot, W * sg / tot
            mode = "solver"
        m_t = W - m_b - g
        yl = base_y + m_b + rh + vt / 2
        yu = yl + vt + g
        xa, xb = cx - hs, cx + hs
        strokes = []
        for yc in (yl, yu):
            strokes.append([(xa, yc - rh + vt / 2, True), (xb, yc + rh + vt / 2, True),
                            (xb, yc + rh - vt / 2, True), (xa, yc - rh - vt / 2, True)])
        if hs < s / 2 + 0.4 * s:
            b.notes.append(f"WARNING: strokes extend less than 0.4 stem past the stem at {_fmt_loc(loc)}")
        if heavy and G and min(g, m_t) < G - 0.5:
            b.notes.append(f"WARNING: heaviest-master internal gaps {g:.1f}/{m_t:.1f} below "
                           f"the rule minimum {G:.1f} at {_fmt_loc(loc)}")
        if min(m_b, g, m_t) < 0:
            raise ValueError(f"{name}: strokes do not fit at {_fmt_loc(loc)}")
        b.shapes[k] = round_shape(shape + [reslant(c, k_sl) for c in strokes])
        b.measurements[k] = dict(
            mode=mode, T_stem=(round(sl), round(sr)), T_crossbar=(round(cb_lo), round(cb_hi)),
            stroke_thickness=round(t, 1), thickness_ratio=round(t / h, 3), stroke_vertical=round(vt, 1),
            rise=round(2 * rh, 1), angle=round(theta, 2), stroke_x=(round(xa), round(xb)),
            protrusion=round(hs - s / 2, 1), lower_centre_y=round(yl, 1), upper_centre_y=round(yu, 1),
            gaps=(round(m_b, 1), round(g, 1), round(m_t, 1)), **extra)
    b.tracks = [base, [[i, i] for i in range(sum(len(c) for c in gs.shape(base, {})))]]
    d = b.measurements[()]
    b.notes.append(
        f"'{base}' outline + two parallel strokes (vertical end cuts) centred on the stem: "
        f"perpendicular thickness {d['stroke_thickness']} (= "
        f"{d['stroke_thickness'] / (d['T_crossbar'][1] - d['T_crossbar'][0]):.2f} x crossbar "
        f"{d['T_crossbar'][1] - d['T_crossbar'][0]}), angle {d['angle']} deg, x {d['stroke_x'][0]}..{d['stroke_x'][1]} "
        f"({p['span']:.0%} of the crossbar), centre lines cross the stem axis at y={d['lower_centre_y']} "
        f"and y={d['upper_centre_y']}; white gaps baseline/between/crossbar = {d['gaps']} (default)")
    if heaviest is not None and heaviest != ():
        hm = b.measurements[heaviest]
        b.notes.append(
            f"heaviest master ({','.join(f'{a}={v:+g}' for a, v in heaviest)}, {hm['mode']}): "
            f"thickness {hm['stroke_thickness']} ({hm['thickness_ratio']} x crossbar), {hm['angle']} deg, "
            f"x {hm['stroke_x'][0]}..{hm['stroke_x'][1]} (protrudes {hm['protrusion']} past the stem), "
            f"gaps {hm['gaps']}; family internal gaps {hm.get('family_gaps')} -> rule minimum "
            f"{hm.get('min_internal_gap')}")
        if hm["mode"] == "override":
            # what the generic rule alone would have produced (for future families)
            alt = dict(spec)
            alt.pop("master_overrides", None)
            try:
                ab = build_tugrik(gs, locs, name, alt)
                am = ab.measurements[heaviest]
                b.notes.append(f"  (generic heavy rule without the override would give: thickness "
                               f"{am['stroke_thickness']}, {am['angle']} deg, x {am['stroke_x'][0]}.."
                               f"{am['stroke_x'][1]}, gaps {am['gaps']})")
            except Exception as e:  # informative only
                b.notes.append(f"  (generic heavy rule failed: {e})")
    return b


# --------------------------------------------------------------------------
# straight u (U+04AF), general version: any single-contour v (curved
# vertex, ink traps, italic) + the font's own descender stem and terminal
# --------------------------------------------------------------------------

def _seg_len(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def _outer_edges(c, xh):
    """Indices (j0, j1) of the straight outer-edge segments next to the
    bottom of a v contour: walking backwards from the lowest on-curve point
    the first long straight segment is one outer edge (its lower end is
    c[j0]); walking forwards, the other (its lower end is c[j1])."""
    n = len(c)
    ys = [p[1] for p in c]
    bot = min((i for i in range(n) if c[i][2]), key=lambda i: ys[i])
    lmin = 0.25 * xh

    def straight(i, j):
        a, b = c[i % n], c[j % n]
        L = _seg_len(a, b)
        return a[2] and b[2] and L >= lmin and abs(b[1] - a[1]) >= 0.6 * L   # long, steep arm edge

    j0 = bot
    for _ in range(n):
        if straight(j0 - 1, j0):
            break
        j0 -= 1
    j1 = bot
    for _ in range(n):
        if straight(j1, j1 + 1):
            break
        j1 += 1
    return j0 % n, j1 % n, bot


def _p_terminal(c, y_split):
    """Stem contour of p: the two straight segments crossing y_split (right
    side going down, left side going up in TrueType clockwise order) and the
    run of points below them.  Returns (i_right_seg, i_left_seg, run_idx)."""
    n = len(c)
    cross = []
    for i in range(n):
        a, b = c[i], c[(i + 1) % n]
        if (a[1] - y_split) * (b[1] - y_split) < 0:
            cross.append(i)
    if len(cross) != 2:
        raise ValueError(f"stem contour crosses y={y_split:.0f} {len(cross)} times (expected 2)")
    for i in cross:
        if not (c[i][2] and c[(i + 1) % n][2]):
            raise ValueError("stem side is curved at the split height")
    # the crossing whose segment goes DOWN starts the run
    down = [i for i in cross if c[(i + 1) % n][1] < c[i][1]]
    up = [i for i in cross if c[(i + 1) % n][1] > c[i][1]]
    if len(down) != 1 or len(up) != 1:
        raise ValueError("unexpected stem contour direction")
    i_down, i_up = down[0], up[0]
    run, i = [], (i_down + 1) % n
    while i != (i_up + 1) % n:
        run.append(i)
        i = (i + 1) % n
    return i_down, i_up, run


def _x_at(a, b, y):
    return a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])


def build_straight_u_p(gs, locs, name, spec):
    """ү = the font's v + a straight stem with the font's own descender
    terminal (copied from p / Cyrillic р, same depth and end shape).

    mode "edges" (default when possible): v's two outer arm edges run
    straight on until they meet a stem of p's width; if that join would sit
    deeper than max_join_depth x |descender| (steep, heavy v's), the stem is
    widened so the join stays at that depth.
    mode "drop" (automatic fallback for curved-arm / cursive italic v's): the
    stem hangs straight down from v's own bottom corners (stem width = v's
    bottom width), p's terminal scaled to that width.
    Italic fonts are handled in deslanted space (spec['_slant']).
    Opt-in: "terminal": "flat" - for a p whose descender sides are curved
    (slightly tapered) the stem ends in a plain flat cut at p's depth, its
    width measured on p at the split height; "mode":
    "tangent" - for a v with CURVED arms and a flat two-point bottom: like
    "edges", but the arms are continued along their end tangents (the line
    from the last off-curve point to the bottom corner)."""
    base, stem_ref = spec["base"], spec["stem_ref"]
    k = spec.get("_slant", 0.0)
    split_frac = spec.get("split", 0.4)       # where the p stem is cut, fraction of its descender
    max_join = spec.get("max_join_depth", 0.25)
    mode = spec.get("mode", "auto")
    d0 = gs.shape(base, {})
    if len(d0) != 1:
        raise ValueError(f"{name}: '{base}' must be a single contour (got {len(d0)})")
    xh = bounds(d0)[3]
    c0 = deslant(d0, k)[0]
    n = len(c0)
    region = None
    if mode == "tangent":
        ymin = min(p[1] for p in c0 if p[2])
        low = [i for i, p in enumerate(c0) if p[2] and p[1] <= ymin + 1.0]
        if len(low) != 2 or (low[1] - low[0]) % n not in (1, n - 1):
            raise ValueError(f"{name}: '{base}' has no flat two-point bottom for tangent mode")
        j0, j1 = (low[0], low[1]) if (low[1] - low[0]) % n == 1 else (low[1], low[0])
        region = [j0, j1]
    elif mode in ("auto", "edges"):
        j0, j1, bot = _outer_edges(c0, xh)
        region = []
        i = j0
        while True:
            region.append(i)
            if i == j1:
                break
            i = (i + 1) % n
        if len(region) > n // 2 or len(region) > 8:
            if mode == "edges":
                raise ValueError(f"{name}: could not isolate the bottom of '{base}'")
            region = None
    if region is None:      # "drop" mode: the two lowest on-curve points must be consecutive
        ymin = min(p[1] for p in c0 if p[2])
        low = [i for i, p in enumerate(c0) if p[2] and p[1] <= ymin + 1.0]
        if len(low) != 2 or (low[1] - low[0]) % n not in (1, n - 1):
            raise ValueError(f"{name}: '{base}' has no flat two-point bottom for drop mode")
        i_r, i_l = (low[0], low[1]) if (low[1] - low[0]) % n == 1 else (low[1], low[0])
        mode_used = "drop"
    else:
        mode_used = "edges"
    ps0 = deslant(gs.shape(stem_ref, {}), k)
    ci = min(range(len(ps0)), key=lambda q: min(p[1] for p in ps0[q]))
    desc0 = min(p[1] for p in ps0[ci])
    flat = spec.get("terminal") == "flat"
    if not flat:
        i_down, i_up, run = _p_terminal(ps0[ci], split_frac * desc0)
    b = Built(name, "simple", metrics_base=base, overlap=True)
    for loc in locs:
        orig = gs.shape(base, loc)[0]
        c = deslant([orig], k)[0]
        pc = deslant(gs.shape(stem_ref, loc), k)[ci]
        desc = min(p[1] for p in pc)
        ys = split_frac * desc
        m = len(pc)
        if flat:
            xl, xr = max(ink_intervals([pc], ys, axis=1), key=lambda ab: ab[1] - ab[0])
        else:
            xr = _x_at(pc[i_down], pc[(i_down + 1) % m], ys)
            xl = _x_at(pc[i_up], pc[(i_up + 1) % m], ys)
        if xr < xl:
            raise ValueError(f"{name}: stem sides of '{stem_ref}' are reversed")
        pcx, pw = (xr + xl) / 2, xr - xl
        widened = False
        if mode_used == "edges":
            # right edge comes INTO the bottom (j0-1 -> j0), left edge leaves it (j1 -> j1+1)
            ea, eb = c[(j0 - 1) % n], c[j0]
            fa, fb = c[j1], c[(j1 + 1) % n]
            if _x_at(ea, eb, 0) < _x_at(fa, fb, 0):
                raise ValueError(f"{name}: '{base}' contour is counter-clockwise")
            cx = (_x_at(ea, eb, 0) + _x_at(fa, fb, 0)) / 2
            sr, sl = cx + pw / 2, cx - pw / 2
            jr = (sr, _y_on(ea, eb, sr))
            jl = (sl, _y_on(fa, fb, sl))
            y_lim = -max_join * abs(desc)
            if min(jr[1], jl[1]) < y_lim:
                sr, sl = _x_at(ea, eb, y_lim), _x_at(fa, fb, y_lim)
                jr, jl = (sr, y_lim), (sl, y_lim)
                widened = True
            crotch = min(p[1] for idx, p in enumerate(c) if idx not in region and p[1] > 1)
            if not (ys < jr[1] < crotch and ys < jl[1] < crotch):
                raise ValueError(f"{name}: stem join out of range at {_fmt_loc(loc)} "
                                 f"(join y {jr[1]:.0f}/{jl[1]:.0f}, split {ys:.0f}, crotch {crotch:.0f})")
            head, tail = [(jr[0], jr[1], True)], [(jl[0], jl[1], True)]
            keep_after = []
            q = (j1 + 1) % n
            while q != j0:
                keep_after.append(q)
                q = (q + 1) % n
            join_y = (jr[1] + jl[1]) / 2
        else:
            sr, sl = c[i_r][0], c[i_l][0]
            if sr <= sl:
                raise ValueError(f"{name}: unexpected bottom order in '{base}'")
            head, tail = [], []
            keep_seq, q = [], i_l          # bottom-left ... around ... bottom-right (cyclic)
            while True:
                keep_seq.append(q)
                if q == i_r:
                    break
                q = (q + 1) % n
            join_y = 0.0
        w = sr - sl
        cx_new, sc = (sr + sl) / 2, w / pw
        if flat:
            mid = [(sr, desc, True), (sl, desc, True)]
        else:
            mid = [(sr, ys, True)] + [(cx_new + (pc[q][0] - pcx) * sc, pc[q][1], pc[q][2]) for q in run] + \
                  [(sl, ys, True)]
        new_pts = reslant(head + mid + tail, k)
        if mode_used == "edges":
            contour = new_pts + [orig[q] for q in keep_after]
            tracks = [[len(new_pts) + t, q] for t, q in enumerate(keep_after)]
        else:
            contour = [orig[q] for q in keep_seq] + new_pts
            tracks = [[t, q] for t, q in enumerate(keep_seq)]
        b.shapes[loc_key(loc)] = round_shape([contour])
        b.tracks = [base, tracks]
        b.measurements[loc_key(loc)] = dict(
            mode=mode_used, stem=round(w, 1), p_stem=round(pw, 1), widened=widened,
            stem_x=(round(sl), round(sr)), join_y=round(join_y, 1), descender=round(desc, 1),
            split_y=round(ys, 1))
    d = b.measurements[()]
    if mode_used == "edges":
        how = (f"outer arm edges {'(curved: continued along their end tangents)' if mode == 'tangent' else 'extended'} to meet a stem of '{stem_ref}''s width at y={d['join_y']}"
               + ("; stem widened where the join would sit deeper than "
                  f"{max_join:g} x descender" if any(m['widened'] for m in b.measurements.values()) else ""))
    else:
        how = "stem hangs straight down from the v's own bottom corners (curved arms)"
    if flat:
        how += f"; flat end cut at '{stem_ref}''s depth (its descender sides are curved, so no terminal is copied)"
    b.notes.append(f"'{base}' outline with a straight stem and '{stem_ref}''s terminal: stem width {d['stem']} "
                   f"('{stem_ref}' {d['p_stem']}, deslanted), down to y={d['descender']}; {how}"
                   + (f"; italic slant {math.degrees(math.atan(k)):.1f} deg" if k else ""))
    return b


def _y_on(a, b, x):
    return b[1] + (x - b[0]) * (a[1] - b[1]) / (a[0] - b[0])


BUILDERS = {
    "component": build_component,
    "barred_o": build_barred_o,
    "straight_u": build_straight_u,
    "straight_u_p": build_straight_u_p,
    "tugrik": build_tugrik,
}


def build_glyph(gs, locs, name, spec):
    method = spec["method"]
    b = BUILDERS[method](gs, locs, name, dict(spec))
    if b.tracks and getattr(gs, "normalize_direction", False):
        # tracked point indices refer to the direction-normalized base: map them to the font's own order
        pm = gs.point_map(b.tracks[0])
        b.tracks = [b.tracks[0], [[i, pm[j]] for i, j in b.tracks[1]]]
    if b.kind == "simple":
        # sanity: identical structure at every master, outer contours clockwise
        ref = b.shapes[()]
        for k, sh in b.shapes.items():
            if [len(c) for c in sh] != [len(c) for c in ref] or \
               [[p[2] for p in c] for c in sh] != [[p[2] for p in c] for c in ref]:
                raise ValueError(f"{name}: incompatible outlines between masters ({k})")
        for k, sh in b.shapes.items():
            bad = orientation_problems(sh)
            if bad:
                raise ValueError(f"{name}: contours {bad} have the wrong direction at {k}")
    return b
