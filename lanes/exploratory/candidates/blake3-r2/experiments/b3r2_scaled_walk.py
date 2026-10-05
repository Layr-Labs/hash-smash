"""Scaled end-to-end run of the blake3-r2 salted distinguished-point rho search.

Stdlib only. Organizer mode (default): read one JSON request on stdin and write
one JSON result. Each organizer trial runs Steps 1-6 of proof.md Section 2 once,
with the parameters scaled down as follows (proof.md Section 5):

  point x: 16 bits, two bits in each of the eight walk lanes (N_t = 2^16);
  message M(x): word j = (C_j with its low two bits replaced by bits 2j..2j+1
      of x) for j = 0..7, and word 8 + j = S_j (salt), little-endian;
      C_0..C_7 and S_0..S_7 are fresh per-trial coins;
  f(x): bits 2j..2j+1 of f(x) are the low two bits of digest lane o[j];
  distinguished point: the two bits taken from lane 0 are zero (theta = 1/4);
  k' = 2^8 = sqrt(N_t), g = 2^5, gap bound 2g = 2^6, k = k' + g, D_max = 2^9.

A returned pair (M(p), M(q)) satisfies, when the trial succeeds, that the two
messages differ and their complete 2-round BLAKE3 digests agree on the low two
bits of every digest lane, i.e. on mask 03000000 repeated eight times. The
organizer recomputes this for every returned pair. A failed trial returns two
nulls. Observations are informational only.

Model mode (local, not used by the organizer): `python3 FILE --model TRIALS SEED`
runs the identical attempt() on a lazily sampled uniformly random function on
2^16 points and prints the success frequency, which is the random-function
prediction this experiment is compared with.
"""

import hashlib
import json
import struct
import sys

MASK32 = 0xFFFFFFFF
BITS = 2                      # bits of the point per walk lane
LANE_LOW = (1 << BITS) - 1
N_POINTS = 1 << (8 * BITS)    # 2^16
K_PRIME = 1 << 8              # sqrt(N_POINTS)
G_WIN = 1 << 5                # theta * g = 8
GAP = 2 * G_WIN
K_WALK = K_PRIME + G_WIN
D_MAX = 1 << 9                # never binding here: at most K_WALK + 1 records


def g(a, b, c, d, x, y):
    a = (a + b + x) & MASK32; d ^= a; d = ((d >> 16) | (d << 16)) & MASK32
    c = (c + d) & MASK32; b ^= c; b = ((b >> 12) | (b << 20)) & MASK32
    a = (a + b + y) & MASK32; d ^= a; d = ((d >> 8) | (d << 24)) & MASK32
    c = (c + d) & MASK32; b ^= c; b = ((b >> 7) | (b << 25)) & MASK32
    return a, b, c, d


def compress2(m):
    """Digest lanes o[0..7] of the 2-round root compression of one 64-byte block
    (IV chaining value, counter 0, block length 64, flags 11)."""
    v0, v1, v2, v3 = 0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A
    v4, v5, v6, v7 = 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
    v8, v9, v10, v11 = 0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A
    v12, v13, v14, v15 = 0, 0, 64, 11
    for _ in (0, 1):
        v0, v4, v8, v12 = g(v0, v4, v8, v12, m[0], m[1])
        v1, v5, v9, v13 = g(v1, v5, v9, v13, m[2], m[3])
        v2, v6, v10, v14 = g(v2, v6, v10, v14, m[4], m[5])
        v3, v7, v11, v15 = g(v3, v7, v11, v15, m[6], m[7])
        v0, v5, v10, v15 = g(v0, v5, v10, v15, m[8], m[9])
        v1, v6, v11, v12 = g(v1, v6, v11, v12, m[10], m[11])
        v2, v7, v8, v13 = g(v2, v7, v8, v13, m[12], m[13])
        v3, v4, v9, v14 = g(v3, v4, v9, v14, m[14], m[15])
        m = (m[2], m[6], m[3], m[10], m[7], m[0], m[4], m[13],
             m[1], m[11], m[12], m[5], m[9], m[14], m[15], m[8])
    return (v0 ^ v8, v1 ^ v9, v2 ^ v10, v3 ^ v11, v4 ^ v12, v5 ^ v13, v6 ^ v14, v7 ^ v15)


