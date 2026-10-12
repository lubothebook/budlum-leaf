//! RG-18 acceptance, part 1: `10 000` frames stream from one validator, and
//! a second validator matches a sample bit for bit.

mod common;

use std::time::Instant;

use budlum_leaf_duty::crypto::ValidatorKey;
use budlum_leaf_duty::mirror::FIXED_POINT_SCALE;
use budlum_leaf_duty::raster::Raster;
use budlum_leaf_duty::scene::{GlyphAtlas, ImageStore};
use budlum_leaf_duty::validator::{LeafValidator, Sampler};
use common::*;

fn run_stream(viewport: (u32, u32), frames: u64, rate: u64, spec: usize) -> String {
    let atlas = GlyphAtlas::build();
    let images = ImageStore::demo();
    let raster = Raster { atlas: &atlas, images: &images, threads: 1 };
    let mut w = World::new(viewport);
    let mut primary = LeafValidator::new(ValidatorKey::from_test_seed(1), &w.open, spec);
    // The second validator is a separate instance with its own key and its
    // own copy of the engine; it shares nothing with the primary but the chain.
    let mut sampler = Sampler::new(ValidatorKey::from_test_seed(2), &w.open, rate, spec);
    let t0 = Instant::now();
    let mut inputs = 0;
    for f in 0..frames {
        if let Some(s) = slot_ended_before(f) {
            w.finalize_as_served(s, &primary.engine.history);
        }
        for tx in w.script(f) {
            inputs += 1;
            primary.receive(tx);
        }
        let (h, root) = primary.produce(&w.chain, &raster);
        sampler.on_header(&h, &w.chain);
        if let Some(r) = root {
            let faults = sampler.on_second_root(&r, &w.chain, &raster);
            assert!(faults.is_empty(), "honest frames must match bit for bit: {faults:?}");
        }
    }
    if let Some(r) = primary.seal_second() {
        assert!(sampler.on_second_root(&r, &w.chain, &raster).is_empty());
    }
    let st = sampler.stats;
    assert_eq!(st.frames_replayed, frames);
    assert!(st.frames_rendered > 0);
    assert_eq!(st.frames_matched, st.frames_rendered, "every sampled frame matched bit for bit");
    assert!(sampler.detections.is_empty());
    assert_eq!(primary.engine.reconciliations, sampler.engine.reconciliations);
    assert!(primary.engine.reconciliations.iter().all(|r| !r.diverged));
    assert_eq!(sampler.engine.state.root(), primary.engine.state.root());
    format!(
        "viewport {}x{}, frames {}, inputs {}, seconds signed {}, sample rate {}/{}, \
         frames re-rendered by the second validator {}, matched bit for bit {}, \
         speculative frames per frame {}, reconciliations {} (diverged 0), wall time {:.1} s\n",
        viewport.0,
        viewport.1,
        frames,
        inputs,
        st.seconds_checked,
        rate,
        FIXED_POINT_SCALE,
        st.frames_rendered,
        st.frames_matched,
        spec,
        primary.engine.reconciliations.len(),
        t0.elapsed().as_secs_f64()
    )
}

/// `10 000` frames at `400 x 800` (a quarter of the panel in each axis, the
/// same scene code), one speculative frame per frame, sample rate `1/16`.
#[test]
fn ten_thousand_frames_sampled_bit_exact() {
    let r = run_stream((400, 800), 10_000, FIXED_POINT_SCALE / 16, 1);
    println!("{r}");
    write_result("rg18-stream-10000.txt", &r);
}

/// The full `1600 x 3200` panel: every frame of a short stream re-rendered
/// by the second validator and matched bit for bit.
#[test]
fn full_panel_every_frame_bit_exact() {
    let r = run_stream((1600, 3200), 60, FIXED_POINT_SCALE, 0);
    println!("{r}");
    write_result("rg18-stream-full-panel.txt", &r);
}
