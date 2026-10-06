"""Scaled end-to-end run of the seven-lane grouped birthday search.

Stdlib only. Organizer mode (default) reads one JSON request on stdin and writes
one JSON result. Each organizer trial runs the algorithm of proof.md Section 3
once, scaled to N_t = 2^10 messages (proof.md Section 7):

  b3r2-swar-spread:    32 groups x t = 0..31, key = mask on o0..o3, o5;
  b3r2-swar-single:     1 group  x t = 0..1023, key = mask on o0..o3, o5;
  b3r2-swar-fullword:  32 groups x t = 0..31, key = mask on all of o0..o7;
  b3r2-swar-keysub:    32 groups x t = 0..31, event = 20-bit mask on o0..o7,
                       key = its 16 bits inside o0..o3, o5 (a strict projection).

A group draws U0 (m0..m7) and U1 (m8..m14) from SHA-256 of (domain, seed, group
index); a message is (m0..m14, m15) with m15 = (t - S) mod 2^32, S = a3h + b4h
(proof.md Section 2), so t is the round-1 state word a3'.

Counted path. In the spread, single and keysub experiments every batch of seven messages is
executed by `run_batch`, an interpreter for the exact register program PROG_FULL
of proof.md Section 4 (298 instructions: 291 ALU instructions and 7 table steps,
on a file of 64 registers; it contains no other memory access). The packed T
advance (1 ALU operation) follows each batch. Each table step is `table_step`,
a literal transcript of proof.md Section 5 (sparse address = the key itself,
dense array growing down from TOP = 2^256 - 1, record = the dense address), over
a memory whose unwritten words are adversarial garbage: once a record exists,
about half of them hold the address of a genuinely written dense entry. The only
scaling step is that the key register is ANDed with the event mask restricted to
o0..o3, o5 before its table step (not part of the counted program); for spread
and single that restriction is the whole 20-bit event mask, for keysub it is 16
of the 20 bits, so key matches with differing event bits occur and exercise the
declined-MATCH path (dummy dense entries, the scaled analogue of F2'). Lanes of the last batch of a
scaled group beyond its last t are not tabled.

Evidence-only full mode (b3r2-swar-fullword): the readable packed body
`packed_body(full=True)` also performs the three skipped final b rotations; all
eight words are extracted lane by lane (never counted), and the sparse address is
2^257 + key (outside the machine; evidence only).

On a key match both messages are rebuilt from the stored group records and
re-hashed with the independent reference `compress2`; the pair is returned when
the messages differ and the masked digest bits agree; otherwise a dummy dense
entry is written and the run continues, as in proof.md Section 5. A failed trial
returns two nulls. Observations (untrusted): counted ALU operations per batch
(min, max), table-step operations (min, max), verifications, dummy entries,
stale pointers.

Local mode (not used by the organizer):
  python3 FILE --selftest BATCHES SEED
"""

import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
W = (1 << 256) - 1
B = 1 << 32
LANES = 7
STRIDE = 36
TOP = W                                  # dense entries: TOP, TOP-1, ... (proof.md Section 5)
GAP = 1 << 32                            # bit 32: set in every record/constant address, never in a key
NREG = 64
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
LAYOUT = {"b3r2-swar-spread": (32, 32, False, False), "b3r2-swar-single": (1, 1024, False, False),
          "b3r2-swar-fullword": (32, 32, True, False), "b3r2-swar-keysub": (32, 32, False, True)}
KEY_WORDS = (0, 1, 2, 3, 5)
Q = (1 << 32) // LANES                   # 613566756 full batches per group
TAIL = (1 << 32) - LANES * Q             # 4 lanes in the last batch


def slots(v, js=range(LANES)):
    return sum(v << (STRIDE * j) for j in js)


def LOW(k, js=range(LANES)):
    return slots((1 << k) - 1, js)


# ---- register file of the counted program (proof.md Section 4) ----------------
CONST_REGS = ("d14", "c9", "b4", "A0x", "d12", "c8", "s1", "d13h", "b5", "A1y",
              "a2h", "c10", "b6", "A2y", "B7x", "d15", "c11", "b7", "s7", "s8",
              "s9", "s10", "s11", "s12", "s13", "s15", "negS")          # r0..r26
ROT = (7, 8, 12, 16, 20, 24, 25)                                          # r27..r33: LOW_k
R_T, R_CC, R_BC7, R_ONE = 34, 35, 36, 37
EXTRACT_MASKS = (("W0", (0,)), ("W14", (1, 4)), ("W25", (2, 5)), ("W36", (3, 6)),
                 ("M012", (0, 1, 2)), ("W13", (1, 3)), ("W05", (0, 5)),
                 ("W246", (2, 4, 6)), ("M34", (3, 4)))                    # r38..r46
FIRST_FREE = 47                                                           # r47..r63 temporaries


def fixed_registers():
    """Program constants (installed once per run)."""
    reg = [0] * NREG
    for i, k in enumerate(ROT):
        reg[27 + i] = LOW(k)
    reg[R_BC7] = slots(7)
    reg[R_ONE] = 1
    for i, (_, js) in enumerate(EXTRACT_MASKS):
        reg[38 + i] = LOW(32, js)
    reg[R_CC] = TOP
    return reg


