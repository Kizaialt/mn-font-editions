"""OpenType Layout updates for added glyphs.

Each new glyph may name an `otl_base`: an existing glyph whose kerning,
mark-attachment anchors and contextual-lookup membership it inherits.
New glyphs are appended at the end of the glyph order, so appending them
to coverage tables keeps those tables sorted by glyph ID.
"""
from __future__ import annotations

import copy


def _subtables(table, want_types):
    """Yield (lookup_index, real_type, subtable), unwrapping extensions."""
    for li, lk in enumerate(table.LookupList.Lookup):
        for st in lk.SubTable:
            t = lk.LookupType
            if hasattr(st, "ExtSubTable"):
                t = st.ExtensionLookupType
                st = st.ExtSubTable
            if t in want_types:
                yield li, t, st


def clone_kerning(font, pairs, log):
    """pairs: list of (new_glyph, otl_base), new glyphs in glyph-ID order."""
    if "GPOS" not in font:
        return
    gpos = font["GPOS"].table
    subs = [(li, st) for li, t, st in _subtables(gpos, {2})]
    # phase A: new glyph as FIRST glyph
    for new, base in pairs:
        n1 = 0
        for li, st in subs:
            cov = st.Coverage.glyphs
            if base not in cov:
                continue
            if st.Format == 1:
                ps = copy.deepcopy(st.PairSet[cov.index(base)])
                cov.append(new)
                st.PairSet.append(ps)
                st.PairSetCount = len(st.PairSet)
                n1 += len(ps.PairValueRecord)
            else:
                cov.append(new)
                c1 = st.ClassDef1.classDefs
                if base in c1:
                    c1[new] = c1[base]
                n1 += 1
        log.append(f"kern: {new} as 1st glyph cloned from {base} ({n1} pair records/class rows)")
    # phase B: new glyph as SECOND glyph
    for new, base in pairs:
        n2 = 0
        for li, st in subs:
            if st.Format == 1:
                for ps in st.PairSet:
                    for r in list(ps.PairValueRecord):
                        if r.SecondGlyph == base:
                            r2 = copy.deepcopy(r)
                            r2.SecondGlyph = new
                            ps.PairValueRecord.append(r2)
                            ps.PairValueCount = len(ps.PairValueRecord)
                            n2 += 1
            else:
                c2 = st.ClassDef2.classDefs
                if base in c2:
                    c2[new] = c2[base]
                    n2 += 1
        log.append(f"kern: {new} as 2nd glyph cloned from {base} ({n2} pair records/classes)")


def clone_marks(font, pairs, log):
    if "GPOS" not in font:
        return
    gpos = font["GPOS"].table
    for new, base in pairs:
        n = 0
        for li, t, st in _subtables(gpos, {4}):
            cov = st.BaseCoverage.glyphs
            if base in cov:
                rec = copy.deepcopy(st.BaseArray.BaseRecord[cov.index(base)])
                cov.append(new)
                st.BaseArray.BaseRecord.append(rec)
                st.BaseArray.BaseCount = len(st.BaseArray.BaseRecord)
                n += 1
        log.append(f"mark: {new} base anchors cloned from {base} ({n} subtables)")


def clone_context_membership(font, pairs, log):
    """Add new glyphs next to their otl_base in backtrack/look-ahead
    coverages (format 3) and class defs (format 2) of chaining contextual
    lookups, so neighbouring-glyph rules treat them like the base."""
    for tag, ctx_types in (("GSUB", {6}), ("GPOS", {8})):
        if tag not in font:
            continue
        table = font[tag].table
        for new, base in pairs:
            hits = []
            for li, t, st in _subtables(table, ctx_types):
                if st.Format == 3:
                    for attr in ("BacktrackCoverage", "LookAheadCoverage"):
                        for cov in getattr(st, attr) or []:
                            if base in cov.glyphs and new not in cov.glyphs:
                                cov.glyphs.append(new)
                                hits.append(f"{li}:{attr[:4]}")
                elif st.Format == 2:
                    for attr in ("BacktrackClassDef", "LookAheadClassDef"):
                        cd = getattr(st, attr, None)
                        if cd is not None and base in cd.classDefs:
                            cd.classDefs[new] = cd.classDefs[base]
                            hits.append(f"{li}:{attr[:4]}")
                else:
                    pass  # format 1 (glyph sequences): not cloned
            if hits:
                log.append(f"{tag} context: {new} added beside {base} in lookups {sorted(set(hits))}")


