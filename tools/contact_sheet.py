#!/usr/bin/env python3
"""Contact sheet for a batch of MN editions: per font file and weight one row
with "О Ө о ө Y Ү v ү у Т ₮" and "Өндөр Үүлс · ₮12 500", new glyphs in blue.

    python tools/contact_sheet.py proofs/batch1-contact tools/families/a.json tools/families/b.json ...

Writes <prefix>.png, or <prefix>-1.png, <prefix>-2.png ... when one sheet
would get taller than --max-height px (width is fixed at 1950 px).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from fontTools.ttLib import TTFont  # noqa: E402
from mnfont.render import HBFont, Page  # noqa: E402

LINE1 = "О Ө  о ө  Y Ү  v ү у  Т ₮"
LINE2 = "Өндөр Үүлс · ₮12 500"
ROW_H, HEAD_H, W = 96, 54, 1950


def rows_for(cfg_path):
    import build_mn
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    out_dir = os.path.join(ROOT, cfg["out_dir"])
    info = json.load(open(os.path.join(out_dir, "build-info.json"), encoding="utf-8"))
    rows = []
    for fc in build_mn.font_configs(cfg):
        path = os.path.join(out_dir, fc["out_file"])
        f = TTFont(path)
        finfo = next(x for x in info["fonts"] if x["file"] == fc["out_file"])
        hl = set(finfo["glyphs"]) | set(finfo.get("alts", {}))
        style = "Italic" if f["post"].italicAngle else "Roman"
        if "fvar" in f:
            ax = next(a for a in f["fvar"].axes if a.axisTag == "wght")
            reg = 400 if ax.minValue <= 400 <= ax.maxValue else ax.defaultValue
            bold = 700 if ax.minValue <= 700 <= ax.maxValue else ax.maxValue
            ws = [(reg, "Regular" if reg == 400 else f"{reg:g}"), (bold, "Bold" if bold == 700 else f"{bold:g}")]
        else:
            ws = [(None, f["name"].getDebugName(17) or f["name"].getDebugName(2))]
        for w, wl in ws:
            rows.append(dict(family=cfg["new_family_name"], path=path, w=w,
                             label=f"{style} {wl}", hl=hl, added=finfo.get("added", "")))
    return rows


def render(rows, out, title):
    pg = Page(W, HEAD_H + ROW_H * len(rows) + 20)
    pg.label((20, 14), title + "  -  new glyphs in blue", 22, (60, 60, 60))
    y = HEAD_H
    fonts = {}
    for r in rows:
        hb = fonts.setdefault(r["path"], HBFont(r["path"]))
        hb.set_wght(r["w"])
        pg.hline(y + 2, 20, W - 20, fill=(225, 225, 220))
        pg.label((20, y + 14), r["family"], 18, (40, 40, 40))
        pg.label((20, y + 40), f"{r['label']}   +{r['added']}", 15, (120, 120, 120))
        base = y + 72
        x = 330
        x += pg.text(hb, LINE1, x, base, 60, highlight=r["hl"]) + 60
        pg.text(hb, LINE2, max(x, 1150), base, 52, highlight=r["hl"])
        y += ROW_H
    pg.save(out)
    print(out, pg.img.size)


def main(prefix, cfgs, max_height):
    rows = [r for c in cfgs for r in rows_for(c)]
    per = max(1, (max_height - HEAD_H - 20) // ROW_H)
    chunks = [rows[i:i + per] for i in range(0, len(rows), per)]
    title = os.path.basename(prefix)
    if len(chunks) == 1:
        render(chunks[0], prefix + ".png", title)
    else:
        for i, ch in enumerate(chunks, 1):
            render(ch, f"{prefix}-{i}.png", f"{title} ({i}/{len(chunks)})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", help="output path without .png, e.g. proofs/batch1-contact")
    ap.add_argument("configs", nargs="+")
    ap.add_argument("--max-height", type=int, default=1900)
    a = ap.parse_args()
    main(a.prefix if os.path.isabs(a.prefix) else os.path.join(ROOT, a.prefix), a.configs, a.max_height)
