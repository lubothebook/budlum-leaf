//! The validator side of the Leaf duty: the two speeds, the producer, the hot
//! shadow and the sampling re-executor.
//!
//! * The state speed: inputs are transactions, consensus orders them in the
//!   `6 s` slot, and `ChainSim::finalize_slot` fixes the canonical state.
//! * The frame speed: the serving validator applies each input at once, in
//!   arrival order, renders, and streams. It never waits for the slot.
//! * The join: at a fixed frame after each slot (`FINALITY_LAG_FRAMES`), every
//!   engine replays its unfinalized ops on the finalized snapshot. If that
//!   differs from the optimistic state, the next frame shows the final state.

use std::collections::HashSet;

use crate::app;
use crate::chain::{step_state, ChainSim};
use crate::crypto::ValidatorKey;
use crate::fixed::Fx;
use crate::frame::{genesis_link, spec_leaf, FrameHeader, SecondRoot, SignedSecondRoot, FRAME_HZ};
use crate::mirror::{hash_fields_bytes, merkle_root, Address, FIXED_POINT_SCALE};
use crate::raster::{Frame, Raster};
use crate::scene::{Prim, Rgba};
use crate::session::{InputTx, SessionOpen, SessionState, TxId, FRAMES_PER_SLOT};

/// A record of one reconciliation with finality.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Reconciliation {
    pub slot: u64,
    pub frame: u64,
    pub diverged: bool,
}

/// The deterministic session engine shared by every role.
#[derive(Clone)]
pub struct Engine {
    pub open: SessionOpen,
    pub state: SessionState,
    /// The ops of each frame, by frame number.
    pub history: Vec<Vec<TxId>>,
    pub reconciliations: Vec<Reconciliation>,
}

impl Engine {
    pub fn new(open: &SessionOpen) -> Self {
        Engine { open: open.clone(), state: SessionState::genesis(open), history: Vec::new(), reconciliations: Vec::new() }
    }

    pub fn next_frame(&self) -> u64 {
        self.history.len() as u64
    }

    /// The mandatory reconciliation at the start of a frame, if this frame
    /// is the one that joins a finalized slot.
    pub fn begin_frame(&mut self, chain: &ChainSim) -> Option<(u64, bool)> {
        let f = self.next_frame();
        let slot = ChainSim::slot_to_reconcile_at(f)?;
        let snap = chain
            .snapshots
            .get(slot as usize + 1)
            .expect("finality of the slot must be known at its reconcile frame");
        let finalized: HashSet<TxId> =
            chain.finalized[..=slot as usize].iter().flat_map(|b| b.ordered.iter().map(|(_, id)| *id)).collect();
        let mut canon = snap.clone();
        for g in (slot + 1) * FRAMES_PER_SLOT..f {
            let ops: Vec<TxId> = self.history[g as usize].iter().filter(|id| !finalized.contains(*id)).copied().collect();
            step_state(&mut canon, &ops, &chain.txs);
        }
        let diverged = canon.root() != self.state.root();
        if diverged {
            self.state = canon;
        }
        self.reconciliations.push(Reconciliation { slot, frame: f, diverged });
        Some((slot, diverged))
    }

    /// Apply the given ops, tick, and record the frame.
    pub fn finish_frame(&mut self, ops: Vec<TxId>, chain: &ChainSim) {
        step_state(&mut self.state, &ops, &chain.txs);
        self.history.push(ops);
    }
}

/// Speculative frames: the state after each predicted action, rendered now.
pub fn render_spec(state: &SessionState, spec_count: usize, raster: &Raster, buf: &mut Frame) -> Vec<[u8; 32]> {
    let mut leaves = Vec::new();
    for ev in app::predictions(&state.app).into_iter().take(spec_count) {
        let mut a = state.app.clone();
        app::apply(&mut a, &ev);
        app::tick(&mut a, state.frame_no + 1);
        let scene = app::view(&a, buf.width, buf.height);
        raster.render_into(&scene, buf);
        leaves.push(spec_leaf(state.frame_no - 1, &ev.encode(), &buf.frame_hash()));
    }
    leaves
}

