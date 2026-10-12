#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::cell::Cell;
use std::rc::Rc;

use bls12_381::{G1Affine, G1Projective, G2Affine, Scalar};
use budlum_leaf_u7::bls::{hash_pop_to_g1, hash_to_g1};
use budlum_leaf_u7::chain::*;
use budlum_leaf_u7::hash::{hash_fields_bytes, merkle_root, sha3};
use budlum_leaf_u7::light_client::{ChainParams, LightClient, TrustedCheckpoint};
use budlum_leaf_u7::session::*;
use budlum_leaf_u7::wallet::{verify_wallet_signature, Clock, Entropy, WalletKey, ML_DSA_87_PUBLIC_KEY_LEN, ML_DSA_87_SIGNATURE_LEN};
use budlum_leaf_u7::U7Error;
use ed25519_dalek::{Signer, SigningKey};

const CHAIN: u64 = 1337;
const PARAMS: ChainParams = ChainParams { chain_id: CHAIN, checkpoint_interval: 10 };

// ---------- test fixtures ----------

struct Rng(u64);
impl Entropy for Rng {
    fn fill(&mut self, buf: &mut [u8]) -> Result<(), U7Error> {
        for chunk in buf.chunks_mut(32) {
            self.0 += 1;
            let d = sha3(&[b"test-rng", &self.0.to_le_bytes()]);
            chunk.copy_from_slice(&d[..chunk.len()]);
        }
        Ok(())
    }
}

#[derive(Clone)]
struct TestClock(Rc<Cell<u64>>);
impl Clock for TestClock {
    fn now_us(&self) -> u64 {
        self.0.get()
    }
}
impl TestClock {
    fn add(&self, us: u64) {
        self.0.set(self.0.get() + us);
    }
}

struct Val {
    ed: SigningKey,
    bls_sk: Scalar,
    cv: ConsensusValidator,
}

fn make_val(seed: u8, stake: u64) -> Val {
    let ed = SigningKey::from_bytes(&[seed; 32]);
    let address = Address(ed.verifying_key().to_bytes());
    let mut wide = [0u8; 64];
    wide[0] = seed;
    wide[1] = 0x5a;
    let bls_sk = Scalar::from_bytes_wide(&wide);
    let pk = G2Affine::from(G2Affine::generator() * bls_sk).to_compressed().to_vec();
    let pop_msg = pop_signing_message(CHAIN, &address, &pk);
    let pop = G1Affine::from(G1Projective::from(hash_pop_to_g1(&pop_msg)) * bls_sk).to_compressed().to_vec();
    let entry = ValidatorEntry { address, stake, bls_public_key: pk, pop_signature: pop, pq_public_key: vec![seed; PQ_ML_DSA_65_PUBLIC_KEY_LEN] };
    Val { ed, bls_sk, cv: ConsensusValidator { entry, vrf_public_key: vec![seed; 32] } }
}

/// A set sorted by address, as the tree's `get_active_validators` sorts it.
fn make_set(seeds: &[u8], stake: u64) -> Vec<Val> {
    let mut v: Vec<Val> = seeds.iter().map(|s| make_val(*s, stake)).collect();
    v.sort_by_key(|x| x.cv.entry.address);
    v
}

fn snapshot(epoch: u64, set: &[Val]) -> ValidatorSetSnapshot {
    ValidatorSetSnapshot::new(epoch, set.iter().map(|v| v.cv.entry.clone()).collect())
}

fn witness(set: &[Val]) -> Vec<ConsensusValidator> {
    set.iter().map(|v| v.cv.clone()).collect()
}

fn cert(snap: &ValidatorSetSnapshot, set: &[Val], signers: &[usize], height: u64, hash: [u8; 32]) -> FinalityCert {
    let mut c = FinalityCert {
        epoch: snap.epoch,
        checkpoint_height: height,
        checkpoint_hash: hash,
        agg_sig_bls: vec![],
        bitmap: vec![0u8; set.len().div_ceil(8)],
        set_hash: snap.set_hash,
    };
    let h = hash_to_g1(&c.signing_message());
    let mut agg = G1Projective::identity();
    for &i in signers {
        c.bitmap[i / 8] |= 1 << (i % 8);
        agg += G1Projective::from(h) * set[i].bls_sk;
    }
    c.agg_sig_bls = G1Affine::from(agg).to_compressed().to_vec();
    c
}