# The counted batch programs, as emitted by our scheduler/register allocator.
# Instruction "op d a b": r_d = r_a op r_b (op in xor/and/or/add); "shl/shr d a n":
# r_d = r_a shifted by the immediate n; "tstep k s w": one table step on key r_k
# with scratch registers r_s, r_w (lanes in order 0..6).
PROG_FULL = (
    "xor 47 0 34;shr 48 47 8;and 48 48 32;and 47 47 28;shl 47 47 24;or 47 48 47;add 48 1 "
    "47;xor 47 47 10;xor 49 2 48;add 48 48 7;shr 50 49 7;and 50 50 33;and 49 49 27;shl 49 "
    "49 25;or 49 50 49;add 50 3 49;xor 51 4 50;shr 52 51 16;and 52 52 30;and 51 51 30;shl "
    "51 51 16;or 51 52 51;add 52 5 51;xor 49 49 52;shr 53 49 12;and 53 53 31;and 49 49 "
    "29;shl 49 49 20;or 49 53 49;add 50 50 49;add 50 50 6;xor 51 51 50;shr 53 51 8;and 53 "
    "53 32;and 51 51 28;shl 51 51 24;or 51 53 51;add 52 52 51;xor 49 49 52;shr 53 49 "
    "7;and 53 53 33;and 49 49 27;shl 49 49 25;or 49 53 49;xor 53 8 48;shr 54 53 12;and 54 "
    "54 31;and 53 53 29;shl 53 53 20;or 53 54 53;add 54 9 53;xor 55 7 54;shr 56 55 8;and "
    "56 56 32;and 55 55 28;shl 55 55 24;or 55 56 55;add 48 48 55;xor 53 53 48;shr 56 53 "
    "7;and 56 56 33;and 53 53 27;shl 53 53 25;or 53 56 53;add 50 50 53;add 50 50 19;shr "
    "56 47 16;and 56 56 30;and 47 47 30;shl 47 47 16;or 47 56 47;add 56 11 47;xor 57 12 "
    "56;shr 58 57 12;and 58 58 31;and 57 57 29;shl 57 57 20;or 57 58 57;add 58 13 57;xor "
    "47 47 58;shr 59 47 8;and 59 59 32;and 47 47 28;shl 47 47 24;or 47 59 47;add 56 56 "
    "47;xor 57 57 56;shr 59 57 7;and 59 59 33;and 57 57 27;shl 57 57 25;or 57 59 57;add "
    "54 54 57;add 54 54 21;xor 51 51 54;add 59 34 14;xor 60 15 59;shr 61 60 16;and 61 61 "
    "30;and 60 60 30;shl 60 60 16;or 60 61 60;add 61 16 60;xor 62 17 61;shr 63 62 12;and "
    "63 63 31;and 62 62 29;shl 62 62 20;or 62 63 62;add 59 59 62;add 59 59 18;xor 60 60 "
    "59;add 59 59 49;add 59 59 34;add 59 59 26;xor 47 47 59;shr 63 60 8;and 63 63 32;and "
    "60 60 28;shl 60 60 24;or 60 63 60;add 61 61 60;xor 62 62 61;xor 60 60 50;shr 63 62 "
    "7;and 63 63 33;and 62 62 27;shl 62 62 25;or 62 63 62;add 58 58 62;add 58 58 23;xor "
    "55 55 58;shr 63 60 16;and 63 63 30;and 60 60 30;shl 60 60 16;or 60 63 60;add 56 56 "
    "60;xor 53 53 56;shr 63 53 12;and 63 63 31;and 53 53 29;shl 53 53 20;or 53 63 53;add "
    "50 50 53;add 50 50 20;xor 60 60 50;shr 63 60 8;and 63 63 32;and 60 60 28;shl 60 60 "
    "24;or 60 63 60;add 56 56 60;xor 53 53 56;shr 60 53 7;and 60 60 33;and 53 53 27;shl "
    "53 53 25;or 53 60 53;shr 60 51 16;and 60 60 30;and 51 51 30;shl 51 51 16;or 51 60 "
    "51;add 60 61 51;xor 57 57 60;shr 61 57 12;and 61 61 31;and 57 57 29;shl 57 57 20;or "
    "57 61 57;add 54 54 57;add 54 54 22;xor 51 51 54;shr 57 51 8;and 57 57 32;and 51 51 "
    "28;shl 51 51 24;or 51 57 51;add 51 60 51;shr 57 55 16;and 57 57 30;and 55 55 30;shl "
    "55 55 16;or 55 57 55;add 52 52 55;xor 57 62 52;shr 60 57 12;and 60 60 31;and 57 57 "
    "29;shl 57 57 20;or 57 60 57;add 57 58 57;add 57 57 24;xor 55 55 57;xor 56 57 56;shr "
    "57 55 8;and 57 57 32;and 55 55 28;shl 55 55 24;or 55 57 55;add 52 52 55;xor 50 50 "
    "52;xor 52 53 55;shr 53 47 16;and 53 53 30;and 47 47 30;shl 47 47 16;or 47 53 47;add "
    "48 48 47;xor 49 49 48;shr 53 49 12;and 53 53 31;and 49 49 29;shl 49 49 20;or 49 53 "
    "49;add 49 59 49;add 49 49 25;xor 47 47 49;xor 49 49 51;shr 51 47 8;and 51 51 32;and "
    "47 47 28;shl 47 47 24;or 47 51 47;add 47 48 47;xor 47 54 47;and 48 50 38;and 51 47 "
    "38;shl 51 51 36;or 48 48 51;and 51 56 38;shl 51 51 72;or 48 48 51;and 51 50 39;shr "
    "51 51 36;and 53 47 39;or 51 51 53;and 53 56 39;shl 53 53 36;or 51 51 53;and 53 51 "
    "42;shr 51 51 108;and 54 50 40;shr 54 54 72;and 50 50 41;shr 50 50 72;and 55 47 "
    "40;shr 55 55 36;or 54 54 55;and 47 47 41;shr 47 47 36;or 47 50 47;and 50 56 40;or 50 "
    "54 50;and 54 56 41;or 47 47 54;and 54 50 42;shr 50 50 108;shr 55 47 36;and 55 55 "
    "42;shr 47 47 144;and 56 49 43;and 57 52 43;shl 57 57 36;or 56 56 57;shl 57 56 72;and "
    "57 57 46;or 53 53 57;and 56 56 46;or 55 55 56;and 56 49 44;and 49 49 45;shr 49 49 "
    "36;and 57 52 44;shl 57 57 36;or 56 56 57;and 52 52 45;or 49 49 52;shl 52 56 108;or "
    "48 48 52;tstep 48 52 57;tstep 53 48 52;shr 48 56 72;or 48 50 48;shl 50 49 72;and 50 "
    "50 46;or 50 54 50;tstep 50 52 53;tstep 55 50 52;and 50 49 46;or 50 51 50;tstep 50 51 "
    "52;tstep 48 50 51;shr 48 49 72;and 48 48 46;or 47 47 48;tstep 47 48 49 ")
