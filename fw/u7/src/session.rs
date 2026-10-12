//! Session admission, input signing, receipts and the lease.
//!
//! FINAL/21 section 21.5.4 and 21.5.8: U7 accepts a frame stream only from an
//! active validator key (gate SW-22), at the lowest proven round trip with a
//! relay-proof distance check (gate SW-24), and the session names its
//! application by the on-chain program entry.

use alloc::vec::Vec;
use ed25519_dalek::{Signature, VerifyingKey};

use crate::chain::{Address, BlockHeader, ConsensusValidator, FinalityCert, ValidatorSetSnapshot, POS_SLOT_SECONDS, ROLE_VALIDATOR};
use crate::hash::{merkle_root, presence_tagged, sha3, Preimage};
use crate::light_client::LightClient;
use crate::wallet::{Clock, Entropy, WalletKey};
use crate::U7Error;

/// Domain tags of the Leaf messages. They follow the `BDLM_*` convention of
/// `src/crypto/domain_tags.rs`; registering them there is open issue U7-3.
pub mod tags {
    pub const HELLO: &[u8] = b"BDLM_LEAF_HELLO_V1";
    pub const LEASE: &[u8] = b"BDLM_LEAF_LEASE_V1";
    pub const INPUT_BATCH: &[u8] = b"BDLM_LEAF_INPUT_BATCH_V1";
    pub const FRAME_ROOT: &[u8] = b"BDLM_LEAF_FRAME_ROOT_V1";
    pub const RECEIPT: &[u8] = b"BDLM_LEAF_RECEIPT_V1";
}

/// What the display path may show. U6 and U1 read this line; anything but
/// `Stream` shows the local safe screen (gate SW-22).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DisplayGate {
    Stream,
    SafeScreen,
}

/// The application, named by its on-chain program. Programs are named by a
/// 32-byte program hash in the tree (`program_hash`, `src/ai/types.rs:539`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ProgramEntry {
    pub program_hash: [u8; 32],
    pub entry: u32,
}

/// The radio bearer of the session, reported by U2A or U5.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Bearer {
    WiFi,
    Nr5g,
}

/// The distance class U7 proves (FINAL/21 section 21.5.4 table).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum DistanceClass {
    Room = 0,
    Metro = 1,
    Cell = 2,
    Far = 3,
}

/// An authenticated UWB ranging result from U2B (IEEE 802.15.4z STS).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct UwbRanging {
    /// Commitment to the STS key of the ranging session. The validator signs
    /// the same commitment in its hello, so a relay cannot range in its place.
    pub sts_commitment: [u8; 32],
    pub distance_cm: u32,
}

/// The evidence the radios hand to U7 with a hello.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DistanceEvidence {
    pub bearer: Bearer,
    pub uwb: Option<UwbRanging>,
}

/// Round-trip ceilings per class, microseconds. The defaults are the air and
/// network rows of the FINAL/21 section 21.5.7 table plus a `1 ms` margin;
/// `rtt_limits_follow_the_budget_table` recomputes them.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RttLimits {
    pub room_us: u64,
    pub metro_us: u64,
    pub cell_us: u64,
}

impl RttLimits {
    /// Room: air up `1.0` + network `0.1` + air down `1.0` + margin `1.0` ms.
    /// Metro: air `2.0` + city network `1.2` + `80 km` more fibre at `10 µs/km`
    /// round trip `0.8` + margin `1.0` ms. Cell: air up `2.3` + network `0.3`
    /// + air down `1.3` + margin `1.0` ms.
    pub const DEFAULT: Self = Self { room_us: 3_100, metro_us: 5_000, cell_us: 4_900 };
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AppletConfig {
    /// Highest head height a hello may claim above the U7 anchor.
    pub max_anchor_lag_blocks: u64,
    /// Lease length in blocks.
    pub lease_blocks: u64,
    /// UWB ceiling for the room class, `10 m`.
    pub room_uwb_max_cm: u32,
    pub rtt: RttLimits,
}

impl AppletConfig {
    pub const DEFAULT: Self = Self {
        // Two epochs of the mainnet (`epoch_len 100`, `src/core/chain_config.rs:128`).
        max_anchor_lag_blocks: 200,
        // One hour at the `6 s` slot.
        lease_blocks: 600,
        room_uwb_max_cm: 1_000,
        rtt: RttLimits::DEFAULT,
    };
}

/// The validator's signed answer to a U7 challenge.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatorHello {
    pub chain_id: u64,
    pub validator: Address,
    pub session_id: [u8; 32],
    pub challenge: [u8; 32],
    pub head_height: u64,
    pub program: ProgramEntry,
    pub uwb_sts_commitment: Option<[u8; 32]>,
}

