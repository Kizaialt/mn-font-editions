# FONTLOG for Tuul One MN

Tuul One MN is a modified version of **Russo One** v1.000 (https://github.com/googlefonts/russoone), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

RESERVED FONT NAME: the original OFL.txt reserves the name 'Russo' (Copyright (c) 2011-2012, Jovanny Lemonad (jovanny.ru), with Reserved Font Name "Russo"). A modified version may not use the reserved name, so this edition is released as 'Tuul One MN' (files TuulOneMN-*.ttf) and its font names (family, full, PostScript, unique ID, trademark line, compatible full name) no longer contain the word 'Russo'; the original author is credited in the copyright notice and below. NameID 0 (the copyright notice) keeps the original line verbatim, including its Reserved-Font-Name declaration, because the OFL requires the copyright notice to be retained; every other name record is renamed.

## Changelog

### 2026-10-19 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `TuulOneMN-Regular.ttf` (from `RussoOne-Regular.ttf`)

- U+04E8 Ө `uni04E8`: 'afii10032' + bar from afii10031 crossbar: thickness 140.0, centre y=350.0, x 130..600 (default); kerning from `afii10032`; mark anchors from `afii10032`.
- U+04E9 ө `uni04E9`: 'afii10080' + bar from afii10079 crossbar: thickness 107.7, centre y=265.0, x 128..502 (default); kerning from `afii10080`; mark anchors from `afii10080`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `afii10037`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'afii10082''s terminal: stem width 175.0 ('afii10082' 175.0, deslanted), down to y=-170.0; outer arm edges extended to meet a stem of 'afii10082''s width at y=-33.1; kerning from `afii10085`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 109.2 (= 0.78 x crossbar 140), angle 20 deg, x 124..496 (62% of the crossbar), centre lines cross the stem axis at y=173.8 and y=366.9; white gaps baseline/between/crossbar = (48.0, 76.9, 67.3) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/russoone.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `TuulOneMN-Regular.ttf` - static font

## Acknowledgements

Original design: the Russo One Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
