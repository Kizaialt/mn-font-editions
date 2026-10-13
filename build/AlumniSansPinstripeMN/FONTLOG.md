# FONTLOG for Alumni Sans Pinstripe MN

Alumni Sans Pinstripe MN is a modified version of **Alumni Sans Pinstripe** v1.010 (https://github.com/googlefonts/alumni-sans-pinstripe), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Alumni Sans Pinstripe MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `AlumniSansPinstripeMN-Regular.ttf` (from `AlumniSansPinstripe-Regular.ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 16.0, centre y=293.5, x 75..340 (default); kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 16.0, centre y=248.0, x 67..295 (default); kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 16.0 ('uni0440' 16.0, deslanted), down to y=-116.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-4.1; kerning from `uni0443`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 16.0 (= 1.00 x crossbar 16), angle 20 deg, x 56..204 (62% of the crossbar), centre lines cross the stem axis at y=157.2 and y=369.1; white gaps baseline/between/crossbar = (121.8, 194.8, 170.5) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

#### `AlumniSansPinstripeMN-Italic.ttf` (from `AlumniSansPinstripe-Italic.ttf`)

Italic: new outlines constructed upright and re-slanted by 8.0 deg (the font's own slant).

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 16.0, centre y=293.5, x 82..347 (default); kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 16.0, centre y=248.0, x 67..295 (default); kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 17.0 ('uni0440' 16.2, deslanted), down to y=-116.0; stem hangs straight down from the v's own bottom corners (curved arms); italic slant 8.0 deg; kerning from `uni0443`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 16.0 (= 1.00 x crossbar 16), angle 20 deg, x 22..170 (62% of the crossbar), centre lines cross the stem axis at y=157.3 and y=369.0; white gaps baseline/between/crossbar = (121.7, 194.7, 170.4) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/alumnisanspinstripe.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `AlumniSansPinstripeMN-Regular.ttf` - static font
- `AlumniSansPinstripeMN-Italic.ttf` - static font

## Acknowledgements

Original design: the Alumni Sans Pinstripe Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
