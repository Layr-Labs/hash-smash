# SHA3-256 prefix rounds 0-5: generic distinguished-point collision search

Lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Cost model: `collision-frontier-v5`, C = 1626.
A six-round PERM6 call costs 1 unit; any other word operation 1/1626.

## 0. Summary

| claim.json field | value |
| --- | --- |
| `time_log2` | 127.9944 (worst case 2^127.99439380 in every run, rounded up; Sec. 6) |
| `success_probability` | 0.39 (bound 0.3900000103815 under H-RF; Sec. 5) |
| `memory_log2_bytes` | 112 (at most 2^111.81 + 2^19 bytes; Sec. 7) |
| `preprocessing_log2` / advice | 0 (setup <= 39 operations, inside T) / 0 (zero bytes) |
| certificates / experiments | none / none declared |

**Method.** The generic birthday attack: van Oorschot-Wiener distinguished-point collision search
(J. Cryptology 12(1):1-28, 1999) on one processor. The step map f sends a 256-bit word x to the
six-round SHA3-256 digest of the 32-byte message LE32(x). Chains start at uniform words and stop at
the first output with lane 0 below 2^32 (a DP); (start, length) is stored in a trie keyed by the DP.
The first repeated DP triggers one RELOCATE walk that returns two distinct inputs with equal
images. Budget: K0 = 8340625 * 2^105 = 0.99428 * 2^128 main-loop evaluations. No cryptanalytic
advance is claimed; `sha3-256-r6-nominal-v2` names the organizer reference only.

**Relation to our accepted package 1e370c6c (128.014).** Same algorithm family, target, step map,
trie, RELOCATE, H-RF and evidence; only the accounting is tighter. (a) PERM6 is called out of
place: it reads its 25 operand registers and never writes them, so the 21 constant lanes are written
once, at setup (1e370c6c paid 21 rewrites per evaluation). (b) The DP test is compare plus branch.
(c) The loop is unrolled 256 times; K0 is on the 2^105 grid. Operations per evaluation drop from
403/16 to 771/256. **The edge below 128.0 depends on convention (a)**, which
Section 2 and the Appendix show to be the reference data path that defines C. Under the strict
per-call reading (the constant lanes are rewritten before every call), the same algorithm scores
log2 T = 128.01287, and that reading is covered by 1e370c6c.

**Verification checklist** (every number can be recomputed from this file):

1. C = 1626 (`scripts/reference_operation_costs.py`). The Appendix trace of
   `verifier/keccak.py:_permute_lanes` finds 1626 operations, inputs unchanged, peak 35 live values.
2. Per main-loop evaluation: 1 issue + 2 (compare, branch) + 3/256 block control = 771/256 ops.
3. Per-chain work outside evaluations <= 11 + 3837 = 3848 ops, charged as 2^13 (Sec. 3).
4. Chains <= 2^98 (record cap) + 2^88 (abandoned) + 1.
5. K0 = 0.99427998065948486328125 * 2^128, so log2 K0 = 128 - 0.008275935421.
6. With N = 2^256, K0^2/(2N) = 69566025390625/2^47 = 0.494296339970112797. This exceeds
   -ln 0.61 = 0.494296321814780119 by d = 1.81553e-8.
7. B1 <= 4.621476e-10, B2 <= 2.310738e-10, B3 <= 2.03e-27, B4 < 2^-(2^97), so
   eps = 6.932214e-10 (Sec. 5.3).
8. Success >= 1 - exp(-K0(K0+1)/(2N)) - eps = 0.3900000103815. K0 = 8340624 * 2^105 gives
   0.3899999381.
9. log2 T <= log2 K0 + log2(417027/416256) + 2^-27.66/ln 2
   = 127.991724065 + 0.002669725 + 0.000000007. The exact sum is 127.99439379630 (Sec. 6).
10. Strict per-call reading: 771/256 + 21 operations per evaluation gives log2 T = 128.01287308.
11. Memory: 2^98 keys * 224 nodes * 2 words * 32 bytes = 2^111.8074 bytes (Sec. 7).

## 1. Target and step map