def feature_variation_alternates(font, component_base):
    """Return {alt_glyph: [lookup indices]} for FeatureVariations
    (e.g. 'BRACKET' glyphs) substituting `component_base`."""
    if "GSUB" not in font:
        return {}
    gsub = font["GSUB"].table
    fv = getattr(gsub, "FeatureVariations", None)
    if fv is None:
        return {}
    lookups = set()
    for rec in fv.FeatureVariationRecord:
        for sr in rec.FeatureTableSubstitution.SubstitutionRecord:
            lookups.update(sr.Feature.LookupListIndex)
    out = {}
    for li, t, st in _subtables(gsub, {1}):
        if li in lookups and component_base in st.mapping:
            out.setdefault(st.mapping[component_base], []).append(li)
    return out


def add_feature_variation_mapping(font, new, new_alt, component_base, lookup_indices, log):
    gsub = font["GSUB"].table
    for li, t, st in _subtables(gsub, {1}):
        if li in lookup_indices and component_base in st.mapping:
            st.mapping[new] = new_alt
    log.append(f"GSUB FeatureVariations: {new} -> {new_alt} in lookups {sorted(set(lookup_indices))}")


# ==========================================================================
# Explicit pair kerning (look-alike mapping, selective cloning, caps)
# ==========================================================================
#
# Pairs that must differ from what class-cloning gives are written to a NEW
# PairPos format-1 subtable inserted FIRST in each kerning lookup.  A
# format-1 subtable only fires when it has a record for the exact pair;
# otherwise the lookup falls through to the original subtables, so kerning
# between existing glyphs is unaffected.

import unicodedata

from fontTools.ttLib.tables import otTables as ot
from fontTools.ttLib.tables.otBase import ValueRecord


def kern_lookup_indices(font):
    if "GPOS" not in font:
        return []
    gpos = font["GPOS"].table
    idx = set()
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag in ("kern", "dist"):
            idx.update(fr.Feature.LookupListIndex)
    out = []
    for li in sorted(idx):
        if any(t == 2 for _, t, _ in _lookup_subtables(gpos.LookupList.Lookup[li])):
            out.append(li)
    return out


def _lookup_subtables(lk):
    for st in lk.SubTable:
        t = lk.LookupType
        if hasattr(st, "ExtSubTable"):
            t, st = st.ExtensionLookupType, st.ExtSubTable
        yield st, t, lk


def pair_value(lookup, g1, g2):
    """(Value1, Value2) the lookup applies to the pair g1 g2: first
    subtable that covers g1 and (format 1) has a record for g2."""
    for st, t, _ in _lookup_subtables(lookup):
        if t != 2:
            continue
        cov = st.Coverage.glyphs
        if g1 not in cov:
            continue
        if st.Format == 1:
            for r in st.PairSet[cov.index(g1)].PairValueRecord:
                if r.SecondGlyph == g2:
                    return getattr(r, "Value1", None), getattr(r, "Value2", None)
            continue
        c1 = st.ClassDef1.classDefs.get(g1, 0)
        c2 = st.ClassDef2.classDefs.get(g2, 0)
        rec = st.Class1Record[c1].Class2Record[c2]
        return getattr(rec, "Value1", None), getattr(rec, "Value2", None)
    return None, None


def _vsig(v):
    if v is None:
        return ()
    out = []
    for name in ("XPlacement", "YPlacement", "XAdvance", "YAdvance"):
        val = getattr(v, name, 0) or 0
        if val:
            out.append((name, val))
    for name in ("XPlaDevice", "YPlaDevice", "XAdvDevice", "YAdvDevice"):
        d = getattr(v, name, None)
        if d is not None:
            out.append((name, d.DeltaFormat, d.StartSize, d.EndSize))
    return tuple(out)


def _pairsig(vv):
    return (_vsig(vv[0]), _vsig(vv[1]))


def _zero():
    v = ValueRecord()
    v.XAdvance = 0
    return v