PROG_TAIL = (
    "xor 47 0 34;shr 48 47 8;and 48 48 32;and 47 47 28;shl 47 47 24;or 47 48 47;add 48 1 "
    "47;xor 47 47 10;xor 49 2 48;add 48 48 7;shr 50 49 7;and 50 50 33;and 49 49 27;shl 49 "
    "49 25;or 49 50 49;add 50 3 49;xor 51 4 50;shr 52 51 16;and 52 52 30;and 51 51 30;shl "
    "51 51 16;or 51 52 51;add 52 5 51;xor 49 49 52;shr 53 49 12;and 53 53 31;and 49 49 "
    "29;shl 49 49 20;or 49 53 49;add 50 50 49;add 50 50 6;xor 51 51 50;shr 53 51 8;and 53 "
    "53 32;and 51 51 28;shl 51 51 24;or 51 53 51;add 52 52 51;xor 49 49 52;shr 53 49 "
    "7;and 53 53 33;and 49 49 27;shl 49 49 25;or 49 53 49;xor 53 8 48;shr 54 53 12;and 54 "
    "54 31;and 53 53 29;shl 53 53 20;or 53 54 53;add 54 9 53;xor 55 7 54;shr 56 55 8;and "
    "56 56 32;and 55 55 28;shl 55 55 24;or 55 56 55;add 48 48 55;xor 53 53 48;shr 56 53 "
    "7;and 56 56 33;and 53 53 27;shl 53 53 25;or 53 56 53;add 50 50 53;add 50 50 19;shr "
    "56 47 16;and 56 56 30;and 47 47 30;shl 47 47 16;or 47 56 47;add 56 11 47;xor 57 12 "
    "56;shr 58 57 12;and 58 58 31;and 57 57 29;shl 57 57 20;or 57 58 57;add 58 13 57;xor "
    "47 47 58;shr 59 47 8;and 59 59 32;and 47 47 28;shl 47 47 24;or 47 59 47;add 56 56 "
    "47;xor 57 57 56;shr 59 57 7;and 59 59 33;and 57 57 27;shl 57 57 25;or 57 59 57;add "
    "54 54 57;add 54 54 21;xor 51 51 54;add 59 34 14;xor 60 15 59;shr 61 60 16;and 61 61 "
    "30;and 60 60 30;shl 60 60 16;or 60 61 60;add 61 16 60;xor 62 17 61;shr 63 62 12;and "
    "63 63 31;and 62 62 29;shl 62 62 20;or 62 63 62;add 59 59 62;add 59 59 18;xor 60 60 "
    "59;add 59 59 49;add 59 59 34;add 59 59 26;xor 47 47 59;shr 63 60 8;and 63 63 32;and "
    "60 60 28;shl 60 60 24;or 60 63 60;add 61 61 60;xor 62 62 61;xor 60 60 50;shr 63 62 "
    "7;and 63 63 33;and 62 62 27;shl 62 62 25;or 62 63 62;add 58 58 62;add 58 58 23;xor "
    "55 55 58;shr 63 60 16;and 63 63 30;and 60 60 30;shl 60 60 16;or 60 63 60;add 56 56 "
    "60;xor 53 53 56;shr 63 53 12;and 63 63 31;and 53 53 29;shl 53 53 20;or 53 63 53;add "
    "50 50 53;add 50 50 20;xor 60 60 50;shr 63 60 8;and 63 63 32;and 60 60 28;shl 60 60 "
    "24;or 60 63 60;add 56 56 60;xor 53 53 56;shr 60 53 7;and 60 60 33;and 53 53 27;shl "
    "53 53 25;or 53 60 53;shr 60 51 16;and 60 60 30;and 51 51 30;shl 51 51 16;or 51 60 "
    "51;add 60 61 51;xor 57 57 60;shr 61 57 12;and 61 61 31;and 57 57 29;shl 57 57 20;or "
    "57 61 57;add 54 54 57;add 54 54 22;xor 51 51 54;shr 57 51 8;and 57 57 32;and 51 51 "
    "28;shl 51 51 24;or 51 57 51;add 51 60 51;shr 57 55 16;and 57 57 30;and 55 55 30;shl "
    "55 55 16;or 55 57 55;add 52 52 55;xor 57 62 52;shr 60 57 12;and 60 60 31;and 57 57 "
    "29;shl 57 57 20;or 57 60 57;add 57 58 57;add 57 57 24;xor 55 55 57;xor 56 57 56;shr "
    "57 55 8;and 57 57 32;and 55 55 28;shl 55 55 24;or 55 57 55;add 52 52 55;xor 50 50 "
    "52;xor 52 53 55;shr 53 47 16;and 53 53 30;and 47 47 30;shl 47 47 16;or 47 53 47;add "
    "48 48 47;xor 49 49 48;shr 53 49 12;and 53 53 31;and 49 49 29;shl 49 49 20;or 49 53 "
    "49;add 49 59 49;add 49 49 25;xor 47 47 49;xor 49 49 51;shr 51 47 8;and 51 51 32;and "
    "47 47 28;shl 47 47 24;or 47 51 47;add 47 48 47;xor 47 54 47;and 48 50 38;and 51 47 "
    "38;shl 51 51 36;or 48 48 51;and 51 56 38;shl 51 51 72;or 48 48 51;and 51 50 39;shr "
    "51 51 36;and 53 47 39;or 51 51 53;and 53 56 39;shl 53 53 36;or 51 51 53;and 51 51 "
    "42;and 53 50 40;shr 53 53 72;and 50 50 41;shr 50 50 72;and 54 47 40;shr 54 54 36;or "
    "53 53 54;and 47 47 41;shr 47 47 36;or 47 50 47;and 50 56 40;or 50 53 50;and 50 50 "
    "42;and 53 56 41;or 47 47 53;shr 47 47 36;and 47 47 42;and 53 49 43;and 54 52 43;shl "
    "54 54 36;or 53 53 54;shl 54 53 72;and 54 54 46;or 51 51 54;and 53 53 46;or 47 47 "
    "53;and 53 49 44;and 49 49 45;shr 49 49 36;and 54 52 44;shl 54 54 36;or 53 53 54;shl "
    "53 53 108;or 48 48 53;tstep 48 53 54;tstep 51 48 53;and 48 52 45;or 48 49 48;shl 48 "
    "48 72;and 48 48 46;or 48 50 48;tstep 48 49 50;tstep 47 48 49 ")


