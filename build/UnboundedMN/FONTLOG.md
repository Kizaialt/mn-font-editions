# FONTLOG for Unbounded MN

Unbounded MN is a modified version of **Unbounded** v1.701 (https://github.com/googlefonts/unbounded), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

## Changelog

### 2026-10-13 - MN 0.2 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.

Changes in this release:

- Ү: kerning now derived from Latin Y through Latin look-alikes of each Cyrillic partner (Unbounded keeps Latin and Cyrillic kerning separate); partners without a look-alike, and ҮА / Ү. / Ү, keep the У values.
- ₮: Black master redrawn per design review (strokes 120 thick, x 150..690, 15 deg, gaps 24/52/51); ExtraLight and Regular masters unchanged.
- ₮: kerning from Latin T against digits and punctuation only; ₮4 capped at -98/-60/-40 (wght 200/400/900).
- Ү and ү: mark anchors now from Y and v.
- Ө, ө, ү outlines unchanged.

Glyphs:

- U+04E8 Ө `uni04E8`: composite of 'uni019F': verified at every master to be 'O' + a full-width bar joined to both walls; kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: composite of 'uni0275': verified at every master to be 'o' + a full-width bar joined to both walls; kerning from `uni043E`; mark anchors from `uni043E`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with its bottom replaced by a straight stem: stem width 130.0 (= 'p' descender stem), x 292..422, down to y=-165.0 ('p' descender); outer arm edges extended to meet the stem at y=-16.4 ('v' bottom flat was 146.0 wide); kerning from `uni0443`; mark anchors from `v`.
  - per master (normalized wght): default: stem 130.0, join_y -16.4; wght=-1: stem 54.0, join_y -3.9; wght=+1: stem 254.0, join_y -39.7
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 90.5 (= 0.78 x crossbar 116), angle 20 deg, x 159..625 (62% of the crossbar), centre lines cross the stem axis at y=200.9 and y=405.9; white gaps baseline/between/crossbar = (67.9, 108.7, 95.1) (default); kerning: `T`'s values against digits and punctuation only (capped: four).
  - per master (normalized wght): default: stroke_thickness 90.5, angle 20, stroke_x (159, 625), gaps (67.9, 108.7, 95.1); wght=-1: stroke_thickness 50.0, angle 20, stroke_x (151, 599), gaps (107.6, 172.1, 150.6); wght=+1: stroke_thickness 120, angle 15, stroke_x (150, 690), gaps (24, 52, 50.8)
  - heaviest master (wght=+1, override): thickness 120 (0.522 x crossbar), 15 deg, x 150..690 (protrudes 141.0 past the stem), gaps (24, 52, 50.8); family internal gaps {'uni20B8': 41.0, 'Euro': 42.0, 'yen': 40.0, 'e': 42.2} -> rule minimum 48.0
- `uni04E9.BRACKET.varAlt01`: composite of `uni0275.BRACKET.varAlt01` - the font's heavy-weight ('BRACKET') alternate, swapped in by the same GSUB FeatureVariations rule as its base.

### 2026-10-13 - MN 0.1 - Font Shuugch project

First prototype: Ө ө (composites of the font's Ɵ ɵ), Ү (composite of Y), ү (v + straight stem), ₮ (T + two diagonal strokes); kerning cloned from О о У у.

## Method

tools/build_mn.py with tools/families/unbounded.json. Constructed outlines are computed from the font's own glyphs at every variation master, so they interpolate across the weight axis like their neighbours; advance widths and HVAR come from the base glyphs, kerning and mark anchors as listed above (`otl_base`, `anchor_base`, `kern_lookalike`, `kern_like` in the JSON).

## Files

- `UnboundedMN[wght].ttf` - variable font
- `static/UnboundedMN-ExtraLight.ttf` - ExtraLight instance
- `static/UnboundedMN-Light.ttf` - Light instance
- `static/UnboundedMN-Regular.ttf` - Regular instance
- `static/UnboundedMN-Medium.ttf` - Medium instance
- `static/UnboundedMN-SemiBold.ttf` - SemiBold instance
- `static/UnboundedMN-Bold.ttf` - Bold instance
- `static/UnboundedMN-ExtraBold.ttf` - ExtraBold instance
- `static/UnboundedMN-Black.ttf` - Black instance
  (static instances: fontTools instancer; overlaps removed in the new simple glyphs only)

## Acknowledgements

Original design: the Unbounded Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
