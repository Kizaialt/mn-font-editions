"""Rename a font family for an OFL-modified version ("<Family> MN")."""
from __future__ import annotations

import re


def _mac_ok(c):
    try:
        c.encode("mac_roman")
        return True
    except UnicodeEncodeError:
        return False


def rename_family(font, cfg, log):
    old, new = cfg["family_name"], cfg["new_family_name"]
    old_ps, new_ps = old.replace(" ", ""), new.replace(" ", "")
    suffix = cfg["version_suffix"]                 # e.g. "MN 0.1"
    tag = suffix.replace(" ", "")                   # e.g. "MN0.1"
    name = font["name"]
    rev = font["head"].fontRevision
    ver = f"{rev:.3f}"
    changes = {}

    def sub_family(s):
        return s.replace(old, new, 1) if s.startswith(old) else s

    def sub_ps(s):
        return s.replace(old_ps, new_ps, 1) if s.startswith(old_ps) else s

    for rec in list(name.names):
        nid = rec.nameID
        try:
            s = rec.toUnicode()
        except UnicodeDecodeError:
            continue
        ns = s
        if nid in (1, 4, 16, 21):
            ns = sub_family(s)
        elif nid in (6, 25):
            ns = sub_ps(s)
        elif nid == 3:
            parts = s.split(";")
            parts = [sub_ps(p) for p in parts]
            if tag not in parts:
                parts.insert(1, tag)
            ns = ";".join(parts)
        elif nid == 5:
            m = re.match(r"(Version \d+\.\d+)", s)
            ns = f"{m.group(1) if m else 'Version ' + ver};{suffix}"
        elif nid == 0:
            add = cfg.get("copyright_append")
            if add and add not in s:
                ns = s.rstrip() + ("" if s.rstrip().endswith(".") else ".") + " " + add
        if ns != s:
            if rec.platformID == 1:
                try:
                    ns.encode("mac_roman")
                except UnicodeEncodeError:
                    if nid != 0:
                        continue
                    # Mac Roman cannot hold the new letters: spell them as code points in the copyright note
                    ns = "".join(c if _mac_ok(c) else f"U+{ord(c):04X}" for c in ns)
            rec.string = ns
            changes.setdefault(nid, (s, ns))
    # Reserved Font Name: when the OFL.txt reserves the original name, no name record may carry it
    # any more.  The copyright notice (nameID 0) is kept verbatim: the OFL requires it to be retained.
    rfn = cfg.get("reserved_font_name")
    if rfn:
        overrides = {int(k): v for k, v in cfg.get("name_overrides", {}).items()}
        pat = re.compile(re.escape(rfn), re.I)
        for rec in name.names:
            nid = rec.nameID
            if nid == 0:
                continue
            try:
                s = rec.toUnicode()
            except UnicodeDecodeError:
                continue
            if nid in overrides:
                ns = overrides[nid]
            elif pat.search(s):
                ns = pat.sub(new_ps if nid in (3, 6, 25) else new, s)
            else:
                continue
            if ns != s:
                rec.string = ns
                changes.setdefault(nid, (s, ns))
    for nid, (a, b) in sorted(changes.items()):
        log.append(f"name {nid}: {a!r} -> {b!r}")
    # fvar named instances: PostScript names only if present
    if "fvar" in font:
        for inst in font["fvar"].instances:
            if inst.postscriptNameID not in (0xFFFF, None):
                rec = name.getName(inst.postscriptNameID, 3, 1, 0x409)
                if rec:
                    rec.string = sub_ps(rec.toUnicode())
    # sanity: no record still starts with the old family where it should not
    leftovers = [(r.nameID, r.toUnicode()) for r in name.names
                 if r.nameID in (1, 4, 6, 16, 21, 25)
                 and (r.toUnicode().startswith(old) and not r.toUnicode().startswith(new))
                 and not (r.nameID in (6, 25) and r.toUnicode().startswith(new_ps))]
    if leftovers:
        raise ValueError(f"rename incomplete: {leftovers}")
    if rfn:
        bad = [(r.nameID, r.toUnicode()) for r in name.names
               if r.nameID != 0 and rfn.lower() in r.toUnicode().lower()]
        if bad:
            raise ValueError(f"reserved font name '{rfn}' still present: {bad}")
