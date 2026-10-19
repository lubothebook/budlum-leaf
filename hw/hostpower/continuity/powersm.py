#!/usr/bin/env python3
"""powersm.py - the host-power states beside the dead-pad and safe-screen machine.

Continuity team of hw/hostpower, revision L.6.1 (proposed). The executable
model behind POWER-STATES.md. It sits beside fw/boot/bootsm.py, which is
imported read only. bootsm answers "how does a dead Leaf boot". powersm
answers "what is a Leaf doing between a host losing power and the next host".

The new states
  HOST_AUTH   a host is at the contact. Its pads stay at 0 V until U7 passes it.
  HOST        the host carries the load and tops up the store.
  BRIDGE      the host is gone. The store carries a live session. Minutes.
  ISLAND      Full tier, no host, by choice or by lack. Hours.
  PAUSING     the store is at its floor. U7 signs a SessionPause and commits it.
  SUSPENDED   the pause is on record. Only U7 and the rear display are alive.
  RESUMING    power is back. The boot path of bootsm runs, then SessionResume.
  RESUME_STATED  a floor state: the resume was refused and the Leaf says why.
DEAD is the DEAD of bootsm: no energy at all, a session paused on chain.

The three laws of this file
  P-law 1  a host pad stays at 0 V until its handshake passes (extends ENR-19)
  P-law 2  a host never holds authority; U7 is the only signer in every state
  P-law 3  a session is live in exactly one place, or paused on chain

Every number is [HYPOTHESIS] unless the comment names a source.

Run: python3 powersm.py            the state table, the energy times, a trace
     python3 powersm.py --fuzz     random event sequences against the laws
"""
import os
import random
import sys
from dataclasses import dataclass, field

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "fw", "boot"))
import bootsm  # noqa: E402  read only: the dead-pad and safe-screen model

# ------------------------------------------------------------ the loads ---
# Watts at the cells. Source: hw/energy/out/budget.txt (budget/runtime.py).
W = {
    "live": 2.242,      # delta session, 250 nits, Wi-Fi (battery side)  [TREE]
    "peak": 8.7,        # the worst peak of BRIEF Section 5               [DECISION]
    "hold": 0.40,       # radios kept, decoder idle, face dark (B cell)   [TREE]
    "safe": 0.219,      # safe screen, no link                            [TREE]
    "glance": 0.117,    # rear display glance, body dark                  [TREE]
    "standby": 0.061,   # wallet standby with Wi-Fi TWT                   [TREE]
    "suspended": 0.025, # U7 0.020 W plus hub 0.005 W, radios off         [TREE] runtime.py
    "suspended_warm": 0.055,  # the same with the modem attached in idle   [TREE] runtime.py radio 0.030 W
    "island_reduced": 1.0,   # FINAL/08 Section 8.3, 20 to 60 percent      [HYPOTHESIS]
    "island_essential": 0.385,  # static page at 10 Hz, under 20 percent   [TREE]
    "topup": 20.0,      # the host refills the store at up to 20 W         [HYPOTHESIS]
}
USABLE = 0.96           # fraction above the seat cut-off, runtime.py       [TREE]
B_CELL_WH = 0.144       # the B cell, hw/energy/05                          [TREE]
B_FLOOR_J = 0.03 * 3600  # kept for SUSPENDED and the pause: 1.2 h          [HYPOTHESIS]
E_PAUSE_J = 0.5         # sign, send and commit one SessionPause           [HYPOTHESIS]
T_PAUSING_S = 0.30      # time of PAUSING: sign 25 ms, send, NVM commit     [HYPOTHESIS]
ISLAND_FLOOR = 0.05     # the reserve tier of FINAL/08 Section 8.3
GLANCE_J = 0.04 * 5.0   # one 5 s rear glance on top of SUSPENDED            [TREE] rear 0.04 W


@dataclass(frozen=True)
class Tier:
    name: str
    cap_j: float        # capacitor store, usable
    body_wh: float      # micro cells kept for the bridge, nominal
    bcell: bool         # the 0.14 Wh B cell of the ring is present and charged

    @property
    def body_j(self):
        return self.cap_j + self.body_wh * 3600.0 * USABLE

    @property
    def b_j(self):
        return B_CELL_WH * 3600.0 * USABLE if self.bcell else 0.0

    @property
    def can_island(self):
        return self.body_wh >= 3.0


