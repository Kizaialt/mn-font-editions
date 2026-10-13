#!/usr/bin/env python3
"""Render PNG proofs for an MN edition (HarfBuzz-shaped, so kerning and
weight-range glyph swaps are shown exactly as in apps).

    python tools/proof_mn.py tools/families/unbounded.json [--tag v1] [--compare old.ttf]

New glyphs are drawn in blue, existing glyphs in near-black.  Families
with several fonts (roman + italic) get one proof set per font:
proofs/<family>-<tag>-*.png for the first font, <family>-<tag>-<style>-*.png
for the others.  Weights come from each font's wght axis (min / 400 / 700 /
max when available); static fonts are proofed at their only weight.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.pens.recordingPen import DecomposingRecordingPointPen  # noqa: E402
from mnfont.render import HBFont, Page  # noqa: E402

PAIRS = "О Ө  о ө  Y Ү  v ү у  Т ₮"
WORDS = ["Өндөр Үүлс хөх тэнгэрт хөвнө",
         "ӨНДӨР ҮҮЛС ХӨХ ТЭНГЭР",
         "₮25 000 · Монгол Улс · Өглөө · Үүр"]
PARA = ("Монгол Улсын нийслэл Улаанбаатар хотод өглөө үүр цайхад хөх тэнгэрт үүл хөвнө. "
        "Үнэ 12 500₮, хөнгөлөлттэй үнэ 9 900₮. Өвөл, үхэр, өнгө, түүх, бүтээл, Өлгий, Үнэгүй.")
GUIDE = "ӨОөоҮYүvур₮Т"
KERN = ["АҮА ГҮГ ТҮТ ЛҮЛ ДҮД ХҮХ Ү. «Ү» ЬҮ ҮӨҮ",
        "АУА ГУГ ТУТ ЛУЛ ДУД ХУХ У. «У» ЬУ УОУ",
        "аүа гүг түт рүр лүл фүф ү. Тү Гү үө өү",
        "ауа гуг тут рур лул фуф у. Ту Гу уо оу",
        "ТӨТ АӨА ХӨХ төт хөх Гө Тө Ө. ₮1 ₮4 ₮7 10₮",
        "ТОТ АОА ХОХ тот хох Го То О. Т1 Т4 Т7 10Т"]


class Ctx:
    """Weights to proof for one font."""

    def __init__(self, font):
        self.static = "fvar" not in font
        if self.static:
            w = font["OS/2"].usWeightClass
            self.w_min = self.w_reg = self.w_bold = self.w_max = None
            self.all = [None]
            self.label_w = w
            return
        ax = next(a for a in font["fvar"].axes if a.axisTag == "wght")
        self.w_min, self.w_max = ax.minValue, ax.maxValue
        inside = lambda w: ax.minValue <= w <= ax.maxValue  # noqa: E731
        self.w_reg = 400 if inside(400) else ax.defaultValue
        self.w_bold = 700 if inside(700) else ax.maxValue
        self.all = sorted({self.w_min, self.w_reg, self.w_bold, self.w_max})
        self.label_w = None

    def label(self, w):
        return f"static (usWeightClass {self.label_w})" if w is None else f"wght {w:g}"

    def interp_steps(self):
        if self.static:
            return [None]
        n = 14
        return sorted({round(self.w_min + (self.w_max - self.w_min) * i / n) for i in range(n + 1)})


def wname(w):
    return {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium",
            600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}.get(w, "")


def proof_pairs(hbf, hl, out, title, ctx):
    size, row = 118, 190
    ws = ctx.all
    pg = Page(1900, 70 + row * len(ws))
    pg.label((24, 18), f"{title} - new glyph (blue) beside its base", 22, (60, 60, 60))
    for i, w in enumerate(ws):
        hbf.set_wght(w)
        base = 70 + row * i + 150
        pg.label((24, base - 160), f"{ctx.label(w)} {('(' + wname(w) + ')') if w and wname(w) else ''}", 17)
        pg.text(hbf, PAIRS, 24, base, size, highlight=hl)
    pg.save(out)


def proof_words(hbf, hl, out, title, ctx):
    size, lh = 50, 72
    ws = ctx.all
    blk = 40 + lh * len(WORDS) + 20
    pg = Page(1700, 70 + blk * len(ws) + 330)
    pg.label((24, 18), f"{title} - words (HarfBuzz shaping, GPOS kerning on)", 22, (60, 60, 60))
    y = 70
    for w in ws:
        hbf.set_wght(w)
        pg.label((24, y), ctx.label(w), 17)
        for j, line in enumerate(WORDS):
            pg.text(hbf, line, 24, y + 30 + lh * (j + 1) - 12, size, highlight=hl)
        y += blk
    rw = [ctx.w_reg, ctx.w_bold] if not ctx.static else [None]
    pg.label((24, y), "running text 20 px, " + " / ".join(ctx.label(w) for w in rw), 17)
    for k, w in enumerate(rw):
        hbf.set_wght(w)
        words, line, lines = PARA.split(" "), "", []
        for wd in words:
            t = (line + " " + wd).strip()
            if pg.measure(hbf, t, 20) > 1640:
                lines.append(line)
                line = wd
            else:
                line = t
        lines.append(line)
        for j, ln in enumerate(lines):
            pg.text(hbf, ln, 24, y + 52 + k * 130 + j * 32, 20, highlight=hl)
    pg.save(out)


def proof_guides(hbf, hl, out, title, ctx):
    size, row = 150, 300
    ws = [None] if ctx.static else sorted({ctx.w_min, ctx.w_reg, ctx.w_max})
    pg = Page(1950, 60 + row * len(ws))
    pg.label((24, 16), f"{title} - metrics: baseline / x-height / cap-height / descender (p)", 22, (60, 60, 60))
    for i, w in enumerate(ws):
        hbf.set_wght(w)
        sc = size / hbf.upem
        base = 60 + row * i + 215
        ext = {c: hbf.extents(hbf.gid(c)) for c in "xHp"}
        xh = ext["x"].y_bearing
        cap = ext["H"].y_bearing
        desc = ext["p"].y_bearing + ext["p"].height
        x0 = 150
        wtxt = pg.measure(hbf, GUIDE, size)
        for val, lab, col in ((0, "baseline 0", (225, 120, 120)), (xh, f"x {xh}", (120, 170, 120)),
                              (cap, f"cap {cap}", (120, 140, 210)), (desc, f"desc {desc}", (200, 150, 90))):
            y = base - val * sc
            pg.hline(y, x0 - 10, x0 + wtxt + 10, fill=col, width=1)
            pg.label((10, y - 12), lab, 15, col)
        pg.label((10, base - 205), ctx.label(w), 17, (60, 60, 60))
        pg.text(hbf, GUIDE, x0, base, size, highlight=hl, color=(24, 24, 24, ))
    pg.save(out)


def proof_interp(hbf, hl, out, title, ctx):
    steps = ctx.interp_steps()
    size, lh = 52, 66
    pg = Page(1500, 60 + lh * len(steps) + 10)
    pg.label((24, 16), f"{title} - interpolation across the weight axis", 22, (60, 60, 60))
    for i, w in enumerate(steps):
        hbf.set_wght(w)
        y = 60 + lh * (i + 1) - 10
        pg.label((24, y - 32), "" if w is None else f"{w:g}", 16)
        pg.text(hbf, "ӨөҮү₮ ОоYvуТ ӨНДӨР үүр ₮100", 100, y, size, highlight=hl)
    pg.save(out)


def proof_kerning(hbf, hl, out, title, ctx):
    size, lh = 46, 66
    ws = [None] if ctx.static else sorted({ctx.w_reg, ctx.w_max})
    blk = 36 + lh * len(KERN) + 16
    pg = Page(1700, 60 + blk * len(ws))
    pg.label((24, 16), f"{title} - kerning: new glyph lines vs. the base glyph they inherit from", 22, (60, 60, 60))
    y = 60
    for w in ws:
        hbf.set_wght(w)
        pg.label((24, y), ctx.label(w), 17)
        for j, line in enumerate(KERN):
            pg.text(hbf, line, 24, y + 22 + lh * (j + 1) - 14, size, highlight=hl,
                    color=(24, 24, 24) if j % 2 == 0 else (120, 120, 120))
        y += blk
    pg.save(out)


def _kadj(hbf, text):
    infos, poss = hbf.shape(text)
    return poss[0].x_advance - hbf.font.get_glyph_h_advance(infos[0].codepoint)


def proof_lookalike_kerning(hbf, hl, out, title, spec, ctx, compare=None):
    """Kerning sheet for a look-alike-kerned glyph (Ү) vs its Latin twin."""
    la = spec["kern_lookalike"]
    ch = chr(int(spec["unicode"], 16))
    twin_ch = chr(next(c for c, g in TTFont(hbf.path).getBestCmap().items() if g == la["latin_twin"]))
    keep_l = set(la.get("keep_fallback", {}).get("as_left", []))
    keep_r = set(la.get("keep_fallback", {}).get("as_right", []))
    lefts = [p for p in la["map"] if p not in keep_l]
    rights = [p for p in la["map"] if p not in keep_r]
    cyr = [ch + p for p in lefts] + [p + ch for p in rights]
    lat = [twin_ch + la["map"][p] for p in lefts] + [la["map"][p] + twin_ch for p in rights]
    keep = [ch + p for p in keep_l] + [p + ch for p in keep_r]
    words = "Үүр Үнэ Үе Үхэр Үд Үйл · АҮ «Үнэ» ҮНЭ ӨҮ"
    ws = [None] if ctx.static else sorted({ctx.w_reg, ctx.w_max})
    size, lh = 44, 62
    cols = 13
    chunks = [list(range(i, min(i + cols, len(cyr)))) for i in range(0, len(cyr), cols)]
    rows_per_w = len(chunks) * (3 if compare else 2) + 1
    tbl_h = 34 + 22 * (len(cyr) + len(keep)) // 3 + 40
    pg = Page(1950, 70 + len(ws) * (40 + rows_per_w * lh) + tbl_h + 40)
    pg.label((24, 16), f"{title} - {ch} kerning: blue = {ch} pairs, grey = Latin {twin_ch} twins"
             + (", light = previous build" if compare else ""), 22, (60, 60, 60))
    y = 70
    for w in ws:
        hbf.set_wght(w)
        if compare:
            compare.set_wght(w)
        pg.label((24, y), ctx.label(w), 17)
        y += 30
        for ck in chunks:
            y += lh
            pg.text(hbf, "  ".join(cyr[i] for i in ck), 24, y, size, highlight=hl)
            y += lh
            pg.text(hbf, "  ".join(lat[i] for i in ck), 24, y, size, color=(135, 135, 135))
            if compare:
                y += lh
                pg.text(compare, "  ".join(cyr[i] for i in ck), 24, y, size, color=(185, 195, 225),
                        highlight=None)
        y += lh
        pg.text(hbf, words, 24, y, size, highlight=hl)
        y += 26
    y += 20
    wl = " / ".join(ctx.label(w) for w in ws)
    pg.label((24, y), f"first-glyph kerning (units) at {wl}:  {ch}-pair  |  Latin twin"
             + ("  |  previous build" if compare else "") + "   (* = kept on the fallback values by review)", 17,
             (60, 60, 60))
    y += 30
    items = list(zip(cyr, lat)) + [(k, None) for k in keep]
    colw = 640
    for i, (c, l) in enumerate(items):
        vals = []
        for w in ws:
            hbf.set_wght(w)
            a = _kadj(hbf, c)
            b = _kadj(hbf, l) if l else None
            p = None
            if compare:
                compare.set_wght(w)
                p = _kadj(compare, c)
            vals.append((a, b, p))
        txt = (f"{c}{'*' if l is None else ''}  " + "/".join(str(v[0]) for v in vals)
               + (f"  |  {l} " + "/".join(str(v[1]) for v in vals) if l else "")
               + ("  |  " + "/".join(str(v[2]) for v in vals) if compare else ""))
        pg.label((24 + (i % 3) * colw, y + (i // 3) * 22), txt, 16, (40, 40, 40))
    pg.save(out)


def _shape_at(f, name, wght):
    gs = f.getGlyphSet(location={"wght": wght}) if wght is not None else f.getGlyphSet()
    pen = DecomposingRecordingPointPen(gs)
    gs[name].drawPoints(pen)
    cs, cur = [], None
    for op, args, kw in pen.value:
        if op == "beginPath":
            cur = []
        elif op == "addPoint":
            cur.append((args[0][0], args[0][1], args[1] is not None))
        elif op == "endPath":
            cs.append(cur)
    return cs


def tugrik_geometry(f, gname, base, wght, k=0.0):
    """Measured ₮ stroke geometry at a user weight, in deslanted space."""
    from mnfont.construct import measure_t_shape, deslant
    sh = deslant(_shape_at(f, gname, wght), k)
    pts = [p for c in sh for p in c]
    lo, up = pts[-8:-4], pts[-4:]
    m = measure_t_shape(deslant(_shape_at(f, base, wght), k))
    xa, xb = lo[0][0], lo[1][0]
    vt = lo[0][1] - lo[3][1]
    rise = lo[1][1] - lo[0][1]
    ang = math.degrees(math.atan2(rise, xb - xa))
    bar_lo = m["bar"][0]
    return dict(x=(round(xa, 1), round(xb, 1)), span=round(xb - xa, 1),
                thickness=vt * math.cos(math.radians(ang)), angle=ang,
                stem=m["stem"], crossbar=m["bar"], protrusion=round(m["stem"][0] - xa, 1),
                gaps=(round(lo[3][1], 1), round(up[3][1] - lo[0][1], 1), round(bar_lo - up[1][1], 1)))


def _norm(f, w):
    from fontTools.varLib.models import normalizeLocation, piecewiseLinearMap
    if w is None or "fvar" not in f:
        return {}
    axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in f["fvar"].axes}
    n = normalizeLocation({"wght": w}, axes)
    if "avar" in f and "wght" in f["avar"].segments:
        n = {"wght": piecewiseLinearMap(n["wght"], f["avar"].segments["wght"])}
    return {k: v for k, v in n.items() if v}


def proof_tugrik_gaps(hbf, hl, out, title, spec, ctx, slant):
    """Table of ₮ geometry per weight + the heavy-master whitespace rule,
    and the heaviest ₮ beside the font's own double-stroke signs."""
    from mnfont.construct import measure_internal_gaps
    from mnfont.outline import GlyphSets
    b = spec["build"]
    gname = None
    f = TTFont(hbf.path)
    gname = f.getBestCmap()[int(spec["unicode"], 16)]
    ws = [None] if ctx.static else sorted({ctx.w_min, ctx.w_reg, ctx.w_max})
    pg = Page(1900, 1060)
    pg.label((24, 16), f"{title} - ₮ geometry (measured from the built font, deslanted)", 22, (60, 60, 60))
    hdr = ["weight", "thickness", "x crossbar", "angle", "stroke x", "span", "protrudes", "gaps bottom / between / under bar"]
    xs = [24, 140, 300, 470, 580, 760, 870, 1010]
    y = 64
    for x, h in zip(xs, hdr):
        pg.label((x, y), h, 17, (60, 60, 60))
    for w in ws:
        y += 32
        g = tugrik_geometry(f, gname, b["base"], w, slant)
        cb = g["crossbar"][1] - g["crossbar"][0]
        row = ["static" if w is None else f"{w:g}", f"{g['thickness']:.1f}", f"{g['thickness'] / cb:.2f} x {cb:.0f}",
               f"{g['angle']:.1f}°", f"{g['x'][0]:g}..{g['x'][1]:g}", f"{g['span']:g}", f"{g['protrusion']:g}",
               " / ".join(f"{v:g}" for v in g["gaps"])]
        for x, t in zip(xs, row):
            pg.label((x, y), t, 17, (30, 30, 30))
    if not ctx.static:
        gs = GlyphSets(f)
        fam = measure_internal_gaps(gs, b.get("heavy_gap_refs", []), _norm(f, ctx.w_max), slant)
        if fam:
            G = b.get("heavy_gap_factor", 1.2) * min(fam.values())
            y += 44
            pg.label((24, y), f"heavy-master rule: internal gaps (between strokes, under crossbar) >= "
                     f"{b.get('heavy_gap_factor', 1.2)} x the family's tightest internal gap at wght {ctx.w_max:g}: "
                     + ", ".join(f"{k} {v:g}" for k, v in fam.items()) + f"  ->  min {G:.1f}", 17, (40, 70, 200))
    hbf.set_wght(ctx.w_max)
    y += 300
    x = 24
    x += pg.text(hbf, "₮", x, y, 260, highlight=hl) + 40
    for s in ("₸", "Ŧ", "¥", "€", "e"):
        x += pg.text(hbf, s, x, y, 260, color=(24, 24, 24)) + 30
    y += 150
    pg.text(hbf, "25 000₮  ₮25 000  12 500₮", 24, y, 86, highlight=hl)
    y += 70
    pg.text(hbf, "Үнэ 12 500₮ · 25 000₮ · ₮100", 24, y, 20, highlight=hl)
    hbf.set_wght(ctx.w_reg)
    pg.text(hbf, "Үнэ 12 500₮ · 25 000₮ · ₮100", 600, y, 20, highlight=hl)
    pg.label((24, y + 14), f"20 px at {ctx.label(ctx.w_max)} and {ctx.label(ctx.w_reg)}", 15)
    pg.save(out)


