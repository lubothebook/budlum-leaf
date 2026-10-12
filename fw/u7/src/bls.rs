//! BLS12-381 finality verification, mirrored from `src/chain/finality.rs`.
//!
//! Public keys are compressed G2 points (96 bytes), signatures compressed G1
//! points (48 bytes), hashed to G1 by RFC 9380 `expand_message_xmd(SHA-256)`.

use alloc::vec::Vec;
use bls12_381::hash_to_curve::{ExpandMsgXmd, HashToCurve};
use bls12_381::{G1Affine, G1Projective, G2Affine, G2Projective};
use sha2_09::Sha256;

use crate::chain::{pop_signing_message, FinalityCert, ValidatorEntry, ValidatorSetSnapshot};
use crate::U7Error;

/// `src/chain/finality.rs:298`.
pub const BLS_SIGNATURE_DST: &[u8] = b"BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_POP_";
/// `src/chain/finality.rs:299`.
pub const BLS_POP_DST: &[u8] = b"BLS_POP_BLS12381G1_XMD:SHA-256_SSWU_RO_POP_";
/// `src/chain/finality.rs:296`.
pub const BLS_RFC9380_ACTIVATION_EPOCH: u64 = 0;

/// Mirror of `hash_to_g1`, `src/chain/finality.rs:307-314`.
#[must_use]
pub fn hash_to_g1(msg: &[u8]) -> G1Affine {
    G1Affine::from(<G1Projective as HashToCurve<ExpandMsgXmd<Sha256>>>::hash_to_curve(msg, BLS_SIGNATURE_DST))
}

/// Mirror of `hash_pop_to_g1`, `src/chain/finality.rs:330-334`.
#[must_use]
pub fn hash_pop_to_g1(msg: &[u8]) -> G1Affine {
    G1Affine::from(<G1Projective as HashToCurve<ExpandMsgXmd<Sha256>>>::hash_to_curve(msg, BLS_POP_DST))
}

fn parse_pk(bytes: &[u8]) -> Result<G2Affine, U7Error> {
    let arr: [u8; 96] = bytes.try_into().map_err(|_| U7Error::BadBlsKey)?;
    let pk = G2Affine::from_compressed(&arr).into_option().ok_or(U7Error::BadBlsKey)?;
    // Subgroup and identity check, `src/chain/finality.rs:836-843`.
    if !bool::from(pk.is_torsion_free()) || bool::from(pk.is_identity()) {
        return Err(U7Error::BadBlsKey);
    }
    Ok(pk)
}

fn parse_sig(bytes: &[u8]) -> Result<G1Affine, U7Error> {
    let arr: [u8; 48] = bytes.try_into().map_err(|_| U7Error::BadBlsSignature)?;
    let sig = G1Affine::from_compressed(&arr).into_option().ok_or(U7Error::BadBlsSignature)?;
    if !bool::from(sig.is_torsion_free()) || bool::from(sig.is_identity()) {
        return Err(U7Error::BadBlsSignature);
    }
    Ok(sig)
}

fn pairing_holds(sig: &G1Affine, h_msg: &G1Affine, pk: &G2Affine) -> bool {
    let g2_neg = -G2Affine::generator();
    let r = bls12_381::multi_miller_loop(&[(sig, &g2_neg.into()), (h_msg, &(*pk).into())]).final_exponentiation();
    r == bls12_381::Gt::identity()
}

/// Mirror of `verify_pop`, `src/chain/finality.rs:402-445`.
#[must_use]
pub fn verify_pop(entry: &ValidatorEntry, chain_id: u64) -> bool {
    let Ok(pk) = parse_pk(&entry.bls_public_key) else { return false };
    let Ok(sig) = parse_sig(&entry.pop_signature) else { return false };
    let msg = pop_signing_message(chain_id, &entry.address, &entry.bls_public_key);
    pairing_holds(&sig, &hash_pop_to_g1(&msg), &pk)
}

/// Mirror of `FinalityCert::verify`, `src/chain/finality.rs:789-935`:
/// canonical bitmap, subgroup checks on every signer, exact `u128` stake
/// quorum and `ceil(2n/3)` count quorum, then one aggregate pairing.
///
/// # Errors
/// One `U7Error` per failed check, in the tree's order.
pub fn verify_finality_cert(cert: &FinalityCert, snapshot: &ValidatorSetSnapshot) -> Result<(), U7Error> {
    if cert.epoch.checked_sub(BLS_RFC9380_ACTIVATION_EPOCH).is_none() {
        return Err(U7Error::CertificateBinding);
    }
    if cert.set_hash != snapshot.set_hash {
        return Err(U7Error::TrustBinding);
    }
    if cert.epoch != snapshot.epoch {
        return Err(U7Error::CertificateBinding);
    }
    let n = snapshot.validators.len();
    if cert.bitmap.len() != n.div_ceil(8) {
        return Err(U7Error::BitmapNotCanonical);
    }
    let trailing = n % 8;
    if trailing != 0 {
        if let Some(last) = cert.bitmap.last() {
            if last >> trailing != 0 {
                return Err(U7Error::BitmapNotCanonical);
            }
        }
    }
    let mut voted_stake: u128 = 0;
    let mut voted_count = 0usize;
    let mut pks: Vec<G2Projective> = Vec::new();
    for (idx, v) in snapshot.validators.iter().enumerate() {
        if cert.bitmap[idx / 8] & (1 << (idx % 8)) != 0 {
            voted_stake += u128::from(v.stake);
            voted_count += 1;
            pks.push(G2Projective::from(parse_pk(&v.bls_public_key)?));
        }
    }
    if voted_stake < snapshot.quorum_stake() {
        return Err(U7Error::InsufficientStakeQuorum);
    }
    if voted_count < snapshot.quorum_count() {
        return Err(U7Error::InsufficientCountQuorum);
    }
    if pks.is_empty() {
        return Err(U7Error::InsufficientCountQuorum);
    }
    let mut agg = G2Projective::identity();
    for pk in pks {
        agg += pk;
    }
    let agg = G2Affine::from(agg);
    if bool::from(agg.is_identity()) {
        return Err(U7Error::BadBlsKey);
    }
    // The tree parses the aggregate without a torsion check (`finality.rs:881-891`);
    // U7 adds it, which only refuses more.
    let sig = parse_sig(&cert.agg_sig_bls)?;
    if pairing_holds(&sig, &hash_to_g1(&cert.signing_message()), &agg) {
        Ok(())
    } else {
        Err(U7Error::BlsVerifyFailed)
    }
}
