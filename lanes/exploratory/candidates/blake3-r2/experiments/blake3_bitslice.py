"""Bitsliced 2-round BLAKE3 (one 64-byte root chunk) over 256 messages per 256-bit word,
with an exact operation count.

Word i of the input holds bit i of 256 messages (message l lives in bit l of every word).
32-bit additions are ripple-carry full adders on bit words; rotations are renamings.
The program is compiled once as straight-line code for a 16-register 256-bit machine
(it uses 15 registers; the 16th holds the key write pointer of the surrounding loop):
  LD r, a / ST a, r            256-bit load / store at a fixed address
  XOR/AND/OR rd, ra, rb        bitwise ops
  NOT rd, ra                   bitwise complement
  SHL/SHR rd, ra, k            shift by a constant
Every instruction executed is one charged primitive. The interpreter below runs that
exact instruction list; nothing outside the list touches the state.

Without arguments the file speaks the HashSmash python-message-pairs-v1 protocol
(one JSON request on stdin, one JSON document on stdout). With --report it prints
the operation counts and checks a batch against an independent reference.
"""

import hashlib
import json
import sys

ROUNDS = 2
WORD = 256
REGISTERS = 16           # machine registers
PROGRAM_REGISTERS = 15   # the hash program's share; the 16th holds the key write pointer
ALL = (1 << WORD) - 1
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
SCHEDULE = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
FLAGS = 1 | 2 | 8          # CHUNK_START | CHUNK_END | ROOT
G_CALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
           (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))
M32 = 0xFFFFFFFF


# ----------------------------------------------------------------------------
# Reference: scalar BLAKE3 root compression of one 64-byte chunk, first 2 rounds.

def _rotr32(v, n):
    return ((v >> n) | (v << (32 - n))) & M32


def reference_blake3_r2(message):
    assert len(message) == 64
    m = [int.from_bytes(message[4 * j: 4 * j + 4], "little") for j in range(16)]
    v = list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]
    for r in range(ROUNDS):
        for k, (a, b, c, d) in enumerate(G_CALLS):
            x, y = m[2 * k], m[2 * k + 1]
            v[a] = (v[a] + v[b] + x) & M32
            v[d] = _rotr32(v[d] ^ v[a], 16)
            v[c] = (v[c] + v[d]) & M32
            v[b] = _rotr32(v[b] ^ v[c], 12)
            v[a] = (v[a] + v[b] + y) & M32
            v[d] = _rotr32(v[d] ^ v[a], 8)
            v[c] = (v[c] + v[d]) & M32
            v[b] = _rotr32(v[b] ^ v[c], 7)
        m = [m[i] for i in SCHEDULE]
    return b"".join((v[i] ^ v[i + 8]).to_bytes(4, "little") for i in range(8))


# ----------------------------------------------------------------------------
# Compiler: symbolic bits are (node, flip). node None is the constant 0, so
# (None, 1) is the all-ones word. The real word is stored(node) XOR (flip ? ALL : 0).
# Flips are compile-time facts; they cost nothing until a word must be produced.

class Graph:
    def __init__(self):
        self.ops = []          # node id -> (op, args...)
        self.memo = {}

    def node(self, op, *args):
        if op in ("XOR", "AND", "OR"):
            args = tuple(sorted(args))
        key = (op,) + tuple(args)
        hit = self.memo.get(key)
        if hit is None:
            hit = len(self.ops)
            self.ops.append(key)
            self.memo[key] = hit
        return hit


def bxor(g, u, v):
    (un, uf), (vn, vf) = u, v
    if un is None:
        return (vn, uf ^ vf)
    if vn is None:
        return (un, uf ^ vf)
    if un == vn:
        return (None, uf ^ vf)
    return (g.node("XOR", un, vn), uf ^ vf)



