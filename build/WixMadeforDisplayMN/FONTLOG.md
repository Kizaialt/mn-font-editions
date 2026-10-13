# FONTLOG for Wix Madefor Display MN

Wix Madefor Display MN is a modified version of **Wix Madefor Display** v3.100 (https://github.com/wix/wixmadefor), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Wix Madefor Display MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `WixMadeforDisplayMN[wght].ttf` (from `WixMadeforDisplay[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 69.0, centre y=357.5, x 96..756 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 63.0, centre y=246.0, x 87..527 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 74.0 ('uni0440' 74.0, deslanted), down to y=-194.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=1.2; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 74.0, join_y 1.2; wght=+1: stem 169.0, join_y 7.1
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 69.0 (= 1.00 x crossbar 69), angle 20 deg, x 141..484 (62% of the crossbar), centre lines cross the stem axis at y=192.7 and y=415.9; white gaps baseline/between/crossbar = (93.6, 149.7, 131.0) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 69.0, angle 20, stroke_x (141, 484), gaps (93.6, 149.7, 131.0); wght=+1: stroke_thickness 113.1, angle 20, stroke_x (144, 518), gaps (39.8, 78.4, 75.2)
  - heaviest master (wght=+1, heavy rule): thickness 113.1 (0.78 x crossbar), 20 deg, x 144..518 (protrudes 100.6 past the stem), gaps (39.8, 78.4, 75.2); family internal gaps {'yen': 44.0, 'e': 88.8} -> rule minimum 52.8

## Method

tools/build_mn.py with tools/families/wixmadefordisplay.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `WixMadeforDisplayMN[wght].ttf` - variable font
  - `static/WixMadeforDisplayMN-Regular.ttf` - Regular
  - `static/WixMadeforDisplayMN-Medium.ttf` - Medium
  - `static/WixMadeforDisplayMN-SemiBold.ttf` - SemiBold
  - `static/WixMadeforDisplayMN-Bold.ttf` - Bold
  - `static/WixMadeforDisplayMN-ExtraBold.ttf` - ExtraBold

## Acknowledgements

Original design: the Wix Madefor Display Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