def insert_front_pairs(font, li, pairs, log, label):
    """pairs: {(g1, g2): (Value1, Value2)} -> new format-1 subtable first in lookup li."""
    if not pairs:
        return
    gpos = font["GPOS"].table
    lk = gpos.LookupList.Lookup[li]
    vf1 = vf2 = 0
    for v1, v2 in pairs.values():
        vf1 |= v1.getFormat() if v1 is not None else 0
        vf2 |= v2.getFormat() if v2 is not None else 0
    if vf1 == 0:
        vf1 = 0x0004
    gid = font.getGlyphID
    st = ot.PairPos()
    st.Format = 1
    st.ValueFormat1, st.ValueFormat2 = vf1, vf2
    st.Coverage = ot.Coverage()
    firsts = sorted({a for a, _ in pairs}, key=gid)
    st.Coverage.glyphs = firsts
    st.PairSet = []
    for g1 in firsts:
        ps = ot.PairSet()
        ps.PairValueRecord = []
        for g2 in sorted((b for a, b in pairs if a == g1), key=gid):
            v1, v2 = pairs[(g1, g2)]
            r = ot.PairValueRecord()
            r.SecondGlyph = g2
            r.Value1 = copy.deepcopy(v1) if v1 is not None else _zero()
            if vf2:
                r.Value2 = copy.deepcopy(v2) if v2 is not None else ValueRecord()
            ps.PairValueRecord.append(r)
        ps.PairValueCount = len(ps.PairValueRecord)
        st.PairSet.append(ps)
    st.PairSetCount = len(st.PairSet)
    if lk.LookupType == 9:
        ext = ot.ExtensionPos()
        ext.Format = 1
        ext.ExtensionLookupType = 2
        ext.ExtSubTable = st
        lk.SubTable.insert(0, ext)
    else:
        lk.SubTable.insert(0, st)
    lk.SubTableCount = len(lk.SubTable)
    log.append(f"kern: {label}: {len(pairs)} explicit pairs in a new first subtable of lookup {li}")


def feature_variation_alts(font, glyph):
    """Glyphs that `glyph` is swapped to by GSUB FeatureVariations rules."""
    if "GSUB" not in font:
        return []
    gsub = font["GSUB"].table
    fv = getattr(gsub, "FeatureVariations", None)
    if fv is None:
        return []
    lookups = set()
    for rec in fv.FeatureVariationRecord:
        for sr in rec.FeatureTableSubstitution.SubstitutionRecord:
            lookups.update(sr.Feature.LookupListIndex)
    alts = []
    for li, t, st in _subtables(gsub, {1}):
        if li in lookups and glyph in st.mapping and st.mapping[glyph] not in alts:
            alts.append(st.mapping[glyph])
    return alts


def _variants(font, glyph):
    """glyph + every glyph named glyph.<suffix> (e.g. hyphen.case, four.tf)."""
    order = font.getGlyphOrder()
    return [glyph] + [g for g in order if g.startswith(glyph + ".")]


def _total_kern(font, lookups, g1, g2):
    return sum((getattr(pair_value(font["GPOS"].table.LookupList.Lookup[li], g1, g2)[0], "XAdvance", 0) or 0)
               for li in lookups)


def kerning_shared(font, twin, mapping, cmap, exclude=()):
    """Do Latin and Cyrillic look-alikes share kerning (same classes or
    cross-script pairs)?  Compares twin+Latin vs twin+Cyrillic for every
    letter in the look-alike map, on both sides.  Returns (bool, detail)."""
    lookups = kern_lookup_indices(font)
    n = same = 0
    examples = []
    for c, l in mapping.items():
        if c == l or not c.isalpha():
            continue
        gc, gl = cmap.get(ord(c)), cmap.get(ord(l))
        if not gc or not gl or gc in exclude:     # glyphs being added have no kerning yet
            continue
        for a, b in (((twin, gl), (twin, gc)), ((gl, twin), (gc, twin))):
            kl, kc = _total_kern(font, lookups, *a), _total_kern(font, lookups, *b)
            if kl:
                n += 1
                same += kl == kc
                if kl != kc and len(examples) < 3:
                    examples.append(f"{a[0]}+{a[1]} {kl} vs {b[0]}+{b[1]} {kc}")
    shared = n > 0 and same / n >= 0.8
    return shared, f"{same}/{n} look-alike pairs kern alike ({'; '.join(examples)})"