fn header(index: u64, prev: [u8; 32], epoch: u64, set_hash: [u8; 32]) -> BlockHeader {
    BlockHeader {
        index,
        timestamp: u128::from(index) * 6_000,
        previous_hash: prev,
        producer: Some(Address([7; 32])),
        chain_id: CHAIN,
        state_root: [index as u8; 32],
        tx_root: [3; 32],
        epoch,
        slot: index,
        validator_set_hash: set_hash,
        ..Default::default()
    }
}

fn segment(from: u64, prev: [u8; 32], len: u64, epoch_of: impl Fn(u64) -> u64, set_of: impl Fn(u64) -> [u8; 32]) -> Vec<BlockHeader> {
    let mut out = Vec::new();
    let mut p = prev;
    for i in from..from + len {
        let h = header(i, p, epoch_of(i), set_of(i));
        p = h.calculate_hash();
        out.push(h);
    }
    out
}

struct World {
    set: Vec<Val>,
    snap: ValidatorSetSnapshot,
    lc: LightClient,
}

fn world() -> World {
    let set = make_set(&[1, 2, 3, 4], 100);
    let snap = snapshot(1, &set);
    let anchor = TrustedCheckpoint { height: 10, block_hash: [0xaa; 32], set_hash: snap.set_hash, epoch: 1 };
    let lc = LightClient::bootstrap(PARAMS, anchor, &snap).unwrap();
    World { set, snap, lc }
}

const APP: ProgramEntry = ProgramEntry { program_hash: [0x42; 32], entry: 3 };

fn applet(lc: LightClient) -> (Applet<Rng, TestClock>, TestClock) {
    let clock = TestClock(Rc::new(Cell::new(1_000_000)));
    let wallet = WalletKey::from_seed(&[9u8; 32]);
    (Applet::new(wallet, lc, Rng(0), clock.clone(), AppletConfig::DEFAULT), clock)
}

fn hello_for(v: &Val, nonce: [u8; 32], sid: [u8; 32], uwb: Option<[u8; 32]>) -> (ValidatorHello, [u8; 64]) {
    let h = ValidatorHello {
        chain_id: CHAIN,
        validator: v.cv.entry.address,
        session_id: sid,
        challenge: nonce,
        head_height: 15,
        program: APP,
        uwb_sts_commitment: uwb,
    };
    let sig = v.ed.sign(&h.signing_bytes()).to_bytes();
    (h, sig)
}

const WIFI: DistanceEvidence = DistanceEvidence { bearer: Bearer::WiFi, uwb: None };

fn admitted(w: &World) -> (Applet<Rng, TestClock>, TestClock, Signed<SessionLease>) {
    let (mut a, clock) = applet(w.lc.clone());
    let (nonce, sid) = a.challenge(APP).unwrap();
    clock.add(3_000);
    let (h, sig) = hello_for(&w.set[0], nonce, sid, None);
    let lease = a.admit(&h, &sig, &WIFI).unwrap();
    (a, clock, lease)
}

// ---------- golden vectors (scripts/vectors.py) ----------

fn hexs(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
}

