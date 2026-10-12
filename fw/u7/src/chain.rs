//! Mirrors of the Budlum chain types that U7 reads.
//!
//! Strings in the tree that hold a 64-hex digest are `[u8; 32]` here. The
//! applet re-encodes them as lowercase hex wherever the tree hashes the ASCII
//! form, so a hash computed here equals the tree's hash for an honest header.

use alloc::vec::Vec;
use sha3::{Digest as _, Sha3_256};

use crate::hash::{hash_fields_bytes, hex32, presence_tagged};
use crate::U7Error;

/// Stake quorum numerator. `src/core/chain_config.rs:260`.
pub const FINALITY_QUORUM_NUMERATOR: u64 = 2;
/// Stake quorum denominator. `src/core/chain_config.rs:261`.
pub const FINALITY_QUORUM_DENOMINATOR: u64 = 3;
/// Default checkpoint interval. `src/core/chain_config.rs:252`.
pub const FINALITY_CHECKPOINT_INTERVAL: u64 = 10;
/// PoS slot, seconds. `src/consensus/pos.rs:42`.
pub const POS_SLOT_SECONDS: u64 = 6;
/// The validator role. `src/registry/role.rs` (`roles::VALIDATOR = RoleId(1)`).
pub const ROLE_VALIDATOR: u32 = 1;
/// The BLS suite tag in vote preimages. `src/chain/finality.rs:289`.
pub const BLS_SCHEME_RFC9380_V1: &str = "BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_POP_";
/// BLS G2 public key bytes (compressed). `src/chain/finality.rs:820` (`[u8; 96]`).
pub const BLS_PUBLIC_KEY_LEN: usize = 96;
/// BLS G1 signature bytes (compressed). `src/chain/finality.rs:881` (`[u8; 48]`).
pub const BLS_SIGNATURE_LEN: usize = 48;
/// Validator ML-DSA-65 public key. `src/crypto/primitives.rs:244-252`.
pub const PQ_ML_DSA_65_PUBLIC_KEY_LEN: usize = 1952;
/// schnorrkel VRF public key. `src/core/account.rs:999`.
pub const VRF_PUBLIC_KEY_LEN: usize = 32;

/// A 32-byte account address. `src/core/address.rs:6`.
///
/// For a validator it is the Ed25519 consensus public key:
/// `ConsensusSigner::address` is `Address::from(self.public_key_bytes())`,
/// `src/crypto/signer.rs:6-8`, and `BlockHeader::verify_signature` verifies
/// with the producer address as the key, `src/core/block.rs:151-162`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
pub struct Address(pub [u8; 32]);

/// Mirror of `ValidatorEntry`, `src/chain/finality.rs:25-34`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatorEntry {
    pub address: Address,
    pub stake: u64,
    pub bls_public_key: Vec<u8>,
    pub pop_signature: Vec<u8>,
    pub pq_public_key: Vec<u8>,
}

/// One active validator with all four consensus keys, as the state holds it.
/// `AccountState::consensus_validator_set_hash` reads all four,
/// `src/core/account.rs:990-1025`. U7 needs the VRF key only to match the
/// `validator_set_hash` of a header during a set transition.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConsensusValidator {
    pub entry: ValidatorEntry,
    pub vrf_public_key: Vec<u8>,
}

/// Length-prefixed key fields. Mirror of `update_consensus_keys_sha3`,
/// `src/crypto/key_set_preimage.rs:93-108`.
fn update_consensus_keys_sha3(h: &mut Sha3_256, vrf: Option<&[u8]>, bls: &[u8], pop: &[u8], pq: &[u8]) {
    let mut put = |b: &[u8]| {
        h.update((b.len() as u64).to_le_bytes());
        h.update(b);
    };
    if let Some(vrf) = vrf {
        put(vrf);
    }
    put(bls);
    put(pop);
    put(pq);
}