# BRIEF Section 4. Bare: seconds of capacitor. Buffer: 0.3 to 1.5 Wh. Full: 5.9 Wh.
# Bare-0 drops the B cell. That breaks rule 5 of hw/energy/05 (U7 always-on
# supply comes from the B cell), so it is a stress case and not a tier.
BARE0 = Tier("Bare-0", 5.0, 0.0, False)
BARE = Tier("Bare", 5.0, 0.0, True)
# hw/hostpower/powerpath finds that 5 J of capacitor does not fit the body margin.
# A store for the safe screen (0.66 J for 3 s) and one pause (0.5 J) is the
# smaller case. It carries a lit session for half a second only.
BARE_S = Tier("Bare-1.2J", 1.2, 0.0, True)
BUFFER = Tier("Buffer", 5.0, 0.9, True)
BUFFER_LO = Tier("Buffer-0.3", 5.0, 0.3, True)
BUFFER_HI = Tier("Buffer-1.5", 5.0, 1.5, True)
FULL = Tier("Full", 5.0, 5.9, True)
TIERS = [BARE, BUFFER, FULL]

# ----------------------------------------------------- the state table ---
LIVE_STATES = {"HOST", "BRIDGE", "ISLAND", "PAUSING"}
PAUSED_STATES = {"SUSPENDED", "DEAD", "RESUMING", "RESUME_STATED"}
ALL_STATES = ["DEAD", "HOST_AUTH", "HOST", "BRIDGE", "ISLAND", "PAUSING",
              "SUSPENDED", "RESUMING", "RESUME_STATED"]

STATE_INFO = {
    "DEAD": dict(
        entry="no energy in the store and no host; the pause is on chain",
        alive="nothing in the Leaf; the chain holds the session",
        face="dark", rear="dark",
        source="none", w=0.0),
    "HOST_AUTH": dict(
        entry="a host is at the contact: a seat event, a Qi field or a PD sink",
        alive="U4 ROM, U7 and the rear display on the B cell; the host pads at 0 V",
        face="what the previous state showed, unchanged",
        rear="host glyph and the word CHECKING",
        source="B cell, else the host AON feed", w=0.025),
    "HOST": dict(
        entry="the host passed the U7 handshake of the trust team",
        alive="everything; the host carries the load and refills the store",
        face="the session, full class",
        rear="host glyph and the store level",
        source="host", w=0.0),
    "BRIDGE": dict(
        entry="the host left, and the store holds the floor for a pause",
        alive="the session, the link radios, U7; the face while the body store lasts",
        face="the session, then a dark face with the frame store kept",
        rear="a bridge glyph and the minutes left",
        source="body store, then the B cell at 0.40 W", w=W["live"]),
    "ISLAND": dict(
        entry="Full tier, no host, over the bridge horizon or by user choice",
        alive="the session under the energy policy of FINAL/08 Section 8.3",
        face="the session, tier stated on the class line",
        rear="an island glyph and the hours left",
        source="all cells", w=W["live"]),
    "PAUSING": dict(
        entry="the store reached its floor with a live session",
        alive="U7 signs the SessionPause; one radio sends it; U7 commits it",
        face="a last frame with the line SESSION PAUSED",
        rear="a pause glyph",
        source="B cell, else the pause reserve of the body store", w=1.0),
    "SUSPENDED": dict(
        entry="the SessionPause is committed",
        alive="U4 ROM, U7, the rear display on touch; radios and body off",
        face="dark",
        rear="on a touch: PAUSED, the host that is needed and the days left",
        source="B cell at 0.025 W", w=W["suspended"]),
    "RESUMING": dict(
        entry="a host passed the handshake, or a wake with energy",
        alive="the boot path of bootsm, then SessionResume with the validator",
        face="the safe screen at 23 ms, then the session",
        rear="the word RESUMING",
        source="host", w=W["safe"]),
    "RESUME_STATED": dict(
        entry="the resume was refused: grant, anchor or state root",
        alive="the safe screen, the wallet, the update class; no session",
        face="the safe screen and one stated line",
        rear="the reason code",
        source="host or the B cell", w=W["safe"]),
}

