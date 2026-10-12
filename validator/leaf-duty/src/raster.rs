//! The deterministic software rasteriser.
//!
//! Integer and Q16.16 arithmetic only, no floating point, no SIMD intrinsics
//! whose rounding differs by CPU, and no dependence on the thread count: the
//! frame is cut into horizontal slices, each slice is rendered alone from the
//! whole scene, and the slices are the units of hashing and of streaming.
//! Two validators on two machines therefore produce the same bytes.

use crate::fixed::{div255, Fx};
use crate::mirror::{hash_fields_bytes, merkle_root};
use crate::scene::{GlyphAtlas, ImageStore, Prim, Rgba, Scene, CELL_H, CELL_W};

/// Slices per frame. At `1600 x 3200` one slice is `200` rows, one tile row.
pub const SLICES: u32 = 16;

/// A rendered frame: RGBA8 pixels (alpha always 255), and the slice hashes.
#[derive(Clone)]
pub struct Frame {
    pub width: u32,
    pub height: u32,
    pub pixels: Vec<u8>,
    pub slice_hashes: Vec<[u8; 32]>,
}

impl Frame {
    pub fn new(width: u32, height: u32) -> Self {
        assert!(height % SLICES == 0, "height must split into {SLICES} slices");
        Frame {
            width,
            height,
            pixels: vec![0u8; (width * height * 4) as usize],
            slice_hashes: vec![[0u8; 32]; SLICES as usize],
        }
    }
    pub fn slice_rows(&self) -> u32 {
        self.height / SLICES
    }
    pub fn slice_bytes(&self) -> usize {
        (self.width * self.slice_rows() * 4) as usize
    }
    pub fn slice(&self, idx: usize) -> &[u8] {
        let n = self.slice_bytes();
        &self.pixels[idx * n..(idx + 1) * n]
    }
    /// The frame hash: the Budlum SHA3 Merkle root over the slice hashes.
    pub fn frame_hash(&self) -> [u8; 32] {
        merkle_root(&self.slice_hashes)
    }
}

/// The content hash of one slice, the unit `U6` checks at line rate.
pub fn slice_hash(width: u32, idx: u32, pixels: &[u8]) -> [u8; 32] {
    hash_fields_bytes(&[b"BDLM_LEAF_FRAME_SLICE_V1", &width.to_le_bytes(), &idx.to_le_bytes(), pixels])
}

/// The rendering context shared by every frame of a session.
pub struct Raster<'a> {
    pub atlas: &'a GlyphAtlas,
    pub images: &'a ImageStore,
    pub threads: usize,
}

impl<'a> Raster<'a> {
    /// Render `scene` into `frame` and fill its slice hashes.
    pub fn render_into(&self, scene: &Scene, frame: &mut Frame) {
        assert_eq!((scene.width, scene.height), (frame.width, frame.height));
        let rows = frame.slice_rows();
        let sb = frame.slice_bytes();
        let width = frame.width;
        let threads = self.threads.clamp(1, SLICES as usize);
        let mut jobs: Vec<(usize, &mut [u8], &mut [u8; 32])> = frame
            .pixels
            .chunks_mut(sb)
            .zip(frame.slice_hashes.iter_mut())
            .enumerate()
            .map(|(i, (p, h))| (i, p, h))
            .collect();
        if threads == 1 {
            for (i, px, h) in jobs.iter_mut() {
                let y0 = *i as u32 * rows;
                self.render_rows(scene, y0, y0 + rows, px);
                **h = slice_hash(width, *i as u32, px);
            }
            return;
        }
        let per = jobs.len().div_ceil(threads);
        std::thread::scope(|s| {
            for chunk in jobs.chunks_mut(per) {
                s.spawn(move || {
                    for (i, px, h) in chunk.iter_mut() {
                        let y0 = *i as u32 * rows;
                        self.render_rows(scene, y0, y0 + rows, px);
                        **h = slice_hash(width, *i as u32, px);
                    }
                });
            }
        });
    }

    pub fn render(&self, scene: &Scene) -> Frame {
        let mut f = Frame::new(scene.width, scene.height);
        self.render_into(scene, &mut f);
        f
    }

    /// Render only slice `idx`. The evidence verifier uses this, so a forged
    /// frame is proved by re-rendering one slice, not the whole frame.
    pub fn render_slice(&self, scene: &Scene, idx: u32) -> (Vec<u8>, [u8; 32]) {
        let rows = scene.height / SLICES;
        let mut px = vec![0u8; (scene.width * rows * 4) as usize];
        self.render_rows(scene, idx * rows, (idx + 1) * rows, &mut px);
        let h = slice_hash(scene.width, idx, &px);
        (px, h)
    }

