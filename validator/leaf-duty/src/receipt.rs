//! Receipts and coverage rewards.
//!
//! Once per second `U7` countersigns the validator's signed root with the
//! round trip it measured. The receipt follows the shape of
//! `ai::types::AiAgentPaymentReceipt`: a domain-separated `receipt_id` over
//! every field. The receipts settle the session in the slot window, and
//! they hold a live latency map on chain (FINAL 21.5.4).

use std::collections::BTreeMap;

use crate::crypto::{address_from_public_key, verify_wallet, WalletKey};
use crate::frame::{SignedSecondRoot, FRAME_HZ};
use crate::mirror::{hash_fields_bytes, Address};

/// The `30 ms` p99 target of DST-11, in microseconds.
pub const P99_TARGET_US: u32 = 30_000;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LeafReceipt {
    pub receipt_id: [u8; 32],
    pub session_id: [u8; 32],
    pub second: u64,
    pub validator: Address,
    pub links_root: [u8; 32],
    /// The hash of the validator's signature, binding the receipt to it.
    pub root_signature_hash: [u8; 32],
    pub frames_shown: u32,
    pub rtt_us: u32,
    pub wallet: Address,
    pub wallet_public_key: Vec<u8>,
    pub signature: Vec<u8>,
}

impl LeafReceipt {
    fn compute_id(&self) -> [u8; 32] {
        hash_fields_bytes(&[
            b"BDLM_LEAF_RECEIPT_V1",
            &self.session_id,
            &self.second.to_le_bytes(),
            self.validator.as_bytes(),
            &self.links_root,
            &self.root_signature_hash,
            &self.frames_shown.to_le_bytes(),
            &self.rtt_us.to_le_bytes(),
            self.wallet.as_bytes(),
        ])
    }

    pub fn countersign(s: &SignedSecondRoot, frames_shown: u32, rtt_us: u32, wallet: &WalletKey) -> Self {
        let mut r = LeafReceipt {
            receipt_id: [0; 32],
            session_id: s.root.session_id,
            second: s.root.second,
            validator: s.root.validator,
            links_root: s.root.links_root,
            root_signature_hash: hash_fields_bytes(&[b"BDLM_LEAF_RECEIPT_V1", b"sig", &s.signature]),
            frames_shown,
            rtt_us,
            wallet: wallet.address,
            wallet_public_key: wallet.public_key.clone(),
            signature: Vec::new(),
        };
        r.receipt_id = r.compute_id();
        r.signature = wallet.sign(&r.receipt_id);
        r
    }

    pub fn verify(&self) -> bool {
        self.receipt_id == self.compute_id()
            && address_from_public_key(&self.wallet_public_key) == self.wallet
            && verify_wallet(&self.wallet_public_key, &self.receipt_id, &self.signature)
    }
}

/// Nearest-rank 99th percentile, integers only.
pub fn p99(values: &mut [u32]) -> u32 {
    if values.is_empty() {
        return u32::MAX;
    }
    values.sort_unstable();
    let rank = (values.len() * 99).div_ceil(100);
    values[rank.max(1) - 1]
}

/// Coverage emission: pay each validator per served session minute, only
/// where the 99th percentile of its signed round trips is under `30 ms`.
pub fn coverage_rewards(receipts: &[LeafReceipt], reward_per_minute: u64) -> BTreeMap<Address, u64> {
    let mut by: BTreeMap<Address, (u64, Vec<u32>)> = BTreeMap::new();
    for r in receipts.iter().filter(|r| r.verify()) {
        let e = by.entry(r.validator).or_default();
        e.0 += r.frames_shown as u64;
        e.1.push(r.rtt_us);
    }
    by.into_iter()
        .map(|(v, (frames, mut rtts))| {
            let minutes = frames / (FRAME_HZ * 60);
            let pay = if p99(&mut rtts) < P99_TARGET_US { minutes * reward_per_minute } else { 0 };
            (v, pay)
        })
        .collect()
}
