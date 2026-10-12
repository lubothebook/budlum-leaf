//! Keys: ML-DSA-65 for validators, ML-DSA-87 for the Leaf wallet in `U7`.
//!
//! Mirrors `src/crypto/primitives.rs` (`PqKeyPair` with the `pq-ml-dsa`
//! backend, and `WalletKeyPair`). One difference, on purpose: signing here is
//! deterministic (FIPS 204 `sign_deterministic`), so a test run is
//! reproducible byte for byte. Upstream signs hedged; verifiers accept both.

use crate::mirror::{hash_fields_bytes, Address};
use ml_dsa::{EncodedSignature, EncodedVerifyingKey, MlDsa65, MlDsa87, Signature, SigningKey, VerifyingKey};
use sha3::{Digest as _, Sha3_256};

/// Every domain tag this crate feeds to a hash or a signature. Upstream, each
/// one joins `DOMAIN_TAGS` in `src/crypto/domain_tags.rs`.
pub const LEAF_DOMAIN_TAGS: &[&str] = &[
    "BDLM_LEAF_FRAME_HEADER_V1",
    "BDLM_LEAF_FRAME_SLICE_V1",
    "BDLM_LEAF_INPUT_TX_V1",
    "BDLM_LEAF_RECEIPT_V1",
    "BDLM_LEAF_SAMPLE_V1",
    "BDLM_LEAF_SECOND_ROOT_V1",
    "BDLM_LEAF_SESSION_OPEN_V1",
    "BDLM_LEAF_SESSION_STATE_V1",
    "BDLM_LEAF_SPEC_FRAME_V1",
    "BDLM_LEAF_ADDRESS_SEED_V1",
];

/// Mirror of `wallet_address_from_ml_dsa_87_public_key`:
/// `SHA3-256("BUDLUM_ADDRESS_V2" || public_key)`. Applied to validator keys
/// too in this crate `[HYPOTHESIS]`.
pub fn address_from_public_key(pk: &[u8]) -> Address {
    let mut h = Sha3_256::new();
    h.update(b"BUDLUM_ADDRESS_V2");
    h.update(pk);
    Address(h.finalize().into())
}

fn seed_from(label: &[u8], n: u64) -> ml_dsa::Seed {
    let s = hash_fields_bytes(&[b"BDLM_LEAF_ADDRESS_SEED_V1", label, &n.to_le_bytes()]);
    ml_dsa::Seed::from(s)
}

/// A validator key, ML-DSA-65 (the default `pq-ml-dsa` backend upstream).
pub struct ValidatorKey {
    sk: SigningKey<MlDsa65>,
    pub public_key: Vec<u8>,
    pub address: Address,
}

impl ValidatorKey {
    /// A key from a fixed test seed. Production keys come from the node keystore.
    pub fn from_test_seed(n: u64) -> Self {
        let sk = SigningKey::<MlDsa65>::from_seed(&seed_from(b"validator", n));
        let vk: VerifyingKey<MlDsa65> = sk.expanded_key().verifying_key();
        let public_key = vk.encode().to_vec();
        let address = address_from_public_key(&public_key);
        Self { sk, public_key, address }
    }

    pub fn sign(&self, msg: &[u8]) -> Vec<u8> {
        self.sk
            .expanded_key()
            .sign_deterministic(msg, b"")
            .map(|s| s.encode().to_vec())
            .unwrap_or_default()
    }
}

/// Verify an ML-DSA-65 validator signature.
pub fn verify_validator(pk: &[u8], msg: &[u8], sig: &[u8]) -> bool {
    let Ok(enc_vk) = EncodedVerifyingKey::<MlDsa65>::try_from(pk) else { return false };
    let vk = VerifyingKey::<MlDsa65>::decode(&enc_vk);
    let Ok(enc_sig) = EncodedSignature::<MlDsa65>::try_from(sig) else { return false };
    let Some(sig) = Signature::<MlDsa65>::decode(&enc_sig) else { return false };
    vk.verify_with_context(msg, &[], &sig)
}

/// The Leaf wallet key held in `U7`, ML-DSA-87 (upstream `WalletKeyPair`).
pub struct WalletKey {
    sk: SigningKey<MlDsa87>,
    pub public_key: Vec<u8>,
    pub address: Address,
}

impl WalletKey {
    pub fn from_test_seed(n: u64) -> Self {
        let sk = SigningKey::<MlDsa87>::from_seed(&seed_from(b"wallet", n));
        let vk: VerifyingKey<MlDsa87> = sk.expanded_key().verifying_key();
        let public_key = vk.encode().to_vec();
        let address = address_from_public_key(&public_key);
        Self { sk, public_key, address }
    }

    pub fn sign(&self, msg: &[u8]) -> Vec<u8> {
        self.sk
            .expanded_key()
            .sign_deterministic(msg, b"")
            .map(|s| s.encode().to_vec())
            .unwrap_or_default()
    }
}

/// Verify an ML-DSA-87 wallet signature.
pub fn verify_wallet(pk: &[u8], msg: &[u8], sig: &[u8]) -> bool {
    let Ok(enc_vk) = EncodedVerifyingKey::<MlDsa87>::try_from(pk) else { return false };
    let vk = VerifyingKey::<MlDsa87>::decode(&enc_vk);
    let Ok(enc_sig) = EncodedSignature::<MlDsa87>::try_from(sig) else { return false };
    let Some(sig) = Signature::<MlDsa87>::decode(&enc_sig) else { return false };
    vk.verify_with_context(msg, &[], &sig)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn keys_sign_and_verify() {
        let v = ValidatorKey::from_test_seed(1);
        let s = v.sign(b"m");
        assert!(verify_validator(&v.public_key, b"m", &s));
        assert!(!verify_validator(&v.public_key, b"n", &s));
        let w = WalletKey::from_test_seed(1);
        let s = w.sign(b"m");
        assert!(verify_wallet(&w.public_key, b"m", &s));
        assert_eq!(v.public_key.len(), 1952);
        assert_eq!(w.public_key.len(), 2592);
    }

    #[test]
    fn domain_tags_are_unique() {
        let mut t = LEAF_DOMAIN_TAGS.to_vec();
        t.sort();
        t.dedup();
        assert_eq!(t.len(), LEAF_DOMAIN_TAGS.len());
    }
}
