//! The demo application: a wallet feed with a scrolling list, a balance, a
//! text field, a button, a menu and two images. It stands for an on-chain
//! program: `apply` and `tick` are its state transition, `view` its scene.
//! All of it runs in design units of the `1600 x 3200` panel, in Q16.16.

use crate::fixed::Fx;
use crate::scene::{Prim, Rgba, Scene};

pub const DESIGN_W: i32 = 1600;
pub const DESIGN_H: i32 = 3200;
const TOP_H: i32 = 200;
const BOTTOM_Y: i32 = 2800;
const ROW_H: i32 = 260;
const ROWS: i32 = 64;
const MAX_TEXT: usize = 24;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InputEvent {
    /// Drag the list by `dy` design pixels.
    Scroll { dy: Fx },
    /// Release with a velocity in design pixels per frame.
    Fling { v: Fx },
    Tap { x: Fx, y: Fx },
    Key(u8),
    Backspace,
    /// Replace the text field. It does not commute with `Key`, which is
    /// what the reconciliation test needs.
    SetText(Vec<u8>),
    ToggleMenu,
}

impl InputEvent {
    pub fn encode(&self) -> Vec<u8> {
        let mut b = Vec::new();
        match self {
            InputEvent::Scroll { dy } => {
                b.push(1);
                b.extend_from_slice(&dy.to_le_bytes());
            }
            InputEvent::Fling { v } => {
                b.push(2);
                b.extend_from_slice(&v.to_le_bytes());
            }
            InputEvent::Tap { x, y } => {
                b.push(3);
                b.extend_from_slice(&x.to_le_bytes());
                b.extend_from_slice(&y.to_le_bytes());
            }
            InputEvent::Key(k) => b.extend_from_slice(&[4, *k]),
            InputEvent::Backspace => b.push(5),
            InputEvent::SetText(t) => {
                b.push(6);
                b.extend_from_slice(&(t.len() as u32).to_le_bytes());
                b.extend_from_slice(t);
            }
            InputEvent::ToggleMenu => b.push(7),
        }
        b
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct AppState {
    pub scroll: Fx,
    pub velocity: Fx,
    pub selected: i32,
    pub balance: u64,
    pub text: Vec<u8>,
    pub menu_open: bool,
    pub anim: u64,
}

impl AppState {
    pub fn encode(&self) -> Vec<u8> {
        let mut b = Vec::new();
        b.extend_from_slice(&self.scroll.to_le_bytes());
        b.extend_from_slice(&self.velocity.to_le_bytes());
        b.extend_from_slice(&self.selected.to_le_bytes());
        b.extend_from_slice(&self.balance.to_le_bytes());
        b.extend_from_slice(&(self.text.len() as u32).to_le_bytes());
        b.extend_from_slice(&self.text);
        b.push(self.menu_open as u8);
        b.extend_from_slice(&self.anim.to_le_bytes());
        b
    }
}

fn max_scroll() -> Fx {
    Fx::int(ROWS * ROW_H - (BOTTOM_Y - TOP_H))
}

/// The state transition of one input.
pub fn apply(s: &mut AppState, e: &InputEvent) {
    match e {
        InputEvent::Scroll { dy } => {
            s.scroll = (s.scroll + *dy).clamp(Fx::ZERO, max_scroll());
            s.velocity = Fx::ZERO;
        }
        InputEvent::Fling { v } => s.velocity = *v,
        InputEvent::Tap { x, y } => {
            let (x, y) = (x.floor(), y.floor());
            if y < TOP_H {
                if x >= 1300 {
                    s.menu_open = !s.menu_open;
                }
            } else if y >= BOTTOM_Y {
                if (1220..1540).contains(&x) {
                    s.balance = s.balance.wrapping_add(1);
                }
            } else if !s.menu_open {
                let row = (Fx::int(y - TOP_H) + s.scroll).floor() / ROW_H;
                s.selected = row;
            }
        }
        InputEvent::Key(k) => {
            if s.text.len() < MAX_TEXT {
                s.text.push(*k);
            }
        }
        InputEvent::Backspace => {
            s.text.pop();
        }
        InputEvent::SetText(t) => {
            s.text = t.iter().copied().take(MAX_TEXT).collect();
        }
        InputEvent::ToggleMenu => s.menu_open = !s.menu_open,
    }
}

/// The frame-clock transition: fling decay at `243/256` per frame.
pub fn tick(s: &mut AppState, frame_no: u64) {
    if s.velocity != Fx::ZERO {
        s.scroll = (s.scroll + s.velocity).clamp(Fx::ZERO, max_scroll());
        s.velocity = s.velocity.scale256(243);
        if s.velocity.0.abs() < (1 << 12) {
            s.velocity = Fx::ZERO;
        }
    }
    s.anim = frame_no;
}

/// The actions the validator renders ahead as speculative frames.
pub fn predictions(s: &AppState) -> Vec<InputEvent> {
    let next_row_y = Fx::int(TOP_H + ROW_H / 2 + ((s.selected + 1).max(0) * ROW_H)) - s.scroll;
    vec![
        InputEvent::Scroll { dy: Fx::int(48) },
        InputEvent::Scroll { dy: Fx::int(-48) },
        InputEvent::ToggleMenu,
        InputEvent::Tap { x: Fx::int(800), y: next_row_y.clamp(Fx::int(TOP_H), Fx::int(BOTTOM_Y - 1)) },
    ]
}

fn fmt_u64(mut v: u64) -> Vec<u8> {
    let mut d = Vec::new();
    loop {
        d.push(b'0' + (v % 10) as u8);
        v /= 10;
        if v == 0 {
            break;
        }
    }
    d.reverse();
    d
}

/// The scene of a state at a viewport. Design units scale by `width / 1600`.
pub fn view(s: &AppState, width: u32, height: u32) -> Scene {
    let k = Fx::ratio(width as i64, DESIGN_W as i64);
    let d = |v: i32| Fx::int(v).mul(k);
    let df = |v: Fx| v.mul(k);
    let gs = |n: u32| (n * width / DESIGN_W as u32).max(1);
    let mut p = Vec::with_capacity(96);

    // The list, under the bars.
    let first = (s.scroll.floor() / ROW_H).max(0);
    let last = ((s.scroll.floor() + BOTTOM_Y - TOP_H) / ROW_H + 1).min(ROWS - 1);
    for i in first..=last {
        let y = Fx::int(TOP_H + i * ROW_H) - s.scroll;
        let sel = i == s.selected;
        let card = if sel {
            Rgba::opaque(46, 120, 220)
        } else if i % 2 == 0 {
            Rgba::opaque(32, 38, 52)
        } else {
            Rgba::opaque(38, 44, 60)
        };
        p.push(Prim::Rect { x: d(60), y: df(y + Fx::int(15)), w: d(1480), h: d(ROW_H - 30), radius: d(28), color: card });
        let mut label = b"ROW ".to_vec();
        label.extend(fmt_u64(i as u64));
        label.extend_from_slice(b"  BUD ");
        label.extend(fmt_u64((i as u64 * 7919 + s.balance) % 100_000));
        p.push(Prim::Glyphs { x: d(110), y: df(y + Fx::int(60)), scale: gs(5), text: label, color: Rgba::opaque(230, 236, 245) });
        if i % 6 == 3 {
            p.push(Prim::Image { id: (i / 6 % 2) as u32, x: d(1100), y: df(y + Fx::int(40)), w: d(380), h: d(180), opacity: 255 });
        }
    }

    // The top bar, its title, the balance and a spinner.
    p.push(Prim::Rect { x: d(0), y: d(0), w: d(DESIGN_W), h: d(TOP_H), radius: Fx::ZERO, color: Rgba::new(8, 10, 16, 235) });
    p.push(Prim::Glyphs { x: d(60), y: d(50), scale: gs(6), text: b"BUDLUM LEAF".to_vec(), color: Rgba::opaque(250, 250, 250) });
    let mut bal = b"BAL ".to_vec();
    bal.extend(fmt_u64(s.balance));
    p.push(Prim::Glyphs { x: d(900), y: d(70), scale: gs(4), text: bal, color: Rgba::opaque(120, 230, 160) });
    for j in 0..8i32 {
        let phase = ((s.anim / 6) as i32 + j) % 8;
        let (ox, oy) = [(0, -40), (28, -28), (40, 0), (28, 28), (0, 40), (-28, 28), (-40, 0), (-28, -28)][j as usize];
        p.push(Prim::Rect {
            x: d(1480 + ox - 9),
            y: d(100 + oy - 9),
            w: d(18),
            h: d(18),
            radius: d(9),
            color: Rgba::new(255, 255, 255, (40 + phase * 30) as u8),
        });
    }

    // The bottom bar: the text field with a blinking cursor, and the + button.
    p.push(Prim::Rect { x: d(0), y: d(BOTTOM_Y), w: d(DESIGN_W), h: d(DESIGN_H - BOTTOM_Y), radius: Fx::ZERO, color: Rgba::opaque(18, 20, 28) });
    p.push(Prim::Rect { x: d(60), y: d(2860), w: d(1100), h: d(160), radius: d(40), color: Rgba::opaque(236, 238, 242) });
    let mut t = s.text.clone();
    if (s.anim / 120) % 2 == 0 {
        t.push(b'|');
    }
    p.push(Prim::Glyphs { x: d(110), y: d(2895), scale: gs(5), text: t, color: Rgba::opaque(20, 24, 32) });
    p.push(Prim::Rect { x: d(1220), y: d(2860), w: d(320), h: d(160), radius: d(80), color: Rgba::opaque(46, 120, 220) });
    p.push(Prim::Glyphs { x: d(1350), y: d(2900), scale: gs(6), text: b"+".to_vec(), color: Rgba::opaque(255, 255, 255) });

    // The menu, a translucent sheet.
    if s.menu_open {
        p.push(Prim::Rect { x: d(0), y: d(0), w: d(DESIGN_W), h: d(DESIGN_H), radius: Fx::ZERO, color: Rgba::new(0, 0, 0, 150) });
        p.push(Prim::Rect { x: d(760), y: d(220), w: d(800), h: d(760), radius: d(36), color: Rgba::new(250, 250, 252, 245) });
        for (n, item) in [&b"SEND"[..], b"RECEIVE", b"STAKE", b"SETTINGS"].iter().enumerate() {
            p.push(Prim::Glyphs { x: d(830), y: d(290 + n as i32 * 170), scale: gs(6), text: item.to_vec(), color: Rgba::opaque(20, 24, 32) });
        }
    }

    Scene { width, height, clear: Rgba::opaque(14, 17, 24), prims: p }
}