msg(x) = LE32(x) (exactly 32 little-endian bytes) is injective. Rate 1088, capacity 512, zero IV,
suffix 0x06 with pad10*1, 256-bit output: a 32-byte message pads to the one block
m || 06 || 00^102 || 80 (one PERM6, no squeeze permutation, no feed-forward). The input state has
the lanes of x in A[0..3], A[4] = 0x06, A[16] = 2^63 and 0 elsewhere, so A[4..24] is fixed. PERM6 is
Keccak-f[1600] rounds 0-5 (prefix convention: theta, rho, pi, chi, iota with RC[0..5] = 0x1,
0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001; exactly as defined by the
organizer's `verifier/keccak.py`). f(x) = A[0] + 2^64 A[1] + 2^128 A[2] + 2^192 A[3]
after PERM6, so LE32(f(x)) is the digest of msg(x), and x != x' with f(x) = f(x') is an ordinary
full-digest collision of two 32-byte messages (Appendix check (4)).

## 2. Machine model and the PERM6 instruction

Probabilistic 256-bit word RAM, fewer than 128 registers. Load, store, add, sub, AND, OR, XOR, NOT,
constant shift, compare, conditional branch and RAND each cost 1/1626. As in 1e370c6c, a jump, a
move and an immediate write cost one operation each, and every memory access is charged. Code is
counted in memory; no memory is read before it is written.

Lanes are held in the low 64 bits of registers. `PERM6(in: I0..I24; out: O0..O3)` applies the six
rounds, writes lanes 0..3 to O0..O3 and lanes 4..24 to private scratch, and never writes I0..I24.
It costs 1 unit plus 1 charged issue operation. Why this is exactly the organizer's normalization:

* C counts the data-word operations of `_permute_lanes` (`scripts/reference_operation_costs.py`);
  `docs/RESCORING.md` excludes memory traffic. Each counted operation yields a new value
  (`lanes[i] = ...` only rebinds a slot), so the priced data path never destroys its inputs. The
  Appendix trace confirms 1626 operations, unchanged inputs and peak 35 live values; straight-line
  code needs that many registers and no moves. So the call is the 1626 reference operations in 35
  scratch registers, with lanes 0..3 computed directly into O0..O3. Out-of-place is therefore the
  reference's own SSA data path, not an added discount: an in-place realisation of the same 1626
  operations would have to add writes that overwrite the I-registers, which the reference never does.
* Round 1 reads A[0..24] only through the theta parities and the A ^ D terms. Out of place, the
  operations are the same and only the destinations change. Per `docs/RESCORING.md`, "a whole
  compression's internals must not also be charged individually".
* Register-resident PERM6 with no lane load or store is the convention accepted in 1e370c6c.
* To be conservative, the setup writes the 64-bit mask and six round constants (immediates in the
  reference) into R0..R6 once (7 charged operations).

So the constant lanes live in K4..K24 (K4 = 6, K16 = 2^63, the rest 0), written once at setup.

## 3. Parameters and program, with operation counts

DP: output lane 0 < 2^32 (digest bytes 4..7 zero), theta = 2^-32. Maximum chain L = 2^40 =
256 * 2^32. Budget K0 = 8340625 * 2^105. Record cap Dcap = 2^98. Registers (93): K4..K24, lane
banks P0..P3 and Q0..Q3, 15 scalars (g = evaluations of completed chains, r = records, free, cnt, s,
off, len, key, node, i, b, c, p, created, t), Z0..Z3, M64, T32, K0, 35 PERM6 scratch, R0..R6. ROOT
is a two-word node at a nonzero address.