def proof_tugrik_digits(hbf, hl, out, title, spec, ctx):
    """Digit / punctuation + ₮ clearance sheet with measured gaps."""
    from mnfont.outline import GlyphSets, pair_clearance
    src = spec["kern_like"]["glyph"]
    f = TTFont(hbf.path)
    cm = f.getBestCmap()
    gname = cm[int(spec["unicode"], 16)]
    tch, ch = chr(next(c for c, g in cm.items() if g == src)), chr(int(spec["unicode"], 16))
    gs = GlyphSets(f)
    ws = ctx.all
    size, lh = 64, 84
    pg = Page(1950, 80 + len(ws) * (4 * lh + 40) + 300)
    pg.label((24, 16), f"{title} - digits/punctuation beside ₮ (blue), with Latin {tch} pairs (grey) for reference",
             22, (60, 60, 60))
    y = 70
    lines = [" ".join(d + ch for d in "0123456789"), " ".join(ch + d for d in "0123456789"),
             f"{ch}. {ch}, {ch}- -{ch} {ch}: «{ch}» ({ch}) 25 000{ch} {ch}100",
             " ".join(tch + d for d in "0123456789") + "   " + " ".join(d + tch for d in "0469")]
    for w in ws:
        hbf.set_wght(w)
        pg.label((24, y), ctx.label(w), 17)
        for j, ln in enumerate(lines):
            pg.text(hbf, ln, 24, y + 20 + lh * (j + 1) - 16, size, highlight=hl,
                    color=(24, 24, 24) if j < 3 else (135, 135, 135))
        y += 4 * lh + 40
    pg.label((24, y), "kerning and min. white gap (units) between the ink of the pair, per weight", 17, (60, 60, 60))
    y += 30
    tw = [None] if ctx.static else sorted({ctx.w_min, ctx.w_reg, ctx.w_max})
    for d in "0123456789":
        dg = cm[ord(d)]
        txt = []
        for w in tw:
            hbf.set_wght(w)
            k1, k2 = _kadj(hbf, ch + d), _kadj(hbf, d + ch)
            loc = _norm(f, w)
            c1 = pair_clearance(gs, gname, dg, k1, loc, 3)[0]
            c2 = pair_clearance(gs, dg, gname, k2, loc, 3)[0]
            txt.append(f"{'' if w is None else f'{w:g}'}: {ch}{d} {k1:+d} gap {c1:.0f} | {d}{ch} {k2:+d} gap {c2:.0f}")
        pg.label((24, y), "     ".join(txt), 16, (30, 30, 30))
        y += 24
    pg.save(out)