/// What a dishonest validator does, for the slashing tests.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Forgery {
    /// Paint over a slice after rendering, and hash the painted slice, so
    /// the stream is self-consistent and only re-execution catches it.
    Pixels { frame: u64 },
    /// The same paint on every frame from `frame` on: an injected overlay.
    PixelsFrom { frame: u64 },
    /// Credit the balance before rendering: a forged state.
    State { frame: u64 },
}

/// A validator serving one Leaf session, as primary or as hot shadow.
pub struct LeafValidator {
    pub key: ValidatorKey,
    pub engine: Engine,
    pub inbox: Vec<InputTx>,
    pub headers: Vec<FrameHeader>,
    pub roots: Vec<SignedSecondRoot>,
    pub frame: Frame,
    spec_buf: Frame,
    pub spec_count: usize,
    pub forgery: Option<Forgery>,
    second_links: Vec<[u8; 32]>,
}

impl LeafValidator {
    pub fn new(key: ValidatorKey, open: &SessionOpen, spec_count: usize) -> Self {
        let (w, h) = open.viewport;
        LeafValidator {
            key,
            engine: Engine::new(open),
            inbox: Vec::new(),
            headers: Vec::new(),
            roots: Vec::new(),
            frame: Frame::new(w, h),
            spec_buf: Frame::new(w, h),
            spec_count,
            forgery: None,
            second_links: Vec::new(),
        }
    }

    pub fn address(&self) -> Address {
        self.key.address
    }

    /// An input arrives (multipath: the primary and the shadow both get it).
    pub fn receive(&mut self, tx: InputTx) {
        if tx.verify() {
            self.inbox.push(tx);
        }
    }

    pub fn last_link(&self) -> [u8; 32] {
        self.headers.last().map(|h| h.link()).unwrap_or_else(|| genesis_link(&self.engine.state.session_id))
    }

    /// Produce the next frame as the serving validator. Returns the header
    /// and, at the end of each second, the signed second root.
    pub fn produce(&mut self, chain: &ChainSim, raster: &Raster) -> (FrameHeader, Option<SignedSecondRoot>) {
        let reconciled = self.engine.begin_frame(chain);
        // The frame speed: apply every pending input now, in arrival order.
        let mut ops = Vec::new();
        let mut probe = self.engine.state.clone();
        for tx in std::mem::take(&mut self.inbox) {
            if probe.apply_tx(&tx).is_ok() {
                ops.push(tx.id());
            }
        }
        self.engine.finish_frame(ops.clone(), chain);
        let f = self.engine.next_frame() - 1;
        if self.forgery == Some(Forgery::State { frame: f }) {
            self.engine.state.app.balance += 1_000_000;
        }
        self.finish(ops, reconciled, raster)
    }

    /// Follow the primary as hot shadow: apply the primary's ops, render the
    /// same frame, and check that the links agree.
    pub fn follow(&mut self, primary: &FrameHeader, chain: &ChainSim, raster: &Raster) -> Result<(), [u8; 32]> {
        let reconciled = self.engine.begin_frame(chain);
        let done: HashSet<TxId> = primary.ops.iter().copied().collect();
        self.inbox.retain(|tx| !done.contains(&tx.id()));
        self.engine.finish_frame(primary.ops.clone(), chain);
        let (h, _) = self.finish(primary.ops.clone(), reconciled, raster);
        if h.link() == primary.link() {
            Ok(())
        } else {
            Err(h.link())
        }
    }