# (state, event) -> note. The guards live in PowerSM.on().
TRANSITIONS = [
    ("DEAD", "HOST_SEEN", "HOST_AUTH", "a seat event, a Qi field or a PD sink"),
    ("SUSPENDED", "HOST_SEEN", "HOST_AUTH", "the same, the pause stays on record"),
    ("BRIDGE", "HOST_SEEN", "HOST_AUTH", "make before break: the store keeps the session"),
    ("ISLAND", "HOST_SEEN", "HOST_AUTH", "a host found on an island"),
    ("RESUME_STATED", "HOST_SEEN", "HOST_AUTH", "a host while a refusal is shown"),
    ("HOST_AUTH", "HANDSHAKE_PASS", "HOST or RESUMING",
     "HOST if the session is live, RESUMING if it is paused"),
    ("HOST_AUTH", "HANDSHAKE_FAIL", "the previous state", "the pads stay at 0 V; a stated line"),
    ("HOST_AUTH", "HOST_LOST", "the previous state", "the host left before the pass"),
    ("HOST", "HOST_LOST", "BRIDGE or PAUSING", "BRIDGE if the store holds the floor"),
    ("BRIDGE", "STORE_LOW", "PAUSING", "the body store and B cell reached the floor"),
    ("BRIDGE", "USER_ISLAND", "ISLAND", "Full tier only"),
    ("BRIDGE", "HORIZON", "ISLAND", "Full tier, after the bridge horizon"),
    ("ISLAND", "SOC_RESERVE", "PAUSING", "the 5 percent reserve tier of FINAL/08"),
    ("PAUSING", "PAUSE_COMMITTED", "SUSPENDED", "the validator acknowledged the pause"),
    ("PAUSING", "PAUSE_UNSENT", "SUSPENDED", "no link: the validator pauses by lapse"),
    ("SUSPENDED", "B_EMPTY", "DEAD", "the B cell is empty"),
    ("SUSPENDED", "TOUCH", "SUSPENDED", "a rear glance; it costs 0.2 J"),
    ("HOST_AUTH", "HANDSHAKE_PASS", "RESUMING", "a paused session at a passed host"),
    ("RESUMING", "RESUME_OK", "HOST", "ResumeAck with the same state root"),
    ("RESUMING", "RESUME_REFUSED", "RESUME_STATED", "grant, anchor or state root"),
    ("RESUMING", "HOST_LOST", "SUSPENDED", "the resume was not acknowledged: the pause stands"),
    ("RESUME_STATED", "USER_REGRANT", "RESUMING", "one user action with the wallet"),
    ("RESUME_STATED", "HOST_LOST", "SUSPENDED", "no host, no resume"),
]


class IllegalEvent(Exception):
    pass