def _gate(g, u, v, kind):
    """kind AND or OR of two symbolic bits, choosing the stored polarity by De Morgan."""
    (un, uf), (vn, vf) = u, v
    is_and = kind == "AND"
    for p, q in ((u, v), (v, u)):
        if p[0] is None:
            if p[1] == (0 if is_and else 1):
                return p
            return q
    if un == vn:
        return u if uf == vf else (None, 0 if is_and else 1)
    if uf == vf:
        if uf == 0:
            return (g.node(kind, un, vn), 0)
        return (g.node("OR" if is_and else "AND", un, vn), 1)
    if uf == 1:                       # make u the operand with flip 0
        (un, uf), (vn, vf) = (vn, vf), (un, uf)
    return (g.node(kind, un, g.node("NOT", vn)), 0)


def band(g, u, v):
    return _gate(g, u, v, "AND")


def bor(g, u, v):
    return _gate(g, u, v, "OR")


def full_add(g, x, y, c, need_carry):
    """Sum bit and carry of x + y + c. Every gate is chosen so that no NOT is needed:
    with no constant operand the majority is ((q^p) & (r^p)) ^ p for a pivot p whose
    two partners carry equal flips (one always exists among three flips)."""
    vals = (x, y, c)
    consts = [v for v in vals if v[0] is None]
    others = [v for v in vals if v[0] is not None]
    s = bxor(g, bxor(g, x, y), c)
    if not need_carry:
        return s, None
    if len(consts) >= 2:
        if consts[0][1] == consts[1][1]:
            return s, consts[0]
        return s, (others[0] if others else consts[2])
    if len(consts) == 1:
        k = consts[0][1]
        p, q = others
        if p[1] == q[1]:
            return s, (band(g, p, q) if k == 0 else bor(g, p, q))
        t = bxor(g, p, q)                     # flip 1, already built for s
        if k == 0:                            # p & q = r & NOT(p ^ q), r the flip-0 operand
            nt = (t[0], t[1] ^ 1)
            r = p if p[1] == nt[1] else q
            return s, band(g, r, nt)
        r = p if p[1] == t[1] else q          # p | q = r | (p ^ q), r the flip-1 operand
        return s, bor(g, r, t)
    for p, q, r in ((c, x, y), (x, y, c), (y, x, c)):
        if q[1] == r[1]:
            break
    t1 = bxor(g, q, p)
    t2 = bxor(g, r, p)
    s = bxor(g, t1, r)
    return s, bxor(g, band(g, t1, t2), p)


def add(g, x, y):
    """Ripple-carry sum of two 32-bit words (lists of symbolic bits, bit 0 first) mod 2^32."""
    out, carry = [], (None, 0)
    for i in range(32):
        bit, carry = full_add(g, x[i], y[i], carry, i < 31)
        out.append(bit)
    return out


def xor_word(g, x, y):
    return [bxor(g, a, b) for a, b in zip(x, y)]


def rotr(x, n):
    return [x[(i + n) % 32] for i in range(32)]


def const_word(value):
    return [(None, value >> i & 1) for i in range(32)]


def compile_blake3(g, on_block=None):
    """Returns the 256 digest-bit values; calls on_block(j0, bits) per 8 output bits."""
    m = [[(g.node("IN", 32 * j + i), 0) for i in range(32)] for j in range(16)]
    v = [const_word(w) for w in IV] + [const_word(w) for w in IV[:4]] + \
        [const_word(0), const_word(0), const_word(64), const_word(FLAGS)]
    for r in range(ROUNDS):
        for k, (a, b, c, d) in enumerate(G_CALLS):
            x, y = m[2 * k], m[2 * k + 1]
            v[a] = add(g, add(g, v[a], v[b]), x)
            v[d] = rotr(xor_word(g, v[d], v[a]), 16)
            v[c] = add(g, v[c], v[d])
            v[b] = rotr(xor_word(g, v[b], v[c]), 12)
            v[a] = add(g, add(g, v[a], v[b]), y)
            v[d] = rotr(xor_word(g, v[d], v[a]), 8)
            v[c] = add(g, v[c], v[d])
            v[b] = rotr(xor_word(g, v[b], v[c]), 7)
        m = [m[i] for i in SCHEDULE]
    digest = []
    for i in range(8):
        for blk in range(4):
            bits = [bxor(g, v[i][t], v[i + 8][t]) for t in range(8 * blk, 8 * blk + 8)]
            digest.extend(bits)
            if on_block is not None:
                on_block(32 * i + 8 * blk, bits)
    return digest


