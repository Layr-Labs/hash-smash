# SHA3-256 with 6 prefix rounds: a generic low-memory collision search, 256 walks per step in bit-sliced lockstep, time_log2 125.19730

## 1. Claim

Target `sha3-256-r6-prefix-v1`: SHA3-256 (FIPS 202) with Keccak-f rounds 0 to 5 in every permutation call, zero initial
state, rate 136 bytes, suffix 0x06 with pad10*1, the full 256-bit digest. The algorithm below outputs two distinct
one-block messages of 135 bytes with equal complete digests.

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, unit 1626 word operations, rounded up) | 125.19730 (Section 5 and Appendix A) |
| memory | at most 1,108,384 bytes, log2 = 20.0801 (Section 7) |
| score S = time_log2 + max(0, memory_log2 - 20) | 125.2774 |
| success probability | at least 0.39 for one attempt, under the one premise H_rand (Section 6) |
| preprocessing | none; no advice |

The method is generic: it uses no property of the six rounds. It iterates a function f on 256-bit values with an
injective message encoding, follows walks of f to distinguished points, stores the distinguished points in a table of
5,000 words, and replays two walks that end at the same point. Its only declared premise is that f behaves like a
uniformly random function (Section 6). What is new compared with a one-walk-at-a-time implementation (1247.5 operations per
evaluation of f) is how f is evaluated. The word RAM of the cost model has 256-bit words and bitwise operations, so one
operation applies one gate to 256 independent computations. The program advances 256 walks together, one evaluation of f
each per step, in a bit-sliced program: word number (lane, z) holds bit z of Keccak lane `lane` for all 256 walks. A step of
all 256 walks costs 54,009 operations, 210.97 per evaluation of f. The state of 25 lanes is 1600 words and
does not fit in 64 registers, so the program keeps it in memory between the rounds and **every word load and store is
counted as an operation** (18,691 of the 54,009 operations are loads and stores). There is no fused AND-NOT; a NOT is an
XOR with an all-ones immediate, one operation. The time is counted in word operations of the program itself, exactly as the
program executes them (Sections 4 and 5), and divided by 1626, the cost of one reference compression.

## 2. The function f and the encoding

For a 256-bit value x with little-endian lanes x0..x3 let M(x) be the 135-byte message made of the 32 bytes of x
followed by 103 zero bytes. Absorbed with the SHA3 padding (byte 135 equal to 0x86) it is one block: state lanes 0 to 3
hold x0..x3, lane 16 holds 0x8600000000000000, every other lane of the 25 is zero. Rounds 0 to 5 are applied and
f(x) is lanes 0 to 3 of the result, 32 bytes. The encoding x -> M(x) is injective. Hence f(a) = f(b) with a != b gives
two distinct messages M(a), M(b) with equal complete digests. Domain and range of f have n = 2^256 elements.

