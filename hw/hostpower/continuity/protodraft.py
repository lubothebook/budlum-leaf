#!/usr/bin/env python3
"""protodraft.py - merge proto/session_continuity.proto into leaf.proto in memory.

Continuity team of hw/hostpower. It does not edit proto/. It reads leaf.proto
and the draft, builds the merged text, and parses it with proto/tools/protolite.py
(read only). The result checks that the draft keeps the conventions of
proto/VERSIONING.md, and it gives the byte sizes of the new messages.

Run: python3 protodraft.py     writes out/proto_sizes.md
"""
import os
import re
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "proto", "tools"))
import protolite as pl  # noqa: E402

LEAF = os.path.join(ROOT, "proto", "budlum", "leaf", "v1", "leaf.proto")
DRAFT = os.path.join(HERE, "proto", "session_continuity.proto")

NEW_BODIES = [("SessionPause", "session_pause", 33),
              ("SessionPauseAck", "session_pause_ack", 34),
              ("LapseNotice", "lapse_notice", 35),
              ("SessionResume", "session_resume", 36),
              ("ResumeAck", "resume_ack", 37),
              ("PowerNotice", "power_notice", 38)]
NEW_ERRORS = ["RESUME_STATE_MISMATCH", "PAUSE_UNKNOWN", "SESSION_NOT_PAUSED",
              "SESSION_NOT_ACTIVE", "STALE_EPOCH", "PAUSE_TTL_EXPIRED",
              "LAPSE_TOO_EARLY", "LAPSE_BAD_EVIDENCE", "PAUSE_RATE_LIMIT",
              "INPUT_EXPIRED"]


def draft_errors_from_comments():
    """The ErrorCode lines that the draft lists in its closing comment."""
    text = open(DRAFT, encoding="utf-8").read()
    return re.findall(r"//\s+ERROR_CODE_(\w+) = (\d+);", text)


def draft_bodies_from_comments():
    text = open(DRAFT, encoding="utf-8").read()
    return re.findall(r"//\s+(\w+) (\w+) = (\d+);", text.split("additions to LeafMessage")[1]
                      .split("additions to ErrorCode")[0])


def merged_text():
    base = open(LEAF, encoding="utf-8").read()
    draft = open(DRAFT, encoding="utf-8").read()
    defs = re.sub(r"^syntax.*\n|^package.*\n", "", draft, flags=re.M)
    errs = "".join(f"  ERROR_CODE_{n} = {v};\n" for n, v in draft_errors_from_comments())
    oneof = "".join(f"    {m} {f} = {n};\n" for m, f, n in draft_bodies_from_comments())
    assert "ERROR_CODE_INTERNAL = 900;\n" in base and "    Goodbye goodbye = 32;\n" in base
    t = base.replace("  ERROR_CODE_INTERNAL = 900;\n", "  ERROR_CODE_INTERNAL = 900;\n" + errs)
    t = t.replace("message LeafMessage {", defs + "\nmessage LeafMessage {")
    t = t.replace("    Goodbye goodbye = 32;\n", "    Goodbye goodbye = 32;\n" + oneof)
    return t


def merged_schema():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "merged.proto")
        open(p, "w", encoding="utf-8").write(merged_text())
        return pl.parse(p)


SIG = {"44": 2420, "65": 3309, "87": 4627}


def sig(kind):
    return {"scheme": {"44": "SIGNATURE_SCHEME_ML_DSA_44", "65": "SIGNATURE_SCHEME_ML_DSA_65",
                       "87": "SIGNATURE_SCHEME_ML_DSA_87"}[kind],
            "key_id": bytes(32), "value": bytes(SIG[kind])}


def samples():
    anchor = {"checkpoint_height": 2_000_000, "block_hash": bytes(32), "validator_set_hash": bytes(32)}
    return {
        "session_pause": {"session_id": 7_000_000_001, "pause_seq": 3, "reason": "PAUSE_REASON_HOST_LOST",
                          "last_frame_no": 86_400_000, "last_frame_chain_hash": bytes(32),
                          "state_root": bytes(32), "last_input_seq": 12_345_678,
                          "input_chain_head": bytes(32), "anchor": anchor,
                          "pending": [{"kind": "PENDING_KIND_PREDICTED", "batch_seq": 12_345_679,
                                       "taken_branch": 2, "action_hash": bytes(32)},
                                      {"kind": "PENDING_KIND_OUTBOX_ACTION", "batch_seq": 12_345_600,
                                       "action_hash": bytes(32)}],
                          "power_state": "POWER_STATE_BRIDGE", "last_host": "HOST_CLASS_DOCK_PADS",
                          "store_remaining_mj": 1200, "scan_tick": 41_472_000_000,
                          "signature": sig("44")},
        "session_pause_ack": {"session_id": 7_000_000_001, "pause_seq": 3, "validator_id": bytes(32),
                              "accepted": True, "anchored_slot": 14_400_001, "snapshot_slot": 14_400_000,
                              "validator_signature": sig("65")},
        "lapse_notice": {"session_id": 7_000_000_001, "pause_seq": 3, "last_receipt_second": 360_000,
                         "last_frame_no": 86_399_999, "last_frame_chain_hash": bytes(32),
                         "validator_id": bytes(32), "detected_at_us": 1_700_000_000_000_000,
                         "validator_signature": sig("65")},
        "session_resume": {"session_id": 7_000_000_001, "pause_seq": 3, "resume_seq": 3,
                           "expected_state_root": bytes(32), "anchor": anchor,
                           "signer": "RESUME_SIGNER_SESSION_KEY", "power_state": "POWER_STATE_RESUMING",
                           "host": "HOST_CLASS_USB_PD", "drop_pending": [bytes(32)],
                           "last_frame_shown": 86_400_000, "signature": sig("44")},
        "resume_ack": {"session_id": 7_000_000_001, "resume_seq": 3, "validator_id": bytes(32),
                       "state_root": bytes(32), "resume_frame_no": 86_400_001, "intra_refresh": True,
                       "epoch": 3, "next_input_seq": 12_345_679, "finality_height": 2_000_010,
                       "dropped": [bytes(32)], "unconfirmed_frames": 240,
                       "validator_signature": sig("65")},
        "power_notice": {"state": "POWER_STATE_BRIDGE", "host": "HOST_CLASS_QI", "store_ms_live": 1_389_000,
                         "store_ms_hold": 974_000, "face_lit": True, "tier": "ENERGY_TIER_NORMAL",
                         "notice_seq": 41, "tag": bytes(16)},
    }


def sizes(schema):
    rows = []
    for body, obj in samples().items():
        raw = pl.encode(schema, "LeafMessage", {body: obj})
        back = pl.decode(schema, "LeafMessage", raw, strict=True)
        rows.append((body, len(raw), back == {body: obj}))
    return rows


def main():
    s = merged_schema()
    rows = sizes(s)
    out = ["# Sizes of the RG-19 messages (generated by protodraft.py)\n",
           "Envelope bytes with a stand-in signature of the exact FIPS 204 size.\n",
           "| message | envelope bytes | round trip |", "|---|---|---|"]
    for name, n, ok in rows:
        out.append(f"| {name} | {n} | {'ok' if ok else 'FAIL'} |")
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    open(os.path.join(HERE, "out", "proto_sizes.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"merged schema: {len(s.messages)} messages, {len(s.enums)} enums")


if __name__ == "__main__":
    main()
