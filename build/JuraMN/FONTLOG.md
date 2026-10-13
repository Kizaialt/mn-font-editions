# FONTLOG for Jura MN

Jura MN is a modified version of **Jura** v5.106 (https://github.com/ossobuffo/jura), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Jura MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `JuraMN[wght].ttf` (from `Jura[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 84.0, centre y=636.0, x 172..976 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 84.0, centre y=461.0, x 166..970 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 84.0 ('uni0440' 84.0, deslanted), down to y=-364.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=8.8; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 84.0, join_y 8.8; wght=+1: stem 168.0, join_y 42.9
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 84.0 (= 1.00 x crossbar 84), angle 20 deg, x 228..876 (62% of the crossbar), centre lines cross the stem axis at y=353.4 and y=751.4; white gaps baseline/between/crossbar = (192.9, 308.7, 270.1) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 84.0, angle 20, stroke_x (228, 876), gaps (192.9, 308.7, 270.1); wght=+1: stroke_thickness 131.0, angle 20, stroke_x (269, 959), gaps (150.0, 264.2, 242.0)
  - heaviest master (wght=+1, heavy rule): thickness 131.0 (0.78 x crossbar), 20 deg, x 269..959 (protrudes 260.7 past the stem), gaps (150.0, 264.2, 242.0); family internal gaps {'Euro': 78.0, 'yen': 72.0, 'e': 240.0} -> rule minimum 86.4

## Method

tools/build_mn.py with tools/families/jura.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `JuraMN[wght].ttf` - variable font
  - `static/JuraMN-Light.ttf` - Light
  - `static/JuraMN-Regular.ttf` - Regular
  - `static/JuraMN-Medium.ttf` - Medium
  - `static/JuraMN-SemiBold.ttf` - SemiBold
  - `static/JuraMN-Bold.ttf` - Bold

## Acknowledgements

Original design: the Jura Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
