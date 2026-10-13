# FONTLOG for Bona Nova MN

Bona Nova MN is a modified version of **Bona Nova** v4.001 (https://github.com/kosmynkab/Bona-Nova), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Bona Nova MN' so it never clashes with the original. Regular and Bold only: the Italic is not built, because its v is a rounded cursive form with a single bottom point and no straight arm edges, so the straight-stem ү cannot be derived from it.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `BonaNovaMN-Regular.ttf` (from `BonaNova-Regular.ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 36.0, centre y=332.5, x 109..681 (default); kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 36.0, centre y=220.0, x 89..446 (default); kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 80.0 ('uni0440' 80.0, deslanted), down to y=-225.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=53.1; kerning from `uni0443`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 29.3 (= 0.77 x crossbar 38), angle 20 deg, x 143..478 (62% of the crossbar), centre lines cross the stem axis at y=187.3 and y=395.8; white gaps baseline/between/crossbar = (110.8, 177.3, 155.2) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

#### `BonaNovaMN-Bold.ttf` (from `BonaNova-Bold.ttf`)

- U+04E8 Ө `uni04E8`: composite of 'Theta': verified at every master to be 'uni041E' + a full-width bar joined to both walls; kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: composite of 'uni0275': verified at every master to be 'uni043E' + a full-width bar joined to both walls; kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 150.0 ('uni0440' 150.0, deslanted), down to y=-224.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=116.8; kerning from `uni0443`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 37.2 (= 0.78 x crossbar 48), angle 20 deg, x 141..495 (62% of the crossbar), centre lines cross the stem axis at y=186.5 and y=389.9; white gaps baseline/between/crossbar = (102.4, 163.8, 143.3) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/bonanova.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `BonaNovaMN-Regular.ttf` - static font
- `BonaNovaMN-Bold.ttf` - static font

## Acknowledgements

Original design: the Bona Nova Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