@dataclass
class PowerSM:
    tier: Tier
    state: str = "DEAD"
    session: str = "NONE"          # NONE, LIVE, PAUSED, PAUSED_LAPSE
    e_body: float = 0.0            # joules in the body store (caps and cells)
    e_b: float = 0.0               # joules in the B cell
    host_present: bool = False
    host_pass: bool = False        # handshake passed for the present host
    host_pad_live: bool = False    # the host pads carry current
    came_from: str = "DEAD"
    link_up: bool = True           # a radio reaches a validator
    horizon_s: float = 600.0       # BRIDGE becomes ISLAND on Full tier
    t_in_state: float = 0.0
    t_off_host: float = 0.0        # seconds of a live session with no host
    t: float = 0.0
    authority_holder: str = "U7"   # P-law 2. Never a host.
    refused_hosts: int = 0
    log: list = field(default_factory=list)
    reason: str = ""
    marks: dict = field(default_factory=dict)   # first entry time of each state

    # ------------------------------------------------------------ setup ---
    @classmethod
    def hosted(cls, tier, link_up=True):
        """A Leaf on a host with a live session and a full store."""
        sm = cls(tier=tier, state="HOST", session="LIVE", e_body=tier.body_j,
                 e_b=tier.b_j, host_present=True, host_pass=True,
                 host_pad_live=True, link_up=link_up)
        sm._log("start HOST")
        return sm

    # ---------------------------------------------------------- queries ---
    def soc(self):
        full = self.tier.body_j + self.tier.b_j
        return (self.e_body + self.e_b) / full if full else 0.0

    def surface(self):
        info = STATE_INFO[self.state]
        return info["face"], info["rear"]

    def _eff(self):
        """The state whose load applies. HOST_AUTH keeps the old load."""
        if self.state == "HOST_AUTH" and self.came_from in ("BRIDGE", "ISLAND"):
            return self.came_from
        return self.state

    def _body_floor(self):
        """The body store keeps the pause energy when no B cell exists."""
        return 0.0 if self.tier.bcell else E_PAUSE_J

    def _band(self):
        """The ISLAND energy band: 0 normal, 1 reduced, 2 essential, 3 floor."""
        full = self.tier.body_j + self.tier.b_j
        e = self.e_body + self.e_b
        for i, frac in enumerate((0.6, 0.2, ISLAND_FLOOR)):
            if e > frac * full + 1e-9:
                return i
        return 3

    def drain(self):
        """The power and the source in the current state: (watts, source)."""
        s = self._eff()
        if s == "HOST":
            return 0.0, "host"
        if s == "BRIDGE":
            if self.e_body > self._body_floor() + 1e-9:
                return W["live"], "body"
            return W["hold"], "bcell"
        if s == "ISLAND":
            band = self._band()
            w = (W["live"], W["island_reduced"], W["island_essential"],
                 W["island_essential"])[band]
            return w, "all"
        if s == "SUSPENDED":
            return W["suspended"], "bcell"
        if s == "HOST_AUTH":
            return 0.025, "bcell" if self.tier.bcell else "host"
        if s in ("RESUMING", "RESUME_STATED"):
            return W["safe"], "host" if self.host_pad_live else "bcell"
        return 0.0, "none"

    def time_to_threshold(self):
        """(seconds, kind) until the next automatic event, or (None, None)."""
        w, src = self.drain()
        s = self._eff()
        if s == "HOST" or w <= 0 or src == "host":
            return None, None
        if s == "BRIDGE":
            horizon = None
            if self.tier.can_island and self.session == "LIVE":
                horizon = max(0.0, self.horizon_s - self.t_off_host)
            if src == "body":
                t = (self.e_body - self._body_floor()) / w
                if horizon is not None and horizon < t:
                    return horizon, "horizon"
                return max(t, 0.0), "live_end"
            t = max(0.0, (self.e_b - B_FLOOR_J) / w)
            if horizon is not None and horizon < t:
                return horizon, "horizon"
            return t, "store_floor"
        if s == "ISLAND":
            full = self.tier.body_j + self.tier.b_j
            e = self.e_body + self.e_b
            band = self._band()
            if band == 3:
                return 0.0, "island_floor"
            frac = (0.6, 0.2, ISLAND_FLOOR)[band]
            kind = "island_floor" if band == 2 else "tier"
            return (e - frac * full) / w, kind
        if s == "SUSPENDED":
            return self.e_b / w, "b_empty"
        return None, None

    # ---------------------------------------------------------- the clock ---
    def advance(self, dt):
        """Run the clock `dt` seconds. Automatic events fire at their time."""
        if dt < 0:
            raise ValueError("dt")
        guard = 0
        while dt > 1e-12:
            guard += 1
            if guard > 10000:
                raise RuntimeError("advance did not settle")
            if self.state == "PAUSING":
                step = min(dt, T_PAUSING_S - self.t_in_state)
                self._tick(step, 0.0, "none")
                dt -= step
                if self.t_in_state >= T_PAUSING_S - 1e-12:
                    self._finish_pause()
                continue
            if self.state == "HOST":
                self._topup(dt)
                self._tick(dt, 0.0, "host")
                return
            w, src = self.drain()
            ttt, kind = self.time_to_threshold()
            step = dt if ttt is None else min(dt, ttt)
            self._tick(step, w, src)
            dt -= step
            if ttt is not None and step >= ttt - 1e-12:
                self._threshold(kind)

    def _tick(self, dt, w, src):
        e = w * dt
        if src == "body":
            self.e_body = max(0.0, self.e_body - e)
        elif src == "bcell":
            self.e_b = max(0.0, self.e_b - e)
        elif src == "all":
            take = min(self.e_body, e)
            self.e_body -= take
            self.e_b = max(0.0, self.e_b - (e - take))
        self.t += dt
        self.t_in_state += dt
        if self.session == "LIVE" and self.state != "HOST":
            self.t_off_host += dt

    def _topup(self, dt):
        room = self.tier.body_j - self.e_body
        self.e_body += min(room, W["topup"] * dt)
        room_b = self.tier.b_j - self.e_b
        self.e_b += min(room_b, 0.037 * 3.87 * dt)   # U4 charges the B cell at 37 mA

    def _threshold(self, kind):
        s = self._eff()
        if kind == "horizon":
            if self.state == "BRIDGE":
                self._go("ISLAND", "bridge horizon")
            else:
                self.came_from = "ISLAND"       # HOST_AUTH keeps waiting
            return
        if kind == "live_end":
            if not self.tier.bcell:
                self._go("PAUSING", "the body store reached the pause reserve")
            self.marks.setdefault("hold_start", self.t)
            return                              # B cell: live ends, hold goes on
        if kind in ("store_floor", "island_floor"):
            self._go("PAUSING", "the store reached its floor")
            return
        if kind == "b_empty":
            self._go("DEAD", "the B cell is empty")
        # "tier": the power changed, the state did not
        _ = s

    def _finish_pause(self):
        if self.tier.bcell:
            self.e_b = max(0.0, self.e_b - E_PAUSE_J)
        else:
            self.e_body = max(0.0, self.e_body - E_PAUSE_J)
        if self.link_up:
            self.session, self.reason = "PAUSED", "clean pause"
        else:
            self.session = "PAUSED_LAPSE"
            self.reason = "no link: the validator pauses by lapse"
        self.t_off_host = 0.0
        if self.host_present and not self.host_pass:
            self.came_from = "SUSPENDED" if self.e_b > 1e-9 else "DEAD"
            self._go("HOST_AUTH", self.reason + "; handshake goes on")
        else:
            self._go("SUSPENDED" if self.e_b > 1e-9 else "DEAD", self.reason)

    # --------------------------------------------------------- the events ---
    def on(self, event, **kw):
        """Apply one event. Returns True if it changed the state or the data."""
        s = self.state
        if event == "HOST_SEEN":
            if s in ("DEAD", "SUSPENDED", "BRIDGE", "ISLAND", "RESUME_STATED"):
                self.came_from = s
                self.host_present, self.host_pass, self.host_pad_live = True, False, False
                self._go("HOST_AUTH", "host at the contact")
                return True
            return False
        if event == "HANDSHAKE_PASS" and s == "HOST_AUTH":
            self.host_pass = True
            self.host_pad_live = True
            if self.session == "LIVE":
                self._go("HOST", "host passed, the session never stopped")
                self.t_off_host = 0.0
            else:
                self._go("RESUMING", "host passed, resume from the chain record")
            return True
        if event == "HANDSHAKE_FAIL" and s == "HOST_AUTH":
            self.refused_hosts += 1
            self.host_present, self.host_pass, self.host_pad_live = False, False, False
            self._go(self.came_from, "host refused: pads stay at 0 V")
            return True
        if event == "HOST_LOST":
            return self._host_lost()
        if event == "STORE_LOW" and s == "BRIDGE":
            self._go("PAUSING", "forced")
            return True
        if event == "USER_ISLAND" and s == "BRIDGE" and self.tier.can_island:
            self._go("ISLAND", "user choice")
            return True
        if event == "TOUCH" and s == "SUSPENDED":
            self.e_b = max(0.0, self.e_b - GLANCE_J)
            self.log.append((round(self.t, 3), s, "rear glance"))
            if self.e_b <= 1e-9:
                self._go("DEAD", "the glance emptied the B cell")
            return True
        if event == "RESUME_OK" and s == "RESUMING":
            self.session = "LIVE"
            self.t_off_host = 0.0
            if self.host_present:
                self._go("HOST", "ResumeAck, same state root")
            else:
                self._go("BRIDGE", "resumed on the store")
            return True
        if event == "RESUME_REFUSED" and s == "RESUMING":
            self.reason = kw.get("reason", "refused")
            self._go("RESUME_STATED", self.reason)
            return True
        if event == "USER_REGRANT" and s == "RESUME_STATED" and self.host_present:
            self._go("RESUMING", "new grant signed by the wallet")
            return True
        return False

    def _host_lost(self):
        s = self.state
        was_present = self.host_present
        self.host_present = False
        self.host_pad_live = False
        self.host_pass = False
        if not was_present:
            return False
        if s == "HOST":
            floor_ok = (self.e_body > self._body_floor() + 1e-9) or \
                       (self.tier.bcell and self.e_b > B_FLOOR_J + 1e-9)
            self._go("BRIDGE" if floor_ok else "PAUSING", "host lost")
            return True
        if s == "HOST_AUTH":
            self._go(self.came_from, "host left before the pass")
            return True
        if s in ("RESUMING", "RESUME_STATED"):
            self._go("SUSPENDED" if self.e_b > 1e-9 else "DEAD",
                     "no host: the pause stands")
            return True
        return False

    # ---------------------------------------------------------- internals ---
    def _go(self, dst, why):
        if dst not in ALL_STATES:
            raise IllegalEvent(dst)
        self.log.append((round(self.t, 3), f"{self.state}->{dst}", why))
        self.marks.setdefault("enter_" + dst, self.t)
        if dst == "PAUSING":
            self.marks.setdefault("e_b_pause", self.e_b)
        self.state = dst
        self.t_in_state = 0.0

    def _log(self, msg):
        self.log.append((round(self.t, 3), self.state, msg))