def butterfly(g, w, idx, s):
    """One transpose stage on the word indices idx (all with bit s clear) and idx + s."""
    m = g.node("CONST", s)
    for j in idx:
        lo, hi = w[j], w[j + s]
        t = g.node("AND", g.node("XOR", g.node("SHR", lo, s), hi), m)
        w[j + s] = g.node("XOR", hi, t)
        w[j] = g.node("XOR", lo, g.node("SHL", t, s))


def sweep(g, w, group, stages):
    """Apply the stages to the words listed in group (a subcube of word indices)."""
    for s in stages:
        butterfly(g, w, [j for j in group if not j & s], s)



def build():
    """BLAKE3 program fused with a 256x256 bit-matrix transpose. The transpose stages
    commute (stage s exchanges word-index bit s with bit-position bit s), so they run
    in three register-sized sweeps: stages 1,2,4 as each block of 8 digest bits is
    formed, then 8,16,32, then 64,128."""
    g = Graph()
    w = [None] * 256

    def first_sweep(j0, block):
        for k, val in enumerate(block):
            assert val[0] is not None
            w[j0 + k] = val[0]
        sweep(g, w, range(j0, j0 + 8), (1, 2, 4))

    digest = compile_blake3(g, first_sweep)
    flips = [f for (_, f) in digest]
    for low in range(8):
        for high in range(4):
            sweep(g, w, [low + 8 * k + 64 * high for k in range(8)], (8, 16, 32))
    for low in range(64):
        sweep(g, w, [low + 64 * k for k in range(4)], (64, 128))
    return g, flips, w


def transpose_mask(s):
    m = 0
    for bit in range(WORD):
        if not bit & s:
            m |= 1 << bit
    return m


# ----------------------------------------------------------------------------
# Register allocation (Belady: evict the value whose next use is furthest).

IN_BASE, CONST_BASE, SPILL_BASE, OUT_BASE = 0, 512, 1024, 1 << 20


def _args(op):
    if op[0] in ("XOR", "AND", "OR"):
        return (op[1], op[2])
    if op[0] in ("NOT", "SHL", "SHR"):
        return (op[1],)
    return ()