    /// Render rows `y0..y1` of the scene into `out` (row-major RGBA8).
    pub fn render_rows(&self, scene: &Scene, y0: u32, y1: u32, out: &mut [u8]) {
        fill_span(out, scene.clear);
        let band = Band { w: scene.width as i32, y0: y0 as i32, y1: y1 as i32 };
        for prim in &scene.prims {
            match prim {
                Prim::Rect { x, y, w, h, radius, color } => {
                    draw_rect(&band, out, *x, *y, *x + *w, *y + *h, *radius, *color)
                }
                Prim::Glyphs { x, y, scale, text, color } => {
                    draw_glyphs(&band, out, self.atlas, *x, *y, *scale, text, *color)
                }
                Prim::Image { id, x, y, w, h, opacity } => {
                    if let Some(img) = self.images.images.get(*id as usize) {
                        draw_image(&band, out, img, *x, *y, *w, *h, *opacity)
                    }
                }
            }
        }
    }
}

/// The rows a slice covers, in panel pixels.
struct Band {
    w: i32,
    y0: i32,
    y1: i32,
}

impl Band {
    /// Row `y` of the band, as RGBA8 bytes.
    #[inline(always)]
    fn row<'b>(&self, out: &'b mut [u8], y: i32) -> &'b mut [u8] {
        let n = (self.w * 4) as usize;
        let i = (y - self.y0) as usize * n;
        &mut out[i..i + n]
    }
}

/// Fill a row span with an opaque colour.
#[inline(always)]
fn fill_span(span: &mut [u8], c: Rgba) {
    let px = [c.r, c.g, c.b, 255];
    for p in span.chunks_exact_mut(4) {
        p.copy_from_slice(&px);
    }
}

/// Blend `c` at effective alpha `a` (0..=255) over a span of opaque pixels.
/// `dst' = round((c * a + dst * (255 - a)) / 255)`, exact in integers.
#[inline(always)]
fn blend_span(span: &mut [u8], c: Rgba, a: u32) {
    if a == 0 {
        return;
    }
    if a >= 255 {
        fill_span(span, c);
        return;
    }
    let ia = 255 - a;
    let (cr, cg, cb) = (c.r as u32 * a, c.g as u32 * a, c.b as u32 * a);
    for p in span.chunks_exact_mut(4) {
        p[0] = div255(cr + p[0] as u32 * ia) as u8;
        p[1] = div255(cg + p[1] as u32 * ia) as u8;
        p[2] = div255(cb + p[2] as u32 * ia) as u8;
        p[3] = 255;
    }
}

#[inline(always)]
fn blend_px(row: &mut [u8], x: i32, c: Rgba, a: u32) {
    let i = x as usize * 4;
    blend_span(&mut row[i..i + 4], c, a);
}

/// The overlap of pixel `[p, p+1)` with `[lo, hi)`, in 1/256 of a pixel.
#[inline(always)]
fn overlap256(p: i32, lo: i32, hi: i32) -> u32 {
    let a = (p << 16).max(lo);
    let b = ((p + 1) << 16).min(hi);
    if b <= a {
        0
    } else {
        ((b - a) >> 8) as u32
    }
}

/// Coverage of a pixel against a rounded rectangle, by 4 x 4 supersampling.
/// Returns 0..=256.
#[inline(never)]
fn corner_coverage(px: i32, py: i32, ax0: i32, ay0: i32, ax1: i32, ay1: i32, r: i32) -> u32 {
    let r2 = (r as i64) * (r as i64);
    let mut n = 0u32;
    for j in 0..4i64 {
        let sy = ((py as i64) << 16) + ((2 * j + 1) << 13);
        if sy < ay0 as i64 || sy >= ay1 as i64 {
            continue;
        }
        let ccy = sy.clamp((ay0 + r) as i64, (ay1 - r) as i64);
        for i in 0..4i64 {
            let sx = ((px as i64) << 16) + ((2 * i + 1) << 13);
            if sx < ax0 as i64 || sx >= ax1 as i64 {
                continue;
            }
            let ccx = sx.clamp((ax0 + r) as i64, (ax1 - r) as i64);
            let (dx, dy) = (sx - ccx, sy - ccy);
            if dx * dx + dy * dy <= r2 {
                n += 1;
            }
        }
    }
    n * 16
}