def _script_kern_lookups(font, tag):
    gpos = font["GPOS"].table
    for sr in gpos.ScriptList.ScriptRecord:
        if sr.ScriptTag == tag and sr.Script.DefaultLangSys is not None:
            out = []
            for fi in sr.Script.DefaultLangSys.FeatureIndex:
                fr = gpos.FeatureList.FeatureRecord[fi]
                if fr.FeatureTag in ("kern", "dist"):
                    out += [li for li in fr.Feature.LookupListIndex if li not in out]
            return out
    return None


def script_lookup_map(font, dst_scripts, src_script="latn"):
    """[(dst_lookup, src_lookup)]: where the values of a Latin pair must be
    read from (src) and where the new pair must be written (dst) so that it
    is active when the new glyph is shaped in `dst_scripts` text.  Lookups
    shared by both scripts map to themselves; script-specific lookups map
    positionally (e.g. Yanone Kaffeesatz: cyrl [3, 1] / latn [3, 2] -> 1<-2).
    Fonts without per-script kerning give the identity over all kern lookups."""
    allk = kern_lookup_indices(font)
    src = _script_kern_lookups(font, src_script) or _script_kern_lookups(font, "DFLT") or allk
    pairs = []
    for ds in dst_scripts:
        dst = _script_kern_lookups(font, ds)
        if dst is None:
            continue
        shared = [l for l in dst if l in src]
        d_only = [l for l in dst if l not in src]
        s_only = [l for l in src if l not in dst]
        cand = [(l, l) for l in shared]
        if len(d_only) == len(s_only):
            cand += list(zip(d_only, s_only))
        for d, s_ in cand:
            if d in allk and s_ in allk and all(d != x for x, _ in pairs):
                pairs.append((d, s_))
    if not pairs:
        pairs = [(l, l) for l in allk]
    return sorted(pairs)


def script_gaps(font, dst_scripts, src_script="latn"):
    """[(dst_script, [src lookups])]: Latin kern lookups that text in dst_script
    never reaches because that script's kern feature lists fewer lookups (e.g. Bona
    Nova: DFLT kern = [1], latn/cyrl = [1, 2, 3]) and that script_lookup_map could not
    pair up positionally.  Pairs added for a new glyph would be silent there."""
    allk = kern_lookup_indices(font)
    src = _script_kern_lookups(font, src_script) or _script_kern_lookups(font, "DFLT") or allk
    out = []
    for ds in dst_scripts:
        dst = _script_kern_lookups(font, ds)
        if dst is None:
            continue
        d_only = [l for l in dst if l not in src]
        s_only = [l for l in src if l not in dst]
        if len(d_only) == len(s_only):
            continue
        miss = [l for l in s_only if l in allk]
        if miss:
            out.append((ds, miss))
    return out


def add_gap_lookup(font, script, pairs, log, label):
    """New kern lookup holding `pairs`, appended to the kern feature(s) that `script` uses
    by default - so the pairs also work for text shaped in that script."""
    if not pairs:
        return
    gpos = font["GPOS"].table
    lk = ot.Lookup()
    lk.LookupType, lk.LookupFlag, lk.SubTable, lk.SubTableCount = 2, 0, [], 0
    gpos.LookupList.Lookup.append(lk)
    gpos.LookupList.LookupCount = len(gpos.LookupList.Lookup)
    li = len(gpos.LookupList.Lookup) - 1
    insert_front_pairs(font, li, pairs, log, f"{label} (new lookup {li} for {script} text)")
    for sr in gpos.ScriptList.ScriptRecord:
        if sr.ScriptTag == script and sr.Script.DefaultLangSys is not None:
            for fi in sr.Script.DefaultLangSys.FeatureIndex:
                fr = gpos.FeatureList.FeatureRecord[fi]
                if fr.FeatureTag == "kern" and li not in fr.Feature.LookupListIndex:
                    fr.Feature.LookupListIndex.append(li)
                    fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)