#[test]
fn golden_vectors_match_python() {
    let b = |n: usize, v: u8| vec![v; n];
    let a32 = |v: u8| [v; 32];
    let ha = BlockHeader {
        index: 20, timestamp: 1_700_000_000_000, previous_hash: a32(1), producer: Some(Address(a32(2))), chain_id: 1337,
        state_root: a32(3), tx_root: a32(4), slashing_evidence_bincode: None, nonce: 7, epoch: 2, slot: 20,
        vrf_output: b(32, 5), vrf_proof: b(64, 6), validator_set_hash: a32(7), storage_root: None, shards_root: None,
    };
    assert_eq!(hexs(&ha.calculate_hash()), "c14e325b18bd1ef0b28eeaa3b99daa99ac3ca1fe8f4bf51a71549e3113fc24ed");
    let hb = BlockHeader {
        index: 21, timestamp: 5, previous_hash: a32(9), producer: None, chain_id: 1337, state_root: a32(3), tx_root: a32(4),
        slashing_evidence_bincode: Some(b(8, 0)), nonce: 0, epoch: 2, slot: 21, vrf_output: vec![], vrf_proof: vec![],
        validator_set_hash: a32(7), storage_root: Some(a32(0)), shards_root: Some(a32(8)),
    };
    assert_eq!(hexs(&hb.calculate_hash()), "ee3fefc5031f2e76b98f268570fd9c4442821278f39c29f837768561fd24cdea");
    let e = |a: u8, s: u64, x: u8, y: u8, z: u8| ValidatorEntry { address: Address(a32(a)), stake: s, bls_public_key: b(96, x), pop_signature: b(48, y), pq_public_key: b(1952, z) };
    let vals = vec![e(0x22, 500, 1, 2, 3), e(0x11, 300, 4, 5, 6)];
    assert_eq!(hexs(&ValidatorSetSnapshot::compute_hash(&vals)), "bfcaf85fdc68229648a1fcf00447747ea3dd641661fc565340a7ab6b8a69da2f");
    let cv: Vec<ConsensusValidator> = vec![vals[1].clone(), vals[0].clone()].into_iter().map(|entry| ConsensusValidator { entry, vrf_public_key: b(32, 9) }).collect();
    assert_eq!(hexs(&consensus_validator_set_hash(1337, &cv).unwrap()), "63159ff42c0c9c8fb8d588089c70d2dfd94dac20c647b4b24784e101a92660df");
    let leaves: Vec<[u8; 32]> = (0u8..5).map(|i| [i; 32]).collect();
    assert_eq!(hexs(&merkle_root(&leaves)), "4426f805df814482c7e3517a41377f184b55fae39f38fc77302125d57bc47ed7");
    assert_eq!(hexs(&wallet_address(&b(2592, 0xab)).0), "7cd45e939c4788778a88a1d9bab7d821d0b4be3ad7fa32e62dc0b937b3ca25d2");
    let m = checkpoint_signing_message(3, 30, &a32(0xcd));
    use sha2::Digest;
    assert_eq!(hexs(&sha2::Sha256::digest(&m)), "d8dddc5807d4e680513f2cd34400d2d794a8e18f95e0c696d9b953635d9cbf9c");
    // The framing of hash_fields_bytes on a single empty field.
    assert_eq!(hash_fields_bytes(&[b""]), <[u8; 32]>::from(sha2::Sha256::digest([0u8; 8])));
}

#[test]
fn unsorted_consensus_witness_is_refused() {
    let set = make_set(&[1, 2], 10);
    let mut w = witness(&set);
    w.reverse();
    assert_eq!(consensus_validator_set_hash(CHAIN, &w), Err(U7Error::SetWitnessNotSorted));
}

// ---------- light client ----------

#[test]
fn bootstrap_binds_the_anchor_and_checks_pop() {
    let w = world();
    assert!(w.lc.is_active_validator(&w.set[2].cv.entry.address));
    assert!(!w.lc.is_active_validator(&Address([0xee; 32])));
    let wrong = TrustedCheckpoint { height: 10, block_hash: [0; 32], set_hash: [1; 32], epoch: 1 };
    assert_eq!(LightClient::bootstrap(PARAMS, wrong, &w.snap).unwrap_err(), U7Error::TrustBinding);
    let mut bad = w.snap.clone();
    bad.validators[0].pop_signature = w.snap.validators[1].pop_signature.clone();
    bad.set_hash = ValidatorSetSnapshot::compute_hash(&bad.validators);
    let anchor = TrustedCheckpoint { height: 10, block_hash: [0; 32], set_hash: bad.set_hash, epoch: 1 };
    assert_eq!(LightClient::bootstrap(PARAMS, anchor, &bad).unwrap_err(), U7Error::InvalidPop);
    let mut lying = w.snap.clone();
    lying.total_stake = 1;
    assert_eq!(lying.validate_metadata(), Err(U7Error::MalformedSnapshot));
}

#[test]
fn advance_follows_a_quorum_certificate() {
    let mut w = world();
    let seg = segment(11, [0xaa; 32], 10, |_| 1, |_| [5; 32]);
    let last = seg.last().unwrap();
    let c = cert(&w.snap, &w.set, &[0, 1, 2], 20, last.calculate_hash());
    let v = w.lc.verify_checkpoint(last, &c, &w.snap).unwrap();
    w.lc.advance(&v).unwrap();
    assert_eq!(w.lc.trusted().height, 20);
    assert_eq!(w.lc.trusted().block_hash, last.calculate_hash());
    assert_eq!(w.lc.advance(&v), Err(U7Error::NotForward));
}