/// The header-committed set hash.
/// Mirror of `AccountState::consensus_validator_set_hash`, `src/core/account.rs:990-1025`.
/// The tree sorts by address (`get_active_validators`, `src/core/account.rs:980-988`);
/// U7 demands the witness already sorted, strictly, so the order is not chosen by the host.
///
/// # Errors
/// `SetWitnessNotSorted` or `BadConsensusKeyLength`.
pub fn consensus_validator_set_hash(chain_id: u64, set: &[ConsensusValidator]) -> Result<[u8; 32], U7Error> {
    for pair in set.windows(2) {
        if pair[0].entry.address >= pair[1].entry.address {
            return Err(U7Error::SetWitnessNotSorted);
        }
    }
    let mut h = Sha3_256::new();
    h.update(b"BDLM_CONSENSUS_VALIDATOR_SET_V1");
    h.update(chain_id.to_le_bytes());
    h.update((set.len() as u64).to_le_bytes());
    for v in set {
        // The tree rejects a set with incomplete keys (`src/core/account.rs:997-1009`).
        // U7 checks the lengths; the curve checks of VRF and PQ stay on the validators.
        if v.vrf_public_key.len() != VRF_PUBLIC_KEY_LEN
            || v.entry.bls_public_key.len() != BLS_PUBLIC_KEY_LEN
            || v.entry.pop_signature.len() != BLS_SIGNATURE_LEN
            || v.entry.pq_public_key.len() != PQ_ML_DSA_65_PUBLIC_KEY_LEN
        {
            return Err(U7Error::BadConsensusKeyLength);
        }
        h.update(v.entry.address.0);
        h.update(v.entry.stake.to_le_bytes());
        update_consensus_keys_sha3(
            &mut h,
            Some(&v.vrf_public_key),
            &v.entry.bls_public_key,
            &v.entry.pop_signature,
            &v.entry.pq_public_key,
        );
    }
    Ok(h.finalize().into())
}

/// Mirror of `ValidatorSetSnapshot`, `src/chain/finality.rs:17-22`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatorSetSnapshot {
    pub epoch: u64,
    pub validators: Vec<ValidatorEntry>,
    pub set_hash: [u8; 32],
    pub total_stake: u64,
}

impl ValidatorSetSnapshot {
    /// Mirror of `ValidatorSetSnapshot::new`, `src/chain/finality.rs:37-50`.
    #[must_use]
    pub fn new(epoch: u64, validators: Vec<ValidatorEntry>) -> Self {
        let total_stake = validators.iter().fold(0u64, |a, v| a.saturating_add(v.stake));
        let set_hash = Self::compute_hash(&validators);
        Self { epoch, validators, set_hash, total_stake }
    }

    /// Mirror of `compute_hash`, `src/chain/finality.rs:52-73`.
    #[must_use]
    pub fn compute_hash(validators: &[ValidatorEntry]) -> [u8; 32] {
        let mut sorted: Vec<&ValidatorEntry> = validators.iter().collect();
        sorted.sort_by_key(|v| v.address);
        let mut h = Sha3_256::new();
        for v in sorted {
            h.update(v.address.0);
            h.update(v.stake.to_le_bytes());
            update_consensus_keys_sha3(&mut h, None, &v.bls_public_key, &v.pop_signature, &v.pq_public_key);
        }
        h.finalize().into()
    }

    /// Mirror of `validate_metadata`, `src/chain/finality.rs:76-93`.
    ///
    /// # Errors
    /// `MalformedSnapshot` when the hash or the total disagrees with the list.
    pub fn validate_metadata(&self) -> Result<(), U7Error> {
        if self.set_hash != Self::compute_hash(&self.validators) {
            return Err(U7Error::MalformedSnapshot);
        }
        let sum = self.stake_sum();
        let expected = u64::try_from(sum).unwrap_or(u64::MAX);
        if self.total_stake != expected {
            return Err(U7Error::MalformedSnapshot);
        }
        Ok(())
    }

    fn stake_sum(&self) -> u128 {
        self.validators.iter().map(|v| u128::from(v.stake)).sum()
    }

    /// Mirror of `quorum_stake`, `src/chain/finality.rs:119-124`.
    #[must_use]
    pub fn quorum_stake(&self) -> u128 {
        (self.stake_sum() * u128::from(FINALITY_QUORUM_NUMERATOR)) / u128::from(FINALITY_QUORUM_DENOMINATOR) + 1
    }

    /// Mirror of `quorum_count`, `src/chain/finality.rs:129-134`.
    #[must_use]
    pub fn quorum_count(&self) -> usize {
        self.validators
            .len()
            .saturating_mul(FINALITY_QUORUM_NUMERATOR as usize)
            .div_ceil(FINALITY_QUORUM_DENOMINATOR as usize)
    }
}

/// Mirror of `FinalityCert`, `src/chain/finality.rs:156-163`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinalityCert {
    pub epoch: u64,
    pub checkpoint_height: u64,
    pub checkpoint_hash: [u8; 32],
    pub agg_sig_bls: Vec<u8>,
    pub bitmap: Vec<u8>,
    pub set_hash: [u8; 32],
}

