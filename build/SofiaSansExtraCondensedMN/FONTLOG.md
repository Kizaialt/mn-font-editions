# FONTLOG for Sofia Sans Extra Condensed MN

Sofia Sans Extra Condensed MN is a modified version of **Sofia Sans Extra Condensed** v4.101 (https://github.com/lettersoup/Sofia-Sans), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Sofia Sans Extra Condensed MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `SofiaSansExtraCondensedMN[wght].ttf` (from `SofiaSansExtraCondensed[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 62.0, centre y=327.5, x 76..324 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 61.0, centre y=243.0, x 70..268 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 65.0 ('uni0440' 65.0, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-36.2; stem widened where the join would sit deeper than 0.25 x descender; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 65.0, join_y -36.2; wght=-1: stem 16.0, join_y -9.7; wght=+1: stem 166.5, join_y -46.2
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 49.1 (= 0.78 x crossbar 63), angle 20 deg, x 73..252 (62% of the crossbar), centre lines cross the stem axis at y=164.4 and y=385.4; white gaps baseline/between/crossbar = (105.5, 168.8, 147.7) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 49.1, angle 20, stroke_x (73, 252), gaps (105.5, 168.8, 147.7); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (76, 244), gaps (135.9, 217.4, 190.2); wght=+1: stroke_thickness 113.9, angle 20, stroke_x (37, 385), gaps (27.7, 56.8, 55.2)
  - heaviest master (wght=+1, heavy rule): thickness 113.9 (0.78 x crossbar), 20 deg, x 37..385 (protrudes 91.3 past the stem), gaps (27.7, 56.8, 55.2); family internal gaps {'Euro': 37.0, 'yen': 49.0, 'e': 87.0} -> rule minimum 44.4

#### `SofiaSansExtraCondensedMN-Italic[wght].ttf` (from `SofiaSansExtraCondensed-Italic[wght].ttf`)

Italic: new outlines constructed upright and re-slanted by 9.0 deg (the font's own slant).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 62.0, centre y=327.5, x 96..340 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 60.0, centre y=243.0, x 78..271 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 62.0 ('uni0440' 62.0, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-37.7; stem widened where the join would sit deeper than 0.25 x descender; italic slant 9.0 deg; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 62.0, join_y -37.7; wght=-1: stem 15.9, join_y -8.0; wght=+1: stem 163.3, join_y -46.2
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 47.6 (= 0.78 x crossbar 61), angle 20 deg, x 41..218 (62% of the crossbar), centre lines cross the stem axis at y=164.5 and y=386.6; white gaps baseline/between/crossbar = (107.1, 171.4, 150.0) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 47.6, angle 20, stroke_x (41, 218), gaps (107.1, 171.4, 150.0); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (45, 210), gaps (136.2, 217.9, 190.7); wght=+1: stroke_thickness 113.9, angle 20, stroke_x (8, 346), gaps (28.7, 58.3, 56.6)
  - heaviest master (wght=+1, heavy rule): thickness 113.9 (0.78 x crossbar), 20 deg, x 8..346 (protrudes 88.6 past the stem), gaps (28.7, 58.3, 56.6); family internal gaps {'Euro': 37.0, 'yen': 49.0, 'e': 84.7} -> rule minimum 44.4

## Method

tools/build_mn.py with tools/families/sofiasansextracondensed.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `SofiaSansExtraCondensedMN[wght].ttf` - variable font
  - `static/SofiaSansExtraCondensedMN-Thin.ttf` - Thin
  - `static/SofiaSansExtraCondensedMN-ExtraLight.ttf` - ExtraLight
  - `static/SofiaSansExtraCondensedMN-Light.ttf` - Light
  - `static/SofiaSansExtraCondensedMN-Regular.ttf` - Regular
  - `static/SofiaSansExtraCondensedMN-Medium.ttf` - Medium
  - `static/SofiaSansExtraCondensedMN-SemiBold.ttf` - SemiBold
  - `static/SofiaSansExtraCondensedMN-Bold.ttf` - Bold
  - `static/SofiaSansExtraCondensedMN-ExtraBold.ttf` - ExtraBold
  - `static/SofiaSansExtraCondensedMN-Black.ttf` - Black
- `SofiaSansExtraCondensedMN-Italic[wght].ttf` - variable font
  - `static/SofiaSansExtraCondensedMN-ThinItalic.ttf` - Thin Italic
  - `static/SofiaSansExtraCondensedMN-ExtraLightItalic.ttf` - ExtraLight Italic
  - `static/SofiaSansExtraCondensedMN-LightItalic.ttf` - Light Italic
  - `static/SofiaSansExtraCondensedMN-Italic.ttf` - Italic
  - `static/SofiaSansExtraCondensedMN-MediumItalic.ttf` - Medium Italic
  - `static/SofiaSansExtraCondensedMN-SemiBoldItalic.ttf` - SemiBold Italic
  - `static/SofiaSansExtraCondensedMN-BoldItalic.ttf` - Bold Italic
  - `static/SofiaSansExtraCondensedMN-ExtraBoldItalic.ttf` - ExtraBold Italic
  - `static/SofiaSansExtraCondensedMN-BlackItalic.ttf` - Black Italic

## Acknowledgements

Original design: the Sofia Sans Extra Condensed Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