#[test]
fn advance_refuses_weak_or_unbound_certificates() {
    let w = world();
    let h = header(20, [1; 32], 1, [5; 32]);
    let hash = h.calculate_hash();
    // 2 of 4 equal stakes: 200 < 267.
    let c = cert(&w.snap, &w.set, &[0, 1], 20, hash);
    assert_eq!(w.lc.verify_checkpoint(&h, &c, &w.snap), Err(U7Error::InsufficientStakeQuorum));
    // A certificate over another hash.
    let c = cert(&w.snap, &w.set, &[0, 1, 2], 20, [9; 32]);
    assert_eq!(w.lc.verify_checkpoint(&h, &c, &w.snap), Err(U7Error::CertificateBinding));
    // A bitmap that claims a signer whose signature is missing.
    let mut c = cert(&w.snap, &w.set, &[0, 1], 20, hash);
    c.bitmap[0] |= 1 << 2;
    assert_eq!(w.lc.verify_checkpoint(&h, &c, &w.snap), Err(U7Error::BlsVerifyFailed));
    // A padded bitmap.
    let mut c = cert(&w.snap, &w.set, &[0, 1, 2], 20, hash);
    c.bitmap.push(0);
    assert_eq!(w.lc.verify_checkpoint(&h, &c, &w.snap), Err(U7Error::BitmapNotCanonical));
    // Not a checkpoint height.
    let h2 = header(21, [1; 32], 1, [5; 32]);
    let c = cert(&w.snap, &w.set, &[0, 1, 2], 21, h2.calculate_hash());
    assert_eq!(w.lc.verify_checkpoint(&h2, &c, &w.snap), Err(U7Error::NotCheckpointHeight));
    // A foreign set.
    let other = make_set(&[7, 8, 9], 100);
    let osnap = snapshot(1, &other);
    let c = cert(&osnap, &other, &[0, 1, 2], 20, hash);
    assert_eq!(w.lc.verify_checkpoint(&h, &c, &osnap), Err(U7Error::TrustBinding));
}

#[test]
fn count_quorum_holds_against_a_stake_whale() {
    let mut set = make_set(&[1, 2, 3, 4], 1);
    set[0].cv.entry.stake = 1_000;
    let snap = snapshot(1, &set);
    let anchor = TrustedCheckpoint { height: 10, block_hash: [0xaa; 32], set_hash: snap.set_hash, epoch: 1 };
    let lc = LightClient::bootstrap(PARAMS, anchor, &snap).unwrap();
    let h = header(20, [1; 32], 1, [5; 32]);
    let c = cert(&snap, &set, &[0, 1], 20, h.calculate_hash());
    assert_eq!(lc.verify_checkpoint(&h, &c, &snap), Err(U7Error::InsufficientCountQuorum));
}

#[test]
fn rotate_moves_to_the_next_set_vouched_by_the_current_set() {
    let mut w = world();
    let next = make_set(&[2, 3, 4, 5], 100);
    let next_hash = consensus_validator_set_hash(CHAIN, &witness(&next)).unwrap();
    let seg = segment(11, [0xaa; 32], 10, |i| if i >= 15 { 2 } else { 1 }, |i| if i >= 15 { next_hash } else { [5; 32] });
    let last = seg.last().unwrap();
    let c = cert(&w.snap, &w.set, &[0, 1, 3], 20, last.calculate_hash());
    let snap2 = w.lc.rotate(&seg, &c, &w.snap, &witness(&next)).unwrap();
    assert_eq!(w.lc.trusted().epoch, 2);
    assert_eq!(w.lc.trusted().set_hash, snap2.set_hash);
    let leaver = w.set.iter().find(|v| !next.iter().any(|n| n.cv.entry.address == v.cv.entry.address)).unwrap();
    assert!(!w.lc.is_active_validator(&leaver.cv.entry.address));
    let joiner = next.iter().find(|v| !w.set.iter().any(|n| n.cv.entry.address == v.cv.entry.address)).unwrap();
    assert!(w.lc.is_active_validator(&joiner.cv.entry.address));
    // The new set now finalizes on its own.
    let seg2 = segment(21, w.lc.trusted().block_hash, 10, |_| 2, |_| next_hash);
    let last2 = seg2.last().unwrap();
    let c2 = cert(&snap2, &next, &[0, 1, 2], 30, last2.calculate_hash());
    let v = w.lc.verify_checkpoint(last2, &c2, &snap2).unwrap();
    w.lc.advance(&v).unwrap();
    assert_eq!(w.lc.trusted().height, 30);
}