impl ValidatorHello {
    #[must_use]
    pub fn signing_bytes(&self) -> Vec<u8> {
        Preimage::new(tags::HELLO)
            .u64(self.chain_id)
            .field(&self.validator.0)
            .field(&self.session_id)
            .field(&self.challenge)
            .u64(self.head_height)
            .field(&self.program.program_hash)
            .field(&self.program.entry.to_le_bytes())
            .field(&presence_tagged(self.uwb_sts_commitment))
            .finish()
    }
}

/// The session lease, signed by the wallet. It names the on-chain program
/// entry, the validator and the role it serves in.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SessionLease {
    pub chain_id: u64,
    pub wallet: Address,
    pub validator: Address,
    pub validator_role: u32,
    pub session_id: [u8; 32],
    pub program: ProgramEntry,
    pub start_height: u64,
    pub expiry_height: u64,
    pub class: DistanceClass,
    pub admission_rtt_us: u64,
}

impl SessionLease {
    #[must_use]
    pub fn signing_bytes(&self) -> Vec<u8> {
        Preimage::new(tags::LEASE)
            .u64(self.chain_id)
            .field(&self.wallet.0)
            .field(&self.validator.0)
            .field(&self.validator_role.to_le_bytes())
            .field(&self.session_id)
            .field(&self.program.program_hash)
            .field(&self.program.entry.to_le_bytes())
            .u64(self.start_height)
            .u64(self.expiry_height)
            .field(&[self.class as u8])
            .u64(self.admission_rtt_us)
            .finish()
    }
    #[must_use]
    pub fn hash(&self) -> [u8; 32] {
        sha3(&[&self.signing_bytes()])
    }
}

/// One touch input batch, signed by the wallet.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InputBatch {
    pub chain_id: u64,
    pub session_id: [u8; 32],
    pub wallet: Address,
    pub validator: Address,
    pub lease_hash: [u8; 32],
    pub batch_seq: u64,
    pub first_scan: u64,
    pub scan_count: u32,
    pub samples_hash: [u8; 32],
}

impl InputBatch {
    #[must_use]
    pub fn signing_bytes(&self) -> Vec<u8> {
        Preimage::new(tags::INPUT_BATCH)
            .u64(self.chain_id)
            .field(&self.session_id)
            .field(&self.wallet.0)
            .field(&self.validator.0)
            .field(&self.lease_hash)
            .u64(self.batch_seq)
            .u64(self.first_scan)
            .field(&self.scan_count.to_le_bytes())
            .field(&self.samples_hash)
            .finish()
    }
}

/// The validator's once-per-second Merkle root of the frame hashes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrameRoot {
    pub chain_id: u64,
    pub session_id: [u8; 32],
    pub validator: Address,
    pub seq: u64,
    pub frame_count: u32,
    pub merkle_root: [u8; 32],
    /// The U7 probe nonce, echoed so U7 measures the round trip itself.
    pub probe_echo: [u8; 32],
}

impl FrameRoot {
    #[must_use]
    pub fn signing_bytes(&self) -> Vec<u8> {
        Preimage::new(tags::FRAME_ROOT)
            .u64(self.chain_id)
            .field(&self.session_id)
            .field(&self.validator.0)
            .u64(self.seq)
            .field(&self.frame_count.to_le_bytes())
            .field(&self.merkle_root)
            .field(&self.probe_echo)
            .finish()
    }
}

/// The receipt U7 countersigns over a frame root.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Receipt {
    pub chain_id: u64,
    pub session_id: [u8; 32],
    pub wallet: Address,
    pub validator: Address,
    pub lease_hash: [u8; 32],
    pub seq: u64,
    pub frame_count: u32,
    pub merkle_root: [u8; 32],
    pub validator_sig_hash: [u8; 32],
    pub rtt_us: u64,
    pub class: DistanceClass,
}

impl Receipt {
    #[must_use]
    pub fn signing_bytes(&self) -> Vec<u8> {
        Preimage::new(tags::RECEIPT)
            .u64(self.chain_id)
            .field(&self.session_id)
            .field(&self.wallet.0)
            .field(&self.validator.0)
            .field(&self.lease_hash)
            .u64(self.seq)
            .field(&self.frame_count.to_le_bytes())
            .field(&self.merkle_root)
            .field(&self.validator_sig_hash)
            .u64(self.rtt_us)
            .field(&[self.class as u8])
            .finish()
    }
}

/// A message and the wallet's ML-DSA-87 signature over its `signing_bytes`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Signed<T> {
    pub body: T,
    pub signature: Vec<u8>,
}