def allocate(g, outputs):
    """Straight-line register program for the graph nodes reachable from outputs.
    outputs[i] is stored to OUT_BASE + i once computed."""
    seen, stack = set(), list(outputs)
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            stack.extend(_args(g.ops[n]))
    order = [n for n in range(len(g.ops)) if n in seen and g.ops[n][0] not in ("IN", "CONST")]
    end = len(order)
    uses = {}
    for t, n in enumerate(order):
        for a in _args(g.ops[n]):
            uses.setdefault(a, []).append(t)
    out_slot = {}
    for i, n in enumerate(outputs):
        out_slot.setdefault(n, OUT_BASE + i)
        uses.setdefault(n, []).append(end)
    ptr = {}
    never = 1 << 60

    def next_use(n, t):
        u = uses.get(n, ())
        p = ptr.get(n, 0)
        while p < len(u) and u[p] < t:
            p += 1
        ptr[n] = p
        return u[p] if p < len(u) else never

    home = {}
    for n in seen:
        op = g.ops[n]
        if op[0] == "IN":
            home[n] = IN_BASE + op[1]
        elif op[0] == "CONST":
            home[n] = CONST_BASE + op[1].bit_length()
    reg_of, held, prog = {}, [None] * PROGRAM_REGISTERS, []
    spill = [SPILL_BASE]

    def take(t, keep):
        best, far = None, -1
        for r in range(PROGRAM_REGISTERS):
            v = held[r]
            if v is None:
                return r
            if v in keep:
                continue
            nu = next_use(v, t)
            if nu > far:
                best, far = r, nu
        v = held[best]
        if far != never and v not in home:
            if v in out_slot:
                home[v] = out_slot[v]
            else:
                home[v] = spill[0]
                spill[0] += 1
            prog.append(("ST", home[v], best))
        del reg_of[v]
        held[best] = None
        return best

    for t, n in enumerate(order):
        op = g.ops[n]
        args = _args(op)
        for a in args:
            if a not in reg_of:
                r = take(t, set(args))
                prog.append(("LD", r, home[a]))
                held[r], reg_of[a] = a, r
        src = tuple(reg_of[a] for a in args)
        for a in set(args):
            if next_use(a, t + 1) == never:
                held[reg_of[a]] = None
                del reg_of[a]
        rd = take(t + 1, set())
        prog.append((op[0], rd, src, op[2] if op[0] in ("SHL", "SHR") else None))
        held[rd], reg_of[n] = n, rd
        if n in out_slot and next_use(n, t + 1) == end:
            if n not in home:
                prog.append(("ST", out_slot[n], rd))
                home[n] = out_slot[n]
            held[rd] = None
            del reg_of[n]
    for n in outputs:   # an output that was already stored elsewhere (never for this graph)
        assert home.get(n) == out_slot[n], "output stored outside its slot"
    return prog


def run(prog, planes, consts):
    """Execute the register program. planes: 512 input words. Returns the output memory."""
    mem = {IN_BASE + i: w for i, w in enumerate(planes)}
    mem.update(consts)
    reg = [0] * REGISTERS
    for ins in prog:
        k = ins[0]
        if k == "LD":
            reg[ins[1]] = mem[ins[2]]
        elif k == "ST":
            mem[ins[1]] = reg[ins[2]]
        elif k == "XOR":
            s = ins[2]
            reg[ins[1]] = reg[s[0]] ^ reg[s[1]]
        elif k == "AND":
            s = ins[2]
            reg[ins[1]] = reg[s[0]] & reg[s[1]]
        elif k == "OR":
            s = ins[2]
            reg[ins[1]] = reg[s[0]] | reg[s[1]]
        elif k == "NOT":
            reg[ins[1]] = reg[ins[2][0]] ^ ALL
        elif k == "SHL":
            reg[ins[1]] = (reg[ins[2][0]] << ins[3]) & ALL
        elif k == "SHR":
            reg[ins[1]] = reg[ins[2][0]] >> ins[3]
        else:
            raise ValueError(k)
    return mem


def constants():
    c = {CONST_BASE + 0: 0}
    s = 128
    while s:
        c[CONST_BASE + s.bit_length()] = transpose_mask(s)
        s >>= 1
    return c


def count(prog):
    tally = {}
    for ins in prog:
        tally[ins[0]] = tally.get(ins[0], 0) + 1
    return tally


# ----------------------------------------------------------------------------
# Batches, keys and the experiment protocol.

def planes_from_seed(seed_hex):
    raw = hashlib.shake_256(bytes.fromhex(seed_hex) + b"bitslice-planes").digest(512 * 32)
    return [int.from_bytes(raw[32 * i: 32 * i + 32], "little") for i in range(512)]


def message(planes, lane):
    bits = 0
    for i in range(512):
        bits |= (planes[i] >> lane & 1) << i
    return bits.to_bytes(64, "little")


class Machine:
    def __init__(self):
        g, self.flips, keys = build()
        self.prog = allocate(g, keys)
        self.consts = constants()
        self.flip_mask = sum(f << j for j, f in enumerate(self.flips))

    def keys(self, planes):
        mem = run(self.prog, planes, self.consts)
        return [mem[OUT_BASE + l] for l in range(256)]

    def key_of_digest(self, digest):
        return int.from_bytes(digest, "little") ^ self.flip_mask

    def tally(self):
        c = count(self.prog)
        return {"LD": c.get("LD", 0), "ST": c.get("ST", 0),
                "ALU": sum(v for k, v in c.items() if k not in ("LD", "ST")),
                "NOT": c.get("NOT", 0), "total": len(self.prog)}