#[test]
fn rotate_refuses_a_set_the_chain_did_not_commit() {
    let w = world();
    let next = make_set(&[2, 3, 4, 5], 100);
    let forged = make_set(&[6, 7, 8], 100);
    let next_hash = consensus_validator_set_hash(CHAIN, &witness(&next)).unwrap();
    let seg = segment(11, [0xaa; 32], 10, |i| if i >= 15 { 2 } else { 1 }, |i| if i >= 15 { next_hash } else { [5; 32] });
    let c = cert(&w.snap, &w.set, &[0, 1, 2], 20, seg.last().unwrap().calculate_hash());
    assert_eq!(w.lc.clone().rotate(&seg, &c, &w.snap, &witness(&forged)), Err(U7Error::SetWitnessMismatch));
    // No epoch change in the segment.
    let flat = segment(11, [0xaa; 32], 10, |_| 1, |_| next_hash);
    let c = cert(&w.snap, &w.set, &[0, 1, 2], 20, flat.last().unwrap().calculate_hash());
    assert_eq!(w.lc.clone().rotate(&flat, &c, &w.snap, &witness(&next)), Err(U7Error::NoSetTransition));
    // A segment that does not continue the anchor.
    let loose = segment(11, [0xbb; 32], 10, |i| if i >= 15 { 2 } else { 1 }, |_| next_hash);
    let c = cert(&w.snap, &w.set, &[0, 1, 2], 20, loose.last().unwrap().calculate_hash());
    assert_eq!(w.lc.clone().rotate(&loose, &c, &w.snap, &witness(&next)), Err(U7Error::HeaderChain));
    // The new set cannot vouch for itself.
    let snap_next = snapshot(1, &next);
    let c = cert(&snap_next, &next, &[0, 1, 2], 20, seg.last().unwrap().calculate_hash());
    assert_eq!(w.lc.clone().rotate(&seg, &c, &snap_next, &witness(&next)), Err(U7Error::TrustBinding));
}

// ---------- wallet ----------

#[test]
fn wallet_signatures_are_chain_ml_dsa_87() {
    let k = WalletKey::from_seed(&[9u8; 32]);
    assert_eq!(k.public_key().len(), ML_DSA_87_PUBLIC_KEY_LEN);
    assert_eq!(k.address(), wallet_address(k.public_key()));
    let mut rng = Rng(77);
    let sig = k.sign(b"budlum", &mut rng).unwrap();
    assert_eq!(sig.len(), ML_DSA_87_SIGNATURE_LEN);
    assert!(verify_wallet_signature(k.public_key(), b"budlum", &sig));
    assert!(!verify_wallet_signature(k.public_key(), b"budlun", &sig));
    // Hedged: two signatures of one message differ, both verify.
    let sig2 = k.sign(b"budlum", &mut rng).unwrap();
    assert_ne!(sig, sig2);
    assert!(verify_wallet_signature(k.public_key(), b"budlum", &sig2));
    // The same seed is the same key.
    assert_eq!(WalletKey::from_seed(&[9u8; 32]).address(), k.address());
    let g = WalletKey::generate(&mut Rng(5)).unwrap();
    assert_ne!(g.address(), k.address());
}

// ---------- session: SW-22 ----------

#[test]
fn sw22_active_validator_is_admitted_and_the_lease_names_the_program() {
    let w = world();
    let (a, _clock, lease) = admitted(&w);
    assert_eq!(a.display_gate(), DisplayGate::Stream);
    assert_eq!(lease.body.program, APP);
    assert_eq!(lease.body.validator_role, 1);
    assert_eq!(lease.body.validator, w.set[0].cv.entry.address);
    assert_eq!(lease.body.class, DistanceClass::Metro);
    assert_eq!(lease.body.admission_rtt_us, 3_000);
    assert_eq!(lease.body.expiry_height, 15 + 600);
    assert!(verify_wallet_signature(a.wallet_public_key(), &lease.body.signing_bytes(), &lease.signature));
}

#[test]
fn sw22_a_key_outside_the_active_set_gets_the_safe_screen() {
    let w = world();
    let (mut a, _) = applet(w.lc.clone());
    let outsider = make_val(99, 100);
    let (nonce, sid) = a.challenge(APP).unwrap();
    let (h, sig) = hello_for(&outsider, nonce, sid, None);
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::NotActiveValidator);
    assert_eq!(a.display_gate(), DisplayGate::SafeScreen);
    assert!(a.sign_input_batch(0, 8, b"x").is_err());
}

