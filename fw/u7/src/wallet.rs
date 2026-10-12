//! The wallet key: ML-DSA-87, held inside U7, never exported.
//!
//! The tree pins user keys to ML-DSA-87 (`WalletKeyPair`,
//! `src/crypto/primitives.rs:831-893`) and derives the address as
//! `SHA3-256("BUDLUM_ADDRESS_V2" || pk)`. Signatures are hedged FIPS 204
//! `ML-DSA.Sign` with an empty context, as the tree's `sign` is
//! (`sign_randomized(message, b"", rng)`), so the chain's
//! `verify_ml_dsa_87_signature` accepts them unchanged.

use alloc::vec::Vec;
use ml_dsa::{Keypair as _, MlDsa87, SigningKey, B32};
use zeroize::Zeroize;

use crate::chain::{wallet_address, Address};
use crate::U7Error;

/// `ML_DSA_87_PUBLIC_KEY_LEN`, `src/crypto/primitives.rs:764`.
pub const ML_DSA_87_PUBLIC_KEY_LEN: usize = 2592;
/// `ML_DSA_87_SIGNATURE_LEN`, `src/crypto/primitives.rs:766`.
pub const ML_DSA_87_SIGNATURE_LEN: usize = 4627;

/// The true random number generator of the secure element.
pub trait Entropy {
    /// Fill `buf` with fresh random bytes.
    ///
    /// # Errors
    /// `EntropyFailure` when the TRNG health test fails.
    fn fill(&mut self, buf: &mut [u8]) -> Result<(), U7Error>;
}

/// A monotonic microsecond timer inside U7. It measures every round trip
/// the receipts carry, so the validator never reports its own latency.
pub trait Clock {
    fn now_us(&self) -> u64;
}

/// The wallet key. It has no accessor for the seed or the expanded key.
pub struct WalletKey {
    sk: SigningKey<MlDsa87>,
    public_key: Vec<u8>,
    address: Address,
}

impl WalletKey {
    /// Generate a key on the device from 32 TRNG bytes (FIPS 204 `KeyGen`).
    ///
    /// # Errors
    /// `EntropyFailure`.
    pub fn generate(rng: &mut dyn Entropy) -> Result<Self, U7Error> {
        let mut seed = [0u8; 32];
        rng.fill(&mut seed)?;
        let key = Self::from_seed(&seed);
        seed.zeroize();
        Ok(key)
    }

    /// Restore from a 32-byte seed (recovery). The caller zeroizes its copy.
    #[must_use]
    pub fn from_seed(seed: &[u8; 32]) -> Self {
        let mut xi = B32::from(*seed);
        let sk = SigningKey::<MlDsa87>::from_seed(&xi);
        xi.as_mut_slice().zeroize();
        let public_key = sk.verifying_key().encode().as_slice().to_vec();
        let address = wallet_address(&public_key);
        Self { sk, public_key, address }
    }

    /// The 2592-byte public key.
    #[must_use]
    pub fn public_key(&self) -> &[u8] {
        &self.public_key
    }

    /// The account address on chain.
    #[must_use]
    pub const fn address(&self) -> Address {
        self.address
    }

    /// Hedged FIPS 204 `ML-DSA.Sign(sk, M, ctx = "")`: `M' = 0x00 || 0x00 || M`.
    ///
    /// # Errors
    /// `EntropyFailure`.
    pub fn sign(&self, message: &[u8], rng: &mut dyn Entropy) -> Result<Vec<u8>, U7Error> {
        let mut rnd = [0u8; 32];
        rng.fill(&mut rnd)?;
        let r = B32::from(rnd);
        rnd.zeroize();
        let sig = self.sk.expanded_key().sign_internal(&[&[0u8, 0u8], message], &r);
        Ok(sig.encode().as_slice().to_vec())
    }
}

/// Verify an ML-DSA-87 signature with an empty context, as the chain does
/// (`verify_ml_dsa_87_signature`, `src/crypto/primitives.rs:922-955`).
#[must_use]
pub fn verify_wallet_signature(public_key: &[u8], message: &[u8], signature: &[u8]) -> bool {
    use ml_dsa::{EncodedSignature, EncodedVerifyingKey, Signature, VerifyingKey};
    if public_key.len() != ML_DSA_87_PUBLIC_KEY_LEN || signature.len() != ML_DSA_87_SIGNATURE_LEN {
        return false;
    }
    let Ok(enc_vk) = EncodedVerifyingKey::<MlDsa87>::try_from(public_key) else { return false };
    let vk = VerifyingKey::<MlDsa87>::decode(&enc_vk);
    let Ok(enc_sig) = EncodedSignature::<MlDsa87>::try_from(signature) else { return false };
    let Some(sig) = Signature::<MlDsa87>::decode(&enc_sig) else { return false };
    vk.verify_with_context(message, b"", &sig)
}