/// The signed proof of a frame fault: kept for the slashing report.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrameFault {
    pub root: FrameRoot,
    pub validator_signature: [u8; 64],
    pub shown_root: [u8; 32],
    pub shown_count: u32,
}

/// One probe of a candidate validator (layer L1, once per second).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Probe {
    pub validator: Address,
    pub rtt_us: u64,
}

/// Ed25519 strict verification with the validator address as the key,
/// as `verify_signature` does, `src/crypto/primitives.rs:726-760`.
#[must_use]
pub fn verify_validator_signature(validator: &Address, message: &[u8], signature: &[u8; 64]) -> bool {
    let Ok(vk) = VerifyingKey::from_bytes(&validator.0) else { return false };
    vk.verify_strict(message, &Signature::from_bytes(signature)).is_ok()
}

#[derive(Debug, Clone, Copy)]
struct Pending {
    nonce: [u8; 32],
    session_id: [u8; 32],
    program: ProgramEntry,
    issued_us: u64,
}

#[derive(Debug, Clone)]
struct Session {
    lease: SessionLease,
    lease_hash: [u8; 32],
    expiry_us: u64,
    input_seq: u64,
    root_seq: u64,
    probe: Option<([u8; 32], u64)>,
}

/// The U7 applet.
pub struct Applet<R: Entropy, C: Clock> {
    wallet: WalletKey,
    lc: LightClient,
    rng: R,
    clock: C,
    cfg: AppletConfig,
    pending: Option<Pending>,
    session: Option<Session>,
    gate: DisplayGate,
}

impl<R: Entropy, C: Clock> Applet<R, C> {
    pub fn new(wallet: WalletKey, lc: LightClient, rng: R, clock: C, cfg: AppletConfig) -> Self {
        Self { wallet, lc, rng, clock, cfg, pending: None, session: None, gate: DisplayGate::SafeScreen }
    }

    #[must_use]
    pub const fn display_gate(&self) -> DisplayGate {
        self.gate
    }
    #[must_use]
    pub const fn light_client(&self) -> &LightClient {
        &self.lc
    }
    #[must_use]
    pub const fn wallet_address(&self) -> Address {
        self.wallet.address()
    }
    #[must_use]
    pub fn wallet_public_key(&self) -> &[u8] {
        self.wallet.public_key()
    }
    #[must_use]
    pub fn lease(&self) -> Option<&SessionLease> {
        self.session.as_ref().map(|s| &s.lease)
    }

    fn safe_screen(&mut self) {
        self.session = None;
        self.pending = None;
        self.gate = DisplayGate::SafeScreen;
    }

    /// Re-check the session after the set changed: a validator that left the
    /// set loses the stream at once.
    fn recheck_session(&mut self) {
        if let Some(s) = &self.session {
            if !self.lc.is_active_validator(&s.lease.validator) {
                self.safe_screen();
            }
        }
    }

    /// Advance the anchor with a finality certificate of the same set.
    ///
    /// # Errors
    /// Any light-client error; the anchor is unchanged on error.
    pub fn advance(&mut self, header: &BlockHeader, cert: &FinalityCert, snapshot: &ValidatorSetSnapshot) -> Result<(), U7Error> {
        let v = self.lc.verify_checkpoint(header, cert, snapshot)?;
        self.lc.advance(&v)
    }

    /// Move to the next validator set (see `LightClient::rotate`).
    ///
    /// # Errors
    /// Any light-client error; the anchor is unchanged on error.
    pub fn rotate(
        &mut self,
        segment: &[BlockHeader],
        cert: &FinalityCert,
        current: &ValidatorSetSnapshot,
        next: &[ConsensusValidator],
    ) -> Result<(), U7Error> {
        let mut lc = self.lc.clone();
        lc.rotate(segment, cert, current, next)?;
        self.lc = lc;
        self.recheck_session();
        Ok(())
    }

    /// Pick the lowest round trip among active validators (gate SW-24).
    /// A probe from a key outside the set is ignored, whatever its latency.
    #[must_use]
    pub fn select_nearest(&self, probes: &[Probe]) -> Option<Probe> {
        probes
            .iter()
            .filter(|p| self.lc.is_active_validator(&p.validator))
            .min_by_key(|p| (p.rtt_us, p.validator))
            .copied()
    }