#[test]
fn sw22_forged_replayed_or_wrong_program_hellos_are_refused() {
    let w = world();
    let (mut a, _) = applet(w.lc.clone());
    // Forged: signed by another key than the named validator.
    let (nonce, sid) = a.challenge(APP).unwrap();
    let (mut h, _) = hello_for(&w.set[0], nonce, sid, None);
    let sig = w.set[1].ed.sign(&h.signing_bytes()).to_bytes();
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::BadValidatorSignature);
    // Replayed: the challenge is single use.
    let sig = w.set[0].ed.sign(&h.signing_bytes()).to_bytes();
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::NoPendingChallenge);
    // Old challenge against a new one.
    let (_n2, sid2) = a.challenge(APP).unwrap();
    h.session_id = sid2;
    let sig = w.set[0].ed.sign(&h.signing_bytes()).to_bytes();
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::ChallengeMismatch);
    // Another program than the one the user opened.
    let (nonce, sid) = a.challenge(APP).unwrap();
    let (mut h, _) = hello_for(&w.set[0], nonce, sid, None);
    h.program.entry = 4;
    let sig = w.set[0].ed.sign(&h.signing_bytes()).to_bytes();
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::ProgramMismatch);
    // A zero program is not an on-chain program.
    assert_eq!(a.challenge(ProgramEntry { program_hash: [0; 32], entry: 0 }).unwrap_err(), U7Error::ZeroProgram);
    // A head far beyond the U7 anchor: U7 must catch up first.
    let (nonce, sid) = a.challenge(APP).unwrap();
    let (mut h, _) = hello_for(&w.set[0], nonce, sid, None);
    h.head_height = 10 + 201;
    let sig = w.set[0].ed.sign(&h.signing_bytes()).to_bytes();
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::StaleLightClient);
    assert_eq!(a.display_gate(), DisplayGate::SafeScreen);
}

#[test]
fn sw22_a_validator_rotated_out_loses_the_stream() {
    let w = world();
    let (mut a, _clock, _) = admitted(&w);
    // The next set drops set[0], the serving validator.
    let next: Vec<Val> = make_set(&[1, 2, 3, 4], 100).into_iter().skip(1).collect();
    let next_hash = consensus_validator_set_hash(CHAIN, &witness(&next)).unwrap();
    let seg = segment(11, [0xaa; 32], 10, |i| if i >= 12 { 2 } else { 1 }, |i| if i >= 12 { next_hash } else { [5; 32] });
    let c = cert(&w.snap, &w.set, &[1, 2, 3], 20, seg.last().unwrap().calculate_hash());
    a.rotate(&seg, &c, &w.snap, &witness(&next)).unwrap();
    assert_eq!(a.display_gate(), DisplayGate::SafeScreen);
    assert!(a.lease().is_none());
}

// ---------- session: SW-24 ----------

#[test]
fn sw24_uwb_room_proof_and_relay_refusal() {
    let w = world();
    let sts = [0x55; 32];
    let room = DistanceEvidence { bearer: Bearer::WiFi, uwb: Some(UwbRanging { sts_commitment: sts, distance_cm: 320 }) };
    let (mut a, clock) = applet(w.lc.clone());
    let (nonce, sid) = a.challenge(APP).unwrap();
    clock.add(2_100);
    let (h, sig) = hello_for(&w.set[1], nonce, sid, Some(sts));
    assert_eq!(a.admit(&h, &sig, &room).unwrap().body.class, DistanceClass::Room);

    // A relay ranges with its own STS key: the commitment differs.
    let (mut a, clock) = applet(w.lc.clone());
    let (nonce, sid) = a.challenge(APP).unwrap();
    clock.add(2_100);
    let (h, sig) = hello_for(&w.set[1], nonce, sid, Some([0x66; 32]));
    assert_eq!(a.admit(&h, &sig, &room).unwrap_err(), U7Error::DistanceProofFailed);
    assert_eq!(a.display_gate(), DisplayGate::SafeScreen);

    // A relay that forwards the true STS exchange still adds round trip.
    let (mut a, clock) = applet(w.lc.clone());
    let (nonce, sid) = a.challenge(APP).unwrap();
    clock.add(9_000);
    let (h, sig) = hello_for(&w.set[1], nonce, sid, Some(sts));
    assert_eq!(a.admit(&h, &sig, &room).unwrap_err(), U7Error::RttOverClassLimit);

    // A room claim with no ranging at all.
    let (mut a, _) = applet(w.lc.clone());
    let (nonce, sid) = a.challenge(APP).unwrap();
    let (h, sig) = hello_for(&w.set[1], nonce, sid, Some(sts));
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::DistanceProofFailed);
}