def parse(text):
    prog = []
    for line in text.split(";"):
        p = line.split()
        prog.append((p[0],) + tuple(int(x) for x in p[1:]))
    return prog


def ror(z, r):
    return ((z >> r) | (z << (32 - r))) & M


def g(a, b, c, d, x, y):
    a = (a + b + x) & M; d = ror(d ^ a, 16); c = (c + d) & M; b = ror(b ^ c, 12)
    a = (a + b + y) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    return a, b, c, d


def compress2(m):
    """Independent reference: digest words o0..o7 of the 2-round root compression
    of one 64-byte block (IV chaining value, counter 0, length 64, flags 11)."""
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    for _ in (0, 1):
        for (a, b, c, d), i in zip(((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
                                    (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)),
                                   range(0, 16, 2)):
            v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], m[i], m[i + 1])
        m = [m[i] for i in PERM]
    return [v[i] ^ v[i + 8] for i in range(8)]


def unpack(U0, U1):
    return [(U0 >> (32 * i)) & M for i in range(8)] + [(U1 >> (32 * i)) & M for i in range(7)]


def setup(m):
    """Group constants (proof.md Section 2) from m0..m14."""
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    calls = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
             (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13))
    for (a, b, c, d), i in zip(calls, range(0, 14, 2)):
        v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], m[i], m[i + 1])
    a3h = (v[3] + v[4] + m[14]) & M
    d14 = ror(v[14] ^ a3h, 16)
    c9 = (v[9] + d14) & M
    b4 = ror(v[4] ^ c9, 12)
    S = (a3h + b4) & M
    s = [m[i] if i != 15 else None for i in PERM]
    a1h = (v[1] + v[5] + s[2]) & M
    a2h = (v[2] + v[6] + s[4]) & M
    return {
        "S": S, "negS": (-S) & M, "d14": d14, "c9": c9, "b4": b4,
        "A0x": (v[0] + s[0]) & M, "d12": v[12], "c8": v[8], "s1": s[1],
        "d13h": ror(v[13] ^ a1h, 16), "b5": v[5], "A1y": (a1h + s[3]) & M,
        "a2h": a2h, "c10": v[10], "b6": v[6], "A2y": (a2h + s[5]) & M,
        "B7x": (v[7] + s[6]) & M, "d15": v[15], "c11": v[11], "b7": v[7], "s7": s[7],
        "s8": s[8], "s9": s[9], "s10": s[10], "s11": s[11], "s12": s[12], "s13": s[13], "s15": s[15],
    }


