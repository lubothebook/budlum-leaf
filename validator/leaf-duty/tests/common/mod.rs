#![allow(dead_code)]

use budlum_leaf_duty::app::InputEvent;
use budlum_leaf_duty::chain::ChainSim;
use budlum_leaf_duty::crypto::{ValidatorKey, WalletKey};
use budlum_leaf_duty::fixed::Fx;
use budlum_leaf_duty::session::{InputTx, SessionOpen, TxId, FRAMES_PER_SLOT};

pub const STAKE: u64 = 1_000_000;

pub struct World {
    pub open: SessionOpen,
    pub chain: ChainSim,
    pub owner: WalletKey,
    pub collab: WalletKey,
    pub nonces: [u64; 2],
}

impl World {
    pub fn new(viewport: (u32, u32)) -> Self {
        let owner = WalletKey::from_test_seed(1);
        let collab = WalletKey::from_test_seed(2);
        let open = SessionOpen {
            program_hash: [0x42; 32],
            owner: owner.address,
            writers: vec![owner.address, collab.address],
            open_block: 7,
            viewport,
        };
        let mut chain = ChainSim::new(open.clone());
        for n in 1..=3 {
            let k = ValidatorKey::from_test_seed(n);
            chain.register_validator(k.address, k.public_key.clone(), STAKE);
        }
        World { open, chain, owner, collab, nonces: [0, 0] }
    }

    pub fn sid(&self) -> [u8; 32] {
        self.open.session_id()
    }

    /// A signed input from writer `w` (0 owner, 1 collaborator) at frame `f`.
    pub fn tx(&mut self, w: usize, f: u64, ev: InputEvent) -> InputTx {
        let key = if w == 0 { &self.owner } else { &self.collab };
        let tx = InputTx::new_signed(key, self.open.session_id(), self.nonces[w], 2 * f, ev);
        self.nonces[w] += 1;
        assert!(self.chain.admit(&tx));
        tx
    }

    /// The owner's deterministic input script: drags, flings, typing, taps,
    /// the menu and a text replace.
    pub fn script(&mut self, f: u64) -> Vec<InputTx> {
        let mut ev = Vec::new();
        if f % 3 == 0 && (f / 240) % 4 < 2 {
            ev.push(InputEvent::Scroll { dy: Fx::ratio(((f * 37) % 61) as i64 - 22, 3) });
        }
        if f % 240 == 120 {
            ev.push(InputEvent::Fling { v: Fx::ratio((f % 7) as i64 * 9 - 20, 2) });
        }
        if f % 50 == 25 {
            ev.push(InputEvent::Key(b'A' + ((f / 50) % 26) as u8));
        }
        if f % 400 == 200 {
            ev.push(InputEvent::Backspace);
        }
        if f % 500 == 450 {
            ev.push(InputEvent::Tap { x: Fx::int(800), y: Fx::int(600 + (f % 900) as i32) });
        }
        if f % 1000 == 990 || (f > 1000 && f % 1000 == 30) {
            ev.push(InputEvent::ToggleMenu);
        }
        if f % 1700 == 1600 {
            ev.push(InputEvent::SetText(b"BUD".to_vec()));
        }
        if f % 600 == 590 {
            ev.push(InputEvent::Tap { x: Fx::int(1300), y: Fx::int(2900) });
        }
        ev.into_iter().map(|e| self.tx(0, f, e)).collect()
    }

    /// Consensus adopts the serving validator's order for slot `s`.
    pub fn finalize_as_served(&mut self, slot: u64, history: &[Vec<TxId>]) {
        let ordered = order_of(slot, history);
        self.chain.finalize_slot(slot, ordered);
    }
}

pub fn order_of(slot: u64, history: &[Vec<TxId>]) -> Vec<(u64, TxId)> {
    let start = slot * FRAMES_PER_SLOT;
    (start..start + FRAMES_PER_SLOT)
        .flat_map(|g| history[g as usize].iter().map(move |id| (g, *id)))
        .collect()
}

/// True when frame `f` is the first frame after slot `f / F - 1` ended.
pub fn slot_ended_before(f: u64) -> Option<u64> {
    if f > 0 && f % FRAMES_PER_SLOT == 0 {
        Some(f / FRAMES_PER_SLOT - 1)
    } else {
        None
    }
}

pub fn write_result(name: &str, text: &str) {
    let _ = std::fs::create_dir_all("results");
    let _ = std::fs::write(format!("results/{name}"), text);
}
