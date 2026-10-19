# FONTLOG for Plain One MN

Plain One MN is a modified version of **Prosto One** v1.000 (https://github.com/googlefonts/googlefontdirectory-hg), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

RESERVED FONT NAME: the original OFL.txt reserves the names 'Prosto' and 'Prosto One' (Copyright (c) 2012, Jovanny Lemonad, Copyright (c) 2012, Pavel Emelyanov, with Reserved Font Name "Prosto" and "Prosto One"). A modified version may not use the reserved names, so this edition is released as 'Plain One MN' (files PlainOneMN-*.ttf) and its font names (family, full, PostScript, unique ID, trademark line) no longer contain the word 'Prosto'; the original authors are credited in the copyright notice and below. NameID 0 (the copyright notice) keeps the original line verbatim, including its Reserved-Font-Name declaration, because the OFL requires the copyright notice to be retained; every other name record is renamed.

## Changelog

### 2026-10-19 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `PlainOneMN-Regular.ttf` (from `ProstoOne-Regular.ttf`)

Removed the optional per-glyph device tables `hdmx`, `LTSH` (they have no entries for the new glyphs; renderers compute these values themselves).

- U+04E8 Ө `uni04E8`: 'afii10032' + bar from afii10031 crossbar: thickness 75.0, centre y=350.0, x 128..772 (default); kerning from `afii10032`; mark anchors from `afii10032`.
- U+04E9 ө `uni04E9`: 'afii10080' + bar from afii10079 crossbar: thickness 70.0, centre y=260.0, x 121..579 (default); kerning from `afii10080`; mark anchors from `afii10080`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `afii10037`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: 'v' outline with a straight stem and 'afii10082''s terminal: stem width 157.7 ('afii10082' 140.0, deslanted), down to y=-180.0; outer arm edges extended to meet a stem of 'afii10082''s width at y=-81.0; stem widened where the join would sit deeper than 0.45 x descender; kerning from `afii10085`; mark anchors from `v`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 58.5 (= 0.78 x crossbar 75), angle 20 deg, x 140..565 (62% of the crossbar), centre lines cross the stem axis at y=194.9 and y=395.5; white gaps baseline/between/crossbar = (86.5, 138.4, 121.1) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/prostoone.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `PlainOneMN-Regular.ttf` - static font

## Acknowledgements

Original design: the Prosto One Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