def load_group(reg, K):
    """Broadcast group constants into r0..r26 (group setup) and set T = (0..6)."""
    for i, n in enumerate(CONST_REGS):
        reg[i] = slots(K[n])
    reg[R_T] = sum(j << (STRIDE * j) for j in range(LANES))


# ---- readable packed body and extraction (cross-checks; full mode) -------------
def pror(z, r):
    """((z >> r) & LOW_{32-r}) | ((z & LOW_r) << (32 - r)): exact 32-bit rotation of
    every slot whose value is below 2^36 (guard bits discarded); 5 operations."""
    return ((z >> r) & LOW(32 - r)) | ((z & LOW(r)) << (32 - r))


def packed_body(K, T, full=False):
    """tekkac's seven-lane delayed-reduction body (227 operations), our rotation form."""
    z = K["d14"] ^ T; d14 = pror(z, 8); c9 = K["c9"] + d14; z = K["b4"] ^ c9; b4 = pror(z, 7)
    a0 = K["A0x"] + b4
    z = K["d12"] ^ a0; d12 = pror(z, 16); c8 = K["c8"] + d12; z = b4 ^ c8; b4 = pror(z, 12)
    a0 = a0 + b4 + K["s1"]
    z = d12 ^ a0; d12 = pror(z, 8); c8 = c8 + d12; z = b4 ^ c8; b4 = pror(z, 7)
    c9 = c9 + K["d13h"]; z = K["b5"] ^ c9; b5 = pror(z, 12)
    a1 = K["A1y"] + b5
    z = K["d13h"] ^ a1; d13 = pror(z, 8); c9 = c9 + d13; z = b5 ^ c9; b5 = pror(z, 7)
    z = d14 ^ K["a2h"]; d14 = pror(z, 16); c10 = K["c10"] + d14; z = K["b6"] ^ c10; b6 = pror(z, 12)
    a2 = K["A2y"] + b6
    z = d14 ^ a2; d14 = pror(z, 8); c10 = c10 + d14; z = b6 ^ c10; b6 = pror(z, 7)
    a3 = T + K["B7x"]
    z = K["d15"] ^ a3; d15 = pror(z, 16); c11 = K["c11"] + d15; z = K["b7"] ^ c11; b7 = pror(z, 12)
    a3 = a3 + b7 + K["s7"]
    z = d15 ^ a3; d15 = pror(z, 8); c11 = c11 + d15; z = b7 ^ c11; b7 = pror(z, 7)
    a0 = a0 + b5 + K["s8"]; z = d15 ^ a0; d15 = pror(z, 16); c10 = c10 + d15; z = b5 ^ c10; b5 = pror(z, 12)
    a0 = a0 + b5 + K["s9"]; z = d15 ^ a0; d15 = pror(z, 8); c10 = c10 + d15; z = b5 ^ c10; b5 = pror(z, 7)
    a1 = a1 + b6 + K["s10"]; z = d12 ^ a1; d12 = pror(z, 16); c11 = c11 + d12; z = b6 ^ c11; b6 = pror(z, 12)
    a1 = a1 + b6 + K["s11"]; z = d12 ^ a1; d12 = pror(z, 8); c11 = c11 + d12
    a2 = a2 + b7 + K["s12"]; z = d13 ^ a2; d13 = pror(z, 16); c8 = c8 + d13; z = b7 ^ c8; b7 = pror(z, 12)
    a2 = a2 + b7 + K["s13"]; z = d13 ^ a2; d13 = pror(z, 8); c8 = c8 + d13
    a3 = a3 + b4 + T + K["negS"]; z = d14 ^ a3; d14 = pror(z, 16); c9 = c9 + d14; z = b4 ^ c9; b4 = pror(z, 12)
    a3 = a3 + b4 + K["s15"]; z = d14 ^ a3; d14 = pror(z, 8); c9 = c9 + d14
    if not full:
        return a0 ^ c8, a1 ^ c9, a2 ^ c10, a3 ^ c11, b5 ^ d13
    b4 = pror(b4 ^ c9, 7); b6 = pror(b6 ^ c11, 7); b7 = pror(b7 ^ c8, 7)
    return (a0 ^ c8, a1 ^ c9, a2 ^ c10, a3 ^ c11, b4 ^ d12, b5 ^ d13, b6 ^ d14, b7 ^ d15)


# Interleaved extraction (proof.md Section 4): for key-slot set S and lane group G,
# the word OR_{k in S} ((o_k & W_G) shifted by k - delta slots) holds lane j's key
# slot k at word slot j - delta + k; one shift by delta - j slots (and, where other
# lanes' fields would land in slots 0..7, an AND with M_S) moves it into place.
DESIGN = (((0, 1, 2), (((0,), 0), ((1, 4), 1), ((2, 5), 2), ((3, 6), 2))),
          ((3, 4), (((1, 3), 3), ((0, 5), 3), ((2, 4, 6), 4))))


