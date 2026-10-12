//! Types mirrored from the Budlum tree (`/home/claude/budlum`).
//!
//! Every item here is a copy of an upstream item, kept byte-compatible so the
//! Leaf duty can be moved into the tree by swapping `crate::mirror::X` for the
//! upstream path. The README lists the upstream `file:line` of each one.
//! Nothing in this module invents protocol behaviour.

use sha2::{Digest as _, Sha256};
use sha3::Sha3_256;

// ---------------------------------------------------------------------------
// src/core/address.rs
// ---------------------------------------------------------------------------

/// Mirror of `budlum_core::core::address::Address`.
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
pub struct Address(pub [u8; 32]);

impl Address {
    pub fn zero() -> Self {
        Address([0u8; 32])
    }
    pub fn as_bytes(&self) -> &[u8; 32] {
        &self.0
    }
    pub fn to_hex(&self) -> String {
        self.0.iter().map(|b| format!("{b:02x}")).collect()
    }
}

impl std::fmt::Debug for Address {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Address({})", &self.to_hex()[..16])
    }
}

// ---------------------------------------------------------------------------
// src/core/hash.rs
// ---------------------------------------------------------------------------

/// Mirror of `budlum_core::core::hash::hash_fields_bytes`: SHA-256 over
/// length-prefixed fields, so no two field lists share a preimage.
pub fn hash_fields_bytes(fields: &[&[u8]]) -> [u8; 32] {
    let mut hasher = Sha256::new();
    for field in fields {
        hasher.update((field.len() as u64).to_le_bytes());
        hasher.update(field);
    }
    hasher.finalize().into()
}

// ---------------------------------------------------------------------------
// src/registry/role.rs
// ---------------------------------------------------------------------------

/// Mirror of `budlum_core::registry::role::RoleId`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct RoleId(pub u32);

/// Mirror of `budlum_core::registry::role::roles` (the subset the duty uses).
pub mod roles {
    use super::RoleId;
    /// Consensus block-producing validator. The Leaf duty needs no new role:
    /// the same validators that produce blocks serve Leaf sessions.
    pub const VALIDATOR: RoleId = RoleId(1);
}

// ---------------------------------------------------------------------------
// src/consensus/pos.rs and src/core/chain_config.rs
// ---------------------------------------------------------------------------

/// Mirror of `chain_config::FIXED_POINT_SCALE`.
pub const FIXED_POINT_SCALE: u64 = 1_000_000;

/// Mirror of `PoSConfig::default().slot_duration` (seconds).
pub const SLOT_DURATION_SECS: u64 = 6;

/// Mirror of `PoSConfig::default().double_sign_penalty`.
pub const DOUBLE_SIGN_PENALTY: u64 = FIXED_POINT_SCALE / 2;

/// Mirror of `PoSConfig::default().slashing_penalty`.
pub const SLASHING_PENALTY: u64 = FIXED_POINT_SCALE / 10;

// ---------------------------------------------------------------------------
// src/registry/permissionless.rs and src/registry/evidence.rs
// ---------------------------------------------------------------------------

/// Mirror of `registry::permissionless::SlashingCondition`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SlashingCondition {
    DoubleSign,
    LivenessFault,
    MaliciousBehaviour,
}

/// Mirror of `registry::evidence::ProofProvenance`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProofProvenance {
    ConsensusVerified,
    Unverified,
}

/// Mirror of `registry::evidence::SlashingProof`, plus the one variant RG-18
/// proposes upstream (`ForgedFrame`). Until that variant lands, the same
/// bytes travel as `Other { tag: "LEAF_FORGED_FRAME_V1", .. }`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SlashingProof {
    DoubleSign {
        height: u64,
        block_hash_1: String,
        block_hash_2: String,
        signature_1: Vec<u8>,
        signature_2: Vec<u8>,
    },
    Liveness {
        window_start_epoch: u64,
        window_end_epoch: u64,
        missed: u64,
        expected: u64,
    },
    Other {
        tag: String,
        data: Vec<u8>,
    },
    InvalidSignatureSpam {
        epoch: u64,
        count: u64,
        threshold: u64,
    },
    /// RG-18 proposal: a signed frame commitment that re-execution refutes.
    /// `data` is the canonical encoding of `evidence::ForgedFrameEvidence`.
    ForgedFrame {
        session_id: [u8; 32],
        frame_no: u64,
        data: Vec<u8>,
    },
}

impl SlashingProof {
    /// Upstream `SlashingProof::condition`, with the RG-18 rule from
    /// FINAL 21.5.3: a forged frame is slashed like a double sign.
    pub fn condition(&self) -> SlashingCondition {
        match self {
            SlashingProof::DoubleSign { .. } => SlashingCondition::DoubleSign,
            SlashingProof::Liveness { .. } => SlashingCondition::LivenessFault,
            SlashingProof::Other { .. } => SlashingCondition::MaliciousBehaviour,
            SlashingProof::InvalidSignatureSpam { .. } => SlashingCondition::MaliciousBehaviour,
            SlashingProof::ForgedFrame { .. } => SlashingCondition::DoubleSign,
        }
    }
}

