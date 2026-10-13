# FONTLOG for Bona Nova SC MN

Bona Nova SC MN is a modified version of **Bona Nova SC** v4.001 (https://github.com/kosmynkab/Bona-Nova), released under the SIL Open Font License 1.1 (see OFL.txt). It is renamed so that it never clashes with the original.

OFL.txt declares no Reserved Font Name, so the name may be reused; the edition is still renamed 'Bona Nova SC MN' so it never clashes with the original. Regular and Bold only: the Italic is not built (its v is a rounded cursive form with no straight arm edges). This family shows all lowercase as small caps by default (ccmp -> .sc), so the lowercase ө and ү are built directly as small-cap forms: ө = barred small-cap o (uni043E.sc + bar from uni043D.sc), ү = composite of the Latin small-cap y.sc; kerning and anchors come from the matching small-cap glyphs. Capital Ө and Ү are the normal capitals.

## Changelog

### 2026-10-13 - MN 0.1 - Font Shuugch project

Added the letters Mongolian Cyrillic needs that the original lacks. No existing glyph was altered.


#### `BonaNovaSCMN-Regular.ttf` (from `BonaNovaSC-Regular.ttf`)

- U+04E8 Ө `uni04E8`: 'uni041E' + bar from uni041D crossbar: thickness 36.0, centre y=332.5, x 109..681 (default); kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E.sc' + bar from uni043D.sc crossbar: thickness 36.0, centre y=262.5, x 97..554 (default); kerning from `uni043E.sc`; mark anchors from `uni043E.sc`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: composite of 'y.sc' (offset 0,0); kerning from `uni0443.sc`; mark anchors from `y.sc`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 29.3 (= 0.77 x crossbar 38), angle 20 deg, x 143..478 (62% of the crossbar), centre lines cross the stem axis at y=187.3 and y=395.8; white gaps baseline/between/crossbar = (110.8, 177.3, 155.2) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

#### `BonaNovaSCMN-Bold.ttf` (from `BonaNovaSC-Bold.ttf`)

- U+04E8 Ө `uni04E8`: composite of 'Theta': verified at every master to be 'uni041E' + a full-width bar joined to both walls; kerning from `uni041E`; mark anchors from `uni041E`.
- U+04E9 ө `uni04E9`: 'uni043E.sc' + bar from uni043D.sc crossbar: thickness 43.0, centre y=262.5, x 137..531 (default); kerning from `uni043E.sc`; mark anchors from `uni043E.sc`.
- U+04AE Ү `uni04AE`: composite of 'Y' (offset 0,0); kerning: Latin `Y`'s values via the Latin look-alike of each partner, other partners from `uni0423`; mark anchors from `Y`.
- U+04AF ү `uni04AF`: composite of 'y.sc' (offset 0,0); kerning from `uni0443.sc`; mark anchors from `y.sc`.
- U+20AE ₮ `uni20AE`: 'T' outline + two parallel strokes (vertical end cuts) centred on the stem: perpendicular thickness 37.2 (= 0.78 x crossbar 48), angle 20 deg, x 141..495 (62% of the crossbar), centre lines cross the stem axis at y=186.5 and y=389.9; white gaps baseline/between/crossbar = (102.4, 163.8, 143.3) (default); kerning: `T`'s values against digits and punctuation only (capped: four).

## Method

tools/build_mn.py with tools/families/bonanovasc.json (same pipeline and review rules as Unbounded MN): designer's own Ɵ/ɵ (or a full-bar Θ) when present, else О/о + a bar measured from Н/н; Ү = composite of Y; ү = v + the font's own р/p stem and terminal; ₮ = T + two diagonal strokes with the heaviest-master whitespace rule; kerning as listed.

## Files

- `BonaNovaSCMN-Regular.ttf` - static font
- `BonaNovaSCMN-Bold.ttf` - static font

## Acknowledgements

Original design: the Bona Nova SC Project Authors. Mongolian additions: Font Shuugch project (kizaialt.github.io/mn-font-finder).
