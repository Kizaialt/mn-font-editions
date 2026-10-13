# FONTLOG for Sofia Sans MN

Sofia Sans MN is a modified version of **Sofia Sans** v4.101 (https://github.com/lettersoup/Sofia-Sans), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Sofia Sans MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `SofiaSansMN[wght].ttf` (from `SofiaSans[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 74.0, centre y=327.5, x 116..526 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 73.0, centre y=244.0, x 104..432 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 85.0 ('uni0440' 85.0, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-37.9; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 85.0, join_y -37.9; wght=-1: stem 16.0, join_y -6.6; wght=+1: stem 180.0, join_y -41.3
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 60.1 (= 0.78 x crossbar 77), angle 20 deg, x 123..412 (62% of the crossbar), centre lines cross the stem axis at y=170.7 and y=372.7; white gaps baseline/between/crossbar = (86.3, 138.1, 120.8) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 60.1, angle 20, stroke_x (123, 412), gaps (86.3, 138.1, 120.8); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (132, 414), gaps (125.6, 201.0, 175.9); wght=+1: stroke_thickness 121.6, angle 20, stroke_x (87, 477), gaps (17.3, 38.4, 38.4)
  - heaviest master (wght=+1, heavy rule): thickness 121.6 (0.76 x crossbar), 20 deg, x 87..477 (protrudes 102.3 past the stem), gaps (17.3, 38.4, 38.4); family internal gaps {'Euro': 32.0, 'yen': 46.0, 'e': 80.0} -> rule minimum 38.4

#### `SofiaSansMN-Italic[wght].ttf` (from `SofiaSans-Italic[wght].ttf`)

Italic: new outlines constructed upright and re-slanted by 9.0 deg (the font's own slant).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 74.0, centre y=327.5, x 136..537 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 73.0, centre y=244.0, x 112..432 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 83.1 ('uni0440' 83.1, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-38.7; italic slant 9.0 deg; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 83.1, join_y -38.7; wght=-1: stem 15.9, join_y -5.4; wght=+1: stem 177.0, join_y -41.5
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 60.1 (= 0.78 x crossbar 77), angle 20 deg, x 90..373 (62% of the crossbar), centre lines cross the stem axis at y=170.2 and y=373.0; white gaps baseline/between/crossbar = (86.8, 138.9, 121.5) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 60.1, angle 20, stroke_x (90, 373), gaps (86.8, 138.9, 121.5); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (99, 376), gaps (126.1, 201.7, 176.5); wght=+1: stroke_thickness 123.1, angle 20, stroke_x (56, 437), gaps (17.3, 38.4, 38.4)
  - heaviest master (wght=+1, heavy rule): thickness 123.1 (0.77 x crossbar), 20 deg, x 56..437 (protrudes 99.9 past the stem), gaps (17.3, 38.4, 38.4); family internal gaps {'Euro': 32.0, 'yen': 46.0, 'e': 80.4} -> rule minimum 38.4

## Method

tools/build_mn.py with tools/families/sofiasans.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `SofiaSansMN[wght].ttf` - variable font
  - `static/SofiaSansMN-Thin.ttf` - Thin
  - `static/SofiaSansMN-ExtraLight.ttf` - ExtraLight
  - `static/SofiaSansMN-Light.ttf` - Light
  - `static/SofiaSansMN-Regular.ttf` - Regular
  - `static/SofiaSansMN-Medium.ttf` - Medium
  - `static/SofiaSansMN-SemiBold.ttf` - SemiBold
  - `static/SofiaSansMN-Bold.ttf` - Bold
  - `static/SofiaSansMN-ExtraBold.ttf` - ExtraBold
  - `static/SofiaSansMN-Black.ttf` - Black
- `SofiaSansMN-Italic[wght].ttf` - variable font
  - `static/SofiaSansMN-ThinItalic.ttf` - Thin Italic
  - `static/SofiaSansMN-ExtraLightItalic.ttf` - ExtraLight Italic
  - `static/SofiaSansMN-LightItalic.ttf` - Light Italic
  - `static/SofiaSansMN-Italic.ttf` - Italic
  - `static/SofiaSansMN-MediumItalic.ttf` - Medium Italic
  - `static/SofiaSansMN-SemiBoldItalic.ttf` - SemiBold Italic
  - `static/SofiaSansMN-BoldItalic.ttf` - Bold Italic
  - `static/SofiaSansMN-ExtraBoldItalic.ttf` - ExtraBold Italic
  - `static/SofiaSansMN-BlackItalic.ttf` - Black Italic

## Acknowledgements

Original design: the Sofia Sans Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
