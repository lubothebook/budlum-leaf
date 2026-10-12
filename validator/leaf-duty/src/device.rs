//! A model of the fixed-function receive path on the Leaf: `U6` checks each
//! slice at line rate and decodes it into the frame store, `U1` scans the
//! frame out, and `U7` checks the validator key and signs receipts. It runs
//! no program; every step below is a compare, a hash or a copy.

use crate::crypto::WalletKey;
use crate::frame::{genesis_link, FrameHeader, SignedSecondRoot};
use crate::mirror::merkle_root;
use crate::raster::slice_hash;
use crate::receipt::LeafReceipt;

/// `U6` leaves the primary at the next slice when its round trip crosses
/// this limit `[HYPOTHESIS]`, set below the `30 ms` p99 target of DST-11.
pub const HANDOVER_RTT_US: u32 = 20_000;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Refusal {
    /// SW-22: the sender is not an active validator. The safe screen shows.
    NotActiveValidator,
    BrokenChain,
    MalformedHeader,
    BadSliceTag,
    NoHeader,
    RootMismatch,
}

pub struct LeafDevice {
    pub wallet: WalletKey,
    /// The active validator keys, kept current from finality proofs.
    pub active_set: Vec<Vec<u8>>,
    pub session_id: [u8; 32],
    pub width: u32,
    pub height: u32,
    last_link: [u8; 32],
    current: Option<(FrameHeader, Vec<bool>)>,
    pub frame_store: Vec<u8>,
    /// Frames shown, in order: `(frame_no, link)`.
    pub shown: Vec<(u64, [u8; 32])>,
    /// Frames whose partial slices were thrown away for a new key frame.
    pub restarts: u64,
    pub safe_screen: bool,
    pub serving: Option<Vec<u8>>,
    pub receipts: Vec<LeafReceipt>,
}

impl LeafDevice {
    pub fn new(wallet: WalletKey, active_set: Vec<Vec<u8>>, session_id: [u8; 32], width: u32, height: u32) -> Self {
        LeafDevice {
            wallet,
            active_set,
            session_id,
            width,
            height,
            last_link: genesis_link(&session_id),
            current: None,
            frame_store: vec![0u8; (width * height * 4) as usize],
            shown: Vec::new(),
            restarts: 0,
            safe_screen: false,
            serving: None,
            receipts: Vec::new(),
        }
    }

    /// Once per session and on each handover: the key must be active.
    pub fn attach(&mut self, validator_pk: &[u8]) -> Result<(), Refusal> {
        if !self.active_set.iter().any(|k| k == validator_pk) {
            self.safe_screen = true;
            return Err(Refusal::NotActiveValidator);
        }
        self.serving = Some(validator_pk.to_vec());
        self.safe_screen = false;
        Ok(())
    }

    pub fn on_header(&mut self, h: &FrameHeader) -> Result<(), Refusal> {
        if self.serving.is_none() || self.safe_screen {
            return Err(Refusal::NotActiveValidator);
        }
        if h.session_id != self.session_id || h.prev_link != self.last_link {
            return Err(Refusal::BrokenChain);
        }
        if !h.is_well_formed() {
            return Err(Refusal::MalformedHeader);
        }
        match &self.current {
            // Handover inside a frame: the new validator's header for the same
            // frame has the same link, so the slices already stored stay.
            Some((cur, _)) if cur.link() == h.link() => {}
            Some(_) => {
                self.restarts += 1;
                self.current = Some((h.clone(), vec![false; h.slice_hashes.len()]));
            }
            None => self.current = Some((h.clone(), vec![false; h.slice_hashes.len()])),
        }
        Ok(())
    }

    /// One slice: check its tag, decode it into the frame store. When the
    /// last slice lands, the frame is shown.
    pub fn on_slice(&mut self, idx: u32, pixels: &[u8]) -> Result<Option<u64>, Refusal> {
        let (h, have) = self.current.as_mut().ok_or(Refusal::NoHeader)?;
        if h.slice_hashes.get(idx as usize) != Some(&slice_hash(self.width, idx, pixels)) {
            return Err(Refusal::BadSliceTag);
        }
        let n = pixels.len();
        self.frame_store[idx as usize * n..(idx as usize + 1) * n].copy_from_slice(pixels);
        have[idx as usize] = true;
        if have.iter().all(|x| *x) {
            let link = h.link();
            let f = h.frame_no;
            self.shown.push((f, link));
            self.last_link = link;
            self.current = None;
            return Ok(Some(f));
        }
        Ok(None)
    }

    /// Once per second: check the signed root against the links shown, and
    /// countersign a receipt with the measured round trip.
    pub fn on_second_root(&mut self, s: &SignedSecondRoot, rtt_us: u32) -> Result<LeafReceipt, Refusal> {
        if !self.active_set.iter().any(|k| *k == s.public_key) || !s.verify() {
            return Err(Refusal::NotActiveValidator);
        }
        let first = s.root.first_frame;
        let links: Vec<[u8; 32]> =
            self.shown.iter().filter(|(f, _)| *f >= first && *f < first + s.root.count as u64).map(|(_, l)| *l).collect();
        if links.len() as u32 != s.root.count || merkle_root(&links) != s.root.links_root {
            return Err(Refusal::RootMismatch);
        }
        let r = LeafReceipt::countersign(s, links.len() as u32, rtt_us, &self.wallet);
        self.receipts.push(r.clone());
        Ok(r)
    }
}
