# FONTLOG for El Messiri MN

El Messiri MN is a modified version of **El Messiri** v2.020 (https://github.com/Gue3bara/El-Messiri), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'El Messiri MN' so it never clashes with the original.

## Changelog

### 2026-10-19 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `ElMessiriMN[wght].ttf` (from `ElMessiri[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 40.0, centre y=330.0, x 96..616 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 40.0, centre y=235.0, x 93..437 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 90.0 ('uni0440' 90.0, deslanted), down to y=-190.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=72.2; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 90.0, join_y 72.2; wght=+1: stem 130.0, join_y 93.7
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 41.6 (= 0.99 x crossbar 42), angle 20 deg, x 130..472 (62% of the crossbar), centre lines cross the stem axis at y=185.6 and y=392.2; white gaps baseline/between/crossbar = (101.4, 162.3, 142.0) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 41.6, angle 20, stroke_x (130, 472), gaps (101.4, 162.3, 142.0); wght=+1: stroke_thickness 41.6, angle 20, stroke_x (125, 469), gaps (77.9, 161.6, 157.9)
  - heaviest master (wght=+1, heavy rule): thickness 41.6 (0.853 x crossbar), 20 deg, x 125..469 (protrudes 107.1 past the stem), gaps (77.9, 161.6, 157.9); family internal gaps {'e': 173.0, 'equal': 110.0} -> rule minimum 132.0

## Method

tools/build_mn.py with tools/families/elmessiri.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `ElMessiriMN[wght].ttf` - variable font
  - `static/ElMessiriMN-Regular.ttf` - Regular
  - `static/ElMessiriMN-Medium.ttf` - Medium
  - `static/ElMessiriMN-SemiBold.ttf` - SemiBold
  - `static/ElMessiriMN-Bold.ttf` - Bold

## Acknowledgements

Original design: the El Messiri Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
