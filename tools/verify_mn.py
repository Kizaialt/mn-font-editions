#!/usr/bin/env python3
"""Verify an MN edition against its sources.

    python tools/verify_mn.py tools/families/<family>.json [--baseline old.ttf]

Uses build/<Family>MN/build-info.json (written by build_mn.py).  Exit code
0 = all checks passed.  Per font file:
  cmap coverage, fontTools round-trip, OTS sanitizer (VF + statics);
  original glyphs / metrics / variations / cmap untouched; shaping of text
  without new glyphs identical to the source; new glyphs: GDEF class,
  advances, interpolation (constructed outlines track their base glyph at
  every weight step), contour direction, overlap flag; kerning parity with
  the chosen base (clone / Latin twin / look-alike mapping), ₮ kerning =
  T's against digits+punctuation with caps, no letter kerning; mark anchors;
  heavy-master ₮ geometry and whitespace rule; FeatureVariations parity;
  review targets (if any); static instances; names.
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.pens.recordingPen import RecordingPointPen, DecomposingRecordingPointPen  # noqa: E402

from mnfont.outline import GlyphSets, orientation_problems  # noqa: E402
from mnfont.render import HBFont  # noqa: E402

REQUIRED = list(range(0x0410, 0x0450)) + [0x0401, 0x0451, 0x04E8, 0x04E9, 0x04AE, 0x04AF, 0x20AE]
PARTNERS = ("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            "ӨөҮү.,-:;«»0123456789 ")
SAMPLE = ("Съешь же ещё этих мягких французских булок, да выпей чаю. "
          "The quick brown fox jumps over the lazy dog 0123456789 ТАТА Уа Ту ГО Ѓ ɵƟ fi.")
NOCCMP = {"ccmp": False}   # SC families map Latin lowercase to .sc in ccmp; compare base glyphs

results = []


def check(ok, label, detail=""):
    results.append((bool(ok), label, detail))
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    return ok


def kern_adjust(hbf, text, features=None):
    """Per-glyph positioning adjustment (shaped advance - nominal advance, offsets)."""
    infos, poss = hbf.shape(text, features)
    return [(p.x_advance - hbf.font.get_glyph_h_advance(i.codepoint), p.x_offset, p.y_offset)
            for i, p in zip(infos, poss)]


def tv_sig(tvs):
    return sorted((tuple(sorted(tv.axes.items())), tuple(tv.coordinates)) for tv in tvs)


def weights_of(font):
    if "fvar" not in font:
        return [None], None
    ax = next(a for a in font["fvar"].axes if a.axisTag == "wght")
    key = sorted({ax.minValue, ax.defaultValue, ax.maxValue})
    return key, ax


def user_of(ax, loc):
    """normalized master location (wght only) -> user value."""
    v = loc.get("wght", 0.0)
    if v == 0 or ax is None:
        return ax.defaultValue if ax else None
    return ax.defaultValue + v * ((ax.maxValue - ax.defaultValue) if v > 0 else (ax.defaultValue - ax.minValue))


def main(cfg_path, baseline=None):
    import build_mn
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    out_dir = os.path.join(ROOT, cfg["out_dir"])
    info = json.load(open(os.path.join(out_dir, "build-info.json"), encoding="utf-8"))
    fcfgs = list(build_mn.font_configs(cfg))
    import ots
    for fc in fcfgs:
        finfo = next(x for x in info["fonts"] if x["file"] == fc["out_file"])
        var_path = os.path.join(out_dir, fc["out_file"])
        src_path = os.path.join(ROOT, fc["source"])
        statics = [os.path.join(out_dir, "static", s) for s in finfo.get("statics", [])]
        print(f"\n===== {fc['out_file']} =====")
        verify_font(cfg, fc, finfo, var_path, src_path, statics, ots, baseline)
    nfail = sum(1 for ok, *_ in results if not ok)
    print(f"\n{len(results) - nfail}/{len(results)} checks passed")
    return nfail


def verify_font(cfg, fc, finfo, var_path, src_path, statics, ots, baseline):
    import build_mn
    tag = os.path.basename(var_path)
    files = [var_path] + statics
    for p in files:
        f = TTFont(p)
        cm = f.getBestCmap()
        missing = [f"U+{c:04X}" for c in REQUIRED if c not in cm]
        check(not missing, f"cmap coverage {os.path.basename(p)}", ", ".join(missing))
        f.ensureDecompiled()
        buf = io.BytesIO()
        f.save(buf)
        buf.seek(0)
        g = TTFont(buf)
        g.ensureDecompiled()
        check(g.getGlyphOrder() == f.getGlyphOrder(), f"fontTools save/reopen {os.path.basename(p)}")
        r = ots.sanitize(p, os.devnull, capture_output=True, text=True)
        msg = (r.stdout + r.stderr).strip().replace("\n", " | ")
        check(r.returncode == 0, f"OTS sanitize {os.path.basename(p)}", msg[:300])

    src, out = TTFont(src_path), TTFont(var_path)
    ws, ax = weights_of(out)
    new_names = list(finfo["glyphs"].keys())

    # 2. existing glyphs untouched ------------------------------------------
    order = src.getGlyphOrder()
    check(out.getGlyphOrder()[:len(order)] == order, f"{tag}: original glyph order preserved (new glyphs appended)")
    sg, og = src["glyf"], out["glyf"]
    bad = [n for n in order if sg[n].compile(sg) != og[n].compile(og)]
    check(not bad, f"{tag}: glyf data of all original glyphs byte-identical", ", ".join(bad[:5]))
    bad = [n for n in order if src["hmtx"][n] != out["hmtx"][n]]
    check(not bad, f"{tag}: hmtx of all original glyphs identical", ", ".join(bad[:5]))
    if "gvar" in src:
        bad = [n for n in order if tv_sig(src["gvar"].variations.get(n, [])) != tv_sig(out["gvar"].variations.get(n, []))]
        check(not bad, f"{tag}: gvar of all original glyphs identical", ", ".join(bad[:5]))
    if "HVAR" in src:
        sh, oh = src["HVAR"].table, out["HVAR"].table
        if sh.AdvWidthMap is not None:
            ok = all(sh.AdvWidthMap.mapping[n] == oh.AdvWidthMap.mapping[n] for n in order)
        else:
            ok = oh.VarStore.VarData[0].Item[:len(order)] == sh.VarStore.VarData[0].Item[:len(order)]
        check(ok, f"{tag}: HVAR data of original glyphs identical")
    scm, ocm = src.getBestCmap(), out.getBestCmap()
    check(all(ocm.get(c) == n for c, n in scm.items()), f"{tag}: cmap entries of the source unchanged")
    hs, ho = HBFont(src_path), HBFont(var_path)
    diffs = []
    for w in ws:
        hs.set_wght(w)
        ho.set_wght(w)
        a = [(i.codepoint, p.x_advance, p.x_offset, p.y_offset) for i, p in zip(*hs.shape(SAMPLE))]
        b = [(i.codepoint, p.x_advance, p.x_offset, p.y_offset) for i, p in zip(*ho.shape(SAMPLE))]
        if a != b:
            diffs.append(w)
    check(not diffs, f"{tag}: shaping of text without new glyphs identical to source ({ws})", str(diffs))

    # 3. new glyphs ---------------------------------------------------------
    # fonts without a GDEF glyph-class table (e.g. old kern-only fonts) get none added either
    gdef = out["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in src and src["GDEF"].table.GlyphClassDef else None
    steps = [None] if ax is None else sorted({round(ax.minValue + (ax.maxValue - ax.minValue) * i / 14)
                                              for i in range(15)})
    ugs = {w: (out.getGlyphSet(location={"wght": w}) if w is not None else out.getGlyphSet()) for w in steps}
    for n, gi in finfo["glyphs"].items():
        if gdef is not None:
            check(gdef.get(n) == 1, f"{n} GDEF class 1 (base)")
        else:
            check("GDEF" not in out, f"{n}: source has no GDEF, none added")
        mb = gi["metrics_base"]
        bad = [w for w, s in ugs.items() if abs(s[n].width - s[mb].width) > 0.01]
        check(not bad, f"{n} advance == {mb} at every weight step", str(bad))
        if gi.get("tracks"):
            base, pairs = gi["tracks"]
            worst = 0.0
            for w, s in ugs.items():
                pa, pb = DecomposingRecordingPointPen(s), DecomposingRecordingPointPen(s)
                s[n].drawPoints(pa)
                s[base].drawPoints(pb)
                A = [a[0] for op, a, k in pa.value if op == "addPoint"]
                B = [a[0] for op, a, k in pb.value if op == "addPoint"]
                for i, j in pairs:
                    worst = max(worst, abs(A[i][0] - B[j][0]), abs(A[i][1] - B[j][1]))
            check(worst <= 1.0, f"{n}: '{base}' points track '{base}' at every weight step",
                  f"{len(pairs)} points, max dev {worst:.2f} units")
        g = out["glyf"][n]
        if not g.isComposite():
            coords, ends, flags = g.getCoordinates(out["glyf"])
            s0, shape = 0, []
            for e in ends:
                shape.append([(coords[i][0], coords[i][1], bool(flags[i] & 1)) for i in range(s0, e + 1)])
                s0 = e + 1
            bad = orientation_problems(shape)
            check(not bad, f"{n}: contour directions OK (outer clockwise, ink on the right)", str(bad))
            check(bool(flags[0] & 0x40), f"{n}: OVERLAP_SIMPLE flag set")

    # 4. kerning ------------------------------------------------------------
    hb = HBFont(var_path)
    rev = {g: c for c, g in ocm.items()}
    digits_punct = "0123456789.,:;-«»()!?–—\"'"
    letters = "АаОоYyAaTтнеНЕ"
    owned = {chr(int(fc["glyphs"][nn]["unicode"], 16)) for nn, k in finfo["kern"].items()
             if k["mode"] == "lookalike" and nn in fc["glyphs"]}
    for n, kinfo in finfo["kern"].items():
        if n not in fc["glyphs"]:
            continue
        ch = chr(int(fc["glyphs"][n]["unicode"], 16))
        base = kinfo["base"]
        # SC fonts: the new letter is built on the small-cap glyph (not in the cmap), so it is compared
        # with the letter named in "verify_as" under the default features (ccmp swaps in the small caps)
        va = fc["glyphs"][n].get("verify_as")
        bch = va or chr(rev[base])
        kfeat = None if va else NOCCMP
        la = kinfo.get("lookalike")
        lmap = la["map"] if la else {}
        keep_l = set(la.get("keep_fallback", {}).get("as_left", [])) if la else set()
        keep_r = set(la.get("keep_fallback", {}).get("as_right", [])) if la else set()
        twin_ch = chr(rev[la["latin_twin"]]) if la else None
        mism = []
        for w in ws:
            hb.set_wght(w)
            for p in PARTNERS:
                if p in (ch, bch) or (p in owned and kinfo["mode"] != "lookalike"):
                    continue
                for side, s1 in (("L", ch + p), ("R", p + ch)):
                    if p in lmap and p not in (keep_l if side == "L" else keep_r):
                        q = lmap[p]
                        s2 = twin_ch + q if side == "L" else q + twin_ch
                    else:
                        s2 = bch + p if side == "L" else p + bch
                    a, c = kern_adjust(hb, s1, kfeat), kern_adjust(hb, s2, kfeat)
                    if a != c:
                        mism.append(f"{w}:{s1!r}~{s2!r} {a[0][0]}/{c[0][0]}")
        what = {"clone": base, "twin": f"Latin twin {base} (shared kerning)",
                "lookalike": f"{la['latin_twin'] if la else ''} via look-alikes / {base} otherwise"}[kinfo["mode"]]
        check(not mism, f"{n} kerning == {what} with {len(PARTNERS)} partners at {ws}", " ".join(mism[:6]))
    for n, kl in finfo.get("kern_like", {}).items():
        ch = chr(int(fc["glyphs"][n]["unicode"], 16))
        src_ch = chr(rev[kl["glyph"]])
        caps = {}       # by glyph name: the partner as actually shaped (e.g. four.sc in SC fonts)
        for pg, per in kl.get("capped", {}).items():
            caps[pg] = {(user_of(ax, m) if ax else None): v for m, v in per}
        mism, cap_bad, letter_bad = [], [], []
        mw = sorted({user_of(ax, m) for m in finfo["masters"]}) if ax else [None]
        for w in mw:
            hb.set_wght(w)
            for p in digits_punct:
                for s1, s2 in ((ch + p, src_ch + p), (p + ch, p + src_ch)):
                    a, c = kern_adjust(hb, s1)[0], kern_adjust(hb, s2)[0]
                    pn = hb.name(hb.shape(s1)[0][1].codepoint) if s1[0] == ch and len(s1) == 2 else None
                    if pn in caps:
                        want = caps[pn].get(w)
                        if want is None or a[0] != want:
                            cap_bad.append(f"{w}:{s1} {a[0]} want {want}")
                    elif a != c:
                        mism.append(f"{w}:{s1!r} {a[0]} vs {c[0]}")
            for p in letters:
                for s1 in (ch + p, p + ch):
                    if kern_adjust(hb, s1)[0][0] != 0:
                        letter_bad.append(f"{w}:{s1}")
        check(not mism, f"{n} kerning == {kl['glyph']}'s against digits+punctuation ({mw})", " ".join(mism[:6]))
        check(not cap_bad, f"{n} capped pairs follow the per-master caps {list(caps)}", " ".join(cap_bad[:6]))
        check(not letter_bad, f"{n} has no kerning with letters", " ".join(letter_bad[:6]))
    rt = cfg.get("review_targets", {})
    for pair, vals in rt.get("kerning", {}).items():
        if pair.startswith("_"):
            continue
        got = []
        for w, want in zip(rt["weights"], vals):
            hb.set_wght(w)
            got.append(kern_adjust(hb, pair)[0][0])
        ok = all(abs(g - v) <= 1 for g, v in zip(got, vals))
        check(ok, f"review target {pair}: {'/'.join(map(str, got))} (target {'/'.join(map(str, vals))})")

    # 5. mark anchors -------------------------------------------------------
    gpos = out["GPOS"].table
    for n, ab in finfo.get("anchors", {}).items():
        same = True
        for lk in gpos.LookupList.Lookup:
            for st in lk.SubTable:
                st = getattr(st, "ExtSubTable", st)
                if hasattr(st, "BaseCoverage"):
                    cov = st.BaseCoverage.glyphs
                    if (n in cov) != (ab in cov):
                        same = False
                    elif n in cov:
                        ra = st.BaseArray.BaseRecord[cov.index(n)].BaseAnchor
                        rb = st.BaseArray.BaseRecord[cov.index(ab)].BaseAnchor
                        sig = lambda r: [(a.XCoordinate, a.YCoordinate) if a else None for a in r]  # noqa: E731
                        same &= sig(ra) == sig(rb)
        check(same, f"{n} mark anchors == {ab}")

    # 6. ₮ heavy master -----------------------------------------------------
    for n, g in fc["glyphs"].items():
        if n not in finfo["glyphs"] or g["build"].get("method") != "tugrik" or ax is None:
            continue
        spec = build_mn.resolve_spec(out, g)
        b = spec["build"]
        from mnfont.construct import measure_internal_gaps, measure_t_shape, deslant
        k = finfo.get("slant", 0.0)
        heavy_w = ax.maxValue
        s = out.getGlyphSet(location={"wght": heavy_w})
        pen = RecordingPointPen()
        s[n].drawPoints(pen)
        pts = [(a[0][0] - k * a[0][1], a[0][1]) for op, a, kk in pen.value if op == "addPoint"]
        lo, up = pts[-8:-4], pts[-4:]
        xa, xb = lo[0][0], lo[1][0]
        vt = lo[0][1] - lo[3][1]
        ang = math.degrees(math.atan2(lo[1][1] - lo[0][1], xb - xa))
        t = vt * math.cos(math.radians(ang))
        gs_out = GlyphSets(out)
        hloc = {"wght": 1.0}
        mt = measure_t_shape(deslant(gs_out.shape(b["base"], hloc), k))
        gaps = (lo[3][1], up[3][1] - lo[0][1], mt["bar"][0] - up[1][1])
        print(f"     {n} @ wght {heavy_w:g}: x {xa:.0f}..{xb:.0f} (span {xb - xa:.0f}), thickness {t:.1f}, "
              f"angle {ang:.2f}, gaps bottom/between/top ({gaps[0]:.0f}, {gaps[1]:.0f}, {gaps[2]:.0f})")
        ov = next(iter(v for kk, v in b.get("master_overrides", {}).items() if not kk.startswith("_")), None)
        if ov:
            ok = (abs((xb - xa) - ov["x_span"]) <= 1 and abs(t - ov["thickness"]) <= 1.5 and
                  abs(ang - ov["angle"]) <= 0.3 and abs(gaps[0] - ov["gap_bottom"]) <= 1 and
                  abs(gaps[1] - ov["gap_between"]) <= 1)
            check(ok, f"{n} heaviest master matches the reviewed override")
        fam = measure_internal_gaps(gs_out, b.get("heavy_gap_refs", []), hloc, k)
        if fam:
            G = b.get("heavy_gap_factor", 1.2) * min(fam.values())
            check(min(gaps[1], gaps[2]) >= G - 0.5,
                  f"{n} heaviest-master internal gaps {gaps[1]:.0f}/{gaps[2]:.0f} >= {G:.1f} "
                  f"({b.get('heavy_gap_factor', 1.2)} x tightest family gap {min(fam.values())} in {fam})")

    # 7. FeatureVariations alternates ---------------------------------------
    for alt, parent in finfo.get("alts", {}).items():
        comp = out["glyf"][parent].components[0].glyphName
        pch, bch = chr(int(fc["glyphs"][parent]["unicode"], 16)), chr(rev[comp])
        fv = []
        for w in range(int(ax.minValue), int(ax.maxValue) + 1, 10):
            hb.set_wght(w)
            a = hb.name(hb.shape(pch)[0][0].codepoint)
            b2 = hb.name(hb.shape(bch)[0][0].codepoint)
            if (a == parent) != (b2 == comp):
                fv.append(f"{w}:{a}/{b2}")
        check(not fv, f"{pch} swaps to {alt} exactly where {bch} swaps", " ".join(fv[:5]))

    # 7b. comparison with a previous build -----------------------------------
    if baseline:
        base_f = TTFont(baseline)
        hb_b = HBFont(baseline)
        for n in cfg.get("frozen_glyphs", []):
            same = (base_f["glyf"][n].compile(base_f["glyf"]) == out["glyf"][n].compile(out["glyf"])
                    and base_f["hmtx"][n] == out["hmtx"][n]
                    and tv_sig(base_f["gvar"].variations.get(n, [])) == tv_sig(out["gvar"].variations.get(n, [])))
            check(same, f"{n} outline/metrics/variations identical to baseline {os.path.basename(baseline)}")
            ch = chr(int(cfg["glyphs"][n]["unicode"], 16))
            diff = []
            for w in ws:
                hb.set_wght(w)
                hb_b.set_wght(w)
                for p in PARTNERS:
                    if p in "Ү₮":
                        continue
                    for s1 in (ch + p, p + ch):
                        if kern_adjust(hb, s1) != kern_adjust(hb_b, s1):
                            diff.append(f"{w}:{s1}")
            check(not diff, f"{n} kerning identical to baseline (partners other than Ү ₮)", " ".join(diff[:6]))
        for n, keep in cfg.get("frozen_masters", {}).items():
            gb, go = base_f["glyf"][n], out["glyf"][n]
            same = gb.getCoordinates(base_f["glyf"])[0] == go.getCoordinates(out["glyf"])[0]
            tb = {tuple(sorted(tv.axes.items())): tv.coordinates for tv in base_f["gvar"].variations[n]}
            to = {tuple(sorted(tv.axes.items())): tv.coordinates for tv in out["gvar"].variations[n]}
            for kk in keep:
                if kk == "default":
                    continue
                key = next((x for x in tb if dict(x).get("wght", (0, 0, 0))[1] == float(kk.split("=")[1])), None)
                same &= key is not None and tb[key] == to.get(key)
            check(same, f"{n} masters {keep} identical to baseline")

    # 8. static instances ----------------------------------------------------
    for p in statics:
        f = TTFont(p)
        hm = f["hmtx"]
        bad = [n for n, gi in finfo["glyphs"].items() if hm[n][0] != hm[gi["metrics_base"]][0]]
        check(not bad, f"{os.path.basename(p)}: advances of new glyphs == base", ",".join(bad))
        bad = []
        for n in finfo["glyphs"]:
            g = f["glyf"][n]
            if g.isComposite():
                continue
            coords, ends, flags = g.getCoordinates(f["glyf"])
            s0, shape = 0, []
            for e in ends:
                shape.append([(coords[i][0], coords[i][1], bool(flags[i] & 1)) for i in range(s0, e + 1)])
                s0 = e + 1
            if orientation_problems(shape):
                bad.append(n)
        check(not bad, f"{os.path.basename(p)}: new simple glyphs correctly oriented", ",".join(bad))
        w = f["OS/2"].usWeightClass
        if w in rt.get("weights", []):
            i = rt["weights"].index(w)
            hsx = HBFont(p)
            bad = []
            for pair, vals in rt["kerning"].items():
                if not pair.startswith("_"):
                    got = kern_adjust(hsx, pair)[0][0]
                    if abs(got - vals[i]) > 1:
                        bad.append(f"{pair} {got}/{vals[i]}")
            check(not bad, f"{os.path.basename(p)}: review kerning targets hold in the static instance", " ".join(bad[:6]))

    # 9. names ---------------------------------------------------------------
    note = cfg["copyright_append"].split("{added}")[0]
    for p in files:
        f = TTFont(p)
        nm = f["name"]
        ids = [1, 2, 3, 4, 5, 6, 16, 17, 25]
        line = " | ".join(f"{i}={nm.getDebugName(i)!r}" for i in ids if nm.getDebugName(i))
        print(f"     names {os.path.basename(p)}: {line}")
        fam = nm.getDebugName(16) or nm.getDebugName(1)
        check(fam.startswith(cfg["new_family_name"]), f"{os.path.basename(p)} family name '{fam}'")
        check("Open Font License" in (nm.getDebugName(13) or ""), f"{os.path.basename(p)} OFL licence string kept")
        check(note in (nm.getDebugName(0) or ""), f"{os.path.basename(p)} copyright note")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--baseline", help="previous build of the variable font, for frozen-glyph checks")
    a = ap.parse_args()
    sys.exit(1 if main(a.config, a.baseline) else 0)