| block | instructions | ops |
| --- | --- | ---: |
| setup | ROOT[0..1] = 0; M64, T32, K0; free, g = 0, r = 0; K4..K24; R0..R6 | 36 |
| CHAIN | if g >= K0 halt fail (2); s = RAND; P0..P3 = lanes of s by shift/AND (6); cnt = 2^32; jump | 11 |
| copy k (odd) | `PERM6(in: P0..P3, K4..K24; out: Q0..Q3)`; if Q0 < T32 goto DP_k | 1 unit + 3 |
| copy k (even) | the same with P and Q exchanged | 1 unit + 3 |
| after copy 256 | cnt -= 1; if cnt != 0 goto BLOCK | 3 per 256 evaluations |
| ABANDON | g += L; goto CHAIN | 2 |
| DP_k stub | off = k; Z0..Z3 = outputs of copy k (4 moves); goto DPFOUND | 6 |
| DPFOUND head | len = ((2^32 - cnt) << 8) + off (4); g += len; key = pack(Z3..Z0) (6) << 32; node = ROOT; i = 224 | 14 |
| trie level (x224) | b = key >> 255; key <<= 1; p = node + b; c = load [p]; if c == 0 goto ALLOC (6); created = 0, jump (2) or ALLOC (7) | |
| | ALLOC: c = free; store [c] = 0; t = c + 1; store [t] = 0; free += 2; store [p] = c; created = 1 | |
| | JOIN: node = c; i -= 1; if i != 0 goto LEVEL (4) | <= 17 |
| old key | if created goto NEWKEY (2); s', len' = load [node], [node + 1] (3); goto RELOCATE | 6 |
| NEWKEY | (2); store s, len at [node], [node + 1] (3); r += 1; if r == Dcap halt fail; goto CHAIN | 9 |

DPFOUND with stub costs at most 6 + 14 + 224 * 17 + 9 = 3837, so a chain costs at most
11 + 3837 = 3848 < 2^12 operations besides evaluations and block control; we charge 2^13. A copy's
operands are the previous outputs plus the untouched K4..K24, exactly the padded block of the
current point. Every evaluation is DP-tested, so a chain stops at its first DP, or is abandoned
after L evaluations and stores nothing. A DP in copy k of block j has len = 256(j - 1) + k. As
Z0 < 2^32, the 224 high bits of the shifted key determine z. Address 0 never occurs and only full
insertions create nodes, so the last level creates a node exactly when z is new; otherwise the leaf
holds the earlier (s', len').

RELOCATE: with (s1, l1) the longer chain, set a = s1 advanced l1 - l2 steps and b = s2. Repeat at
most l2 times: if a == b, halt (fail); if f(a) == f(b), go to OUTPUT(a, b); else a = f(a),
b = f(b). Then halt (fail). Each f costs 1 unit + 13 ops (6 split, 1 issue, 6 pack), under 64 with
loop control; at most 2L evaluations, charged as 3L. OUTPUT recomputes f(a), f(b), checks a != b and
all 256 bits, and writes msg(a), msg(b): 2 units + at most 200 ops. One run, no restart; the run
halts at its first RELOCATE.

## 4. Every output is a valid collision (unconditional)

OUTPUT is reached only after it has verified a != b and f(a) = f(b) by recomputation. By Section 1,
msg(a) and msg(b) are distinct and collide on all 256 bits.

## 5. Success probability under H-RF

**H-RF** (declared in claim.json): when the algorithm evaluates f at a point it has not evaluated
before, the output is uniform on {0,1}^256 and independent of the coins and of every value seen so
far. This is the standard van Oorschot-Wiener premise, as in 1e370c6c, used only in this section.

### 5.1 Definitions and Lemma 1

p_j is the input of main-loop evaluation j, and V_j = {p_1..p_j} together with
{f(p_1)..f(p_{j-1})}. Evaluation j makes contact if f(p_j) is in V_j, and tau is the first contact.
Before tau, every non-start input is a fresh previous output.

**Lemma 1.** Pr(no contact in evaluations 1..K0 and no B1) <= exp(-K0(K0+1)/(2N)). *Proof.* Given no
earlier contact and a fresh start, p_j is unevaluated, so f(p_j) is uniform. V_j holds j distinct
inputs, so the step survives with probability at most 1 - j/N. Take the product and use
1 - u <= e^-u. Chains start while g < K0, so all K0 evaluations run unless B4 halts the run.

### 5.2 Chain count

S = chains started before tau within K0 evaluations. Each later start follows a DP (probability
theta per fresh output) or an abandonment (L evaluations), so
E[S] <= 1 + K0 theta + K0/L = 2^96 (0.99427998065948486328125 (1 + 2^-8) + 2^-96)
= 0.998163886834 * 2^96. At every start, |V| <= 2 K0 = 1.98856 * 2^128.

### 5.3 Bad events