def sh(x, n):
    """shift by n slots (left if n > 0); a zero shift is no instruction"""
    return x if n == 0 else (x << (STRIDE * n) if n > 0 else x >> (-STRIDE * n))


def extract_keys(o, mask):
    """Seven gapped keys o0 | o1<<36 | o2<<72 | o3<<108 | o5<<144 from the five
    packed outputs o = (o0, o1, o2, o3, o5); mask(name) gives the mask words.
    64 operations."""
    parts = {j: [] for j in range(LANES)}
    for S, words in DESIGN:
        for G, delta in words:
            Wg = mask("W" + "".join(map(str, G)))
            w = None
            for k in S:
                v = sh(o[k] & Wg, k - delta)
                w = v if w is None else w | v
            for j in G:
                x = sh(w, delta - j)
                if any(0 <= jj - delta + k + delta - j <= 7 for jj in G if jj != j for k in S):
                    x = x & mask("M" + "".join(map(str, S)))
                parts[j].append(x)
    keys = []
    for j in range(LANES):
        k = parts[j][0]
        for x in parts[j][1:]:
            k = k | x
        keys.append(k)
    return keys


MASKS = {n: LOW(32, js) for n, js in EXTRACT_MASKS}


def pack_key(d):
    return d[0] | d[1] << 36 | d[2] << 72 | d[3] << 108 | d[5] << 144


# ---- memory and table (proof.md Section 5) ------------------------------------------
class Memory:
    """Never-initialised memory. An unwritten word reads as seed-derived garbage;
    once a dense entry exists, about half of the unwritten words hold the address
    of a genuinely written dense entry (a stale pointer, address > CC)."""
    def __init__(self, seed):
        self.seed, self.cells, self.stale = seed, {}, 0

    def load(self, a, CC):
        if a in self.cells:
            return self.cells[a]
        h = hashlib.sha256(b"garbage" + self.seed + a.to_bytes(33, "little")).digest()
        x = int.from_bytes(h, "little")
        if CC < TOP and h[0] & 1:
            self.stale += 1
            return CC + 1 + x % (TOP - CC)
        if h[0] & 2:
            return CC - (x & 0xFFFFF)          # at or just below CC: never written
        return x

    def store(self, a, v):
        self.cells[a] = v


def table_step(mem, sa, key, CC):
    """Literal transcript of proof.md Section 5 with its operations counted.
    Returns (matched, w, CC, ops); on MATCH, CC is unchanged (the handler writes
    the dummy entry)."""
    w = mem.load(sa, CC); ops = 1               # load [K]
    ops += 2                                    # compare CC < w, branch
    if CC < w:
        q = mem.load(w, CC); ops += 1           # load [w]
        ops += 2                                # compare q == K, branch
        if q == key:
            return True, w, CC, ops             # MATCH entry: 6
    mem.store(sa, CC); ops += 1                 # store [K] <- CC
    mem.store(CC, key); ops += 1                # store [CC] <- K
    CC = CC - 1; ops += 1                       # CC = CC - ONE
    return False, w, CC, ops                    # 9 (both tests) or 6


def dummy_entry(mem, key, CC):
    """Declined MATCH (inside the charged handler): store [CC] <- K; CC -= 1."""
    mem.store(CC, key)
    return CC - 1


# ---- interpreter of the counted register program --------------------------------------
def run_batch(prog, reg, on_tstep):
    """Execute one batch program on the 64-register file; returns the number of
    ALU instructions executed. on_tstep(lane, key) performs the table step."""
    alu = 0
    lane = 0
    for ins in prog:
        op = ins[0]
        if op == "tstep":
            on_tstep(lane, reg[ins[1]])
            lane += 1
            continue
        d, a, b = ins[1], ins[2], ins[3]
        if op == "xor":
            reg[d] = reg[a] ^ reg[b]
        elif op == "and":
            reg[d] = reg[a] & reg[b]
        elif op == "or":
            reg[d] = reg[a] | reg[b]
        elif op == "add":
            reg[d] = (reg[a] + reg[b]) & W
        elif op == "shl":
            reg[d] = (reg[a] << b) & W
        elif op == "shr":
            reg[d] = reg[a] >> b
        else:
            raise ValueError(op)
        alu += 1
    return alu


def key_masks(mask_hex, project=False):
    """k5: the event mask restricted to the key words o0..o3, o5 in gapped key
    layout (None if the event has bits elsewhere, unless project is set);
    k8: the event mask in the full-mode layout; words: the event mask words."""
    words = struct.unpack("<8I", bytes.fromhex(mask_hex))
    k8 = sum(w << (32 * i) for i, w in enumerate(words))
    k5 = None if any(words[i] for i in (4, 6, 7)) and not project else \
        sum(words[w] << (36 * j) for j, w in enumerate(KEY_WORDS))
    return k5, k8, words


def group_words(seed, gi):
    h = hashlib.sha256(b"b3r2-grouped-v1" + seed + gi.to_bytes(4, "little")).digest()
    h += hashlib.sha256(b"b3r2-grouped-v1" + seed + gi.to_bytes(4, "little") + b"\x01").digest()
    w = struct.unpack("<16I", h)
    U0 = sum(w[i] << (32 * i) for i in range(8))
    U1 = sum(w[8 + i] << (32 * i) for i in range(7))
    return U0, U1


