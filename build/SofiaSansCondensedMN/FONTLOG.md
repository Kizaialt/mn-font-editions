# FONTLOG for Sofia Sans Condensed MN

Sofia Sans Condensed MN is a modified version of **Sofia Sans Condensed** v4.101 (https://github.com/lettersoup/Sofia-Sans), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Sofia Sans Condensed MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.

Standard Russian-style Cyrillic forms are the default in this Mongolian edition; the original's default is Bulgarian. See the per-file notes below.


#### `SofiaSansCondensedMN[wght].ttf` (from `SofiaSansCondensed[wght].ttf`)

Default forms: standard Russian-style Cyrillic forms are the default in this Mongolian edition; the original's default is Bulgarian. The cmap maps 30 letters (Љ Д Л Ф в г д ж з и й к л п т ц ш щ ъ ы ь ю ѓ љ њ ќ ѝ џ ґ ӣ) to their `.loclRUS` glyphs, which the original reaches only through the `locl` feature for language RUS. No outline, metric, kerning or other layout table was changed; the original Bulgarian-style glyphs stay in the font under their plain names.

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 67.0, centre y=327.5, x 90..403 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 66.0, centre y=243.5, x 83..331 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 72.0 ('uni0440' 72.0, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-36.0; stem widened where the join would sit deeper than 0.25 x descender; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 72.0, join_y -36.0; wght=-1: stem 16.0, join_y -7.5; wght=+1: stem 171.4, join_y -46.2
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 53.0 (= 0.78 x crossbar 68), angle 20 deg, x 92..314 (62% of the crossbar), centre lines cross the stem axis at y=166.9 and y=380.7; white gaps baseline/between/crossbar = (98.3, 157.3, 137.7) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 53.0, angle 20, stroke_x (92, 314), gaps (98.3, 157.3, 137.7); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (98, 310), gaps (131.9, 211.0, 184.6); wght=+1: stroke_thickness 118.6, angle 20, stroke_x (57, 423), gaps (22.8, 47.9, 47.0)
  - heaviest master (wght=+1, heavy rule): thickness 118.6 (0.78 x crossbar), 20 deg, x 57..423 (protrudes 95.7 past the stem), gaps (22.8, 47.9, 47.0); family internal gaps {'Euro': 34.0, 'yen': 47.0, 'e': 83.0} -> rule minimum 40.8

#### `SofiaSansCondensedMN-Italic[wght].ttf` (from `SofiaSansCondensed-Italic[wght].ttf`)

Default forms: standard Russian-style Cyrillic forms are the default in this Mongolian edition; the original's default is Bulgarian. The cmap maps 13 letters (Љ Д Л Ф в д ж з к л ю љ ќ) to their `.loclRUS` glyphs, which the original reaches only through the `locl` feature for language RUS. No outline, metric, kerning or other layout table was changed; the original Bulgarian-style glyphs stay in the font under their plain names.

Italic: new outlines constructed upright and re-slanted by 9.0 deg (the font's own slant).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 65.0, centre y=327.5, x 111..417 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 64.0, centre y=243.5, x 91..334 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 68.9 ('uni0440' 68.9, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-35.6; stem widened where the join would sit deeper than 0.25 x descender; italic slant 9.0 deg; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 68.9, join_y -35.6; wght=-1: stem 15.9, join_y -6.2; wght=+1: stem 158.5, join_y -46.2
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 51.5 (= 0.78 x crossbar 66), angle 20 deg, x 60..278 (62% of the crossbar), centre lines cross the stem axis at y=167.1 and y=381.9; white gaps baseline/between/crossbar = (100.1, 160.1, 140.1) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 51.5, angle 20, stroke_x (60, 278), gaps (100.1, 160.1, 140.1); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (65, 273), gaps (132.3, 211.7, 185.2); wght=+1: stroke_thickness 112.3, angle 20, stroke_x (34, 370), gaps (29.9, 60.7, 58.8)
  - heaviest master (wght=+1, heavy rule): thickness 112.3 (0.78 x crossbar), 20 deg, x 34..370 (protrudes 88.2 past the stem), gaps (29.9, 60.7, 58.8); family internal gaps {'Euro': 38.0, 'yen': 49.0, 'e': 90.7} -> rule minimum 45.6

## Method

tools/build_mn.py with tools/families/sofiasanscondensed.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `SofiaSansCondensedMN[wght].ttf` - variable font
  - `static/SofiaSansCondensedMN-Thin.ttf` - Thin
  - `static/SofiaSansCondensedMN-ExtraLight.ttf` - ExtraLight
  - `static/SofiaSansCondensedMN-Light.ttf` - Light
  - `static/SofiaSansCondensedMN-Regular.ttf` - Regular
  - `static/SofiaSansCondensedMN-Medium.ttf` - Medium
  - `static/SofiaSansCondensedMN-SemiBold.ttf` - SemiBold
  - `static/SofiaSansCondensedMN-Bold.ttf` - Bold
  - `static/SofiaSansCondensedMN-ExtraBold.ttf` - ExtraBold
  - `static/SofiaSansCondensedMN-Black.ttf` - Black
- `SofiaSansCondensedMN-Italic[wght].ttf` - variable font
  - `static/SofiaSansCondensedMN-ThinItalic.ttf` - Thin Italic
  - `static/SofiaSansCondensedMN-ExtraLightItalic.ttf` - ExtraLight Italic
  - `static/SofiaSansCondensedMN-LightItalic.ttf` - Light Italic
  - `static/SofiaSansCondensedMN-Italic.ttf` - Italic
  - `static/SofiaSansCondensedMN-MediumItalic.ttf` - Medium Italic
  - `static/SofiaSansCondensedMN-SemiBoldItalic.ttf` - SemiBold Italic
  - `static/SofiaSansCondensedMN-BoldItalic.ttf` - Bold Italic
  - `static/SofiaSansCondensedMN-ExtraBoldItalic.ttf` - ExtraBold Italic
  - `static/SofiaSansCondensedMN-BlackItalic.ttf` - Black Italic

## Acknowledgements

Original design: the Sofia Sans Condensed Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
