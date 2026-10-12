"""Generate the U6 test vectors and check the whole scheme end to end.

Writes vectors/<name>.json (protocol view) and vectors/rtl_events.json
(the word-level stream that sim/test_slice_auth.py replays into the RTL).
Run: python3 ref/gen_vectors.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from keccak import _selftest
from leafauth import *  # noqa: F401,F403

OUT = os.path.join(os.path.dirname(__file__), "..", "vectors")
rng = random.Random(0xB0D1)
hx = lambda b: b.hex()
events = []          # the RTL stream, in order
u6 = U6Checker()     # the golden checker, fed the same stream


def ev_load(slot, sid, prefix):
    u6.load(slot, sid, prefix)
    events.append(dict(op="load", slot=slot, sid=hx(sid), prefix=[f"{v:016x}" for v in prefix]))


def ev_clear(slot):
    u6.clear(slot)
    events.append(dict(op="clear", slot=slot))


def ev_slice(name, wire, expect_err):
    words = wire_words(wire) if isinstance(wire, (bytes, bytearray)) else wire
    r = u6.check(words)
    assert r["err"] == expect_err, (name, ERR_NAME[r["err"]], ERR_NAME[expect_err])
    e = dict(op="slice", name=name, words=[f"{w:016x}" for w in words], err=r["err"],
             err_name=ERR_NAME[r["err"]])
    if "digest" in r:
        e.update(digest=hx(r["digest"]), seq=r["seq"])
    events.append(e)
    return r


def payload(n):
    return bytes(rng.getrandbits(8) for _ in range(n))


def main():
    assert _selftest()
    os.makedirs(OUT, exist_ok=True)
    vectors = {}

    # ---- the chain view: three validators, one program ---------------------
    good, shadow, inactive, slashed, outsider = (Validator(s) for s in
                                                 (b"val-A", b"val-B", b"val-C", b"val-D", b"val-E"))
    vset = ValidatorSet(epoch=4242)
    vset.add(good.ed_pub, good.pq_pub)
    vset.add(shadow.ed_pub, shadow.pq_pub)
    vset.add(inactive.ed_pub, inactive.pq_pub, active=False)
    vset.add(slashed.ed_pub, slashed.pq_pub, slashed=True)
    app = H(b"program:leaf.home")
    u7 = U7(b"leaf-0001", vset, programs={app})

    # ---- 1. the valid stream --------------------------------------------------
    sh = good.server_hello(u7.client_hello(app, 0, bytes(32)), H(b"n-V-A"))
    ok, why, prefix = u7.accept(sh)
    assert ok, why
    assert good.sid == u7.sid
    ev_load(0, u7.sid, prefix)
    sizes = [[1, 7, 8, 2605], [120, 3000, 0, 9], [137, 64, 513, 1024]]
    seq, wires, frame_hashes, shown = 1, [], [], []
    for fno, row in enumerate(sizes):
        digests = []
        for si, n in enumerate(row):
            fl = F_LAST if si == len(row) - 1 else 0
            w, d = good.slice(fl, si, seq, fno, payload(n), 0, y0=si * 100)
            r = ev_slice(f"valid f{fno} s{si}", w, OK)
            assert r["digest"] == d
            wires.append(w); digests.append(d); seq += 1
        frame_hashes.append(frame_hash(u7.sid, fno, digests))
    shown = list(frame_hashes)          # U7 builds these from the U6 digests
    msg, s_ed, s_pq = good.sign_root(0, 0, frame_hashes)
    (rcpt, rsig), why = u7.countersign(0, 0, 0, shown, msg, s_ed, s_pq, rtt_us=1180)
    assert why == "ok"
    mldsa.MLDSA87PublicKey.from_public_bytes(u7.wallet_pub).verify(rsig, rcpt)
    vectors["valid_stream"] = dict(
        sid=hx(u7.sid), validator_ed25519=hx(good.ed_pub), mac_prefix_state=[f"{v:016x}" for v in prefix],
        slices=[hx(w) for w in wires], frame_hashes=[hx(f) for f in frame_hashes],
        merkle_root=hx(merkle_root(frame_hashes)), root_msg=hx(msg), root_sig_ed25519=hx(s_ed),
        receipt=hx(rcpt), receipt_sig_mldsa87_len=len(rsig), expect="all OK, receipt countersigned")

    # ---- 2. forged slices -----------------------------------------------------
    w = bytearray(good.slice(0, 0, seq, 3, payload(500), 0)[0])
    forged = {}
    for name, pos in (("payload byte flipped", 32 + 100), ("tag bit flipped", len(w) - 1),
                      ("header seq changed", 8), ("header y0 changed", 28)):
        f = bytearray(w); f[pos] ^= 0x01
        ev_slice(f"forged: {name}", bytes(f), BAD_TAG)
        forged[name] = hx(bytes(f))
    other = Validator(b"val-A")                  # same validator, another session key
    other.sid, other.key = u7.sid, H(b"another session key")
    f = other.slice(0, 0, seq, 3, payload(40), 0)[0]
    ev_slice("forged: tag under another session key", f, BAD_TAG)
    forged["another session key"] = hx(f)
    ev_slice("valid after forgeries", w, OK)
    seq += 1
    vectors["forged_slice"] = dict(original=hx(bytes(w)), forged=forged, expect="BAD_TAG on each, the valid one passes")

    # ---- 3. replay --------------------------------------------------------------
    ev_slice("replay: frame 0 slice 1 again", wires[1], REPLAY)
    ev_slice("replay: the last valid slice again", bytes(w), REPLAY)
    vectors["replay"] = dict(replayed=[hx(wires[1]), hx(bytes(w))], expect="REPLAY")

    # ---- 4. handover to the shadow: zero frames lost -----------------------------
    sh2 = shadow.server_hello(u7.client_hello(app, 1, H(b"n-L-2")), H(b"n-V-B"))
    ok, why, prefix2 = u7.accept(sh2)
    assert ok and shadow.sid == u7.sid, why
    ev_load(1, u7.sid, prefix2)
    p = payload(777)
    wa, da = good.slice(0, 0, seq, 4, p, 0)
    wb, db = shadow.slice(0, 0, seq, 4, p, 1)
    assert da == db, "deterministic render: same digest from both validators"
    ev_slice("handover: shadow slice on slot 1", wb, OK)
    ev_slice("handover: primary's copy of the same slice", wa, REPLAY)
    seq += 1
    ev_clear(0)
    vectors["handover"] = dict(primary=hx(wa), shadow=hx(wb), digest=hx(da),
                               expect="shadow OK; the primary copy is a REPLAY; slot 0 cleared")

    # ---- 5. wrong validator -------------------------------------------------------
    wrong = {}
    for name, v in (("inactive", inactive), ("slashed", slashed), ("not in the set", outsider)):
        u7b = U7(b"leaf-0002", vset, programs={app})
        ok, why, _ = u7b.accept(v.server_hello(u7b.client_hello(app, 0, bytes(32)), H(b"n")))
        assert not ok and why == "key is not an active validator", (name, why)
        wrong[name] = why
    u7b = U7(b"leaf-0003", vset, programs={app})
    ok, why, _ = u7b.accept(good.server_hello(u7b.client_hello(H(b"not a program"), 0, bytes(32)), H(b"n")))
    assert not ok and why == "app is not an on-chain program entry"
    wrong["app not on chain"] = why
    # a forged ServerHello: the outsider claims the good validator's identity
    u7b = U7(b"leaf-0004", vset, programs={app})
    sh_f = outsider.server_hello(u7b.client_hello(app, 0, bytes(32)), H(b"n"))
    sh_f["ed_pub"], sh_f["pq_pub"] = good.ed_pub, good.pq_pub
    ok, why, _ = u7b.accept(sh_f)
    assert not ok and why == "handshake signature invalid"
    wrong["identity theft in the handshake"] = why
    # U6 view: the refused validator streams into slot 0, which holds no key now
    outsider.sid = u7.sid
    f = outsider.slice(0, 0, seq, 5, payload(300), 0)[0]
    ev_slice("wrong validator: slot 0 has no key", f, NO_KEY)
    # U7 view: a root signed by another validator is refused
    msg_o, so_ed, so_pq = outsider.sign_root(0, 0, frame_hashes)
    rc, why = u7.countersign(0, 0, 0, shown, msg, so_ed, so_pq, rtt_us=1180)
    assert rc is None and why == "root signature is not from the session validator"
    wrong["root signed by another key"] = why
    rc, why = u7.countersign(0, 0, 0, shown[:2], msg, s_ed, s_pq, rtt_us=1180)
    assert rc is None and why == "root does not match the shown frames"
    wrong["root over frames not shown"] = why
    vectors["wrong_validator"] = dict(refusals=wrong, slice_into_empty_slot=hx(f), expect="refused; U6 NO_KEY; safe screen")

    # ---- 6. framing errors --------------------------------------------------------
    w = shadow.slice(0, 0, seq, 5, payload(200), 1)[0]
    ev_slice("length: one word short", wire_words(w)[:-1], LENGTH)
    ev_slice("length: one word long", wire_words(w) + [0], LENGTH)
    big = pack_header(1, 0, seq, 5, MAX_PAYLOAD + 8, 0, 0)
    ev_slice("length: payload over 64 KiB", wire_words(big + bytes(16)), LENGTH)
    bad_v = bytearray(w); bad_v[0] = 2
    ev_slice("version 2", bytes(bad_v), BAD_VERSION)
    ev_slice("valid after framing errors", w, OK)
    seq += 1

    for k, v in vectors.items():
        with open(os.path.join(OUT, k + ".json"), "w") as fh:
            json.dump(v, fh, indent=1)
    with open(os.path.join(OUT, "rtl_events.json"), "w") as fh:
        json.dump(events, fh, indent=0)
    n = sum(e["op"] == "slice" for e in events)
    tally = {}
    for e in events:
        if e["op"] == "slice":
            tally[e["err_name"]] = tally.get(e["err_name"], 0) + 1
    print(f"vectors: {len(vectors)} protocol files, {n} RTL slices {tally}")
    print("all protocol assertions pass")


if __name__ == "__main__":
    main()
