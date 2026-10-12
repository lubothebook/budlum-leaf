# BUDLUM LEAF · FW/BOOT · THE FIRMWARE-INTEGRITY TEAM

**Revision L.6.0 · 2026-10-12**. The Leaf has no general-purpose CPU, but ten kinds of part carry vendor code on small cores. This directory says who signs that code, how `U7` measures it, how it is updated, and how the Leaf boots when a part fails.

## 1 · What is here

| File | What it holds |
|---|---|
| `MODEL.md` | deliverable 1: the four signatures, the manifest, the five measure methods, the update path, rollback, the failure table |
| `leaffw.py` | deliverable 2: the manifest tool, ed25519 and SHA-256 with Merkle chunks |
| `ZERO-CPU.md` | deliverable 3: the compliance argument per part, tests Z1 to Z6 |
| `chips.json` | the data of every part with code: jobs, size, store, signers, measure method, gate, fail policy |
| `zero_cpu.py` | the Z1 to Z6 check over `chips.json` |
| `STATE-MACHINE.md` | deliverable 4: the dead-pad and safe-screen state machine |
| `bootsm.py` | the executable state machine, the step times and the fault sweep |
| `tests/` | `57` tests: `30` of the tool, `19` of the state machine, `8` of the declaration |

## 2 · How to run it

```sh
cd fw/boot
python3 -m unittest discover -s tests -v       # 57 tests, about 25 s
python3 leaffw.py demo /tmp/leafdemo           # a full signed set, verified
python3 bootsm.py --sweep                      # the trace, the budgets, 131 072 boots
python3 zero_cpu.py --markdown                 # the compliance table
```

The tool flow for a real release:

1. Run `leaffw.py keygen` once per key. In production the keys live in HSMs.
2. Run `leaffw.py build spec.json images/ manifest.json`.
3. Run `leaffw.py vsign manifest.json U2A wifi-vendor.key` once per chip.
4. Run `leaffw.py sign manifest.json release-N.key` three times.
5. Run `leaffw.py hash manifest.json`. The governance proposal carries this hash.
6. Run `leaffw.py verify manifest.json images/ trust.json state.json chain.json`.
7. Run `leaffw.py commit state.json manifest.json --trial-passed` after a clean trial.

Dependency: the `cryptography` package for ed25519. It is installed.

## 3 · The key results

1. **Two independent compromises per attack**. The vendor key, three of five release keys and the chain vote must all agree. `[DECISION]` `MODEL.md` Section 2.
2. **No part trusts a validator for code**. Validators carry bytes. `U7` checks every `4 KiB` chunk against the release on chain. `[DECISION]`
3. **Rollback is closed at two levels**: `release_seq` and a per-chip `svn` floor. Floors rise only after a clean trial. `[DECISION]` eight rollback tests pass.
4. **Tamper is located**. A one-bit flip names its chip and its `4 KiB` chunk. `test_flip_one_byte_in_a_blob`.
5. **The safe screen lands at `23.2 ms`**, against the `60 ms` target. The worst of `131 072` fault boots lands at `31.2 ms`. `[HYPOTHESIS]` step times.
6. **Never a brick**. Every one of `171 072` modelled boots ends in a visible, stated state. `0` violations of seven invariants.
7. **Zero CPU holds for `13` of `14` entries**: `2` PASS and `11` CONDITIONAL on supplier terms. The eSIM is OPEN. `ZERO-CPU.md`.
8. **The firmware store**. The boot NOR set is `6.9 MiB` per slot. Two slots fit a `16 MiB` NOR. A whole release is `55 MiB` with the modem. `[HYPOTHESIS]` sizes.

## 4 · The gates

SW-21, SW-22, ENR-19, MON-16, the boot matrix of `FINAL/08` Section 8.8 step 6, refusal R5. Proposed: FW-1 tamper, FW-2 replay, FW-3 revocation, in `MODEL.md` Section 9.

## 5 · The open issues

| No. | The issue | The owner | What it needs |
|---|---|---|---|
| O1 | the eSIM carries operator applets inside the card | Ayaz | a ruling: is a sealed credential card inside the rule. `ZERO-CPU.md` Section 6 |
| O2 | a `16 MiB` boot NOR is not on the part list of `HARDWARE/13` | the hardware team | a WLCSP NOR on the ring PCBA, about `2 x 3 mm` `[HYPOTHESIS]` |
| O3 | DICE or an owner-key boot on `U6`, `U2A`, `U2B`, `U5` | purchasing | the conditions of `ZERO-CPU.md` Section 4 in each purchase specification |
| O4 | a hostless Wi-Fi 7 combo that boots from its own flash | purchasing, link team | a supplier part; the transport layer location agreed with the link team |
| O5 | `U7` on slot B takes step 1 to `23 ms`, over `20 ms` | the `U7` team | a `6 ms` `U7` slot check |
| O6 | the release record is not a `ProposalType` in the tree | the chain team | `LeafFirmwareRelease {release_hash, release_seq, floor_release_seq}`, and its domain tags |
| O7 | the touch front end and the ISP have no part yet | the hardware team | `chips.json` assumes the touch front end sits in `U1` |
| O8 | the reference checks ed25519 only | this team | add the ML-DSA-87 half when a Python binding is chosen |
| O9 | every step time and size | the bench | the boot matrix measures them; rerun `bootsm.py` with the values |
