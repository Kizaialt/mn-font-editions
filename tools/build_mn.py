#!/usr/bin/env python3
"""Build a Mongolian ("MN") edition of an OFL font family by ADDING the
missing Mongolian Cyrillic glyphs (Ө ө Ү ү ₮) in the font's own style.

    python tools/build_mn.py tools/families/unbounded.json

Existing glyphs are never modified.  Works on variable TrueType fonts
(glyf+gvar+HVAR) and on static TrueType fonts (no gvar).  Per-family
parameters live in tools/families/<family>.json:

  * single-font family: "source" + "out_file" at the top level (Unbounded);
  * multi-font family:  "fonts": [{"source", "out_file", "glyph_overrides"?,
    "statics"?}, ...] - e.g. roman + italic, sharing the glyph specs.

Glyph references in the JSON may be glyph names or "@<char>" (resolved
through the font's cmap, e.g. "@Y", "@р", "@4"), so one spec works across
fonts with different glyph-naming schemes.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import json
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.ttLib.tables.O_S_2f_2 import intersectUnicodeRanges  # noqa: E402

from mnfont.outline import GlyphSets, master_locations, loc_key, bounds, ink_intervals  # noqa: E402
from mnfont.construct import build_glyph, Built  # noqa: E402
from mnfont.varglyph import add_glyph, map_unicode  # noqa: E402
from mnfont import otl  # noqa: E402
from mnfont.names import rename_family  # noqa: E402


def _p(path):
    return path if os.path.isabs(path) else os.path.join(ROOT, path)


def _rel(path):
    try:
        return os.path.relpath(path, ROOT)
    except ValueError:      # different drive on Windows
        return path


def _involved_glyphs(spec):
    names = [spec.get("base"), spec.get("bar_ref"), spec.get("stem_ref")]
    names += spec.get("prefer_component", [])
    return [n for n in names if n]


# --------------------------------------------------------------------------
# glyph references ("@X" -> cmap) and per-font spec merging
# --------------------------------------------------------------------------

def resolve_ref(font, ref, required=True):
    if not isinstance(ref, str) or not ref.startswith("@"):
        return ref
    cm = font.getBestCmap()
    key = ref[1:]
    cp = int(key[2:], 16) if key.upper().startswith("U+") else (ord(key) if len(key) == 1 else None)
    g = cm.get(cp) if cp is not None else None
    if g is None and required:
        raise KeyError(f"glyph reference {ref} not in the font's cmap")
    return g


def resolve_spec(font, g):
    g = copy.deepcopy(g)
    for key in ("otl_base", "anchor_base"):
        if g.get(key):
            g[key] = resolve_ref(font, g[key])
    b = g["build"]
    for key in ("base", "bar_ref", "stem_ref"):
        if b.get(key):
            b[key] = resolve_ref(font, b[key])
    if "prefer_component" in b:
        b["prefer_component"] = [r for r in (resolve_ref(font, x, False) for x in b["prefer_component"]) if r]
    if "heavy_gap_refs" in b:
        refs = []
        for r in b["heavy_gap_refs"]:
            gname = resolve_ref(font, r["glyph"], False)
            if gname:
                refs.append(dict(r, glyph=gname))
        b["heavy_gap_refs"] = refs
    if g.get("kern_lookalike"):
        g["kern_lookalike"]["latin_twin"] = resolve_ref(font, g["kern_lookalike"]["latin_twin"])
    if g.get("kern_like"):
        kl = g["kern_like"]
        kl["glyph"] = resolve_ref(font, kl["glyph"])
        if "caps" in kl:
            kl["caps"] = {(k if k.startswith("_") else resolve_ref(font, k)): v for k, v in kl["caps"].items()}
    return g


def font_configs(cfg):
    """Yield one config per font file of the family."""
    if not cfg.get("fonts"):
        yield cfg
        return
    for fs in cfg["fonts"]:
        c = copy.deepcopy({k: v for k, v in cfg.items() if k != "fonts"})
        for k, v in fs.items():
            if k == "glyph_overrides":
                for gname, ov in v.items():
                    if gname not in c["glyphs"]:
                        continue
                    for kk, vv in ov.items():
                        if kk == "build":
                            c["glyphs"][gname]["build"].update(vv)
                        else:
                            c["glyphs"][gname][kk] = vv
            else:
                c[k] = v
        yield c


def measured_slant(font):
    """tan(italic slant) from post.italicAngle, cross-checked against the
    stem of 'I' (two horizontal rays)."""
    ang = font["post"].italicAngle
    k_post = math.tan(math.radians(-ang)) if ang else 0.0
    k_meas = None
    g = font.getBestCmap().get(ord("I"))
    if g:
        gs = GlyphSets(font)
        sh = gs.shape(g, {})
        x0, y0, x1, y1 = bounds(sh)
        a = ink_intervals(sh, y0 + 0.2 * (y1 - y0), 1)
        b = ink_intervals(sh, y0 + 0.8 * (y1 - y0), 1)
        if len(a) == 1 and len(b) == 1:
            k_meas = ((b[0][0] + b[0][1]) - (a[0][0] + a[0][1])) / 2 / (0.6 * (y1 - y0))
    return k_post, k_meas


# --------------------------------------------------------------------------
# one font file
# --------------------------------------------------------------------------

def build_font(cfg, log):
    src = _p(cfg["source"])
    out_dir = _p(cfg["out_dir"])
    os.makedirs(out_dir, exist_ok=True)
    font = TTFont(src, recalcTimestamp=False)   # reproducible: fixed head.modified below
    order0 = set(font.getGlyphOrder())
    cmap = font.getBestCmap()
    orig_version = f"{font['head'].fontRevision:.3f}"
    is_var = "fvar" in font and "gvar" in font
    log.append(f"source: {cfg['source']} (v{orig_version}, {len(order0)} glyphs, "
               f"{'variable' if is_var else 'static'})")

    k_post, k_meas = measured_slant(font)
    slant = 0.0
    if k_post or (k_meas and abs(k_meas) > 0.02):
        slant = k_meas if (k_meas is not None and abs(k_meas - k_post) > math.tan(math.radians(1.0))) else k_post
        log.append(f"italic: post.italicAngle {font['post'].italicAngle} deg -> tan {k_post:.4f}; "
                   f"measured on I {k_meas if k_meas is None else round(k_meas, 4)}; using {slant:.4f}")

    todo = {}
    for gname, g in cfg["glyphs"].items():
        cp = int(g["unicode"], 16)
        if cp in cmap:
            log.append(f"skip U+{cp:04X}: already mapped to {cmap[cp]}")
            continue
        if gname in order0:
            raise ValueError(f"glyph name {gname} already used in source")
        g = resolve_spec(font, g) if cfg.get("fonts") or _has_refs(g) else g
        if slant:
            g = copy.deepcopy(g)
            g["build"]["_slant"] = slant
        todo[gname] = g
    if not todo:
        log.append("nothing to add")

    involved = sorted({n for g in todo.values() for n in _involved_glyphs(g["build"]) if n in order0})
    if is_var:
        masters = master_locations(font, involved)
        axis_order = [a.axisTag for a in font["fvar"].axes]
    else:
        masters, axis_order = [{}], []
    log.append("masters (normalized): " + ", ".join(
        ",".join(f"{k}={v:+g}" for k, v in m.items()) or "default" for m in masters))

    # 1. construct every glyph from the untouched source outlines
    gs = GlyphSets(font)
    built = {}
    for gname, g in todo.items():
        b = build_glyph(gs, masters, gname, g["build"])
        built[gname] = b
        for n in b.notes:
            log.append(f"{gname} (U+{g['unicode']}): {n}")
        if b.measurements:
            for k, m in b.measurements.items():
                log.append(f"    {gname} @ {dict(k) or 'default'}: {m}")

    # 2. insert glyphs (+ FeatureVariations alternates of component bases)
    pairs, extra_alts, alt_parent = [], [], {}
    for gname, g in todo.items():
        b = built[gname]
        add_glyph(font, b, masters, axis_order)
        map_unicode(font, gname, int(g["unicode"], 16))
        if g.get("otl_base"):
            pairs.append((gname, g["otl_base"]))
    for gname, g in todo.items():
        b = built[gname]
        if b.kind != "composite" or len(b.components) != 1:
            continue
        comp = b.components[0][0]
        for alt, lookups in otl.feature_variation_alternates(font, comp).items():
            alt_name = gname + alt[len(comp):] if alt.startswith(comp) else f"{gname}.{alt}"
            ab = Built(alt_name, "composite", metrics_base=alt, components=[(alt, 0, 0)])
            add_glyph(font, ab, masters, axis_order)
            otl.add_feature_variation_mapping(font, gname, alt_name, comp, lookups, log)
            log.append(f"{alt_name}: composite of '{alt}' (weight-range alternate, mirrors {comp})")
            extra_alts.append((alt_name, alt))
            alt_parent[alt_name] = gname
            if g.get("otl_base"):
                pairs.append((alt_name, g["otl_base"]))

    # 3. layout: kerning, mark anchors, contextual membership
    #    otl_base      -> kerning classes/pairs (fallback), contextual membership
    #    anchor_base   -> mark anchors (defaults to otl_base)
    #    kern_lookalike-> Latin-twin values for partners with a Latin look-alike
    #                     (auto: only if Latin and Cyrillic kerning are separate)
    #    kern_like     -> another glyph's kerning, digits + punctuation only
    parent = {gname: gname for gname in todo}
    parent.update({alt: gname for alt, gname in alt_parent.items()})
    cmap_now = font.getBestCmap()
    kern_pairs, anchor_pairs, lookalike = [], [], {}
    info_kern = {}
    for name, base in pairs:
        spec = todo[parent[name]]
        kb = base
        la = spec.get("kern_lookalike")
        mode_used = "clone"
        if la and name == parent[name]:
            mode = la.get("mode", "auto")
            shared, detail = otl.kerning_shared(font, la["latin_twin"], la["map"], cmap_now,
                                                exclude=set(parent))
            log.append(f"kern: {name}: Latin/Cyrillic kerning shared = {shared} ({detail}); mode {mode}")
            if mode == "shared" or (mode == "auto" and shared):
                kb = la["latin_twin"]
                mode_used = "twin"
            else:
                lookalike[name] = la
                mode_used = "lookalike"
        info_kern[name] = dict(mode=mode_used, base=kb, lookalike=la if mode_used == "lookalike" else None)
        kern_pairs.append((name, kb))
        anchor_pairs.append((name, spec.get("anchor_base") or base))
    for gname, g in todo.items():
        if not g.get("otl_base") and g.get("anchor_base"):
            anchor_pairs.append((gname, g["anchor_base"]))
    otl.clone_kerning(font, kern_pairs, log)
    for name, la in lookalike.items():
        otl.lookalike_kerning(font, name, la, log)
    info_kern_like = {}
    for gname, g in todo.items():
        if g.get("kern_like"):
            capped = otl.selective_kerning(font, gname, g["kern_like"], masters, log)
            info_kern_like[gname] = dict(glyph=g["kern_like"]["glyph"], capped=capped)
    otl.clone_marks(font, anchor_pairs, log)
    otl.clone_context_membership(font, pairs, log)

    # 3b. default language forms (opt-in): e.g. "default_locl_lang": "RUS" makes the
    #     Russian-style forms the default in a font whose default is Bulgarian.  After
    #     everything above, so kerning/anchor cloning still sees the original cmap.
    default_locl = None
    if cfg.get("default_locl_lang"):
        lang = cfg["default_locl_lang"]
        changed = otl.default_locl_remap(font, lang, log)
        default_locl = dict(lang=lang, script="cyrl",
                            remapped={f"U+{cp:04X}": [a, b] for cp, (a, b) in sorted(changed.items())})

    # 4. naming, OS/2, misc
    added = " ".join(chr(int(g["unicode"], 16)) for g in todo.values())
    ncfg = dict(cfg)
    if "{added}" in cfg.get("copyright_append", ""):
        ncfg["copyright_append"] = cfg["copyright_append"].replace("{added}", added)
    rename_family(font, ncfg, log)
    os2 = font["OS/2"]
    new_cps = {int(g["unicode"], 16) for g in todo.values()}
    before = os2.getUnicodeRanges()
    os2.setUnicodeRanges(before | intersectUnicodeRanges(new_cps))
    if os2.getUnicodeRanges() != before:
        log.append(f"OS/2 ulUnicodeRange bits added: {sorted(os2.getUnicodeRanges() - before)}")
    os2.updateFirstAndLastCharIndex(font)
    if "DSIG" in font and getattr(font["DSIG"], "usNumSigs", 0):
        del font["DSIG"]
        log.append("removed DSIG (a digital signature is invalid after any modification)")

    from fontTools.misc.timeTools import timestampFromString
    font["head"].modified = timestampFromString(
        datetime.datetime.strptime(cfg.get("date", "2026-10-13"), "%Y-%m-%d").strftime("%a %b %d 00:00:00 %Y"))
    out_path = os.path.join(out_dir, cfg["out_file"])
    font.save(out_path)
    log.append(f"saved {_rel(out_path)}")

    # 5. static instances (optional)
    statics = []
    if is_var and cfg.get("statics"):
        statics = make_statics(out_path, out_dir, [b.name for b in built.values() if b.kind == "simple"], log)

    info = dict(file=cfg["out_file"], source=cfg["source"], variable=is_var, slant=slant,
                masters=[dict(m) for m in masters], added=added,
                glyphs={n: dict(kind=b.kind, metrics_base=b.metrics_base,
                                components=[c[0] for c in b.components],
                                tracks=getattr(b, "tracks", None),
                                measurements={",".join(f"{a}={v:+g}" for a, v in k) or "default": m
                                              for k, m in b.measurements.items()})
                        for n, b in built.items()},
                alts={a: p for a, p in alt_parent.items()},
                kern=info_kern, kern_like=info_kern_like,
                anchors={n: a for n, a in anchor_pairs},
                statics=[os.path.basename(p) for _, _, p in statics])
    if default_locl:        # key only present for opt-in families: other builds stay byte-identical
        info["default_locl"] = default_locl
    return dict(out_path=out_path, orig_version=orig_version, todo=todo, built=built,
                statics=statics, extra_alts=extra_alts, info=info, cfg=cfg)


def _has_refs(g):
    return "@" in json.dumps(g, ensure_ascii=False)


def build(cfg_path, no_statics=False):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    if no_statics:
        cfg["statics"] = False
        for fs in cfg.get("fonts", []):
            fs["statics"] = False
    log = []
    out_dir = _p(cfg["out_dir"])
    sdir = os.path.join(out_dir, "static")
    if os.path.isdir(sdir) and any(fc.get("statics") for fc in font_configs(cfg)):
        for fn in os.listdir(sdir):          # our own previous outputs: rebuilt below
            if fn.endswith(".ttf"):
                os.remove(os.path.join(sdir, fn))
    results = [build_font(fc, log) for fc in font_configs(cfg)]
    shutil.copyfile(_p(cfg["license"]), os.path.join(out_dir, "OFL.txt"))
    if not cfg.get("fonts"):
        r = results[0]
        write_fontlog(cfg, out_dir, r["orig_version"], r["todo"], r["built"], r["statics"], r["extra_alts"], r["info"])
    else:
        write_fontlog_multi(cfg, out_dir, results)
    with open(os.path.join(out_dir, "build-log.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    with open(os.path.join(out_dir, "build-info.json"), "w", encoding="utf-8") as fh:
        json.dump(dict(family=cfg["new_family_name"], fonts=[r["info"] for r in results]), fh,
                  ensure_ascii=False, indent=1, default=str)
    print("\n".join(log))
    return [r["out_path"] for r in results]


def make_statics(var_path, out_dir, simple_new, log):
    from fontTools.varLib import instancer
    from fontTools.ttLib.removeOverlaps import removeOverlaps
    sdir = os.path.join(out_dir, "static")
    os.makedirs(sdir, exist_ok=True)
    vf = TTFont(var_path, recalcTimestamp=False)
    name = vf["name"]
    out = []
    for inst in vf["fvar"].instances:
        style = name.getDebugName(inst.subfamilyNameID)
        f = instancer.instantiateVariableFont(TTFont(var_path, recalcTimestamp=False),
                                              dict(inst.coordinates), updateFontNames=True)
        f["name"].removeNames(nameID=25)   # variations PS-name prefix: variable fonts only
        # PostScript name <FamilyPS>-<Style> (instancer derives it from the italic
        # VF's prefix, e.g. 'SofiaSansMNItalic-BoldItalic'; normalise to 'SofiaSansMN-BoldItalic')
        fam_ps = vf["name"].getDebugName(6).split("-")[0]
        sty = (f["name"].getDebugName(17) or f["name"].getDebugName(2)).replace(" ", "")
        want = f"{fam_ps}-{sty}"
        old_ps = f["name"].getDebugName(6)
        if old_ps != want:
            for rec in f["name"].names:
                if rec.nameID in (3, 6) and old_ps in rec.toUnicode():
                    rec.string = rec.toUnicode().replace(old_ps, want)
        present = [g for g in simple_new if g in f.getGlyphOrder()]
        removeOverlaps(f, glyphNames=present, removeHinting=False)
        ps = f["name"].getDebugName(6)
        path = os.path.join(sdir, f"{ps}.ttf")
        f.save(path)
        out.append((style, inst.coordinates, path))
        log.append(f"static {style} {dict(inst.coordinates)} -> {_rel(path)} "
                   f"(names: {f['name'].getDebugName(1)!r} / {f['name'].getDebugName(2)!r} / "
                   f"{f['name'].getDebugName(4)!r}; overlaps removed in {present})")
    return out


def _glyph_lines(todo, built, extra_alts):
    lines = []
    for gname, g in todo.items():
        b = built[gname]
        ch = chr(int(g["unicode"], 16))
        summary = next((n for n in b.notes if n.startswith(("'", "composite"))), b.notes[0])
        if g.get("kern_lookalike"):
            la = g["kern_lookalike"]
            kern = (f"; kerning: Latin `{la['latin_twin']}`'s values via the Latin look-alike of each "
                    f"partner, other partners from `{g['otl_base']}`")
        elif g.get("kern_like"):
            kern = f"; kerning: `{g['kern_like']['glyph']}`'s values against digits and punctuation only"
            if g["kern_like"].get("caps"):
                kern += " (capped: " + ", ".join(k for k in g["kern_like"]["caps"] if not k.startswith("_")) + ")"
        elif g.get("otl_base"):
            kern = f"; kerning from `{g['otl_base']}`"
        else:
            kern = "; no kerning"
        anc = g.get("anchor_base") or g.get("otl_base")
        kern += f"; mark anchors from `{anc}`" if anc else ""
        lines.append(f"- U+{g['unicode']} {ch} `{gname}`: {summary}{kern}.")
        if b.kind == "simple" and len(b.measurements) > 1:
            per = []
            for k, m in b.measurements.items():
                loc = ",".join(f"{a}={v:+g}" for a, v in k) or "default"
                keys = [x for x in ("stroke_thickness", "angle", "stroke_x", "gaps", "stem", "join_y") if x in m]
                per.append(f"{loc}: " + ", ".join(f"{x} {m[x]}" for x in keys))
            lines.append(f"  - per master (normalized wght): " + "; ".join(per))
        for n in b.notes:
            if n.startswith("heaviest master"):
                lines.append(f"  - {n}")
    for alt in extra_alts:
        lines.append(f"- `{alt[0]}`: composite of `{alt[1]}` - the font's heavy-weight "
                     f"('BRACKET') alternate, swapped in by the same GSUB FeatureVariations rule as its base.")
    return lines


def _locl_lines(info, family_level=False):
    """FONTLOG text for the opt-in `default_locl_lang` change (empty for other families)."""
    dl = info.get("default_locl") if info else None
    if not dl:
        return []
    if family_level:
        return ["Standard Russian-style Cyrillic forms are the default in this Mongolian edition; "
                "the original's default is Bulgarian. See the per-file notes below.", ""]
    chars = " ".join(chr(int(k[2:], 16)) for k in dl["remapped"])
    return [f"Default forms: standard Russian-style Cyrillic forms are the default in this Mongolian edition; "
            f"the original's default is Bulgarian. The cmap maps {len(dl['remapped'])} letters ({chars}) to their "
            f"`.locl{dl['lang']}` glyphs, which the original reaches only through the `locl` feature for language "
            f"{dl['lang']}. No outline, metric, kerning or other layout table was changed; the original "
            f"Bulgarian-style glyphs stay in the font under their plain names.", ""]


def write_fontlog(cfg, out_dir, orig_version, todo, built, statics, extra_alts=(), info=None):
    today = cfg.get("date") or datetime.date(2026, 10, 13).isoformat()
    lines = [
        f"# FONTLOG for {cfg['new_family_name']}",
        "",
        f"{cfg['new_family_name']} is a modified version of **{cfg['family_name']}** "
        f"v{orig_version} ({cfg.get('upstream', '')}), released under the SIL Open Font "
        "License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.",
        "",
        "## Changelog",
        "",
        f"### {today} - {cfg['version_suffix']} - Font Shuugch project",
        "",
        "Added the letters Mongolian Cyrillic needs that the original lacks. "
        "No existing glyph was altered.",
        "",
    ]
    lines += _locl_lines(info, True) + _locl_lines(info)
    if cfg.get("release_notes"):
        lines += ["Changes in this release:", ""] + [f"- {n}" for n in cfg["release_notes"]] + ["", "Glyphs:", ""]
    lines += _glyph_lines(todo, built, extra_alts)
    lines += [
        "",
    ]
    for h in cfg.get("fontlog_history", []):
        lines += [f"### {h['date']} - {h['version']} - Font Shuugch project", "", h["text"], ""]
    lines += [
        "## Method",
        "",
        "tools/build_mn.py with tools/families/" + cfg["family_id"] + ".json. "
        "Constructed outlines are computed from the font's own glyphs at every variation master, "
        "so they interpolate across the weight axis like their neighbours; advance widths and HVAR "
        "come from the base glyphs, kerning and mark anchors as listed above (`otl_base`, "
        "`anchor_base`, `kern_lookalike`, `kern_like` in the JSON).",
        "",
        "## Files",
        "",
        f"- `{cfg['out_file']}` - variable font",
    ]
    for style, coords, path in statics:
        lines.append(f"- `static/{os.path.basename(path)}` - {style} instance")
    if statics:
        lines.append("  (static instances: fontTools instancer; overlaps removed in the new simple glyphs only)")
    lines += ["", "## Acknowledgements", "",
              f"Original design: the {cfg['family_name']} Project Authors. "
              "Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).", ""]
    with open(os.path.join(out_dir, "FONTLOG.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def write_fontlog_multi(cfg, out_dir, results):
    today = cfg.get("date") or datetime.date(2026, 10, 13).isoformat()
    vers = sorted({r["orig_version"] for r in results})
    lines = [
        f"# FONTLOG for {cfg['new_family_name']}",
        "",
        f"{cfg['new_family_name']} is a modified version of **{cfg['family_name']}** "
        f"v{'/'.join(vers)} ({cfg.get('upstream', '')}), released under the SIL Open Font "
        "License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.",
        "",
    ]
    if cfg.get("license_note"):
        lines += [cfg["license_note"], ""]
    lines += ["## Changelog", "", f"### {today} - {cfg['version_suffix']} - Font Shuugch project", "",
              "Added the letters Mongolian Cyrillic needs that the original lacks. "
              "No existing glyph was altered.", ""]
    if any(r["info"].get("default_locl") for r in results):
        lines += _locl_lines(results[0]["info"], True)
    for n in cfg.get("release_notes", []):
        lines.append(f"- {n}")
    for r in results:
        info = r["info"]
        lines += ["", f"#### `{info['file']}` (from `{os.path.basename(info['source'])}`)", ""]
        lines += _locl_lines(info)
        if info["slant"]:
            lines.append(f"Italic: new outlines constructed upright and re-slanted by "
                         f"{math.degrees(math.atan(info['slant'])):.1f} deg (the font's own slant).")
            lines.append("")
        skipped = [g for g in cfg["glyphs"] if g not in r["todo"]]
        if skipped:
            lines.append("Already in the original (left untouched): " + ", ".join(
                f"U+{cfg['glyphs'][g]['unicode']} {chr(int(cfg['glyphs'][g]['unicode'], 16))}" for g in skipped))
            lines.append("")
        lines += _glyph_lines(r["todo"], r["built"], r["extra_alts"])
    lines += ["", "## Method", "",
              "tools/build_mn.py with tools/families/" + cfg["family_id"] + ".json (same pipeline and "
              "review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a "
              "bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; "
              "₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.",
              "", "## Files", ""]
    for r in results:
        lines.append(f"- `{r['info']['file']}` - {'variable' if r['info']['variable'] else 'static'} font")
        for style, coords, path in r["statics"]:
            lines.append(f"  - `static/{os.path.basename(path)}` - {style}")
    lines += ["", "## Acknowledgements", "",
              f"Original design: the {cfg['family_name']} Project Authors. "
              "Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).", ""]
    with open(os.path.join(out_dir, "FONTLOG.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", help="family JSON, e.g. tools/families/unbounded.json")
    ap.add_argument("--no-statics", action="store_true", help="skip static instances (quick iteration)")
    a = ap.parse_args()
    build(a.config, a.no_statics)
