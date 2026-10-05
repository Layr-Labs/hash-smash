"""Partial-eval Word-op meter + matched-scale masked birthday (python-message-pairs-v1).

Uses the same Word-accounting convention as scripts/reference_operation_costs.py
(every +,&,|,^,<<,>> on Word counts 1; _ror = shift+shift+OR+mask). Organizer
_g meters at 30. This program:

1. Implements the grouped m15 partial-eval body used by the claim.
2. Meters that body segment-by-segment (r1_finish..ff).
3. Checks digests against an inlined 2-round compress (same ops as
   verifier/blake3.py) so returned pairs are bit-exact.
4. Emits (untrusted) observations of the segment counts for judge visibility.

Checked event remains digest-xor-mask; the host recomputes digests and does not
credit observation op counts as attack cost. The score-critical cost claim is
the analytic ledger in proof.md; this experiment is linked evidence that the
252-op body is organizer-Word-faithful and digest-correct.
"""

from __future__ import annotations

import hashlib
import json
import operator
import struct
import sys

MASK = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
SCHEDULE = [
    (0, 4, 8, 12, 0, 1), (1, 5, 9, 13, 2, 3), (2, 6, 10, 14, 4, 5), (3, 7, 11, 15, 6, 7),
    (0, 5, 10, 15, 8, 9), (1, 6, 11, 12, 10, 11), (2, 7, 8, 13, 12, 13), (3, 4, 9, 14, 14, 15),
]
FLAGS = 1 | 2 | 8

# Expected organizer-faithful segment counts (FF xor-only).
EXPECTED = {
    "r1_finish": 15,
    "r2_col0_full": 30,
    "r2_col1_partial": 22,
    "r2_col2_partial": 27,
    "r2_col3_full": 30,
    "r2_diagonals": 120,
    "ff": 8,
    "total": 252,
}


class Word(int):
    operations = 0

    def _c(self, op, other=None):
        Word.operations += 1
        return Word(op(int(self)) if other is None else op(int(self), int(other)))

    __add__ = lambda s, o: s._c(operator.add, o)
    __and__ = lambda s, o: s._c(operator.and_, o)
    __or__ = lambda s, o: s._c(operator.or_, o)
    __xor__ = lambda s, o: s._c(operator.xor, o)
    __lshift__ = lambda s, o: s._c(operator.lshift, o)
    __rshift__ = lambda s, o: s._c(operator.rshift, o)


def _ror(v, n):
    return ((v >> n) | (v << (32 - n))) & Word(MASK)


