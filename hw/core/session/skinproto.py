#!/usr/bin/env python3
"""skinproto.py - merge the RG-19A drafts in memory, check them and size them.

Session seat of hw/core. It reads proto/budlum/leaf/v1/leaf.proto, the continuity
draft and this directory's drafts, and parses the result with proto/tools/protolite.py
(read only). It edits nothing outside hw/core/session/.

Run: python3 skinproto.py     writes out/proto_sizes.md
"""
import os
import re
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "hw", "hostpower", "continuity"))
import protodraft as D  # noqa: E402  the continuity draft, read only
pl = D.pl

CHAIN = os.path.join(HERE, "proto", "skin_chain.proto")
LINK = os.path.join(HERE, "proto", "skin_link.proto")

ERRORS = [("VIEW_UNKNOWN", 1100), ("PAIRING_STALE", 1101), ("PAIRING_REVOKED", 1102),
          ("NOT_A_WRITER", 1103), ("SKIN_NOT_ALLOWED", 1104)]
BODIES = [("WriterGrant", "writer_grant", 39), ("WriterTakeOver", "writer_take_over", 40),
          ("SkinLinkLost", "skin_link_lost", 41)]
PAUSE_FIELDS = "  repeated ViewRef views = 16;\n  bytes core_id = 17;\n"
RESUME_FIELDS = ("  bytes core_id = 13;\n  repeated ViewRef views = 14;\n  bytes prev_core_id = 15;\n"
                 "  CoreDistance distance = 16;\n")


def merged_text():
    t = D.merged_text()                      # leaf.proto plus the continuity draft
    defs = re.sub(r"^syntax.*\n|^package.*\n", "", open(CHAIN, encoding="utf-8").read(), flags=re.M)
    errs = "".join(f"  ERROR_CODE_{n} = {v};\n" for n, v in ERRORS)
    t = t.replace("\n  ERROR_CODE_INPUT_EXPIRED = 1009;\n", "\n  ERROR_CODE_INPUT_EXPIRED = 1009;\n" + errs, 1)
    t = t.replace("\n  PAUSE_REASON_LAPSE = 4;\n", "\n  PAUSE_REASON_LAPSE = 4;\n  PAUSE_REASON_VIEWS_LOST = 5;\n", 1)
    assert "  Signature signature = 15;\n}" in t and "  Signature signature = 12;\n}" in t
    t = re.sub(r"(message SessionPause \{.*?  Signature signature = 15;\n)\}",
               lambda m: m.group(1) + PAUSE_FIELDS + "}", t, count=1, flags=re.S)
    t = re.sub(r"(message SessionResume \{.*?  Signature signature = 12;\n)\}",
               lambda m: m.group(1) + RESUME_FIELDS + "}", t, count=1, flags=re.S)
    t = t.replace("message LeafMessage {", defs + "\nmessage LeafMessage {")
    oneof = "".join(f"    {m} {f} = {n};\n" for m, f, n in BODIES)
    t = t.replace("\n    PowerNotice power_notice = 38;\n", "\n    PowerNotice power_notice = 38;\n" + oneof, 1)
    return t


def _parse_text(text):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "m.proto")
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return pl.parse(p)


def merged_schema():
    return _parse_text(merged_text())


def link_schema():
    return pl.parse(LINK)


def sig(kind):
    return D.sig(kind)


def chain_samples():
    view = {"skin_id": bytes(16), "view_id": 2, "mode": "VIEW_MODE_EXTEND",
            "rect": {"x": 1600, "y": 200, "w": 1600, "h": 3200}, "bind_epoch": 3, "pairing_epoch": 5}
    return {
        "writer_grant": {"session_id": 7_000_000_001, "core_id": bytes(32), "expiry_height": 2_100_000,
                         "distance": "CORE_DISTANCE_C2", "wallet_signature": sig("87")},
        "writer_take_over": {"session_id": 7_000_000_001, "from_core_id": bytes(32), "to_core_id": bytes(32),
                             "resume_seq": 4, "to_distance": "CORE_DISTANCE_C2", "signature": sig("44")},
        "skin_link_lost": {"skin_id": bytes(16), "view_id": 2, "since_frame": 86_400_000, "outage_ms": 1500},
        "session_pause": dict(D.samples()["session_pause"], views=[view, dict(view, view_id=3)],
                              core_id=bytes(32)),
        "session_resume": dict(D.samples()["session_resume"], core_id=bytes(32), prev_core_id=bytes(32),
                               views=[view, dict(view, view_id=3)], distance="CORE_DISTANCE_C1"),
    }


def pairing_sample():
    return {"skin_id": bytes(16), "core_id": bytes(32), "pairing_epoch": 5, "skin_class": "SKIN_CLASS_LEAF_160",
            "link": "SKIN_LINK_KIND_CABLE", "allowed_cores": [bytes(32), bytes(32)],
            "paired_at_height": 2_000_000, "wallet_signature": sig("87")}


def link_samples():
    return {
        "SkinAttach": {"skin_id": bytes(16), "pairing_epoch": 5, "nonce": bytes(16), "store_mj": 72_000,
                       "powered_by_link": True, "tag": bytes(16)},
        "SkinAttachAck": {"code": "ATTACH_CODE_OK", "link_key_epoch": 5, "from_frame": 86_400_001,
                          "views": [{"view_id": 2, "bind_epoch": 3, "x": 1600, "y": 200, "w": 1600, "h": 3200}],
                          "tag": bytes(16)},
        "ViewBind": {"view": {"view_id": 2, "bind_epoch": 3, "x": 1600, "y": 200, "w": 1600, "h": 3200},
                     "from_frame": 86_400_001, "tag": bytes(16)},
        "ViewUnbind": {"view_id": 2, "bind_epoch": 3, "reason": "UNBIND_REASON_SESSION_MOVED", "tag": bytes(16)},
        "SkinEvent": {"seq": 123456, "kind": "EVENT_KIND_TOUCH", "x": 812, "y": 1630, "pairing_epoch": 5,
                      "tag": bytes(16)},
    }


def sizes():
    s, ls = merged_schema(), link_schema()
    rows = []
    for body, obj in chain_samples().items():
        raw = pl.encode(s, "LeafMessage", {body: obj})
        rows.append((body, len(raw), pl.decode(s, "LeafMessage", raw, strict=True) == {body: obj}))
    raw = pl.encode(s, "PairingRecord", pairing_sample())
    rows.append(("PairingRecord (chain payload)", len(raw), pl.decode(s, "PairingRecord", raw, strict=True) == pairing_sample()))
    for name, obj in link_samples().items():
        raw = pl.encode(ls, name, obj)
        rows.append((f"{name} (Skin link)", len(raw), pl.decode(ls, name, raw, strict=True) == obj))
    return rows


def main():
    rows = sizes()
    out = ["# Sizes of the RG-19A messages (generated by skinproto.py)\n",
           "Stand-in signatures of the exact FIPS 204 size. Skin link messages carry a `16` byte tag.\n",
           "| message | bytes | round trip |", "|---|---|---|"]
    for n, b, ok in rows:
        out.append(f"| {n} | {b} | {'ok' if ok else 'FAIL'} |")
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "proto_sizes.md"), "w") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
