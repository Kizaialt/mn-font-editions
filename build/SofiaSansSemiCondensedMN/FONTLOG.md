# FONTLOG for Sofia Sans Semi Condensed MN

Sofia Sans Semi Condensed MN is a modified version of **Sofia Sans Semi Condensed** v4.101 (https://github.com/lettersoup/Sofia-Sans), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Sofia Sans Semi Condensed MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


Standard Russian-style Cyrillic forms are the default in this Mongolian edition; the original's default is Bulgarian. See the per-file notes below.

#### `SofiaSansSemiCondensedMN[wght].ttf` (from `SofiaSansSemiCondensed[wght].ttf`)

Default forms: standard Russian-style Cyrillic forms are the default in this Mongolian edition; the original's default is Bulgarian. The cmap maps 30 letters (Љ Д Л Ф в г д ж з и й к л п т ц ш щ ъ ы ь ю ѓ љ њ ќ ѝ џ ґ ӣ) to their `.loclRUS` glyphs, which the original reaches only through the `locl` feature for language RUS. No outline, metric, kerning or other layout table was changed; the original Bulgarian-style glyphs stay in the font under their plain names.

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 71.0, centre y=327.5, x 109..501 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 69.0, centre y=244.0, x 98..409 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 80.0 ('uni0440' 80.0, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-33.4; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 80.0, join_y -33.4; wght=-1: stem 16.0, join_y -7.3; wght=+1: stem 175.0, join_y -42.5
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 56.9 (= 0.78 x crossbar 73), angle 20 deg, x 117..393 (62% of the crossbar), centre lines cross the stem axis at y=170.5 and y=375.4; white gaps baseline/between/crossbar = (90.2, 144.2, 126.2) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 56.9, angle 20, stroke_x (117, 393), gaps (90.2, 144.2, 126.2); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (123, 387), gaps (127.3, 203.6, 178.2); wght=+1: stroke_thickness 121.7, angle 20, stroke_x (81, 462), gaps (18.8, 41.5, 41.4)
  - heaviest master (wght=+1, heavy rule): thickness 121.7 (0.78 x crossbar), 20 deg, x 81..462 (protrudes 99.6 past the stem), gaps (18.8, 41.5, 41.4); family internal gaps {'Euro': 34.0, 'yen': 47.0, 'e': 82.0} -> rule minimum 40.8

#### `SofiaSansSemiCondensedMN-Italic[wght].ttf` (from `SofiaSansSemiCondensed-Italic[wght].ttf`)

Default forms: standard Russian-style Cyrillic forms are the default in this Mongolian edition; the original's default is Bulgarian. The cmap maps 13 letters (Љ Д Л Ф в д ж з к л ю љ ќ) to their `.loclRUS` glyphs, which the original reaches only through the `locl` feature for language RUS. No outline, metric, kerning or other layout table was changed; the original Bulgarian-style glyphs stay in the font under their plain names.

Italic: new outlines constructed upright and re-slanted by 9.0 deg (the font's own slant).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 70.0, centre y=327.5, x 129..513 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 68.0, centre y=243.5, x 105..410 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 77.0 ('uni0440' 77.0, deslanted), down to y=-185.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-33.1; italic slant 9.0 deg; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 77.0, join_y -33.1; wght=-1: stem 15.7, join_y -6.2; wght=+1: stem 170.9, join_y -41.3
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 56.2 (= 0.78 x crossbar 72), angle 20 deg, x 85..355 (62% of the crossbar), centre lines cross the stem axis at y=170.3 and y=376.2; white gaps baseline/between/crossbar = (91.3, 146.1, 127.9) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 56.2, angle 20, stroke_x (85, 355), gaps (91.3, 146.1, 127.9); wght=-1: stroke_thickness 16.0, angle 20, stroke_x (91, 350), gaps (127.7, 204.2, 178.7); wght=+1: stroke_thickness 120.9, angle 20, stroke_x (52, 418), gaps (20.7, 44.5, 44.0)
  - heaviest master (wght=+1, heavy rule): thickness 120.9 (0.78 x crossbar), 20 deg, x 52..418 (protrudes 96.0 past the stem), gaps (20.7, 44.5, 44.0); family internal gaps {'Euro': 34.0, 'yen': 47.0, 'e': 85.2} -> rule minimum 40.8

## Method

tools/build_mn.py with tools/families/sofiasanssemicondensed.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `SofiaSansSemiCondensedMN[wght].ttf` - variable font
  - `static/SofiaSansSemiCondensedMN-Thin.ttf` - Thin
  - `static/SofiaSansSemiCondensedMN-ExtraLight.ttf` - ExtraLight
  - `static/SofiaSansSemiCondensedMN-Light.ttf` - Light
  - `static/SofiaSansSemiCondensedMN-Regular.ttf` - Regular
  - `static/SofiaSansSemiCondensedMN-Medium.ttf` - Medium
  - `static/SofiaSansSemiCondensedMN-SemiBold.ttf` - SemiBold
  - `static/SofiaSansSemiCondensedMN-Bold.ttf` - Bold
  - `static/SofiaSansSemiCondensedMN-ExtraBold.ttf` - ExtraBold
  - `static/SofiaSansSemiCondensedMN-Black.ttf` - Black
- `SofiaSansSemiCondensedMN-Italic[wght].ttf` - variable font
  - `static/SofiaSansSemiCondensedMN-ThinItalic.ttf` - Thin Italic
  - `static/SofiaSansSemiCondensedMN-ExtraLightItalic.ttf` - ExtraLight Italic
  - `static/SofiaSansSemiCondensedMN-LightItalic.ttf` - Light Italic
  - `static/SofiaSansSemiCondensedMN-Italic.ttf` - Italic
  - `static/SofiaSansSemiCondensedMN-MediumItalic.ttf` - Medium Italic
  - `static/SofiaSansSemiCondensedMN-SemiBoldItalic.ttf` - SemiBold Italic
  - `static/SofiaSansSemiCondensedMN-BoldItalic.ttf` - Bold Italic
  - `static/SofiaSansSemiCondensedMN-ExtraBoldItalic.ttf` - ExtraBold Italic
  - `static/SofiaSansSemiCondensedMN-BlackItalic.ttf` - Black Italic

## Acknowledgements

Original design: the Sofia Sans Semi Condensed Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
