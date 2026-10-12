#!/usr/bin/env python3
"""Independent golden vectors for the U7 mirrors of the Budlum hashes.

Each function is written from the Budlum tree source, not from the Rust in
fw/u7, so a match proves the two readings agree. Run: python3 vectors.py
The Rust test `golden_vectors_match_python` pins the printed values.
"""
import hashlib, struct

def le64(v): return struct.pack('<Q', v)
def le128(v): return v.to_bytes(16, 'little')

def hash_fields_bytes(fields):  # src/core/hash.rs:13-20
    h = hashlib.sha256()
    for f in fields:
        h.update(le64(len(f))); h.update(f)
    return h.digest()

def presence_tagged(root):  # src/core/hash.rs:29-37
    return b'\x00' * 33 if root is None else b'\x01' + root

def header_hash(index, ts, prev, producer, chain_id, state_root, tx_root, evidence,
                nonce, epoch, slot, vrf_out, vrf_proof, set_hash, storage_root, shards_root):
    # src/core/block.rs:84-149
    fields = [b'BDLM_BLOCK_V4', le64(index), le128(ts), prev.hex().encode(), tx_root.hex().encode(),
              le64(nonce), producer or b'', evidence or b'', le64(chain_id), state_root.hex().encode(),
              le64(epoch), le64(slot), vrf_out, vrf_proof, set_hash.hex().encode(), presence_tagged(storage_root)]
    if shards_root is not None:
        fields.append(shards_root)
    return hash_fields_bytes(fields)

def lp(b): return le64(len(b)) + b

def snapshot_hash(vals):  # src/chain/finality.rs:52-73
    h = hashlib.sha3_256()
    for addr, stake, bls, pop, pq in sorted(vals, key=lambda v: v[0]):
        h.update(addr); h.update(le64(stake)); h.update(lp(bls) + lp(pop) + lp(pq))
    return h.digest()

def consensus_set_hash(chain_id, vals):  # src/core/account.rs:990-1025
    h = hashlib.sha3_256()
    h.update(b'BDLM_CONSENSUS_VALIDATOR_SET_V1'); h.update(le64(chain_id)); h.update(le64(len(vals)))
    for addr, stake, vrf, bls, pop, pq in sorted(vals, key=lambda v: v[0]):
        h.update(addr); h.update(le64(stake)); h.update(lp(vrf) + lp(bls) + lp(pop) + lp(pq))
    return h.digest()

def merkle_root(leaves):  # src/consensus/merkle_tree.rs:103-165
    if not leaves: return b'\x00' * 32
    layer = list(leaves)
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            if i + 1 < len(layer):
                nxt.append(hashlib.sha3_256(layer[i] + layer[i + 1]).digest())
            else:
                nxt.append(hashlib.sha3_256(b'BDLM_MERKLE_ODD_PROMOTE_V1' + layer[i]).digest())
        layer = nxt
    return layer[0]

def wallet_address(pk):  # src/crypto/primitives.rs:895-914
    return hashlib.sha3_256(b'BUDLUM_ADDRESS_V2' + pk).digest()

def checkpoint_msg(epoch, height, hsh):  # src/chain/finality.rs:257-265
    return b'BUDLUM_PRECOMMIT' + b'BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_POP_' + le64(epoch) + le64(height) + hsh.hex().encode()

if __name__ == '__main__':
    b = lambda n, v: bytes([v]) * n
    hh = header_hash(20, 1_700_000_000_000, b(32, 1), b(32, 2), 1337, b(32, 3), b(32, 4), None,
                     7, 2, 20, b(32, 5), b(64, 6), b(32, 7), None, None)
    hh2 = header_hash(21, 5, b(32, 9), None, 1337, b(32, 3), b(32, 4), b(8, 0),
                      0, 2, 21, b'', b'', b(32, 7), b(32, 0), b(32, 8))
    vals = [(b(32, 0x22), 500, b(96, 1), b(48, 2), b(1952, 3)), (b(32, 0x11), 300, b(96, 4), b(48, 5), b(1952, 6))]
    cvals = [(v[0], v[1], b(32, 9)) + v[2:] for v in vals]
    leaves = [bytes([i]) * 32 for i in range(5)]
    print('header_a       ', hh.hex())
    print('header_b       ', hh2.hex())
    print('snapshot_hash  ', snapshot_hash(vals).hex())
    print('consensus_hash ', consensus_set_hash(1337, cvals).hex())
    print('merkle_5       ', merkle_root(leaves).hex())
    print('wallet_addr    ', wallet_address(b(2592, 0xab)).hex())
    print('checkpoint_msg ', hashlib.sha256(checkpoint_msg(3, 30, b(32, 0xcd))).hexdigest())
