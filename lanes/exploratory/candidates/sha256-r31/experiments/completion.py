# -*- coding: utf-8 -*-
"""Phase 3 (completion) of the two-block sha256-r31 attack, run on the published prefix.

Kind `python-message-pairs-v1`, event `full-collision`. For every organizer-supplied seed the
program keeps the published first block M0 and the published second-block words W0..W12 and
searches for new (W13, W14, W15) with the exact tests of the proof's completion section, then
returns the two resulting 128-byte messages M0||M1 and M0||M1'. It does NOT search for a first
block (Phases 1-2, the ~2^39-trial matching phase, are not run here).

Only the Python standard library is used. All randomness is derived deterministically from the
per-trial organizer seed, so two identical organizer requests produce byte-identical stdout
(the runner enforces this with a second execution).

CHANGES vs the PR-134 completion program (fixing judge finding
`lane_cryptanalysis/F2-completion-experiment-algorithm-mismatch`):
  1. FRESH OFFSETS PER CANDIDATE. PR-134 derived one (r13, r15) per trial and reused it across
     every (g, w14) candidate; the proof declares fresh offsets inside the per-candidate loop.
     Here `candidate_offsets(seed, j)` draws independent r13_j, r15_j for each candidate index j.
  2. GLOBAL TOTAL-INNER-ITERATION CAP. PR-134 had no global stop; capping only outer
     x-evaluations still structurally permits CAP13*CAP15 = 2^30 inner iterations. Here a single
     counter `iters` is incremented on EVERY inner iteration -- each outer x-evaluation AND each
     inner z-iteration -- across ALL candidates in one call, and hard-stops every loop the moment
     it reaches GLOBAL_PHASE3_CAP. So the TOTAL inner iterations per matched prefix (hence the
     per-call word-operation cost) is bounded by GLOBAL_PHASE3_CAP, matching the per-call budget
     and operation bound stated in proof.md Section 9. GLOBAL_PHASE3_CAP is identical here and in
     proof.md.
"""
import hashlib
import json
import sys

M = 0xFFFFFFFF
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

# ============================================================================================
# BEGIN ATTACK-SPECIFIC CONSTANTS (final; identical to the values stated in proof.md Sections 3-9)
# The completion experiment runs Phase 3 on the published prefix: M0 and the second-block words
# W0..W12 are the published two-block collision's words, and only (W13,W14,W15) are searched.
# CAP13, CAP15 and GLOBAL_PHASE3_CAP below are the exact caps quoted in proof.md Section 9.
# ============================================================================================
# Published first-block words M0 (16 x 32-bit, big-endian), and the two published second blocks
# M1 / M1P that collide after the full two-block sha256-r31 (W0..W12 fixed; W13..W15 searched).
M0 = [0x8ce3f805, 0x5c401aed, 0x579e5f7f, 0xbc3116cb, 0xca189b3c, 0xeb75f04c, 0x958f0a0e, 0x7760b082,
      0xdcd5027d, 0x32260ad6, 0x7b12b659, 0xeee66518, 0xad7f88dd, 0xf8ad20bb, 0x7ae40ffd, 0x21609249]
M1 = [0x9abdeb1b, 0x1f195f41, 0x5a7210c1, 0x55614f13, 0xa2269dd1, 0xbe888a61, 0x359257d4, 0xadf3737b,
      0x9f0484a6, 0xeb830a58, 0x66add94a, 0x9669232d, 0x45271fa5, 0xb8f69585, 0x428bbce3, 0x0703b904]
M1P = [0x9abdeb1b, 0x1f195f41, 0x5a7210c1, 0x55614f13, 0xa2269dd1, 0xbe887a67, 0x35b2dfc5, 0xfde32975,
       0xc70595a6, 0xeb838a5c, 0x66add94a, 0x9669232d, 0x45271fa5, 0xb8f69585, 0x428bbce3, 0x0703b904]
