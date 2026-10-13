# FONTLOG for Orangerie MN

Orangerie MN is a modified version of **Oranienbaum** v1.000 (https://github.com/googlefonts/oranienbaum), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

RESERVED FONT NAME: the original OFL.txt reserves the name 'Oranienbaum' (Copyright (c) 2012 Oleg Pospelov, Jovanny Lemonad, with Reserved Font Name 'Oranienbaum'). A modified version may not use the reserved name, so this edition is released as 'Orangerie MN' (files OrangerieMN-*.ttf) and its font names (family, full, PostScript, unique ID, trademark line) no longer contain the word 'Oranienbaum'; the original author is credited in the copyright notice and below. NameID 0 (the copyright notice) keeps the original line verbatim, including its Reserved-Font-Name declaration, because the OFL requires the copyright notice to be retained; every other name record is renamed.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `OrangerieMN-Regular.ttf` (from `Oranienbaum-Regular.ttf`)

- U+04E8 Ө `uni04E8`: 'afii10032' + bar from afii10031 crossbar: thickness 20.0, centre y=350.0, x 88..462 (default); kerning from `afii10032`; mark anchors from `afii10032`.
- U+04E9 ө `uni04E9`: 'afii10080' + bar from afii10079 crossbar: thickness 20.0, centre y=230.0, x 90..380 (default); kerning from `afii10080`; mark anchors from `afii10080`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `afii10037`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'afii10082''s terminal: stem width 80.0 ('afii10082' 80.0, deslanted), down to y=-240.0; outer arm edges extended to meet a stem of 'afii10082''s width at y=76.0; kerning from `afii10085`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 15.6 (= 0.78 x crossbar 20), angle 20 deg, x 113..382 (62% of the crossbar), centre lines cross the stem axis at y=194.5 and y=430.6; white gaps baseline/between/crossbar = (137.2, 219.5, 192.0) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/oranienbaum.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `OrangerieMN-Regular.ttf` - static font

## Acknowledgements

Original design: the Oranienbaum Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
