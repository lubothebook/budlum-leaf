//! Release-mode benchmark: render time per `1600 x 3200` frame.
//! Run: `cargo bench --bench render`. Writes `results/bench-render.txt`.

use std::time::Instant;

use budlum_leaf_duty::app::{self, AppState, InputEvent};
use budlum_leaf_duty::fixed::Fx;
use budlum_leaf_duty::mirror::hash_fields_bytes;
use budlum_leaf_duty::raster::{Frame, Raster};
use budlum_leaf_duty::scene::{GlyphAtlas, ImageStore};

fn stats(mut v: Vec<f64>) -> (f64, f64, f64, f64) {
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let mean = v.iter().sum::<f64>() / v.len() as f64;
    let p50 = v[v.len() / 2];
    let p99 = v[(v.len() * 99).div_ceil(100) - 1];
    (v[0], mean, p50, p99)
}

fn main() {
    let (w, h) = (1600u32, 3200u32);
    let atlas = GlyphAtlas::build();
    let images = ImageStore::demo();
    let cores = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1);
    let n = 240usize;
    // A scrolling list with a fling, the menu opening half way.
    let mut st = AppState::default();
    let mut scenes = Vec::new();
    for f in 0..n as u64 {
        if f == 0 {
            app::apply(&mut st, &InputEvent::Fling { v: Fx::ratio(73, 2) });
        }
        if f == n as u64 / 2 {
            app::apply(&mut st, &InputEvent::ToggleMenu);
        }
        app::tick(&mut st, f + 1);
        scenes.push(app::view(&st, w, h));
    }
    let mut out = String::new();
    out += &format!("frame {w} x {h}, {} MB RGBA8, {n} frames, {cores} cores\n", w * h * 4 / 1_000_000);
    for threads in [1usize, cores] {
        let r = Raster { atlas: &atlas, images: &images, threads };
        let mut frame = Frame::new(w, h);
        r.render_into(&scenes[0], &mut frame); // warm up
        let mut t_render = Vec::new();
        for s in &scenes {
            let t = Instant::now();
            r.render_into(s, &mut frame);
            t_render.push(t.elapsed().as_secs_f64() * 1e3);
        }
        let (mn, m, p50, p99) = stats(t_render);
        out += &format!("threads {threads}: render + 16 slice hashes per frame: min {mn:.2} ms, mean {m:.2} ms, p50 {p50:.2} ms, p99 {p99:.2} ms\n");
    }
    // The raster alone, single thread, no hashing.
    {
        let r = Raster { atlas: &atlas, images: &images, threads: 1 };
        let mut frame = Frame::new(w, h);
        let rows = h / 16;
        let sb = frame.slice_bytes();
        let mut t_r = Vec::new();
        for s in &scenes {
            let t = Instant::now();
            for (i, px) in frame.pixels.chunks_mut(sb).enumerate() {
                r.render_rows(s, i as u32 * rows, (i as u32 + 1) * rows, px);
            }
            t_r.push(t.elapsed().as_secs_f64() * 1e3);
        }
        let (mn, m, p50, p99) = stats(t_r);
        out += &format!("raster only, one thread: min {mn:.2} ms, mean {m:.2} ms, p50 {p50:.2} ms, p99 {p99:.2} ms\n");
    }
    // The hash share alone, single thread.
    let frame = Frame::new(w, h);
    let mut t_h = Vec::new();
    for _ in 0..40 {
        let t = Instant::now();
        std::hint::black_box(hash_fields_bytes(&[&frame.pixels]));
        t_h.push(t.elapsed().as_secs_f64() * 1e3);
    }
    let (mn, m, p50, p99) = stats(t_h);
    out += &format!("SHA-256 of one full frame, one thread: min {mn:.2} ms, mean {m:.2} ms, p50 {p50:.2} ms, p99 {p99:.2} ms\n");
    print!("{out}");
    let _ = std::fs::create_dir_all("results");
    let _ = std::fs::write("results/bench-render.txt", out);
}