/// Mirror of `registry::evidence::SlashingReport`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SlashingReport {
    pub offender: Address,
    pub role: RoleId,
    pub proof: SlashingProof,
    pub provenance: ProofProvenance,
    pub reporter: Option<Address>,
}

// ---------------------------------------------------------------------------
// src/consensus/merkle_tree.rs
// ---------------------------------------------------------------------------

/// Mirror of `merkle_tree::combine_sha3`.
pub fn combine_sha3(left: &[u8; 32], right: &[u8; 32]) -> [u8; 32] {
    let mut h = Sha3_256::new();
    h.update(left);
    h.update(right);
    h.finalize().into()
}

/// Mirror of `merkle_tree::promote_sha3`.
pub fn promote_sha3(node: &[u8; 32]) -> [u8; 32] {
    let mut h = Sha3_256::new();
    h.update(b"BDLM_MERKLE_ODD_PROMOTE_V1");
    h.update(node);
    h.finalize().into()
}

/// Mirror of `merkle_tree::odd_promotion_sentinel`.
pub fn odd_promotion_sentinel() -> [u8; 32] {
    static S: std::sync::OnceLock<[u8; 32]> = std::sync::OnceLock::new();
    *S.get_or_init(|| hash_fields_bytes(&[b"BDLM_MERKLE_ODD_SENTINEL_V1"]))
}

fn parent_layer(layer: &[[u8; 32]]) -> Vec<[u8; 32]> {
    layer
        .chunks(2)
        .map(|c| if c.len() == 2 { combine_sha3(&c[0], &c[1]) } else { promote_sha3(&c[0]) })
        .collect()
}

/// Mirror of `merkle_tree::merkle_root` with the production SHA3 pair.
pub fn merkle_root(leaves: &[[u8; 32]]) -> [u8; 32] {
    if leaves.is_empty() {
        return [0u8; 32];
    }
    let mut layer = leaves.to_vec();
    while layer.len() > 1 {
        layer = parent_layer(&layer);
    }
    layer[0]
}

/// Mirror of `merkle_tree::merkle_proof` with the production SHA3 pair.
pub fn merkle_proof(leaves: &[[u8; 32]], leaf_index: usize) -> Option<Vec<[u8; 32]>> {
    if leaf_index >= leaves.len() {
        return None;
    }
    let mut proof = Vec::new();
    let mut layer = leaves.to_vec();
    let mut idx = leaf_index;
    while layer.len() > 1 {
        if idx % 2 == 0 && idx + 1 >= layer.len() {
            proof.push(odd_promotion_sentinel());
        } else if idx % 2 == 0 {
            proof.push(layer[idx + 1]);
        } else {
            proof.push(layer[idx - 1]);
        }
        layer = parent_layer(&layer);
        idx /= 2;
    }
    Some(proof)
}

/// Mirror of `merkle_tree::merkle_root_from_proof` with the SHA3 pair.
pub fn merkle_root_from_proof(leaf: &[u8; 32], index: usize, siblings: &[[u8; 32]]) -> [u8; 32] {
    let sentinel = odd_promotion_sentinel();
    let mut cur = *leaf;
    let mut idx = index;
    for s in siblings {
        cur = if *s == sentinel {
            promote_sha3(&cur)
        } else if idx % 2 == 0 {
            combine_sha3(&cur, s)
        } else {
            combine_sha3(s, &cur)
        };
        idx /= 2;
    }
    cur
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_proof_rebuilds_the_root() {
        for n in 1..20usize {
            let leaves: Vec<[u8; 32]> = (0..n).map(|i| [i as u8; 32]).collect();
            let root = merkle_root(&leaves);
            for i in 0..n {
                let p = merkle_proof(&leaves, i).unwrap();
                assert_eq!(merkle_root_from_proof(&leaves[i], i, &p), root);
            }
        }
    }

    #[test]
    fn odd_tail_is_promoted_never_duplicated() {
        let a = [[1u8; 32], [2u8; 32], [3u8; 32]];
        let b = [[1u8; 32], [2u8; 32], [3u8; 32], [3u8; 32]];
        assert_ne!(merkle_root(&a), merkle_root(&b));
    }

    #[test]
    fn forged_frame_is_slashed_like_a_double_sign() {
        let p = SlashingProof::ForgedFrame { session_id: [0; 32], frame_no: 0, data: vec![] };
        assert_eq!(p.condition(), SlashingCondition::DoubleSign);
    }
}
