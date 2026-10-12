//! # U7: the secure-element applet of the Budlum Leaf
//!
//! The Leaf is a wallet on the nearest validator (FINAL/21, section 21.5.4).
//! This crate is the applet logic that runs inside `U7`. It is `no_std` with
//! `alloc`, so it builds for a secure-element core and for the host tests alike.
//!
//! The applet does six jobs:
//!
//! 1. holds the ML-DSA-87 wallet key and never exports it ([`wallet`]);
//! 2. keeps the active validator set current from finality proofs ([`light_client`]);
//! 3. admits a session only for an active validator key, at a proven distance ([`session`]);
//! 4. signs each touch input batch ([`session::Applet::sign_input_batch`]);
//! 5. countersigns a receipt with the round trip it measured itself ([`session::Applet::on_frame_root`]);
//! 6. signs a lease that names the on-chain program entry ([`session::SessionLease`]).
//!
//! Every chain structure is a mirror of the Budlum tree at `/home/claude/budlum`.
//! Each mirror cites the file and line it copies.

#![no_std]
#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used)]

extern crate alloc;

pub mod bls;
pub mod chain;
pub mod hash;
pub mod light_client;
pub mod session;
pub mod wallet;

/// Every refusal the applet can return. No variant carries heap data, so an
/// error path never allocates.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum U7Error {
    // light client
    MalformedSnapshot,
    TrustBinding,
    CertificateBinding,
    NotCheckpointHeight,
    BitmapNotCanonical,
    InsufficientStakeQuorum,
    InsufficientCountQuorum,
    BadBlsKey,
    BadBlsSignature,
    BlsVerifyFailed,
    InvalidPop,
    NotForward,
    HeaderChain,
    ChainIdMismatch,
    NoSetTransition,
    SetWitnessMismatch,
    SetWitnessNotSorted,
    BadConsensusKeyLength,
    // wallet
    EntropyFailure,
    // session
    NoPendingChallenge,
    ChallengeMismatch,
    BadValidatorSignature,
    NotActiveValidator,
    StaleLightClient,
    ProgramMismatch,
    ZeroProgram,
    DistanceProofFailed,
    RttOverClassLimit,
    NoActiveSession,
    SessionMismatch,
    SequenceNotNext,
    FrameRootMismatch,
    NoRttProbe,
    RttProbeMismatch,
    LeaseExpired,
    CounterExhausted,
}