    /// Step 1 of admission or handover: a fresh challenge. A handover keeps
    /// the session id of the running session.
    ///
    /// # Errors
    /// `EntropyFailure`, `ZeroProgram`.
    pub fn challenge(&mut self, program: ProgramEntry) -> Result<([u8; 32], [u8; 32]), U7Error> {
        if program.program_hash == [0u8; 32] {
            return Err(U7Error::ZeroProgram);
        }
        let mut nonce = [0u8; 32];
        self.rng.fill(&mut nonce)?;
        let session_id = match &self.session {
            Some(s) => s.lease.session_id,
            None => {
                let mut id = [0u8; 32];
                self.rng.fill(&mut id)?;
                id
            }
        };
        self.pending = Some(Pending { nonce, session_id, program, issued_us: self.clock.now_us() });
        Ok((nonce, session_id))
    }

    fn classify(&self, hello: &ValidatorHello, ev: &DistanceEvidence, rtt_us: u64) -> Result<DistanceClass, U7Error> {
        let lim = &self.cfg.rtt;
        match (hello.uwb_sts_commitment, ev.uwb) {
            (Some(signed), Some(ranged)) => {
                // A relay cannot hold the validator's STS key, so its ranging
                // carries another commitment, or none.
                if signed != ranged.sts_commitment || ranged.distance_cm > self.cfg.room_uwb_max_cm {
                    return Err(U7Error::DistanceProofFailed);
                }
                if rtt_us > lim.room_us {
                    return Err(U7Error::RttOverClassLimit);
                }
                return Ok(DistanceClass::Room);
            }
            (Some(_), None) => return Err(U7Error::DistanceProofFailed),
            (None, _) => {}
        }
        let ceiling = match ev.bearer {
            Bearer::WiFi => (lim.metro_us, DistanceClass::Metro),
            Bearer::Nr5g => (lim.cell_us, DistanceClass::Cell),
        };
        Ok(if rtt_us <= ceiling.0 { ceiling.1 } else { DistanceClass::Far })
    }

    fn admission_checks(
        &mut self,
        hello: &ValidatorHello,
        sig: &[u8; 64],
        ev: &DistanceEvidence,
    ) -> Result<Signed<SessionLease>, U7Error> {
        let now = self.clock.now_us();
        let p = self.pending.take().ok_or(U7Error::NoPendingChallenge)?;
        let rtt_us = now.saturating_sub(p.issued_us);
        if hello.challenge != p.nonce || hello.session_id != p.session_id {
            return Err(U7Error::ChallengeMismatch);
        }
        if hello.chain_id != self.lc.params().chain_id {
            return Err(U7Error::ChainIdMismatch);
        }
        if !verify_validator_signature(&hello.validator, &hello.signing_bytes(), sig) {
            return Err(U7Error::BadValidatorSignature);
        }
        // SW-22, first check: the key is an active validator.
        if !self.lc.is_active_validator(&hello.validator) {
            return Err(U7Error::NotActiveValidator);
        }
        // The U7 set must be recent against the head the validator claims.
        if hello.head_height > self.lc.trusted().height.saturating_add(self.cfg.max_anchor_lag_blocks) {
            return Err(U7Error::StaleLightClient);
        }
        // SW-22, second check: the stream is the program the user opened.
        if hello.program != p.program {
            return Err(U7Error::ProgramMismatch);
        }
        let class = self.classify(hello, ev, rtt_us)?;
        let lease = SessionLease {
            chain_id: hello.chain_id,
            wallet: self.wallet.address(),
            validator: hello.validator,
            validator_role: ROLE_VALIDATOR,
            session_id: hello.session_id,
            program: hello.program,
            start_height: hello.head_height,
            expiry_height: hello.head_height.saturating_add(self.cfg.lease_blocks),
            class,
            admission_rtt_us: rtt_us,
        };
        let signature = self.wallet.sign(&lease.signing_bytes(), &mut self.rng)?;
        let lease_hash = lease.hash();
        let expiry_us = now.saturating_add(self.cfg.lease_blocks.saturating_mul(POS_SLOT_SECONDS * 1_000_000));
        self.session = Some(Session { lease: lease.clone(), lease_hash, expiry_us, input_seq: 0, root_seq: 0, probe: None });
        self.gate = DisplayGate::Stream;
        Ok(Signed { body: lease, signature })
    }

    /// Step 2: admit the validator that answered the challenge, and sign the
    /// lease. A refused first admission shows the safe screen. A refused
    /// handover keeps the running session.
    ///
    /// # Errors
    /// The first failed check.
    pub fn admit(&mut self, hello: &ValidatorHello, sig: &[u8; 64], ev: &DistanceEvidence) -> Result<Signed<SessionLease>, U7Error> {
        let handover = self.session.is_some();
        let r = self.admission_checks(hello, sig, ev);
        if r.is_err() && !handover {
            self.safe_screen();
        }
        r
    }

