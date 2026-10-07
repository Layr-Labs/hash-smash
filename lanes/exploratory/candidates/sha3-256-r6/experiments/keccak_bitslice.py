"""Bitsliced 6-round SHA3-256 over 256 messages per 256-bit word, with an exact operation count.

Word i of the input holds bit i of 256 messages (message l lives in bit l of every word).
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

ROUNDS = 6
WORD = 256
REGISTERS = 16           # machine registers
PROGRAM_REGISTERS = 15   # the hash program's share; the 16th holds the key write pointer
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
ALL = (1 << WORD) - 1


# ----------------------------------------------------------------------------
# Reference: scalar SHA3-256 with the first 6 Keccak-f[1600] rounds.

def _rol64(v, n):
    n %= 64
    return ((v << n) | (v >> (64 - n))) & 0xFFFFFFFFFFFFFFFF if n else v


def reference_sha3_256_r6(message):
    rate = 136
    padded = bytearray(message) + b"\x06" + bytes((-len(message) - 1) % rate)
    padded[-1] |= 0x80
    a = [0] * 25
    for off in range(0, len(padded), rate):
        for i in range(rate // 8):
            a[i] ^= int.from_bytes(padded[off + 8 * i: off + 8 * i + 8], "little")
        for r in range(ROUNDS):
            c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
            d = [c[(x + 4) % 5] ^ _rol64(c[(x + 1) % 5], 1) for x in range(5)]
            b = [0] * 25
            for x in range(5):
                for y in range(5):
                    b[y + 5 * ((2 * x + 3 * y) % 5)] = _rol64(a[x + 5 * y] ^ d[x], RHO[x + 5 * y])
            a = [b[i] ^ (~b[(i % 5 + 1) % 5 + 5 * (i // 5)] & b[(i % 5 + 2) % 5 + 5 * (i // 5)])
                 for i in range(25)]
            a[0] ^= RC[r]
    return b"".join(a[i].to_bytes(8, "little") for i in range(4))


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


def andn(g, b, c, use):
    """Return (NOT b) AND c. When b and c carry equal flips one operand needs a NOT;
    use ("b" or "c") names which one."""
    (bn, bf), (cn, cf) = b, c
    if bn is None:
        return c if bf else (None, 0)
    if cn is None:
        return (bn, bf ^ 1) if cf else (None, 0)
    if bn == cn:
        return (bn, bf ^ 1) if bf != cf else (None, 0)
    if bf == 1 and cf == 0:                       # stored b is NOT b
        return (g.node("AND", bn, cn), 0)
    if bf == 0 and cf == 1:                       # b OR (NOT c) = NOT((NOT b) AND c)
        return (g.node("OR", bn, cn), 1)
    if bf == 0:
        if use == "b":
            return (g.node("AND", g.node("NOT", bn), cn), 0)
        return (g.node("OR", bn, g.node("NOT", cn)), 1)
    if use == "b":
        return (g.node("OR", g.node("NOT", bn), cn), 1)
    return (g.node("AND", bn, g.node("NOT", cn)), 0)


def _needs_not(b, c):
    (bn, bf), (cn, cf) = b, c
    return bn is not None and cn is not None and bn != cn and bf == cf


def chi_row(g, row, outputs):
    """row: 5 symbolic bits; outputs: which x positions are needed. Minimises new NOT nodes."""
    terms = list(outputs)
    best = None
    for mask in range(32):
        cost = 0
        ok = True
        for x in terms:
            b, c = (x + 1) % 5, (x + 2) % 5
            if _needs_not(row[b], row[c]) and not (mask >> b & 1 or mask >> c & 1):
                ok = False
                break
        if not ok:
            continue
        for i in range(5):
            if mask >> i & 1:
                n = row[i][0]
                if n is None or ("NOT", n) in g.memo:
                    continue
                cost += 1
        if best is None or cost < best[0]:
            best = (cost, mask)
    mask = best[1]
    out = {}
    for x in terms:
        b, c = (x + 1) % 5, (x + 2) % 5
        use = "b" if mask >> b & 1 else "c"
        out[x] = bxor(g, row[x], andn(g, row[b], row[c], use))
    return out


def compile_keccak(g, on_block=None):
    """State bits as symbolic values; returns the 256 digest-bit values.
    Column parities of the next round are accumulated as each chi row is produced,
    so the scheduler finds them in registers."""
    a = [[(None, 0)] * 64 for _ in range(25)]
    for i in range(512):
        a[i // 64][i % 64] = (g.node("IN", i), 0)
    for i in (512 + 1, 512 + 2, 1087):    # padding 0x06 at byte 64, 0x80 at byte 135
        a[i // 64][i % 64] = bxor(g, a[i // 64][i % 64], (None, 1))
    c = [[(None, 0)] * 64 for _ in range(5)]
    for x in range(5):
        for z in range(64):
            for y in range(5):
                c[x][z] = bxor(g, c[x][z], a[x + 5 * y][z])
    src = {}
    for x in range(5):
        for y in range(5):
            src[(y, (2 * x + 3 * y) % 5)] = (x, y)
    for r in range(ROUNDS):
        last = r == ROUNDS - 1
        d = [[None] * 64 for _ in range(5)]

        def dval(x, z):
            if d[x][z] is None:
                d[x][z] = bxor(g, c[(x + 4) % 5][z], c[(x + 1) % 5][(z - 1) % 64])
            return d[x][z]

        new = [[(None, 0)] * 64 for _ in range(25)]
        nc = [[(None, 0)] * 64 for _ in range(5)]
        rows = [0] if last else range(5)
        need = (0, 1, 2, 3) if last else (0, 1, 2, 3, 4)
        for z in range(64):
            for y in rows:
                row = []
                for x in range(5):
                    sx, sy = src[(x, y)]
                    zz = (z - RHO[sx + 5 * sy]) % 64
                    row.append(bxor(g, a[sx + 5 * sy][zz], dval(sx, zz)))
                out = chi_row(g, row, need)
                if y == 0 and RC[r] >> z & 1:
                    out[0] = bxor(g, out[0], (None, 1))
                for x in need:
                    new[x + 5 * y][z] = out[x]
                    if not last:
                        nc[x][z] = bxor(g, nc[x][z], out[x])
            if last and on_block is not None and z % 8 == 7:
                for x in need:
                    on_block(64 * x + z - 7, [new[x][zz] for zz in range(z - 7, z + 1)])
        a, c = new, nc
    return [a[j // 64][j % 64] for j in range(256)]


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
    """Keccak program fused with a 256x256 bit-matrix transpose. The transpose stages
    commute (stage s exchanges word-index bit s with bit-position bit s), so they run
    in three register-sized sweeps: stages 1,2,4 as each block of 8 digest planes
    leaves the last round, then 8,16,32, then 64,128."""
    g = Graph()
    w = [None] * 256

    def first_sweep(j0, block):
        for k, v in enumerate(block):
            assert v[0] is not None
            w[j0 + k] = v[0]
        sweep(g, w, range(j0, j0 + 8), (1, 2, 4))

    digest = compile_keccak(g, first_sweep)
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
        bad = (m.key_of_digest(reference_sha3_256_r6(ma)) != keys[la]) + (m.key_of_digest(reference_sha3_256_r6(mb)) != keys[lb])
        out.append((ma, mb, bad))
    mismatches = None
    if full_check:
        mismatches = sum(m.key_of_digest(reference_sha3_256_r6(message(planes, lane))) != keys[lane]
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
    bad = sum(m.key_of_digest(reference_sha3_256_r6(message(planes, l))) != keys[l] for l in range(256))
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
