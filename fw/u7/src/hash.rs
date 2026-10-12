//! Hash constructions copied from the Budlum tree.

use alloc::vec::Vec;
use sha2::{Digest as _, Sha256};
use sha3::Sha3_256;

/// Length-prefixed SHA-256 over fields.
/// Mirror of `hash_fields_bytes`, budlum `src/core/hash.rs:13-20`.
#[must_use]
pub fn hash_fields_bytes(fields: &[&[u8]]) -> [u8; 32] {
    let mut hasher = Sha256::new();
    for field in fields {
        hasher.update((field.len() as u64).to_le_bytes());
        hasher.update(field);
    }
    hasher.finalize().into()
}

/// One presence byte, then the root or zeros.
/// Mirror of `presence_tagged`, budlum `src/core/hash.rs:29-36`.
#[must_use]
pub fn presence_tagged(root: Option<[u8; 32]>) -> [u8; 33] {
    let mut tagged = [0u8; 33];
    if let Some(root) = root {
        tagged[0] = 1;
        tagged[1..].copy_from_slice(&root);
    }
    tagged
}

/// Lowercase hex of a 32-byte digest, as `hex::encode` writes it.
/// The tree stores hashes as these 64 ASCII bytes and hashes the ASCII form,
/// for example `self.previous_hash.as_bytes()` at `src/core/block.rs:131`.
#[must_use]
pub fn hex32(bytes: &[u8; 32]) -> [u8; 64] {
    const DIGITS: &[u8; 16] = b"0123456789abcdef";
    let mut out = [0u8; 64];
    for (i, b) in bytes.iter().enumerate() {
        out[2 * i] = DIGITS[usize::from(b >> 4)];
        out[2 * i + 1] = DIGITS[usize::from(b & 0x0f)];
    }
    out
}

/// SHA3-256 of the concatenation of `parts`.
#[must_use]
pub fn sha3(parts: &[&[u8]]) -> [u8; 32] {
    let mut h = Sha3_256::new();
    for p in parts {
        h.update(p);
    }
    h.finalize().into()
}

/// Merkle pair. Mirror of `combine_sha3`, budlum `src/consensus/merkle_tree.rs:34-43`.
#[must_use]
pub fn combine_sha3(left: &[u8; 32], right: &[u8; 32]) -> [u8; 32] {
    sha3(&[left, right])
}

/// Odd-node promotion. Mirror of `promote_sha3`, budlum `src/consensus/merkle_tree.rs:52-61`.
#[must_use]
pub fn promote_sha3(node: &[u8; 32]) -> [u8; 32] {
    sha3(&[b"BDLM_MERKLE_ODD_PROMOTE_V1", node])
}

/// Merkle root over leaves, all zeros when empty.
/// Mirror of `merkle_root` with `merkle_parent_layer`,
/// budlum `src/consensus/merkle_tree.rs:103-165`, with SHA3 combine and promote.
#[must_use]
pub fn merkle_root(leaves: &[[u8; 32]]) -> [u8; 32] {
    if leaves.is_empty() {
        return [0u8; 32];
    }
    let mut layer: Vec<[u8; 32]> = leaves.to_vec();
    while layer.len() > 1 {
        let mut next = Vec::with_capacity(layer.len().div_ceil(2));
        let mut i = 0;
        while i < layer.len() {
            if i + 1 < layer.len() {
                next.push(combine_sha3(&layer[i], &layer[i + 1]));
            } else {
                next.push(promote_sha3(&layer[i]));
            }
            i += 2;
        }
        layer = next;
    }
    layer[0]
}

/// A signed-message preimage: a domain tag, then length-prefixed fields.
/// The same framing as `hash_fields_bytes`, kept unhashed so the signer
/// signs the full message.
pub struct Preimage(Vec<u8>);

impl Preimage {
    #[must_use]
    pub fn new(tag: &[u8]) -> Self {
        let mut p = Self(Vec::with_capacity(256));
        p.field(tag);
        p
    }
    pub fn field(&mut self, bytes: &[u8]) -> &mut Self {
        self.0.extend_from_slice(&(bytes.len() as u64).to_le_bytes());
        self.0.extend_from_slice(bytes);
        self
    }
    pub fn u64(&mut self, v: u64) -> &mut Self {
        self.field(&v.to_le_bytes())
    }
    #[must_use]
    pub fn finish(&mut self) -> Vec<u8> {
        core::mem::take(&mut self.0)
    }
}