#[test]
fn sw24_classes_follow_the_measured_round_trip() {
    let w = world();
    for (bearer, rtt, class) in [
        (Bearer::WiFi, 5_000, DistanceClass::Metro),
        (Bearer::WiFi, 5_001, DistanceClass::Far),
        (Bearer::Nr5g, 4_900, DistanceClass::Cell),
        (Bearer::Nr5g, 30_000, DistanceClass::Far),
    ] {
        let (mut a, clock) = applet(w.lc.clone());
        let (nonce, sid) = a.challenge(APP).unwrap();
        clock.add(rtt);
        let (h, sig) = hello_for(&w.set[2], nonce, sid, None);
        let lease = a.admit(&h, &sig, &DistanceEvidence { bearer, uwb: None }).unwrap();
        assert_eq!(lease.body.class, class, "{bearer:?} {rtt}");
    }
}

#[test]
fn sw24_nearest_is_the_lowest_round_trip_among_active_keys() {
    let w = world();
    let (a, _) = applet(w.lc.clone());
    let outsider = make_val(99, 100).cv.entry.address;
    let probes = [
        Probe { validator: w.set[0].cv.entry.address, rtt_us: 4_000 },
        Probe { validator: outsider, rtt_us: 100 },
        Probe { validator: w.set[3].cv.entry.address, rtt_us: 2_500 },
        Probe { validator: w.set[1].cv.entry.address, rtt_us: 9_000 },
    ];
    assert_eq!(a.select_nearest(&probes).unwrap().validator, w.set[3].cv.entry.address);
    assert!(a.select_nearest(&probes[1..2]).is_none());
}

#[test]
fn rtt_limits_follow_the_budget_table() {
    // FINAL/21 section 21.5.7 rows, in tenths of a millisecond.
    let margin = 10;
    let room = 10 + 1 + 10 + margin;
    let metro = 10 + 12 + 8 + 10 + margin; // 80 km more fibre at 10 us/km round trip
    let cell = 23 + 3 + 13 + margin;
    assert_eq!(RttLimits::DEFAULT.room_us, room * 100);
    assert_eq!(RttLimits::DEFAULT.metro_us, metro * 100);
    assert_eq!(RttLimits::DEFAULT.cell_us, cell * 100);
}

// ---------- input batches, receipts, handover ----------

#[test]
fn input_batches_are_signed_in_sequence() {
    let w = world();
    let (mut a, _clock, lease) = admitted(&w);
    let b1 = a.sign_input_batch(0, 8, b"touch-samples-1").unwrap();
    let b2 = a.sign_input_batch(8, 8, b"touch-samples-2").unwrap();
    assert_eq!((b1.body.batch_seq, b2.body.batch_seq), (1, 2));
    assert_eq!(b1.body.lease_hash, lease.body.hash());
    assert_eq!(b1.body.samples_hash, sha3(&[b"touch-samples-1"]));
    assert!(verify_wallet_signature(a.wallet_public_key(), &b2.body.signing_bytes(), &b2.signature));
}

fn frame_root(v: &Val, sid: [u8; 32], seq: u64, frames: &[[u8; 32]], echo: [u8; 32]) -> (FrameRoot, [u8; 64]) {
    let r = FrameRoot {
        chain_id: CHAIN,
        session_id: sid,
        validator: v.cv.entry.address,
        seq,
        frame_count: frames.len() as u32,
        merkle_root: merkle_root(frames),
        probe_echo: echo,
    };
    let sig = v.ed.sign(&r.signing_bytes()).to_bytes();
    (r, sig)
}