# Low-discrepancy (Weyl) increment used to walk the x and z search ranges deterministically.
WEYL = 0x9e3779b9
# s1 differential winning set G16 (the 64 w with s1(w + d16) - s1(w) == d18), enumerated as
# (hi << 28) | lo over these high nibbles and low residues.
G16_HI = range(16)
G16_LO = (0x31bbffc, 0x64bbffe, 0x9b3bffd, 0xce3bfff)
# Per-candidate local loop caps (number of x values and number of z values tried per candidate).
CAP13 = 1 << 18
CAP15 = 1 << 12
# GLOBAL Phase-3 budget per organizer seed: the total number of INNER ITERATIONS -- every
# outer x-evaluation AND every inner z-iteration -- across ALL candidates in one call, counted
# by the single global counter `iters` in search(). The search hard-stops every loop the moment
# the budget is reached, so the per-call work is bounded by GLOBAL_PHASE3_CAP inner iterations
# (NOT the structural product CAP13*CAP15). This matches the per-matched-prefix budget declared
# in proof.md Section 9. It is 2^16: the local Docker runner keeps the pathological all-fail
# 256-trial request well inside the 20 s sandbox budget at this cap, and the published prefix
# completes far below it.
GLOBAL_PHASE3_CAP = 1 << 16
# ============================================================================================
# END ATTACK-SPECIFIC CONSTANTS
# ============================================================================================


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def S0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def S1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def s0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def s1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def ch(e, f, g):
    return g ^ (e & (f ^ g))


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def trace(h, m):
    """31 steps from chaining value h; returns the output and the lists A[i+4], E[i+4], W[i]."""
    w = list(m)
    for t in range(16, 31):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & M)
    a, b, c, d, e, f, g, hh = h
    A = [d, c, b, a]
    E = [hh, g, f, e]
    for t in range(31):
        t1 = (hh + S1(e) + ch(e, f, g) + K[t] + w[t]) & M
        t2 = (S0(a) + maj(a, b, c)) & M
        hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & M, c, b, a, (t1 + t2) & M
        A.append(a)
        E.append(e)
    out = [(x + y) & M for x, y in zip(h, (a, b, c, d, e, f, g, hh))]
    return out, A, E, w


def s1_inverse_table():
    """Rows giving w14 from y = s1(w14) by GF(2) linear algebra (s1 is a linear map over GF(2))."""
    rows = []
    for i in range(32):
        mask = 0
        for j in range(32):
            if (s1(1 << j) >> i) & 1:
                mask |= 1 << j
        rows.append([mask, 1 << i])
    for c in range(32):
        p = c
        while not (rows[p][0] >> c) & 1:
            p += 1
        rows[c], rows[p] = rows[p], rows[c]
        for r in range(32):
            if r != c and (rows[r][0] >> c) & 1:
                rows[r][0] ^= rows[c][0]
                rows[r][1] ^= rows[c][1]
    return [row[1] for row in rows]


def candidate_offsets(seed_hex, j):
    """FRESH per-candidate offsets r13_j, r15_j, deterministic in the organizer seed and index j."""
    block = hashlib.sha256(bytes.fromhex(seed_hex) + j.to_bytes(4, "big")).digest()
    return int.from_bytes(block[0:4], "big"), int.from_bytes(block[4:8], "big")


def build_setup():
    """Derive the fixed completion data from the published prefix. Returns None if the published
    constants are not a self-consistent colliding configuration (so the experiment then reports
    only failed trials rather than crashing an organizer run)."""
    try:
        cv1 = trace(IV, M0)[0]
        out, A, E, W = trace(cv1, M1)
        outp, Ap, Ep, Wp = trace(cv1, M1P)
        if out != outp:
            return None
        a = lambda i: A[i + 4]
        e = lambda i: E[i + 4]
        ap = lambda i: Ap[i + 4]
        ep = lambda i: Ep[i + 4]
        d16 = (Wp[16] - W[16]) & M
        d18 = (Wp[18] - W[18]) & M
        x18 = (s1(Wp[18]) - s1(W[18])) & M
        da10 = (ap(10) - a(10)) & M
        inv = s1_inverse_table()
        c16 = (W[9] + s0(W[1]) + W[0]) & M
        c18 = (W[11] + s0(W[3]) + W[2]) & M
        g16 = [(hi << 28) | lo for hi in G16_HI for lo in G16_LO]
        if not all((s1((g + d16) & M) - s1(g)) & M == d18 for g in g16):
            return None
        good = []
        for g in g16:
            w18 = (s1(g) + c18) & M
            if (s1((w18 + d18) & M) - s1(w18)) & M == x18:
                y = (g - c16) & M
                w14 = 0
                for c in range(32):
                    w14 |= (bin(inv[c] & y).count("1") & 1) << c
                if s1(w14) != y:
                    return None
                good.append((g, w14))
        b13 = (a(9) + e(9) + S1(e(12)) + ch(e(12), e(11), e(10)) + K[13]) & M
        k14 = (a(10) + e(10) + K[14]) & M
        k14p = (ap(10) + ep(10) + K[14]) & M
        return {
            "good": good, "da10": da10, "d16": d16,
            "e11": e(11), "e12": e(12), "e11p": ep(11), "e12p": ep(12),
            "m14": e(12) ^ e(11), "m14p": ep(12) ^ ep(11),
            "a11": a(11), "a12": a(12), "b13": b13, "k14": k14, "k14p": k14p,
        }
    except Exception:
        return None


