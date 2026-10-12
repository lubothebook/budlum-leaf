//! The validator-set light client inside U7.
//!
//! It follows `LightClient` of the tree, `src/light_client/mod.rs:162-470`:
//! one trust anchor, advanced by BLS finality certificates, strictly forward.
//!
//! The tree's light client refuses any set change (`advance`,
//! `src/light_client/mod.rs:431-449`, error `SetChanged`). A Leaf lives for
//! years across many epochs, so U7 adds one rule, [`LightClient::rotate`]:
//! the current set must finalize a checkpoint whose ancestry carries the
//! new set's hash. That rule is U7's own, not the tree's; see the README.

use alloc::vec::Vec;

use crate::bls::{verify_finality_cert, verify_pop};
use crate::chain::{
    consensus_validator_set_hash, Address, BlockHeader, ConsensusValidator, FinalityCert, ValidatorSetSnapshot,
};
use crate::U7Error;

/// Mirror of `TrustedCheckpoint`, `src/light_client/mod.rs:53-61`, plus the
/// epoch of the set, which `FinalityCert::verify` binds (`src/chain/finality.rs:803`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TrustedCheckpoint {
    pub height: u64,
    pub block_hash: [u8; 32],
    pub set_hash: [u8; 32],
    pub epoch: u64,
}

/// Mirror of `VerifiedCheckpoint`, `src/light_client/mod.rs:64-80`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct VerifiedCheckpoint {
    pub height: u64,
    pub block_hash: [u8; 32],
    pub set_hash: [u8; 32],
    pub epoch: u64,
    pub state_root: [u8; 32],
}

/// Fixed parameters of the chain the Leaf belongs to.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ChainParams {
    pub chain_id: u64,
    /// `finality_checkpoint_interval_for_chain_id`, `src/core/chain_config.rs:254-258`.
    pub checkpoint_interval: u64,
}

/// What U7 keeps of the active set: address and stake, sorted by address.
/// `40` bytes per validator; the BLS and PQ keys stay with the host and are
/// re-checked against `set_hash` on every proof, as the tree does.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ActiveSet {
    members: Vec<(Address, u64)>,
}

impl ActiveSet {
    fn from_snapshot(s: &ValidatorSetSnapshot) -> Self {
        let mut members: Vec<(Address, u64)> = s.validators.iter().map(|v| (v.address, v.stake)).collect();
        members.sort_by_key(|m| m.0);
        Self { members }
    }
    /// Stake of `addr` when it is an active validator.
    #[must_use]
    pub fn stake_of(&self, addr: &Address) -> Option<u64> {
        self.members
            .binary_search_by_key(addr, |m| m.0)
            .ok()
            .map(|i| self.members[i].1)
    }
    #[must_use]
    pub fn len(&self) -> usize {
        self.members.len()
    }
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.members.is_empty()
    }
}

/// The U7 light client.
#[derive(Debug, Clone)]
pub struct LightClient {
    params: ChainParams,
    trusted: TrustedCheckpoint,
    active: ActiveSet,
}

fn check_snapshot(params: &ChainParams, s: &ValidatorSetSnapshot) -> Result<(), U7Error> {
    // `validate_snapshot_metadata`, `src/light_client/mod.rs:205-209`.
    s.validate_metadata()?;
    // Every entry must carry a valid PoP, as the snapshot builder demands
    // (`build_validator_snapshot_from_state`, `src/chain/blockchain.rs:3535`).
    if s.validators.iter().all(|v| verify_pop(v, params.chain_id)) {
        Ok(())
    } else {
        Err(U7Error::InvalidPop)
    }
}

impl LightClient {
    /// Bootstrap from the anchor provisioned at manufacture or recovery,
    /// with the snapshot it names. Mirror of `LightClient::new`,
    /// `src/light_client/mod.rs:176-191`, plus the snapshot check.
    ///
    /// # Errors
    /// `TrustBinding` when the snapshot is not the anchored set.
    pub fn bootstrap(params: ChainParams, trusted: TrustedCheckpoint, snapshot: &ValidatorSetSnapshot) -> Result<Self, U7Error> {
        check_snapshot(&params, snapshot)?;
        if snapshot.set_hash != trusted.set_hash || snapshot.epoch != trusted.epoch {
            return Err(U7Error::TrustBinding);
        }
        Ok(Self { params, trusted, active: ActiveSet::from_snapshot(snapshot) })
    }

    #[must_use]
    pub const fn trusted(&self) -> &TrustedCheckpoint {
        &self.trusted
    }
    #[must_use]
    pub const fn params(&self) -> &ChainParams {
        &self.params
    }
    #[must_use]
    pub const fn active_set(&self) -> &ActiveSet {
        &self.active
    }
    /// `true` when `addr` is a key of the active set (gate SW-22).
    #[must_use]
    pub fn is_active_validator(&self, addr: &Address) -> bool {
        self.active.stake_of(addr).is_some()
    }

    fn is_checkpoint(&self, h: u64) -> bool {
        // `is_checkpoint_height_for_chain`, `src/chain/finality.rs:202-205`.
        self.params.checkpoint_interval != 0 && h > 0 && h.is_multiple_of(self.params.checkpoint_interval)
    }