    fn finish(&mut self, ops: Vec<TxId>, reconciled: Option<(u64, bool)>, raster: &Raster) -> (FrameHeader, Option<SignedSecondRoot>) {
        let f = self.engine.next_frame() - 1;
        let scene = app::view(&self.engine.state.app, self.frame.width, self.frame.height);
        raster.render_into(&scene, &mut self.frame);
        let paint = match self.forgery {
            Some(Forgery::Pixels { frame }) => f == frame,
            Some(Forgery::PixelsFrom { frame }) => f >= frame,
            _ => false,
        };
        if paint {
            // Paint a fake balance over slice 0, then re-hash that slice.
            let fake = crate::scene::Scene {
                prims: vec![
                    Prim::Rect { x: Fx::int(0), y: Fx::int(0), w: Fx::int(self.frame.width as i32), h: Fx::int((self.frame.height / 16) as i32), radius: Fx::ZERO, color: Rgba::opaque(8, 10, 16) },
                    Prim::Glyphs { x: Fx::int(4), y: Fx::int(4), scale: 1, text: b"BAL 999999".to_vec(), color: Rgba::opaque(120, 230, 160) },
                ],
                ..scene.clone()
            };
            let (px, h) = raster.render_slice(&fake, 0);
            let n = self.frame.slice_bytes();
            self.frame.pixels[..n].copy_from_slice(&px);
            self.frame.slice_hashes[0] = h;
        }
        let spec_leaves = render_spec(&self.engine.state, self.spec_count, raster, &mut self.spec_buf);
        let header = FrameHeader {
            session_id: self.engine.state.session_id,
            frame_no: f,
            prev_link: self.last_link(),
            state_root: self.engine.state.root(),
            ops,
            slice_hashes: self.frame.slice_hashes.clone(),
            frame_hash: self.frame.frame_hash(),
            spec_leaves,
            reconciled,
        };
        let link = header.link();
        self.headers.push(header.clone());
        self.second_links.push(link);
        let signed = if (f + 1) % FRAME_HZ == 0 { self.seal_second() } else { None };
        (header, signed)
    }

    /// Sign the root of the frames since the last root. Called at each full
    /// second, and once more when the session closes on a partial second.
    pub fn seal_second(&mut self) -> Option<SignedSecondRoot> {
        let last = self.headers.last()?;
        if self.second_links.is_empty() {
            return None;
        }
        let count = self.second_links.len() as u64;
        let root = SecondRoot {
            session_id: last.session_id,
            second: last.frame_no / FRAME_HZ,
            first_frame: last.frame_no + 1 - count,
            count: count as u32,
            links_root: merkle_root(&self.second_links),
            last_link: last.link(),
            validator: self.key.address,
        };
        let s = SignedSecondRoot::sign(root, &self.key);
        self.roots.push(s.clone());
        self.second_links.clear();
        Some(s)
    }
}

/// One mismatch the sampler found.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Fault {
    StateRoot,
    Slice(u32),
    Spec(u32),
}

/// A frame the sampler holds until the second's root is signed.
#[derive(Clone)]
struct Pending {
    header: FrameHeader,
    pre_state: SessionState,
    post_state: SessionState,
    state_ok: bool,
}

/// A detected forgery, with what the evidence builder needs.
#[derive(Clone)]
pub struct Detection {
    pub signed_root: SignedSecondRoot,
    pub header: FrameHeader,
    pub prev_header: Option<FrameHeader>,
    pub second_links: Vec<[u8; 32]>,
    pub pre_state: SessionState,
    pub fault: Fault,
}

#[derive(Debug, Default, Clone, Copy)]
pub struct SamplerStats {
    pub frames_replayed: u64,
    pub frames_rendered: u64,
    pub frames_matched: u64,
    pub seconds_checked: u64,
}

/// The sampling re-executor run by a second validator. It replays the state
/// of every frame (cheap), and re-renders a sample of the frames, chosen by
/// a seed the primary cannot know before it signs.
pub struct Sampler {
    pub key: ValidatorKey,
    pub engine: Engine,
    /// The sampling rate in `FIXED_POINT_SCALE` units.
    pub rate: u64,
    pub spec_count: usize,
    pending: Vec<Pending>,
    last_link: [u8; 32],
    last_header: Option<FrameHeader>,
    pub stats: SamplerStats,
    pub detections: Vec<Detection>,
    frame: Frame,
    spec_buf: Frame,
}