def _style_key(out_file, first):
    if first:
        return ""
    base = os.path.splitext(out_file)[0].split("[")[0]
    return "-" + (base.split("-")[-1].lower() if "-" in base else base.lower())


def main(cfg_path, tag, font_path=None, compare_path=None):
    import build_mn
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    pdir = os.path.join(ROOT, "proofs")
    os.makedirs(pdir, exist_ok=True)
    info_path = os.path.join(ROOT, cfg["out_dir"], "build-info.json")
    info = json.load(open(info_path, encoding="utf-8")) if os.path.exists(info_path) else {"fonts": []}
    outs = []
    for i, fc in enumerate(build_mn.font_configs(cfg)):
        path = font_path or os.path.join(ROOT, fc["out_dir"], fc["out_file"])
        font = TTFont(path)
        finfo = next((x for x in info["fonts"] if x["file"] == fc["out_file"]), {})
        hbf = HBFont(path)
        hl = set(fc["glyphs"].keys()) | set(finfo.get("alts", {}).keys()) | \
            {n + ".BRACKET.varAlt01" for n in fc["glyphs"]}
        hl = {g for g in hl if g in finfo.get("glyphs", {}) or g in finfo.get("alts", {})} if finfo else hl
        ctx = Ctx(font)
        pre = os.path.join(pdir, f"{cfg['family_id']}-{tag}{_style_key(fc['out_file'], i == 0)}")
        title = f"{cfg['new_family_name']} ({os.path.basename(path)})"
        for fn, suffix in ((proof_pairs, "pairs"), (proof_words, "words"),
                           (proof_guides, "guides"), (proof_interp, "interpolation"),
                           (proof_kerning, "kerning")):
            out = f"{pre}-{suffix}.png"
            fn(hbf, hl, out, title, ctx)
            outs.append(out)
            print(out)
        compare = HBFont(compare_path) if compare_path else None
        for gname, g in fc["glyphs"].items():
            if gname not in finfo.get("glyphs", {gname: 1}):
                continue      # glyph was already in the original font
            spec = build_mn.resolve_spec(font, g)
            if spec.get("kern_lookalike"):
                twin = spec["kern_lookalike"]["latin_twin"]
                out = f"{pre}-kerning-{twin}.png"
                proof_lookalike_kerning(hbf, hl, out, title, spec, ctx, compare)
                outs.append(out)
                print(out)
            if spec["build"].get("method") == "tugrik":
                out = f"{pre}-tugrik-gaps.png"
                proof_tugrik_gaps(hbf, hl, out, title, spec, ctx, finfo.get("slant", 0.0))
                outs.append(out)
                print(out)
                if spec.get("kern_like"):
                    out = f"{pre}-tugrik-digits.png"
                    proof_tugrik_digits(hbf, hl, out, title, spec, ctx)
                    outs.append(out)
                    print(out)
        if font_path:
            break
    return outs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--tag", default="v1")
    ap.add_argument("--font", default=None)
    ap.add_argument("--compare", default=None, help="previous build, shown light on the kerning sheet")
    a = ap.parse_args()
    main(a.config, a.tag, a.font, a.compare)