#[test]
fn receipts_carry_the_round_trip_u7_measured() {
    let w = world();
    let (mut a, clock, lease) = admitted(&w);
    let sid = lease.body.session_id;
    let frames: Vec<[u8; 32]> = (0..240u32).map(|i| sha3(&[&i.to_le_bytes()])).collect();
    let probe = a.begin_rtt_probe().unwrap();
    clock.add(2_750);
    let (r, sig) = frame_root(&w.set[0], sid, 1, &frames, probe);
    let rc = a.on_frame_root(&r, &sig, &frames).unwrap();
    assert_eq!(rc.body.rtt_us, 2_750);
    assert_eq!(rc.body.frame_count, 240);
    assert_eq!(rc.body.validator_sig_hash, sha3(&[&sig]));
    assert!(verify_wallet_signature(a.wallet_public_key(), &rc.body.signing_bytes(), &rc.signature));
    // A replay of the same root is not the next sequence.
    let _ = a.begin_rtt_probe().unwrap();
    assert_eq!(a.on_frame_root(&r, &sig, &frames).unwrap_err(), Ok(U7Error::SequenceNotNext));
    // No probe, no receipt: the validator cannot pick its own latency.
    let (mut a, _c, lease) = admitted(&w);
    let (r, sig) = frame_root(&w.set[0], lease.body.session_id, 1, &frames, [0; 32]);
    assert_eq!(a.on_frame_root(&r, &sig, &frames).unwrap_err(), Ok(U7Error::NoRttProbe));
    let _ = a.begin_rtt_probe().unwrap();
    assert_eq!(a.on_frame_root(&r, &sig, &frames).unwrap_err(), Ok(U7Error::RttProbeMismatch));
}

#[test]
fn a_root_over_other_frames_is_a_signed_fault() {
    let w = world();
    let (mut a, _clock, lease) = admitted(&w);
    let shown: Vec<[u8; 32]> = (0..10u8).map(|i| [i; 32]).collect();
    let mut claimed = shown.clone();
    claimed[4] = [0xff; 32];
    let probe = a.begin_rtt_probe().unwrap();
    let (r, sig) = frame_root(&w.set[0], lease.body.session_id, 1, &claimed, probe);
    let fault = a.on_frame_root(&r, &sig, &shown).unwrap_err().unwrap_err();
    assert_eq!(fault.shown_root, merkle_root(&shown));
    assert!(verify_validator_signature(&fault.root.validator, &fault.root.signing_bytes(), &fault.validator_signature));
    assert_eq!(a.display_gate(), DisplayGate::SafeScreen);
}

#[test]
fn a_root_signed_by_another_key_gets_the_safe_screen() {
    let w = world();
    let (mut a, _clock, lease) = admitted(&w);
    let frames = [[1u8; 32]];
    let probe = a.begin_rtt_probe().unwrap();
    let (r, _) = frame_root(&w.set[0], lease.body.session_id, 1, &frames, probe);
    let sig = w.set[1].ed.sign(&r.signing_bytes()).to_bytes();
    assert_eq!(a.on_frame_root(&r, &sig, &frames).unwrap_err(), Ok(U7Error::BadValidatorSignature));
    assert_eq!(a.display_gate(), DisplayGate::SafeScreen);
}

#[test]
fn handover_keeps_the_session_and_a_failed_one_keeps_the_stream() {
    let w = world();
    let (mut a, clock, lease) = admitted(&w);
    let sid = lease.body.session_id;
    // A failed handover to an outsider: the primary keeps streaming.
    let (nonce, sid2) = a.challenge(APP).unwrap();
    assert_eq!(sid2, sid);
    let (h, sig) = hello_for(&make_val(99, 1), nonce, sid, None);
    assert_eq!(a.admit(&h, &sig, &WIFI).unwrap_err(), U7Error::NotActiveValidator);
    assert_eq!(a.display_gate(), DisplayGate::Stream);
    assert_eq!(a.lease().unwrap().validator, w.set[0].cv.entry.address);
    // A good handover to the hot shadow.
    let (nonce, _) = a.challenge(APP).unwrap();
    clock.add(1_500);
    let (h, sig) = hello_for(&w.set[3], nonce, sid, None);
    let l2 = a.admit(&h, &sig, &WIFI).unwrap();
    assert_eq!(l2.body.session_id, sid);
    assert_eq!(l2.body.validator, w.set[3].cv.entry.address);
    assert_eq!(a.display_gate(), DisplayGate::Stream);
}

#[test]
fn an_expired_lease_ends_the_stream() {
    let w = world();
    let (mut a, clock, _) = admitted(&w);
    clock.add(600 * 6 * 1_000_000 + 1);
    assert_eq!(a.sign_input_batch(0, 1, b"").unwrap_err(), U7Error::LeaseExpired);
    assert_eq!(a.display_gate(), DisplayGate::SafeScreen);
}