def rec_addr(g, k):
    return (g << 36) | GAP | k


def trial(seed, groups, per_group, full, k5, k8, wmask, prog):
    mem = Memory(seed)
    reg = fixed_registers()
    obs = {"verifications": 0, "dummy_entries": 0}
    alu_seen, tab_seen = set(), set()
    state = {"msgs": 0, "found": None}

    def verify(w, key, gi, m, Kc):
        """MATCH handler (proof.md Section 5): decode, rebuild, re-hash."""
        obs["verifications"] += 1
        i = TOP - w
        gz, tz = divmod(i, per_group)               # full scale: g = i >> 32, t = i & M
        mz = unpack(mem.load(rec_addr(gz, 1), 0), mem.load(rec_addr(gz, 2), 0)) + \
            [(tz - mem.load(rec_addr(gz, 3), 0)) & M]
        ix = TOP - reg[R_CC]
        mx = m + [((ix % per_group) + Kc["negS"]) & M]
        dz, dx = compress2(mz), compress2(mx)
        if mz != mx and all((dz[i] ^ dx[i]) & wmask[i] == 0 for i in range(8)):
            return mz, mx
        return None

    for gi in range(groups):
        if state["found"]:
            break
        U0, U1 = group_words(seed, gi)
        m = unpack(U0, U1)
        Kc = setup(m)
        mem.store(rec_addr(gi, 1), U0)
        mem.store(rec_addr(gi, 2), U1)
        mem.store(rec_addr(gi, 3), Kc["S"])
        load_group(reg, Kc)
        PK = {n: slots(v) for n, v in Kc.items() if n != "S"}
        for base in range(0, per_group, LANES):
            if state["found"]:
                break
            active = min(LANES, per_group - base)

            def on_tstep(lane, key, active=active):
                if lane >= active or state["found"]:
                    return
                key = key & kmask
                sa = key + (1 << 257) if full else key
                matched, w, CC, ops = table_step(mem, sa, key, reg[R_CC])
                tab_seen.add(ops)
                state["msgs"] += 1
                if matched:
                    res = verify(w, key, gi, m, Kc)
                    if res:
                        state["found"] = res
                        return
                    CC = dummy_entry(mem, key, CC)
                    obs["dummy_entries"] += 1
                reg[R_CC] = CC

            if full:
                kmask = k8
                o = packed_body(PK, reg[R_T], True)
                for j in range(LANES):
                    on_tstep(j, sum(((o[i] >> (STRIDE * j)) & M) << (32 * i) for i in range(8)))
            else:
                kmask = k5
                alu_seen.add(run_batch(prog, reg, on_tstep))
            reg[R_T] = (reg[R_T] + reg[R_BC7]) & W   # packed T advance (1 operation)
    if alu_seen:
        obs.update(batch_alu_ops_min=min(alu_seen), batch_alu_ops_max=max(alu_seen))
    obs.update(messages=state["msgs"], table_ops_min=min(tab_seen), table_ops_max=max(tab_seen),
               stale_garbage_pointers=mem.stale)
    if state["found"]:
        mz, mx = state["found"]
        return struct.pack("<16I", *mz).hex(), struct.pack("<16I", *mx).hex(), obs
    return None, None, obs


# ---- local self-test ---------------------------------------------------------------
class V:
    """Counting word: every operation with a V operand is counted once."""
    n = 0

    def __init__(self, x): self.x = x

    def _op(self, f, o):
        V.n += 1
        return V(f(self.x, o.x if isinstance(o, V) else o) & W)

    def __add__(self, o): return self._op(lambda a, b: a + b, o)
    __radd__ = __add__
    def __xor__(self, o): return self._op(lambda a, b: a ^ b, o)
    __rxor__ = __xor__
    def __and__(self, o): return self._op(lambda a, b: a & b, o)
    __rand__ = __and__
    def __or__(self, o): return self._op(lambda a, b: a | b, o)
    __ror__ = __or__
    def __rshift__(self, k): return self._op(lambda a, b: a >> b, k)
    def __lshift__(self, k): return self._op(lambda a, b: a << b, k)
    def __neg__(self): return self._op(lambda a, b: -a, 0)


def range_check(prog):
    """Static per-slot bound analysis of the shipped program (proof.md Lemma 2).
    bound[r] = strict upper bound of every slot 0..6 of r (bits 252..255 zero), or
    None when slots are not separated. Every ADD must have bounded inputs whose
    sum stays below 2^36; returns the largest ADD result bound in units of B."""
    bound = [None] * NREG
    for i in range(27):
        bound[i] = B                                    # broadcast 32-bit constants
    bound[R_T] = B                                      # T lanes < 2^32 (Lemma 2)
    for i, k in enumerate(ROT):
        bound[27 + i] = ("LOW", k)
    for i in range(len(EXTRACT_MASKS)):
        bound[38 + i] = ("MASK", 32)
    worst = 0
    for ins in prog:
        op = ins[0]
        if op == "tstep":
            continue
        d, a, b = ins[1], ins[2], ins[3]
        x, y = bound[a], bound[b] if op not in ("shl", "shr") else None
        if op == "add":
            assert isinstance(x, int) and isinstance(y, int), ins
            r = x + y - 1
            assert r <= 1 << 36, ins
            worst = max(worst, r)
            bound[d] = r
        elif op in ("xor", "or"):
            if isinstance(x, int) and isinstance(y, int):
                bound[d] = 1 << max((x - 1).bit_length(), (y - 1).bit_length())
            else:
                bound[d] = None
        elif op == "and":
            m = x if isinstance(x, tuple) else y if isinstance(y, tuple) else None
            if m is not None and m[0] == "LOW":
                bound[d] = 1 << m[1]
            elif m is not None:
                bound[d] = None                         # extraction: slot moves follow
            else:
                bound[d] = None
        elif op == "shl":
            bound[d] = (x << b) if isinstance(x, int) and x << b <= 1 << 36 and b < STRIDE else None
        elif op == "shr":
            bound[d] = None                             # neighbour bits enter; must be masked
        for r in (d,):
            pass
    return worst / B


