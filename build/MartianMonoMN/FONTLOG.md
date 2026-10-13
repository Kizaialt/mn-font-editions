# FONTLOG for Martian Mono MN

Martian Mono MN is a modified version of **Martian Mono** v1.000 (https://github.com/evilmartians/mono), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Martian Mono MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `MartianMonoMN[wdth,wght].ttf` (from `MartianMono[wdth,wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 108.0, centre y=400.0, x 118..632 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: ; wdth=-1: ; wdth=-1,wght=-1: ; wdth=-1,wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 104.0, centre y=300.0, x 136..614 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=-1: ; wght=+1: ; wdth=-1: ; wdth=-1,wght=-1: ; wdth=-1,wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 133.3 ('uni0440' 110.0, deslanted), down to y=-200.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-50.0; stem widened where the join would sit deeper than 0.25 x descender; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 133.3, join_y -50.0; wght=-1: stem 40.0, join_y -34.2; wght=+1: stem 272.3, join_y -50.0; wdth=-1: stem 139.8, join_y -50.0; wdth=-1,wght=-1: stem 40.0, join_y -34.6; wdth=-1,wght=+1: stem 263.4, join_y -50.0
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 84.2 (= 0.78 x crossbar 108), angle 20 deg, x 180..570 (62% of the crossbar), centre lines cross the stem axis at y=208.5 and y=446.4; white gaps baseline/between/crossbar = (92.6, 148.2, 129.7) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 84.2, angle 20, stroke_x (180, 570), gaps (92.6, 148.2, 129.7); wght=-1: stroke_thickness 38.0, angle 20, stroke_x (198, 552), gaps (138.1, 221.0, 193.4); wght=+1: stroke_thickness 137.0, angle 20, stroke_x (166, 584), gaps (32.4, 72.0, 72.0); wdth=-1: stroke_thickness 82.7, angle 20, stroke_x (145, 455), gaps (101.3, 162.1, 141.8); wdth=-1,wght=-1: stroke_thickness 38.0, angle 20, stroke_x (170, 430), gaps (146.6, 234.5, 205.2); wdth=-1,wght=+1: stroke_thickness 137.3, angle 20, stroke_x (128, 472), gaps (51.6, 82.5, 72.2)
  - heaviest master (wght=+1, heavy rule): thickness 137.0 (0.761 x crossbar), 20 deg, x 166..584 (protrudes 114.9 past the stem), gaps (32.4, 72.0, 72.0); family internal gaps {'yen': 60.0, 'e': 110.0} -> rule minimum 72.0

## Method

tools/build_mn.py with tools/families/martianmono.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `MartianMonoMN[wdth,wght].ttf` - variable font
  - `static/MartianMonoMN-Thin.ttf` - Thin
  - `static/MartianMonoMN-ExtraLight.ttf` - ExtraLight
  - `static/MartianMonoMN-Light.ttf` - Light
  - `static/MartianMonoMN-Regular.ttf` - Regular
  - `static/MartianMonoMN-Medium.ttf` - Medium
  - `static/MartianMonoMN-SemiBold.ttf` - SemiBold
  - `static/MartianMonoMN-Bold.ttf` - Bold
  - `static/MartianMonoMN-ExtraBold.ttf` - ExtraBold

## Acknowledgements

Original design: the Martian Mono Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
