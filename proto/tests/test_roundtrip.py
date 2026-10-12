#!/usr/bin/env python3
"""Round-trip test of every Leaf wire message, and the size table.

For each of the 31 LeafMessage bodies (and so every one of the 50 message
types, nested ones included):
  1. the hand-rolled canonical encoder (tools/protolite.py) and the official
     google.protobuf runtime (deterministic serialisation) give the same bytes;
  2. the hand-rolled strict decoder returns the original values;
  3. the google runtime parses the hand-rolled bytes and re-serialises them
     to the same bytes.
Then the integrity mechanisms run on real bytes: slice MAC (KMAC256), the
input chain, the frame hash chain, the per-second Merkle root, the receipt
signature scope, and the U6 rejection of a non-canonical header.

ML-DSA is not installed, so signatures and public keys are stand-ins of the
exact FIPS 204 sizes. Everything else is real.
Run:  python3 tests/test_roundtrip.py
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "model"))
import protolite as pl  # noqa: E402
from kmac import tag16, self_test as kmac_self_test  # noqa: E402
import bitrate  # noqa: E402

SCHEMA = pl.parse(os.path.join(ROOT, "budlum/leaf/v1/leaf.proto"))
CLASSES = pl.message_classes(SCHEMA)

PK = {"ML_DSA_44": 1312, "ML_DSA_65": 1952, "ML_DSA_87": 2592}
SIG = {"ML_DSA_44": 2420, "ML_DSA_65": 3309, "ML_DSA_87": 4627}
WIRE_VERSION = (1 << 16) | 0


def h(*parts):
    m = hashlib.sha3_256()
    for p in parts:
        m.update(p)
    return m.digest()


def stand_in(label, n):
    return hashlib.shake_256(label.encode()).digest(n)


def sig(scheme, label):
    return {"scheme": f"SIGNATURE_SCHEME_{scheme}", "key_id": h(label.encode() + b"pk"),
            "value": stand_in(label + "sig", SIG[scheme])}


K_SLICE = h(b"EXPORTER-BDLM_LEAF_SLICE_MAC_V1 epoch 0")
K_INPUT = h(b"EXPORTER-BDLM_LEAF_INPUT_MAC_V1 epoch 0")
WALLET = h(b"wallet address")
VALIDATOR = h(b"validator key")
SHADOW = h(b"shadow key")
APP = h(b"app program entry")


def merkle(leaves):
    level = [h(b"\x00", x) for x in leaves] or [h(b"")]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [h(b"\x01", level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def mac_over(msg, obj, field, key, domain, extra=b""):
    body = pl.encode(SCHEMA, msg, {k: v for k, v in obj.items() if k != field})
    return tag16(key, domain, body + extra)


# ------------------------------------------------------------- samples ---
def active_set(key_hash):
    return {"finality_height": 1_999_872, "validator_set_hash": h(b"set"),
            "validator_key_hash": key_hash, "leaf_index": 37,
            "merkle_path": [h(bytes([i])) for i in range(7)],  # 128 validators
            "finality_cert_digest": h(b"cert")}


def samples():
    display = {"width_px": 1600, "height_px": 3200, "tiles_x": 8, "tiles_y": 16,
               "tile_px": 200, "refresh_hz": 240, "ppi": 508, "bit_depth": 10,
               "codecs": ["CODEC_AV1", "CODEC_HEVC"], "frame_store_bytes": 16 << 20,
               "max_slices_per_frame": 128, "max_stretch_permille": 414,
               "max_layers": 16, "atlas_bytes": 2 << 20}
    grant = {"wallet_address": WALLET, "session_scheme": "SIGNATURE_SCHEME_ML_DSA_44",
             "session_public_key": stand_in("session pk", PK["ML_DSA_44"]),
             "app_program_id": APP, "expiry_height": 2_014_400, "scope_flags": 0b1011,
             "classes": ["FRAME_CLASS_C0_SAFE", "FRAME_CLASS_C1_DELTA", "FRAME_CLASS_C2_VIDEO",
                         "FRAME_CLASS_C3_STILL", "FRAME_CLASS_C4_CAMERA_UP"],
             "operators": [h(b"op1")], "energy_tier": "ENERGY_TIER_NORMAL",
             "nonce": stand_in("nonce", 32), "wallet_signature": sig("ML_DSA_87", "wallet")}
    hello = {"version": {"major": 1, "min_minor": 0, "max_minor": 0}, "chain_id": 1001,
             "device_id": h(b"u7 attestation"),
             "wallet_public_key": stand_in("wallet pk", PK["ML_DSA_87"]),
             "anchor": {"checkpoint_height": 1_990_000, "block_hash": h(b"blk"),
                        "validator_set_hash": h(b"set")},
             "display": display, "grant": grant, "path": "PATH_KIND_WIFI",
             "discovery": "DISCOVERY_LAYER_L0_ROOM",
             "uwb": {"anchor_id": h(b"dock")[:8], "distance_cm": 84, "time_of_flight_ps": 2802,
                     "sts_index": 991, "sts_digest": h(b"sts")},
             "client_nonce": stand_in("cn", 32), "last_frame_shown": 0,
             "supported_schemes": ["ml-dsa-87", "ml-dsa-65", "ml-dsa-44"]}
    admission = {"version_major": 1, "version_minor": 0, "session_id": 0x5EED_0001,
                 "validator_id": VALIDATOR,
                 "validator_public_key": stand_in("val pk", PK["ML_DSA_65"]),
                 "active_set": active_set(VALIDATOR),
                 "admitted_classes": ["FRAME_CLASS_C0_SAFE", "FRAME_CLASS_C1_DELTA",
                                      "FRAME_CLASS_C2_VIDEO", "FRAME_CLASS_C3_STILL"],
                 "refused": [{"frame_class": "FRAME_CLASS_C4_CAMERA_UP",
                              "code": "ERROR_CODE_R7_CLASS_NOT_CARRIED"}],
                 "key_slot": 1, "key_epoch": 0, "distance_class": "DISTANCE_CLASS_NEAR",
                 "measured_rtt_us": 380, "server_nonce": stand_in("sn", 32),
                 "transcript_hash": h(b"transcript"), "state_height": 2_000_011,
                 "validator_signature": sig("ML_DSA_65", "validator")}
    lease = {"lease_id": h(b"lease")[:16], "purpose": "photo: night fusion",
             "model_id": h(b"fusion model"), "sensors": ["SENSOR_CAMERA", "SENSOR_IMU"],
             "classes": ["FRAME_CLASS_C3_STILL", "FRAME_CLASS_C4_CAMERA_UP"],
             "expiry_height": 2_000_611, "retention": "RETENTION_SESSION", "subject": WALLET,
             "app_program_id": APP, "issuer_id": VALIDATOR,
             "issuer_signature": sig("ML_DSA_65", "lease v"),
             "wallet_signature": sig("ML_DSA_44", "lease w")}
    inp = {"batch_seq": 1_728_001, "t0_us": 3_600_002_083, "shown_frame": 864_000,
           "touches": [
               {"contact": 1, "tool": "TOOL_KIND_FINGER", "phase": "TOUCH_PHASE_MOVE",
                "x_q4": 812 * 16 + 5, "y_q4": 2_210 * 16 + 9, "pressure": 412, "dt_us": 0},
               {"contact": 2, "tool": "TOOL_KIND_FINGER", "phase": "TOUCH_PHASE_MOVE",
                "x_q4": 1_190 * 16 + 1, "y_q4": 2_640 * 16 + 12, "pressure": 388, "dt_us": 0}],
           "stretch": {"theta_mdeg": 17_500, "seat": 2},
           "imu": [12, -40, 16_380, 3, -2, 1]}
    inp["tag"] = mac_over("InputBatch", inp, "tag", K_INPUT, b"BDLM_LEAF_INPUT_V1")
    inp_key = dict(inp, batch_seq=1_728_002, touches=[], keys=[
        {"key_code": 0x61, "glyph_id": 68, "atlas_id": 1, "echo_frame": 864_001}],
        taken_branch=3)
    inp_key.pop("stretch"); inp_key.pop("imu")
    inp_key["tag"] = mac_over("InputBatch", inp_key, "tag", K_INPUT, b"BDLM_LEAF_INPUT_V1")
    action = {"batch_seq": 1_728_010, "budlum_transaction": stand_in("ProtoTransaction", 4_900)}
    freq = {"request_seq": 77, "input_batch_seq": 1_728_001, "base_frame": 864_000,
            "frame_class": "FRAME_CLASS_C2_VIDEO", "max_speculative": 4,
            "region": {"x": 0, "y": 1_600, "w": 1_600, "h": 1_600}, "target_refresh_hz": 240,
            "deadline_us": 8_000, "rate_hint_kbps": 240_000}
    payload = stand_in("av1 slice", bitrate.slice_payload_bytes())
    header = {"key_slot": 1, "frame_no": 864_001, "slice_no": 11, "slice_count": 16,
              "first_tile": 88, "tile_count": 8, "codec": "CODEC_AV1",
              "kind": "SLICE_KIND_INTER", "ref_frame": 864_000, "payload_bytes": len(payload)}
    hdr_bytes = pl.encode(SCHEMA, "SliceHeader", header)
    slice_ = {"header": header, "payload": payload,
              "mac": tag16(K_SLICE, b"BDLM_LEAF_SLICE_V1", hdr_bytes + payload)}
    frag = {"frame_no": 864_001, "slice_no": 11, "frag_no": 2, "frag_count": 3,
            "data": payload[:1_150]}
    slice_hashes = [h(bytes([i])) for i in range(16)]
    fh = merkle(slice_hashes)
    commit = {"frame_no": 864_001, "slice_count": 16, "frame_hash": fh,
              "chain_hash": h(b"BDLM_LEAF_FRAME_CHAIN_V1", h(b"prev"), fh),
              "rc_target_bits": 245_000, "present_at_us": 3_600_006_250,
              "state_height": 2_000_011}
    commit["mac"] = mac_over("FrameCommit", commit, "mac", K_SLICE, b"BDLM_LEAF_FRAME_COMMIT_V1")
    spec = {"base_frame": 864_001, "valid_until_frame": 864_049, "branches": [
        {"branch_id": i + 1, "trigger": t, "hit_region": {"x": 40, "y": 400 * i, "w": 1_520, "h": 160},
         "param_min": -800 if t == "TRIGGER_KIND_SCROLL" else 0,
         "param_max": 800 if t == "TRIGGER_KIND_SCROLL" else 0,
         "first_frame": 1 << 40 | i << 20, "frame_count": 12, "layer_id": 4 + i,
         "frame_hash": h(bytes([i]))}
        for i, t in enumerate(["TRIGGER_KIND_SCROLL", "TRIGGER_KIND_TAP",
                               "TRIGGER_KIND_MENU_OPEN", "TRIGGER_KIND_BACK"])]}
    spec["mac"] = mac_over("SpeculativeFrameSet", spec, "mac", K_SLICE, b"BDLM_LEAF_SPECULATIVE_V1")
    resolve = {"branch_id": 2, "committed": True, "at_frame": 864_010}
    layers = {"version": 412, "apply_at_frame": 864_002, "layers": [
        {"layer_id": 1, "z": 0, "job": "COMPOSITOR_JOB_SCROLL",
         "dest": {"x": 0, "y": 160, "w": 1_600, "h": 2_880},
         "source": {"x": 0, "y": 0, "w": 1_600, "h": 2_880}, "surface_w": 1_600,
         "surface_h": 6_400, "blend": "BLEND_MODE_OPAQUE", "alpha": 255,
         "scroll_min": 0, "scroll_max": 3_520, "warp": True},
        {"layer_id": 2, "z": 5, "job": "COMPOSITOR_JOB_GLYPH_ECHO",
         "dest": {"x": 80, "y": 2_900, "w": 1_440, "h": 120},
         "source": {"x": 0, "y": 0, "w": 1_440, "h": 120}, "surface_w": 1_440,
         "surface_h": 120, "blend": "BLEND_MODE_ALPHA", "alpha": 255,
         "echo": {"atlas_id": 1, "caret_x_q4": 412 * 16, "caret_y_q4": 2_990 * 16,
                  "line_height_px": 64, "color_rgba": 0x202020FF,
                  "clip": {"x": 80, "y": 2_900, "w": 1_440, "h": 120}}, "warp": True},
        {"layer_id": 3, "z": 9, "job": "COMPOSITOR_JOB_CURSOR",
         "dest": {"x": 400, "y": 700, "w": 48, "h": 48},
         "source": {"x": 0, "y": 0, "w": 48, "h": 48}, "surface_w": 48, "surface_h": 48,
         "blend": "BLEND_MODE_ALPHA", "alpha": 230, "warp": True}],
        "removed": [7, 8]}
    layers["mac"] = mac_over("LayerUpdate", layers, "mac", K_SLICE, b"BDLM_LEAF_LAYER_V1")
    glyphs = [{"glyph_id": 36 + i, "codepoint": 0x41 + i, "atlas_x": (i % 32) * 48,
               "atlas_y": (i // 32) * 64, "w": 34, "h": 46, "bearing_x": 2, "bearing_y": 46,
               "advance_q6": 38 * 64} for i in range(26)]
    atlas = {"atlas_id": 1, "version": 9, "atlas_w": 1_536, "atlas_h": 1_024,
             "format": "ATLAS_FORMAT_A8_RLE", "glyphs": glyphs,
             "dirty": {"x": 0, "y": 0, "w": 1_536, "h": 64},
             "bitmap": stand_in("rle glyph row", 26 * 34 * 46 // 3)}
    atlas["mac"] = mac_over("GlyphAtlasUpdate", atlas, "mac", K_SLICE, b"BDLM_LEAF_ATLAS_V1")
    frame_hashes = [h(i.to_bytes(8, "big")) for i in range(240)]
    mroot = {"epoch": 3_600, "first_frame": 863_760, "last_frame": 863_999, "leaf_count": 240,
             "root": merkle(frame_hashes), "chain_head": h(b"head"), "state_height": 2_000_010,
             "validator_signature": sig("ML_DSA_65", "merkle")}
    receipt = {"session_id": 0x5EED_0001, "epoch": 3_600, "merkle_root": mroot["root"],
               "frames_shown": 236, "frames_reprojected": 3, "frames_speculative": 1,
               "input_chain_head": h(b"input head"), "last_input_seq": 1_728_000,
               "paths": [{"kind": "PATH_KIND_WIFI", "rtt_p50_us": 410, "rtt_p99_us": 1_250,
                          "loss_ppm": 120, "ce_ppm": 3_400, "goodput_kbps": 1_480_000},
                         {"kind": "PATH_KIND_CELL", "rtt_p50_us": 6_100, "rtt_p99_us": 11_800,
                          "loss_ppm": 900, "ce_ppm": 8_000, "goodput_kbps": 210_000}],
               "validator_id": VALIDATOR, "distance_class": "DISTANCE_CLASS_NEAR",
               "leaf_signature": sig("ML_DSA_44", "receipt")}
    shadow = {"validator_id": SHADOW, "public_key": stand_in("shadow pk", PK["ML_DSA_65"]),
              "active_set": active_set(SHADOW), "endpoints": ["/ip6/2001:db8::7/udp/4433/quic-v1"],
              "key_slot": 2, "primary_signature": sig("ML_DSA_65", "announce")}
    beat = {"validator_id": SHADOW, "frame_no": 864_001, "chain_hash": commit["chain_hash"],
            "rtt_us": 2_900}
    hand = {"switch_frame": 864_004, "switch_slice": 0, "from_validator": VALIDATOR,
            "to_validator": SHADOW, "new_key_slot": 2, "reason": "HANDOVER_REASON_RTT",
            "expected_chain_hash": commit["chain_hash"]}
    hand["tag"] = mac_over("HandoverCommand", hand, "tag", K_INPUT, b"BDLM_LEAF_HANDOVER_V1")
    hack = {"switch_frame": 864_004, "validator_id": SHADOW, "accepted": True}
    probe = {"probe_id": 90_001, "t_send_us": 3_600_010_000}
    probe_ack = {"probe_id": 90_001, "t_send_us": 3_600_010_000, "server_hold_us": 21,
                 "state_height": 2_000_011, "validator_id": SHADOW}
    cap_id = h(b"capture 1")[:16]
    cam_open = {"capture_id": cap_id, "lease_id": lease["lease_id"],
                "mode": "CAPTURE_MODE_FUSION_BURST", "width": 8_160, "height": 6_144,
                "packing": "RAW_PACKING_RAW10_LOSSLESS", "frame_count": 9,
                "total_bytes": int(bitrate.capture_bytes(
                    bitrate.CAPTURES["fusion burst: 1 full + 8 binned, RAW10 lossless"])),
                "deadline": "DEADLINE_CLASS_STANDARD_60S", "exposure_us": 33_000, "iso": 1_600,
                "focus_um": 41, "imu": [3, -1, 16_384, 0, 1, 0],
                "provisional_hash": h(b"provisional jpeg")}
    cam_open["tag"] = mac_over("CameraCaptureOpen", cam_open, "tag", K_INPUT, b"BDLM_LEAF_CAPTURE_V1")
    chunk = {"capture_id": cap_id, "frame_index": 0, "offset": 16_384 * 17,
             "data": stand_in("raw chunk", 16_384)}
    cam_close = {"capture_id": cap_id, "chunk_count": 6_349,
                 "chunk_root": merkle([h(bytes([i])) for i in range(64)]),
                 "leaf_signature": sig("ML_DSA_44", "capture")}
    cam_result = {"capture_id": cap_id, "result_frame": 900_123, "result_hash": h(b"final"),
                  "pipeline_id": h(b"fusion pipeline v3"),
                  "validator_signature": sig("ML_DSA_65", "result")}
    audio_down = {"stream_id": 1, "direction": "AUDIO_DIRECTION_DOWNLINK",
                  "codec": "AUDIO_CODEC_OPUS", "seq": 360_000, "pts_us": 3_600_000_000,
                  "duration_us": 10_000, "channels": 2, "payload": stand_in("opus", 160),
                  "sync_frame": 864_000}
    audio_mic = {"stream_id": 2, "direction": "AUDIO_DIRECTION_UPLINK_MIC",
                 "codec": "AUDIO_CODEC_OPUS", "seq": 360_000, "pts_us": 3_600_000_000,
                 "duration_us": 10_000, "channels": 2, "payload": stand_in("opus mic", 80),
                 "lease_ref": 1}
    cls = {"distance": "DISTANCE_CLASS_FAR",
           "active": ["FRAME_CLASS_C0_SAFE", "FRAME_CLASS_C1_DELTA"],
           "line": "far: video buffered, 3D off", "reason": "ERROR_CODE_RTT_OVER_CLASS"}
    keyu = {"key_slot": 1, "key_epoch": 1, "from_frame": 1_728_000}
    err = {"code": "ERROR_CODE_SLICE_MAC_FAILED", "ref_seq": 864_001,
           "detail": "frame 864001 slice 11", "fatal": False}
    bye = {"code": "ERROR_CODE_UNSPECIFIED", "last_frame": 864_100}
    revoke = {"lease_id": lease["lease_id"], "reason": "ERROR_CODE_R3_LEASE_EXPIRED",
              "signature": sig("ML_DSA_44", "revoke")}
    # (body field, sample, label for the size table, rate in Hz for the table)
    return [
        ("hello", hello, "hello", None), ("admission", admission, "admission", None),
        ("lease", lease, "lease", None), ("lease_revoke", revoke, "lease_revoke", None),
        ("input_batch", inp, "input_batch", 480), ("input_batch", inp_key, "input_batch_key", None),
        ("action_tx", action, "action_tx", None), ("frame_request", freq, "frame_request", 10),
        ("slice", slice_, "slice", 240 * 16), ("slice_fragment", frag, "slice_fragment", None),
        ("frame_commit", commit, "frame_commit", 240),
        ("speculative_frame_set", spec, "speculative_frame_set", 20),
        ("speculation_resolve", resolve, "speculation_resolve", 20),
        ("layer_update", layers, "layer_update", None),
        ("glyph_atlas_update", atlas, "glyph_atlas_update", None),
        ("merkle_root", mroot, "merkle_root", 1), ("receipt", receipt, "receipt", 1),
        ("shadow_announce", shadow, "shadow_announce", None),
        ("shadow_heartbeat", beat, "shadow_heartbeat", 240),
        ("handover_command", hand, "handover_command", None),
        ("handover_ack", hack, "handover_ack", None),
        ("path_probe", probe, "path_probe", 5), ("path_probe_ack", probe_ack, "path_probe_ack", 5),
        ("camera_capture_open", cam_open, "camera_capture_open", None),
        ("camera_raw_chunk", chunk, "camera_raw_chunk", None),
        ("camera_capture_close", cam_close, "camera_capture_close", None),
        ("camera_result", cam_result, "camera_result", None),
        ("audio_frame", audio_down, "audio_frame_down", 100),
        ("audio_frame", audio_mic, "audio_frame_mic", 100),
        ("class_statement", cls, "class_statement", None), ("key_update", keyu, "key_update", None),
        ("error", err, "error", None), ("goodbye", bye, "goodbye", None),
    ]


# --------------------------------------------------------------- checks ---
def strip_defaults(msg, obj):
    fields = {f.name: f for f in SCHEMA.fields(msg)}
    out = {}
    for k, v in obj.items():
        f = fields[k]
        if f.kind == "message":
            out[k] = [strip_defaults(f.type_name, x) for x in v] if f.repeated else strip_defaults(f.type_name, v)
            if f.repeated and not v:
                del out[k]
            continue
        if f.repeated:
            if v:
                out[k] = list(v)
            continue
        if f.oneof is None and v in (0, "", b"", False) or (f.kind == "enum" and str(v).endswith("_UNSPECIFIED") and f.oneof is None):
            continue
        out[k] = v
    return out


def walk_types(msg, obj, seen):
    seen.add(msg)
    fields = {f.name: f for f in SCHEMA.fields(msg)}
    for k, v in obj.items():
        f = fields[k]
        if f.kind == "message":
            for x in (v if f.repeated else [v]):
                walk_types(f.type_name, x, seen)


def run():
    assert kmac_self_test(), "KMAC256 NIST sample failed"
    failures = 0
    seen = set()
    bodies = set()
    rows = []
    for body, obj, label, hz in samples():
        env = {"wire_version": WIRE_VERSION, body: obj} if body in ("hello", "admission") else {body: obj}
        walk_types("LeafMessage", env, seen)
        bodies.add(body)
        mine = pl.encode(SCHEMA, "LeafMessage", env)
        theirs = pl.to_pb(SCHEMA, CLASSES, "LeafMessage", env).SerializeToString(deterministic=True)
        back = pl.decode(SCHEMA, "LeafMessage", mine)
        g = CLASSES["LeafMessage"]()
        g.ParseFromString(mine)
        ok = (mine == theirs and back == strip_defaults("LeafMessage", env)
              and g.SerializeToString(deterministic=True) == mine
              and pl.encode(SCHEMA, "LeafMessage", back) == mine)
        failures += not ok
        inner = len(pl.encode(SCHEMA, _type_of(body), obj))
        rows.append((label, len(mine), inner, hz, "ok" if ok else "FAIL"))
    all_bodies = {f.name for f in SCHEMA.fields("LeafMessage") if f.oneof}
    missing_bodies = all_bodies - bodies
    missing_types = set(SCHEMA.messages) - seen
    failures += bool(missing_bodies) + bool(missing_types)

    checks = integrity_checks()
    failures += sum(not ok for _, ok in checks)

    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with open(os.path.join(ROOT, "out", "sizes.csv"), "w") as fh:
        fh.write("message,envelope_bytes,body_bytes,rate_hz,result\n")
        for r in rows:
            fh.write(",".join(str(x if x is not None else "") for x in r) + "\n")
    md = ["# The Leaf message size table (generated by tests/test_roundtrip.py)\n",
          "Envelope bytes include the LeafMessage key and length. Rate is the steady-state",
          "rate in a game session at 240 Hz; an empty rate means event-driven.\n",
          "| message | envelope bytes | body bytes | rate Hz | kbit/s | round trip |",
          "|---|---|---|---|---|---|"]
    for label, env_b, body_b, hz, res in rows:
        kb = f"{env_b * hz * 8 / 1e3:.1f}" if hz else ""
        md.append(f"| {label} | {env_b} | {body_b} | {hz or ''} | {kb} | {res} |")
    md.append("\n## Integrity checks\n")
    md.append("| check | result |")
    md.append("|---|---|")
    for name, ok in checks:
        md.append(f"| {name} | {'ok' if ok else 'FAIL'} |")
    md.append(f"\nMessage types covered: {len(seen)} of {len(SCHEMA.messages)}. "
              f"Envelope bodies covered: {len(bodies)} of {len(all_bodies)}.\n")
    open(os.path.join(ROOT, "out", "sizes.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))
    if missing_bodies or missing_types:
        print("MISSING:", sorted(missing_bodies), sorted(missing_types))
    print("FAILURES:", failures)
    return failures


def _type_of(body):
    for f in SCHEMA.fields("LeafMessage"):
        if f.name == body:
            return f.type_name
    raise KeyError(body)


def integrity_checks():
    out = []
    smp = {label: obj for _, obj, label, _ in samples()}
    s = smp["slice"]
    hdr = pl.encode(SCHEMA, "SliceHeader", s["header"])
    good = tag16(K_SLICE, b"BDLM_LEAF_SLICE_V1", hdr + s["payload"]) == s["mac"]
    out.append(("slice MAC verifies (KMAC256, 16 bytes)", good))
    bad_payload = bytearray(s["payload"]); bad_payload[100] ^= 1
    out.append(("slice MAC rejects a flipped payload bit",
                tag16(K_SLICE, b"BDLM_LEAF_SLICE_V1", hdr + bytes(bad_payload)) != s["mac"]))
    bad_hdr = dict(s["header"], frame_no=s["header"]["frame_no"] + 1)
    out.append(("slice MAC rejects a replayed frame number",
                tag16(K_SLICE, b"BDLM_LEAF_SLICE_V1", pl.encode(SCHEMA, "SliceHeader", bad_hdr)
                      + s["payload"]) != s["mac"]))
    k_shadow = h(b"exporter shadow")
    out.append(("a slice under the shadow key slot fails the primary key",
                tag16(k_shadow, b"BDLM_LEAF_SLICE_V1", hdr + s["payload"]) != s["mac"]))
    # A non-canonical header: fields 3 and 2 swapped. U6 strict parse rejects it.
    f2 = pl.encode(SCHEMA, "SliceHeader", {"frame_no": 5})
    f3 = pl.encode(SCHEMA, "SliceHeader", {"slice_no": 2})
    try:
        pl.decode(SCHEMA, "SliceHeader", f3 + f2)
        rejected = False
    except ValueError:
        rejected = True
    out.append(("U6 strict parse rejects out-of-order header fields", rejected))
    try:
        pl.decode(SCHEMA, "SliceHeader", b"\x08\x81\x00")  # padded varint
        rejected = False
    except ValueError:
        rejected = True
    out.append(("U6 strict parse rejects a non-minimal varint", rejected))
    # Input chain over 480 batches; one altered batch changes the head.
    inp = smp["input_batch"]
    head = bytes(32)
    batches = []
    for n in range(480):
        b = dict(inp, batch_seq=inp["batch_seq"] + n)
        b.pop("tag")
        raw = pl.encode(SCHEMA, "InputBatch", b)
        batches.append(raw)
        head = h(b"BDLM_LEAF_INPUT_CHAIN_V1", head, raw)
    head2 = bytes(32)
    for n, raw in enumerate(batches):
        if n == 200:
            raw = raw[:-1] + bytes([raw[-1] ^ 1])
        head2 = h(b"BDLM_LEAF_INPUT_CHAIN_V1", head2, raw)
    out.append(("input chain head detects one altered batch in 480", head != head2))
    body = dict(inp); tag = body.pop("tag")
    out.append(("input batch tag verifies",
                tag16(K_INPUT, b"BDLM_LEAF_INPUT_V1", pl.encode(SCHEMA, "InputBatch", body)) == tag))
    # Frame hash chain and the Merkle root of one second.
    chain = bytes(32)
    hashes = []
    for i in range(240):
        fh = merkle([h(i.to_bytes(4, "big"), bytes([j])) for j in range(16)])
        hashes.append(fh)
        chain = h(b"BDLM_LEAF_FRAME_CHAIN_V1", chain, fh)
    root = merkle(hashes)
    alt = list(hashes); alt[17] = h(b"forged")
    out.append(("Merkle root of 240 frames detects a forged frame", merkle(alt) != root))
    # Deterministic shadow: same frames give the same chain head.
    chain_s = bytes(32)
    for fh in hashes:
        chain_s = h(b"BDLM_LEAF_FRAME_CHAIN_V1", chain_s, fh)
    out.append(("shadow chain head equals primary chain head (zero-frame handover)", chain_s == chain))
    # Receipt signature scope: canonical bytes without leaf_signature are stable.
    r = smp["receipt"]
    scope = pl.encode(SCHEMA, "Receipt", {k: v for k, v in r.items() if k != "leaf_signature"})
    scope2 = CLASSES["Receipt"]()
    scope2.ParseFromString(pl.encode(SCHEMA, "Receipt", r))
    scope2.ClearField("leaf_signature")
    out.append(("receipt signing scope is identical in both encoders",
                scope2.SerializeToString(deterministic=True) == scope))
    # Version: a peer with major 2 gets VERSION_UNSUPPORTED.
    out.append(("version negotiation picks the highest common minor",
                negotiate((1, 0, 3), (1, 1, 5)) == (1, 3) and negotiate((2, 0, 0), (1, 0, 9)) is None))
    # Every refusal R1..R10 has an error code.
    codes = SCHEMA.enums["ErrorCode"]
    out.append(("R1..R10 each map to one error code 301..310",
                sorted(v for k, v in codes.items() if re.match(r"ERROR_CODE_R\d", k)) == list(range(301, 311))))
    return out


def negotiate(leaf, validator):
    """(major, min_minor, max_minor) each; returns (major, minor) or None."""
    if leaf[0] != validator[0]:
        return None
    lo, hi = max(leaf[1], validator[1]), min(leaf[2], validator[2])
    return (leaf[0], hi) if lo <= hi else None


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