def lookalike_kerning(font, new, spec, log):
    """Ү-style kerning: partners that have a Latin look-alike get the Latin
    twin's value with that look-alike (Ү+е = Y+e, А+Ү = A+Y ...), both as
    left and right member; everything else keeps the fallback (class-cloned)
    values.  FeatureVariations alternates of partners (e.g. heavy-weight
    'BRACKET' е) are mapped to the look-alike's alternate."""
    cmap = font.getBestCmap()
    twin = spec["latin_twin"]
    keep = spec.get("keep_fallback", {})
    keep_l = {cmap.get(ord(c)) for c in keep.get("as_left", [])}
    keep_r = {cmap.get(ord(c)) for c in keep.get("as_right", [])}
    gpos = font["GPOS"].table
    dst_scripts = ["cyrl"] if _script_kern_lookups(font, "cyrl") is not None else ["DFLT"]
    for li, si in script_lookup_map(font, dst_scripts):
        lk = gpos.LookupList.Lookup[li]
        sk = gpos.LookupList.Lookup[si]
        pairs = {}
        for c, l in spec["map"].items():
            gc, gl = cmap.get(ord(c)), cmap.get(ord(l))
            if not gc or not gl:
                continue
            cands = [(v, v.replace(gc, gl, 1) if v != gc else gl) for v in
                     (_variants(font, gc) if c == l else [gc])]
            gl_alts = feature_variation_alts(font, gl)
            for ga in feature_variation_alts(font, gc):
                cands.append((ga, gl_alts[0] if gl_alts else gl))
            for pc, pl in cands:
                if pl not in font.getGlyphOrder():
                    pl = gl
                if gc not in keep_l:
                    want = pair_value(sk, twin, pl)
                    if _pairsig(want) != _pairsig(pair_value(lk, new, pc)):
                        pairs[(new, pc)] = want
                if gc not in keep_r:
                    want = pair_value(sk, pl, twin)
                    if _pairsig(want) != _pairsig(pair_value(lk, pc, new)):
                        pairs[(pc, new)] = want
        insert_front_pairs(font, li, pairs, log, f"{new} look-alike pairs from {twin}")


# ---- variable values (caps) ----------------------------------------------

def _region_index(store, support, axis_order):
    regions = store.VarRegionList.Region
    want = [support.get(a, (0.0, 0.0, 0.0)) for a in axis_order]
    for i, r in enumerate(regions):
        have = [(ax.StartCoord, ax.PeakCoord, ax.EndCoord) for ax in r.VarRegionAxis]
        if all(abs(x - y) < 1e-4 for h, w in zip(have, want) for x, y in zip(h, w)):
            return i
    reg = ot.VarRegion()
    reg.VarRegionAxis = []
    for s, p, e in want:
        ax = ot.VarRegionAxis()
        ax.StartCoord, ax.PeakCoord, ax.EndCoord = s, p, e
        reg.VarRegionAxis.append(ax)
    regions.append(reg)
    store.VarRegionList.RegionCount = len(regions)
    return len(regions) - 1


def variable_value(font, masters, per_master):
    """ValueRecord whose XAdvance takes per_master[i] at masters[i]
    (normalized locations, default first) - deltas stored in GDEF VarStore."""
    from fontTools.varLib.models import VariationModel
    from fontTools.varLib import builder as _vb  # noqa: F401  (registers VarData.calculateNumShorts)
    if "fvar" not in font or len(masters) == 1:
        v = ValueRecord()
        v.XAdvance = round(per_master[0])
        return v
    axis_order = [a.axisTag for a in font["fvar"].axes]
    model = VariationModel(masters, axisOrder=axis_order)
    deltas = [round(d) for d in model.getDeltas(per_master)]
    v = ValueRecord()
    v.XAdvance = deltas[0]
    if not any(deltas[1:]):
        return v
    store = font["GDEF"].table.VarStore
    ridx = [_region_index(store, sup, axis_order) for sup in model.supports[1:]]
    row = deltas[1:]
    vd_i = next((i for i, vd in enumerate(store.VarData) if list(vd.VarRegionIndex) == ridx), None)
    if vd_i is None:
        vd = ot.VarData()
        vd.VarRegionIndex, vd.VarRegionCount, vd.Item, vd.ItemCount, vd.NumShorts = ridx, len(ridx), [], 0, 0
        store.VarData.append(vd)
        store.VarDataCount = len(store.VarData)
        vd_i = len(store.VarData) - 1
    vd = store.VarData[vd_i]
    vd.Item.append(list(row))
    vd.ItemCount = len(vd.Item)
    vd.calculateNumShorts(optimize=False)
    dev = ot.Device()
    dev.DeltaFormat = 0x8000
    dev.StartSize, dev.EndSize = vd_i, vd.ItemCount - 1
    v.XAdvDevice = dev
    return v


