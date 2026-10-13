# FONTLOG for Alumni Sans SC MN

Alumni Sans SC MN is a modified version of **Alumni Sans SC** v1.016/1.018 (https://github.com/googlefonts/alumni), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Alumni Sans SC MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `AlumniSansSCMN[wght].ttf` (from `AlumniSansSC[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 20.0, centre y=293.5, x 78..330 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 20.0, centre y=248.0, x 61..279 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 23.0 ('uni0440' 23.0, deslanted), down to y=-116.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-8.3; stem widened where the join would sit deeper than 0.25 x descender; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 23.0, join_y -8.3; wght=+1: stem 175.5, join_y -29.0
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 19.0 (= 1.00 x crossbar 19), angle 20 deg, x 56..202 (62% of the crossbar), centre lines cross the stem axis at y=156.4 and y=367.8; white gaps baseline/between/crossbar = (119.5, 191.2, 167.3) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 19.0, angle 20, stroke_x (56, 202), gaps (119.5, 191.2, 167.3); wght=+1: stroke_thickness 86.6, angle 20, stroke_x (13, 332), gaps (39.4, 72.5, 67.6)
  - heaviest master (wght=+1, heavy rule): thickness 86.6 (0.78 x crossbar), 20 deg, x 13..332 (protrudes 80.1 past the stem), gaps (39.4, 72.5, 67.6); family internal gaps {'Euro': 28.0, 'e': 113.0} -> rule minimum 33.6

#### `AlumniSansSCMN-Italic[wght].ttf` (from `AlumniSansSC-Italic[wght].ttf`)

Italic: new outlines constructed upright and re-slanted by 8.0 deg (the font's own slant).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 20.0, centre y=293.5, x 85..337 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 20.0, centre y=248.0, x 61..279 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 26.0 ('uni0440' 23.1, deslanted), down to y=-116.0; stem hangs straight down from the v's own bottom corners (curved arms); italic slant 8.0 deg; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 26.0, join_y 0.0; wght=+1: stem 150.0, join_y 0.0
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 19.0 (= 1.00 x crossbar 19), angle 20 deg, x 21..168 (62% of the crossbar), centre lines cross the stem axis at y=156.4 and y=367.8; white gaps baseline/between/crossbar = (119.5, 191.2, 167.3) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 19.0, angle 20, stroke_x (21, 168), gaps (119.5, 191.2, 167.3); wght=+1: stroke_thickness 86.6, angle 20, stroke_x (-22, 297), gaps (39.4, 72.4, 67.6)
  - heaviest master (wght=+1, heavy rule): thickness 86.6 (0.78 x crossbar), 20 deg, x -22..297 (protrudes 80.3 past the stem), gaps (39.4, 72.4, 67.6); family internal gaps {'Euro': 28.0, 'e': 117.8} -> rule minimum 33.6

## Method

tools/build_mn.py with tools/families/alumnisanssc.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `AlumniSansSCMN[wght].ttf` - variable font
  - `static/AlumniSansSCMN-Thin.ttf` - Thin
  - `static/AlumniSansSCMN-ExtraLight.ttf` - ExtraLight
  - `static/AlumniSansSCMN-Light.ttf` - Light
  - `static/AlumniSansSCMN-Regular.ttf` - Regular
  - `static/AlumniSansSCMN-Medium.ttf` - Medium
  - `static/AlumniSansSCMN-SemiBold.ttf` - SemiBold
  - `static/AlumniSansSCMN-Bold.ttf` - Bold
  - `static/AlumniSansSCMN-ExtraBold.ttf` - ExtraBold
  - `static/AlumniSansSCMN-Black.ttf` - Black
- `AlumniSansSCMN-Italic[wght].ttf` - variable font
  - `static/AlumniSansSCMN-ThinItalic.ttf` - Thin Italic
  - `static/AlumniSansSCMN-ExtraLightItalic.ttf` - ExtraLight Italic
  - `static/AlumniSansSCMN-LightItalic.ttf` - Light Italic
  - `static/AlumniSansSCMN-Italic.ttf` - Italic
  - `static/AlumniSansSCMN-MediumItalic.ttf` - Medium Italic
  - `static/AlumniSansSCMN-SemiBoldItalic.ttf` - SemiBold Italic
  - `static/AlumniSansSCMN-BoldItalic.ttf` - Bold Italic
  - `static/AlumniSansSCMN-ExtraBoldItalic.ttf` - ExtraBold Italic
  - `static/AlumniSansSCMN-BlackItalic.ttf` - Black Italic

## Acknowledgements

Original design: the Alumni Sans SC Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
