# BUDLUM LEAF · FW/BOOT · THE SIGNED-FIRMWARE MODEL

**Revision L.6.0 · 2026-10-12 · Firmware-Integrity team**. Sources: `FINAL/21` Section 21.5.1, `FINAL/08` Sections 8.1, 8.2 and 8.7, `HARDWARE/02`, `HARDWARE/13`. The tool `leaffw.py` is the executable form of this file.

## 1 · The problem in one paragraph

The Leaf has no general-purpose CPU. Ten kinds of part still carry vendor code on small cores: `U7`, `U1`, `U2A`, `U2B`, `U3`, `U4`, `U5`, `U6`, `U8` and the quadrant nodes. The port part and the camera carry settings. No host processor exists to load them, check them or update them. Therefore `U7` is the only verifier. Each part boots itself and proves what it booted. `[DECISION]`

## 2 · The four signatures

| Signer | What it signs | Who holds the key | Where it is checked |
|---|---|---|---|
| the chip vendor | one blob: chip, version, `svn`, SHA-256, Merkle root | the vendor HSM | the chip ROM, and `U7` through `leaffw` check B2 |
| the Budlum owner key | the same blob, as a second boot key | a Budlum HSM, its hash fused into the chip OTP | the chip ROM, on parts that support an owner key |
| the Budlum release keys | the manifest: every blob entry, `release_seq`, floors | `5` keys, `3` needed, on separate HSMs | `U7`, check M2 |
| the chain | the release hash, by a governance vote of the validators | stake of the `VALIDATOR` role, `RoleId(1)` `[TREE]` | `U7`, through a finality proof, check M3 |

**Why four**. A stolen vendor key alone fails M2. Three stolen release keys alone fail M3. A captured validator set fails at the device anchor rule of `FINAL/08` Section 8.5. Every attack needs two independent compromises. `[DECISION]`

**The cryptography**. The reference uses ed25519 and SHA-256, as the tree uses `ed25519-dalek` and `sha2` `[TREE]`. The production manifest adds an ML-DSA-87 release signature beside ed25519. `U7` checks ML-DSA-87 at install only. At boot it checks ed25519 and the stored digest, which keeps step 1 inside `20 ms`. `[HYPOTHESIS]`

**The domain tags**. `BDLM_LEAF_FW_MANIFEST_V1`, `BDLM_LEAF_FW_RELEASE_V1`, `BDLM_LEAF_FW_VENDOR_BLOB_V1`, `BDLM_LEAF_FW_CHUNK_LEAF_V1`, `BDLM_LEAF_FW_CHUNK_NODE_V1`, `BDLM_LEAF_FW_KEY_ID_V1`. They enter the tag inventory of `src/crypto/domain_tags.rs` when the chain team adds the release record. `[TREE]`

## 3 · The manifest

```text
Manifest { format, product, release_seq, floor_release_seq, blobs: [BlobEntry] }
BlobEntry { chip, vendor, version, svn, floor_svn, size, chunk = 4096,
            sha256, merkle_root, measure, store, file, vendor_sig }
release_hash = SHA-256( BDLM_LEAF_FW_RELEASE_V1 || canonical(Manifest) )
```

1. `svn` is the security version of the blob. `floor_svn` is the lowest `svn` that stays bootable after this release commits.
2. `merkle_root` covers `4 KiB` chunks. A download checks every chunk before it writes, and a tamper names its chunk.
3. `measure` names how `U7` learns what the part booted. Section 4 lists the five methods.

## 4 · How U7 measures each part

| Method | How it works | Parts | Strength |
|---|---|---|---|
| `self-rom` | the `U7` ROM checks its own slot A, then slot B | `U7` | root of trust |
| `direct` | `U7` reads the blob from the boot NOR and hashes it, then releases the part | `U4` patch, `U1` microcode, `U3`, `U8`, `CAM` | strongest: `U7` sees the bytes |
| `dice` | the part ROM hashes its image before it runs it, and derives its report key from that hash | `U6`, `U2A`, `U2B` | a changed image cannot sign the old hash `[PUBLICATION]` TCG DICE |
| `owner-key+scrub` | the part ROM runs only owner-signed images and sends a signed report; `U7` re-reads the store at rest | `U5` | relies on the vendor ROM |
| `handshake` | the dead-pad answer carries the hash of the part code and tables | quadrant nodes, port part | inside the `3 ms` window |

**The gate rule**. A part runs its code before `U7` passes it. Its outputs stay closed meanwhile. `U4` holds the PA rail, the microphone bias or the data lane open. `U7` releases the gate only on PASS. `[DECISION]`

**The timing** comes from `bootsm.py`. The `U7` direct hashes take `75 ms` at a `6 MB/s` SPI read. They start after the safe screen, so they never delay it. `[HYPOTHESIS]`

## 5 · How an update arrives