def coins(seed):
    """17 32-bit words from SHA-256(domain || seed || counter): C_0..C_7, S_0..S_7, start."""
    stream = b"".join(hashlib.sha256(b"b3r2-scaled-walk-v1" + seed + bytes([i])).digest() for i in range(3))
    words = struct.unpack("<24I", stream)
    return words[0:8], words[8:16], words[16] & (N_POINTS - 1)


def words_of(x, consts, salt):
    lanes = tuple((consts[j] & ~LANE_LOW & MASK32) | ((x >> (BITS * j)) & LANE_LOW) for j in range(8))
    return lanes + tuple(salt)


def make_map(consts, salt):
    def f(x):
        o = compress2(words_of(x, consts, salt))
        y = 0
        for j in range(8):
            y |= (o[j] & LANE_LOW) << (BITS * j)
        return y
    return f


def is_dp(x):
    return x & LANE_LOW == 0


def attempt(f, x0):
    """Steps 1-5 of proof.md Section 2 at the scaled parameters.
    Returns (code, p, q, records): code 0 success, otherwise a failure code."""
    # Step 1: walk of exactly K_WALK steps; record index 0 and every DP.
    records = [(x0, 0)]
    x = x0
    for i in range(1, K_WALK + 1):
        x = f(x)
        if is_dp(x):
            if len(records) >= D_MAX:
                return 7, None, None, len(records)
            records.append((x, i))
    # Step 2: stable sort by value (Python's sort is stable).
    by_value = sorted(records, key=lambda r: r[0])
    # Step 3: first revisit = candidate (first index of group, index) with smallest j.
    best = None
    group_first = None
    for t in range(len(by_value)):
        if t > 0 and by_value[t][0] == by_value[t - 1][0]:
            if best is None or by_value[t][1] < best[1]:
                best = (group_first, by_value[t][1])
        else:
            group_first = by_value[t][1]
    if best is None:
        return 1, None, None, len(records)
    i_star, j_star = best
    if i_star == 0:
        return 2, None, None, len(records)
    lam = j_star - i_star
    # Step 4: neighbours in index order (records is increasing in index).
    pos = {idx: n for n, (_, idx) in enumerate(records)}
    a_rec = records[pos[i_star] - 1]
    b_rec = records[pos[j_star] - 1]
    a, b = a_rec[1], b_rec[1]
    if i_star - a > GAP or j_star - b > GAP:
        return 3, None, None, len(records)
    # Step 5: relocate and lockstep.
    p, q = a_rec[0], b_rec[0]
    if b - lam > a:
        for _ in range(b - lam - a):
            p = f(p)
    else:
        for _ in range(a + lam - b):
            q = f(q)
    if p == q:
        return 4, None, None, len(records)
    for _ in range(GAP):
        fp, fq = f(p), f(q)
        if fp == fq:
            return 0, p, q, len(records)
        p, q = fp, fq
    return 5, None, None, len(records)


def trial(seed):
    consts, salt, x0 = coins(seed)
    f = make_map(consts, salt)
    code, p, q, nrec = attempt(f, x0)
    obs = {"failure_code": code, "records": nrec}
    if code != 0:
        return None, None, obs
    # Step 6: recompute both digests from the full messages and check.
    wp, wq = words_of(p, consts, salt), words_of(q, consts, salt)
    op, oq = compress2(wp), compress2(wq)
    if wp == wq or any((op[j] ^ oq[j]) & LANE_LOW for j in range(8)):
        obs["failure_code"] = 6
        return None, None, obs
    return struct.pack("<16I", *wp).hex(), struct.pack("<16I", *wq).hex(), obs


def model(trials, seed):
    import random
    rng = random.Random(seed)
    counts = {}
    for _ in range(trials):
        table = {}

        def f(x):
            y = table.get(x)
            if y is None:
                y = table[x] = rng.randrange(N_POINTS)
            return y
        code = attempt(f, rng.randrange(N_POINTS))[0]
        counts[code] = counts.get(code, 0) + 1
    print(json.dumps({"trials": trials, "seed": seed, "codes": counts,
                      "success": counts.get(0, 0) / trials}, sort_keys=True))


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--model":
        model(int(sys.argv[2]), int(sys.argv[3]))
        return
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"].get("kind") != "digest-xor-mask":
        raise ValueError("unexpected organizer event")
    rows = []
    for item in request["trials"]:
        first, second, obs = trial(bytes.fromhex(item["seed"]))
        rows.append({"trial": item["trial"], "message_a_hex": first, "message_b_hex": second,
                     "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
