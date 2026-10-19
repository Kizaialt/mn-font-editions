# FONTLOG for Jost MN

Jost MN is a modified version of **Jost** v3.710 (https://github.com/indestructible-type/Jost), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Jost MN' so it never clashes with the original.

## Changelog

### 2026-10-19 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `JostMN[wght].ttf` (from `Jost[wght].ttf`)

Contour direction: the original's outlines of `T`, `Y`, `uni041D`, `uni041E`, `uni043D`, `uni043E`, `uni0440`, `v` run counter-clockwise (PostScript order); the new glyphs are built in TrueType order (clockwise outer contours), the original glyphs are left as they are.

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 80.0, centre y=350.0, x 86..704 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 75.0, centre y=230.0, x 77..469 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 80.0 ('uni0440' 80.0, deslanted), down to y=-220.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=55.0; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 80.0, join_y 55.0; wght=-1: stem 10.0, join_y -3.1; wght=+1: stem 195.0, join_y 108.5
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 62.4 (= 0.78 x crossbar 80), angle 20 deg, x 95..370 (62% of the crossbar), centre lines cross the stem axis at y=180.1 and y=401.2; white gaps baseline/between/crossbar = (96.7, 154.7, 135.4) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 62.4, angle 20, stroke_x (95, 370), gaps (96.7, 154.7, 135.4); wght=-1: stroke_thickness 11.0, angle 20, stroke_x (94, 337), gaps (144.3, 230.9, 202.1); wght=+1: stroke_thickness 114.1, angle 20, stroke_x (79, 541), gaps (17.3, 38.4, 38.4)
  - heaviest master (wght=+1, heavy rule): thickness 114.1 (0.585 x crossbar), 20 deg, x 79..541 (protrudes 121.0 past the stem), gaps (17.3, 38.4, 38.4); family internal gaps {'Euro': 32.0, 'yen': 34.6, 'e': 65.9} -> rule minimum 38.4

#### `JostMN-Italic[wght].ttf` (from `Jost-Italic[wght].ttf`)

Contour direction: the original's outlines of `T`, `Y`, `uni041D`, `uni041E`, `uni043D`, `uni043E`, `uni0440`, `v` run counter-clockwise (PostScript order); the new glyphs are built in TrueType order (clockwise outer contours), the original glyphs are left as they are.

Italic: new outlines constructed upright and re-slanted by 9.7 deg (the font's own slant).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 79.0, centre y=350.0, x 117..715 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 74.0, centre y=230.5, x 88..467 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 81.9 ('uni0440' 81.9, deslanted), down to y=-220.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=58.8; italic slant 9.7 deg; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 81.9, join_y 58.8; wght=-1: stem 10.0, join_y -2.8; wght=+1: stem 195.0, join_y 111.5
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 62.4 (= 0.78 x crossbar 80), angle 20 deg, x 64..333 (62% of the crossbar), centre lines cross the stem axis at y=179.5 and y=401.6; white gaps baseline/between/crossbar = (97.3, 155.7, 136.2) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 62.4, angle 20, stroke_x (64, 333), gaps (97.3, 155.7, 136.2); wght=-1: stroke_thickness 11.0, angle 20, stroke_x (64, 299), gaps (145.0, 231.9, 202.9); wght=+1: stroke_thickness 115.1, angle 20, stroke_x (46, 502), gaps (17.3, 38.4, 38.4)
  - heaviest master (wght=+1, heavy rule): thickness 115.1 (0.59 x crossbar), 20 deg, x 46..502 (protrudes 119.4 past the stem), gaps (17.3, 38.4, 38.4); family internal gaps {'Euro': 32.0, 'yen': 33.7, 'e': 66.0} -> rule minimum 38.4

## Method

tools/build_mn.py with tools/families/jost.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `JostMN[wght].ttf` - variable font
  - `static/JostMN-Thin.ttf` - Thin
  - `static/JostMN-ExtraLight.ttf` - ExtraLight
  - `static/JostMN-Light.ttf` - Light
  - `static/JostMN-Regular.ttf` - Regular
  - `static/JostMN-Medium.ttf` - Medium
  - `static/JostMN-SemiBold.ttf` - SemiBold
  - `static/JostMN-Bold.ttf` - Bold
  - `static/JostMN-ExtraBold.ttf` - ExtraBold
  - `static/JostMN-Black.ttf` - Black
- `JostMN-Italic[wght].ttf` - variable font
  - `static/JostMN-ThinItalic.ttf` - Thin Italic
  - `static/JostMN-ExtraLightItalic.ttf` - ExtraLight Italic
  - `static/JostMN-LightItalic.ttf` - Light Italic
  - `static/JostMN-Italic.ttf` - Italic
  - `static/JostMN-MediumItalic.ttf` - Medium Italic
  - `static/JostMN-SemiBoldItalic.ttf` - SemiBold Italic
  - `static/JostMN-BoldItalic.ttf` - Bold Italic
  - `static/JostMN-ExtraBoldItalic.ttf` - ExtraBold Italic
  - `static/JostMN-BlackItalic.ttf` - Black Italic

## Acknowledgements

Original design: the Jost Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
