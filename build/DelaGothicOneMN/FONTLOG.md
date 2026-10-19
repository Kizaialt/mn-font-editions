# FONTLOG for Dela Gothic One MN

Dela Gothic One MN is a modified version of **Dela Gothic One** v1.005 (https://github.com/syakuzen/DelaGothic), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Dela Gothic One MN' so it never clashes with the original.

## Changelog

### 2026-10-19 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `DelaGothicOneMN-Regular.ttf` (from `DelaGothicOne-Regular.ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 158.6, centre y=368.5, x 161..810 (default); kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 75.3, centre y=273.0, x 137..599 (default); kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 244.2 ('uni0440' 221.8, deslanted), down to y=-232.0; outer arm edges (curved: continued along their end tangents) to meet a stem of 'uni0440''s width at y=-104.4; stem widened where the join would sit deeper than 0.45 x descender; flat end cut at 'uni0440''s depth (its descender sides are curved, so no terminal is copied); kerning from `uni0443`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 119.9 (= 0.58 x crossbar 206), angle 17.5 deg, x 203..735 (62% of the crossbar), centre lines cross the stem axis at y=172.0 and y=337.9; white gaps baseline/between/crossbar = (25.1, 40.2, 35.2) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/delagothicone.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `DelaGothicOneMN-Regular.ttf` - static font

## Acknowledgements

Original design: the Dela Gothic One Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
