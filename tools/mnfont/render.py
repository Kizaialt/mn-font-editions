"""Tiny proofing renderer: HarfBuzz shaping (kerning, FeatureVariations,
variable axes) + a numpy non-zero-winding scanline rasterizer with 4x4
supersampling.  No system font installation needed."""
from __future__ import annotations

import math

import numpy as np
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from PIL import Image, ImageDraw, ImageFont


class _FlattenPen(BasePen):
    def __init__(self, xf, steps=12):
        super().__init__(None)
        self.xf, self.steps, self.segs = xf, steps, []
        self.start = self.cur = None

    def _seg(self, a, b):
        self.segs.append((*self.xf(a), *self.xf(b)))

    def _moveTo(self, p):
        self.start = self.cur = p

    def _lineTo(self, p):
        self._seg(self.cur, p)
        self.cur = p

    def _qCurveToOne(self, c, p):
        p0 = self.cur
        for i in range(1, self.steps + 1):
            t = i / self.steps
            q = ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p[0],
                 (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p[1])
            self._seg(self.cur, q)
            self.cur = q
        self.cur = p

    def _curveToOne(self, c1, c2, p):
        p0 = self.cur
        for i in range(1, self.steps + 1):
            t = i / self.steps
            mt = 1 - t
            q = (mt ** 3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * p[0],
                 mt ** 3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * p[1])
            self._seg(self.cur, q)
            self.cur = q
        self.cur = p

    def _closePath(self):
        if self.cur is not None and self.start is not None and self.cur != self.start:
            self._seg(self.cur, self.start)
        self.cur = self.start

    _endPath = _closePath


def rasterize(segs, x0, y0, w, h, ss=4):
    """Coverage (h, w) in [0,1] of segments (pixel coords, y down) inside the
    box (x0, y0, w, h), non-zero winding."""
    if not segs or w <= 0 or h <= 0:
        return np.zeros((max(h, 0), max(w, 0)))
    s = (np.asarray(segs, dtype=np.float64) - [x0, y0, x0, y0]) * ss
    ax, ay, bx, by = s.T
    m = ay != by
    ax, ay, bx, by = ax[m], ay[m], bx[m], by[m]
    d = np.where(by > ay, 1.0, -1.0)
    H, W = h * ss, w * ss
    r0 = np.clip(np.ceil(np.minimum(ay, by) - 0.5), 0, H).astype(np.int64)
    r1 = np.clip(np.ceil(np.maximum(ay, by) - 0.5), 0, H).astype(np.int64)
    cnt = r1 - r0
    k = cnt > 0
    ax, ay, bx, by, d, r0, cnt = ax[k], ay[k], bx[k], by[k], d[k], r0[k], cnt[k]
    if cnt.sum() == 0:
        return np.zeros((h, w))
    idx = np.repeat(np.arange(len(cnt)), cnt)
    offs = np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    rows = r0[idx] + offs
    yc = rows + 0.5
    xs = ax[idx] + (yc - ay[idx]) * (bx[idx] - ax[idx]) / (by[idx] - ay[idx])
    cols = np.clip(np.ceil(xs - 0.5), 0, W).astype(np.int64)
    diff = np.bincount(rows * (W + 1) + cols, weights=d[idx], minlength=H * (W + 1))
    wind = np.cumsum(diff.reshape(H, W + 1), axis=1)[:, :W]
    cov = (np.abs(wind) > 0.5).reshape(h, ss, w, ss).mean(axis=(1, 3))
    return cov


class HBFont:
    def __init__(self, path):
        self.path = path
        self.blob = hb.Blob.from_file_path(path)
        self.face = hb.Face(self.blob)
        self.font = hb.Font(self.face)
        self.upem = self.face.upem
        self.wght = None

    def set_wght(self, w):
        if w is not None:
            self.font.set_variations({"wght": w})
        self.wght = w

    def shape(self, text, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, features or {})
        return buf.glyph_infos, buf.glyph_positions

    def name(self, gid):
        return self.font.glyph_to_string(gid)

    def gid(self, ch):
        return self.font.get_nominal_glyph(ord(ch))

    def extents(self, gid):
        return self.font.get_glyph_extents(gid)

    def segments(self, gid, xf):
        pen = _FlattenPen(xf)
        self.font.draw_glyph_with_pen(gid, pen)
        return pen.segs


class Page:
    def __init__(self, w, h, bg=(250, 250, 246)):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w, h), bg)
        self.draw = ImageDraw.Draw(self.img)
        self._label_fonts = {}

    def label(self, xy, text, size=18, fill=(110, 110, 110)):
        if size not in self._label_fonts:
            for cand in ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"):
                try:
                    self._label_fonts[size] = ImageFont.truetype(cand, size)
                    break
                except OSError:
                    continue
            else:
                self._label_fonts[size] = ImageFont.load_default()
        self.draw.text(xy, text, font=self._label_fonts[size], fill=fill)

    def hline(self, y, x0, x1, fill=(200, 200, 200), width=1):
        self.draw.line([(x0, y), (x1, y)], fill=fill, width=width)

    def _composite(self, segs, color):
        if not segs:
            return
        a = np.asarray(segs)
        xs = np.concatenate([a[:, 0], a[:, 2]])
        ys = np.concatenate([a[:, 1], a[:, 3]])
        x0, y0 = int(math.floor(xs.min())) - 1, int(math.floor(ys.min())) - 1
        x1, y1 = int(math.ceil(xs.max())) + 1, int(math.ceil(ys.max())) + 1
        x0c, y0c = max(x0, 0), max(y0, 0)
        x1c, y1c = min(x1, self.w), min(y1, self.h)
        if x1c <= x0c or y1c <= y0c:
            return
        cov = rasterize(segs, x0c, y0c, x1c - x0c, y1c - y0c)
        arr = np.asarray(self.img, dtype=np.float64)
        region = arr[y0c:y1c, x0c:x1c]
        c = cov[..., None]
        region[:] = region * (1 - c) + np.asarray(color, dtype=np.float64) * c
        self.img = Image.fromarray(arr.round().astype(np.uint8))
        self.draw = ImageDraw.Draw(self.img)

    def text(self, hbf, text, x, baseline, size, color=(24, 24, 24), highlight=None,
             hl_color=(40, 70, 200), features=None):
        """Draw shaped text; glyphs whose names are in `highlight` get hl_color.
        Returns the advance in px."""
        infos, poss = hbf.shape(text, features)
        sc = size / hbf.upem
        pen_x = 0
        groups = {}
        for info, pos in zip(infos, poss):
            gx = x + (pen_x + pos.x_offset) * sc
            gy = baseline - pos.y_offset * sc

            def xf(p, gx=gx, gy=gy):
                return (gx + p[0] * sc, gy - p[1] * sc)
            segs = hbf.segments(info.codepoint, xf)
            col = hl_color if highlight and hbf.name(info.codepoint) in highlight else color
            groups.setdefault(col, []).extend(segs)
            pen_x += pos.x_advance
        for col, segs in groups.items():
            self._composite(segs, col)
        return pen_x * sc

    def measure(self, hbf, text, size, features=None):
        infos, poss = hbf.shape(text, features)
        return sum(p.x_advance for p in poss) * size / hbf.upem

    def save(self, path):
        self.img.save(path, optimize=True)