def value_at(font, v, loc):
    """Evaluate a ValueRecord's XAdvance at a normalized location."""
    from fontTools.varLib.models import supportScalar
    if v is None:
        return 0
    x = getattr(v, "XAdvance", 0) or 0
    d = getattr(v, "XAdvDevice", None)
    if d is None or d.DeltaFormat != 0x8000 or "fvar" not in font:
        return x
    store = font["GDEF"].table.VarStore
    vd = store.VarData[d.StartSize]
    row = vd.Item[d.EndSize]
    axis_order = [a.axisTag for a in font["fvar"].axes]
    for ri, delta in zip(vd.VarRegionIndex, row):
        reg = store.VarRegionList.Region[ri]
        sup = {a: (ax.StartCoord, ax.PeakCoord, ax.EndCoord)
               for a, ax in zip(axis_order, reg.VarRegionAxis) if ax.PeakCoord}
        x += delta * supportScalar(loc, sup)
    return x


def digit_punct_glyphs(font):
    """Glyphs for Unicode digits (Nd) and punctuation (P*), plus their
    named variants (.tf, .case, .dnom ...)."""
    out = []
    for cp, g in sorted(font.getBestCmap().items()):
        cat = unicodedata.category(chr(cp))
        if cat == "Nd" or cat.startswith("P"):
            for v in _variants(font, g):
                if v not in out:
                    out.append(v)
    return out


def selective_kerning(font, new, spec, masters, log):
    """₮-style kerning: copy the values of `glyph` (e.g. Latin T) but only
    against digits and punctuation, both sides; optional per-partner caps
    {partner_base: {"wght=1": -40, "default": -60, ...}} limit how far the
    copied value may tighten (applied to the partner's variants too)."""
    from .construct import _parse_loc
    src = spec["glyph"]
    partners = digit_punct_glyphs(font)
    caps = {}
    for pb, cm in spec.get("caps", {}).items():
        if pb.startswith("_"):
            continue
        if "ratio" in cm:       # generic rule: at most `ratio` x the source glyph's own value
            lim = ("ratio", float(cm["ratio"]))
        else:                   # reviewed per-master numbers
            lim = {_parse_loc(k): v for k, v in cm.items() if not k.startswith("_")}
        for v in _variants(font, pb):
            caps[v] = lim
    capped = {}
    gpos = font["GPOS"].table

    def collect(lk, record):
        pairs = {}
        for p in partners:
            for (a, b), key in (((src, p), (new, p)), ((p, src), (p, new))):
                v1, v2 = pair_value(lk, a, b)
                if not _vsig(v1) and not _vsig(v2):
                    continue
                if key[0] == new and p in caps:
                    from .outline import loc_key
                    lim = caps[p]
                    vals = []
                    for m in masters:
                        cur = value_at(font, v1, m)
                        if isinstance(lim, tuple):
                            cap = round(lim[1] * cur) if cur < 0 else cur
                        else:
                            cap = lim.get(loc_key(m))
                        if cap is None:
                            raise ValueError(f"cap for {p} has no value at master {m}")
                        vals.append(max(cur, cap))
                    v1 = variable_value(font, masters, vals)
                    if record:      # a pair kerned in several lookups: the recorded cap is their sum
                        if p in capped:
                            capped[p] = [[m, w + x] for (m, w), x in zip(capped[p], vals)]
                        else:
                            capped[p] = [[dict(m), v] for m, v in zip(masters, vals)]
                        log.append(f"kern: {new}+{p} capped: {src}+{p} -> per-master values {vals}")
                pairs[key] = (v1, v2)
        return pairs

    for li, si in script_lookup_map(font, ["cyrl", "DFLT"]):
        pairs = collect(gpos.LookupList.Lookup[si], True)   # read the source glyph's values here
        insert_front_pairs(font, li, pairs, log, f"{new} digit/punctuation pairs from {src}")
    for ds, miss in script_gaps(font, ["cyrl", "DFLT"]):
        for si in miss:
            add_gap_lookup(font, ds, collect(gpos.LookupList.Lookup[si], False), log,
                           f"{new} digit/punctuation pairs from {src} (lookup {si})")
    return capped