1. The vendor delivers a blob and its signature. The team reviews the binary and records an SBOM.
2. `leaffw.py build` makes the manifest. The vendor signs its entry with `vsign`.
3. Three release keys sign with `sign`. `leaffw.py hash` prints the release hash.
4. A governance proposal carries `{release_hash, release_seq, floor_release_seq, activation_epoch}`. Validators vote by stake.
5. The tree has `activation_epoch` on `Proposal` `[TREE]`. It has no Leaf release variant yet. The chain team adds `ProposalType::LeafFirmwareRelease`.
6. Validators pin the blobs. The serving validator streams them as an update class, while the Leaf rests or charges.
7. `U7` proves the finalised record with the finality certificates it already follows, as in Section 21.5.4.
8. Each `4 KiB` chunk passes `U7`, which checks its Merkle leaf. Then `U7` writes it to the inactive NOR slot.
9. `U5` writes its own NAND slot. Its ROM checks the owner signature at the trial boot.
10. `U7` runs `verify` on the full set: checks M1 to M5 and B1 to B4.
11. The next boot is a trial boot of the new slot.
12. A clean trial reaches a session. Then `U7` runs `commit` and raises the floors.

**The cost**. The NOR set is `6.9 MiB` per slot, so two slots fit in a `16 MiB` NOR. A whole release is `55 MiB` with the modem. Writing the NOR takes about `9 s` at a `0.8 MB/s` program rate. `[HYPOTHESIS]` `bootsm.py`

**The validator never decides**. A validator only carries bytes. The chain record and the release keys decide. A forged chunk fails at `U7` and costs one re-fetch. `[DECISION]`

## 6 · Rollback protection

| Rule | Where | Test |
|---|---|---|
| `release_seq` never falls below the installed one | `U7` state, check M4 | `test_older_release_refused` |
| `release_seq` never falls below the floor on chain | the governance record, check M4 | `test_release_floor_from_chain` |
| one `release_seq` has one hash | check M4 | `test_same_seq_other_hash` |
| a blob `svn` never falls below its floor | `U7` counters, check B3 | `test_chip_svn_below_floor` |
| an old signed release is refused after a newer commit | M4 | `test_old_signed_release_replayed` |
| floors rise only after a clean trial | `commit` | `test_failed_trial_does_not_raise_floors` |
| floors rise to `floor_svn`, never to `svn` | `commit` | `test_commit_raises_floor_to_floor_svn_only` |
| floors never fall | `commit` | `test_floor_never_drops` |

**Why `floor_svn` and `svn` differ**. An ordinary release keeps the previous slot bootable, so slot B stays a real fallback. A security fix sets `floor_svn = svn`, and the old slot dies on commit. `[DECISION]`

**Revocation**. The chain can raise `floor_release_seq` or list a release hash as revoked. The Leaf then enters `UPDATE_REQUIRED`: the safe screen, the wallet, and only the update class on the link.

## 7 · When a part fails attestation

| Part | First answer | Second answer | What the user sees |
|---|---|---|---|
| `U7` | its slot B | `SE_FAULT`: no pad closes, wallet locked | the rear safe screen and a service line |
| `U4` patch | ROM defaults, charge limited | none needed | a stated line |
| `U1` microcode | the radio and stream domain restarts on slot B | `RECOVERY` | the ROM safe screen |
| `U6` | slot B | `RECOVERY`, repair through `U7` | the safe screen and the recovery offer |
| `U2A` or `U5` | the other radio carries the session | both lost: slot B, then `RECOVERY` | a stated line per radio |
| `U2B`, `U3`, `U8`, `CAM` | held off, repair download queued | none | a stated line: no ranging, no audio, default seat, no camera |
| a quadrant | stays at `0 V` | the others serve | a stated line per quadrant |
| the port part | its pads stay dead | none | refusal R5 of Part 8 |

**The repair**. A quarantined part gets its blob again from the same manifest. No new release is needed. The repair download uses any attested radio. `[DECISION]`

**A trial is stricter**. On a trial boot, any refused part reverts the whole set to the previous slot. The floors stay where they were. `[DECISION]` `test_trial_reverts_on_any_fault`

## 8 · The gates

| Result | Gate |
|---|---|
| a stream key outside the active set gives the safe screen | SW-22 |
| the compositor in `U1` runs no program, its inputs are data | SW-21 |
| the boot matrix and refusals R1 to R5 | `FINAL/08` Section 8.8 step 6 |
| the pads stay at `0 V` until the handshake passes | ENR-19, MON-16 |
| proposed: tamper, rollback and revocation on hardware | FW-1, FW-2, FW-3 (Section 9) |

## 9 · Proposed new gates

| Gate | The test | The pass condition |
|---|---|---|
| **FW-1** | flip one bit in each blob of a real image set | the part is held off, the chunk is named, the repair restores it |
| **FW-2** | replay every older signed release after a commit | each is refused at M4 or B3 |
| **FW-3** | revoke the installed release on a test chain | `UPDATE_REQUIRED` within one finality proof, and the update installs |