# ------------------------------------------------------------ the laws ---
def check_laws(sm):
    """Return the list of broken laws. An empty list means all hold."""
    bad = []
    if sm.host_pad_live and not sm.host_pass:
        bad.append("P1 host pad live before the handshake")
    if sm.host_pad_live and not sm.host_present:
        bad.append("P1 host pad live with no host")
    if sm.authority_holder != "U7":
        bad.append("P2 authority held by a host")
    live = sm.state in LIVE_STATES
    if sm.state == "HOST_AUTH":
        live = sm.came_from in LIVE_STATES
    if live and sm.session != "LIVE":
        bad.append(f"P3 live state {sm.state} with session {sm.session}")
    if not live and sm.session == "LIVE":
        bad.append(f"P3 session LIVE in {sm.state}")
    if sm.e_body < -1e-9 or sm.e_b < -1e-9:
        bad.append("E1 negative energy")
    if sm.state != "DEAD":
        face, rear = sm.surface()
        if face == "dark" and rear == "dark":
            bad.append("S1 no visible surface")
    if sm.state in ("BRIDGE", "ISLAND") and sm.e_body + sm.e_b <= 1e-9:
        bad.append("E2 live session with an empty store")
    return bad


# -------------------------------------------------- the times, via bootsm ---
def boot_times(link):
    """Milliseconds from the wake event, from bootsm, read only.

    link: 'wifi' (cached association), 'cell_warm' (modem attached in standby),
    'cell_cold' (modem power-cycled), 'both' (the nominal boot).
    The faults are only a way to select the path in bootsm. [HYPOTHESIS]
    """
    faults = {
        "both": [],
        "wifi": ["U5_A", "U5_B"],
        "cell_warm": ["U2A_A", "U2A_B"],
        "cell_cold": ["U2A_A", "U2A_B", "U5_COLD"],
    }[link]
    r = bootsm.boot(faults)
    rear = bootsm.boot(["PAD_B"])
    return dict(t_rear=rear.t_safe, t_safe=r.t_safe, t_link=r.t_link,
                t_session=r.t_session)


