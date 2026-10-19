# FONTLOG for Alto Sans MN

Alto Sans MN is a modified version of **Tenor Sans** v1.001 (https://github.com/googlefonts/googlefontdirectory-hg), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

RESERVED FONT NAME: the original OFL.txt reserves the names 'Tenor' and 'Tenor Sans' (Copyright (c) 2011, Denis Masharov, with Reserved Font Name "Tenor", "Tenor Sans"). A modified version may not use the reserved names, so this edition is released as 'Alto Sans MN' (files AltoSansMN-*.ttf) and its font names (family, full, PostScript, unique ID, trademark line) no longer contain the word 'Tenor'; the original author is credited in the copyright notice and below. NameID 0 (the copyright notice) keeps the original line verbatim, because the OFL requires the copyright notice to be retained; every other name record is renamed.

## Changelog

### 2026-10-19 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `AltoSansMN-Regular.ttf` (from `TenorSans-Regular.ttf`)

Contour direction: the original's outlines of `T`, `Y`, `uni041D`, `uni041E`, `uni043D`, `uni0440`, `v` run counter-clockwise (PostScript order); the new glyphs are built in TrueType order (clockwise outer contours), the original glyphs are left as they are.

Removed the optional per-glyph device tables `hdmx`, `LTSH` (they have no entries for the new glyphs; renderers compute these values themselves).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 46.0, centre y=350.0, x 99..766 (default); kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 34.0, centre y=249.5, x 98..520 (default); kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 85.0 ('uni0440' 85.0, deslanted), down to y=-250.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=30.5; kerning from `uni0443`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 42.9 (= 0.78 x crossbar 55), angle 20 deg, x 139..528 (62% of the crossbar), centre lines cross the stem axis at y=196.6 and y=407.2; white gaps baseline/between/crossbar = (103.1, 164.9, 144.3) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/tenorsans.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `AltoSansMN-Regular.ttf` - static font

## Acknowledgements

Original design: the Tenor Sans Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
