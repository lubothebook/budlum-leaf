//! The small UI scene model the validator renders: rectangles with rounded
//! corners, glyph runs from a glyph atlas, and images. The same model is what
//! the validator would send to the `U1` compositor as layers (FINAL 21.5.6).

use crate::fixed::Fx;
use crate::mirror::hash_fields_bytes;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Rgba {
    pub r: u8,
    pub g: u8,
    pub b: u8,
    pub a: u8,
}

impl Rgba {
    pub const fn new(r: u8, g: u8, b: u8, a: u8) -> Self {
        Rgba { r, g, b, a }
    }
    pub const fn opaque(r: u8, g: u8, b: u8) -> Self {
        Rgba { r, g, b, a: 255 }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Prim {
    /// A rectangle in panel pixels, Q16.16, with an optional corner radius.
    Rect { x: Fx, y: Fx, w: Fx, h: Fx, radius: Fx, color: Rgba },
    /// A run of glyphs from the atlas; the origin snaps to the pixel grid.
    Glyphs { x: Fx, y: Fx, scale: u32, text: Vec<u8>, color: Rgba },
    /// An image from the content-addressed image store, bilinear in Q16.16.
    Image { id: u32, x: Fx, y: Fx, w: Fx, h: Fx, opacity: u8 },
}

/// One frame's scene: a clear colour and an ordered list of primitives.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Scene {
    pub width: u32,
    pub height: u32,
    pub clear: Rgba,
    pub prims: Vec<Prim>,
}

// ---------------------------------------------------------------------------
// The glyph atlas
// ---------------------------------------------------------------------------

/// Cell size of one atlas glyph, in atlas pixels.
pub const CELL_W: usize = 12;
pub const CELL_H: usize = 16;

/// A 5 x 7 bitmap font, row-major, bit 4 is the left column.
fn font5x7(c: u8) -> [u8; 7] {
    match c.to_ascii_uppercase() {
        b'0' => [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
        b'1' => [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
        b'2' => [0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F],
        b'3' => [0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E],
        b'4' => [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
        b'5' => [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
        b'6' => [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
        b'7' => [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
        b'8' => [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
        b'9' => [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],
        b'A' => [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
        b'B' => [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
        b'C' => [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
        b'D' => [0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C],
        b'E' => [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
        b'F' => [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
        b'G' => [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F],
        b'H' => [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
        b'I' => [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
        b'J' => [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
        b'K' => [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
        b'L' => [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
        b'M' => [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
        b'N' => [0x11, 0x11, 0x19, 0x15, 0x13, 0x11, 0x11],
        b'O' => [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
        b'P' => [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
        b'Q' => [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
        b'R' => [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
        b'S' => [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
        b'T' => [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
        b'U' => [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
        b'V' => [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
        b'W' => [0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A],
        b'X' => [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
        b'Y' => [0x11, 0x11, 0x11, 0x0A, 0x04, 0x04, 0x04],
        b'Z' => [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
        b'.' => [0, 0, 0, 0, 0, 0x0C, 0x0C],
        b',' => [0, 0, 0, 0, 0x0C, 0x04, 0x08],
        b':' => [0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0],
        b'-' => [0, 0, 0, 0x1F, 0, 0, 0],
        b'+' => [0, 0x04, 0x04, 0x1F, 0x04, 0x04, 0],
        b'#' => [0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A],
        b'_' => [0, 0, 0, 0, 0, 0, 0x1F],
        b'|' => [0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
        b'>' => [0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08],
        b'<' => [0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02],
        _ => [0; 7],
    }
}

/// An 8-bit coverage atlas of 128 glyphs, built only with integers.
/// Each font pixel is a 2 x 2 block, smoothed by a `[1 2 1]` kernel in both
/// axes, which gives anti-aliased edges with exact integer weights.
pub struct GlyphAtlas {
    pub cells: Vec<[u8; CELL_W * CELL_H]>,
    pub hash: [u8; 32],
}

impl GlyphAtlas {
    pub fn build() -> Self {
        let mut cells = Vec::with_capacity(128);
        for c in 0u8..128 {
            let rows = font5x7(c);
            let mut hard = [0u32; CELL_W * CELL_H];
            for (fy, row) in rows.iter().enumerate() {
                for fx in 0..5 {
                    if row & (0x10 >> fx) != 0 {
                        for dy in 0..2 {
                            for dx in 0..2 {
                                let x = 1 + fx * 2 + dx;
                                let y = 1 + fy * 2 + dy;
                                hard[y * CELL_W + x] = 255;
                            }
                        }
                    }
                }
            }
            let k = [1u32, 2, 1];
            let mut soft = [0u8; CELL_W * CELL_H];
            for y in 0..CELL_H {
                for x in 0..CELL_W {
                    let mut acc = 0u32;
                    for (j, kj) in k.iter().enumerate() {
                        for (i, ki) in k.iter().enumerate() {
                            let sx = x as i32 + i as i32 - 1;
                            let sy = y as i32 + j as i32 - 1;
                            if sx >= 0 && sy >= 0 && (sx as usize) < CELL_W && (sy as usize) < CELL_H {
                                acc += kj * ki * hard[sy as usize * CELL_W + sx as usize];
                            }
                        }
                    }
                    // Weight sum is 16; double the gain and clamp, so stems stay solid.
                    soft[y * CELL_W + x] = ((acc + 4) / 8).min(255) as u8;
                }
            }
            cells.push(soft);
        }
        let flat: Vec<u8> = cells.iter().flat_map(|c| c.iter().copied()).collect();
        let hash = hash_fields_bytes(&[b"BDLM_LEAF_SESSION_STATE_V1", b"atlas", &flat]);
        GlyphAtlas { cells, hash }
    }
}

// ---------------------------------------------------------------------------
// The image store
// ---------------------------------------------------------------------------

/// An RGBA8 image. On chain it is a content-addressed asset; here it is
/// generated from its id so every validator holds the same bytes.
pub struct Image {
    pub w: u32,
    pub h: u32,
    pub rgba: Vec<u8>,
    pub hash: [u8; 32],
}

pub struct ImageStore {
    pub images: Vec<Image>,
}

impl ImageStore {
    /// Two procedural images, built with integer arithmetic only.
    pub fn demo() -> Self {
        let mut images = Vec::new();
        for id in 0..2u32 {
            let (w, h) = (256u32, 160u32);
            let mut rgba = vec![0u8; (w * h * 4) as usize];
            for y in 0..h {
                for x in 0..w {
                    let i = ((y * w + x) * 4) as usize;
                    let check = ((x / 16) + (y / 16)) % 2;
                    let (r, g, b) = if id == 0 {
                        (x as u8, (y * 255 / h) as u8, (128 + 64 * check) as u8)
                    } else {
                        let d = ((x as i32 - 128).pow(2) + (y as i32 - 80).pow(2)) as u32;
                        let ring = ((d / 97) % 2) as u8;
                        (200 - 120 * ring, 60 + 100 * ring, (y * 255 / h) as u8)
                    };
                    rgba[i..i + 4].copy_from_slice(&[r, g, b, 255]);
                }
            }
            let hash = hash_fields_bytes(&[b"BDLM_LEAF_SESSION_STATE_V1", b"image", &rgba]);
            images.push(Image { w, h, rgba, hash });
        }
        ImageStore { images }
    }
}