| event | meaning | bound | value |
| --- | --- | --- | --- |
| B1 | a start drawn before tau lies in V | E[S] 2K0/N | 4.621476e-10 |
| B2 | first contact on a start or on the current chain (incl. a fixed point) | K0 (E[S] + L)/N | 2.310738e-10 |
| B3 | a chain before tau has L/2 consecutive non-DP outputs | E[S] e^(-theta L/2) = E[S] e^-128 | 2.03e-27 |
| B4 | Dcap reached first; X ~ Bin(K0, theta), mu < 2^96, a = 2^98 - 1 >= 4 mu | Chernoff (e/4)^a | < 2^-(2^97) |

eps = 6.932214e-10 < 7.0e-10. Without B3, every chain before tau (and the current one up to
contact) has length at most L/2. Before tau, chains are disjoint, so stored DPs are distinct.

### 5.4 Lemma 2: contact at tau <= K0 with no B1-B4 yields a collision

Let the current chain's a-th evaluation hit v = f(x_{a-1}). Without B2, B3, v is a non-start point
c'_b (b >= 1) of an earlier completed chain (s', l'), and x_{a-1} != c'_{b-1} (x_{a-1} was
unevaluated). As f is deterministic, the chain follows c' to its DP z', has length a + l' - b < L,
and DPFOUND finds leaf (s', l'). x_0..x_{a-1} are disjoint from c' (x_0 fresh by no B1, the rest
fresh outputs). RELOCATE aligns both walks at distance min(l_c, l') from z'; until v, one walk is on
some x_i (i < a) and the other on c', so a == b never fires. Both then reach v from the distinct
pair (x_{a-1}, c'_{b-1}), and OUTPUT succeeds. No other chain completes in between.

### 5.5 Result

Pr(success) >= 1 - exp(-K0(K0+1)/(2N)) - eps, where K0(K0+1)/(2N) - K0^2/(2N) < 2^-129. With d as
in item 6, exp(-K0(K0+1)/(2N)) <= 0.61 e^-d < 0.61 - 1.1074e-8. Hence

    Pr(success) > 0.39 + 1.1074e-8 - 7.0e-10 > 0.39 + 1.03e-8   (80 digits: 0.3900000103815)

The margin is small by design but exact (rounded against us). K0 is the smallest multiple of 2^105
reaching 0.39. The probability is over the algorithm's coins under H-RF, not a confidence level.

## 6. Total charged time (worst case, every run)

| term | count | units each | log2 of term |
| --- | --- | --- | ---: |
| main-loop evaluations | K0 - 1 + L | 1 + 771/(256 * 1626) = 417027/416256 | 127.99439 |
| per-chain work | 2^98 + 2^88 + 1 chains | 2^13/1626 | 100.3343 |
| RELOCATE (at most one) | 3L | 1 + 64/1626 | 41.6407 |
| OUTPUT and setup | 1 | 2 + 239/1626 | 1.10 |

Worst-case counts: a chain starts only while g < K0 and makes at most L evaluations; block control
is at most 3/256 per evaluation in every chain; at most Dcap chains store a record and at most
(K0 - 1 + L)/L < 2^88 + 1 are abandoned. Terms 2-4 sum to below 2^-27.66 of K0 * 417027/416256,
and K0 - 1 + L < K0 (1 + 2^-87.99). So

    log2 T <= log2 K0 + log2(417027/416256) + 2^-27.66/ln 2
            = (128 - 0.0082759354) + 0.0026697250 + 0.0000000071 = 127.9943937967
    80-digit exact sum: 127.99439379630.  time_log2: 127.9944 (rounded up)

No lane is loaded, stored, moved or rewritten per evaluation. Each extra operation per evaluation
adds about 0.00089 bits. **Strict per-call reading:** rewriting the 21 constant lanes before each
call gives the factor 1 + (771/256 + 21)/1626 and log2 T = 128.01287308, above 128.0; our accepted
1e370c6c (128.014) satisfies that reading. Nothing is precomputed, searched or repeated.

## 7. Memory, preprocessing, advice

Each new key allocates at most 224 two-word nodes (the leaf holds (s, len)): 2^98 * 14336 bytes =
2^111.8074. Registers, ROOT, output buffer and code (under 2600 instructions of <= 4 words) take
under 2^19 bytes, so M < 2^112. Preprocessing is the setup (<= 39 ops, already in T). Advice is zero
bytes; 0 (one byte) is a conservative bound since log2 0 is not encodable. `data_log2` is omitted.

## 8. Evidence for H-RF (our own reduced-output experiments)

Our own runs for 1e370c6c, reused since f and H-RF are unchanged; not organizer-run (no experiment
manifest); no number here enters Section 5. Program: the deterministic C source in Appendix A of
1e370c6c's proof, SHA-256 `273e5fc67dcb82b0fa4c3d4da1c2b19468401a222b93f8df1be7bc26178d32ee`.
Arguments: n, t, trials, threads, track flag, c = 0.9944, log2 L = t + 5, seed, rounds. It runs the
DP search on f_n (low n bits of lane 0 of the real six-round map on n-bit inputs) with uniform n-bit
starts, a hash map, no record cap, K0 = ceil(0.9944 * 2^(n/2)), DP = low t bits zero and
L = 2^(t+5). Control: keyed 24-round Keccak-f[1600] (random A[5] per trial). The DP predicate (only
its density matters) and the calling convention change no value of f. Prediction
1 - exp(-K0(K0+1)/2^(n+1)) = 0.3903 (n = 24), 0.3901 (n >= 32). Contact includes starts landing on
visited points (B1). Semantics: f_n(x) = low n bits of lane 0 after PERM6 on the padded block of the
32-byte message LE32(x) with x zero-extended from n bits; starts come from per-thread splitmix64
streams seeded from `seed`; the control keys lane A[5] with a random word per trial; after alignment
RELOCATE tests a == b once (not before every step), which gives the same outcome for a deterministic f.

| run | n | t | rounds | trials | threads | seed | contact <= K0 | success |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 24 | 4 | 6 | 2000 | 14 | 7 | 852 (0.4260) | 751 (0.3755) |
| 2 | 24 | 4 | 24 ctrl | 2000 | 14 | 7 | 843 (0.4215) | 756 (0.3780) |
| 3 | 32 | 8 | 6 | 20000 | 14 | 11 | 7774 (0.3887) | 7759 (0.3880) |
| 4 | 32 | 8 | 24 ctrl | 20000 | 14 | 12 | 7917 (0.3958) | 7852 (0.3926) |
| 5 | 40 | 10 | 6 | 5000 | 14 | 21 | 2025 (0.4050) | 2025 (0.4050) |
| 6 | 40 | 10 | 24 ctrl | 5000 | 14 | 22 | 1983 (0.3966) | 1976 (0.3952) |
| 7 | 48 | 12 | 6 | 1000 | 14 | 31 | - | 372 (0.3720) |
| 8 | 48 | 12 | 24 ctrl | 1000 | 14 | 32 | - | 386 (0.3860) |
| 9 | 32 | 8 | 6 | 20000 | 12 | 777 | 7822 (0.3911) | 7775 (0.3887) |
| 10 | 32 | 8 | 24 ctrl | 20000 | 12 | 778 | 7865 (0.3932) | 7788 (0.3894) |
| 11 | 48 | 12 | 6 | 2000 | 14 | 33 | - | 793 (0.3965) |

"-" = not measured (the program keeps the visited set only for n <= 40).

All runs are listed, none discarded. Runs 3-8 were launched together, 9-10 re-ran n = 32 with fresh
seeds, 11 was added after 7. Rows other than 7, 8, 11 were regenerated bit-exactly. Six-round
z-scores against the prediction: -1.36, -0.62, +2.16, -1.17, -0.39, +0.59 (runs 1, 3, 5,
7, 9, 11; binomial standard errors 0.0109, 0.0034, 0.0069, 0.0154, 0.0034, 0.0109) and -0.20 for
n = 48 pooled. Start collisions (B1) occurred in 97 and 89 trials at n = 24 and in under 0.4% of
trials at n = 32 and 40. Against the control, each six-round rate is within 1.01 standard errors of the
difference. Pooled six-round rates are 0.3884 (n = 32) and 0.3883 (n = 48). At these widths B1 and
abandonment are of order 2^-7, so the baseline is the control, which pools to 0.3910 at n = 32
(difference -0.76 standard errors): no departure from random-mapping behaviour. **Limits:**
24-48-bit outputs on n-bit input subsets only; runs cannot exclude a full-width property or
resolve the 1e-8 margin. The 0.39 floor rests on the analytic H-RF bound alone, as in 1e370c6c
(margin 8e-6). Zero-sum and cube-type distinguishers need chosen structured inputs, which a
pseudo-random walk does not choose. **Sensitivity:** a contact-probability shortfall delta at K0
would need K0 larger by about 1 + 1.66 delta to restore 0.39, about 2.4 delta bits.

## 9. Literature status and limitations

No classical sub-birthday collision attack on six-round SHA3-256 is known to us; Guo, Liu, Song and
Tu (ASIACRYPT 2022, ePrint 2022/184) give only quantum ones. The method is van Oorschot-Wiener's;
parameters, program, counts, trace, bounds and arithmetic are ours. The certificate manifest is
empty. `plausible_not_refuted` is neither a mathematical proof nor human acceptance.

## Appendix. SSA trace of the reference PERM6 core (out-of-place call)

Run from the repository root (Python 3.9+). It wraps the organizer's `_permute_lanes`, counts the
operators that `scripts/reference_operation_costs.py` counts, and gives each result a fresh SSA id.

```python
import operator, os, random, sys
sys.path.insert(0, os.getcwd())
from verifier import keccak
TRACE = []  # (out_id, in_ids) per counted op
class V(int):  # data word with SSA id; 0..24 = inputs
    def __new__(cls, value, vid):
        o = int.__new__(cls, value); o.vid = vid; return o
def _op(fn):
    def apply(a, b=None):
        ins = [a.vid] + ([b.vid] if isinstance(b, V) else [])
        out = V(fn(int(a)) if b is None else fn(int(a), int(b)), 25 + len(TRACE))
        TRACE.append((out.vid, ins)); return out
    return apply
for n, fn in {"add": operator.add, "and": operator.and_, "or": operator.or_,
              "xor": operator.xor, "lshift": operator.lshift,
              "rshift": operator.rshift, "invert": operator.invert}.items():
    setattr(V, f"__{n}__", _op(fn)); setattr(V, f"__r{n}__", _op(lambda a, b, fn=fn: fn(b, a)))
CONST = {4: 0x06, 16: 1 << 63}  # padding lanes; the other 19 are 0
def perm6(m):  # 4 message lanes + 21 constant lanes
    TRACE.clear()
    ins = [V(m[i] if i < 4 else CONST.get(i, 0), i) for i in range(25)]
    lanes = list(ins); keccak._permute_lanes(lanes, 64, 6); return ins, lanes
rng = random.Random(1); x = [rng.getrandbits(64) for _ in range(4)]
ins, out = perm6(x)
print("counted operations:", len(TRACE))  # (1)
assert all(o >= 25 for o, _ in TRACE)
assert all(int(ins[i]) == (x[i] if i < 4 else CONST.get(i, 0)) for i in range(25))
print("input lanes unchanged after the call: yes")  # (2)
last = {v: t for t, (_, i) in enumerate(TRACE) for v in i}
last.update({out[k].vid: len(TRACE) for k in range(4)})
live, peak = set(), 0
for t, (o, _) in enumerate(TRACE):
    live.add(o); peak = max(peak, len(live)); live = {v for v in live if last.get(v, -1) > t}
print("peak live internal values:", peak)  # (3)
cur = [rng.getrandbits(64) for _ in range(4)]
for _ in range(200):
    nxt = [int(v) for v in perm6(cur)[1][:4]]
    le = lambda w: b"".join(v.to_bytes(8, "little") for v in w)
    assert le(nxt) == keccak.sha3_256(le(cur), rounds=6); cur = nxt
print("200 chained steps agree with sha3_256(rounds=6): yes")  # (4)
for _ in range(1000):  # (5) DP predicate: lane 0 < 2^32 iff digest bytes 4..7 are zero
    z = rng.getrandbits(64) >> rng.choice((0, 31, 32, 33))
    assert (z < 2**32) == (z.to_bytes(8, "little")[4:8] == bytes(4))
print("DP predicate check: yes")  # (5)
```

Output on the build revision: (1) 1626 = C; (2) inputs unchanged (operand registers only read);
(3) peak 35 (35 scratch registers, no moves); (4) 200 of 200 chained steps match; (5) the DP
predicate "lane 0 below 2^32" equals "digest bytes 4..7 zero".
