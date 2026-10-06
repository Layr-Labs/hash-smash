# Clean-source fixed-seed construction for SHA-256 r31

This is an **exploratory conditional construction** for the exact
`sha256-r31-prefix-v1` ordinary-collision target. Seven distinct pairs were
found in one predeclared deterministic `2^35`-block campaign. All seven pairs
were independently rehashed through the complete padded three-block target;
`certificates/manifest.json` supplies them. The lowest-counter pair is at
ChaCha20 counter 3,657,090,739 and has digest
`38bfee3b3697ce5531983a3f306d29166f089a4f55858605aa674354d0348e75`.

The selected target uses the standard fixed SHA-256 IV once at message start,
original constants and schedule indices, rounds 0 through 30 inclusive for
every padded block, all eight feed-forward additions, and FIPS padding. The
messages are distinct 128-byte strings, share the first 64-byte block, and
have the same full 256-bit digest. A free-start or second-block-only match
would not qualify.

The declared algorithm regenerates the clean source table from fixed public
trail constants, runs every one of the predeclared `2^35` first blocks, tries
one capped completion for every qualifying event, and selects the
lowest-counter verified collision. Its exact completed deterministic replay
has success probability 1 on this fixed target. The fixed seed and seven
witnesses establish this particular construction, not an ideal-independent-
coin estimate for fresh random seeds. The score charges the entire source,
table, search, failed trials, completion and validation under explicit
exploratory cost premises. It does not price a witness as a cheap lookup.

The score-critical limitations are stated in Section 7. In particular,
published target-specific differential guidance is treated as reusable
algorithm text; its original discovery is unmetered. The source-solver
Cachegrind-to-word-RAM conversion and a kernel reserve are heuristics.
A literal all-history charge or a requirement to price the original trail
search could invalidate the `39.98` scalar. AI screening is not mathematical
acceptance or human review.

## 2. Public differential and exact arithmetic

All trail equations use 32-bit modular arithmetic. Let little sigma zero/one be the FIPS SHA-256 message-schedule
functions; capital Sigma zero/one are the SHA-256 state functions. Ch and Maj have their standard definitions. For t
at least 16, the ordinary schedule is

    W[t] = W[t-16] + sigma0(W[t-15]) + W[t-7] + sigma1(W[t-2]).

The paired second blocks have modular differences:

    dW5=fffff006, dW6=002087f1, dW7=4fefb5fa,
    dW8=28011100, dW9=00008004, dW10=dW11=dW12=0.

The local source model additionally fixes published modular state differences DA5..12 and DE5..12 and signed A/E
masks. Those literal arrays are given in the reproduction appendix below. This guidance is a relaxation of the public Li–Liu–Wang–Dong–Sun 31-step
signed characteristic printed in [their ASIACRYPT 2024 slides](https://iacr.org/submit/files/slides/2024/asiacrypt/asiacrypt2024/64/64_slides.pdf#page=14).
It is not a newly derived characteristic. The masks were fixed before these
source solves. The published authors explicitly separate message-difference
selection, trail search, and pair finding; this submission does not measure
their trail-search work.

For j=5..8, define Vj as all 32-bit w satisfying sigma0(w+dWj)-sigma0(w)=cj, with c5=d0018020, c6=00000ffa,
c7=ffdf780f, c8=b00fca02. Exhaustive counts are |V5|=16,384; |V6|=8,388,608; |V7|=512; |V8|=49,408. Use the complete
modular V8 set in table construction; the signed W7/W8 constraints are applied to source solving. The later schedule
sets G16, G18 and S are generated from the exact difference equations:

    G16 = {w : sigma1(w+00008004)-sigma1(w)=ffff7ffc}
    G18 = {w : sigma1(w+ffff7ffc)-sigma1(w)=2ffe7fe0}
    S = {c : some g in G16 has sigma1(g)+c in G18}.

The support scans yield |G16|=64, |G18|=42,467,328 and |S|=584,683,520. The W20..W25 schedule differences cancel as
`x18+c5=0`, `c6+dW5=0`, `c7+dW6=0`, `dW16+c8+dW7=0`, `-dW8+dW8=0`, and `dW18+dW9=0`; W26..W30 then agree. These identities are checked again by full two-lane forward compression.

The local feasibility equations are exact, with primes denoting lane b:

    F8: (E8'-A4'-Sigma1(E7')-Ch(E7',E6',E5'))
      - (E8 -A4 -Sigma1(E7 )-Ch(E7 ,E6 ,E5 )) = dW8.
    F7: Ch(E6',E5',E4)-Ch(E6,E5,E4)
       = (E7'-E7)-(Sigma1(E6')-Sigma1(E6))-dW7.
    F6: Ch(E5',E4,E3)-Ch(E5,E4,E3)
       = (E6'-E6)-(Sigma1(E5')-Sigma1(E5))-dW6.

