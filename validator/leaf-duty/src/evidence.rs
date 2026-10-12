//! Slashing evidence for the Leaf duty.
//!
//! `ForgedFrameEvidence` is self-contained: any node holding the chain
//! (the session open record, the transactions, the active set) re-checks it
//! by re-executing one frame and re-rendering one slice. No trust in the
//! reporter is needed, so the report is `ProofProvenance::ConsensusVerified`
//! once `verify` passes, as `registry::evidence` requires before a slash.

use std::collections::HashMap;

use crate::app;
use crate::chain::{step_state, ChainSim};
use crate::frame::{genesis_link, FrameHeader, SignedSecondRoot};
use crate::mirror::{
    hash_fields_bytes, merkle_proof, merkle_root_from_proof, roles, Address, ProofProvenance, SlashingProof,
    SlashingReport,
};
use crate::raster::{Frame, Raster};
use crate::session::{InputTx, SessionState};
use crate::validator::{render_spec, Detection, Fault};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvidenceError {
    SignerNotActive,
    BadSignature,
    WrongSession,
    LinkNotInRoot,
    PreStateNotAuthenticated,
    TxsDoNotMatchOps,
    BadTxSignature,
    MalformedHeader,
    /// A frame that also reconciles with finality needs the replay window
    /// in the evidence; not carried in this version.
    ReconcileFrameUnsupported,
    /// Re-execution reproduced the committed frame: there is no forgery.
    NotAForgery,
}

/// The evidence that a validator signed a frame its inputs do not produce.
#[derive(Debug, Clone)]
pub struct ForgedFrameEvidence {
    pub signed_root: SignedSecondRoot,
    pub header: FrameHeader,
    pub link_index: u32,
    pub link_proof: Vec<[u8; 32]>,
    pub prev_header: Option<FrameHeader>,
    pub pre_state: SessionState,
    pub txs: Vec<InputTx>,
    pub fault: Fault,
}

fn encode_header(h: &FrameHeader) -> Vec<u8> {
    let mut b = Vec::new();
    b.extend_from_slice(&h.link());
    b.extend_from_slice(&h.frame_no.to_le_bytes());
    for x in [&h.session_id, &h.prev_link, &h.state_root, &h.frame_hash] {
        b.extend_from_slice(x);
    }
    for list in [&h.ops, &h.slice_hashes, &h.spec_leaves] {
        b.extend_from_slice(&(list.len() as u32).to_le_bytes());
        for x in list.iter() {
            b.extend_from_slice(x);
        }
    }
    b
}

impl ForgedFrameEvidence {
    /// Build the evidence from a sampler detection and the chain's mempool.
    pub fn from_detection(d: &Detection, chain: &ChainSim) -> Self {
        let idx = (d.header.frame_no - d.signed_root.root.first_frame) as usize;
        ForgedFrameEvidence {
            signed_root: d.signed_root.clone(),
            header: d.header.clone(),
            link_index: idx as u32,
            link_proof: merkle_proof(&d.second_links, idx).unwrap_or_default(),
            prev_header: d.prev_header.clone(),
            pre_state: d.pre_state.clone(),
            txs: d.header.ops.iter().filter_map(|id| chain.txs.get(id).cloned()).collect(),
            fault: d.fault.clone(),
        }
    }

