# FONTLOG for Gidole MN

Gidole MN is a modified version of **Gidole** v2.100 (https://github.com/googlefonts/gidole), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Gidole MN' so it never clashes with the original.

## Changelog

### 2026-10-19 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `GidoleMN-Regular.ttf` (from `Gidole-Regular.ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 140.0, centre y=708.0, x 208..1048 (default); kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E' + bar from uni043D crossbar: thickness 135.0, centre y=541.0, x 200..900 (default); kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'uni0440''s terminal: stem width 150.0 ('uni0440' 150.0, deslanted), down to y=-414.0; outer arm edges extended to meet a stem of 'uni0440''s width at y=8.7; kerning from `uni0443`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 109.2 (= 0.78 x crossbar 140), angle 20 deg, x 236..812 (62% of the crossbar), centre lines cross the stem axis at y=371.6 and y=821.9; white gaps baseline/between/crossbar = (208.8, 334.1, 292.3) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/gidole.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `GidoleMN-Regular.ttf` - static font

## Acknowledgements

Original design: the Gidole Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
