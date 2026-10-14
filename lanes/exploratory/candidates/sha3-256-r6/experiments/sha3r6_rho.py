"""Bit-sliced parallel collision search on SHA3-256 with rounds 0..5 (sha3-256-r6-prefix-v1).

Chain step f(x) = H(x) for a 32-byte message x; 256 trails run as bit planes, so plane j (digest bit j)
is one 256-bit word whose bit t belongs to trail t. The straight line has XOR, AND, OR and NOT only:
rotations are renaming, constants are folded, and NOT is folded into a per-plane polarity.

  python3 sha3r6_rho.py --ledger          operation counts, register peak and code size of the step
  python3 sha3r6_rho.py --selftest N      step versus the reference on N messages and chained steps
  python3 sha3r6_rho.py --stats T         the experiment searches on T local trials, with an ideal control
  python3 sha3r6_rho.py < request.json    organizer experiment (python-message-pairs-v1)
"""
import hashlib
import json
import sys

RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
      0x000000000000808B, 0x0000000080000001)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
ROUNDS = 6
N_IN = 256          # input and digest planes
REGS = 2304         # declared register file (proof.md Section 4)
LANES = 256         # trails per batch
FULL = (1 << LANES) - 1


# ---------------------------------------------------------------- reference

def keccak_r6(msg):
    """sha3-256-r6-prefix-v1 digest of a message shorter than 136 bytes (one block)."""
    block = bytearray(msg) + b'\x06' + bytes(135 - len(msg))
    block[135] |= 0x80
    a = [int.from_bytes(block[8 * i:8 * i + 8], 'little') for i in range(17)] + [0] * 8
    m = (1 << 64) - 1
    for rc in RC:
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ (((c[(x + 1) % 5] << 1) | (c[(x + 1) % 5] >> 63)) & m) for x in range(5)]
        b = [0] * 25
        for y in range(5):
            for x in range(5):
                v = a[x + 5 * y] ^ d[x]
                r = RHO[x + 5 * y]
                b[y + 5 * ((2 * x + 3 * y) % 5)] = ((v << r) | (v >> (64 - r))) & m if r else v
        a = [b[i] ^ (~b[(i % 5 + 1) % 5 + 5 * (i // 5)] & b[(i % 5 + 2) % 5 + 5 * (i // 5)]) for i in range(25)]
        a[0] ^= rc
    return b''.join(v.to_bytes(8, 'little') for v in a[:4])


# ---------------------------------------------------------------- generator

class Gen:
    """SSA straight line. A logical value is ('c', bit) or ('v', node, polarity); nodes < N_IN are inputs."""

    def __init__(self):
        self.ins = []
        self.memo = {}

    def emit(self, op, a, b):
        key = (op, min(a, b), max(a, b))
        if key not in self.memo:
            self.ins.append((op, a, b))
            self.memo[key] = N_IN + len(self.ins) - 1
        return self.memo[key]

    def xor(self, a, b):
        if a[0] == 'c':
            return b if not a[1] else neg(b)
        if b[0] == 'c':
            return self.xor(b, a)
        if a[1] == b[1]:
            return ('c', a[2] ^ b[2])
        return ('v', self.emit('XOR', a[1], b[1]), a[2] ^ b[2])

    def and_(self, a, b):
        if a[0] == 'c':
            return b if a[1] else ('c', 0)
        if b[0] == 'c':
            return self.and_(b, a)
        (_, na, pa), (_, nb, pb) = a, b
        if na == nb:
            return a if pa == pb else ('c', 0)
        if pa == pb:
            return ('v', self.emit('AND' if pa == 0 else 'OR', na, nb), pa)
        if pa:
            na, nb = nb, na                      # na has polarity 0: na AND NOT nb = na XOR (na AND nb)
        return ('v', self.emit('XOR', na, self.emit('AND', na, nb)), 0)

    def flip(self, a):
        return ('v', self.emit('NOT', a[1], a[1]), a[2] ^ 1)


def neg(a):
    return ('c', a[1] ^ 1) if a[0] == 'c' else ('v', a[1], a[2] ^ 1)


def two_op_terms(pols, live):
    """AND terms (NOT b) AND c of a chi row that cost two operations (b and c of equal polarity)."""
    return sum(1 for x in live if pols[(x + 1) % 5] is not None and pols[(x + 1) % 5] == pols[(x + 2) % 5])


def chi_row(g, row, live):
    pols = [b[2] if b[0] == 'v' else None for b in row]
    var = [x for x in range(5) if pols[x] is not None]
    best, flips = two_op_terms(pols, live), ()
    for mask in range(1, 1 << len(var)):
        fl = [var[i] for i in range(len(var)) if mask >> i & 1]
        cost = two_op_terms([1 - p if x in fl else p for x, p in enumerate(pols)], live) + len(fl)
        if cost < best:
            best, flips = cost, tuple(fl)
    row = [g.flip(b) if x in flips else b for x, b in enumerate(row)]
    return [g.xor(row[x], g.and_(neg(row[(x + 1) % 5]), row[(x + 2) % 5])) if x in live else None
            for x in range(5)]


def build(in_pol):
    """Six rounds with theta evaluated lazily per chi row. Returns (Gen, digest planes)."""
    g = Gen()
    lanes = [[('c', 0)] * 64 for _ in range(25)]
    for j in range(N_IN):
        lanes[j // 64][j % 64] = ('v', j, in_pol[j])
    for z in range(64):
        lanes[4][z] = ('c', (0x06 >> z) & 1)
        lanes[16][z] = ('c', int(z == 63))
    for r in range(ROUNDS):
        par = [[lanes[x][z] for z in range(64)] for x in range(5)]
        for x in range(5):
            for y in range(1, 5):
                par[x] = [g.xor(par[x][z], lanes[x + 5 * y][z]) for z in range(64)]
        d = [[g.xor(par[(x - 1) % 5][z], par[(x + 1) % 5][(z - 1) % 64]) for z in range(64)] for x in range(5)]
        src = {}
        for y in range(5):
            for x in range(5):
                src[y + 5 * ((2 * x + 3 * y) % 5)] = (x + 5 * y, RHO[x + 5 * y])
        last = r == ROUNDS - 1
        new = [[None] * 64 for _ in range(25)]
        for y in range(1 if last else 5):
            for z in range(64):
                row = []
                for x in range(5):
                    i, rot = src[x + 5 * y]
                    zz = (z - rot) % 64
                    row.append(g.xor(lanes[i][zz], d[i % 5][zz]))
                out = chi_row(g, row, range(4) if last else range(5))
                for x in range(5):
                    new[x + 5 * y][z] = out[x]
        for z in range(64):
            if (RC[r] >> z) & 1:
                new[0][z] = neg(new[0][z])
        lanes = new
    return g, [lanes[j // 64][j % 64] for j in range(N_IN)]


def step_program():
    """The chain step as (instructions, input polarity). An instruction is (op, dst, a, b) on registers.

    The input polarity is the first of eight iterates P -> P' (P' the digest polarity) with the fewest
    operations; digest planes whose polarity differs from the input polarity get one NOT each, which also
    writes the plane into its input register."""
    best = None
    pol = [0] * N_IN
    for _ in range(8):
        g, outs = build(pol)
        need = set(o[1] for o in outs)
        keep = [False] * len(g.ins)
        for i in range(len(g.ins) - 1, -1, -1):
            if N_IN + i in need:
                keep[i] = True
                need.update(g.ins[i][1:])
        fix = sum(o[2] != p for o, p in zip(outs, pol))
        cost = sum(keep) + fix
        nxt = [o[2] for o in outs]
        if best is None or cost < best[0]:
            best = (cost, g, outs, keep, list(pol))
        del g, outs, keep
        pol = nxt
    _, g, outs, keep, pol = best
    return allocate(g, outs, keep, pol), pol


def allocate(g, outs, keep, pol):
    """Registers: input plane j and digest plane j live in register j; temporaries use 256..REGS-1."""
    seq = [(N_IN + i,) + g.ins[i] for i in range(len(g.ins)) if keep[i]]
    last = {}
    for k, (d, op, a, b) in enumerate(seq):
        last[a] = k
        last[b] = k
    out_of = {}
    for j, o in enumerate(outs):
        if o[2] == pol[j] and o[1] not in out_of and o[1] >= N_IN:
            out_of[o[1]] = j                     # computed straight into register j
    reg = {j: j for j in range(N_IN)}
    free = list(range(REGS - 1, N_IN - 1, -1))
    prog = []
    peak = 0
    for k, (d, op, a, b) in enumerate(seq):
        ra, rb = reg[a], reg[b]
        for n in {a, b}:
            if last[n] == k and n not in out_of and n >= N_IN:
                free.append(reg[n])
        if d in out_of:
            rd = out_of[d]
        else:
            if not free:
                raise SystemExit('register file exhausted')
            rd = free.pop()
        reg[d] = rd
        prog.append((op, rd, ra, rb))
        peak = max(peak, REGS - len(free))
    for j, o in enumerate(outs):
        if o[1] not in out_of or out_of[o[1]] != j:
            prog.append(('NOT' if o[2] != pol[j] else 'MOV', j, reg[o[1]], reg[o[1]]))
    allocate.peak = peak
    return prog


def compile_step(prog, chunk=1500):
    """A Python function r -> None executing the straight line on the register list r.

    The straight line is compiled in pieces of `chunk` instructions to bound the compiler's memory."""
    sym = {'XOR': '^', 'AND': '&', 'OR': '|'}
    parts = []
    for start in range(0, len(prog), chunk):
        lines = ['def part(r):', ' F = %d' % FULL]
        for op, d, a, b in prog[start:start + chunk]:
            if op == 'NOT':
                lines.append(f' r[{d}] = r[{a}] ^ F')
            elif op == 'MOV':
                lines.append(f' r[{d}] = r[{a}]')
            else:
                lines.append(f' r[{d}] = r[{a}] {sym[op]} r[{b}]')
        env = {}
        exec(compile('\n'.join(lines), '<step>', 'exec'), env)
        parts.append(env['part'])

    def step(r):
        for part in parts:
            part(r)
    return step


# ---------------------------------------------------------------- planes

def to_planes(points, pol, width=256):
    """Points (ints < 2^width, one per lane) -> 256 physical planes; planes >= width carry logical 0."""
    planes = []
    for j in range(N_IN):
        w = 0
        if j < width:
            for t, x in enumerate(points):
                w |= ((x >> j) & 1) << t
        planes.append(w ^ (FULL if pol[j] else 0))
    return planes


def lane_point(r, pol, t, width=256):
    x = 0
    for j in range(width):
        x |= (((r[j] >> t) & 1) ^ pol[j]) << j
    return x


def message(x):
    return x.to_bytes(32, 'little')


# ---------------------------------------------------------------- search

class Coins:
    """The search's random words; here SHAKE-256 of a seed, a reproducible stand-in for the primitive."""

    def __init__(self, seed):
        self.xof = hashlib.shake_256(b'sha3r6-rho-coins' + seed).digest(1 << 16)
        self.pos = 0

    def word(self, bits):
        n = (bits + 7) // 8
        if self.pos + n > len(self.xof):
            self.xof = hashlib.shake_256(self.xof[-32:]).digest(1 << 16)
            self.pos = 0
        v = int.from_bytes(self.xof[self.pos:self.pos + n], 'little') & ((1 << bits) - 1)
        self.pos += n
        return v


def search(step, pol, coins, width, dbits, batches, cap, table_cap, f_point=None):
    """One attempt of the 256-lane distinguished-point search on the width-bit chain (proof.md Section 5).

    Trail i starts at R + i mod 2^width for one random word R; a point is distinguished when its dbits
    low physical planes are zero. Returns (pair or None, observations)."""
    mask = (1 << width) - 1
    base = coins.word(width)
    nxt = [LANES]
    starts = [(base + t) & mask for t in range(LANES)]
    lengths = [0] * LANES
    points = list(starts)
    table = {}
    obs = {'batches': 0, 'dps': 0, 'cut': 0, 'merges': 0, 'robin_hood': 0}
    if f_point is None:
        regs = to_planes(points, pol, width) + [0] * (REGS - N_IN)
    for _ in range(batches):
        obs['batches'] += 1
        if f_point is None:
            step(regs)
            for j in range(width, N_IN):         # reduced width: planes above width carry logical 0
                regs[j] = FULL if pol[j] else 0
            w = 0
            for j in range(dbits):
                w |= regs[j]
            hits = [t for t in range(LANES) if not (w >> t) & 1]
        else:
            points = [f_point(p) & mask for p in points]
            hits = [t for t in range(LANES) if all(((points[t] >> j) & 1) == pol[j] for j in range(dbits))]
        for t in range(LANES):
            lengths[t] += 1
        restarts = []
        for t in hits:
            x = lane_point(regs, pol, t, width) if f_point is None else points[t]
            obs['dps'] += 1
            if x in table:
                obs['merges'] += 1
                return recover(table[x], (starts[t], lengths[t]), width, f_point, obs), obs
            if len(table) >= table_cap:
                return None, obs
            table[x] = (starts[t], lengths[t])
            restarts.append(t)
        restarts += [t for t in range(LANES) if lengths[t] >= cap and t not in restarts]
        obs['cut'] += sum(1 for t in restarts if lengths[t] >= cap)
        for t in restarts:
            starts[t] = (base + nxt[0]) & mask
            nxt[0] += 1
            lengths[t] = 0
            points[t] = starts[t]
            if f_point is None:
                set_lane(regs, pol, t, starts[t], width)
    return None, obs


def set_lane(regs, pol, t, x, width):
    for j in range(width):
        bit = ((x >> j) & 1) ^ pol[j]
        regs[j] = (regs[j] & ~(1 << t)) | (bit << t)


def chain(x, n, width, f_point):
    mask = (1 << width) - 1
    for _ in range(n):
        x = (f_point(x) if f_point else int.from_bytes(keccak_r6(message(x)), 'little')) & mask
    return x


def recover(a, b, width, f_point, obs):
    """Walk two trails (start, length) ending at the same distinguished point to their merge."""
    (sa, la), (sb, lb) = a, b
    if la < lb:
        (sa, la), (sb, lb) = (sb, lb), (sa, la)
    xa = chain(sa, la - lb, width, f_point)
    xb = sb
    if xa == xb:
        obs['robin_hood'] += 1
        return None
    mask = (1 << width) - 1
    for _ in range(lb):
        ya = (f_point(xa) if f_point else int.from_bytes(keccak_r6(message(xa)), 'little')) & mask
        yb = (f_point(xb) if f_point else int.from_bytes(keccak_r6(message(xb)), 'little')) & mask
        if ya == yb:
            return xa, xb
        xa, xb = ya, yb
    return None


# ---------------------------------------------------------------- experiment

RHO_W = {'width': 22, 'dbits': 2, 'batches': 14, 'cap': 36, 'table_cap': 1 << 16}
PROJ_BITS = 22
PROJ_STEPS = 8


def rho_trial(step, pol, seed, ideal=False):
    """Experiment rho-w22: one attempt of the search at width 22 (with an ideal-function control locally)."""
    coins = Coins(seed)
    f = None
    if ideal:
        cache = {}
        oracle = Coins(b'ideal' + seed)

        def f(x):
            if x not in cache:
                cache[x] = oracle.word(RHO_W['width'])
            return cache[x]
    return search(step, pol, coins, RHO_W['width'], RHO_W['dbits'], RHO_W['batches'], RHO_W['cap'],
                  RHO_W['table_cap'], f)


def proj_trial(step, pol, seed):
    """Experiment proj-w256: 256 lanes from random planes, PROJ_STEPS chained full-width steps; the first pair
    of distinct inputs (in step-major order) whose digests agree on the PROJ_BITS low bits."""
    coins = Coins(seed)
    regs = [coins.word(256) for _ in range(N_IN)] + [0] * (REGS - N_IN)
    starts = [lane_point(regs, pol, t) for t in (0, 1)]
    seen = {}
    for s in range(PROJ_STEPS):
        step(regs)
        for t in range(LANES):
            key = 0
            for j in range(PROJ_BITS):
                key |= (((regs[j] >> t) & 1) ^ pol[j]) << j
            if key in seen:
                return seen[key], (s, t), {'steps': s + 1}
            seen[key] = (s, t)
    return None, None, {'steps': PROJ_STEPS}


def proj_input(seed, pol, pos):
    """The input (step-s point) of lane t, recomputed from the trial's random planes with the reference."""
    s, t = pos
    coins = Coins(seed)
    regs = [coins.word(256) for _ in range(N_IN)]
    x = lane_point(regs, pol, t)
    for _ in range(s):
        x = int.from_bytes(keccak_r6(message(x)), 'little')
    return x


def serve():
    req = json.load(sys.stdin)
    prog, pol = step_program()
    step = compile_step(prog)
    out = []
    for tr in req['trials']:
        seed = bytes.fromhex(tr['seed'])
        rec = {'trial': tr['trial'], 'message_a_hex': None, 'message_b_hex': None}
        if req['experiment_id'] == 'proj-w256':
            a, b, obs = proj_trial(step, pol, seed)
            if a:
                rec['message_a_hex'] = message(proj_input(seed, pol, a)).hex()
                rec['message_b_hex'] = message(proj_input(seed, pol, b)).hex()
        else:
            pair, obs = rho_trial(step, pol, seed)
            if pair:
                rec['message_a_hex'], rec['message_b_hex'] = message(pair[0]).hex(), message(pair[1]).hex()
        rec['observations'] = obs
        out.append(rec)
    json.dump({'schema_version': 1, 'trials': out}, sys.stdout, separators=(',', ':'))


def main():
    args = sys.argv[1:]
    if not args:
        return serve()
    prog, pol = step_program()
    counts = {}
    for op, *_ in prog:
        counts[op] = counts.get(op, 0) + 1
    if args[0] == '--ledger':
        print(json.dumps({'instructions': len(prog), 'by_op': counts, 'register_peak': allocate.peak,
                          'registers': REGS, 'complemented_inputs': sum(pol)}))
    elif args[0] == '--selftest':
        import os
        n = int(args[1])
        step = compile_step(prog)
        bad = 0
        for k in range(0, n, LANES):
            xs = [int.from_bytes(os.urandom(32), 'little') for _ in range(min(LANES, n - k))]
            r = to_planes(xs + [0] * (LANES - len(xs)), pol) + [0] * (REGS - N_IN)
            for s in range(4):
                step(r)
                xs = [int.from_bytes(keccak_r6(message(x)), 'little') for x in xs]
                bad += sum(lane_point(r, pol, t) != x for t, x in enumerate(xs))
        print(f'selftest: {n} messages, 4 chained steps each: {bad} differences')
    elif args[0] == '--stats':
        import os
        step = compile_step(prog)
        n = int(args[1])
        res = {}
        for name in ('target', 'ideal'):
            res[name] = sum(rho_trial(step, pol, os.urandom(32), name == 'ideal')[0] is not None for _ in range(n))
        res['proj'] = sum(proj_trial(step, pol, os.urandom(32))[0] is not None for _ in range(n))
        print(json.dumps({'trials': n, 'rho_w22_target': res['target'], 'rho_w22_ideal': res['ideal'],
                          'proj_w256': res['proj']}))


if __name__ == '__main__':
    main()