#[allow(clippy::too_many_arguments)]
fn draw_rect(band: &Band, out: &mut [u8], x0: Fx, y0: Fx, x1: Fx, y1: Fx, r: Fx, c: Rgba) {
    if x1 <= x0 || y1 <= y0 || c.a == 0 {
        return;
    }
    let (ax0, ax1, ay0, ay1) = (x0.0, x1.0, y0.0, y1.0);
    let half = Fx((x1.0 - x0.0).min(y1.0 - y0.0) / 2);
    let r = r.clamp(Fx::ZERO, half).0;
    let py0 = y0.floor().max(band.y0);
    let py1 = y1.ceil().min(band.y1);
    let px0 = x0.floor().max(0);
    let px1 = x1.ceil().min(band.w);
    if py0 >= py1 || px0 >= px1 {
        return;
    }
    // Columns fully inside the rectangle horizontally.
    let fx0 = x0.ceil().clamp(px0, px1);
    let fx1 = x1.floor().clamp(fx0, px1);
    // Pixels outside these bands are clear of every corner.
    let cy_top = Fx(ay0 + r).ceil();
    let cy_bot = Fx(ay1 - r).floor();
    let cx_left = Fx(ax0 + r).ceil().clamp(px0, px1);
    let cx_right = Fx(ax1 - r).floor().clamp(cx_left, px1);
    for py in py0..py1 {
        let cov_y = overlap256(py, ay0, ay1);
        let row = band.row(out, py);
        let corner_row = r > 0 && (py < cy_top || py >= cy_bot);
        let (lo, hi) = if corner_row {
            for px in (px0..cx_left).chain(cx_right..px1) {
                let cov = corner_coverage(px, py, ax0, ay0, ax1, ay1, r);
                blend_px(row, px, c, (c.a as u32 * cov + 128) >> 8);
            }
            (cx_left, cx_right)
        } else {
            (px0, px1)
        };
        // Analytic coverage: edge columns one by one, the interior as a span.
        let (s0, s1) = (fx0.clamp(lo, hi), fx1.clamp(lo, hi));
        for px in (lo..s0).chain(s1..hi) {
            let cov = (overlap256(px, ax0, ax1) * cov_y) >> 8;
            blend_px(row, px, c, (c.a as u32 * cov + 128) >> 8);
        }
        if s1 > s0 {
            blend_span(&mut row[s0 as usize * 4..s1 as usize * 4], c, (c.a as u32 * cov_y + 128) >> 8);
        }
    }
}

#[allow(clippy::too_many_arguments)]
fn draw_glyphs(band: &Band, out: &mut [u8], atlas: &GlyphAtlas, x: Fx, y: Fx, scale: u32, text: &[u8], c: Rgba) {
    let s = scale.max(1) as i32;
    let gy = y.round();
    let gh = CELL_H as i32 * s;
    let row0 = gy.max(band.y0);
    let row1 = (gy + gh).min(band.y1);
    if row0 >= row1 {
        return;
    }
    let gw = CELL_W as i32 * s;
    // Effective alpha per coverage value, computed once per run.
    let mut alpha = [0u32; 256];
    for (v, a) in alpha.iter_mut().enumerate() {
        *a = div255(c.a as u32 * v as u32);
    }
    for py in row0..row1 {
        let ay = ((py - gy) / s) as usize;
        let row = band.row(out, py);
        let mut gx = x.round();
        for &ch in text {
            let cell = &atlas.cells[(ch & 0x7F) as usize][ay * CELL_W..(ay + 1) * CELL_W];
            for (ax, &v) in cell.iter().enumerate() {
                if v == 0 {
                    continue;
                }
                let a = alpha[v as usize];
                let c0 = (gx + ax as i32 * s).max(0);
                let c1 = (gx + (ax as i32 + 1) * s).min(band.w);
                if c1 > c0 {
                    blend_span(&mut row[c0 as usize * 4..c1 as usize * 4], c, a);
                }
            }
            gx += gw;
        }
    }
}