def search(seed_hex, S):
    """Capped, fresh-offset-per-candidate completion search. Returns (found, iters).

    `iters` is a SINGLE global counter incremented on EVERY inner iteration -- each outer
    x-evaluation AND each inner z-iteration -- and the search hard-stops every loop the moment
    `iters` reaches GLOBAL_PHASE3_CAP. So the total number of inner iterations per call (hence
    the per-call word-operation cost) is bounded by GLOBAL_PHASE3_CAP, not by the structural
    product CAP13*CAP15; this is the F5 fix (previously only outer x-evaluations were capped)."""
    good, da10, d16 = S["good"], S["da10"], S["d16"]
    e11, e12, e11p, e12p = S["e11"], S["e12"], S["e11p"], S["e12p"]
    m14, m14p, a11, a12 = S["m14"], S["m14p"], S["a11"], S["a12"]
    b13, k14, k14p = S["b13"], S["k14"], S["k14p"]
    iters = 0
    for j, (g, w14) in enumerate(good):
        if iters >= GLOBAL_PHASE3_CAP:
            break
        r13, r15 = candidate_offsets(seed_hex, j)  # FRESH offsets for this candidate
        base = (k14 + w14) & M
        basep = (k14p + w14) & M
        for i in range(CAP13):
            if iters >= GLOBAL_PHASE3_CAP:
                break
            iters += 1  # one inner iteration (x-evaluation), counted against the global budget
            x = (r13 + i * WEYL) & M
            c = e11 ^ (x & m14)
            cp = e11p ^ (x & m14p)
            if (basep + cp - base - c) & M != da10:
                continue
            sx = S1(x)
            y14 = (base + sx + c) & M
            y14p = (basep + sx + cp) & M
            x15 = (e11 + S1(y14) + ch(y14, x, e12)) & M
            if x15 != (e11p + S1(y14p) + ch(y14p, x, e12p)) & M:
                continue
            for k in range(CAP15):
                if iters >= GLOBAL_PHASE3_CAP:
                    break
                iters += 1  # one inner iteration (z-iteration), counted against the same budget
                z = (r15 + k * WEYL) & M
                y16 = (e12 + ch(z, y14, x)) & M
                if y16 != (e12p + ch(z, y14p, x) + d16) & M:
                    continue
                e16 = (a12 + y16 + S1(z) + K[16] + g) & M
                if ch(e16, z, y14) != ch(e16, z, y14p):
                    continue
                return ((x - b13) & M, w14, (z - a11 - x15 - K[15]) & M), iters
    return None, iters


def main():
    request = json.load(sys.stdin)
    S = build_setup()
    rows = []
    for item in request["trials"]:
        found = None
        iters = 0
        if S is not None:
            found, iters = search(item["seed"], S)
        row = {"trial": item["trial"], "message_a_hex": None, "message_b_hex": None,
               "observations": {"phase3_iters": iters,
                                "setup_ok": 1 if S is not None else 0}}
        if found is not None:
            ma = M0 + M1[:13] + list(found)
            mb = M0 + M1P[:13] + list(found)
            row["message_a_hex"] = b"".join(v.to_bytes(4, "big") for v in ma).hex()
            row["message_b_hex"] = b"".join(v.to_bytes(4, "big") for v in mb).hex()
        rows.append(row)
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"))


main()