impl Sampler {
    pub fn new(key: ValidatorKey, open: &SessionOpen, rate: u64, spec_count: usize) -> Self {
        let (w, h) = open.viewport;
        Sampler {
            key,
            engine: Engine::new(open),
            rate,
            spec_count,
            pending: Vec::new(),
            last_link: genesis_link(&open.session_id()),
            last_header: None,
            stats: SamplerStats::default(),
            detections: Vec::new(),
            frame: Frame::new(w, h),
            spec_buf: Frame::new(w, h),
        }
    }

    /// The sample seed: a hash of this sampler's own signature over the
    /// signed links root. The primary cannot compute it before signing.
    pub fn sampled(&self, links_root: &[u8; 32], frame_no: u64) -> bool {
        Self::pick(&self.key.sign(links_root), frame_no, self.rate)
    }

    fn pick(vrf: &[u8], frame_no: u64, rate: u64) -> bool {
        let h = hash_fields_bytes(&[b"BDLM_LEAF_SAMPLE_V1", vrf, &frame_no.to_le_bytes()]);
        let v = u64::from_le_bytes(h[..8].try_into().unwrap_or([0; 8]));
        v % FIXED_POINT_SCALE < rate
    }

    /// Replay one streamed header. The state root is checked on every frame.
    pub fn on_header(&mut self, header: &FrameHeader, chain: &ChainSim) {
        assert_eq!(header.prev_link, self.last_link, "the hash chain must be continuous");
        let pre_state = self.engine.state.clone();
        let _ = self.engine.begin_frame(chain);
        self.engine.finish_frame(header.ops.clone(), chain);
        let state_ok = self.engine.state.root() == header.state_root && header.is_well_formed();
        self.stats.frames_replayed += 1;
        self.pending.push(Pending { header: header.clone(), pre_state, post_state: self.engine.state.clone(), state_ok });
        self.last_link = header.link();
    }

    /// The signed root for the pending second arrives: check it, choose the
    /// sample, re-render, and record any forgery.
    pub fn on_second_root(&mut self, signed: &SignedSecondRoot, chain: &ChainSim, raster: &Raster) -> Vec<Fault> {
        assert!(signed.verify() && chain.is_active_key(&signed.public_key).is_some(), "root from an active validator");
        let links: Vec<[u8; 32]> = self.pending.iter().map(|p| p.header.link()).collect();
        assert_eq!(merkle_root(&links), signed.root.links_root, "the signed root covers the streamed links");
        self.stats.seconds_checked += 1;
        let mut faults = Vec::new();
        let pending = std::mem::take(&mut self.pending);
        let mut prev = self.last_header.clone();
        let vrf = self.key.sign(&signed.root.links_root);
        for p in &pending {
            let fault = if !p.state_ok {
                Some(Fault::StateRoot)
            } else if Self::pick(&vrf, p.header.frame_no, self.rate) {
                self.stats.frames_rendered += 1;
                let scene = app::view(&p.post_state.app, self.frame.width, self.frame.height);
                raster.render_into(&scene, &mut self.frame);
                if self.frame.slice_hashes != p.header.slice_hashes {
                    let i = (0..self.frame.slice_hashes.len()).find(|&i| self.frame.slice_hashes[i] != p.header.slice_hashes[i]).unwrap_or(0);
                    Some(Fault::Slice(i as u32))
                } else {
                    let spec = render_spec(&p.post_state, self.spec_count, raster, &mut self.spec_buf);
                    match (0..spec.len().max(p.header.spec_leaves.len())).find(|&i| spec.get(i) != p.header.spec_leaves.get(i)) {
                        Some(i) => Some(Fault::Spec(i as u32)),
                        None => {
                            self.stats.frames_matched += 1;
                            None
                        }
                    }
                }
            } else {
                None
            };
            if let Some(fault) = fault {
                faults.push(fault.clone());
                self.detections.push(Detection {
                    signed_root: signed.clone(),
                    header: p.header.clone(),
                    prev_header: prev.clone(),
                    second_links: links.clone(),
                    pre_state: p.pre_state.clone(),
                    fault,
                });
            }
            prev = Some(p.header.clone());
        }
        self.last_header = prev;
        faults
    }
}