impl FinalityCert {
    /// Mirror of `FinalityCert::signing_message`, `src/chain/finality.rs:937-939`.
    #[must_use]
    pub fn signing_message(&self) -> Vec<u8> {
        checkpoint_signing_message(self.epoch, self.checkpoint_height, &self.checkpoint_hash)
    }
}

/// Mirror of `checkpoint_signing_message`, `src/chain/finality.rs:257-265`.
#[must_use]
pub fn checkpoint_signing_message(epoch: u64, height: u64, hash: &[u8; 32]) -> Vec<u8> {
    let mut msg = Vec::with_capacity(16 + 43 + 16 + 64);
    msg.extend_from_slice(b"BUDLUM_PRECOMMIT");
    msg.extend_from_slice(BLS_SCHEME_RFC9380_V1.as_bytes());
    msg.extend_from_slice(&epoch.to_le_bytes());
    msg.extend_from_slice(&height.to_le_bytes());
    msg.extend_from_slice(&hex32(hash));
    msg
}

/// Mirror of `pop_signing_message`, `src/chain/finality.rs:270-286`.
#[must_use]
pub fn pop_signing_message(chain_id: u64, address: &Address, bls_pk: &[u8]) -> Vec<u8> {
    let mut msg = Vec::with_capacity(15 + 8 + 32 + bls_pk.len());
    msg.extend_from_slice(b"BDLM_BLS_POP_V1");
    msg.extend_from_slice(&chain_id.to_le_bytes());
    msg.extend_from_slice(&address.0);
    msg.extend_from_slice(bls_pk);
    msg
}

/// Mirror of `BlockHeader`, `src/core/block.rs:25-47`.
///
/// `slashing_evidence` is carried as the bincode bytes the tree hashes
/// (`src/core/block.rs:91-99`): U7 hashes them and never parses them.
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct BlockHeader {
    pub index: u64,
    pub timestamp: u128,
    pub previous_hash: [u8; 32],
    pub producer: Option<Address>,
    pub chain_id: u64,
    pub state_root: [u8; 32],
    pub tx_root: [u8; 32],
    pub slashing_evidence_bincode: Option<Vec<u8>>,
    pub nonce: u64,
    pub epoch: u64,
    pub slot: u64,
    pub vrf_output: Vec<u8>,
    pub vrf_proof: Vec<u8>,
    pub validator_set_hash: [u8; 32],
    pub storage_root: Option<[u8; 32]>,
    pub shards_root: Option<[u8; 32]>,
}

impl BlockHeader {
    /// The `BDLM_BLOCK_V4` header hash.
    /// Mirror of `BlockHeader::calculate_hash_bytes`, `src/core/block.rs:84-149`.
    /// U7 never takes a claimed hash: it always recomputes this one.
    #[must_use]
    pub fn calculate_hash(&self) -> [u8; 32] {
        let producer: &[u8] = self.producer.as_ref().map_or(&[], |p| &p.0);
        let evidence: &[u8] = self.slashing_evidence_bincode.as_deref().unwrap_or(&[]);
        let index = self.index.to_le_bytes();
        let timestamp = self.timestamp.to_le_bytes();
        let nonce = self.nonce.to_le_bytes();
        let chain_id = self.chain_id.to_le_bytes();
        let epoch = self.epoch.to_le_bytes();
        let slot = self.slot.to_le_bytes();
        let prev = hex32(&self.previous_hash);
        let tx_root = hex32(&self.tx_root);
        let state_root = hex32(&self.state_root);
        let set_hash = hex32(&self.validator_set_hash);
        let storage_root = presence_tagged(self.storage_root);
        let mut fields: Vec<&[u8]> = alloc::vec![
            b"BDLM_BLOCK_V4",
            &index,
            &timestamp,
            &prev,
            &tx_root,
            &nonce,
            producer,
            evidence,
            &chain_id,
            &state_root,
            &epoch,
            &slot,
            &self.vrf_output,
            &self.vrf_proof,
            &set_hash,
            &storage_root,
        ];
        if let Some(shards_root) = &self.shards_root {
            fields.push(shards_root.as_slice());
        }
        hash_fields_bytes(&fields)
    }
}

/// Wallet address from an ML-DSA-87 public key: `SHA3-256("BUDLUM_ADDRESS_V2" || pk)`.
/// Mirror of `wallet_address_from_ml_dsa_87_public_key`, `src/crypto/primitives.rs:895-914`.
#[must_use]
pub fn wallet_address(public_key: &[u8]) -> Address {
    Address(crate::hash::sha3(&[b"BUDLUM_ADDRESS_V2", public_key]))
}