    fn live_session(&mut self) -> Result<&mut Session, U7Error> {
        let now = self.clock.now_us();
        let expired = self.session.as_ref().is_some_and(|s| now > s.expiry_us);
        if expired {
            self.safe_screen();
            return Err(U7Error::LeaseExpired);
        }
        self.session.as_mut().ok_or(U7Error::NoActiveSession)
    }

    /// Sign one batch of touch scans (FINAL/21 section 21.5.5 step 1).
    ///
    /// # Errors
    /// `NoActiveSession`, `LeaseExpired`, `CounterExhausted`, `EntropyFailure`.
    pub fn sign_input_batch(&mut self, first_scan: u64, scan_count: u32, samples: &[u8]) -> Result<Signed<InputBatch>, U7Error> {
        let chain_id = self.lc.params().chain_id;
        let wallet = self.wallet.address();
        let s = self.live_session()?;
        let seq = s.input_seq.checked_add(1).ok_or(U7Error::CounterExhausted)?;
        let body = InputBatch {
            chain_id,
            session_id: s.lease.session_id,
            wallet,
            validator: s.lease.validator,
            lease_hash: s.lease_hash,
            batch_seq: seq,
            first_scan,
            scan_count,
            samples_hash: sha3(&[samples]),
        };
        s.input_seq = seq;
        let signature = self.wallet.sign(&body.signing_bytes(), &mut self.rng)?;
        Ok(Signed { body, signature })
    }

    /// Send a probe nonce with the next frame-root request; U7 starts its timer.
    ///
    /// # Errors
    /// `NoActiveSession`, `LeaseExpired`, `EntropyFailure`.
    pub fn begin_rtt_probe(&mut self) -> Result<[u8; 32], U7Error> {
        let mut nonce = [0u8; 32];
        self.rng.fill(&mut nonce)?;
        let now = self.clock.now_us();
        let s = self.live_session()?;
        s.probe = Some((nonce, now));
        Ok(nonce)
    }

    /// Check a signed frame root against the frames U6 showed, and countersign
    /// the receipt with the round trip U7 measured. A forged or mismatched root
    /// shows the safe screen and returns the slashing evidence.
    ///
    /// # Errors
    /// `Err(Ok(e))` for a refusal with no fault, `Err(Err(fault))` for a
    /// signed fault (wrong root over the shown frames), kept for slashing.
    pub fn on_frame_root(
        &mut self,
        root: &FrameRoot,
        sig: &[u8; 64],
        shown_frame_hashes: &[[u8; 32]],
    ) -> Result<Signed<Receipt>, Result<U7Error, alloc::boxed::Box<FrameFault>>> {
        let now = self.clock.now_us();
        let chain_id = self.lc.params().chain_id;
        let wallet = self.wallet.address();
        let s = self.live_session().map_err(Ok)?;
        if root.session_id != s.lease.session_id || root.validator != s.lease.validator || root.chain_id != chain_id {
            return Err(Ok(U7Error::SessionMismatch));
        }
        if !verify_validator_signature(&root.validator, &root.signing_bytes(), sig) {
            self.safe_screen();
            return Err(Ok(U7Error::BadValidatorSignature));
        }
        if root.seq != s.root_seq.saturating_add(1) {
            return Err(Ok(U7Error::SequenceNotNext));
        }
        let shown_root = merkle_root(shown_frame_hashes);
        let shown_count = u32::try_from(shown_frame_hashes.len()).unwrap_or(u32::MAX);
        if root.merkle_root != shown_root || root.frame_count != shown_count {
            let fault = alloc::boxed::Box::new(FrameFault { root: root.clone(), validator_signature: *sig, shown_root, shown_count });
            self.safe_screen();
            return Err(Err(fault));
        }
        let (nonce, t0) = s.probe.take().ok_or(Ok(U7Error::NoRttProbe))?;
        if nonce != root.probe_echo {
            return Err(Ok(U7Error::RttProbeMismatch));
        }
        s.root_seq = root.seq;
        let body = Receipt {
            chain_id,
            session_id: s.lease.session_id,
            wallet,
            validator: s.lease.validator,
            lease_hash: s.lease_hash,
            seq: root.seq,
            frame_count: root.frame_count,
            merkle_root: root.merkle_root,
            validator_sig_hash: sha3(&[sig]),
            rtt_us: now.saturating_sub(t0),
            class: s.lease.class,
        };
        let signature = self.wallet.sign(&body.signing_bytes(), &mut self.rng).map_err(Ok)?;
        Ok(Signed { body, signature })
    }

    /// End the session and show the safe screen.
    pub fn end_session(&mut self) {
        self.safe_screen();
    }
}
