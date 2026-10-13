"""Insert constructed glyphs into a (variable) TrueType font:
glyf + hmtx + gvar (incl. phantom points) + HVAR + cmap + GDEF class."""
from __future__ import annotations

from fontTools.pens.ttGlyphPen import TTGlyphPointPen
from fontTools.misc.roundTools import otRound
from fontTools.ttLib.tables._g_l_y_f import (Glyph, GlyphComponent, GlyphCoordinates,
                                             flagOverlapSimple, ROUND_XY_TO_GRID,
                                             USE_MY_METRICS, ARGS_ARE_XY_VALUES)
from fontTools.ttLib.tables.TupleVariation import TupleVariation
from fontTools.varLib.models import VariationModel

from .outline import full_coords, loc_key


def _simple_glyph(shape, overlap):
    pen = TTGlyphPointPen(None)
    for contour in shape:
        pen.beginPath()
        for x, y, on in contour:
            pen.addPoint((x, y), "line" if on else None)
        pen.endPath()
    g = pen.glyph()
    if overlap and g.numberOfContours > 0:
        g.flags[0] |= flagOverlapSimple
    return g


def _composite_glyph(font, components, metrics_base):
    g = Glyph()
    g.numberOfContours = -1
    g.components = []
    for name, dx, dy in components:
        c = GlyphComponent()
        c.glyphName = name
        c.x, c.y = dx, dy
        c.flags = ROUND_XY_TO_GRID | ARGS_ARE_XY_VALUES
        if name == metrics_base:
            c.flags |= USE_MY_METRICS
        g.components.append(c)
    return g


def _phantoms(font, base, loc):
    return list(full_coords(font, base, loc))[-4:]


def add_glyph(font, built, masters, axis_order):
    """Add a `Built` glyph (see construct.py) to `font` in place."""
    name = built.name
    glyf, hmtx = font["glyf"], font["hmtx"]
    order = font.getGlyphOrder()
    if name in order:
        raise ValueError(f"glyph {name} already exists")
    base = built.metrics_base
    adv = hmtx[base][0]

    if built.kind == "simple":
        glyph = _simple_glyph(built.shapes[()], built.overlap)
    else:
        glyph = _composite_glyph(font, built.components, base)

    new_order = order + [name]
    font.setGlyphOrder(new_order)
    glyf.glyphOrder = new_order
    glyf.glyphs[name] = glyph
    glyph.recalcBounds(glyf)

    base_pp = {loc_key(l): _phantoms(font, base, l) for l in masters}
    pp1x = base_pp[()][0][0]          # = xMin - lsb of the metrics base (normally 0)
    xmin = getattr(glyph, "xMin", 0)
    hmtx[name] = (adv, otRound(xmin - pp1x))

    # ---- gvar --------------------------------------------------------------
    if "gvar" in font:
        values = []
        for loc in masters:
            k = loc_key(loc)
            if built.kind == "simple":
                pts = [(x, y) for c in built.shapes[k] for x, y, _ in c]
            else:
                pts = [(dx, dy) for _, dx, dy in built.components]
            values.append(GlyphCoordinates(pts + base_pp[k]))
        model = VariationModel(masters, axisOrder=axis_order)
        deltas = model.getDeltas(values)
        tvs = []
        for support, delta in zip(model.supports[1:], deltas[1:]):
            coords = [(otRound(x), otRound(y)) for x, y in delta]
            if any(c != (0, 0) for c in coords):
                tvs.append(TupleVariation(dict(support), coords))
        font["gvar"].variations[name] = tvs

    # ---- HVAR / VVAR -------------------------------------------------------
    if "HVAR" in font:
        hv = font["HVAR"].table
        if hv.AdvWidthMap is None:
            # implicit mapping: glyph ID = inner index into VarData[0]
            vd = hv.VarStore.VarData[0]
            gid_new = len(new_order) - 1
            if len(vd.Item) != gid_new:
                raise NotImplementedError(f"HVAR implicit mapping has {len(vd.Item)} rows for {gid_new} glyphs")
            vd.Item.append(list(vd.Item[font.getGlyphID(base)]))
            vd.ItemCount = len(vd.Item)
        for attr in ("AdvWidthMap", "LsbMap", "RsbMap"):
            m = getattr(hv, attr)
            if m is not None:
                m.mapping[name] = m.mapping[base]
    if "vmtx" in font:
        # vertical metrics (fonts with vhea/vmtx, e.g. CJK-capable families): same advance
        # height as the base; top side bearing shifts with yMax so the vertical origin is the same
        vadv, vtsb = font["vmtx"].metrics[base]
        ymax_base = getattr(glyf[base], "yMax", None)
        ymax_new = getattr(glyph, "yMax", None)
        shift = (ymax_base - ymax_new) if (ymax_base is not None and ymax_new is not None) else 0
        font["vmtx"].metrics[name] = (vadv, otRound(vtsb + shift))
    if "VVAR" in font:
        vv = font["VVAR"].table
        if vv.AdvHeightMap is None:
            vd = vv.VarStore.VarData[0]
            gid_new = len(new_order) - 1
            if len(vd.Item) != gid_new:
                raise NotImplementedError(f"VVAR implicit mapping has {len(vd.Item)} rows for {gid_new} glyphs")
            vd.Item.append(list(vd.Item[font.getGlyphID(base)]))
            vd.ItemCount = len(vd.Item)
        for attr in ("AdvHeightMap", "TsbMap", "BsbMap", "VOrgMap"):
            m = getattr(vv, attr)
            if m is not None:
                m.mapping[name] = m.mapping[base]

    # ---- GDEF glyph class --------------------------------------------------
    if "GDEF" in font and font["GDEF"].table.GlyphClassDef is not None:
        font["GDEF"].table.GlyphClassDef.classDefs[name] = 1
    return glyph


def map_unicode(font, name, codepoint):
    for st in font["cmap"].tables:
        if st.isUnicode() and (codepoint <= 0xFFFF or st.format in (12, 13)):
            st.cmap[codepoint] = name