    /// Re-check the evidence from scratch. `Ok(offender)` means slashable.
    pub fn verify(&self, chain: &ChainSim, raster: &Raster) -> Result<Address, EvidenceError> {
        let r = &self.signed_root.root;
        let offender = chain.validators.get(&r.validator).map(|v| v.address).ok_or(EvidenceError::SignerNotActive)?;
        if chain.validators.get(&offender).map(|v| v.public_key.as_slice()) != Some(self.signed_root.public_key.as_slice()) {
            return Err(EvidenceError::SignerNotActive);
        }
        if !self.signed_root.verify() {
            return Err(EvidenceError::BadSignature);
        }
        let session = chain.open.session_id();
        if r.session_id != session || self.header.session_id != session {
            return Err(EvidenceError::WrongSession);
        }
        let h = &self.header;
        if h.frame_no < r.first_frame
            || h.frame_no - r.first_frame != self.link_index as u64
            || merkle_root_from_proof(&h.link(), self.link_index as usize, &self.link_proof) != r.links_root
        {
            return Err(EvidenceError::LinkNotInRoot);
        }
        // The pre-state is authenticated by the hash chain.
        match &self.prev_header {
            None => {
                if h.frame_no != 0
                    || h.prev_link != genesis_link(&session)
                    || self.pre_state != SessionState::genesis(&chain.open)
                {
                    return Err(EvidenceError::PreStateNotAuthenticated);
                }
            }
            Some(p) => {
                if p.link() != h.prev_link || p.frame_no + 1 != h.frame_no || p.state_root != self.pre_state.root() {
                    return Err(EvidenceError::PreStateNotAuthenticated);
                }
            }
        }
        if h.reconciled.is_some() {
            return Err(EvidenceError::ReconcileFrameUnsupported);
        }
        let ids: Vec<[u8; 32]> = self.txs.iter().map(InputTx::id).collect();
        if ids != h.ops {
            return Err(EvidenceError::TxsDoNotMatchOps);
        }
        if !self.txs.iter().all(InputTx::verify) {
            return Err(EvidenceError::BadTxSignature);
        }
        // Re-execute the frame.
        let txs: HashMap<[u8; 32], InputTx> = self.txs.iter().map(|t| (t.id(), t.clone())).collect();
        let mut post = self.pre_state.clone();
        step_state(&mut post, &h.ops, &txs);
        if post.root() != h.state_root {
            return Ok(offender);
        }
        if !h.is_well_formed() {
            return Err(EvidenceError::MalformedHeader);
        }
        let (w, ht) = chain.open.viewport;
        match self.fault {
            Fault::StateRoot => Err(EvidenceError::NotAForgery),
            Fault::Slice(i) => {
                let scene = app::view(&post.app, w, ht);
                let (_, sh) = raster.render_slice(&scene, i);
                if h.slice_hashes.get(i as usize) != Some(&sh) {
                    Ok(offender)
                } else {
                    Err(EvidenceError::NotAForgery)
                }
            }
            Fault::Spec(i) => {
                let mut buf = Frame::new(w, ht);
                let leaves = render_spec(&post, i as usize + 1, raster, &mut buf);
                if leaves.get(i as usize) != h.spec_leaves.get(i as usize) {
                    Ok(offender)
                } else {
                    Err(EvidenceError::NotAForgery)
                }
            }
        }
    }

    /// Canonical bytes of the evidence, carried in the slashing proof.
    pub fn encode(&self) -> Vec<u8> {
        let mut b = Vec::new();
        b.extend_from_slice(&self.signed_root.root.signing_hash());
        b.extend_from_slice(&(self.signed_root.signature.len() as u32).to_le_bytes());
        b.extend_from_slice(&self.signed_root.signature);
        b.extend_from_slice(&encode_header(&self.header));
        b.extend_from_slice(&self.link_index.to_le_bytes());
        for s in &self.link_proof {
            b.extend_from_slice(s);
        }
        if let Some(p) = &self.prev_header {
            b.extend_from_slice(&encode_header(p));
        }
        b.extend_from_slice(&self.pre_state.encode());
        for t in &self.txs {
            b.extend_from_slice(&t.id());
        }
        b.extend_from_slice(match self.fault {
            Fault::StateRoot => b"state".as_slice(),
            Fault::Slice(_) => b"slice",
            Fault::Spec(_) => b"spec",
        });
        b
    }

    pub fn digest(&self) -> [u8; 32] {
        hash_fields_bytes(&[b"BDLM_LEAF_FRAME_HEADER_V1", b"evidence", &self.encode()])
    }

    /// Verify, then wrap as a Budlum `SlashingReport` under `RoleId(1)`.
    pub fn into_report(&self, chain: &ChainSim, raster: &Raster, reporter: Address) -> Result<SlashingReport, EvidenceError> {
        let offender = self.verify(chain, raster)?;
        Ok(SlashingReport {
            offender,
            role: roles::VALIDATOR,
            proof: SlashingProof::ForgedFrame {
                session_id: self.header.session_id,
                frame_no: self.header.frame_no,
                data: self.encode(),
            },
            provenance: ProofProvenance::ConsensusVerified,
            reporter: Some(reporter),
        })
    }
}

/// Two different second roots signed for the same session and second: the
/// frame-speed form of a double sign.
pub struct RootEquivocation {
    pub a: SignedSecondRoot,
    pub b: SignedSecondRoot,
}

impl RootEquivocation {
    pub fn into_report(&self, reporter: Address) -> Option<SlashingReport> {
        let (a, b) = (&self.a.root, &self.b.root);
        let ok = self.a.verify()
            && self.b.verify()
            && a.validator == b.validator
            && a.session_id == b.session_id
            && a.second == b.second
            && a.signing_hash() != b.signing_hash();
        if !ok {
            return None;
        }
        let hex = |h: [u8; 32]| h.iter().map(|x| format!("{x:02x}")).collect::<String>();
        Some(SlashingReport {
            offender: a.validator,
            role: roles::VALIDATOR,
            proof: SlashingProof::DoubleSign {
                height: a.second,
                block_hash_1: hex(a.signing_hash()),
                block_hash_2: hex(b.signing_hash()),
                signature_1: self.a.signature.clone(),
                signature_2: self.b.signature.clone(),
            },
            provenance: ProofProvenance::ConsensusVerified,
            reporter: Some(reporter),
        })
    }
}