_PROFILE = {}


def bridge_profile(tier):
    """Run the machine from a full store and a lost host. Seconds of each phase.

    live_s     the face stays lit (BRIDGE live, or ISLAND under the policy)
    hold_s     the B cell holds the radios, the face is dark
    bridge_s   from the host loss to the start of PAUSING
    suspended_s  how long the B cell then keeps U7 and the rear display
    """
    key = (tier.name, tier.cap_j, tier.body_wh, tier.bcell)
    if key in _PROFILE:
        return _PROFILE[key]
    sm = PowerSM.hosted(tier)
    sm.on("HOST_LOST")
    t0 = sm.t
    sm.advance(1.0e7)
    t_pause = sm.marks.get("enter_PAUSING", sm.t) - t0
    t_hold = sm.marks.get("hold_start", sm.marks.get("enter_PAUSING", sm.t)) - t0
    e_b = sm.marks.get("e_b_pause", sm.e_b)
    prof = dict(live_s=t_hold, hold_s=t_pause - t_hold, bridge_s=t_pause,
                island_s=(sm.marks["enter_ISLAND"] - t0) if "enter_ISLAND" in sm.marks else None,
                e_b_at_pause_j=e_b,
                suspended_s=e_b / W["suspended"] if tier.bcell else 0.0)
    _PROFILE[key] = prof
    return prof