MASK_BITS = [(byte, bit) for byte in (0, 8, 16, 24) for bit in (0, 7)]


def masked(key):
    """The digest bits named by MASK_BITS, read from a key (key bit 8*byte+bit)."""
    return tuple(key >> (8 * byte + bit) & 1 for byte, bit in MASK_BITS)


def mask_hex():
    digest = bytearray(32)
    for byte, bit in MASK_BITS:
        digest[byte] |= 1 << bit
    return digest.hex()


def batch_pairs(m, seed, need, full_check):
    """Key one 256-message batch; return up to `need` disjoint lane pairs whose keys agree
    on the masked digest bits (as messages, with a reference re-check of each), and the
    number of reference mismatches over the whole batch when full_check is set."""
    planes = planes_from_seed(seed)
    keys = m.keys(planes)
    groups = {}
    for lane in range(256):
        groups.setdefault(masked(keys[lane] ^ m.flip_mask), []).append(lane)
    found = []
    for lanes in groups.values():
        for i in range(0, len(lanes) - 1, 2):
            found.append((lanes[i], lanes[i + 1]))
    found.sort()
    out = []
    for la, lb in found[:need]:
        ma, mb = message(planes, la), message(planes, lb)
        bad = (m.key_of_digest(reference_blake3_r2(ma)) != keys[la]) + (m.key_of_digest(reference_blake3_r2(mb)) != keys[lb])
        out.append((ma, mb, bad))
    mismatches = None
    if full_check:
        mismatches = sum(m.key_of_digest(reference_blake3_r2(message(planes, lane))) != keys[lane]
                         for lane in range(256))
    return out, mismatches


def protocol(request):
    m = Machine()
    t = m.tally()
    trials = request["trials"]
    batches = min(len(trials), 512)
    pairs, checks = [], None
    for k in range(batches):
        need = (len(trials) - 1 - k) // batches + 1
        got, mismatches = batch_pairs(m, trials[k]["seed"], need, k == 0)
        pairs.append(got)
        if k == 0:
            checks = mismatches
    rows = []
    for index, trial in enumerate(trials):
        k, use = index % batches, index // batches
        obs = {"batch": k}
        if use < len(pairs[k]):
            ma, mb, bad = pairs[k][use]
            row = {"trial": trial["trial"], "message_a_hex": ma.hex(), "message_b_hex": mb.hex()}
            obs["pair_reference_mismatches"] = bad
        else:
            row = {"trial": trial["trial"], "message_a_hex": None, "message_b_hex": None}
        if index == 0:
            obs["batch_messages_checked"] = 256
            obs["batch_reference_mismatches"] = checks
            obs["program_instructions"] = t["total"]
            obs["program_alu"] = t["ALU"]
            obs["program_loads"] = t["LD"]
            obs["program_stores"] = t["ST"]
            obs["program_registers"] = PROGRAM_REGISTERS
        row["observations"] = obs
        rows.append(row)
    return {"schema_version": 1, "trials": rows}


def report():
    m = Machine()
    t = m.tally()
    planes = planes_from_seed("00" * 32)
    keys = m.keys(planes)
    bad = sum(m.key_of_digest(reference_blake3_r2(message(planes, l))) != keys[l] for l in range(256))
    print("program registers", PROGRAM_REGISTERS, "of", REGISTERS)
    print("program per 256-message batch:", t)
    print("program instructions per message: %d/256 = %.4f" % (t["total"], t["total"] / 256))
    print("reference mismatches in a 256-message batch:", bad)


if __name__ == "__main__":
    if sys.argv[1:] == ["--report"]:
        report()
    else:
        out = protocol(json.loads(sys.stdin.read()))
        sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")
