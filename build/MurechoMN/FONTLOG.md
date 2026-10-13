# FONTLOG for Murecho MN

Murecho MN is a modified version of **Murecho** v1.010 (https://github.com/positype/Murecho-Project), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Murecho MN' so it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `MurechoMN[wght].ttf` (from `Murecho[wght].ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 19.0, centre y=364.0, x 57..623 (default); kerning from `uni041E`; mark anchors from `uni041E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 18.0, centre y=260.0, x 58..487 (default); kerning from `uni043E`; mark anchors from `uni043E`.
  - per master (normalized wght): default: ; wght=+1: 
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 20.0 ('uni0440' 20.0, deslanted), down to y=-224.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=-1.3; kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 20.0, join_y -1.3; wght=+1: stem 199.0, join_y -8.8
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 19.0 (= 1.00 x crossbar 19), angle 20 deg, x 94..392 (62% of the crossbar), centre lines cross the stem axis at y=204.3 and y=448.6; white gaps baseline/between/crossbar = (140.1, 224.1, 196.1) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 19.0, angle 20, stroke_x (94, 392), gaps (140.1, 224.1, 196.1); wght=+1: stroke_thickness 129.5, angle 20, stroke_x (78, 498), gaps (25.0, 54.5, 54.1)
  - heaviest master (wght=+1, heavy rule): thickness 129.5 (0.78 x crossbar), 20 deg, x 78..498 (protrudes 110.0 past the stem), gaps (25.0, 54.5, 54.1); family internal gaps {'Euro': 61.0, 'yen': 43.0, 'e': 66.6} -> rule minimum 51.6

## Method

tools/build_mn.py with tools/families/murecho.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `MurechoMN[wght].ttf` - variable font
  - `static/MurechoMN-Thin.ttf` - Thin
  - `static/MurechoMN-ExtraLight.ttf` - ExtraLight
  - `static/MurechoMN-Light.ttf` - Light
  - `static/MurechoMN-Regular.ttf` - Regular
  - `static/MurechoMN-Medium.ttf` - Medium
  - `static/MurechoMN-SemiBold.ttf` - SemiBold
  - `static/MurechoMN-Bold.ttf` - Bold
  - `static/MurechoMN-ExtraBold.ttf` - ExtraBold
  - `static/MurechoMN-Black.ttf` - Black

## Acknowledgements

Original design: the Murecho Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
