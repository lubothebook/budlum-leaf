//! A minimal stand-in for the Budlum chain, holding only what the Leaf duty
//! reads from it: the session open record, the admitted input transactions,
//! the finalized order per slot, the canonical state at each slot boundary,
//! the active validator set and the stakes.
//!
//! In the tree these come from `PoSEngine` finality, the mempool and the
//! `PermissionlessRegistry` of `RoleId(1)`. Here the test harness plays
//! consensus and calls `finalize_slot` once per `6 s` slot.

use std::collections::{BTreeMap, HashMap, HashSet};

use crate::mirror::{roles, Address, SlashingReport, DOUBLE_SIGN_PENALTY, FIXED_POINT_SCALE};
use crate::session::{InputTx, SessionOpen, SessionState, TxId, FRAMES_PER_SLOT};

/// Frames between the end of a slot and the frame that must reconcile with
/// its finality: `1 s` at `240 Hz` `[HYPOTHESIS]`, to be set from the
/// measured finality latency of the Budlum PoS domain.
pub const FINALITY_LAG_FRAMES: u64 = 240;

/// One finalized slot: each transaction with the frame it takes effect in.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SlotBlock {
    pub slot: u64,
    pub ordered: Vec<(u64, TxId)>,
}

#[derive(Debug, Clone)]
pub struct ValidatorEntry {
    pub address: Address,
    pub public_key: Vec<u8>,
    pub stake: u64,
    pub active: bool,
}

pub struct ChainSim {
    pub open: SessionOpen,
    pub txs: HashMap<TxId, InputTx>,
    pub finalized: Vec<SlotBlock>,
    /// `snapshots[s]` is the canonical state before frame `s * FRAMES_PER_SLOT`.
    pub snapshots: Vec<SessionState>,
    pub finalized_ids: HashSet<TxId>,
    pub validators: BTreeMap<Address, ValidatorEntry>,
    pub slashed: Vec<SlashingReport>,
}

/// Apply one frame of ops then tick: the single state transition rule that
/// every producer, follower, sampler and evidence verifier uses.
pub fn step_state(state: &mut SessionState, ops: &[TxId], txs: &HashMap<TxId, InputTx>) {
    for id in ops {
        if let Some(tx) = txs.get(id) {
            let _ = state.apply_tx(tx);
        }
    }
    state.tick();
}

impl ChainSim {
    pub fn new(open: SessionOpen) -> Self {
        let g = SessionState::genesis(&open);
        ChainSim {
            open,
            txs: HashMap::new(),
            finalized: Vec::new(),
            snapshots: vec![g],
            finalized_ids: HashSet::new(),
            validators: BTreeMap::new(),
            slashed: Vec::new(),
        }
    }

    /// Register a validator under `RoleId(1)` with a stake.
    pub fn register_validator(&mut self, address: Address, public_key: Vec<u8>, stake: u64) {
        let _ = roles::VALIDATOR;
        self.validators.insert(address, ValidatorEntry { address, public_key, stake, active: true });
    }

    pub fn is_active_key(&self, pk: &[u8]) -> Option<Address> {
        self.validators.values().find(|v| v.active && v.public_key == pk).map(|v| v.address)
    }

    pub fn active_keys(&self) -> Vec<Vec<u8>> {
        self.validators.values().filter(|v| v.active).map(|v| v.public_key.clone()).collect()
    }

    /// Admit a transaction to the mempool after the wallet check.
    pub fn admit(&mut self, tx: &InputTx) -> bool {
        if !tx.verify() {
            return false;
        }
        self.txs.insert(tx.id(), tx.clone());
        true
    }

    /// Finalize slot `s` with the order consensus agreed on, and compute the
    /// canonical state at the next slot boundary.
    pub fn finalize_slot(&mut self, slot: u64, ordered: Vec<(u64, TxId)>) {
        assert_eq!(slot as usize, self.finalized.len(), "slots finalize in order");
        let start = slot * FRAMES_PER_SLOT;
        let mut per_frame: BTreeMap<u64, Vec<TxId>> = BTreeMap::new();
        for (f, id) in &ordered {
            assert!((start..start + FRAMES_PER_SLOT).contains(f), "tx frame outside slot");
            per_frame.entry(*f).or_default().push(*id);
            self.finalized_ids.insert(*id);
        }
        let mut st = self.snapshots[slot as usize].clone();
        for f in start..start + FRAMES_PER_SLOT {
            let ops = per_frame.get(&f).map(Vec::as_slice).unwrap_or(&[]);
            step_state(&mut st, ops, &self.txs);
        }
        self.snapshots.push(st);
        self.finalized.push(SlotBlock { slot, ordered });
    }

    /// The highest finalized slot that frame `frame` must have reconciled with.
    pub fn slot_to_reconcile_at(frame: u64) -> Option<u64> {
        if frame < FRAMES_PER_SLOT + FINALITY_LAG_FRAMES {
            return None;
        }
        let f = frame - FINALITY_LAG_FRAMES;
        if f % FRAMES_PER_SLOT == 0 {
            Some(f / FRAMES_PER_SLOT - 1)
        } else {
            None
        }
    }

    /// Apply a verified slashing report: the double-sign penalty, and the
    /// offender leaves the active set (it can no longer serve a Leaf).
    pub fn slash(&mut self, report: SlashingReport) -> u64 {
        let mut burned = 0;
        if let Some(v) = self.validators.get_mut(&report.offender) {
            burned = (v.stake as u128 * DOUBLE_SIGN_PENALTY as u128 / FIXED_POINT_SCALE as u128) as u64;
            v.stake -= burned;
            v.active = false;
        }
        self.slashed.push(report);
        burned
    }
}