A walk starts at rho + j (mod 2^256) for its trail number j = 0, 1, 2, ..., where rho is one fresh independent uniform
random 256-bit word (the cost model's random-word primitive, one operation, kept in one word of memory). Distinct trail numbers give
distinct starts.

## 3. The algorithm

Parameters: L = 256 walks; H = 116, theta = 2^-116; a point is a distinguished point (DP) when its 116 top bits are zero:
lane 3 is zero and the top 52 bits of lane 2 are zero; for a uniform point this has probability theta. Lc = 2^120 - 2 is the cap
on the length of a walk (the number of evaluations since its start); U = 5,000 is the limit on trails started in an attempt; the
table has S = U = 5,000 words; Tb = 1406345520049800208543858999779393536 = 1.05801678 * 2^120 is the number of steps of an attempt.

State in memory (words of 256 bits): IN, the 256 input planes (plane (lane, z), lanes 0 to 3); two buffers P and Q of 1600
planes; a table RCT of five words (the complemented round constants of rounds 0 to 4); LID[l] and LST[l] for each of the 256
walks (its trail number, the step at which it started); the table TAB of S words; rho. A table word holds a record: bits 0 to
122 the end of the trail (lane 0 and the low 59 bits of lane 1, 123 of the 140 bits of the end that are not forced to zero), bits 123 to 135
the trail number (13 bits), bits 136 to 255 the length of the trail (120 bits). A record is nonzero (its length is at least 1);
an empty slot is zero.

```
rho := random word; idn := 256; TAB := 0; for l < 256: LID[l] := l; LST[l] := 0; plane word of IN := bits of (rho + l)
c := 0; nxt := min(Tb, Lc)
loop:
  c += 1
  one step of the 256 walks (Section 4): IN := the digest planes of the walks; pf := prefilter word of 16 planes of lane 3
  if pf != all-ones:                                  -- some walk has the low 16 bits of lane 3 zero (probability 2^-16 each)
      slow test of the remaining 48 planes of lane 3 and the 52 planes of lane 2 -> the set of walks l that are at a DP
      for each such walk l, in increasing order:
          record := (end of walk l) | LID[l] << 123 | (c - LST[l]) << 136
          probe TAB from the slot (low 13 bits of the end, folded into [0, S)), linear probing, wrap at S:
             empty slot: store the record there
             a record with the same 123 end bits and a different trail number: REPLAY(that record, this record); if it returns two
                inputs a != b, output M(a), M(b) and stop
          restart(l)
  if c = nxt:
      if c = Tb: halt, the attempt failed
      for each walk l with c - LST[l] = Lc (no DP within Lc steps): restart(l)
      nxt := min(Tb, min over l of LST[l] + Lc)
restart(l):  if idn = U: halt, the attempt failed
             LID[l] := idn; LST[l] := c; plane bit l of IN := bits of (rho + idn); idn += 1
REPLAY(record A of trail a, length lA; record B of trail b, length lB):   -- the two trails end at the same point
  p := rho + a, q := rho + b; the trail with the greater length is advanced by |lA - lB| steps (p := f(p), one evaluation at a time)
  repeat min(lA, lB) times: if f(p) = f(q) return (p, q); p := f(p); q := f(q)
  if p = q after the advance, or no merge was seen: return nothing (no collision; the walk continues)
```

The walks l are independent walks of f; only the instruction stream is shared. A walk whose point is a DP is recorded
and restarted at once, in the same step, so that all 256 lanes always work. The replay uses the one-walk program of f (Section 5), not
the bit-sliced program. If the two trails end at the same DP and neither start lies on the other trail, they merge at a first point: after the advance both are at the same
distance d <= min(lA, lB) from their common end, so the first position where f(p) = f(q) is found within d iterations; the
two values just before it are different and have the same image.

The restart rule. If the loop halts (c reaches Tb or the trail limit U is reached) the attempt has failed; a new attempt starts
again with a fresh rho. Section 8 prices the restart. One attempt is what the claim of success 0.39 refers to.

## 4. One step of 256 walks: the bit-sliced program

The step is a straight-line register program, built by the generator in Appendix A and executed by the experiment
of Section 9. Its instructions are `ld` (register from an immediate address), `st`, `xor`, `and`, `or` (two registers, or a register and an immediate),
`shr` and `sub` by an immediate. Every instruction is one operation; there is no other kind. The machine has 64 registers and no spill code beyond the loads and stores listed; the allocation by linear scan
uses at most 44 of them in any section, and six more hold the loop state (the pointer into the round constants, the step counter c, the next deadline nxt,
the next trail number idn, the address of rho, one temporary), so at most 50 of 64 are in use.

**Planes.** Plane (lane, z) is the word whose bit i is bit z of Keccak lane `lane` for walk i. Theta, rho, pi, chi and iota act on
the 1600 planes; rho and pi are renamings of planes (free: the addresses are immediates), theta and chi are XOR, AND, OR and NOT of whole planes.

**Stored polarity.** Some planes are stored complemented (the polarity pattern Q of the program; the Keccak designers' lane complementing
transform is the origin of this device). chi of a row is x ^ (~y & z); with the stored polarities of y and z different, `and` or `or` of the stored
planes gives the term or its complement with no NOT, and the polarity of the stored result absorbs the complement. The pattern Q is a fixed point of a whole
round: stored polarity of every plane of the next round equals that of this round. It was found by an exhaustive search of the 2^25 patterns for the one with the
fewest NOTs; the search is not part of the proof, the program is, and the program is checked by running it (below). The cost is **6 NOTs per slice and round**
(384 per round) in place of 25.

**Theta carried to the next round.** The round code reads planes T = A xor D (theta already added) and writes the planes T' of the next round. It goes slice by slice
(z = 0, 1, ..., 63). For slice z and for each of the five rows it loads the five planes of the row of B = pi(rho(T)) (five loads: the addresses are immediates, the shifts of
rho are renamings), computes the five chi outputs, XORs them into the five column sums C'[x][z], and keeps them in registers (25 values per slice). When the five rows
are done, D'[x][z] = C'[x-1][z] xor C'[x+1][z-1] (the column sums of this slice and of slice z-1, both in registers) is added to the 25 values and the 25 results are stored. Slice 0
needs C' of slice 63: its 25 raw values are stored first and re-read, finished and re-stored at the end (25 loads, 25 stores, in the count). Every plane of T is loaded once, every
plane of T' is stored once. Iota adds the round constant to the 64 planes of lane 0: a constant bit set in no round 0 to 4 is skipped; at the 7 positions
z in {0, 1, 3, 7, 15, 31, 63} the constant word is shifted, masked to its bit z and turned into 0 or all-ones by a subtraction (shr, and, sub), then XORed: 4 operations
each, with the complemented constant in the table RCT.

**Phase 1** reads the 256 input planes and writes T of round 0: the input state has only lanes 0 to 3 and lane 16 nonzero, so theta needs 3 XORs of the column sums per slice (the
zero columns fold away), 4 more to add them to lanes 0 to 3, a few NOTs to match the stored polarity, and 1600 stores. **The last round** (round 5) computes only the five chi inputs of row 0 and the four outputs
x = 0 to 3 for each slice (its only outputs are lanes 0 to 3 of the result; the other chi outputs are never read), applies the round constant of round 5 (two NOTs), stores the 256 output planes into IN, and builds the
prefilter word pf as the OR of the first 16 planes of lane 3 (15 operations) while they are in registers. The stored polarity of the four output lanes is the one phase 1 expects.

**The loop.** Rounds 0 to 4 are the same code with the buffers exchanged (GA reads P, writes Q; GB reads Q, writes P), executed GA GB GA GB GA; the code GA GB is shared by the
first two and next two rounds by a loop (exit test after each GA, jump after each GB), and the round constant of the round is read from RCT through the pointer. The loop control is
1 + 5 + 3 x 2 + 2 x 1 = 14 operations (pointer initialisation, five pointer steps, three exit tests of two, two jumps), the prefilter test costs 2 and the step counter 3
(add, compare, branch, against nxt).

**Check by execution.** The ledger program of Appendix A builds the sections, executes them as Python on 256 random inputs at once (the 256 lanes of one trial) and compares two chained steps with the
plain Keccak permutation: they agree. The experiment of Section 9 repeats this check before it runs.

**Counts.** Phase 1 has 2506 instructions; the round code 10063 each (647 and, 1626 ld, 960 or, 7 shr, 1625 st, 7 sub, 5191 xor, of which 384 are NOTs); the last round 1169. A step is
2506 + 5 x 10063 + 1169 + 14 + 2 + 3 = **54,009** operations. Loads and stores are 18,691 of them. The code is straight-line with immediate addresses and
constants, so there is no index arithmetic.

## 5. The rest of the operation count

The one-walk program of f used by the replay is the straight-line program `build_ops` of Appendix A with F = 1244 operations (the first round folds the
constant and zero lanes of the one-block state, the last round computes only lanes 0 to 3, a rotation is four operations: shl, shr, or, and). It is the same program as in the one-walk implementation. The replay runs it on one input
at a time with the four digest lanes moved back into the input lanes (4 moves) between evaluations: the advance costs F + 7 per evaluation (moves 4 and counter 3) and a lock-step iteration 2F + 26
(two evaluations, 16 moves, the equality test of the four lanes 9, a jump 1). The replay therefore costs at most (F + 7)(max - min) + (2F + 26) min <= (2F + 26) Lc, where min and max are the two trail lengths,
both at most Lc.

Rare operations. Each routine below is straight-line or a counted loop; its count is an upper bound on what it executes, and the totals are below 2^-15 of N.

- Slow test of a prefilter hit: 48 loads and 48 ORs (lane 3 planes 16 to 63), 52 loads and 51 ANDs (lane 2 planes 12 to 63), 2 operations to combine, a compare and a branch, a call and a return: **205**.
  A hit has probability 2^-16 per walk and step; over Tb steps the number of hits is at most Tb 2^-8 (1 + 2^-20) with probability above 1 - exp(-2^72/3) (Chernoff, mean 2^112).
- A walk at a DP: gathering the 123 end planes by a loop (load, shift right by l, and 1, shift left, or: 5 per plane, plus 2 for the polarity of lane 1, plus the loop control) at most 640, the record word 4, the probe at most 10 per slot over at most S slots 10 S + 20,
  the store 6, the restart of a walk (a 256-bit add, the new trail number, then for each of the 256 planes: load, shift/and for its bit, shift left, and, or, store, plus the polarity of two lanes) 2,460, and the new deadline nxt (a loop over the 256 walks) 1,100: **54,230** each; every restart uses a trail number, so there are at most U restarts (a walk at a DP, or a dead walk, whose restart costs less), plus one last walk at a DP when the limit stops the attempt: at most U + 1 times.
- The dead-walk scan at a deadline: 1,300, at most U + 1 times.
- The start of an attempt (256 walks), the replay entry and the final bookkeeping: 704,000 in all.

So R = hits x 205 + (U + 1) x 54,230 + (U + 1) x 1,300 + 704,000 = 1,126,176,197,481,670,109,261,685,155,142,578,695.

Total. N = Tb x 54,009 + (2F + 26) Lc + R = 79298120549970419637834713353785194323555 operations (Appendix A).

## 6. Success probability and the premise

**Premise H_rand.** f behaves as a uniformly random function from 256 bits to 256 bits: the values of f at distinct inputs are independent and uniform, and the random word rho is uniform. This is the only heuristic; the cost
model, the program and the search procedure are exact. (It is the standard premise of birthday collision search; it is not proved for six Keccak rounds.) Consequences used below, all for evaluations at distinct inputs: (i) the first coincidence of images among
e evaluations has probability 1 - prod_{k<e}(1 - k/n) >= 1 - exp(-e(e-1)/(2n)) =: G(e); (ii) the point reached just after a coincidence is uniform, so the number l of further evaluations of a trail until its DP
satisfies P(l >= j) = (1 - theta)^j, independently of when the coincidence happened.

Evaluations are numbered step by step and, inside a step, by walk: evaluation e = 256 (b - 1) + (i + 1) is the one of walk i at step b. Let e* be the number of the first evaluation whose image equals the image of an earlier one (the coincidence), at step b* = ceil(e*/256). The
trail B of that evaluation and the earlier trail A (the one holding the other input) have equal points from then on; both end at the same DP, after l further evaluations of B. B is recorded at step b* + l at the latest, and A, which reached the same point no later, was recorded before (or in the same step, in a lower lane: the later one finds
the earlier record). So the search succeeds if (a) b* + l <= Tb, (b) both trails have at most Lc evaluations, (c) the table has room (fewer than U trails), (d) the coincidence is between two different trails (not inside one), and (e) the stored 123 end bits are those of the real ends and the replay finds the merge.

Split l into bins of w = 2^104 steps, bin j holding l in [(j-1) w, j w - 1], j = 1, ..., 2^16 - 1, with probability p_j = (1-theta)^((j-1) w) - (1-theta)^(j w). If l is in bin j, (a) holds when e* <= 256 (Tb - j w). By independence (ii),

    Pr[(a)] >= sum_j p_j G(256 (Tb - j w)).

The failure events the sum does not cover:

- F1, some trail of the attempt has no DP within Lc steps: at most U (1 - theta)^Lc <= U e^-kappa, kappa = Lc theta = 16 - 2^-115 (5.627e-04). This covers (b).
- F2, more than U - 256 DPs in the 256 Tb evaluations of the attempt, so that the trail limit stops it: the number of DPs is binomial with mean mu = 256 Tb theta = 4333.6, and the Chernoff bound
  e^-mu (e mu/(U-256))^(U-256) holds (6.553e-09). This covers (c).
- F3, the coincidence is inside one trail (a cycle or a self-merge, which a table of ends cannot see): at most U/(theta^2 n) = U 2^232/2^256 (2.980e-04), by the sum over trails of E[l(l-1)/2]/n with l geometric with parameter theta. This covers (d).
- F4, 2^-90: a start equal to another trail's point (starts are rho + j, j < U), two different ends with the same 123 stored bits (U^2/2 pairs, 2^-123 each, below 2^-99), a failed replay
  for a reason other than an equal end, and the prefilter-hit bound. This covers (e).

With the further 2^-60 for rounding, the success probability of one attempt is at least 0.3900000075 for the Tb above, and below 0.39 with 2^96 fewer steps (Appendix A computes both with 80-digit decimals). Tb is
the least multiple of 2^96 for which the bound reaches 0.39. In units of evaluations: Tb x 256 = 1.058017 x 2^128; the birthday point for success 0.39 is 0.99430 x 2^128, the failure terms cost 0.00086 of the probability, and the wait for the DP of the last trails costs about 256 x 2^116 = 2^124 evaluations (a sixteenth of 2^128): that last effect is why
the number of evaluations is above the one-walk figure. Against the one-walk implementation (time_log2 127.61957) the change is -2.56 bit for the operations per evaluation (210.97 against 1247.5), +0.09 bit for the number of evaluations (1.058 x 2^128 against 0.997 x 2^128) and +0.05 bit for the replay and the rare operations.

## 7. Memory

- code: one 256-bit word per instruction: phase 1 2506, the round code GA and GB 2 x 10063, the last round 1169, loop control, the slow test, the gathering, probing, restart, deadline, start and output routines (435 words in all), the
  one-walk program of f F = 1244 plus its replay loops (120): 25,600 words;
- data: the planes P, Q (2 x 1600) and IN (256), RCT (5), LID and LST (512), the table (5,000), 64 scratch words: 9,037 words;

in all 1,108,384 bytes, log2 = 20.0801. Memory is declared as memory_log2_bytes = 20.0801 and the score is time_log2 + (memory_log2 - 20) = 125.2774. The code size is a declared bound of the program of Appendix A (the instruction counts of its sections are computed; the routines of Section 5 are counted by the sums above), not a measurement.

## 8. A walk pair without a real collision, and the restart price

Two trails with the same DP can fail to give a collision only if one start lies on the other's trail (or the starts are equal, which distinct trail numbers exclude); the replay finds this after the advance (p = q) and the walk continues. This has probability below
2^-90 per attempt (F4). A dead walk (no DP in Lc steps) is restarted at its deadline; its steps are inside the Tb steps of the attempt. If an attempt fails, which has probability at most 0.61 under the premise, a new attempt with a fresh rho costs at most N again with independent coins, so the expected cost until a collision
is at most N/0.39 = 2.57 N, 1.36 bits more than the claim. The claim is the cost of one attempt with success 0.39.

## 9. The declared experiment (organizer-run)

experiments/rho.py runs the same program: the generator of Appendix A builds the bit-sliced sections, the program is executed on Python integers (one integer holds a plane for all 256 trials of a request, trial t in bits 256 t to 256 t + 255; every instruction acts on all trials at once, and trials never
interact), the same DP rule (on the low H bits of the kept digest), table with stored lengths, restart rule, deadlines and replay, on a reduced digest: f' keeps the low 18 bits of f(x) (after each step the planes above bit 18 are set to zero, the only difference from the full-size program), H = 4, trail cap 256, 3000 trails per attempt, 200 steps per attempt. It runs the self-test of the
bit-sliced program (256 inputs, two chained steps against the plain permutation) and of the one-walk program before the trials. Per trial it returns two different messages whose six-round digests agree in the low 18 bits. This is a partial collision, not a collision of the full digest. About 7 steps per trial
suffice; the whole request of 256 trials takes about 2.5 seconds. The experiment shows that the program works end to end on the target: planes, rounds, polarity, the table, the restart rule and the replay. It does not measure the cost at full size or the premise at 256 bits.

## 10. Toy-width validation on a GPU (preregistered)

This is our own measurement on an RTX 3090, not an organizer run; the program, the seeds and the raw lines are in Appendix B. **What it tests.** The dynamics of the lockstep search (256 walks, restart on DP, caps, tail), not the bit-sliced
circuit (which Section 4 checks by execution). The toy is an exact scale model of the full design: the full design has n = 2^256 and H = 116, so n = 2^(2 (H + 12)); the toy has n = 2^56 and H = 16, so every ratio of the design is the same (records per attempt mu = 4,334, the tail 256 x 2^H over sqrt(n) = 1/16, U/mu, U/(theta^2 n)). The function is f(x) = the low 56 bits of lane 0 of rounds 0 to 5 on the same one-block state with x in lane 0,
a real six-round function; the CUDA program implements the walks one thread each, the table, restart, deadlines and the replay, and agrees with the Python reference permutation on 64 test inputs.

**Preregistration** (written 2026-10-11 21:52 local time, before any run; the text, with the SHA-256 of the program, the parameter and prediction scripts, the analysis script and the seed files, is in Appendix B): 200 runs of the dense search with fresh seeds (rho from SHA-256 of
"s6d-prereg-2026-10-11/dense/i"), the control of 200 runs of the one-walk search of the one-walk implementation (trails one after another, trail cap 17.5 x 2^H, 8,700 trails, m = 267,054,329 evaluations, same f and width, H = 15); the dense parameters Tb = 1,109,659 steps, Lc = 2^20, U = 5,000. Pass rules fixed in advance: success rate at the horizon in the band
0.39 +- 2 sqrt(0.39 x 0.61/200) = [0.321, 0.459]; success rate by the point n* = n0 + L/theta (n0 = 266,899,995 the birthday point of success 0.39, L/theta = 256 x 2^16) in the same band; the median summed work to detection within +-10% of the model; the maximum number of trails started by the horizon below U; the mean number of table records within +-1%;
the mean number of duplicate endpoints within +-25% of the model; every first duplicate replays to a real collision; at most 3 dead walks. For the control the same rules with its own cap U = 8,700.

**Results.** Dense search, 200 runs, every preregistered criterion as printed by the analysis script of Appendix B:

```
A1 success at the design horizon (rate)                    0.3300 (66/200)        PASS CI95 [0.265, 0.400]; band [0.321, 0.459]; model 0.3909
A2 detected by n* = n0 + 256 2^H (rate)                    0.3300 (66/200)        PASS n*=283677211 model 0.3900
A3 median summed work to detection                         3.567e+08              PASS model 3.33e+08 (band +-10%)
A4a max trails at the horizon < U=5000                     4803 (max rec 4547)    PASS 
A4b mean records at the horizon                            4338.6                 PASS model 4334.6 (band +-1%)
A5 mean duplicate endpoints at the horizon                 0.415                  PASS model 0.4958 (band +-25%); rate per record 9.57e-05
A6 every first duplicate replays to a real collision       bad runs []            PASS 
A7 dead trails over all runs (model 0.10)                  0                      PASS 
info: detected at all (cap 1.6 horizon) 140/200; mean trails at T 4595.0; max trails 4803; mean dups_total 0.785; mean la+lb of replay 259386
ALL PASS
```

Control, the one-walk search at the same width, 200 runs:

```
B1 success at the halt (rate)                              0.3850 (77/200)        PASS CI95 [0.317, 0.456]; model 0.3903
B2 detected by n* = n0 + 2^H (rate)                        0.3850 (77/200)        PASS n*=266932763
B3 max trails < U=8700 (no U-halt); mean trails            8369; mean 8156.6      PASS model 8149.9
B4 mean duplicate endpoints                                0.485                  PASS model 0.4949
B5 every first duplicate replays to a real collision       bad runs []            PASS 
B6 mean evaluations at the halt / m                        1.000130               PASS model 1.000123
info: dead trails total 0; U-halts 0
ALL PASS
```

Extension, **not preregistered**, added after the first result: 1000 further runs of the dense search with fresh seeds (SHA-256 of "s6d-ext-2026-10-11/dense/i"), the same statistics with z-scores against the model:

```
N 1000
success at horizon 390/1000 = 0.3900  model 0.3909  z -0.06
detected by n*       389/1000 = 0.3890  model 0.3900  z -0.07
median work 3.308e+08  model 3.33e+08  ratio 0.9934
mean dups at horizon 0.4970  model 0.4958  ratio 1.002 (se 0.045)
mean records 4333.1 model 4334.6 ; max trails 4819 ; max rec 4562 ; dead 1 ; replay not real 0
```

**Reading.** The dense search passed all seven preregistered criteria (A1 to A7) and the control all six (B1 to B6); no criterion, band or run was changed. The first 200 dense runs gave a success rate of 0.330 (66/200), inside the band but at its low end (1.8 standard errors under the model
0.3909); the median work (3.57e8 against 3.33e8) and the duplicate-endpoint mean (0.415 against 0.496) were also on the low side. Because 200 runs cannot tell a six-point shortfall from a fluctuation, 1000 further runs with fresh seeds were added afterwards (the extension above, not preregistered):
success 0.390 (390/1000, model 0.3909, z = -0.06), detected by n* 0.389 (model 0.3900), median work 0.993 of the model, duplicate endpoints 0.497 (model 0.496), mean table records 4,333.1 (model 4,334.6), and the largest number of trails started by the horizon in all 1200 dense runs is 4,819, below the cap U = 5,000.
The shortfall of the first 200 is therefore consistent with a fluctuation; the 1200 runs together give 456/1200 = 0.380 against 0.391 (z = -0.8). Every first duplicate in the 1200 runs replayed to two different inputs with equal f (no start lay on the other trail, no end mismatch), and dead walks were 0 in 200 and 1 in 1000 runs (model 0.10 and 0.52).
The control, the one-walk search at the same width, gave 77/200 = 0.385 (model 0.3903), 8,156.6 trails on average (model 8,149.9), 0.485 duplicate endpoints (model 0.495), and finished at 1.000130 m (model 1.000123).

What is measured: on the real six-round function truncated to 56 bits and an exact scale model of the design, the lockstep search finds its collision by the horizon with the probability of the random-function model (0.390 in 1000 runs), the number of table records and trails matches the model and stays under the cap, duplicate endpoints and the work to detection match the n* = n0 + L/theta charge (the tail of 256 walks waiting for their distinguished points is real and as large as charged:
the dense horizon is 1.064 times the control's, 284.07e6 against 267.05e6 evaluations, 0.089 bit; the full-size ledger charges 1.058/0.997 = 1.061). What is not measured: the bit-sliced circuit (checked by execution in Section 4 and by the organizer's sandbox at 18 bits), the premise at 256 bits (the toy function is a fixed six-round function at 56 bits with 200 and 1000 runs, which
resolves a gross error but not a few percent), and wall-clock performance. The GPU program evaluates f as 64-bit lanes, one walk per thread; it is not the bit-sliced program.

## 11. Limits

The premise of Section 6 is not tested at 256 bits: no run reaches the scale 2^128 and no full collision is claimed. The experiment checks 18 bits on the program's own digests; the GPU runs check the dynamics at 56 bits on 200 runs, which resolves a gross error but not a few percent. The word-operation counts are the ledger's accounting of the described program,
which is not executed at full scale; the bit-sliced program is executed and compared with the plain permutation, as are the one-walk program and, in the experiment, the whole search at a reduced width. The routines of Section 5 (slow test, gathering, probing, restart, deadline scan) are counted but not generated as straight-line code in the ledger; their total, below 2^-15 of N, does not move the fifth decimal of time_log2 by more than the stated sums.
The code size and the 64 scratch words are declared bounds. The reference cost 1626 is the unit; the one-walk program of f is charged its own F = 1244 operations in the replay.
The program keeps its registers within 64; a machine with fewer registers would need more loads and stores.

## Appendix A. The exact ledger

The following program contains the generator of the bit-sliced program (Section 4), the one-walk program of f (Section 5), the check by execution, the success bound (Section 6) and the ledger. It uses integers and Fractions; Decimal with 80 digits is used only for the exponentials and logarithms of the success bound. It runs in about half a minute. Its output follows.

```python
import hashlib

M64 = (1 << 64) - 1
ALL = (1 << 256) - 1
RC = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001]
ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
Q_FIX = 4361286          # polarity (bit X+5Y) of the stored chi outputs: a fixed point of a whole round, found by search
PAD = 0x8600000000000000  # lane 16
PF_K = 16                # planes of lane 3 in the DP prefilter


def xmap(X, Y):
    return (3 * Y + X) % 5           # old column x of the lane that lands on B(X, Y)  (X = old y)


def polarities(q=Q_FIX):
    Q = {(X, Y): (q >> (X + 5 * Y)) & 1 for X in range(5) for Y in range(5)}
    pC = [sum(Q[(X, Y)] for Y in range(5)) % 2 for X in range(5)]
    pD = [(pC[(X - 1) % 5] ^ pC[(X + 1) % 5]) for X in range(5)]
    pT = {(X, Y): Q[(X, Y)] ^ pD[X] for X in range(5) for Y in range(5)}     # stored polarity of T(x=X, y=Y)
    return Q, pC, pD, pT


def plan_row(pB, qwant, need=(0, 1, 2, 3, 4)):
    """Cheapest way to compute the chi outputs X in `need` of one row from stored planes with polarities pB[0..4] so that
    output X has stored polarity qwant[X] (None = any). Returns (cost, S, choices); choices[X] = (v1, v2, op, resinv, qq)."""
    best = None
    for S in range(32):
        cS = bin(S).count('1')
        opts = []
        ok = True
        for X in need:
            o = []
            a, b = (X + 1) % 5, (X + 2) % 5
            for v1 in ((0, 1) if (S >> a) & 1 else (0,)):
                for v2 in ((0, 1) if (S >> b) & 1 else (0,)):
                    p1, p2 = pB[a] ^ v1, pB[b] ^ v2
                    if p1 == p2:
                        continue
                    op, flip = ('and', 0) if p1 == 1 else ('or', 1)
                    for ri in (0, 1):
                        qq = pB[X] ^ flip ^ ri
                        if qwant[X] is None or qq == qwant[X]:
                            o.append((ri, (v1, v2, op, ri, qq)))
            if not o:
                ok = False
                break
            opts.append(o)
        if not ok:
            continue
        c = cS + sum(min(r for r, _ in o) for o in opts)
        if best is None or c < best[0]:
            ch = {}
            for X, o in zip(need, opts):
                m = min(r for r, _ in o)
                ch[X] = [c2 for r, c2 in o if r == m][0]
            best = (c, S, ch)
    return best


class Prog:
    def __init__(self):
        self.ins = []          # (kind, dst, a, b): a/b are vregs (int) or ('i', imm); ld: a = address; st: dst = address, a = vreg
        self.nv = 0

    def new(self):
        self.nv += 1
        return self.nv - 1

    def ld(self, addr):
        d = self.new()
        self.ins.append(('ld', d, addr, None))
        return d

    def st(self, addr, r):
        self.ins.append(('st', addr, r, None))

    def op(self, kind, a, b):
        d = self.new()
        self.ins.append((kind, d, a, b))
        return d

    def xor(self, a, b):
        return self.op('xor', a, b)

    def and_(self, a, b):
        return self.op('and', a, b)

    def or_(self, a, b):
        return self.op('or', a, b)

    def not_(self, a):
        return self.op('xor', a, ('i', ALL))


def chi_row(P, s, pB, plan, need=(0, 1, 2, 3, 4)):
    cost, S, ch = plan
    inv = {j: P.not_(s[j]) for j in range(5) if (S >> j) & 1}
    out = {}
    for X in need:
        v1, v2, op, ri, qq = ch[X]
        a, b = (X + 1) % 5, (X + 2) % 5
        e1 = inv[a] if v1 else s[a]
        e2 = inv[b] if v2 else s[b]
        u = P.and_(e1, e2) if op == 'and' else P.or_(e1, e2)
        if ri:
            u = P.not_(u)
        out[X] = P.xor(s[X], u)
    return out


def addr(buf, lane, z):
    return buf * 1600 + lane * 64 + z


IOTA_Z = (0, 1, 3, 7, 15, 31, 63)       # union of the set bits of RC[0..4]


def gen_G(src, dst, q=Q_FIX):
    """One generic round: reads T planes (theta already added, stored polarity pT) from buffer src, writes T' to buffer dst.
    The round constant is a 64-bit word loaded from the RC cell; iota is applied from it at the 7 positions in IOTA_Z."""
    Qp, pC, pD, pT = polarities(q)
    P = Prog()
    plans = []
    for Y in range(5):
        pB = [pT[(xmap(X, Y), X)] for X in range(5)]
        plans.append((pB, plan_row(pB, [Qp[(X, Y)] for X in range(5)])))
    rcv = P.ld(('rc',))
    C0 = None
    Cprev = None
    for z in range(64):
        o = {}
        Cc = [None] * 5
        for Y in range(5):
            s = []
            for X in range(5):
                x = xmap(X, Y)
                s.append(P.ld(addr(src, x + 5 * X, (z - ROT[x][X]) % 64)))
            res = chi_row(P, s, plans[Y][0], plans[Y][1])
            for X in range(5):
                v = res[X]
                if Y == 0 and X == 0 and z in IOTA_Z:           # iota: o ^= -(bit z of RC)
                    m = P.op('shr', rcv, ('i', z))
                    m = P.op('and', m, ('i', 1))
                    m = P.op('sub', m, ('i', 1))                # rcv holds the complement of the round constant: (1 - bit) - 1 = -bit
                    v = P.xor(v, m)
                o[(X, Y)] = v
                Cc[X] = v if Cc[X] is None else P.xor(Cc[X], v)
        if z == 0:
            for (X, Y), v in o.items():
                P.st(addr(dst, X + 5 * Y, 0), v)
            C0 = Cc
        else:
            D = [P.xor(Cc[(X - 1) % 5], Cprev[(X + 1) % 5]) for X in range(5)]   # D[X][z] = C[X-1][z] ^ C[X+1][z-1]
            for (X, Y), v in o.items():
                P.st(addr(dst, X + 5 * Y, z), P.xor(v, D[X]))
        Cprev = Cc
    D = [P.xor(C0[(X - 1) % 5], Cprev[(X + 1) % 5]) for X in range(5)]       # slice 0 last: needs C[.][63]
    for Y in range(5):
        for X in range(5):
            r = P.ld(addr(dst, X + 5 * Y, 0))
            P.st(addr(dst, X + 5 * Y, 0), P.xor(r, D[X]))
    return P


def gen_phase1(dst, pIn, q=Q_FIX):
    """Reads the 256 input planes (buffer 2, lanes 0..3, stored polarity pIn[l]) and writes T0 (theta added to the dense-input state) to dst."""
    Qp, pC, pD, pT = polarities(q)
    P = Prog()
    kz = {57, 58, 63}
    cache = {}

    def lane_in(l, z):
        z %= 64
        if (l, z) not in cache:
            cache[(l, z)] = (P.ld(addr(2, l, z)), pIn[l])      # true value = reg ^ pol
        return cache[(l, z)]

    def flipk(u, z):
        return (u[0], u[1] ^ (1 if z in kz else 0))

    def cx(a, b):
        if a is None:
            return b
        if b is None:
            return a
        return (P.xor(a[0], b[0]), a[1] ^ b[1])

    for z in range(64):
        zm = (z - 1) % 64
        for key in [k for k in cache if k[1] not in (z, zm)]:
            del cache[key]
        C = [lane_in(0, z), flipk(lane_in(1, z), z), lane_in(2, z), lane_in(3, z), None]
        Cm = [lane_in(0, zm), flipk(lane_in(1, zm), zm), lane_in(2, zm), lane_in(3, zm), None]
        D = [cx(C[4], Cm[1]), cx(C[0], Cm[2]), cx(C[1], Cm[3]), cx(C[2], Cm[4]), cx(C[3], Cm[0])]
        T = {}
        for x in range(5):
            for y in range(5):
                if y == 0:
                    T[(x, y)] = cx(lane_in(x, z) if x < 4 else None, D[x])
                elif (x, y) == (1, 3):
                    T[(x, y)] = (D[1][0], D[1][1] ^ (1 if z in kz else 0))
                else:
                    T[(x, y)] = D[x]
        nots = {}
        for x in range(5):
            for y in range(5):
                r, p = T[(x, y)]
                if p != pT[(x, y)]:
                    if r not in nots:
                        nots[r] = P.not_(r)
                    r = nots[r]
                P.st(addr(dst, x + 5 * y, z), r)
    return P


def gen_R5(src, q=Q_FIX, qwant=None):
    """Last round: row 0 only, outputs lanes 0..3 into buffer 2 (the input planes of the next step); builds the DP prefilter on lane 3."""
    Qp, pC, pD, pT = polarities(q)
    P = Prog()
    pB = [pT[(xmap(X, 0), X)] for X in range(5)]
    plan = plan_row(pB, (list(qwant) + [None]) if qwant else [None] * 5, need=(0, 1, 2, 3))
    pOut = {X: plan[2][X][4] for X in range(4)}
    pf = None
    for z in range(64):
        s = [P.ld(addr(src, xmap(X, 0) + 5 * X, (z - ROT[xmap(X, 0)][X]) % 64)) for X in range(5)]
        res = chi_row(P, s, pB, plan, need=(0, 1, 2, 3))
        for X in range(4):
            v = res[X]
            if X == 0 and z in (0, 31):
                v = P.not_(v)            # iota of round 5 (RC = 0x80000001)
            P.st(addr(2, X, z), v)
            if X == 3 and z < PF_K:
                pf = v if pf is None else (P.or_(pf, v) if pOut[3] == 0 else P.and_(pf, v))
    return P, pOut, pf


def stats(P):
    ins = P.ins
    last = {}
    defi = {}
    for i, (k, d, a, b) in enumerate(ins):
        srcs = [] if k == 'ld' else ([a] if k == 'st' else [a, b])
        for s in srcs:
            if isinstance(s, int):
                last[s] = i
        if k != 'st':
            defi[d] = i
    delta = [0] * (len(ins) + 2)
    for v, d in defi.items():
        l = last.get(v, d)
        delta[d] += 1
        delta[l + 1] -= 1
    cur = 0
    peak = 0
    for i in range(len(ins)):
        cur += delta[i]
        k, d, a, b = ins[i]
        dying = 0
        if k not in ('ld', 'st'):
            dying = sum(1 for s in {a, b} if isinstance(s, int) and last.get(s) == i)
        peak = max(peak, cur - (1 if dying else 0))
    cnt = {}
    for k, *_ in ins:
        cnt[k] = cnt.get(k, 0) + 1
    return len(ins), cnt, peak


def regalloc(P):
    """Linear-scan allocation of the virtual registers to physical registers 0.. (a source that dies at an instruction
    frees its register for that instruction's result). Returns (map, number of registers used)."""
    ins = P.ins
    last = {}
    for i, (k, d, a, b) in enumerate(ins):
        for s in ([] if k == 'ld' else ([a] if k == 'st' else [a, b])):
            if isinstance(s, int):
                last[s] = i
    free = []
    nxt = 0
    phys = {}
    for i, (k, d, a, b) in enumerate(ins):
        srcs = [] if k == 'ld' else ([a] if k == 'st' else [a, b])
        for s in set(x for x in srcs if isinstance(x, int)):
            if last[s] == i:
                free.append(phys[s])
        if k != 'st':
            if free:
                free.sort()
                phys[d] = free.pop(0)
            else:
                phys[d] = nxt
                nxt += 1
            if d not in last:
                free.append(phys[d])
    return phys, nxt


def to_python(P, name, allw='ALLW'):
    """Straight-line python over the physical registers: memory list M, registers p<k> as locals."""
    phys, nreg = regalloc(P)
    L = ["def %s(M, RC=0):" % name]

    def v(x):
        if isinstance(x, tuple):
            return allw if x[1] == ALL else "%d" % x[1]
        return "p%d" % phys[x]
    for k, d, a, b in P.ins:
        if k == 'ld':
            L.append("    p%d = %s" % (phys[d], "RC" if isinstance(a, tuple) else "M[%d]" % a))
        elif k == 'st':
            L.append("    M[%d] = p%d" % (d, phys[a]))
        elif k == 'xor':
            L.append("    p%d = %s ^ %s" % (phys[d], v(a), v(b)))
        elif k == 'and':
            L.append("    p%d = %s & %s" % (phys[d], v(a), v(b)))
        elif k == 'or':
            L.append("    p%d = %s | %s" % (phys[d], v(a), v(b)))
        elif k == 'shr':
            L.append("    p%d = %s >> %s" % (phys[d], v(a), v(b)))
        elif k == 'sub':
            L.append("    p%d = (%s - %s) & %s" % (phys[d], v(a), v(b), allw))
        else:
            raise ValueError(k)
    L.append("    return")
    return chr(10).join(L), nreg

RC_ALL = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001, 0x8000000080008081,
          0x8000000000008009, 0x8A, 0x88, 0x80008009, 0x8000000A, 0x8000808B, 0x800000000000008B,
          0x8000000000008089, 0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x800A,
          0x800000008000000A, 0x8000000080008081, 0x8000000000008080, 0x80000001, 0x8000000080008008]


def build_ops():
    """Straight-line program of f. A lane is a 64-bit value in a 256-bit RAM word. An int is an immediate (a
    constant folded when the program is built), a str names a RAM word. Every emitted op is ONE word operation:
    xor, and, or of two words or of a word and an immediate, shl or shr of a word by an immediate.
    Inputs in0..in3; the result is lanes 0..3. Returns (ops, outs); ops = (dst, op, x, y, round)."""
    ops = []
    rnd = [0]

    def emit(op, x, y, mask=False):
        cx, cy = isinstance(x, int), isinstance(y, int)
        if cx and cy:
            return {'xor': x ^ y, 'and': x & y, 'or': x | y, 'shl': x << y, 'shr': x >> y}[op]
        if cx and op in ('xor', 'and', 'or'):
            x, y, cx, cy = y, x, cy, cx
        if not mask:
            if op in ('xor', 'or') and cy and y == 0:
                return x                       # x ^ 0, x | 0
            if op == 'and' and cy and y == 0:
                return 0
            if op == 'and' and cy and y == M64:
                return x                       # x is already a 64-bit lane
            if op == 'or' and cy and y == M64:
                return M64
        name = 't%d' % len(ops)
        ops.append((name, op, x, y, rnd[0]))
        return name

    def rot(v, r):                             # shl, shr, or, and (the mask): 4 operations
        if r == 0:
            return v
        return emit('and', emit('or', emit('shl', v, r), emit('shr', v, 64 - r)), M64, True)

    a = ['in0', 'in1', 'in2', 'in3'] + [0] * 12 + [0x8600000000000000] + [0] * 8
    for r in range(6):
        rnd[0] = r
        c = []
        for x in range(5):
            t = a[x]
            for y in range(1, 5):
                t = emit('xor', t, a[x + 5 * y])
            c.append(t)
        d = [emit('xor', c[(x + 4) % 5], rot(c[(x + 1) % 5], 1)) for x in range(5)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = rot(emit('xor', a[x + 5 * y], d[x]), ROT[x][y])
        a = [0] * 25
        for y in range(5):
            for x in range(5):
                nb = emit('xor', b[(x + 1) % 5 + 5 * y], M64)       # NOT = xor with all ones; no fused AND-NOT
                a[x + 5 * y] = emit('xor', b[x + 5 * y], emit('and', nb, b[(x + 2) % 5 + 5 * y]))
        a[0] = emit('xor', a[0], RC[r])
    outs = a[:4]                       # lanes 4..24 of the last round are never read: their ops are dropped
    live = {o for o in outs if isinstance(o, str)}
    kept = []
    for op in reversed(ops):
        if op[0] in live:
            kept.append(op)
            live |= {v for v in op[2:4] if isinstance(v, str)}
    kept.reverse()
    return kept, outs


def perm(a, rounds):
    """Reference Keccak-f, used only to check the straight-line program and the digests."""
    for rc in RC_ALL[:rounds]:
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x + 4) % 5] ^ (((c[(x + 1) % 5] << 1) | (c[(x + 1) % 5] >> 63)) & M64) for x in range(5)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                v = a[x + 5 * y] ^ d[x]
                r = ROT[x][y]
                b[y + 5 * ((2 * x + 3 * y) % 5)] = ((v << r) | (v >> (64 - r))) & M64 if r else v
        for y in range(5):
            for x in range(5):
                a[x + 5 * y] = b[x + 5 * y] ^ (~b[(x + 1) % 5 + 5 * y] & b[(x + 2) % 5 + 5 * y])
        a[0] ^= rc
    return a


def digest(msg, rounds=6):
    st = [0] * 25
    blk = bytearray(136)
    blk[:len(msg)] = msg
    blk[len(msg)] ^= 6
    blk[135] ^= 0x80
    for i in range(17):
        st[i] ^= int.from_bytes(blk[8 * i:8 * i + 8], "little")
    perm(st, rounds)
    return b"".join(st[i].to_bytes(8, "little") for i in range(4))


def msg_of(x):
    return x.to_bytes(32, "little") + bytes(103)


def build_sections():
    P5, pOut, pf = gen_R5(1, qwant=[0, 1, 1, 0])
    pIn = [pOut[i] for i in range(4)]
    secs = {'phase1': gen_phase1(0, pIn), 'GA': gen_G(0, 1), 'GB': gen_G(1, 0), 'R5': P5}
    return secs, pIn, pOut


def step_count(secs):
    """Word operations of one batch step, as executed: phase 1, five generic rounds (GA GB GA GB GA), the last round, the loop
    control (pointer init 1, pointer step 5, exit test after each GA 3 x 2, jump after each GB 2 x 1), the prefilter test 2, the counter 3."""
    n1, nG, n5 = len(secs['phase1'].ins), len(secs['GA'].ins), len(secs['R5'].ins)
    assert nG == len(secs['GB'].ins)
    return n1 + 5 * nG + n5 + (1 + 5 + 3 * 2 + 2 * 1) + 2 + 3


def dense_selftest(secs, pIn, pOut):
    """The dense program on 256 inputs at once (the 256 lanes of one trial), two chained steps, against the plain permutation."""
    env = {'ALLW': ALL}
    for k, P in secs.items():
        exec(to_python(P, k)[0], env)
    xs = [int.from_bytes(hashlib.sha256(b"dense%d" % i).digest(), "little") for i in range(256)]
    M = [0] * 4800
    for l in range(4):
        for z in range(64):
            w = 0
            for i, x in enumerate(xs):
                w |= ((x >> (64 * l + z)) & 1) << i
            M[addr(2, l, z)] = w ^ (ALL if pIn[l] else 0)
    rc = [(~r) & M64 for r in RC]
    for _ in range(2):
        env['phase1'](M)
        env['GA'](M, rc[0]); env['GB'](M, rc[1]); env['GA'](M, rc[2]); env['GB'](M, rc[3]); env['GA'](M, rc[4])
        env['R5'](M)
        want = [int.from_bytes(digest(msg_of(x)), "little") for x in xs]
        got = []
        for i in range(256):
            y = 0
            for l in range(4):
                for z in range(64):
                    y |= (((M[addr(2, l, z)] ^ (ALL if pOut[l] else 0)) >> i) & 1) << (64 * l + z)
            got.append(y)
        assert got == want
        xs = want
    return len(xs)


# ---- the exact ledger (integers and Fractions; Decimal only for the success bound) ----
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext, ROUND_CEILING
getcontext().prec = 80
ceil = lambda v: int(v.to_integral_value(rounding=ROUND_CEILING)) if isinstance(v, D) else -((-v.numerator) // v.denominator)

secs, pIn, pOut = build_sections()
sizes = {k: len(P.ins) for k, P in secs.items()}
kinds = {k: dict(sorted(stats(P)[1].items())) for k, P in secs.items()}
regs = {k: regalloc(P)[1] for k, P in secs.items()}
print('instructions', sizes)
print('by kind (round code)', kinds['GA'])
print('registers used by the straight-line code', regs, ' + 6 reserved for the loop and search state: at most', max(regs.values()) + 6, 'of 64')
assert max(regs.values()) + 6 <= 64
assert dense_selftest(secs, pIn, pOut) == 256              # the program, executed, agrees with the plain permutation on 256 inputs, twice chained
F = len(build_ops()[0])
n1, nG, n5 = sizes['phase1'], sizes['GA'], sizes['R5']
assert sizes['GB'] == nG
loop = 1 + 5 + 3 * 2 + 2 * 1                               # pointer init, pointer steps, exit test after each GA, jump after each GB
Bcore = step_count(secs)
assert Bcore == n1 + 5 * nG + n5 + loop + 2 + 3
print('F =', F, ' step of 256 walks: phase 1', n1, '+ 5 rounds x', nG, '+ last round', n5, '+ loop', loop, '+ prefilter test 2 + counter 3 =', Bcore)

# ---- parameters of the search ----
L, Hb, U = 256, 116, 5000                                    # walks, distinguished-point bits (theta = 2^-116), trail limit = table slots
S = U
Lc = 2 ** 120 - 2                                           # trail cap in steps
n = D(2) ** 256
theta = D(2) ** -Hb
J = 2 ** 16                                                 # bins of the remaining trail length
w = 2 ** 104
lq = (1 - theta).ln()


def success(Tb):
    """Lower bound on the success probability of one attempt of Tb batch steps (Section 6)."""
    s = D(0)
    qprev = D(1)
    for j in range(1, J):
        qj = (w * j * lq).exp()
        e = L * (Tb - j * w)
        if e > 1:
            s += (qprev - qj) * (1 - (-D(e) * (e - 1) / (2 * n)).exp())
        qprev = qj
    kappa = D(Lc) * theta
    e1 = U * (-kappa).exp()                                  # F1: some trail of the attempt has no distinguished point within Lc steps
    mu, k = D(L * Tb) * theta, U - L
    e2 = (-mu + k * (1 + (mu / k).ln())).exp()               # F2: more than U - L distinguished points (Chernoff)
    e3 = D(U) * D(2) ** (2 * Hb) / n                         # F3: a coincidence inside one trail
    e4 = D(2) ** -90                                         # F4: starts, truncated-end matches, prefilter hits
    return s - (e1 + e2 + e3 + e4 + D(2) ** -60), (e1, e2, e3, e4)


TB = 17750576 * 2 ** 96                                                # least multiple of 2^96 with success >= 0.39 (checked below)
p, (e1, e2, e3, e4) = success(TB)
p_less, _ = success(TB - 2 ** 96)
assert p >= D('0.39') > p_less
print('Tb = %d = %.8f * 2^120' % (TB, D(TB) / D(2) ** 120), ' evaluations', L * TB, '= %.6f * 2^128' % (D(L * TB) / D(2) ** 128))
print('failure terms: F1 %.3e  F2 %.3e  F3 %.3e  F4 %.3e' % (e1, e2, e3, e4), ' success bound', str(p)[:12], ' (one step fewer by 2^96:', str(p_less)[:12], ')')

# ---- rare operations, each at most the count of its routine (Section 4) ----
hits = (TB * (1 + Fr(1, 2 ** 20))) // 2 ** 8 + 1             # prefilter hits: E / 2^16 (1 + 2^-20), 256 evaluations per step
C_hit = 205                                                  # slow test of a hit: 48 + 48 (lane 3) + 52 + 51 (lane 2) + 2 + 2 + 2 operations
C_dp = 640 + 4 + (10 * S + 20) + 6 + 2460 + 1100             # extract 123 end planes, pack, probe (at most S), store, restart a walk, next deadline
R = hits * C_hit + (U + 1) * C_dp + (U + 1) * 1300 + 700000 + 3000 + 1000
replay = (2 * F + 26) * Lc                                   # advance (F + 7 per step) + lock step (2F + 26 per iteration): at most (2F + 26) Lc
N = TB * Bcore + replay + R
print('main', TB * Bcore, ' replay', replay, ' rare R', R)
print('N =', N)

code = n1 + 2 * nG + n5 + 20 + 205 + 30 + 40 + 40 + 40 + 40 + (F + 120) + 20
data = 3200 + 256 + 5 + 512 + S + 64                           # planes: two buffers of 1600 and the 256 input planes; RC table; trail starts and ids; table; scratch
mem = 32 * (code + data)
mlog = D(mem).ln() / D(2).ln()
mlog = D(ceil(mlog * 10 ** 4)) / 10 ** 4
print('memory: code words', code, 'data words', data, 'bytes', mem, ' log2 =', mlog)

K = 100000
e = ceil(K * (D(N) / 1626).ln() / D(2).ln())
while N ** K > (1626 ** K) << e: e += 1
while N ** K <= (1626 ** K) << (e - 1): e -= 1
print('certificate: 1626^%d * 2^%d < N^%d <= 1626^%d * 2^%d' % (K, e - 1, K, K, e))
print('time_log2 = %d.%05d' % divmod(e, K))
print('S = time_log2 + max(0, memory_log2 - 20) = %s' % (D(e) / K + max(D(0), mlog - 20)))
```

Output:

```
instructions {'phase1': 2506, 'GA': 10063, 'GB': 10063, 'R5': 1169}
by kind (round code) {'and': 647, 'ld': 1626, 'or': 960, 'shr': 7, 'st': 1625, 'sub': 7, 'xor': 5191}
registers used by the straight-line code {'phase1': 12, 'GA': 44, 'GB': 44, 'R5': 8}  + 6 reserved for the loop and search state: at most 50 of 64
F = 1244  step of 256 walks: phase 1 2506 + 5 rounds x 10063 + last round 1169 + loop 14 + prefilter test 2 + counter 3 = 54009
Tb = 1406345520049800208543858999779393536 = 1.05801678 * 2^120  evaluations 360024453132748853387227903943524745216 = 1.058017 * 2^128
failure terms: F1 5.627e-04  F2 6.553e-09  F3 2.980e-04  F4 8.078e-28  success bound 0.3900000075  (one step fewer by 2^96: 0.3899999715 )
main 75955315192369659463245280719085265485824  replay 3341679181403278504480170949544786259036  rare R 1126176197481670109261685155142578695
N = 79298120549970419637834713353785194323555
memory: code words 25600 data words 9037 bytes 1108384  log2 = 20.0801
certificate: 1626^100000 * 2^12519729 < N^100000 <= 1626^100000 * 2^12519730
time_log2 = 125.19730
S = time_log2 + max(0, memory_log2 - 20) = 125.2774
```

so N = 79298120549970419637834713353785194323555
word operations and, by the integer certificate printed above,

    1626^100000 * 2^12519729 < N^100000 <= 1626^100000 * 2^12519730

time_log2 = log2(N/1626) rounded up at five decimals = 125.19730.


## Appendix B. Toy-width validation: preregistration, program, seeds and raw lines

Everything in this appendix is verbatim. The seeds of run i are the first 7 bytes (little-endian, masked to 56 bits) of SHA-256 of "s6d-prereg-2026-10-11/dense/i" and ".../scalar/i" (extension: "s6d-ext-2026-10-11/dense/i"). The runs: `./toy dense 56 16 1048576 1109659 1775454 5000 15 200 seeds_dense.txt out_dense.txt`, `./toy scalar 56 15 573440 267054329 0 8700 15 200 seeds_scalar.txt out_scalar.txt`, extension `./toy dense 56 16 1048576 1109659 1775454 5000 15 1000 seeds_dense_ext.txt out_dense_ext.txt`; CUDA 12.4 on an RTX 3090 (`nvcc -O3 -arch=sm_86`).

### B.1 Preregistration (written before the runs)

~~~
# Preregistration: toy-width validation of the dense lockstep distinguished-point rho (r6 memory-rule route)

Written before any toy run of this study (see the clock line at the end; file hashes of everything the runs read are recorded
there). Nothing below is changed after the runs.

## What is tested
The algorithm of the dense package (256 walks advanced in lockstep, one evaluation of f per walk per batch step; a walk that
reaches a distinguished point (DP) is recorded in a table keyed by its end and restarted; a walk with no DP after Lc steps is
restarted; the run halts at batch step Tb; a DP end already in the table is a duplicate endpoint, resolved by a replay), against
the one-walker rho of the one-walk package (control). Same function f at toy width: f(x) = low W = 56 bits of lane 0 of rounds 0-5
of Keccak-f[1600] on the state (lane0 = x, lane16 = 0x8600000000000000, other lanes 0); the same CUDA code runs both.
Starts of trail j: (rho + j) mod 2^56, rho a fresh random 56-bit word per run (SHA-256 of "s6d-prereg-2026-10-11/<dense|scalar>/<i>",
first 7 bytes; files seeds_dense.txt, seeds_scalar.txt). 200 runs each.

The toy is an exact scale model of the full design: the full design has n = 2^256, H = 116, so n = 2^(2(H+12)); the toy has
n = 2^56, H = 16, so the same relation holds and every ratio in the design (records per run mu = 4334, tail 256 2^H / sqrt(n) =
1/16, U / mu, U / (theta^2 n)) is the same.

## Parameters (computed by toy_params.py, predictions by predictions.py -> predictions.json, both unchanged by the runs)
Dense: L = 256, H = 16, kappa = 16 (Lc = 1,048,576), U = 5,000, Tb = 1,109,659 batch steps (= 284,072,704 evaluations), the least
Tb with (detection bound by the convolution over the remaining trail length) - (failure terms U e^-kappa, Chernoff, U 2^2H / n,
2^-90, 2^-60) >= 0.39. Run limit 1.6 Tb steps, or Tb steps when a duplicate was found earlier (the run continues to Tb to count duplicates).
Control (the one-walk package scaled to the same width): H = 15, kappa = 17.5 (Lc = 573,440), U = 8,700, m = 267,054,329 evaluations
(same formula as the package); trails start while E < m; halt when E >= m or 8,700 trails started.

## Statistics and declared pass rules (fixed now)
Band for a rate near 0.39 with 200 runs: 0.39 +- 2 sqrt(0.39 * 0.61 / 200) = [0.321, 0.459]. A replay of every first duplicate (walk both
trails to their ends, align, step both until the images agree) must show two different inputs with equal f.

Dense:
- A1 success at the design horizon (first duplicate at step <= Tb and replay real): rate in [0.321, 0.459]. Model 0.3909.
- A2 detected by n* = n0 + 256 * 2^H = 283,677,211 evaluations (earlier analysis: birthday point n0 = 266,899,995 plus L/theta): rate in [0.321, 0.459]. Model 0.3900.
- A3 median summed work to detection (256 * first duplicate step): within +-10% of the model 3.330e8.
- A4a max over runs of trails started by step Tb < U = 5,000 (the cap); A4b mean table records at Tb within +-1% of 4334.6.
- A5 mean duplicate endpoints met by step Tb within +-25% of 0.4958 (model (E - 256 2^H)^2 / 2n).
- A6 every first duplicate replays to a real collision (none is a start lying on the other trail, none has different ends).
- A7 dead trails over all 200 runs <= 3 (model 0.10).
Control:
- B1 success at the halt: rate in [0.321, 0.459]. Model 0.3903.
- B2 detected by n* = n0 + 2^H = 266,932,763: rate in [0.321, 0.459].
- B3 max trails < 8,700 and mean trails within +-1% of 8149.9.
- B4 mean duplicate endpoints within +-25% of 0.4949.
- B5 every first duplicate replays to a real collision.
- B6 mean evaluations at the halt / m in [1.0, 1.003].
Any criterion that fails is reported as failed; no criterion, band or parameter is edited after the runs, and no run is repeated except
for a crash. The statistics resolve gross errors (a factor of 2 in tail, cap, duplicate rate, or a success rate below 0.32); they cannot resolve a 3% shift.

## Commands (WSL, RTX 3090): see run_toy.sh. Dense and control are run one after the other (one process each).
~~~

### B.2 SHA-256 of the files the runs read (taken before the runs)

~~~
2d0676a0efc8659471c614df3ac29e8163938589a34dc03f86c49ddaac174153 *toy.cu
543551617c733f27721bbd3aa340d51e57c43913a4dace677d8469b32377cc7f *toy_params.py
8289a0b5854563168ae05ba3bf2578ad44ba815c9dbaaefa7e666c02e02198c6 *predictions.py
7326e278bf655ed636010f7b8d36d400dce4e02c1efde12d2b8a32a00e93563d *predictions.json
f8836f23e6fe9afd24d40dbb327bf9b57df84f07d517e3c4d7daace3f234f27c *analyze_toy.py
8b784108d11dae9dcea5a7223d61e23949061786e3837c8f0223ff195772f0c3 *seeds_dense.txt
5d5108f9ccfe630e649c05a1b4d9ad392e280176611f16e6fd30f1913534b1b9 *seeds_scalar.txt
a23497464ef596f6f54b3e69dca6ff04049ad13ba1fa23fb9c543aa27d9a5d5f *PREREG.md
~~~

### B.3 Parameters (toy_params.py)

~~~python
"""Toy parameters (exact scale model of the full-scale design) -- computed BEFORE any toy run.
Full scale: n = 2^256, L = 256 lanes, H = 116, kappa = 16, U = 5000.   Toy: n = 2^56, H = 16 (n = 2^(2(H+12)) in both)."""
from decimal import Decimal as D, getcontext
from math import isqrt, log
getcontext().prec = 60
def exp(x): return x.exp()
def success(Tb, n, H, Lc, J, eps, L=256):
    th = D(2) ** -H
    w = Lc // J
    s = D(0); qprev = D(1)
    a = D(w) * (1 - th).ln()
    for j in range(1, J + 1):
        qj = exp(a * j)
        e = L * (Tb - j * w)
        if e > 1:
            s += (qprev - qj) * (1 - exp(-D(e) * (e - 1) / (2 * n)))
        qprev = qj
    return s - eps
def dense_design(W, H, kap, U, J=2048, L=256, target=D('0.39')):
    n = D(2) ** W
    Lc = int(kap * 2 ** H)
    th = D(2) ** -H
    e1 = U * exp(-D(Lc) * th)
    e3 = D(U) * D(2) ** (2 * H) / n
    e4 = D(2) ** -90
    Tb = D(2) ** (W // 2 - 8) * D('1.06')
    for _ in range(3):
        mu = L * Tb * th; k = U - L
        e2 = exp(-mu + k * (1 + (mu / k).ln()))
        eps = e1 + e2 + e3 + e4 + D(2) ** -60
        lo, hi = D(2) ** (W // 2 - 8) * D('0.7'), D(2) ** (W // 2 - 8) * D('1.5')
        for _ in range(40):
            mid = (lo + hi) / 2
            if success(mid, n, H, Lc, J, eps) >= target: hi = mid
            else: lo = mid
        Tb = hi
    return dict(Tb=int(hi) + 1, mu=float(mu), eps=float(eps), e1=float(e1), e2=float(e2), e3=float(e3), Lc=Lc)
def scalar_design(W, H, kap2, U, target=D('0.39')):
    """one-walk-style scalar design: kappa = kap2/2, Lc = kappa 2^H."""
    n = D(2) ** W
    Lc = kap2 * 2 ** (H - 1); th = D(2) ** -H; kappa = D(kap2) / 2
    e1 = U * (-kappa).exp()
    mu = (D(2) ** (W // 2) + Lc) * th; k = U - 1
    e2 = (-mu + k * (1 + (mu / k).ln())).exp()
    e3 = D(U) * D(2) ** (2 * H) / n
    e4 = D(2) ** -90
    eps = e1 + e2 + e3 + e4
    need = -2 * n * (1 - target - D(2) ** -60 - eps).ln()
    m = isqrt(int(need)) + 2
    while m * (m - 1) < need: m += 1
    while (m - 1) * (m - 2) >= need: m -= 1
    return dict(m=m, Lc=int(Lc), eps=float(eps), mu=float(mu))
if __name__ == '__main__':
    import json
    W, H = 56, 16
    d = dense_design(W, H, 16, 5000)
    s = scalar_design(W, H - 1, 35, 8700)
    n = 2 ** W
    n0 = -2 * n * log(1 - 0.39)
    n0 = n0 ** 0.5
    out = dict(dense=d, scalar=s, n0=n0, tail_dense=256 * 2 ** H, tail_scalar=2 ** (H - 1))
    print(json.dumps(out, indent=1))
~~~

### B.4 Predictions (predictions.py) and their output (predictions.json)

~~~python
"""Model predictions for the toy runs, computed BEFORE the runs (random-function model, exact formulas)."""
from decimal import Decimal as D, getcontext
import toy_params as tp, json
getcontext().prec = 50
W, H = 56, 16
n = D(2) ** W
d = tp.dense_design(W, H, 16, 5000, J=2048)
s = tp.scalar_design(W, H - 1, 35, 8700)
Tb = d['Tb']; Lc = d['Lc']
th = D(2) ** -H
# model probability that the first coincidence's trail completes by batch step Tb (no failure terms)
def p_detect(Tb_, J=4096):
    return tp.success(D(Tb_), n, H, Lc, J, D(0))
def solve_quantile(p, J=4096):
    lo, hi = D(2) ** 19, D(2) ** 22
    for _ in range(50):
        mid = (lo + hi) / 2
        if tp.success(mid, n, H, Lc, J, D(0)) >= p: hi = mid
        else: lo = mid
    return hi
n0 = (-2 * n * (1 - D('0.39')).ln()).sqrt()
nstar_dense = n0 + 256 * 2 ** H
nstar_scalar = n0 + 2 ** (H - 1)
out = {}
out['dense'] = dict(Tb=Tb, E_h=256 * Tb, Lc=Lc, U=5000,
    p_detect_at_horizon=float(p_detect(Tb)),
    n0=float(n0), nstar=float(nstar_dense),
    p_detect_at_nstar=float(p_detect(nstar_dense / 256)),
    median_E=float(256 * solve_quantile(D('0.5'))),
    mean_trails_at_T=float(256 + 256 * Tb * th), mean_rec_at_T=float(256 * Tb * th),
    mean_dups_at_T=float((D(256 * Tb) - 256 * 2 ** H) ** 2 / (2 * n)),
    expected_dead=float((256 + 256 * Tb * th) * (-D(Lc) * th).exp()))
m = s['m']
out['scalar'] = dict(m=m, Lc=s['Lc'], U=8700, p_detect_at_halt=float(1 - (-D(m) * (m - 1) / (2 * n)).exp()),
    nstar=float(nstar_scalar), mean_trails=float(m * D(2) ** -(H - 1)), mean_rec=float(m * D(2) ** -(H - 1)),
    mean_dups=float(D(m) ** 2 / (2 * n)), mean_E_at_halt=float(m + 2 ** (H - 1)))
print(json.dumps(out, indent=1))
json.dump(out, open('predictions.json', 'w'), indent=1)

# ---- output ----
{
 "dense": {
  "Tb": 1109659,
  "E_h": 284072704,
  "Lc": 1048576,
  "U": 5000,
  "p_detect_at_horizon": 0.3909346881584988,
  "n0": 266899995.09842786,
  "nstar": 283677211.09842783,
  "p_detect_at_nstar": 0.3900447103493618,
  "median_E": 333001653.5414449,
  "mean_trails_at_T": 4590.60546875,
  "mean_rec_at_T": 4334.60546875,
  "mean_dups_at_T": 0.4957623055493059,
  "expected_dead": 0.0005166045884929676
 },
 "scalar": {
  "m": 267054329,
  "Lc": 573440,
  "U": 8700,
  "p_detect_at_halt": 0.3903487064304327,
  "nstar": 266932763.09842786,
  "mean_trails": 8149.851348876953,
  "mean_rec": 8149.851348876953,
  "mean_dups": 0.49486813700788834,
  "mean_E_at_halt": 267087097.0
 }
}
~~~

### B.5 Analysis (analyze_toy.py)

~~~python
"""Preregistered analysis of the toy runs (criteria fixed in PREREG.md before the runs)."""
import json, sys, math
pred = json.load(open('predictions.json'))
def load(fn):
    rows = []
    for line in open(fn).read().split('\n')[1:]:
        if not line.strip(): continue
        p = line.split()
        rows.append(dict(run=int(p[0]), first=int(p[2]), idA=int(p[3]), idB=int(p[4]), dT=int(p[6]), dtot=int(p[7]), recT=int(p[8]),
                         rec=int(p[9]), trT=int(p[10]), dead=int(p[11]), steps=int(p[12]), rep=int(p[13]), la=int(p[14]), lb=int(p[15])))
    return rows
def band(v, c, w): return c - w <= v <= c + w
def cp(k, n, a=0.05):
    from math import comb
    # exact Clopper-Pearson via bisection on the binomial cdf
    def cdf(kk, p): return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(kk + 1))
    lo, hi = 0.0, 1.0
    if k == 0: lo_ = 0.0
    else:
        l, h = 0.0, 1.0
        for _ in range(60):
            mid = (l + h) / 2
            if 1 - cdf(k - 1, mid) > a / 2: h = mid
            else: l = mid
        lo_ = h
    if k == n: hi_ = 1.0
    else:
        l, h = 0.0, 1.0
        for _ in range(60):
            mid = (l + h) / 2
            if cdf(k, mid) > a / 2: l = mid
            else: h = mid
        hi_ = l
    return lo_, hi_
res = {}
ok_all = True
def check(name, val, passed, extra=''):
    global ok_all
    ok_all &= bool(passed)
    print('%-58s %-22s %s %s' % (name, val, 'PASS' if passed else 'FAIL', extra))
sd = 0.0345; lo_b, hi_b = 0.39 - 2 * sd, 0.39 + 2 * sd
if len(sys.argv) > 1 and sys.argv[1] == 'dense':
    R = load('out_dense.txt'); N = len(R); P = pred['dense']
    det = [r for r in R if r['first'] > 0 and r['first'] <= P['Tb'] and r['rep'] == 1]
    k = len(det); lo, hi = cp(k, N)
    check('A1 success at the design horizon (rate)', '%.4f (%d/%d)' % (k / N, k, N), lo_b <= k / N <= hi_b, 'CI95 [%.3f, %.3f]; band [%.3f, %.3f]; model %.4f' % (lo, hi, lo_b, hi_b, P['p_detect_at_horizon']))
    k2 = sum(1 for r in R if r['first'] > 0 and 256 * r['first'] <= P['nstar'] and r['rep'] == 1)
    check('A2 detected by n* = n0 + 256 2^H (rate)', '%.4f (%d/%d)' % (k2 / N, k2, N), lo_b <= k2 / N <= hi_b, 'n*=%.0f model %.4f' % (P['nstar'], P['p_detect_at_nstar']))
    works = sorted([256 * r['first'] if r['first'] > 0 else float('inf') for r in R])
    med = (works[N // 2 - 1] + works[N // 2]) / 2
    check('A3 median summed work to detection', '%.4g' % med, abs(med / P['median_E'] - 1) <= 0.10, 'model %.4g (band +-10%%)' % P['median_E'])
    mrec = sum(r['recT'] for r in R) / N; mxtr = max(r['trT'] for r in R); mxrec = max(r['recT'] for r in R)
    check('A4a max trails at the horizon < U=5000', '%d (max rec %d)' % (mxtr, mxrec), mxtr < 5000)
    check('A4b mean records at the horizon', '%.1f' % mrec, abs(mrec / P['mean_rec_at_T'] - 1) <= 0.01, 'model %.1f (band +-1%%)' % P['mean_rec_at_T'])
    mdup = sum(r['dT'] for r in R) / N
    check('A5 mean duplicate endpoints at the horizon', '%.3f' % mdup, 0.75 * P['mean_dups_at_T'] <= mdup <= 1.25 * P['mean_dups_at_T'], 'model %.4f (band +-25%%); rate per record %.3g' % (P['mean_dups_at_T'], mdup / mrec))
    bad = [r['run'] for r in R if r['first'] > 0 and r['rep'] != 1]
    check('A6 every first duplicate replays to a real collision', 'bad runs %s' % bad, not bad)
    dead = sum(r['dead'] for r in R)
    check('A7 dead trails over all runs (model %.2f)' % (200 * P['expected_dead']), dead, dead <= 3)
    ndet = sum(1 for r in R if r['first'] > 0)
    print('info: detected at all (cap 1.6 horizon) %d/%d; mean trails at T %.1f; max trails %d; mean dups_total %.3f; mean la+lb of replay %.0f' % (ndet, N, sum(r['trT'] for r in R) / N, mxtr, sum(r['dtot'] for r in R) / N, sum(r['la'] + r['lb'] for r in R if r['first'] > 0) / max(1, ndet)))
else:
    R = load('out_scalar.txt'); N = len(R); P = pred['scalar']
    det = [r for r in R if r['first'] > 0 and r['rep'] == 1]
    k = len(det); lo, hi = cp(k, N)
    check('B1 success at the halt (rate)', '%.4f (%d/%d)' % (k / N, k, N), lo_b <= k / N <= hi_b, 'CI95 [%.3f, %.3f]; model %.4f' % (lo, hi, P['p_detect_at_halt']))
    k2 = sum(1 for r in R if r['first'] > 0 and r['first'] <= P['nstar'] and r['rep'] == 1)
    check('B2 detected by n* = n0 + 2^H (rate)', '%.4f (%d/%d)' % (k2 / N, k2, N), lo_b <= k2 / N <= hi_b, 'n*=%.0f' % P['nstar'])
    mtr = sum(r['trT'] for r in R) / N; mx = max(r['trT'] for r in R)
    check('B3 max trails < U=8700 (no U-halt); mean trails', '%d; mean %.1f' % (mx, mtr), mx < 8700 and abs(mtr / P['mean_trails'] - 1) <= 0.01, 'model %.1f' % P['mean_trails'])
    mdup = sum(r['dT'] for r in R) / N
    check('B4 mean duplicate endpoints', '%.3f' % mdup, 0.75 * P['mean_dups'] <= mdup <= 1.25 * P['mean_dups'], 'model %.4f' % P['mean_dups'])
    bad = [r['run'] for r in R if r['first'] > 0 and r['rep'] != 1]
    check('B5 every first duplicate replays to a real collision', 'bad runs %s' % bad, not bad)
    mE = sum(r['steps'] for r in R) / N
    check('B6 mean evaluations at the halt / m', '%.6f' % (mE / P['m']), 1.0 <= mE / P['m'] <= 1.003, 'model %.6f' % (P['mean_E_at_halt'] / P['m']))
    print('info: dead trails total %d; U-halts %d' % (sum(r['dead'] for r in R), 0))
print('ALL PASS' if ok_all else 'SOME CRITERION FAILED')
~~~

### B.6 The GPU program (toy.cu)

~~~cuda
// Toy-width validation of the lockstep 256-lane distinguished-point rho (dense) and of the scalar rho (control).
// f(x) = low W bits of lane 0 of rounds 0..5 of Keccak-f[1600] on the state: lane0 = x (W bits), lane16 = 0x86<<56, rest 0.
// Usage: toy dense|scalar|test  params...   (see main)
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
typedef unsigned long long u64;
typedef unsigned int u32;

#define RCc_DEF constexpr u64 RCc[6] = {0x1ULL, 0x8082ULL, 0x800000000000808AULL, 0x8000000080008000ULL, 0x808BULL, 0x80000001ULL}
#define ROTc_DEF constexpr int ROTc[5][5] = {{0, 36, 3, 41, 18}, {1, 44, 10, 45, 2}, {62, 6, 43, 15, 61}, {28, 55, 25, 21, 56}, {27, 20, 39, 8, 14}}

__device__ __forceinline__ u64 rol(u64 v, int r) { return r ? (v << r) | (v >> (64 - r)) : v; }

__device__ __forceinline__ u64 fkeccak(u64 x, u64 mask) {
    RCc_DEF; ROTc_DEF;
    u64 a[25];
#pragma unroll
    for (int i = 0; i < 25; i++) a[i] = 0;
    a[0] = x;
    a[16] = 0x8600000000000000ULL;
#pragma unroll
    for (int r = 0; r < 6; r++) {
        u64 c[5], d[5], b[25];
#pragma unroll
        for (int xx = 0; xx < 5; xx++) c[xx] = a[xx] ^ a[xx + 5] ^ a[xx + 10] ^ a[xx + 15] ^ a[xx + 20];
#pragma unroll
        for (int xx = 0; xx < 5; xx++) d[xx] = c[(xx + 4) % 5] ^ rol(c[(xx + 1) % 5], 1);
#pragma unroll
        for (int xx = 0; xx < 5; xx++)
#pragma unroll
            for (int yy = 0; yy < 5; yy++) b[yy + 5 * ((2 * xx + 3 * yy) % 5)] = rol(a[xx + 5 * yy] ^ d[xx], ROTc[xx][yy]);
#pragma unroll
        for (int yy = 0; yy < 5; yy++)
#pragma unroll
            for (int xx = 0; xx < 5; xx++) a[xx + 5 * yy] = b[xx + 5 * yy] ^ (~b[(xx + 1) % 5 + 5 * yy] & b[(xx + 2) % 5 + 5 * yy]);
        a[0] ^= RCc[r];
    }
    return a[0] & mask;
}

struct Params {
    int W, H;
    u64 Lc;          // trail cap (steps)
    u64 Tb;          // horizon in batch steps (dense) or m evaluations (scalar)
    u64 capsteps;    // run limit in batch steps (dense) or evaluations (scalar)
    int U;           // trail/record cap of the design
    int TS_log;      // log2 table slots
};

struct RunOut {
    u64 first_dup_step;   // batch step (dense) / evaluation count at detection (scalar); 0 = none
    u64 idA, idB, endv;
    u32 dups_at_T;        // duplicate endpoints met up to the horizon
    u32 dups_total;
    u32 rec_at_T;         // table entries at the horizon
    u32 rec_total;
    u32 trails_at_T;
    u32 dead_total;
    u32 started_before_m; // scalar: trail count when halting rule would stop (info)
    u64 steps_done;
};

__device__ __forceinline__ u32 hslot(u64 end, int H, int TS_log) {
    return (u32)(((end >> H) * 0x9E3779B97F4A7C15ULL) >> (64 - TS_log));
}

__global__ void dense_kernel(Params P, const u64* rho, RunOut* out, u64* tabkey, u32* tabid) {
    int run = blockIdx.x, l = threadIdx.x;
    __shared__ u64 lx[256];
    __shared__ u32 lid[256];
    __shared__ u32 lage[256];
    __shared__ unsigned char flag[256];
    __shared__ u32 next_id, recs, dups, dead, recs_T, dups_T, trails_T;
    __shared__ u64 fdstep, fa, fb, fend;
    __shared__ int stop;
    u64 mask = (P.W == 64) ? ~0ULL : ((1ULL << P.W) - 1);
    u64 dpmask = (1ULL << P.H) - 1;
    u64 r0 = rho[run];
    u64* tk = tabkey + (size_t)run * (1u << P.TS_log);
    u32* ti = tabid + (size_t)run * (1u << P.TS_log);
    if (l == 0) { next_id = 256; recs = dups = dead = recs_T = dups_T = trails_T = 0; fdstep = 0; stop = 0; }
    lid[l] = l; lx[l] = (r0 + l) & mask; lage[l] = 0;
    for (u32 i = l; i < (1u << P.TS_log); i += 256) tk[i] = 0;
    __syncthreads();
    u64 step = 0;
    for (;;) {
        step++;
        u64 x = fkeccak(lx[l], mask);
        u32 age = lage[l] + 1;
        int fl = 0;
        if ((x & dpmask) == 0) fl = 1;
        else if (age == (u32)P.Lc) fl = 2;
        lx[l] = x; lage[l] = age; flag[l] = (unsigned char)fl;
        int any = __syncthreads_or(fl != 0);
        if (any) {
            if (l == 0) {
                for (int i = 0; i < 256; i++) {
                    int f = flag[i];
                    if (!f) continue;
                    if (f == 1) {
                        u64 e = lx[i];
                        u64 key = e | 1ULL;
                        u32 s = hslot(e, P.H, P.TS_log);
                        u32 mk = (1u << P.TS_log) - 1;
                        bool found = false;
                        while (tk[s] != 0) { if (tk[s] == key) { found = true; break; } s = (s + 1) & mk; }
                        if (found) {
                            dups++;
                            if (step <= P.Tb) dups_T++;
                            if (fdstep == 0) { fdstep = step; fa = ti[s]; fb = lid[i]; fend = e; }
                        } else {
                            tk[s] = key; ti[s] = lid[i]; recs++;
                            if (step <= P.Tb) recs_T++;
                        }
                    } else dead++;
                    u32 nid = next_id++;
                    lid[i] = nid; lx[i] = (r0 + nid) & mask; lage[i] = 0;
                }
                if (step <= P.Tb) trails_T = next_id;
            }
            __syncthreads();
        }
        if (l == 0) {
            if (step == P.Tb) trails_T = next_id;
            if (step >= P.Tb && fdstep != 0) stop = 1;
            if (step >= P.capsteps) stop = 1;
        }
        __syncthreads();
        if (stop) break;
    }
    if (l == 0) {
        RunOut& o = out[run];
        o.first_dup_step = fdstep; o.idA = fa; o.idB = fb; o.endv = fend;
        o.dups_at_T = dups_T; o.dups_total = dups; o.rec_at_T = recs_T; o.rec_total = recs; o.trails_at_T = trails_T;
        o.dead_total = dead; o.steps_done = step;
    }
}

// scalar control: one-walk-style, one trail after another, while E < m (the design halt) ; also halts when U trails are started.
__global__ void scalar_kernel(Params P, const u64* rho, RunOut* out, u64* tabkey, u32* tabid, int nruns) {
    int run = blockIdx.x * blockDim.x + threadIdx.x;
    if (run >= nruns) return;
    u64 mask = (P.W == 64) ? ~0ULL : ((1ULL << P.W) - 1);
    u64 dpmask = (1ULL << P.H) - 1;
    u64 r0 = rho[run];
    u64* tk = tabkey + (size_t)run * (1u << P.TS_log);
    u32* ti = tabid + (size_t)run * (1u << P.TS_log);
    u32 mk = (1u << P.TS_log) - 1;
    for (u32 i = 0; i <= mk; i++) tk[i] = 0;
    u64 E = 0; u32 trails = 0, recs = 0, dups = 0, dead = 0, uhalt = 0;
    u64 fdE = 0, fa = 0, fb = 0, fend = 0;
    for (;;) {
        if (E >= P.Tb) break;
        if (trails == (u32)P.U) { uhalt = 1; break; }
        u32 id = trails++;
        u64 x = (r0 + id) & mask;
        u64 c = 0; bool isdp = false;
        for (;;) {
            x = fkeccak(x, mask); c++;
            if ((x & dpmask) == 0) { isdp = true; break; }
            if (c == P.Lc) break;
        }
        E += c;
        if (!isdp) { dead++; continue; }
        u64 key = x | 1ULL; u32 s = hslot(x, P.H, P.TS_log);
        bool found = false;
        while (tk[s] != 0) { if (tk[s] == key) { found = true; break; } s = (s + 1) & mk; }
        if (found) {
            dups++;
            if (fdE == 0) { fdE = E; fa = ti[s]; fb = id; fend = x; }
        } else { tk[s] = key; ti[s] = id; recs++; }
    }
    RunOut& o = out[run];
    o.first_dup_step = fdE; o.idA = fa; o.idB = fb; o.endv = fend; o.dups_at_T = dups; o.dups_total = dups;
    o.rec_at_T = recs; o.rec_total = recs; o.trails_at_T = trails; o.dead_total = dead; o.steps_done = E; o.started_before_m = uhalt;
}

// replay: from the two starts with equal ends, find the first merge. Returns 1 if two different inputs with equal f are found.
__global__ void replay_kernel(Params P, const u64* rho, const RunOut* out, int* res, u64* lens, int nruns) {
    int run = blockIdx.x * blockDim.x + threadIdx.x;
    if (run >= nruns) return;
    const RunOut& o = out[run];
    res[run] = -1;
    if (o.first_dup_step == 0) return;
    u64 mask = (P.W == 64) ? ~0ULL : ((1ULL << P.W) - 1);
    u64 dpmask = (1ULL << P.H) - 1;
    u64 sa = (rho[run] + o.idA) & mask, sb = (rho[run] + o.idB) & mask;
    u64 la = 0, lb = 0, x = sa;
    while (la < 4 * P.Lc) { x = fkeccak(x, mask); la++; if ((x & dpmask) == 0) break; }
    u64 ea = x; x = sb;
    while (lb < 4 * P.Lc) { x = fkeccak(x, mask); lb++; if ((x & dpmask) == 0) break; }
    u64 eb = x;
    lens[2 * run] = la; lens[2 * run + 1] = lb;
    if (ea != eb) { res[run] = -2; return; }
    u64 a = sa, b = sb;
    if (la > lb) { for (u64 i = 0; i < la - lb; i++) a = fkeccak(a, mask); }
    else if (lb > la) { for (u64 i = 0; i < lb - la; i++) b = fkeccak(b, mask); }
    if (a == b) { res[run] = 0; return; }       // one start on the other trail: no collision
    for (u64 i = 0; i < 2 * P.Lc + 10; i++) {
        u64 na = fkeccak(a, mask), nb = fkeccak(b, mask);
        if (na == nb) { res[run] = 1; return; }
        a = na; b = nb;
    }
    res[run] = -3;
}

__global__ void test_kernel(const u64* in, u64* outv, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) outv[i] = fkeccak(in[i], ~0ULL);
}

static void ck(cudaError_t e, const char* w) { if (e != cudaSuccess) { fprintf(stderr, "CUDA error %s: %s\n", w, cudaGetErrorString(e)); exit(2); } }

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    const char* mode = argv[1];
    if (!strcmp(mode, "test")) {
        std::vector<u64> in(64), o(64);
        for (int i = 0; i < 64; i++) in[i] = 0x0123456789abcdefULL * (u64)(i + 1) ^ (u64)i * 0xdeadbeefULL;
        u64 *din, *dout; cudaMalloc(&din, 512); cudaMalloc(&dout, 512);
        cudaMemcpy(din, in.data(), 512, cudaMemcpyHostToDevice);
        test_kernel<<<1, 64>>>(din, dout, 64);
        cudaMemcpy(o.data(), dout, 512, cudaMemcpyDeviceToHost);
        for (int i = 0; i < 64; i++) printf("%016llx %016llx\n", in[i], o[i]);
        return 0;
    }
    // args: mode W H Lc Tb capsteps U TS_log nruns seedfile outfile
    Params P;
    P.W = atoi(argv[2]); P.H = atoi(argv[3]); P.Lc = strtoull(argv[4], 0, 10); P.Tb = strtoull(argv[5], 0, 10);
    P.capsteps = strtoull(argv[6], 0, 10); P.U = atoi(argv[7]); P.TS_log = atoi(argv[8]);
    int nruns = atoi(argv[9]);
    FILE* f = fopen(argv[10], "r");
    std::vector<u64> rho(nruns);
    for (int i = 0; i < nruns; i++) { unsigned long long v; if (fscanf(f, "%llx", &v) != 1) { fprintf(stderr, "seed file short\n"); return 3; } rho[i] = v; }
    fclose(f);
    u64 *drho, *dtk, *dlens; u32* dti; RunOut* dout; int* dres;
    size_t slots = (size_t)1 << P.TS_log;
    ck(cudaMalloc(&drho, nruns * 8), "m1"); ck(cudaMalloc(&dtk, slots * 8 * nruns), "m2"); ck(cudaMalloc(&dti, slots * 4 * nruns), "m3");
    ck(cudaMalloc(&dout, nruns * sizeof(RunOut)), "m4"); ck(cudaMalloc(&dres, nruns * 4), "m5"); ck(cudaMalloc(&dlens, nruns * 16), "m6");
    cudaMemcpy(drho, rho.data(), nruns * 8, cudaMemcpyHostToDevice);
    cudaMemset(dout, 0, nruns * sizeof(RunOut));
    if (!strcmp(mode, "dense")) dense_kernel<<<nruns, 256>>>(P, drho, dout, dtk, dti);
    else scalar_kernel<<<(nruns + 31) / 32, 32>>>(P, drho, dout, dtk, dti, nruns);
    ck(cudaGetLastError(), "launch"); ck(cudaDeviceSynchronize(), "run");
    replay_kernel<<<(nruns + 31) / 32, 32>>>(P, drho, dout, dres, dlens, nruns);
    ck(cudaGetLastError(), "launch2"); ck(cudaDeviceSynchronize(), "replay");
    std::vector<RunOut> ho(nruns); std::vector<int> hr(nruns); std::vector<u64> hl(2 * nruns);
    cudaMemcpy(ho.data(), dout, nruns * sizeof(RunOut), cudaMemcpyDeviceToHost);
    cudaMemcpy(hr.data(), dres, nruns * 4, cudaMemcpyDeviceToHost);
    cudaMemcpy(hl.data(), dlens, nruns * 16, cudaMemcpyDeviceToHost);
    FILE* g = fopen(argv[11], "w");
    fprintf(g, "run rho first_dup idA idB end dups_at_T dups_total rec_at_T rec_total trails_at_T dead steps_done replay la lb\n");
    for (int i = 0; i < nruns; i++) {
        RunOut& o = ho[i];
        fprintf(g, "%d %llx %llu %llu %llu %llx %u %u %u %u %u %u %llu %d %llu %llu\n", i, (unsigned long long)rho[i], (unsigned long long)o.first_dup_step,
                (unsigned long long)o.idA, (unsigned long long)o.idB, (unsigned long long)o.endv, o.dups_at_T, o.dups_total, o.rec_at_T, o.rec_total,
                o.trails_at_T, o.dead_total, (unsigned long long)o.steps_done, hr[i], (unsigned long long)hl[2 * i], (unsigned long long)hl[2 * i + 1]);
    }
    fclose(g);
    return 0;
}
~~~

### B.7 Raw lines, dense search (out_dense.txt; first_dup in steps, replay 1 = two different inputs with equal f)

~~~
run first_dup replay dups_at_T rec_at_T trails_at_T dead
0 839919 1 1 4323 4580 0
1 1143442 1 0 4281 4537 0
2 377727 1 1 4322 4579 0
3 882836 1 1 4376 4633 0
4 1545924 1 0 4274 4530 0
5 0 -1 0 4232 4488 0
6 1664136 1 0 4360 4616 0
7 392922 1 1 4245 4502 0
8 1647750 1 0 4345 4601 0
9 0 -1 0 4270 4526 0
10 1557839 1 0 4278 4534 0
11 1619911 1 0 4334 4590 0
12 263262 1 1 4271 4528 0
13 1250138 1 0 4315 4571 0
14 0 -1 0 4335 4591 0
15 993105 1 1 4415 4672 0
16 790390 1 1 4324 4581 0
17 0 -1 0 4234 4490 0
18 981441 1 2 4380 4638 0
19 1431708 1 0 4268 4524 0
20 0 -1 0 4378 4634 0
21 1243809 1 0 4348 4604 0
22 0 -1 0 4399 4655 0
23 1193111 1 0 4267 4523 0
24 441570 1 1 4374 4631 0
25 577322 1 3 4242 4501 0
26 720534 1 1 4265 4522 0
27 1223651 1 0 4386 4642 0
28 405100 1 1 4302 4559 0
29 1067906 1 1 4261 4518 0
30 1602145 1 0 4340 4596 0
31 0 -1 0 4286 4542 0
32 1342818 1 0 4294 4550 0
33 1683661 1 0 4224 4480 0
34 584212 1 1 4474 4731 0
35 1384623 1 0 4317 4573 0
36 1571688 1 0 4374 4630 0
37 0 -1 0 4270 4526 0
38 1767093 1 0 4369 4625 0
39 486812 1 1 4348 4605 0
40 0 -1 0 4451 4707 0
41 931555 1 1 4293 4550 0
42 1749229 1 0 4321 4577 0
43 604112 1 1 4443 4700 0
44 1475577 1 0 4284 4540 0
45 1678603 1 0 4386 4642 0
46 1418346 1 0 4340 4596 0
47 714149 1 4 4352 4612 0
48 0 -1 0 4308 4564 0
49 0 -1 0 4328 4584 0
50 1415768 1 0 4305 4561 0
51 1338430 1 0 4377 4633 0
52 708290 1 1 4339 4596 0
53 1000484 1 1 4255 4512 0
54 0 -1 0 4392 4648 0
55 1629648 1 0 4411 4667 0
56 915150 1 1 4340 4597 0
57 0 -1 0 4388 4644 0
58 353496 1 1 4439 4696 0
59 1461855 1 0 4353 4609 0
60 631685 1 3 4250 4509 0
61 1689620 1 0 4347 4603 0
62 1171221 1 0 4340 4596 0
63 1272147 1 0 4360 4616 0
64 0 -1 0 4194 4450 0
65 1439446 1 0 4352 4608 0
66 831606 1 2 4197 4455 0
67 1759892 1 0 4231 4487 0
68 0 -1 0 4292 4548 0
69 0 -1 0 4322 4578 0
70 1197222 1 0 4437 4693 0
71 1334670 1 0 4287 4543 0
72 0 -1 0 4348 4604 0
73 778359 1 1 4342 4599 0
74 0 -1 0 4321 4577 0
75 0 -1 0 4441 4697 0
76 1180225 1 0 4365 4621 0
77 1133956 1 0 4432 4688 0
78 0 -1 0 4365 4621 0
79 867189 1 1 4408 4665 0
80 0 -1 0 4362 4618 0
81 924957 1 1 4278 4535 0
82 0 -1 0 4387 4643 0
83 0 -1 0 4370 4626 0
84 1154535 1 0 4323 4579 0
85 1009028 1 1 4322 4579 0
86 600557 1 1 4193 4450 0
87 1037058 1 1 4312 4569 0
88 275874 1 1 4301 4558 0
89 1060391 1 1 4418 4675 0
90 0 -1 0 4302 4558 0
91 587982 1 2 4245 4503 0
92 1116799 1 0 4359 4615 0
93 0 -1 0 4398 4654 0
94 0 -1 0 4328 4584 0
95 547678 1 2 4407 4665 0
96 1460792 1 0 4341 4597 0
97 1395767 1 0 4465 4721 0
98 0 -1 0 4396 4652 0
99 478682 1 1 4405 4662 0
100 1321257 1 0 4271 4527 0
101 0 -1 0 4331 4587 0
102 1150307 1 0 4383 4639 0
103 915383 1 1 4460 4717 0
104 0 -1 0 4386 4642 0
105 0 -1 0 4265 4521 0
106 270320 1 2 4387 4645 0
107 1202308 1 0 4452 4708 0
108 0 -1 0 4373 4629 0
109 0 -1 0 4488 4744 0
110 1262408 1 0 4320 4576 0
111 0 -1 0 4293 4549 0
112 0 -1 0 4285 4541 0
113 0 -1 0 4351 4607 0
114 1347207 1 0 4362 4618 0
115 976137 1 1 4344 4601 0
116 1293899 1 0 4334 4590 0
117 930037 1 1 4356 4613 0
118 0 -1 0 4280 4536 0
119 0 -1 0 4306 4562 0
120 1057482 1 1 4239 4496 0
121 0 -1 0 4357 4613 0
122 0 -1 0 4246 4502 0
123 0 -1 0 4389 4645 0
124 1503673 1 0 4325 4581 0
125 0 -1 0 4547 4803 0
126 494724 1 2 4433 4691 0
127 0 -1 0 4394 4650 0
128 1397281 1 0 4362 4618 0
129 1281540 1 0 4283 4539 0
130 0 -1 0 4290 4546 0
131 1632595 1 0 4481 4737 0
132 1475582 1 0 4420 4676 0
133 1113975 1 0 4346 4602 0
134 0 -1 0 4360 4616 0
135 0 -1 0 4345 4601 0
136 1003211 1 1 4283 4540 0
137 448466 1 1 4411 4668 0
138 1736014 1 0 4246 4502 0
139 1211144 1 0 4329 4585 0
140 912513 1 1 4382 4639 0
141 1320807 1 0 4313 4569 0
142 1460395 1 0 4274 4530 0
143 517354 1 1 4265 4522 0
144 1005653 1 1 4373 4630 0
145 1305137 1 0 4361 4617 0
146 367259 1 2 4270 4528 0
147 1513226 1 0 4326 4582 0
148 1558497 1 0 4291 4547 0
149 1533278 1 0 4271 4527 0
150 0 -1 0 4423 4679 0
151 1124801 1 0 4410 4666 0
152 319110 1 1 4369 4626 0
153 0 -1 0 4322 4578 0
154 1592718 1 0 4365 4621 0
155 810523 1 2 4296 4554 0
156 1472711 1 0 4384 4640 0
157 463803 1 1 4408 4665 0
158 611264 1 2 4453 4711 0
159 533576 1 2 4298 4556 0
160 711809 1 1 4396 4653 0
161 1150448 1 0 4388 4644 0
162 0 -1 0 4432 4688 0
163 890798 1 1 4313 4570 0
164 1419893 1 0 4292 4548 0
165 712200 1 1 4425 4682 0
166 342082 1 1 4286 4543 0
167 795878 1 1 4270 4527 0
168 0 -1 0 4333 4589 0
169 0 -1 0 4310 4566 0
170 1390811 1 0 4476 4732 0
171 0 -1 0 4215 4471 0
172 0 -1 0 4285 4541 0
173 0 -1 0 4354 4610 0
174 1658321 1 0 4363 4619 0
175 1496581 1 0 4347 4603 0
176 975548 1 1 4235 4492 0
177 0 -1 0 4317 4573 0
178 1220634 1 0 4403 4659 0
179 638322 1 1 4265 4522 0
180 0 -1 0 4337 4593 0
181 0 -1 0 4423 4679 0
182 923895 1 1 4403 4660 0
183 1560355 1 0 4341 4597 0
184 1459032 1 0 4365 4621 0
185 0 -1 0 4323 4579 0
186 655278 1 1 4249 4506 0
187 1370258 1 0 4261 4517 0
188 333392 1 1 4312 4569 0
189 1278312 1 0 4324 4580 0
190 281211 1 1 4515 4772 0
191 0 -1 0 4385 4641 0
192 445149 1 1 4324 4581 0
193 1293443 1 0 4403 4659 0
194 1556246 1 0 4192 4448 0
195 190137 1 1 4265 4522 0
196 1559258 1 0 4361 4617 0
197 0 -1 0 4405 4661 0
198 0 -1 0 4236 4492 0
199 1073979 1 1 4281 4538 0
~~~

### B.8 Raw lines, control (out_scalar.txt)

~~~
run first_dup_eval replay dups rec trails dead evals_at_halt
0 178223621 1 1 8016 8017 0 267059849
1 0 -1 0 8020 8020 0 267107627
2 0 -1 0 8176 8176 0 267054643
3 0 -1 0 8142 8142 0 267070462
4 0 -1 0 8194 8194 0 267109237
5 0 -1 0 8250 8250 0 267075569
6 0 -1 0 8242 8242 0 267133860
7 0 -1 0 8092 8092 0 267091806
8 160838796 1 1 8082 8083 0 267076375
9 0 -1 0 8165 8165 0 267096917
10 0 -1 0 8205 8205 0 267063008
11 122784532 1 1 8064 8065 0 267056239
12 0 -1 0 8094 8094 0 267085536
13 0 -1 0 8007 8007 0 267087604
14 247528277 1 1 8190 8191 0 267054576
15 0 -1 0 8202 8202 0 267058582
16 114453661 1 2 8078 8080 0 267154801
17 238186035 1 1 8185 8186 0 267075475
18 57581772 1 1 8167 8168 0 267117483
19 159642373 1 1 8069 8070 0 267057245
20 0 -1 0 8207 8207 0 267058016
21 0 -1 0 8167 8167 0 267071841
22 0 -1 0 8184 8184 0 267090639
23 160208754 1 1 8288 8289 0 267128636
24 61927419 1 1 8113 8114 0 267058264
25 0 -1 0 8095 8095 0 267061608
26 0 -1 0 8076 8076 0 267057459
27 0 -1 0 8085 8085 0 267090624
28 127834477 1 1 8056 8057 0 267116186
29 134923267 1 3 8209 8212 0 267115816
30 0 -1 0 8136 8136 0 267075506
31 0 -1 0 8155 8155 0 267126906
32 0 -1 0 8245 8245 0 267106120
33 0 -1 0 8268 8268 0 267055132
34 0 -1 0 8310 8310 0 267062741
35 0 -1 0 8148 8148 0 267076001
36 114448760 1 1 8128 8129 0 267158339
37 93365951 1 1 8275 8276 0 267067880
38 0 -1 0 8278 8278 0 267143518
39 226583293 1 1 8089 8090 0 267060734
40 0 -1 0 8173 8173 0 267161287
41 0 -1 0 8103 8103 0 267074876
42 0 -1 0 8317 8317 0 267072988
43 0 -1 0 8170 8170 0 267060936
44 0 -1 0 8079 8079 0 267099861
45 217846138 1 1 8259 8260 0 267086293
46 0 -1 0 8117 8117 0 267066825
47 244557884 1 1 8217 8218 0 267070663
48 0 -1 0 8194 8194 0 267067239
49 6531886 1 1 8251 8252 0 267083238
50 0 -1 0 8061 8061 0 267066122
51 0 -1 0 8276 8276 0 267119024
52 240379818 1 1 8189 8190 0 267080241
53 0 -1 0 8256 8256 0 267066492
54 0 -1 0 8035 8035 0 267172955
55 0 -1 0 7852 7852 0 267167879
56 0 -1 0 8115 8115 0 267057821
57 208111889 1 2 8209 8211 0 267056955
58 243759457 1 1 8126 8127 0 267071804
59 132289632 1 1 8109 8110 0 267055613
60 0 -1 0 8089 8089 0 267056793
61 114025146 1 1 8102 8103 0 267094457
62 168390124 1 1 8112 8113 0 267078350
63 213049903 1 1 8115 8116 0 267086459
64 0 -1 0 8263 8263 0 267072022
65 188692443 1 1 8209 8210 0 267070281
66 183794157 1 1 8166 8167 0 267158039
67 16689781 1 1 8196 8197 0 267064444
68 158486793 1 1 8089 8090 0 267103363
69 163860591 1 1 8123 8124 0 267056996
70 188208116 1 2 7950 7952 0 267055580
71 0 -1 0 8209 8209 0 267061687
72 240152720 1 1 8070 8071 0 267099515
73 0 -1 0 8036 8036 0 267069358
74 0 -1 0 8188 8188 0 267071836
75 0 -1 0 8145 8145 0 267073961
76 0 -1 0 8184 8184 0 267071496
77 0 -1 0 8247 8247 0 267104739
78 0 -1 0 8176 8176 0 267086049
79 0 -1 0 8182 8182 0 267109292
80 0 -1 0 8127 8127 0 267087190
81 0 -1 0 8208 8208 0 267111777
82 0 -1 0 8082 8082 0 267056431
83 0 -1 0 8030 8030 0 267063139
84 0 -1 0 8268 8268 0 267086339
85 176618969 1 1 8097 8098 0 267079814
86 215641044 1 1 8223 8224 0 267082957
87 194305503 1 1 8299 8300 0 267096276
88 0 -1 0 8249 8249 0 267073146
89 0 -1 0 8130 8130 0 267062528
90 109354697 1 1 8115 8116 0 267098015
91 239665838 1 1 8014 8015 0 267071490
92 0 -1 0 8188 8188 0 267104140
93 187238494 1 1 8065 8066 0 267098852
94 65808009 1 2 8138 8140 0 267054423
95 0 -1 0 8286 8286 0 267083159
96 130699790 1 1 8140 8141 0 267064420
97 0 -1 0 8318 8318 0 267056514
98 206352188 1 1 8299 8300 0 267074170
99 0 -1 0 8097 8097 0 267091253
100 0 -1 0 8283 8283 0 267061454
101 0 -1 0 8186 8186 0 267103980
102 0 -1 0 8348 8348 0 267123968
103 0 -1 0 8201 8201 0 267079673
104 133304569 1 1 8064 8065 0 267063764
105 114594707 1 1 8215 8216 0 267097045
106 0 -1 0 8026 8026 0 267055063
107 0 -1 0 8307 8307 0 267060694
108 0 -1 0 8108 8108 0 267085873
109 0 -1 0 8217 8217 0 267102010
110 98191022 1 1 8049 8050 0 267099613
111 0 -1 0 8241 8241 0 267082996
112 0 -1 0 8260 8260 0 267110585
113 0 -1 0 8273 8273 0 267260417
114 187325757 1 1 8245 8246 0 267072841
115 0 -1 0 8206 8206 0 267071038
116 252474762 1 1 8136 8137 0 267086365
117 260438348 1 1 8150 8151 0 267128999
118 0 -1 0 8159 8159 0 267085728
119 0 -1 0 8075 8075 0 267091124
120 206979941 1 1 8096 8097 0 267056473
121 0 -1 0 8369 8369 0 267073890
122 233686815 1 1 8055 8056 0 267166148
123 0 -1 0 8079 8079 0 267095025
124 56744473 1 1 8268 8269 0 267125033
125 131715114 1 1 8298 8299 0 267124000
126 0 -1 0 8136 8136 0 267107322
127 0 -1 0 8075 8075 0 267063184
128 0 -1 0 8242 8242 0 267055058
129 0 -1 0 8104 8104 0 267078638
130 138409758 1 1 8083 8084 0 267133855
131 134590586 1 2 8152 8154 0 267127732
132 0 -1 0 8042 8042 0 267073504
133 36259324 1 1 8262 8263 0 267096889
134 0 -1 0 8174 8174 0 267127269
135 0 -1 0 8199 8199 0 267102356
136 175015299 1 1 8248 8249 0 267072601
137 154961412 1 1 8057 8058 0 267061757
138 159495089 1 1 8129 8130 0 267096937
139 0 -1 0 8207 8207 0 267104895
140 0 -1 0 7977 7977 0 267073286
141 0 -1 0 8149 8149 0 267125220
142 0 -1 0 8212 8212 0 267054719
143 0 -1 0 8069 8069 0 267084124
144 184918451 1 1 8230 8231 0 267100234
145 0 -1 0 8122 8122 0 267116079
146 0 -1 0 8162 8162 0 267055797
147 224028893 1 1 8154 8155 0 267112514
148 0 -1 0 8090 8090 0 267093787
149 170583881 1 2 8159 8161 0 267324806
150 171769031 1 1 8174 8175 0 267078858
151 0 -1 0 8076 8076 0 267069326
152 140389852 1 1 8258 8259 0 267098225
153 0 -1 0 8049 8049 0 267077214
154 72006970 1 2 8183 8185 0 267060381
155 151248876 1 2 8191 8193 0 267061635
156 0 -1 0 8265 8265 0 267074156
157 0 -1 0 8095 8095 0 267105923
158 0 -1 0 8091 8091 0 267065941
159 0 -1 0 8210 8210 0 267070635
160 0 -1 0 8101 8101 0 267263808
161 124353393 1 1 8156 8157 0 267075484
162 0 -1 0 8122 8122 0 267115514
163 0 -1 0 8002 8002 0 267086755
164 0 -1 0 8116 8116 0 267055154
165 0 -1 0 8149 8149 0 267096020
166 153502762 1 5 8142 8147 0 267094006
167 0 -1 0 8240 8240 0 267096363
168 0 -1 0 8123 8123 0 267118162
169 0 -1 0 8155 8155 0 267105290
170 0 -1 0 8198 8198 0 267101669
171 226481145 1 1 8048 8049 0 267058045
172 241394801 1 1 8129 8130 0 267120996
173 0 -1 0 8265 8265 0 267063518
174 64995441 1 1 8112 8113 0 267089887
175 0 -1 0 8033 8033 0 267075630
176 0 -1 0 8155 8155 0 267066772
177 0 -1 0 8224 8224 0 267085827
178 0 -1 0 8197 8197 0 267098760
179 142459997 1 2 8232 8234 0 267056548
180 0 -1 0 8235 8235 0 267078303
181 0 -1 0 7961 7961 0 267061968
182 197893623 1 2 8215 8217 0 267075935
183 0 -1 0 8301 8301 0 267089225
184 63648474 1 2 8137 8139 0 267083389
185 0 -1 0 8086 8086 0 267067510
186 0 -1 0 7989 7989 0 267069680
187 0 -1 0 8170 8170 0 267081046
188 0 -1 0 8014 8014 0 267078215
189 52465342 1 3 8212 8215 0 267094775
190 82066879 1 2 8020 8022 0 267059326
191 0 -1 0 7951 7951 0 267099191
192 0 -1 0 8232 8232 0 267081277
193 218815711 1 1 8176 8177 0 267075462
194 0 -1 0 8133 8133 0 267095042
195 0 -1 0 8214 8214 0 267059003
196 134084886 1 1 8167 8168 0 267064603
197 0 -1 0 8284 8284 0 267065251
198 247208792 1 1 8281 8282 0 267172167
199 0 -1 0 8113 8113 0 267092290
~~~

### B.9 Extension analysis (analyze_ext.py)

~~~python
"""Extension (not preregistered): 1000 further fresh seeds of the dense search; same statistics, with z-scores against the model."""
import json, math
pred = json.load(open('predictions.json'))['dense']
rows = []
for line in open('out_dense_ext.txt').read().split('\n')[1:]:
    if not line.strip(): continue
    p = line.split()
    rows.append(dict(first=int(p[2]), dT=int(p[6]), recT=int(p[8]), trT=int(p[10]), dead=int(p[11]), rep=int(p[13])))
N = len(rows)
def z(obs, p, n): return (obs - p * n) / math.sqrt(n * p * (1 - p))
k = sum(1 for r in rows if 0 < r['first'] <= pred['Tb'] and r['rep'] == 1)
print('N', N)
print('success at horizon %d/%d = %.4f  model %.4f  z %.2f' % (k, N, k / N, pred['p_detect_at_horizon'], z(k, pred['p_detect_at_horizon'], N)))
k2 = sum(1 for r in rows if r['first'] > 0 and 256 * r['first'] <= pred['nstar'] and r['rep'] == 1)
print('detected by n*       %d/%d = %.4f  model %.4f  z %.2f' % (k2, N, k2 / N, pred['p_detect_at_nstar'], z(k2, pred['p_detect_at_nstar'], N)))
works = sorted(256 * r['first'] if r['first'] > 0 else float('inf') for r in rows)
med = (works[N // 2 - 1] + works[N // 2]) / 2
print('median work %.4g  model %.4g  ratio %.4f' % (med, pred['median_E'], med / pred['median_E']))
md = sum(r['dT'] for r in rows) / N
print('mean dups at horizon %.4f  model %.4f  ratio %.3f (se %.3f)' % (md, pred['mean_dups_at_T'], md / pred['mean_dups_at_T'], math.sqrt(pred['mean_dups_at_T'] / N) / pred['mean_dups_at_T']))
print('mean records %.1f model %.1f ; max trails %d ; max rec %d ; dead %d ; replay not real %d' % (sum(r['recT'] for r in rows) / N, pred['mean_rec_at_T'], max(r['trT'] for r in rows), max(r['recT'] for r in rows), sum(r['dead'] for r in rows), sum(1 for r in rows if r['first'] > 0 and r['rep'] != 1)))
~~~