def _g(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & Word(MASK)
    v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & Word(MASK)
    v[b] = _ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & Word(MASK)
    v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & Word(MASK)
    v[b] = _ror(v[b] ^ v[c], 7)


def _g_first(v, a, b, c, d, x):
    v[a] = (v[a] + v[b] + x) & Word(MASK)
    v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & Word(MASK)
    v[b] = _ror(v[b] ^ v[c], 12)


def _g_second(v, a, b, c, d, y):
    v[a] = (v[a] + v[b] + y) & Word(MASK)
    v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & Word(MASK)
    v[b] = _ror(v[b] ^ v[c], 7)


def _plain_ror(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK


def _plain_g(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & MASK
    v[d] = _plain_ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _plain_ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & MASK
    v[d] = _plain_ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _plain_ror(v[b] ^ v[c], 7)


def reference_digest(m014, m15):
    """Inlined 2-round root compress; bit-identical to verifier/blake3.py."""
    words = list(m014) + [m15]
    v = list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]
    m = list(words)
    for _ in range(2):
        for a, b, c, d, x, y in SCHEDULE:
            _plain_g(v, a, b, c, d, m[x], m[y])
        m = [m[i] for i in PERM]
    out = [(v[i] ^ v[i + 8]) & MASK for i in range(8)]
    return struct.pack("<8I", *out)


def group_setup(m014):
    m = [Word(x) for x in list(m014) + [0]]
    v = [Word(x) for x in list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]]
    for a, b, c, d, x, y in SCHEDULE[:7]:
        _g(v, a, b, c, d, m[x], m[y])
    a, b, c, d, x, y = SCHEDULE[7]
    _g_first(v, a, b, c, d, m[x])
    mp = [m[i] for i in PERM]
    a1 = (v[1] + v[5] + mp[2]) & Word(MASK)
    d1 = _ror(v[13] ^ a1, 16)
    a1c2 = (v[2] + v[6] + mp[4]) & Word(MASK)
    return v, (a1, d1, a1c2)


def digest_for_metered(m014, m15, mid, inv):
    segs = {}
    Word.operations = 0

    def mark(name, start):
        segs[name] = Word.operations - start

    v = [Word(int(x)) for x in mid]
    t = Word.operations
    _g_second(v, 3, 4, 9, 14, Word(m15))
    mark("r1_finish", t)

    m = [Word(x) for x in list(m014) + [m15]]
    mp = [m[i] for i in PERM]
    a1, d1, a1c2 = inv

    t = Word.operations
    _g(v, 0, 4, 8, 12, mp[0], mp[1])
    mark("r2_col0_full", t)

    t = Word.operations
    v[1], v[13] = Word(int(a1)), Word(int(d1))
    v[9] = (v[9] + v[13]) & Word(MASK)
    v[5] = _ror(v[5] ^ v[9], 12)
    _g_second(v, 1, 5, 9, 13, mp[3])
    mark("r2_col1_partial", t)

    t = Word.operations
    v[2] = Word(int(a1c2))
    v[14] = _ror(v[14] ^ v[2], 16)
    v[10] = (v[10] + v[14]) & Word(MASK)
    v[6] = _ror(v[6] ^ v[10], 12)
    _g_second(v, 2, 6, 10, 14, mp[5])
    mark("r2_col2_partial", t)

    t = Word.operations
    _g(v, 3, 7, 11, 15, mp[6], mp[7])
    mark("r2_col3_full", t)

    t = Word.operations
    for a, b, c, d, x, y in SCHEDULE[4:]:
        _g(v, a, b, c, d, mp[x], mp[y])
    mark("r2_diagonals", t)

    t = Word.operations
    out = [v[i] ^ v[i + 8] for i in range(8)]
    mark("ff", t)
    segs["total"] = Word.operations
    dig = struct.pack("<8I", *[int(x) & MASK for x in out])
    return dig, segs


def expand_prefixes(seed_hex, n_groups):
    raw = bytes.fromhex(seed_hex)
    out = []
    counter = 0
    while len(out) < n_groups:
        words = []
        while len(words) < 15:
            block = hashlib.sha256(raw + counter.to_bytes(4, "little")).digest()
            counter += 1
            words.extend(struct.unpack("<8I", block))
        out.append(words[:15])
    return out


def key_spread20(dig):
    o = struct.unpack("<8I", dig)
    return (o[0] & 0xFF) | ((o[1] & 0xFF) << 8) | ((o[2] & 0xF) << 16)


def message_bytes(m014, m15):
    return struct.pack("<16I", *(list(m014) + [m15]))


def run_trial(seed_hex):
    prefixes = expand_prefixes(seed_hex, 32)
    bags = {}
    meter_ok = 0
    meter_fail = 0
    ref_ok = 0
    ref_fail = 0
    last_segs = None
    inserts = 0
    for m014 in prefixes:
        mid, inv = group_setup(m014)
        for y in range(32):
            dig, segs = digest_for_metered(m014, y, mid, inv)
            last_segs = segs
            if segs == EXPECTED:
                meter_ok += 1
            else:
                meter_fail += 1
            ref = reference_digest(m014, y)
            if dig == ref:
                ref_ok += 1
            else:
                ref_fail += 1
            key = key_spread20(dig)
            msg = message_bytes(m014, y)
            inserts += 1
            if key in bags and bags[key] != msg:
                obs = {
                    "messages": inserts,
                    "body_ops_total": segs["total"],
                    "body_ops_segments": segs,
                    "expected_segments": EXPECTED,
                    "meter_ok": meter_ok,
                    "meter_fail": meter_fail,
                    "ref_ok": ref_ok,
                    "ref_fail": ref_fail,
                    "full_g_ops": 30,
                }
                return bags[key].hex(), msg.hex(), obs
            bags[key] = msg
    obs = {
        "messages": inserts,
        "body_ops_total": (last_segs or {}).get("total"),
        "body_ops_segments": last_segs,
        "expected_segments": EXPECTED,
        "meter_ok": meter_ok,
        "meter_fail": meter_fail,
        "ref_ok": ref_ok,
        "ref_fail": ref_fail,
        "full_g_ops": 30,
    }
    return None, None, obs


def main():
    request = json.load(sys.stdin)
    rows = []
    for trial in request["trials"]:
        a_hex, b_hex, obs = run_trial(trial["seed"])
        row = {
            "trial": trial["trial"],
            "message_a_hex": a_hex,
            "message_b_hex": b_hex,
            "observations": obs,
        }
        rows.append(row)
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
