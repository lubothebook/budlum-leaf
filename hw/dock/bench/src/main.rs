//! Dock team: measures the leaf-duty deterministic rasteriser (read only,
//! mounted by #[path]) at 1600 x 3200 and prints the per-frame cost as JSON.
#![allow(dead_code)]
#[path = "../../../../validator/leaf-duty/src/fixed.rs"] mod fixed;
#[path = "../../../../validator/leaf-duty/src/mirror.rs"] mod mirror;
#[path = "../../../../validator/leaf-duty/src/crypto.rs"] mod crypto;
#[path = "../../../../validator/leaf-duty/src/scene.rs"] mod scene;
#[path = "../../../../validator/leaf-duty/src/raster.rs"] mod raster;
#[path = "../../../../validator/leaf-duty/src/app.rs"] mod app;

use std::time::Instant;

fn main() {
    let threads: usize = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(1);
    let frames: u64 = std::env::args().nth(2).and_then(|s| s.parse().ok()).unwrap_or(60);
    let atlas = scene::GlyphAtlas::build();
    let images = scene::ImageStore::demo();
    let r = raster::Raster { atlas: &atlas, images: &images, threads };
    let mut st = app::AppState::default();
    let mut buf = raster::Frame::new(1600, 3200);
    // warm up
    let sc = app::view(&st, 1600, 3200);
    r.render_into(&sc, &mut buf);
    let t0 = Instant::now();
    let mut prims = 0usize;
    for f in 0..frames {
        app::apply(&mut st, &app::InputEvent::Scroll { dy: fixed::Fx::int(7) });
        app::tick(&mut st, f);
        let sc = app::view(&st, 1600, 3200);
        prims += sc.prims.len();
        r.render_into(&sc, &mut buf);
    }
    // overdraw: touched pixels per frame over the frame area, last scene
    let sc = app::view(&st, 1600, 3200);
    let clip = |x0: i64, y0: i64, x1: i64, y1: i64| -> i64 {
        let (a, b, c, d) = (x0.max(0), y0.max(0), x1.min(1600), y1.min(3200));
        if c > a && d > b { (c - a) * (d - b) } else { 0 }
    };
    let mut touched: i64 = 1600 * 3200; // the clear
    for p in &sc.prims {
        touched += match p {
            scene::Prim::Rect { x, y, w, h, .. } | scene::Prim::Image { x, y, w, h, .. } =>
                clip(x.floor() as i64, y.floor() as i64, (*x + *w).ceil() as i64, (*y + *h).ceil() as i64),
            scene::Prim::Glyphs { x, y, scale, text, .. } => {
                let s = (*scale).max(1) as i64;
                clip(x.round() as i64, y.round() as i64,
                     x.round() as i64 + text.len() as i64 * scene::CELL_W as i64 * s,
                     y.round() as i64 + scene::CELL_H as i64 * s)
            }
        };
    }
    let overdraw = touched as f64 / (1600.0 * 3200.0);
    let dt = t0.elapsed().as_secs_f64() / frames as f64;
    // the hash share: SHA-256 over the 16 slices, one thread
    let t1 = Instant::now();
    for _ in 0..frames { for i in 0..raster::SLICES { let _ = raster::slice_hash(1600, i, buf.slice(i as usize)); } }
    let dh = t1.elapsed().as_secs_f64() / frames as f64;
    println!("{{\"threads\":{},\"frames\":{},\"ms_per_frame\":{:.3},\"prims_per_frame\":{},\"hash_ms_per_frame\":{:.3},\"overdraw\":{:.3},\"frame_hash\":\"{:02x?}\"}}",
        threads, frames, dt * 1e3, prims as u64 / frames, dh * 1e3, overdraw, &buf.frame_hash()[..4]);
}