    /// Mirror of `verify_checkpoint`, `src/light_client/mod.rs:223-268`.
    /// The header hash is recomputed, never read, so the tree's self-consistency
    /// check (`mod.rs:226`) holds by construction.
    ///
    /// # Errors
    /// One `U7Error` per failed binding or failed BLS check.
    pub fn verify_checkpoint(
        &self,
        header: &BlockHeader,
        cert: &FinalityCert,
        snapshot: &ValidatorSetSnapshot,
    ) -> Result<VerifiedCheckpoint, U7Error> {
        snapshot.validate_metadata()?;
        if header.chain_id != self.params.chain_id {
            return Err(U7Error::ChainIdMismatch);
        }
        if !self.is_checkpoint(header.index) {
            return Err(U7Error::NotCheckpointHeight);
        }
        let hash = header.calculate_hash();
        if header.index != cert.checkpoint_height || hash != cert.checkpoint_hash {
            return Err(U7Error::CertificateBinding);
        }
        if cert.set_hash != self.trusted.set_hash || snapshot.set_hash != cert.set_hash {
            return Err(U7Error::TrustBinding);
        }
        verify_finality_cert(cert, snapshot)?;
        Ok(VerifiedCheckpoint {
            height: header.index,
            block_hash: hash,
            set_hash: cert.set_hash,
            epoch: cert.epoch,
            state_root: header.state_root,
        })
    }

    /// Mirror of `advance`, `src/light_client/mod.rs:431-449`: strictly forward,
    /// same set only.
    ///
    /// # Errors
    /// `NotForward` or `TrustBinding`.
    pub fn advance(&mut self, v: &VerifiedCheckpoint) -> Result<(), U7Error> {
        if v.height <= self.trusted.height {
            return Err(U7Error::NotForward);
        }
        if v.set_hash != self.trusted.set_hash {
            return Err(U7Error::TrustBinding);
        }
        self.trusted = TrustedCheckpoint { height: v.height, block_hash: v.block_hash, set_hash: v.set_hash, epoch: v.epoch };
        Ok(())
    }

    /// Mirror of `verify_header_chain`, `src/light_client/mod.rs:373-417`:
    /// the segment continues the anchor and is contiguous and parent-linked.
    /// Returns the recomputed hash of every header.
    fn header_chain_hashes(&self, headers: &[BlockHeader]) -> Result<Vec<[u8; 32]>, U7Error> {
        let first = headers.first().ok_or(U7Error::HeaderChain)?;
        if first.index != self.trusted.height.saturating_add(1) || first.previous_hash != self.trusted.block_hash {
            return Err(U7Error::HeaderChain);
        }
        let mut hashes = Vec::with_capacity(headers.len());
        for (i, h) in headers.iter().enumerate() {
            if h.chain_id != self.params.chain_id {
                return Err(U7Error::ChainIdMismatch);
            }
            if i > 0 {
                let prev = &headers[i - 1];
                if h.index != prev.index.saturating_add(1) || h.previous_hash != hashes[i - 1] {
                    return Err(U7Error::HeaderChain);
                }
            }
            hashes.push(h.calculate_hash());
        }
        Ok(hashes)
    }

    /// Move to the next validator set (U7 rule, not in the tree).
    ///
    /// Accepts `next` when all of these hold:
    /// 1. `segment` continues the anchor, contiguous and parent-linked;
    /// 2. its last header is a checkpoint finalized by the *current* set (`cert`);
    /// 3. the first header of a later epoch commits, through `validator_set_hash`
    ///    (checked by the tree at `src/consensus/pos.rs:734-745`), to the
    ///    consensus hash of `next`, and every later header in the segment keeps it;
    /// 4. every entry of `next` carries a valid PoP.
    ///
    /// The current set thus vouches for the block that names the new set.
    /// The new set's snapshot epoch is the epoch of that header.
    ///
    /// # Errors
    /// `NoSetTransition`, `SetWitnessMismatch`, or any checkpoint error.
    pub fn rotate(
        &mut self,
        segment: &[BlockHeader],
        cert: &FinalityCert,
        current: &ValidatorSetSnapshot,
        next: &[ConsensusValidator],
    ) -> Result<ValidatorSetSnapshot, U7Error> {
        let hashes = self.header_chain_hashes(segment)?;
        let last = segment.last().ok_or(U7Error::HeaderChain)?;
        let verified = self.verify_checkpoint(last, cert, current)?;
        debug_assert_eq!(verified.block_hash, hashes[hashes.len() - 1]);

        let k = segment
            .iter()
            .position(|h| h.epoch > self.trusted.epoch)
            .ok_or(U7Error::NoSetTransition)?;
        let new_epoch = segment[k].epoch;
        let committed = consensus_validator_set_hash(self.params.chain_id, next)?;
        for h in &segment[k..] {
            if h.epoch != new_epoch || h.validator_set_hash != committed {
                return Err(U7Error::SetWitnessMismatch);
            }
        }
        let snapshot = ValidatorSetSnapshot::new(new_epoch, next.iter().map(|c| c.entry.clone()).collect());
        check_snapshot(&self.params, &snapshot)?;

        self.trusted = TrustedCheckpoint {
            height: verified.height,
            block_hash: verified.block_hash,
            set_hash: snapshot.set_hash,
            epoch: new_epoch,
        };
        self.active = ActiveSet::from_snapshot(&snapshot);
        Ok(snapshot)
    }
}
