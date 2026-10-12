//! Frame commitments: the per-frame header and hash chain, the per-second
//! Merkle root that the validator signs, and the speculative-frame leaves.

use crate::crypto::{verify_validator, ValidatorKey};
use crate::mirror::{hash_fields_bytes, merkle_root, Address};
use crate::session::TxId;

pub use crate::session::FRAME_HZ;

/// One frame's header. It is streamed before the slices, so `U6` can check
/// each slice against `slice_hashes` at line rate.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrameHeader {
    pub session_id: [u8; 32],
    pub frame_no: u64,
    pub prev_link: [u8; 32],
    /// The session state root after this frame.
    pub state_root: [u8; 32],
    /// The transactions applied in this frame, in order (the optimistic order).
    pub ops: Vec<TxId>,
    /// The slice hashes; their Budlum SHA3 Merkle root is `frame_hash`.
    pub slice_hashes: Vec<[u8; 32]>,
    pub frame_hash: [u8; 32],
    /// One `spec_leaf` per speculative frame rendered from this state.
    pub spec_leaves: Vec<[u8; 32]>,
    /// `Some((slot, diverged))` when this frame reconciled with finality.
    pub reconciled: Option<(u64, bool)>,
}

pub fn genesis_link(session_id: &[u8; 32]) -> [u8; 32] {
    hash_fields_bytes(&[b"BDLM_LEAF_FRAME_HEADER_V1", b"genesis", session_id])
}

pub fn ops_root(ops: &[TxId]) -> [u8; 32] {
    merkle_root(ops)
}

impl FrameHeader {
    /// The hash-chain link of this frame. It binds the previous link, so the
    /// links form a chain that no one can reorder or splice.
    pub fn link(&self) -> [u8; 32] {
        let rec = match self.reconciled {
            None => [0u8; 10],
            Some((s, d)) => {
                let mut r = [0u8; 10];
                r[0] = 1;
                r[1..9].copy_from_slice(&s.to_le_bytes());
                r[9] = d as u8;
                r
            }
        };
        hash_fields_bytes(&[
            b"BDLM_LEAF_FRAME_HEADER_V1",
            &self.session_id,
            &self.frame_no.to_le_bytes(),
            &self.prev_link,
            &self.state_root,
            &ops_root(&self.ops),
            &self.frame_hash,
            &merkle_root(&self.spec_leaves),
            &rec,
        ])
    }

    /// The header is internally consistent: its slice hashes give its frame hash.
    pub fn is_well_formed(&self) -> bool {
        merkle_root(&self.slice_hashes) == self.frame_hash
    }
}

/// The Merkle root over one second of frame links, `240` at `240 Hz`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SecondRoot {
    pub session_id: [u8; 32],
    pub second: u64,
    pub first_frame: u64,
    pub count: u32,
    pub links_root: [u8; 32],
    pub last_link: [u8; 32],
    pub validator: Address,
}

impl SecondRoot {
    pub fn signing_hash(&self) -> [u8; 32] {
        hash_fields_bytes(&[
            b"BDLM_LEAF_SECOND_ROOT_V1",
            &self.session_id,
            &self.second.to_le_bytes(),
            &self.first_frame.to_le_bytes(),
            &self.count.to_le_bytes(),
            &self.links_root,
            &self.last_link,
            self.validator.as_bytes(),
        ])
    }
}

/// A second root with the validator's ML-DSA-65 signature.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SignedSecondRoot {
    pub root: SecondRoot,
    pub public_key: Vec<u8>,
    pub signature: Vec<u8>,
}

impl SignedSecondRoot {
    pub fn sign(root: SecondRoot, key: &ValidatorKey) -> Self {
        let signature = key.sign(&root.signing_hash());
        SignedSecondRoot { root, public_key: key.public_key.clone(), signature }
    }
    pub fn verify(&self) -> bool {
        crate::crypto::address_from_public_key(&self.public_key) == self.root.validator
            && verify_validator(&self.public_key, &self.root.signing_hash(), &self.signature)
    }
}

/// The frame hash a speculative frame commits to, bound to its base frame
/// and to the predicted action.
pub fn spec_leaf(base_frame: u64, event: &[u8], frame_hash: &[u8; 32]) -> [u8; 32] {
    hash_fields_bytes(&[b"BDLM_LEAF_SPEC_FRAME_V1", &base_frame.to_le_bytes(), event, frame_hash])
}