For P4 define p=(E9'-E9)+Sigma1(E12')-Sigma1(E12)+Ch(E12',E11',E10')-Ch(E12,E11,E10). Require p=0 and
p+Sigma0(A12')-Sigma0(A12)+Maj(A12',A11',A10')-Maj(A12,A11,A10)=0. The numeric auditor checks both exact modular
equalities before retaining a row.

## 3. Deterministic clean source recipe

One source row is two arrays of 24 unsigned 32-bit words, each in order (A1..A12,E5..E12,W9..W12), stored
little-endian. The paired model uses shared A1..A4, equal W10..W12, the published modular DA/DE differences, the
signed patterns below, W9/V9, F8/F7/F6, and P4. For each lane it imposes the exact inverse A recurrence

    A[t-4] = E[t]-A[t]+Sigma0(A[t-1])
             +Maj(A[t-1],A[t-2],A[t-3]), t=8,7,6,5,

and the exact E-to-message inverse recurrence

    W[t] = E[t]-A[t-4]-E[t-4]-Sigma1(E[t-1])
           -Ch(E[t-1],E[t-2],E[t-3])-K[t], t=9..12.

The model has no inherited list of 159 fixed equal-bit E values and no inherited W9 signed pattern. Every produced row
is independently checked numerically against the recurrences, differences, F8, V9, P4, and masks. Z3 is a search
engine here; its SAT verdict is not accepted as a substitute for numeric row verification.

First obtain one standalone row with a 2,000,000-conflict cap and `timeout=0` in the metered production worker. Then solve 128 publicly indexed four-equality-bit
cubes. Cube i seeds Python random.Random with the 32-byte SHA256 digest of "r31-publicmask-cube-" followed by
decimal(i). The eligible pool lists every equals-mask bit of A5..8 then E5..8 in increasing t and bit order. Four
times, draw a pool index and then one bit from that PRNG; constrain the selected lane-a bit to the drawn value.
Repeated constraints are allowed. Each solve has max_conflicts=500000, rlimit=90000000, timeout=0. This campaign
returned 61 SAT, 54 UNSAT, 13 unknown. Keep the 55 SAT rows whose conflict counts are at most 450000. Of the six later
SAT cubes retain only the lowest index, cube 33, as one extra fiber source. The 128-call campaign charges all unused
and failed calls. A separate direct 450000-conflict replay produced the same 55 SAT rows, 54 UNSAT and 19 unknown, all
selected SAT rows byte-for-byte identical. That separate 450,000-conflict
replay is validation evidence, not an operation of the prospective source
route; it would add cost under literal executed-history accounting.

Sort the 55 selected cube rows and prepend the standalone row, making 56 seeds. For each seed, fix A5..12 and E9..12;
enumerate distinct E5..8 tuples with at most 1000 models under max_conflicts=500000, rlimit=90000000, timeout=0 per
solve. Extend the six fibers at indices 6,18,25,28,32,53 from 1000 to at most 5000 models under the same per-solve
caps. Enumerate the selected cube-33 seed to 1000 models. Separately run the bounded signed local-repair BFS from the
55 sorted cube rows: at most 10000 nodes, 20 million early checks, and 5 billion full checks. It actually produced
2074 nodes from 10,983,442 early candidates, exactly 5 billion full checks and 74,609 full passes.

Sort and deduplicate the exact union of the initial fibers (20,823 rows), BFS output (2,074 rows), five extended-fiber
tails (4,670 rows), extended fiber-6 tail (1,767 rows), and cube-33 fiber (988 rows). The sequential new-row counts
are 20,823, 718, 4,601, 1,718, 988, giving **28,848** rows. No E-pair recombination output is needed for this corpus.
The final 5,538,816-byte row file has SHA-256 66b27ab1e470d232a74a1b2f4e5e48684ac3d5897e337fc26c41e7a7cab64590. An
independent rebuild produced identical bytes.

The exact literal signed patterns and solver caps are reproducibility parameters, not secret advice:

    DA5..12 = fffff006 ff800001 0edfeffd fffffffc
              00000000 00008004 00000000 00000000
    DE5..12 = fffff006 fff87fff 4f880387 44ff8804
              00000008 ef808008 10bffff8 ffff7ff8
    t  signed A pattern                 signed E pattern
    5  ===================n=unnnnnnn=n=  ==================nu======unnnu=
    6  ========n======================u  ============n===u==============n
    7  ===u===n==n========n=========n=u  un=u====n===u========u==n===u==n
    8  =============================n==  =u==un=u========n===u========u==
    9  ================================  ============================u===
    10 ================u============u==  ==n=uuuuu======un====unnnnnnn===
    11 ================================  ===u====uu==================n===
    12 ================================  ================n===========n===
    W7 xor mask=50105a0e, lane-a masked value=0010520a
    W8 xor mask=58011100, lane-a masked value=18000000

The 32-character signed strings run from most to least significant bit. An equals sign fixes equal lane bits, u means
(0,1), n means (1,0), and 0/1 fixes both lane bits to that value. The W7/W8 masks fix both each lane-a masked value
and the lane XOR. The model and production workers are listed in the evidence index.

## 4. Exact first-eight table

Process the 28,848 rows in little-endian byte order. For each row scan every V8 word and V7 word in increasing
unsigned order. Invert step 8 to get a common E4; retain W8 only if the exact F7 equation holds. Invert step 7 to get
common E3; retain W7 only if exact F6 gives the same E2 in both lanes. F5 then gives common E1 for dW5. Compute A0 and
A[-1] by the inverse A recurrence. The 32-bit A[-1] is the lookup key. Retain only the first eight tuples for each
key, in row/V8/V7 order, regardless of later fixed-IV data.

One deterministic table pass finds 190,385,880 F7-passing W8 cases, 649,543,864 F6 tuples, 148,169,452 distinct keys
and 523,821,326 retained first-eight records. The direct-address builder aborts unless these exact counts agree; an
independent 1000-group sample checked the stored tuple order and reconstructed inverse constants. This replay
construction needs no uniform-CV overlap lower bound. Earlier full low16 scans and their `L=508,643,946.769831657` result
were exploratory diagnostics, not an operation of this single-route replay or a
premise for its success. A strict historical-work reading adds them to the
cost, as Section 7 explains.

The slot array uses 2^32 four-byte entries (16 GiB). Each stored group holds a key, count and up to eight packed
point/V8/V7 indices in 72 bytes. The group allocation is capped at 160 million entries (11.52 billion bytes), while
the source rows occupy 5.54 million bytes and V6's full-word bitset occupies 0.54 billion bytes. These explicit arrays
sum below 30 billion bytes, with more than 38 billion bytes of space remaining under the conservative 2^36-byte
peak claim for source workers, thread buffers, verifier state, code and retained advice. The two measured sampler peaks were 27,217,984 and 27,225,128 KiB;
the higher is 27,878,531,072 bytes. The 2^36-byte memory claim leaves ample headroom
for the other stages; it is an exploratory peak bound because no end-to-end
historical discovery RSS record is available.

## 5. Prespecified fixed-IV production search

Before launch, the clean-row hash, derivative-file hashes, table code, first-block generator, seed, nonce, N and
completion policy were recorded in the frozen protocol. The ChaCha20 key is SHA-256 of "HashSmash sha256-r31 clean28k
fixed-seed prospective replay 2026-10-06 run 1": 6af5170aa5223b656b9b8e8267b49a5bc7a9efa543d14360207ff63f292dab5f. Use
the original 64-bit-counter/64-bit-nonce ChaCha20 layout, nonce 726f756e64333121, 20 rounds. Counter i yields one full
64-byte first block. Counters 0 through 2^35-1 are partitioned into disjoint contiguous ranges across 16 threads;
thread scheduling cannot choose or omit counters. Python and C ChaCha20 outputs agree at counters 0, 1, and 2^32.

For every first block, compute its exact 31-step fixed-IV CV. Lookup the CV's A[-1] in the table, test every retained
tuple in order, and select the first whose reconstructed W6 is in V6 and W5 is in V5. Then compute c18 from the exact
inverse message equations and test membership in S. Preserve every exact prefix and every c18-selected JOINT with
counter, first block, CV, selected slot and tuple indices. The sampler runs all N=34,359,738,368 blocks even after
successes. Successful completion requires exit code zero, built-in self-test, exact table counts, 1000-group order
audit, and samples=requested=N.

The production sampler exited 0 after all 34,359,738,368 requested counters,
with no early stop. It reported 1,185,317,301 key hits, 4,190,434,465 retained
slot visits, 8,194,220 W6-passing slot visits, 50 exact selected prefixes,
and seven c18-selected JOINTs. Exact table counts, self-test and independent
1,000-group order audit passed. Sample wall time was 870.060 seconds; total
process wall time was 15:44.30. Peak RSS was 27,217,984 KiB.

The sampler source SHA-256 is
`3aaf828693f0dd0cb91b20d6ef3b06bf51e113c774d97cde261d515068702179`;
summary SHA-256 is
`591b9498d60e198f198328fd99ddd3fbb8652fe1f111f22ec73e7951ddbc67e2`;
event log SHA-256 is
`3458f231e7a9ce585cedb309c6d2484852235f694dad01af1d9480c6b150dee0`.
A separate Python audit regenerated all 50 event counters and first blocks,
recomputed the selected tuple and 31-step first-block CV, and checked every
first-match group. The frozen seed and algorithm were declared before the
run; the `2^35` sample was completed even after qualifying events appeared.
An older OS-random `2^37` validation found 14 JOINTs, but is not used to
infer this deterministic route's success and is excluded from the prospective
single-route scalar. Its cost would be additional under literal all-history
accounting.

The original sampler consumed a 1,000-group check file that had also been
created by an earlier, more expensive overlap audit. To remove that accidental
historical dependency, Appendix C.2 gives a bounded generator from only the
clean rows and V7/V8 arrays; it produced the same 120,000-byte file without
the overlap scan. Appendix C.3–C.4 gives a sampler whose startup test uses a
newly generated zero-block vector instead of a published collision block.
This hygiene sampler was run over the **same prespecified key and all `2^35`
counters** after the original result was known. It is a provenance replay,
not an independent random-seed experiment or a second run in the proposed
single-route cost. It exited zero with self-test and group audit passed,
34,359,738,368 samples, 148,169,452 keys, 523,821,326 retained table
records, 1,185,317,301 key hits, 4,190,434,465 slot visits, 8,194,220
W6-passing visits, 50 exact prefixes and seven JOINTs. Its sorted 50
counter/event/group records are byte-identical to the original run's records;
all 20 stdout statistic lines agree except elapsed time. The hygiene sampler
source SHA-256 is
`1364fa7c9ee828660bd55901d206c18c2c40aaca2772404907fadba4cde9162f`;
stdout SHA-256 is
`1d1b29d8a0da10d406626a672c240633ee9c2fa692e5c9aa10c0231bcb4ef7ac`;
stderr SHA-256 is
`dac334e6a66c35878a958e5724e1335a80fbe56a1210edeb8e9ab0e033cf13e3`.
Its sampling wall time was 864.428 seconds, process wall time 15:38.52,
and peak RSS 27,225,128 KiB.

## 6. Prespecified Phase-3 completion and exact collision audit

After the fixed-size sample completed, sort all seven JOINT records by
counter. Independently recompute each first-block CV and selected table
tuple. For JOINT at counter `i`, derive the offset pair for eligible G16
candidate `j` from the first eight bytes of ChaCha20 block
`2^48+64*i+j`, interpreted as two big-endian 32-bit words. This counter
domain is disjoint from the first-block domain. Make one Phase-3 call per
JOINT with a global cap of 65,536 x/z candidate iterations, preserving the
offset tape and every success or failure. The completion-script source was
finalized before any completion was attempted; its SHA-256 is
`21056297468073e16ef286a0bc7cbb832e60350fcf0a6746f6491c95758d3715`.

Phase 3 solves the later E13/E15 and W13/W15 identities, enforces C14..C17
and schedule cancellation through W30, and forms two 128-byte messages.
All seven JOINTs completed within the cap. Their counted iterations in
ascending-counter order were `603, 6019, 4135, 2392, 4517, 175, 185`,
total 18,026. All seven pairs are in the certificate manifest; the earliest
counter is 3,657,090,739, selected slot 4, key `094c88ed`, and digest
`38bfee3b3697ce5531983a3f306d29166f089a4f55858605aa674354d0348e75`.
The complete offset tapes and message hex were retained in the completion
receipt (SHA-256
`d3b198e7335e98eb703f76e04d57ea6cbb5e6efdd8e759ae68b2bf5db01264c2`);
Appendix D prints the outcome summary, and the manifest contains every
binary message pair. The organizer intake cannot include the larger scratch
receipt as a separate file.

A second completion pass read the hygiene sampler's event log using the
portable Appendix D.3 runner. It again completed all seven JOINTs in 18,026
iterations and produced byte-identical message pairs and digests. Its summary
SHA-256 is
`a2508824fc5ca1bfac2ebc79b4da9b96bfc3d0da9cdb6d38b3e8860ae4e75f4b`.
The second independent three-block rehash passed all seven pairs; the audit
log SHA-256 is
`5526927421fec01fbb411bc98d4b032a12fba5d4157879cc6bbdb1c25c9e65d6`.

The organizer's `verifier.hash_functions.digest` independently rehashed
both 128-byte strings plus padding for each pair with 31 steps, fixed IV,
and original schedule and constants. A separately coded FIPS-style SHA-256
implementation also rehashed all seven three-compression pairs and matched
the reported digests. Both checks established message inequality, common
first block, and full digest equality. The new certificates are independent
of the nominal reference and do not reuse the prior submission's witnesses.

## 7. Charged work and conditional scalar

Collision-frontier-v5 prices one selected 31-step compression as one unit;
other ordinary 256-bit word-RAM primitives cost `1/2140` unit each. Sum
work across processors. All preprocessing, randomness, source solving,
failed calls and trials, sorting, table construction, completion, rehash,
and retained advice construction belong in time. Memory is reported
separately. Appendix C gives the exact cardinalities, operation ceilings and arithmetic.

The deterministic source and fiber workers were replayed under Cachegrind
3.26 with their conflict, resource and model caps, timeout disabled. The
replay covers one standalone source solve, all 128 cube solves including
unused/unknown calls, 56 initial fibers, and seven extensions. They executed
7,140,260,742,107 guest instruction references and 2,992,097,049,978
user-mode data references. Assigning `B=160` ordinary primitives per
instruction-plus-data reference gives
`160*(I+D)/2140 = 757,559,461,090.467` v5 units. This is a **score-critical
heuristic**, not a proved machine-to-word-RAM conversion. A Callgrind pilot
of the standalone solve and a hard cube found overwhelmingly scalar moves,
comparisons, branches, additions and shifts, with a very small fraction of
divides (<0.009% of instructions, each emulated in <=64 word-RAM primitives, while scalar instructions and data references require <=8 primitives). The standalone pilot counted 29,405,876,761 user instructions
(28,092,689,774 in libz3), including 2,405,925 64-bit and 129,668 32-bit
divides. The hard cube-85 pilot counted 113,042,022,709 user instructions
(110,707,946,264 in libz3), including 5,109,590 64-bit `div`, 220,287
`divl`, and 8,961 `idiv`. These two pilots support B=160 (a >20x margin over the pilot instruction/memory mix) but do not audit
every instruction or kernel path. Every source row was also numerically
audited against the paired modular recurrences, masks, F8 and V9.

The prospective bounded finite stages sum to 72,722,193,813.054 units:
6,301,961,359.551 for derivative/support scans;
60,661,940,336.209 for bounded local repair;
1,019,303,749.383 for sort/recombination reserve;
and 4,738,988,367.910 for one exact first-eight table. A separate bounded
table pass regenerated the 1,000-group order-check file directly from the
clean rows and V7/V8 arrays, with no low16 overlap scan. That pass produced
the same 120,000 bytes, SHA-256
`44a1c1fbe538b2f565c51a0a8bc847a85fbce1f389c7877fb876ddd2491f2171`,
and costs another 4,738,988,367.910 units under the same table-build ceiling.
The reserve even charges E-pair recombination work unnecessary in the final
corpus.

The fixed run costs 82,012,828,673.907 units under the explicit generous
per-event operation ceilings in Appendix C. It charges all `N=2^35`
compressions and ChaCha20 blocks, all 1,185,317,301 key hits, all
4,190,434,465 slot visits, all W6 and exact hits, all seven completion
attempts, 18,026 counted x/z iterations, parsing and serialization,
and 100 further target calls for rehashes. The source, finite stages,
extra table pass and fixed run sum to `917,033,471,945.338` units. An
additional **heuristic** reserve of `2^48` ordinary operations for
uninstrumented kernel, I/O and auxiliary work adds
`131,530,362,948.904` units. The proposed total is
`1,048,563,834,894.243` units, `log2=39.931552`; the declared scalar is
rounded **up** to `time_log2=39.98`, leaving about 35.8 billion units of
slack. Preprocessing is included in this scalar. The generated row corpus
and loaded derivative arrays are below the declared `2^26` bytes of
retained advice; the explicit table peak plus workers fits the declared
`2^36`-byte memory bound under the same single-route interpretation.

**Public trail interpretation (score-critical).** The Li–Liu–Wang–Dong–Sun
signed trail, message differences and modular DA/DE values are published
algorithm text. This prospective implementation uses them as fixed public
constants and charges every executed differential instantiation: all
source solves, derivative scans, bounded repairs, table operations and
failed calls. The original research that discovered the published trail
has no full runtime/conflict record in this package. The authors explicitly
identify trail search as a distinct task; their reported pair-finding
complexity cannot be substituted for that search. If v5 requires charging
that original discovery as omitted target-specific nonuniform advice, the
`39.98` bound is **not established**. The earlier exploratory campaigns,
`2^37` validation and two full overlap audits are likewise excluded from
the prospective one-route algorithm but would add substantial work under
a literal executed-history interpretation, as would the hygiene replay
after the first fixed-seed run. These are policy and cost
limitations, not claims that those activities were free or measured.

The complete deterministic route gives success probability 1 for this
fixed selected target because seven full witnesses were actually produced.
This does not infer a fresh random-seed probability or expected runtime.
A review requiring a random-coin attack rather than an exact deterministic
construction would have an additional unproven success obligation.

## 8. In-package evidence and review status

The organizer intake permits only `claim.json`, `proof.md`, a certificate
manifest, and its declared message files. Accordingly, the seven complete
pairs are in `certificates/`; all critical algorithms, metering summaries,
counts and hashes are documented below rather than relying on external files.
The original corpus and raw profiling logs are too large for this 4-MiB
candidate format. Their SHA-256 commitments and deterministic reconstruction
instructions are included, but a reviewer should distinguish a logged
self-report from organizer-executed evidence. No participant experiment is
declared: the organizer's bounded Python experiment runner cannot reproduce
a `2^35`-block C search or the Z3 source campaign.

Appendix A contains the source model, workers, local repair and derivative
scanner as inert source text. Appendix B contains all 128 cube and 63 fiber
metering records, including unsuccessful calls, plus the standalone source
record. Appendix C gives the fixed-seed run protocol, table source and full
search receipts. Appendix D gives the completion logic and all seven outcomes.
All counts in Sections 3–7 are assertions by this submission; exact collision
certificates can be checked by the organizer without running our programs.
An AI exploratory screen is not mathematical proof, human acceptance, or
promotion.

## Appendix A: source construction programs

### A.1 Bit-vector source model

Source SHA-256: `668f12a22662889dfdbcc9253c07e276f128966702c5554b83f9382478dfb3a7`. Paths in this original research source are scratch
paths; substitute equivalent local inputs to reproduce it.

```python
import sys,time
sys.path.insert(0,'/tmp/hashsmash_z3/pkg')
import z3
M=0xffffffff
DA={1:0,2:0,3:0,4:0,5:0xfffff006,6:0xff800001,7:0x0edfeffd,8:0xfffffffc,9:0,10:0x8004,11:0,12:0}
DE={5:0xfffff006,6:0xfff87fff,7:0x4f880387,8:0x44ff8804,9:8,10:0xef808008,11:0x10bffff8,12:0xffff7ff8}
AP={5:'===================n=unnnnnnn=n=',6:'========n======================u',7:'===u===n==n========n=========n=u',8:'=============================n==',9:'================================',10:'================u============u==',11:'================================',12:'================================'}
EP={5: '==================nu======unnnu=', 6: '============n===u==============n', 7: 'un=u====n===u========u==n===u==n', 8: '=u==un=u========n===u========u==', 9: '============================u===', 10: '==n=uuuuu======un====unnnnnnn===', 11: '===u====uu==================n===', 12: '================n===========n==='}
K={8:0xab1c5ed5,9:0xd807aa98,10:0x12835b01,11:0x243185be,12:0x550c7dc3}
# proof index uses conventional K[t], K[8]=d807aa98 etc
K={8:0xd807aa98,9:0x12835b01,10:0x243185be,11:0x550c7dc3,12:0x72be5d74}
bv=lambda n:z3.BitVecVal(n,32)
ro=lambda x,n:z3.RotateRight(x,n)
S0=lambda x:ro(x,2)^ro(x,13)^ro(x,22)
S1=lambda x:ro(x,6)^ro(x,11)^ro(x,25)
s0=lambda x:ro(x,7)^ro(x,18)^z3.LShR(x,3)
Ch=lambda x,y,z:z^(x&(y^z))
Maj=lambda x,y,z:(x&y)^(x&z)^(y&z)
s=z3.SolverFor('QF_BV');s.set(timeout=120000)
A=[None]*13;E=[None]*13
for t in range(5,13):A[t]=z3.BitVec(f'A{t}',32);E[t]=z3.BitVec(f'E{t}',32)
for t in range(8,4,-1):A[t-4]=E[t]-A[t]+S0(A[t-1])+Maj(A[t-1],A[t-2],A[t-3])
B=[None]*13;F=[None]*13
for t in range(5,13):B[t]=A[t]+bv(DA[t]);F[t]=E[t]+bv(DE[t])
for t in range(8,4,-1):B[t-4]=F[t]-B[t]+S0(B[t-1])+Maj(B[t-1],B[t-2],B[t-3])
for t in range(1,5):s.add(A[t]==B[t])
for t in range(9,13):s.add(A[t]-E[t]==S0(A[t-1])+Maj(A[t-1],A[t-2],A[t-3])-A[t-4]);s.add(B[t]-F[t]==S0(B[t-1])+Maj(B[t-1],B[t-2],B[t-3])-B[t-4])
def sign(x,y,pat):
 for i,c in enumerate(pat[::-1]):
  if c=='=':s.add(z3.Extract(i,i,x)==z3.Extract(i,i,y))
  if c=='0':s.add(z3.Extract(i,i,x)==0,z3.Extract(i,i,y)==0)
  if c=='1':s.add(z3.Extract(i,i,x)==1,z3.Extract(i,i,y)==1)
  if c=='u':s.add(z3.Extract(i,i,x)==0,z3.Extract(i,i,y)==1)
  if c=='n':s.add(z3.Extract(i,i,x)==1,z3.Extract(i,i,y)==0)
for t in range(5,13):sign(A[t],B[t],AP[t]);sign(E[t],F[t],EP[t])
W={};V={}
for t in range(9,13):
 W[t]=E[t]-A[t-4]-E[t-4]-S1(E[t-1])-Ch(E[t-1],E[t-2],E[t-3])-bv(K[t]);V[t]=F[t]-B[t-4]-F[t-4]-S1(F[t-1])-Ch(F[t-1],F[t-2],F[t-3])-bv(K[t]);s.add(V[t]-W[t]==bv(0x8004 if t==9 else 0))
s.add(s0(V[9])-s0(W[9])==bv((-0x28011100)&M))
# F8 paired E4 equality under W8'=W8+d8
s.add((F[8]-B[4]-S1(F[7])-Ch(F[7],F[6],F[5]))-(E[8]-A[4]-S1(E[7])-Ch(E[7],E[6],E[5]))==bv(0x28011100))
# P4
p4e=F[9]-E[9]+S1(F[12])-S1(E[12])+Ch(F[12],F[11],F[10])-Ch(E[12],E[11],E[10]);s.add(p4e==0)
s.add(p4e+S0(B[12])-S0(A[12])+Maj(B[12],B[11],B[10])-Maj(A[12],A[11],A[10])==0)

# PR#295 Section 5 model M: explicit one-tuple witness.
W7=z3.BitVec('W7',32);W8=z3.BitVec('W8',32)
def advice_mask(x,y,xor,n):
 s.add((x&bv(xor))==bv(n));s.add((x^y)==bv(xor))
advice_mask(W7,W7+bv(0x4fefb5fa),0x50105a0e,0x0010520a)
advice_mask(W8,W8+bv(0x28011100),0x58011100,0x18000000)
s.add(s0(W7+bv(0x4fefb5fa))-s0(W7)==bv(0xffdf780f))
s.add(s0(W8+bv(0x28011100))-s0(W8)==bv(0xb00fca02))
E4=E[8]-A[4]-S1(E[7])-Ch(E[7],E[6],E[5])-bv(K[8])-W8
E3=E[7]-A[3]-S1(E[6])-Ch(E[6],E[5],E4)-bv(0xab1c5ed5)-W7
s.add(Ch(F[6],F[5],E4)-Ch(E[6],E[5],E4)==(F[7]-E[7])-(S1(F[6])-S1(E[6]))-bv(0x4fefb5fa))
s.add(Ch(F[5],E4,E3)-Ch(E[5],E4,E3)==(F[6]-E[6])-(S1(F[5])-S1(E[5]))-bv(0x002087f1))
```

### A.2 Deterministic indexed cube worker

Source SHA-256: `40cf9ecfa6abf73af6040a776ed452e010b4d40f74e3c81d5f07c3ae9fe03a9f`. Paths in this original research source are scratch
paths; substitute equivalent local inputs to reproduce it.

```python
"""Deterministic bounded source cubes using only public xor/n signs.

The imported model has no fixed equal-bit values in E and no W9 signed
pattern.  Every SAT row is independently auditable from its W7/W8 witness.
"""
import sys, time, json, struct, hashlib, random, resource
from pathlib import Path
from r31_source_model_publicmask_builder import *

i = int(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
start = time.monotonic(); c0 = time.process_time()
rng = random.Random(hashlib.sha256(f'r31-publicmask-cube-{i}'.encode()).digest())
eligible = [(A[t], bit) for t in range(5, 9) for bit, c in enumerate(AP[t][::-1]) if c == '='] + [(E[t], bit) for t in range(5, 9) for bit, c in enumerate(EP[t][::-1]) if c == '=']
cube=[]
for _ in range(4):
    x, bit = eligible[rng.randrange(len(eligible))]
    v = rng.randrange(2)
    s.add(z3.Extract(bit,bit,x)==v)
    cube.append((str(x),bit,v))
s.set(max_conflicts=500000, rlimit=90000000, timeout=0)
r=s.check(); st=s.statistics()
data={'index':i,'cube':cube,'status':str(r),'reason':s.reason_unknown() if r==z3.unknown else None,
      'wall_s':time.monotonic()-start,'cpu_s':time.process_time()-c0,
      'maxrss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'model':'public signed A/E/W7/W8 xor/n masks; no E fixed equal 0/1; no W9 sign'}
for key,name in [('sat conflicts','conflicts'),('sat decisions','decisions'),('rlimit count','rlimit')]:
    try:data[name]=st.get_key_value(key)
    except:data[name]=None
if r==z3.sat:
    m=s.model(); val=lambda x:m.eval(x).as_long()
    a=[val(A[t]) for t in range(1,13)]+[val(E[t]) for t in range(5,13)]+[val(W[t]) for t in range(9,13)]
    b=[(val(A[t])+DA[t])&M for t in range(1,13)]+[(val(E[t])+DE[t])&M for t in range(5,13)]+[val(V[t]) for t in range(9,13)]
    raw=struct.pack('<48I',*(a+b))
    data.update({'core8':[f'{x:08x}' for x in a[4:8]+a[12:16]],'w7':f'{val(W7):08x}','w8':f'{val(W8):08x}',
                 'sha256':hashlib.sha256(raw).hexdigest()})
    (out/f'sp_{i:03d}.bin').write_bytes(raw)
(out/f'log_{i:03d}.json').write_text(json.dumps(data,sort_keys=True)+'\n')
print(json.dumps(data,sort_keys=True))
```

### A.3 Initial 56 fixed-late fibers

Source SHA-256: `4cd0bdeae27579c90457652654cdacef8bdf0c1f5244f382c3aa67e499b73ed0`. Paths in this original research source are scratch
paths; substitute equivalent local inputs to reproduce it.

```python
"""Bounded exact early-E enumeration in one clean seed's fixed-late fiber."""
import hashlib,json,resource,struct,sys,time
from pathlib import Path
from r31_source_model_publicmask_builder import *

index=int(sys.argv[1]); seeds=Path(sys.argv[2]).read_bytes();out=Path(sys.argv[3]);out.mkdir(exist_ok=True)
assert len(seeds)%192==0 and 0<=index<len(seeds)//192
seed_raw=seeds[index*192:(index+1)*192];seed=struct.unpack('<48I',seed_raw)
for t in range(5,13):s.add(A[t]==bv(seed[t-1]))
for t in range(9,13):s.add(E[t]==bv(seed[t+7]))
seed_hash=hashlib.sha256(seed_raw).hexdigest()
start=time.monotonic();cpu0=time.process_time();records=[];rows=bytearray();witnesses=bytearray()
for n in range(1000):
    if False:  # metering uses deterministic rlimit/conflict caps
        records.append({'index':n,'status':'cpu_cap','cpu_s_cumulative':time.process_time()-cpu0})
        break
    s.set(max_conflicts=500000,rlimit=90000000,timeout=0)
    t0=time.process_time();w0=time.monotonic()
    answer=s.check();stat=s.statistics()
    d={'index':n,'status':str(answer),'reason':s.reason_unknown() if answer==z3.unknown else None,
       'cpu_s':time.process_time()-t0,'wall_s':time.monotonic()-w0,
       'cpu_s_cumulative':time.process_time()-cpu0}
    for key,name in [('sat conflicts','conflicts_cumulative'),('sat decisions','decisions_cumulative'),('rlimit count','rlimit_cumulative')]:
        try:d[name]=stat.get_key_value(key)
        except:d[name]=None
    if answer!=z3.sat:
        records.append(d);break
    m=s.model();val=lambda x:m.eval(x).as_long()
    early=tuple(val(E[t]) for t in range(5,9))
    a=[val(A[t]) for t in range(1,13)]+[val(E[t]) for t in range(5,13)]+[val(W[t]) for t in range(9,13)]
    b=[(val(A[t])+DA[t])&M for t in range(1,13)]+[(val(E[t])+DE[t])&M for t in range(5,13)]+[val(V[t]) for t in range(9,13)]
    raw=struct.pack('<48I',*(a+b));rows.extend(raw)
    w7,w8=val(W7),val(W8);witnesses.extend(struct.pack('<II',w7,w8))
    d.update({'early_E':[f'{x:08x}' for x in early],'row_sha256':hashlib.sha256(raw).hexdigest(),
              'w7':f'{w7:08x}','w8':f'{w8:08x}'})
    records.append(d)
    s.add(z3.Or(*(E[t]!=bv(x) for t,x in zip(range(5,9),early))))
else:
    records.append({'index':1000,'status':'model_cap','cpu_s_cumulative':time.process_time()-cpu0})
data=bytes(rows);wdata=bytes(witnesses)
(out/f'fiber_{index:03d}.bin').write_bytes(data)
(out/f'witness_{index:03d}.bin').write_bytes(wdata)
(out/f'log_{index:03d}.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in records))
summary={'seed_index':index,'seed_sha256':seed_hash,'sat_rows':len(data)//192,
         'last_status':records[-1]['status'],'attempts':len(records),
         'cpu_s':time.process_time()-cpu0,'wall_s':time.monotonic()-start,
         'maxrss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'last_conflicts_cumulative':records[-1].get('conflicts_cumulative'),
         'last_rlimit_cumulative':records[-1].get('rlimit_cumulative'),
         'rows_sha256':hashlib.sha256(data).hexdigest(),
         'witness_sha256':hashlib.sha256(wdata).hexdigest()}
(out/f'summary_{index:03d}.json').write_text(json.dumps(summary,sort_keys=True)+'\n')
print(json.dumps(summary,sort_keys=True),flush=True)
```

### A.4 Seven extended fibers

Source SHA-256: `b74cdfec0501be02b2130f285d8cf08a1b06751ded202e40cfd840bef1232266`. Paths in this original research source are scratch
paths; substitute equivalent local inputs to reproduce it.

```python
"""Bounded exact early-E enumeration in one clean seed's fixed-late fiber."""
import hashlib,json,resource,struct,sys,time
from pathlib import Path
from r31_source_model_publicmask_builder import *

index=int(sys.argv[1]); seeds=Path(sys.argv[2]).read_bytes();out=Path(sys.argv[3]);out.mkdir(exist_ok=True)
assert len(seeds)%192==0 and 0<=index<len(seeds)//192
seed_raw=seeds[index*192:(index+1)*192];seed=struct.unpack('<48I',seed_raw)
for t in range(5,13):s.add(A[t]==bv(seed[t-1]))
for t in range(9,13):s.add(E[t]==bv(seed[t+7]))
seed_hash=hashlib.sha256(seed_raw).hexdigest()
start=time.monotonic();cpu0=time.process_time();records=[];rows=bytearray();witnesses=bytearray()
for n in range(5000):
    if False:  # deterministic metering caps
        records.append({'index':n,'status':'cpu_cap','cpu_s_cumulative':time.process_time()-cpu0})
        break
    s.set(max_conflicts=500000,rlimit=90000000,timeout=0)
    t0=time.process_time();w0=time.monotonic()
    answer=s.check();stat=s.statistics()
    d={'index':n,'status':str(answer),'reason':s.reason_unknown() if answer==z3.unknown else None,
       'cpu_s':time.process_time()-t0,'wall_s':time.monotonic()-w0,
       'cpu_s_cumulative':time.process_time()-cpu0}
    for key,name in [('sat conflicts','conflicts_cumulative'),('sat decisions','decisions_cumulative'),('rlimit count','rlimit_cumulative')]:
        try:d[name]=stat.get_key_value(key)
        except:d[name]=None
    if answer!=z3.sat:
        records.append(d);break
    m=s.model();val=lambda x:m.eval(x).as_long()
    early=tuple(val(E[t]) for t in range(5,9))
    a=[val(A[t]) for t in range(1,13)]+[val(E[t]) for t in range(5,13)]+[val(W[t]) for t in range(9,13)]
    b=[(val(A[t])+DA[t])&M for t in range(1,13)]+[(val(E[t])+DE[t])&M for t in range(5,13)]+[val(V[t]) for t in range(9,13)]
    raw=struct.pack('<48I',*(a+b));rows.extend(raw)
    w7,w8=val(W7),val(W8);witnesses.extend(struct.pack('<II',w7,w8))
    d.update({'early_E':[f'{x:08x}' for x in early],'row_sha256':hashlib.sha256(raw).hexdigest(),
              'w7':f'{w7:08x}','w8':f'{w8:08x}'})
    records.append(d)
    s.add(z3.Or(*(E[t]!=bv(x) for t,x in zip(range(5,9),early))))
else:
    records.append({'index':5000,'status':'model_cap','cpu_s_cumulative':time.process_time()-cpu0})
data=bytes(rows);wdata=bytes(witnesses)
(out/f'fiber_{index:03d}.bin').write_bytes(data)
(out/f'witness_{index:03d}.bin').write_bytes(wdata)
(out/f'log_{index:03d}.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in records))
summary={'seed_index':index,'seed_sha256':seed_hash,'sat_rows':len(data)//192,
         'last_status':records[-1]['status'],'attempts':len(records),
         'cpu_s':time.process_time()-cpu0,'wall_s':time.monotonic()-start,
         'maxrss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'last_conflicts_cumulative':records[-1].get('conflicts_cumulative'),
         'last_rlimit_cumulative':records[-1].get('rlimit_cumulative'),
         'rows_sha256':hashlib.sha256(data).hexdigest(),
         'witness_sha256':hashlib.sha256(wdata).hexdigest()}
(out/f'summary_{index:03d}.json').write_text(json.dumps(summary,sort_keys=True)+'\n')
print(json.dumps(summary,sort_keys=True),flush=True)
```

### A.5 Bounded signed local repair

Source SHA-256: `d107d7bfa5dfca0b9edd0c96491c936adbe51ec22a001980c5d71139845d90ae`. Paths in this original research source are scratch
paths; substitute equivalent local inputs to reproduce it.

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {uint32_t a[24],b[24];} Point;
typedef struct {uint32_t f[12];} Node;
typedef struct {uint32_t eq,z,o,u,n;} Mask;
static const uint32_t DA[13]={0,0,0,0,0,0xfffff006U,0xff800001U,0x0edfeffdU,0xfffffffcU,0,0x8004U,0,0};
static const uint32_t DE[13]={0,0,0,0,0,0xfffff006U,0xfff87fffU,0x4f880387U,0x44ff8804U,8,0xef808008U,0x10bffff8U,0xffff7ff8U};
static const uint32_t K[13]={0,0,0,0,0,0,0,0,0xd807aa98U,0x12835b01U,0x243185beU,0x550c7dc3U,0x72be5d74U};
static const char *AP[13]={0,0,0,0,0,"===================n=unnnnnnn=n=","========n======================u","===u===n==n========n=========n=u","=============================n==","================================","================u============u==","================================","================================"};
static const char *EP[13]={0,0,0,0,0,"==================nu======unnnu=","============n===u==============n","un=u====n===u========u==n===u==n","=u==un=u========n===u========u==","============================u===","==n=uuuuu======un====unnnnnnn===","===u====uu==================n===","================n===========n==="};
static Mask Am[13],Em[13],W9m;
static uint32_t V7[512],V8[49408];
static inline uint32_t ro(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return ro(x,2)^ro(x,13)^ro(x,22);}
static inline uint32_t S1(uint32_t x){return ro(x,6)^ro(x,11)^ro(x,25);}
static inline uint32_t s0(uint32_t x){return ro(x,7)^ro(x,18)^(x>>3);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static Mask parse(const char *p){Mask m={0};for(int i=0;i<32;i++){uint32_t b=1U<<i;switch(p[31-i]){case '=':m.eq|=b;break;case '0':m.z|=b;break;case '1':m.o|=b;break;case 'u':m.u|=b;break;case 'n':m.n|=b;break;default:abort();}}return m;}
static inline int signok(uint32_t a,uint32_t b,Mask m){
 return !((a^b)&m.eq)&&!((a|b)&m.z)&&((a&b&m.o)==m.o)&&((~a&b&m.u)==m.u)&&((a&~b&m.n)==m.n);
}
static void build(const Node *n,Point *p){
 memset(p,0,sizeof(*p));uint32_t *a=p->a,*b=p->b;
 for(int t=5;t<=8;t++){a[t-1]=n->f[t-5];b[t-1]=a[t-1]+DA[t];}
 for(int t=5;t<=12;t++){a[t+7]=n->f[t-1];b[t+7]=a[t+7]+DE[t];}
 for(int k=0;k<2;k++){
  uint32_t *q=k?b:a;
  for(int t=8;t>=5;t--)q[t-5]=q[t+7]-q[t-1]+S0(q[t-2])+Maj(q[t-2],q[t-3],q[t-4]);
  for(int t=9;t<=12;t++)q[t-1]=q[t+7]+S0(q[t-2])+Maj(q[t-2],q[t-3],q[t-4])-q[t-5];
  for(int t=9;t<=12;t++)q[t+11]=q[t+7]-q[t-5]-q[t+3]-S1(q[t+6])-Ch(q[t+6],q[t+5],q[t+4])-K[t];
 }
}
static int early(const Node *n){
 for(int t=5;t<=8;t++)if(!signok(n->f[t-5],n->f[t-5]+DA[t],Am[t])||!signok(n->f[t-1],n->f[t-1]+DE[t],Em[t]))return 0;
 Point p;build(n,&p);uint32_t *a=p.a,*b=p.b;
 if(memcmp(a,b,4*sizeof(uint32_t)))return 0;
 uint32_t d9=DE[9]+(S0(b[7])-S0(a[7]))+(Maj(b[7],b[6],b[5])-Maj(a[7],a[6],a[5]))-DA[5];
 if(d9!=0)return 0;
 uint32_t ua=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12]);
 uint32_t ub=b[15]-b[3]-S1(b[14])-Ch(b[14],b[13],b[12]);
 return ub-ua==0x28011100U;
}
static int full(const Node *n,Point *p){
 build(n,p);uint32_t *a=p->a,*b=p->b;
 if(memcmp(a,b,4*sizeof(uint32_t)))return 0;
 for(int t=5;t<=12;t++){
  if(b[t-1]-a[t-1]!=DA[t]||!signok(a[t-1],b[t-1],Am[t]))return 0;
  if(!signok(a[t+7],b[t+7],Em[t]))return 0;
 }
 if(b[20]-a[20]!=0x8004U||memcmp(a+21,b+21,3*sizeof(uint32_t)))return 0;
 /* W9 modular/V9 numeric conditions suffice; no unpublished sign pattern. */
 if(s0(b[20])-s0(a[20])!=(uint32_t)-0x28011100U)return 0;
 uint32_t ua=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12]);
 uint32_t ub=b[15]-b[3]-S1(b[14])-Ch(b[14],b[13],b[12]);
 if(ub-ua!=0x28011100U)return 0;
 uint32_t de13=b[16]-a[16]+S1(b[19])-S1(a[19])+Ch(b[19],b[18],b[17])-Ch(a[19],a[18],a[17]);
 if(de13)return 0;
 uint32_t da13=de13+S0(b[11])-S0(a[11])+Maj(b[11],b[10],b[9])-Maj(a[11],a[10],a[9]);
 return da13==0;
}
static int has_tuple(const Point *p){
 const uint32_t *a=p->a,*b=p->b;
 uint32_t rhs7=b[14]-a[14]-(S1(b[13])-S1(a[13]))-0x4fefb5faU;
 uint32_t rhs6=b[13]-a[13]-(S1(b[12])-S1(a[12]))-0x002087f1U;
 uint32_t c4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98U;
 for(int j=0;j<49408;j++){
  uint32_t e4=c4-V8[j];if(Ch(b[13],b[12],e4)-Ch(a[13],a[12],e4)!=rhs7)continue;
  uint32_t c3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5U;
  for(int k=0;k<512;k++){
   uint32_t e3=c3-V7[k];if(Ch(b[12],e4,e3)-Ch(a[12],e4,e3)!=rhs6)continue;
   uint32_t e2=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4U;
   uint32_t e2p=b[13]-b[1]-S1(b[12])-Ch(b[12],e4,e3)-0x923f82a4U-0x002087f1U;
   if(e2==e2p)return 1;
  }
 }
 return 0;
}
int main(int argc,char **argv){
 if(argc!=6){fprintf(stderr,"usage: bfs source.bin out.bin maxnodes maxcandidates maxfull\n");return 1;}
 size_t maxnodes=strtoull(argv[3],0,0),maxcand=strtoull(argv[4],0,0),maxfull=strtoull(argv[5],0,0);
 if(!maxnodes||maxnodes>1000000)return 2;
 FILE *f=fopen("/tmp/r31_v7.bin","rb");if(!f||fread(V7,sizeof(V7),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_v8.bin","rb");if(!f||fread(V8,sizeof(V8),1,f)!=1)return 4;fclose(f);
 for(int t=5;t<=12;t++){Am[t]=parse(AP[t]);Em[t]=parse(EP[t]);}
 W9m=parse("================u==========1=u==");
 f=fopen(argv[1],"rb");if(!f)return 5;fseek(f,0,SEEK_END);long sz=ftell(f);rewind(f);if(sz<0||sz%sizeof(Point))return 6;
 size_t nb=sz/sizeof(Point);Point *base=malloc(sz);if(!base||fread(base,sizeof(Point),nb,f)!=nb)return 7;fclose(f);
 Node *Q=calloc(maxnodes,sizeof(Node));Point *out=calloc(maxnodes,sizeof(Point));if(!Q||!out)return 8;
 size_t n=0,head=0;unsigned long long cand=0,earlypass=0,fullcalls=0,fullpass=0,tuplepass=0;
 for(size_t i=0;i<nb&&n<maxnodes;i++){
  Node node;for(int j=0;j<4;j++)node.f[j]=base[i].a[4+j];for(int j=0;j<8;j++)node.f[4+j]=base[i].a[12+j];
  Point p;if(!full(&node,&p)||!has_tuple(&p)){fprintf(stderr,"bad source %zu\n",i);return 9;}
  int duplicate=0;for(size_t j=0;j<n;j++)if(!memcmp(Q[j].f,node.f,8*sizeof(uint32_t))){duplicate=1;break;}
  if(!duplicate){Q[n]=node;out[n++]=p;}
 }
 time_t start=time(0);
 for(;head<n&&n<maxnodes&&cand<maxcand&&fullcalls<maxfull;head++){
  Node original=Q[head];
  // Bit ordering is deterministic: one bit, two bits in one word, then cross-word pairs.
  for(int mode=0;mode<3&&n<maxnodes&&cand<maxcand&&fullcalls<maxfull;mode++){
   for(int w1=0;w1<8&&n<maxnodes&&cand<maxcand&&fullcalls<maxfull;w1++){
    int w2first=mode==2?w1+1:w1,w2last=mode==2?8:w1+1;
    for(int w2=w2first;w2<w2last&&n<maxnodes&&cand<maxcand&&fullcalls<maxfull;w2++){
     for(int b1=0;b1<32&&n<maxnodes&&cand<maxcand&&fullcalls<maxfull;b1++){
      int b2first=mode==0?-1:(mode==1?b1+1:0),b2last=mode==0?0:32;
      for(int b2=b2first;b2<b2last&&n<maxnodes&&cand<maxcand&&fullcalls<maxfull;b2++){
       Node x=original;x.f[w1]^=1U<<b1;if(b2>=0)x.f[w2]^=1U<<b2;cand++;
       int seen=0;for(size_t j=0;j<n;j++)if(!memcmp(Q[j].f,x.f,8*sizeof(uint32_t))){seen=1;break;}
       if(seen||!early(&x))continue;earlypass++;
       // Preserve original E9..12 first, then repair with at most two bit flips.
       int found=0;Point p;
       for(int repair_mode=0;repair_mode<4&&!found&&fullcalls<maxfull;repair_mode++){
        for(int rw1=0;rw1<(repair_mode?4:1)&&!found&&fullcalls<maxfull;rw1++){
         int rw2first=repair_mode==3?rw1+1:rw1,rw2last=repair_mode==3?4:rw1+1;
         for(int rw2=rw2first;rw2<rw2last&&!found&&fullcalls<maxfull;rw2++){
          for(int rb1=repair_mode?0:-1;rb1<(repair_mode?32:0)&&!found&&fullcalls<maxfull;rb1++){
           int rb2first=repair_mode==0||repair_mode==1?-1:(repair_mode==2?rb1+1:0);
           int rb2last=repair_mode<=1?0:32;
           for(int rb2=rb2first;rb2<rb2last&&!found&&fullcalls<maxfull;rb2++){
            Node y=x;if(rb1>=0)y.f[8+rw1]^=1U<<rb1;if(rb2>=0)y.f[8+rw2]^=1U<<rb2;
            fullcalls++;if(!full(&y,&p))continue;fullpass++;
            if(has_tuple(&p)){tuplepass++;Q[n]=y;out[n++]=p;found=1;}
            else found=2;
           }
          }
         }
        }
       }
      }
     }
    }
   }
  }
  fprintf(stderr,"head=%zu nodes=%zu cand=%llu early=%llu full=%llu fullpass=%llu active=%llu sec=%ld\n",head+1,n,cand,earlypass,fullcalls,fullpass,tuplepass,time(0)-start);
 }
 f=fopen(argv[2],"wb");if(!f||fwrite(out,sizeof(Point),n,f)!=n)return 10;fclose(f);
 printf("bases=%zu nodes=%zu expanded=%zu candidates=%llu early=%llu full=%llu fullpass=%llu active_added=%llu sec=%ld\n",nb,n,head,cand,earlypass,fullcalls,fullpass,tuplepass,time(0)-start);
 return 0;
}
```

### A.6 Exhaustive derivative-set scan

Source SHA-256: `5737e528d2b36289a6fb29460ba843ced8187fb4a3aecfdcfae684f80e9f3866`. Paths in this original research source are scratch
paths; substitute equivalent local inputs to reproduce it.

```c
#include <stdint.h>
#include <stdio.h>
#include <time.h>
static inline uint32_t rot(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return rot(x,7)^rot(x,18)^(x>>3);}
int main(void){
 FILE *f7=fopen("/tmp/r31_v7.bin","wb"),*f8=fopen("/tmp/r31_v8.bin","wb");
 if(!f7||!f8){perror("fopen");return 1;}
 const uint32_t d7=0x4fefb5fa, c7=0xffdf780f, d8=0x28011100, c8=0xb00fca02;
 uint64_t n7=0,n8=0;time_t start=time(0);
 for(uint64_t i=0;i<(1ULL<<32);i++){
  uint32_t x=(uint32_t)i,s=s0(x);
  if((uint32_t)(s0(x+d7)-s)==c7){fwrite(&x,4,1,f7);n7++;}
  if((uint32_t)(s0(x+d8)-s)==c8){fwrite(&x,4,1,f8);n8++;}
 }
 fclose(f7);fclose(f8);
 fprintf(stderr,"V7=%llu V8=%llu seconds=%lld\n",(unsigned long long)n7,(unsigned long long)n8,(long long)(time(0)-start));
 return (n7==512 && n8==49408)?0:2;
}
```

### A.7 Standalone source-row metered worker

Source SHA-256: `f6e1fa8b64bc70e1c503b21f1d1e09b6ead04ab6ecb0bda13435cb626d6abf64`. This sets `timeout=0`; scratch output paths are environment-specific.

```python
"""Bounded numerical source solve with only published signed XOR/n masks."""
import json
import resource
import struct
import time
from pathlib import Path

from r31_source_model_publicmask_builder import A, E, W, V, W7, W8, DA, DE, M, s

start = time.monotonic()
cpu = time.process_time()
s.set(max_conflicts=2000000, timeout=0)
answer = s.check()
stats = s.statistics()
report = {
    "status": str(answer),
    "reason": s.reason_unknown() if str(answer) == "unknown" else None,
    "wall_s": time.monotonic() - start,
    "cpu_s": time.process_time() - cpu,
    "maxrss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}
for name in ("sat conflicts", "sat decisions", "rlimit count"):
    try:
        report[name] = stats.get_key_value(name)
    except Exception:
        report[name] = None
if str(answer) == "sat":
    model = s.model()
    value = lambda x: model.eval(x).as_long()
    lane0 = [value(A[t]) for t in range(1, 13)] + [value(E[t]) for t in range(5, 13)] + [value(W[t]) for t in range(9, 13)]
    lane1 = [(value(A[t]) + DA[t]) & M for t in range(1, 13)] + [(value(E[t]) + DE[t]) & M for t in range(5, 13)] + [value(V[t]) for t in range(9, 13)]
    Path("/tmp/r31_valgrind_publicmask_source.bin").write_bytes(struct.pack("<48I", *(lane0 + lane1)))
    report["w7"] = f"{value(W7):08x}"
    report["w8"] = f"{value(W8):08x}"
Path("/tmp/r31_valgrind_publicmask_source.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(json.dumps(report, sort_keys=True))
```

### A.8 Rebuild 56 seeds from bounded cube logs

Source SHA-256: `b9699a49a75964b8b50e0545c56e4852cf60ca509dd8e695f70a70d8cfe137e4`. Scratch input/output paths are environment-specific.

```python
#!/usr/bin/env python3
"""Reconstruct clean source seeds from one 500k-conflict metered cube pass."""
import hashlib, json
from pathlib import Path

ROOT = Path('/tmp/r31_valgrind_publicmask')
rows = []
late = []
statuses = {}
for index in range(128):
    log = json.loads((ROOT / f'log_{index:03}.json').read_text())
    status = log['status']
    statuses[status] = statuses.get(status, 0) + 1
    if status != 'sat':
        continue
    row = (ROOT / f'sp_{index:03}.bin').read_bytes()
    assert len(row) == 192
    assert hashlib.sha256(row).hexdigest() == log['sha256']
    if log['conflicts'] <= 450000:
        rows.append(row)
    else:
        late.append((index, log['conflicts'], row))

print('statuses:', statuses, 'selected:', len(rows), 'late:', [(i, c) for i,c,_ in late])
assert statuses == {'sat': 61, 'unsat': 54, 'unknown': 13}
assert len(rows) == 55 and late[0][0] == 33
by_index = b''.join(rows)
by_byte_order = b''.join(sorted(set(rows)))
assert len(by_byte_order) == 55*192
assert hashlib.sha256(by_index).hexdigest() == 'b5b94832660125c556cdf54a63fdbcd03b170956d660e2e9413a416985303ff6'
assert hashlib.sha256(by_byte_order).hexdigest() == 'b65713f1fff43ceeb76e232eba9e8ef9e2ec300bd08f1bf38f0b9aefc2618fab'
assert by_byte_order == Path('/tmp/r31_publicmask_cubes128/all_sat_unique.bin').read_bytes()
standalone = Path('/tmp/r31_valgrind_publicmask_source.bin').read_bytes()
assert len(standalone) == 192
seeds = standalone + by_byte_order
assert hashlib.sha256(seeds).hexdigest() == 'bd4891cba6cc95e23c959b8e536bc3bb033194d4f42e78dc2cb56192529841c4'
assert seeds == Path('/tmp/r31_publicmask_fibers56/seeds.bin').read_bytes()
assert late[0][2] == Path('/tmp/r31_publicmask_cube33_fiber/seed.bin').read_bytes()
print('cube rows sorted SHA', hashlib.sha256(by_byte_order).hexdigest())
print('56 seeds SHA', hashlib.sha256(seeds).hexdigest())
print('cube33 seed SHA', hashlib.sha256(late[0][2]).hexdigest())
```

### A.9 Rebuild final sorted unique corpus

Source SHA-256: `7a2fdedf99387e34873fa912ae0ef7a07450c8d8974e593c127b90b4950074a7`. Scratch input/output paths are environment-specific.

```python
#!/usr/bin/env python3
"""Rebuild the signed-clean 28,848-point corpus from bounded-stage outputs."""
from hashlib import sha256
from pathlib import Path

ROW_BYTES = 192
SOURCES = (
    Path('/tmp/r31_publicmask_fibers56/all_fiber_unique.bin'),
    Path('/tmp/r31_publicmask_cubes128/bfs_5b.bin'),
    Path('/tmp/r31_publicmask_fiber_extensions5/all_tails.bin'),
    Path('/tmp/r31_publicmask_fiber_extension6/tail_006.bin'),
    Path('/tmp/r31_publicmask_cube33_fiber/fiber_000.bin'),
)
EXPECTED = '66b27ab1e470d232a74a1b2f4e5e48684ac3d5897e337fc26c41e7a7cab64590'
rows = set()
for path in SOURCES:
    data = path.read_bytes()
    assert len(data) % ROW_BYTES == 0, path
    fresh = 0
    for offset in range(0, len(data), ROW_BYTES):
        row = data[offset:offset+ROW_BYTES]
        if row not in rows:
            fresh += 1
            rows.add(row)
    print(f'{path}: input={len(data)//ROW_BYTES}, new={fresh}, cumulative={len(rows)}, sha256={sha256(data).hexdigest()}')
result = b''.join(sorted(rows))
digest = sha256(result).hexdigest()
assert len(rows) == 28848 and digest == EXPECTED, (len(rows), digest)
out = Path('/tmp/r31_clean28k_rebuilt.bin')
out.write_bytes(result)
original = Path('/tmp/r31_publicmask_fibers56/final_clean_union.bin').read_bytes()
assert result == original
print(f'{out}: rows={len(rows)}, sha256={digest}, byte-identical=True')
```

The final 28,848-row corpus independently passed both signed-mask and
numeric paired-state audits. Their one-line receipts were:

    rows=28848 SHA256=66b27ab1e470d232a74a1b2f4e5e48684ac3d5897e337fc26c41e7a7cab64590 active_AE_masks=pass
    rows 28848 unique 28848 SHA256 66b27ab1e470d232a74a1b2f4e5e48684ac3d5897e337fc26c41e7a7cab64590 numeric audit pass

### A.10 Signed-mask audit

Source SHA-256: `f185223d8635e1a52f0a8223bf97e6b5d43bc62bb0f215c25aeb9de3ced2fda1`.

```python
#!/usr/bin/env python3
"""Check every final paired row against the published active A/E sign masks."""
import hashlib
import struct
import sys
from pathlib import Path

AP = {
    5: '===================n=unnnnnnn=n=',
    6: '========n======================u',
    7: '===u===n==n========n=========n=u',
    8: '=============================n==',
    9: '================================',
    10: '================u============u==',
    11: '================================',
    12: '================================',
}
EP = {
    5: '==================nu======unnnu=',
    6: '============n===u==============n',
    7: 'un=u====n===u========u==n===u==n',
    8: '=u==un=u========n===u========u==',
    9: '============================u===',
    10: '==n=uuuuu======un====unnnnnnn===',
    11: '===u====uu==================n===',
    12: '================n===========n===',
}

def check(x, y, pat):
    assert len(pat) == 32
    for bit, c in enumerate(pat[::-1]):
        p, q = (x >> bit) & 1, (y >> bit) & 1
        assert (c == '=' and p == q) or (c == '0' and p == q == 0) or \
               (c == '1' and p == q == 1) or (c == 'u' and (p, q) == (0, 1)) or \
               (c == 'n' and (p, q) == (1, 0)), (bit, c, p, q)

data = Path(sys.argv[1]).read_bytes()
assert len(data) % 192 == 0
for j in range(0, len(data), 192):
    w = struct.unpack_from('<48I', data, j)
    a, b = w[:24], w[24:]
    for t in range(5, 13):
        check(a[t - 1], b[t - 1], AP[t])
        check(a[t + 7], b[t + 7], EP[t])
print(f'rows={len(data)//192} SHA256={hashlib.sha256(data).hexdigest()} active_AE_masks=pass')
```

### A.11 Numeric two-lane audit

Source SHA-256: `f6078184b896906a131ab87166d096ecc90db05297e02e3e01a16edc7fe7122e`.

```python
"""Independent exact numeric audit of the augmented r31 source table.

This checks the fixed modular trail, two-lane round recurrence, V9, F8, and
P4 for every 48-word row. It intentionally imposes no signed-bit masks.
"""
import argparse
import hashlib
import struct
from pathlib import Path

M = (1 << 32) - 1
DA = {5: 0xfffff006, 6: 0xff800001, 7: 0x0edfeffd, 8: 0xfffffffc,
      9: 0, 10: 0x8004, 11: 0, 12: 0}
DE = {5: 0xfffff006, 6: 0xfff87fff, 7: 0x4f880387, 8: 0x44ff8804,
      9: 8, 10: 0xef808008, 11: 0x10bffff8, 12: 0xffff7ff8}
K = {9: 0x12835b01, 10: 0x243185be, 11: 0x550c7dc3, 12: 0x72be5d74}


def ro(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def S0(x):
    return ro(x, 2) ^ ro(x, 13) ^ ro(x, 22)


def S1(x):
    return ro(x, 6) ^ ro(x, 11) ^ ro(x, 25)


def s0(x):
    return ro(x, 7) ^ ro(x, 18) ^ (x >> 3)


def ch(x, y, z):
    return z ^ (x & (y ^ z))


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def check(row):
    words = struct.unpack("<48I", row)
    lanes = []
    for offset in (0, 24):
        q = words[offset:offset + 24]
        A = {t: q[t - 1] for t in range(1, 13)}
        E = {t: q[t + 7] for t in range(5, 13)}
        W = {t: q[t + 11] for t in range(9, 13)}
        lanes.append((A, E, W))
        for t in range(8, 4, -1):
            got = (E[t] - A[t] + S0(A[t - 1]) +
                   maj(A[t - 1], A[t - 2], A[t - 3])) & M
            assert got == A[t - 4], ("reverse A", t)
        for t in range(9, 13):
            got = (E[t] - A[t - 4] - E[t - 4] - S1(E[t - 1]) -
                   ch(E[t - 1], E[t - 2], E[t - 3]) - K[t]) & M
            assert got == W[t], ("W recurrence", t)
    A, E, W = lanes[0]
    B, F, V = lanes[1]
    for t in range(1, 5):
        assert A[t] == B[t], ("A1..4", t)
    for t in range(5, 13):
        assert (B[t] - A[t]) & M == DA[t], ("DA", t)
        assert (F[t] - E[t]) & M == DE[t], ("DE", t)
    assert (V[9] - W[9]) & M == 0x8004
    assert all(V[t] == W[t] for t in range(10, 13))
    assert (s0(V[9]) - s0(W[9])) & M == (-0x28011100) & M
    f8 = ((F[8] - B[4] - S1(F[7]) - ch(F[7], F[6], F[5])) -
          (E[8] - A[4] - S1(E[7]) - ch(E[7], E[6], E[5]))) & M
    assert f8 == 0x28011100
    p4e = ((F[9] - E[9]) + S1(F[12]) - S1(E[12]) +
           ch(F[12], F[11], F[10]) - ch(E[12], E[11], E[10])) & M
    p4a = (p4e + S0(B[12]) - S0(A[12]) +
           maj(B[12], B[11], B[10]) - maj(A[12], A[11], A[10])) & M
    assert p4e == p4a == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("points")
    args = ap.parse_args()
    data = Path(args.points).read_bytes()
    assert len(data) % 192 == 0
    seen = set()
    for i in range(0, len(data), 192):
        row = data[i:i + 192]
        assert row not in seen, ("duplicate", i // 192)
        seen.add(row)
        check(row)
    print("rows", len(seen), "unique", len(seen), "SHA256", hashlib.sha256(data).hexdigest(), "numeric audit pass")


if __name__ == "__main__":
    main()
```

## Appendix B: source meter receipts

Cachegrind 3.26 counted `Irefs` and `Drefs` for deterministic cap replays
of the Python 3.14.4 / Z3 5.1.0 workers. The seed0 command was
`valgrind --tool=cachegrind python3 r31_publicmask_source_worker_meter.py`;
the indexed cube and fiber workers used the same Valgrind tool wrapper with
their documented arguments and caps. The raw seed0 log reports precisely
`Irefs=29,463,160,155` and `Drefs=12,449,083,890`. The JSONL records below
carry the remaining per-worker counts;
`row_match` and `rows_match` compare produced source bytes against the
recorded clean corpus. The 128-cube file includes every failed and unused
call. Source seed0 adds `Irefs=29,463,160,155`,
`Drefs=12,449,083,890`; its output row hash is
`b591835c31fad7b8c362901d8f02d2e14b66281e8b4c0e455ce0ffd16a159293`.
The complete source/expansion totals are `Irefs=7,140,260,742,107`,
`Drefs=2,992,097,049,978`.

### B.1 All 128 cube solves

Record SHA-256: `f7df96f15047509bd1b0b26cc787672aa9169510a96ea35e0b618898cac782b4`.

```jsonl
{"Drefs": 30102606775, "Irefs": 72724327549, "conflicts": 379668, "cpu_s": 186.961661158, "decisions": 627679, "index": 0, "orig_status": "sat", "rlimit": 55290744, "row_match": true, "status": "sat"}
{"Drefs": 673942133, "Irefs": 1590505954, "conflicts": 73, "cpu_s": 3.743884936, "decisions": 490, "index": 1, "orig_status": "unsat", "rlimit": 727843, "row_match": null, "status": "unsat"}
{"Drefs": 10815846351, "Irefs": 25949278541, "conflicts": 128986, "cpu_s": 68.166662355, "decisions": 257277, "index": 2, "orig_status": "sat", "rlimit": 23521092, "row_match": true, "status": "sat"}
{"Drefs": 5805467292, "Irefs": 13904286784, "conflicts": 85912, "cpu_s": 36.293617153, "decisions": 174950, "index": 3, "orig_status": "sat", "rlimit": 12921662, "row_match": true, "status": "sat"}
{"Drefs": 18780230678, "Irefs": 44752442391, "conflicts": 207311, "cpu_s": 115.856905381, "decisions": 394620, "index": 4, "orig_status": "sat", "rlimit": 36946367, "row_match": true, "status": "sat"}
{"Drefs": 23971682721, "Irefs": 58237104520, "conflicts": 290061, "cpu_s": 149.122277658, "decisions": 509378, "index": 5, "orig_status": "sat", "rlimit": 43955777, "row_match": true, "status": "sat"}
{"Drefs": 47205813871, "Irefs": 113236260814, "conflicts": 500001, "cpu_s": 291.864021467, "decisions": 951584, "index": 6, "orig_status": "unknown", "rlimit": 78099206, "row_match": null, "status": "unknown"}
{"Drefs": 18191942152, "Irefs": 43413383355, "conflicts": 242586, "cpu_s": 112.530682969, "decisions": 454508, "index": 7, "orig_status": "sat", "rlimit": 36349536, "row_match": true, "status": "sat"}
{"Drefs": 1078284579, "Irefs": 2528651405, "conflicts": 390, "cpu_s": 6.2295903919999995, "decisions": 3129, "index": 8, "orig_status": "unsat", "rlimit": 1312913, "row_match": null, "status": "unsat"}
{"Drefs": 1409873426, "Irefs": 3337131777, "conflicts": 11344, "cpu_s": 8.261859685000001, "decisions": 26319, "index": 9, "orig_status": "unsat", "rlimit": 2000087, "row_match": null, "status": "unsat"}
{"Drefs": 1565552533, "Irefs": 3697688272, "conflicts": 17293, "cpu_s": 9.295393, "decisions": 49337, "index": 10, "orig_status": "unsat", "rlimit": 2562031, "row_match": null, "status": "unsat"}
{"Drefs": 41429966757, "Irefs": 99018845725, "conflicts": 500001, "cpu_s": 252.88455582, "decisions": 919785, "index": 11, "orig_status": "unknown", "rlimit": 63745456, "row_match": null, "status": "unknown"}
{"Drefs": 28640305950, "Irefs": 68311080933, "conflicts": 334261, "cpu_s": 178.934137379, "decisions": 610783, "index": 12, "orig_status": "sat", "rlimit": 56191650, "row_match": true, "status": "sat"}
{"Drefs": 3009253870, "Irefs": 7323224393, "conflicts": 48713, "cpu_s": 18.218899758000003, "decisions": 82740, "index": 13, "orig_status": "unsat", "rlimit": 4642390, "row_match": null, "status": "unsat"}
{"Drefs": 24405811686, "Irefs": 58856666818, "conflicts": 284721, "cpu_s": 154.763811727, "decisions": 519188, "index": 14, "orig_status": "sat", "rlimit": 47628518, "row_match": true, "status": "sat"}
{"Drefs": 1248473064, "Irefs": 2937993027, "conflicts": 6945, "cpu_s": 7.366315956999999, "decisions": 25257, "index": 15, "orig_status": "unsat", "rlimit": 1791206, "row_match": null, "status": "unsat"}
{"Drefs": 1106323733, "Irefs": 2591121367, "conflicts": 1323, "cpu_s": 6.358455929000001, "decisions": 11746, "index": 16, "orig_status": "unsat", "rlimit": 1406030, "row_match": null, "status": "unsat"}
{"Drefs": 1271079985, "Irefs": 2980368359, "conflicts": 6263, "cpu_s": 7.604802230000001, "decisions": 31799, "index": 17, "orig_status": "unsat", "rlimit": 1928741, "row_match": null, "status": "unsat"}
{"Drefs": 1409702396, "Irefs": 3327935306, "conflicts": 13094, "cpu_s": 8.390445786, "decisions": 30411, "index": 18, "orig_status": "unsat", "rlimit": 2054609, "row_match": null, "status": "unsat"}
{"Drefs": 2064553991, "Irefs": 4938735903, "conflicts": 30410, "cpu_s": 12.989751127999998, "decisions": 63777, "index": 19, "orig_status": "unsat", "rlimit": 3427002, "row_match": null, "status": "unsat"}
{"Drefs": 39934522265, "Irefs": 95132678446, "conflicts": 500001, "cpu_s": 247.278489657, "decisions": 829154, "index": 20, "orig_status": "unknown", "rlimit": 62992583, "row_match": null, "status": "unknown"}
{"Drefs": 1051726575, "Irefs": 2472195259, "conflicts": 367, "cpu_s": 6.037802272, "decisions": 2357, "index": 21, "orig_status": "unsat", "rlimit": 1157074, "row_match": null, "status": "unsat"}
{"Drefs": 1186662347, "Irefs": 2775405844, "conflicts": 3777, "cpu_s": 7.117818487000001, "decisions": 22713, "index": 22, "orig_status": "unsat", "rlimit": 1690371, "row_match": null, "status": "unsat"}
{"Drefs": 9044143583, "Irefs": 21603618377, "conflicts": 121876, "cpu_s": 56.485381263, "decisions": 254996, "index": 23, "orig_status": "sat", "rlimit": 19883863, "row_match": true, "status": "sat"}
{"Drefs": 16943716665, "Irefs": 40364277738, "conflicts": 206148, "cpu_s": 108.840022964, "decisions": 388409, "index": 24, "orig_status": "sat", "rlimit": 33544777, "row_match": true, "status": "sat"}
{"Drefs": 7921689809, "Irefs": 19121618208, "conflicts": 120582, "cpu_s": 51.065039467000005, "decisions": 237277, "index": 25, "orig_status": "unsat", "rlimit": 15414177, "row_match": null, "status": "unsat"}
{"Drefs": 22565300399, "Irefs": 53980697931, "conflicts": 278700, "cpu_s": 144.350012096, "decisions": 514317, "index": 26, "orig_status": "sat", "rlimit": 45412214, "row_match": true, "status": "sat"}
{"Drefs": 1125175049, "Irefs": 2640435501, "conflicts": 1660, "cpu_s": 6.677042709999999, "decisions": 11334, "index": 27, "orig_status": "unsat", "rlimit": 1440193, "row_match": null, "status": "unsat"}
{"Drefs": 14535014995, "Irefs": 34529629618, "conflicts": 188640, "cpu_s": 90.108704703, "decisions": 346262, "index": 28, "orig_status": "sat", "rlimit": 27895460, "row_match": true, "status": "sat"}
{"Drefs": 28770489062, "Irefs": 70123164352, "conflicts": 332615, "cpu_s": 182.827295593, "decisions": 594936, "index": 29, "orig_status": "sat", "rlimit": 48463275, "row_match": true, "status": "sat"}
{"Drefs": 12582410236, "Irefs": 29860463843, "conflicts": 161738, "cpu_s": 79.897904409, "decisions": 313330, "index": 30, "orig_status": "sat", "rlimit": 26356320, "row_match": true, "status": "sat"}
{"Drefs": 2082648382, "Irefs": 4996116717, "conflicts": 27453, "cpu_s": 13.041013594999999, "decisions": 52718, "index": 31, "orig_status": "unsat", "rlimit": 3329708, "row_match": null, "status": "unsat"}
{"Drefs": 30862650823, "Irefs": 74409881594, "conflicts": 379408, "cpu_s": 195.843976166, "decisions": 654050, "index": 32, "orig_status": "sat", "rlimit": 56557915, "row_match": true, "status": "sat"}
{"Drefs": 45014690032, "Irefs": 108947171401, "conflicts": 475115, "cpu_s": 282.117874389, "decisions": 831810, "index": 33, "orig_status": "unknown", "rlimit": 75472212, "row_match": null, "status": "sat"}
{"Drefs": 25678768971, "Irefs": 61498847647, "conflicts": 262861, "cpu_s": 166.135046932, "decisions": 466180, "index": 34, "orig_status": "sat", "rlimit": 52038597, "row_match": true, "status": "sat"}
{"Drefs": 39868620554, "Irefs": 96999438969, "conflicts": 435123, "cpu_s": 252.46237704300003, "decisions": 726734, "index": 35, "orig_status": "sat", "rlimit": 74057594, "row_match": true, "status": "sat"}
{"Drefs": 44749108373, "Irefs": 107339242300, "conflicts": 500001, "cpu_s": 283.023520342, "decisions": 923752, "index": 36, "orig_status": "unknown", "rlimit": 77264805, "row_match": null, "status": "unknown"}
{"Drefs": 1103295440, "Irefs": 2584534242, "conflicts": 1119, "cpu_s": 6.3977532, "decisions": 4512, "index": 37, "orig_status": "unsat", "rlimit": 1336554, "row_match": null, "status": "unsat"}
{"Drefs": 20838276062, "Irefs": 49679273991, "conflicts": 246699, "cpu_s": 132.813942746, "decisions": 503736, "index": 38, "orig_status": "sat", "rlimit": 43848675, "row_match": true, "status": "sat"}
{"Drefs": 1329738602, "Irefs": 3123599120, "conflicts": 9645, "cpu_s": 7.772231453000001, "decisions": 33740, "index": 39, "orig_status": "unsat", "rlimit": 2045878, "row_match": null, "status": "unsat"}
{"Drefs": 7262233118, "Irefs": 17077050959, "conflicts": 96346, "cpu_s": 46.047304673, "decisions": 197680, "index": 40, "orig_status": "unsat", "rlimit": 16875947, "row_match": null, "status": "unsat"}
{"Drefs": 42180835558, "Irefs": 100883033804, "conflicts": 500001, "cpu_s": 266.35674626400004, "decisions": 894046, "index": 41, "orig_status": "unknown", "rlimit": 67455696, "row_match": null, "status": "unknown"}
{"Drefs": 1142483865, "Irefs": 2675140338, "conflicts": 2465, "cpu_s": 6.652201165, "decisions": 15663, "index": 42, "orig_status": "unsat", "rlimit": 1539174, "row_match": null, "status": "unsat"}
{"Drefs": 21447424713, "Irefs": 51155124396, "conflicts": 259783, "cpu_s": 134.757699988, "decisions": 511754, "index": 43, "orig_status": "sat", "rlimit": 44064498, "row_match": true, "status": "sat"}
{"Drefs": 15354591629, "Irefs": 36312210549, "conflicts": 159416, "cpu_s": 96.688061348, "decisions": 300142, "index": 44, "orig_status": "sat", "rlimit": 32575694, "row_match": true, "status": "sat"}
{"Drefs": 1614390569, "Irefs": 3820875105, "conflicts": 17712, "cpu_s": 9.557904734000001, "decisions": 43740, "index": 45, "orig_status": "unsat", "rlimit": 2549337, "row_match": null, "status": "unsat"}
{"Drefs": 1123368278, "Irefs": 2629996474, "conflicts": 1922, "cpu_s": 6.533794907, "decisions": 12982, "index": 46, "orig_status": "unsat", "rlimit": 1488082, "row_match": null, "status": "unsat"}
{"Drefs": 1131308407, "Irefs": 2649683857, "conflicts": 2143, "cpu_s": 6.634662861, "decisions": 19102, "index": 47, "orig_status": "unsat", "rlimit": 1515274, "row_match": null, "status": "unsat"}
{"Drefs": 24625806850, "Irefs": 59890095180, "conflicts": 267738, "cpu_s": 156.829325543, "decisions": 455536, "index": 48, "orig_status": "sat", "rlimit": 40692436, "row_match": true, "status": "sat"}
{"Drefs": 1405440409, "Irefs": 3316494997, "conflicts": 10684, "cpu_s": 8.449676972, "decisions": 32848, "index": 49, "orig_status": "unsat", "rlimit": 2205688, "row_match": null, "status": "unsat"}
{"Drefs": 44363445552, "Irefs": 105661581397, "conflicts": 476791, "cpu_s": 280.286003892, "decisions": 826064, "index": 50, "orig_status": "unknown", "rlimit": 71400434, "row_match": null, "status": "sat"}
{"Drefs": 23775976333, "Irefs": 57636041976, "conflicts": 308523, "cpu_s": 154.472468676, "decisions": 531087, "index": 51, "orig_status": "sat", "rlimit": 43217139, "row_match": true, "status": "sat"}
{"Drefs": 1857913586, "Irefs": 4410382038, "conflicts": 29132, "cpu_s": 11.310494982, "decisions": 59478, "index": 52, "orig_status": "unsat", "rlimit": 3166409, "row_match": null, "status": "unsat"}
{"Drefs": 21045265402, "Irefs": 50503344158, "conflicts": 249868, "cpu_s": 137.79107263, "decisions": 458338, "index": 53, "orig_status": "sat", "rlimit": 39824016, "row_match": true, "status": "sat"}
{"Drefs": 21119350850, "Irefs": 50719377662, "conflicts": 264593, "cpu_s": 140.402187994, "decisions": 492068, "index": 54, "orig_status": "sat", "rlimit": 40835946, "row_match": true, "status": "sat"}
{"Drefs": 1500697302, "Irefs": 3536168448, "conflicts": 15942, "cpu_s": 9.331665189, "decisions": 43317, "index": 55, "orig_status": "unsat", "rlimit": 2426113, "row_match": null, "status": "unsat"}
{"Drefs": 6720043754, "Irefs": 16395541179, "conflicts": 90001, "cpu_s": 42.803527523, "decisions": 182613, "index": 56, "orig_status": "unsat", "rlimit": 11879984, "row_match": null, "status": "unsat"}
{"Drefs": 1097904708, "Irefs": 2568847403, "conflicts": 984, "cpu_s": 6.74336828, "decisions": 4911, "index": 57, "orig_status": "unsat", "rlimit": 1356960, "row_match": null, "status": "unsat"}
{"Drefs": 1091031832, "Irefs": 2554168309, "conflicts": 627, "cpu_s": 6.613130892000001, "decisions": 3565, "index": 58, "orig_status": "unsat", "rlimit": 1275414, "row_match": null, "status": "unsat"}
{"Drefs": 16120489423, "Irefs": 38427416170, "conflicts": 180777, "cpu_s": 105.519609121, "decisions": 357718, "index": 59, "orig_status": "sat", "rlimit": 33930909, "row_match": true, "status": "sat"}
{"Drefs": 1128334894, "Irefs": 2644423682, "conflicts": 1990, "cpu_s": 6.993634490000001, "decisions": 16464, "index": 60, "orig_status": "unsat", "rlimit": 1456875, "row_match": null, "status": "unsat"}
{"Drefs": 688312397, "Irefs": 1622154895, "conflicts": 126, "cpu_s": 3.874873043, "decisions": 1379, "index": 61, "orig_status": "unsat", "rlimit": 746655, "row_match": null, "status": "unsat"}
{"Drefs": 1195647057, "Irefs": 2798820204, "conflicts": 3450, "cpu_s": 7.487878201, "decisions": 23897, "index": 62, "orig_status": "unsat", "rlimit": 1712169, "row_match": null, "status": "unsat"}
{"Drefs": 19370750444, "Irefs": 46218260696, "conflicts": 210528, "cpu_s": 123.937658487, "decisions": 398165, "index": 63, "orig_status": "sat", "rlimit": 39616825, "row_match": true, "status": "sat"}
{"Drefs": 1392675341, "Irefs": 3282383601, "conflicts": 11413, "cpu_s": 8.812180706, "decisions": 32714, "index": 64, "orig_status": "unsat", "rlimit": 2118847, "row_match": null, "status": "unsat"}
{"Drefs": 1073217279, "Irefs": 2513648745, "conflicts": 268, "cpu_s": 6.381985868999999, "decisions": 846, "index": 65, "orig_status": "unsat", "rlimit": 1276874, "row_match": null, "status": "unsat"}
{"Drefs": 21082869663, "Irefs": 50056046048, "conflicts": 243004, "cpu_s": 133.79641149, "decisions": 463301, "index": 66, "orig_status": "sat", "rlimit": 44647489, "row_match": true, "status": "sat"}
{"Drefs": 33840408868, "Irefs": 82543701867, "conflicts": 404782, "cpu_s": 215.878326392, "decisions": 735270, "index": 67, "orig_status": "sat", "rlimit": 61142772, "row_match": true, "status": "sat"}
{"Drefs": 10085905911, "Irefs": 24214914697, "conflicts": 128356, "cpu_s": 64.26162786, "decisions": 266136, "index": 68, "orig_status": "sat", "rlimit": 21976777, "row_match": true, "status": "sat"}
{"Drefs": 42985143917, "Irefs": 103313700072, "conflicts": 500001, "cpu_s": 265.04675750999996, "decisions": 865771, "index": 69, "orig_status": "unknown", "rlimit": 69555043, "row_match": null, "status": "unknown"}
{"Drefs": 27197599642, "Irefs": 65654714518, "conflicts": 329018, "cpu_s": 170.15073072700002, "decisions": 597856, "index": 70, "orig_status": "sat", "rlimit": 50067031, "row_match": true, "status": "sat"}
{"Drefs": 1089932933, "Irefs": 2551350615, "conflicts": 704, "cpu_s": 6.481076464999999, "decisions": 4295, "index": 71, "orig_status": "unsat", "rlimit": 1312878, "row_match": null, "status": "unsat"}
{"Drefs": 21181834425, "Irefs": 50891451458, "conflicts": 239764, "cpu_s": 135.800839611, "decisions": 432767, "index": 72, "orig_status": "sat", "rlimit": 41037469, "row_match": true, "status": "sat"}
{"Drefs": 44801329274, "Irefs": 106778074563, "conflicts": 500001, "cpu_s": 283.613243295, "decisions": 923302, "index": 73, "orig_status": "unknown", "rlimit": 76688249, "row_match": null, "status": "unknown"}
{"Drefs": 27191701362, "Irefs": 65235288924, "conflicts": 328040, "cpu_s": 167.59199891, "decisions": 602297, "index": 74, "orig_status": "sat", "rlimit": 50194859, "row_match": true, "status": "sat"}
{"Drefs": 13203356995, "Irefs": 31539414479, "conflicts": 173198, "cpu_s": 84.23347321, "decisions": 341167, "index": 75, "orig_status": "sat", "rlimit": 26873951, "row_match": true, "status": "sat"}
{"Drefs": 33826469820, "Irefs": 81590055778, "conflicts": 414382, "cpu_s": 212.473719037, "decisions": 701754, "index": 76, "orig_status": "sat", "rlimit": 62977724, "row_match": true, "status": "sat"}
{"Drefs": 45283499890, "Irefs": 108291328912, "conflicts": 500001, "cpu_s": 281.07659089, "decisions": 860653, "index": 77, "orig_status": "unknown", "rlimit": 75535320, "row_match": null, "status": "unknown"}
{"Drefs": 26294044660, "Irefs": 63971530457, "conflicts": 288710, "cpu_s": 166.241988145, "decisions": 519163, "index": 78, "orig_status": "sat", "rlimit": 47899042, "row_match": true, "status": "sat"}
{"Drefs": 14283881428, "Irefs": 34160977954, "conflicts": 186520, "cpu_s": 89.48641010600001, "decisions": 334881, "index": 79, "orig_status": "sat", "rlimit": 28243785, "row_match": true, "status": "sat"}
{"Drefs": 1097010357, "Irefs": 2574648834, "conflicts": 670, "cpu_s": 6.364964832, "decisions": 4656, "index": 80, "orig_status": "unsat", "rlimit": 1331097, "row_match": null, "status": "unsat"}
{"Drefs": 22755709910, "Irefs": 54520880612, "conflicts": 276040, "cpu_s": 145.47910457499998, "decisions": 501462, "index": 81, "orig_status": "sat", "rlimit": 45917403, "row_match": true, "status": "sat"}
{"Drefs": 1080539260, "Irefs": 2534640352, "conflicts": 593, "cpu_s": 6.295777134000001, "decisions": 3742, "index": 82, "orig_status": "unsat", "rlimit": 1316449, "row_match": null, "status": "unsat"}
{"Drefs": 1091689717, "Irefs": 2554444935, "conflicts": 698, "cpu_s": 6.3302479929999995, "decisions": 5288, "index": 83, "orig_status": "unsat", "rlimit": 1351452, "row_match": null, "status": "unsat"}
{"Drefs": 1040809210, "Irefs": 2445386823, "conflicts": 218, "cpu_s": 6.122747411, "decisions": 2654, "index": 84, "orig_status": "unsat", "rlimit": 1167722, "row_match": null, "status": "unsat"}
{"Drefs": 46750864430, "Irefs": 113258588522, "conflicts": 472450, "cpu_s": 298.303845681, "decisions": 799122, "index": 85, "orig_status": "unknown", "rlimit": 70815203, "row_match": null, "status": "sat"}
{"Drefs": 33927592491, "Irefs": 81722728665, "conflicts": 367223, "cpu_s": 214.483202393, "decisions": 602087, "index": 86, "orig_status": "sat", "rlimit": 66755767, "row_match": true, "status": "sat"}
{"Drefs": 26834342449, "Irefs": 64564749673, "conflicts": 333978, "cpu_s": 169.053299752, "decisions": 589237, "index": 87, "orig_status": "sat", "rlimit": 48533689, "row_match": true, "status": "sat"}
{"Drefs": 17928696265, "Irefs": 42650010441, "conflicts": 224379, "cpu_s": 111.21305482800001, "decisions": 377800, "index": 88, "orig_status": "sat", "rlimit": 32390438, "row_match": true, "status": "sat"}
{"Drefs": 1496037350, "Irefs": 3515823140, "conflicts": 14379, "cpu_s": 9.014224946, "decisions": 44936, "index": 89, "orig_status": "unsat", "rlimit": 2561586, "row_match": null, "status": "unsat"}
{"Drefs": 28252610950, "Irefs": 67764519157, "conflicts": 341673, "cpu_s": 181.84292594, "decisions": 607600, "index": 90, "orig_status": "sat", "rlimit": 54703931, "row_match": true, "status": "sat"}
{"Drefs": 46096182940, "Irefs": 109498842724, "conflicts": 500001, "cpu_s": 287.180923983, "decisions": 841975, "index": 91, "orig_status": "unknown", "rlimit": 70201923, "row_match": null, "status": "unknown"}
{"Drefs": 222152472, "Irefs": 574049238, "conflicts": null, "cpu_s": 0.25913937200000037, "decisions": null, "index": 92, "orig_status": "unsat", "rlimit": 15990, "row_match": null, "status": "unsat"}
{"Drefs": 1079533642, "Irefs": 2522850601, "conflicts": 494, "cpu_s": 6.1433804489999995, "decisions": 4461, "index": 93, "orig_status": "unsat", "rlimit": 1263545, "row_match": null, "status": "unsat"}
{"Drefs": 1091736514, "Irefs": 2551863302, "conflicts": 676, "cpu_s": 6.237708798, "decisions": 4685, "index": 94, "orig_status": "unsat", "rlimit": 1344467, "row_match": null, "status": "unsat"}
{"Drefs": 20572495701, "Irefs": 49476139853, "conflicts": 222447, "cpu_s": 130.671916574, "decisions": 404059, "index": 95, "orig_status": "sat", "rlimit": 34327099, "row_match": true, "status": "sat"}
{"Drefs": 45102580466, "Irefs": 104707281432, "conflicts": 487028, "cpu_s": 285.745400443, "decisions": 899334, "index": 96, "orig_status": "unknown", "rlimit": 78262733, "row_match": null, "status": "sat"}
{"Drefs": 222199594, "Irefs": 574179179, "conflicts": null, "cpu_s": 0.2629936269999993, "decisions": null, "index": 97, "orig_status": "unsat", "rlimit": 15994, "row_match": null, "status": "unsat"}
{"Drefs": 43085350317, "Irefs": 102988053480, "conflicts": 500001, "cpu_s": 280.32796535700004, "decisions": 862922, "index": 98, "orig_status": "unknown", "rlimit": 74039690, "row_match": null, "status": "unknown"}
{"Drefs": 1554252928, "Irefs": 3680838376, "conflicts": 15434, "cpu_s": 9.263501372, "decisions": 35129, "index": 99, "orig_status": "unsat", "rlimit": 2433911, "row_match": null, "status": "unsat"}
{"Drefs": 44867988373, "Irefs": 107310347374, "conflicts": 464579, "cpu_s": 291.39571440199995, "decisions": 779856, "index": 100, "orig_status": "unknown", "rlimit": 81093602, "row_match": null, "status": "sat"}
{"Drefs": 1381890554, "Irefs": 3260256084, "conflicts": 10792, "cpu_s": 8.483542115, "decisions": 33580, "index": 101, "orig_status": "unsat", "rlimit": 2103774, "row_match": null, "status": "unsat"}
{"Drefs": 17872550309, "Irefs": 42399269092, "conflicts": 207936, "cpu_s": 113.15571404500001, "decisions": 368229, "index": 102, "orig_status": "sat", "rlimit": 33428718, "row_match": true, "status": "sat"}
{"Drefs": 43894675938, "Irefs": 105246559083, "conflicts": 459329, "cpu_s": 284.451905544, "decisions": 823586, "index": 103, "orig_status": "unknown", "rlimit": 72845906, "row_match": null, "status": "sat"}
{"Drefs": 1102514794, "Irefs": 2582754316, "conflicts": 541, "cpu_s": 6.6216399269999995, "decisions": 5985, "index": 104, "orig_status": "unsat", "rlimit": 1371158, "row_match": null, "status": "unsat"}
{"Drefs": 27812209757, "Irefs": 68184048477, "conflicts": 302852, "cpu_s": 186.047252172, "decisions": 547743, "index": 105, "orig_status": "sat", "rlimit": 49141915, "row_match": true, "status": "sat"}
{"Drefs": 33137663251, "Irefs": 79647795085, "conflicts": 431963, "cpu_s": 219.169969115, "decisions": 751403, "index": 106, "orig_status": "sat", "rlimit": 63263038, "row_match": true, "status": "sat"}
{"Drefs": 678970464, "Irefs": 1598280115, "conflicts": 148, "cpu_s": 3.8909817799999997, "decisions": 840, "index": 107, "orig_status": "unsat", "rlimit": 738688, "row_match": null, "status": "unsat"}
{"Drefs": 38803526069, "Irefs": 92600766895, "conflicts": 500001, "cpu_s": 251.498646024, "decisions": 948434, "index": 108, "orig_status": "unknown", "rlimit": 66799644, "row_match": null, "status": "unknown"}
{"Drefs": 8066508478, "Irefs": 19603732322, "conflicts": 112977, "cpu_s": 52.995106458, "decisions": 204220, "index": 109, "orig_status": "unsat", "rlimit": 13380472, "row_match": null, "status": "unsat"}
{"Drefs": 14253936837, "Irefs": 33738803484, "conflicts": 168912, "cpu_s": 94.077786338, "decisions": 310962, "index": 110, "orig_status": "sat", "rlimit": 31123849, "row_match": true, "status": "sat"}
{"Drefs": 44414610628, "Irefs": 106532007366, "conflicts": 500001, "cpu_s": 288.350848763, "decisions": 907381, "index": 111, "orig_status": "unknown", "rlimit": 70470427, "row_match": null, "status": "unknown"}
{"Drefs": 9693441599, "Irefs": 23460126246, "conflicts": 115880, "cpu_s": 63.118705694000006, "decisions": 229505, "index": 112, "orig_status": "sat", "rlimit": 18933917, "row_match": true, "status": "sat"}
{"Drefs": 1183473432, "Irefs": 2770466111, "conflicts": 4534, "cpu_s": 7.101763142000001, "decisions": 18372, "index": 113, "orig_status": "unsat", "rlimit": 1657555, "row_match": null, "status": "unsat"}
{"Drefs": 32496374776, "Irefs": 78535471480, "conflicts": 404894, "cpu_s": 216.346499473, "decisions": 781548, "index": 114, "orig_status": "sat", "rlimit": 59751643, "row_match": true, "status": "sat"}
{"Drefs": 19282529051, "Irefs": 46291559818, "conflicts": 260368, "cpu_s": 125.323919014, "decisions": 444489, "index": 115, "orig_status": "sat", "rlimit": 35874361, "row_match": true, "status": "sat"}
{"Drefs": 1062131049, "Irefs": 2487343218, "conflicts": 132, "cpu_s": 6.296357019, "decisions": 1481, "index": 116, "orig_status": "unsat", "rlimit": 1225158, "row_match": null, "status": "unsat"}
{"Drefs": 28282465716, "Irefs": 68014694848, "conflicts": 349307, "cpu_s": 188.655555168, "decisions": 606317, "index": 117, "orig_status": "sat", "rlimit": 47164917, "row_match": true, "status": "sat"}
{"Drefs": 690432432, "Irefs": 1623988064, "conflicts": 337, "cpu_s": 3.94887271, "decisions": 2550, "index": 118, "orig_status": "unsat", "rlimit": 798158, "row_match": null, "status": "unsat"}
{"Drefs": 33405555586, "Irefs": 80781149189, "conflicts": 425514, "cpu_s": 220.05235175899998, "decisions": 768685, "index": 119, "orig_status": "sat", "rlimit": 61112807, "row_match": true, "status": "sat"}
{"Drefs": 1091545731, "Irefs": 2560514203, "conflicts": 798, "cpu_s": 6.459327012999999, "decisions": 5003, "index": 120, "orig_status": "unsat", "rlimit": 1346048, "row_match": null, "status": "unsat"}
{"Drefs": 20599747575, "Irefs": 48926930144, "conflicts": 245665, "cpu_s": 136.309872924, "decisions": 463501, "index": 121, "orig_status": "sat", "rlimit": 40169354, "row_match": true, "status": "sat"}
{"Drefs": 15353662485, "Irefs": 36601404603, "conflicts": 175475, "cpu_s": 99.889837525, "decisions": 332709, "index": 122, "orig_status": "sat", "rlimit": 29830933, "row_match": true, "status": "sat"}
{"Drefs": 29432409814, "Irefs": 71717617525, "conflicts": 343214, "cpu_s": 199.31650203200002, "decisions": 619363, "index": 123, "orig_status": "sat", "rlimit": 50042237, "row_match": true, "status": "sat"}
{"Drefs": 1126255075, "Irefs": 2631899239, "conflicts": 1798, "cpu_s": 6.608217649, "decisions": 16169, "index": 124, "orig_status": "unsat", "rlimit": 1474321, "row_match": null, "status": "unsat"}
{"Drefs": 39967904325, "Irefs": 95399091978, "conflicts": 500001, "cpu_s": 260.18341690799997, "decisions": 915631, "index": 125, "orig_status": "unknown", "rlimit": 70944945, "row_match": null, "status": "unknown"}
{"Drefs": 1086547242, "Irefs": 2550126848, "conflicts": 287, "cpu_s": 6.551366059000001, "decisions": 1774, "index": 126, "orig_status": "unsat", "rlimit": 1290612, "row_match": null, "status": "unsat"}
{"Drefs": 20066477978, "Irefs": 48433811040, "conflicts": 266189, "cpu_s": 131.748190214, "decisions": 485833, "index": 127, "orig_status": "sat", "rlimit": 37314299, "row_match": true, "status": "sat"}
```

### B.2 Initial 56 fiber solves

Record SHA-256: `d6c795f59fda64925f3ea9f1ff9c8416a11d30b0df0d56b4e39a87c4ce1ff6a7`.

```jsonl
{"Drefs": 11522194763, "Irefs": 27477397089, "index": 0, "result": "ok", "rows_match": true, "sat_rows": 605, "status": "unsat", "summary_match": true}
{"Drefs": 1253421945, "Irefs": 2960034200, "index": 1, "result": "ok", "rows_match": true, "sat_rows": 28, "status": "unsat", "summary_match": true}
{"Drefs": 9346279989, "Irefs": 22072806172, "index": 2, "result": "ok", "rlimit": 7276822, "rows_match": true, "sat_rows": 522, "status": "unsat", "summary_match": true, "wall_s": 76.59546720894286}
{"Drefs": 4189557962, "Irefs": 9957568443, "index": 3, "result": "ok", "rlimit": 4573936, "rows_match": true, "sat_rows": 252, "status": "unsat", "summary_match": true, "wall_s": 36.928047532972414}
{"Drefs": 3175858864, "Irefs": 7533888067, "index": 4, "result": "ok", "rlimit": 4247169, "rows_match": true, "sat_rows": 168, "status": "unsat", "summary_match": true, "wall_s": 28.512875574990176}
{"Drefs": 3062522304, "Irefs": 7332676132, "index": 5, "result": "ok", "rlimit": 3842058, "rows_match": true, "sat_rows": 184, "status": "unsat", "summary_match": true, "wall_s": 28.412459462007973}
{"Drefs": 21241997093, "Irefs": 50047344239, "index": 6, "result": "ok", "rlimit": null, "rows_match": true, "sat_rows": 1000, "status": "model_cap", "summary_match": true, "wall_s": 165.25475117901806}
{"Drefs": 5094104711, "Irefs": 12089003584, "index": 7, "result": "ok", "rlimit": 5570845, "rows_match": true, "sat_rows": 283, "status": "unsat", "summary_match": true, "wall_s": 43.28802751598414}
{"Drefs": 19740777060, "Irefs": 46501012991, "index": 8, "result": "ok", "rlimit": 11234262, "rows_match": true, "sat_rows": 960, "status": "unsat", "summary_match": true, "wall_s": 152.8238017950207}
{"Drefs": 2968174373, "Irefs": 7107781211, "index": 9, "result": "ok", "rlimit": 3910445, "rows_match": true, "sat_rows": 175, "status": "unsat", "summary_match": true, "wall_s": 27.609584294026718}
{"Drefs": 5242513669, "Irefs": 12474973367, "index": 10, "result": "ok", "rlimit": 5270459, "rows_match": true, "sat_rows": 294, "status": "unsat", "summary_match": true, "wall_s": 45.03519665898057}
{"Drefs": 8807120031, "Irefs": 20918856764, "index": 11, "result": "ok", "rlimit": 7892719, "rows_match": true, "sat_rows": 476, "status": "unsat", "summary_match": true, "wall_s": 73.32475680700736}
{"Drefs": 19540261481, "Irefs": 46181749898, "index": 12, "result": "ok", "rlimit": 11065516, "rows_match": true, "sat_rows": 976, "status": "unsat", "summary_match": true, "wall_s": 156.81482008798048}
{"Drefs": 3266857559, "Irefs": 7791877329, "index": 13, "result": "ok", "rlimit": 3675095, "rows_match": true, "sat_rows": 208, "status": "unsat", "summary_match": true, "wall_s": 30.611537933000363}
{"Drefs": 1455468415, "Irefs": 3438688403, "index": 14, "result": "ok", "rlimit": 2547986, "rows_match": true, "sat_rows": 48, "status": "unsat", "summary_match": true, "wall_s": 14.535529593995307}
{"Drefs": 4798024610, "Irefs": 11450620255, "index": 15, "result": "ok", "rlimit": 4767772, "rows_match": true, "sat_rows": 308, "status": "unsat", "summary_match": true, "wall_s": 43.42804265097948}
{"Drefs": 6617389346, "Irefs": 15756225335, "index": 16, "result": "ok", "rlimit": 6088883, "rows_match": true, "sat_rows": 378, "status": "unsat", "summary_match": true, "wall_s": 58.04973564099055}
{"Drefs": 2623206944, "Irefs": 6233397724, "index": 17, "result": "ok", "rlimit": 3884072, "rows_match": true, "sat_rows": 122, "status": "unsat", "summary_match": true, "wall_s": 24.098719595989678}
{"Drefs": 20317190301, "Irefs": 48073896191, "index": 18, "result": "ok", "rlimit": null, "rows_match": true, "sat_rows": 1000, "status": "model_cap", "summary_match": true, "wall_s": 159.79268081398914}
{"Drefs": 8300954172, "Irefs": 19629680354, "index": 19, "result": "ok", "rlimit": 6353840, "rows_match": true, "sat_rows": 480, "status": "unsat", "summary_match": true, "wall_s": 69.64165620499989}
{"Drefs": 14179092937, "Irefs": 33582821598, "index": 20, "result": "ok", "rlimit": 9491095, "rows_match": true, "sat_rows": 718, "status": "unsat", "summary_match": true, "wall_s": 114.16294155700598}
{"Drefs": 16709683344, "Irefs": 39643555146, "index": 21, "result": "ok", "rlimit": 10856084, "rows_match": true, "sat_rows": 826, "status": "unsat", "summary_match": true, "wall_s": 133.15757928899257}
{"Drefs": 2819607213, "Irefs": 6648092262, "index": 22, "result": "ok", "rlimit": 3681528, "rows_match": true, "sat_rows": 145, "status": "unsat", "summary_match": true, "wall_s": 25.962775474006776}
{"Drefs": 1600688914, "Irefs": 3748123030, "index": 23, "result": "ok", "rlimit": 3586915, "rows_match": true, "sat_rows": 18, "status": "unsat", "summary_match": true, "wall_s": 15.605873304011766}
{"Drefs": 8426537805, "Irefs": 19906790410, "index": 24, "result": "ok", "rlimit": 6770325, "rows_match": true, "sat_rows": 488, "status": "unsat", "summary_match": true, "wall_s": 71.29951649700524}
{"Drefs": 22239379425, "Irefs": 52722089816, "index": 25, "result": "ok", "rlimit": null, "rows_match": true, "sat_rows": 1000, "status": "model_cap", "summary_match": true, "wall_s": 168.73766212898772}
{"Drefs": 4601027894, "Irefs": 10951738406, "index": 26, "result": "ok", "rlimit": 4504902, "rows_match": true, "sat_rows": 300, "status": "unsat", "summary_match": true, "wall_s": 41.474053138983436}
{"Drefs": 1492129380, "Irefs": 3525647601, "index": 27, "result": "ok", "rlimit": 2683108, "rows_match": true, "sat_rows": 48, "status": "unsat", "summary_match": true, "wall_s": 14.786656057985965}
{"Drefs": 21064978232, "Irefs": 49615066685, "index": 28, "result": "ok", "rlimit": null, "rows_match": true, "sat_rows": 1000, "status": "model_cap", "summary_match": true, "wall_s": 160.6019814760075}
{"Drefs": 3115153680, "Irefs": 7429082219, "index": 29, "result": "ok", "rlimit": 3784982, "rows_match": true, "sat_rows": 192, "status": "unsat", "summary_match": true, "wall_s": 29.561157322023064}
{"Drefs": 3911107770, "Irefs": 9268436099, "index": 30, "result": "ok", "rlimit": 4785981, "rows_match": true, "sat_rows": 218, "status": "unsat", "summary_match": true, "wall_s": 34.169090327981394}
{"Drefs": 1149883535, "Irefs": 2708126517, "index": 31, "result": "ok", "rlimit": 2247693, "rows_match": true, "sat_rows": 18, "status": "unsat", "summary_match": true, "wall_s": 11.582546446996275}
{"Drefs": 20227426495, "Irefs": 47719790291, "index": 32, "result": "ok", "rlimit": null, "rows_match": true, "sat_rows": 1000, "status": "model_cap", "summary_match": true, "wall_s": 155.66026481700828}
{"Drefs": 10013710639, "Irefs": 23709546542, "index": 33, "result": "ok", "rlimit": 7520458, "rows_match": true, "sat_rows": 555, "status": "unsat", "summary_match": true, "wall_s": 80.10558931698324}
{"Drefs": 5635379961, "Irefs": 13477437859, "index": 34, "result": "ok", "rlimit": 5681793, "rows_match": true, "sat_rows": 350, "status": "unsat", "summary_match": true, "wall_s": 49.645868379971944}
{"Drefs": 3083203230, "Irefs": 7341590184, "index": 35, "result": "ok", "rlimit": 3874947, "rows_match": true, "sat_rows": 184, "status": "unsat", "summary_match": true, "wall_s": 28.564684952027164}
{"Drefs": 2849768428, "Irefs": 6806875015, "index": 36, "result": "ok", "rlimit": 4180793, "rows_match": true, "sat_rows": 156, "status": "unsat", "summary_match": true, "wall_s": 26.60737776599126}
{"Drefs": 4974049280, "Irefs": 11893431677, "index": 37, "result": "ok", "rlimit": 5265846, "rows_match": true, "sat_rows": 315, "status": "unsat", "summary_match": true, "wall_s": 44.2381655810168}
{"Drefs": 5750469147, "Irefs": 13659060381, "index": 38, "result": "ok", "rlimit": 6465028, "rows_match": true, "sat_rows": 320, "status": "unsat", "summary_match": true, "wall_s": 47.99138225900242}
{"Drefs": 1742545999, "Irefs": 4129205838, "index": 39, "result": "ok", "rlimit": 3243975, "rows_match": true, "sat_rows": 60, "status": "unsat", "summary_match": true, "wall_s": 16.74412334896624}
{"Drefs": 1593484811, "Irefs": 3745354471, "index": 40, "result": "ok", "rlimit": 2821637, "rows_match": true, "sat_rows": 44, "status": "unsat", "summary_match": true, "wall_s": 15.086926841002423}
{"Drefs": 8676330955, "Irefs": 20591519143, "index": 41, "result": "ok", "rlimit": 6518989, "rows_match": true, "sat_rows": 536, "status": "unsat", "summary_match": true, "wall_s": 73.19968526001321}
{"Drefs": 3188279168, "Irefs": 7591814257, "index": 42, "result": "ok", "rlimit": 4140962, "rows_match": true, "sat_rows": 191, "status": "unsat", "summary_match": true, "wall_s": 29.363258183002472}
{"Drefs": 1450968260, "Irefs": 3397737639, "index": 43, "result": "ok", "rlimit": 3556962, "rows_match": true, "sat_rows": 9, "status": "unsat", "summary_match": true, "wall_s": 13.386112829030026}
{"Drefs": 4154242175, "Irefs": 9896795758, "index": 44, "result": "ok", "rlimit": 4149911, "rows_match": true, "sat_rows": 272, "status": "unsat", "summary_match": true, "wall_s": 37.62791131599806}
{"Drefs": 1413168679, "Irefs": 3350848458, "index": 45, "result": "ok", "rlimit": 2324645, "rows_match": true, "sat_rows": 48, "status": "unsat", "summary_match": true, "wall_s": 14.036856487044133}
{"Drefs": 4011327874, "Irefs": 9557060902, "index": 46, "result": "ok", "rlimit": 5028653, "rows_match": true, "sat_rows": 241, "status": "unsat", "summary_match": true, "wall_s": 35.92524636001326}
{"Drefs": 15684252210, "Irefs": 37315669370, "index": 47, "result": "ok", "rlimit": 11033931, "rows_match": true, "sat_rows": 812, "status": "unsat", "summary_match": true, "wall_s": 122.70758976397337}
{"Drefs": 4959435195, "Irefs": 11880877604, "index": 48, "result": "ok", "rlimit": 5520014, "rows_match": true, "sat_rows": 305, "status": "unsat", "summary_match": true, "wall_s": 43.18350752600236}
{"Drefs": 1140173431, "Irefs": 2657476354, "index": 49, "result": "ok", "rlimit": 2567195, "rows_match": true, "sat_rows": 4, "status": "unsat", "summary_match": true, "wall_s": 11.08369149704231}
{"Drefs": 2292816632, "Irefs": 5397605778, "index": 50, "result": "ok", "rlimit": 4362905, "rows_match": true, "sat_rows": 64, "status": "unsat", "summary_match": true, "wall_s": 19.696274674963206}
{"Drefs": 7294980904, "Irefs": 17241379900, "index": 51, "result": "ok", "rlimit": 6465195, "rows_match": true, "sat_rows": 416, "status": "unsat", "summary_match": true, "wall_s": 59.36885249399347}
{"Drefs": 4281834968, "Irefs": 10201895938, "index": 52, "result": "ok", "rlimit": 4585824, "rows_match": true, "sat_rows": 267, "status": "unsat", "summary_match": true, "wall_s": 38.13131931098178}
{"Drefs": 21425561991, "Irefs": 50760472955, "index": 53, "result": "ok", "rlimit": null, "rows_match": true, "sat_rows": 1000, "status": "model_cap", "summary_match": true, "wall_s": 161.03750252601458}
{"Drefs": 1859661833, "Irefs": 4381698561, "index": 54, "result": "ok", "rlimit": 3632614, "rows_match": true, "sat_rows": 48, "status": "unsat", "summary_match": true, "wall_s": 16.846118574030697}
{"Drefs": 3300923790, "Irefs": 7906573521, "index": 55, "result": "ok", "rlimit": 4516898, "rows_match": true, "sat_rows": 188, "status": "unsat", "summary_match": true, "wall_s": 29.616212112014182}
```

### B.3 Seven extended fibers

Record SHA-256: `c51af143908cfece5271cadd0dd7f326be0b5dbbb361548ab90f57a5865407e4`.

```jsonl
{"Drefs": 20562049304, "Irefs": 48512245871, "name": "cube33", "result": "ok", "rows_match": true, "sat_rows": 988, "status": "unsat", "summary_match": true, "wall_s": 157.4564475620282}
{"Drefs": 29962855339, "Irefs": 70642782758, "name": "extension_018", "result": "ok", "rows_match": true, "sat_rows": 1296, "status": "unsat", "summary_match": true, "wall_s": 228.96005071303807}
{"Drefs": 42284141454, "Irefs": 99649523345, "name": "extension_053", "result": "ok", "rows_match": true, "sat_rows": 1575, "status": "unsat", "summary_match": true, "wall_s": 302.4954550290131}
{"Drefs": 56693670250, "Irefs": 132799942181, "name": "extension_032", "result": "ok", "rows_match": true, "sat_rows": 1939, "status": "unsat", "summary_match": true, "wall_s": 405.36728254001355}
{"Drefs": 82884202185, "Irefs": 193808368490, "name": "extension_028", "result": "ok", "rows_match": true, "sat_rows": 2404, "status": "unsat", "summary_match": true, "wall_s": 582.3578611249686}
{"Drefs": 89127824359, "Irefs": 209083052165, "name": "extension_025", "result": "ok", "rows_match": true, "sat_rows": 2456, "status": "unsat", "summary_match": true, "wall_s": 609.8110443049809}
{"Drefs": 106313414635, "Irefs": 248205426768, "name": "extension_006", "result": "ok", "rows_match": true, "sat_rows": 2767, "status": "unsat", "summary_match": true, "wall_s": 731.5263600430335}
```

## Appendix C: self-contained first-block search and ledger

The original 2^35 protocol was fixed before the first production run. Its
1000-group audit input was later independently regenerated from the same
clean corpus and derivative sets, byte for byte, without the costly low16
pair scan. The hygiene replay uses that regenerated file, a zero-block
compressor test vector, the same key and counter range, and the same table
and first-match code. This is a **provenance replay of the same deterministic
stream**, not a second independent success-rate observation. The final
prospective algorithm needs one source campaign, one audit-file generator,
one table build in the sampler, and one full sample. Literal research-history
accounting would count both executions.

The generated 1000-group file has 120,000 bytes and SHA-256
`44a1c1fbe538b2f565c51a0a8bc847a85fbce1f389c7877fb876ddd2491f2171`.
The standalone generator produced exact F7-pass, F6-tuple, key and retained
counts `190385880`, `649543864`, `148169452`, `523821326`. It has fixed
28,848×49,408 W8 probes and at most 512 W7 checks per F7 pass.

The other finite stages use these ordinary-operation ceilings:

    derivative/support scans:
      6*2^32*512 + 64*2^26*64 + 2^28*64
      = 13,486,197,309,440 ops = 6,301,961,359.551 v5
    bounded local repair:
      10,983,442*4096 early checks
      + 2,074*10,983,442*128 node comparisons
      + 5,000,000,000*1024 full checks (<=204 ops actual in build+full)
      + 74,609*49,408*(256+512*64) tuple probes
      + 2,074*4096 node bookkeeping
      = 129,816,552,319,488 ops = 60,661,940,336.209 v5
    sort/recombination/row audit reserve:
      465,356,800*4096 hypothetical recombination cases
      + 9,213*20*512 raw-row sort upper
      + 2^38 data motion + 28,848*8192 final row audit
      = 2,181,310,023,680 ops = 1,019,303,749.383 v5.

The last reserve intentionally overcharges: no E-pair recombination output
is needed in the final 28,848-row corpus. The BFS cap is 10,000 nodes,
20,000,000 early checks and 5,000,000,000 full checks; the receipt reports
2,074 nodes, 10,983,442 early candidates and 74,609 full passes.
One table-build ceiling is:

    28,848*49,408*256
  + 190,385,880*512*64
  + 649,543,864*1024
  + 523,821,326*1024
  + 2^32*32 + 2^41
  = 10,141,435,107,328 ordinary primitives
  = 4,738,988,367.910 v5 units.

The selected first-block and completion charge uses all observed counts and
the following deliberately generous ceilings:

    N = 2^35 = 34,359,738,368
    key_hits = 1,185,317,301
    slot_visits = 4,190,434,465
    W6_slot_hits = 8,194,220
    exact_prefixes = 50
    JOINTs = 7
    Phase3_xz_iterations = 18,026
    Phase3_offset_blocks = 27
    v5_run = N + 100
      + [N*(2048+384)
         + key_hits*1024
         + slot_visits*4096
         + W6_slot_hits*4096
         + exact_prefixes*2^20
         + Phase3_xz_iterations*2^16
         + Phase3_offset_blocks*2048
         + 2^31]/2140
      = 82,012,828,673.907.

The source cost is `160*(7,140,260,742,107+2,992,097,049,978)/2140
=757,559,461,090.467`. Derivative/support scans, BFS, conservative
sorting/recombination, and one sampler table build are `72,722,193,813.054`.
Add the independent audit-file generator table build
`4,738,988,367.910`, the fixed run `82,012,828,673.907`, and the
heuristic `2^48/2140=131,530,362,948.904` uninstrumented reserve. Total
`1,048,563,834,894.243`, log2 `39.931552` < declared `39.98`.
The B=160 conversion, uninstrumented reserve and public-trail treatment
remain explicitly heuristic or conditional.

### C.1 Original prospective protocol

SHA-256: `89148556acb2b2abe25c9ec8e4ba76825a820884b71861095b4154db229bb6f5`. Original scratch paths in this source designate the
inputs described above.

```markdown
# Prospective clean-table deterministic first-block campaign

Declared before launch on 2026-10-06 UTC. This is scratch research and does not change the HashSmash candidate. No earlier witness, block, PRNG seed or event count was used to choose the seed below.

## Frozen inputs and algorithm

- Target: full `sha256-r31-prefix-v1` ordinary collision, standard fixed IV, 31 steps per compression, original schedule/constants and feed-forward.
- Input paired states: `/tmp/r31_publicmask_fibers56/final_clean_union.bin`, exactly 28,848 records of 48 little-endian uint32 words; SHA-256 `66b27ab1e470d232a74a1b2f4e5e48684ac3d5897e337fc26c41e7a7cab64590`.
- Derivative files SHA-256: V5 `34ba7fd8ef34ed6edd4da5408b35fac8cc2fa20c2a7d2aac9b043a1c0c94ac14`; V6 `0479cc49cb235a7dfa0055eb7b719da623386549533ccca10ac383cd6ecf6c8f`; V7 `38734819a79c54a68f0e34a1ce1874cac6db45e1938a0db75c8646bb27a3e147`; V8 `2d96f8568b3d4127c76ba5647623e0411980a13cefc3febbee302112e4949ce6`.
- Independent 1,000-group audit file SHA-256 `44a1c1fbe538b2f565c51a0a8bc847a85fbce1f389c7877fb876ddd2491f2171`.
- Frozen sampler source `/tmp/r31_fixedseed_clean_sampler.c` SHA-256 `3aaf828693f0dd0cb91b20d6ef3b06bf51e113c774d97cde261d515068702179`; compiled binary `/tmp/r31_fixedseed_clean_sampler` SHA-256 `559ef53f0426bed6c34e404c4d4b96e6430b1633ec3d4b3005e28d67f55eff5e`. Compiled with `cc -std=c11 -O3 -march=native -pthread -Wall -Wextra -Werror ... -lm`. A separate Python ChaCha20 implementation matched binary outputs at counters 0, 1 and 2^32.
- Public key derivation string: `HashSmash sha256-r31 clean28k fixed-seed prospective replay 2026-10-06 run 1`. Its SHA-256 is the 32-byte ChaCha20 key `6af5170aa5223b656b9b8e8267b49a5bc7a9efa543d14360207ff63f292dab5f`. Use original ChaCha20 64-bit-counter/64-bit-nonce layout, nonce `726f756e64333121` (little-endian state words), rounds 20. Block counter i produces exactly one 64-byte first block. Every counter 0 through `2^35-1` is used once, partitioned into contiguous ranges among exactly 16 threads. Counter-domain disjointness makes the block stream independent of thread scheduling; no probabilistic independence is inferred from the deterministic PRNG.
- Fixed size N=`2^35 = 34,359,738,368` first blocks. Run every block even after JOINT observations. Self-test, exact table count verification and 1,000-group order check must pass. Log all EXACT and JOINT events, full first-block bytes, full CV, selected group/slot and counter. Do not write/overwrite the 5.376 GB prior group stream. A completed sample requires exit status 0 and `samples=requested=N`.
- After the sample, sort JOINTs by counter. For each, attempt one globally capped Phase-3 completion with deterministic fresh domain-separated offset words; count and preserve all failures, full messages and independent rehash. Select the lowest-counter completed witness. Offset derivation will use ChaCha20 with the same key and nonce at counters `2^48 + 64*i + j` for first-block counter i and g16 candidate j (0<=j<64), taking the first 8 output bytes as the two 32-bit offsets in big-endian order. This is disjoint from the first-block counter domain. The completion-script source and its hash will be frozen before completion execution. If no JOINT completes, this campaign fails; any second seed is a separately declared, fully charged restart.

## Resources and interpretation

- Prior OS-random N=2^37 sampler took 3,776.552 seconds sampling plus about 114 seconds setup, with 27,251,596 KiB peak RSS. ChaCha20 generation adds work; allow considerably more wall time than simple quarter-scaling. Memory and /tmp free space were checked before launch: 358 GiB available RAM, 151 GB /tmp free.
- Dynamic v5 receipt counts all N target compressions, table build, 20-round ChaCha20 generation, all key/group operations, all failed prefix tests, completion and verification. A conservative ChaCha20 ceiling is 2,048 ordinary word-RAM primitives per block (80 quarter rounds ×12 primitives =960, plus state, output and control). No ideal-random-coin success probability follows from this deterministic run. The witness, if any, proves reachability and supports a deterministic stored-witness replay whose construction cost must include the entire search and all prerequisite clean-source/table work.
- This run reuses the existing clean table input. That table's source/trail provenance and all-history v5 charges remain unresolved; a fresh witness does not by itself close them. Do not submit a `ready` claim solely because this run finds a collision.
```

### C.2 Bounded independent samplegroup generator

SHA-256: `52b8a9a1ca2f5f88af4cfc4f575e268e2ef5a585285190b3dfd5efe8c76991e8`. Original scratch paths in this source designate the
inputs described above.

```c
/* Bounded, standalone generator for the fixed-seed sampler's 1000 group check.
 * Inputs: clean paired-state corpus, ordered V7 and V8 derivative lists.
 * Output: samplegroup records in first-key order. No overlap scan is used.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct { uint32_t lane_a[24], lane_b[24]; } PairRow;
typedef struct { uint32_t key, count; uint64_t tuple[8]; } Bucket;
typedef struct { uint16_t e4, e3, a0, ce2, base, c6, key; } Projection;
typedef struct { uint32_t key, count; Projection projection[8]; } AuditGroup;
_Static_assert(sizeof(PairRow) == 192, "paired state record layout");
_Static_assert(sizeof(Bucket) == 72, "bucket layout");
_Static_assert(sizeof(AuditGroup) == 120, "audit record layout");

static const char *const output_path =
    "/tmp/r31_fixedseed_regenerated_samplegroups.bin";
static PairRow *rows;
static uint32_t v7[512], v8[49408];
static uint32_t *key_dir;
static Bucket *buckets;
static uint64_t keys, tuples, kept, pass8;

static inline uint32_t ror(uint32_t x, unsigned n) {
    return (x >> n) | (x << (32 - n));
}
static inline uint32_t sigma_a(uint32_t x) {
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22);
}
static inline uint32_t sigma_e(uint32_t x) {
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25);
}
static inline uint32_t ch(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ ((~x) & z);
}
static inline uint32_t maj(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (x & z) ^ (y & z);
}

static void read_whole(const char *path, void *dst, size_t bytes) {
    FILE *f = fopen(path, "rb");
    if (!f) { perror(path); exit(2); }
    if (fread(dst, 1, bytes, f) != bytes || fgetc(f) != EOF) {
        fprintf(stderr, "wrong input length: %s\n", path); exit(3);
    }
    if (fclose(f)) { perror(path); exit(4); }
}

static uint32_t sample_hash(uint32_t key) {
    key ^= key >> 16;
    key *= 0x7feb352dU;
    key ^= key >> 15;
    key *= 0x846ca68bU;
    key ^= key >> 16;
    return key;
}

static Projection project(uint32_t key, uint64_t packed) {
    const uint32_t p = (uint32_t)(packed >> 25);
    const uint32_t j = (uint32_t)((packed >> 9) & 65535U);
    const uint32_t k = (uint32_t)(packed & 511U);
    if (p >= 28848U || j >= 49408U || k >= 512U) exit(5);
    const uint32_t *a = rows[p].lane_a;
    const uint32_t e4 = a[15] - a[3] - sigma_e(a[14])
        - ch(a[14], a[13], a[12]) - 0xd807aa98U - v8[j];
    const uint32_t e3 = a[14] - a[2] - sigma_e(a[13])
        - ch(a[13], a[12], e4) - 0xab1c5ed5U - v7[k];
    const uint32_t a0 = e4 - a[3] + sigma_a(a[2])
        + maj(a[2], a[1], a[0]);
    const uint32_t rebuilt_key = e3 - a[2] + sigma_a(a[1])
        + maj(a[1], a[0], a0);
    if (rebuilt_key != key) exit(6);
    const uint32_t ce2 = a[1] - sigma_a(a[0])
        - maj(a[0], a0, key);
    const uint32_t base = a[12] - 2U * a[0] + sigma_a(a0)
        - sigma_e(e4) - 0x59f111f1U;
    const uint32_t c6 = a[13] - 2U * a[1] + sigma_a(a[0])
        + maj(a[0], a0, key) - sigma_e(a[12])
        - ch(a[12], e4, e3) - 0x923f82a4U;
    return (Projection){e4, e3, a0, ce2, base, c6, key};
}

int main(void) {
    const time_t started = time(NULL);
    rows = malloc(28848U * sizeof(*rows));
    key_dir = calloc(UINT64_C(1) << 32, sizeof(*key_dir));
    buckets = malloc(UINT64_C(160000000) * sizeof(*buckets));
    if (!rows || !key_dir || !buckets) { perror("allocation"); return 7; }
    read_whole("/tmp/r31_publicmask_fibers56/final_clean_union.bin",
               rows, 28848U * sizeof(*rows));
    read_whole("/tmp/r31_v7.bin", v7, sizeof(v7));
    read_whole("/tmp/r31_v8.bin", v8, sizeof(v8));

    for (uint32_t p = 0; p < 28848U; p++) {
        const uint32_t *a = rows[p].lane_a;
        const uint32_t *b = rows[p].lane_b;
        const uint32_t need7 = b[14] - a[14]
            - (sigma_e(b[13]) - sigma_e(a[13])) - 0x4fefb5faU;
        const uint32_t need6 = b[13] - a[13]
            - (sigma_e(b[12]) - sigma_e(a[12])) - 0x002087f1U;
        const uint32_t e4_base = a[15] - a[3] - sigma_e(a[14])
            - ch(a[14], a[13], a[12]) - 0xd807aa98U;
        const uint32_t a0_base = 0U - a[3] + sigma_a(a[2])
            + maj(a[2], a[1], a[0]);
        for (uint32_t j = 0; j < 49408U; j++) {
            const uint32_t e4 = e4_base - v8[j];
            if (ch(b[13], b[12], e4) - ch(a[13], a[12], e4)
                != need7) continue;
            if (++pass8 > 190385880ULL) {
                fprintf(stderr, "F7 cap exceeded\n"); return 8;
            }
            const uint32_t e3_base = a[14] - a[2] - sigma_e(a[13])
                - ch(a[13], a[12], e4) - 0xab1c5ed5U;
            const uint32_t a0 = e4 + a0_base;
            for (uint32_t k = 0; k < 512U; k++) {
                const uint32_t e3 = e3_base - v7[k];
                if (ch(b[12], e4, e3) - ch(a[12], e4, e3)
                    != need6) continue;
                const uint32_t e2 = a[13] - a[1] - sigma_e(a[12])
                    - ch(a[12], e4, e3) - 0x923f82a4U;
                const uint32_t e2p = b[13] - b[1] - sigma_e(b[12])
                    - ch(b[12], e4, e3) - 0x923f82a4U - 0x002087f1U;
                if (e2 != e2p) {
                    fprintf(stderr, "noncommon E2 at p=%u j=%u k=%u\n",p,j,k);
                    return 9;
                }
                if (++tuples > 649543864ULL) {
                    fprintf(stderr, "tuple cap exceeded\n"); return 10;
                }
                const uint32_t key = e3 - a[2] + sigma_a(a[1])
                    + maj(a[1], a[0], a0);
                uint32_t id = key_dir[key];
                if (!id) {
                    if (keys >= 148169452ULL) {
                        fprintf(stderr, "key cap exceeded\n"); return 11;
                    }
                    id = (uint32_t)(++keys);
                    key_dir[key] = id;
                    buckets[id - 1].key = key;
                    buckets[id - 1].count = 0;
                }
                Bucket *g = &buckets[id - 1];
                if (g->key != key) return 12;
                if (g->count < 8U) {
                    if (++kept > 523821326ULL) {
                        fprintf(stderr, "retained-record cap exceeded\n");
                        return 13;
                    }
                    g->tuple[g->count++] = ((uint64_t)p << 25)
                        | ((uint64_t)j << 9) | k;
                }
            }
        }
        if ((p + 1) % 10000U == 0)
            fprintf(stderr, "rows=%u pass8=%llu tuples=%llu keys=%llu kept=%llu seconds=%ld\n",
                    p + 1, (unsigned long long)pass8,
                    (unsigned long long)tuples, (unsigned long long)keys,
                    (unsigned long long)kept, (long)(time(NULL) - started));
    }
    if (pass8 != 190385880ULL || tuples != 649543864ULL
        || keys != 148169452ULL || kept != 523821326ULL) {
        fprintf(stderr, "final table counts disagree\n"); return 14;
    }
    FILE *out = fopen(output_path, "wb");
    if (!out) { perror(output_path); return 15; }
    uint32_t count = 0;
    for (uint64_t i = 0; i < keys && count < 1000U; i++) {
        Bucket *g = &buckets[i];
        if (g->count < 2U || (sample_hash(g->key) & 65535U)) continue;
        AuditGroup record;
        memset(&record, 0, sizeof(record));
        record.key = g->key;
        record.count = g->count;
        for (uint32_t j = 0; j < g->count; j++)
            record.projection[j] = project(g->key, g->tuple[j]);
        if (fwrite(&record, sizeof(record), 1, out) != 1) {
            perror(output_path); return 16;
        }
        count++;
    }
    if (fclose(out)) { perror(output_path); return 17; }
    if (count != 1000U) {
        fprintf(stderr, "sample count %u != 1000\n", count); return 18;
    }
    fprintf(stderr, "PASS output=%s samples=%u pass8=%llu tuples=%llu keys=%llu kept=%llu seconds=%ld\n",
            output_path, count, (unsigned long long)pass8,
            (unsigned long long)tuples, (unsigned long long)keys,
            (unsigned long long)kept, (long)(time(NULL) - started));
    return 0;
}
```

### C.3 Hygiene replay protocol

SHA-256: `debddfc9aea467962854e70dc08f360db8c66b305d4981b5561e94483a3f2b60`. Original scratch paths in this source designate the
inputs described above.

```markdown
# Self-contained-input fixed-seed hygiene replay

Prepared before this replay on 2026-10-06 UTC. This is an exact replay of the
already declared public ChaCha20 seed and fixed `2^35` counter range. Its
success is known from the original run, so this replay is a reproducibility
and provenance check, not a new independent success-rate experiment.

The independent samplegroup generator
`/tmp/r31_fixedseed_regen_samplegroups.c` SHA-256
`52b8a9a1ca2f5f88af4cfc4f575e268e2ef5a585285190b3dfd5efe8c76991e8`
reads only the clean 28,848-row corpus and ordered V7/V8 arrays. It generated
`/tmp/r31_fixedseed_regenerated_samplegroups.bin`, SHA-256
`44a1c1fbe538b2f565c51a0a8bc847a85fbce1f389c7877fb876ddd2491f2171`,
byte-identical to the former 1,000-group file. Its loop/counter caps and
one-table-build ceiling are recorded in the source-cost ledger. The old full
low16 pair scan is not an input to this replay.

The hygiene sampler source
`/tmp/r31_fixedseed_clean_sampler_hygiene.c` SHA-256
`1364fa7c9ee828660bd55901d206c18c2c40aaca2772404907fadba4cde9162f`
and binary `/tmp/r31_fixedseed_clean_sampler_hygiene` SHA-256
`ab9cf86aa8d841bda2a7fba1f01595f1723143354bd35c0c32a4268626b2d7b8`
differ from the original only in reading the regenerated samplegroup path and
using a zero-block 31-step compressor test vector instead of a published
message; the synthetic prefix self-test using a table tuple was removed.
The zero-block expected CV
`4040405c f2748fa6 da85111b 3466cf21 24fa803e 070adead 4164f0c4 8e90bc86`
was obtained independently from two Python compressors. This variant has no
published collision block, published second-block pair, or old overlap output
as runtime input.

The sample is exactly all counters `0..2^35-1`, 16 disjoint ranges, no early
stop. The only first-block input is original ChaCha20 with key
`6af5170aa5223b656b9b8e8267b49a5bc7a9efa543d14360207ff63f292dab5f`
and nonce `726f756e64333121`. Results will be redirected to
`/tmp/r31_fixedseed_hygiene_2p35.stdout` and `.stderr`; the original run's
logs and collision records are left intact. Compare event counter sets, exact
and JOINT counts, output messages and collision digests to the original; do
not infer independent statistical evidence from this identical deterministic
stream. Charge both executions if literal all-history review requires them.
```

### C.4 Hygiene fixed-seed sampler

SHA-256: `1364fa7c9ee828660bd55901d206c18c2c40aaca2772404907fadba4cde9162f`. Original scratch paths in this source designate the
inputs described above.

```c
/* Prospective fixed-seed fixed-size first-block search against the clean
 * SHA-256-r31 tuple table. Scratch evidence only; not participant code.
 * ChaCha20 uses a 64-bit block counter and a fixed 64-bit nonce. */
#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <math.h>
#include <stdatomic.h>

typedef struct {uint32_t a[24],b[24];} Point;
typedef struct {uint32_t key,n;uint64_t packed[8];} Group;
_Static_assert(sizeof(Group)==72,"group layout");
static Point *P;
static Group *G;
static uint32_t *slot;
static uint32_t v5[16384],v7[512],v8[49408];
static uint8_t *v5lo16,*v5lo20,*v5lo24,*v6bits;
static size_t ng;
static uint64_t nretained;
static const uint8_t PRNG_KEY[32]={
 0x6a,0xf5,0x17,0x0a,0xa5,0x22,0x3b,0x65,
 0x6b,0x9b,0x8e,0x82,0x67,0xb4,0x9a,0x5b,
 0xc7,0xa9,0xef,0xa5,0x43,0xd1,0x43,0x60,
 0x20,0x7f,0xf6,0x3f,0x29,0x2d,0xab,0x5f};
static const uint64_t PRNG_NONCE=0x726f756e64333121ULL;

static const uint32_t K[31]={
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351};
static const uint32_t IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t B0(uint32_t x){return R(x,2)^R(x,13)^R(x,22);}
static inline uint32_t B1(uint32_t x){return R(x,6)^R(x,11)^R(x,25);}
static inline uint32_t S0(uint32_t x){return R(x,7)^R(x,18)^(x>>3);}
static inline uint32_t S1(uint32_t x){return R(x,17)^R(x,19)^(x>>10);}
static inline uint32_t C(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t M(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static inline uint32_t BE(const unsigned char*p){return ((uint32_t)p[0]<<24)|((uint32_t)p[1]<<16)|((uint32_t)p[2]<<8)|p[3];}
static inline uint32_t LE(const uint8_t*p){return (uint32_t)p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24);}
static inline void storeLE(uint8_t*p,uint32_t x){p[0]=x;p[1]=x>>8;p[2]=x>>16;p[3]=x>>24;}
static inline uint32_t rol32(uint32_t x,unsigned n){return (x<<n)|(x>>(32-n));}
#define QR(a,b,c,d) do { \
 x[a]+=x[b];x[d]^=x[a];x[d]=rol32(x[d],16); \
 x[c]+=x[d];x[b]^=x[c];x[b]=rol32(x[b],12); \
 x[a]+=x[b];x[d]^=x[a];x[d]=rol32(x[d],8);  \
 x[c]+=x[d];x[b]^=x[c];x[b]=rol32(x[b],7);  \
} while(0)
static void chacha20_block(uint64_t counter,uint8_t out[64]){
 uint32_t s[16]={0x61707865,0x3320646e,0x79622d32,0x6b206574};
 for(int i=0;i<8;i++)s[4+i]=LE(PRNG_KEY+4*i);
 s[12]=(uint32_t)counter;s[13]=(uint32_t)(counter>>32);
 s[14]=(uint32_t)PRNG_NONCE;s[15]=(uint32_t)(PRNG_NONCE>>32);
 uint32_t x[16];memcpy(x,s,sizeof(x));
 for(int i=0;i<10;i++){
  QR(0,4,8,12);QR(1,5,9,13);QR(2,6,10,14);QR(3,7,11,15);
  QR(0,5,10,15);QR(1,6,11,12);QR(2,7,8,13);QR(3,4,9,14);
 }
 for(int i=0;i<16;i++)storeLE(out+4*i,x[i]+s[i]);
}
#undef QR
static inline void compress31(const unsigned char*b,uint32_t*out){
 uint32_t w[31];for(int i=0;i<16;i++)w[i]=BE(b+4*i);
 for(int i=16;i<31;i++)w[i]=w[i-16]+S0(w[i-15])+w[i-7]+S1(w[i-2]);
 uint32_t a=IV[0],bb=IV[1],c=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
 for(int i=0;i<31;i++){
  uint32_t t1=h+B1(e)+C(e,f,g)+K[i]+w[i],t2=B0(a)+M(a,bb,c);
  h=g;g=f;f=e;e=d+t1;d=c;c=bb;bb=a;a=t1+t2;
 }
 out[0]=IV[0]+a;out[1]=IV[1]+bb;out[2]=IV[2]+c;out[3]=IV[3]+d;
 out[4]=IV[4]+e;out[5]=IV[5]+f;out[6]=IV[6]+g;out[7]=IV[7]+h;
}
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
static int load_words(const char*name,void*dst,size_t bytes){
 FILE*f=fopen(name,"rb");if(!f){perror(name);return 0;}
 if(fread(dst,1,bytes,f)!=bytes){fprintf(stderr,"short read %s\n",name);fclose(f);return 0;}
 if(fgetc(f)!=EOF){fprintf(stderr,"extra bytes %s\n",name);fclose(f);return 0;}
 fclose(f);return 1;
}
static void build_table(void){
 double t0=now();P=malloc(28848*sizeof(Point));
 if(!P||!load_words("/tmp/r31_publicmask_fibers56/final_clean_union.bin",P,28848*sizeof(Point))||
    !load_words("/tmp/r31_v7.bin",v7,sizeof(v7))||!load_words("/tmp/r31_v8.bin",v8,sizeof(v8))||
    !load_words("/tmp/r31_v5.bin",v5,sizeof(v5)))exit(2);
 slot=calloc(1ULL<<32,sizeof(uint32_t));
 G=malloc(160000000ULL*sizeof(Group));if(!slot||!G){perror("table allocation");exit(3);}
 uint64_t tuples=0,pass8=0,reject5=0;
 for(uint32_t p=0;p<28848;p++){
  uint32_t *a=P[p].a,*b=P[p].b;
  uint32_t rhs7=b[14]-a[14]-(B1(b[13])-B1(a[13]))-0x4fefb5fa;
  uint32_t rhs6=b[13]-a[13]-(B1(b[12])-B1(a[12]))-0x002087f1;
  uint32_t c4=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98;
  uint32_t c0=-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
  for(uint32_t j=0;j<49408;j++){
   uint32_t e4=c4-v8[j];
   if(C(b[13],b[12],e4)-C(a[13],a[12],e4)!=rhs7)continue;
   pass8++;
   uint32_t c3=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4+c0;
   for(uint32_t k=0;k<512;k++){
    uint32_t e3=c3-v7[k];
    if(C(b[12],e4,e3)-C(a[12],e4,e3)!=rhs6)continue;
    uint32_t e2=a[13]-a[1]-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
    uint32_t e2p=b[13]-b[1]-B1(b[12])-C(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2p){reject5++;continue;}
    uint32_t key=e3-a[2]+B0(a[1])+M(a[1],a[0],a0);
    uint32_t id=slot[key];Group *g;
    if(!id){if(ng>=160000000ULL){fprintf(stderr,"table capacity\n");exit(4);}
     g=&G[ng];g->key=key;g->n=0;slot[key]=(uint32_t)(++ng);
    }else g=&G[id-1];
    if(g->n<8){g->packed[g->n++]=((uint64_t)p<<25)|((uint64_t)j<<9)|k;nretained++;}
    tuples++;
   }
  }
  if((p+1)%10000==0)fprintf(stderr,"build rows=%u tuples=%llu keys=%zu retained=%llu elapsed=%.1f\n",
   p+1,(unsigned long long)tuples,ng,(unsigned long long)nretained,now()-t0);
 }
 if(tuples!=649543864ULL||ng!=148169452ULL||nretained!=523821326ULL||
    pass8!=190385880ULL||reject5!=0){
  fprintf(stderr,"TABLE COUNT FAILURE: tuples=%llu keys=%zu retained=%llu pass8=%llu reject5=%llu\n",
   (unsigned long long)tuples,ng,(unsigned long long)nretained,(unsigned long long)pass8,(unsigned long long)reject5);exit(5);
 }
 fprintf(stderr,"build verified tuples=%llu keys=%zu retained=%llu pass8=%llu reject5=%llu seconds=%.3f\n",
  (unsigned long long)tuples,ng,(unsigned long long)nretained,(unsigned long long)pass8,(unsigned long long)reject5,now()-t0);
 fprintf(stderr,"group_stream_bytes_not_rewritten=%llu (prior stream independently audited)\n",(unsigned long long)(8*ng+8*nretained));
 typedef struct {uint16_t e4,e3,a0,ce2,base,c6,key;} Info;
 typedef struct {uint32_t key,m;Info in[8];} SampleGroup;
 _Static_assert(sizeof(SampleGroup)==120,"sample group layout");
 FILE*sf=fopen("/tmp/r31_fixedseed_regenerated_samplegroups.bin","rb");
 if(!sf){perror("sample groups");exit(13);}
 uint32_t checked=0;
 for(size_t i=0;i<ng&&checked<1000;i++){
  const Group*g=&G[i];if(g->n<2)continue;
  uint32_t hash=g->key;hash^=hash>>16;hash*=0x7feb352dU;hash^=hash>>15;hash*=0x846ca68bU;hash^=hash>>16;
  if(hash&65535u)continue;
  SampleGroup old;memset(&old,0,sizeof(old));if(fread(&old,sizeof(old),1,sf)!=1)exit(14);
  if(old.key!=g->key||old.m!=g->n){fprintf(stderr,"sample group header mismatch at %u\n",checked);exit(15);}
  for(uint32_t z=0;z<g->n;z++){
   uint64_t packed=g->packed[z];uint32_t p=packed>>25,j=(packed>>9)&65535,k=packed&511;
   uint32_t*a=P[p].a,key=g->key;
   uint32_t e4=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98-v8[j];
   uint32_t e3=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5-v7[k];
   uint32_t a0=e4-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
   uint32_t ce2=a[1]-B0(a[0])-M(a[0],a0,key);
   uint32_t base=a[12]-2*a[0]+B0(a0)-B1(e4)-0x59f111f1;
   uint32_t c6=a[13]-2*a[1]+B0(a[0])+M(a[0],a0,key)-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
   Info fresh={e4,e3,a0,ce2,base,c6,key};
   if(memcmp(&fresh,&old.in[z],sizeof(fresh))){fprintf(stderr,"sample group tuple mismatch group %u slot %u\n",checked,z);exit(16);}
  }
  checked++;
 }
 if(checked!=1000||fgetc(sf)!=EOF){fprintf(stderr,"sample groups count mismatch %u\n",checked);exit(17);}
 fclose(sf);fprintf(stderr,"independent_low8_samplegroups_match=1000\n");
}
static void build_sets(void){
 v5lo16=calloc(1,1u<<13);v5lo20=calloc(1,1u<<17);v5lo24=calloc(1,1u<<21);
 v6bits=calloc(1,1ULL<<29);if(!v5lo16||!v5lo20||!v5lo24||!v6bits)exit(6);
 for(int i=0;i<16384;i++){
  uint32_t w=v5[i],k=w&65535;v5lo16[k>>3]|=1u<<(k&7);
  k=w&1048575;v5lo20[k>>3]|=1u<<(k&7);
  k=w&16777215;v5lo24[k>>3]|=1u<<(k&7);
 }
 FILE*f=fopen("/tmp/r31_v6.bin","rb");if(!f){perror("v6");exit(7);}
 for(size_t i=0;i<(1ULL<<23);i++){
  uint32_t w;if(fread(&w,4,1,f)!=1)exit(8);v6bits[w>>3]|=(uint8_t)(1u<<(w&7));
 }if(fgetc(f)!=EOF)exit(9);fclose(f);
}
static inline int in5(uint32_t w){
 size_t lo=0,hi=16384;while(lo<hi){size_t mid=(lo+hi)>>1;if(v5[mid]<w)lo=mid+1;else hi=mid;}
 return lo<16384&&v5[lo]==w;
}
static inline int good_c18(uint32_t c18){
 static const uint32_t low[4]={0x031bbffc,0x064bbffe,0x09b3bffd,0x0ce3bfff};
 for(uint32_t hi=0;hi<16;hi++)for(int z=0;z<4;z++){
  uint32_t g=(hi<<28)|low[z],u=S1(g)+c18;
  if(S1(u+0xffff7ffc)-S1(u)==0x2ffe7fe0)return 1;
 }return 0;
}
typedef struct{
 uint64_t start,target,processed,key_hits,slots_seen,slot_w6[8],slot_w5low16[8],slot_w5low20[8],slot_w5low24[8],slot_exact[8];
 uint64_t any_w6,any_w5low16,any_w5low20,any_w5low24,any_exact,joint,w6_mismatch,key_mismatch;
 uint64_t multiplicity[9],hist[256];int err;
} Stat;
static void*worker(void*arg){
 Stat*s=arg;uint8_t block[64];
 for(uint64_t ix=0;ix<s->target;ix++){
   chacha20_block(s->start+ix,block);
   uint32_t cv[8];compress31(block,cv);uint32_t key=cv[0];s->hist[key>>24]++;
   if((ix&((1ULL<<27)-1))==0)
    fprintf(stderr,"PROGRESS thread_start=%llu processed=%llu\n",(unsigned long long)s->start,(unsigned long long)ix);
   uint32_t id=slot[key];if(!id)continue;
   s->key_hits++;const Group*g=&G[id-1];if(g->key!=key){s->key_mismatch++;continue;}
   s->slots_seen+=g->n;s->multiplicity[g->n]++;
   int flag6=0,flag16=0,flag20=0,flag24=0,flag_exact=0;
   for(uint32_t z=0;z<g->n;z++){
    uint64_t pack=g->packed[z];uint32_t p=(uint32_t)(pack>>25),j=(uint32_t)((pack>>9)&65535),k=(uint32_t)(pack&511);
    if(p>=28848||j>=49408||k>=512){s->err=3;return NULL;}
    uint32_t*a=P[p].a;
    uint32_t e4=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98-v8[j];
    uint32_t e3=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5-v7[k];
    uint32_t a0=e4-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
    uint32_t c6=a[13]-2*a[1]+B0(a[0])+M(a[0],a0,key)-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
    uint32_t w6=c6-cv[1];if(!((v6bits[w6>>3]>>(w6&7))&1))continue;
    flag6=1;s->slot_w6[z]++;
    uint32_t e2=a[1]+cv[1]-B0(a[0])-M(a[0],a0,key);
    uint32_t w6check=a[13]-a[1]-e2-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
    if(w6check!=w6){s->w6_mismatch++;continue;}
    uint32_t e1=a[0]+cv[2]-B0(a0)-M(a0,key,cv[1]);
    uint32_t w5=a[12]-a[0]-e1-B1(e4)-C(e4,e3,e2)-0x59f111f1;
    int q16=(v5lo16[(w5&65535)>>3]>>((w5&65535)&7))&1;
    int q20=(v5lo20[(w5&1048575)>>3]>>((w5&1048575)&7))&1;
    int q24=(v5lo24[(w5&16777215)>>3]>>((w5&16777215)&7))&1;
    s->slot_w5low16[z]+=q16;s->slot_w5low20[z]+=q20;s->slot_w5low24[z]+=q24;
    flag16|=q16;flag20|=q20;flag24|=q24;
    if(!in5(w5))continue;
    s->slot_exact[z]++;
    if(!flag_exact){
     flag_exact=1;
     uint32_t e0=a0+cv[3]-B0(key)-M(key,cv[1],cv[2]);
     uint32_t w2=e2-cv[1]-cv[5]-B1(e1)-C(e1,e0,cv[4])-K[2];
     uint32_t w3=e3-key-cv[4]-B1(e2)-C(e2,e1,e0)-K[3];
     uint32_t c18=a[22]+S0(w3)+w2;
     int good=good_c18(c18);s->joint+=good;
     flockfile(stderr);
     fprintf(stderr,"COUNTER value=%llu\n",(unsigned long long)(s->start+ix));
     fprintf(stderr,"%s slot=%u key=%08x point=%u v8_index=%u v7_index=%u w6=%08x w5=%08x c18=%08x cv=",
      good?"JOINT":"EXACT",z,key,p,j,k,w6,w5,c18);
     for(int q=0;q<8;q++)fprintf(stderr,"%08x%s",cv[q],q==7?"":" ");
     fprintf(stderr," block=");for(int q=0;q<64;q++)fprintf(stderr,"%02x",block[q]);
     fprintf(stderr,"\nGROUP key=%08x selected_slot=%u count=%u entries=",key,z,g->n);
     for(uint32_t q=0;q<g->n;q++){
      uint64_t value=g->packed[q];
      fprintf(stderr,"%s%u:%u:%u",q?",":"",(unsigned)(value>>25),
       (unsigned)((value>>9)&65535),(unsigned)(value&511));
     }
     fprintf(stderr,"\n");funlockfile(stderr);
    }
   }
   s->any_w6+=flag6;s->any_w5low16+=flag16;s->any_w5low20+=flag20;s->any_w5low24+=flag24;s->any_exact+=flag_exact;
 }
 s->processed=s->target;return NULL;
}
int main(int argc,char**argv){
 if(argc==2&&!strcmp(argv[1],"--prng-selftest")){
  uint8_t block[64];const uint64_t at[]={0,1,0x100000000ULL};
  for(int j=0;j<3;j++){
   chacha20_block(at[j],block);
   printf("PRNG_COUNTER=%llu BLOCK=",(unsigned long long)at[j]);
   for(int k=0;k<64;k++)printf("%02x",block[k]);
   putchar('\n');
  }
  return 0;
 }
 if(argc!=3){fprintf(stderr,"usage: %s samples threads\n",argv[0]);return 1;}
 uint64_t n=strtoull(argv[1],0,0),requested=n;int nt=atoi(argv[2]);if(n!=(1ULL<<35)||nt!=16)return 1;
 uint8_t zero_block[64]={0};uint32_t cv[8];compress31(zero_block,cv);
 static const uint32_t expect_cv[8]={
  0x4040405c,0xf2748fa6,0xda85111b,0x3466cf21,
  0x24fa803e,0x070adead,0x4164f0c4,0x8e90bc86};
 if(memcmp(cv,expect_cv,sizeof(expect_cv))){fprintf(stderr,"zero-block selftest fail\n");return 2;}
 fprintf(stderr,"zero-block 31-step selftest pass\n");
 build_table();build_sets();
 pthread_t thread[128];Stat stats[128]={0},sum={0};double t0=now();
 uint64_t next=0;
 for(int i=0;i<nt;i++){
  stats[i].start=next;stats[i].target=n/nt+(i<(int)(n%nt));next+=stats[i].target;
  if(pthread_create(&thread[i],0,worker,&stats[i]))return 3;
 }
 if(next!=n)return 3;
 for(int i=0;i<nt;i++)pthread_join(thread[i],0);
 for(int i=0;i<nt;i++){
  Stat*s=&stats[i];if(s->err){fprintf(stderr,"worker error=%d\n",s->err);return 4;}
  sum.processed+=s->processed;sum.key_hits+=s->key_hits;sum.slots_seen+=s->slots_seen;
  sum.any_w6+=s->any_w6;sum.any_w5low16+=s->any_w5low16;sum.any_w5low20+=s->any_w5low20;
  sum.any_w5low24+=s->any_w5low24;sum.any_exact+=s->any_exact;sum.joint+=s->joint;
  sum.w6_mismatch+=s->w6_mismatch;sum.key_mismatch+=s->key_mismatch;
  for(int z=0;z<8;z++){
   sum.slot_w6[z]+=s->slot_w6[z];sum.slot_w5low16[z]+=s->slot_w5low16[z];
   sum.slot_w5low20[z]+=s->slot_w5low20[z];sum.slot_w5low24[z]+=s->slot_w5low24[z];sum.slot_exact[z]+=s->slot_exact[z];
  }
  for(int z=0;z<9;z++)sum.multiplicity[z]+=s->multiplicity[z];
  for(int z=0;z<256;z++)sum.hist[z]+=s->hist[z];
 }
 n=sum.processed;
 double p=(double)ng/4294967296.0,expected=(double)n*p;
 double z=((double)sum.key_hits-expected)/sqrt(expected*(1-p));
 double chi=0,eb=(double)n/256;for(int i=0;i<256;i++){double d=sum.hist[i]-eb;chi+=d*d/eb;}
 uint64_t all_w6=0;for(int z=0;z<8;z++)all_w6+=sum.slot_w6[z];
 double expected_slot=(double)n*(double)nretained/4294967296.0/512.0;
 double exp_lower_prefix=(double)n*148169452.0/576460752303423488.0;
 double exp_upper_prefix=(double)n*(double)nretained/576460752303423488.0;
 printf("samples=%llu requested=%llu stopped_on_joint=0 threads=%d prng=ChaCha20_64bit_counter nonce=%016llx key=6af5170aa5223b656b9b8e8267b49a5bc7a9efa543d14360207ff63f292dab5f selftest=pass sample_wall_s=%.3f\n",
  (unsigned long long)n,(unsigned long long)requested,nt,(unsigned long long)PRNG_NONCE,now()-t0);
 printf("table_keys=%zu table_retained=%llu key_hits=%llu expected_key_hits=%.3f key_z=%.5f top8_chisq_255df=%.3f key_mismatch=%llu\n",
  ng,(unsigned long long)nretained,(unsigned long long)sum.key_hits,expected,z,chi,(unsigned long long)sum.key_mismatch);
 printf("slots_seen=%llu all_slot_w6=%llu expected_all_slot_w6=%.3f z=%.5f any_w6=%llu w6_mismatch=%llu\n",
  (unsigned long long)sum.slots_seen,(unsigned long long)all_w6,expected_slot,
  ((double)all_w6-expected_slot)/sqrt(expected_slot),(unsigned long long)sum.any_w6,(unsigned long long)sum.w6_mismatch);
 printf("any_w5_low16=%llu any_w5_low20=%llu any_w5_low24=%llu any_exact=%llu joint_c18=%llu uniform_prefix_bounds=[%.6f,%.6f] uniform_joint_lower=%.6f\n",
  (unsigned long long)sum.any_w5low16,(unsigned long long)sum.any_w5low20,
  (unsigned long long)sum.any_w5low24,(unsigned long long)sum.any_exact,(unsigned long long)sum.joint,
  exp_lower_prefix,exp_upper_prefix,exp_lower_prefix*584683520.0/4294967296.0);
 for(int z=0;z<8;z++)printf("slot%u w6=%llu w5low16=%llu w5low20=%llu w5low24=%llu exact=%llu\n",
  z,(unsigned long long)sum.slot_w6[z],(unsigned long long)sum.slot_w5low16[z],
  (unsigned long long)sum.slot_w5low20[z],(unsigned long long)sum.slot_w5low24[z],
  (unsigned long long)sum.slot_exact[z]);
 for(int z=1;z<=8;z++)printf("key_group_hist%u=%llu\n",z,(unsigned long long)sum.multiplicity[z]);
 return 0;
}
```

## Appendix D: literal-difference completion and exact witnesses

The completion helpers below contain literal public dW5..9 values and no
legacy message data or Git-file reads. They reconstruct paired second-block
states, enumerate eligible G16 words, consume domain-separated ChaCha20
offset pairs, enforce the global Phase3 cap and independently rehash each
padded full message. The separate FIPS-style audit tested the same seven
pairs; all passed. The organizer's certificate verifier separately checks
the binary messages in `certificates/manifest.json`.

### D.1 SHA-256 core and literal constants

SHA-256: `5720b0601151bc32918c7125349aad2398dee7e1c411e216aa9b2aae87c1a96b`. Original scratch paths in this source designate the
inputs described above.

```python
"""Minimal SHA-256/31 core with no published message or pair values."""

MASK = 0xFFFFFFFF

K = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B,
    0x59F111F1, 0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01,
    0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7,
    0xC19BF174, 0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA, 0x983E5152,
    0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147,
    0x06CA6351,
]

IV = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

def rr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK

def big0(x):
    return rr(x, 2) ^ rr(x, 13) ^ rr(x, 22)

def big1(x):
    return rr(x, 6) ^ rr(x, 11) ^ rr(x, 25)

def small0(x):
    return rr(x, 7) ^ rr(x, 18) ^ (x >> 3)

def small1(x):
    return rr(x, 17) ^ rr(x, 19) ^ (x >> 10)

def choose(x, y, z):
    return (x & y) ^ ((~x) & z)

def majority(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def compress(h, block):
    w = list(block)
    for t in range(16, 31):
        w.append((small1(w[t-2]) + w[t-7] + small0(w[t-15]) + w[t-16]) & MASK)
    a, b, c, d, e, f, g, hh = h
    aa = [d, c, b, a]
    ee = [hh, g, f, e]
    for t in range(31):
        p = (hh + big1(e) + choose(e, f, g) + K[t] + w[t]) & MASK
        q = (big0(a) + majority(a, b, c)) & MASK
        a, b, c, d, e, f, g, hh = (p+q)&MASK, a, b, c, (d+p)&MASK, e, f, g
        aa.append(a)
        ee.append(e)
    return tuple((x+y)&MASK for x,y in zip(h,(a,b,c,d,e,f,g,hh))),aa,ee,w

def inverse_small1(y):
    rows = []
    for bit in range(32):
        row = sum(((small1(1 << j) >> bit) & 1) << j for j in range(32))
        rows.append([row, 1 << bit])
    for col in range(32):
        pivot = next(j for j in range(col,32) if (rows[j][0] >> col) & 1)
        rows[col],rows[pivot] = rows[pivot],rows[col]
        for j in range(32):
            if j != col and ((rows[j][0] >> col) & 1):
                rows[j][0] ^= rows[col][0]
                rows[j][1] ^= rows[col][1]
    out = 0
    for col in range(32):
        out |= ((rows[col][1] & y).bit_count() & 1) << col
    assert small1(out) == y
    return out
```

### D.2 Inverse state and capped completion helpers

SHA-256: `f49b6a5ae200fb4ec1ed682586a09be07a33145da4e430ef98787f28360ef04d`. Original scratch paths in this source designate the
inputs described above.

```python
"""Minimal literal-trail SHA-256/31 collision completion; no legacy pair inputs."""
from r31_sha31_core_literal import (IV,K,MASK,big0,big1,choose,compress,inverse_small1,majority,small0,small1)

DELTAS = {5:0xfffff006, 6:0x002087f1, 7:0x4fefb5fa, 8:0x28011100, 9:0x00008004}

D16 = 0x00008004

D18 = 0xFFFF7FFC

X18 = 0x2FFE7FE0

G16 = [(hi << 28) | lo for hi in range(16) for lo in
       (0x031BBFFC, 0x064BBFFE, 0x09B3BFFD, 0x0CE3BFFF)]

INV_BASIS = [inverse_small1(1 << j) for j in range(32)]

def inv(y):
    out = 0
    while y:
        low = y & -y
        out ^= INV_BASIS[low.bit_length() - 1]
        y -= low
    return out

def build_start(a, b, W7, W8, W5, W6):
    """Reconstruct a selected F6/F7-compatible backward tuple."""
    A = {i: a[i - 1] for i in range(1, 13)}
    E = {i: a[i + 7] for i in range(5, 13)}
    AP = {i: b[i - 1] for i in range(1, 13)}
    EP = {i: b[i + 7] for i in range(5, 13)}
    E[4] = (E[8] - A[4] - big1(E[7]) - choose(E[7], E[6], E[5]) - K[8] - W8) & MASK
    EP[4] = (EP[8] - AP[4] - big1(EP[7]) - choose(EP[7], EP[6], EP[5]) - K[8]
             - W8 - DELTAS[8]) & MASK
    if E[4] != EP[4]:
        return None
    A[0] = (E[4] - A[4] + big0(A[3]) + majority(A[3], A[2], A[1])) & MASK
    AP[0] = (EP[4] - AP[4] + big0(AP[3]) + majority(AP[3], AP[2], AP[1])) & MASK
    E[3] = (E[7] - A[3] - big1(E[6]) - choose(E[6], E[5], E[4]) - K[7] - W7) & MASK
    EP[3] = (EP[7] - AP[3] - big1(EP[6]) - choose(EP[6], EP[5], EP[4]) - K[7]
             - W7 - DELTAS[7]) & MASK
    if E[3] != EP[3] or A[0] != AP[0]:
        return None
    A[-1] = (E[3] - A[3] + big0(A[2]) + majority(A[2], A[1], A[0])) & MASK
    AP[-1] = (EP[3] - AP[3] + big0(AP[2]) + majority(AP[2], AP[1], AP[0])) & MASK
    if A[-1] != AP[-1]:
        return None
    E[2] = (E[6] - A[2] - big1(E[5]) - choose(E[5], E[4], E[3])
            - K[6] - W6) & MASK
    A[-2] = (E[2] + big0(A[1]) + majority(A[1], A[0], A[-1]) - A[2]) & MASK
    E[1] = (E[5] - A[1] - big1(E[4]) - choose(E[4], E[3], E[2])
            - K[5] - W5) & MASK
    A[-3] = (E[1] + big0(A[0]) + majority(A[0], A[-1], A[-2]) - A[1]) & MASK
    # Check the second lane's backward constraints using shared A_-2,A_-3,E3,E4.
    e2p = (EP[6] - AP[2] - big1(EP[5]) - choose(EP[5], EP[4], EP[3])
           - K[6] - ((W6 + DELTAS[6]) & MASK)) & MASK
    a_minus2_p = (e2p + big0(AP[1]) + majority(AP[1], AP[0], AP[-1]) - AP[2]) & MASK
    e1p = (EP[5] - AP[1] - big1(EP[4]) - choose(EP[4], EP[3], e2p)
           - K[5] - ((W5 + DELTAS[5]) & MASK)) & MASK
    a_minus3_p = (e1p + big0(AP[0]) + majority(AP[0], AP[-1], a_minus2_p) - AP[1]) & MASK
    if (A[-2], A[-3]) != (a_minus2_p, a_minus3_p):
        return None
    for i in range(9, 13):
        A[i], E[i] = a[i - 1], a[i + 7]
    return A, E, AP, EP, a[20:24], [W5, W6, W7, W8]

def good_words(w):
    c16 = (w[9] + small0(w[1]) + w[0]) & MASK
    c18 = (w[11] + small0(w[3]) + w[2]) & MASK
    good = []
    for g in G16:
        u = (small1(g) + c18) & MASK
        if (small1((u + D18) & MASK) - small1(u)) & MASK == X18:
            good.append((g, inv((g-c16)&MASK)))
    return good

def complete(start, good, rng):
    A,E,AP,EP,_,_ = start
    da10 = (AP[10] - A[10]) & MASK
    b13 = (A[9] + E[9] + big1(E[12]) + choose(E[12],E[11],E[10]) + K[13]) & MASK
    k14 = (A[10] + E[10] + K[14]) & MASK
    k14p = (AP[10] + EP[10] + K[14]) & MASK
    m14,m14p = E[12]^E[11],EP[12]^EP[11]
    used = 0
    for g,w14 in good:
        if used >= 65536: break
        r13,r15 = rng.getrandbits(32),rng.getrandbits(32)
        base,basep = (k14+w14)&MASK,(k14p+w14)&MASK
        for i in range(1<<18):
            if used >= 65536: break
            used += 1
            x = (r13 + i*0x9E3779B9)&MASK
            c = E[11] ^ (x&m14)
            cp = EP[11] ^ (x&m14p)
            if (basep+cp-base-c)&MASK != da10: continue
            sx=big1(x)
            y,yp=(base+sx+c)&MASK,(basep+sx+cp)&MASK
            x15=(E[11]+big1(y)+choose(y,x,E[12]))&MASK
            if x15!=(EP[11]+big1(yp)+choose(yp,x,EP[12]))&MASK: continue
            for j in range(1<<12):
                if used >= 65536: break
                used += 1
                z=(r15+j*0x9E3779B9)&MASK
                y16=(E[12]+choose(z,y,x))&MASK
                if y16!=(EP[12]+choose(z,yp,x)+D16)&MASK: continue
                e16=(A[12]+y16+big1(z)+K[16]+g)&MASK
                if choose(e16,z,y)!=choose(e16,z,yp): continue
                return ((x-b13)&MASK,w14,(z-A[11]-x15-K[15])&MASK),used
    return None,used
```

### D.3 Fixed-seed completion runner

SHA-256: `79b056dc2de32b8a90ec4d0afcda264e6a7dcea474b33ac1bf7d1d75138f1451`. Original scratch paths in this source designate the
inputs described above.

```python
"""Deterministic capped Phase3 completion for each fixed-seed JOINT prefix.

Counter-domain-separated ChaCha20 offsets were fixed in the prospective
protocol before the 2^35-block sampler was launched. No OS randomness is used.
"""
import hashlib,json,re,struct,sys
from pathlib import Path
from r31_h2_completion_literal_min import build_start,good_words,complete
from r31_sha31_core_literal import K,IV,MASK,big0,big1,choose,majority,compress,small0
sys.path.insert(0,str(Path.cwd()))
from verifier.hash_functions import digest,_compress

PRNG_KEY=bytes.fromhex('6af5170aa5223b656b9b8e8267b49a5bc7a9efa543d14360207ff63f292dab5f')
PRNG_NONCE=0x726f756e64333121
MASK32=(1<<32)-1
def rol32(x,n): return ((x<<n)|(x>>(32-n)))&MASK32
def chacha20_block(counter):
    s=list(struct.unpack('<4I',b'expand 32-byte k'))+list(struct.unpack('<8I',PRNG_KEY))
    s.extend((counter&MASK32,counter>>32,PRNG_NONCE&MASK32,PRNG_NONCE>>32))
    x=s.copy()
    def qr(a,b,c,d):
        x[a]=(x[a]+x[b])&MASK32;x[d]=rol32(x[d]^x[a],16)
        x[c]=(x[c]+x[d])&MASK32;x[b]=rol32(x[b]^x[c],12)
        x[a]=(x[a]+x[b])&MASK32;x[d]=rol32(x[d]^x[a],8)
        x[c]=(x[c]+x[d])&MASK32;x[b]=rol32(x[b]^x[c],7)
    for _ in range(10):
        for t in ((0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),
                  (0,5,10,15),(1,6,11,12),(2,7,8,13),(3,4,9,14)):
            qr(*t)
    return struct.pack('<16I',*((a+b)&MASK32 for a,b in zip(x,s)))

class OffsetTape:
    def __init__(self,pairs):
        self.pairs=pairs;self.words=[];self.used=0
        for pair in pairs:
            raw=bytes.fromhex(pair);assert len(raw)==8
            self.words.extend((int.from_bytes(raw[:4],'big'),int.from_bytes(raw[4:],'big')))
    def getrandbits(self,n):
        assert n==32 and self.used<len(self.words)
        v=self.words[self.used];self.used+=1;return v

assert len(sys.argv)==2
log_path=Path(sys.argv[1])
line_re=re.compile(r'^JOINT slot=(\d+) key=([0-9a-f]{8}) point=(\d+) v8_index=(\d+) v7_index=(\d+) w6=([0-9a-f]{8}) w5=([0-9a-f]{8}) c18=([0-9a-f]{8}) cv=((?:[0-9a-f]{8} ?){8}) block=([0-9a-f]{128})$')
all_lines=log_path.read_text().splitlines()
events=[]
for index,line in enumerate(all_lines):
    if not line.startswith('JOINT '): continue
    assert index and all_lines[index-1].startswith('COUNTER value=')
    counter=int(all_lines[index-1].split('=',1)[1])
    assert 0<=counter<(1<<35)
    events.append((counter,line))
events.sort()
assert events and len({counter for counter,_ in events})==len(events)
outdir=Path('/tmp/r31_fixedseed_hygiene_portable_results')
outdir.mkdir(exist_ok=True)
points=Path('/tmp/r31_publicmask_fibers56/final_clean_union.bin').read_bytes()
v7_bytes=Path('/tmp/r31_v7.bin').read_bytes()
v8_bytes=Path('/tmp/r31_v8.bin').read_bytes()
out=[]
for index,(counter,line) in enumerate(events):
    m=line_re.match(line);assert m,line
    slot=int(m[1]);key=int(m[2],16)
    pi,j,k=map(int,(m[3],m[4],m[5]))
    W6=int(m[6],16);W5=int(m[7],16);c18=int(m[8],16)
    cv=tuple(int(s,16) for s in m[9].split());block=bytes.fromhex(m[10])
    assert chacha20_block(counter)==block
    row=struct.unpack_from('<48I',points,192*pi)
    W7=struct.unpack_from('<I',v7_bytes,4*k)[0]
    W8=struct.unpack_from('<I',v8_bytes,4*j)[0]
    start=build_start(list(row[:24]),list(row[24:]),W7,W8,W5,W6)
    assert start is not None and start[0][-1]==key
    A,E,AP,EP,W912,W5678=start
    A[-4]=cv[3]
    for t in range(-4,0):E[t]=cv[3-t]
    E[0]=(A[0]+A[-4]-big0(A[-1])-majority(A[-1],A[-2],A[-3]))&MASK
    w=[0]*16
    for t in range(5):
        w[t]=(E[t]-A[t-4]-E[t-4]-big1(E[t-1])
              -choose(E[t-1],E[t-2],E[t-3])-K[t])&MASK
    w[5:9]=W5678;w[9:13]=W912
    wp=w.copy()
    for t,d in {5:0xfffff006,6:0x002087f1,7:0x4fefb5fa,8:0x28011100,9:0x00008004}.items():
        wp[t]=(wp[t]+d)&MASK
    assert w[5]==W5 and w[6]==W6
    assert (w[11]+small0(w[3])+w[2])&MASK==c18
    assert tuple(_compress('sha256',tuple(IV),block,31))==cv
    assert compress(tuple(IV),list(struct.unpack('>16I',block)))[0]==cv
    good=good_words(w)
    assert good
    assert len(good)<=64
    offset_pairs=[chacha20_block((1<<48)+64*counter+j)[:8].hex()
                  for j in range(len(good))]
    tape=OffsetTape(offset_pairs)
    found,used=complete(start,good,tape)
    assert tape.used%2==0
    record={'event_index':index,'prng_counter':counter,'source_log':str(log_path),'selected_slot':slot,
            'key':f'{key:08x}','point_index':pi,'v8_index':j,'v7_index':k,
            'W5':f'{W5:08x}','W6':f'{W6:08x}','c18':f'{c18:08x}',
            'good_g16_count':len(good),'first_block_hex':block.hex(),
            'first_cv':[f'{x:08x}' for x in cv],
            'phase3_offset_source':'domain-separated fixed-key ChaCha20 at 2^48+64*counter+j',
            'phase3_offset_pairs_hex':offset_pairs,
            'phase3_offset_pairs_consumed':tape.used//2,
            'phase3_counted_iterations':used,
            'phase3_success':found is not None}
    if found is not None:
        w[13:16]=found;wp[13:16]=found
        second_a=struct.pack('>16I',*w);second_b=struct.pack('>16I',*wp)
        msg_a=block+second_a;msg_b=block+second_b
        assert msg_a!=msg_b and len(msg_a)==len(msg_b)==128
        cv2a=compress(cv,w)[0];cv2b=compress(cv,wp)[0]
        assert cv2a==cv2b
        dig_a=digest(msg_a,'sha256',31);dig_b=digest(msg_b,'sha256',31)
        assert dig_a==dig_b
        record.update({'second_cv':[f'{x:08x}' for x in cv2a],
                       'digest_hex':dig_a.hex(),
                       'message_a_hex':msg_a.hex(),'message_b_hex':msg_b.hex(),
                       'independent_verifier_digest_equal':True})
    item_path=outdir/f'joint_counter_{counter:012d}.json'
    item_path.write_text(json.dumps(record,indent=2)+'\n')
    record['individual_result_path']=str(item_path)
    record['individual_result_sha256']=hashlib.sha256(item_path.read_bytes()).hexdigest()
    out.append(record)
    print(json.dumps({k:record[k] for k in ('event_index','key','phase3_success',
                                             'phase3_counted_iterations','good_g16_count')},sort_keys=True),flush=True)
summary={'source_log':str(log_path),'source_sha256':hashlib.sha256(log_path.read_bytes()).hexdigest(),
         'JOINT_events':len(events),'Phase3_calls':len(out),
         'Phase3_successes':sum(r['phase3_success'] for r in out),
         'Phase3_failures':sum(not r['phase3_success'] for r in out),
         'Phase3_total_counted_iterations':sum(r['phase3_counted_iterations'] for r in out),
         'events':out}
path=outdir/'joint_completions.json'
path.write_text(json.dumps(summary,indent=2)+'\n')
print('summary',json.dumps({k:v for k,v in summary.items() if k!='events'},sort_keys=True),flush=True)
print('summary_path',path,'sha256',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
```

### D.4 Completed fixed-IV pairs

The rows below are in ascending first-block counter order, with one capped
completion attempt per JOINT. Each digest is the full 256-bit output after
the common first block, differing second blocks and final padding block.
The two message files for each row are declared in the manifest. The hygiene
sampler and portable completion pass reproduced these exact records.

| Pair | Counter | Selected slot | Key | Row | V8 index | V7 index | Phase-3 iterations | Full digest |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| fixedseed-1 | 3,657,090,739 | 4 | `094c88ed` | 2966 | 17361 | 367 | 603 | `38bfee3b3697ce5531983a3f306d29166f089a4f55858605aa674354d0348e75` |
| fixedseed-2 | 3,730,573,566 | 5 | `795fa8c6` | 4057 | 11085 | 415 | 6019 | `2032408e18b540953192dedc1119a1ea6e70a474bfc37ac58a792ab814f85bee` |
| fixedseed-3 | 19,220,456,670 | 3 | `3b398263` | 9920 | 1340 | 205 | 4135 | `0be0b2d41db6b6a72b02ec536cb932347e200ca197b6215722bad2f747a5c646` |
| fixedseed-4 | 23,769,127,359 | 6 | `8d81a61b` | 19386 | 34794 | 116 | 2392 | `dfa2040d9e436bc412f00829d204c9006c23bc12fb860f5c223f2e37fb9bfc32` |
| fixedseed-5 | 24,812,210,494 | 3 | `b449c013` | 20858 | 3776 | 205 | 4517 | `86c968da89768279b585e87272d237793149c39640def6b2870c308096d3dbd6` |
| fixedseed-6 | 27,048,001,964 | 0 | `beaf20a4` | 9976 | 209 | 308 | 175 | `68fa707d79da9e54115a7febde3c90b0b042ec8c3260dfd05d80be9f96870a46` |
| fixedseed-7 | 30,930,496,763 | 7 | `d3410f31` | 24765 | 28690 | 359 | 185 | `dcb3b8bc1a79302a3ad18365e9690ad5dc2fab1a68d4e4e09f40f23bb9507a43` |