def selftest(batches, seed):
    import random
    rng = random.Random(seed)
    full, tail = parse(PROG_FULL), parse(PROG_TAIL)
    regs_used = {r for p in (full, tail) for ins in p for r in
                 ((ins[1], ins[2]) if ins[0] in ("shl", "shr") else ins[1:4])}
    assert max(regs_used) < NREG and min(regs_used) >= 0
    out = {"prog_full_len": len(full), "prog_tail_len": len(tail),
           "registers_used_max": max(regs_used),
           "range_max_add_over_B": [round(range_check(full), 4), round(range_check(tail), 4)]}
    ok = 0
    alu_counts, v_counts = {}, {}
    for c in range(batches):
        m = [rng.getrandbits(32) for _ in range(15)]
        K = setup(m)
        reg = fixed_registers()
        load_group(reg, K)
        is_tail = c % 10 == 9
        t0 = LANES * Q if is_tail else LANES * rng.randrange(Q)
        nl = TAIL if is_tail else LANES
        T = sum(((t0 + j) & M) << (STRIDE * j) for j in range(LANES))
        reg[R_T] = T
        got = []
        alu = run_batch(tail if is_tail else full, reg, lambda lane, key: got.append(key))
        alu_counts[(is_tail, alu, len(got))] = alu_counts.get((is_tail, alu, len(got)), 0) + 1
        PK = {n: slots(v) for n, v in K.items() if n != "S"}
        V.n = 0
        o = packed_body({n: V(v) for n, v in PK.items()}, V(T))
        nb = V.n
        ks = extract_keys(o, lambda n: V(MASKS[n]))
        v_counts[(nb, V.n - nb)] = v_counts.get((nb, V.n - nb), 0) + 1
        fo = packed_body(PK, T, True)
        for j in range(nl):
            d = compress2(m + [((t0 + j) - K["S"]) & M])
            assert got[j] == pack_key(d) == ks[j].x, (c, j)
            assert [(fo[i] >> (STRIDE * j)) & M for i in range(8)] == d, (c, j)
            ok += 1
    out["batch_alu_ops"] = {"%s,%d,%d" % k: n for k, n in alu_counts.items()}
    out["readable_body_extract_ops"] = {"%d,%d" % k: n for k, n in v_counts.items()}
    out["keys_equal_reference"] = ok
    # group constants with counted message words
    V.n = 0
    m = [V(rng.getrandbits(32)) for _ in range(15)]
    setup(m)
    out["group_constant_ops"] = V.n
    # table semantics under adversarial garbage with 12-bit keys (frequent MATCHes)
    tc = {}
    for r in range(100):
        mem, CC, first = Memory(b"tbl" + r.to_bytes(4, "little")), TOP, {}
        for i in range(256):
            key = rng.getrandbits(12)
            matched, w, CC2, ops = table_step(mem, key, key, CC)
            path = "match" if matched else ("stale" if ops == 9 else "fresh")
            tc[(path, ops)] = tc.get((path, ops), 0) + 1
            assert matched == (key in first), "table semantics"
            if matched:
                assert TOP - w == first[key] and CC2 == CC
                CC2 = dummy_entry(mem, key, CC)
            else:
                first[key] = TOP - CC
            assert TOP - CC == i
            CC = CC2
    out["table_paths"] = {"%s,%d" % k: n for k, n in sorted(tc.items())}
    print(json.dumps(out, sort_keys=True))


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--selftest":
        selftest(int(sys.argv[2]), int(sys.argv[3]))
        return
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    event = request["event"]
    if event.get("kind") != "digest-xor-mask" or int(event["expected_hex"], 16) != 0:
        raise ValueError("unexpected organizer event")
    groups, per_group, full, project = LAYOUT[request["experiment_id"]]
    k5, k8, wmask = key_masks(event["mask_hex"], project)
    if not full and k5 is None:
        raise ValueError("counted-key experiments need a mask inside o0..o3, o5")
    if project and (k5 == 0 or not any(wmask[i] for i in (4, 6, 7))):
        raise ValueError("keysub needs event bits both inside and outside o0..o3, o5")
    prog = parse(PROG_FULL)
    rows = []
    for item in request["trials"]:
        first, second, obs = trial(bytes.fromhex(item["seed"]), groups, per_group, full, k5, k8, wmask, prog)
        rows.append({"trial": item["trial"], "message_a_hex": first, "message_b_hex": second,
                     "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
