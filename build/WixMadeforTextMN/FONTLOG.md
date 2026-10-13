# FONTLOG for Wix Madefor Text MN

Wix Madefor Text MN is a modified version of **Wix Madefor Text** v3.100 (https://github.com/wix/wixmadefor), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Wix Madefor Text MN' so it never clashes with the original. Roman only: the Italic variable font has no Cyrillic at all (no cyrl script, no О Н о н р у), so there is nothing to base Ө ө Ү ү on and the italic is not built.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `WixMadeforTextMN[wght].ttf` (from `WixMadeforText[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 71.0, centre y=357.5, x 107..722 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 65.0, centre y=246.0, x 95..506 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 77.0 ('uni0440' 77.0, deslanted), down to y=-194.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=1.2; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 77.0, join_y 1.2; wght=+1: stem 163.0, join_y 7.5
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 71.0 (= 1.00 x crossbar 71), angle 20 deg, x 138..462 (62% of the crossbar), centre lines cross the stem axis at y=190.6 and y=416.0; white gaps baseline/between/crossbar = (93.7, 149.9, 131.1) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 71.0, angle 20, stroke_x (138, 462), gaps (93.7, 149.9, 131.1); wght=+1: stroke_thickness 111.5, angle 20, stroke_x (137, 488), gaps (43.1, 83.7, 79.9)
  - heaviest master (wght=+1, heavy rule): thickness 111.5 (0.78 x crossbar), 20 deg, x 137..488 (protrudes 93.3 past the stem), gaps (43.1, 83.7, 79.9); family internal gaps {'yen': 44.0, 'e': 92.2} -> rule minimum 52.8

## Method

tools/build_mn.py with tools/families/wixmadefortext.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `WixMadeforTextMN[wght].ttf` - variable font
  - `static/WixMadeforTextMN-Regular.ttf` - Regular
  - `static/WixMadeforTextMN-Medium.ttf` - Medium
  - `static/WixMadeforTextMN-SemiBold.ttf` - SemiBold
  - `static/WixMadeforTextMN-Bold.ttf` - Bold
  - `static/WixMadeforTextMN-ExtraBold.ttf` - ExtraBold

## Acknowledgements

Original design: the Wix Madefor Text Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