def tier_times(tier):
    """The time in seconds that a tier lives in each phase, from a full store."""
    x = dict(bridge_profile(tier))
    x["peak_s"] = tier.body_j / W["peak"]
    x["live_peak_free_s"] = tier.body_j / W["live"]
    x["suspended_min_s"] = (B_FLOOR_J - E_PAUSE_J) / W["suspended"] if tier.bcell else 0.0
    x["suspended_max_s"] = x["suspended_s"]
    return x


# ------------------------------------------------------------ the fuzz ---
EVENTS = ["HOST_SEEN", "HANDSHAKE_PASS", "HANDSHAKE_FAIL", "HOST_LOST",
          "STORE_LOW", "USER_ISLAND", "TOUCH", "RESUME_OK", "RESUME_REFUSED",
          "USER_REGRANT"]


def fuzz(n_seq=2000, n_ev=40, seed=1):
    """Random event sequences against the laws. Returns (steps, violations)."""
    rnd = random.Random(seed)
    steps, viol = 0, []
    for k in range(n_seq):
        tier = rnd.choice([BARE0, BARE, BUFFER, FULL])
        sm = PowerSM.hosted(tier, link_up=rnd.random() < 0.8)
        for _ in range(n_ev):
            if rnd.random() < 0.55:
                sm.advance(rnd.choice([0.01, 0.5, 3.0, 40.0, 600.0, 3600.0, 20000.0]))
            else:
                sm.on(rnd.choice(EVENTS), reason="grant")
            steps += 1
            bad = check_laws(sm)
            if bad:
                viol.append((k, tier.name, sm.state, bad, list(sm.log[-4:])))
                break
    return steps, viol


# ------------------------------------------------------------- the CLI ---
def print_tables():
    print("the new states beside DEAD..SESSION of bootsm")
    for s in ALL_STATES:
        i = STATE_INFO[s]
        print(f"  {s:14s} {i['entry']}")
    print()
    print("the time a tier lives in each phase, from a full store, seconds")
    for t in (BARE0, BARE, BUFFER_LO, BUFFER, BUFFER_HI, FULL):
        x = tier_times(t)
        print(f"  {t.name:11s} live {x['live_s']:9.1f}  hold {x['hold_s']:7.1f}  "
              f"bridge {x['bridge_s']:9.1f}  suspended {x['suspended_s']/3600:5.2f} h  "
              f"at {W['peak']} W: {x['peak_s']:8.2f} s")
    print()
    for link in ("both", "wifi", "cell_warm", "cell_cold"):
        b = boot_times(link)
        print(f"  bootsm {link:10s} rear {b['t_rear']:.1f} ms  safe {b['t_safe']:.1f} ms  "
              f"link {b['t_link']:.1f} ms  session {b['t_session']:.1f} ms")


def demo():
    print("\ntrace: Buffer tier, host lost, a 20 min walk, a new host")
    sm = PowerSM.hosted(BUFFER)
    sm.on("HOST_LOST")
    sm.advance(1200)
    sm.on("HOST_SEEN")
    sm.on("HANDSHAKE_PASS")
    for row in sm.log:
        print("  ", row)
    print(f"  final {sm.state}, session {sm.session}, "
          f"body {sm.e_body:.1f} J, B cell {sm.e_b:.1f} J")


def main(argv):
    print_tables()
    demo()
    if "--fuzz" in argv:
        n, v = fuzz()
        print(f"\nfuzz: {n} steps, {len(v)} violations")
        for x in v[:5]:
            print("  ", x)
        return 1 if v else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
