# SHA3-256 prefix rounds 0–5: bitsliced counted evaluation + unconditional radix birthday (125.66)

The scalar is `time_log2` under `collision-frontier-v5` (C = 1626); memory is reported only.
Lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Attack: ordinary collision. Heuristics: **none**.
Total charged time < 2^125.6522 ≤ 2^125.66. Peak memory < 2^136 bytes. Success probability > 0.39.
This is a generic birthday search with a constant-factor speedup. No cryptanalytic weakness of SHA3 is claimed.
`baseline_improved: sha3-256-r6-nominal-v2` is the required identifier only.

## 0. Credits

- The compiler and counted simulator `ir.py` (Appendix A) are taken unchanged from **winglock**'s package
  7e40f784 (SHA-256 877005938fac…). They do store-to-load forwarding under a register budget,
  dead-scratch-store elimination, interval-colouring allocation onto 62+2 registers, and op counting.
- The idea of evaluating the selected permutation in ordinary word operations, bitsliced 256 messages
  to a word, follows the public 124.x line on this track (winglock 5e73af65/7e40f784, 5kyguy 6e715d9a,
  may93182 11c46f4d for the bit-plane Keccak and the delta-swap transpose).
- The plane-ordered theta fold (each round's output stored already XORed with the next round's D,
  using the previous plane's parities and a 5-word fix for the first plane) is **winglock**'s gen_round
  technique (7e40f784), re-implemented here for a full-state bitsliced round.
- Static polarity tracking for chi follows **tekkac** b001199a (lane-complement chi). Per-message
  charging follows zeeshan8281 and tekkac (f58275ef).
- This package uses **none** of their message families, linear structures, tagged tables, or the H1
  premise. The search is our own unconditional radix birthday, from our tickets 50b542cf → f75b4650.
  The bitsliced generator `bsk5.py` and the checker `check5.py` are ours.

## 1. Target, messages, coins

`N = 2^256`. `Q = 256·ceil(ceil(9943·2^128/10000)/256)`, so Q/2^128 ≈ 0.9943 and Q < 2^128.
Messages are 64 bytes, i.e. 512 bits. The algorithm draws Q/256 blocks. Block b draws 512 fresh
uniform 256-bit words M_b[0..511] (512 `rand` ops). Message k of block b (k = 0..255) has message bit
w = bit k of M_b[w], where bit w is bit (w mod 8) of byte (w div 8), little-endian lanes. All Q messages
are therefore iid uniform on {0,1}^512. These are the only coins.
Index of message (b, k): i = 256b + k.
H = SHA3-256 with rounds 0..5: one 1088-bit rate block, the message in lanes 0..7, 0x06 at the start of
lane 8, 0x80 at the end of lane 16 (bit 63), capacity zero.

## 2. Algorithm (exact)

```
for each block b:
    M_b[0..511] <- rand; store (512 stores)              # message slices (kept: Msg memory)
    run BLOCK (Appendix A, bsk5.py: straight-line, 60,909 counted ops) on M_b
        -> DG[0..255]: DG[k] = H(message (b,k)) XOR POL  (POL a fixed public 256-bit constant)
    for k in 0..255:  d <- DG[k]; i <- 256b + k; Src[i] <- (d, i); Cnt_p[digit_p(d)] += 1 for p = 0,1,2
PREFIX sums on Cnt_0 (2^86), Cnt_1, Cnt_2 (2^85 each)
3 stable LSD counting-sort scatter passes over (d, i) on digits 86/85/85 bits
SCAN adjacent pairs; at the first pair with equal d:
    rebuild both messages from M (bit k of 512 words), if distinct recompute H with the target
    permutation (2 units) and output the pair if the digests are equal; halt either way.
output FAIL
```

**BLOCK.** It is the bitsliced Keccak-f prefix (rounds 0..5) on 1600 slice words. For each round:
round 0 computes theta from the message state (C to CS3, D to CS4). Every later round reads its
input already theta-applied: round r produces its output plane by plane (z = 0..63, all 25 lanes of a
plane together), forms the plane's column parities C[x][z] in registers, and stores
out ⊕ D with D[x][z] = C[x-1][z] ^ C[x+1][z-1], using C of the previous plane. For z = 0 the term
C[x+1][63] is not yet known; it is stored once (FIX3[x]) after plane 63, and the next round XORs it
into its plane-0 inputs. rho and pi are pure renaming (moved lane bit z = (A^D) bit z−ρ); chi row-wise; iota complements the
slices of lane 0 where RC bit z = 1. Constant slices (capacity, padding) are folded at generation time.
The last round computes only lanes 0..3 (the 256 output bits). Each value is tracked as (physical word,
static polarity), so NOT is free, chi's (¬b)∧c becomes AND or OR, and a physical NOT is emitted only on
a polarity mismatch (cached per value). The polarity of each of the 256 output slices is a fixed
compile-time bit, giving the constant POL. A 256×256 delta-swap transpose (8 stages × 128 swaps:
shr, xor, andi, xor, shl, xor) turns the slices into one word per message. The stages act on distinct
bit dimensions and commute; the five stages of span 128, 64, 32, 16, 8 only pair slices (L, z) whose
z agree mod 8, so the last round emits its planes grouped by z mod 8 and applies those five stages
to each group of 32 output slices in registers before the first store; the spans 4, 2, 1 run from memory.

**Correctness.** DG[k] XOR POL = H(m_{b,k}) for every k. This is a deterministic program on fixed
code, checked by simulation against the organizer verifier (Section 5). Since x ↦ x⊕POL is a
bijection, DG values are equal exactly when the digests are equal. The radix sort is a permutation and
sorts by the full 256-bit key (LSD invariant: after pass p the order is by the low 86+85p bits). So
equal digests form contiguous runs, and SCAN reaches the first equal pair. Any output is re-verified
with the target permutation, so no false collision is ever output.

## 3. Success probability (unconditional over the coins)

Let E = some pair of the Q messages collides under H, and R = some pair of messages is equal. By
Schur-convexity of collision probability in the output distribution of a fixed H on iid uniform inputs,
the uniform-output case is the minimum: `Pr(E) ≥ 1-exp(-Q(Q-1)/2^257) > 0.390012` (Q(Q-1)/2^257 ≥ 0.49431 > -ln 0.61).
`Pr(R) ≤ Q^2/2^513 < 2^-256`. On E \ R every equal-digest pair has distinct messages, so the first one
found is output. Success > 0.39.

## 4. Cost ledger (ordinary ops; measured/itemized → charged)

| Hot path | measured / itemized | charged | spare |
|---|---:|---:|---:|
| BLOCK per 256 messages (measured: ld 9582, st 7927, xor 28432, or 5311, and 2945, not 3640, shr/andi/shl 1024 each) | 60,909 | **61,500** | +591 |
| Message slices per message: 2 rand + 2 stores | 4 | (in record) | |
| Record per message: 2 rand + 2 M stores + ld DG + add index + 2 Src stores + histograms (5+6+5) + 1 loop (unrolled 16×) | 25 | **28** | +3 |
| Scatter passes 0/1/2 per record | 12/13/12 | **15/16/15** | +3 each |
| Scan per adjacent pair (common path) | 5 | **7** | +2 |

Per message charged: 61,500/256 + 28 + 46 + 7 = 321.23 ordinary ops. No target-permutation call
happens on the hot path, so permutation units are only the ≤ 2 in final verification.
Cold and fixed terms: count tables 2^87 entries × ≤ 8 ops < 2^91 (charged 2^92); setup 2^30;
the message rebuild plus scan branch ≤ 2^12; block loop control ≤ 8 per block (inside the +591).

    W ≤ 321.234375·Q + 2^92 + 2^30 + 2^20
    T ≤ W/1626 + 4
    log2 T ≈ 125.65212 < 125.66

Without spare (304.93 ops/message) the bound would be ≈ 125.577.

## 5. Evidence that BLOCK computes H (deterministic, reproducible)

Extract Appendix A and run, from the repository root:

```sh
mkdir -p /tmp/hedge && python3 - <<'EOF'
import hashlib, re
t = open("lanes/exploratory/candidates/sha3-256-r6/proof.md").read()
n = 0
for name, sha, body in re.findall(r"<!-- file: (\S+) sha256=(\w+) -->\n```python\n(.*?)```\n", t, re.S):
    assert hashlib.sha256(body.encode()).hexdigest() == sha, name
    open("/tmp/hedge/" + name, "w").write(body); n += 1
assert n == 3
EOF
cd /tmp/hedge && python3 bsk5.py && python3 check5.py REPO_ROOT code5.pkl 8
```

`bsk5.py` prints `compiled 60909 hw 62 …` (about 7 s). `check5.py` runs the compiled code on the
counted 64-register simulator for 8 random blocks (2,048 messages) and asserts DG[k] ^ POL equals
`verifier.keccak.sha3_256(m, 6)` for each message. Our run: `ALL OK 2048 digests;
POL=15602b6744518985e4cc13a22290880008d42dd8e1680252e15c5194d21e6688`. The program is straight-line,
with no data-dependent branch, so the measured count is the same for every input.

## 6. Cost-model sensitivity (disclosed)

The count charges each executed primitive once. A constant address is an instruction operand (the
same reading as the counted programs on this track), and each 'rand' is one op. If every
constant-address load/store also paid one address add (+17,509 per block, +68.4 per message), the
bound would be ≈ 125.94.

## 7. Memory

Msg slices 64Q bytes; Src + Dst 128Q bytes; count tables 2^87 words = 2^92 bytes; per-block scratch
(B3, B4, CS3, CS4, FIX3, TR, DG) < 2^18 bytes. Total ≈ 192Q + 2^92 < 2^135.58 ≤ 2^136.

## 8. Limitations

Constant-factor generic search, with no heuristics, experiments or certificates. The ledger depends on
the v5 reading that the selected permutation may be evaluated in ordinary operations. Every hot-path
count is measured by the shipped simulator, with spare added.

## Appendix A. Program sources (Python 3 stdlib; `ir.py` by winglock, unchanged)

<!-- file: ir.py sha256=877005938fac4f0982553c8eb01b06ef47c2608f66914a61d7cee82920abf055 -->
```python
"""SSA IR, straight-line compiler (store-to-load forwarding under a register
budget, scratch dead-store elimination, interval-colouring register
allocation) and a counted 256-bit word-RAM simulator with 64 registers.

Instruction tuple: (op, dst, a, b, imm)
  ld   dst <- MEM[imm]            imm = (array, index): constant address
  st   MEM[imm] <- a
  ldr  dst <- MEM[a]              register-addressed (table)
  str  MEM[a] <- b
  xor/and/or dst <- a op b ; not dst <- ~a
  rot  dst <- rotl256(a, imm)
  andi dst <- a & imm ; cmplt dst <- (a < imm) ; cmpeq dst <- (a == imm)
  add  dst <- a + imm (mod 2^256)
  br   if a: candidate path (out of line), then fall through
Persistent registers 'S' (step counter) and 'C' (table word) live in physical
registers 62 and 63; all other values get registers 0..61.
"""
import heapq

W = (1 << 256) - 1
NREG = 62
PERSIST = ('S', 'C')
SCRATCH = {'ROWIN', 'TR', 'C1S', 'D1', 'O1', 'C2', 'A2P', 'CSS', 'FIXS', 'B3', 'B4', 'B5', 'FIX3', 'FIX4', 'FIX5', 'CS3', 'CS4', 'CS5', 'DL', 'ROWS', 'LR'}


class Bld:
    def __init__(self):
        self.ins = []
        self.tags = []
        self.tag = None
        self.n = 0

    def emit(self, op, a=None, b=None, imm=None, dst=True):
        d = None
        if dst:
            d = self.n
            self.n += 1
        self.ins.append((op, d, a, b, imm))
        self.tags.append(self.tag)
        return d

    def ld(self, arr, i):
        return self.emit('ld', imm=(arr, i))

    def st(self, arr, i, v):
        self.emit('st', a=v, imm=(arr, i), dst=False)

    def xor(self, a, b):
        return self.emit('xor', a, b)

    def and_(self, a, b):
        return self.emit('and', a, b)

    def or_(self, a, b):
        return self.emit('or', a, b)

    def not_(self, a):
        return self.emit('not', a)

    def rot(self, a, k):
        k %= 256
        assert k
        return self.emit('rot', a, imm=k)


def _uses(ins):
    op, d, a, b, imm = ins
    u = []
    if a is not None:
        u.append(a)
    if b is not None:
        u.append(b)
    return u


class SegTree:
    """range add, range max over [0, n)."""

    def __init__(self, vals):
        n = 1
        while n < len(vals):
            n *= 2
        self.n = n
        self.mx = [0] * (2 * n)
        self.lz = [0] * (2 * n)
        for i, v in enumerate(vals):
            self.mx[n + i] = v
        for i in range(n - 1, 0, -1):
            self.mx[i] = max(self.mx[2 * i], self.mx[2 * i + 1])

    def add(self, l, r, v, node=1, nl=0, nr=None):
        if nr is None:
            nr = self.n
        if r <= nl or nr <= l or l >= r:
            return
        if l <= nl and nr <= r:
            self.mx[node] += v
            self.lz[node] += v
            return
        m = (nl + nr) // 2
        self.add(l, r, v, 2 * node, nl, m)
        self.add(l, r, v, 2 * node + 1, m, nr)
        self.mx[node] = max(self.mx[2 * node], self.mx[2 * node + 1]) + self.lz[node]

    def query(self, l, r, node=1, nl=0, nr=None):
        if nr is None:
            nr = self.n
        if r <= nl or nr <= l or l >= r:
            return -10 ** 9
        if l <= nl and nr <= r:
            return self.mx[node]
        m = (nl + nr) // 2
        return max(self.query(l, r, 2 * node, nl, m), self.query(l, r, 2 * node + 1, m, nr)) + self.lz[node]


def compile_block(ins, tags=None, nreg=NREG, forward=True):
    """Forward loads, drop dead scratch stores, allocate registers.
    Returns (physical instruction list, high-water register count)."""
    ins = list(ins)
    n = len(ins)
    parent = {}

    def find(v):
        while v in parent and parent[v] != v:
            nxt = parent[v]
            if nxt in parent and parent[nxt] != nxt:
                parent[v] = parent[nxt]
            v = nxt
        return v
    # memval candidates (fixed by program order)
    cand = []           # (p, prev value)
    last = {}
    for p, (op, d, a, b, imm) in enumerate(ins):
        if op == 'ld':
            if imm in last:
                cand.append((p, last[imm]))
            last[imm] = d
        elif op == 'st':
            last[imm] = a
    alive = [True] * n
    forwarded = set()

    def intervals():
        dpos, end = {}, {}
        for p in range(n):
            if not alive[p]:
                continue
            op, d, a, b, imm = ins[p]
            for u in _uses(ins[p]):
                if u in PERSIST:
                    continue
                r = find(u)
                if end.get(r, -1) < p:
                    end[r] = p
            if d is not None and d not in PERSIST and find(d) == d:
                dpos[d] = p
        iv = {}
        for v, p in dpos.items():
            iv[v] = [p, max(end.get(v, p + 1), p + 1)]
        return iv

    # store groups: loads between a store and the next store to the same address
    grp = {}
    cur = {}
    for p, (op, d, a_, b_, imm) in enumerate(ins):
        if op == 'st':
            cur[imm] = p
        elif op == 'ld' and imm in cur:
            grp.setdefault(cur[imm], []).append(p)
    gsize = {}
    for sp, lds in grp.items():
        for p in lds:
            gsize[p] = len(lds) if ins[sp][4][0] in SCRATCH else 0
    while forward:
        changed = False
        # 1. free forwards (the previous value is still live at the load)
        iv = intervals()
        for p, pv in cand:
            if p in forwarded:
                continue
            r = find(pv)
            l = ins[p][1]
            if iv[r][1] > p:
                iv[r][1] = max(iv[r][1], iv[l][1])
                parent[l] = r
                del iv[l]
                alive[p] = False
                forwarded.add(p)
                changed = True
        # 2. max-weight forwards under the register budget (min-cost flow)
        iv = intervals()
        diff = [0] * (n + 1)
        for s_, e_ in iv.values():
            diff[s_] += 1
            diff[e_] -= 1
        pres, c = [], 0
        for p in range(n):
            c += diff[p]
            pres.append(c)
        if max(pres) > nreg:
            raise RuntimeError("baseline pressure %d exceeds the budget" % max(pres))
        items = []
        for p, pv in cand:
            if p in forwarded:
                continue
            r = find(pv)
            ev = iv[r][1]
            w = 1000 + (1000 // gsize[p] if gsize.get(p) else 0)
            items.append((ev, p, w, pv))
        sel = select_intervals(items, pres, n, nreg)
        for ev, p, w, pv in sel:
            r = find(pv)
            l = ins[p][1]
            parent[l] = r
            alive[p] = False
            forwarded.add(p)
            changed = True
        # 3. dead scratch stores
        nextld = {}
        for p in range(n - 1, -1, -1):
            op, d, a_, b_, imm = ins[p]
            if op == 'ld' and alive[p]:
                nextld[imm] = True
            elif op == 'st':
                if alive[p] and imm[0] in SCRATCH and not nextld.get(imm, False):
                    alive[p] = False
                    changed = True
                nextld[imm] = False
        if not changed:
            break
    # rewrite
    out = []
    otags = []
    for p in range(n):
        if not alive[p]:
            continue
        op, d, a, b, imm = ins[p]
        a2 = a if a in PERSIST or a is None else find(a)
        b2 = b if b in PERSIST or b is None else find(b)
        out.append((op, d, a2, b2, imm))
        otags.append(tags[p] if tags else None)
    # check: every scratch load is preceded by a live store in the block
    written = set()
    for op, d, a, b, imm in out:
        if op == 'st':
            written.add(imm)
        elif op == 'ld' and imm[0] in SCRATCH and imm not in written:
            raise RuntimeError("scratch load before store: %r" % (imm,))
    code, hw = allocate(out, nreg)
    return code, hw, otags


def select_intervals(items, pres, n, nreg):
    """Max-weight subset of intervals [a, b) (items (a, b, w, key)) such that
    pres[x] + #chosen covering x <= nreg everywhere (exact, min-cost flow)."""
    items = [it for it in items if it[0] < it[1]]
    if not items:
        return []
    coords = sorted({0, n} | {it[0] for it in items} | {it[1] for it in items})
    idx = {c: i for i, c in enumerate(coords)}
    m = len(coords)
    INF = float('inf')
    to, cap, cost, adj = [], [], [], [[] for _ in range(m)]

    def add(u, v, c, w):
        adj[u].append(len(to)); to.append(v); cap.append(c); cost.append(w)
        adj[v].append(len(to)); to.append(u); cap.append(0); cost.append(-w)
    M = 10 ** 9
    for i in range(m - 1):
        bm = max(pres[coords[i]:coords[i + 1]])
        add(i, i + 1, bm, -M)
        add(i, i + 1, nreg - bm, 0)
    ie = []
    for it in items:
        ie.append(len(to))
        add(idx[it[0]], idx[it[1]], 1, -it[2])
    # potentials: DAG shortest paths (all original edges go forward)
    pot = [INF] * m
    pot[0] = 0
    for u in range(m):
        if pot[u] == INF:
            continue
        for e in adj[u]:
            if cap[e] > 0 and pot[u] + cost[e] < pot[to[e]]:
                pot[to[e]] = pot[u] + cost[e]
    flow = 0
    while flow < nreg:
        dist = [INF] * m
        prev = [-1] * m
        dist[0] = 0
        h = [(0, 0)]
        while h:
            d, u = heapq.heappop(h)
            if d > dist[u]:
                continue
            pu = pot[u]
            for e in adj[u]:
                if cap[e] > 0:
                    v = to[e]
                    nd = d + cost[e] + pu - pot[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        prev[v] = e
                        heapq.heappush(h, (nd, v))
        if dist[m - 1] == INF:
            break
        for v in range(m):
            if dist[v] < INF:
                pot[v] += dist[v]
        f = nreg - flow
        v = m - 1
        while v != 0:
            e = prev[v]
            f = min(f, cap[e])
            v = to[e ^ 1]
        v = m - 1
        while v != 0:
            e = prev[v]
            cap[e] -= f
            cap[e ^ 1] += f
            v = to[e ^ 1]
        flow += f
    return [it for it, e in zip(items, ie) if cap[e] == 0]


def allocate(ins, nreg):
    n = len(ins)
    dpos, end = {}, {}
    for p, x in enumerate(ins):
        for u in _uses(x):
            if u in PERSIST:
                continue
            end[u] = p
        d = x[1]
        if d is not None and d not in PERSIST:
            if d in dpos:
                raise RuntimeError("SSA violated")
            dpos[d] = p
    starts = sorted((p, v) for v, p in dpos.items())
    free = list(range(nreg))[::-1]
    import heapq as hq
    act = []
    reg = {}
    hw = 0
    for p, v in starts:
        e = max(end.get(v, p + 1), p + 1)
        while act and act[0][0] <= p:
            _, r = hq.heappop(act)
            free.append(r)
        if not free:
            raise RuntimeError("register budget exceeded at %d" % p)
        r = free.pop()
        reg[v] = r
        hq.heappush(act, (e, r))
        hw = max(hw, len(act))
    phys = {'S': 62, 'C': 63}

    def R(v):
        if v is None:
            return None
        if v in phys:
            return phys[v]
        return reg[v]
    out = [(op, R(d), R(a), R(b), imm) for op, d, a, b, imm in ins]
    return out, hw


class Machine:
    """Counted simulator: 64 registers of 256 bits, word memory (dict)."""

    def __init__(self, layout):
        self.reg = [None] * 64
        self.mem = {}
        self.layout = layout      # array name -> base address
        self.count = 0
        self.hist = {}
        self.cand_hook = None
        self.units = 0

    def mem_get(self, a):
        if a not in self.mem:
            import random
            self.mem[a] = random.Random(a).getrandbits(256)
        return self.mem[a]

    def addr(self, imm):
        return self.layout[imm[0]] + imm[1]

    def run(self, code):
        reg, mem = self.reg, self.mem
        cnt = 0
        hist = self.hist
        for op, d, a, b, imm in code:
            cnt += 1
            hist[op] = hist.get(op, 0) + 1
            if op == 'ld':
                reg[d] = mem[self.addr(imm)]
            elif op == 'st':
                mem[self.addr(imm)] = reg[a]
            elif op == 'xor':
                reg[d] = reg[a] ^ reg[b]
            elif op == 'and':
                reg[d] = reg[a] & reg[b]
            elif op == 'or':
                reg[d] = reg[a] | reg[b]
            elif op == 'not':
                reg[d] = reg[a] ^ W
            elif op == 'rot':
                x = reg[a]
                reg[d] = ((x << imm) | (x >> (256 - imm))) & W
            elif op == 'ldr':
                reg[d] = self.load_table(reg[a]) if imm is None else self.mem_get(reg[a])
            elif op == 'str':
                if imm == 'mem':
                    mem[reg[a]] = reg[b]
                else:
                    self.store_table(reg[a], reg[b])
            elif op == 'cmplt':
                reg[d] = 1 if reg[a] < imm else 0
            elif op == 'add':
                reg[d] = (reg[a] + imm) & W
            elif op == 'br':
                if reg[a]:
                    self.count += cnt
                    cnt = 0
                    self.cand_hook(self, b, imm)
            elif op == 'shr':
                reg[d] = reg[a] >> imm
            elif op == 'shl':
                reg[d] = (reg[a] << imm) & W
            elif op == 'andi':
                reg[d] = reg[a] & imm
            elif op == 'addr':
                reg[d] = (reg[a] + reg[b]) & W
            elif op == 'cmpeq':
                reg[d] = 1 if reg[a] == reg[b] else 0
            elif op == 'rand':
                reg[d] = self.rng.getrandbits(256)
            elif op == 'xori':
                reg[d] = reg[a] ^ imm
            elif op == 'hash':
                cnt -= 1
                self.units += 1
                reg[d] = self.hashfn(reg[a], reg[b])
            elif op == 'hash4':
                cnt -= 1
                self.units += 1
                reg[d] = self.hashfn(*[reg[r] for r in imm])
            elif op == 'ldi':
                reg[d] = self.mem_get(self.layout[imm[0]] + imm[1])
            else:
                raise RuntimeError(op)
        self.count += cnt

    def load_table(self, k):
        return self.table_get(k)

    def store_table(self, k, v):
        self.table_put(k, v)
```

<!-- file: bsk5.py sha256=9997ca97323b4eb1701e1cf4b5e4c7c0d1ef0685807bf6615faf0eb5c7c0036f -->
```python
"""Bitsliced 6-round SHA3-256 for 256 messages per block, with static polarity
tracking (lane complementing, after tekkac b001199a). Every SSA value is held
as (physical, neg), so a NOT costs nothing. Chi's ~b & c needs a NOT only when
the operand polarities disagree. The digest slices come out XORed with a fixed
known mask POL (the same for every message), so digest equality is unchanged.
The compiler/simulator is ir.py from winglock 7e40f784 (credited)."""
import ir
W = ir.W
RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001]
RHO = (0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,41,45,15,21,8,18,2,61,56,14)

class V:                       # value: const c in {0,1} (word all-0/all-1), or (ref) or (ssa id, neg)
    __slots__ = ('c', 'r', 'id', 'neg')
    def __init__(s, c=None, r=None, id=None, neg=0):
        s.c, s.r, s.id, s.neg = c, r, id, neg

class G:
    def __init__(s):
        s.B = ir.Bld()
        s.nc = {}
    def mat(s, v):             # make physical
        if v.r is not None:
            arr, i, neg = v.r
            return V(id=s.B.ld(arr, i), neg=neg)
        return v
    def xor(s, a, b):
        if a.c is not None and b.c is not None: return V(c=a.c ^ b.c)
        if a.c is not None: b = s.mat(b); return V(id=b.id, neg=b.neg ^ a.c)
        if b.c is not None: a = s.mat(a); return V(id=a.id, neg=a.neg ^ b.c)
        a = s.mat(a); b = s.mat(b)
        return V(id=s.B.xor(a.id, b.id), neg=a.neg ^ b.neg)
    def not_(s, a):
        if a.c is not None: return V(c=1 - a.c)
        if a.r is not None: return V(r=(a.r[0], a.r[1], a.r[2] ^ 1))
        return V(id=a.id, neg=a.neg ^ 1)
    def andv(s, x, y):         # actual x & y
        if x.c is not None: return y if x.c else V(c=0)
        if y.c is not None: return x if y.c else V(c=0)
        x = s.mat(x); y = s.mat(y)
        if x.neg == 0 and y.neg == 0: return V(id=s.B.and_(x.id, y.id), neg=0)
        if x.neg == 1 and y.neg == 1: return V(id=s.B.or_(x.id, y.id), neg=1)   # ~p & ~q = ~(p|q)
        if x.neg == 1: x, y = y, x        # now x.neg 0, y.neg 1: x & ~q
        # x & ~q = ~(~x | q): one physical NOT on x
        # choose which operand to complement: prefer one already complemented (cache)
        if x.id in s.nc:
            return V(id=s.B.or_(s.nc[x.id], y.id), neg=1)
        if y.id in s.nc:                  # x & ~q with q' = ~q physical: x & q' -> and
            return V(id=s.B.and_(x.id, s.nc[y.id]), neg=0)
        nx = s.B.not_(x.id); s.nc[x.id] = nx
        return V(id=s.B.or_(nx, y.id), neg=1)
    def store(s, arr, i, v):
        if v.c is not None: return v
        v = s.mat(v)
        s.B.st(arr, i, v.id)
        return V(r=(arr, i, v.neg))

def build(transpose=True):
    g = G()
    cur = {}
    for l in range(25):
        for z in range(64):
            if l < 8: cur[(l, z)] = V(r=('M', 64 * l + z, 0))
            elif l == 8: cur[(l, z)] = V(c=1 if z in (1, 2) else 0)
            elif l == 16: cur[(l, z)] = V(c=1 if z == 63 else 0)
            else: cur[(l, z)] = V(c=0)
    pol = {}
    src = {}
    for y in range(5):
        for x in range(5):
            src[y + 5 * ((2 * x + 3 * y) % 5)] = (x, y, RHO[x + 5 * y])
    # round-0 theta materialized (input is the message state)
    C = {}
    for x in range(5):
        for z in range(64):
            v = V(c=0)
            for y in range(5): v = g.xor(v, cur[(x + 5 * y, z)])
            C[(x, z)] = g.store('CS3', 64 * x + z, v)
    D0 = {}
    for x in range(5):
        for z in range(64):
            D0[(x, z)] = g.store('CS4', 64 * x + z, g.xor(C[((x - 1) % 5, z)], C[((x + 1) % 5, (z - 1) % 64)]))
    T = None; FIX = None
    for r in range(6):
        last = r == 5
        def inp(L, z, r=r, T=T, FIX=FIX):
            if r == 0:
                return g.xor(cur[(L, z)], D0[(L % 5, z)])
            v = T[(L, z)]
            if z == 0: v = g.xor(v, FIX[L % 5])
            return v
        out = 'B3' if r % 2 == 0 else 'B4'
        newT = {}; Cprev = None; Cfirst = None
        order = [z0 + 8 * k for z0 in range(8) for k in range(8)] if last else list(range(64))
        grp = {}
        for z in order:
            outs = {}
            for y in ([0] if last else range(5)):
                m = []
                for x in range(5):
                    sx, sy, ro = src[x + 5 * y]
                    m.append(g.mat(inp(sx + 5 * sy, (z - ro) % 64)))
                for x in range(5):
                    if last and x > 3: continue
                    v = g.xor(m[x], g.andv(g.not_(m[(x + 1) % 5]), m[(x + 2) % 5]))
                    if x + 5 * y == 0 and (RC[r] >> z) & 1: v = g.not_(v)
                    outs[x + 5 * y] = v
            if last:
                for L in range(4):
                    v = outs[L]; v = g.mat(v) if v.c is None else v
                    assert v.c is None
                    grp[64 * L + z] = v.id; pol[64 * L + z] = v.neg
                if len(grp) == 32:      # fused transpose stages 128..8 in registers
                    for s_ in (128, 64, 32, 16, 8):
                        mask = sum(1 << k for k in range(256) if not (k // s_) % 2)
                        for j in sorted(grp):
                            if (j // s_) % 2: continue
                            a = grp[j]; b = grp[j + s_]
                            t = g.B.emit('andi', g.B.xor(g.B.emit('shr', a, imm=s_), b), imm=mask)
                            grp[j + s_] = g.B.xor(b, t)
                            grp[j] = g.B.xor(a, g.B.emit('shl', t, imm=s_))
                    for j, v in grp.items(): g.B.st('TR', j, v)
                    grp = {}
                continue
            outs = {L: (g.mat(v) if v.c is None else v) for L, v in outs.items()}
            Cz = {}
            for x in range(5):
                v = V(c=0)
                for y in range(5): v = g.xor(v, outs[x + 5 * y])
                Cz[x] = g.mat(v) if v.c is None else v
            for x in range(5):
                Dx = Cz[(x - 1) % 5] if z == 0 else g.xor(Cz[(x - 1) % 5], Cprev[(x + 1) % 5])
                for y in range(5):
                    L = x + 5 * y
                    newT[(L, z)] = g.store(out, 64 * L + z, g.xor(outs[L], Dx))
            Cprev = Cz
        if not last:
            FIX = {x: g.store('FIX3', x, Cprev[(x + 1) % 5]) for x in range(5)}
            T = newT
    if transpose:
        s_ = 4
        while s_:
            mask = 0
            for k in range(256):
                if not (k // s_) % 2: mask |= 1 << k
            for j in range(256):
                if (j // s_) % 2: continue
                a = g.B.ld('TR', j); b = g.B.ld('TR', j + s_)
                t = g.B.emit('andi', g.B.xor(g.B.emit('shr', a, imm=s_), b), imm=mask)
                dst = 'DG' if s_ == 1 else 'TR'
                g.B.st(dst, j + s_, g.B.xor(b, t))
                g.B.st(dst, j, g.B.xor(a, g.B.emit('shl', t, imm=s_)))
            s_ //= 2
    POL = sum(pol[j] << j for j in range(256))
    return g.B, POL

if __name__ == '__main__':
    import time, pickle; t0 = time.time()
    B, POL = build()
    code, hw, _ = ir.compile_block(B.ins, B.tags)
    hist = {}
    for c in code: hist[c[0]] = hist.get(c[0], 0) + 1
    print('compiled', len(code), 'hw', hw, hist, '%.0fs' % (time.time() - t0), flush=True)
    pickle.dump((code, POL), open('code5.pkl', 'wb'))
```

<!-- file: check5.py sha256=1618c6b94360dd8aa662bf63c5e74801002b6ad3da458c8f93e21df3bd58d117 -->
```python
import sys,pickle,random,os; d=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,d); sys.path.insert(0,sys.argv[1])
import ir
from verifier.keccak import sha3_256
code,POL=pickle.load(open(os.path.join(d,sys.argv[2]),'rb'))
lay={a:i*4096 for i,a in enumerate(['M','B3','B4','CS3','CS4','TR','DG','FIX3'])}
n=int(sys.argv[3]) if len(sys.argv)>3 else 4
for seed in range(n):
    rng=random.Random(1000+seed); msgs=[rng.getrandbits(512) for _ in range(256)]
    m=ir.Machine(lay)
    for w in range(512): m.mem[lay['M']+w]=sum(((msgs[k]>>w)&1)<<k for k in range(256))
    m.run(code)
    for k in range(256):
        assert m.mem[lay['DG']+k]^POL==int.from_bytes(sha3_256(msgs[k].to_bytes(64,'little'),6),'little'),(seed,k)
    print('seed',seed,'ok',m.count,flush=True)
print('ALL OK', n*256, 'digests; POL=%064x'%POL)
```
