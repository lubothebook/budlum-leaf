//! Session state as chain state.
//!
//! A Leaf session is opened on chain (`SessionOpen`), it names its program by
//! its on-chain entry, and every user action is a signed transaction
//! (`InputTx`). The state is a pure function of the open record, the ordered
//! transactions and the frame clock, so any validator rebuilds it.

use crate::app::{self, AppState, InputEvent};
use crate::crypto::{address_from_public_key, verify_wallet, WalletKey};
use crate::mirror::{hash_fields_bytes, Address};

/// The frame rate of the Leaf face, `240 Hz` (FINAL 21.2.3).
pub const FRAME_HZ: u64 = 240;
/// The touch scan, `480 Hz` (FINAL 21.5.5).
pub const SCAN_HZ: u64 = 480;
/// Frames in one Budlum slot: `6 s x 240 Hz`.
pub const FRAMES_PER_SLOT: u64 = crate::mirror::SLOT_DURATION_SECS * FRAME_HZ;

pub type TxId = [u8; 32];

/// The on-chain record that opens a session.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SessionOpen {
    /// The program entry of the application, as `ExecutionPublicInputs::program_hash`.
    pub program_hash: [u8; 32],
    pub owner: Address,
    /// Accounts that may write to the session. Index 0 is the owner.
    pub writers: Vec<Address>,
    pub open_block: u64,
    pub viewport: (u32, u32),
}

impl SessionOpen {
    pub fn session_id(&self) -> [u8; 32] {
        let writers: Vec<u8> = self.writers.iter().flat_map(|a| a.0).collect();
        hash_fields_bytes(&[
            b"BDLM_LEAF_SESSION_OPEN_V1",
            &self.program_hash,
            self.owner.as_bytes(),
            &writers,
            &self.open_block.to_le_bytes(),
            &self.viewport.0.to_le_bytes(),
            &self.viewport.1.to_le_bytes(),
        ])
    }
}

/// A user action as a chain transaction, signed by `U7` (ML-DSA-87).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InputTx {
    pub session_id: [u8; 32],
    pub from: Address,
    pub nonce: u64,
    /// The touch-scan tick at `480 Hz` when `U7` signed the batch.
    pub scan_tick: u64,
    pub event: InputEvent,
    pub public_key: Vec<u8>,
    pub signature: Vec<u8>,
}

impl InputTx {
    pub fn signing_hash(&self) -> [u8; 32] {
        hash_fields_bytes(&[
            b"BDLM_LEAF_INPUT_TX_V1",
            &self.session_id,
            self.from.as_bytes(),
            &self.nonce.to_le_bytes(),
            &self.scan_tick.to_le_bytes(),
            &self.event.encode(),
        ])
    }
    pub fn id(&self) -> TxId {
        hash_fields_bytes(&[b"BDLM_LEAF_INPUT_TX_V1", b"id", &self.signing_hash(), &self.signature])
    }
    pub fn new_signed(wallet: &WalletKey, session_id: [u8; 32], nonce: u64, scan_tick: u64, event: InputEvent) -> Self {
        let mut tx = InputTx {
            session_id,
            from: wallet.address,
            nonce,
            scan_tick,
            event,
            public_key: wallet.public_key.clone(),
            signature: Vec::new(),
        };
        tx.signature = wallet.sign(&tx.signing_hash());
        tx
    }
    /// The admission check every validator runs: key binds the sender, and
    /// the wallet signature holds.
    pub fn verify(&self) -> bool {
        address_from_public_key(&self.public_key) == self.from
            && verify_wallet(&self.public_key, &self.signing_hash(), &self.signature)
    }
}

/// The session state. It is chain state: small, canonical and hashable.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SessionState {
    pub session_id: [u8; 32],
    pub writers: Vec<Address>,
    /// The next nonce of each writer, in the order of `writers`.
    pub nonces: Vec<u64>,
    /// The number of frames ticked so far.
    pub frame_no: u64,
    pub app: AppState,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ApplyError {
    WrongSession,
    NotAWriter,
    BadNonce,
}

impl SessionState {
    pub fn genesis(open: &SessionOpen) -> Self {
        SessionState {
            session_id: open.session_id(),
            writers: open.writers.clone(),
            nonces: vec![0; open.writers.len()],
            frame_no: 0,
            app: AppState::default(),
        }
    }

    /// Apply one transaction. A failed check leaves the state untouched.
    pub fn apply_tx(&mut self, tx: &InputTx) -> Result<(), ApplyError> {
        if tx.session_id != self.session_id {
            return Err(ApplyError::WrongSession);
        }
        let w = self.writers.iter().position(|a| *a == tx.from).ok_or(ApplyError::NotAWriter)?;
        if self.nonces[w] != tx.nonce {
            return Err(ApplyError::BadNonce);
        }
        self.nonces[w] += 1;
        app::apply(&mut self.app, &tx.event);
        Ok(())
    }

    /// Advance the frame clock: animations, fling decay, cursor blink.
    pub fn tick(&mut self) {
        self.frame_no += 1;
        app::tick(&mut self.app, self.frame_no);
    }

    pub fn encode(&self) -> Vec<u8> {
        let mut b = Vec::with_capacity(256);
        b.extend_from_slice(&self.session_id);
        b.extend_from_slice(&(self.writers.len() as u32).to_le_bytes());
        for (w, n) in self.writers.iter().zip(&self.nonces) {
            b.extend_from_slice(w.as_bytes());
            b.extend_from_slice(&n.to_le_bytes());
        }
        b.extend_from_slice(&self.frame_no.to_le_bytes());
        b.extend_from_slice(&self.app.encode());
        b
    }

    pub fn root(&self) -> [u8; 32] {
        hash_fields_bytes(&[b"BDLM_LEAF_SESSION_STATE_V1", &self.encode()])
    }
}