#[allow(clippy::too_many_arguments)]
fn draw_image(band: &Band, out: &mut [u8], img: &crate::scene::Image, x: Fx, y: Fx, w: Fx, h: Fx, opacity: u8) {
    let (dx0, dy0) = (x.round(), y.round());
    let (dx1, dy1) = ((x + w).round(), (y + h).round());
    let (dw, dh) = (dx1 - dx0, dy1 - dy0);
    if dw <= 0 || dh <= 0 || opacity == 0 {
        return;
    }
    let step_u = ((img.w as i64) << 16) / dw as i64;
    let step_v = ((img.h as i64) << 16) / dh as i64;
    let max_u = ((img.w as i64 - 1) << 16) - 1;
    let max_v = ((img.h as i64 - 1) << 16) - 1;
    let row0 = dy0.max(band.y0);
    let row1 = dy1.min(band.y1);
    let col0 = dx0.max(0);
    let col1 = dx1.min(band.w);
    if row0 >= row1 || col0 >= col1 {
        return;
    }
    let stride = img.w as usize * 4;
    // The horizontal sample positions are the same on every row.
    let us: Vec<(usize, u32)> = (col0..col1)
        .map(|px| {
            let u = ((px - dx0) as i64 * step_u + step_u / 2 - (1 << 15)).clamp(0, max_u);
            ((u >> 16) as usize * 4, ((u >> 8) & 0xFF) as u32)
        })
        .collect();
    let op = opacity as u32;
    for py in row0..row1 {
        let v = ((py - dy0) as i64 * step_v + step_v / 2 - (1 << 15)).clamp(0, max_v);
        let (iv, fv) = ((v >> 16) as usize, ((v >> 8) & 0xFF) as u32);
        let r0 = &img.rgba[iv * stride..(iv + 1) * stride];
        let r1 = &img.rgba[(iv + 1) * stride..(iv + 2) * stride];
        let row = band.row(out, py);
        let dst = &mut row[col0 as usize * 4..col1 as usize * 4];
        for (p, &(iu, fu)) in dst.chunks_exact_mut(4).zip(us.iter()) {
            let mut s = [0u32; 4];
            for k in 0..4 {
                let top = r0[iu + k] as u32 * (256 - fu) + r0[iu + 4 + k] as u32 * fu;
                let bot = r1[iu + k] as u32 * (256 - fu) + r1[iu + 4 + k] as u32 * fu;
                s[k] = (top * (256 - fv) + bot * fv + (1 << 15)) >> 16;
            }
            let a = div255(s[3] * op);
            blend_span(p, Rgba::new(s[0] as u8, s[1] as u8, s[2] as u8, 255), a);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn scene(w: u32, h: u32) -> Scene {
        Scene {
            width: w,
            height: h,
            clear: Rgba::opaque(10, 20, 30),
            prims: vec![
                Prim::Rect { x: Fx::ratio(33, 10), y: Fx::ratio(71, 10), w: Fx::int(50), h: Fx::ratio(401, 4), radius: Fx::int(12), color: Rgba::new(200, 100, 50, 180) },
                Prim::Glyphs { x: Fx::int(5), y: Fx::int(40), scale: 2, text: b"LEAF 42".to_vec(), color: Rgba::opaque(255, 255, 255) },
                Prim::Image { id: 1, x: Fx::int(10), y: Fx::int(80), w: Fx::int(90), h: Fx::int(60), opacity: 200 },
            ],
        }
    }

    #[test]
    fn thread_count_does_not_change_a_byte() {
        let atlas = GlyphAtlas::build();
        let images = ImageStore::demo();
        let s = scene(128, 256);
        let f1 = Raster { atlas: &atlas, images: &images, threads: 1 }.render(&s);
        let f4 = Raster { atlas: &atlas, images: &images, threads: 4 }.render(&s);
        let f3 = Raster { atlas: &atlas, images: &images, threads: 3 }.render(&s);
        assert!(f1.pixels == f4.pixels && f1.pixels == f3.pixels);
        assert_eq!(f1.frame_hash(), f4.frame_hash());
    }

    #[test]
    fn render_slice_matches_the_full_frame() {
        let atlas = GlyphAtlas::build();
        let images = ImageStore::demo();
        let s = scene(128, 256);
        let r = Raster { atlas: &atlas, images: &images, threads: 2 };
        let f = r.render(&s);
        for i in 0..SLICES {
            let (px, h) = r.render_slice(&s, i);
            assert_eq!(px.as_slice(), f.slice(i as usize));
            assert_eq!(h, f.slice_hashes[i as usize]);
        }
    }

    #[test]
    fn subpixel_edge_is_antialiased() {
        let atlas = GlyphAtlas::build();
        let images = ImageStore::demo();
        let s = Scene {
            width: 16,
            height: 16,
            clear: Rgba::opaque(0, 0, 0),
            prims: vec![Prim::Rect { x: Fx::ratio(5, 2), y: Fx::int(0), w: Fx::int(4), h: Fx::int(16), radius: Fx::ZERO, color: Rgba::opaque(255, 255, 255) }],
        };
        let f = Raster { atlas: &atlas, images: &images, threads: 1 }.render(&s);
        // Column 2 is half covered, column 3 is full, column 6 is half covered.
        assert_eq!(&f.pixels[2 * 4..2 * 4 + 3], &[128, 128, 128]);
        assert_eq!(&f.pixels[3 * 4..3 * 4 + 3], &[255, 255, 255]);
        assert_eq!(&f.pixels[6 * 4..6 * 4 + 3], &[128, 128, 128]);
    }
}
