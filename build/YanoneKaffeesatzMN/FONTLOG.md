# FONTLOG for Yanone Kaffeesatz MN

Yanone Kaffeesatz MN is a modified version of **Yanone Kaffeesatz** v2.003 (https://github.com/yanone/kaffeesatz), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Yanone Kaffeesatz MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `YanoneKaffeesatzMN[wght].ttf` (from `YanoneKaffeesatz[wght].ttf`)

Already in the original (left untouched): U+20AE ₮

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 24.0, centre y=350.0, x 60..406 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 24.0, centre y=250.0, x 52..349 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 24.0 ('uni0440' 24.0, deslanted), down to y=-197.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=10.9; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 24.0, join_y 10.9; wght=+1: stem 112.0, join_y -17.3

## Method

tools/build_mn.py with tools/families/yanonekaffeesatz.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `YanoneKaffeesatzMN[wght].ttf` - variable font
  - `static/YanoneKaffeesatzMN-ExtraLight.ttf` - ExtraLight
  - `static/YanoneKaffeesatzMN-Light.ttf` - Light
  - `static/YanoneKaffeesatzMN-Regular.ttf` - Regular
  - `static/YanoneKaffeesatzMN-Medium.ttf` - Medium
  - `static/YanoneKaffeesatzMN-SemiBold.ttf` - SemiBold
  - `static/YanoneKaffeesatzMN-Bold.ttf` - Bold

## Acknowledgements

Original design: the Yanone Kaffeesatz Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
