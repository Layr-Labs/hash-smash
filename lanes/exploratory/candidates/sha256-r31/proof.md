# Recombined-state, eight-representative fresh-run search for 31-step SHA-256

Track `sha256-r31-exploratory`; target `sha256-r31-prefix-v1`; cost model `collision-frontier-v5`, with 2140 primitive word operations per charged target compression. The submitted bound is `time_log2=40.52`, `preprocessing_log2=40.51`, `memory_log2_bytes=40`, and `nonuniform_advice_log2_bytes=17`. Its algorithmic success probability exceeds 0.39 **conditional** on H1, H2, and H3 below. The numerical upper bound is `2^40.519643` compression units. H1/H2 are rare-event distribution/completion premises; H3 is an unmetered bound on all inherited advice generation and development/verification work charged as preprocessing. This is an exploratory claim, not a mathematical proof or a full 64-step SHA-256 attack.

The 400 paired source states and eight full-message certificates are attributed to `@Akashneelesh`'s unpromoted, rejected 40.46 submission; their construction work is charged under H3, and their earlier tuple-count and work claims are **not** adopted. We transform those states algebraically, validate every generated state, and retain up to eight deterministic tuples per distinct 32-bit key. A full-domain low-bit overlap certificate gives a rigorous uniform-state prefix lower bound without assuming tuple independence. The source trail and practical collision are due to Li, Liu, Wang, Dong and Sun. The in-review 40.76 replay submission is not treated as an accepted baseline.

## 1. Exact target, variables, and differential conditions

The complete message starts from the standard SHA-256 IV once. Each block inherits its input chaining state, uses the original constants and schedule, executes round indices 0 through 30 inclusive, and adds all eight input words as feed-forward. Both output messages are distinct 128-byte strings `M0 || M1` and `M0 || M1'` sharing their 64-byte first block; second-block differences occur only in W5..W9. FIPS padding adds the same third block to both. The entire fixed-IV, three-block hash is independently checked before a pair is returned. No chosen-IV or compression-only result is counted as a full-message collision.

All equations are modulo `2^32`. Let `s0(x)=ROTR7(x) xor ROTR18(x) xor (x>>3)`, `s1(x)=ROTR17(x) xor ROTR19(x) xor (x>>10)`, `S0(x)=ROTR2(x) xor ROTR13(x) xor ROTR22(x)`, and `S1(x)=ROTR6(x) xor ROTR11(x) xor ROTR25(x)`. Also `Ch(x,y,z)=z xor (x and (y xor z))` and `Maj(x,y,z)=(x and y) xor (x and z) xor (y and z)`. The standard schedule is `W[t]=W[t-16]+s0(W[t-15])+W[t-7]+s1(W[t-2])` for 16≤t≤30.

Write the first-block chaining value as `CV=(A_-1,A_-2,A_-3,A_-4,E_-1,E_-2,E_-3,E_-4)` in inverse SHA-256 state notation. A paired point consists of lanes a,b, each in the 24-word order `A1..A12 E5..E12 W9..W12`; Appendix A supplies 400 paired input points. The required second-block word differences `W'_t-W_t` are

```text
d5=fffff006  d6=002087f1  d7=4fefb5fa  d8=28011100  d9=00008004
d16=00008004 d18=ffff7ffc x18=2ffe7fe0
c5=d0018020  c6=00000ffa  c7=ffdf780f  c8=b00fca02.
```

Define `Vj={w:s0(w+dj)-s0(w)=cj}` for j=5..8, `V9={w:s0(w+d9)-s0(w)=-d8}`, `G16={w:s1(w+d16)-s1(w)=d18}`, `G18={w:s1(w+d18)-s1(w)=x18}`, and `S={c:∃g∈G16, s1(g)+c∈G18}`. Exhaustive 32-bit enumeration yields `|V5|=16,384`, `|V6|=8,388,608`, `|V7|=512`, `|V8|=49,408`, `|G16|=64`, `|G18|=42,467,328`, and `|S|=584,683,520`. The V8 test is the full modular derivative; only 8,192 of its 49,408 values satisfy the older extra signed W8 mask. The schedule differences cancel at W20..W25 as `x18+c5=0`, `c6+d5=0`, `c7+d6=0`, `d16+c8+d7=0`, `-d8+d8=0`, and `d18+d9=0`; W26..W30 then agree.

## 2. Recombine the 400 source states

For each source point, hold A5..A12 and E9..E12 of both lanes fixed. Replace the four paired E5..E8 words with **every** pair allowed by their published signed conditions *and* the source pair's modular E difference. The four finite pair sets have sizes 2, 128, 4, and 128; this tests 131,072 combinations per source point, or 52,428,800 overall. A signed condition has 32 characters from high bit to low: `=` means equal bits, `0` means both zero, `1` means both one, `u` means (0,1), and `n` means (1,0). Appendix B includes their literal patterns and generator.

For each lane, calculate A4,A3,A2,A1 in that order by the exact SHA-256 identity

```text
A[t-4] = E[t]-A[t]+S0(A[t-1])+Maj(A[t-1],A[t-2],A[t-3]), t=8,7,6,5.
```

Derive W9..W12 by the E-round recurrence `W[t]=E[t]-A[t-4]-E[t-4]-S1(E[t-1])-Ch(E[t-1],E[t-2],E[t-3])-K[t]`. Keep a generated pair only when A1..A4 agree across lanes, W9 has exactly difference d9 and its signed mask, W10..W12 agree, W9 satisfies V9, and the two step-8 inverse equations give a common E4:

```text
F8: [E8'-A4'-S1(E7')-Ch(E7',E6',E5')]
   -[E8 -A4 -S1(E7 )-Ch(E7 ,E6 ,E5 )] = d8.
```

Sort the 48-word rows by their little-endian byte encoding, remove duplicates, and assign indices 0..64,799. This yields exactly **64,800 distinct F8-valid generated points**. Independent exhaustive checks on all 64,800 verified the published A/E/W signed masks, common A1..A4, both lanes' A-minus-E identities at t=5..12, W9..W12 E recurrences, V9, and the step-13 P4 equality. All 400 original source points appear verbatim among the eventual active points. This is an algebraic recombination of fixed advice, not a claim that arbitrary early A words can be mutated.

## 3. Enumerate tuples and retain the first eight per key


For each generated point in bytewise order, scan V8 and V7 in increasing unsigned order. Given a W8 in V8, solve `E4=E8-A4-S1(E7)-Ch(E7,E6,E5)-K8-W8`; F8 makes E4 common. Keep W8 only if the step-7 inverse equation gives the **same E3** in both lanes for W7 differing by d7:

```text
Ch(E6',E5',E4)-Ch(E6,E5,E4)
  = (E7'-E7)-(S1(E6')-S1(E6))-d7.                     (F7)
```

Given W7 in V7, solve `E3=E7-A3-S1(E6)-Ch(E6,E5,E4)-K7-W7`; keep it only if the step-6 inverse equation gives the **same E2** in both lanes for W6 differing by d6:

```text
Ch(E5',E4,E3)-Ch(E5,E4,E3)
  = (E6'-E6)-(S1(E5')-S1(E5))-d6.                     (F6)
```

The generator explicitly checks common E2 (zero tuples fail); step 5 then gives common E1 for W5 differing by d5, because A1,E4,E3,E2 are shared and every generated point has `E5'-E5=d5`. Compute `A0=E4-A4+S0(A3)+Maj(A3,A2,A1)` and `key=A_-1=E3-A3+S0(A2)+Maj(A2,A1,A0)`. A direct-address slot indexed by the 32-bit key points to a compact group. Store the first **up to eight** valid tuples in the fixed point/W8/W7 order; discard later tuples for that key. This table rule depends only on fixed source advice, never on an online CV. Full enumeration gives **409,618,384 F7-passing W8 cases, 755,416,216 F6/F5 tuples from 30,540 active points, and K=195,265,888 distinct keys**. It retains **M=641,616,343** tuple records. Group histogram for sizes one through eight is `43,868,559; 63,634,538; 9,728,941; 39,655,796; 2,246,421; 8,280,176; 1,056,116; 26,795,341`. Independent full-table key bitmaps agree byte-for-byte, SHA-256 `b5031aaccb00257ab7285864ae17d21af1f65f017b94d4b74185e2056d936917`.

The online direct-address array has `2^32` 32-bit slots (16 GiB). Each used slot indexes a 136-byte group holding key, count and eight 16-byte `(point,W7,W8,C6)` records. Reserve at most 200 million groups (27.2 GB), above the observed K=195,265,888; the actual groups occupy 26.56 GB. In a separate companion array, precompute up to five additional 32-bit inverse constants per retained tuple (at most 12.84 GB) under setup. Together with the slots, generated rows, derivative sets and scratch, explicit peak is below `2^36` bytes. The finite builder stops if a count or allocation cap is exceeded. No key-group truncation or tuple-independence assumption enters the prefix lower bound.

### Full-domain low-16-bit overlap certificate

For each tuple i, write `x=A_-2`, `y=A_-3`, `W6_i=C6_i-x`, and `W5_i=C5_i(x)-y`. Exhaustive V5/V6 enumeration finds 512 supported V5 low-16 residues, each with exactly 32 full-word lifts, and 2048 supported V6 low-16 residues, each with exactly 4096 lifts. Thus every tuple accepts exactly `|V6|*|V5|=2^37` `(x,y)` pairs. A separate full-domain verifier recomputes these multiplicities.

For two same-key tuples i,j, inspect the V6 low-16 residues shared by `C6_i-x` and `C6_j-x`. For every accepted low-16 value `x16`, calculate `delta16=C5_j(x16)-C5_i(x16) mod 2^16` and let `corr5(delta16)` count V5 low-16 residues r for which both r and `r+delta16` are supported. The low 16 bits of C5 depend only on the low 16 bits of x: its x-dependent operations are modular addition, Ch and Maj. Each projected `(x16,y16)` pair lifts to at most `4096*32=2^17` full `(x,y)` pairs in either tuple. Hence the pair intersection is at most `b_ij*2^37`, where

```text
b_ij = min(2^20, sum_{shared x16} corr5(delta16))/2^20.
```

These b values are **upper** overlap bounds. For a fixed key group with m≤8 tuples in online order, define `B_1=1` and increment `B_z=B_(z-1)+max(0,1-sum_{i<z} b_(i,z))` for z=2..m. The union gained by tuple z is at least its full mass less the sum of intersections with **all previous** tuples, so B_m is a valid lower bound even when that sum exceeds one. This sequential certificate does not choose tuples for the attack; online tests all first-eight records. The complete 195,265,888-key scan gives integer numerator **649,493,203,868,568/2^20**, or **L=619,404,987.209861755 tuple equivalents**. It evaluates 1,249,588,536 pair bounds over 1,799,034,803,537 inner shared-residue iterations and checks zero common-E2 rejects. A second independently implemented full all-previous scan reproduces the exact numerator, tuple counts and group histogram. A third certificate that greedily uses a subset gives the stronger valid numerator 649,527,829,603,725/2^20; the claim uses the smaller all-previous value. All three complete scans reproduce K, M, the group histogram and the raw tuple counts. Appendix B prints their sources and the exact support verifier.

## 4. Online search, uniform-state lower bound, and completion

Each of `N=9,800,000,000` trials draws two fresh independent uniform 256-bit RAM words, concatenates them into one 512-bit first block M0, and computes its exact fixed-IV 31-step CV. For a key hit, inspect the eight retained tuples in order, selecting the **first** whose W6 and W5 tests pass. For a tuple and `x=A_-2`, `y=A_-3`, reconstruct E2,W6 then E1,W5:

```text
E2=A2+x-S0(A1)-Maj(A1,A0,key)
W6=E6-A2-E2-S1(E5)-Ch(E5,E4,E3)-K6
E1=A1+y-S0(A0)-Maj(A0,key,x)
W5=E5-A1-E1-S1(E4)-Ch(E4,E3,E2)-K5.
```

The paired W5..W8 differences follow from F8/F7/F6/F5 and the retained point. Solve the earlier E and W0..W4 equations backward from CV; W9..W12 are in the point. Define `c16=W9+s0(W1)+W0` and `c18=W11+s0(W3)+W2`. Skip completion if `c18∉S`. The first-match rule depends on the online CV's A triple but **not** on its E_-2 word.

For each `g∈G16` satisfying `s1(g)+c18∈G18`, set `W16=g`, solve `W14=s1^{-1}(g-c16)`, then use fresh independent offsets and Weyl increments to search E13=x and E15=z. The inner test enforces C14 (`E14'-E14=d16`), C15 (`E15'=E15`), C16 (`E16'=E16`), and C17 (`Ch(E16,z,E14')=Ch(E16,z,E14)`), then solves W13/W15. Local maxima are `CAP13=2^18`, `CAP15=2^12`; a **single global cap of 2^16 total x- and z-candidate iterations per call** covers all g values. Phase 3 is invoked at most once per trial. The algorithm independently rehashes both distinct complete 128-byte outputs, including FIPS padding, from the fixed IV before success.

The run stops with FAIL at global caps `Q_key=2^31` key-hit trials and `Q_prefix=2^14` prefix-valid selected trials, or after N trials. Failed trials, skipped completions, invalid pairs and cap-triggered stops are charged. Different keys are disjoint, and the within-key union is bounded by the full certificate, so for a uniform 256-bit CV U,

```text
Pr_U(prefix) >= L/2^59 = 1.0744963724500611e-9.
Pr_U(prefix) <= M/2^59 = 641,616,343/2^59.
```

For a fixed A triple and its first passing tuple, A_-4 and E_-1, the inverse A equations fix E0,E1,E2. W3 depends on E_-1 but not E_-2, whereas `W2=E2-A_-2-E_-2-S1(E1)-Ch(E1,E0,E_-1)-K2`. Hence c18 is an affine bijection of the free uniform E_-2, and first-match selection does not bias it. The exact U conditional c18 fraction is `|S|/2^32=584,683,520/2^32`, giving a rigorous U joint lower bound

```text
Pr_U(prefix and c18∈S) >= (L/2^59)*(584,683,520/2^32)
                          = 1.4627359837091825e-10.
```

H1 posits that the **real fixed-IV joint event** has probability at least 0.4 times this U lower bound, while real key-hit and prefix probabilities are at most 4 times `K/2^32` and `2^10` times `M/2^59`, respectively. H2 posits at least 0.9 capped Phase-3 completion under the **real conditional first-match-of-eight** distribution with fresh Phase-3 coins. Neither follows from uniform-state counting. Fresh first blocks give independent Bernoulli trials; the per-trial winning lower bound is `q=0.4*0.9*1.4627359837091825e-10=5.265849541353058e-11`, and `1-(1-q)^N=0.4031283946`. At H2=0.9, success 0.39 would require H1≈0.38314; at H1=0.4, it would require H2≈0.86206.

Under H1's upper factors, means over N trials are at most 1,782,184,189.558 key hits and 11,169.448 prefix-valid trials. Binomial Chernoff bounds put exceeding Q_key below `2^-50,658,883` and Q_prefix below `2^-1,532`. A cap can remove success only on those rare events, so capped success remains greater than 0.40312, above 0.39. This is conditional algorithmic probability, not a reviewer-confidence score.

## 5. All-work v5 ledger and memory

The cost model charges one unit per selected-round target compression and 1/2140 per other 256-bit word primitive, including random words, loads/stores, arithmetic, branches and checks. Charge **128 primitives on every first-block trial**, beyond its compression, for two independent random draws, slot lookup, state extraction and counters. Charge **16+8×256 additional primitives on every key-hit trial** for group access, worst-case eight tuple reconstructions, V6/V5 bitmap tests and precomputed inverse constants; earlier matches only reduce work. Charge `2^14` full units for **every prefix-valid trial**, including c18 skips and unsuccessful completion. The Phase-3 cap costs at most `(2^16*512+2^18)/2140+6=15,808.14<2^14` units: at most 512 primitives per candidate iteration, `2^18` fixed primitives for G16 search, inversion, reconstruction, random seeds, assembly and control, plus six full compressions for independent three-block rehashes.

We charge a separate **`2^33`-unit finite setup cap** for derivative enumeration, recombination, tuple generation, retaining the first eight per key, bitsets and serialization. The builder aborts if E-pair set sizes differ from (2,128,4,128), generated rows exceed `2^17`, F7-passing W8 cases exceed `2^29`, F6-passing W7 tuples exceed `2^30`, retained records exceed `2^30`, key groups exceed 200 million, or `|G18|` exceeds `2^26`. The fixed advice has respectively 64,800 rows, 409,618,384 F7 cases, 755,416,216 F6 tuples, 641,616,343 retained records, 195,265,888 groups and 42,467,328 G18 words, so guards do not fire. The hard word-operation ledger charges 400×131,072×2,048 E combinations; 6×`2^32`×128 derivative scans; `2^17`×49,408×256 W8 probes; `2^29`×512×32 W7 tests; `2^30`×256 F6-passing tuple handling; 64×`2^26`×64 S joins; `2^32`×32 direct slots; `2^30`×1024 representative records/inverse constants; plus `2^41` for parsing, sorting, bitsets, writes, checks and remaining setup. Total **17,845,589,114,880 primitives /2140 = 8,339,060,334.056 v5 units**, below `2^33=8,589,934,592`. The rejected-W7 32-primitive charge covers load, subtraction, two three-operation Ch functions, compare/branch, loop control and spare index operations; accepted F6 tuples receive a separate 256-primitive charge. Full overlap certificates and independent rebuilds are validation, not table selection; the charged construction is one deterministic pass.

H3 is a separate **unmeasured `2^40.5`-unit bound** on all historical computation creating the characteristic, 400 source points and eight inherited certificates, including failed/abandoned SAT/SMT searches, mathematical overlap-certificate verification, auxiliary experiments, validation and serialization. Public self-reports give 58,015 CPU-seconds for 24 unfinished characteristic-search calls and 8,769.7 CPU-seconds for selected compatible-point solving, without complete logs or the K400 solver model. At an **assumed, unvalidated** `2^23` v5 units per CPU-second, those 66,784.7 seconds (if disjoint) are below the H3 allowance of about 185,364 seconds. The first full low-16 certificate logged 1,799,034,803,537 inner residue iterations and 1,249,588,536 pair calls; pricing these generously at 256 primitives per residue and 4096 per pair would charge about 217.60 billion v5 units. Three similarly sized full scans would be about 652.81 billion. Together with the conditional 560.23-billion-unit conversion of those partial CPU reports and the bounded 47.39-billion-unit first-slot campaign and 33.62-billion-unit first-eight campaign, that illustrative subtotal is 1.294 trillion, below H3=1.555 trillion; missing historical work could consume the remainder. H3 covers certificate scans and validation if charged as development, plus ninth- and tenth-witness production if classified as extra nonuniform advice. These reports and the new experiment are partial evidence, **not** a measured all-history cap. If all-history work exceeds H3 or the conversion is too low, the scalar claim fails. H3 at `2^40.7` with other terms fixed would score about 40.71711; at `2^40.72` it would score about 40.73688.

The total hard work bound **conditional on H3** is

```text
T <= 9,800,000,000*(1+128/2140)
   + 2^31*(16+8*256)/2140
   + 2^14*2^14
   + 2^33 + 2^40.5
   = 1,576,260,012,133.622 < 2^40.52.
```

All work is summed across processors; no cross-target amortization is used. Preprocessing is `2^40.5+2^33=2^40.507948` units, below `2^40.51`. The 400 source pairs occupy 76,800 bytes; characteristic, constants, ten certificates and related advice remain below `2^17` bytes. The explicit group table, direct slots and precomputed constants fit under `2^36` bytes. Declared peak `2^40` bytes also covers H4, a supporting **unmeasured** historical solver/allocator/thread peak bound; a partial report gave 5.8 GB without an all-history RSS receipt. Memory is reviewed but has no v5 scalar contribution.

## 6. Reproduction, experimental scope, and open obligations

Appendix A prints all 800 attributed 24-word source rows. Appendix B includes signed-pair, derivative-set, recombination, two independent full first-eight low-16-bit sequential certificates, a stronger subset certificate, key-count and support-verification source. The E-pair file has sizes (2,128,4,128), SHA-256 `4d0218a189ae8a1c2f0cbe828f90a9fc3ecf8a84c13d62db17c38b1eb527f6f6`; generated rows hash to `85a2542618f9592845c79de787fffb89d4b4716c189e0e2afec885da790e9d44` and active rows to `3a7ec9aef7635a75030f52de90454c00551f1d839a8d7c5496a05bcead82e7ff`. Full C enumerations agree on all 64,800 rows, 755,416,216 tuples, 195,265,888 keys and the byte-identical 512 MiB key bitmap. The conservative certificate gives M=641,616,343 and L numerator 649,493,203,868,568/2^20; a second implementation reproduces the exact sequential numerator and a third subset certificate is slightly stronger. A separate row audit checked all generated A/E/W masks and recurrences; 48,094 sampled first-key tuples passed independent backward reconstruction, and 200 active rows passed full synthetic-CV forward two-lane compressor equality.

For H2, a deterministic hash-of-key 1-in-4096 sample contains 48,094 key groups. An exact synthetic uniform-CV-on-union sampler proposes a key, one of its first eight tuple slots, W5 uniformly from V5 and W6 uniformly from V6, then rejects vacancy and uses inverse-multiplicity weighting for CVs accepted by several tuples. It screens c18 for the actual first-matching tuple, draws the remaining CV words, runs capped completion and independently checks full two-lane 31-step compressor equality and W20..W30 cancellation. With fixed seed `0xF041F0A`, **1,000/1,000** c18-screened cases completed under the 65,536 iteration cap, covering selected slots 0..7 in counts 306/218/141/125/50/61/47/52 across 958 generated points from 253 source origins. Median/max were 2,970/27,864 iterations. All accepted cases had tuple multiplicity one, but the sampler implements the general inverse-multiplicity rule. Earlier first-tuple-only synthetic studies completed 2,000/2,000 randomized-W5/W6, 5,000/5,000 default-W5/W6 and 1,000/1,000 independent cases. The hash-filtered key subsample could bias coverage, and synthetic CVs are not proven to have the rare real fixed-IV conditional distribution. The organizer-declared fixed-prefix experiment tests one inherited full-message prefix only.

For H1, two initial fresh fixed-IV `2^30`-block samples used the exact **31-step** compressor and observed 48,820,570 and 48,810,818 key hits versus 48,816,472 under U; the latter also found 95,473 first-representative W6 hits versus 95,344.672. A subsequent **34 independent batches of `2^30` OS-random first blocks** used a reduced-round self-test and rebuilt first-tuple map. Across 36,507,222,016 trials they observed 1,659,723,916 key hits (U expectation 1,659,760,048), 3,238,990 first-representative W6 hits (3,241,718.844), ten exact first-tuple W5/W6 prefixes (12.366), and **one** prefix with c18 in S (1.683). This one genuine fixed-IV joint prefix completed in 7,305 Phase-3 candidate iterations using fresh coins, producing the new ninth full-message collision certificate. Its two distinct 128-byte messages share the first block and independently hash in the organizer verifier to `b2a4c07e8d4f8ab1402e552c5cb8eb4bd73e252f18a2657aa3958bf045f14041` on the exact three-block 31-step target. The first tuple remains included in the eight-tuple table, so this is a witness for its selection rule. The 34-batch sampler tested only the first tuple per key, not later slots. That first-slot observation alone proves reachability but cannot establish H1's 0.4 rate factor or H2's 0.9 conditional completion probability. A preliminary scratch sampler that executed all 64 rounds is expressly excluded.

A separate exact first-eight fixed-IV sampler built the entire fixed-order table anew and checked 755,416,216 raw tuples, K=195,265,888 keys and M=641,616,343 retained records. Its four fixed-size `2^30`-block batches gave 195,275,948 key hits versus 195,265,888 under U, 1,250,873 all-slot W6 hits versus 1,253,156.920 expected as a sum, and 9,441/4,673/1,182 any-slot W5 low-16/20/24 hits. They found **five exact first-selected prefixes** (slots 1,2,3,3,6), versus a U union expectation between 4.615 and 4.780; none passed c18. The three-batch extension was chosen after the first batch, so this combined rate is descriptive rather than a preregistered estimate. The all-slot W6 count is correlated within a key and no independent-Poisson z score is asserted. An additional run requested `8×2^30` blocks and **stopped on its first c18 joint event after 2,816,700,416 blocks**, so its eight exact prefixes (slots 0,0,1,1,1,3,4,5) are optional-stopping evidence of reachability, not an unbiased rate estimate. Its JOINT prefix selected later slot 3, key `8b6504bf`; an independent forward-trace audit rebuilt all eight group tuples and confirmed slot 3 was the unique first W6/W5 match. Fresh Phase-3 coins completed it in **2,052** iterations. The tenth pair of distinct 128-byte messages independently hashes over all three padded 31-step blocks to `77026a470b6f4c2e73afd4086bb0978599bb38cd41f81448ce0aa4899c2fb101`. Thus real later-slot prefix and capped completion are witnessed directly, but one later-slot joint event still cannot establish the H1/H2 rates. Appendix D gives sampler, verifier, logged records, completion source and result.

The earlier first-slot evidence campaign used at most 47,393,223,481 v5 units including map construction, based on all 34 batches and explicitly charged lookup/reconstruction overhead; it was an independent validation run and did not select the 400 source points or first-eight table. The new first-eight sampler campaign is charged at most 33,619,757,821 v5 units using three full setup charges, all 7,111,667,712 sampled blocks, all 323,333,464 key hits, one capped completion and a witness-audit reserve. H3 covers both campaigns if validation or the ninth/tenth stored witnesses are charged as advice or development work. Appendix C gives scoped synthetic-CV and portable real-input reproduction source plus the logged seed and joint record; the binary witness in the manifest is the definitive independently rehashed output. `python3 scripts/local_tracks.py check sha256-r31-exploratory` mechanically verifies all **ten** certificates; this is not an AI verdict or human acceptance.

**H1 (score-critical):** Real first-block CVs give at least 0.4 times the certified U joint lower mass and at most 4/1024 times the specified U key/union upper masses. Scope: fresh fixed-IV blocks with the deterministic first-eight/first-match rule. Evidence: exact finite L/M/K counts, one first-slot and one later-slot real c18 joint success, ten full-message witnesses, four fixed-size real first-eight batches with five exact later-slot prefixes, key/W6 marginals and independent forward audits. Limitation: two rare joint events and the stopped-on-joint follow-up cannot estimate the 0.4 lower factor precisely; it could be false.

**H2 (score-critical):** Real first-matched prefixes with c18 in S complete under the specified global cap with probability at least 0.9 over fresh Phase-3 coins. Scope: the actual fixed-IV conditional prefix distribution across all eight retained slots. Evidence: 1,000/1,000 weighted synthetic-union tests including later slots, older first-slot studies, full compressor equality, fixed-prefix organizer experiment and two real-input completed collisions, including later slot 3. Limitation: the synthetic CV distribution is not established as the rare real conditional distribution; two real completions cannot estimate 0.9.

**H3 (score-critical):** All historical characteristic/400-point/eight-certificate advice generation and charged development/verification, including failed/abandoned searches, full overlap scans, auxiliary experiments, validation and any charged production of the ninth and tenth certificates, cost at most `2^40.5` v5 units. Evidence: two partial public CPU reports, bounded new validation and overlap campaigns, and a larger conditional allowance. Limitation: missing solver model/logs, incomplete historical accounting and unvalidated CPU-to-v5 conversion make this unmetered, not an audited cap. A concrete all-history ledger could strengthen or falsify the scalar.

**H4 (supporting):** Historical advice generation used less than `2^40` peak bytes. Evidence: explicit new-table layout and partial 5.8 GB report. Limitation: all-history peak memory is unmeasured.

The finite point and overlap calculations are exact for the printed source records. H1/H2/H3/H4 remain reviewable premises; neither a favorable AI decision nor a nominal reference turns them into proof or a promoted baseline.

## Appendix A. Attributed 400 paired source points


The following 400 paired records are attributed to the public 40.46 follow-up by `@Akashneelesh`. Their row format is `spNNN a/b` followed by the 24 words `A1..A12 E5..E12 W9..W12`. Each pair was independently checked for its displayed step-5..12 window, P4, V9, and modular recurrence relations before being used. Their existence does not prove a low-cost method of generating more such records.

```text
sp000 a 98c96dbf ecf4928a 349f3880 7503ea49 f99073ff 56be91c0 efb5970c 74c2979d ca80dd7e 620c51c9 04817481 60a00551 1d1fafdd adcb79e7 4cd7cae5 943bc249 61d543d1 7026b3fa aa271418 b1e7c9ec 984a7c52 664cd119 ae988d72 e1fce9d2
sp000 b 98c96dbf ecf4928a 349f3880 7503ea49 f9906405 563e91c1 fe958709 74c29799 ca80dd7e 620cd1cd 04817481 60a00551 1d1f9fe3 adc3f9e6 9c5fce6c d93b4a4d 61d543d9 5fa73402 bae71410 b1e749e4 984afc56 664cd119 ae988d72 e1fce9d2
sp001 a c7f0b583 5c048902 97e3d638 d7a2ccf0 062f93fe 899df778 2b229fbc 456399ac b725b9f1 424f67cb 19db1cc6 0c206f8e 1d1fafdd adca7be7 4cd7cae5 947fc049 61d531d1 7026b3fa 2a3f1c19 31ffb9e9 eda742db 730169a7 f3035ec3 8b7419a2
sp001 b c7f0b583 5c048902 97e3d638 d7a2ccf0 062f8404 891df779 3a028fb9 456399a8 b725b9f1 424fe7cf 19db1cc6 0c206f8e 1d1f9fe3 adc2fbe6 9c5fce6c d97f484d 61d531d9 5fa73402 3aff1c11 31ff39e1 eda7c2df 730169a7 f3035ec3 8b7419a2
sp002 a 9a1f4dbe 855f31ba 63e1abe4 7cf2b934 056fb3fe 2ed442b8 652b5a74 a47c8864 18f98bb3 e35464f9 741226a6 5e81291f 1d1fafdd adeb78e7 4c97cbe5 947fc049 61d161d1 7026b3fa 2a371419 b1ffd9e8 eea355db cbc2111d b936ab0b a8572bc8
sp002 b 9a1f4dbe 855f31ba 63e1abe4 7cf2b934 056fa404 2e5442b9 740b4a71 a47c8860 18f98bb3 e354e4fd 741226a6 5e81291f 1d1f9fe3 ade3f8e6 9c1fcf6c d97f484d 61d161d9 5fa73402 3af71411 b1ff59e0 eea3d5df cbc2111d b936ab0b a8572bc8
sp003 a 9599b240 14f41a8a 06a0dca4 2115ae6d f9d073fb daec9de4 abb612a4 d69c7377 62955b20 8c950d22 e323fa6d 6236b99e 1d1fafdd adeb7be7 4c97cbe5 943bc249 61d543d3 f02293fa 2a3f041d 31ef81ed 980a7c58 59baa3f5 f2f3f099 09e6f57a
sp003 b 9599b240 14f41a8a 06a0dca4 2115ae6d f9d06401 da6c9de5 ba9602a1 d69c7373 62955b20 8c958d26 e323fa6d 6236b99e 1d1f9fe3 ade3fbe6 9c1fcf6c d93b4a4d 61d543db dfa31402 3aff0415 31ef01e5 980afc5c 59baa3f5 f2f3f099 09e6f57a
sp004 a bf4d39a5 3cf91b0d f5a42302 d6f219ce 066f93fe e79ba242 e3681c84 2178092c dff52ee5 c06721cb 6b0cfdcb a2d9f941 1d1fa7dd ad8a79e7 4c97cbe5 946f8048 61d101d1 f02293fa 2a3f0c18 f17d89e9 e1b35953 93579118 bb0e30b7 6ac9e964
sp004 b bf4d39a5 3cf91b0d f5a42302 d6f219ce 066f8404 e71ba243 f2480c81 21780928 dff52ee5 c067a1cf 6b0cfdcb a2d9f941 1d1f97e3 ad82f9e6 9c1fcf6c d96f084c 61d101d9 dfa31402 3aff0c10 f17d09e1 e1b3d957 93579118 bb0e30b7 6ac9e964
sp005 a df73bcb7 27473809 6d628200 67efb8c8 066f93fe 8fd60340 4921da0c 8139a976 f1f6e2ab 542713c2 49a93a87 a4a761c4 1d1fa7dd af8978e7 4c97cbe5 947fc049 61d531d1 f02293fa 2a3f0419 317fb9e9 eba74ddb eb0640df 55441b2f 4f160979
sp005 b df73bcb7 27473809 6d628200 67efb8c8 066f8404 8f560341 5801ca09 8139a972 f1f6e2ab 542793c6 49a93a87 a4a761c4 1d1f97e3 af81f8e6 9c1fcf6c d97f484d 61d531d9 dfa31402 3aff0411 317f39e1 eba7cddf eb0640df 55441b2f 4f160979
sp006 a 73ad4dd5 38ab0a3e 7239cf7c 7e841db0 066f9bfa cb8f4e3c a72a98fc e133ad8c d92ee60f 036f61da f7c123ab c8470128 1d1fa7dd ade87ae7 4c97cbe5 943bc249 61d523d3 7026b3fa aa2f2c19 f1e9f1ed 8b6b3d59 e8ef1319 f76b8281 b5ba0b4a
sp006 b 73ad4dd5 38ab0a3e 7239cf7c 7e841db0 066f8c00 cb0f4e3d b60a88f9 e133ad88 d92ee60f 036fe1de f7c123ab c8470128 1d1f97e3 ade0fae6 9c1fcf6c d93b4a4d 61d523db 5fa73402 baef2c11 f1e971e5 8b6bbd5d e8ef1319 f76b8281 b5ba0b4a
sp007 a ee599471 992b03d7 4b0e59d9 d167a309 fa905bff 51fa1080 4bb9904c 958936fd af4f3e3e 94900941 e31482cb 7f8fc4d0 1d1fa7dd afea7ae7 4c97cbe5 946bc049 61d171d1 f02293fa 2a373418 b173d9e8 ed97115a 26b12117 52b894ee baa69d32
sp007 b ee599471 992b03d7 4b0e59d9 d167a309 fa904c05 517a1081 5a998049 958936f9 af4f3e3e 94908945 e31482cb 7f8fc4d0 1d1f97e3 afe2fae6 9c1fcf6c d96b484d 61d171d9 dfa31402 3af73410 b17359e0 ed97915e 26b12117 52b894ee baa69d32
sp008 a fcd66764 0ce3e44b f5c80970 606c53b9 f9d07bff f2f12030 41bb517c 9cce068f 24410fae 726074ea d6d3f13a 3f039a92 1d1fafdd ada878e7 4cd7cae5 947fc049 61c131d1 7026b3fa 2a371418 f1e989ed f9f25dda ffcff66f dc66a502 f3cf9d21
sp008 b fcd66764 0ce3e44b f5c80970 606c53b9 f9d06c05 f2712031 509b4179 9cce068b 24410fae 7260f4ee d6d3f13a 3f039a92 1d1f9fe3 ada0f8e6 9c5fce6c d97f484d 61c131d9 5fa73402 3af71410 f1e909e5 f9f2ddde ffcff66f dc66a502 f3cf9d21
sp009 a 9b7033ce ae806dfe d0fee50f 1636bfc3 f9d07bfb 30a64c4e 23f89484 fec247bd e6146a6a e1cc2ff9 23fec1a5 1567f925 1d1fafdd adeb7ae7 4cd7cae5 947b8048 61c111d3 7026b3fa 2a2f0418 717d99e9 f3f64ad8 c9a7c6ce fa21b1f9 156b6cb0
sp009 b 9b7033ce ae806dfe d0fee50f 1636bfc3 f9d06c01 30264c4f 32d88481 fec247b9 e6146a6a e1ccaffd 23fec1a5 1567f925 1d1f9fe3 ade3fae6 9c5fce6c d97b084c 61c111db 5fa73402 3aef0410 717d19e1 f3f6cadc c9a7c6ce fa21b1f9 156b6cb0
sp010 a f582cccc c8cc9109 63b7be03 e4884cca 066f9bfe 2dd0b742 8160f98e a5223eae d579518f e4191742 f55b90a1 d84095e3 1d1fafdd afe97be7 4c97cbe5 947fc049 61c111d1 f02293fa 2a370419 f1edf9ed eb931adb 42bb3bd9 1cfcfbad e79bf545
sp010 b f582cccc c8cc9109 63b7be03 e4884cca 066f8c04 2d50b743 9040e98b a5223eaa d579518f e4199746 f55b90a1 d84095e3 1d1f9fe3 afe1fbe6 9c1fcf6c d97f484d 61c111d9 dfa31402 3af70411 f1ed79e5 eb939adf 42bb3bd9 1cfcfbad e79bf545
sp011 a fd51a9b6 981c8d07 66e3cd00 9e289fcd f99073fb 34e20c44 89bc5284 f6c4c0a5 88c4e230 e44726e2 17dd0445 93bd234e 1d1fafdd ade979e7 4cd7cae5 943bc249 61d503d3 7026b3fa 2a371419 f1edd1ed 984a3c58 7fab568d 94a1d1f9 9641478a
sp011 b fd51a9b6 981c8d07 66e3cd00 9e289fcd f9906401 34620c45 989c4281 f6c4c0a1 88c4e230 e447a6e6 17dd0445 93bd234e 1d1f9fe3 ade1f9e6 9c5fce6c d93b4a4d 61d503db 5fa73402 3af71411 f1ed51e5 984abc5c 7fab568d 94a1d1f9 9641478a
sp012 a f7706079 331f5b0a 89a8172c 8986edfc 056fb3fe a6df1670 2f2a9eb4 86357986 baf41459 13994e7b 5fb8e4dd 5989fe4e 1d1fafdd afeb79e7 4c97cbe5 943bc249 61c533d1 f02293fa 2a27041c 316f81ed 8a5b2c53 8bdfeea7 6f67548a 61adddec
sp012 b f7706079 331f5b0a 89a8172c 8986edfc 056fa404 a65f1671 3e0a8eb1 86357982 baf41459 1399ce7f 5fb8e4dd 5989fe4e 1d1f9fe3 afe3f9e6 9c1fcf6c d93b4a4d 61c533d9 dfa31402 3ae70414 316f01e5 8a5bac57 8bdfeea7 6f67548a 61adddec
sp013 a cb26c90f ce483b4d 4c09a277 ece5b8be 066f93fe cbd52332 cf63ba76 657909be 5b62293b 0b5b7638 851cda55 584592cf 1d1fafdd ad8b7be7 4c97cbe5 946fc049 61d501d1 7026b3fa 2a370419 f1e1d9ed e5b750db 31213ea7 4f0a5b09 27451a35
sp013 b cb26c90f ce483b4d 4c09a277 ece5b8be 066f8404 cb552333 de43aa73 657909ba 5b62293b 0b5bf63c 851cda55 584592cf 1d1f9fe3 ad83fbe6 9c1fcf6c d96f484d 61d501d9 5fa73402 3af70411 f1e159e5 e5b7d0df 31213ea7 4f0a5b09 27451a35
sp014 a 55b11431 f68466cb 4d40d9e9 746e8b3d fa9053ff 53bb30b0 efbf9674 91dd93df 47c4d522 8ffc7d31 bde41167 a3f008be 1d1fa7dd adea7be7 4c97cbe5 947fc049 61d101d1 f02293fa aa3f2c18 b1e7d1ec f9825ada 26c800a9 2ea696c6 38be6777
sp014 b 55b11431 f68466cb 4d40d9e9 746e8b3d fa904405 533b30b1 fe9f8671 91dd93db 47c4d522 8ffcfd35 bde41167 a3f008be 1d1f97e3 ade2fbe6 9c1fcf6c d97f484d 61d101d9 dfa31402 baff2c10 b1e751e4 f982dade 26c800a9 2ea696c6 38be6777
sp015 a c03c1429 b7dfa39a 1e0a309b 902c6a4f fad05bff f1f891c2 eff4968c 5dc0157f e1c473c8 23eb6b5a 1b91a5ec 6703f5cd 1d1fa7dd afab7ae7 4cd7cae5 943b8248 61c523d1 7026b3fa 2a3f1c1c 31efa1ec 913a7cda c1029294 2e71b5f7 7eabc352
sp015 b c03c1429 b7dfa39a 1e0a309b 902c6a4f fad04c05 f17891c3 fed48689 5dc0157b e1c473c8 23ebeb5e 1b91a5ec 6703f5cd 1d1f97e3 afa3fae6 9c5fce6c d93b0a4c 61c523d9 5fa73402 3aff1c14 31ef21e4 913afcde c1029294 2e71b5f7 7eabc352
sp016 a ee8ea085 a832c28e 2252a0a4 97279a6d f9907bff 18fda1e0 c3b31724 1c9ba51f 0246acde d68b5843 17e53e63 4e4405fb 1d1fafdd ada97be7 4c97cbe5 947bc049 61d111d1 f02293fa aa2f3c18 b1fff1e9 f8864a5a 61ce8f3b 5aa71616 b61427f2
sp016 b ee8ea085 a832c28e 2252a0a4 97279a6d f9906c05 187da1e1 d2930721 1c9ba51b 0246acde d68bd847 17e53e63 4e4405fb 1d1f9fe3 ada1fbe6 9c1fcf6c d97b484d 61d111d9 dfa31402 baef3c10 b1ff71e1 f886ca5e 61ce8f3b 5aa71616 b61427f2
sp017 a 2dd11e6b f302798a f921568f 4cfb4c5e 056fb3fe a89697d2 af65b916 ea207996 fe633e37 38d138ab c4c9affa 6c5dedb2 1d1fa7dd adc97ae7 4c97cbe5 942bc249 61d523d1 7026b3fa 2a3f0c19 716181ed 847b6353 1456ca83 6f504269 26650d7e
sp017 b 2dd11e6b f302798a f921568f 4cfb4c5e 056fa404 a81697d3 be45a913 ea207992 fe633e37 38d1b8af c4c9affa 6c5dedb2 1d1f97e3 adc1fae6 9c1fcf6c d92b4a4d 61d523d9 5fa73402 3aff0c11 716101e5 847be357 1456ca83 6f504269 26650d7e
sp018 a 314efa0b d2fed953 f8f7ec5d c32fde89 fad053fb f5e5ad04 0bb095cc 3bd7c265 a5cfefe4 100215eb b34e075b 14fd3cd9 1d1fa7dd adc879e7 4cd7cae5 943bc249 61d503d3 7026b3fa 2a272c18 b17381e8 970a6458 bec8b5cd 129da6b0 1c6fa7ab
sp018 b 314efa0b d2fed953 f8f7ec5d c32fde89 fad04401 f565ad05 1a9085c9 3bd7c261 a5cfefe4 100295ef b34e075b 14fd3cd9 1d1f97e3 adc0f9e6 9c5fce6c d93b4a4d 61d503db 5fa73402 3ae72c10 b17301e0 970ae45c bec8b5cd 129da6b0 1c6fa7ab
sp019 a dce7b667 3213e35b fb20f95e c0590b8f fa905bff d5fc3002 e7f896cc 399cb36f 8504d6f8 c5a61a70 4239687e 745d23ce 1d1fa7dd adcb79e7 4c97cbe5 943b8248 61c523d1 7026b3fa 2a270418 b1f7c9e9 933a7bda dedef554 36959cb3 1f4b3e00
sp019 b dce7b667 3213e35b fb20f95e c0590b8f fa904c05 d57c3003 f6d886c9 399cb36b 8504d6f8 c5a69a74 4239687e 745d23ce 1d1f97e3 adc3f9e6 9c1fcf6c d93b0a4c 61c523d9 5fa73402 3ae70410 b1f749e1 933afbde dedef554 36959cb3 1f4b3e00
sp020 a 34d55431 c6bd1ccb d14298c7 172bea0f f99073fb daa29986 47f096cc bec9552f aac05160 653110d1 2c7bf6d5 f206b065 1d1fafdd afe87be7 4c97cbe5 947f8048 61d511d3 f02293fa aa271418 71f1e9e8 f4864158 97aaa716 d65dae6d d7c0d03b
sp020 b 34d55431 c6bd1ccb d14298c7 172bea0f f9906401 da229987 56d086c9 bec9552b aac05160 653190d5 2c7bf6d5 f206b065 1d1f9fe3 afe0fbe6 9c1fcf6c d97f084c 61d511db dfa31402 bae71410 71f169e0 f486c15c 97aaa716 d65dae6d d7c0d03b
sp021 a e81ae1f3 88c3d8c6 00be8fff f6d11536 062f93fe cbda66ba 016e7ff6 67316f9c 3fad2181 c2de6ecb 0fe0bdf5 495bd454 1d1fafdd adaa79e7 4c97cbe5 947fc049 61d131d1 7026b3fa aa3f2c18 71f991e8 ede344db 2ee4ece5 9cfb8d88 a3781bb6
sp021 b e81ae1f3 88c3d8c6 00be8fff f6d11536 062f8404 cb5a66bb 104e6ff3 67316f98 3fad2181 c2deeecf 0fe0bdf5 495bd454 1d1f9fe3 ada2f9e6 9c1fcf6c d97f484d 61d131d9 5fa73402 baff2c10 71f911e0 ede3c4df 2ee4ece5 9cfb8d88 a3781bb6
sp022 a 97ee6c04 0cda254a 98698574 ff569fbd f9d073fb baa42c34 8fbe92f4 9e9960f7 8c5a2358 957c32f0 f8d0f91c 24e7f76d 1d1fafdd adc97be7 4c97cbe5 943bc249 61d503d3 7026b3fa aa270418 71f199e9 980a3c58 fa09349d 0ecf8088 782840b5
sp022 b 97ee6c04 0cda254a 98698574 ff569fbd f9d06401 ba242c35 9e9e82f1 9e9960f3 8c5a2358 957cb2f4 f8d0f91c 24e7f76d 1d1f9fe3 adc1fbe6 9c1fcf6c d93b4a4d 61d503db 5fa73402 bae70410 71f119e1 980abc5c fa09349d 0ecf8088 782840b5
sp023 a f578fbfe b5b6830f 64a10c07 3a295ecf f9d073ff 92f98542 0bf01384 54d8808d ae47e30a 18423288 d51421ee 241b6074 1d1fa7dd afca7be7 4cd7cae5 947f8048 61c121d1 f02293fa 2a272418 f1f9a1e9 f3f25952 dd996e9c 921e52b7 43c16d66
sp023 b f578fbfe b5b6830f 64a10c07 3a295ecf f9d06405 92798543 1ad00381 54d88089 ae47e30a 1842b28c d51421ee 241b6074 1d1f97e3 afc2fbe6 9c5fce6c d97f084c 61c121d9 dfa31402 3ae72410 f1f921e1 f3f2d956 dd996e9c 921e52b7 43c16d66
sp024 a c7b7e7a5 d46e1f83 68ac74b4 fc294e61 fad053fb f3e7ddec 2bb692a4 d98fb187 a74790f6 57ed6b50 511d002b 10504e7a 1d1fa7dd af8978e7 4c97cbe5 943bc249 61d513d3 7026b3fa aa2f3c19 f17599e9 954a7558 bf0d85a7 72dfa8d9 bcf19f09
sp024 b c7b7e7a5 d46e1f83 68ac74b4 fc294e61 fad04401 f367dded 3a9682a1 d98fb183 a74790f6 57edeb54 511d002b 10504e7a 1d1f97e3 af81f8e6 9c1fcf6c d93b4a4d 61d513db 5fa73402 baef3c11 f17519e1 954af55c bf0d85a7 72dfa8d9 bcf19f09
sp025 a 6dbd5e77 3550f785 04e67392 27bb0942 052fb3fe 209af2ca e3699c04 0c7d9994 b6f89c0f e5b90b50 f37b65b2 1a567ee1 1d1fa7dd afc878e7 4cd7cae5 947f8048 61d561d1 7026b3fa aa273c18 b1fb81e9 e8a75c53 da1eb08c baa4d27b 4a25c47e
sp025 b 6dbd5e77 3550f785 04e67392 27bb0942 052fa404 201af2cb f2498c01 0c7d9990 b6f89c0f e5b98b54 f37b65b2 1a567ee1 1d1f97e3 afc0f8e6 9c5fce6c d97f084c 61d561d9 5fa73402 bae73c10 b1fb01e1 e8a7dc57 da1eb08c baa4d27b 4a25c47e
sp026 a 87987929 3083c34d 09604b42 68c7998e 066f93fe 25d08202 436c1ac4 a972885c 1f6ee53d 2b6c7099 12021559 898d3fb3 1d1fa7dd adc879e7 4c97cbe5 943b8248 61d553d1 7026b3fa aa2f2c18 3173e1e8 876b73db 9746209a 5b2a50bb 28e510f7
sp026 b 87987929 3083c34d 09604b42 68c7998e 066f8404 25508203 524c0ac1 a9728858 1f6ee53d 2b6cf09d 12021559 898d3fb3 1d1f97e3 adc0f9e6 9c1fcf6c d93b0a4c 61d553d9 5fa73402 baef2c10 317361e0 876bf3df 9746209a 5b2a50bb 28e510f7
sp027 a 99b39fb9 1485b30d 57481725 cc9c8dec 066f9bfe c1939660 872abeae 4d3ebe2c 39719b49 0e466581 a69b23dd eeba723d 1d1fafdd afc87be7 4c97cbe5 946b8048 61d101d1 7026b3fa aa3f3418 f1e181ec ddb757d3 3725bafa 174fc6d1 3d6afcc8
sp027 b 99b39fb9 1485b30d 57481725 cc9c8dec 066f8c04 c1139661 960aaeab 4d3ebe28 39719b49 0e46e585 a69b23dd eeba723d 1d1f9fe3 afc0fbe6 9c1fcf6c d96b084c 61d101d9 5fa73402 baff3410 f1e101e4 ddb7d7d7 3725bafa 174fc6d1 3d6afcc8
sp028 a 9186cab8 b3151589 ecec92af 0b83c87a 052fb3fe aada33f2 c962fcb6 ee7edae4 5eefdfbf a8f73ca8 634e4043 d22803a2 1d1fa7dd afcb78e7 4cd7cae5 947bc049 61d141d1 f02293fa 2a27341d 71edf9ec eaa74d5b cde7ff5f d4af3989 35aad8d0
sp028 b 9186cab8 b3151589 ecec92af 0b83c87a 052fa404 aa5a33f3 d842ecb3 ee7edae0 5eefdfbf a8f7bcac 634e4043 d22803a2 1d1f97e3 afc3f8e6 9c5fce6c d97b484d 61d141d9 dfa31402 3ae73415 71ed79e4 eaa7cd5f cde7ff5f d4af3989 35aad8d0
sp029 a 7e4679d7 187f19ce cb3744c4 bb087e09 f99073ff b2b10580 01b0d4cc f082a0bf 0c4ee656 4833172b 97831701 1f2c7fb2 1d1fafdd afcb78e7 4c97cbe5 947bc049 61d101d1 7026b3fa aa271c1c 31fb89e8 f686455a 45f54ed9 9ca158b6 f594e2cd
sp029 b 7e4679d7 187f19ce cb3744c4 bb087e09 f9906405 b2310581 1090c4c9 f082a0bb 0c4ee656 4833972f 97831701 1f2c7fb2 1d1f9fe3 afc3f8e6 9c1fcf6c d97b484d 61d101d9 5fa73402 bae71c14 31fb09e0 f686c55e 45f54ed9 9ca158b6 f594e2cd
sp030 a 8f9f6a8b 6a91f17e 334c3088 d3778a41 f9d073fb 56aef9cc 4db0d084 72817265 88d81df4 8fe97eb0 5ad4a560 78eed409 1d1fafdd ad887ae7 4cd7cae5 943bc249 61c543d3 f02293fa aa371418 f17589e8 983a7d58 e65b0b0d d0b143b4 9be00d04
sp030 b 8f9f6a8b 6a91f17e 334c3088 d3778a41 f9d06401 562ef9cd 5c90c081 72817261 88d81df4 8fe9feb4 5ad4a560 78eed409 1d1f9fe3 ad80fae6 9c5fce6c d93b4a4d 61c543db dfa31402 baf71410 f17509e0 983afd5c e65b0b0d d0b143b4 9be00d04
sp031 a 419421a5 7085e4f9 7f821723 0a908df6 052fbbfe 2eda767a 2d6e78b6 ae65db3c f024d769 41cc2bf8 dc3c6c77 78bc53b4 1d1fa7dd af897be7 4c97cbe5 947fc049 61d521d1 7026b3fa aa27241d f1f599e9 ece712db cbfdeae3 70df9ccd f3cba877
sp031 b 419421a5 7085e4f9 7f821723 0a908df6 052fac04 2e5a767b 3c4e68b3 ae65db38 f024d769 41ccabfc dc3c6c77 78bc53b4 1d1f97e3 af81fbe6 9c1fcf6c d97f484d 61d521d9 5fa73402 bae72415 f1f519e1 ece792df cbfdeae3 70df9ccd f3cba877
sp032 a 1bff1cd4 56b44307 5784cd3e c72bdff7 f9d073ff 50ba447a 25fb5334 bc9d214f 2e8f6398 f6f47ec3 9d3ac477 6404862c 1d1fafdd afa979e7 4cd7cae5 943b8248 61c503d1 f02293fa 2a3f0c18 31ffb9e9 923a3bda e24ec158 786ef907 105afd41
sp032 b 1bff1cd4 56b44307 5784cd3e c72bdff7 f9d06405 503a447b 34db4331 bc9d214b 2e8f6398 f6f4fec7 9d3ac477 6404862c 1d1f9fe3 afa1f9e6 9c5fce6c d93b0a4c 61c503d9 dfa31402 3aff0c10 31ff39e1 923abbde e24ec158 786ef907 105afd41
sp033 a 408b2fd7 06e5203b e6a63447 9241ce97 fa905bff f9b7f51a 29f1d25c 5bc3d0cd c1119570 9dd83e10 9121793f 0f9d574c 1d1fa7dd ade878e7 4c97cbe5 947f8048 61d501d1 7026b3fa 2a371419 31ffc1e9 f5865452 02d16fc0 f46c9324 71106b61
sp033 b 408b2fd7 06e5203b e6a63447 9241ce97 fa904c05 f937f51b 38d1c259 5bc3d0c9 c1119570 9dd8be14 9121793f 0f9d574c 1d1f97e3 ade0f8e6 9c1fcf6c d97f084c 61d501d9 5fa73402 3af71411 31ff41e1 f586d456 02d16fc0 f46c9324 71106b61
sp034 a 63665894 8f9ca35a 798a947b 3b2f8eaf fad05bff fbbdb522 aff71264 b992309d c5071e46 810f05d9 6de7b59b 2661cf13 1d1fa7dd afab79e7 4c97cbe5 943b8248 61d513d1 7026b3fa 2a3f0418 3177f9e9 914a6bda bf55ae72 6eaf311b 12d61dd2
sp034 b 63665894 8f9ca35a 798a947b 3b2f8eaf fad04c05 fb3db523 bed70261 b9923099 c5071e46 810f85dd 6de7b59b 2661cf13 1d1f97e3 afa3f9e6 9c1fcf6c d93b0a4c 61d513d9 5fa73402 3aff0410 317779e1 914aebde bf55ae72 6eaf311b 12d61dd2
sp035 a 54409fc8 4c9b2fce a8519bf5 84f6293c 062f93fe 879c12b0 ef2e3dfe 83327abc 1fa21fbf aa174789 5209cdcb 66b08d30 1d1fa7dd af8b78e7 4c97cbe5 942f8248 61d103d1 f02293fa aa2f041c 31efe9ed 7ff3525b b19721a2 2f780541 df1d93f7
sp035 b 54409fc8 4c9b2fce a8519bf5 84f6293c 062f8404 871c12b1 fe0e2dfb 83327ab8 1fa21fbf aa17c78d 5209cdcb 66b08d30 1d1f97e3 af83f8e6 9c1fcf6c d92f0a4c 61d103d9 dfa31402 baef0414 31ef69e5 7ff3d25f b19721a2 2f780541 df1d93f7
sp036 a 243332cf 878b29b9 479a8fc7 7fbcf512 052fb3fe 0e90469a 0b683fd6 007c0fae 746b657b bd533532 1d4ffe9c fa869525 1d1fafdd ade87ae7 4cd7cae5 947bc049 61d151d1 7026b3fa aa272c18 f16dc9ec eca7535b ec210a79 92a9eea8 959556a8
sp036 b 243332cf 878b29b9 479a8fc7 7fbcf512 052fa404 0e10469b 1a482fd3 007c0faa 746b657b bd53b536 1d4ffe9c fa869525 1d1f9fe3 ade0fae6 9c5fce6c d97b484d 61d151d9 5fa73402 bae72c10 f16d49e4 eca7d35f ec210a79 92a9eea8 959556a8
sp037 a 0ca13c9a 6329927a b7b4afa4 12cb9d70 056fbbfe 4495e6f8 0b2f983c 042f2d34 34b04c33 1d413392 d22f8fa6 38dd9647 1d1fa7dd af8b7be7 4c97cbe5 947fc049 61d121d1 f02293fa aa2f0c18 b167c9ec eca312db 343c4ae5 132674fe cdcc679e
sp037 b 0ca13c9a 6329927a b7b4afa4 12cb9d70 056fac04 4415e6f9 1a0f8839 042f2d30 34b04c33 1d41b396 d22f8fa6 38dd9647 1d1f97e3 af83fbe6 9c1fcf6c d97f484d 61d121d9 dfa31402 baef0c10 b16749e4 eca392df 343c4ae5 132674fe cdcc679e
sp038 a 9738e757 e142fb0d beefe225 5387d0ec 066f93fe 839a8360 e326bbae c3664f9c f37a0557 8e626580 90759649 407df811 1d1fafdd adc97be7 4c97cbe5 946f8048 61c111d1 f02293fa 2a2f2419 716981ed e1a35f53 ef116fbc bb3f998e 54d34cdc
sp038 b 9738e757 e142fb0d beefe225 5387d0ec 066f8404 831a8361 f206abab c3664f98 f37a0557 8e62e584 90759649 407df811 1d1f9fe3 adc1fbe6 9c1fcf6c d96f084c 61c111d9 dfa31402 3aef2411 716901e5 e1a3df57 ef116fbc bb3f998e 54d34cdc
sp039 a d7f6116a c3f84c82 6126708b ce142a43 f99073ff f2fbd1ca c3f0168c fed7d4ff 6242911a 7a0556a9 df0f12af 8c1e4344 1d1fa7dd ad8b7be7 4cd7cae5 943b8248 61c533d1 7026b3fa 2a273418 b1f781e9 947a73da c227514e 5a5e3df3 5a07c532
sp039 b d7f6116a c3f84c82 6126708b ce142a43 f9906405 f27bd1cb d2d00689 fed7d4fb 6242911a 7a05d6ad df0f12af 8c1e4344 1d1f97e3 ad83fbe6 9c5fce6c d93b0a4c 61c533d9 5fa73402 3ae73410 b1f701e1 947af3de c227514e 5a5e3df3 5a07c532
sp040 a 3387958b a31b5a96 db6692b9 bdc32868 056fb3fe 4a9913e0 6927fd2e 0c761d9e 5c287a67 97895ff2 5c38c0c9 73f3bbb2 1d1fa7dd afe87be7 4cd7cae5 943b8248 61c573d1 f02293fa 2a2f3c19 71f989e9 865b73db e8492e40 35326f0e 0c934335
sp040 b 3387958b a31b5a96 db6692b9 bdc32868 056fa404 4a1913e1 7807ed2b 0c761d9a 5c287a67 9789dff6 5c38c0c9 73f3bbb2 1d1f97e3 afe0fbe6 9c5fce6c d93b0a4c 61c573d9 dfa31402 3aef3c11 71f909e1 865bf3df e8492e40 35326f0e 0c934335
sp041 a a2cccfdb f203bb9a 405e3f9a dec9454e 056fb3fe a29a36c2 096d5804 2e307b0e 18ab3fd1 ea13470b daccea0f f3c08174 1d1fa7dd afea7ae7 4c97cbe5 946f8048 61d121d1 7026b3fa 2a3f1418 b1ffb9e8 e0b35853 55ed1c1c 150ced7b 1e93779e
sp041 b a2cccfdb f203bb9a 405e3f9a dec9454e 056fa404 a21a36c3 184d4801 2e307b0a 18ab3fd1 ea13c70f daccea0f f3c08174 1d1f97e3 afe2fae6 9c1fcf6c d96f084c 61d121d9 5fa73402 3aff1410 b1ff39e0 e0b3d857 55ed1c1c 150ced7b 1e93779e
sp042 a e559a200 f718744a dfc7d941 6c714b89 f99073ff d6f89000 c1b8d6cc 5ed654ff 685a3394 d0841a6b 786a8e43 51a7ec51 1d1fa7dd afeb78e7 4c97cbe5 943bc249 61d533d1 7026b3fa aa372418 31fbb9e8 964a7552 e3cad417 dce52cb2 70157b32
sp042 b e559a200 f718744a dfc7d941 6c714b89 f9906405 d6789001 d098c6c9 5ed654fb 685a3394 d0849a6f 786a8e43 51a7ec51 1d1f97e3 afe3f8e6 9c1fcf6c d93b4a4d 61d533d9 5fa73402 baf72410 31fb39e0 964af556 e3cad417 dce52cb2 70157b32
sp043 a 1f6fe890 1429e255 12b1565a cec9cc8a 052fbbfe 809eb702 2165d84c 242ebcc4 d2add0eb d46c23e2 f7880577 5a3151ce 1d1fafdd adca7ae7 4c97cbe5 946f8048 61d531d1 7026b3fa 2a3f0c19 b16ba9ec e2f75853 7c10ab1e fd105534 2c1d2650
sp043 b 1f6fe890 1429e255 12b1565a cec9cc8a 052fac04 801eb703 3045c849 242ebcc0 d2add0eb d46ca3e6 f7880577 5a3151ce 1d1f9fe3 adc2fae6 9c1fcf6c d96f084c 61d531d9 5fa73402 3aff0c11 b16b29e4 e2f7d857 7c10ab1e fd105534 2c1d2650
sp044 a f93f8bc3 12f19c52 5ea46d5b 1a21bf8f fa905bfb 55ac8c06 8ffd954c d9d88687 e58489e0 cc941b82 a71b63c4 979c01d7 1d1fa7dd ade97ae7 4c97cbe5 946f8048 61c571d3 f02293fa 2a27041c 317389e8 ed870058 26afb812 0e609ff1 0ddadce5
sp044 b f93f8bc3 12f19c52 5ea46d5b 1a21bf8f fa904c01 552c8c07 9edd8549 d9d88683 e58489e0 cc949b86 a71b63c4 979c01d7 1d1f97e3 ade1fae6 9c1fcf6c d96f084c 61c571db dfa31402 3ae70414 317309e0 ed87805c 26afb812 0e609ff1 0ddadce5
sp045 a 43a4160e 3cae53c2 f69c4cea ac0f963b fa9053fb 91adadb6 8df252fc ffdf4725 41050e58 a306577a 099d8ff4 ff00c177 1d1fa7dd af8b7ae7 4c97cbe5 946b8048 61d161d3 f02293fa aa3f3418 f1e1f9ed e99708d8 df14c520 9088223d 0acecbce
sp045 b 43a4160e 3cae53c2 f69c4cea ac0f963b fa904401 912dadb7 9cd242f9 ffdf4721 41050e58 a306d77e 099d8ff4 ff00c177 1d1f97e3 af83fae6 9c1fcf6c d96b084c 61d161db dfa31402 baff3410 f1e179e5 e99788dc df14c520 9088223d 0acecbce
sp046 a b48fb41c e978c4fe 8beb2508 c252dfc5 f9d073fb b0a66c4c 89bc528c d2dec0b7 82cec9f4 168b5e62 8f057e1b 6c057938 1d1fafdd ade87be7 4cd7cae5 943bc249 61d503d3 f02293fa 2a271c19 b16f91ec 980a3c58 83e3d485 1495c9ad 81a0c998
sp046 b b48fb41c e978c4fe 8beb2508 c252dfc5 f9d06401 b0266c4d 989c4289 d2dec0b3 82cec9f4 168bde66 8f057e1b 6c057938 1d1f9fe3 ade0fbe6 9c5fce6c d93b4a4d 61d503db dfa31402 3ae71c11 b16f11e4 980abc5c 83e3d485 1495c9ad 81a0c998
sp047 a a5e95442 2ed5f4be 86b1f3c9 328b0904 066f93fa 25c25a8c c12c7bce 4724ffa6 9f7f9939 620950eb 2adb4bee 0d9c20b7 1d1fafdd ade87be7 4c97cbe5 946f8048 61c511d3 7026b3fa 2a3f0419 717d89e8 e1a75f59 d68ec810 5d49c9b0 c934e347
sp047 b a5e95442 2ed5f4be 86b1f3c9 328b0904 066f8400 25425a8d d00c6bcb 4724ffa2 9f7f9939 6209d0ef 2adb4bee 0d9c20b7 1d1f9fe3 ade0fbe6 9c1fcf6c d96f084c 61c511db 5fa73402 3aff0411 717d09e0 e1a7df5d d68ec810 5d49c9b0 c934e347
sp048 a 0e9ac20d 349cc1b9 8f095be5 52ef4930 052fbbfe 609252b8 c32b3c76 82387f5e da63586d 8a537028 5f87a4cb f916eb69 1d1fafdd adab78e7 4cd7cae5 946f8048 61d121d1 f02293fa aa2f3c1d b1e3c1ed e2b34a53 1a2fe226 5afb41ca 64075b39
sp048 b 0e9ac20d 349cc1b9 8f095be5 52ef4930 052fac04 601252b9 d20b2c73 82387f5a da63586d 8a53f02c 5f87a4cb f916eb69 1d1f9fe3 ada3f8e6 9c5fce6c d96f084c 61d121d9 dfa31402 baef3c15 b1e341e5 e2b3ca57 1a2fe226 5afb41ca 64075b39
sp049 a 0601f28f cc93728e 54565084 67656a4d f9907bff b6ffb1c0 4db45084 70983275 8c451634 8ca90a02 c021f3c2 f6bdf078 1d1fa7dd adca7be7 4c97cbe5 943bc249 61d503d1 7026b3fa 2a370418 316399ec 984a3c52 05ecb011 d0e9c2fa 5fbbacfc
sp049 b 0601f28f cc93728e 54565084 67656a4d f9906c05 b67fb1c1 5c944081 70983271 8c451634 8ca98a06 c021f3c2 f6bdf078 1d1f97e3 adc2fbe6 9c1fcf6c d93b4a4d 61d503d9 5fa73402 3af70410 316319e4 984abc56 05ecb011 d0e9c2fa 5fbbacfc
sp050 a 62b15698 f2ccd905 dba9820b 2e8738c6 066f93fe 69d2634a 69607d8e c7386916 dda24f7b 58fc2f88 394afb05 c1bef04f 1d1fafdd adcb79e7 4c97cbe5 947fc049 61c501d1 f02293fa 2a2f1c19 717589e9 ed9714db 0acfa28f 34f59fad 5118fc38
sp050 b 62b15698 f2ccd905 dba9820b 2e8738c6 066f8404 6952634b 78406d8b c7386912 dda24f7b 58fcaf8c 394afb05 c1bef04f 1d1f9fe3 adc3f9e6 9c1fcf6c d97f484d 61c501d9 dfa31402 3aef1c11 717509e1 ed9794df 0acfa28f 34f59fad 5118fc38
sp051 a 18f3ddc7 727927c6 953246d1 0d83dc00 056fb3fe e0da6788 2b21394e 6c6f0a0c bc210b29 edd23cb0 0179f6fc c2d7950d 1d1fafdd adcb78e7 4c97cbe5 942b8248 61d503d1 f02293fa aa370418 316fd9ec 807b3adb 5c1cdd4a f39109ed e1f555a6
sp051 b 18f3ddc7 727927c6 953246d1 0d83dc00 056fa404 e05a6789 3a01294b 6c6f0a08 bc210b29 edd2bcb4 0179f6fc c2d7950d 1d1f9fe3 adc3f8e6 9c1fcf6c d92b0a4c 61d503d9 dfa31402 baf70410 316f59e4 807bbadf 5c1cdd4a f39109ed e1f555a6
sp052 a 0756fe49 151c2d8d 28e296a3 ad82cc6e 066f9bfe a59317e2 23673926 eb705dbe 95323ab9 666c7741 4085a5d5 72c3b456 1d1fa7dd adc878e7 4c97cbe5 947fc049 61d101d1 f02293fa 2a2f3418 b1f3a1e9 eda315db d5121c77 7aeefc14 691b1f72
sp052 b 0756fe49 151c2d8d 28e296a3 ad82cc6e 066f8c04 a51317e3 32472923 eb705dba 95323ab9 666cf745 4085a5d5 72c3b456 1d1f97e3 adc0f8e6 9c1fcf6c d97f484d 61d101d9 dfa31402 3aef3410 b1f321e1 eda395df d5121c77 7aeefc14 691b1f72
sp053 a 6db587bf 64b23589 8c39f6af 83c48c7a 052fb3fe 6ed937f2 09667ebe 0c7d9886 1a6fba85 b6124043 65d87c40 b65f09e8 1d1fafdd ade978e7 4cd7cae5 947fc049 61d511d1 f02293fa aa27341d f1fdf9e9 eea705db 0db30ca9 14a7a781 15c85aeb
sp053 b 6db587bf 64b23589 8c39f6af 83c48c7a 052fa404 6e5937f3 18466ebb 0c7d9882 1a6fba85 b612c047 65d87c40 b65f09e8 1d1f9fe3 ade1f8e6 9c5fce6c d97f484d 61d511d9 dfa31402 bae73415 f1fd79e1 eea785df 0db30ca9 14a7a781 15c85aeb
sp054 a 1c55e275 b23b4296 ace11e99 b8c1ec48 056fb3fe 4ad537c0 a1247e86 aa64d9cc 7e659793 450f16f1 52027634 49ff13a7 1d1fa7dd afca7be7 4cd7cae5 943b8248 61d573d1 f02293fa aa2f3419 f161f9ec 866b73db f02b4860 7d35e5b6 6c08f6a9
sp054 b 1c55e275 b23b4296 ace11e99 b8c1ec48 056fa404 4a5537c1 b0046e83 aa64d9c8 7e659793 450f96f5 52027634 49ff13a7 1d1f97e3 afc2fbe6 9c5fce6c d93b0a4c 61d573d9 dfa31402 baef3411 f16179e4 866bf3df f02b4860 7d35e5b6 6c08f6a9
sp055 a bc05cb69 59fdb9c6 a203ecd6 042a1e07 fa9053fb 17e24d8e 21f452cc 1388e1a5 e55d8fc4 2b6c64b8 ca1059d0 c6b83bf1 1d1fa7dd afa978e7 4c97cbe5 946b8048 61c171d3 f02293fa 2a2f2418 317fc9e8 e9871ad8 60b9e90a 7c76026d c0aac34b
sp055 b bc05cb69 59fdb9c6 a203ecd6 042a1e07 fa904401 17624d8f 30d442c9 1388e1a1 e55d8fc4 2b6ce4bc ca1059d0 c6b83bf1 1d1f97e3 afa1f8e6 9c1fcf6c d96b084c 61c171db dfa31402 3aef2410 317f49e0 e9879adc 60b9e90a 7c76026d c0aac34b
sp056 a 2c0ed09e dabba219 777afe38 dbda6cec 052fbbfe 0adf1760 a7261fa4 0c669f86 5063925b 323946eb 32310ffc 8e9c241c 1d1fa7dd adcb7ae7 4cd7cae5 947fc049 61d551d1 7026b3fa aa272c1d b17f99e8 eea743db f1ef4a33 f6e80edf 5558944d
sp056 b 2c0ed09e dabba219 777afe38 dbda6cec 052fac04 0a5f1761 b6060fa1 0c669f82 5063925b 3239c6ef 32310ffc 8e9c241c 1d1f97e3 adc3fae6 9c5fce6c d97f484d 61d551d9 5fa73402 bae72c15 b17f19e0 eea7c3df f1ef4a33 f6e80edf 5558944d
sp057 a 2dc1df2a f6d84179 ef577fa2 4ff76d76 052fbbfe e89cf6fa 296bde3c c27b5e44 74e35b91 74ce2f41 1543bd94 cab58067 1d1fafdd afa978e7 4cd7cae5 947f8048 61d561d1 f02293fa aa3f141d 316789ed e8a74c53 92378c5c f4ba7804 9b3426ae
sp057 b 2dc1df2a f6d84179 ef577fa2 4ff76d76 052fac04 e81cf6fb 384bce39 c27b5e40 74e35b91 74ceaf45 1543bd94 cab58067 1d1f9fe3 afa1f8e6 9c5fce6c d97f084c 61d561d9 dfa31402 baff1415 316709e5 e8a7cc57 92378c5c f4ba7804 9b3426ae
sp058 a 0f5ed627 d527f20f 200b3924 1e33cbe9 f9d073ff 30fb3060 c9bed0ac bc91b047 4c84f4a4 318e1c7a f4b1037b 4c5e18a3 1d1fa7dd adcb78e7 4cd7cae5 947fc049 61c121d1 f02293fa 2a273c19 716da9ec f9f25dda 4196c67d d44f6d8f 57a7f58e
sp058 b 0f5ed627 d527f20f 200b3924 1e33cbe9 f9d06405 307b3061 d89ec0a9 bc91b043 4c84f4a4 318e9c7e f4b1037b 4c5e18a3 1d1f97e3 adc3f8e6 9c5fce6c d97f484d 61c121d9 dfa31402 3ae73c11 716d29e4 f9f2ddde 4196c67d d44f6d8f 57a7f58e
sp059 a 2d890601 d4a4c00a b8a4be2d a58becfc 056fbbfe 60dab770 8327383e ee307c04 58f31f41 39ca3db9 2b4fe6b4 fdfab915 1d1fafdd af8b7ae7 4c97cbe5 946f8048 61d521d1 7026b3fa aa373c19 b17781e9 e0b74853 9a0baaee 1b473542 5c2f5f8f
sp059 b 2d890601 d4a4c00a b8a4be2d a58becfc 056fac04 605ab771 9207283b ee307c00 58f31f41 39cabdbd 2b4fe6b4 fdfab915 1d1f9fe3 af83fae6 9c1fcf6c d96f084c 61d521d9 5fa73402 baf73c11 b17701e1 e0b7c857 9a0baaee 1b473542 5c2f5f8f
sp060 a f141dbe9 eaef99c5 00396fff 7bd63536 066f93fe 679d46ba 8d6bf87e ef68cd86 bfaace2b ed841990 f3fc3b0f d6957e5f 1d1fa7dd afe978e7 4c97cbe5 947fc049 61d541d1 7026b3fa aa3f3c19 f1e581ed eba75ddb 930b1d17 10fa5501 9f546d10
sp060 b f141dbe9 eaef99c5 00396fff 7bd63536 066f8404 671d46bb 9c4be87b ef68cd82 bfaace2b ed849994 f3fc3b0f d6957e5f 1d1f97e3 afe1f8e6 9c1fcf6c d97f484d 61d541d9 5fa73402 baff3c11 f1e501e5 eba7dddf 930b1d17 10fa5501 9f546d10
sp061 a 101e9706 f14cd806 beffa23e 2accd0f2 062f93fe 8d9f637a 61665bb4 cb764fae 3bad2d05 e06422ea 73eaa831 11c392f2 1d1fafdd afc87ae7 4c97cbe5 947f8048 61d101d1 7026b3fa aa27341d b17bc9e9 e7e31253 6b09eee0 3cec29d0 964993c4
sp061 b 101e9706 f14cd806 beffa23e 2accd0f2 062f8404 8d1f637b 70464bb1 cb764faa 3bad2d05 e064a2ee 73eaa831 11c392f2 1d1f9fe3 afc0fae6 9c1fcf6c d97f084c 61d101d9 5fa73402 bae73415 b17b49e1 e7e39257 6b09eee0 3cec29d0 964993c4
sp062 a e8f1a6f3 b0df6505 6ff7ab19 f68a19d4 066f93fe 03dee258 4d2d7b16 a36ac86c 1f6e83ef 5e5f6502 3e917532 90d17fdb 1d1fafdd adaa7be7 4c97cbe5 946f8048 61d111d1 f02293fa aa3f0c18 b1fb81e8 e1b35f53 76fc4ec4 d148c225 27451263
sp062 b e8f1a6f3 b0df6505 6ff7ab19 f68a19d4 066f8404 035ee259 5c0d6b13 a36ac868 1f6e83ef 5e5fe506 3e917532 90d17fdb 1d1f9fe3 ada2fbe6 9c1fcf6c d96f084c 61d111d9 dfa31402 baff0c10 b1fb01e0 e1b3df57 76fc4ec4 d148c225 27451263
sp063 a ff30974c 658ef48b a41b3d90 b0584759 f9d07bff 58f734d0 0db9521c b49b3747 c0863600 34ca3fe1 ebccceb7 daa393a6 1d1fa7dd adc979e7 4c97cbe5 943bc249 61d503d1 7026b3fa aa373c18 f1f9d9e8 980a3c52 63f62f01 90e4f962 da5ab8c9
sp063 b ff30974c 658ef48b a41b3d90 b0584759 f9d06c05 587734d1 1c994219 b49b3743 c0863600 34cabfe5 ebccceb7 daa393a6 1d1f97e3 adc1f9e6 9c1fcf6c d93b4a4d 61d503d9 5fa73402 baf73c10 f1f959e0 980abc56 63f62f01 90e4f962 da5ab8c9
sp064 a e7f34d07 e2424ebb 36e9a5c7 9303df13 fa9053ff 9dfe449a 2bf9925c 3bca4007 8b0640ac bc9609a1 33d29290 0386fd80 1d1fafdd adaa7be7 4c97cbe5 947f8048 61d101d1 f02293fa 2a37041d b17bc1e8 f5825152 dcc4ecc0 7264b2e4 20020de8
sp064 b e7f34d07 e2424ebb 36e9a5c7 9303df13 fa904405 9d7e449b 3ad98259 3bca4003 8b0640ac bc9689a5 33d29290 0386fd80 1d1f9fe3 ada2fbe6 9c1fcf6c d97f084c 61d101d9 dfa31402 3af70415 b17b41e0 f582d156 dcc4ecc0 7264b2e4 20020de8
sp065 a 0cf77975 a60d7001 72630617 ae80bcc2 056fb3fa ce83ef4e 2f64398e cc710f54 b83e6293 512f07f9 2ab0901d 254df257 1d1fa7dd ade978e7 4cd7cae5 943bc249 61c573d3 7026b3fa aa371418 b17bf9e9 8c5b7559 ee2136d1 6ef9baee 81f2c016
sp065 b 0cf77975 a60d7001 72630617 ae80bcc2 056fa400 ce03ef4f 3e44298b cc710f50 b83e6293 512f87fd 2ab0901d 254df257 1d1f97e3 ade1f8e6 9c5fce6c d93b4a4d 61c573db 5fa73402 baf71410 b17b79e1 8c5bf55d ee2136d1 6ef9baee 81f2c016
sp066 a dd6d3423 19ea048f 9e74e4a5 160b5e69 f9d07bff 94b525e0 21b2d4ac 9683e007 e6c0ccba e146217b 5a4a7d95 118c7ffc 1d1fa7dd afea7be7 4cd7cae5 947fc049 61c111d1 f02293fa aa2f041c 31ffd9e9 f7f242da dbd5cd3b fc632192 cb9bd2a7
sp066 b dd6d3423 19ea048f 9e74e4a5 160b5e69 f9d06c05 943525e1 3092c4a9 9683e003 e6c0ccba e146a17f 5a4a7d95 118c7ffc 1d1f97e3 afe2fbe6 9c5fce6c d97f484d 61c111d9 dfa31402 baef0414 31ff59e1 f7f2c2de dbd5cd3b fc632192 cb9bd2a7
sp067 a 92e80be7 ff006286 8b8584a2 646abe6f f9d073fb baed0de6 2ff3952c 58cb022f 8e1c4eb6 eb1a45b9 8284f3bb 9202fe38 1d1fa7dd afc87be7 4cd7cae5 947b8048 61c101d3 f02293fa aa3f1418 f1fdf1e9 f1f649d8 bd77e474 ee36c10d b1df483c
sp067 b 92e80be7 ff006286 8b8584a2 646abe6f f9d06401 ba6d0de7 3ed38529 58cb022b 8e1c4eb6 eb1ac5bd 8284f3bb 9202fe38 1d1f97e3 afc0fbe6 9c5fce6c d97b084c 61c101db dfa31402 baff1410 f1fd71e1 f1f6c9dc bd77e474 ee36c10d b1df483c
sp068 a 869fa908 1b9a0ffa ddf08a25 97cb58f0 056fb3fe ca9e4378 4722bbbe 0a734c3c 54e46bcb 86b34cc2 748b81d5 39a7c96e 1d1fa7dd afe878e7 4cd7cae5 943b8248 61d563d1 f02293fa aa2f0419 71e9b9ec 866b64db 703c3fe6 d737887e 8c6a34f7
sp068 b 869fa908 1b9a0ffa ddf08a25 97cb58f0 056fa404 ca1e4379 5602abbb 0a734c38 54e46bcb 86b3ccc6 748b81d5 39a7c96e 1d1f97e3 afe0f8e6 9c5fce6c d93b0a4c 61d563d9 dfa31402 baef0411 71e939e4 866be4df 703c3fe6 d737887e 8c6a34f7
sp069 a fbf6b59d c2d1910d 71fc7721 dc930dec 066f9bfe 21dd3660 af2a38a6 a5791b06 95e25795 443e05c0 c7918c8b 2524dd18 1d1fa7dd afab79e7 4c97cbe5 947f8048 61d141d1 7026b3fa 2a270c1d 316381ed e7a35353 d7095bf2 6f2824de 3e2a710f
sp069 b fbf6b59d c2d1910d 71fc7721 dc930dec 066f8c04 215d3661 be0a28a3 a5791b02 95e25795 443e85c4 c7918c8b 2524dd18 1d1f97e3 afa3f9e6 9c1fcf6c d97f084c 61d141d9 5fa73402 3ae70c15 316301e5 e7a3d357 d7095bf2 6f2824de 3e2a710f
sp070 a e23776cf 45520e5b 7769655f b1569f8f fa9053ff 7bfb0402 23fd954c b3d94037 238521e0 ab6c663b 14a59b44 aa9a88c4 1d1fa7dd ade87ae7 4c97cbe5 946b8048 61d161d1 f02293fa 2a37241d f169d1ec eb9708d2 feaa6dd4 7a74cff4 e7e4dd40
sp070 b e23776cf 45520e5b 7769655f b1569f8f fa904405 7b7b0403 32dd8549 b3d94033 238521e0 ab6ce63f 14a59b44 aa9a88c4 1d1f97e3 ade0fae6 9c1fcf6c d96b084c 61d161d9 dfa31402 3af72415 f16951e4 eb9788d6 feaa6dd4 7a74cff4 e7e4dd40
sp071 a c6f95457 fc514ed6 6f36a6dd 9d9dbc0c 052fb3fa 60cb0f84 2b20b8ce e667cfa4 9a7580ab ef844b13 1fbe5845 e7ea79e5 1d1fa7dd af8879e7 4c97cbe5 947f8048 61c151d3 7026b3fa aa272418 b1f781e9 e8d34b59 98064590 7331acaf 703b8e8d
sp071 b c6f95457 fc514ed6 6f36a6dd 9d9dbc0c 052fa400 604b0f85 3a00a8cb e667cfa0 9a7580ab ef84cb17 1fbe5845 e7ea79e5 1d1f97e3 af80f9e6 9c1fcf6c d97f084c 61c151db 5fa73402 bae72410 b1f701e1 e8d3cb5d 98064590 7331acaf 703b8e8d
sp072 a fd92fd2f 933af106 b8a63401 015fcecd f9d073fb f4ea3d44 05b45384 d4cf9095 0cd1b666 76eb7c61 0c977292 73f97fe3 1d1fafdd adea79e7 4c97cbe5 943bc249 61d503d3 f02293fa aa3f2419 f175a9e9 980a3c58 3f9e058d 18f5cfb5 39ba3e1c
sp072 b fd92fd2f 933af106 b8a63401 015fcecd f9d06401 f46a3d45 14944381 d4cf9091 0cd1b666 76ebfc65 0c977292 73f97fe3 1d1f9fe3 ade2f9e6 9c1fcf6c d93b4a4d 61d503db dfa31402 baff2411 f17529e1 980abc5c 3f9e058d 18f5cfb5 39ba3e1c
sp073 a fa665545 9acd9806 99e5ff21 d884edec 066f9bfa 8bc81e64 2f2e38a6 c17d1d26 93eb79a3 6bca7eb8 85c78167 28809edc 1d1fa7dd ad8b78e7 4c97cbe5 947b8048 61d121d3 f02293fa 2a3f1c19 71e9f1ed e7a744d9 e6ca157a 6f3c2494 4f4d0e2b
sp073 b fa665545 9acd9806 99e5ff21 d884edec 066f8c00 8b481e65 3e0e28a3 c17d1d22 93eb79a3 6bcafebc 85c78167 28809edc 1d1f97e3 ad83f8e6 9c1fcf6c d97b084c 61d121db dfa31402 3aff1c11 71e971e5 e7a7c4dd e6ca157a 6f3c2494 4f4d0e2b
sp074 a 527da152 a954e059 420dba7e e4a988ae 052fb3fe ead59322 65665de4 8436b95e f224dd2b f01a07ea 205e068d 61ca0007 1d1fafdd af887ae7 4cd7cae5 946b8048 61c101d1 7026b3fa aa3f1c1d f17df9e8 dea740d3 06138138 38d410a0 19a39bb0
sp074 b 527da152 a954e059 420dba7e e4a988ae 052fa404 ea559323 74464de1 8436b95a f224dd2b f01a87ee 205e068d 61ca0007 1d1f9fe3 af80fae6 9c5fce6c d96b084c 61c101d9 5fa73402 baff1c15 f17d79e0 dea7c0d7 06138138 38d410a0 19a39bb0
sp075 a bc2993ff 8c5f3fcd 18652ff3 27fe3d3e 066f9bfe 07dea6b2 0b6eb9f6 6b386e26 712a426f 39ab1bbb d7d0b3a1 e2219ca0 1d1fa7dd adca78e7 4cd7cae5 943bc249 61d553d1 7026b3fa aa373c18 317be1e9 8b6b6d53 b535bce9 92ef8288 633f49eb
sp075 b bc2993ff 8c5f3fcd 18652ff3 27fe3d3e 066f8c04 075ea6b3 1a4ea9f3 6b386e22 712a426f 39ab9bbf d7d0b3a1 e2219ca0 1d1f97e3 adc2f8e6 9c5fce6c d93b4a4d 61d553d9 5fa73402 baf73c10 317b61e1 8b6bed57 b535bce9 92ef8288 633f49eb
sp076 a 77ea2b01 1a0a9981 3a15e7a8 f2bc5d78 056fbbfa a8830ef4 052f583c 24698f2e d6e88e2b f2e96ec9 cb38253e 9c19348c 1d1fa7dd afeb7ae7 4cd7cae5 942bc249 61d543d3 7026b3fa 2a2f041d 71ede9ed 827b7b59 0a3853e5 1936bc45 0413ffc3
sp076 b 77ea2b01 1a0a9981 3a15e7a8 f2bc5d78 056fac00 a8030ef5 140f4839 24698f2a d6e88e2b f2e9eecd cb38253e 9c19348c 1d1f97e3 afe3fae6 9c5fce6c d92b4a4d 61d543db 5fa73402 3aef0415 71ed69e5 827bfb5d 0a3853e5 1936bc45 0413ffc3
sp077 a 702acba7 ba9030c9 133dced2 11883c06 052fbbfe e4db478a 2765194c 003fadf6 9228e621 8397485b 041a7fe6 0b1d798f 1d1fafdd ade979e7 4c97cbe5 947b8048 61d161d1 7026b3fa aa270c1d 717991e8 e8e75bd3 15bd4b4c 76ed2438 216dce5a
sp077 b 702acba7 ba9030c9 133dced2 11883c06 052fac04 e45b478b 36450949 003fadf2 9228e621 8397c85f 041a7fe6 0b1d798f 1d1f9fe3 ade1f9e6 9c1fcf6c d97b084c 61d161d9 5fa73402 bae70c15 717911e0 e8e7dbd7 15bd4b4c 76ed2438 216dce5a
sp078 a 9661ae91 88d7358e faed8281 1c88f84c 062f93fe e39503c0 cb253d06 0926a906 77a8c229 475b6152 9cfe63a6 4459696d 1d1fa7dd ad8a78e7 4c97cbe5 947f8048 61d531d1 f02293fa 2a371418 b1ffc9e8 e9e74c53 99464060 d3390835 47917aa6
sp078 b 9661ae91 88d7358e faed8281 1c88f84c 062f8404 e31503c1 da052d03 0926a902 77a8c229 475be156 9cfe63a6 4459696d 1d1f97e3 ad82f8e6 9c1fcf6c d97f084c 61d531d9 dfa31402 3af71410 b1ff49e0 e9e7cc57 99464060 d3390835 47917aa6
sp079 a a6b7dbe0 79a84a09 1a136729 96ff95fc 052fb3fe ead62670 0b2f393e 007a8ce4 f42cab33 1bb35b39 81936d46 8b087e07 1d1fa7dd adca7ae7 4c97cbe5 946b8048 61d101d1 f02293fa 2a3f2c19 71e9d1ec e0f748d3 8fdd0bea 934b33fe 1047adb4
sp079 b a6b7dbe0 79a84a09 1a136729 96ff95fc 052fa404 ea562671 1a0f293b 007a8ce0 f42cab33 1bb3db3d 81936d46 8b087e07 1d1f97e3 adc2fae6 9c1fcf6c d96b084c 61d101d9 dfa31402 3aff2c11 71e951e4 e0f7c8d7 8fdd0bea 934b33fe 1047adb4
sp080 a c6aff1ea f6c0140f 1ef2d135 970dabf9 f9d07bff b8fd9070 43be16bc 54c5909d 8087dde6 c80f018b e95c5e2a df3a6dc2 1d1fa7dd af8878e7 4cd7cae5 947fc049 61c111d1 f02293fa aa37341d 3177a9e8 f7f245da b7ef65ab da600f83 050a54d3
sp080 b c6aff1ea f6c0140f 1ef2d135 970dabf9 f9d06c05 b87d9071 529e06b9 54c59099 8087dde6 c80f818f e95c5e2a df3a6dc2 1d1f97e3 af80f8e6 9c5fce6c d97f484d 61c111d9 dfa31402 baf73415 317729e0 f7f2c5de b7ef65ab da600f83 050a54d3
sp081 a 1fbae9d3 31100dca 1583c5c7 15769f0f f9d07bfb f2af8c86 8ff91244 d0952565 464c04ce cc463602 fa61fa9a dcbea152 1d1fa7dd ada87ae7 4cd7cae5 947f8048 61c121d3 7026b3fa aa370418 f169c9ed f5f25258 07c98758 0e292439 bd710e4c
sp081 b 1fbae9d3 31100dca 1583c5c7 15769f0f f9d06c01 f22f8c87 9ed90241 d0952561 464c04ce cc46b606 fa61fa9a dcbea152 1d1f97e3 ada0fae6 9c5fce6c d97f084c 61c121db 5fa73402 baf70410 f16949e5 f5f2d25c 07c98758 0e292439 bd710e4c
sp082 a dc00252c 6ac2b08d 1e637ea1 04f50c6c 066f93fe eb9417e0 0b273f26 81729c9e 7576b62f 3d081633 b30d7c6a 60010132 1d1fa7dd afcb79e7 4cd7cae5 943b8248 61d553d1 7026b3fa 2a3f0419 31fff9e8 856b73db cf7f8abc 133f055a 4f9d7251
sp082 b dc00252c 6ac2b08d 1e637ea1 04f50c6c 066f8404 eb1417e1 1a072f23 81729c9a 7576b62f 3d089637 b30d7c6a 60010132 1d1f97e3 afc3f9e6 9c5fce6c d93b0a4c 61d553d9 5fa73402 3aff0411 31ff79e0 856bf3df cf7f8abc 133f055a 4f9d7251
sp083 a 81435d46 c75ecb06 5dd8af00 3ebaddcc 066f93fa a58b8e44 8b29990c 29768cec bba0a44f c3c07cfa 21cc0231 55b65be2 1d1fafdd adeb79e7 4cd7cae5 943bc249 61d553d3 7026b3fa aa3f041d 7179f9e8 8b6b6c59 0f27d557 133c6b75 f4834440
sp083 b 81435d46 c75ecb06 5dd8af00 3ebaddcc 066f8400 a50b8e45 9a098909 29768ce8 bba0a44f c3c0fcfe 21cc0231 55b65be2 1d1f9fe3 ade3f9e6 9c5fce6c d93b4a4d 61d553db 5fa73402 baff0415 717979e0 8b6bec5d 0f27d557 133c6b75 f4834440
sp084 a 02d74871 4c517a46 9655fd41 8d130f89 f9d073fb 1eecbc04 a9bdd54c 3884b227 ee81f82a f6d369e3 fdf83a27 06ec26a4 1d1fafdd ad8878e7 4cd7cae5 943bc249 61d543d3 f02293fa aa273418 71f5e1e9 984a7d58 161d88d5 74945eec 5e5ce7c7
sp084 b 02d74871 4c517a46 9655fd41 8d130f89 f9d06401 1e6cbc05 b89dc549 3884b223 ee81f82a f6d3e9e7 fdf83a27 06ec26a4 1d1f9fe3 ad80f8e6 9c5fce6c d93b4a4d 61d543db dfa31402 bae73410 71f561e1 984afd5c 161d88d5 74945eec 5e5ce7c7
sp085 a 915df6d1 85f8b006 6a0d560e c0dbecc2 062f9bfe 4bd3d74a 8d61d804 47237e0e 973c5365 3b1e521b 5b599ec0 cc8a8231 1d1fa7dd afa878e7 4c97cbe5 947f8048 61c531d1 f02293fa aa27041d 71e1f1ed e7d74453 26e92ed6 90ec5d3c 5afe8e26
sp085 b 915df6d1 85f8b006 6a0d560e c0dbecc2 062f8c04 4b53d74b 9c41c801 47237e0a 973c5365 3b1ed21f 5b599ec0 cc8a8231 1d1f97e3 afa0f8e6 9c1fcf6c d97f084c 61c531d9 dfa31402 bae70415 71e171e5 e7d7c457 26e92ed6 90ec5d3c 5afe8e26
sp086 a 99b4633d 123ab2c2 b2d9d8fa 48780a33 f99073ff b6bc51ba 63f290fc 94d01437 240d1e6e ac423621 bd51f270 03f6f8fb 1d1fafdd afca79e7 4cd7cae5 943b8248 61d503d1 f02293fa aa3f041d f16d81ec 924a3bda 842bf218 ba77b344 8921d4fc
sp086 b 99b4633d 123ab2c2 b2d9d8fa 48780a33 f9906405 b63c51bb 72d280f9 94d01433 240d1e6e ac42b625 bd51f270 03f6f8fb 1d1f9fe3 afc2f9e6 9c5fce6c d93b0a4c 61d503d9 dfa31402 baff0415 f16d01e4 924abbde 842bf218 ba77b344 8921d4fc
sp087 a 43be9442 4d2427cd 0aba72c3 78ce880e 066f93fe 0b9a1382 c364bcce e377db24 5d6eb853 570f40d2 6c9c50ae 1a1d3116 1d1fa7dd adab78e7 4c97cbe5 947bc049 61d131d1 f02293fa 2a3f1418 316ff1ed eba75d5b 6f20211d db05486c e8b40f8c
sp087 b 43be9442 4d2427cd 0aba72c3 78ce880e 066f8404 0b1a1383 d244accb e377db20 5d6eb853 570fc0d6 6c9c50ae 1a1d3116 1d1f97e3 ada3f8e6 9c1fcf6c d97b484d 61d131d9 dfa31402 3aff1410 316f71e5 eba7dd5f 6f20211d db05486c e8b40f8c
sp088 a 6ae491b4 0e1ac9c7 35202ce3 5f43be2f f99073fb 3ce52da6 0bf71364 b4c1014d 08826fc4 31c03958 954cfa91 90b0e701 1d1fafdd ad8b78e7 4c97cbe5 947f8048 61d511d3 f02293fa aa2f0419 b17b99e8 f6864458 37c515f6 125f21d6 216ab3e0
sp088 b 6ae491b4 0e1ac9c7 35202ce3 5f43be2f f9906401 3c652da7 1ad70361 b4c10149 08826fc4 31c0b95c 954cfa91 90b0e701 1d1f9fe3 ad83f8e6 9c1fcf6c d97f084c 61d511db dfa31402 baef0411 b17b19e0 f686c45c 37c515f6 125f21d6 216ab3e0
sp089 a 92b9b1f0 a3a98af6 b06c3e26 1e8a0cf6 052fbbfa 00845f7e 0b6699bc cc7b1cc6 1e6753af 45b909d2 2716e2d0 b0fb9198 1d1fafdd af8b7be7 4c97cbe5 947f8048 61d531d3 7026b3fa aa273c1c 316fa9ed e8e71959 f21a00a2 92e7c3c5 191ca74e
sp089 b 92b9b1f0 a3a98af6 b06c3e26 1e8a0cf6 052fac00 00045f7f 1a4689b9 cc7b1cc2 1e6753af 45b989d6 2716e2d0 b0fb9198 1d1f9fe3 af83fbe6 9c1fcf6c d97f084c 61d531db 5fa73402 bae73c14 316f29e5 e8e7995d f21a00a2 92e7c3c5 191ca74e
sp090 a bd718143 60dadb0a d7687710 518a6dc4 056fb3fe 44dc5648 8d29df04 c431388c 52277a99 0d150313 7103dc05 7155864c 1d1fafdd afe879e7 4c97cbe5 943bc249 61d573d1 7026b3fa 2a271c18 3163f9ec 8a6b6c53 760a0bd7 91641c7a 141e5944
sp090 b bd718143 60dadb0a d7687710 518a6dc4 056fa404 445c5649 9c09cf01 c4313888 52277a99 0d158317 7103dc05 7155864c 1d1f9fe3 afe0f9e6 9c1fcf6c d93b4a4d 61d573d9 5fa73402 3ae71c10 316379e4 8a6bec57 760a0bd7 91641c7a 141e5944
sp091 a eada09eb 1b245f8d b2866a83 f4d7b84e 066f93fe e99003c2 63653d06 e72b69a6 97e24007 dabe4a8a ba4fb3d3 7469f329 1d1fafdd adc878e7 4c97cbe5 947fc049 61d531d1 7026b3fa 2a373c19 71e5a9ec eda745db 1311605d baf8e079 25825a2f
sp091 b eada09eb 1b245f8d b2866a83 f4d7b84e 066f8404 e91003c3 72452d03 e72b69a2 97e24007 dabeca8e ba4fb3d3 7469f329 1d1f9fe3 adc0f8e6 9c1fcf6c d97f484d 61d531d9 5fa73402 3af73c11 71e529e4 eda7c5df 1311605d baf8e079 25825a2f
sp092 a c4439bb3 0e0b4187 94d0c4af 7a2bde63 f9d07bff faf345ea 0ff7132c 5cc4031f a6c32694 958a1e53 6e798499 9531fcb2 1d1fa7dd afc978e7 4cd7cae5 942b8248 61d503d1 7026b3fa aa272c1c b1e381ed 8a1a7ada c00a1ee8 8e676957 0993a539
sp092 b c4439bb3 0e0b4187 94d0c4af 7a2bde63 f9d06c05 fa7345eb 1ed70329 5cc4031b a6c32694 958a9e57 6e798499 9531fcb2 1d1f97e3 afc1f8e6 9c5fce6c d92b0a4c 61d503d9 5fa73402 bae72c14 b1e301e5 8a1afade c00a1ee8 8e676957 0993a539
sp093 a 2cb286a1 79f10a46 8e1eb37e 5fcbe1b2 062f93fe e1db523a 4b6e1cf4 c52cbef4 91269293 ba154488 cfc03915 c3793b04 1d1fa7dd ad887ae7 4cd7cae5 947f8048 61d131d1 f02293fa 2a371c19 31e7c1ec e9a34a53 9901e066 52b03148 07975d5e
sp093 b 2cb286a1 79f10a46 8e1eb37e 5fcbe1b2 062f8404 e15b523b 5a4e0cf1 c52cbef0 91269293 ba15c48c cfc03915 c3793b04 1d1f97e3 ad80fae6 9c5fce6c d97f084c 61d131d9 dfa31402 3af71c11 31e741e4 e9a3ca57 9901e066 52b03148 07975d5e
sp094 a 9aa940ed 5eabd84e 01562365 08fd71a8 062f93fe ef910220 c92a7ae6 27346e54 f5a74ae1 1d0a1512 9db0fce7 6c08fd3f 1d1fa7dd ad8978e7 4cd7cae5 946f8048 61d101d1 7026b3fa 2a2f041d 31f7c1e8 e1b35a53 0b67523a 54ffdb9e c10f7c9b
sp094 b 9aa940ed 5eabd84e 01562365 08fd71a8 062f8404 ef110221 d80a6ae3 27346e50 f5a74ae1 1d0a9516 9db0fce7 6c08fd3f 1d1f97e3 ad81f8e6 9c5fce6c d96f084c 61d101d9 5fa73402 3aef0415 31f741e0 e1b3da57 0b67523a 54ffdb9e c10f7c9b
sp095 a 90ec5201 2b9cb95a 0b92b27e 23e008ae 056fb3fe 2693b322 c7621de4 ce7c5af4 3826301d 6e1953a2 b4dcfe83 ca6aa90b 1d1fa7dd ade979e7 4c97cbe5 946f8048 61d111d1 7026b3fa aa271c19 f1f9f9e8 e2b34953 d40c9ffa d7003f9c c445db1a
sp095 b 90ec5201 2b9cb95a 0b92b27e 23e008ae 056fa404 2613b323 d6420de1 ce7c5af0 3826301d 6e19d3a6 b4dcfe83 ca6aa90b 1d1f97e3 ade1f9e6 9c1fcf6c d96f084c 61d111d9 5fa73402 bae71c11 f1f979e0 e2b3c957 d40c9ffa d7003f9c c445db1a
sp096 a c3f9fcfa fe0ee942 7e29365a 1df34c92 062f93fe 6ddbd71a 29645fd4 09731806 132572a5 cfd76932 b4018c33 c9aeffe9 1d1fafdd ad8b7be7 4c97cbe5 946f8048 61d511d1 f02293fa 2a270419 b16fa1ec e1f75f53 0f1e6a82 74f9d568 4accc5ed
sp096 b c3f9fcfa fe0ee942 7e29365a 1df34c92 062f8404 6d5bd71b 38444fd1 09731802 132572a5 cfd7e936 b4018c33 c9aeffe9 1d1f9fe3 ad83fbe6 9c1fcf6c d96f084c 61d511d9 dfa31402 3ae70411 b16f21e4 e1f7df57 0f1e6a82 74f9d568 4accc5ed
sp097 a 9bf2db06 83e48c0e 4ef93907 4a7863cf f99073ff 94f29042 c3f81084 7091362d e2cc3a96 9af6798b cc12cde2 62e0861b 1d1fafdd ad8a78e7 4c97cbe5 947f8048 61d521d1 f02293fa aa2f3c1d 7175e9e8 f6865452 e7e0b41c 5a5e6cbc 3530cc65
sp097 b 9bf2db06 83e48c0e 4ef93907 4a7863cf f9906405 94729043 d2d80081 70913629 e2cc3a96 9af6f98f cc12cde2 62e0861b 1d1f9fe3 ad82f8e6 9c1fcf6c d97f084c 61d521d9 dfa31402 baef3c15 717569e0 f686d456 e7e0b41c 5a5e6cbc 3530cc65
sp098 a 358eb089 d0aba786 0a282381 54c4594c 066f9bfa c58f2ac4 e32dba0e e53f2e2c f52521cb 775261d3 d700db14 713dbb2e 1d1fa7dd afaa78e7 4c97cbe5 947f8048 61d541d3 f02293fa 2a2f041d 7171a9e8 e7a75459 ad145a0e bb288b30 427264c1
sp098 b 358eb089 d0aba786 0a282381 54c4594c 066f8c00 c50f2ac5 f20daa0b e53f2e28 f52521cb 7752e1d7 d700db14 713dbb2e 1d1f97e3 afa2f8e6 9c1fcf6c d97f084c 61d541db dfa31402 3aef0415 717129e0 e7a7d45d ad145a0e bb288b30 427264c1
sp099 a 5406404e b60896c7 d2b995f6 2823673b f99073fb 12e59cb6 a9fad5f4 94d5170f 024c10c6 14fd3b62 3fe3d2d0 09bfc8f0 1d1fa7dd afc87be7 4c97cbe5 947b8048 61d111d3 7026b3fa 2a3f341c 717581e8 f28659d8 dd8bb366 746f9f8d 86c8a61f
sp099 b 5406404e b60896c7 d2b995f6 2823673b f9906401 12659cb7 b8dac5f1 94d5170b 024c10c6 14fdbb66 3fe3d2d0 09bfc8f0 1d1f97e3 afc0fbe6 9c1fcf6c d97b084c 61d111db 5fa73402 3aff3414 717501e0 f286d9dc dd8bb366 746f9f8d 86c8a61f
sp100 a 5b706162 fe8b0835 90bcaf42 7e9df592 052fb3fe 6691661a 0f6818d4 8223eadc 5c7aa24f 47ed6ef3 750d7ff0 1c825443 1d1fa7dd afea78e7 4c97cbe5 947f8048 61c151d1 7026b3fa 2a2f041d 71f999e9 e8d34c53 8a1deefa 0ef22cb0 a6218814
sp100 b 5b706162 fe8b0835 90bcaf42 7e9df592 052fa404 6611661b 1e4808d1 8223ead8 5c7aa24f 47edeef7 750d7ff0 1c825443 1d1f97e3 afe2f8e6 9c1fcf6c d97f084c 61c151d9 5fa73402 3aef0415 71f919e1 e8d3cc57 8a1deefa 0ef22cb0 a6218814
sp101 a 279d4900 9ccdc04e 52c86644 5dd03c8c 062f9bfe 47992700 8f211844 a361cc26 31a0a461 399b1a39 406f66a6 18f677b6 1d1fafdd ad8a78e7 4cd7cae5 947bc049 61d141d1 f02293fa aa270419 71f9d9e8 eba75d5b 336a0c51 8ef0edf7 ef4bda08
sp101 b 279d4900 9ccdc04e 52c86644 5dd03c8c 062f8c04 47192701 9e010841 a361cc22 31a0a461 399b9a3d 406f66a6 18f677b6 1d1f9fe3 ad82f8e6 9c5fce6c d97b484d 61d141d9 dfa31402 bae70411 71f959e0 eba7dd5f 336a0c51 8ef0edf7 ef4bda08
sp102 a 82977892 c53cea81 c54977a9 7ef44d7c 056fbbfa 0e803ef4 8b2e3fbe 0c7a9f7c 7cfeda0f e24d60ca 16bf2879 97330e79 1d1fafdd adeb7be7 4c97cbe5 947f8048 61c121d3 f02293fa aa272c19 31e7a9ed ea930959 6bb1b3ea 93202d7c 4641565b
sp102 b 82977892 c53cea81 c54977a9 7ef44d7c 056fac00 0e003ef5 9a0e2fbb 0c7a9f78 7cfeda0f e24de0ce 16bf2879 97330e79 1d1f9fe3 ade3fbe6 9c1fcf6c d97f084c 61c121db dfa31402 bae72c11 31e729e5 ea93895d 6bb1b3ea 93202d7c 4641565b
sp103 a 877b9806 e1ccf29b ec44a0ba a22fda6f fa905bff 15f4a1e2 6bf216a4 d5c50555 090363e0 b4c42ac3 ff99bb77 5c6bf665 1d1fa7dd ad887be7 4c97cbe5 947f8048 61d501d1 7026b3fa 2a3f0c18 31fb81e9 f5865152 e6f4bff8 b27446db f6e6e53b
sp103 b 877b9806 e1ccf29b ec44a0ba a22fda6f fa904c05 1574a1e3 7ad206a1 d5c50551 090363e0 b4c4aac7 ff99bb77 5c6bf665 1d1f97e3 ad80fbe6 9c1fcf6c d97f084c 61d501d9 5fa73402 3aff0c10 31fb01e1 f586d156 e6f4bff8 b27446db f6e6e53b
sp104 a 1c30b67c 65e6010a f4e59616 86f60cc2 056fbbfe aed0574a 2f649f84 a2745fcc 12613c77 07875cd1 3742a879 2affb363 1d1fafdd af8a7be7 4c97cbe5 947f8048 61d561d1 f02293fa aa273c18 b177e1e8 e8a74953 cc23290c eee9ddb7 33af7e45
sp104 b 1c30b67c 65e6010a f4e59616 86f60cc2 056fac04 ae50574b 3e448f81 a2745fc8 12613c77 0787dcd5 3742a879 2affb363 1d1f9fe3 af82fbe6 9c1fcf6c d97f084c 61d561d9 dfa31402 bae73c10 b17761e0 e8a7c957 cc23290c eee9ddb7 33af7e45
sp105 a 5a58851c 3585538a 91f4e496 4901be47 fad05bff b3fb65ca 25f0d284 5d85217f 650060a0 3f6d6093 0014a9fd 96c79ff4 1d1fafdd af8b7ae7 4cd7cae5 947f8048 61c101d1 7026b3fa 2a3f2c1c 71fd81e8 f2f24a52 3ceaae90 f839abff be98ab94
sp105 b 5a58851c 3585538a 91f4e496 4901be47 fad04c05 b37b65cb 34d0c281 5d85217b 650060a0 3f6de097 0014a9fd 96c79ff4 1d1f9fe3 af83fae6 9c5fce6c d97f084c 61c101d9 5fa73402 3aff2c14 71fd01e0 f2f2ca56 3ceaae90 f839abff be98ab94
sp106 a d6df9694 d752934a 7c075140 9079ab89 f9907bff 30bb9000 e3b9974c 5a93f39d 608095f0 d7ed7cd0 7f7e059d da721b85 1d1fafdd af8879e7 4c97cbe5 947fc049 61d521d1 f02293fa aa270419 31f7e9e8 f8864cda 4a19b35d 3a946def f813e291
sp106 b d6df9694 d752934a 7c075140 9079ab89 f9906c05 303b9001 f2998749 5a93f399 608095f0 d7edfcd4 7f7e059d da721b85 1d1f9fe3 af80f9e6 9c1fcf6c d97f484d 61d521d9 dfa31402 bae70411 31f769e0 f886ccde 4a19b35d 3a946def f813e291
sp107 a 0e77333e e2a028bd f6afcffa 90925d36 062f93fa 03ce6ebe 256fd87c 81382c04 fdee2ad9 a2e56fc8 69eef0b7 3e25ffbf 1d1fafdd afaa79e7 4cd7cae5 947f8048 61d541d3 7026b3fa 2a2f2c19 f16d91ed e7a75359 eed93514 f8a6a602 16e53093
sp107 b 0e77333e e2a028bd f6afcffa 90925d36 062f8400 034e6ebf 344fc879 81382c00 fdee2ad9 a2e5efcc 69eef0b7 3e25ffbf 1d1f9fe3 afa2f9e6 9c5fce6c d97f084c 61d541db 5fa73402 3aef2c11 f16d11e5 e7a7d35d eed93514 f8a6a602 16e53093
sp108 a 0011d982 f707afc5 b2b87eff ffcbec32 066f93fe 0dd1f7ba 23663ef6 836ada16 39bfb667 09533738 87950acb dbb87e42 1d1fafdd adc978e7 4cd7cae5 943bc249 61c553d1 7026b3fa aa372c19 71f9d1e9 8b5b6d53 a7432de1 7af7ed89 87a2cdbe
sp108 b 0011d982 f707afc5 b2b87eff ffcbec32 066f8404 0d51f7bb 32462ef3 836ada12 39bfb667 0953b73c 87950acb dbb87e42 1d1f9fe3 adc1f8e6 9c5fce6c d93b4a4d 61c553d9 5fa73402 baf72c11 71f951e1 8b5bed57 a7432de1 7af7ed89 87a2cdbe
sp109 a 3522e4df 449d150e d1173904 f058cbc9 f9907bff bcb01040 e1b9d10c f4d091d7 8ec1f638 adf13e90 905a5c36 36c93ddf 1d1fafdd afc87be7 4cd7cae5 942bc249 61d503d1 f02293fa aa3f1418 71f581e8 8e5a7252 7e4a3191 3cc0432e 96210494
sp109 b 3522e4df 449d150e d1173904 f058cbc9 f9906c05 bc301041 f099c109 f4d091d3 8ec1f638 adf1be94 905a5c36 36c93ddf 1d1f9fe3 afc0fbe6 9c5fce6c d92b4a4d 61d503d9 dfa31402 baff1410 71f501e0 8e5af256 7e4a3191 3cc0432e 96210494
sp110 a 6218999c cce86c8f c98b71a7 d9360b6f f9d073ff dcb7b0e2 4bfb1024 1494b2bd 46c3bcce d37073f9 5fda0f21 7b687780 1d1fafdd afc97be7 4cd7cae5 943b8248 61d503d1 f02293fa 2a270c18 f169f1ed 920a3bda 5e3190f0 52573c17 83bd86d7
sp110 b 6218999c cce86c8f c98b71a7 d9360b6f f9d06405 dc37b0e3 5adb0021 1494b2b9 46c3bcce d370f3fd 5fda0f21 7b687780 1d1f9fe3 afc1fbe6 9c5fce6c d93b0a4c 61d503d9 dfa31402 3ae70c10 f16971e5 920abbde 5e3190f0 52573c17 83bd86d7
sp111 a 3a94c3e5 5afc731a 5f078d1e 0561ffcf fad053ff d3f52442 03fc948c b99aa20f 8f94ce90 ac250380 76d92d84 bc123bcd 1d1fafdd afab79e7 4c97cbe5 943b8248 61d523d1 f02293fa 2a3f1c18 b1f3e1e9 914a7bda 67021f14 9aadc6af 935974bf
sp111 b 3a94c3e5 5afc731a 5f078d1e 0561ffcf fad04405 d3752443 12dc8489 b99aa20b 8f94ce90 ac258384 76d92d84 bc123bcd 1d1f9fe3 afa3f9e6 9c1fcf6c d93b0a4c 61d523d9 dfa31402 3aff1c10 b1f361e1 914afbde 67021f14 9aadc6af 935974bf
sp112 a a0761e0e d02fb2b5 ac838fe3 9ee97d32 052fb3fe 0a98c6ba 836abffe ee7e49bc 766a2fb5 d4880a61 2343915a 45f7da69 1d1fafdd ada87be7 4cd7cae5 946bc049 61c101d1 7026b3fa aa3f2419 b1e781ed e4a7405b e8304c9f 1acf7681 604940fb
sp112 b a0761e0e d02fb2b5 ac838fe3 9ee97d32 052fa404 0a18c6bb 924aaffb ee7e49b8 766a2fb5 d4888a65 2343915a 45f7da69 1d1f9fe3 ada0fbe6 9c5fce6c d96b484d 61c101d9 5fa73402 baff2411 b1e701e5 e4a7c05f e8304c9f 1acf7681 604940fb
sp113 a ba549578 cec274b3 068d05e5 703d3f31 fad053fb 71aa4cbc 87bf1474 95d3030f adc40420 9eb85901 0efee69e f7f2d945 1d1fa7dd adab7be7 4cd7cae5 943bc249 61d503d3 7026b3fa aa271419 b1f3e1e9 974a6458 43211415 168f1009 bd18d6dc
sp113 b ba549578 cec274b3 068d05e5 703d3f31 fad04401 712a4cbd 969f0471 95d3030b adc40420 9eb8d905 0efee69e f7f2d945 1d1f97e3 ada3fbe6 9c5fce6c d93b4a4d 61d503db 5fa73402 bae71411 b1f361e1 974ae45c 43211415 168f1009 bd18d6dc
sp114 a 2cc31857 6cfd80fa 25b0f607 25802cd6 056fbbfe 46d2f75a 8d657816 6a30ffec d0e79705 c4011162 9b372aaa 868f4ea2 1d1fafdd adeb7be7 4c97cbe5 943bc249 61d573d1 f02293fa 2a271c1c f16581ed 8c6b6453 f60c48c5 112c9328 3da417e5
sp114 b 2cc31857 6cfd80fa 25b0f607 25802cd6 056fac04 4652f75b 9c456813 6a30ffe8 d0e79705 c4019166 9b372aaa 868f4ea2 1d1f9fe3 ade3fbe6 9c1fcf6c d93b4a4d 61d573d9 dfa31402 3ae71c14 f16501e5 8c6be457 f60c48c5 112c9328 3da417e5
sp115 a 92184ae7 bcd73cc2 f6f6a4fa dd5dde33 f99073ff 10fc65ba 87f71574 9ede430d 060a2558 e9e02cbb 500fc745 a45fc924 1d1fafdd afaa7be7 4c97cbe5 943b8248 61c503d1 7026b3fa 2a270c18 b1ff81e9 927a3bda a20fbe18 9697460b ba158683
sp115 b 92184ae7 bcd73cc2 f6f6a4fa dd5dde33 f9906405 107c65bb 96d70571 9ede4309 060a2558 e9e0acbf 500fc745 a45fc924 1d1f9fe3 afa2fbe6 9c1fcf6c d93b0a4c 61c503d9 5fa73402 3ae70c10 b1ff01e1 927abbde a20fbe18 9697460b ba158683
sp116 a f03fb3bb 70c78fba 612aa7c6 df8e1d12 056fbbfe 6495e69a 2b691854 46356e04 76a26119 ce955e03 9c3695d6 5e50dfac 1d1fafdd afea78e7 4c97cbe5 943b8248 61c533d1 f02293fa 2a271419 f1e1d9ec 865b24db ce2a1f7e 73292ae8 4ec8842d
sp116 b f03fb3bb 70c78fba 612aa7c6 df8e1d12 056fac04 6415e69b 3a490851 46356e00 76a26119 ce95de07 9c3695d6 5e50dfac 1d1f9fe3 afe2f8e6 9c1fcf6c d93b0a4c 61c533d9 dfa31402 3ae71411 f1e159e4 865ba4df ce2a1f7e 73292ae8 4ec8842d
sp117 a cca9738c 902d3177 99b44c82 b041de53 fa9053ff f5ffe5da 0ff4949c 5981a28f 89caec38 6be96a3a d2967e24 c0301e05 1d1fafdd ad8878e7 4c97cbe5 947f8048 61d501d1 f02293fa 2a3f3c1c b16bb9ec f5865452 86e55f00 8e71e8a3 021672c6
sp117 b cca9738c 902d3177 99b44c82 b041de53 fa904405 f57fe5db 1ed48499 5981a28b 89caec38 6be9ea3e d2967e24 c0301e05 1d1f9fe3 ad80f8e6 9c1fcf6c d97f084c 61d501d9 dfa31402 3aff3c14 b16b39e4 f586d456 86e55f00 8e71e8a3 021672c6
sp118 a 553b851b 0d3e283a 0bc8c244 89e55094 056fb3fe 4c9d6318 cd25da5c ce7ecf9e 5cfae417 8c1802a1 bf7d0eb0 2dc553b9 1d1fafdd af8978e7 4c97cbe5 946fc049 61d511d1 f02293fa aa273c1d b16ba1ed e4b743db 2e5ee183 513852e3 1348cbf8
sp118 b 553b851b 0d3e283a 0bc8c244 89e55094 056fa404 4c1d6319 dc05ca59 ce7ecf9a 5cfae417 8c1882a5 bf7d0eb0 2dc553b9 1d1f9fe3 af81f8e6 9c1fcf6c d96f484d 61d511d9 dfa31402 bae73c15 b16b21e5 e4b7c3df 2e5ee183 513852e3 1348cbf8
sp119 a 9ade953d d0345253 8057e47b a0795eaf fad053fb 9fecad26 03f3946c fdc4018f e9de04ba 21be0ffb 5f9adfef e1adbeac 1d1fa7dd afab7ae7 4cd7cae5 947f8048 61c101d3 f02293fa 2a270c18 31efb9ed f2f25a58 d8954634 9a1ab9cd dae00403
sp119 b 9ade953d d0345253 8057e47b a0795eaf fad04401 9f6cad27 12d38469 fdc4018b e9de04ba 21be8fff 5f9adfef e1adbeac 1d1f97e3 afa3fae6 9c5fce6c d97f084c 61c101db dfa31402 3ae70c10 31ef39e5 f2f2da5c d8954634 9a1ab9cd dae00403
sp120 a 155787c9 6d0c7a1a cb9f5e1c 67ac64cc 056fb3fe 2a92b740 a3201f84 a4751fae 7ea85c29 0b456418 ecf5c3bd ae4cdf66 1d1fa7dd af8b7ae7 4c97cbe5 946bc049 61d111d1 7026b3fa 2a2f2419 31ffd9e9 e2b7595b ce6b9adb 7b4a05fb 344a74c5
sp120 b 155787c9 6d0c7a1a cb9f5e1c 67ac64cc 056fa404 2a12b741 b2000f81 a4751faa 7ea85c29 0b45e41c ecf5c3bd ae4cdf66 1d1f97e3 af83fae6 9c1fcf6c d96b484d 61d111d9 5fa73402 3aef2411 31ff59e1 e2b7d95f ce6b9adb 7b4a05fb 344a74c5
sp121 a f0ebbe1b db4b924e 98c4fb74 efe209bc 062f9bfe 4399b230 e32b1d7c 67217f94 1f601c79 380b17a9 6542b7ac 3679b86d 1d1fafdd afea78e7 4c97cbe5 947fc049 61d141d1 f02293fa 2a37141d b16be9ed ebe34ddb 35098121 bb32f7c3 f4a2669d
sp121 b f0ebbe1b db4b924e 98c4fb74 efe209bc 062f8c04 4319b231 f20b0d79 67217f90 1f601c79 380b97ad 6542b7ac 3679b86d 1d1f9fe3 afe2f8e6 9c1fcf6c d97f484d 61d141d9 dfa31402 3af71415 b16b69e5 ebe3cddf 35098121 bb32f7c3 f4a2669d
sp122 a b62e4feb 8c0cd806 f5ab8a3c 6fcb70f0 062f93fe 2b9d6378 eb279a3c c52a2ef4 352c0a47 5913121b 1f17ddb1 fe9498ba 1d1fa7dd afca7ae7 4c97cbe5 947fc049 61d501d1 7026b3fa aa3f0c1c b16be1ed ebe71bdb cf09ff61 b33e8346 9461dddf
sp122 b b62e4feb 8c0cd806 f5ab8a3c 6fcb70f0 062f8404 2b1d6379 fa078a39 c52a2ef0 352c0a47 5913921f 1f17ddb1 fe9498ba 1d1f97e3 afc2fae6 9c1fcf6c d97f484d 61d501d9 5fa73402 baff0c14 b16b61e5 ebe79bdf cf09ff61 b33e8346 9461dddf
sp123 a c2a46d63 8fefab5b ff52e55b a029378f fa905bff 77fe8402 87f91544 5bd9c685 c500e3d6 ec7723a2 ea04233b f56b0e61 1d1fafdd ada979e7 4c97cbe5 947b8048 61d101d1 f02293fa 2a273419 716df9ed f3865bd2 02c5af58 16595ff8 b8506f31
sp123 b c2a46d63 8fefab5b ff52e55b a029378f fa904c05 777e8403 96d90541 5bd9c681 c500e3d6 ec77a3a6 ea04233b f56b0e61 1d1f9fe3 ada1f9e6 9c1fcf6c d97b084c 61d101d9 dfa31402 3ae73411 716d79e5 f386dbd6 02c5af58 16595ff8 b8506f31
sp124 a e6161984 869cb14a 8726ef6f 49ce5dba 056fbbfe 0e9f0632 a16f797e 2e6bcdae d4adeb9d 245f2060 23bf0ebb 28c171d0 1d1fa7dd af8879e7 4c97cbe5 947fc049 61d121d1 f02293fa 2a27341d f161e1ed eca314db 6a362dab fcdebbc1 752e0e07
sp124 b e6161984 869cb14a 8726ef6f 49ce5dba 056fac04 0e1f0633 b04f697b 2e6bcdaa d4adeb9d 245fa064 23bf0ebb 28c171d0 1d1f97e3 af80f9e6 9c1fcf6c d97f484d 61d121d9 dfa31402 3ae73415 f16161e5 eca394df 6a362dab fcdebbc1 752e0e07
sp125 a 486e8e34 0eb17302 d656393d 8d3a83f5 f9d073fb 9cef787c 6dbad0bc 7acad79f 2e06beee a7cd7972 42bf1603 3a1c0e21 1d1fafdd adea79e7 4cd7cae5 943bc249 61d543d3 7026b3fa 2a273c19 f169c9ec 980a7c58 17bceb5d b0937bc1 199a8a34
sp125 b 486e8e34 0eb17302 d656393d 8d3a83f5 f9d06401 9c6f787d 7c9ac0b9 7acad79b 2e06beee a7cdf976 42bf1603 3a1c0e21 1d1f9fe3 ade2f9e6 9c5fce6c d93b4a4d 61d543db 5fa73402 3ae73c11 f16949e4 980afc5c 17bceb5d b0937bc1 199a8a34
sp126 a 77830ee0 c278a77a fb1b4286 d3beb852 056fb3fe 60d5c3da 65655d14 8a60cbce 3c7a878d 55171672 dbcb0b42 453b3d43 1d1fa7dd afaa78e7 4c97cbe5 942b8248 61c113d1 f02293fa aa2f3c18 b177e9e8 7ea752db d036323a b9450e27 48273543
sp126 b 77830ee0 c278a77a fb1b4286 d3beb852 056fa404 6055c3db 74454d11 8a60cbca 3c7a878d 55179676 dbcb0b42 453b3d43 1d1f97e3 afa2f8e6 9c1fcf6c d92b0a4c 61c113d9 dfa31402 baef3c10 b17769e0 7ea7d2df d036323a b9450e27 48273543
sp127 a 3e3ae88a 48c1ef85 656176bc 66ee2c74 066f9bfe ab9bf7f8 092258b4 87377eec f1e738eb ed7823b2 4cd3a6e7 c2c49ff7 1d1fa7dd adea7ae7 4c97cbe5 946fc049 61d101d1 7026b3fa 2a371c19 b173e9e9 e5b351db 4efb5a61 154fd4cb c524a562
sp127 b 3e3ae88a 48c1ef85 656176bc 66ee2c74 066f8c04 ab1bf7f9 180248b1 87377ee8 f1e738eb ed78a3b6 4cd3a6e7 c2c49ff7 1d1f97e3 ade2fae6 9c1fcf6c d96f484d 61d101d9 5fa73402 3af71c11 b17369e1 e5b3d1df 4efb5a61 154fd4cb c524a562
sp128 a a5dcf2d0 ec58d8c5 8217e6fa 43bf1436 066f93fe 659567ba 0367997c ad740d7e 91640d9b 24a51fc1 6f82eec5 5008c647 1d1fafdd af8a79e7 4c97cbe5 946f8048 61c101d1 f02293fa aa27141c b167f1ec dfa35153 0b4d8da0 1af6bbc3 382c1df2
sp128 b a5dcf2d0 ec58d8c5 8217e6fa 43bf1436 066f8404 651567bb 12478979 ad740d7a 91640d9b 24a59fc5 6f82eec5 5008c647 1d1f9fe3 af82f9e6 9c1fcf6c d96f084c 61c101d9 dfa31402 bae71414 b16771e4 dfa3d157 0b4d8da0 1af6bbc3 382c1df2
sp129 a 2c4f0e67 bf2fa7fe 53bd4639 368dfcf4 066f9bfa e78aef7c 8922f9be c9768cae 31a1e751 83374259 51447fd7 3443351f 1d1fa7dd afe87ae7 4c97cbe5 947f8048 61d541d3 f02293fa aa27041c b17f91e9 e7a75259 8ada9356 952b4b7f 1c190eff
sp129 b 2c4f0e67 bf2fa7fe 53bd4639 368dfcf4 066f8c00 e70aef7d 9802e9bb c9768caa 31a1e751 8337c25d 51447fd7 3443351f 1d1f97e3 afe0fae6 9c1fcf6c d97f084c 61d541db dfa31402 bae70414 b17f11e1 e7a7d25d 8ada9356 952b4b7f 1c190eff
sp130 a d3f7bc7c 3858165a 7a878559 f22ddf8d fad05bff d1fd8400 a7b812c4 f586216f 4b5c63d2 838f5efa 3059971d d1eeb41d 1d1fafdd afab7ae7 4cd7cae5 943bc249 61d523d1 7026b3fa aa37241d 3173e9e8 954a7552 e8fdde55 f6a601bf e47df043
sp130 b d3f7bc7c 3858165a 7a878559 f22ddf8d fad04c05 d17d8401 b69802c1 f586216b 4b5c63d2 838fdefe 3059971d d1eeb41d 1d1f9fe3 afa3fae6 9c5fce6c d93b4a4d 61d523d9 5fa73402 baf72415 317369e0 954af556 e8fdde55 f6a601bf e47df043
sp131 a 244204a3 a2b15c8f 0f752da6 696d176f f9d073ff 96b384e2 83ff942c 3ecd46bf ce406dbe 4811062b 9bc792d1 2b91bed0 1d1fa7dd afab7be7 4cd7cae5 947b8048 61c101d1 7026b3fa 2a3f341c b1e781ed f1f649d2 5a128e78 9a2af257 1d427676
sp131 b 244204a3 a2b15c8f 0f752da6 696d176f f9d06405 963384e3 92df8429 3ecd46bb ce406dbe 4811862f 9bc792d1 2b91bed0 1d1f97e3 afa3fbe6 9c5fce6c d97b084c 61c101d9 5fa73402 3aff3414 b1e701e5 f1f6c9d6 5a128e78 9a2af257 1d427676
sp132 a 7e55a77f aa6e4359 b22a7e58 ebb8ac8c 052fbbfe 88993700 23251844 08799eb6 f6afb017 cd8f1bb2 a64d1831 6c862663 1d1fafdd af887be7 4c97cbe5 947bc049 61d151d1 7026b3fa aa27341d f1f1f9e9 eae74a5b 70781913 7b2d1d3f 99bff4bb
sp132 b 7e55a77f aa6e4359 b22a7e58 ebb8ac8c 052fac04 88193701 32050841 08799eb2 f6afb017 cd8f9bb6 a64d1831 6c862663 1d1f9fe3 af80fbe6 9c1fcf6c d97b484d 61d151d9 5fa73402 bae73415 f1f179e1 eae7ca5f 70781913 7b2d1d3f 99bff4bb
sp133 a 49f5f1af a2c27c1a 93f3513e 064e8beb fad053ff bdbe9062 4dfed0ac f98f3035 27c01588 c61d5041 ca7dbf4f 3c4bca17 1d1fafdd adaa7ae7 4cd7cae5 947f8048 61c501d1 7026b3fa aa271c18 7161e1ec f4f65252 37089478 500f9dd3 1c7aed5c
sp133 b 49f5f1af a2c27c1a 93f3513e 064e8beb fad04405 bd3e9063 5cdec0a9 f98f3031 27c01588 c61dd045 ca7dbf4f 3c4bca17 1d1f9fe3 ada2fae6 9c5fce6c d97f084c 61c501d9 5fa73402 bae71c10 716161e4 f4f6d256 37089478 500f9dd3 1c7aed5c
sp134 a 27c6ce88 2273ef52 cfca595a 6606cb8b fa9053fb 9beb1806 41fdd14c 77ca50c5 adca3dd8 27467150 2a89ab96 1ab2d8f6 1d1fa7dd afa87be7 4c97cbe5 947f8048 61d501d3 7026b3fa aa272418 71f589e9 f3865958 569e48d4 5c50a431 9ec7656c
sp134 b 27c6ce88 2273ef52 cfca595a 6606cb8b fa904401 9b6b1807 50ddc149 77ca50c1 adca3dd8 2746f154 2a89ab96 1ab2d8f6 1d1f97e3 afa0fbe6 9c1fcf6c d97f084c 61d501db 5fa73402 bae72410 71f509e1 f386d95c 569e48d4 5c50a431 9ec7656c
sp135 a 7d587cde 1070c0ce 6a700ac2 978d980e 062f93fe 45dc8382 e9605ac4 af62ca16 b93bcb87 b10600d9 ec7912b1 46b40338 1d1fa7dd afeb7be7 4cd7cae5 946f8048 61c501d1 f02293fa aa27341c 31ffe9e8 dfa75753 2ca58058 34be1b7b b6e559da
sp135 b 7d587cde 1070c0ce 6a700ac2 978d980e 062f8404 455c8383 f8404ac1 af62ca12 b93bcb87 b10680dd ec7912b1 46b40338 1d1f97e3 afe3fbe6 9c5fce6c d96f084c 61c501d9 dfa31402 bae73414 31ff69e0 dfa7d757 2ca58058 34be1b7b b6e559da
sp136 a 0c63b3aa cd5bb4bb 9b0e0dc5 0f387f11 fa905bff ddb96498 87bd1454 dbd6c2f7 0142ae0a 90f83f4a f2dc705e 75f1567e 1d1fafdd afc87be7 4cd7cae5 943bc249 61d513d1 f02293fa 2a2f3418 716de9ec 954a6452 5d38dcfb 169d0fe6 3872fe3c
sp136 b 0c63b3aa cd5bb4bb 9b0e0dc5 0f387f11 fa904c05 dd396499 969d0451 dbd6c2f3 0142ae0a 90f8bf4e f2dc705e 75f1567e 1d1f9fe3 afc0fbe6 9c5fce6c d93b4a4d 61d513d9 dfa31402 3aef3410 716d69e4 954ae456 5d38dcfb 169d0fe6 3872fe3c
sp137 a c77c7f58 a908a8da 750962ff abdb582a 056fb3fe ca9283a2 49667ae6 0e376ab4 322365a7 1be36fb8 717add81 71c4be48 1d1fa7dd adeb79e7 4cd7cae5 942bc249 61d533d1 7026b3fa aa370419 f17581e8 847b7253 f240df75 55076999 7c4e2d7a
sp137 b c77c7f58 a908a8da 750962ff abdb582a 056fa404 ca1283a3 58466ae3 0e376ab0 322365a7 1be3efbc 717add81 71c4be48 1d1f97e3 ade3f9e6 9c5fce6c d92b4a4d 61d533d9 5fa73402 baf70411 f17501e0 847bf257 f240df75 55076999 7c4e2d7a
sp138 a 5451fe68 55148186 cb9663bf 78ed9972 062f9bfe 8597c2fa 6f6b3a36 093f2e3e 77e84a63 09be1b3b 2854fb35 d2f3bfad 1d1fafdd afe878e7 4c97cbe5 947bc049 61d141d1 f02293fa aa270418 f1e5e9ed e9e75d5b f30d7057 aee6cb04 0d3a8774
sp138 b 5451fe68 55148186 cb9663bf 78ed9972 062f8c04 8517c2fb 7e4b2a33 093f2e3a 77e84a63 09be9b3f 2854fb35 d2f3bfad 1d1f9fe3 afe0f8e6 9c1fcf6c d97b484d 61d141d9 dfa31402 bae70410 f1e569e5 e9e7dd5f f30d7057 aee6cb04 0d3a8774
sp139 a 3d6874f5 460feada eb60c4f8 68069e2d fad053ff 73fda5a0 a3b614e4 77c44407 c7d36772 abfe7f18 9a0df8e5 dc4af594 1d1fa7dd afc87be7 4cd7cae5 943bc249 61d503d1 7026b3fa 2a27041d 31e381ed 950a6452 46f0bc31 7a97ff9f 6c9f43ec
sp139 b 3d6874f5 460feada eb60c4f8 68069e2d fad04405 737da5a1 b29604e1 77c44403 c7d36772 abfeff1c 9a0df8e5 dc4af594 1d1f97e3 afc0fbe6 9c5fce6c d93b4a4d 61d503d9 5fa73402 3ae70415 31e301e5 950ae456 46f0bc31 7a97ff9f 6c9f43ec
sp140 a f7619617 7287880a a162a215 5dafd8c0 056fb3fe e0d4e348 63243b8e 6c7889a4 70e5e97b 6ff96b12 5abe4e6d 5d635ec7 1d1fa7dd ad8878e7 4c97cbe5 946f8048 61c521d1 f02293fa 2a273419 71e189ed e2a75a53 94002316 3b3a39ae a8413c12
sp140 b f7619617 7287880a a162a215 5dafd8c0 056fa404 e054e349 72042b8b 6c7889a0 70e5e97b 6ff9eb16 5abe4e6d 5d635ec7 1d1f97e3 ad80f8e6 9c1fcf6c d96f084c 61c521d9 dfa31402 3ae73411 71e109e5 e2a7da57 94002316 3b3a39ae a8413c12
sp141 a 4e7d64ac 52aae7c6 5e3c8cc2 1f3ede0b f9d073fb dca1ad86 29f4d2cc be88e1bd 665aca36 656b22f2 88c75672 24345c22 1d1fa7dd afab78e7 4cd7cae5 947f8048 61c121d3 7026b3fa 2a2f1c18 7175a1e8 f3f25c58 1bd46858 f4257bb1 55a4bb0e
sp141 b 4e7d64ac 52aae7c6 5e3c8cc2 1f3ede0b f9d06401 dc21ad87 38d4c2c9 be88e1b9 665aca36 656ba2f6 88c75672 24345c22 1d1f97e3 afa3f8e6 9c5fce6c d97f084c 61c121db 5fa73402 3aef1c10 717521e0 f3f2dc5c 1bd46858 f4257bb1 55a4bb0e
sp142 a 6bd2a49a 29c3720b c494f810 6e35aad9 f9d07bff d0ff3150 c3b4179c 548fb495 080ad770 72954fe8 6df46307 d8367f8c 1d1fa7dd adc978e7 4cd7cae5 947bc049 61c101d1 7026b3fa aa3f3c19 b16781ec f7f6455a 21a8e509 da7636e3 f9b3c600
sp142 b 6bd2a49a 29c3720b c494f810 6e35aad9 f9d06c05 d07f3151 d2940799 548fb491 080ad770 7295cfec 6df46307 d8367f8c 1d1f97e3 adc1f8e6 9c5fce6c d97b484d 61c101d9 5fa73402 baff3c11 b16701e4 f7f6c55e 21a8e509 da7636e3 f9b3c600
sp143 a 7f2e52f3 1624820b dc0ff82e fe358afb fa905bff f5b01172 65f651bc d9d29195 0dd2f51c a88a180b 503b4869 1b135ee0 1d1fa7dd ad8a7ae7 4c97cbe5 947f8048 61d501d1 7026b3fa 2a3f1c18 f1e5a1ec f5865252 07375168 b8701bc3 b2cb693c
sp143 b 7f2e52f3 1624820b dc0ff82e fe358afb fa904c05 f5301173 74d641b9 d9d29191 0dd2f51c a88a980f 503b4869 1b135ee0 1d1f97e3 ad82fae6 9c1fcf6c d97f084c 61d501d9 5fa73402 3aff1c10 f1e521e4 f586d256 07375168 b8701bc3 b2cb693c
sp144 a eab6b54a 7fc62aca 1c17cfd0 b2c43504 056fb3fe e2d04688 212d584c 82704e0e 10a225e7 70fa29ea d5cea622 3ee6fe6b 1d1fafdd adea79e7 4c97cbe5 947bc049 61d151d1 f02293fa aa3f2c18 b16f99ed eca7545b 97daeb8b fd3cc4ee 47b72549
sp144 b eab6b54a 7fc62aca 1c17cfd0 b2c43504 056fa404 e2504689 300d4849 82704e0a 10a225e7 70faa9ee d5cea622 3ee6fe6b 1d1f9fe3 ade2f9e6 9c1fcf6c d97b484d 61d151d9 dfa31402 baff2c10 b16f19e5 eca7d45f 97daeb8b fd3cc4ee 47b72549
sp145 a db2369b1 25723a46 dea0df76 d7cd2dba 066f9bfa 418b1e36 036e1efc 0f61de4e 55a1b8f7 ca2e5328 8874261b 6c9329db 1d1fa7dd afeb7ae7 4c97cbe5 947f8048 61d501d3 7026b3fa 2a3f0419 b177b1e8 e7a71259 b0bb43a4 1af83682 40e23c9f
sp145 b db2369b1 25723a46 dea0df76 d7cd2dba 066f8c00 410b1e37 124e0ef9 0f61de4a 55a1b8f7 ca2ed32c 8874261b 6c9329db 1d1f97e3 afe3fae6 9c1fcf6c d97f084c 61d501db 5fa73402 3aff0411 b17731e0 e7a7925d b0bb43a4 1af83682 40e23c9f
sp146 a 6f3f4031 68563605 ab2ba22e 359938fe 056fbbfa 4cc22b76 67669bb4 02614f84 9c3a026f c63e5363 dceee601 87f5ee50 1d1fafdd af8878e7 4c97cbe5 947f8048 61c161d3 f02293fa 2a3f141c b16ba1ed e8934c59 2bf30b60 36ffb989 59424d2b
sp146 b 6f3f4031 68563605 ab2ba22e 359938fe 056fac00 4c422b77 76468bb1 02614f80 9c3a026f c63ed367 dceee601 87f5ee50 1d1f9fe3 af80f8e6 9c1fcf6c d97f084c 61c161db dfa31402 3aff1414 b16b21e5 e893cc5d 2bf30b60 36ffb989 59424d2b
sp147 a 3d406867 bb6f99fb 0b915401 c7620ed5 fa9053ff dfbe7558 85b4d39c 1b9970a7 2d1d3bfa 3e7b6103 8da6f185 b7a98225 1d1fafdd af8978e7 4c97cbe5 947fc049 61d501d1 f02293fa aa3f2c1c 317fb9e9 f78655da 9b25cf81 98b159a2 3e1a74ac
sp147 b 3d406867 bb6f99fb 0b915401 c7620ed5 fa904405 df3e7559 9494c399 1b9970a3 2d1d3bfa 3e7be107 8da6f185 b7a98225 1d1f9fe3 af81f8e6 9c1fcf6c d97f484d 61d501d9 dfa31402 baff2c14 317f39e1 f786d5de 9b25cf81 98b159a2 3e1a74ac
sp148 a 34d893f6 69d9ba31 a00b6766 2ae4ddb2 056fbbfa 46c5ee3e ab6e18f4 c6236d74 fa642bab c72b45d2 772ffc4c a358f9ee 1d1fa7dd afcb7ae7 4c97cbe5 947b8048 61d141d3 f02293fa 2a2f041c 31f381e8 e6a742d9 29bc8414 f2ec2c49 1df3fcf8
sp148 b 34d893f6 69d9ba31 a00b6766 2ae4ddb2 056fac00 4645ee3f ba4e08f1 c6236d70 fa642bab c72bc5d6 772ffc4c a358f9ee 1d1f97e3 afc3fae6 9c1fcf6c d97b084c 61d141db dfa31402 3aef0414 31f301e0 e6a7c2dd 29bc8414 f2ec2c49 1df3fcf8
sp149 a f412128b 6d2cd899 37b1dbbb adc3a16e 052fb3fe 069692e2 676bbc2e c4353f94 bc2259d5 f6716043 f107d601 b5048510 1d1fafdd adab79e7 4c97cbe5 946fc049 61c511d1 f02293fa 2a3f3418 b1fff9e9 e6e742db 6e3372b9 370a690c 8882d39c
sp149 b f412128b 6d2cd899 37b1dbbb adc3a16e 052fa404 061692e3 764bac2b c4353f90 bc2259d5 f671e047 f107d601 b5048510 1d1f9fe3 ada3f9e6 9c1fcf6c d96f484d 61c511d9 dfa31402 3aff3410 b1ff79e1 e6e7c2df 6e3372b9 370a690c 8882d39c
sp150 a c0588f0e 471eb885 7bcd5eb6 3ab02c7a 062f93fa 418d1ff6 2f661ebc c7307fee 31fb3b3b cf536192 b51182dd 9d42f485 1d1fafdd adea7be7 4cd7cae5 946f8048 61c111d3 f02293fa 2a3f3c1d 717d91e9 e1a35f59 38bdd226 6ed04f82 58a96ce3
sp150 b c0588f0e 471eb885 7bcd5eb6 3ab02c7a 062f8400 410d1ff7 3e460eb9 c7307fea 31fb3b3b cf53e196 b51182dd 9d42f485 1d1f9fe3 ade2fbe6 9c5fce6c d96f084c 61c111db dfa31402 3aff3c15 717d11e1 e1a3df5d 38bdd226 6ed04f82 58a96ce3
sp151 a 7d4f7507 851f2487 62db2dbd 8f52bf71 f9d07bff 74ffc4f8 adbf5434 7ac6c015 2a0eadde 047b36c0 828c4b31 41332a4b 1d1fafdd ade879e7 4cd7cae5 947fc049 61c531d1 7026b3fa aa370c19 b1e7f9ec f9f65cda 7f816027 f05e9a4b cfe1543e
sp151 b 7d4f7507 851f2487 62db2dbd 8f52bf71 f9d06c05 747fc4f9 bc9f4431 7ac6c011 2a0eadde 047bb6c4 828c4b31 41332a4b 1d1f9fe3 ade0f9e6 9c5fce6c d97f484d 61c531d9 5fa73402 baf70c11 b1e779e4 f9f6dcde 7f816027 f05e9a4b cfe1543e
sp152 a 20fa5cea 174922bf 07e2c4cd c55dde01 f99073fb 7ce66d8c 2db5d344 929361dd cccb2c4a fda50e32 b3c2ea84 10aebc86 1d1fafdd adea79e7 4cd7cae5 943bc249 61d503d3 f02293fa aa2f2c1c 31ffb9e8 984a3c58 b7a1d545 f0a458f8 cfd43d73
sp152 b 20fa5cea 174922bf 07e2c4cd c55dde01 f9906401 7c666d8d 3c95c341 929361d9 cccb2c4a fda58e36 b3c2ea84 10aebc86 1d1f9fe3 ade2f9e6 9c5fce6c d93b4a4d 61d503db dfa31402 baef2c14 31ff39e0 984abc5c b7a1d545 f0a458f8 cfd43d73
sp153 a a27f9c52 8cad9a32 8fa10c61 dc5c7eb5 fa9053fb 1fe16d3c 87b3927c d3d1c22d 21c8cb5e 45c12d50 e37c7942 83053f50 1d1fa7dd adca78e7 4cd7cae5 943bc249 61d503d3 f02293fa aa271c18 71e189ed 974a6558 14c6d695 969e89bc c2efbf62
sp153 b a27f9c52 8cad9a32 8fa10c61 dc5c7eb5 fa904401 1f616d3d 96938279 d3d1c229 21c8cb5e 45c1ad54 e37c7942 83053f50 1d1f97e3 adc2f8e6 9c5fce6c d93b4a4d 61d503db dfa31402 bae71c10 71e109e5 974ae55c 14c6d695 969e89bc c2efbf62
sp154 a 20294692 d8663b0a bce07617 32e94cc2 056fb3fe acd2f74a 0f603f8e 6e3f7834 b2a05b2f 262954e1 8cc0fd99 3664e6b0 1d1fafdd afeb7be7 4c97cbe5 946fc049 61d111d1 f02293fa 2a270418 71f9c1e9 e4b340db cbc739d1 8efdb5ac aa6a453a
sp154 b 20294692 d8663b0a bce07617 32e94cc2 056fa404 ac52f74b 1e402f8b 6e3f7830 b2a05b2f 2629d4e5 8cc0fd99 3664e6b0 1d1f9fe3 afe3fbe6 9c1fcf6c d96f484d 61d111d9 dfa31402 3ae70410 71f941e1 e4b3c0df cbc739d1 8efdb5ac aa6a453a
sp155 a 1fc097f8 1a57c04d f659cb60 d4f2b9ac 066f9bfe 4bd28220 e72f1b64 657e0e3e d36401e1 f7925953 38a48f3f 2583e726 1d1fafdd afaa78e7 4c97cbe5 947fc049 61c141d1 7026b3fa aa3f3c18 7171d1e8 eb934ddb a5149331 b73b321a a4ab7cd2
sp155 b 1fc097f8 1a57c04d f659cb60 d4f2b9ac 066f8c04 4b528221 f60f0b61 657e0e3a d36401e1 f792d957 38a48f3f 2583e726 1d1f9fe3 afa2f8e6 9c1fcf6c d97f484d 61c141d9 5fa73402 baff3c10 717151e0 eb93cddf a5149331 b73b321a a4ab7cd2
sp156 a c80e6925 159988c6 2529cef1 6fdc7c38 066f93fa 61c40fb4 0526f8f6 0723ef24 57e0e057 6a496709 33bf3848 510c6633 1d1fafdd afeb79e7 4c97cbe5 947f8048 61d531d3 7026b3fa aa3f1c19 b1f781e9 e7a74359 907a526c 993f4488 479bcbe9
sp156 b c80e6925 159988c6 2529cef1 6fdc7c38 066f8400 61440fb5 1406e8f3 0723ef20 57e0e057 6a49e70d 33bf3848 510c6633 1d1f9fe3 afe3f9e6 9c1fcf6c d97f084c 61d531db 5fa73402 baff1c11 b1f701e1 e7a7c35d 907a526c 993f4488 479bcbe9
sp157 a 8b0f76e8 e2f7d2fb e53e4823 6d63faf7 fa905bff 19f9417a 49f657b4 f78ce4c7 a9908650 1ab6490a b3a71845 e8b8534d 1d1fafdd af8a7be7 4c97cbe5 947f8048 61d501d1 f02293fa 2a2f3c1d f1e9e1ed f3864952 60ea0060 5460258c b0991610
sp157 b 8b0f76e8 e2f7d2fb e53e4823 6d63faf7 fa904c05 1979417b 58d647b1 f78ce4c3 a9908650 1ab6c90e b3a71845 e8b8534d 1d1f9fe3 af82fbe6 9c1fcf6c d97f084c 61d501d9 dfa31402 3aef3c15 f1e961e5 f386c956 60ea0060 5460258c b0991610
sp158 a ad49dd36 2a5e624a ad49e753 f8af3d9a 062f9bfe 0f910612 a569795e 693fad96 9125ce25 842107e1 5fff2143 bebb1e8a 1d1fafdd adab78e7 4c97cbe5 947bc049 61d141d1 7026b3fa aa27241c 717589e9 ebe75d5b eb554d3f f8e8bc24 bc55869c
sp158 b ad49dd36 2a5e624a ad49e753 f8af3d9a 062f8c04 0f110613 b449695b 693fad92 9125ce25 842187e5 5fff2143 bebb1e8a 1d1f9fe3 ada3f8e6 9c1fcf6c d97b484d 61d141d9 5fa73402 bae72414 717509e1 ebe7dd5f eb554d3f f8e8bc24 bc55869c
sp159 a a6ba0684 f8cdc14a 4b1b7e51 bef7ec84 056fb3fe 64def708 0124ffc6 c838bc64 d07cbd13 39f63e18 a7d30936 881070e5 1d1fafdd adc879e7 4c97cbe5 943b8248 61d573d1 f02293fa aa372c1c f1edc9ed 886b6bdb d8238b18 1d7d5b79 562d45f4
sp159 b a6ba0684 f8cdc14a 4b1b7e51 bef7ec84 056fa404 645ef709 1004efc3 c838bc60 d07cbd13 39f6be1c a7d30936 881070e5 1d1f9fe3 adc0f9e6 9c1fcf6c d93b0a4c 61d573d9 dfa31402 baf72c14 f1ed49e5 886bebdf d8238b18 1d7d5b79 562d45f4
sp160 a 77768af5 2163a547 ce234560 a85f37a9 f99073fb 94ec8c24 2dbfd36c 18dc879f 0e12e264 43064378 988c6e09 8aeb7e39 1d1fafdd adc879e7 4cd7cae5 943bc249 61d533d3 7026b3fa aa271419 71e9a9ed 984a6c58 1fb9d5f3 708e2111 fa04fa50
sp160 b 77768af5 2163a547 ce234560 a85f37a9 f9906401 946c8c25 3c9fc369 18dc879b 0e12e264 4306c37c 988c6e09 8aeb7e39 1d1f9fe3 adc0f9e6 9c5fce6c d93b4a4d 61d533db 5fa73402 bae71411 71e929e5 984aec5c 1fb9d5f3 708e2111 fa04fa50
sp161 a 620c7bb0 30b2015b f983505f 3a270a8f fa905bff d9f11102 47f417c4 b584b6cd 070096d6 d2e57f69 93da12db 6a026623 1d1fa7dd afeb79e7 4c97cbe5 943b8248 61c523d1 7026b3fa 2a3f0418 716591ec 913a7bda d8ca1454 d6b21bbb 56d11fa5
sp161 b 620c7bb0 30b2015b f983505f 3a270a8f fa904c05 d9711103 56d407c1 b584b6c9 070096d6 d2e5ff6d 93da12db 6a026623 1d1f97e3 afe3f9e6 9c1fcf6c d93b0a4c 61c523d9 5fa73402 3aff0410 716511e4 913afbde d8ca1454 d6b21bbb 56d11fa5
sp162 a 14442e24 3fe08ac5 31b0b2fb 5b85a836 066f93fe 2194d3ba 65677d76 4d7d1a04 f7ec3565 1a00438b 8012b630 51438623 1d1fa7dd adab7be7 4c97cbe5 947bc049 61d131d1 7026b3fa aa373419 3167f9ed eba75a5b d9297de5 38fa9809 7cc2f971
sp162 b 14442e24 3fe08ac5 31b0b2fb 5b85a836 066f8404 2114d3bb 74476d73 4d7d1a00 f7ec3565 1a00c38f 8012b630 51438623 1d1f97e3 ada3fbe6 9c1fcf6c d97b484d 61d131d9 5fa73402 baf73411 316779e5 eba7da5f d9297de5 38fa9809 7cc2f971
sp163 a 2457e752 4f1f5541 ad81bf7a 82eccdb2 066f93fe 859af63a a16f5f74 05759836 7762f1bd ebe56999 93c60943 1736757a 1d1fafdd ada87be7 4c97cbe5 946f8048 61c511d1 f02293fa 2a3f0c18 71fd91e8 e1a75f53 ef320d62 fd06ddc7 074c5259
sp163 b 2457e752 4f1f5541 ad81bf7a 82eccdb2 066f8404 851af63b b04f4f71 05759832 7762f1bd ebe5e99d 93c60943 1736757a 1d1f9fe3 ada0fbe6 9c1fcf6c d96f084c 61c511d9 dfa31402 3aff0c10 71fd11e0 e1a7df57 ef320d62 fd06ddc7 074c5259
sp164 a 9cfb4d31 fcc2bb4d fe3c4645 1ccab48c 066f93fe 6f9b8700 ab20b9ce 8d36ad64 9d608bef c7b74e72 ab8f16e9 56536ae0 1d1fafdd adcb7be7 4c97cbe5 947b8048 61c121d1 7026b3fa aa371c19 71edc9ed e79741d3 82fa8cde f34193b2 7d8376af
sp164 b 9cfb4d31 fcc2bb4d fe3c4645 1ccab48c 066f8404 6f1b8701 ba00a9cb 8d36ad60 9d608bef c7b7ce76 ab8f16e9 56536ae0 1d1f9fe3 adc3fbe6 9c1fcf6c d97b084c 61c121d9 5fa73402 baf71c11 71ed49e5 e797c1d7 82fa8cde f34193b2 7d8376af
sp165 a b0e0b9e5 2787a4b6 68e73be3 75f9e932 056fb3fe 8c94d2ba 4f6a3df6 003fba26 187bb1fd 933b56f9 a96a5348 a40468e1 1d1fa7dd adc87be7 4c97cbe5 942bc249 61d533d1 f02293fa aa3f3419 f175d1e9 847b7253 b05d6e5d cf4fe545 0e622c4b
sp165 b b0e0b9e5 2787a4b6 68e73be3 75f9e932 056fa404 8c14d2bb 5e4a2df3 003fba22 187bb1fd 933bd6fd a96a5348 a40468e1 1d1f97e3 adc0fbe6 9c1fcf6c d92b4a4d 61d533d9 dfa31402 baff3411 f17551e1 847bf257 b05d6e5d cf4fe545 0e622c4b
sp166 a ab9363d8 b5d4a246 1e3ea54e b430bf87 f9907bff 16b8c40a 29f8d2c4 98d8015f 0e0d0114 21693159 6ee5864b 46f3d4eb 1d1fa7dd afe878e7 4c97cbe5 943b8248 61d503d1 f02293fa 2a3f3418 316399ec 924a3cda 241180c8 74b1a077 3377edd5
sp166 b ab9363d8 b5d4a246 1e3ea54e b430bf87 f9906c05 1638c40b 38d8c2c1 98d8015b 0e0d0114 2169b15d 6ee5864b 46f3d4eb 1d1f97e3 afe0f8e6 9c1fcf6c d93b0a4c 61d503d9 dfa31402 3aff3410 316319e4 924abcde 241180c8 74b1a077 3377edd5
sp167 a d73fdc04 cd7c9cc2 d5f505fb 9b725f33 f99073ff dcb164ba a7fb947c 5ac4c06f 0e00afa6 1e407782 dad34ee0 01ed2f69 1d1fafdd afe979e7 4cd7cae5 943b8248 61d503d1 f02293fa 2a2f141c 31e7f9ed 924a3bda 5e17df18 f65ebfc3 898f4e42
sp167 b d73fdc04 cd7c9cc2 d5f505fb 9b725f33 f9906405 dc3164bb b6db8479 5ac4c06b 0e00afa6 1e40f786 dad34ee0 01ed2f69 1d1f9fe3 afe1f9e6 9c5fce6c d93b0a4c 61d503d9 dfa31402 3aef1414 31e779e5 924abbde 5e17df18 f65ebfc3 898f4e42
sp168 a 24fc54f8 844641bd 2e2fe7cd 90d17d00 062f93fa cf866e8c 032d384e 0137ad8c 1168ad3f 30e02ecb 734d51c9 4a004600 1d1fa7dd ad887ae7 4c97cbe5 947f8048 61d541d3 f02293fa 2a3f3c18 31efd9ec e9e75a59 a53f1446 9b3944eb cb6445c7
sp168 b 24fc54f8 844641bd 2e2fe7cd 90d17d00 062f8400 cf066e8d 120d284b 0137ad88 1168ad3f 30e0aecf 734d51c9 4a004600 1d1f97e3 ad80fae6 9c1fcf6c d97f084c 61d541db dfa31402 3aff3c10 31ef59e4 e9e7da5d a53f1446 9b3944eb cb6445c7
sp169 a 9c13a524 28991a86 ef25c7b8 40f9fd74 062f93fe 6b9366f8 012a5fb4 ab35698c 39e30ef3 63915cf9 4f229f9c 5741ef25 1d1fafdd adca7be7 4cd7cae5 946fc049 61d101d1 7026b3fa 2a3f041d 317f89e9 e5b350db 8f23ea61 1d0fb6cf 34a64b63
sp169 b 9c13a524 28991a86 ef25c7b8 40f9fd74 062f8404 6b1366f9 100a4fb1 ab356988 39e30ef3 6391dcfd 4f229f9c 5741ef25 1d1f9fe3 adc2fbe6 9c5fce6c d96f484d 61d101d9 5fa73402 3aff0415 317f09e1 e5b3d0df 8f23ea61 1d0fb6cf 34a64b63
sp170 a 9839d6a3 d0add287 d88d0893 ee2d5a43 fa905bff 39fe41ca e7f09684 f1c3838d c7448296 d5563650 76875499 fbb621b1 1d1fafdd afea7be7 4c97cbe5 947f8048 61d101d1 7026b3fa aa270419 31fb89e8 f3824952 be890f90 b661befc e0e452a2
sp170 b 9839d6a3 d0add287 d88d0893 ee2d5a43 fa904c05 397e41cb f6d08681 f1c38389 c7448296 d556b654 76875499 fbb621b1 1d1f9fe3 afe2fbe6 9c1fcf6c d97f084c 61d101d9 5fa73402 bae70411 31fb09e0 f382c956 be890f90 b661befc e0e452a2
sp171 a 9861332f d1fd317e 3cf350bb 58266a77 f9d073fb 74e4f9fe 49f656b4 34d29507 0c409294 1e0a4720 142a3e4a 38bc5978 1d1fafdd ad8b7ae7 4cd7cae5 947f8048 61c111d3 f02293fa 2a3f1c18 71e1d1ec f5f24258 05c4f91e 542ff785 d7cb95c8
sp171 b 9861332f d1fd317e 3cf350bb 58266a77 f9d06401 7464f9ff 58d646b1 34d29503 0c409294 1e0ac724 142a3e4a 38bc5978 1d1f9fe3 ad83fae6 9c5fce6c d97f084c 61c111db dfa31402 3aff1c10 71e151e4 f5f2c25c 05c4f91e 542ff785 d7cb95c8
sp172 a 0e619339 808178cd 225266e0 83ed5c2c 066f93fe cfdd87a0 2b2298ec 6778498c 7f7921bb c6407460 79d4b0d7 d3d998c7 1d1fafdd adcb79e7 4c97cbe5 942bc249 61d513d1 f02293fa aa373c19 b1f3f1e9 837b6a53 6d21bbf3 f38f924f 63abde06
sp172 b 0e619339 808178cd 225266e0 83ed5c2c 066f8404 cf5d87a1 3a0288e9 67784988 7f7921bb c640f464 79d4b0d7 d3d998c7 1d1f9fe3 adc3f9e6 9c1fcf6c d92b4a4d 61d513d9 dfa31402 baf73c11 b1f371e1 837bea57 6d21bbf3 f38f924f 63abde06
sp173 a 05e526a3 b61e8fca 8c0007d3 3b95bd06 056fbbfe e4d3e68a a969784e cc242e0e 9c7a2573 bbce7eba 80209d37 ca00c957 1d1fa7dd ada878e7 4c97cbe5 947fc049 61c121d1 f02293fa 2a3f3c19 71f9c1e9 ee9315db 8de11053 f4fcc4ed 44a1acc4
sp173 b 05e526a3 b61e8fca 8c0007d3 3b95bd06 056fac04 e453e68b b849684b cc242e0a 9c7a2573 bbcefebe 80209d37 ca00c957 1d1f97e3 ada0f8e6 9c1fcf6c d97f484d 61c121d9 dfa31402 3aff3c11 71f941e1 ee9395df 8de11053 f4fcc4ed 44a1acc4
sp174 a a334eb0a ad0da787 09ebc4a3 7b5efe6f f9907bfb daad0de6 abf294ac 5a9be7d7 ca838bfe c3825bdb 70123939 77021930 1d1fa7dd ad8b78e7 4c97cbe5 947f8048 61d511d3 f02293fa 2a2f1c1c 31eff9ed f6864458 99fd35b6 f263b891 89802af9
sp174 b a334eb0a ad0da787 09ebc4a3 7b5efe6f f9906c01 da2d0de7 bad284a9 5a9be7d3 ca838bfe c382dbdf 70123939 77021930 1d1f97e3 ad83f8e6 9c1fcf6c d97f084c 61d511db dfa31402 3aef1c14 31ef79e5 f686c45c 99fd35b6 f263b891 89802af9
sp175 a 79a05118 0a57f313 de128038 fb755ae9 fad053fb bfe60964 67b3962c ff8fe455 c98986d0 42c77fc8 8110757e 7e3d3547 1d1fa7dd afc97be7 4cd7cae5 943bc249 61d503d3 f02293fa 2a273c18 71e5b1ec 950a6458 72c3376d 369ea60c 1935c5fd
sp175 b 79a05118 0a57f313 de128038 fb755ae9 fad04401 bf660965 76938629 ff8fe451 c98986d0 42c7ffcc 8110757e 7e3d3547 1d1f97e3 afc1fbe6 9c5fce6c d93b4a4d 61d503db dfa31402 3ae73c10 71e531e4 950ae45c 72c3376d 369ea60c 1935c5fd
sp176 a 0bf01a23 32d0903a b8d38c44 b26bbe95 fad053ff 55b1c518 81b0d3dc 318c2107 6d8007d4 61d12ef9 750af8c1 568bc369 1d1fa7dd adaa78e7 4cd7cae5 947fc049 61c101d1 7026b3fa 2a370418 71eda1ec f8f25dda 9d155141 9c7142a2 df0dca6a
sp176 b 0bf01a23 32d0903a b8d38c44 b26bbe95 fad04405 5531c519 9090c3d9 318c2103 6d8007d4 61d1aefd 750af8c1 568bc369 1d1f97e3 ada2f8e6 9c5fce6c d97f484d 61c101d9 5fa73402 3af70410 71ed21e4 f8f2ddde 9d155141 9c7142a2 df0dca6a
sp177 a 5a56c5d2 9663b672 60d26da7 e305b773 fa9053fb 1bea6cfe 2fff923c 51ca879f 45c5878a 55493573 2a1623bc 75506afd 1d1fa7dd af897be7 4c97cbe5 947f8048 61d501d3 7026b3fa aa2f041d 31eba1ec f3865958 d6bdf3dc 6e56c346 944d4392
sp177 b 5a56c5d2 9663b672 60d26da7 e305b773 fa904401 1b6a6cff 3edf8239 51ca879b 45c5878a 5549b577 2a1623bc 75506afd 1d1f97e3 af81fbe6 9c1fcf6c d97f084c 61d501db 5fa73402 baef0415 31eb21e4 f386d95c d6bdf3dc 6e56c346 944d4392
sp178 a e7035497 b021d1c2 d23224ee b512363b fa9053fb 11ed0db6 89f2d2f4 f7dcc70f afd28688 e3b44a59 831467e7 6b8618fc 1d1fa7dd afc878e7 4c97cbe5 946b8048 61d161d3 f02293fa 2a270c18 3167f9ec e9970ad8 5e986720 146f7a45 e0431e82
sp178 b e7035497 b021d1c2 d23224ee b512363b fa904401 116d0db7 98d2c2f1 f7dcc70b afd28688 e3b4ca5d 831467e7 6b8618fc 1d1f97e3 afc0f8e6 9c1fcf6c d96b084c 61d161db dfa31402 3ae70c10 316779e4 e9978adc 5e986720 146f7a45 e0431e82
sp179 a 96dfb637 f15b80f9 09eb1e23 8e8c4cf6 052fbbfe aa91577a 2566f9be 0a69dd1e 5425df31 85f62d70 1b7a7e85 97887c1e 1d1fa7dd ade979e7 4c97cbe5 947fc049 61d561d1 f02293fa aa2f3419 316f89ec eee754db d202eadb f8ef3b7d 4bcd4756
sp179 b 96dfb637 f15b80f9 09eb1e23 8e8c4cf6 052fac04 aa11577b 3446e9bb 0a69dd1a 5425df31 85f6ad74 1b7a7e85 97887c1e 1d1f97e3 ade1f9e6 9c1fcf6c d97f484d 61d561d9 dfa31402 baef3411 316f09e4 eee7d4df d202eadb f8ef3b7d 4bcd4756
sp180 a 97c81b0e d365928a 50ecaeb3 91ba5c66 056fb3fe 8ed8e7ea 8163f926 6e65c924 b065c9d7 b73744d0 35941f18 1e8c4a49 1d1fafdd afeb7be7 4cd7cae5 942bc249 61d503d1 7026b3fa 2a372418 31e3f9ed 827b3a53 2c0279e7 9d0a3b58 626e56d2
sp180 b 97c81b0e d365928a 50ecaeb3 91ba5c66 056fa404 8e58e7eb 9043e923 6e65c920 b065c9d7 b737c4d4 35941f18 1e8c4a49 1d1f9fe3 afe3fbe6 9c5fce6c d92b4a4d 61d503d9 5fa73402 3af72410 31e379e5 827bba57 2c0279e7 9d0a3b58 626e56d2
sp181 a 2814208e 4ce26b46 31e1b47f 6203aeb3 f99073ff f2bbf53a 07f7927c 7283f04f 2c0ef416 b45534e0 35030323 cbd111c0 1d1fafdd adc879e7 4c97cbe5 947f8048 61d121d1 7026b3fa 2a2f3419 31f7e9e9 f6825352 07dd5ea4 1662d304 6627f463
sp181 b 2814208e 4ce26b46 31e1b47f 6203aeb3 f9906405 f23bf53b 16d78279 7283f04b 2c0ef416 b455b4e4 35030323 cbd111c0 1d1f9fe3 adc0f9e6 9c1fcf6c d97f084c 61d121d9 5fa73402 3aef3411 31f769e1 f682d356 07dd5ea4 1662d304 6627f463
sp182 a 920caf14 8e9d7336 4b534766 ddfc3db6 052fb3fa 0ec16e3e 076a98fc 2a386b06 9e212bc1 acb50f01 9821befc 7af3d376 1d1fafdd af8b7be7 4cd7cae5 946f8048 61d521d3 f02293fa 2a3f0c1d b1f3b1e9 e0b74f59 63e0d220 96cbb542 361f9209
sp182 b 920caf14 8e9d7336 4b534766 ddfc3db6 052fa400 0e416e3f 164a88f9 2a386b02 9e212bc1 acb58f05 9821befc 7af3d376 1d1f9fe3 af83fbe6 9c5fce6c d96f084c 61d521db dfa31402 3aff0c15 b1f331e1 e0b7cf5d 63e0d220 96cbb542 361f9209
sp183 a 527c351a 2aa64177 c1bd51a3 182eab73 fa905bff bbf5d0fa 43fa97bc bf83f407 63459a70 752c1671 bbcb7bf5 01f17e9c 1d1fa7dd adab78e7 4c97cbe5 947f8048 61d501d1 f02293fa 2a271418 b17781e9 f5865452 c0cc73e0 5a53bd7f 989bc9a6
sp183 b 527c351a 2aa64177 c1bd51a3 182eab73 fa904c05 bb75d0fb 52da87b9 bf83f403 63459a70 752c9675 bbcb7bf5 01f17e9c 1d1f97e3 ada3f8e6 9c1fcf6c d97f084c 61d501d9 dfa31402 3ae71410 b17701e1 f586d456 c0cc73e0 5a53bd7f 989bc9a6
sp184 a 7ba530c9 9e9f4455 bf5c5779 6fb4ada8 052fbbfe 20db3620 892a7ee6 227b5e54 946778fd 8ec96823 2e86d020 6fa9fc3a 1d1fafdd afe97ae7 4cd7cae5 947f8048 61d521d1 f02293fa aa373419 717da1e9 e8a70a53 59990c3e 94f3f756 67dabd1e
sp184 b 7ba530c9 9e9f4455 bf5c5779 6fb4ada8 052fac04 205b3621 980a6ee3 227b5e50 946778fd 8ec9e827 2e86d020 6fa9fc3a 1d1f9fe3 afe1fae6 9c5fce6c d97f084c 61d521d9 dfa31402 baf73411 717d21e1 e8a78a57 59990c3e 94f3f756 67dabd1e
sp185 a bd5700d1 72282f8d ae5adfb2 47ee8d7e 066f9bfe 23d616f2 0d6adfb4 a97f9f4e 3337bc53 667576c3 faa9762d a4bd080c 1d1fa7dd af8b78e7 4c97cbe5 947b8048 61d121d1 7026b3fa 2a3f341c 71e9f1ed e5a744d3 d5003dec 10ff85cf 72928de7
sp185 b bd5700d1 72282f8d ae5adfb2 47ee8d7e 066f8c04 235616f3 1c4acfb1 a97f9f4a 3337bc53 6675f6c7 faa9762d a4bd080c 1d1f97e3 af83f8e6 9c1fcf6c d97b084c 61d121d9 5fa73402 3aff3414 71e971e5 e5a7c4d7 d5003dec 10ff85cf 72928de7
sp186 a e000c7f3 c60f9945 39d33672 c7f54cbe 062f9bfa cfc63f36 2d66dff4 4b67dffe 9d609bbb e6ad5861 dbf40507 15517c9c 1d1fafdd adaa79e7 4c97cbe5 946f8048 61d501d3 f02293fa 2a2f2418 71fd81e9 e1f74959 a4cd03a4 70ff8545 c935ccf3
sp186 b e000c7f3 c60f9945 39d33672 c7f54cbe 062f8c00 cf463f37 3c46cff1 4b67dffa 9d609bbb e6add865 dbf40507 15517c9c 1d1f9fe3 ada2f9e6 9c1fcf6c d96f084c 61d501db dfa31402 3aef2410 71fd01e1 e1f7c95d a4cd03a4 70ff8545 c935ccf3
sp187 a f13b27ac d5706016 efd7be1b c3f1ccca 056fbbfe 80951742 2d61f80e a278de86 bca8d4c7 863f47c3 45a300e3 ae21605b 1d1fafdd adc97ae7 4cd7cae5 943bc249 61d573d1 7026b3fa aa3f3418 717d99e8 8c6b6553 3c7049dd 71041c70 67fc7069
sp187 b f13b27ac d5706016 efd7be1b c3f1ccca 056fac04 80151743 3c41e80b a278de82 bca8d4c7 863fc7c7 45a300e3 ae21605b 1d1f9fe3 adc1fae6 9c5fce6c d93b4a4d 61d573d9 5fa73402 baff3410 717d19e0 8c6be557 3c7049dd 71041c70 67fc7069
sp188 a ae3950ec c6d58f8e eebb7ea6 d2c1ec6e 062f9bfe 8fd617e2 29625ea4 4726ffde 5fbcf595 b80711a8 9efe41c2 5a436183 1d1fa7dd afeb78e7 4c97cbe5 947f8048 61c131d1 f02293fa aa370418 b1ffa1e8 e7d34453 e0a3debe f4fbd697 8778fbd0
sp188 b ae3950ec c6d58f8e eebb7ea6 d2c1ec6e 062f8c04 8f5617e3 38424ea1 4726ffda 5fbcf595 b80791ac 9efe41c2 5a436183 1d1f97e3 afe3f8e6 9c1fcf6c d97f084c 61c131d9 dfa31402 baf70410 b1ff21e0 e7d3c457 e0a3debe f4fbd697 8778fbd0
sp189 a 43cceb33 3910c682 399109ba b7745b73 f99073ff 50be40fa 6ffa11b4 d49ca2d5 ce05abc8 e96930bb e1827e04 c81609af 1d1fafdd afea7be7 4cd7cae5 943b8248 61d543d1 f02293fa aa27041d f1f1f1e8 924a7bda ea2a3fe0 ae58328c 4dc9555a
sp189 b 43cceb33 3910c682 399109ba b7745b73 f9906405 503e40fb 7eda01b1 d49ca2d1 ce05abc8 e969b0bf e1827e04 c81609af 1d1f9fe3 afe2fbe6 9c5fce6c d93b0a4c 61d543d9 dfa31402 bae70415 f1f171e0 924afbde ea2a3fe0 ae58328c 4dc9555a
sp190 a c4115535 329e8347 dbac7068 2c1e0ab9 fa905bff d7ba9130 c5b251fc b7cd5287 8b805b9a 1f427732 bbd1e555 5929d7ac 1d1fa7dd af887be7 4c97cbe5 946bc049 61d171d1 f02293fa aa27341d 7169c1ec ed97105a a1529f67 58afd343 e9f828ed
sp190 b c4115535 329e8347 dbac7068 2c1e0ab9 fa904c05 d73a9131 d49241f9 b7cd5283 8b805b9a 1f42f736 bbd1e555 5929d7ac 1d1f97e3 af80fbe6 9c1fcf6c d96b484d 61d171d9 dfa31402 bae73415 716941e4 ed97905e a1529f67 58afd343 e9f828ed
sp191 a a1846e46 acafb3fe fb65d118 5823abd5 f9d073fb 1aa1f85c edbdd11c 7a9671ef ead47656 99f43d99 918d8780 7f9f9f58 1d1fafdd ad8b7ae7 4cd7cae5 943bc249 61d503d3 7026b3fa 2a2f3c1d 31e7e9ed 984a3d58 9a496975 30987b65 6dcd2ce5
sp191 b a1846e46 acafb3fe fb65d118 5823abd5 f9d06401 1a21f85d fc9dc119 7a9671eb ead47656 99f4bd9d 918d8780 7f9f9f58 1d1f9fe3 ad83fae6 9c5fce6c d93b4a4d 61d503db 5fa73402 3aef3c15 31e769e5 984abd5c 9a496975 30987b65 6dcd2ce5
sp192 a d97c5c32 a839ba85 38073b85 46f06948 062f93fa ad8b3ac4 ed287b86 c13dbedc 7920bdfb 5f2844b3 696972a4 949e1606 1d1fa7dd af897be7 4cd7cae5 946f8048 61d501d3 7026b3fa aa270c1d b1ffd9e8 dfb75759 452d2616 b0f5e2fc a1026572
sp192 b d97c5c32 a839ba85 38073b85 46f06948 062f8400 ad0b3ac5 fc086b83 c13dbed8 7920bdfb 5f28c4b7 696972a4 949e1606 1d1f97e3 af81fbe6 9c5fce6c d96f084c 61d501db 5fa73402 bae70c15 b1ff59e0 dfb7d75d 452d2616 b0f5e2fc a1026572
sp193 a 6b583ee2 9a3dc74b 8a7e5954 0628cb85 fa9053ff bfba5008 c7bd114c dddb90b5 e39a9b64 01b41ed9 0afb1bd1 48281210 1d1fafdd afab7be7 4c97cbe5 947fc049 61d501d1 7026b3fa aa3f2418 b1efb1ed f78652da 3b0c11d1 d6a92432 6cc02a81
sp193 b 6b583ee2 9a3dc74b 8a7e5954 0628cb85 fa904405 bf3a5009 d69d0149 dddb90b1 e39a9b64 01b49edd 0afb1bd1 48281210 1d1f9fe3 afa3fbe6 9c1fcf6c d97f484d 61d501d9 5fa73402 baff2410 b1ef31e5 f786d2de 3b0c11d1 d6a92432 6cc02a81
sp194 a 0cb0ba42 fb6eda4a f0ad1f50 95828584 056fb3fe e8907608 ad28dec4 2a3a7dd4 12627aa5 ca1b56a9 31d2c652 500de27b 1d1fafdd adeb78e7 4c97cbe5 947fc049 61c111d1 7026b3fa 2a2f0419 71f991e9 ee9305db 09fda013 713126bb ee8aef1b
sp194 b 0cb0ba42 fb6eda4a f0ad1f50 95828584 056fa404 e8107609 bc08cec1 2a3a7dd0 12627aa5 ca1bd6ad 31d2c652 500de27b 1d1f9fe3 ade3f8e6 9c1fcf6c d97f484d 61c111d9 5fa73402 3aef0411 71f911e1 ee9385df 09fda013 713126bb ee8aef1b
sp195 a c853ccd4 48ad0a42 542bf37b 0ebaa1b2 062f93fe 0d9d523a 6f6b3b76 81789e4e 196ddea3 702810c9 c63f1024 0d137b24 1d1fa7dd afea7ae7 4cd7cae5 947fc049 61d141d1 f02293fa aa3f0c1d f175a1e8 eba35bdb 6b05df17 aebad2c9 9c40ef01
sp195 b c853ccd4 48ad0a42 542bf37b 0ebaa1b2 062f8404 0d1d523b 7e4b2b73 81789e4a 196ddea3 702890cd c63f1024 0d137b24 1d1f97e3 afe2fae6 9c5fce6c d97f484d 61d141d9 dfa31402 baff0c15 f17521e0 eba3dbdf 6b05df17 aebad2c9 9c40ef01
sp196 a c486e417 77fd250b c1cd9917 1b354bc3 fa905bff 73b6f04a cbfd9704 f18430d5 45033de8 b0ea3feb 0b448166 5d9e894e 1d1fafdd afea7be7 4c97cbe5 947f8048 61d111d1 7026b3fa 2a273419 b1fb99e9 f3825952 84d860d2 5254de7c 632b84dd
sp196 b c486e417 77fd250b c1cd9917 1b354bc3 fa904c05 7336f04b dadd8701 f18430d1 45033de8 b0eabfef 0b448166 5d9e894e 1d1f9fe3 afe2fbe6 9c1fcf6c d97f084c 61d111d9 5fa73402 3ae73411 b1fb19e1 f382d956 84d860d2 5254de7c 632b84dd
sp197 a e9ad2e9a 64d18a02 cb163312 81f869c6 052fbbfa ac895a4e 63691d0c 8c7d9f56 b8e4f32f d08f1dc9 05c612a8 c24300c8 1d1fafdd afa878e7 4c97cbe5 947f8048 61d531d3 f02293fa 2a272c1d 317f81e8 e8e71c59 c5f3e8d2 3ae54032 57361c3c
sp197 b e9ad2e9a 64d18a02 cb163312 81f869c6 052fac00 ac095a4f 72490d09 8c7d9f52 b8e4f32f d08f9dcd 05c612a8 c24300c8 1d1f9fe3 afa0f8e6 9c1fcf6c d97f084c 61d531db dfa31402 3ae72c15 317f01e0 e8e79c5d c5f3e8d2 3ae54032 57361c3c
sp198 a 33555a54 8fef6503 d49d650c 8857b7c5 f99073fb 16e5cc4c 01b9530c 9ad7c6df 0a8caf86 300c16ea 4e1b7cf9 3a697cd1 1d1fafdd adcb79e7 4c97cbe5 943bc249 61d503d3 7026b3fa 2a3f1c1d f175b9e9 984a3c58 9dc59685 1cecd875 053a0a6d
sp198 b 33555a54 8fef6503 d49d650c 8857b7c5 f9906401 1665cc4d 10994309 9ad7c6db 0a8caf86 300c96ee 4e1b7cf9 3a697cd1 1d1f9fe3 adc3f9e6 9c1fcf6c d93b4a4d 61d503db 5fa73402 3aff1c15 f17539e1 984abc5c 9dc59685 1cecd875 053a0a6d
sp199 a a7b1e1d8 87839a4d 076b0266 0fb3f8aa 066f93fe cf96a322 4563dc6c 497e881c 5179ced5 27d76a72 2e1026b8 4eac7a53 1d1fafdd af8a7ae7 4c97cbe5 947f8048 61d541d1 f02293fa aa270c18 f1f9f9e8 e7a75253 ab6cdeb0 d8ea70cf cd0f7db3
sp199 b a7b1e1d8 87839a4d 076b0266 0fb3f8aa 066f8404 cf16a323 5443cc69 497e8818 5179ced5 27d7ea76 2e1026b8 4eac7a53 1d1f9fe3 af82fae6 9c1fcf6c d97f084c 61d541d9 dfa31402 bae70c10 f1f979e0 e7a7d257 ab6cdeb0 d8ea70cf cd0f7db3
sp200 a deae0396 56acdd46 10e86d6b 6f40b7a7 f99073ff f0f1442a 8dfb536c 74872545 c8d36bf8 ec623282 30bcb86c a40bd2c7 1d1fafdd ad8979e7 4c97cbe5 947f8048 61d121d1 f02293fa 2a2f0418 f1f1a1e8 f6825352 89e2efb4 105af1cf 200a8729
sp200 b deae0396 56acdd46 10e86d6b 6f40b7a7 f9906405 f071442b 9cdb4369 74872541 c8d36bf8 ec62b286 30bcb86c a40bd2c7 1d1f9fe3 ad81f9e6 9c1fcf6c d97f084c 61d121d9 dfa31402 3aef0410 f1f121e0 f682d356 89e2efb4 105af1cf 200a8729
sp201 a 2225fd92 f3088b3e f7546749 0abdbd80 066f9bfa a384ee0c a32d394e 033aebcc b37fe44d 2105035b f0d70292 9432165a 1d1fafdd afeb7be7 4c97cbe5 946f8048 61c101d3 7026b3fa aa2f3419 f16df1ec dfa34759 54c1244e fb3d4c30 931700a7
sp201 b 2225fd92 f3088b3e f7546749 0abdbd80 066f8c00 a304ee0d b20d294b 033aebc8 b37fe44d 2105835f f0d70292 9432165a 1d1f9fe3 afe3fbe6 9c1fcf6c d96f084c 61c101db 5fa73402 baef3411 f16d71e4 dfa3c75d 54c1244e fb3d4c30 931700a7
sp202 a 1b012b59 9edf8f89 54631a82 d4b6084a 066f93fe 039433c2 4d64dc8c 2b337afc 77607227 291a153b 93bfcb09 bd0bfb89 1d1fa7dd ade878e7 4cd7cae5 943b8248 61d513d1 f02293fa aa27141c f175d9e8 876b34db 393e10d2 d0ed67b3 fa9e9470
sp202 b 1b012b59 9edf8f89 54631a82 d4b6084a 066f8404 031433c3 5c44cc89 2b337af8 77607227 291a953f 93bfcb09 bd0bfb89 1d1f97e3 ade0f8e6 9c5fce6c d93b0a4c 61d513d9 dfa31402 bae71414 f17559e0 876bb4df 393e10d2 d0ed67b3 fa9e9470
sp203 a a92eafc5 1d338b39 74832344 fde81194 052fb3fe a8976218 ed2cdadc a27acdf6 30eca2d1 503607c8 5fd9020f 037d39ef 1d1fa7dd afab7be7 4c97cbe5 946bc049 61c111d1 7026b3fa 2a373419 b17781e8 e2e7585b 4836b103 31455aa3 a9d4cdba
sp203 b a92eafc5 1d338b39 74832344 fde81194 052fa404 a8176219 fc0ccad9 a27acdf2 30eca2d1 503687cc 5fd9020f 037d39ef 1d1f97e3 afa3fbe6 9c1fcf6c d96b484d 61c111d9 5fa73402 3af73411 b17701e0 e2e7d85f 4836b103 31455aa3 a9d4cdba
sp204 a c2cd08f3 eed02789 25e80baf 5e88117e 052fb3fe 64d4a2f2 476a3bbe 602caf6c 92e3a50f 900d004b c5616be3 ce0462b2 1d1fafdd ad8878e7 4c97cbe5 947fc049 61d111d1 7026b3fa aa3f1418 71e5f1ed eee305db 961cb129 56ffd9c0 aa5d5b04
sp204 b c2cd08f3 eed02789 25e80baf 5e88117e 052fa404 6454a2f3 564a2bbb 602caf68 92e3a50f 900d804f c5616be3 ce0462b2 1d1f9fe3 ad80f8e6 9c1fcf6c d97f484d 61d111d9 5fa73402 baff1410 71e571e5 eee385df 961cb129 56ffd9c0 aa5d5b04
sp205 a f2696a48 71daa502 1cc30518 d03ddfd1 f9907bff 76f46458 0fb91514 92c8c087 42c9c412 932c41f9 074f36ec 6cd6663d 1d1fafdd afc97be7 4cd7cae5 943bc249 61d543d1 7026b3fa aa3f1c1d 71e999ed 964a7452 4418fc81 8ead176f 8bacb08b
sp205 b f2696a48 71daa502 1cc30518 d03ddfd1 f9906c05 76746459 1e990511 92c8c083 42c9c412 932cc1fd 074f36ec 6cd6663d 1d1f9fe3 afc1fbe6 9c5fce6c d93b4a4d 61d543d9 5fa73402 baff1c15 71e919e5 964af456 4418fc81 8ead176f 8bacb08b
sp206 a 08c0ddf4 f7233406 ead3d71d 5be36dd4 062f9bfe e39d5658 a52c7e96 cb7ddfa4 776a9591 4ef97923 d3cd17df 3cb164a7 1d1fafdd afc87ae7 4cd7cae5 942f8248 61d513d1 f02293fa 2a3f141c 31f389e8 7fb7525b 5760ec3c f949c5a9 10fe0108
sp206 b 08c0ddf4 f7233406 ead3d71d 5be36dd4 062f8c04 e31d5659 b40c6e93 cb7ddfa0 776a9591 4ef9f927 d3cd17df 3cb164a7 1d1f9fe3 afc0fae6 9c5fce6c d92f0a4c 61d513d9 dfa31402 3aff1414 31f309e0 7fb7d25f 5760ec3c f949c5a9 10fe0108
sp207 a 22a76b4d 5467918e 4c3453b7 48d9a97a 062f9bfe 85d4b2f2 696bfc36 252b3fbc d9627aab 7ea65aa2 11b6a4ed 2009c59f 1d1fafdd adea78e7 4c97cbe5 947bc049 61d141d1 f02293fa 2a2f3c19 31f7f9e8 ebe75d5b f4ce805f 34ee4105 b38c5515
sp207 b 22a76b4d 5467918e 4c3453b7 48d9a97a 062f8c04 8554b2f3 784bec33 252b3fb8 d9627aab 7ea6daa6 11b6a4ed 2009c59f 1d1f9fe3 ade2f8e6 9c1fcf6c d97b484d 61d141d9 dfa31402 3aef3c11 31f779e0 ebe7dd5f f4ce805f 34ee4105 b38c5515
sp208 a 481fd8b6 c000ca89 5c120b89 befc515c 052fb3fe ac9b02d0 ef2dba16 60372e16 7ceb2ba5 5e767383 49c9ffb3 36cae3f9 1d1fafdd afe97be7 4cd7cae5 946f8048 61d521d1 f02293fa 2a372c18 31ff99e8 e0b74f53 cde93e8e af00b425 707cf5fd
sp208 b 481fd8b6 c000ca89 5c120b89 befc515c 052fa404 ac1b02d1 fe0daa13 60372e12 7ceb2ba5 5e76f387 49c9ffb3 36cae3f9 1d1f9fe3 afe1fbe6 9c5fce6c d96f084c 61d521d9 dfa31402 3af72c10 31ff19e0 e0b7cf57 cde93e8e af00b425 707cf5fd
sp209 a 47b769f8 06d12349 108d1e68 03920cbc 052fbbfe 889ab730 2f239874 e421bebe d2bed939 13b559f8 ec0b78f7 71697efe 1d1fa7dd ad887be7 4c97cbe5 947fc049 61c521d1 7026b3fa 2a2f0c19 716d81ed eed712db 6c3e6c2d ef32650b 341b8e56
sp209 b 47b769f8 06d12349 108d1e68 03920cbc 052fac04 881ab731 3e038871 e421beba d2bed939 13b5d9fc ec0b78f7 71697efe 1d1f97e3 ad80fbe6 9c1fcf6c d97f484d 61c521d9 5fa73402 3aef0c11 716d01e5 eed792df 6c3e6c2d ef32650b 341b8e56
sp210 a 66f9cf17 4b690d3d 3b31235a 89ca9996 062f9bfa 4f814a1e e76c9adc af29efde bd3ba8bb 140101c1 4f0c2f3f 79e26a57 1d1fafdd af8a7be7 4cd7cae5 946f8048 61c101d3 7026b3fa 2a3f3c18 717da1e8 dfa34759 a925c83c 36cdf3a1 5d0beb71
sp210 b 66f9cf17 4b690d3d 3b31235a 89ca9996 062f8c00 4f014a1f f64c8ad9 af29efda bd3ba8bb 140181c5 4f0c2f3f 79e26a57 1d1f9fe3 af82fbe6 9c5fce6c d96f084c 61c101db 5fa73402 3aff3c10 717d21e0 dfa3c75d a925c83c 36cdf3a1 5d0beb71
sp211 a 3b5bcdb6 ef83037f 164805bf 8a343773 f99073fb 7ae9ecfe 8ffa93bc 5a9465d7 6cc20492 fbc07b19 3cd08d1d 3a00da5e 1d1fa7dd afe878e7 4c97cbe5 947b8048 61d101d3 7026b3fa aa37141c b1eb81ec f2864cd8 755f665c 0e67d1c5 037f9797
sp211 b 3b5bcdb6 ef83037f 164805bf 8a343773 f9906401 7a69ecff 9eda83b9 5a9465d3 6cc20492 fbc0fb1d 3cd08d1d 3a00da5e 1d1f97e3 afe0f8e6 9c1fcf6c d97b084c 61d101db 5fa73402 baf71414 b1eb01e4 f286ccdc 755f665c 0e67d1c5 037f9797
sp212 a 966014ba 7173d905 e38eca2d 40f2d8fc 056fb3fa 208aab74 e3223bbe 6274cfbc 74b4cb55 067876e3 c4df3ab1 6c3e7468 1d1fafdd afcb79e7 4c97cbe5 946b8048 61c101d3 f02293fa aa2f0418 b16399ed dea741d9 57d748e6 3b48097b 6fa2f4f5
sp212 b 966014ba 7173d905 e38eca2d 40f2d8fc 056fa400 200aab75 f2022bbb 6274cfb8 74b4cb55 0678f6e7 c4df3ab1 6c3e7468 1d1f9fe3 afc3f9e6 9c1fcf6c d96b084c 61c101db dfa31402 baef0410 b16319e5 dea7c1dd 57d748e6 3b48097b 6fa2f4f5
sp213 a f06fd941 8fbfeafa 2c2fc227 6ebd78f6 056fb3fe ec9dc37a 6563fc3e 82396a56 58224ba7 c5c92951 245dbe3b 822bfcbb 1d1fafdd afc97be7 4cd7cae5 942bc249 61c503d1 7026b3fa aa3f2c18 71e599ec 826b3a53 c64f6057 39124040 88b03500
sp213 b f06fd941 8fbfeafa 2c2fc227 6ebd78f6 056fa404 ec1dc37b 7443ec3b 82396a52 58224ba7 c5c9a955 245dbe3b 822bfcbb 1d1f9fe3 afc1fbe6 9c5fce6c d92b4a4d 61c503d9 5fa73402 baff2c10 71e519e4 826bba57 c64f6057 39124040 88b03500
sp214 a d4947946 3eba01c7 054b8cff 266cbe37 f9d07bff f4bd65ba a1f6d4fc b4d2801d 44c0cace 64a11cc2 68392398 037b7d28 1d1fa7dd adca78e7 4cd7cae5 947f8048 61c111d1 f02293fa aa27041c 716989ec f5f24452 7ded9062 7c176143 f0b74395
sp214 b d4947946 3eba01c7 054b8cff 266cbe37 f9d06c05 f43d65bb b0d6c4f9 b4d28019 44c0cace 64a19cc6 68392398 037b7d28 1d1f97e3 adc2f8e6 9c5fce6c d97f084c 61c111d9 dfa31402 bae70414 716909e4 f5f2c456 7ded9062 7c176143 f0b74395
sp215 a a24e63a5 682b6546 ea01ec4a c164be87 f99073ff 50b3450a a5f0d3c4 389d216f 4ac10170 e57827d3 1485ef67 672fd395 1d1fafdd af897be7 4cd7cae5 943b8248 61c503d1 f02293fa 2a3f3418 b16789ed 927a3bda e275bec8 f879a077 13b6bdc6
sp215 b a24e63a5 682b6546 ea01ec4a c164be87 f9906405 5033450b b4d0c3c1 389d216b 4ac10170 e578a7d7 1485ef67 672fd395 1d1f9fe3 af81fbe6 9c5fce6c d93b0a4c 61c503d9 dfa31402 3aff3410 b16709e5 927abbde e275bec8 f879a077 13b6bdc6
sp216 a 792c52c9 b831683a 7cbf8645 50d61494 056fb3fe ecdde718 892479d6 ce2d6d04 16a803f9 8bde689a 4f30cad5 b9d7bdcd 1d1fafdd afab78e7 4c97cbe5 947b8048 61d111d1 f02293fa aa272c19 b1ffc1e9 e6a714d3 8bec4d04 952de366 049a90d1
sp216 b 792c52c9 b831683a 7cbf8645 50d61494 056fa404 ec5de719 980469d3 ce2d6d00 16a803f9 8bdee89e 4f30cad5 b9d7bdcd 1d1f9fe3 afa3f8e6 9c1fcf6c d97b084c 61d111d9 dfa31402 bae72c11 b1ff41e1 e6a794d7 8bec4d04 952de366 049a90d1
sp217 a f960a7cd 8b5adfcd a695cac4 05e6f808 066f93fe c99ba380 ed205ac4 c774ca0c db29848f ea526209 2bcb6119 85081298 1d1fafdd adea78e7 4cd7cae5 942bc249 61d513d1 7026b3fa 2a270c18 f17199e9 837b6b53 f348c113 313db1ba d0f0c783
sp217 b f960a7cd 8b5adfcd a695cac4 05e6f808 066f8404 c91ba381 fc004ac1 c774ca08 db29848f ea52e20d 2bcb6119 85081298 1d1f9fe3 ade2f8e6 9c5fce6c d92b4a4d 61d513d9 5fa73402 3ae70c10 f17119e1 837beb57 f348c113 313db1ba d0f0c783
sp218 a 7054e639 549b6a0a 3721e22e 06c118fe 056fb3fe 02d50372 eb639c34 e6256a7c 3e7e0073 8fc07811 8fc3f68d f3d18504 1d1fa7dd afaa7ae7 4c97cbe5 946f8048 61c111d1 7026b3fa 2a270418 71edc9ec e0a34853 edfa10aa 32fea94b 32849af6
sp218 b 7054e639 549b6a0a 3721e22e 06c118fe 056fa404 02550373 fa438c31 e6256a78 3e7e0073 8fc0f815 8fc3f68d f3d18504 1d1f97e3 afa2fae6 9c1fcf6c d96f084c 61c111d9 5fa73402 3ae70410 71ed49e4 e0a3c857 edfa10aa 32fea94b 32849af6
sp219 a 691abfe5 d656f09b cc51c8bc 9671ba69 fa905bff 17f7a1e0 ebb296ac 3f81e55d 0991ad64 33ae4f78 c81e714b 7da90579 1d1fa7dd afc879e7 4c97cbe5 946fc049 61d171d1 f02293fa aa372c19 b1ef89ed ef9302da 60d590b7 32bb868f 8b519e7b
sp219 b 691abfe5 d656f09b cc51c8bc 9671ba69 fa904c05 1777a1e1 fa9286a9 3f81e559 0991ad64 33aecf7c c81e714b 7da90579 1d1f97e3 afc0f9e6 9c1fcf6c d96f484d 61d171d9 dfa31402 baf72c11 b1ef09e5 ef9382de 60d590b7 32bb868f 8b519e7b
sp220 a 47e034be ec28cec2 452e91d8 fa078b11 f99073ff dafc7098 45b95654 bac1d15d 2652b2e0 905a346a 86641bb7 a94c3f46 1d1fa7dd adca7be7 4c97cbe5 947bc049 61d101d1 7026b3fa aa371c19 316ff1ed f8864a5a 1faae0c1 58a8d72b 0f7a5ab5
sp220 b 47e034be ec28cec2 452e91d8 fa078b11 f9906405 da7c7099 54994651 bac1d159 2652b2e0 905ab46e 86641bb7 a94c3f46 1d1f97e3 adc2fbe6 9c1fcf6c d97b484d 61d101d9 5fa73402 baf71c11 316f71e5 f886ca5e 1faae0c1 58a8d72b 0f7a5ab5
sp221 a 77ed4b3a 84435cca 88b913d6 e28bc906 056fb3fe 4c97f28a 616c5bcc 6e76d924 d2b69fa5 da03422b 0dd86369 574b0e1b 1d1fa7dd afcb7be7 4cd7cae5 943b8248 61d523d1 7026b3fa aa373418 b17bd1e8 866b23db 6e436ecc 3cf208b3 dffd4ecc
sp221 b 77ed4b3a 84435cca 88b913d6 e28bc906 056fa404 4c17f28b 704c4bc9 6e76d920 d2b69fa5 da03c22f 0dd86369 574b0e1b 1d1f97e3 afc3fbe6 9c5fce6c d93b0a4c 61d523d9 5fa73402 baf73410 b17b51e0 866ba3df 6e436ecc 3cf208b3 dffd4ecc
sp222 a d938486a 32c512ce 00be97c3 56d4ad0e 062f9bfe 61d73682 036dbe4e 056d1efc 9fbf7163 a6f36bc3 a8c7cd9e 75669cad 1d1fa7dd adc979e7 4c97cbe5 947fc049 61c131d1 7026b3fa aa272c19 f1e981ec edd344db 90c8df1d 9ae44f31 8d4c3edb
sp222 b d938486a 32c512ce 00be97c3 56d4ad0e 062f8c04 61573683 124dae4b 056d1ef8 9fbf7163 a6f3ebc7 a8c7cd9e 75669cad 1d1f97e3 adc1f9e6 9c1fcf6c d97f484d 61c131d9 5fa73402 bae72c11 f1e901e4 edd3c4df 90c8df1d 9ae44f31 8d4c3edb
sp223 a 50fdeab9 0adac906 5ebbb238 82d208f4 062f93fe 499e7378 e1225db4 af75594c 79a51693 0e566380 be95fc4e dac18065 1d1fafdd ad897be7 4cd7cae5 947fc049 61c131d1 7026b3fa 2a271c18 317fb1e9 ed9342db a941a027 3cefa0ca 28c23481
sp223 b 50fdeab9 0adac906 5ebbb238 82d208f4 062f8404 491e7379 f0024db1 af755948 79a51693 0e56e384 be95fc4e dac18065 1d1f9fe3 ad81fbe6 9c5fce6c d97f484d 61c131d9 5fa73402 3ae71c10 317f31e1 ed93c2df a941a027 3cefa0ca 28c23481
sp224 a c201c50a b301f58a 5cd985af 9b465f7b fad05bff 35bd24f2 09ffd234 9f89e117 4d9d827c be944e81 8a700df1 6d99469b 1d1fa7dd adca7ae7 4c97cbe5 943b8248 61d523d1 7026b3fa aa3f3c18 b16781ec 930a7cda 871f3d64 94a6994b aad9d5fe
sp224 b c201c50a b301f58a 5cd985af 9b465f7b fad04c05 353d24f3 18dfc231 9f89e113 4d9d827c be94ce85 8a700df1 6d99469b 1d1f97e3 adc2fae6 9c1fcf6c d93b0a4c 61d523d9 5fa73402 baff3c10 b16701e4 930afcde 871f3d64 94a6994b aad9d5fe
sp225 a 3f1e2a1e e6c49afa ed615e23 f0b644f6 056fb3fe 4cd2777a 0567f83e 88669bf6 507a9939 1b677699 ad013287 fea152ac 1d1fafdd adcb7be7 4c97cbe5 946bc049 61c111d1 f02293fa 2a372c1c f1ed81ed e4a7505b 25d77ba1 990a2500 17bf2221
sp225 b 3f1e2a1e e6c49afa ed615e23 f0b644f6 056fa404 4c52777b 1447e83b 88669bf2 507a9939 1b67f69d ad013287 fea152ac 1d1f9fe3 adc3fbe6 9c1fcf6c d96b484d 61c111d9 dfa31402 3af72c14 f1ed01e5 e4a7d05f 25d77ba1 990a2500 17bf2221
sp226 a e6f973a2 acf66ccf 29cf31d7 9b29eb1b f9d073ff dcbfb092 c9fdd054 1a97f0df 6052d58a 5b5072bb 3d507f9f 82800a36 1d1fafdd afa87be7 4c97cbe5 942b8248 61c503d1 7026b3fa aa373418 b173f9e9 8a4a79da d64e7340 d4b0b32b 33e45f12
sp226 b e6f973a2 acf66ccf 29cf31d7 9b29eb1b f9d06405 dc3fb093 d8ddc051 1a97f0db 6052d58a 5b50f2bf 3d507f9f 82800a36 1d1f9fe3 afa0fbe6 9c1fcf6c d92b0a4c 61c503d9 5fa73402 baf73410 b17379e1 8a4af9de d64e7340 d4b0b32b 33e45f12
sp227 a 952ea722 2e936c8e 714a55b1 78772f7d f99073ff 18bbb4f0 a3be95b4 549bb2d7 a6479a00 660347c3 57010d9d bff96cc5 1d1fafdd ada879e7 4cd7cae5 943bc249 61c543d1 f02293fa aa37241c 717581e8 987a7c52 1c6e4fe9 7aa38e8a 494dd75a
sp227 b 952ea722 2e936c8e 714a55b1 78772f7d f9906405 183bb4f1 b29e85b1 549bb2d3 a6479a00 6603c7c7 57010d9d bff96cc5 1d1f9fe3 ada0f9e6 9c5fce6c d93b4a4d 61c543d9 dfa31402 baf72414 717501e0 987afc56 1c6e4fe9 7aa38e8a 494dd75a
sp228 a 5ac2daa1 9444345b 99382d7e fa28ffaf fa905bff 73b20422 23ff936c 7b97e1af 6704e23a 7ba35c3b 340b38e5 d4284b25 1d1fa7dd ad897ae7 4c97cbe5 943b8248 61c523d1 f02293fa 2a3f041c 31f3b9e9 937a7cda c1670034 7aaaafd3 60d01ec0
sp228 b 5ac2daa1 9444345b 99382d7e fa28ffaf fa904c05 73320423 32df8369 7b97e1ab 6704e23a 7ba3dc3f 340b38e5 d4284b25 1d1f97e3 ad81fae6 9c1fcf6c d93b0a4c 61c523d9 dfa31402 3aff0414 31f339e1 937afcde c1670034 7aaaafd3 60d01ec0
sp229 a f069ae4c 569f0ff7 84994c27 447bf6f7 fad053fb 3be9ed7e 85f6d3bc 73cbc69d e1df8fca ce3c54a1 afe412d7 9aa3673d 1d1fafdd ad8b78e7 4cd7cae5 947f8048 61c101d3 7026b3fa 2a273c18 3163f1ed f4f25458 bebc27dc 981bbac1 644047b7
sp229 b f069ae4c 569f0ff7 84994c27 447bf6f7 fad04401 3b69ed7f 94d6c3b9 73cbc699 e1df8fca ce3cd4a5 afe412d7 9aa3673d 1d1f9fe3 ad83f8e6 9c5fce6c d97f084c 61c101db 5fa73402 3ae73c10 316371e5 f4f2d45c bebc27dc 981bbac1 644047b7
sp230 a 840a2329 0d2f2a89 c6588397 b9eeb946 052fb3fe c89c42ca e5687b8e 64708906 5424c1b5 578c5ed1 aafe50a8 ba5e230a 1d1fafdd afe87be7 4c97cbe5 946fc049 61d111d1 f02293fa aa2f1419 7169f9ec e4f340db b000ee51 38fd89ad 31c14bea
sp230 b 840a2329 0d2f2a89 c6588397 b9eeb946 052fa404 c81c42cb f4486b8b 64708902 5424c1b5 578cded5 aafe50a8 ba5e230a 1d1f9fe3 afe0fbe6 9c1fcf6c d96f484d 61d111d9 dfa31402 baef1411 716979e4 e4f3c0df b000ee51 38fd89ad 31c14bea
sp231 a d97e1b94 dec16387 e66ed9ab 0d5c0b7b fa905bff 1db9b0f2 69fe57bc 5f8df485 891a9eb6 d9940f19 785d2af1 683f09c8 1d1fa7dd adea7ae7 4c97cbe5 946f8048 61d171d1 7026b3fa aa273c18 7179a1e8 ed930052 dcf5e0a6 346405c3 b6a3898c
sp231 b d97e1b94 dec16387 e66ed9ab 0d5c0b7b fa904c05 1d39b0f3 78de47b9 5f8df481 891a9eb6 d9948f1d 785d2af1 683f09c8 1d1f97e3 ade2fae6 9c1fcf6c d96f084c 61d171d9 5fa73402 bae73c10 717921e0 ed938056 dcf5e0a6 346405c3 b6a3898c
sp232 a bed83ffd b082c8d5 7d77c2da 659a180a 052fb3fe 02db8382 c7649acc ac292a96 3e2069b5 1eee7aa2 0c44cda3 2168fe78 1d1fa7dd adaa7be7 4c97cbe5 947f8048 61d121d1 f02293fa aa3f1c19 f1ede1ec eae31953 77d7ae5c 5701c270 6290f07c
sp232 b bed83ffd b082c8d5 7d77c2da 659a180a 052fa404 025b8383 d6448ac9 ac292a92 3e2069b5 1eeefaa6 0c44cda3 2168fe78 1d1f97e3 ada2fbe6 9c1fcf6c d97f084c 61d121d9 dfa31402 baff1c11 f1ed61e4 eae39957 77d7ae5c 5701c270 6290f07c
sp233 a 56d3c445 374020c6 819dc4fd 632e5e31 f9907bff babae5b8 afb214f4 30da0427 a81e67a0 4c9e0ea1 81428034 f4b5fc7e 1d1fafdd afea79e7 4c97cbe5 943bc249 61d543d1 f02293fa aa3f2c1d 717d81e9 964a7452 802d5d21 6ef8164b 6d3b64ad
sp233 b 56d3c445 374020c6 819dc4fd 632e5e31 f9906c05 ba3ae5b9 be9204f1 30da0423 a81e67a0 4c9e8ea5 81428034 f4b5fc7e 1d1f9fe3 afe2f9e6 9c1fcf6c d93b4a4d 61d543d9 dfa31402 baff2c15 717d01e1 964af456 802d5d21 6ef8164b 6d3b64ad
sp234 a 0cf3a78e 4999628e 619b6ba6 77f0b96e 062f93fe 6ddf02e2 436b1c24 c136291c 3d3468e9 9d2110b1 6a7e8bfe 2cbe9a67 1d1fa7dd af887be7 4c97cbe5 942f8248 61d503d1 f02293fa aa2f1419 717db1e8 7ff7515b cd573ef0 db3b3718 d54f9fd1
sp234 b 0cf3a78e 4999628e 619b6ba6 77f0b96e 062f8404 6d5f02e3 524b0c21 c1362918 3d3468e9 9d2190b5 6a7e8bfe 2cbe9a67 1d1f97e3 af80fbe6 9c1fcf6c d92f0a4c 61d503d9 dfa31402 baef1411 717d31e0 7ff7d15f cd573ef0 db3b3718 d54f9fd1
sp235 a 7dbbb097 2f46f0f1 bedbc221 07bc18f4 056fb3fa 26c64b7c e1277a36 a630ef04 94a0e1eb d77066d3 621a6714 ebb34355 1d1fa7dd adc979e7 4c97cbe5 946f8048 61d511d3 f02293fa aa370c1d 71f9f1e8 e2b74959 4db5f720 3d46c308 f41d7f4a
sp235 b 7dbbb097 2f46f0f1 bedbc221 07bc18f4 056fa400 26464b7d f0076a33 a630ef00 94a0e1eb d770e6d7 621a6714 ebb34355 1d1f97e3 adc1f9e6 9c1fcf6c d96f084c 61d511db dfa31402 baf70c15 71f971e0 e2b7c95d 4db5f720 3d46c308 f41d7f4a
sp236 a 42e0df1d cc7b9a8a 223f1ea6 7bcf0c6e 066f93fa a3c03fe6 a56258a4 2521bf6e f576bc01 b96b3398 588207d7 26333297 1d1fafdd adc87be7 4c97cbe5 946f8048 61c111d3 7026b3fa 2a2f3c19 716da1ed e1a35f59 56b0d236 790824da f323dd67
sp236 b 42e0df1d cc7b9a8a 223f1ea6 7bcf0c6e 066f8400 a3403fe7 b44248a1 2521bf6a f576bc01 b96bb39c 588207d7 26333297 1d1f9fe3 adc0fbe6 9c1fcf6c d96f084c 61c111db 5fa73402 3aef3c11 716d21e5 e1a3df5d 56b0d236 790824da f323dd67
sp237 a 9c561a04 34d0bf8a cd5996ae 6ebbec7a 056fbbfe a89ab7f2 2b6618bc a6387f7e ba227c55 f77e7172 84a18549 4f3cfa0b 1d1fafdd afab7ae7 4c97cbe5 942b8248 61d123d1 f02293fa 2a3f341d 71e1a1ec 7eb752db 90687ae4 73545a84 7a457937
sp237 b 9c561a04 34d0bf8a cd5996ae 6ebbec7a 056fac04 a81ab7f3 3a4608b9 a6387f7a ba227c55 f77ef176 84a18549 4f3cfa0b 1d1f9fe3 afa3fae6 9c1fcf6c d92b0a4c 61d123d9 dfa31402 3aff3415 71e121e4 7eb7d2df 90687ae4 73545a84 7a457937
sp238 a d3d64158 46cc4afe 8ef5cb09 f48159c4 066f9bfa cfc94a4c c9287c8e 6721ee96 953bef9d db9f5cb8 66a65ee0 99ea2d1b 1d1fafdd af8b7be7 4c97cbe5 946b8048 61c101d3 f02293fa aa3f0418 b17b99e9 dda757d9 a8d8a80e 5551c8ab 630e1417
sp238 b d3d64158 46cc4afe 8ef5cb09 f48159c4 066f8c00 cf494a4d d8086c8b 6721ee92 953bef9d db9fdcbc 66a65ee0 99ea2d1b 1d1f9fe3 af83fbe6 9c1fcf6c d96b084c 61c101db dfa31402 baff0410 b17b19e1 dda7d7dd a8d8a80e 5551c8ab 630e1417
sp239 a 9e139f65 26f1394e c8ea8370 60bcf9bc 062f93fe 67db0230 4f2a1afc e730e85c 7b69e85b 331146da cd3d7367 233f05ee 1d1fafdd ade979e7 4cd7cae5 947fc049 61d501d1 f02293fa aa270419 f179e1e9 eda714db 14a941a9 cee3eb3f 2af905d3
sp239 b 9e139f65 26f1394e c8ea8370 60bcf9bc 062f8404 675b0231 5e0a0af9 e730e858 7b69e85b 3311c6de cd3d7367 233f05ee 1d1f9fe3 ade1f9e6 9c5fce6c d97f484d 61d501d9 dfa31402 bae70411 f17961e1 eda794df 14a941a9 cee3eb3f 2af905d3
sp240 a 09c24bbb 34fe973f bffad14a c821cb83 f99073fb 94aef80e 43fd174c fcda9347 4c839f1c 0e124621 ee6918f3 9aff07a3 1d1fafdd af887be7 4c97cbe5 947f8048 61d121d3 7026b3fa aa3f3418 b16f81ec f4825158 5bea58d0 5a6d4e31 4d4927ab
sp240 b 09c24bbb 34fe973f bffad14a c821cb83 f9906401 942ef80f 52dd0749 fcda9343 4c839f1c 0e12c625 ee6918f3 9aff07a3 1d1f9fe3 af80fbe6 9c1fcf6c d97f084c 61d121db 5fa73402 baff3410 b16f01e4 f482d15c 5bea58d0 5a6d4e31 4d4927ab
sp241 a ad33f373 1d64fb5a 59cff35f f3b2c98a 056fb3fe 82d7b202 e5697b46 ec791a14 50a070d5 a4f628c0 614990b8 a230908b 1d1fa7dd ade879e7 4cd7cae5 943bc249 61c573d1 f02293fa aa272418 71f5e9e8 8c5b7453 b20a521d 38e898f4 aa70881d
sp241 b ad33f373 1d64fb5a 59cff35f f3b2c98a 056fa404 8257b203 f4496b43 ec791a10 50a070d5 a4f6a8c4 614990b8 a230908b 1d1f97e3 ade0f9e6 9c5fce6c d93b4a4d 61c573d9 dfa31402 bae72410 71f569e0 8c5bf457 b20a521d 38e898f4 aa70881d
sp242 a a69e737d 92e3e65a 76d6d15c fe2bab89 fad05bff 79fbb000 41b9d74c 5d9f3127 e346149c bc2f05a0 a39cf550 a893d992 1d1fafdd ade87ae7 4cd7cae5 947fc049 61c101d1 7026b3fa 2a2f1418 716d91ec f8f24bda 788d6459 dc604f32 b6823b88
sp242 b a69e737d 92e3e65a 76d6d15c fe2bab89 fad04c05 797bb001 5099c749 5d9f3123 e346149c bc2f85a4 a39cf550 a893d992 1d1f9fe3 ade0fae6 9c5fce6c d97f484d 61c101d9 5fa73402 3aef1410 716d11e4 f8f2cbde 788d6459 dc604f32 b6823b88
sp243 a ff2e21f2 572f700d 729afa35 11f5c8fc 066f93fe 0b9f1370 c326bdb6 4d3eb896 53bff66d 401f126a a76c7e32 51213e33 1d1fafdd afaa78e7 4c97cbe5 947b8048 61d131d1 f02293fa aa371c18 716991ed e5a754d3 6d1c2130 5b3b8f85 40db32fc
sp243 b ff2e21f2 572f700d 729afa35 11f5c8fc 066f8404 0b1f1371 d206adb3 4d3eb892 53bff66d 401f926e a76c7e32 51213e33 1d1f9fe3 afa2f8e6 9c1fcf6c d97b084c 61d131d9 dfa31402 baf71c10 716911e5 e5a7d4d7 6d1c2130 5b3b8f85 40db32fc
sp244 a 5e521bbf ce30cb16 2e3ab81e 1d6f2acf fa9053fb 3fe81946 43f41184 3f99720d 61805392 19881f98 fa9ff9ed 398680e5 1d1fa7dd afaa79e7 4c97cbe5 947f8048 61d101d3 f02293fa 2a2f0c19 3167f9ec f3825b58 309b1914 5a623bb6 9892b305
sp244 b 5e521bbf ce30cb16 2e3ab81e 1d6f2acf fa904401 3f681947 52d40181 3f997209 61805392 19889f9c fa9ff9ed 398680e5 1d1f97e3 afa2f9e6 9c1fcf6c d97f084c 61d101db dfa31402 3aef0c11 316779e4 f382db5c 309b1914 5a623bb6 9892b305
sp245 a 89ff2263 6a879547 ee78917e 9b31cbb3 f9d07bff 9ef5f03a ebfa96fc 5c80b157 a640db72 315a2579 819025de 04d47dfc 1d1fa7dd ada879e7 4cd7cae5 947f8048 61c111d1 7026b3fa 2a3f241d f1fd89e9 f5f24352 53db24e2 322fcf88 43b9131d
sp245 b 89ff2263 6a879547 ee78917e 9b31cbb3 f9d06c05 9e75f03b fada86f9 5c80b153 a640db72 315aa57d 819025de 04d47dfc 1d1f97e3 ada0f9e6 9c5fce6c d97f084c 61c111d9 5fa73402 3aff2415 f1fd09e1 f5f2c356 53db24e2 322fcf88 43b9131d
sp246 a 6cc08511 0abcb905 18a8de31 69cc2cfc 062f9bfa 8bce9f74 2327b836 057b1e7e fdec18a1 93d97b7b 77cf94bc 2a0896af 1d1fafdd adaa79e7 4cd7cae5 947f8048 61d501d3 f02293fa aa37041d b173f1e8 e9a70b59 e8b4a366 faf68e08 d4395faf
sp246 b 6cc08511 0abcb905 18a8de31 69cc2cfc 062f8c00 8b4e9f75 3207a833 057b1e7a fdec18a1 93d9fb7f 77cf94bc 2a0896af 1d1f9fe3 ada2f9e6 9c5fce6c d97f084c 61d501db dfa31402 baf70415 b17371e0 e9a78b5d e8b4a366 faf68e08 d4395faf
sp247 a ac68621f fee379c5 12cafbc5 fdb86908 062f9bfa a5853a84 c9287bc6 e9779f9c 5d7b915b 47de7853 191b2fa5 7da41af7 1d1fafdd ad8978e7 4c97cbe5 946f8048 61c111d3 7026b3fa 2a372418 b1efe9ec e1e35a59 552ada98 5549e9b7 6724a458
sp247 b ac68621f fee379c5 12cafbc5 fdb86908 062f8c00 a5053a85 d8086bc3 e9779f98 5d7b915b 47def857 191b2fa5 7da41af7 1d1f9fe3 ad81f8e6 9c1fcf6c d96f084c 61c111db 5fa73402 3af72410 b1ef69e4 e1e3da5d 552ada98 5549e9b7 6724a458
sp248 a 92d14364 c6e1520a a1e4b803 70410acb f99073ff f8fd9142 65f1d00c 7c8fb0e5 cc09dbcc adbe1911 0c537ad8 59af48fb 1d1fafdd adca78e7 4c97cbe5 947f8048 61d121d1 7026b3fa 2a2f041d b1e3c1ec f6825452 0199c39c b8686578 eb901a0e
sp248 b 92d14364 c6e1520a a1e4b803 70410acb f9906405 f87d9143 74d1c009 7c8fb0e1 cc09dbcc adbe9915 0c537ad8 59af48fb 1d1f9fe3 adc2f8e6 9c1fcf6c d97f084c 61d121d9 5fa73402 3aef0415 b1e341e4 f682d456 0199c39c b8686578 eb901a0e
sp249 a d572d64d aa47ae09 5371be32 aeb60cfa 066f9bfe ebdf9772 27631e3c 817a1ed6 bd725aa9 9d351711 abdbfe86 1f32bd64 1d1fa7dd afab78e7 4c97cbe5 947f8048 61d501d1 7026b3fa 2a2f1419 b1ffc1e8 e7a71453 0ee6cd68 f6f34744 d749be57
sp249 b d572d64d aa47ae09 5371be32 aeb60cfa 066f8c04 eb5f9773 36430e39 817a1ed2 bd725aa9 9d359715 abdbfe86 1f32bd64 1d1f97e3 afa3f8e6 9c1fcf6c d97f084c 61d501d9 5fa73402 3aef1411 b1ff41e0 e7a79457 0ee6cd68 f6f34744 d749be57
sp250 a e3d79571 8f0d1206 c9ab530e 52b6e9c6 062f9bfe 439f724a 45695d0c e5343eec bfb079ad 751f1472 9c8fc029 a3c8ad30 1d1fa7dd afe878e7 4cd7cae5 946f8048 61d101d1 7026b3fa aa3f3c19 71ede9ed dfb35253 b4f9e210 58d13174 29a1e3ab
sp250 b e3d79571 8f0d1206 c9ab530e 52b6e9c6 062f8c04 431f724b 54494d09 e5343ee8 bfb079ad 751f9476 9c8fc029 a3c8ad30 1d1f97e3 afe0f8e6 9c5fce6c d96f084c 61d101d9 5fa73402 baff3c11 71ed69e5 dfb3d257 b4f9e210 58d13174 29a1e3ab
sp251 a 940fe4e8 66b13982 b9384fa9 bddebd7c 052fb3fa a48a2ef4 af2ab9b6 48608c46 7ae78403 96b14ce3 1d79678d e7230886 1d1fa7dd ada87ae7 4c97cbe5 947b8048 61d111d3 7026b3fa 2a3f2c18 71e9c9ec e8e71ad9 4e072228 6f3fb3c7 c42d76cf
sp251 b 940fe4e8 66b13982 b9384fa9 bddebd7c 052fa400 a40a2ef5 be0aa9b3 48608c42 7ae78403 96b1cce7 1d79678d e7230886 1d1f97e3 ada0fae6 9c1fcf6c d97b084c 61d111db 5fa73402 3aff2c10 71e949e4 e8e79add 4e072228 6f3fb3c7 c42d76cf
sp252 a 1d2a7f7d b13609fe 17aea308 68c039c0 066f9bfa e3c86a4c e32d9b04 65698ff6 7fa5e441 5dfb3ab3 3302340d 70187fd6 1d1fa7dd adeb7ae7 4cd7cae5 943bc249 61d563d3 f02293fa aa37341c 7165b9ed 8b6b7d59 50ced811 3b349938 387821fc
sp252 b 1d2a7f7d b13609fe 17aea308 68c039c0 066f8c00 e3486a4d f20d8b01 65698ff2 7fa5e441 5dfbbab7 3302340d 70187fd6 1d1f97e3 ade3fae6 9c5fce6c d93b4a4d 61d563db dfa31402 baf73414 716539e5 8b6bfd5d 50ced811 3b349938 387821fc
sp253 a 35619b05 523b3387 6003f0bd fd234a71 f9d07bff b4b7f1f8 67b71134 d8ca123f ac4056ca c44f3141 5692fe6c cab3a847 1d1fa7dd ad8b7ae7 4cd7cae5 942bc249 61d503d1 7026b3fa 2a27141d 31fb89e8 905a7b52 088370d9 b6a7134f 0bc96ded
sp253 b 35619b05 523b3387 6003f0bd fd234a71 f9d06c05 b437f1f9 76970131 d8ca123b ac4056ca c44fb145 5692fe6c cab3a847 1d1f97e3 ad83fae6 9c5fce6c d92b4a4d 61d503d9 5fa73402 3ae71415 31fb09e0 905afb56 088370d9 b6a7134f 0bc96ded
sp254 a ad47a965 92ca8d07 b78bed33 9e3adffb f9907bfb 3ced2c76 a9ffd334 fcd48557 acddc350 a6d27f61 08404006 247e01f7 1d1fafdd afc87be7 4c97cbe5 947b8048 61d121d3 f02293fa 2a271c19 f161f9ec f28659d8 33680468 f4528a06 975d90f9
sp254 b ad47a965 92ca8d07 b78bed33 9e3adffb f9906c01 3c6d2c77 b8dfc331 fcd48553 acddc350 a6d2ff65 08404006 247e01f7 1d1f9fe3 afc0fbe6 9c1fcf6c d97b084c 61d121db dfa31402 3ae71c11 f16179e4 f286d9dc 33680468 f4528a06 975d90f9
sp255 a 6cd96ae6 079c6547 89c35168 a73dabb9 fa905bff b1f1b030 e1bf577c 5dc893af c180b0e6 354f32f2 44524592 8d7e2a13 1d1fafdd adc87be7 4c97cbe5 947fc049 61d101d1 f02293fa aa3f3c18 b17391e9 f9824ada c8b38129 3ca6e5be 6c671762
sp255 b 6cd96ae6 079c6547 89c35168 a73dabb9 fa904c05 b171b031 f09f4779 5dc893ab c180b0e6 354fb2f6 44524592 8d7e2a13 1d1f9fe3 adc0fbe6 9c1fcf6c d97f484d 61d101d9 dfa31402 baff3c10 b17311e1 f982cade c8b38129 3ca6e5be 6c671762
sp256 a ca1edab6 8b93c0fe e6b2cc2b d96696e3 f9d073fb 3eabcd6e abf695a4 d49a27c5 4a466e2e 76a85ec1 dfa5b461 3e21f7d3 1d1fa7dd afe879e7 4cd7cae5 947f8048 61c521d3 f02293fa 2a373418 71e189ec f3f65b58 3b8936f0 f227e095 3befdc6d
sp256 b ca1edab6 8b93c0fe e6b2cc2b d96696e3 f9d06401 3e2bcd6f bad685a1 d49a27c1 4a466e2e 76a8dec5 dfa5b461 3e21f7d3 1d1f97e3 afe0f9e6 9c5fce6c d97f084c 61c521db dfa31402 3af73410 71e109e4 f3f6db5c 3b8936f0 f227e095 3befdc6d
sp257 a 02c72a17 f4beb497 e07aed9a 3c77bf4b fa905bff 13b104c2 0dfdd20c d7cc4125 cd1b414a 7e646400 a9808ee7 267cb625 1d1fa7dd afc87be7 4cd7cae5 943b8248 61d523d1 f02293fa 2a273419 71e1c1ed 914a7bda 27293c94 9054a230 3d11b891
sp257 b 02c72a17 f4beb497 e07aed9a 3c77bf4b fa904c05 133104c3 1cddc209 d7cc4121 cd1b414a 7e64e404 a9808ee7 267cb625 1d1f97e3 afc0fbe6 9c5fce6c d93b0a4c 61d523d9 dfa31402 3ae73411 71e141e5 914afbde 27293c94 9054a230 3d11b891
sp258 a ae3f3ed8 6ef23351 a105877b f4f87daa 056fb3fa 84892e26 256a78e6 8c36ad84 762fc563 d94e21b8 e3ff024c 2fb812b5 1d1fa7dd adc979e7 4cd7cae5 943bc249 61d573d3 f02293fa 2a273418 f1edd1ed 8c6b7459 b03814f9 78e7ab52 0c92dcae
sp258 b ae3f3ed8 6ef23351 a105877b f4f87daa 056fa400 84092e27 344a68e3 8c36ad80 762fc563 d94ea1bc e3ff024c 2fb812b5 1d1f97e3 adc1f9e6 9c5fce6c d93b4a4d 61d573db dfa31402 3ae73410 f1ed51e5 8c6bf45d b03814f9 78e7ab52 0c92dcae
sp259 a dd298bfe 18e684cb a47665e1 630e3f29 f9d07bff d8bea4a0 8bbb946c 7ac342f5 86d12002 87576450 83ff81af 9212d88d 1d1fafdd afea79e7 4cd7cae5 943bc249 61d543d1 f02293fa 2a271419 7179b9e8 960a7452 62299e39 12967fcf 99c22f37
sp259 b dd298bfe 18e684cb a47665e1 630e3f29 f9d06c05 d83ea4a1 9a9b8469 7ac342f1 86d12002 8757e454 83ff81af 9212d88d 1d1f9fe3 afe2f9e6 9c5fce6c d93b4a4d 61d543d9 dfa31402 3ae71411 717939e0 960af456 62299e39 12967fcf 99c22f37
sp260 a dc2a3199 26170d4d 09c5f367 25d6e9ae 066f93fe 2f9e9222 cb6ebcee 6d31baec d568f143 ea727308 3759576e 50230a16 1d1fafdd afc97be7 4c97cbe5 943bc249 61d513d1 7026b3fa aa3f341c 71e1f9ec 896b2c53 8b56cf71 d3377694 ad283607
sp260 b dc2a3199 26170d4d 09c5f367 25d6e9ae 066f8404 2f1e9223 da4eaceb 6d31bae8 d568f143 ea72f30c 3759576e 50230a16 1d1f9fe3 afc1fbe6 9c1fcf6c d93b4a4d 61d513d9 5fa73402 baff3414 71e179e4 896bac57 8b56cf71 d3377694 ad283607
sp261 a 4321eeac 151bc10a 3cf93f0f 29c24dda 056fbbfe a6dd3652 a568fe96 0e2c7fbc 5263731d 117037d9 516a9752 b9c4f94a 1d1fa7dd adc979e7 4c97cbe5 946bc049 61d111d1 7026b3fa aa273c19 f1f9d9e8 e4b7525b 53e31cc9 f8f93ee9 84a935d5
sp261 b 4321eeac 151bc10a 3cf93f0f 29c24dda 056fac04 a65d3653 b448ee93 0e2c7fb8 5263731d 1170b7dd 516a9752 b9c4f94a 1d1f97e3 adc1f9e6 9c1fcf6c d96b484d 61d111d9 5fa73402 bae73c11 f1f959e0 e4b7d25f 53e31cc9 f8f93ee9 84a935d5
sp262 a 8387dc96 22d2f041 98ba1678 7ed20cb0 066f9bfe 8bd5d738 8f231e74 012abfce bb3eb3f1 7b09509b 55a27aff 375d5414 1d1fafdd afaa7ae7 4c97cbe5 947fc049 61c511d1 7026b3fa 2a3f0418 31e3d1ed eb971bdb 66f94d63 8f42e70a cb652aa4
sp262 b 8387dc96 22d2f041 98ba1678 7ed20cb0 066f8c04 8b55d739 9e030e71 012abfca bb3eb3f1 7b09d09f 55a27aff 375d5414 1d1f9fe3 afa2fae6 9c1fcf6c d97f484d 61c511d9 5fa73402 3aff0410 31e351e5 eb979bdf 66f94d63 8f42e70a cb652aa4
sp263 a 1bed42f8 ac799839 e12cb360 f6cbe1b4 052fb3fe 88d3d238 ed2f5b74 88611e24 3c397ea7 73496278 9ff981e0 3780fc73 1d1fa7dd afa978e7 4cd7cae5 947bc049 61c141d1 7026b3fa 2a273c18 b16b99ec ea974d5b 68144319 30e2f30a cfb61830
sp263 b 1bed42f8 ac799839 e12cb360 f6cbe1b4 052fa404 8853d239 fc0f4b71 88611e20 3c397ea7 7349e27c 9ff981e0 3780fc73 1d1f97e3 afa1f8e6 9c5fce6c d97b484d 61c141d9 5fa73402 3ae73c10 b16b19e4 ea97cd5f 68144319 30e2f30a cfb61830
sp264 a bc063fa6 9fa787fa ffb46224 2fca38f4 056fb3fe e0956378 e9225db4 a476092c f4e80a79 82cb7bcb f908c86f dc5c80e4 1d1fafdd afea78e7 4c97cbe5 947fc049 61c561d1 f02293fa 2a3f3418 f1edf9ec ec9755db 91fda1dd b543d786 e81fca07
sp264 b bc063fa6 9fa787fa ffb46224 2fca38f4 056fa404 e0156379 f8024db1 a4760928 f4e80a79 82cbfbcf f908c86f dc5c80e4 1d1f9fe3 afe2f8e6 9c1fcf6c d97f484d 61c561d9 dfa31402 3aff3410 f1ed79e4 ec97d5df 91fda1dd b543d786 e81fca07
sp265 a d54ac6b4 4a67b2d1 60a7a7fb e2c2dd2e 056fb3fa 648daea6 2b6ab9ee c634ee8c 58e3a7a3 bbb85898 e4c711bd 0cb42add 1d1fa7dd adc979e7 4c97cbe5 943bc249 61d573d3 7026b3fa 2a373419 f16df1ec 8c6b7459 5037b479 f333598f c640d926
sp265 b d54ac6b4 4a67b2d1 60a7a7fb e2c2dd2e 056fa400 640daea7 3a4aa9eb c634ee88 58e3a7a3 bbb8d89c e4c711bd 0cb42add 1d1f97e3 adc1f9e6 9c1fcf6c d93b4a4d 61d573db 5fa73402 3af73411 f16d71e4 8c6bf45d 5037b479 f333598f c640d926
sp266 a 22e945f8 c468429b 47e238be 680caa6b fa9053ff 75f6b1e2 45f3d12c f9c0128d c78d3cc2 a2f36aeb ba56e165 d94ed446 1d1fa7dd afca79e7 4c97cbe5 947f8048 61d501d1 f02293fa aa3f141c f1f981e9 f3865b52 04ac91f8 d8728413 2061c9e0
sp266 b 22e945f8 c468429b 47e238be 680caa6b fa904405 7576b1e3 54d3c129 f9c01289 c78d3cc2 a2f3eaef ba56e165 d94ed446 1d1f97e3 afc2f9e6 9c1fcf6c d97f084c 61d501d9 dfa31402 baff1414 f1f901e1 f386db56 04ac91f8 d8728413 2061c9e0
sp267 a 8eed9a1b 287eccc2 6d33bbe9 94898938 052fbbfa 6ccb9ab4 c52afbf6 0a24ffc4 1826f0cb 67104671 1a782366 7f1c67fc 1d1fa7dd afaa7be7 4cd7cae5 946f8048 61d531d3 f02293fa aa273c19 f1edc1ec e0b75f59 05bfa56c 58f37244 08a4fdd0
sp267 b 8eed9a1b 287eccc2 6d33bbe9 94898938 052fac00 6c4b9ab5 d40aebf3 0a24ffc0 1826f0cb 6710c675 1a782366 7f1c67fc 1d1f97e3 afa2fbe6 9c5fce6c d96f084c 61d531db dfa31402 bae73c11 f1ed41e4 e0b7df5d 05bfa56c 58f37244 08a4fdd0
sp268 a 0dd3d6f3 0f328085 0be93692 69848c42 052fbbfe 8a97f7ca 8d64d884 2c2e3f06 b47f3b59 dd3c0332 37e588ff d761c02e 1d1fa7dd afc879e7 4c97cbe5 946b8048 61c101d1 7026b3fa aa370419 31efd1ed dee741d3 66111d90 110d7cfc 9e921d2e
sp268 b 0dd3d6f3 0f328085 0be93692 69848c42 052fac04 8a17f7cb 9c44c881 2c2e3f02 b47f3b59 dd3c8336 37e588ff d761c02e 1d1f97e3 afc0f9e6 9c1fcf6c d96b084c 61c101d9 5fa73402 baf70411 31ef51e5 dee7c1d7 66111d90 110d7cfc 9e921d2e
sp269 a ab02138b ddb57e5b 4bb6d958 c775438d fa9053ff bdbb9000 41bd5144 35cc16bd 65c21cee 8ea749a2 01cafceb cec4e580 1d1fafdd afa87ae7 4c97cbe5 947fc049 61d501d1 7026b3fa aa270419 f1f581e9 f78653da 3d0dd2d9 5c90c43b 5cd57772
sp269 b ab02138b ddb57e5b 4bb6d958 c775438d fa904405 bd3b9001 509d4141 35cc16b9 65c21cee 8ea7c9a6 01cafceb cec4e580 1d1f9fe3 afa0fae6 9c1fcf6c d97f484d 61d501d9 5fa73402 bae70411 f1f501e1 f786d3de 3d0dd2d9 5c90c43b 5cd57772
sp270 a 0458ffc4 11559e4a 8cb5fe57 23c18c82 056fbbfe 829fd70a 2b61384e 40721ccc 9ce217c3 c7646651 16068036 e593abd4 1d1fa7dd adcb78e7 4c97cbe5 947bc049 61d101d1 7026b3fa aa373c19 f16df9ec eca7055b 78067d4f 73011531 49d7f6c9
sp270 b 0458ffc4 11559e4a 8cb5fe57 23c18c82 056fac04 821fd70b 3a41284b 40721cc8 9ce217c3 c764e655 16068036 e593abd4 1d1f97e3 adc3f8e6 9c1fcf6c d97b484d 61d101d9 5fa73402 baf73c11 f16d79e4 eca7855f 78067d4f 73011531 49d7f6c9
sp271 a 5d0e507b 7852809b 4905189c cc34ca49 fa905bff 5dbf91c0 47b1970c 978af51d a5cad42c bd350110 8bcd3541 045e1ee1 1d1fafdd adc979e7 4cd7cae5 943bc249 61c523d1 f02293fa 2a270c19 f1f1e9e8 973a7452 d7197395 56a0752f fd7edcf2
sp271 b 5d0e507b 7852809b 4905189c cc34ca49 fa904c05 5d3f91c1 56918709 978af519 a5cad42c bd358114 8bcd3541 045e1ee1 1d1f9fe3 adc1f9e6 9c5fce6c d93b4a4d 61c523d9 dfa31402 3ae70c11 f1f169e0 973af456 d7197395 56a0752f fd7edcf2
sp272 a eb442bd2 502b0502 3a6db028 73176afd fa9053fb f9e81974 63b291b4 7bddd1b7 0747b8f8 33044058 18bc6455 9db3111d 1d1fa7dd afc97be7 4cd7cae5 943bc249 61d503d3 f02293fa 2a273c19 7175f9e8 954a6458 38c1275d 3a9faa85 98982018
sp272 b eb442bd2 502b0502 3a6db028 73176afd fa904401 f9681975 729281b1 7bddd1b3 0747b8f8 3304c05c 18bc6455 9db3111d 1d1f97e3 afc1fbe6 9c5fce6c d93b4a4d 61d503db dfa31402 3ae73c11 717579e0 954ae45c 38c1275d 3a9faa85 98982018
sp273 a 9cf7d1bc 06907f82 37682aba cac39872 062f93fe 4fd9c3fa 4f671b34 6f32e89c 3fa2eb9b a80f06ab ed2722f6 20556e3c 1d1fafdd afca7ae7 4cd7cae5 946f8048 61d101d1 7026b3fa 2a27241d b1ebb9ed dfb35053 a8dd8e60 cebb5b50 f4f4fadc
sp273 b 9cf7d1bc 06907f82 37682aba cac39872 062f8404 4f59c3fb 5e470b31 6f32e898 3fa2eb9b a80f86af ed2722f6 20556e3c 1d1f9fe3 afc2fae6 9c5fce6c d96f084c 61d101d9 5fa73402 3ae72415 b1eb39e5 dfb3d057 a8dd8e60 cebb5b50 f4f4fadc
sp274 a 7a4ad96b 1d4a5f4a 97fcf66d 148b0cb8 056fbbfe 88941730 8527787e 0423be3e de78dc93 dc2504a3 473e5fbd 61737b5e 1d1fafdd afaa79e7 4c97cbe5 942b8248 61c123d1 f02293fa aa3f0c18 31ff81e8 7ea751db a85fdea6 9992d2bd 46d40891
sp274 b 7a4ad96b 1d4a5f4a 97fcf66d 148b0cb8 056fac04 88141731 9407687b 0423be3a de78dc93 dc2584a7 473e5fbd 61737b5e 1d1f9fe3 afa2f9e6 9c1fcf6c d92b0a4c 61c123d9 dfa31402 baff0c10 31ff01e0 7ea7d1df a85fdea6 9992d2bd 46d40891
sp275 a 64df9679 e9861985 dd4aa2b8 c79cb874 066f93fe 2dd843f8 ed225ab4 617e89dc 756ba3d5 95371253 de2450b1 88e17553 1d1fafdd afeb7ae7 4cd7cae5 942bc249 61c513d1 7026b3fa aa2f0418 b1f3c9e8 816b6b53 84fae09b b143a9ca f16516d1
sp275 b 64df9679 e9861985 dd4aa2b8 c79cb874 066f8404 2d5843f9 fc024ab1 617e89d8 756ba3d5 95379257 de2450b1 88e17553 1d1f9fe3 afe3fae6 9c5fce6c d92b4a4d 61c513d9 5fa73402 baef0410 b1f349e0 816beb57 84fae09b b143a9ca f16516d1
sp276 a 839a1f50 0cf14c8a 953b4b95 c6d75140 056fb3fe c69bc2c8 c7283b8e 6225ef94 162384a1 5e3b5522 0d034414 1cd227a4 1d1fa7dd ada97be7 4c97cbe5 947f8048 61d511d1 f02293fa aa3f0c18 31e3e9ed eaa70953 b6307ed4 573e01ad e8625340
sp276 b 839a1f50 0cf14c8a 953b4b95 c6d75140 056fa404 c61bc2c9 d6082b8b 6225ef90 162384a1 5e3bd526 0d034414 1cd227a4 1d1f97e3 ada1fbe6 9c1fcf6c d97f084c 61d511d9 dfa31402 baff0c10 31e369e5 eaa78957 b6307ed4 573e01ad e8625340
sp277 a 519a5f3a 1afefd4d 5ee44374 95bcd9bc 066f93fe 4bdd8230 6b2f1b7c c733ea14 5567aa0d 070c50d1 7c383b00 67c610ca 1d1fafdd afcb7be7 4c97cbe5 943bc249 61d523d1 7026b3fa aa37041d b1ebd1ec 896b3c53 6efddf25 336ed807 9338101e
sp277 b 519a5f3a 1afefd4d 5ee44374 95bcd9bc 066f8404 4b5d8231 7a0f0b79 c733ea10 5567aa0d 070cd0d5 7c383b00 67c610ca 1d1f9fe3 afc3fbe6 9c1fcf6c d93b4a4d 61d523d9 5fa73402 baf70415 b1eb51e4 896bbc57 6efddf25 336ed807 9338101e
sp278 a d02b3fd4 f506d991 3a91c3b9 6dbab96c 056fbbfa c8c28ae4 cf2e3ba6 ca36ef66 387e8305 9dd92c10 16ca7f31 d9e01f58 1d1fafdd afa97ae7 4c97cbe5 946f8048 61c121d3 f02293fa 2a372419 f175f1e9 e0a34859 afb168fa cf402994 c20f8c0c
sp278 b d02b3fd4 f506d991 3a91c3b9 6dbab96c 056fac00 c8428ae5 de0e2ba3 ca36ef62 387e8305 9dd9ac14 16ca7f31 d9e01f58 1d1f9fe3 afa1fae6 9c1fcf6c d96f084c 61c121db dfa31402 3af72411 f17571e1 e0a3c85d afb168fa cf402994 c20f8c0c
sp279 a 94399bcd 4a93c9c5 c51cafe9 c2883538 052fb3fe c8d8a6b0 ad2e7ffe 4c670f46 9e2647a1 f71043d2 bd93d786 c0b3e5ae 1d1fa7dd adeb7ae7 4c97cbe5 947f8048 61d111d1 7026b3fa aa3f2c18 f1f9a9e9 eae30a53 31b5ab6c f13bed81 3e42d40e
sp279 b 94399bcd 4a93c9c5 c51cafe9 c2883538 052fa404 c858a6b1 bc0e6ffb 4c670f42 9e2647a1 f710c3d6 bd93d786 c0b3e5ae 1d1f97e3 ade3fae6 9c1fcf6c d97f084c 61d111d9 5fa73402 baff2c10 f1f929e1 eae38a57 31b5ab6c f13bed81 3e42d40e
sp280 a 68b3cd5c 6f237a06 3f71502a 7d43e2fb fad053ff ddba9172 e1f6d1b4 7fcad79f ad46b5d6 1f627613 062354e9 ed185f59 1d1fafdd ad887ae7 4cd7cae5 947f8048 61c501d1 f02293fa aa3f041c f1ed81ed f4f65252 972a7368 3c2f748b 9a431514
sp280 b 68b3cd5c 6f237a06 3f71502a 7d43e2fb fad04405 dd3a9173 f0d6c1b1 7fcad79b ad46b5d6 1f62f617 062354e9 ed185f59 1d1f9fe3 ad80fae6 9c5fce6c d97f084c 61c501d9 dfa31402 baff0414 f1ed01e5 f4f6d256 972a7368 3c2f748b 9a431514
sp281 a 65fda9da 2ac45386 9dff9f88 78988d44 062f9bfe 819af6c8 ad2c5f8c 07625f06 d1607a2d 98ca3f0b 4507c38b cde1ebb9 1d1fafdd af8b7ae7 4c97cbe5 947bc049 61d101d1 7026b3fa 2a3f3c18 31ebd9ec e9e71b5b 774b5b91 713dedf2 c535744e
sp281 b 65fda9da 2ac45386 9dff9f88 78988d44 062f8c04 811af6c9 bc0c4f89 07625f02 d1607a2d 98cabf0f 4507c38b cde1ebb9 1d1f9fe3 af83fae6 9c1fcf6c d97b484d 61d101d9 5fa73402 3aff3c10 31eb59e4 e9e79b5f 774b5b91 713dedf2 c535744e
sp282 a a3a223ce 35832cfe fdbd4c3a b976def7 f9d07bfb d2a0ed7e a5f6d3bc 3ccc071d 649c0068 acc32f20 8f8d96e7 83c58116 1d1fafdd adeb7be7 4cd7cae5 947b8048 61c121d3 f02293fa aa2f3419 b17ff9e8 f3f659d8 a7910560 7823a27e 99900d52
sp282 b a3a223ce 35832cfe fdbd4c3a b976def7 f9d06c01 d220ed7f b4d6c3b9 3ccc0719 649c0068 acc3af24 8f8d96e7 83c58116 1d1f9fe3 ade3fbe6 9c5fce6c d97b084c 61c121db dfa31402 baef3411 b17f79e0 f3f6d9dc a7910560 7823a27e 99900d52
sp283 a 076f05b1 fc80e2ba 9ec578e3 362eaa37 fad053ff 91f351ba 45f35774 97c7555f 4f401882 fd930cb3 9ad8b17e 898dae2d 1d1fa7dd afab7be7 4cd7cae5 947f8048 61c501d1 f02293fa 2a3f0c1d f1fde9e9 f2f65952 e0ceb220 5832f6cc 088affb2
sp283 b 076f05b1 fc80e2ba 9ec578e3 362eaa37 fad04405 917351bb 54d34771 97c7555b 4f401882 fd938cb7 9ad8b17e 898dae2d 1d1f97e3 afa3fbe6 9c5fce6c d97f084c 61c501d9 dfa31402 3aff0c15 f1fd69e1 f2f6d956 e0ceb220 5832f6cc 088affb2
sp284 a 8ee210d5 542093db bdc8a9ff 797a7b2b fa9053ff 73b6a0a2 4dfe51e4 fbd5c1bf 8743c0a6 f82a0528 96c657e0 cfcf075a 1d1fafdd adea78e7 4c97cbe5 947f8048 61d101d1 f02293fa 2a27041c b177e1e8 f5825452 06cc93b8 504ff35b 6bc269af
sp284 b 8ee210d5 542093db bdc8a9ff 797a7b2b fa904405 7336a0a3 5cde41e1 fbd5c1bb 8743c0a6 f82a852c 96c657e0 cfcf075a 1d1f9fe3 ade2f8e6 9c1fcf6c d97f084c 61d101d9 dfa31402 3ae70414 b17761e0 f582d456 06cc93b8 504ff35b 6bc269af
sp285 a 3ea79e9e 66829f3b 4ba4b167 c20d23b3 fa9053ff 33ff503a e3ff1174 158eb63d 6993b3ba e74060d1 aa87230c 75bb1594 1d1fa7dd afe97be7 4c97cbe5 947f8048 61d101d1 7026b3fa aa271c1d 717df9e9 f3825952 c4890120 ba535c10 0c277dd2
sp285 b 3ea79e9e 66829f3b 4ba4b167 c20d23b3 fa904405 337f503b f2df0171 158eb639 6993b3ba e740e0d5 aa87230c 75bb1594 1d1f97e3 afe1fbe6 9c1fcf6c d97f084c 61d101d9 5fa73402 bae71c15 717d79e1 f382d956 c4890120 ba535c10 0c277dd2
sp286 a af0c958b 48e53b42 e0f2e552 b96c7f87 fa905bfb bdaaec0e 89fcd2c4 dbcc44ff e14c0ad8 5b03561b e6b8e11f 8c0af11e 1d1fa7dd ad8b79e7 4c97cbe5 946f8048 61d171d3 f02293fa 2a270c18 71f981e8 ed930158 b51f878a 14616a75 3ce1188e
sp286 b af0c958b 48e53b42 e0f2e552 b96c7f87 fa904c01 bd2aec0f 98dcc2c1 dbcc44fb e14c0ad8 5b03d61f e6b8e11f 8c0af11e 1d1f97e3 ad83f9e6 9c1fcf6c d96f084c 61d171db dfa31402 3ae70c10 71f901e0 ed93815c b51f878a 14616a75 3ce1188e
sp287 a 258802d9 d14b8739 71f70e63 fac034b6 052fb3fe eed8673a ad6679f6 44392f8c d2e068cb f8f03908 8468b5ce 6c5fe04d 1d1fafdd adc879e7 4c97cbe5 947fc049 61c551d1 f02293fa 2a3f1c1c 31ffa1e8 eed744db 85f49d59 f0ff9348 98024d40
sp287 b 258802d9 d14b8739 71f70e63 fac034b6 052fa404 ee58673b bc4669f3 44392f88 d2e068cb f8f0b90c 8468b5ce 6c5fe04d 1d1f9fe3 adc0f9e6 9c1fcf6c d97f484d 61c551d9 dfa31402 3aff1c14 31ff21e0 eed7c4df 85f49d59 f0ff9348 98024d40
sp288 a 9dcbef64 3719780e 5ee84b36 28d371fe 062f93fe 25d18272 ef6f9b34 ef2befcc 3523ea57 49d92c3a 3ef87c22 50126683 1d1fa7dd adcb78e7 4c97cbe5 947f8048 61d541d1 7026b3fa 2a273c18 71e589ed e9e75c53 d6f52160 2edef24b 2951768a
sp288 b 9dcbef64 3719780e 5ee84b36 28d371fe 062f8404 25518273 fe4f8b31 ef2befc8 3523ea57 49d9ac3e 3ef87c22 50126683 1d1f97e3 adc3f8e6 9c1fcf6c d97f084c 61d541d9 5fa73402 3ae73c10 71e509e5 e9e7dc57 d6f52160 2edef24b 2951768a
sp289 a c903ab37 58298f85 b0db8690 9cb75c40 052fbbfe ccd4c7c8 87209884 e47b0d0e 5e740e69 5eb04d81 fc1f9436 cc93cefc 1d1fa7dd afea78e7 4cd7cae5 947fc049 61d561d1 7026b3fa 2a3f3c19 f1f9f1e8 eca755db 2dc29b8d 970595fb ac469dc3
sp289 b c903ab37 58298f85 b0db8690 9cb75c40 052fac04 cc54c7c9 96008881 e47b0d0a 5e740e69 5eb0cd85 fc1f9436 cc93cefc 1d1f97e3 afe2f8e6 9c5fce6c d97f484d 61d561d9 5fa73402 3aff3c11 f1f971e0 eca7d5df 2dc29b8d 970595fb ac469dc3
sp290 a 93c32d61 f6de7085 d38cfebb 5cd4ac76 066f93fe addbf7fa 0166febe 2b6e586e 75a01295 2d3b1331 14758933 15cbba60 1d1fafdd adc979e7 4c97cbe5 947fc049 61d531d1 7026b3fa aa270c1c b167f1ec eda744db 4ec46b25 9ce6eec4 3a097364
sp290 b 93c32d61 f6de7085 d38cfebb 5cd4ac76 066f8404 ad5bf7fb 1046eebb 2b6e586a 75a01295 2d3b9335 14758933 15cbba60 1d1f9fe3 adc1f9e6 9c1fcf6c d97f484d 61d531d9 5fa73402 bae70c14 b16771e4 eda7c4df 4ec46b25 9ce6eec4 3a097364
sp291 a ef00feb4 8f10e98f 73f935a0 483a476d f9d073ff b8f534e0 2fba15a4 54cf16c7 04423150 bf4d6332 1296ba25 82d6c4c7 1d1fa7dd adc978e7 4cd7cae5 947fc049 61c111d1 f02293fa aa37341d f1f9f9e8 f9f24dda b9b6c13b ee64109b c5831ea9
sp291 b ef00feb4 8f10e98f 73f935a0 483a476d f9d06405 b87534e1 3e9a05a1 54cf16c3 04423150 bf4de336 1296ba25 82d6c4c7 1d1f97e3 adc1f8e6 9c5fce6c d97f484d 61c111d9 dfa31402 baf73415 f1f979e0 f9f2cdde b9b6c13b ee64109b c5831ea9
sp292 a 6767d64f b85c4955 5c8c835b 92e7918a 052fb3fe aa930202 696c7ac6 283aadfc 1427a2a3 3c5e22a3 9f8e2a9e 70f40b3c 1d1fafdd adcb79e7 4c97cbe5 946fc049 61c511d1 7026b3fa 2a371c19 b16389ed e6e742db 4a1b2399 b501a2b9 24111656
sp292 b 6767d64f b85c4955 5c8c835b 92e7918a 052fa404 aa130203 784c6ac3 283aadf8 1427a2a3 3c5ea2a7 9f8e2a9e 70f40b3c 1d1f9fe3 adc3f9e6 9c1fcf6c d96f484d 61c511d9 5fa73402 3af71c11 b16309e5 e6e7c2df 4a1b2399 b501a2b9 24111656
sp293 a a2e35d14 cc070306 d1620c39 2a029ef5 f9907bff 3cf7c578 afb295bc 748b2195 2203457c 0822060b 14d8982b 6302c91b 1d1fa7dd af887be7 4c97cbe5 947bc049 61d101d1 f02293fa 2a3f3c18 717db9e8 f686425a 3bed6be1 eeb7a77e 97a2b1bb
sp293 b a2e35d14 cc070306 d1620c39 2a029ef5 f9906c05 3c77c579 be9285b9 748b2191 2203457c 0822860f 14d8982b 6302c91b 1d1f97e3 af80fbe6 9c1fcf6c d97b484d 61d101d9 dfa31402 3aff3c10 717d39e0 f686c25e 3bed6be1 eeb7a77e 97a2b1bb
sp294 a 771addfa 62b00909 9b7ee235 61c918e4 052fb3fe ecdc6368 6923fa26 64658904 9025a9f3 20a21ec9 974351d7 43586aed 1d1fafdd ada87be7 4cd7cae5 946b8048 61d121d1 7026b3fa aa271c1c b16fa9ec e0b75fd3 0decee76 34fe545d 01363a8d
sp294 b 771addfa 62b00909 9b7ee235 61c918e4 052fa404 ec5c6369 7803ea23 64658900 9025a9f3 20a29ecd 974351d7 43586aed 1d1f9fe3 ada0fbe6 9c5fce6c d96b084c 61d121d9 5fa73402 bae71c14 b16f29e4 e0b7dfd7 0decee76 34fe545d 01363a8d
sp295 a ad4fcf9d 4d37c2d9 b98f3bd8 09b0690c 052fb3fe 0a943280 632c1bc4 047e991e 1269b6f9 3d841810 baf8333e bfdc54ec 1d1fafdd ada87be7 4c97cbe5 947bc049 61d151d1 f02293fa 2a370c18 b1eb99ed ece7525b 7058fd93 3b35e176 4c24fa75
sp295 b ad4fcf9d 4d37c2d9 b98f3bd8 09b0690c 052fa404 0a143281 720c0bc1 047e991a 1269b6f9 3d849814 baf8333e bfdc54ec 1d1f9fe3 ada0fbe6 9c1fcf6c d97b484d 61d151d9 dfa31402 3af70c10 b1eb19e5 ece7d25f 7058fd93 3b35e176 4c24fa75
sp296 a fe3bd0d2 6688f14e 465b5f40 ceffed8c 062f93fe 2fd59600 03281ec4 233e787e 31bd3b77 46c87862 be0cff0b e964c62b 1d1fa7dd afaa79e7 4cd7cae5 947fc049 61d131d1 7026b3fa 2a370419 b1f3e1e9 eba34cdb c8e9bd9f 1af9c7bb 29818371
sp296 b fe3bd0d2 6688f14e 465b5f40 ceffed8c 062f8404 2f559601 12080ec1 233e787a 31bd3b77 46c8f866 be0cff0b e964c62b 1d1f97e3 afa2f9e6 9c5fce6c d97f484d 61d131d9 5fa73402 3af70411 b1f361e1 eba3ccdf c8e9bd9f 1af9c7bb 29818371
sp297 a 75a7b710 a39ac30d c520cb05 1dc419cc 066f9bfe ef998240 e72cbc8e 4d232f24 316147bb da497789 8b6e87f7 2737bf24 1d1fafdd adcb7be7 4c97cbe5 946b8048 61d101d1 f02293fa 2a37341c 717981e9 dfb757d3 8b18af1a b745b8b1 d292cf0d
sp297 b 75a7b710 a39ac30d c520cb05 1dc419cc 066f8c04 ef198241 f60cac8b 4d232f20 316147bb da49f78d 8b6e87f7 2737bf24 1d1f9fe3 adc3fbe6 9c1fcf6c d96b084c 61d101d9 dfa31402 3af73414 717901e1 dfb7d7d7 8b18af1a b745b8b1 d292cf0d
sp298 a da1b4ee0 8c7cccf6 b4253526 6a6b8ff7 fa905bfb 7ba1fc7e 0dfed2bc 1395f6bd 29cdb1e2 320854ea da4e6bf7 68b50cf5 1d1fafdd ade97be7 4c97cbe5 947b8048 61d101d3 7026b3fa aa3f1c19 b17bf9e9 f38659d8 76a653dc 906b9ac2 3ab25c50
sp298 b da1b4ee0 8c7cccf6 b4253526 6a6b8ff7 fa904c01 7b21fc7f 1cdec2b9 1395f6b9 29cdb1e2 3208d4ee da4e6bf7 68b50cf5 1d1f9fe3 ade1fbe6 9c1fcf6c d97b084c 61d101db 5fa73402 baff1c11 b17b79e1 f386d9dc 76a653dc 906b9ac2 3ab25c50
sp299 a 2f63da70 88bc984e e5330f44 148eb588 062f93fe c990a600 ad2dd94c 6365cb96 97fb891d 113a02da 0b1a1790 37ec6f02 1d1fa7dd ade978e7 4cd7cae5 947bc049 61c121d1 7026b3fa 2a37041c b1ff99e8 eb974d5b 28e770dd 70f41d36 fcc9f9d7
sp299 b 2f63da70 88bc984e e5330f44 148eb588 062f8404 c910a601 bc0dc949 6365cb92 97fb891d 113a82de 0b1a1790 37ec6f02 1d1f97e3 ade1f8e6 9c5fce6c d97b484d 61c121d9 5fa73402 3af70414 b1ff19e0 eb97cd5f 28e770dd 70f41d36 fcc9f9d7
sp300 a d225f429 b0aca231 48715346 d986c992 056fb3fa e887da1e 436d1d54 4a705f44 d07a12a7 d37d7158 8526e6f9 c59e843b 1d1fafdd af8878e7 4c97cbe5 947b8048 61c111d3 f02293fa aa3f0c19 7171f9e9 e69714d9 90251afe dafd1fe6 43c9f40b
sp300 b d225f429 b0aca231 48715346 d986c992 056fa400 e807da1f 524d0d51 4a705f40 d07a12a7 d37df15c 8526e6f9 c59e843b 1d1f9fe3 af80f8e6 9c1fcf6c d97b084c 61c111db dfa31402 baff0c11 717179e1 e69794dd 90251afe dafd1fe6 43c9f40b
sp301 a d906347c 6fb4d106 c798be0f 31ec0cc2 062f9bfe 27d4774a 0f64398e 49373cd4 93227b49 0add7809 9d29a796 80c0c2fd 1d1fafdd afc879e7 4c97cbe5 946fc049 61c101d1 f02293fa aa373c19 f16da9ec e3e34adb 48d07e0f 0f0a03ad c122a6c1
sp301 b d906347c 6fb4d106 c798be0f 31ec0cc2 062f8c04 2754774b 1e44298b 49373cd0 93227b49 0addf80d 9d29a796 80c0c2fd 1d1f9fe3 afc0f9e6 9c1fcf6c d96f484d 61c101d9 dfa31402 baf73c11 f16d29e4 e3e3cadf 48d07e0f 0f0a03ad c122a6c1
sp302 a aed1dddd 2ca87aba e22113e2 71b8e936 056fb3fe 8490f2ba e76a9dfc 2427bcc6 f23ff36d 69ef3a18 195530c1 1b597a6b 1d1fa7dd afab79e7 4c97cbe5 942b8248 61c113d1 f02293fa 2a3f3419 316381ec 7ea751db ac7a025a b74fc540 ac5819ef
sp302 b aed1dddd 2ca87aba e22113e2 71b8e936 056fa404 8410f2bb f64a8df9 2427bcc2 f23ff36d 69efba1c 195530c1 1b597a6b 1d1f97e3 afa3f9e6 9c1fcf6c d92b0a4c 61c113d9 dfa31402 3aff3411 316301e4 7ea7d1df ac7a025a b74fc540 ac5819ef
sp303 a 257daa9d 0ab56286 5c13e1be 033b3b73 f9907bff 5ebac0fa c7fe11b4 b4da0155 4edd2a1c 90432169 5aedffc8 36f1a5d1 1d1fa7dd afe879e7 4cd7cae5 943b8248 61d533d1 f02293fa 2a37041d 31f7f1e8 924a6bda dc07821e d664228c 27b2489a
sp303 b 257daa9d 0ab56286 5c13e1be 033b3b73 f9906c05 5e3ac0fb d6de01b1 b4da0151 4edd2a1c 9043a16d 5aedffc8 36f1a5d1 1d1f97e3 afe0f9e6 9c5fce6c d93b0a4c 61d533d9 dfa31402 3af70415 31f771e0 924aebde dc07821e d664228c 27b2489a
sp304 a 288e3dae f5bbad1a 84d66b39 c1fd71ec 056fb3fe e0928260 eb2b3b26 827acffe 72e5a559 52e77cc8 8104480c f2d7565c 1d1fa7dd afea7be7 4cd7cae5 943b8248 61c573d1 7026b3fa aa3f2c18 b16791ed 865b73db d251dfc0 b33b1159 c7e0b75a
sp304 b 288e3dae f5bbad1a 84d66b39 c1fd71ec 056fa404 e0128261 fa0b2b23 827acffa 72e5a559 52e7fccc 8104480c f2d7565c 1d1f97e3 afe2fbe6 9c5fce6c d93b0a4c 61c573d9 5fa73402 baff2c10 b16711e5 865bf3df d251dfc0 b33b1159 c7e0b75a
sp305 a d1d07bf5 fce90905 7274560e decb64c2 066f93fe a795f74a a560d984 c334ff46 9ba0da93 fcd03e02 f06b0b8d 3380139f 1d1fa7dd adeb79e7 4c97cbe5 947f8048 61d531d1 7026b3fa aa3f041d 717981e8 e9a74b53 54e86bd6 f9054c00 5a80bde9
sp305 b d1d07bf5 fce90905 7274560e decb64c2 066f8404 a715f74b b440c981 c334ff42 9ba0da93 fcd0be06 f06b0b8d 3380139f 1d1f97e3 ade3f9e6 9c1fcf6c d97f084c 61d531d9 5fa73402 baff0415 717901e0 e9a7cb57 54e86bd6 f9054c00 5a80bde9
sp306 a 927e28c7 b55dfb05 89de7709 d5ffc5d8 052fb3fe 20deb650 8928f896 84769c8c fc2bd2ed a29d584b a4e170c2 fd0d1fd3 1d1fa7dd afc87be7 4c97cbe5 942b8248 61d113d1 f02293fa 2a2f2419 31ebf9ec 7eb751db 181f7ac4 15815aa6 547973eb
sp306 b 927e28c7 b55dfb05 89de7709 d5ffc5d8 052fa404 205eb651 9808e893 84769c88 fc2bd2ed a29dd84f a4e170c2 fd0d1fd3 1d1f97e3 afc0fbe6 9c1fcf6c d92b0a4c 61d113d9 dfa31402 3aef2411 31eb79e4 7eb7d1df 181f7ac4 15815aa6 547973eb
sp307 a 4bb6fbba d7ee635a 374c197c 4c77eba9 fad053ff 73f3b020 e3bf976c b98cb5b5 4bcc9ce4 2f5e6230 56126423 44c63d1a 1d1fa7dd ad8979e7 4cd7cae5 943bc249 61c503d1 f02293fa aa272419 f1e5e9ec 973a6452 c13555b1 3a928ccf 596d3c01
sp307 b 4bb6fbba d7ee635a 374c197c 4c77eba9 fad04405 7373b021 f29f8769 b98cb5b1 4bcc9ce4 2f5ee234 56126423 44c63d1a 1d1f97e3 ad81f9e6 9c5fce6c d93b4a4d 61c503d9 dfa31402 bae72411 f1e569e4 973ae456 c13555b1 3a928ccf 596d3c01
sp308 a 05b5fcaa eec0224a 59dad956 5c436b83 fad053ff 37fef00a 67fd9144 158e3235 8b077480 dace7b2b f3b9ecc7 755fd567 1d1fafdd ade878e7 4c97cbe5 943b8248 61d523d1 7026b3fa aa272418 31fb91e9 930a7cda 84bf744c 3690c23b c14d87fe
sp308 b 05b5fcaa eec0224a 59dad956 5c436b83 fad04405 377ef00b 76dd8141 158e3231 8b077480 dacefb2f f3b9ecc7 755fd567 1d1f9fe3 ade0f8e6 9c1fcf6c d93b0a4c 61d523d9 5fa73402 bae72410 31fb11e1 930afcde 84bf744c 3690c23b c14d87fe
sp309 a 027583e0 58bf63c3 2fe1ecd9 b00ebe11 f9d07bff 70f14598 03b014d4 bc80a0cf 84838d72 4837008a fd6850cc 1a0f266c 1d1fa7dd af8b7ae7 4cd7cae5 947fc049 61c511d1 7026b3fa 2a373c1c f1edf9ed f7f643da 81fcdf03 1a6e29ae e3957586
sp309 b 027583e0 58bf63c3 2fe1ecd9 b00ebe11 f9d06c05 70714599 129004d1 bc80a0cb 84838d72 4837808e fd6850cc 1a0f266c 1d1f97e3 af83fae6 9c5fce6c d97f484d 61c511d9 5fa73402 3af73c14 f1ed79e5 f7f6c3de 81fcdf03 1a6e29ae e3957586
sp310 a 51e6ccbc 9f17a8ca 30eaa6f4 3c841c3c 066f9bfa 25c6afb4 af2218fc e36c4f9c f7be029d c298596b 395efc4b 9a20e39b 1d1fa7dd afcb7be7 4cd7cae5 943bc249 61c513d3 7026b3fa aa271c18 31ef81ec 895b2c59 94ec72df ef2c0380 f36f29f2
sp310 b 51e6ccbc 9f17a8ca 30eaa6f4 3c841c3c 066f8c00 2546afb5 be0208f9 e36c4f98 f7be029d c298d96f 395efc4b 9a20e39b 1d1f97e3 afc3fbe6 9c5fce6c d93b4a4d 61c513db 5fa73402 bae71c10 31ef01e4 895bac5d 94ec72df ef2c0380 f36f29f2
sp311 a 682febbc cdb769be 9f4d2fca 87e21d02 066f9bfa 47c46e8e a969d844 63256e0e 3bb96f0b a6975e61 ec5bff9c e583816d 1d1fa7dd ade87ae7 4c97cbe5 947b8048 61c121d3 7026b3fa aa3f041d f1fd81e9 e79742d9 b274a550 f5005d3e 3b185f20
sp311 b 682febbc cdb769be 9f4d2fca 87e21d02 066f8c00 47446e8f b849c841 63256e0a 3bb96f0b a697de65 ec5bff9c e583816d 1d1f97e3 ade0fae6 9c1fcf6c d97b084c 61c121db 5fa73402 baff0415 f1fd01e1 e797c2dd b274a550 f5005d3e 3b185f20
sp312 a 6a21f936 c0e1e1ce c17da4c6 88251e0b f9907bff 18b30582 89f55344 12cbc15f 6286e35a 74371741 4e150dec ae1b52bc 1d1fa7dd afeb7ae7 4c97cbe5 942b8248 61d503d1 f02293fa 2a273c1d 31ff89e8 8a5a7ada 22243d50 14ad27fc d1c3fe73
sp312 b 6a21f936 c0e1e1ce c17da4c6 88251e0b f9906c05 18330583 98d54341 12cbc15b 6286e35a 74379745 4e150dec ae1b52bc 1d1f97e3 afe3fae6 9c1fcf6c d92b0a4c 61d503d9 dfa31402 3ae73c15 31ff09e0 8a5afade 22243d50 14ad27fc d1c3fe73
sp313 a c45ea408 d232dfc6 d411c4ff 5b7a7e37 f9907bff 16fc45ba 2df7d57c f6c2c265 04d1eca2 21950858 bf862534 bf950b36 1d1fa7dd afaa78e7 4c97cbe5 947f8048 61d511d1 7026b3fa aa270418 71f1f9e9 f4864452 e3d31ee2 70567003 1fbb734a
sp313 b c45ea408 d232dfc6 d411c4ff 5b7a7e37 f9906c05 167c45bb 3cd7c579 f6c2c261 04d1eca2 2195885c bf862534 bf950b36 1d1f97e3 afa2f8e6 9c1fcf6c d97f084c 61d511d9 5fa73402 bae70410 71f179e1 f486c456 e3d31ee2 70567003 1fbb734a
sp314 a 55f0c118 f4afdc3e d512b94b 5975cb83 f9d073fb b4aed80e 47f816cc 78c912ff 4a5b3fba 8a074708 b46bb8d6 c8cbf63d 1d1fa7dd afa97ae7 4cd7cae5 947f8048 61c121d3 f02293fa aa3f1418 f1fdb1e9 f3f25a58 c3c51bd0 d62e3f6d 91dcd76c
sp314 b 55f0c118 f4afdc3e d512b94b 5975cb83 f9d06401 b42ed80f 56d806c9 78c912fb 4a5b3fba 8a07c70c b46bb8d6 c8cbf63d 1d1f97e3 afa1fae6 9c5fce6c d97f084c 61c121db dfa31402 baff1410 f1fd31e1 f3f2da5c c3c51bd0 d62e3f6d 91dcd76c
sp315 a c29c8ade ad2f27c7 2f9ad0df 507daa17 f9d073ff 9ab7719a edf1d15c b48db27d ecc1df4e 8867202a 28d81641 7e1735a9 1d1fa7dd adc978e7 4cd7cae5 943b8248 61d523d1 f02293fa 2a37141d f17d89e9 940a64da a221d2bc b07082e4 e78c2fb1
sp315 b c29c8ade ad2f27c7 2f9ad0df 507daa17 f9d06405 9a37719b fcd1c159 b48db279 ecc1df4e 8867a02e 28d81641 7e1735a9 1d1f97e3 adc1f8e6 9c5fce6c d93b0a4c 61d523d9 dfa31402 3af71415 f17d09e1 940ae4de a221d2bc b07082e4 e78c2fb1
sp316 a 9c60eb26 665a34c9 231f07d7 33c17d02 052fbbfe 4c94c68a 236c3fce 2c302f34 3ae7405d 9f437092 f3bcc8a1 4c66bb49 1d1fa7dd af8b7be7 4c97cbe5 946fc049 61d111d1 f02293fa aa3f3c19 f1ed81ec e4f340db 2c656a91 fb09ed6d e2a96b61
sp316 b 9c60eb26 665a34c9 231f07d7 33c17d02 052fac04 4c14c68b 324c2fcb 2c302f30 3ae7405d 9f43f096 f3bcc8a1 4c66bb49 1d1f97e3 af83fbe6 9c1fcf6c d96f484d 61d111d9 dfa31402 baff3c11 f1ed01e4 e4f3c0df 2c656a91 fb09ed6d e2a96b61
sp317 a ba52e1ee 36a8254f 98114463 5169feaf f9d07bff b0f60522 03f3926c 5298e20f 224bcb0e 41d828fa a02461b2 b3c63563 1d1fafdd ade87be7 4cd7cae5 943b8248 61d533d1 f02293fa aa371c18 b1fbd9e9 940a63da 8bcc3bf6 1a6eb9cf 7c534d7f
sp317 b ba52e1ee 36a8254f 98114463 5169feaf f9d06c05 b0760523 12d38269 5298e20b 224bcb0e 41d8a8fe a02461b2 b3c63563 1d1f9fe3 ade0fbe6 9c5fce6c d93b0a4c 61d533d9 dfa31402 baf71c10 b1fb59e1 940ae3de 8bcc3bf6 1a6eb9cf 7c534d7f
sp318 a 1dca0b03 e8a0d40f 7734d935 2233c3f9 f9d07bff 98bdb070 e1bf513c b8d597ff 284594fe bbf2793a 301b1c10 71de7d43 1d1fafdd adc978e7 4cd7cae5 947fc049 61c121d1 7026b3fa aa372c1c 7169f1ec f9f24dda 59da666d bc62cd46 64c48657
sp318 b 1dca0b03 e8a0d40f 7734d935 2233c3f9 f9d06c05 983db071 f09f4139 b8d597fb 284594fe bbf2f93e 301b1c10 71de7d43 1d1f9fe3 adc1f8e6 9c5fce6c d97f484d 61c121d9 5fa73402 baf72c14 716971e4 f9f2cdde 59da666d bc62cd46 64c48657
sp319 a d340e63e e77ca932 67fc7e42 dbc04c92 052fbbfa eecd7f1e 2b611e54 642cbf44 1ce7d451 a89b0989 75db2b1e f3550187 1d1fafdd ade979e7 4cd7cae5 947f8048 61d531d3 f02293fa 2a3f0c19 717d99e9 eaa71b59 856ec302 72c51fe6 ac2513cb
sp319 b d340e63e e77ca932 67fc7e42 dbc04c92 052fac00 ee4d7f1f 3a410e51 642cbf40 1ce7d451 a89b898d 75db2b1e f3550187 1d1f9fe3 ade1f9e6 9c5fce6c d97f084c 61d531db dfa31402 3aff0c11 717d19e1 eaa79b5d 856ec302 72c51fe6 ac2513cb
sp320 a b0db6f41 ba52391a 0ad69e1d feb1e4cc 056fb3fe a2d53740 af243f86 04213fbe fa7d344f 23a85d5b a07a808b 9679fbf1 1d1fa7dd adcb79e7 4c97cbe5 946b8048 61c111d1 7026b3fa aa2f1c18 f1e199ed e0a759d3 4fd8dddc ef461df9 8e7c74d4
sp320 b b0db6f41 ba52391a 0ad69e1d feb1e4cc 056fa404 a2553741 be042f83 04213fba fa7d344f 23a8dd5f a07a808b 9679fbf1 1d1f97e3 adc3f9e6 9c1fcf6c d96b084c 61c111d9 5fa73402 baef1c10 f1e119e5 e0a7d9d7 4fd8dddc ef461df9 8e7c74d4
sp321 a c9b17051 dc0b3681 8dfafebd 0bd16c74 062f93fa 838d7ffc ad22febe e5253fde d3fc3b21 aed66a22 8808c6fc ce229807 1d1fafdd af8879e7 4c97cbe5 947f8048 61c531d3 f02293fa aa2f2418 f16de9ec e7d74359 f70f8424 7133567b 2cf8c556
sp321 b c9b17051 dc0b3681 8dfafebd 0bd16c74 062f8400 830d7ffd bc02eebb e5253fda d3fc3b21 aed6ea26 8808c6fc ce229807 1d1f9fe3 af80f9e6 9c1fcf6c d97f084c 61c531db dfa31402 baef2410 f16d69e4 e7d7c35d f70f8424 7133567b 2cf8c556
sp322 a 91aeff33 eb48610a 43911711 acf2cdc4 056fbbfe aadaf648 a92c7e8e 807c1fb6 b2b8146d 951a0271 b00ea21b a75fe2e3 1d1fafdd afeb79e7 4c97cbe5 943b8248 61d573d1 7026b3fa aa3f1c1c b16bb9ed 866b63db 1008abd8 f579bcf5 d95b90dc
sp322 b 91aeff33 eb48610a 43911711 acf2cdc4 056fac04 aa5af649 b80c6e8b 807c1fb2 b2b8146d 951a8275 b00ea21b a75fe2e3 1d1f9fe3 afe3f9e6 9c1fcf6c d93b0a4c 61d573d9 5fa73402 baff1c14 b16b39e5 866be3df 1008abd8 f579bcf5 d95b90dc
sp323 a 9cd2c362 f0d93539 88098f67 91ef7db2 052fbbfe 2096463a a76a38f6 ee3aed86 3eefa397 6b875ab9 03bd55f3 09806cb1 1d1fa7dd afeb7be7 4cd7cae5 946fc049 61d521d1 7026b3fa aa373418 31eb81ec e4b750db d9f01b23 f6c3ed88 e074ae6d
sp323 b 9cd2c362 f0d93539 88098f67 91ef7db2 052fac04 2016463b b64a28f3 ee3aed82 3eefa397 6b87dabd 03bd55f3 09806cb1 1d1f97e3 afe3fbe6 9c5fce6c d96f484d 61d521d9 5fa73402 baf73410 31eb01e4 e4b7d0df d9f01b23 f6c3ed88 e074ae6d
sp324 a 8ab78821 6e7ddf7a 29335e84 bd820c50 056fb3fe 0c93f7d8 23241e94 4823b9de 36a2f3f9 df646531 b5011494 6e2e5db5 1d1fafdd ad8a78e7 4c97cbe5 946bc049 61d111d1 7026b3fa aa3f1c1d 7179e1e9 e4b7535b ee6b5c43 7b55feef d5b24330
sp324 b 8ab78821 6e7ddf7a 29335e84 bd820c50 056fa404 0c13f7d9 32040e91 4823b9da 36a2f3f9 df64e535 b5011494 6e2e5db5 1d1f9fe3 ad82f8e6 9c1fcf6c d96b484d 61d111d9 5fa73402 baff1c15 717961e1 e4b7d35f ee6b5c43 7b55feef d5b24330
sp325 a 2826de4a e7a35c82 e664ebaa 9a91397a 052fbbfa 2c810af6 4b6f1a3c 866ecea6 daa98b55 983f142b b4035299 f7b94fc8 1d1fafdd ad8a7be7 4c97cbe5 947f8048 61d521d3 7026b3fa aa3f341c f175f9e9 eae70959 c8165568 52f74b45 133b6649
sp325 b 2826de4a e7a35c82 e664ebaa 9a91397a 052fac00 2c010af7 5a4f0a39 866ecea2 daa98b55 983f942f b4035299 f7b94fc8 1d1f9fe3 ad82fbe6 9c1fcf6c d97f084c 61d521db 5fa73402 baff3414 f17579e1 eae7895d c8165568 52f74b45 133b6649
sp326 a 1758a6e8 e48616bf af1a31d8 69010b15 f99073fb d4e8d89c e9bcd7dc 9cca96c7 c082f44a fd6c2433 8ba13e17 758173d7 1d1fa7dd afea7be7 4c97cbe5 943bc249 61d533d3 f02293fa 2a3f3418 b1ff89e9 964a7458 5d97677b b4ed4b5c b0210867
sp326 b 1758a6e8 e48616bf af1a31d8 69010b15 f9906401 d468d89d f89cc7d9 9cca96c3 c082f44a fd6ca437 8ba13e17 758173d7 1d1f97e3 afe2fbe6 9c1fcf6c d93b4a4d 61d533db dfa31402 3aff3410 b1ff09e1 964af45c 5d97677b b4ed4b5c b0210867
sp327 a 76c75b87 8d3ed946 c2d5876e 36fe15a6 062f93fe c99d662a 876b196c 2b7bcd2e f3abcb39 53fa7f5a 1e893334 d4ec10f5 1d1fafdd afa879e7 4cd7cae5 946f8048 61c501d1 f02293fa aa27141c f1edf9ed dfa75153 a9279fb0 96b33cd3 faaa6643
sp327 b 76c75b87 8d3ed946 c2d5876e 36fe15a6 062f8404 c91d662b 964b0969 2b7bcd2a f3abcb39 53faff5e 1e893334 d4ec10f5 1d1f9fe3 afa0f9e6 9c5fce6c d96f084c 61c501d9 dfa31402 bae71414 f1ed79e5 dfa7d157 a9279fb0 96b33cd3 faaa6643
sp328 a 0eff7c1d ae82e0cb ef8b98ef b6606a3b fa905bff 5dba31b2 4df7577c b193b55d 4d4ff25a 1e895980 68986844 86020c3f 1d1fa7dd ad8879e7 4c97cbe5 947f8048 61d101d1 f02293fa aa3f2c18 b167f9ec f5825352 1d2b01a8 d06f15bf 1888adfa
sp328 b 0eff7c1d ae82e0cb ef8b98ef b6606a3b fa904c05 5d3a31b3 5cd74779 b193b559 4d4ff25a 1e89d984 68986844 86020c3f 1d1f97e3 ad80f9e6 9c1fcf6c d97f084c 61d101d9 dfa31402 baff2c10 b16779e4 f582d356 1d2b01a8 d06f15bf 1888adfa
sp329 a d97e6540 30e0748a e0ba31a5 1726cb6d f9d073fb 90e1b8e4 63be11a4 dc8f30d7 860257fa 3cda3d00 f2bec1ad 16419915 1d1fa7dd afab7be7 4c97cbe5 943bc249 61c523d3 f02293fa 2a2f341d b16fe1ed 963a6458 a9d54971 3adc2199 8b6c85dc
sp329 b d97e6540 30e0748a e0ba31a5 1726cb6d f9d06401 9061b8e5 729e01a1 dc8f30d3 860257fa 3cdabd04 f2bec1ad 16419915 1d1f97e3 afa3fbe6 9c1fcf6c d93b4a4d 61c523db dfa31402 3aef3415 b16f61e5 963ae45c a9d54971 3adc2199 8b6c85dc
sp330 a da08336d a9c392c9 e6f00ed5 f280fc00 052fbbfe ccdce788 a72438ce 267a4da4 90a70381 2d9b1990 d357e6d4 3b02d81c 1d1fa7dd afab7be7 4c97cbe5 946f8048 61d121d1 7026b3fa aa3f2c18 71fdf1e9 e0f34f53 2be96a56 f75624b1 e443edb0
sp330 b da08336d a9c392c9 e6f00ed5 f280fc00 052fac04 cc5ce789 b60428cb 267a4da0 90a70381 2d9b9994 d357e6d4 3b02d81c 1d1f97e3 afa3fbe6 9c1fcf6c d96f084c 61d121d9 5fa73402 baff2c10 71fd71e1 e0f3cf57 2be96a56 f75624b1 e443edb0
sp331 a 42c3a600 37fb5346 785f334f 378c8986 062f9bfe 8bd0f20a 4d6d7b4e 69253e9e 9f3b5f0b a46d2162 207ac975 55e7f1b7 1d1fa7dd ada879e7 4cd7cae5 947fc049 61c501d1 f02293fa aa2f2419 31ff81e8 ed9714db e8f413cf d0a8aaed edaa2e14
sp331 b 42c3a600 37fb5346 785f334f 378c8986 062f8c04 8b50f20b 5c4d6b4b 69253e9a 9f3b5f0b a46da166 207ac975 55e7f1b7 1d1f97e3 ada0f9e6 9c5fce6c d97f484d 61c501d9 dfa31402 baef2411 31ff01e0 ed9794df e8f413cf d0a8aaed edaa2e14
sp332 a 7443dad7 caeac905 8d910622 20aefcee 062f9bfa c9818f66 8f6219a4 697e8e84 b93eef6d 3ec37900 9e990219 5a7d30a1 1d1fa7dd af8879e7 4cd7cae5 946f8048 61c501d3 7026b3fa 2a270419 f1fd81e8 dfa75159 31279574 8ebc3cda 2b5b3f69
sp332 b 7443dad7 caeac905 8d910622 20aefcee 062f8c00 c9018f67 9e4209a1 697e8e80 b93eef6d 3ec3f904 9e990219 5a7d30a1 1d1f97e3 af80f9e6 9c5fce6c d96f084c 61c501db 5fa73402 3ae70411 f1fd01e0 dfa7d15d 31279574 8ebc3cda 2b5b3f69
sp333 a 89df5e81 6ecacc45 2c71a366 ec9c19aa 062f9bfa 4d8f8a26 696edaec 6b664df4 b1614a9f c98d1c38 92039628 f32f8a0b 1d1fa7dd afe87ae7 4cd7cae5 947f8048 61d501d3 7026b3fa 2a373c18 31f7e1e9 e7a71259 a4b9d7b4 b4afb391 6539ee5c
sp333 b 89df5e81 6ecacc45 2c71a366 ec9c19aa 062f8c00 4d0f8a27 784ecae9 6b664df0 b1614a9f c98d9c3c 92039628 f32f8a0b 1d1f97e3 afe0fae6 9c5fce6c d97f084c 61d501db 5fa73402 3af73c10 31f761e1 e7a7925d a4b9d7b4 b4afb391 6539ee5c
sp334 a 35217550 50c72882 8396f699 9ab3ec50 062f93fe 81d077d8 2b243e96 eb71d9fe b962f40d 5f9859b1 f5960713 e1f67fa1 1d1fafdd afab7be7 4c97cbe5 947f8048 61d531d1 f02293fa 2a3f3c1c 31efa1ec e7e74153 f8e9c948 73422ea9 f0aa2357
sp334 b 35217550 50c72882 8396f699 9ab3ec50 062f8404 815077d9 3a042e93 eb71d9fa b962f40d 5f98d9b5 f5960713 e1f67fa1 1d1f9fe3 afa3fbe6 9c1fcf6c d97f084c 61d531d9 dfa31402 3aff3c14 31ef21e4 e7e7c157 f8e9c948 73422ea9 f0aa2357
sp335 a 0dbdaa06 14ea7fb5 2d949fe1 b3fead30 052fb3fe 60d2f6b8 272f3e76 cc33b88e 7a71d11f 0eab4f80 23d06db1 b5771050 1d1fa7dd af8a78e7 4c97cbe5 947f8048 61d511d1 7026b3fa 2a372c19 f1edb9ed e8e70c53 9a1c6de4 f72f2f0a c07a5b0b
sp335 b 0dbdaa06 14ea7fb5 2d949fe1 b3fead30 052fa404 6052f6b9 360f2e73 cc33b88a 7a71d11f 0eabcf84 23d06db1 b5771050 1d1f97e3 af82f8e6 9c1fcf6c d97f084c 61d511d9 5fa73402 3af72c11 f1ed39e5 e8e78c57 9a1c6de4 f72f2f0a c07a5b0b
sp336 a ec63f363 dadf5e07 3fb89109 f66a63d9 fa9053ff f1b6b050 63bd111c f5cd97ed 4d45bd6e 53145559 cb1a7921 18e12120 1d1fa7dd adc97ae7 4c97cbe5 943bc249 61d503d1 7026b3fa 2a370c18 f16df9ed 974a6552 cb36b281 bae10a62 9a94a7a6
sp336 b ec63f363 dadf5e07 3fb89109 f66a63d9 fa904405 f136b051 729d0119 f5cd97e9 4d45bd6e 5314d55d cb1a7921 18e12120 1d1f97e3 adc1fae6 9c1fcf6c d93b4a4d 61d503d9 5fa73402 3af70c10 f16d79e5 974ae556 cb36b281 bae10a62 9a94a7a6
sp337 a 39bac3e5 0119621a 3df47a3a f685a8ee 056fb3fe 82db1362 ed625da4 826a5b0e b03e7891 df165333 0622dc8e b3baad9f 1d1fa7dd adaa7ae7 4c97cbe5 947b8048 61c111d1 7026b3fa 2a2f3c1d b163f1ed e8971ad3 6ff400ba 30f81fe0 e5458fc9
sp337 b 39bac3e5 0119621a 3df47a3a f685a8ee 056fa404 825b1363 fc424da1 826a5b0a b03e7891 df16d337 0622dc8e b3baad9f 1d1f97e3 ada2fae6 9c1fcf6c d97b084c 61c111d9 5fa73402 3aef3c15 b16371e5 e8979ad7 6ff400ba 30f81fe0 e5458fc9
sp338 a 99312e84 8a5f234d ba432a45 00cf188c 066f93fe c5dea300 eb21ba4e 4932293c b7a24dd9 9f786310 bd16845c 3f2ad95c 1d1fa7dd adca7be7 4c97cbe5 943b8248 61d503d1 f02293fa 2a2f3418 717981e9 876b23db 77099ed2 b378b8ed cb236ff5
sp338 b 99312e84 8a5f234d ba432a45 00cf188c 066f8404 c55ea301 fa01aa4b 49322938 b7a24dd9 9f78e314 bd16845c 3f2ad95c 1d1f97e3 adc2fbe6 9c1fcf6c d93b0a4c 61d503d9 dfa31402 3aef3410 717901e1 876ba3df 77099ed2 b378b8ed cb236ff5
sp339 a 036283bd eacafb47 1f5e0d7e 680497b3 f9d073ff 5cb5c43a 07fe12f4 f883a6e5 0c40ef0c 99000099 1cd065f3 7e737429 1d1fafdd ade879e7 4cd7cae5 947f8048 61c521d1 7026b3fa 2a3f2418 b17b81e9 f5f65352 97c36124 1628438b 5394240e
sp339 b 036283bd eacafb47 1f5e0d7e 680497b3 f9d06405 5c35c43b 16de02f1 f883a6e1 0c40ef0c 9900809d 1cd065f3 7e737429 1d1f9fe3 ade0f9e6 9c5fce6c d97f084c 61c521d9 5fa73402 3aff2410 b17b01e1 f5f6d356 97c36124 1628438b 5394240e
sp340 a c66ce8c9 d0b00a3a f81c8266 43f2d0b6 056fb3fe c0de433a 67679a7c ea3f6f4e 7c2a6ad1 bda21933 6d7b929e e6c49bfc 1d1fa7dd afab7ae7 4c97cbe5 946f8048 61d521d1 7026b3fa 2a271c1d 71f1f9e9 e0b75853 39e81f24 b6f6b308 3a0aa501
sp340 b c66ce8c9 d0b00a3a f81c8266 43f2d0b6 056fa404 c05e433b 76478a79 ea3f6f4a 7c2a6ad1 bda29937 6d7b929e e6c49bfc 1d1f97e3 afa3fae6 9c1fcf6c d96f084c 61d521d9 5fa73402 3ae71c15 71f179e1 e0b7d857 39e81f24 b6f6b308 3a0aa501
sp341 a 0bb5d42a 44ee4dca 99be26ef 82cc9c3a 056fbbfe cad027b2 0562f8f6 e4212d44 f8600d91 9c5421a1 dbd3a55c 789ddedf 1d1fa7dd ad8b78e7 4c97cbe5 947fc049 61d521d1 f02293fa aa370419 31e7a1ed eea715db b2021cab 18fb0c45 66869eef
sp341 b 0bb5d42a 44ee4dca 99be26ef 82cc9c3a 056fac04 ca5027b3 1442e8f3 e4212d40 f8600d91 9c54a1a5 dbd3a55c 789ddedf 1d1f97e3 ad83f8e6 9c1fcf6c d97f484d 61d521d9 dfa31402 baf70411 31e721e5 eea795df b2021cab 18fb0c45 66869eef
sp342 a d4bac49a b6c07afe 048d1838 bd310af1 f9d073fb d4e0597c c5b651b4 1288741d 02401e22 0fbf4c33 4648995f 1e2ef30d 1d1fafdd adab7be7 4c97cbe5 943bc249 61d543d3 7026b3fa aa2f2c18 f161e1ed 984a7c58 e00b085d d8dfe9c8 7fbcf538
sp342 b d4bac49a b6c07afe 048d1838 bd310af1 f9d06401 d460597d d49641b1 12887419 02401e22 0fbfcc37 4648995f 1e2ef30d 1d1f9fe3 ada3fbe6 9c1fcf6c d93b4a4d 61d543db 5fa73402 baef2c10 f16161e5 984afc5c e00b085d d8dfe9c8 7fbcf538
sp343 a 51e88208 5c781af7 eca9d400 815d0ed1 fa9053ff 5bfdf558 87b41394 5b9a72af ed583084 c374667b 80768063 d055c54a 1d1fa7dd afc879e7 4c97cbe5 943bc249 61d513d1 7026b3fa 2a373418 317be9e9 954a7452 5ef86e3b 96ea1fea 74c98d81
sp343 b 51e88208 5c781af7 eca9d400 815d0ed1 fa904405 5b7df559 96940391 5b9a72ab ed583084 c374e67f 80768063 d055c54a 1d1f97e3 afc0f9e6 9c1fcf6c d93b4a4d 61d513d9 5fa73402 3af73410 317b69e1 954af456 5ef86e3b 96ea1fea 74c98d81
sp344 a 705ef8d4 aa33b6c9 e2aad6ec d0c80c38 052fb3fe 66d697b0 ad23df74 486f987c 38a19189 f5971b52 314a0fb6 f4692e77 1d1fafdd afeb79e7 4c97cbe5 947fc049 61d151d1 f02293fa 2a273418 3177d9e9 ece344db 11d39a63 f12a45c6 8f9ffdb4
sp344 b 705ef8d4 aa33b6c9 e2aad6ec d0c80c38 052fa404 665697b1 bc03cf71 486f9878 38a19189 f5979b56 314a0fb6 f4692e77 1d1f9fe3 afe3f9e6 9c1fcf6c d97f484d 61d151d9 dfa31402 3ae73410 317759e1 ece3c4df 11d39a63 f12a45c6 8f9ffdb4
sp345 a d006ab16 08ed048a 8418bb94 05fe0940 056fb3fe 4c9e72c8 cb2c1d8c 4a775804 b67f3af1 35011552 3906c465 d273a424 1d1fa7dd afa87be7 4c97cbe5 946bc049 61d101d1 7026b3fa aa372419 7169f9ec e2b7485b ac3ade91 d34617f3 bfd2cbb2
sp345 b d006ab16 08ed048a 8418bb94 05fe0940 056fa404 4c1e72c9 da0c0d89 4a775800 b67f3af1 35019556 3906c465 d273a424 1d1f97e3 afa0fbe6 9c1fcf6c d96b484d 61d101d9 5fa73402 baf72411 716979e4 e2b7c85f ac3ade91 d34617f3 bfd2cbb2
sp346 a b938a3b5 28d29fba 11cfd8e3 1e7a0a37 fad053ff bfb471ba edf650f4 db92f047 a5c69eb0 e4d33e43 69de7006 5f3612fc 1d1fafdd ada878e7 4cd7cae5 947f8048 61c501d1 f02293fa 2a2f1c1d f16df9ec f4f65452 b5109520 b0200d4c cc37230b
sp346 b b938a3b5 28d29fba 11cfd8e3 1e7a0a37 fad04405 bf3471bb fcd640f1 db92f043 a5c69eb0 e4d3be47 69de7006 5f3612fc 1d1f9fe3 ada0f8e6 9c5fce6c d97f084c 61c501d9 dfa31402 3aef1c15 f16d79e4 f4f6d456 b5109520 b0200d4c cc37230b
sp347 a 2c1bd39f dd61bff2 16ebd701 bdcdedd0 052fb3fa 88cdde5c ab283896 2e785b1e b8fd15b3 49c53b9b c2598506 8a86a4e5 1d1fafdd afeb78e7 4c97cbe5 947b8048 61c151d3 7026b3fa 2a3f3419 f16d81ec e6d754d9 6fa077b8 73423ce8 61bd1f95
sp347 b 2c1bd39f dd61bff2 16ebd701 bdcdedd0 052fa400 884dde5d ba082893 2e785b1a b8fd15b3 49c5bb9f c2598506 8a86a4e5 1d1f9fe3 afe3f8e6 9c1fcf6c d97b084c 61c151db 5fa73402 3aff3411 f16d01e4 e6d7d4dd 6fa077b8 73423ce8 61bd1f95
sp348 a 62443dcd 8e6c7149 a05fd673 9481ecba 066f9bfe 85921732 8167f876 81619e2c 33f9f28b 2b646698 fbbb5c56 9d341b77 1d1fafdd afaa7be7 4c97cbe5 946fc049 61c111d1 7026b3fa aa3f3c1c 3173f1e8 e3a358db 6b3cfbe9 1d12450c 585a4ee4
sp348 b 62443dcd 8e6c7149 a05fd673 9481ecba 066f8c04 85121733 9047e873 81619e28 33f9f28b 2b64e69c fbbb5c56 9d341b77 1d1f9fe3 afa2fbe6 9c1fcf6c d96f484d 61c111d9 5fa73402 baff3c14 317371e0 e3a3d8df 6b3cfbe9 1d12450c 585a4ee4
sp349 a 6e62e505 cb38a34d c690cf62 43fb9dae 066f9bfe 0b92a622 836f1964 ab7dcd2c 9b738cff bf234212 14913a59 781e7568 1d1fafdd afcb7be7 4c97cbe5 946f8048 61d501d1 f02293fa aa37241d b163a9ec dfb74753 6f1f9bb8 9aff4bdc 2e46688b
sp349 b 6e62e505 cb38a34d c690cf62 43fb9dae 066f8c04 0b12a623 924f0961 ab7dcd28 9b738cff bf23c216 14913a59 781e7568 1d1f9fe3 afc3fbe6 9c1fcf6c d96f084c 61d501d9 dfa31402 baf72415 b16329e4 dfb7c757 6f1f9bb8 9aff4bdc 2e46688b
sp350 a c7878094 196b20ce f6dbaaf4 90fe9838 062f93fe cd9223b0 4126daf4 a5282a94 fdf909f7 dca30d80 3dc187c2 0230fc21 1d1fa7dd afc97be7 4cd7cae5 947fc049 61c101d1 7026b3fa aa273418 f1f991e8 eb931adb 2315efa9 5ceb6b8a f185435b
sp350 b c7878094 196b20ce f6dbaaf4 90fe9838 062f8404 cd1223b1 5006caf1 a5282a90 fdf909f7 dca38d84 3dc187c2 0230fc21 1d1f97e3 afc1fbe6 9c5fce6c d97f484d 61c101d9 5fa73402 bae73410 f1f911e0 eb939adf 2315efa9 5ceb6b8a f185435b
sp351 a f16cba36 bebc7b7b c1b295a6 86248777 fa9053ff d3b0d4fa 2dff5234 718db78f 2fc5d0d8 64b71c43 c9056dee b5e6079c 1d1fa7dd afa878e7 4c97cbe5 946b8048 61d171d1 7026b3fa aa373c1d f16db9ed e9971ad2 2540be9e 70730b50 284c1e08
sp351 b f16cba36 bebc7b7b c1b295a6 86248777 fa904405 d330d4fb 3cdf4231 718db78b 2fc5d0d8 64b79c47 c9056dee b5e6079c 1d1f97e3 afa0f8e6 9c1fcf6c d96b084c 61d171d9 5fa73402 baf73c15 f16d39e5 e9979ad6 2540be9e 70730b50 284c1e08
sp352 a 6575f4cb d09e4fc5 2863baff 7ac24832 066f93fe a9d3f3ba c7673d76 677b5d8e dbb512b5 c4d32c61 894e85da 8ae5b272 1d1fafdd afea78e7 4c97cbe5 943bc249 61d553d1 7026b3fa 2a373c19 71f989e8 896b6d53 11206fe1 5736fe09 a58a0243
sp352 b 6575f4cb d09e4fc5 2863baff 7ac24832 066f8404 a953f3bb d6472d73 677b5d8a dbb512b5 c4d3ac65 894e85da 8ae5b272 1d1f9fe3 afe2f8e6 9c1fcf6c d93b4a4d 61d553d9 5fa73402 3af73c11 71f909e0 896bed57 11206fe1 5736fe09 a58a0243
sp353 a 7352bede 69425d36 50d8cb65 e98199b4 052fbbfa 6685ea3c c12f7b76 c62deeb4 1666e9e7 60d32acb 72347532 02786242 1d1fa7dd adca7be7 4c97cbe5 946f8048 61d121d3 f02293fa 2a372419 7165a1ec e2f34f59 0bdd46a2 dd3ee9c4 46083cc1
sp353 b 7352bede 69425d36 50d8cb65 e98199b4 052fac00 6605ea3d d00f6b73 c62deeb0 1666e9e7 60d3aacf 72347532 02786242 1d1f97e3 adc2fbe6 9c1fcf6c d96f084c 61d121db dfa31402 3af72411 716521e4 e2f3cf5d 0bdd46a2 dd3ee9c4 46083cc1
sp354 a 90b1c20b d05731ba c492afe3 bcb8bd36 056fb3fe 029346ba 856efffe c2336bae feed6009 fe776180 1153adc4 d284f164 1d1fa7dd adcb78e7 4cd7cae5 942bc249 61d533d1 7026b3fa aa2f2418 717d89e9 847b7353 ba601d5d 18f70480 5039d584
sp354 b 90b1c20b d05731ba c492afe3 bcb8bd36 056fa404 021346bb 944eeffb c2336baa feed6009 fe77e184 1153adc4 d284f164 1d1f97e3 adc3f8e6 9c5fce6c d92b4a4d 61d533d9 5fa73402 baef2410 717d09e1 847bf357 ba601d5d 18f70480 5039d584
sp355 a 734a9526 331ec509 88a9ab03 fbb419ca 066f93fe a59b8242 41687a86 8375482c 91790585 78653728 2dd1d5c1 ca0fc68a 1d1fafdd ade87be7 4cd7cae5 943bc249 61d553d1 f02293fa aa3f1c19 71e9d9ec 8b6b6c53 9756be59 dd0191b5 0b8466e5
sp355 b 734a9526 331ec509 88a9ab03 fbb419ca 066f8404 a51b8243 50486a83 83754828 91790585 7865b72c 2dd1d5c1 ca0fc68a 1d1f9fe3 ade0fbe6 9c5fce6c d93b4a4d 61d553d9 dfa31402 baff1c11 71e959e4 8b6bec57 9756be59 dd0191b5 0b8466e5
sp356 a 89c0a732 3b543d09 77dc6b33 fab191fa 066f93fe 89960272 496afab6 8f3aee24 9deec86b 12fe6ec9 cc1757d5 d0383d0c 1d1fa7dd adc87be7 4c97cbe5 947bc049 61d121d1 f02293fa aa373c18 317ff9e8 eba74a5b f0ff2f6b d4f74284 bf0545ec
sp356 b 89c0a732 3b543d09 77dc6b33 fab191fa 066f8404 89160273 584aeab3 8f3aee20 9deec86b 12feeecd cc1757d5 d0383d0c 1d1f97e3 adc0fbe6 9c1fcf6c d97b484d 61d121d9 dfa31402 baf73c10 317f79e0 eba7ca5f f0ff2f6b d4f74284 bf0545ec
sp357 a 93798e16 ab6c1549 4180ff42 3aec8d8a 066f93fe a7903602 8b6c9ecc 477fda86 9d69f29b ac4d3222 3aff241f b9ab4b97 1d1fa7dd afeb7be7 4cd7cae5 943b8248 61d513d1 f02293fa 2a2f2c19 31e791ed 856b33db 933f0b92 12edbd70 915fce13
sp357 b 93798e16 ab6c1549 4180ff42 3aec8d8a 066f8404 a7103603 9a4c8ec9 477fda82 9d69f29b ac4db226 3aff241f b9ab4b97 1d1f97e3 afe3fbe6 9c5fce6c d93b0a4c 61d513d9 dfa31402 3aef2c11 31e711e5 856bb3df 933f0b92 12edbd70 915fce13
sp358 a 4a36d620 16e0515a 6830ca5d ef8f188c 056fb3fe a49c0300 cb243bc6 262ce87e 7c6dccf9 c99b0f99 2ddf7d64 d743787c 1d1fa7dd ade879e7 4c97cbe5 947f8048 61d561d1 7026b3fa 2a3f0419 f1edf1ec eaa75b53 57fd9f56 5341f9ba 6a8d1275
sp358 b 4a36d620 16e0515a 6830ca5d ef8f188c 056fa404 a41c0301 da042bc3 262ce87a 7c6dccf9 c99b8f9d 2ddf7d64 d743787c 1d1f97e3 ade0f9e6 9c1fcf6c d97f084c 61d561d9 5fa73402 3aff0411 f1ed71e4 eaa7db57 57fd9f56 5341f9ba 6a8d1275
sp359 a 8836cc7f 020a6a5a aa64e47c ce575ea9 fad053ff b7f9a520 83b3926c f7db4015 2f4966f6 79fd2c99 7463df69 e0b0a9e1 1d1fafdd afab7ae7 4cd7cae5 947fc049 61c501d1 f02293fa aa372c18 31f389e8 f6f653da bac85fb9 9a6a9bce 56cc943d
sp359 b 8836cc7f 020a6a5a aa64e47c ce575ea9 fad04405 b779a521 92938269 f7db4011 2f4966f6 79fdac9d 7463df69 e0b0a9e1 1d1f9fe3 afa3fae6 9c5fce6c d97f484d 61c501d9 dfa31402 baf72c10 31f309e0 f6f6d3de bac85fb9 9a6a9bce 56cc943d
sp360 a b029974a 763d1f85 aa2faabf ddbbf876 066f93fe 679f43fa e562fabe 057509fe db636b93 f5d32a50 bda19507 eb5ba9bd 1d1fa7dd af8878e7 4c97cbe5 947bc049 61d121d1 7026b3fa aa373c19 31ebf1ed e9a74d5b 913a10e3 b8ff32c1 c5530198
sp360 b b029974a 763d1f85 aa2faabf ddbbf876 066f8404 671f43fb f442eabb 057509fa db636b93 f5d3aa54 bda19507 eb5ba9bd 1d1f97e3 af80f8e6 9c1fcf6c d97b484d 61d121d9 5fa73402 baf73c11 31eb71e5 e9a7cd5f 913a10e3 b8ff32c1 c5530198
sp361 a 13778792 74431317 52eb4019 c8013ac9 fa905bff 75fe0140 e1b5d60c 1d852477 cd422358 68c53b08 ecec92ad 5d55ccf6 1d1fa7dd af8b7be7 4c97cbe5 947fc049 61d501d1 f02293fa aa3f1c19 31f7c9e9 f78652da 04e44099 3cb0472f 313ebe97
sp361 b 13778792 74431317 52eb4019 c8013ac9 fa904c05 757e0141 f095c609 1d852473 cd422358 68c5bb0c ecec92ad 5d55ccf6 1d1f97e3 af83fbe6 9c1fcf6c d97f484d 61d501d9 dfa31402 baff1c11 31f749e1 f786d2de 04e44099 3cb0472f 313ebe97
sp362 a af01d675 92e1218e 1d386984 0f7c9b49 f9907bff 9ab700c0 c7bd960c d889a33d 8c4283be 56e36f40 21347ed8 8cc03d18 1d1fafdd afeb78e7 4c97cbe5 947fc049 61d521d1 7026b3fa 2a270418 316ff9ec f8864dda 5fbf639d 56905f72 ff824234
sp362 b af01d675 92e1218e 1d386984 0f7c9b49 f9906c05 9a3700c1 d69d8609 d889a339 8c4283be 56e3ef44 21347ed8 8cc03d18 1d1f9fe3 afe3f8e6 9c1fcf6c d97f484d 61d521d9 5fa73402 3ae70410 316f79e4 f886cdde 5fbf639d 56905f72 ff824234
sp363 a 568d1eac ba56efca 94fdf0c5 1e20ca0d f9d073fb b0e6b984 ebb51144 d49e3457 880377d2 9923079b 2d0f9145 2589fdfd 1d1fafdd ade878e7 4cd7cae5 943bc249 61d543d3 7026b3fa 2a37041c 71f581e8 980a7d58 03c7ab55 32a9033c 4bc75514
sp363 b 568d1eac ba56efca 94fdf0c5 1e20ca0d f9d06401 b066b985 fa950141 d49e3453 880377d2 9923879f 2d0f9145 2589fdfd 1d1f9fe3 ade0f8e6 9c5fce6c d93b4a4d 61d543db 5fa73402 3af70414 71f501e0 980afd5c 03c7ab55 32a9033c 4bc75514
sp364 a 24431f70 b0c2e1c6 c2a97fe8 b5862d38 056fbbfe 62dc16b0 8d2b5e7c 622bfefe 7efebc37 406b20cb 7a33590a a5f0192a 1d1fa7dd adab7ae7 4c97cbe5 946bc049 61c101d1 7026b3fa 2a2f141d f1e5b1ed e4a7415b 8fe9fda9 913ec707 46218c33
sp364 b 24431f70 b0c2e1c6 c2a97fe8 b5862d38 056fac04 625c16b1 9c0b4e79 622bfefa 7efebc37 406ba0cf 7a33590a a5f0192a 1d1f97e3 ada3fae6 9c1fcf6c d96b484d 61c101d9 5fa73402 3aef1415 f1e531e5 e4a7c15f 8fe9fda9 913ec707 46218c33
sp365 a fa168235 10f76f8a 17bffca0 67750669 f9907bff 74fab5e0 03b292ac fe8376fd a4883b1c f2d568ea cb3f8bc2 a87fe6da 1d1fafdd adc878e7 4c97cbe5 947fc049 61d121d1 f02293fa 2a2f3c18 b16f81ed fa824dda 059a7efd 9aa3aa8e 5587e658
sp365 b fa168235 10f76f8a 17bffca0 67750669 f9906c05 747ab5e1 129282a9 fe8376f9 a4883b1c f2d5e8ee cb3f8bc2 a87fe6da 1d1f9fe3 adc0f8e6 9c1fcf6c d97f484d 61d121d9 dfa31402 3aef3c10 b16f01e5 fa82cdde 059a7efd 9aa3aa8e 5587e658
sp366 a 188981f5 141d354e ca791974 56658bb9 f9907bff d4b19030 c9ba50fc 7495b057 4655dbb0 fb805a19 86625a97 7f5b2fd5 1d1fafdd ade97be7 4c97cbe5 947fc049 61d531d1 f02293fa 2a3f2418 716189ed fa865ada a7cab0ef d4abc43e 976bf29f
sp366 b 188981f5 141d354e ca791974 56658bb9 f9906c05 d4319031 d89a40f9 7495b053 4655dbb0 fb80da1d 86625a97 7f5b2fd5 1d1f9fe3 ade1fbe6 9c1fcf6c d97f484d 61d531d9 dfa31402 3aff2410 716109e5 fa86dade a7cab0ef d4abc43e 976bf29f
sp367 a fcd5de8d c7146945 08dcbe7b b0bb04b6 066f93fe 8997d73a 0967f87e cb70dc16 75f3b1bf 4e407323 3b7700c8 fa0f2ae9 1d1fa7dd af8879e7 4c97cbe5 947bc049 61d131d1 f02293fa aa27241d 716d99ed e9a75c5b ef455c65 14ea1cc1 d640b7a1
sp367 b fcd5de8d c7146945 08dcbe7b b0bb04b6 066f8404 8917d73b 1847e87b cb70dc12 75f3b1bf 4e40f327 3b7700c8 fa0f2ae9 1d1f97e3 af80f9e6 9c1fcf6c d97b484d 61d131d9 dfa31402 bae72415 716d19e5 e9a7dc5f ef455c65 14ea1cc1 d640b7a1
sp368 a a6f6f415 11105987 029e648c f77fde45 f9d073ff b0bac5c8 25b0548c bacb4207 ec462c8e 34030563 2adec123 db98df1a 1d1fafdd ada87ae7 4cd7cae5 943bc249 61d543d1 7026b3fa aa3f2418 b173b1e9 984a7d52 0c739c11 78b5dff2 8f98352b
sp368 b a6f6f415 11105987 029e648c f77fde45 f9d06405 b03ac5c9 34904489 bacb4203 ec462c8e 34038567 2adec123 db98df1a 1d1f9fe3 ada0fae6 9c5fce6c d93b4a4d 61d543d9 5fa73402 baff2410 b17331e1 984afd56 0c739c11 78b5dff2 8f98352b
sp369 a c679f4f5 29e8f24b 56d0f046 f830e28f f99073fb 9ea4b906 ebf1904c 16d95737 20887e3a cc632481 1e83b707 185dce5f 1d1fafdd af8878e7 4c97cbe5 947f8048 61d521d3 f02293fa 2a272418 b16fe9ed f4865458 d3f08a58 b25cd4ed 4126debe
sp369 b c679f4f5 29e8f24b 56d0f046 f830e28f f9906401 9e24b907 fad18049 16d95733 20887e3a cc63a485 1e83b707 185dce5f 1d1f9fe3 af80f8e6 9c1fcf6c d97f084c 61d521db dfa31402 3ae72410 b16f69e5 f486d45c d3f08a58 b25cd4ed 4126debe
sp370 a 6d41dd79 e8225a46 4597874a 27f55586 062f93fe 6d92e60a 0f6818cc e17e0ade dfa36b63 7355617b 10d995ff 316bf875 1d1fa7dd adc97ae7 4c97cbe5 946f8048 61d501d1 f02293fa aa3f1418 b17f81e8 e1f75853 0f215cd0 0f0e3c6f e8b9cf8e
sp370 b 6d41dd79 e8225a46 4597874a 27f55586 062f8404 6d12e60b 1e4808c9 e17e0ada dfa36b63 7355e17f 10d995ff 316bf875 1d1f97e3 adc1fae6 9c1fcf6c d96f084c 61d501d9 dfa31402 baff1410 b17f01e0 e1f7d857 0f215cd0 0f0e3c6f e8b9cf8e
sp371 a d4f7349e f42c9449 fef4ef6c 88c3fdbc 052fbbfe 269a2630 a32e18fc 8a336b4c b42129af 10830d68 7a89fb88 3cdceb8b 1d1fa7dd ad8a7ae7 4cd7cae5 947bc049 61d101d1 7026b3fa 2a3f0418 b17fa1e8 eca7035b d44d2c29 7afbfd82 c1fc5f21
sp371 b d4f7349e f42c9449 fef4ef6c 88c3fdbc 052fac04 261a2631 b20e08f9 8a336b48 b42129af 10838d6c 7a89fb88 3cdceb8b 1d1f97e3 ad82fae6 9c5fce6c d97b484d 61d101d9 5fa73402 3aff0410 b17f21e0 eca7835f d44d2c29 7afbfd82 c1fc5f21
sp372 a bbfe6a69 ce33d4d7 883da5d9 94241f09 fa905bff d9fe0480 87b9924c 3193214d 0388282a fad06e0b a569acc6 8d90f78f 1d1fafdd afc97be7 4cd7cae5 943bc249 61d513d1 f02293fa 2a3f341d b17f91e9 954a6452 60f33d13 16b091f3 2e788764
sp372 b bbfe6a69 ce33d4d7 883da5d9 94241f09 fa904c05 d97e0481 96998249 31932149 0388282a fad0ee0f a569acc6 8d90f78f 1d1f9fe3 afc1fbe6 9c5fce6c d93b4a4d 61d513d9 dfa31402 3aff3415 b17f11e1 954ae456 60f33d13 16b091f3 2e788764
sp373 a c71551db cb29428d d99d6aa3 06a9986e 066f93fe 899403e2 6766baae 6b38e9cc 7da4cdd9 7849358a 52990dfc 5eb344f6 1d1fafdd adeb7be7 4cd7cae5 943bc249 61d563d1 f02293fa 2a3f3418 31eff9ed 8b6b7c53 b3433c7b 3703798c 61a2e568
sp373 b c71551db cb29428d d99d6aa3 06a9986e 066f8404 891403e3 7646aaab 6b38e9c8 7da4cdd9 7849b58e 52990dfc 5eb344f6 1d1f9fe3 ade3fbe6 9c5fce6c d93b4a4d 61d563d9 dfa31402 3aff3410 31ef79e5 8b6bfc57 b3433c7b 3703798c 61a2e568
sp374 a 8a3eee10 b5932b8e bc5539b4 547f2379 f99073ff 14ffb0f0 61be51bc 1e8576e7 e24234ae 52de7c6b e963e3f1 2006f432 1d1fa7dd ade978e7 4c97cbe5 947bc049 61d101d1 f02293fa aa3f1c1c 71f181e8 f8864d5a 65848369 bcabcb82 7b9c25a5
sp374 b 8a3eee10 b5932b8e bc5539b4 547f2379 f9906405 147fb0f1 709e41b9 1e8576e3 e24234ae 52defc6f e963e3f1 2006f432 1d1f97e3 ade1f8e6 9c1fcf6c d97b484d 61d101d9 dfa31402 baff1c14 71f101e0 f886cd5e 65848369 bcabcb82 7b9c25a5
sp375 a 9d28bc05 9b0fc7be 75e2c6cb debc5c02 066f9bfa 4bcccf8e 0361394e 873a6f6c 11e5073b 9178367b 6fa19264 4b18f926 1d1fa7dd afc97ae7 4c97cbe5 943bc249 61d523d3 7026b3fa 2a2f3c1d b1efc9ec 896b3d59 66d091c7 1b34f233 e1310f67
sp375 b 9d28bc05 9b0fc7be 75e2c6cb debc5c02 066f8c00 4b4ccf8f 1241294b 873a6f68 11e5073b 9178b67f 6fa19264 4b18f926 1d1f97e3 afc1fae6 9c1fcf6c d93b4a4d 61d523db 5fa73402 3aef3c15 b1ef49e4 896bbd5d 66d091c7 1b34f233 e1310f67
sp376 a ae95d7f3 aed31891 a57d639d 168ff948 056fbbfa e4cb8ac4 ed28fb8e 282aaede 9ebce2e9 baec7f2b 9dc565bc 87b67fe7 1d1fafdd adca79e7 4c97cbe5 947b8048 61c161d3 7026b3fa 2a270c1d f1f181e9 e8975bd9 15abcb12 312941f4 7c1abd31
sp376 b ae95d7f3 aed31891 a57d639d 168ff948 056fac00 e44b8ac5 fc08eb8b 282aaeda 9ebce2e9 baecff2f 9dc565bc 87b67fe7 1d1f9fe3 adc2f9e6 9c1fcf6c d97b084c 61c161db 5fa73402 3ae70c15 f1f101e1 e897dbdd 15abcb12 312941f4 7c1abd31
sp377 a d318e9b5 9e63e806 b25e123a 14f9c8f6 062f93fe c5db537a e7629dbc a53abb36 db23969d 5de62c13 cf3a5dba 62b760d1 1d1fa7dd ad8b7ae7 4cd7cae5 947f8048 61c131d1 f02293fa aa27141d 7161f9ec e9934a53 acfea126 36aba884 fc6f58bb
sp377 b d318e9b5 9e63e806 b25e123a 14f9c8f6 062f8404 c55b537b f6428db9 a53abb32 db23969d 5de6ac17 cf3a5dba 62b760d1 1d1f97e3 ad83fae6 9c5fce6c d97f084c 61c131d9 dfa31402 bae71415 716179e4 e993ca57 acfea126 36aba884 fc6f58bb
sp378 a 282111e9 610db27e 16b056ba 3f8d6c76 066f93fa 058f5ffe 8162d8bc c93c3f0c 1765729b 30c33a68 8dda85a5 e2c0d714 1d1fafdd afeb7be7 4c97cbe5 947b8048 61d131d3 f02293fa 2a3f3c19 71ed89ed e5a751d9 6aaad0a2 1d07947e 4781a3c9
sp378 b 282111e9 610db27e 16b056ba 3f8d6c76 066f8400 050f5fff 9042c8b9 c93c3f08 1765729b 30c3ba6c 8dda85a5 e2c0d714 1d1f9fe3 afe3fbe6 9c1fcf6c d97b084c 61d131db dfa31402 3aff3c11 71ed09e5 e5a7d1dd 6aaad0a2 1d07947e 4781a3c9
sp379 a 4da209b1 531b24bb c8f699e1 5075cb35 fa9053ff 55b870b8 45bfd67c f7967187 e51b5d9a 38f52d08 0cdf872f eb8fa06f 1d1fafdd afca79e7 4c97cbe5 947fc049 61d101d1 7026b3fa aa3f3419 31f3c9e8 f78254da a2eee2a1 58aa6f03 d73150e9
sp379 b 4da209b1 531b24bb c8f699e1 5075cb35 fa904405 553870b9 549fc679 f7967183 e51b5d9a 38f5ad0c 0cdf872f eb8fa06f 1d1f9fe3 afc2f9e6 9c1fcf6c d97f484d 61d101d9 5fa73402 baff3411 31f349e0 f782d4de a2eee2a1 58aa6f03 d73150e9
sp380 a 5d1bfa37 1ee9d919 5b165b1f 92e021ce 052fb3fe 429c1242 6769bd0e 202abf5c 16e4fb23 633c467a 3ef06075 56557065 1d1fafdd adeb79e7 4cd7cae5 947fc049 61d511d1 f02293fa 2a273c19 b1f791e9 eea704db 39ee3159 36a4712d 3488ce76
sp380 b 5d1bfa37 1ee9d919 5b165b1f 92e021ce 052fa404 421c1243 7649ad0b 202abf58 16e4fb23 633cc67e 3ef06075 56557065 1d1f9fe3 ade3f9e6 9c5fce6c d97f484d 61d511d9 dfa31402 3ae73c11 b1f711e1 eea784df 39ee3159 36a4712d 3488ce76
sp381 a ba38e926 3126e785 3cda368e a6e94c42 066f93fe 45d0d7ca 83609e84 4b38fc7c b1b3f693 44b219c1 bfd31157 05700376 1d1fa7dd afe878e7 4cd7cae5 943b8248 61d513d1 7026b3fa aa3f0c18 71e989ed 856b34db 75058cca 1b05adfb bf94e258
sp381 b ba38e926 3126e785 3cda368e a6e94c42 066f8404 4550d7cb 92408e81 4b38fc78 b1b3f693 44b299c5 bfd31157 05700376 1d1f97e3 afe0f8e6 9c5fce6c d93b0a4c 61d513d9 5fa73402 baff0c10 71e909e5 856bb4df 75058cca 1b05adfb bf94e258
sp382 a 74e7e9ad 35ef3d7f b68119bc f82e4b71 f99073fb 90edd8fc e3bf1034 d2d2d24f 68c7bda2 abe06c1a fce0269c 9340798c 1d1fafdd ade87ae7 4cd7cae5 943bc249 61d543d3 f02293fa aa3f0c1c f1ed81ec 984a7d58 a3bc69dd 3aaafc08 47829681
sp382 b 74e7e9ad 35ef3d7f b68119bc f82e4b71 f9906401 906dd8fd f29f0031 d2d2d24b 68c7bda2 abe0ec1e fce0269c 9340798c 1d1f9fe3 ade0fae6 9c5fce6c d93b4a4d 61d543db dfa31402 baff0c14 f1ed01e4 984afd5c a3bc69dd 3aaafc08 47829681
sp383 a bceb68ae 7eef247f 03af048b 8520be43 f99073fb d0adcdce 87f49484 389aa06d 20cbead0 b1682358 69101b3e 1e8934bf 1d1fafdd ad887be7 4c97cbe5 947b8048 61d101d3 f02293fa 2a272c18 31fff1e9 f48641d8 a1f7628c 165dd8b5 9ffd9da5
sp383 b bceb68ae 7eef247f 03af048b 8520be43 f9906401 d02dcdcf 96d48481 389aa069 20cbead0 b168a35c 69101b3e 1e8934bf 1d1f9fe3 ad80fbe6 9c1fcf6c d97b084c 61d101db dfa31402 3ae72c10 31ff71e1 f486c1dc a1f7628c 165dd8b5 9ffd9da5
sp384 a efed7e98 ecb80919 db6aeb3e 4984d1ee 052fb3fe ac94a262 696b5b24 e63f6df6 74700a57 779c59d2 d90bd613 e9c6e908 1d1fa7dd afa979e7 4c97cbe5 947f8048 61d121d1 7026b3fa aa270419 f16989ed e8e31b53 4c23b17c 34e6da5c abd6483e
sp384 b efed7e98 ecb80919 db6aeb3e 4984d1ee 052fa404 ac14a263 784b4b21 e63f6df2 74700a57 779cd9d6 d90bd613 e9c6e908 1d1f97e3 afa1f9e6 9c1fcf6c d97f084c 61d121d9 5fa73402 bae70411 f16909e5 e8e39b57 4c23b17c 34e6da5c abd6483e
sp385 a 9ba51eb5 647c727b b1188087 d22bba57 fa905bff 9bb8e1da c1f5d71c fd87a53d 89158f72 2df03ab0 33ee7dc6 f993556f 1d1fa7dd ade87be7 4c97cbe5 943b8248 61d513d1 7026b3fa 2a370418 f1e9a1ed 934a6bda 211d7fba 5ca86c63 93527236
sp385 b 9ba51eb5 647c727b b1188087 d22bba57 fa904c05 9b38e1db d0d5c719 fd87a539 89158f72 2df0bab4 33ee7dc6 f993556f 1d1f97e3 ade0fbe6 9c1fcf6c d93b0a4c 61d513d9 5fa73402 3af70410 f1e921e5 934aebde 211d7fba 5ca86c63 93527236
sp386 a 0aaa8af4 32c6084b 8ec3446e 136916bb fa905bff 77bb0532 89f7547c d992278d 438c2d22 8b47721b 5b83bf3c 455d8455 1d1fafdd af8b78e7 4c97cbe5 947f8048 61d511d1 7026b3fa aa2f041d f169a9ec f3865c52 83335f6a 145ef108 cc039ba6
sp386 b 0aaa8af4 32c6084b 8ec3446e 136916bb fa904c05 773b0533 98d74479 d9922789 438c2d22 8b47f21f 5b83bf3c 455d8455 1d1f9fe3 af83f8e6 9c1fcf6c d97f084c 61d511d9 5fa73402 baef0415 f16929e4 f386dc56 83335f6a 145ef108 cc039ba6
sp387 a d5fe8901 446db9cd af15a3f7 34b7f93a 066f93fe 2fd8a2b2 c16f7a7e 4537aaee b969e4e3 f08e18c8 9c066404 037e06fd 1d1fafdd adea78e7 4c97cbe5 943bc249 61c553d1 f02293fa aa3f1418 71f1e1e9 8b5b6d53 051762e9 5d3a88bc 45a60b7e
sp387 b d5fe8901 446db9cd af15a3f7 34b7f93a 066f8404 2f58a2b3 d04f6a7b 4537aaea b969e4e3 f08e98cc 9c066404 037e06fd 1d1f9fe3 ade2f8e6 9c1fcf6c d93b4a4d 61c553d9 dfa31402 baff1410 71f161e1 8b5bed57 051762e9 5d3a88bc 45a60b7e
sp388 a 9d122187 2900433a 00ea5f44 698b4d90 056fbbfe 68d7d618 ab2c1ed4 c0751e0e d8ea3319 15f328f2 de45fd54 d8aaeb2e 1d1fafdd afa87be7 4c97cbe5 947bc049 61d151d1 7026b3fa aa2f341c f179f1e9 eaa74a5b 901979fb f32e16ae e12c4ce2
sp388 b 9d122187 2900433a 00ea5f44 698b4d90 056fac04 6857d619 ba0c0ed1 c0751e0a d8ea3319 15f3a8f6 de45fd54 d8aaeb2e 1d1f9fe3 afa0fbe6 9c1fcf6c d97b484d 61d151d9 5fa73402 baef3414 f17971e1 eaa7ca5f 901979fb f32e16ae e12c4ce2
sp389 a 032e6b57 785870c6 533930f1 3e1eea3d f9d073fb d0edb9b4 41b6d0f4 749e328d 6a495e0c 4f5c6132 42a680c3 93cc9f70 1d1fafdd adc979e7 4c97cbe5 943bc249 61d503d3 f02293fa 2a3f3419 716dd9ed 980a3c58 63bb891d 5cf36245 9bdbbc26
sp389 b 032e6b57 785870c6 533930f1 3e1eea3d f9d06401 d06db9b5 5096c0f1 749e3289 6a495e0c 4f5ce136 42a680c3 93cc9f70 1d1f9fe3 adc1f9e6 9c1fcf6c d93b4a4d 61d503db dfa31402 3aff3411 716d59e5 980abc5c 63bb891d 5cf36245 9bdbbc26
sp390 a 969d9804 73360ece 43bb15e6 9c70672b f99073ff 34b814a2 8dfa55e4 1ad4d79f ae4c92a2 d7185373 49b7152d 8d020b46 1d1fafdd ade97be7 4c97cbe5 947f8048 61d111d1 7026b3fa 2a3f341c b16791ed f6824152 c5d83c7a 90701f9f 40b6f596
sp390 b 969d9804 73360ece 43bb15e6 9c70672b f9906405 343814a3 9cda45e1 1ad4d79b ae4c92a2 d718d377 49b7152d 8d020b46 1d1f9fe3 ade1fbe6 9c1fcf6c d97f084c 61d111d9 5fa73402 3aff3414 b16711e5 f682c156 c5d83c7a 90701f9f 40b6f596
sp391 a ae03c4aa 4486dd97 06cab199 30242b49 fa9053ff bdf610c0 6fbc978c b9ce1285 e7437c8c f240706b abcafee9 91a4ab93 1d1fafdd afe87ae7 4c97cbe5 946bc049 61c161d1 f02293fa aa370418 b1ebf9ed ed87015a b29ee315 aeb56dae 14d1d12d
sp391 b ae03c4aa 4486dd97 06cab199 30242b49 fa904405 bd7610c1 7e9c8789 b9ce1281 e7437c8c f240f06f abcafee9 91a4ab93 1d1f9fe3 afe0fae6 9c1fcf6c d96b484d 61c161d9 dfa31402 baf70410 b1eb79e5 ed87815e b29ee315 aeb56dae 14d1d12d
sp392 a 8f30651a 7ca8ca8a d22f07ad 9b947d78 056fb3fe 66d426f0 012af9b6 e4322804 72236087 bea64a82 81bcf850 10f29c5b 1d1fa7dd afe979e7 4cd7cae5 943b8248 61d533d1 7026b3fa 2a2f1c18 3173e9e8 866b33db 53f13c28 1d2b42c9 f02db8c9
sp392 b 8f30651a 7ca8ca8a d22f07ad 9b947d78 056fa404 665426f1 100ae9b3 e4322800 72236087 bea6ca86 81bcf850 10f29c5b 1d1f97e3 afe1f9e6 9c5fce6c d93b0a4c 61d533d9 5fa73402 3aef1c10 317369e0 866bb3df 53f13c28 1d2b42c9 f02db8c9
sp393 a 4164ae92 e537c881 0cab1689 d5ccec58 056fbbfa aec49fd4 8d24789e 42665cfe d8e23fbb 0ce13880 29cef94f 7459a2fd 1d1fa7dd ada87be7 4c97cbe5 946f8048 61d521d3 7026b3fa 2a370c19 71edf9ed e2b74f59 45c4c08a 9149c4e0 ca680715
sp393 b 4164ae92 e537c881 0cab1689 d5ccec58 056fac00 ae449fd5 9c04689b 42665cfa d8e23fbb 0ce1b884 29cef94f 7459a2fd 1d1f97e3 ada0fbe6 9c1fcf6c d96f084c 61d521db 5fa73402 3af70c11 71ed79e5 e2b7cf5d 45c4c08a 9149c4e0 ca680715
sp394 a f6eaca7c ec8eefba 2f1e6ec4 b3b8fc10 056fb3fe 8addc798 0b2498dc 423a6954 1a2c643d 466470c2 e786f99b 642a8702 1d1fafdd afc978e7 4cd7cae5 943bc249 61d573d1 f02293fa 2a370c19 316791ec 8a6b6d53 b0237b87 933d635f 8a44febf
sp394 b f6eaca7c ec8eefba 2f1e6ec4 b3b8fc10 056fa404 8a5dc799 1a0488d9 423a6950 1a2c643d 4664f0c6 e786f99b 642a8702 1d1f9fe3 afc1f8e6 9c5fce6c d93b4a4d 61d573d9 dfa31402 3af70c11 316711e4 8a6bed57 b0237b87 933d635f 8a44febf
sp395 a 99d23002 1867808f 7d05c8a1 8e7aba6d f9d073ff b2b821e0 4db656a4 7e86e4ed 4a04edac f847312a 01fa40b2 a81166a3 1d1fafdd ad8a79e7 4c97cbe5 943bc249 61c503d1 f02293fa aa270c18 716591ed 983a3c52 826fe3f1 d0dbb496 17c6b4e6
sp395 b 99d23002 1867808f 7d05c8a1 8e7aba6d f9d06405 b23821e1 5c9646a1 7e86e4e9 4a04edac f847b12e 01fa40b2 a81166a3 1d1f9fe3 ad82f9e6 9c1fcf6c d93b4a4d 61c503d9 dfa31402 bae70c10 716511e5 983abc56 826fe3f1 d0dbb496 17c6b4e6
sp396 a e6ec6fdb 30d6e835 d6ae4361 27c711b0 052fb3fe 24d4e238 e72e3af6 687e8de6 d03f81f5 b1371279 571a1efa e51e1532 1d1fa7dd ad8878e7 4c97cbe5 947f8048 61d511d1 7026b3fa 2a3f2c19 71edb9ed eae70c53 d81c8264 3738328a a82f64b3
sp396 b e6ec6fdb 30d6e835 d6ae4361 27c711b0 052fa404 2454e239 f60e2af3 687e8de2 d03f81f5 b137927d 571a1efa e51e1532 1d1f97e3 ad80f8e6 9c1fcf6c d97f084c 61d511d9 5fa73402 3aff2c11 71ed39e5 eae78c57 d81c8264 3738328a a82f64b3
sp397 a d7023155 6fe2fd4a 2ea9a562 fa41d7ab f9907bff 9afba422 81fad2ec 9085a4f5 4e5a8608 1fce6933 feda7d9e 3a7f7c5c 1d1fafdd afe87be7 4c97cbe5 947b8048 61d121d1 f02293fa aa370419 3173a1e8 f28659d2 dd798dbc 9c677250 b9b2673a
sp397 b d7023155 6fe2fd4a 2ea9a562 fa41d7ab f9906c05 9a7ba423 90dac2e9 9085a4f1 4e5a8608 1fcee937 feda7d9e 3a7f7c5c 1d1f9fe3 afe0fbe6 9c1fcf6c d97b084c 61d121d9 dfa31402 baf70411 317321e0 f286d9d6 dd798dbc 9c677250 b9b2673a
sp398 a d9b15d58 4c8aaf4a da627a40 8ee50888 062f93fe 8fdc1300 cd21dc4c eb277836 11695271 1c071501 e9999905 7380a7df 1d1fafdd adcb79e7 4cd7cae5 947fc049 61d531d1 7026b3fa aa370418 7171d1e9 eda744db 6cc2501f d0fc0a32 22e67378
sp398 b d9b15d58 4c8aaf4a da627a40 8ee50888 062f8404 8f5c1301 dc01cc49 eb277832 11695271 1c079505 e9999905 7380a7df 1d1f9fe3 adc3f9e6 9c5fce6c d97f484d 61d531d9 5fa73402 baf70410 717151e1 eda7c4df 6cc2501f d0fc0a32 22e67378
sp399 a 8dab5ed5 5519f349 98b6e751 a7c97d84 052fbbfe c094c608 8d29f946 407f0b3c d2b06115 2d523192 ac8ae22a 2f7ec631 1d1fafdd afaa79e7 4cd7cae5 947f8048 61d121d1 7026b3fa aa3f0c1c 316bf9ec e8a30b53 38228dd6 1100453d 990d3997
sp399 b 8dab5ed5 5519f349 98b6e751 a7c97d84 052fac04 c014c609 9c09e943 407f0b38 d2b06115 2d52b196 ac8ae22a 2f7ec631 1d1f9fe3 afa2f9e6 9c5fce6c d97f084c 61d121d9 5fa73402 baff0c14 316b79e4 e8a38b57 38228dd6 1100453d 990d3997
```

## Appendix B. Finite reproduction and audit source

Run the following listings from the candidate directory on a little-endian C11 host. The first-eight full certificate uses up to 64 GiB of RAM and OpenMP; the other checks need less. Temporary paths below are generated outputs, not extra advice. The source rows in Appendix A are the only nonuniform input. The count and bitmap may take minutes. The two independent enumeration implementations must agree before accepting the finite K.

Suggested commands, after saving the listings under their captions: `mkdir -p /tmp/r31_variant`; `python3 r31_extract_points.py`; `python3 make_esets.py`; `cp /tmp/r31_variant/esets_reproduced.bin /tmp/r31_variant/esets.bin`; `cc -O3 -std=c11 r31_vsets.c -o r31_vsets && ./r31_vsets`; `cc -O3 -std=c11 r31_v5.c -o r31_v5 && ./r31_v5`; `cc -O3 -std=c11 r31_v6_dump.c -o r31_v6_dump && ./r31_v6_dump`; `cc -O3 -std=c11 r31_gsets_independent.c -o r31_gsets_independent && ./r31_gsets_independent`; `cc -O3 -std=c11 recombine_all.c -o recombine_all && ./recombine_all 0 400`; `cc -O3 -std=c11 count_keys_sample.c -o count_keys_sample && ./count_keys_sample /tmp/r31_variant/recombined_0_400.bin /tmp/r31_variant/active_0_400.bin 10000 /tmp/r31_variant/first_key_sample_0_400.bin`; `cc -O3 -std=c11 -fopenmp r31_first8_low16_independent_omp.c -o r31_first8_low16_independent_omp && OMP_NUM_THREADS=16 ./r31_first8_low16_independent_omp`; `cc -O3 -std=c11 -fopenmp r31_first8_low16_conservative.c -o r31_first8_low16_conservative && OMP_NUM_THREADS=16 ./r31_first8_low16_conservative`; `cc -O3 -std=c11 -fopenmp r31_first8_low16_fast.c -o r31_first8_low16_fast && OMP_NUM_THREADS=16 ./r31_first8_low16_fast`; `cc -O3 -std=c11 r31_proj_support_verify.c -o r31_proj_support_verify && ./r31_proj_support_verify`; `cc -O3 -std=c11 r31_newkeys_build.c -o r31_newkeys_build && ./r31_newkeys_build /tmp/r31_variant/recombined_0_400.bin /tmp/r31_variant/newkeys_independent.bin`; `python3 audit_active.py /tmp/r31_variant/recombined_0_400.bin`; `python3 audit_active.py /tmp/r31_variant/active_0_400.bin`. For the first-eight synthetic union study, also compile and run `cc -O3 -std=c11 r31_second_sample.c -o r31_second_sample && ./r31_second_sample` after the first-key sample, then run `PYTHONPATH=. python3 h2_first8_uniform_union.py` with the Appendix C Python listings saved alongside it. The optimized all-previous source retains a legacy console label `greedy_numerator`; its pair loop evaluates every earlier tuple, without chosen-subset filtering, and gives exactly the stated sequential bound. The V5/V6 and G/S listings separately verify their full-domain set sizes. Compilation and file names are for reproducibility, not prescriptions for the online 9.8-billion-trial run. The first-key sample uses the fixed 32-bit mixing hash shown in its listing; all retained keys, not only sampled keys, count toward K.


### r31_extract_points.py

```python
import re
import struct

source = open('proof.md', encoding='utf-8').read()
rows = re.findall(r'^sp(\d{3}) ([ab]) ((?:[0-9a-f]{8} ?)+)$', source, re.M)
points = {(int(i), side): [int(word, 16) for word in words.split()]
          for i, side, words in rows}
assert len(points) == 800
with open('/tmp/r31_points.bin', 'wb') as output:
    for i in range(400):
        for side in 'ab':
            record = points[i, side]
            assert len(record) == 24
            output.write(struct.pack('<24I', *record))
print('starting_points=400 paired_rows=800 words_per_row=24')
```


### make_esets.py

```python
"""Generate exact signed E5..E8 pair sets, with modular differences from sp000."""
import struct
M=(1<<32)-1
PAT={
 5:'000111010001111110nu=11111unnnu1',
 6:'101011=11==0n0==u11110==1110011n',
 7:'un0u1100n=01u11111001u1=n110u10n',
 8:'1u01un0u0=1=1=11n=0=u0=001001u0=',
}
raw=open('/tmp/r31_points.bin','rb').read(192)
a=struct.unpack('<24I',raw[:96]);b=struct.unpack('<24I',raw[96:])
with open('/tmp/r31_variant/esets_reproduced.bin','wb') as f:
 for t in range(5,9):
  out=[(0,0)]
  for bit,ch in enumerate(PAT[t][::-1]):
   opts={'=':((0,0),(1,1)),'0':((0,0),),'1':((1,1),),
         'u':((0,1),),'n':((1,0),)}[ch]
   out=[(x|(u<<bit),y|(v<<bit)) for x,y in out for u,v in opts]
  delta=(b[t+7]-a[t+7])&M
  out=sorted((x,y) for x,y in out if ((y-x)&M)==delta)
  f.write(struct.pack('<I',len(out)))
  for x,y in out:f.write(struct.pack('<II',x,y))
  print(f'E{t}: {len(out)} signed pairs; modular delta {delta:08x}')
```


### r31_vsets.c

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


### r31_v5.c

```c
#include <stdint.h>
#include <stdio.h>
static inline uint32_t rot(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return rot(x,7)^rot(x,18)^(x>>3);}
int main(){FILE*f=fopen("/tmp/r31_v5.bin","wb");if(!f)return 1;uint64_t n=0;for(uint64_t i=0;i<(1ULL<<32);i++){uint32_t x=(uint32_t)i;if((uint32_t)(s0(x+0xfffff006)-s0(x))==0xd0018020){fwrite(&x,4,1,f);n++;}}fclose(f);fprintf(stderr,"V5=%llu\n",(unsigned long long)n);return n==(1ULL<<14)?0:2;}
```


### r31_v6_dump.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static inline uint32_t rot(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return rot(x,7)^rot(x,18)^(x>>3);}
int main(void){const uint64_t words=1ULL<<26,mask=words-1;uint64_t*bits=calloc(words,sizeof(uint64_t));if(!bits){perror("calloc");return 1;}const uint32_t d6=0x002087f1,c6=0x00000ffa;uint64_t n=0;time_t t=time(0);FILE*fv=fopen("/tmp/r31_v6.bin","wb");for(uint64_t i=0;i<(1ULL<<32);i++){uint32_t x=(uint32_t)i;if((uint32_t)(s0(x+d6)-s0(x))==c6){bits[x>>6]|=1ULL<<(x&63);fwrite(&x,4,1,fv);n++;}}fclose(fv);fprintf(stderr,"V6=%llu seconds=%lld\n",(unsigned long long)n,(long long)(time(0)-t));if(n!=(1ULL<<23))return 2;free(bits);return 0;}
```


### r31_gsets_independent.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static inline uint32_t rot(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s1(uint32_t x){return rot(x,17)^rot(x,19)^(x>>10);}
static double now(void){struct timespec t;timespec_get(&t,TIME_UTC);return t.tv_sec+t.tv_nsec*1e-9;}
int main(void){
 uint32_t G16[128];size_t n16=0,n18=0;
 uint32_t*G18=malloc(50000000ULL*sizeof(uint32_t));if(!G18)return 1;
 const uint32_t d16=0x00008004,d18=0xffff7ffc,x18=0x2ffe7fe0;
 double t0=now();
 for(uint64_t i=0;i<(1ULL<<32);i++){
  uint32_t x=(uint32_t)i,v=s1(x);
  if((uint32_t)(s1(x+d16)-v)==d18){if(n16==128)return 2;G16[n16++]=x;}
  if((uint32_t)(s1(x+d18)-v)==x18){if(n18==50000000ULL)return 3;G18[n18++]=x;}
 }
 fprintf(stderr,"enumeration_s=%.3f G16=%zu G18=%zu\n",now()-t0,n16,n18);
 uint8_t*B=calloc(1,1ULL<<29);if(!B)return 4;uint64_t size=0;
 for(size_t i=0;i<n16;i++){
  uint32_t shift=s1(G16[i]);
  for(size_t j=0;j<n18;j++){
   uint32_t c=G18[j]-shift;
   uint8_t*byte=&B[c>>3],m=(uint8_t)(1u<<(c&7));
   if(!(*byte&m)){*byte|=m;size++;}
  }
 }
 printf("G16=%zu G18=%zu S=%llu union_s=%.3f total_s=%.3f\n",n16,n18,(unsigned long long)size,now()-t0,now()-t0);
 for(size_t i=0;i<n16;i++)printf("G16[%zu]=%08x\n",i,G16[i]);
 free(B);free(G18);
 return (n16==64&&n18==42467328&&size==584683520)?0:5;
}
```


### recombine_all.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t a,b;} Pair;
typedef struct {uint32_t a[24],b[24];} Point;
static inline uint32_t rot(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return rot(x,2)^rot(x,13)^rot(x,22);}
static inline uint32_t S1(uint32_t x){return rot(x,6)^rot(x,11)^rot(x,25);}
static inline uint32_t s0(uint32_t x){return rot(x,7)^rot(x,18)^(x>>3);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static int signok(uint32_t w,uint32_t wp,const char*s){
 for(int i=0;i<32;i++){char c=s[31-i];int a=(w>>i)&1,b=(wp>>i)&1;
 if(c=='='&&a!=b)return 0;if(c=='0'&&(a||b))return 0;if(c=='1'&&!(a&&b))return 0;
 if(c=='u'&&(a||!b))return 0;if(c=='n'&&(!a||b))return 0;}return 1;
}
static int cmp_point(const void*aa,const void*bb){return memcmp(aa,bb,sizeof(Point));}
static uint32_t K[13]={0,0,0,0,0,0,0,0,0,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74};
int main(int argc,char**argv){
 int first=0,last=400;if(argc>1)first=atoi(argv[1]);if(argc>2)last=atoi(argv[2]);
 Point*base=malloc(400*sizeof(Point));FILE*f=fopen("/tmp/r31_points.bin","rb");if(!f||fread(base,sizeof(Point),400,f)!=400){perror("points");return 1;}fclose(f);
 Pair *V[4];int len[4];f=fopen("/tmp/r31_variant/esets.bin","rb");if(!f){perror("esets");return 1;}
 for(int t=0;t<4;t++){uint32_t n;if(fread(&n,4,1,f)!=1)return 2;len[t]=n;V[t]=malloc(n*sizeof(Pair));if(fread(V[t],sizeof(Pair),n,f)!=n)return 2;}fclose(f);
 if(len[0]!=2||len[1]!=128||len[2]!=4||len[3]!=128){fprintf(stderr,"E-pair cap exceeded or wrong derivative sets\n");return 5;}
 size_t cap=100000,nout=0;Point*out=malloc(cap*sizeof(Point));
 uint64_t counts[7]={0};time_t start=time(0);
 for(int seed=first;seed<last;seed++){
  size_t local=0;
  for(int i5=0;i5<len[0];i5++)for(int i6=0;i6<len[1];i6++)for(int i7=0;i7<len[2];i7++)for(int i8=0;i8<len[3];i8++){
   Point x=base[seed];uint32_t *a=x.a,*b=x.b;
   Pair pp[4]={V[0][i5],V[1][i6],V[2][i7],V[3][i8]};
   for(int j=0;j<4;j++){a[12+j]=pp[j].a;b[12+j]=pp[j].b;}
   for(int lane=0;lane<2;lane++){
    uint32_t *q=lane?b:a;uint32_t A[13],E[13];
    for(int t=5;t<=12;t++){A[t]=q[t-1];E[t]=q[t+7];}
    for(int t=8;t>=5;t--){A[t-4]=E[t]-A[t]+S0(A[t-1])+Maj(A[t-1],A[t-2],A[t-3]);q[t-5]=A[t-4];}
    for(int t=9;t<=12;t++)q[t+11]=E[t]-A[t-4]-E[t-4]-S1(E[t-1])-Ch(E[t-1],E[t-2],E[t-3])-K[t];
   }
   counts[0]++;
   if(memcmp(a,b,4*sizeof(uint32_t)))continue;counts[1]++;
   if(b[20]-a[20]!=0x8004||memcmp(a+21,b+21,3*sizeof(uint32_t)))continue;counts[2]++;
   if(!signok(a[20],b[20],"================u==========1=u=="))continue;counts[3]++;
   if(s0(a[20]+0x8004)-s0(a[20])!=(uint32_t)-0x28011100)continue;counts[4]++;
   // F8: paired step-8 E round must give the same E4 with W8 difference d8.
   uint32_t u=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12]);
   uint32_t v=b[15]-b[3]-S1(b[14])-Ch(b[14],b[13],b[12]);
   if(v-u!=0x28011100)continue;counts[5]++;
   if(nout==cap){cap*=2;out=realloc(out,cap*sizeof(Point));if(!out){perror("realloc");return 3;}}
   if(nout>=131072){fprintf(stderr,"generated-row cap exceeded\n");return 5;}
   out[nout++]=x;local++;
  }
  if((seed-first)%25==0)fprintf(stderr,"seed=%d local=%zu total=%zu seconds=%ld\n",seed,local,nout,time(0)-start);
 }
 qsort(out,nout,sizeof(Point),cmp_point);size_t uniq=0;for(size_t i=0;i<nout;i++)if(i==0||memcmp(out+i,out+i-1,sizeof(Point)))out[uniq++]=out[i];
 fprintf(stderr,"range=%d:%d counts tested=%llu shared=%llu dw=%llu signedW9=%llu V9=%llu F8=%llu raw=%zu uniq=%zu seconds=%ld\n",first,last,(unsigned long long)counts[0],(unsigned long long)counts[1],(unsigned long long)counts[2],(unsigned long long)counts[3],(unsigned long long)counts[4],(unsigned long long)counts[5],nout,uniq,time(0)-start);
 char name[256];snprintf(name,sizeof(name),"/tmp/r31_variant/recombined_%d_%d.bin",first,last);
 f=fopen(name,"wb");if(!f||fwrite(out,sizeof(Point),uniq,f)!=uniq){perror("output");return 4;}fclose(f);
 return 0;
}
```


### count_keys_sample.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t a[24],b[24];} Point;
static inline uint32_t rot(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return rot(x,2)^rot(x,13)^rot(x,22);}
static inline uint32_t S1(uint32_t x){return rot(x,6)^rot(x,11)^rot(x,25);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
int main(int argc,char**argv){
 if(argc!=5){fprintf(stderr,"usage: count_keys_sample inputpoints.bin activeout.bin progress-every sampleout.bin\n");return 1;}
 FILE*f=fopen(argv[1],"rb");if(!f){perror("points");return 2;}fseek(f,0,SEEK_END);long sz=ftell(f);rewind(f);if(sz%sizeof(Point)){fprintf(stderr,"bad size\n");return 2;}size_t N=sz/sizeof(Point);
 if(N>131072){fprintf(stderr,"generated-row cap exceeded\n");return 5;}
 uint8_t*bits=calloc(1,1ULL<<29);if(!bits){perror("bitmap");return 2;}
 uint32_t v7[512],v8[49408];FILE*g=fopen("/tmp/r31_v7.bin","rb");if(!g||fread(v7,sizeof(v7),1,g)!=1)return 2;fclose(g);
 g=fopen("/tmp/r31_v8.bin","rb");if(!g||fread(v8,sizeof(v8),1,g)!=1)return 2;fclose(g);
 FILE*h=fopen(argv[2],"wb");if(!h){perror("active");return 2;} FILE*sample=fopen(argv[4],"wb");if(!sample){perror("sample");return 2;} unsigned long long sampled=0;
 unsigned long long tuple=0,keys=0,pass8=0,rej5=0,active=0;size_t progress=atoi(argv[3]);time_t start=time(0);
 Point P;
 for(size_t p=0;p<N;p++){
  if(fread(&P,sizeof(P),1,f)!=1)return 3;uint32_t *a=P.a,*b=P.b;uint64_t npoint=0;
  uint32_t rhs7=b[14]-a[14]-(S1(b[13])-S1(a[13]))-0x4fefb5fa;
  uint32_t rhs6=b[13]-a[13]-(S1(b[12])-S1(a[12]))-0x002087f1;
  uint32_t c4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98;
  uint32_t c0=-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
  for(int j=0;j<49408;j++){
   uint32_t w8=v8[j],e4=c4-w8;
   if(Ch(b[13],b[12],e4)-Ch(a[13],a[12],e4)!=rhs7)continue;
   if(++pass8>(1ULL<<29)){fprintf(stderr,"F7 W8 cap exceeded\n");return 5;}
   uint32_t c3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4+c0;
   for(int k=0;k<512;k++){
    uint32_t w7=v7[k],e3=c3-w7;
    if(Ch(b[12],e4,e3)-Ch(a[12],e4,e3)!=rhs6)continue;
    if(++tuple>(1ULL<<30)){fprintf(stderr,"F6 tuple cap exceeded\n");return 5;}
    uint32_t e2=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4;
    uint32_t e2p=b[13]-b[1]-S1(b[12])-Ch(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2p){rej5++;continue;}
    uint32_t key=e3-a[2]+S0(a[1])+Maj(a[1],a[0],a0);
    uint8_t mask=(uint8_t)(1u<<(key&7));uint8_t *pos=bits+(key>>3);
    if(!(*pos&mask)){*pos|=mask;keys++; uint32_t hkey=key; hkey^=hkey>>16; hkey*=0x7feb352du; hkey^=hkey>>15; hkey*=0x846ca68bu; hkey^=hkey>>16; if((hkey&4095u)==0){uint32_t row[4]={key,(uint32_t)p,w7,w8};if(fwrite(row,sizeof(row),1,sample)!=1)return 3;sampled++;}}
    npoint++;
   }
  }
  if(npoint){if(fwrite(&P,sizeof(P),1,h)!=1)return 3;active++;}
  if(progress&&((p+1)%progress==0||p+1==N))fprintf(stderr,"points=%zu/%zu active=%llu tuples=%llu keys=%llu pass8=%llu f5rej=%llu sampled=%llu sec=%ld\n",p+1,N,active,tuple,keys,pass8,rej5,sampled,time(0)-start);
 }
 fclose(f);fclose(h);fclose(sample);free(bits);return 0;
}
```


### r31_first8_low16_independent_omp.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct { uint32_t a[24], b[24]; } Point;
typedef struct { uint32_t key,c6,point,w7,w8; } Item;
typedef struct { uint16_t e4,e3,a0,ce2,base,c6,key; } Info;
typedef struct {
 int bits, mask, n5, n6;
 uint32_t f5, f6;
 uint8_t has6[65536];
 uint16_t vals6[2048], corr5[65536];
 uint64_t extra_scaled, positive_extra;
} Projection;

static Point *P;
static Item *T;
static inline uint32_t ro(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return ro(x,2)^ro(x,13)^ro(x,22);}
static inline uint32_t S1(uint32_t x){return ro(x,6)^ro(x,11)^ro(x,25);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static inline uint16_t ch16(uint16_t x,uint16_t y,uint16_t z){return z^(x&(y^z));}
static inline uint16_t maj16(uint16_t x,uint16_t y,uint16_t z){return (x&y)^(x&z)^(y&z);}

static void info(Info *out,const Item *t){
 uint32_t *a=P[t->point].a;
 uint32_t e4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98-t->w8;
 uint32_t e3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5-t->w7;
 uint32_t a0=e4-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
 uint32_t ce2=a[1]-S0(a[0])-Maj(a[0],a0,t->key);
 uint32_t base=a[12]-2*a[0]+S0(a0)-S1(e4)-0x59f111f1;
 uint32_t c6=a[13]-2*a[1]+S0(a[0])+Maj(a[0],a0,t->key)-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4;
 *out=(Info){e4,e3,a0,ce2,base,c6,t->key};
}
static inline uint16_t c5(const Info *p,uint16_t x){
 return p->base+maj16(p->a0,p->key,x)-ch16(p->e4,p->e3,x+p->ce2);
}
static uint32_t pair_upper(const Info *a,const Info *b,const Projection *p){
 uint64_t sum=0;
 for(int h=0;h<p->n6;h++){
  uint16_t x=(uint16_t)((a->c6-p->vals6[h])&p->mask);
  if(!p->has6[(b->c6-x)&p->mask])continue;
  uint16_t delta=(uint16_t)((c5(b,x)-c5(a,x))&p->mask);
  sum+=p->corr5[delta];
 }
 uint64_t scaled=(sum*p->f5*p->f6)>>17;
 return scaled>(1u<<20)?(1u<<20):(uint32_t)scaled;
}
static void init_projection(Projection *p,int bits,const uint32_t *v5,size_t n5,const uint32_t *v6,size_t n6){
 p->bits=bits;p->mask=(1<<bits)-1;
 uint32_t *freq5=calloc(1<<bits,sizeof(uint32_t));
 uint32_t *freq6=calloc(1<<bits,sizeof(uint32_t));
 uint16_t *vals5=malloc(n5*sizeof(uint16_t));
 if(!freq5||!freq6||!vals5)exit(2);
 for(size_t i=0;i<n5;i++)freq5[v5[i]&p->mask]++;
 for(size_t i=0;i<n6;i++)freq6[v6[i]&p->mask]++;
 for(int i=0;i<=p->mask;i++){
  if(freq5[i]){if(p->n5>=512)exit(3);vals5[p->n5++]=i;if(!p->f5)p->f5=freq5[i];else if(p->f5!=freq5[i])exit(4);}
  if(freq6[i]){if(p->n6>=2048)exit(5);p->vals6[p->n6++]=i;p->has6[i]=1;if(!p->f6)p->f6=freq6[i];else if(p->f6!=freq6[i])exit(6);}
 }
 for(int i=0;i<p->n5;i++)for(int j=0;j<p->n5;j++)p->corr5[(vals5[i]-vals5[j])&p->mask]++;
 fprintf(stderr,"bits=%d support5=%d freq5=%u support6=%d freq6=%u\n",bits,p->n5,p->f5,p->n6,p->f6);
 free(freq5);free(freq6);free(vals5);
}
static uint32_t *read_words(const char *path,size_t *n){
 FILE*f=fopen(path,"rb");if(!f){perror(path);exit(7);}fseek(f,0,SEEK_END);long sz=ftell(f);rewind(f);if(sz<0||sz%4)exit(8);*n=sz/4;
 uint32_t*v=malloc(sz);if(!v||fread(v,4,*n,f)!=*n)exit(9);fclose(f);return v;
}
typedef struct { uint32_t key,n; uint64_t packed[8]; } Group;
_Static_assert(sizeof(Group)==72,"group format");
static Group *G;
static uint32_t *slot;
static uint32_t v7[512],v8[49408];
static uint32_t shift_off[65537];
static uint16_t *shift_residue;
static void build_intersection_lists(const Projection *pr){
 if(pr->bits!=16||pr->n6!=2048||pr->f5!=32||pr->f6!=4096)exit(20);
 uint32_t count[65536]={0},cursor[65536];
 for(int i=0;i<pr->n6;i++)for(int j=0;j<pr->n6;j++)count[(pr->vals6[j]-pr->vals6[i])&65535]++;
 for(int d=0;d<65536;d++)shift_off[d+1]=shift_off[d]+count[d];
 if(shift_off[65536]!=(1u<<22))exit(21);
 shift_residue=malloc((1u<<22)*sizeof(uint16_t));if(!shift_residue)exit(22);
 memcpy(cursor,shift_off,65536*sizeof(uint32_t));
 for(int i=0;i<pr->n6;i++)for(int j=0;j<pr->n6;j++){
  int d=(pr->vals6[j]-pr->vals6[i])&65535;
  shift_residue[cursor[d]++]=pr->vals6[i];
 }
}
static inline uint32_t pair_bound_fast(const Info *a,const Info *b,const Projection *pr,uint64_t *iter){
 uint16_t d=(uint16_t)(b->c6-a->c6);uint32_t sum=0;
 for(uint32_t p=shift_off[d];p<shift_off[d+1];p++){
  uint16_t x=(uint16_t)(a->c6-shift_residue[p]);
  uint16_t delta=(uint16_t)(c5(b,x)-c5(a,x));
  sum+=pr->corr5[delta];(*iter)++;
  if(sum>=(1u<<20))return 1u<<20;
 }
 return sum;
}
int main(void){
 time_t t0=time(0);FILE*f=fopen("/tmp/r31_variant/recombined_0_400.bin","rb");if(!f)return 1;
 P=malloc(64800*sizeof(Point));if(!P||fread(P,sizeof(Point),64800,f)!=64800)return 2;fclose(f);
 f=fopen("/tmp/r31_v7.bin","rb");if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_v8.bin","rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 4;fclose(f);
 size_t n5,n6;uint32_t *v5full=read_words("/tmp/r31_v5.bin",&n5),*v6full=read_words("/tmp/r31_v6.bin",&n6);
 Projection *pr=calloc(1,sizeof(Projection));if(!pr)return 5;
 init_projection(pr,16,v5full,n5,v6full,n6);build_intersection_lists(pr);free(v5full);free(v6full);
 slot=calloc(1ULL<<32,sizeof(uint32_t));if(!slot)return 6;
 const size_t cap=200000000ULL;G=malloc(cap*sizeof(Group));if(!G)return 7;
 size_t ng=0;uint64_t tuple=0,pass8=0,rej5=0,retained=0;
 for(uint32_t p=0;p<64800;p++){
  uint32_t *a=P[p].a,*b=P[p].b;
  uint32_t rhs7=b[14]-a[14]-(S1(b[13])-S1(a[13]))-0x4fefb5fa;
  uint32_t rhs6=b[13]-a[13]-(S1(b[12])-S1(a[12]))-0x002087f1;
  uint32_t c4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98;
  uint32_t c0=-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
  for(uint32_t j=0;j<49408;j++){
   uint32_t w8=v8[j],e4=c4-w8;
   if(Ch(b[13],b[12],e4)-Ch(a[13],a[12],e4)!=rhs7)continue;
   pass8++;
   uint32_t c3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4+c0;
   for(uint32_t k=0;k<512;k++){
    uint32_t w7=v7[k],e3=c3-w7;
    if(Ch(b[12],e4,e3)-Ch(a[12],e4,e3)!=rhs6)continue;
    uint32_t e2=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4;
    uint32_t e2prime=b[13]-b[1]-S1(b[12])-Ch(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2prime){rej5++;continue;}
    uint32_t key=e3-a[2]+S0(a[1])+Maj(a[1],a[0],a0);
    uint32_t id=slot[key];Group *g;
    if(id==0){if(ng>=cap)return 8;g=&G[ng];g->key=key;g->n=0;slot[key]=(uint32_t)(++ng);}
    else g=&G[id-1];
    if(g->n<8){g->packed[g->n++]=((uint64_t)p<<25)|((uint64_t)j<<9)|k;retained++;}
    tuple++;
   }
  }
  if((p+1)%10000==0)fprintf(stderr,"rows=%u tuples=%llu keys=%zu retained=%llu sec=%ld\n",p+1,(unsigned long long)tuple,ng,(unsigned long long)retained,time(0)-t0);
 }
 if(tuple!=755416216ULL||ng!=195265888ULL||pass8!=409618384ULL||rej5!=0||retained!=641616343ULL){
  fprintf(stderr,"FAIL finite counts tuple=%llu keys=%zu pass8=%llu rej5=%llu retained=%llu\n",(unsigned long long)tuple,ng,(unsigned long long)pass8,(unsigned long long)rej5,(unsigned long long)retained);return 9;
 }
 free(slot);slot=NULL;
 uint64_t numerator=0,npair=0,niter=0;
 const size_t chunk=5000000;
 for(size_t start=0;start<ng;start+=chunk){
  size_t end=start+chunk<ng?start+chunk:ng;
  uint64_t block_num=0,block_pair=0,block_iter=0;
  #pragma omp parallel for schedule(dynamic,16384) reduction(+:block_num,block_pair,block_iter)
  for(size_t ix=start;ix<end;ix++){
   const Group *g=&G[ix];int m=(int)g->n;
   if(m==1){block_num+=(1u<<20);continue;}
   Info inf[8];
   for(int z=0;z<m;z++){
    uint64_t pack=g->packed[z];uint32_t p=(uint32_t)(pack>>25),j=(uint32_t)((pack>>9)&65535),k=(uint32_t)(pack&511);
    if(p>=64800||j>=49408||k>=512)abort();
    Item it={g->key,0,p,v7[k],v8[j]};info(&inf[z],&it);
   }
   uint64_t value=(1u<<20);
   for(int z=1;z<m;z++){
    uint32_t cost=0;
    for(int q=0;q<z;q++){
     cost+=pair_bound_fast(&inf[q],&inf[z],pr,&block_iter);block_pair++;
     if(cost>=(1u<<20))break;
    }
    if(cost<(1u<<20))value+=(1u<<20)-cost;
   }
   block_num+=value;
  }
  numerator+=block_num;npair+=block_pair;niter+=block_iter;
  fprintf(stderr,"cert_keys=%zu/%zu bound=%.4f pair=%llu iter=%llu elapsed=%ld\n",end,ng,(double)numerator/(1u<<20),(unsigned long long)npair,(unsigned long long)niter,time(0)-t0);
 }
 uint64_t hist[9]={0};for(size_t i=0;i<ng;i++){if(G[i].n<1||G[i].n>8)abort();hist[G[i].n]++;}
 printf("tuples=%llu keys=%zu retained=%llu pass8=%llu rej5=%llu\n",(unsigned long long)tuple,ng,(unsigned long long)retained,(unsigned long long)pass8,(unsigned long long)rej5);
 for(int i=1;i<=8;i++)printf("hist%d=%llu\n",i,(unsigned long long)hist[i]);
 printf("first8_scaled20=%llu equivalent=%.9f ratio=%.9f pair_calls=%llu pair_iterations=%llu elapsed=%ld\n",(unsigned long long)numerator,(double)numerator/(1u<<20),(double)numerator/(double)(1u<<20)/ng,(unsigned long long)npair,(unsigned long long)niter,time(0)-t0);
}
```


### r31_first8_low16_conservative.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {uint32_t a[24],b[24];} Point;
typedef struct {uint32_t point,w7,w8,c6;} Rep;
typedef struct {uint32_t key,count;Rep t[8];} Group;
typedef struct {uint16_t e4,e3,a0,ce2,base,c6,key;} Info;
typedef struct {int bits,mask,n5,n6;uint8_t R6[65536];uint16_t R6vals[2048],Corr5[65536];} Support;
_Static_assert(sizeof(Group)==136,"Group size");
static Point *P;
static Support S8,S12,S16;
static uint64_t calls8,calls12,calls16;
static uint32_t shift_off[65537];
static uint16_t *shift_vals;
static inline uint32_t ro(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return ro(x,2)^ro(x,13)^ro(x,22);}
static inline uint32_t S1(uint32_t x){return ro(x,6)^ro(x,11)^ro(x,25);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static inline uint16_t ch16(uint16_t x,uint16_t y,uint16_t z){return z^(x&(y^z));}
static inline uint16_t maj16(uint16_t x,uint16_t y,uint16_t z){return (x&y)^(x&z)^(y&z);}
static void info(Info *out,uint32_t key,const Rep *t){
 uint32_t *a=P[t->point].a;
 uint32_t e4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98-t->w8;
 uint32_t e3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5-t->w7;
 uint32_t a0=e4-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
 uint32_t ce2=a[1]-S0(a[0])-Maj(a[0],a0,key);
 uint32_t base=a[12]-2*a[0]+S0(a0)-S1(e4)-0x59f111f1;
 uint32_t c6=a[13]-2*a[1]+S0(a[0])+Maj(a[0],a0,key)-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4;
 if(c6!=t->c6){fprintf(stderr,"C6 mismatch row %u key %08x\n",t->point,key);exit(5);}
 *out=(Info){e4,e3,a0,ce2,base,c6,key};
}
static inline uint16_t c5(const Info *t,uint16_t x){
 return t->base+maj16(t->a0,t->key,x)-ch16(t->e4,t->e3,x+t->ce2);
}
static uint32_t pair_bound_for(const Info *a,const Info *b,const Support *s){
 uint32_t sum=0,denom=s->n5*s->n6;
 for(int h=0;h<s->n6;h++){
  uint16_t x=(a->c6-s->R6vals[h])&s->mask;
  if(!s->R6[(b->c6-x)&s->mask])continue;
  uint16_t delta=(c5(b,x)-c5(a,x))&s->mask;
  sum+=s->Corr5[delta];
  if(sum>=denom)return denom;
 }
 return sum;
}
static uint32_t pair_bound(const Info *a,const Info *b){
 uint16_t delta=b->c6-a->c6;
 uint32_t sum=0;
 for(uint32_t p=shift_off[delta];p<shift_off[delta+1];p++){
  uint16_t x=a->c6-shift_vals[p];
  uint16_t dc=c5(b,x)-c5(a,x);
  sum+=S16.Corr5[dc];
  if(sum>=(1<<20))return 1<<20;
 }
 return sum;
}
static int init_support(Support *s,int bits){
 s->bits=bits;s->mask=(1<<bits)-1;
 static uint32_t freq5[65536],freq6[65536];memset(freq5,0,sizeof(freq5));memset(freq6,0,sizeof(freq6));
 uint32_t u;FILE *f=fopen("/tmp/r31_v5.bin","rb");if(!f)return 0;
 while(fread(&u,4,1,f)==1)freq5[u&s->mask]++;fclose(f);
 f=fopen("/tmp/r31_v6.bin","rb");if(!f)return 0;
 while(fread(&u,4,1,f)==1)freq6[u&s->mask]++;fclose(f);
 uint16_t r5vals[512];
 for(int x=0;x<=s->mask;x++){
  if(freq5[x]){if(s->n5==512)return 0;r5vals[s->n5++]=x;}
  if(freq6[x]){if(s->n6==2048)return 0;s->R6[x]=1;s->R6vals[s->n6++]=x;}
 }
 if(!s->n5||!s->n6)return 0;
 for(int x=0;x<=s->mask;x++){
  if(freq5[x]&&freq5[x]!=(1<<14)/s->n5)return 0;
  if(freq6[x]&&freq6[x]!=(1<<23)/s->n6)return 0;
 }
 for(int i=0;i<s->n5;i++)for(int j=0;j<s->n5;j++)s->Corr5[(r5vals[i]-r5vals[j])&s->mask]++;
 return 1;
}
int main(void){
 time_t start=time(0);FILE *f=fopen("/tmp/r31_variant/recombined_0_400.bin","rb");if(!f)return 1;
 P=malloc(64800*sizeof(Point));if(!P||fread(P,sizeof(Point),64800,f)!=64800)return 2;fclose(f);
 uint32_t v7[512],v8[49408];f=fopen("/tmp/r31_v7.bin","rb");if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_v8.bin","rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 4;fclose(f);
 if(!init_support(&S8,8)||!init_support(&S12,12)||!init_support(&S16,16))return 10;
 fprintf(stderr,"supports 8=(%d,%d) 12=(%d,%d) 16=(%d,%d)\n",S8.n5,S8.n6,S12.n5,S12.n6,S16.n5,S16.n6);
 for(int i=0;i<2048;i++)for(int j=0;j<2048;j++){
  uint16_t d=S16.R6vals[i]-S16.R6vals[j];
  shift_off[d+1]++;
 }
 for(int d=1;d<=65536;d++)shift_off[d]+=shift_off[d-1];
 if(shift_off[65536]!=(1u<<22))return 17;
 shift_vals=malloc((1u<<22)*sizeof(uint16_t));if(!shift_vals)return 18;
 uint32_t shift_pos[65536];memcpy(shift_pos,shift_off,65536*sizeof(uint32_t));
 for(int i=0;i<2048;i++)for(int j=0;j<2048;j++){
  uint16_t d=S16.R6vals[i]-S16.R6vals[j];
  shift_vals[shift_pos[d]++]=S16.R6vals[j];
 }
#ifdef SAMPLE_TEST
 typedef struct {uint32_t key,c6,point,w7,w8;} SampleItem;
 f=fopen("/tmp/r31_sample_items.bin","rb");if(!f)return 19;
 SampleItem t,first={0};uint64_t checked=0;int have_first=0;
 while(fread(&t,sizeof(t),1,f)==1){
  if(!have_first||t.key!=first.key){first=t;have_first=1;continue;}
  Rep ar={first.point,first.w7,first.w8,first.c6};
  Rep br={t.point,t.w7,t.w8,t.c6};
  Info ai,bi;info(&ai,t.key,&ar);info(&bi,t.key,&br);
  uint32_t fast=pair_bound(&ai,&bi),slow=pair_bound_for(&ai,&bi,&S16);
  if(fast!=slow){fprintf(stderr,"pair mismatch key %08x fast %u slow %u\n",t.key,fast,slow);return 20;}
  checked++;
 }
 fclose(f);printf("sample_pairs_compared=%llu\n",(unsigned long long)checked);return 0;
#endif
 uint32_t *slot=calloc(1ULL<<32,sizeof(uint32_t));if(!slot)return 11;
 size_t cap=1u<<28;Group *G=malloc(cap*sizeof(Group));if(!G)return 12;
 size_t ng=0;uint64_t tuples=0,pass8=0,rawret=0,rejected_e2=0;uint64_t hist[9]={0};
 for(uint32_t p=0;p<64800;p++){
  uint32_t *a=P[p].a,*b=P[p].b;
  uint32_t rhs7=b[14]-a[14]-(S1(b[13])-S1(a[13]))-0x4fefb5fa;
  uint32_t rhs6=b[13]-a[13]-(S1(b[12])-S1(a[12]))-0x002087f1;
  uint32_t c4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98;
  uint32_t c0=-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
  for(int j=0;j<49408;j++){
   uint32_t w8=v8[j],e4=c4-w8;
   if(Ch(b[13],b[12],e4)-Ch(a[13],a[12],e4)!=rhs7)continue;
   if(++pass8>(1ULL<<29)){fprintf(stderr,"F7-pass cap exceeded\n");return 15;}
   uint32_t c3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4+c0;
   for(int z=0;z<512;z++){
    uint32_t w7=v7[z],e3=c3-w7;
    if(Ch(b[12],e4,e3)-Ch(a[12],e4,e3)!=rhs6)continue;
    if(++tuples>(1ULL<<30)){fprintf(stderr,"F6-pass cap exceeded\n");return 16;}
    uint32_t e2=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4;
    uint32_t e2p=b[13]-b[1]-S1(b[12])-Ch(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2p){rejected_e2++;continue;}
    uint32_t key=e3-a[2]+S0(a[1])+Maj(a[1],a[0],a0);
    uint32_t ix=slot[key];Group *g;
    if(!ix){if(ng==cap)return 13;ix=++ng;slot[key]=ix;g=&G[ix-1];g->key=key;g->count=0;}
    else g=&G[ix-1];
    if(g->count<8){
     uint32_t d2=a[1]-S0(a[0])-Maj(a[0],a0,key);
     uint32_t c6=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4-d2;
     g->t[g->count++]=(Rep){p,w7,w8,c6};rawret++;
    }
   }
  }
  if((p+1)%10000==0)fprintf(stderr,"rows=%u tuples=%llu keys=%zu retained=%llu elapsed=%ld\n",p+1,(unsigned long long)tuples,ng,(unsigned long long)rawret,time(0)-start);
 }
 if(tuples!=755416216||ng!=195265888||pass8!=409618384||rejected_e2!=0){fprintf(stderr,"wrong finite counts %llu %zu %llu e2rej=%llu\n",(unsigned long long)tuples,ng,(unsigned long long)pass8,(unsigned long long)rejected_e2);return 14;}
 free(slot);fprintf(stderr,"enumeration complete tuples=%llu keys=%zu retained=%llu elapsed=%ld\n",(unsigned long long)tuples,ng,(unsigned long long)rawret,time(0)-start);
 uint64_t numerator=0;uint64_t selected=0,zero_pairs=0,total_pairs=0;
 for(size_t k=0;k<ng;k++)hist[G[k].count]++;
#pragma omp parallel for schedule(dynamic,50000) reduction(+:numerator,selected,zero_pairs,total_pairs)
 for(size_t k=0;k<ng;k++){
  Group *g=&G[k];int m=g->count;
  Info in[8];for(int i=0;i<m;i++)info(&in[i],g->key,&g->t[i]);
  int chosen[8]={1};uint32_t value=1<<20;int nchosen=1;
  for(int j=1;j<m;j++){
   uint32_t cost=0;
   for(int i=0;i<j;i++){
    uint32_t pb=pair_bound(&in[i],&in[j]);total_pairs++;if(pb==0)zero_pairs++;
    cost+=pb;
    if(cost>=(1<<20))break;
   }
   if(cost<(1<<20)){chosen[j]=1;nchosen++;value+=(1<<20)-cost;}
  }
  selected+=nchosen;numerator+=value;
 }
 printf("tuples=%llu keys=%zu retained=%llu pass8=%llu rejected_E2=%llu\n",(unsigned long long)tuples,ng,(unsigned long long)rawret,(unsigned long long)pass8,(unsigned long long)rejected_e2);
 for(int i=1;i<=8;i++)printf("hist%d=%llu\n",i,(unsigned long long)hist[i]);
 printf("pairs=%llu zero_pairs=%llu\n",(unsigned long long)total_pairs,(unsigned long long)zero_pairs);
 printf("greedy_numerator=%llu denominator=%u equivalent=%.9f ratio=%.9f selected=%llu elapsed=%ld\n",(unsigned long long)numerator,1u<<20,(double)numerator/(1<<20),(double)numerator/((double)(1<<20)*ng),(unsigned long long)selected,time(0)-start);
 return 0;
}
```


### r31_first8_low16_fast.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {uint32_t a[24],b[24];} Point;
typedef struct {uint32_t point,w7,w8,c6;} Rep;
typedef struct {uint32_t key,count;Rep t[8];} Group;
typedef struct {uint16_t e4,e3,a0,ce2,base,c6,key;} Info;
typedef struct {int bits,mask,n5,n6;uint8_t R6[65536];uint16_t R6vals[2048],Corr5[65536];} Support;
_Static_assert(sizeof(Group)==136,"Group size");
static Point *P;
static Support S8,S12,S16;
static uint64_t calls8,calls12,calls16;
static uint32_t shift_off[65537];
static uint16_t *shift_vals;
static inline uint32_t ro(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return ro(x,2)^ro(x,13)^ro(x,22);}
static inline uint32_t S1(uint32_t x){return ro(x,6)^ro(x,11)^ro(x,25);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static inline uint16_t ch16(uint16_t x,uint16_t y,uint16_t z){return z^(x&(y^z));}
static inline uint16_t maj16(uint16_t x,uint16_t y,uint16_t z){return (x&y)^(x&z)^(y&z);}
static void info(Info *out,uint32_t key,const Rep *t){
 uint32_t *a=P[t->point].a;
 uint32_t e4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98-t->w8;
 uint32_t e3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5-t->w7;
 uint32_t a0=e4-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
 uint32_t ce2=a[1]-S0(a[0])-Maj(a[0],a0,key);
 uint32_t base=a[12]-2*a[0]+S0(a0)-S1(e4)-0x59f111f1;
 uint32_t c6=a[13]-2*a[1]+S0(a[0])+Maj(a[0],a0,key)-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4;
 if(c6!=t->c6){fprintf(stderr,"C6 mismatch row %u key %08x\n",t->point,key);exit(5);}
 *out=(Info){e4,e3,a0,ce2,base,c6,key};
}
static inline uint16_t c5(const Info *t,uint16_t x){
 return t->base+maj16(t->a0,t->key,x)-ch16(t->e4,t->e3,x+t->ce2);
}
static uint32_t pair_bound_for(const Info *a,const Info *b,const Support *s){
 uint32_t sum=0,denom=s->n5*s->n6;
 for(int h=0;h<s->n6;h++){
  uint16_t x=(a->c6-s->R6vals[h])&s->mask;
  if(!s->R6[(b->c6-x)&s->mask])continue;
  uint16_t delta=(c5(b,x)-c5(a,x))&s->mask;
  sum+=s->Corr5[delta];
  if(sum>=denom)return denom;
 }
 return sum;
}
static uint32_t pair_bound(const Info *a,const Info *b){
 uint16_t delta=b->c6-a->c6;
 uint32_t sum=0;
 for(uint32_t p=shift_off[delta];p<shift_off[delta+1];p++){
  uint16_t x=a->c6-shift_vals[p];
  uint16_t dc=c5(b,x)-c5(a,x);
  sum+=S16.Corr5[dc];
  if(sum>=(1<<20))return 1<<20;
 }
 return sum;
}
static int init_support(Support *s,int bits){
 s->bits=bits;s->mask=(1<<bits)-1;
 static uint32_t freq5[65536],freq6[65536];memset(freq5,0,sizeof(freq5));memset(freq6,0,sizeof(freq6));
 uint32_t u;FILE *f=fopen("/tmp/r31_v5.bin","rb");if(!f)return 0;
 while(fread(&u,4,1,f)==1)freq5[u&s->mask]++;fclose(f);
 f=fopen("/tmp/r31_v6.bin","rb");if(!f)return 0;
 while(fread(&u,4,1,f)==1)freq6[u&s->mask]++;fclose(f);
 uint16_t r5vals[512];
 for(int x=0;x<=s->mask;x++){
  if(freq5[x]){if(s->n5==512)return 0;r5vals[s->n5++]=x;}
  if(freq6[x]){if(s->n6==2048)return 0;s->R6[x]=1;s->R6vals[s->n6++]=x;}
 }
 if(!s->n5||!s->n6)return 0;
 for(int x=0;x<=s->mask;x++){
  if(freq5[x]&&freq5[x]!=(1<<14)/s->n5)return 0;
  if(freq6[x]&&freq6[x]!=(1<<23)/s->n6)return 0;
 }
 for(int i=0;i<s->n5;i++)for(int j=0;j<s->n5;j++)s->Corr5[(r5vals[i]-r5vals[j])&s->mask]++;
 return 1;
}
int main(void){
 time_t start=time(0);FILE *f=fopen("/tmp/r31_variant/recombined_0_400.bin","rb");if(!f)return 1;
 P=malloc(64800*sizeof(Point));if(!P||fread(P,sizeof(Point),64800,f)!=64800)return 2;fclose(f);
 uint32_t v7[512],v8[49408];f=fopen("/tmp/r31_v7.bin","rb");if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_v8.bin","rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 4;fclose(f);
 if(!init_support(&S8,8)||!init_support(&S12,12)||!init_support(&S16,16))return 10;
 fprintf(stderr,"supports 8=(%d,%d) 12=(%d,%d) 16=(%d,%d)\n",S8.n5,S8.n6,S12.n5,S12.n6,S16.n5,S16.n6);
 for(int i=0;i<2048;i++)for(int j=0;j<2048;j++){
  uint16_t d=S16.R6vals[i]-S16.R6vals[j];
  shift_off[d+1]++;
 }
 for(int d=1;d<=65536;d++)shift_off[d]+=shift_off[d-1];
 if(shift_off[65536]!=(1u<<22))return 17;
 shift_vals=malloc((1u<<22)*sizeof(uint16_t));if(!shift_vals)return 18;
 uint32_t shift_pos[65536];memcpy(shift_pos,shift_off,65536*sizeof(uint32_t));
 for(int i=0;i<2048;i++)for(int j=0;j<2048;j++){
  uint16_t d=S16.R6vals[i]-S16.R6vals[j];
  shift_vals[shift_pos[d]++]=S16.R6vals[j];
 }
#ifdef SAMPLE_TEST
 typedef struct {uint32_t key,c6,point,w7,w8;} SampleItem;
 f=fopen("/tmp/r31_sample_items.bin","rb");if(!f)return 19;
 SampleItem t,first={0};uint64_t checked=0;int have_first=0;
 while(fread(&t,sizeof(t),1,f)==1){
  if(!have_first||t.key!=first.key){first=t;have_first=1;continue;}
  Rep ar={first.point,first.w7,first.w8,first.c6};
  Rep br={t.point,t.w7,t.w8,t.c6};
  Info ai,bi;info(&ai,t.key,&ar);info(&bi,t.key,&br);
  uint32_t fast=pair_bound(&ai,&bi),slow=pair_bound_for(&ai,&bi,&S16);
  if(fast!=slow){fprintf(stderr,"pair mismatch key %08x fast %u slow %u\n",t.key,fast,slow);return 20;}
  checked++;
 }
 fclose(f);printf("sample_pairs_compared=%llu\n",(unsigned long long)checked);return 0;
#endif
 uint32_t *slot=calloc(1ULL<<32,sizeof(uint32_t));if(!slot)return 11;
 size_t cap=1u<<28;Group *G=malloc(cap*sizeof(Group));if(!G)return 12;
 size_t ng=0;uint64_t tuples=0,pass8=0,rawret=0,rejected_e2=0;uint64_t hist[9]={0};
 for(uint32_t p=0;p<64800;p++){
  uint32_t *a=P[p].a,*b=P[p].b;
  uint32_t rhs7=b[14]-a[14]-(S1(b[13])-S1(a[13]))-0x4fefb5fa;
  uint32_t rhs6=b[13]-a[13]-(S1(b[12])-S1(a[12]))-0x002087f1;
  uint32_t c4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98;
  uint32_t c0=-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
  for(int j=0;j<49408;j++){
   uint32_t w8=v8[j],e4=c4-w8;
   if(Ch(b[13],b[12],e4)-Ch(a[13],a[12],e4)!=rhs7)continue;
   if(++pass8>(1ULL<<29)){fprintf(stderr,"F7-pass cap exceeded\n");return 15;}
   uint32_t c3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4+c0;
   for(int z=0;z<512;z++){
    uint32_t w7=v7[z],e3=c3-w7;
    if(Ch(b[12],e4,e3)-Ch(a[12],e4,e3)!=rhs6)continue;
    if(++tuples>(1ULL<<30)){fprintf(stderr,"F6-pass cap exceeded\n");return 16;}
    uint32_t e2=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4;
    uint32_t e2p=b[13]-b[1]-S1(b[12])-Ch(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2p){rejected_e2++;continue;}
    uint32_t key=e3-a[2]+S0(a[1])+Maj(a[1],a[0],a0);
    uint32_t ix=slot[key];Group *g;
    if(!ix){if(ng==cap)return 13;ix=++ng;slot[key]=ix;g=&G[ix-1];g->key=key;g->count=0;}
    else g=&G[ix-1];
    if(g->count<8){
     uint32_t d2=a[1]-S0(a[0])-Maj(a[0],a0,key);
     uint32_t c6=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4-d2;
     g->t[g->count++]=(Rep){p,w7,w8,c6};rawret++;
    }
   }
  }
  if((p+1)%10000==0)fprintf(stderr,"rows=%u tuples=%llu keys=%zu retained=%llu elapsed=%ld\n",p+1,(unsigned long long)tuples,ng,(unsigned long long)rawret,time(0)-start);
 }
 if(tuples!=755416216||ng!=195265888||pass8!=409618384||rejected_e2!=0){fprintf(stderr,"wrong finite counts %llu %zu %llu e2rej=%llu\n",(unsigned long long)tuples,ng,(unsigned long long)pass8,(unsigned long long)rejected_e2);return 14;}
 free(slot);fprintf(stderr,"enumeration complete tuples=%llu keys=%zu retained=%llu elapsed=%ld\n",(unsigned long long)tuples,ng,(unsigned long long)rawret,time(0)-start);
 uint64_t numerator=0;uint64_t selected=0,zero_pairs=0,total_pairs=0;
 for(size_t k=0;k<ng;k++)hist[G[k].count]++;
#pragma omp parallel for schedule(dynamic,50000) reduction(+:numerator,selected,zero_pairs,total_pairs)
 for(size_t k=0;k<ng;k++){
  Group *g=&G[k];int m=g->count;
  Info in[8];for(int i=0;i<m;i++)info(&in[i],g->key,&g->t[i]);
  int chosen[8]={1};uint32_t value=1<<20;int nchosen=1;
  for(int j=1;j<m;j++){
   uint32_t cost=0;
   for(int i=0;i<j;i++)if(chosen[i]){
    uint32_t pb=pair_bound(&in[i],&in[j]);total_pairs++;if(pb==0)zero_pairs++;
    cost+=pb;
   }
   if(cost<(1<<20)){chosen[j]=1;nchosen++;value+=(1<<20)-cost;}
  }
  selected+=nchosen;numerator+=value;
 }
 printf("tuples=%llu keys=%zu retained=%llu pass8=%llu rejected_E2=%llu\n",(unsigned long long)tuples,ng,(unsigned long long)rawret,(unsigned long long)pass8,(unsigned long long)rejected_e2);
 for(int i=1;i<=8;i++)printf("hist%d=%llu\n",i,(unsigned long long)hist[i]);
 printf("pairs=%llu zero_pairs=%llu\n",(unsigned long long)total_pairs,(unsigned long long)zero_pairs);
 printf("greedy_numerator=%llu denominator=%u equivalent=%.9f ratio=%.9f selected=%llu elapsed=%ld\n",(unsigned long long)numerator,1u<<20,(double)numerator/(1<<20),(double)numerator/((double)(1<<20)*ng),(unsigned long long)selected,time(0)-start);
 return 0;
}
```


### r31_proj_support_verify.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static uint32_t f5[65536], f6[65536];
static inline uint32_t rot(uint32_t x,unsigned n){return (x>>n)|(x<<(32-n));}
static inline uint32_t sig0(uint32_t x){return rot(x,7)^rot(x,18)^(x>>3);}

int main(void){
 FILE *v5=fopen("/tmp/r31_v5.bin","rb"),*v6=fopen("/tmp/r31_v6.bin","rb");
 if(!v5||!v6){perror("V-file");return 1;}
 uint64_t n5=0,n6=0;uint32_t expected;time_t start=time(0);
 for(uint64_t i=0;i<(1ULL<<32);i++){
  uint32_t x=(uint32_t)i,base=sig0(x);
  if((uint32_t)(sig0(x+0xfffff006u)-base)==0xd0018020u){
   if(fread(&expected,4,1,v5)!=1||expected!=x){fprintf(stderr,"V5 mismatch at %llu\n",(unsigned long long)i);return 2;}
   f5[x&65535]++;n5++;
  }
  if((uint32_t)(sig0(x+0x002087f1u)-base)==0x00000ffau){
   if(fread(&expected,4,1,v6)!=1||expected!=x){fprintf(stderr,"V6 mismatch at %llu\n",(unsigned long long)i);return 3;}
   f6[x&65535]++;n6++;
  }
 }
 if(fread(&expected,4,1,v5)==1||fread(&expected,4,1,v6)==1){fprintf(stderr,"trailing V words\n");return 4;}
 fclose(v5);fclose(v6);
 uint32_t s5=0,s6=0,min5=UINT32_MAX,min6=UINT32_MAX,max5=0,max6=0;
 for(int i=0;i<65536;i++){
  if(f5[i]){s5++;if(f5[i]<min5)min5=f5[i];if(f5[i]>max5)max5=f5[i];}
  if(f6[i]){s6++;if(f6[i]<min6)min6=f6[i];if(f6[i]>max6)max6=f6[i];}
 }
 printf("V5 total=%llu support16=%u freq_min=%u freq_max=%u\n",(unsigned long long)n5,s5,min5,max5);
 printf("V6 total=%llu support16=%u freq_min=%u freq_max=%u\n",(unsigned long long)n6,s6,min6,max6);
 printf("seconds=%ld\n",time(0)-start);
 return n5==(1u<<14)&&n6==(1u<<23)&&s5==512&&s6==2048&&min5==32&&max5==32&&min6==4096&&max6==4096?0:5;
}
```


### r31_newkeys_build.c

```c
/* Independent key-set rebuild from every F8-valid recombined point. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t a[24],b[24];} Point;
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t B0(uint32_t x){return R(x,2)^R(x,13)^R(x,22);}
static inline uint32_t B1(uint32_t x){return R(x,6)^R(x,11)^R(x,25);}
static inline uint32_t C(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t M(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
int main(int argc,char**argv){
 if(argc!=3){fprintf(stderr,"usage: %s point-rows.bin output-bitset.bin\n",argv[0]);return 1;}
 FILE*in=fopen(argv[1],"rb");if(!in){perror("points");return 2;}
 fseek(in,0,SEEK_END);long bytes=ftell(in);rewind(in);
 if(bytes<0||bytes%sizeof(Point)){fprintf(stderr,"bad point file size\n");return 2;}
 size_t n=(size_t)bytes/sizeof(Point);
 uint32_t v7[512],v8[49408];FILE*f=fopen("/tmp/r31_v7.bin","rb");
 if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_v8.bin","rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 3;fclose(f);
 uint8_t*bits=calloc(1,1ULL<<29);if(!bits){perror("bitset");return 4;}
 uint64_t keys=0,tuples=0,active=0,e4bad=0,e2bad=0,pass8=0;
 Point p;time_t t0=time(0);
 for(size_t i=0;i<n;i++){
  if(fread(&p,sizeof(p),1,in)!=1)return 5;
  uint32_t *a=p.a,*b=p.b;uint64_t rows=0;
  uint32_t ea=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98;
  uint32_t eb=b[15]-b[3]-B1(b[14])-C(b[14],b[13],b[12])-0xd807aa98;
  if(eb-ea!=0x28011100){e4bad++;continue;}
  uint32_t need7=b[14]-a[14]-(B1(b[13])-B1(a[13]))-0x4fefb5fa;
  uint32_t need6=b[13]-a[13]-(B1(b[12])-B1(a[12]))-0x002087f1;
  for(size_t j=0;j<49408;j++){
   uint32_t e4=ea-v8[j];
   if(C(b[13],b[12],e4)-C(a[13],a[12],e4)!=need7)continue;
   pass8++;
   uint32_t e3base=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
   uint32_t kbase=-a[2]+B0(a[1])+M(a[1],a[0],a0);
   for(size_t k=0;k<512;k++){
    uint32_t e3=e3base-v7[k];
    if(C(b[12],e4,e3)-C(a[12],e4,e3)!=need6)continue;
    uint32_t e2=a[13]-a[1]-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
    uint32_t e2b=b[13]-b[1]-B1(b[12])-C(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2b){e2bad++;continue;}
    uint32_t key=e3+kbase;uint8_t *slot=bits+(key>>3),mask=(uint8_t)(1u<<(key&7));
    if(!(*slot&mask)){*slot|=mask;keys++;}
    tuples++;rows++;
   }
  }
  if(rows)active++;
  if((i+1)%10000==0||i+1==n)fprintf(stderr,"rows=%zu/%zu active=%llu tuples=%llu keys=%llu elapsed=%lld\n",i+1,n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(long long)(time(0)-t0));
 }
 fclose(in);FILE*out=fopen(argv[2],"wb");if(!out){perror("out");return 6;}
 if(fwrite(bits,1,1ULL<<29,out)!=(1ULL<<29)){perror("write bits");return 7;}
 fclose(out);
 printf("points=%zu active=%llu tuples=%llu unique_keys=%llu pass8=%llu bad_E4=%llu bad_E2=%llu elapsed_s=%lld\n",n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(unsigned long long)pass8,(unsigned long long)e4bad,(unsigned long long)e2bad,(long long)(time(0)-t0));
 free(bits);return 0;
}
```


### audit_active.py

```python
import struct,sys
M=(1<<32)-1
MKA=['===================n=unnnnnnn=n=','========n======================u','===u===n==n========n=========n=u','=============================n==','================================','================u============u==','================================','================================']
MKE=['000111010001111110nu=11111unnnu1','101011=11==0n0==u11110==1110011n','un0u1100n=01u11111001u1=n110u10n','1u01un0u0=1=1=11n=0=u0=001001u0=','01100001110=0=010===00=11101u0=1','=1n1uuuuu0100=1un0=10unnnnnnn010','=01u1010uu1==11100===1000001n=0=','==110001=11====1n====0011110n=0=']
MKW=['================u==========1=u==','================================','================================','================================']
K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74]
def ro(x,n):return (x>>n)|(x<<(32-n))&M
def S0(x):return ro(x,2)^ro(x,13)^ro(x,22)
def S1(x):return ro(x,6)^ro(x,11)^ro(x,25)
def Ch(x,y,z):return z^(x&(y^z))
def Maj(x,y,z):return (x&y)^(x&z)^(y&z)
def signed(x,y,s):
 if len(s)!=32:raise ValueError((s,len(s)))
 for i,c in enumerate(s[::-1]):
  a,b=(x>>i)&1,(y>>i)&1
  if c=='=' and a!=b:return False
  if c=='0' and (a or b):return False
  if c=='1' and (not a or not b):return False
  if c=='u' and (a or not b):return False
  if c=='n' and (not a or b):return False
 return True
fn=sys.argv[1] if len(sys.argv)>1 else '/tmp/r31_variant/active_0_400.bin'
n=0
with open(fn,'rb') as f:
 while raw:=f.read(192):
  a,b=[list(x) for x in (struct.unpack('<24I',raw[:96]),struct.unpack('<24I',raw[96:]))]
  n+=1
  for j in range(8):
   assert signed(a[4+j],b[4+j],MKA[j]),('A',n,j)
   assert signed(a[12+j],b[12+j],MKE[j]),('E',n,j)
  for j in range(4):assert signed(a[20+j],b[20+j],MKW[j]),('W',n,j)
  assert a[:4]==b[:4]
  for q in (a,b):
   A={t:q[t-1] for t in range(1,13)};E={t:q[t+7] for t in range(5,13)}
   for t in range(5,13):
    lhs=(A[t]-E[t])&M
    rhs=(S0(A[t-1])+Maj(A[t-1],A[t-2],A[t-3])-A[t-4])&M
    assert lhs==rhs,('forward A-E',n,t)
   for t in range(9,13):
    rhs=(A[t-4]+E[t-4]+S1(E[t-1])+Ch(E[t-1],E[t-2],E[t-3])+K[t]+q[t+11])&M
    assert rhs==E[t],('forward E',n,t)
  de13=(b[16]-a[16]+S1(b[19])-S1(a[19])+Ch(b[19],b[18],b[17])-Ch(a[19],a[18],a[17]))&M
  da13=(de13+S0(b[11])-S0(a[11])+Maj(b[11],b[10],b[9])-Maj(a[11],a[10],a[9]))&M
  assert de13==da13==0,('P4',n)
print('PASS',n,'all A/E/W signed masks; shared A1..4; forward identities t5..12; E recurrences t9..12; P4')
```


The independent key builder checks F8 again, separately computes E4/E3 and the common-E2 condition, and writes the complete 2^32-bit bitmap. The first-key sampler records the representative when its key bit is first set. The first-eight generator stores up to eight records per key in the same pass; E2/W6/E1/W5 constants are then precomputed once under the setup charge. The Python row audit checks signed A/E/W masks and both-lane identities for *every* 64,800 generated row (or 30,540 active rows when passed that file).


## Appendix C. Scoped research probes

These listings are inert research evidence, not additional organizer experiments or code to run in a credential-bearing judge. The synthetic-CV probe depends on the Appendix B generated files. It selects 2,000 records from the deterministic 48,094-record first-key sample, randomizes W5 and W6 over the complete V5/V6 sets, screens c18, and checks full two-lane 31-step compression after capped Phase 3. Python seed `0xe5e8011` gives 2,000/2,000 completions, 14,767 c18 proposals, median 2,807.5 and maximum 32,552 Phase-3 iterations; its JSON SHA-256 is `9b164c28d146f49d5a9d19e7aa5c6d22c5a54e756fd4be7d44067aad373b5af0`. Run with `PYTHONPATH=. python3 h2_uniform_probe.py` after saving the three Python listings in one scratch directory and supplying the Appendix B files. These CVs do not prove H1 or real-CV H2.


### hashsmash_h2_sim.py

```python
"""Independent synthetic-CV probe of the published r31 completion equations.

This is research code, not a candidate or an organizer experiment. It varies
unused chaining-state words while keeping the published matching tuple fixed.
"""

import random
import statistics
import sys

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
B0 = [
    0x8CE3F805, 0x5C401AED, 0x579E5F7F, 0xBC3116CB,
    0xCA189B3C, 0xEB75F04C, 0x958F0A0E, 0x7760B082,
    0xDCD5027D, 0x32260AD6, 0x7B12B659, 0xEEE66518,
    0xAD7F88DD, 0xF8AD20BB, 0x7AE40FFD, 0x21609249,
]
B1 = [
    0x9ABDEB1B, 0x1F195F41, 0x5A7210C1, 0x55614F13,
    0xA2269DD1, 0xBE888A61, 0x359257D4, 0xADF3737B,
    0x9F0484A6, 0xEB830A58, 0x66ADD94A, 0x9669232D,
    0x45271FA5, 0xB8F69585, 0x428BBCE3, 0x0703B904,
]
B1P = [
    0x9ABDEB1B, 0x1F195F41, 0x5A7210C1, 0x55614F13,
    0xA2269DD1, 0xBE887A67, 0x35B2DFC5, 0xFDE32975,
    0xC70595A6, 0xEB838A5C, 0x66ADD94A, 0x9669232D,
    0x45271FA5, 0xB8F69585, 0x428BBCE3, 0x0703B904,
]


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


def run(n):
    rng = random.Random(0xF1B2024)
    cv0 = compress(IV, B0)[0]
    out,a,e,w = compress(cv0,B1)
    outp,ap,ep,wp = compress(cv0,B1P)
    assert out == outp
    A=lambda i:a[i+4]
    E=lambda i:e[i+4]
    AP=lambda i:ap[i+4]
    EP=lambda i:ep[i+4]
    d16=(wp[16]-w[16])&MASK
    d18=(wp[18]-w[18])&MASK
    x18=(small1(wp[18])-small1(w[18]))&MASK
    da10=(AP(10)-A(10))&MASK
    g16=[(hi<<28)|lo for hi in range(16) for lo in
         (0x031BBFFC,0x064BBFFE,0x09B3BFFD,0x0CE3BFFF)]
    assert len(g16)==64
    assert all((small1((g+d16)&MASK)-small1(g))&MASK==d18 for g in g16)
    good_count=[]
    iterations=[]
    success=0
    proposals=0
    for case in range(n):
        while True:
            proposals += 1
            cv=list(cv0)
            cv[5]=rng.getrandbits(32) # free E_-2: controls W2 and c18
            cv[7]=rng.getrandbits(32) # free E_-4: controls W0 and c16
            Et=lambda i: E(i) if i>=0 else cv[3-i]
            vv=list(B1)
            for t in range(5):
                vv[t]=(E(t)-A(t-4)-Et(t-4)-big1(Et(t-1))
                       -choose(Et(t-1),Et(t-2),Et(t-3))-K[t])&MASK
            c16=(vv[9]+small0(vv[1])+vv[0])&MASK
            c18=(vv[11]+small0(vv[3])+vv[2])&MASK
            good=[]
            for g in g16:
                u=(small1(g)+c18)&MASK
                if (small1((u+d18)&MASK)-small1(u))&MASK==x18:
                    w14=inverse_small1((g-c16)&MASK)
                    good.append((g,w14))
            if good:
                break
        # Check that this synthetic CV actually follows the fixed prefix trail.
        vv2=list(vv)
        for i in range(5,10):
            vv2[i]=B1P[i]
        p0, aa0, ee0, _=compress(cv,vv)
        p1, aa1, ee1, _=compress(cv,vv2)
        assert aa0[8:17]==a[8:17] and ee0[8:17]==e[8:17]
        assert aa1[8:17]==ap[8:17] and ee1[8:17]==ep[8:17]
        good_count.append(len(good))
        b13=(A(9)+E(9)+big1(E(12))+choose(E(12),E(11),E(10))+K[13])&MASK
        k14=(A(10)+E(10)+K[14])&MASK
        k14p=(AP(10)+EP(10)+K[14])&MASK
        m14=E(12)^E(11)
        m14p=EP(12)^EP(11)
        cnt=0
        found=None
        for g,w14 in good:
            if cnt>=65536: break
            r13=rng.getrandbits(32)
            r15=rng.getrandbits(32)
            base=(k14+w14)&MASK
            basep=(k14p+w14)&MASK
            for i in range(1<<18):
                if cnt>=65536: break
                cnt+=1
                x=(r13+i*0x9E3779B9)&MASK
                c=E(11)^(x&m14)
                cp=EP(11)^(x&m14p)
                if (basep+cp-base-c)&MASK!=da10: continue
                sx=big1(x)
                y=(base+sx+c)&MASK
                yp=(basep+sx+cp)&MASK
                x15=(E(11)+big1(y)+choose(y,x,E(12)))&MASK
                if x15!=(EP(11)+big1(yp)+choose(yp,x,EP(12)))&MASK: continue
                for j in range(1<<12):
                    if cnt>=65536: break
                    cnt+=1
                    z=(r15+j*0x9E3779B9)&MASK
                    y16=(E(12)+choose(z,y,x))&MASK
                    if y16!=(EP(12)+choose(z,yp,x)+d16)&MASK: continue
                    e16=(A(12)+y16+big1(z)+K[16]+g)&MASK
                    if choose(e16,z,y)!=choose(e16,z,yp): continue
                    found=((x-b13)&MASK,w14,(z-A(11)-x15-K[15])&MASK)
                    break
                if found: break
            if found: break
        iterations.append(cnt)
        if found:
            success+=1
            vv[13:16]=found
            vv2[13:16]=found
            h0=compress(cv,vv)[0]
            h1=compress(cv,vv2)[0]
            assert h0==h1, (case,h0,h1)
        if (case+1)%max(1,n//10)==0:
            print('progress',case+1,'/',n,'success',success,'proposals',proposals,flush=True)
    print('n',n,'success',success,'rate',success/n,'proposals',proposals,
          'mean_good',statistics.mean(good_count),'max_good',max(good_count),
          'median_iters',statistics.median(iterations),'max_iters',max(iterations),
          'cap_failures',sum(x==65536 for x in iterations))


if __name__=='__main__':
    run(int(sys.argv[1]) if len(sys.argv)>1 else 20)
```


### hashsmash_h2_kpoints.py

```python
"""Independent synthetic-CV H2 probe across selected Appendix-B r31 starts.

The submitted candidate source is read as inert text. All attack equations here
were reimplemented independently for research; this is not an ordinary-collision
generator because the sampled CVs are not tied to first message blocks.
"""

import random
import statistics
import struct
import sys
import json

from hashsmash_h2_sim import (
    B1, B1P, IV, K, MASK, big0, big1, choose, compress,
    inverse_small1, majority, small0, small1,
)

DELTAS = {i: (B1P[i] - B1[i]) & MASK for i in range(5, 10)}
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


def build_start(a, b, W7, W8, W5=B1[5], W6=B1[6]):
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


def synthesize(start, rng):
    A0, E0, AP, EP, W912, W5678 = start
    A, E = dict(A0), dict(E0)
    A[-4] = rng.getrandbits(32)
    for j in range(-4, 0):
        E[j] = rng.getrandbits(32)
    E[0] = (A[0] + A[-4] - big0(A[-1]) - majority(A[-1], A[-2], A[-3])) & MASK
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]
    w = [0] * 16
    for i in range(5):
        w[i] = (E[i] - A[i-4] - E[i-4] - big1(E[i-1])
                - choose(E[i-1], E[i-2], E[i-3]) - K[i]) & MASK
    w[5:9] = W5678
    w[9:13] = W912
    wp = list(w)
    for i, delta in DELTAS.items():
        wp[i] = (wp[i] + delta) & MASK
    # Full step trace verifies the reconstructed synthetic prefix for both lanes.
    _, aa, ee, _ = compress(cv, w)
    _, aap, eep, _ = compress(cv, wp)
    for i in range(1, 13):
        assert aa[i+4] == A[i] and aap[i+4] == AP[i]
    for i in range(5, 13):
        assert ee[i+4] == E[i] and eep[i+4] == EP[i]
    return cv, w, wp


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


### h2_uniform_probe.py

```python
"""Independent synthetic CV/Phase3 audit for one representative per key.

Randomizes both W5 and W6 over their full exact differential sets.
"""
import json
import mmap
import random
import statistics
import struct

from hashsmash_h2_kpoints import build_start, synthesize, good_words, complete
from hashsmash_h2_sim import MASK, compress


def read_points(path):
    raw = open(path, "rb").read()
    assert len(raw) % 192 == 0
    return [(list(row[:24]), list(row[24:]))
            for row in struct.iter_unpack("<48I", raw)]


def main():
    seed = 0xE5E8011
    rng = random.Random(seed)
    points = read_points('/tmp/r31_variant/recombined_0_400.bin')
    selected = []
    with open('/tmp/r31_variant/first_key_sample_0_400.bin', 'rb') as f:
        while raw := f.read(16 * 65536):
            for key, point, w7, w8 in struct.iter_unpack('<IIII', raw):
                selected.append((key, point, w7, w8))
    ids = rng.sample(selected, 2000)
    with open('/tmp/r31_v5.bin', 'rb') as f5, open('/tmp/r31_v6.bin', 'rb') as f6:
        mm5 = mmap.mmap(f5.fileno(), 0, access=mmap.ACCESS_READ)
        mm6 = mmap.mmap(f6.fileno(), 0, access=mmap.ACCESS_READ)
        n5, n6 = len(mm5) // 4, len(mm6) // 4
        assert n5 == 2**14 and n6 == 2**23
        total = success = proposals = 0
        useds = []
        failures = []
        for key, point, w7, w8 in ids:
            a, b = points[point]
            assert a[:4] == b[:4]
            w5 = struct.unpack_from('<I', mm5, 4*rng.randrange(n5))[0]
            w6 = struct.unpack_from('<I', mm6, 4*rng.randrange(n6))[0]
            st = build_start(a, b, w7, w8, w5, w6)
            assert st is not None and st[0][-1] == key
            while True:
                proposals += 1
                cv, w, wp = synthesize(st, rng)
                good = good_words(w)
                if good:
                    break
            found, used = complete(st, good, rng)
            useds.append(used)
            total += 1
            if found:
                w[13:16] = found
                wp[13:16] = found
                digest_a, _, _, wa = compress(cv, w)
                digest_b, _, _, wb = compress(cv, wp)
                assert digest_a == digest_b
                assert (wb[16]-wa[16]) & MASK == 0x8004
                assert (wb[18]-wa[18]) & MASK == 0xffff7ffc
                assert all(wa[i] == wb[i] for i in range(20,31))
                success += 1
            else:
                failures.append((point, used))
            if total % 100 == 0:
                print('points', total, 'success', success, 'proposals', proposals, flush=True)
    result = {
        'seed': seed,
        'design': 'uniform sample of hash-filtered globally first tuples per key; one random W5 in full V5 and W6 in full V6, synthetic CV conditioned on c18 in S',
        'selected_key_rows': ids,
        'total': total,
        'success': success,
        'proposals': proposals,
        'median_phase3_iterations': statistics.median(useds),
        'max_phase3_iterations': max(useds),
        'failures': failures,
    }
    with open('/tmp/r31_variant/h2_uniform_selfcontained.json', 'w') as f:
        json.dump(result, f, indent=2)
    print('FINAL', {k:v for k,v in result.items() if k not in ('selected_key_rows','failures')}, flush=True)


if __name__ == '__main__':
    main()
```


### hashsmash_recombine_audit.py

```python
"""Independent full-compression/Phase3 audit of E5..8-recombined K400 points."""
import collections,json,random,statistics,struct,sys
from hashsmash_h2_sim import B1,K,MASK,big0,big1,choose,majority,small0,compress
from hashsmash_h2_kpoints import build_start,synthesize,good_words,complete
from hashsmash_neutral_scan import A_PAT,E_PAT,pattern_ok

def read_points(path):
 raw=open(path,'rb').read()
 assert len(raw)%192==0
 return [(list(a[:24]),list(a[24:])) for a in struct.iter_unpack('<48I',raw)]
def validate(a,b):
 assert all(a[i]==b[i] for i in range(4))
 assert all(pattern_ok(a[i-1],b[i-1],A_PAT[i]) for i in range(5,13))
 assert all(pattern_ok(a[i+7],b[i+7],E_PAT[i]) for i in range(5,13))
 assert b[20]-a[20] & MASK==0x8004
 assert a[21:24]==b[21:24]
 assert (small0(b[20])-small0(a[20]))&MASK==(-0x28011100)&MASK
 A=lambda i:a[i-1];AP=lambda i:b[i-1];E=lambda i:a[i+7];EP=lambda i:b[i+7]
 de13=(EP(9)-E(9)+big1(EP(12))-big1(E(12))+choose(EP(12),EP(11),EP(10))-choose(E(12),E(11),E(10)))&MASK
 da13=(de13+big0(AP(12))-big0(A(12))+majority(AP(12),AP(11),AP(10))-majority(A(12),A(11),A(10)))&MASK
 assert de13==0 and da13==0
 # Full A-E recurrence at rounds 5..12, both lanes.
 for q in [a,b]:
  for t in range(5,13):
   lhs=(q[t-1]-q[t+7])&MASK
   rhs=(big0(q[t-2])+majority(q[t-2],q[t-3],q[t-4])-q[t-5])&MASK
   assert lhs==rhs,(t,lhs,rhs)

def run(tag,point_path,tuple_path,perpoint=5,limit_points=None):
 rng=random.Random(0xE5E8000+len(tag));points=read_points(point_path)
 selected={};seen=collections.Counter()
 with open(tuple_path,'rb') as f:
  while raw:=f.read(16*65536):
   for key,point,w7,w8 in struct.iter_unpack('<IIII',raw):
    seen[point]+=1
    if rng.randrange(seen[point])==0:selected[point]=(key,w7,w8)
 ids=sorted(selected)
 if limit_points is not None:ids=rng.sample(ids,min(limit_points,len(ids)))
 valid=success=total=proposals=0;useds=[];non_signed=0;failures=[]
 w8pat='=u=nn==========u===u===u==1====='
 for point in ids:
  a,b=points[point];validate(a,b)
  key,w7,w8=selected[point]
  st=build_start(a,b,w7,w8)
  assert st and st[0][-1]==key,(point,key,w7,w8)
  valid+=1
  # Published signed W8 row is optional for modular collision.
  if not pattern_ok(w8,(w8+0x28011100)&MASK,w8pat):non_signed+=1
  for case in range(perpoint):
   while True:
    proposals+=1
    cv,w,wp=synthesize(st,rng) # checks full prefix in both lanes
    good=good_words(w)
    if good:break
   found,used=complete(st,good,rng);useds.append(used);total+=1
   if found:
    w[13:16]=found;wp[13:16]=found
    _,_,_,wa=compress(cv,w)
    _,_,_,wb=compress(cv,wp)
    assert (wb[16]-wa[16])&MASK==0x8004
    assert (wb[18]-wa[18])&MASK==0xffff7ffc
    assert all(wa[i]==wb[i] for i in range(20,31))
    assert compress(cv,w)[0]==compress(cv,wp)[0]
    success+=1
   else:failures.append((point,case,used))
  if valid%100==0:print(tag,'points',valid,'success',success,'/',total,flush=True)
 out={'tag':tag,'point_file':point_path,'tuple_file':tuple_path,'point_count':len(points),
      'represented_points':len(selected),'selected_point_ids':ids,'valid_points':valid,
      'non_signed_W8_points':non_signed,'cases_per_point':perpoint,'successes':success,'total':total,
      'proposals':proposals,'median_phase3_iterations':statistics.median(useds),
      'max_phase3_iterations':max(useds),'failures':failures}
 with open('/tmp/hashsmash_recombine_audit_'+tag+'.json','w') as f:json.dump(out,f,indent=2)
 print('FINAL',{k:v for k,v in out.items() if k not in ['selected_point_ids','failures']},flush=True)

if __name__=='__main__':
 run('sp000_64','/tmp/r31_variant/recombined_e_full.bin',
     '/tmp/r31_variant/recombined_e_full_tuples.bin',perpoint=10)
 run('all400_sample','/tmp/r31_variant/recombined_0_400.bin',
     '/tmp/r31_variant/first_key_sample_0_400.bin',perpoint=5,limit_points=1000)
```


### h2_first8_uniform_union.py

```python
"""Exact synthetic-U|prefix sampler for first-eight tuples on 1/4096 sampled keys.

This does not sample reachable fixed-IV chaining values. For each sampled key,
the eight-slot mixture and 1/multiplicity rejection make (key,x,y) uniform over
the union of that key's retained tuple regions. Free CV words are uniform and
screened through the actual first-matching tuple's c18 condition.
"""
import collections
import hashlib
import json
import mmap
import random
import statistics
import struct

from hashsmash_h2_kpoints import build_start, synthesize, good_words, complete
from hashsmash_h2_sim import MASK, compress
from hashsmash_recombine_audit import read_points


def contains_u32(mm, x):
    lo, hi = 0, len(mm) // 4
    while lo < hi:
        mid = (lo + hi) // 2
        v = struct.unpack_from('<I', mm, mid * 4)[0]
        if v < x:
            lo = mid + 1
        else:
            hi = mid
    return lo < len(mm) // 4 and struct.unpack_from('<I', mm, lo * 4)[0] == x


def group_records(path):
    raw = open(path, 'rb').read()
    groups = []
    current_key = None
    for key, c6, point, w7, w8 in struct.iter_unpack('<IIIII', raw):
        if key != current_key:
            groups.append([])
            current_key = key
        if len(groups[-1]) < 8:
            groups[-1].append((key, c6, point, w7, w8))
    assert len(groups) == 48094
    return groups, hashlib.sha256(raw).hexdigest()


def matching_first(group, x, y, points, mm6, set5):
    accepted = []
    for i, (key, c6, point, w7, w8) in enumerate(group):
        w6 = (c6 - x) & MASK
        if not contains_u32(mm6, w6):
            continue
        a, b = points[point]
        st0 = build_start(a, b, w7, w8, W5=0, W6=w6)
        assert st0 is not None and st0[0][-1] == key and st0[0][-2] == x
        w5 = (st0[0][-3] - y) & MASK
        if w5 in set5:
            accepted.append((i, w5, w6))
    return accepted


def main():
    seed = 0xF041F0A
    rng = random.Random(seed)
    groups, sample_sha256 = group_records('/tmp/r31_sample_items.bin')
    points = read_points('/tmp/r31_variant/recombined_0_400.bin')
    base_points = read_points('/tmp/r31_points.bin')
    def signature(point):
        a, b = point
        return tuple(a[4:12] + a[16:20] + b[4:12] + b[16:20])
    source_lookup = {signature(point): i for i, point in enumerate(base_points)}
    assert len(source_lookup) == 400
    origin_by_point = [source_lookup[signature(point)] for point in points]
    with open('/tmp/r31_v5.bin', 'rb') as f:
        v5 = [v[0] for v in struct.iter_unpack('<I', f.read())]
    set5 = set(v5)
    assert len(set5) == 1 << 14
    with open('/tmp/r31_v6.bin', 'rb') as f6:
        mm6 = mmap.mmap(f6.fileno(), 0, access=mmap.ACCESS_READ)
        assert len(mm6) // 4 == 1 << 23
        draws = 0
        accepted = 0
        proposals = 0
        good = 0
        results = []
        selected_index = collections.Counter()
        target_index = collections.Counter()
        source_origins = set()
        generated_points = set()
        multiplicities = collections.Counter()
        while accepted < 1000:
            draws += 1
            group = rng.choice(groups)
            target = rng.randrange(8)
            if target >= len(group):
                continue
            key, _, point, w7, w8 = group[target]
            a, b = points[point]
            w5 = rng.choice(v5)
            w6 = struct.unpack_from('<I', mm6, 4 * rng.randrange(1 << 23))[0]
            target_start = build_start(a, b, w7, w8, W5=w5, W6=w6)
            assert target_start is not None and target_start[0][-1] == key
            x, y = target_start[0][-2], target_start[0][-3]
            matches = matching_first(group, x, y, points, mm6, set5)
            assert any(i == target for i, _, _ in matches)
            multiplicity = len(matches)
            if rng.randrange(multiplicity) != 0:
                continue
            selected, w5s, w6s = matches[0]
            skey, _, spoint, sw7, sw8 = group[selected]
            assert skey == key
            sa, sb = points[spoint]
            start = build_start(sa, sb, sw7, sw8, W5=w5s, W6=w6s)
            assert start is not None and (start[0][-1], start[0][-2], start[0][-3]) == (key, x, y)
            while True:
                proposals += 1
                cv, w, wp = synthesize(start, rng)
                c18_good = good_words(w)
                if c18_good:
                    break
            found, used = complete(start, c18_good, rng)
            accepted += 1
            target_index[target] += 1
            selected_index[selected] += 1
            multiplicities[multiplicity] += 1
            generated_points.add(spoint)
            source_origins.add(origin_by_point[spoint])
            if found is not None:
                w[13:16] = found
                wp[13:16] = found
                digest_a, _, _, wa = compress(cv, w)
                digest_b, _, _, wb = compress(cv, wp)
                assert digest_a == digest_b
                assert ((wb[16] - wa[16]) & MASK) == 0x8004
                assert ((wb[18] - wa[18]) & MASK) == 0xffff7ffc
                assert all(wa[i] == wb[i] for i in range(20, 31))
                good += 1
            results.append((key, point, spoint, target, selected, multiplicity, used, found is not None))
            if accepted % 100 == 0:
                print('accepted', accepted, 'good', good, 'draws', draws, 'proposals', proposals, flush=True)
        mm6.close()
    values = [r[6] for r in results]
    out = {
        'seed': seed,
        'design': 'eight-slot tuple mixture, reject vacant slots and accept with probability 1/multiplicity; exact synthetic uniform union over sampled keys, then uniform free CV and c18 screen for actual first-matching tuple',
        'sample_items_sha256': sample_sha256,
        'sample_keys': len(groups),
        'draws': draws,
        'accepted': accepted,
        'completed': good,
        'c18_proposals': proposals,
        'selected_index': dict(selected_index),
        'target_index': dict(target_index),
        'multiplicities': dict(multiplicities),
        'distinct_generated_points': len(generated_points),
        'distinct_source_origins': len(source_origins),
        'median_phase3_iterations': statistics.median(values),
        'max_phase3_iterations': max(values),
        'cases': results,
    }
    with open('/tmp/hashsmash_first8_uniformunion_h2.json', 'w') as f:
        json.dump(out, f, indent=2)
    print('FINAL', {k: v for k, v in out.items() if k != 'cases'}, flush=True)


if __name__ == '__main__':
    main()
```


### r31_second_sample.c

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t a[24],b[24];} Point;
typedef struct {uint32_t key,c6,point,w7,w8;} Item;
static inline uint32_t ro(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return ro(x,2)^ro(x,13)^ro(x,22);}
static inline uint32_t S1(uint32_t x){return ro(x,6)^ro(x,11)^ro(x,25);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static int comp(const void*aa,const void*bb){const Item*a=aa,*b=bb;return a->key<b->key?-1:a->key>b->key?1:a->point<b->point?-1:a->point>b->point?1:a->w8<b->w8?-1:a->w8>b->w8?1:a->w7<b->w7?-1:a->w7>b->w7?1:0;}
int main(void){
 FILE*f=fopen("/tmp/r31_variant/first_key_sample_0_400.bin","rb");if(!f)return 1;
 uint8_t *sample=calloc(1,1ULL<<29);if(!sample)return 2;uint32_t row[4];size_t ns=0;
 while(fread(row,sizeof(row),1,f)==1){uint32_t k=row[0];sample[k>>3]|=(uint8_t)(1u<<(k&7));ns++;}fclose(f);
 uint32_t v7[512],v8[49408];f=fopen("/tmp/r31_v7.bin","rb");if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_v8.bin","rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_variant/recombined_0_400.bin","rb");if(!f)return 4;
 size_t cap=1000000,n=0;Item*items=malloc(cap*sizeof(Item));if(!items)return 5;
 uint64_t all=0,pass8=0;Point P;time_t start=time(0);
 for(uint32_t p=0;p<64800;p++){
  if(fread(&P,sizeof(P),1,f)!=1)return 6;uint32_t*a=P.a,*b=P.b;
  uint32_t rhs7=b[14]-a[14]-(S1(b[13])-S1(a[13]))-0x4fefb5fa;
  uint32_t rhs6=b[13]-a[13]-(S1(b[12])-S1(a[12]))-0x002087f1;
  uint32_t c4=a[15]-a[3]-S1(a[14])-Ch(a[14],a[13],a[12])-0xd807aa98;
  uint32_t c0=-a[3]+S0(a[2])+Maj(a[2],a[1],a[0]);
  for(int j=0;j<49408;j++){
   uint32_t w8=v8[j],e4=c4-w8;
   if(Ch(b[13],b[12],e4)-Ch(a[13],a[12],e4)!=rhs7)continue;pass8++;
   uint32_t c3=a[14]-a[2]-S1(a[13])-Ch(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4+c0;
   for(int z=0;z<512;z++){
    uint32_t w7=v7[z],e3=c3-w7;
    if(Ch(b[12],e4,e3)-Ch(a[12],e4,e3)!=rhs6)continue;
    uint32_t key=e3-a[2]+S0(a[1])+Maj(a[1],a[0],a0);all++;
    if(!((sample[key>>3]>>(key&7))&1))continue;
    uint32_t d2=a[1]-S0(a[0])-Maj(a[0],a0,key);
    uint32_t c6=a[13]-a[1]-S1(a[12])-Ch(a[12],e4,e3)-0x923f82a4-d2;
    if(n==cap){cap*=2;items=realloc(items,cap*sizeof(Item));if(!items)return 7;}
    items[n++]=(Item){key,c6,p,w7,w8};
   }
  }
  if((p+1)%10000==0)fprintf(stderr,"p=%u all=%llu sampled=%zu elapsed=%ld\n",p+1,(unsigned long long)all,n,time(0)-start);
 }
 fclose(f);fprintf(stderr,"total pass8=%llu all=%llu samplekeys=%zu sampledtuples=%zu\n",(unsigned long long)pass8,(unsigned long long)all,ns,n);
 qsort(items,n,sizeof(Item),comp);
 f=fopen("/tmp/r31_sample_items.bin","wb");if(!f||fwrite(items,sizeof(Item),n,f)!=n)return 11;fclose(f);
 f=fopen("/tmp/r31_v6.bin","rb");if(!f)return 8;uint8_t R[65536]={0},D[65536]={0};uint32_t u;
 for(size_t i=0;i<(1u<<23);i++){if(fread(&u,4,1,f)!=1)return 9;R[u&65535]=1;}fclose(f);
 for(int x=0;x<65536;x++)if(R[x])for(int y=0;y<65536;y++)if(R[y])D[(x-y)&65535]=1;
 uint64_t countkeys=0,twopossible=0,greedy_total=0,rawgroups=0,maxgroup=0;size_t zero_shifts=0;
 for(size_t x=0;x<65536;x++)zero_shifts+=!D[x];
 for(size_t i=0;i<n;){size_t j=i+1;while(j<n&&items[j].key==items[i].key)j++;size_t g=j-i;if(g>maxgroup)maxgroup=g;countkeys++;rawgroups+=g;
  size_t chosen[512],m=0;for(size_t a=i;a<j;a++){
   int okay=1;for(size_t b=0;b<m;b++)if(D[(items[a].c6-items[chosen[b]].c6)&65535]){okay=0;break;}
   if(okay){if(m>=512)return 10;chosen[m++]=a;}
  }
  greedy_total+=m;if(m>=2)twopossible++;
  i=j;
 }
 printf("samplekeys=%zu observedkeys=%llu sampledtuples=%zu maxgroup=%llu zero_low16_deltas=%zu\n",ns,(unsigned long long)countkeys,n,(unsigned long long)maxgroup,zero_shifts);
 printf("low16_greedy_disjoint_regions=%llu secondplus=%llu keys_with_second=%llu average=%.6f\n",(unsigned long long)greedy_total,(unsigned long long)(greedy_total-countkeys),(unsigned long long)twopossible,(double)greedy_total/countkeys);
 free(sample);free(items);return 0;
}
```


The fresh fixed-IV 31-step W6 projection uses the first representative's precomputed C6 for each key, with W6=C6-A_-2 and a V6 bitmap. The C6 map builder produced the same 195,265,888-key bitmap as the independent full enumerator; the 1,000-record validator checked its selected C6 values. The sampler has a reduced-round self-test and draws independent blocks from the OS CSPRNG. One `2^30` run observed 48,810,818 key hits and 95,473 selected-row W6 hits; its log SHA-256 is `d925bd9605aa66af4b5c4dcdd08dbe0bc696a99d231fb5587002b494a5301a46`. OS-random draws are not reproduced bit-for-bit by a later run, and the W5 joint event is not estimated from these data. The preliminary 64-round scratch sampler is excluded.


### r31_w6map_build.c

```c
/* Select the first tuple per key and record its W6 affine constant. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t a[24],b[24];} Point;
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t B0(uint32_t x){return R(x,2)^R(x,13)^R(x,22);}
static inline uint32_t B1(uint32_t x){return R(x,6)^R(x,11)^R(x,25);}
static inline uint32_t C(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t M(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
int main(int argc,char**argv){
 if(argc!=4){fprintf(stderr,"usage: %s point-rows.bin output-c6map.bin output-bitset.bin\n",argv[0]);return 1;}
 FILE*in=fopen(argv[1],"rb");if(!in){perror("points");return 2;}
 fseek(in,0,SEEK_END);long bytes=ftell(in);rewind(in);
 if(bytes<0||bytes%sizeof(Point)){fprintf(stderr,"bad point file size\n");return 2;}
 size_t n=(size_t)bytes/sizeof(Point);
 uint32_t v7[512],v8[49408];FILE*f=fopen("/tmp/r31_v7.bin","rb");
 if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen("/tmp/r31_v8.bin","rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 3;fclose(f);
 uint8_t*bits=calloc(1,1ULL<<29);if(!bits){perror("bitset");return 4;}
 uint32_t*c6map=calloc(1,1ULL<<34);if(!c6map){perror("c6map");return 4;}
 uint64_t keys=0,tuples=0,active=0,e4bad=0,e2bad=0,pass8=0;
 Point p;time_t t0=time(0);
 for(size_t i=0;i<n;i++){
  if(fread(&p,sizeof(p),1,in)!=1)return 5;
  uint32_t *a=p.a,*b=p.b;uint64_t rows=0;
  uint32_t ea=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98;
  uint32_t eb=b[15]-b[3]-B1(b[14])-C(b[14],b[13],b[12])-0xd807aa98;
  if(eb-ea!=0x28011100){e4bad++;continue;}
  uint32_t need7=b[14]-a[14]-(B1(b[13])-B1(a[13]))-0x4fefb5fa;
  uint32_t need6=b[13]-a[13]-(B1(b[12])-B1(a[12]))-0x002087f1;
  for(size_t j=0;j<49408;j++){
   uint32_t e4=ea-v8[j];
   if(C(b[13],b[12],e4)-C(a[13],a[12],e4)!=need7)continue;
   pass8++;
   uint32_t e3base=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
   uint32_t kbase=-a[2]+B0(a[1])+M(a[1],a[0],a0);
   for(size_t k=0;k<512;k++){
    uint32_t e3=e3base-v7[k];
    if(C(b[12],e4,e3)-C(a[12],e4,e3)!=need6)continue;
    uint32_t e2=a[13]-a[1]-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
    uint32_t e2b=b[13]-b[1]-B1(b[12])-C(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2b){e2bad++;continue;}
    uint32_t key=e3+kbase;uint8_t *slot=bits+(key>>3),mask=(uint8_t)(1u<<(key&7));
    if(!(*slot&mask)){
     *slot|=mask;
     uint32_t d2=a[1]-B0(a[0])-M(a[0],a0,key);
     c6map[key]=a[13]-a[1]-B1(a[12])-C(a[12],e4,e3)-0x923f82a4-d2;
     keys++;
    }
    tuples++;rows++;
   }
  }
  if(rows)active++;
  if((i+1)%10000==0||i+1==n)fprintf(stderr,"rows=%zu/%zu active=%llu tuples=%llu keys=%llu elapsed=%lld\n",i+1,n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(long long)(time(0)-t0));
 }
 fclose(in);FILE*out=fopen(argv[2],"wb");if(!out){perror("out c6");return 6;}
 if(fwrite(c6map,4,1ULL<<32,out)!=(1ULL<<32)){perror("write c6");return 7;}
 fclose(out);
 out=fopen(argv[3],"wb");if(!out){perror("out bits");return 6;}
 if(fwrite(bits,1,1ULL<<29,out)!=(1ULL<<29)){perror("write bits");return 7;}
 fclose(out);
 printf("points=%zu active=%llu tuples=%llu unique_keys=%llu pass8=%llu bad_E4=%llu bad_E2=%llu elapsed_s=%lld\n",n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(unsigned long long)pass8,(unsigned long long)e4bad,(unsigned long long)e2bad,(long long)(time(0)-t0));
 free(c6map);free(bits);return 0;
}
```


### r31_w6map_validate.py

```python
"""Check selected C6 constants against independent backward reconstruction."""
import hashlib,mmap,random,struct,sys
sys.path.insert(0,'/tmp')
from hashsmash_h2_kpoints import build_start,MASK
from hashsmash_h2_sim import B1
praw=open('/tmp/r31_variant/recombined_0_400.bin','rb').read()
traw=open('/tmp/r31_variant/first_key_sample_0_400.bin','rb').read()
f=open('/tmp/r31_variant/c6_first_0_400.bin','rb')
mm=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
ids=random.Random(0xC61A11D).sample(range(len(traw)//16),1000)
for idx in ids:
 key,p,w7,w8=struct.unpack_from('<IIII',traw,16*idx)
 row=struct.unpack_from('<48I',praw,192*p)
 s=build_start(list(row[:24]),list(row[24:]),w7,w8)
 assert s and s[0][-1]==key
 c6=(B1[6]+s[0][-2])&MASK
 got=struct.unpack_from('<I',mm,4*key)[0]
 assert got==c6,(idx,key,c6,got)
print('checked',len(ids),'first-key representatives; exact C6 map matches independent backward reconstruction')
mm.close();f.close()
```


### r31_w6_sample.c

```c
/* Fresh fixed-IV first-block key and selected-row W6 probe. */
#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <math.h>
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
static const uint8_t *bits,*v6bits;
static const uint32_t *c6map;
typedef struct {uint64_t target,hits,w6hits,hist[256];int err;} Stat;
static void*worker(void*arg){
 Stat*s=arg;int fd=open("/dev/urandom",O_RDONLY);if(fd<0){s->err=1;return NULL;}
 enum {BATCH=4096};unsigned char buf[BATCH*64];uint64_t remain=s->target;
 while(remain){size_t cnt=remain<BATCH?(size_t)remain:BATCH,want=cnt*64,got=0;
  while(got<want){ssize_t n=read(fd,buf+got,want-got);if(n<=0){s->err=2;close(fd);return NULL;}got+=(size_t)n;}
  for(size_t i=0;i<cnt;i++){
   uint32_t cv[8];compress31(buf+i*64,cv);uint32_t x=cv[0];s->hist[x>>24]++;
   if((bits[x>>3]>>(x&7))&1){
    s->hits++;
    uint32_t w6=c6map[x]-cv[1];
    s->w6hits+=(v6bits[w6>>3]>>(w6&7))&1;
   }
  }
  remain-=cnt;
 }
 close(fd);return NULL;
}
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int main(int argc,char**argv){
 if(argc!=5){fprintf(stderr,"usage: %s bitset.bin c6map.bin samples threads\n",argv[0]);return 1;}
 uint64_t n=strtoull(argv[3],0,0);int nt=atoi(argv[4]);if(!n||nt<1||nt>128)return 2;
 static const unsigned char known[64]={
 0x8c,0xe3,0xf8,0x05,0x5c,0x40,0x1a,0xed,0x57,0x9e,0x5f,0x7f,0xbc,0x31,0x16,0xcb,
 0xca,0x18,0x9b,0x3c,0xeb,0x75,0xf0,0x4c,0x95,0x8f,0x0a,0x0e,0x77,0x60,0xb0,0x82,
 0xdc,0xd5,0x02,0x7d,0x32,0x26,0x0a,0xd6,0x7b,0x12,0xb6,0x59,0xee,0xe6,0x65,0x18,
 0xad,0x7f,0x88,0xdd,0xf8,0xad,0x20,0xbb,0x7a,0xe4,0x0f,0xfd,0x21,0x60,0x92,0x49};
 uint32_t cv[8];compress31(known,cv);
 if(cv[0]!=0xc0a93f38||cv[1]!=0x23b02f67||cv[2]!=0x2f718088){fprintf(stderr,"selftest failed %08x %08x %08x\n",cv[0],cv[1],cv[2]);return 3;}
 int fd=open(argv[1],O_RDONLY);if(fd<0){perror("bitset");return 4;}
 struct stat st;if(fstat(fd,&st)||st.st_size!=(1ULL<<29)){fprintf(stderr,"bad bitset size\n");return 5;}
 bits=mmap(NULL,st.st_size,PROT_READ,MAP_PRIVATE,fd,0);if(bits==MAP_FAILED){perror("mmap");return 6;}
 int cfd=open(argv[2],O_RDONLY);if(cfd<0){perror("c6map");return 4;}
 struct stat cst;if(fstat(cfd,&cst)||cst.st_size!=(1ULL<<34)){fprintf(stderr,"bad c6map size\n");return 5;}
 c6map=mmap(NULL,cst.st_size,PROT_READ,MAP_PRIVATE,cfd,0);if(c6map==MAP_FAILED){perror("mmap c6");return 6;}
 uint8_t*vb=calloc(1,1ULL<<29);if(!vb){perror("v6 bitset");return 6;}
 FILE*vf=fopen("/tmp/r31_v6.bin","rb");if(!vf){perror("v6 input");return 6;}
 for(size_t i=0;i<(1ULL<<23);i++){
  uint32_t x;if(fread(&x,4,1,vf)!=1){fprintf(stderr,"short v6 input\n");return 6;}
  vb[x>>3]|=(uint8_t)(1u<<(x&7));
 }
 fclose(vf);v6bits=vb;
 uint64_t keys=0;for(size_t i=0;i<(1ULL<<29);i+=8){uint64_t x;memcpy(&x,bits+i,8);keys+=__builtin_popcountll(x);}
 pthread_t th[128];Stat stats[128]={0};double t0=now();
 for(int i=0;i<nt;i++){stats[i].target=n/nt+(i<(int)(n%nt));if(pthread_create(&th[i],0,worker,&stats[i]))return 7;}
 for(int i=0;i<nt;i++)pthread_join(th[i],0);
 uint64_t hits=0,w6hits=0,hist[256]={0};for(int i=0;i<nt;i++){
  if(stats[i].err){fprintf(stderr,"thread error %d\n",stats[i].err);return 8;}
  hits+=stats[i].hits;w6hits+=stats[i].w6hits;for(int j=0;j<256;j++)hist[j]+=stats[i].hist[j];
 }
 double p=(double)keys/4294967296.0,expected=n*p,z=((double)hits-expected)/sqrt(expected*(1-p));
 double chi=0,eb=(double)n/256;for(int j=0;j<256;j++){double d=hist[j]-eb;chi+=d*d/eb;}
 printf("samples=%llu threads=%d source=/dev/urandom bytes=%llu selftest=pass wall_s=%.3f\n",(unsigned long long)n,nt,(unsigned long long)(n*64),now()-t0);
 printf("keys=%llu observed_hits=%llu uniform_expected=%.3f ratio=%.8f z=%.5f top8_chisq_255df=%.3f\n",(unsigned long long)keys,(unsigned long long)hits,expected,(double)hits/expected,z,chi);
 double exp6=expected/512.0,z6=((double)w6hits-exp6)/sqrt(exp6*(1-p/512.0));
 printf("v6_size=8388608 observed_w6_hits=%llu uniform_expected_w6=%.3f ratio=%.8f z=%.5f uniform_expected_w5=%.6f\n",(unsigned long long)w6hits,exp6,(double)w6hits/exp6,z6,exp6/262144.0);
 munmap((void*)c6map,cst.st_size);close(cfd);free(vb);munmap((void*)bits,st.st_size);close(fd);return 0;
}
```


The real fixed-IV evidence campaign used 34 independent 2^30-block samples. Its first joint record was `JOINT key=40b02651 point=48107 v8_index=42283 v7_index=377 w6=ec1c56d8 w5=e4238fa0 c18=5fc84526 good=5 cv=40b02651 1c14b514 01438dd2 6bd0f484 26f39996 7230bf6b 7984e25a 85db0290 block=e750a4a10e2a8208b8ef48bf1788c2f5e14897b0f4e5212afb2d98c6c96c8252963fa2685089c3638a509c709f36317d71b6cec37659f16afd64b83a322aa898`. Its logged Phase-3 seed was `834c3c3479eb9fb94002cff0e26f279ecde4b47a7d1f91666cb6dec430f1468f`. The portable completion source reproduces 7,305 iterations and the ninth certificate byte-for-byte when supplied the JOINT log line, generated rows and V7/V8 lists. Fresh OS-random sampling cannot recreate the same first block because raw draws were not retained. This source is validation evidence, not a second table-selection algorithm or rate proof.


### build_first_tuple_map.c

```c
/* Select the first tuple per key and record its point/W8/W7 indices. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t a[24],b[24];} Point;
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t B0(uint32_t x){return R(x,2)^R(x,13)^R(x,22);}
static inline uint32_t B1(uint32_t x){return R(x,6)^R(x,11)^R(x,25);}
static inline uint32_t C(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t M(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
int main(int argc,char**argv){
 if(argc!=6){fprintf(stderr,"usage: %s point-rows.bin output-tuplemap.bin output-bitset.bin v7.bin v8.bin\n",argv[0]);return 1;}
 FILE*in=fopen(argv[1],"rb");if(!in){perror("points");return 2;}
 fseek(in,0,SEEK_END);long bytes=ftell(in);rewind(in);
 if(bytes<0||bytes%sizeof(Point)){fprintf(stderr,"bad point file size\n");return 2;}
 size_t n=(size_t)bytes/sizeof(Point);
 uint32_t v7[512],v8[49408];FILE*f=fopen(argv[4],"rb");
 if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen(argv[5],"rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 3;fclose(f);
 uint8_t*bits=calloc(1,1ULL<<29);if(!bits){perror("bitset");return 4;}
 uint64_t*tuplemap=calloc(1,1ULL<<35);if(!tuplemap){perror("tuplemap");return 4;}
 uint64_t keys=0,tuples=0,active=0,e4bad=0,e2bad=0,pass8=0;
 Point p;time_t t0=time(0);
 for(size_t i=0;i<n;i++){
  if(fread(&p,sizeof(p),1,in)!=1)return 5;
  uint32_t *a=p.a,*b=p.b;uint64_t rows=0;
  uint32_t ea=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98;
  uint32_t eb=b[15]-b[3]-B1(b[14])-C(b[14],b[13],b[12])-0xd807aa98;
  if(eb-ea!=0x28011100){e4bad++;continue;}
  uint32_t need7=b[14]-a[14]-(B1(b[13])-B1(a[13]))-0x4fefb5fa;
  uint32_t need6=b[13]-a[13]-(B1(b[12])-B1(a[12]))-0x002087f1;
  for(size_t j=0;j<49408;j++){
   uint32_t e4=ea-v8[j];
   if(C(b[13],b[12],e4)-C(a[13],a[12],e4)!=need7)continue;
   pass8++;
   uint32_t e3base=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
   uint32_t kbase=-a[2]+B0(a[1])+M(a[1],a[0],a0);
   for(size_t k=0;k<512;k++){
    uint32_t e3=e3base-v7[k];
    if(C(b[12],e4,e3)-C(a[12],e4,e3)!=need6)continue;
    uint32_t e2=a[13]-a[1]-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
    uint32_t e2b=b[13]-b[1]-B1(b[12])-C(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2b){e2bad++;continue;}
    uint32_t key=e3+kbase;uint8_t *slot=bits+(key>>3),mask=(uint8_t)(1u<<(key&7));
    if(!(*slot&mask)){
     *slot|=mask;
     tuplemap[key]=((uint64_t)i<<25)|((uint64_t)j<<9)|k;
     keys++;
    }
    tuples++;rows++;
   }
  }
  if(rows)active++;
  if((i+1)%10000==0||i+1==n)fprintf(stderr,"rows=%zu/%zu active=%llu tuples=%llu keys=%llu elapsed=%lld\n",i+1,n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(long long)(time(0)-t0));
 }
 fclose(in);FILE*out=fopen(argv[2],"wb");if(!out){perror("out tuple");return 6;}
 if(fwrite(tuplemap,8,1ULL<<32,out)!=(1ULL<<32)){perror("write tuple");return 7;}
 fclose(out);
 out=fopen(argv[3],"wb");if(!out){perror("out bits");return 6;}
 if(fwrite(bits,1,1ULL<<29,out)!=(1ULL<<29)){perror("write bits");return 7;}
 fclose(out);
 printf("points=%zu active=%llu tuples=%llu unique_keys=%llu pass8=%llu bad_E4=%llu bad_E2=%llu elapsed_s=%lld\n",n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(unsigned long long)pass8,(unsigned long long)e4bad,(unsigned long long)e2bad,(long long)(time(0)-t0));
 free(tuplemap);free(bits);return 0;
}
```


### build_c6map.c

```c
/* Select the first tuple per key and record its W6 affine constant. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t a[24],b[24];} Point;
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t B0(uint32_t x){return R(x,2)^R(x,13)^R(x,22);}
static inline uint32_t B1(uint32_t x){return R(x,6)^R(x,11)^R(x,25);}
static inline uint32_t C(uint32_t x,uint32_t y,uint32_t z){return z^(x&(y^z));}
static inline uint32_t M(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
int main(int argc,char**argv){
 if(argc!=6){fprintf(stderr,"usage: %s point-rows.bin output-c6map.bin output-bitset.bin v7.bin v8.bin\n",argv[0]);return 1;}
 FILE*in=fopen(argv[1],"rb");if(!in){perror("points");return 2;}
 fseek(in,0,SEEK_END);long bytes=ftell(in);rewind(in);
 if(bytes<0||bytes%sizeof(Point)){fprintf(stderr,"bad point file size\n");return 2;}
 size_t n=(size_t)bytes/sizeof(Point);
 uint32_t v7[512],v8[49408];FILE*f=fopen(argv[4],"rb");
 if(!f||fread(v7,sizeof(v7),1,f)!=1)return 3;fclose(f);
 f=fopen(argv[5],"rb");if(!f||fread(v8,sizeof(v8),1,f)!=1)return 3;fclose(f);
 uint8_t*bits=calloc(1,1ULL<<29);if(!bits){perror("bitset");return 4;}
 uint32_t*c6map=calloc(1,1ULL<<34);if(!c6map){perror("c6map");return 4;}
 uint64_t keys=0,tuples=0,active=0,e4bad=0,e2bad=0,pass8=0;
 Point p;time_t t0=time(0);
 for(size_t i=0;i<n;i++){
  if(fread(&p,sizeof(p),1,in)!=1)return 5;
  uint32_t *a=p.a,*b=p.b;uint64_t rows=0;
  uint32_t ea=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98;
  uint32_t eb=b[15]-b[3]-B1(b[14])-C(b[14],b[13],b[12])-0xd807aa98;
  if(eb-ea!=0x28011100){e4bad++;continue;}
  uint32_t need7=b[14]-a[14]-(B1(b[13])-B1(a[13]))-0x4fefb5fa;
  uint32_t need6=b[13]-a[13]-(B1(b[12])-B1(a[12]))-0x002087f1;
  for(size_t j=0;j<49408;j++){
   uint32_t e4=ea-v8[j];
   if(C(b[13],b[12],e4)-C(a[13],a[12],e4)!=need7)continue;
   pass8++;
   uint32_t e3base=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5;
   uint32_t a0=e4-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
   uint32_t kbase=-a[2]+B0(a[1])+M(a[1],a[0],a0);
   for(size_t k=0;k<512;k++){
    uint32_t e3=e3base-v7[k];
    if(C(b[12],e4,e3)-C(a[12],e4,e3)!=need6)continue;
    uint32_t e2=a[13]-a[1]-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
    uint32_t e2b=b[13]-b[1]-B1(b[12])-C(b[12],e4,e3)-0x923f82a4-0x002087f1;
    if(e2!=e2b){e2bad++;continue;}
    uint32_t key=e3+kbase;uint8_t *slot=bits+(key>>3),mask=(uint8_t)(1u<<(key&7));
    if(!(*slot&mask)){
     *slot|=mask;
     uint32_t d2=a[1]-B0(a[0])-M(a[0],a0,key);
     c6map[key]=a[13]-a[1]-B1(a[12])-C(a[12],e4,e3)-0x923f82a4-d2;
     keys++;
    }
    tuples++;rows++;
   }
  }
  if(rows)active++;
  if((i+1)%10000==0||i+1==n)fprintf(stderr,"rows=%zu/%zu active=%llu tuples=%llu keys=%llu elapsed=%lld\n",i+1,n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(long long)(time(0)-t0));
 }
 fclose(in);FILE*out=fopen(argv[2],"wb");if(!out){perror("out c6");return 6;}
 if(fwrite(c6map,4,1ULL<<32,out)!=(1ULL<<32)){perror("write c6");return 7;}
 fclose(out);
 out=fopen(argv[3],"wb");if(!out){perror("out bits");return 6;}
 if(fwrite(bits,1,1ULL<<29,out)!=(1ULL<<29)){perror("write bits");return 7;}
 fclose(out);
 printf("points=%zu active=%llu tuples=%llu unique_keys=%llu pass8=%llu bad_E4=%llu bad_E2=%llu elapsed_s=%lld\n",n,(unsigned long long)active,(unsigned long long)tuples,(unsigned long long)keys,(unsigned long long)pass8,(unsigned long long)e4bad,(unsigned long long)e2bad,(long long)(time(0)-t0));
 free(c6map);free(bits);return 0;
}
```


### sample_first_blocks.c

```c
/* Fresh fixed-IV first-block selected-row W5 projection probe. */
#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <math.h>
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
typedef struct {uint32_t a[24],b[24];} Point;
static const uint8_t *bits,*v6bits;
static const uint32_t *c6map;
static const uint64_t *tuplemap;
static Point *points;
static uint32_t v7[512],v8[49408],v5[16384];
static uint8_t *v5lo16,*v5lo20,*v5lo24;
typedef struct {uint64_t target,hits,w6hits,w5lo16,w5lo20,w5lo24,w5exact,joint,w6mismatch,hist[256];int err;} Stat;
static void*worker(void*arg){
 Stat*s=arg;int fd=open("/dev/urandom",O_RDONLY);if(fd<0){s->err=1;return NULL;}
 enum {BATCH=4096};unsigned char buf[BATCH*64];uint64_t remain=s->target;
 while(remain){size_t cnt=remain<BATCH?(size_t)remain:BATCH,want=cnt*64,got=0;
  while(got<want){ssize_t n=read(fd,buf+got,want-got);if(n<=0){s->err=2;close(fd);return NULL;}got+=(size_t)n;}
  for(size_t i=0;i<cnt;i++){
   uint32_t cv[8];compress31(buf+i*64,cv);uint32_t x=cv[0];s->hist[x>>24]++;
   if((bits[x>>3]>>(x&7))&1){
    s->hits++;
    uint32_t w6=c6map[x]-cv[1];
    if((v6bits[w6>>3]>>(w6&7))&1){
     s->w6hits++;
     uint64_t enc=tuplemap[x];
     uint32_t pi=(uint32_t)(enc>>25),j=(uint32_t)((enc>>9)&65535),k=(uint32_t)(enc&511);
     if(pi>=64800||j>=49408){s->err=9;close(fd);return NULL;}
     uint32_t *a=points[pi].a;
     uint32_t e4=a[15]-a[3]-B1(a[14])-C(a[14],a[13],a[12])-0xd807aa98-v8[j];
     uint32_t e3=a[14]-a[2]-B1(a[13])-C(a[13],a[12],e4)-0xab1c5ed5-v7[k];
     uint32_t a0=e4-a[3]+B0(a[2])+M(a[2],a[1],a[0]);
     uint32_t e2=a[1]+cv[1]-B0(a[0])-M(a[0],a0,x);
     uint32_t w6check=a[13]-a[1]-e2-B1(a[12])-C(a[12],e4,e3)-0x923f82a4;
     if(w6check!=w6)s->w6mismatch++;
     uint32_t e1=a[0]+cv[2]-B0(a0)-M(a0,x,cv[1]);
     uint32_t w5=a[12]-a[0]-e1-B1(e4)-C(e4,e3,e2)-0x59f111f1;
     s->w5lo16+=(v5lo16[(w5&65535)>>3]>>((w5&65535)&7))&1;
     s->w5lo20+=(v5lo20[(w5&1048575)>>3]>>((w5&1048575)&7))&1;
     s->w5lo24+=(v5lo24[(w5&16777215)>>3]>>((w5&16777215)&7))&1;
     size_t lo=0,hi=16384;while(lo<hi){size_t mid=(lo+hi)>>1;if(v5[mid]<w5)lo=mid+1;else hi=mid;}if(lo<16384&&v5[lo]==w5){
      s->w5exact++;
      uint32_t e0=a0+cv[3]-B0(x)-M(x,cv[1],cv[2]);
      uint32_t w2=e2-cv[1]-cv[5]-B1(e1)-C(e1,e0,cv[4])-K[2];
      uint32_t w3=e3-x-cv[4]-B1(e2)-C(e2,e1,e0)-K[3];
      uint32_t c18=a[22]+S0(w3)+w2;
      static const uint32_t glos[4]={0x031bbffc,0x064bbffe,0x09b3bffd,0x0ce3bfff};
      int good=0;for(uint32_t h=0;h<16;h++)for(int l=0;l<4;l++){
       uint32_t g=(h<<28)|glos[l],u=S1(g)+c18;
       good+=(S1(u+0xffff7ffc)-S1(u)==0x2ffe7fe0);
      }
      if(good)s->joint++;
      flockfile(stderr);
      fprintf(stderr,"%s key=%08x point=%u v8_index=%u v7_index=%u w6=%08x w5=%08x c18=%08x good=%d cv=",good?"JOINT":"EXACT",x,pi,j,k,w6,w5,c18,good);
      for(int t=0;t<8;t++)fprintf(stderr,"%08x%s",cv[t],t==7?"":" ");
      fprintf(stderr," block=");for(int t=0;t<64;t++)fprintf(stderr,"%02x",buf[i*64+t]);fprintf(stderr,"\n");
      funlockfile(stderr);
     }
    }
   }
  }
  remain-=cnt;
 }
 close(fd);return NULL;
}
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int main(int argc,char**argv){
 if(argc!=11){fprintf(stderr,"usage: %s keybits.bin c6map.bin tuplemap.bin points.bin v5.bin v6.bin v7.bin v8.bin samples threads\n",argv[0]);return 1;}
 uint64_t n=strtoull(argv[9],0,0);int nt=atoi(argv[10]);if(!n||nt<1||nt>128)return 2;
 static const unsigned char known[64]={
 0x8c,0xe3,0xf8,0x05,0x5c,0x40,0x1a,0xed,0x57,0x9e,0x5f,0x7f,0xbc,0x31,0x16,0xcb,
 0xca,0x18,0x9b,0x3c,0xeb,0x75,0xf0,0x4c,0x95,0x8f,0x0a,0x0e,0x77,0x60,0xb0,0x82,
 0xdc,0xd5,0x02,0x7d,0x32,0x26,0x0a,0xd6,0x7b,0x12,0xb6,0x59,0xee,0xe6,0x65,0x18,
 0xad,0x7f,0x88,0xdd,0xf8,0xad,0x20,0xbb,0x7a,0xe4,0x0f,0xfd,0x21,0x60,0x92,0x49};
 uint32_t cv[8];compress31(known,cv);
 if(cv[0]!=0xc0a93f38||cv[1]!=0x23b02f67||cv[2]!=0x2f718088){fprintf(stderr,"selftest failed %08x %08x %08x\n",cv[0],cv[1],cv[2]);return 3;}
 int fd=open(argv[1],O_RDONLY);if(fd<0){perror("bitset");return 4;}
 struct stat st;if(fstat(fd,&st)||st.st_size!=(1ULL<<29)){fprintf(stderr,"bad bitset size\n");return 5;}
 bits=mmap(NULL,st.st_size,PROT_READ,MAP_PRIVATE,fd,0);if(bits==MAP_FAILED){perror("mmap");return 6;}
 int cfd=open(argv[2],O_RDONLY);if(cfd<0){perror("c6map");return 4;}
 struct stat cst;if(fstat(cfd,&cst)||cst.st_size!=(1ULL<<34)){fprintf(stderr,"bad c6map size\n");return 5;}
 c6map=mmap(NULL,cst.st_size,PROT_READ,MAP_PRIVATE,cfd,0);if(c6map==MAP_FAILED){perror("mmap c6");return 6;}
 int tfd=open(argv[3],O_RDONLY);if(tfd<0){perror("tuplemap");return 4;}
 struct stat tst;if(fstat(tfd,&tst)||tst.st_size!=(1ULL<<35)){fprintf(stderr,"bad tuplemap size\n");return 5;}
 tuplemap=mmap(NULL,tst.st_size,PROT_READ,MAP_PRIVATE,tfd,0);if(tuplemap==MAP_FAILED){perror("mmap tuple");return 6;}
 FILE*pf=fopen(argv[4],"rb");if(!pf){perror("points");return 4;}
 points=malloc(64800*sizeof(Point));if(!points||fread(points,sizeof(Point),64800,pf)!=64800){fprintf(stderr,"points read failed\n");return 5;}fclose(pf);
 FILE*vf5=fopen(argv[5],"rb");if(!vf5||fread(v5,4,16384,vf5)!=16384)return 5;fclose(vf5);
 FILE*vf7=fopen(argv[7],"rb");if(!vf7||fread(v7,4,512,vf7)!=512)return 5;fclose(vf7);
 FILE*vf8=fopen(argv[8],"rb");if(!vf8||fread(v8,4,49408,vf8)!=49408)return 5;fclose(vf8);
 v5lo16=calloc(1,1ULL<<13);v5lo20=calloc(1,1ULL<<17);v5lo24=calloc(1,1ULL<<21);
 if(!v5lo16||!v5lo20||!v5lo24)return 6;
 for(size_t i=0;i<16384;i++){uint32_t w=v5[i],k=w&65535;v5lo16[k>>3]|=1u<<(k&7);k=w&1048575;v5lo20[k>>3]|=1u<<(k&7);k=w&16777215;v5lo24[k>>3]|=1u<<(k&7);}
 uint8_t*vb=calloc(1,1ULL<<29);if(!vb){perror("v6 bitset");return 6;}
 FILE*vf=fopen(argv[6],"rb");if(!vf){perror("v6 input");return 6;}
 for(size_t i=0;i<(1ULL<<23);i++){
  uint32_t x;if(fread(&x,4,1,vf)!=1){fprintf(stderr,"short v6 input\n");return 6;}
  vb[x>>3]|=(uint8_t)(1u<<(x&7));
 }
 fclose(vf);v6bits=vb;
 uint64_t keys=0;for(size_t i=0;i<(1ULL<<29);i+=8){uint64_t x;memcpy(&x,bits+i,8);keys+=__builtin_popcountll(x);}
 pthread_t th[128];Stat stats[128]={0};double t0=now();
 for(int i=0;i<nt;i++){stats[i].target=n/nt+(i<(int)(n%nt));if(pthread_create(&th[i],0,worker,&stats[i]))return 7;}
 for(int i=0;i<nt;i++)pthread_join(th[i],0);
 uint64_t hits=0,w6hits=0,w5lo16=0,w5lo20=0,w5lo24=0,w5exact=0,joint=0,w6mismatch=0,hist[256]={0};for(int i=0;i<nt;i++){
  if(stats[i].err){fprintf(stderr,"thread error %d\n",stats[i].err);return 8;}
  hits+=stats[i].hits;w6hits+=stats[i].w6hits;w5lo16+=stats[i].w5lo16;w5lo20+=stats[i].w5lo20;w5lo24+=stats[i].w5lo24;w5exact+=stats[i].w5exact;joint+=stats[i].joint;w6mismatch+=stats[i].w6mismatch;for(int j=0;j<256;j++)hist[j]+=stats[i].hist[j];
 }
 double p=(double)keys/4294967296.0,expected=n*p,z=((double)hits-expected)/sqrt(expected*(1-p));
 double chi=0,eb=(double)n/256;for(int j=0;j<256;j++){double d=hist[j]-eb;chi+=d*d/eb;}
 printf("samples=%llu threads=%d source=/dev/urandom bytes=%llu selftest=pass wall_s=%.3f\n",(unsigned long long)n,nt,(unsigned long long)(n*64),now()-t0);
 printf("keys=%llu observed_hits=%llu uniform_expected=%.3f ratio=%.8f z=%.5f top8_chisq_255df=%.3f\n",(unsigned long long)keys,(unsigned long long)hits,expected,(double)hits/expected,z,chi);
 double exp6=expected/512.0,z6=((double)w6hits-exp6)/sqrt(exp6*(1-p/512.0));
 printf("v6_size=8388608 observed_w6_hits=%llu uniform_expected_w6=%.3f ratio=%.8f z=%.5f uniform_expected_w5=%.6f\n",(unsigned long long)w6hits,exp6,(double)w6hits/exp6,z6,exp6/262144.0);
 printf("w5_after_w6 low16=%llu expected=%.3f low20=%llu expected=%.3f low24=%llu expected=%.3f exact=%llu expected=%.6f joint=%llu expected_joint=%.6f w6_reconstruction_mismatch=%llu\n",(unsigned long long)w5lo16,exp6/128.0,(unsigned long long)w5lo20,exp6/256.0,(unsigned long long)w5lo24,exp6/1024.0,(unsigned long long)w5exact,exp6/262144.0,(unsigned long long)joint,exp6/262144.0*584683520.0/4294967296.0,(unsigned long long)w6mismatch);
 munmap((void*)tuplemap,tst.st_size);close(tfd);free(points);free(v5lo16);free(v5lo20);free(v5lo24);
 munmap((void*)c6map,cst.st_size);close(cfd);free(vb);munmap((void*)bits,st.st_size);close(fd);return 0;
}
```


### complete_real_prefix.py

```python
"""Complete a logged real fixed-IV 31-step SHA-256 prefix; check with organizer verifier.

Run from the HashSmash repository root:
  PYTHONPATH=. python3 complete_real_prefix.py JOINT.log points.bin v7.bin v8.bin result.json [seed_hex]
A supplied seed reproduces the recorded Python PRNG offsets; otherwise a fresh
256-bit OS seed is used. This is a finite witness/reproduction tool, not an
estimate of the full search success probability.
"""
import hashlib,json,os,random,re,struct,sys
from pathlib import Path
from verifier.hash_functions import SHA256_K, IV as VER_IV, _compress, digest
MASK=0xffffffff
K=list(SHA256_K[:31])
IV=list(VER_IV['sha256'])
DELTAS={5:0xfffff006,6:0x002087f1,7:0x4fefb5fa,8:0x28011100,9:0x00008004}
D16=0x00008004
D18=0xffff7ffc
X18=0x2ffe7fe0
G16=[(hi<<28)|lo for hi in range(16) for lo in (0x031bbffc,0x064bbffe,0x09b3bffd,0x0ce3bfff)]


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

INV_BASIS=[inverse_small1(1<<j) for j in range(32)]


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


def run(log_path,points_path,v7_path,v8_path,result_path,seed_hex=None):
    line=next(s for s in Path(log_path).read_text().splitlines() if s.startswith('JOINT '))
    pattern=r'^JOINT key=([0-9a-f]{8}) point=(\d+) v8_index=(\d+) v7_index=(\d+) w6=([0-9a-f]{8}) w5=([0-9a-f]{8}) c18=([0-9a-f]{8}) good=(\d+) cv=((?:[0-9a-f]{8} ?){8}) block=([0-9a-f]{128})$'
    m=re.match(pattern,line)
    assert m,line
    key=int(m[1],16);pi,j,k=map(int,(m[2],m[3],m[4]));W6=int(m[5],16);W5=int(m[6],16)
    c18=int(m[7],16);good_logged=int(m[8]);cv=tuple(int(s,16) for s in m[9].split());block=bytes.fromhex(m[10])
    points=Path(points_path).read_bytes()
    row=struct.unpack_from('<48I',points,192*pi)
    v7=struct.unpack_from('<I',Path(v7_path).read_bytes(),4*k)[0]
    v8=struct.unpack_from('<I',Path(v8_path).read_bytes(),4*j)[0]
    start=build_start(list(row[:24]),list(row[24:]),v7,v8,W5,W6)
    assert start is not None and start[0][-1]==key
    A,E,AP,EP,W912,W5678=start
    A[-4]=cv[3]
    for t in range(-4,0):E[t]=cv[3-t]
    E[0]=(A[0]+A[-4]-big0(A[-1])-majority(A[-1],A[-2],A[-3]))&MASK
    w=[0]*16
    for t in range(5):
        w[t]=(E[t]-A[t-4]-E[t-4]-big1(E[t-1])-choose(E[t-1],E[t-2],E[t-3])-K[t])&MASK
    w[5:9]=W5678;w[9:13]=W912
    wp=w.copy()
    for t,d in DELTAS.items():wp[t]=(wp[t]+d)&MASK
    assert w[5]==W5 and w[6]==W6
    assert (w[11]+small0(w[3])+w[2])&MASK==c18
    good=good_words(w)
    assert len(good)==good_logged
    assert _compress('sha256',tuple(IV),block,31)==cv
    seed=bytes.fromhex(seed_hex) if seed_hex else os.urandom(32)
    rng=random.Random(int.from_bytes(seed,'big'))
    found,used=complete(start,good,rng)
    result={'key':f'{key:08x}','point_index':pi,'v8_index':j,'v7_index':k,
            'W5':f'{W5:08x}','W6':f'{W6:08x}','c18':f'{c18:08x}',
            'good_g16_count':good_logged,'first_block_hex':block.hex(),
            'first_cv':[f'{x:08x}' for x in cv],'phase3_seed_hex':seed.hex(),
            'phase3_counted_iterations':used,'phase3_success':found is not None}
    if found is not None:
        w[13:16]=found;wp[13:16]=found
        second_a=struct.pack('>16I',*w);second_b=struct.pack('>16I',*wp)
        message_a=block+second_a;message_b=block+second_b
        assert message_a!=message_b and len(message_a)==len(message_b)==128
        assert [t for t in range(16) if w[t]!=wp[t]]==[5,6,7,8,9]
        cv2a=_compress('sha256',cv,second_a,31);cv2b=_compress('sha256',cv,second_b,31)
        assert cv2a==cv2b
        dig_a=digest(message_a,'sha256',31);dig_b=digest(message_b,'sha256',31)
        assert dig_a==dig_b
        result.update({'second_cv':[f'{x:08x}' for x in cv2a],
                       'digest_hex':dig_a.hex(),'message_a_hex':message_a.hex(),
                       'message_b_hex':message_b.hex(),'independent_verifier_digest_equal':True})
    output=Path(result_path);output.write_text(json.dumps(result,indent=2)+'\n')
    print('phase3_success',result['phase3_success'],'iterations',used)
    if found is not None:print('digest',result['digest_hex'])
    print('result_sha256',hashlib.sha256(output.read_bytes()).hexdigest())

if __name__=='__main__':
    if len(sys.argv) not in (6,7):
        raise SystemExit('usage: complete_real_prefix.py JOINT.log points.bin v7.bin v8.bin result.json [seed_hex]')
    run(*sys.argv[1:])
```


## Appendix D. Fresh fixed-IV first-eight distribution probe
The two C source versions below build the same first-eight fixed-order table from Appendix B; v2 adds stop-on-first-joint and full group logging. They assert their raw K/M/tuple counts, self-test the 31-step fixed-IV compression, draw 64-byte first blocks from the OS CSPRNG, and record first-match W6/W5 and c18 marginals. Run, for example, `cc -O3 -std=c11 -pthread r31_first8_real_sampler.c -lm -o r31_first8_real_sampler` and `./r31_first8_real_sampler 1073741824 16`. OS-random blocks make exact sample counts nonrepeatable. The reported all-slot W6 reference is an expected sum, not an independent-binomial variance model. The Python verifier rebuilds each logged exact prefix, recomputes its first-block CV and two-lane 31-step forward traces, and checks c18; run it with `PYTHONPATH=. python3 r31_first8_real_witness_verify.py <sample-progress-log>`. The probe source and observations are validation evidence, not an online table-selection rule.


### r31_first8_real_sampler_v1.c

```c
/* Fixed-IV 31-step first-block sampling against the deterministic first-eight
 * SHA-256-r31 tuple table. Scratch evidence only; not participant code. */
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
 double t0=now();P=malloc(64800*sizeof(Point));
 if(!P||!load_words("/tmp/r31_variant/recombined_0_400.bin",P,64800*sizeof(Point))||
    !load_words("/tmp/r31_v7.bin",v7,sizeof(v7))||!load_words("/tmp/r31_v8.bin",v8,sizeof(v8))||
    !load_words("/tmp/r31_v5.bin",v5,sizeof(v5)))exit(2);
 slot=calloc(1ULL<<32,sizeof(uint32_t));
 G=malloc(200000000ULL*sizeof(Group));if(!slot||!G){perror("table allocation");exit(3);}
 uint64_t tuples=0,pass8=0,reject5=0;
 for(uint32_t p=0;p<64800;p++){
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
    if(!id){if(ng>=200000000ULL){fprintf(stderr,"table capacity\n");exit(4);}
     g=&G[ng];g->key=key;g->n=0;slot[key]=(uint32_t)(++ng);
    }else g=&G[id-1];
    if(g->n<8){g->packed[g->n++]=((uint64_t)p<<25)|((uint64_t)j<<9)|k;nretained++;}
    tuples++;
   }
  }
  if((p+1)%10000==0)fprintf(stderr,"build rows=%u tuples=%llu keys=%zu retained=%llu elapsed=%.1f\n",
   p+1,(unsigned long long)tuples,ng,(unsigned long long)nretained,now()-t0);
 }
 if(tuples!=755416216ULL||ng!=195265888ULL||nretained!=641616343ULL||
    pass8!=409618384ULL||reject5!=0){
  fprintf(stderr,"TABLE COUNT FAILURE: tuples=%llu keys=%zu retained=%llu pass8=%llu reject5=%llu\n",
   (unsigned long long)tuples,ng,(unsigned long long)nretained,(unsigned long long)pass8,(unsigned long long)reject5);exit(5);
 }
 fprintf(stderr,"build verified tuples=%llu keys=%zu retained=%llu pass8=%llu reject5=%llu seconds=%.3f\n",
  (unsigned long long)tuples,ng,(unsigned long long)nretained,(unsigned long long)pass8,(unsigned long long)reject5,now()-t0);
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
 uint64_t target,key_hits,slots_seen,slot_w6[8],slot_w5low16[8],slot_w5low20[8],slot_w5low24[8],slot_exact[8];
 uint64_t any_w6,any_w5low16,any_w5low20,any_w5low24,any_exact,joint,w6_mismatch,key_mismatch;
 uint64_t multiplicity[9],hist[256];int err;
} Stat;
static void*worker(void*arg){
 Stat*s=arg;int fd=open("/dev/urandom",O_RDONLY);if(fd<0){s->err=1;return NULL;}
 enum{BATCH=4096};unsigned char buf[BATCH*64];uint64_t remain=s->target;
 while(remain){size_t count=remain<BATCH?(size_t)remain:BATCH,want=count*64,got=0;
  while(got<want){ssize_t r=read(fd,buf+got,want-got);if(r<=0){s->err=2;close(fd);return NULL;}got+=(size_t)r;}
  for(size_t ix=0;ix<count;ix++){
   uint32_t cv[8];compress31(buf+ix*64,cv);uint32_t key=cv[0];s->hist[key>>24]++;
   uint32_t id=slot[key];if(!id)continue;
   s->key_hits++;const Group*g=&G[id-1];if(g->key!=key){s->key_mismatch++;continue;}
   s->slots_seen+=g->n;s->multiplicity[g->n]++;
   int flag6=0,flag16=0,flag20=0,flag24=0,flag_exact=0;
   for(uint32_t z=0;z<g->n;z++){
    uint64_t pack=g->packed[z];uint32_t p=(uint32_t)(pack>>25),j=(uint32_t)((pack>>9)&65535),k=(uint32_t)(pack&511);
    if(p>=64800||j>=49408||k>=512){s->err=3;close(fd);return NULL;}
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
     fprintf(stderr,"%s slot=%u key=%08x point=%u v8_index=%u v7_index=%u w6=%08x w5=%08x c18=%08x cv=",
      good?"JOINT":"EXACT",z,key,p,j,k,w6,w5,c18);
     for(int q=0;q<8;q++)fprintf(stderr,"%08x%s",cv[q],q==7?"":" ");
     fprintf(stderr," block=");for(int q=0;q<64;q++)fprintf(stderr,"%02x",buf[ix*64+q]);
     fprintf(stderr,"\n");funlockfile(stderr);
    }
   }
   s->any_w6+=flag6;s->any_w5low16+=flag16;s->any_w5low20+=flag20;s->any_w5low24+=flag24;s->any_exact+=flag_exact;
  }remain-=count;
 }
 close(fd);return NULL;
}
int main(int argc,char**argv){
 if(argc!=3){fprintf(stderr,"usage: %s samples threads\n",argv[0]);return 1;}
 uint64_t n=strtoull(argv[1],0,0);int nt=atoi(argv[2]);if(!n||nt<1||nt>128)return 1;
 static const unsigned char known[64]={
 0x8c,0xe3,0xf8,0x05,0x5c,0x40,0x1a,0xed,0x57,0x9e,0x5f,0x7f,0xbc,0x31,0x16,0xcb,
 0xca,0x18,0x9b,0x3c,0xeb,0x75,0xf0,0x4c,0x95,0x8f,0x0a,0x0e,0x77,0x60,0xb0,0x82,
 0xdc,0xd5,0x02,0x7d,0x32,0x26,0x0a,0xd6,0x7b,0x12,0xb6,0x59,0xee,0xe6,0x65,0x18,
 0xad,0x7f,0x88,0xdd,0xf8,0xad,0x20,0xbb,0x7a,0xe4,0x0f,0xfd,0x21,0x60,0x92,0x49};
 uint32_t cv[8];compress31(known,cv);
 if(cv[0]!=0xc0a93f38||cv[1]!=0x23b02f67||cv[2]!=0x2f718088){fprintf(stderr,"selftest fail\n");return 2;}
 fprintf(stderr,"31-step selftest pass\n");build_table();build_sets();
 pthread_t thread[128];Stat stats[128]={0},sum={0};double t0=now();
 for(int i=0;i<nt;i++){stats[i].target=n/nt+(i<(int)(n%nt));if(pthread_create(&thread[i],0,worker,&stats[i]))return 3;}
 for(int i=0;i<nt;i++)pthread_join(thread[i],0);
 for(int i=0;i<nt;i++){
  Stat*s=&stats[i];if(s->err){fprintf(stderr,"worker error=%d\n",s->err);return 4;}
  sum.key_hits+=s->key_hits;sum.slots_seen+=s->slots_seen;
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
 double p=(double)ng/4294967296.0,expected=(double)n*p;
 double z=((double)sum.key_hits-expected)/sqrt(expected*(1-p));
 double chi=0,eb=(double)n/256;for(int i=0;i<256;i++){double d=sum.hist[i]-eb;chi+=d*d/eb;}
 uint64_t all_w6=0;for(int z=0;z<8;z++)all_w6+=sum.slot_w6[z];
 double expected_slot=(double)n*(double)nretained/4294967296.0/512.0;
 double exp_lower_prefix=(double)n*619404987.209861755/576460752303423488.0;
 double exp_upper_prefix=(double)n*(double)nretained/576460752303423488.0;
 printf("samples=%llu threads=%d urandom_bytes=%llu selftest=pass sample_wall_s=%.3f\n",
  (unsigned long long)n,nt,(unsigned long long)(n*64),now()-t0);
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


### r31_first8_real_sampler.c

```c
/* Fixed-IV 31-step first-block sampling against the deterministic first-eight
 * SHA-256-r31 tuple table. Scratch evidence only; not participant code. */
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
static atomic_int halt_on_joint;

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
 double t0=now();P=malloc(64800*sizeof(Point));
 if(!P||!load_words("/tmp/r31_variant/recombined_0_400.bin",P,64800*sizeof(Point))||
    !load_words("/tmp/r31_v7.bin",v7,sizeof(v7))||!load_words("/tmp/r31_v8.bin",v8,sizeof(v8))||
    !load_words("/tmp/r31_v5.bin",v5,sizeof(v5)))exit(2);
 slot=calloc(1ULL<<32,sizeof(uint32_t));
 G=malloc(200000000ULL*sizeof(Group));if(!slot||!G){perror("table allocation");exit(3);}
 uint64_t tuples=0,pass8=0,reject5=0;
 for(uint32_t p=0;p<64800;p++){
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
    if(!id){if(ng>=200000000ULL){fprintf(stderr,"table capacity\n");exit(4);}
     g=&G[ng];g->key=key;g->n=0;slot[key]=(uint32_t)(++ng);
    }else g=&G[id-1];
    if(g->n<8){g->packed[g->n++]=((uint64_t)p<<25)|((uint64_t)j<<9)|k;nretained++;}
    tuples++;
   }
  }
  if((p+1)%10000==0)fprintf(stderr,"build rows=%u tuples=%llu keys=%zu retained=%llu elapsed=%.1f\n",
   p+1,(unsigned long long)tuples,ng,(unsigned long long)nretained,now()-t0);
 }
 if(tuples!=755416216ULL||ng!=195265888ULL||nretained!=641616343ULL||
    pass8!=409618384ULL||reject5!=0){
  fprintf(stderr,"TABLE COUNT FAILURE: tuples=%llu keys=%zu retained=%llu pass8=%llu reject5=%llu\n",
   (unsigned long long)tuples,ng,(unsigned long long)nretained,(unsigned long long)pass8,(unsigned long long)reject5);exit(5);
 }
 fprintf(stderr,"build verified tuples=%llu keys=%zu retained=%llu pass8=%llu reject5=%llu seconds=%.3f\n",
  (unsigned long long)tuples,ng,(unsigned long long)nretained,(unsigned long long)pass8,(unsigned long long)reject5,now()-t0);
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
 uint64_t target,processed,key_hits,slots_seen,slot_w6[8],slot_w5low16[8],slot_w5low20[8],slot_w5low24[8],slot_exact[8];
 uint64_t any_w6,any_w5low16,any_w5low20,any_w5low24,any_exact,joint,w6_mismatch,key_mismatch;
 uint64_t multiplicity[9],hist[256];int err;
} Stat;
static void*worker(void*arg){
 Stat*s=arg;int fd=open("/dev/urandom",O_RDONLY);if(fd<0){s->err=1;return NULL;}
 enum{BATCH=4096};unsigned char buf[BATCH*64];uint64_t remain=s->target;
 while(remain&&!atomic_load(&halt_on_joint)){size_t count=remain<BATCH?(size_t)remain:BATCH,want=count*64,got=0;
  while(got<want){ssize_t r=read(fd,buf+got,want-got);if(r<=0){s->err=2;close(fd);return NULL;}got+=(size_t)r;}
  for(size_t ix=0;ix<count;ix++){
   uint32_t cv[8];compress31(buf+ix*64,cv);uint32_t key=cv[0];s->hist[key>>24]++;
   uint32_t id=slot[key];if(!id)continue;
   s->key_hits++;const Group*g=&G[id-1];if(g->key!=key){s->key_mismatch++;continue;}
   s->slots_seen+=g->n;s->multiplicity[g->n]++;
   int flag6=0,flag16=0,flag20=0,flag24=0,flag_exact=0;
   for(uint32_t z=0;z<g->n;z++){
    uint64_t pack=g->packed[z];uint32_t p=(uint32_t)(pack>>25),j=(uint32_t)((pack>>9)&65535),k=(uint32_t)(pack&511);
    if(p>=64800||j>=49408||k>=512){s->err=3;close(fd);return NULL;}
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
     if(good)atomic_store(&halt_on_joint,1);
     flockfile(stderr);
     fprintf(stderr,"%s slot=%u key=%08x point=%u v8_index=%u v7_index=%u w6=%08x w5=%08x c18=%08x cv=",
      good?"JOINT":"EXACT",z,key,p,j,k,w6,w5,c18);
     for(int q=0;q<8;q++)fprintf(stderr,"%08x%s",cv[q],q==7?"":" ");
     fprintf(stderr," block=");for(int q=0;q<64;q++)fprintf(stderr,"%02x",buf[ix*64+q]);
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
  }remain-=count;s->processed+=count;
 }
 close(fd);return NULL;
}
int main(int argc,char**argv){
 if(argc!=3){fprintf(stderr,"usage: %s samples threads\n",argv[0]);return 1;}
 uint64_t n=strtoull(argv[1],0,0),requested=n;int nt=atoi(argv[2]);if(!n||nt<1||nt>128)return 1;
 static const unsigned char known[64]={
 0x8c,0xe3,0xf8,0x05,0x5c,0x40,0x1a,0xed,0x57,0x9e,0x5f,0x7f,0xbc,0x31,0x16,0xcb,
 0xca,0x18,0x9b,0x3c,0xeb,0x75,0xf0,0x4c,0x95,0x8f,0x0a,0x0e,0x77,0x60,0xb0,0x82,
 0xdc,0xd5,0x02,0x7d,0x32,0x26,0x0a,0xd6,0x7b,0x12,0xb6,0x59,0xee,0xe6,0x65,0x18,
 0xad,0x7f,0x88,0xdd,0xf8,0xad,0x20,0xbb,0x7a,0xe4,0x0f,0xfd,0x21,0x60,0x92,0x49};
 uint32_t cv[8];compress31(known,cv);
 if(cv[0]!=0xc0a93f38||cv[1]!=0x23b02f67||cv[2]!=0x2f718088){fprintf(stderr,"selftest fail\n");return 2;}
 fprintf(stderr,"31-step selftest pass\n");build_table();build_sets();
 pthread_t thread[128];Stat stats[128]={0},sum={0};double t0=now();
 for(int i=0;i<nt;i++){stats[i].target=n/nt+(i<(int)(n%nt));if(pthread_create(&thread[i],0,worker,&stats[i]))return 3;}
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
 double exp_lower_prefix=(double)n*619404987.209861755/576460752303423488.0;
 double exp_upper_prefix=(double)n*(double)nretained/576460752303423488.0;
 printf("samples=%llu requested=%llu stopped_on_joint=%d threads=%d urandom_bytes=%llu selftest=pass sample_wall_s=%.3f\n",
  (unsigned long long)n,(unsigned long long)requested,atomic_load(&halt_on_joint),nt,
  (unsigned long long)(n*64),now()-t0);
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


### r31_first8_real_witness_verify.py

```python
"""Independent Python forward-trace checks for real first-eight prefix witnesses."""
import re
import struct
import sys
import bisect
from pathlib import Path

from hashsmash_h2_kpoints import build_start, DELTAS
from hashsmash_h2_sim import (
    IV, K, MASK, big0, big1, choose, compress, majority,
)

ROOT = Path("/tmp/r31_variant")
points_bytes = (ROOT / "recombined_0_400.bin").read_bytes()
v7_bytes = Path("/tmp/r31_v7.bin").read_bytes()
v8_bytes = Path("/tmp/r31_v8.bin").read_bytes()
assert len(points_bytes) == 64800 * 48 * 4
assert len(v7_bytes) == 512 * 4
assert len(v8_bytes) == 49408 * 4
v7 = struct.unpack("<512I", v7_bytes)
v8 = struct.unpack("<49408I", v8_bytes)
v5 = struct.unpack("<16384I", Path("/tmp/r31_v5.bin").read_bytes())
v6_bytes = Path("/tmp/r31_v6.bin").read_bytes()
assert len(v6_bytes) == (1 << 23) * 4
assert all(v5[i] < v5[i + 1] for i in range(len(v5) - 1))

def in_v6(value):
    lo, hi = 0, 1 << 23
    while lo < hi:
        mid = (lo + hi) // 2
        if struct.unpack_from("<I", v6_bytes, mid * 4)[0] < value:
            lo = mid + 1
        else:
            hi = mid
    return lo < 1 << 23 and struct.unpack_from("<I", v6_bytes, lo * 4)[0] == value

def in_v5(value):
    i = bisect.bisect_left(v5, value)
    return i < len(v5) and v5[i] == value

rx = re.compile(
    r"^(EXACT|JOINT) slot=(\d+) key=([0-9a-f]{8}) point=(\d+) "
    r"v8_index=(\d+) v7_index=(\d+) w6=([0-9a-f]{8}) "
    r"w5=([0-9a-f]{8}) c18=([0-9a-f]{8}) "
    r"cv=((?:[0-9a-f]{8} ?){8}) block=([0-9a-f]{128})$"
)
group_rx = re.compile(
    r"^GROUP key=([0-9a-f]{8}) selected_slot=(\d+) count=(\d+) "
    r"entries=(\d+:\d+:\d+(?:,\d+:\d+:\d+)*)$"
)

def words(block_hex):
    bb = bytes.fromhex(block_hex)
    assert len(bb) == 64
    return list(struct.unpack(">16I", bb))

def verify(line):
    match = rx.match(line)
    assert match, line
    status, slot, key, pidx, j, k, w6, w5, c18, cv_text, block_hex = match.groups()
    slot, pidx, j, k = map(int, (slot, pidx, j, k))
    key, w6, w5, c18 = [int(v, 16) for v in (key, w6, w5, c18)]
    cv = [int(v, 16) for v in cv_text.split()]
    assert len(cv) == 8
    actual_cv, _, _, _ = compress(IV, words(block_hex))
    assert tuple(cv) == actual_cv
    assert cv[0] == key
    rec = struct.unpack_from("<48I", points_bytes, pidx * 48 * 4)
    a, b = list(rec[:24]), list(rec[24:])
    start = build_start(a, b, v7[k], v8[j], w5, w6)
    assert start is not None
    A, E, AP, EP, W912, W5678 = start
    assert [A[-1], A[-2], A[-3]] == cv[:3]
    assert W5678 == [w5, w6, v7[k], v8[j]]
    A[-4] = cv[3]
    for z in range(-4, 0):
        E[z] = cv[3-z]
    E[0] = (A[0] + A[-4] - big0(A[-1])
            - majority(A[-1], A[-2], A[-3])) & MASK
    w = [0] * 16
    for t in range(5):
        w[t] = (E[t] - A[t - 4] - E[t - 4] - big1(E[t - 1])
                - choose(E[t - 1], E[t - 2], E[t - 3]) - K[t]) & MASK
    w[5:9] = W5678
    w[9:13] = W912
    wp = list(w)
    for t, delta in DELTAS.items():
        wp[t] = (wp[t] + delta) & MASK
    _, aa, ee, _ = compress(cv, w)
    _, aap, eep, _ = compress(cv, wp)
    assert all(aa[t + 4] == A[t] and aap[t + 4] == AP[t] for t in range(1, 13))
    assert all(ee[t + 4] == E[t] and eep[t + 4] == EP[t] for t in range(5, 13))
    from hashsmash_h2_sim import small0, small1
    assert c18 == (w[11] + small0(w[3]) + w[2]) & MASK
    good = any(
        (small1((u + 0xFFFF7FFC) & MASK) - small1(u)) & MASK == 0x2FFE7FE0
        for hi in range(16)
        for lo in (0x031BBFFC, 0x064BBFFE, 0x09B3BFFD, 0x0CE3BFFF)
        for g in [(hi << 28) | lo]
        for u in [(small1(g) + c18) & MASK]
    )
    assert (status == "JOINT") == good
    print(f"PASS slot={slot} key={key:08x} point={pidx} c18={c18:08x} joint={good}")
    return key, slot, cv, pidx, j, k

def verify_group(line, selected):
    match = group_rx.match(line)
    assert match, line
    key_text, slot_text, count_text, entries_text = match.groups()
    key, slot, count = int(key_text, 16), int(slot_text), int(count_text)
    entries = [tuple(map(int, term.split(":"))) for term in entries_text.split(",")]
    assert len(entries) == count and 1 <= count <= 8
    assert key == selected[0] and slot == selected[1]
    cv = selected[2]
    assert entries[slot] == tuple(selected[3:6])
    accepted = []
    for q, (pidx, j, k) in enumerate(entries):
        rec = struct.unpack_from("<48I", points_bytes, pidx * 48 * 4)
        a = rec[:24]
        e4 = (a[15] - a[3] - big1(a[14])
              - choose(a[14], a[13], a[12]) - 0xD807AA98 - v8[j]) & MASK
        e3 = (a[14] - a[2] - big1(a[13])
              - choose(a[13], a[12], e4) - 0xAB1C5ED5 - v7[k]) & MASK
        a0 = (e4 - a[3] + big0(a[2]) + majority(a[2], a[1], a[0])) & MASK
        reconstructed_key = (e3 - a[2] + big0(a[1])
                             + majority(a[1], a[0], a0)) & MASK
        assert reconstructed_key == key
        e2 = (a[1] + cv[1] - big0(a[0])
              - majority(a[0], a0, key)) & MASK
        w6 = (a[13] - a[1] - e2 - big1(a[12])
              - choose(a[12], e4, e3) - 0x923F82A4) & MASK
        if not in_v6(w6):
            accepted.append(False)
            continue
        e1 = (a[0] + cv[2] - big0(a0)
              - majority(a0, key, cv[1])) & MASK
        w5 = (a[12] - a[0] - e1 - big1(e4)
              - choose(e4, e3, e2) - 0x59F111F1) & MASK
        accepted.append(in_v5(w5))
    assert accepted[slot] and not any(accepted[:slot])
    print(f"PASS_GROUP key={key:08x} selected_slot={slot} count={count} first_match=True matches={sum(accepted)}")

count = 0
groups = 0
for filename in sys.argv[1:]:
    selected = None
    for line in Path(filename).read_text().splitlines():
        if line.startswith(("EXACT ", "JOINT ")):
            selected = verify(line)
            count += 1
        elif line.startswith("GROUP "):
            assert selected is not None
            verify_group(line, selected)
            groups += 1
            selected = None
print(f"verified={count} groups={groups}")
```


### complete_real_prefix_slot.py

```python
"""Complete a logged real fixed-IV 31-step SHA-256 prefix; check with organizer verifier.

Run from the HashSmash repository root:
  PYTHONPATH=. python3 complete_real_prefix_slot.py JOINT.log points.bin v7.bin v8.bin result.json [seed_hex]
A supplied seed reproduces the recorded Python PRNG offsets; otherwise a fresh
256-bit OS seed is used. This is a finite witness/reproduction tool, not an
estimate of the full search success probability.
"""
import hashlib,json,os,random,re,struct,sys
from pathlib import Path
from verifier.hash_functions import SHA256_K, IV as VER_IV, _compress, digest
MASK=0xffffffff
K=list(SHA256_K[:31])
IV=list(VER_IV['sha256'])
DELTAS={5:0xfffff006,6:0x002087f1,7:0x4fefb5fa,8:0x28011100,9:0x00008004}
D16=0x00008004
D18=0xffff7ffc
X18=0x2ffe7fe0
G16=[(hi<<28)|lo for hi in range(16) for lo in (0x031bbffc,0x064bbffe,0x09b3bffd,0x0ce3bfff)]


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

INV_BASIS=[inverse_small1(1<<j) for j in range(32)]


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


def run(log_path,points_path,v7_path,v8_path,result_path,seed_hex=None):
    line=next(s for s in Path(log_path).read_text().splitlines() if s.startswith('JOINT '))
    pattern=r'^JOINT(?: slot=(\d+))? key=([0-9a-f]{8}) point=(\d+) v8_index=(\d+) v7_index=(\d+) w6=([0-9a-f]{8}) w5=([0-9a-f]{8}) c18=([0-9a-f]{8}) (?:good=(\d+) )?cv=((?:[0-9a-f]{8} ?){8}) block=([0-9a-f]{128})$'
    m=re.match(pattern,line)
    assert m,line
    slot=int(m[1]) if m[1] is not None else None
    key=int(m[2],16);pi,j,k=map(int,(m[3],m[4],m[5]));W6=int(m[6],16);W5=int(m[7],16)
    c18=int(m[8],16);good_logged=int(m[9]) if m[9] is not None else None
    cv=tuple(int(s,16) for s in m[10].split());block=bytes.fromhex(m[11])
    points=Path(points_path).read_bytes()
    row=struct.unpack_from('<48I',points,192*pi)
    v7=struct.unpack_from('<I',Path(v7_path).read_bytes(),4*k)[0]
    v8=struct.unpack_from('<I',Path(v8_path).read_bytes(),4*j)[0]
    start=build_start(list(row[:24]),list(row[24:]),v7,v8,W5,W6)
    assert start is not None and start[0][-1]==key
    A,E,AP,EP,W912,W5678=start
    A[-4]=cv[3]
    for t in range(-4,0):E[t]=cv[3-t]
    E[0]=(A[0]+A[-4]-big0(A[-1])-majority(A[-1],A[-2],A[-3]))&MASK
    w=[0]*16
    for t in range(5):
        w[t]=(E[t]-A[t-4]-E[t-4]-big1(E[t-1])-choose(E[t-1],E[t-2],E[t-3])-K[t])&MASK
    w[5:9]=W5678;w[9:13]=W912
    wp=w.copy()
    for t,d in DELTAS.items():wp[t]=(wp[t]+d)&MASK
    assert w[5]==W5 and w[6]==W6
    assert (w[11]+small0(w[3])+w[2])&MASK==c18
    good=good_words(w)
    if good_logged is not None: assert len(good)==good_logged
    else: assert good
    assert _compress('sha256',tuple(IV),block,31)==cv
    seed=bytes.fromhex(seed_hex) if seed_hex else os.urandom(32)
    rng=random.Random(int.from_bytes(seed,'big'))
    found,used=complete(start,good,rng)
    result={'key':f'{key:08x}','selected_slot':slot,'point_index':pi,'v8_index':j,'v7_index':k,
            'W5':f'{W5:08x}','W6':f'{W6:08x}','c18':f'{c18:08x}',
            'good_g16_count':len(good),'first_block_hex':block.hex(),
            'first_cv':[f'{x:08x}' for x in cv],'phase3_seed_hex':seed.hex(),
            'phase3_counted_iterations':used,'phase3_success':found is not None}
    if found is not None:
        w[13:16]=found;wp[13:16]=found
        second_a=struct.pack('>16I',*w);second_b=struct.pack('>16I',*wp)
        message_a=block+second_a;message_b=block+second_b
        assert message_a!=message_b and len(message_a)==len(message_b)==128
        assert [t for t in range(16) if w[t]!=wp[t]]==[5,6,7,8,9]
        cv2a=_compress('sha256',cv,second_a,31);cv2b=_compress('sha256',cv,second_b,31)
        assert cv2a==cv2b
        dig_a=digest(message_a,'sha256',31);dig_b=digest(message_b,'sha256',31)
        assert dig_a==dig_b
        result.update({'second_cv':[f'{x:08x}' for x in cv2a],
                       'digest_hex':dig_a.hex(),'message_a_hex':message_a.hex(),
                       'message_b_hex':message_b.hex(),'independent_verifier_digest_equal':True})
    output=Path(result_path);output.write_text(json.dumps(result,indent=2)+'\n')
    print('phase3_success',result['phase3_success'],'iterations',used)
    if found is not None:print('digest',result['digest_hex'])
    print('result_sha256',hashlib.sha256(output.read_bytes()).hexdigest())

if __name__=='__main__':
    if len(sys.argv) not in (6,7):
        raise SystemExit('usage: complete_real_prefix_slot.py JOINT.log points.bin v7.bin v8.bin result.json [seed_hex]')
    run(*sys.argv[1:])
```


The later-slot JOINT was completed with an independent 256-bit Phase-3 seed. Run `PYTHONPATH=. python3 complete_real_prefix_slot.py /tmp/r31_first8_real_sampler_8x2p30.progress /tmp/r31_variant/recombined_0_400.bin /tmp/r31_v7.bin /tmp/r31_v8.bin /tmp/r31_variant/evidence/later_slot_joint_result.json 596699af31dee2be1dc472bfccb7063680ab5ce94dcaf5345820318a586b53df` to reproduce the tenth pair byte-for-byte. The organizer verifier, not the sampler's own verdict, establishes full-message equality.


### Later-slot completion result

```json
{
  "key": "8b6504bf",
  "selected_slot": 3,
  "point_index": 54058,
  "v8_index": 13786,
  "v7_index": 362,
  "W5": "58648729",
  "W6": "f80860bc",
  "c18": "9c793744",
  "good_g16_count": 5,
  "first_block_hex": "5cb6239263375b741224f73781998bab32cc55cdbfec2124e7e6f61b59952a0b7734302c0966fee39f8aa3b199734e0175371bfc64b857fd6e8932d3dbb80cd5",
  "first_cv": [
    "8b6504bf",
    "a058c712",
    "a35cd3cb",
    "0a3cc99a",
    "047c4b65",
    "5eda04fc",
    "b3f4978e",
    "40ecf21d"
  ],
  "phase3_seed_hex": "596699af31dee2be1dc472bfccb7063680ab5ce94dcaf5345820318a586b53df",
  "phase3_counted_iterations": 2052,
  "phase3_success": true,
  "second_cv": [
    "db074f73",
    "ec38c6d8",
    "4d09b8e8",
    "23472722",
    "380907b9",
    "707a15b2",
    "bd4e7cb1",
    "ecae9dca"
  ],
  "digest_hex": "77026a470b6f4c2e73afd4086bb0978599bb38cd41f81448ce0aa4899c2fb101",
  "message_a_hex": "5cb6239263375b741224f73781998bab32cc55cdbfec2124e7e6f61b59952a0b7734302c0966fee39f8aa3b199734e0175371bfc64b857fd6e8932d3dbb80cd511ce74ecb8dae947a461593408a4395887674fa758648729f80860bc8e9557da61591d3de8970bd307f1823838c410a019939bb0b639cee776b7f0f17f044fde",
  "message_b_hex": "5cb6239263375b741224f73781998bab32cc55cdbfec2124e7e6f61b59952a0b7734302c0966fee39f8aa3b199734e0175371bfc64b857fd6e8932d3dbb80cd511ce74ecb8dae947a461593408a4395887674fa75864772ff828e8adde850dd4895a2e3de8978bd707f1823838c410a019939bb0b639cee776b7f0f17f044fde",
  "independent_verifier_digest_equal": true
}
```


### one batch: aggregate output

```text
samples=1073741824 threads=16 urandom_bytes=68719476736 selftest=pass sample_wall_s=27.363
table_keys=195265888 table_retained=641616343 key_hits=48828226 expected_key_hits=48816472.000 key_z=1.72189 top8_chisq_255df=246.550 key_mismatch=0
slots_seen=160442660 all_slot_w6=314567 expected_all_slot_w6=313289.230 z=2.28286 any_w6=161106 w6_mismatch=0
any_w5_low16=2361 any_w5_low20=1164 any_w5_low24=298 any_exact=4 joint_c18=0 uniform_prefix_bounds=[1.153732,1.195104] uniform_joint_lower=0.157060
slot0 w6=96022 w5low16=727 w5low20=349 w5low24=90 exact=0
slot1 w6=74268 w5low16=587 w5low20=291 w5low24=73 exact=0
slot2 w6=42899 w5low16=314 w5low20=157 w5low24=37 exact=1
slot3 w6=38388 w5low16=310 w5low20=145 w5low24=45 exact=2
slot4 w6=18692 w5low16=132 w5low20=65 w5low24=20 exact=0
slot5 w6=17541 w5low16=107 w5low20=58 w5low24=8 exact=0
slot6 w6=13570 w5low16=119 w5low20=51 w5low24=9 exact=1
slot7 w6=13187 w5low16=110 w5low20=60 w5low24=16 exact=0
key_group_hist1=10970123
key_group_hist2=15910928
key_group_hist3=2433513
key_group_hist4=9918874
key_group_hist5=560639
key_group_hist6=2068580
key_group_hist7=264581
key_group_hist8=6700988
```


### one batch: exact-prefix records

```text
EXACT slot=2 key=8e3cabf1 point=45224 v8_index=15237 v7_index=103 w6=d0cd6676 w5=3d988c29 c18=8b2a721b cv=8e3cabf1 31cf31aa 9001107e 1a8b35f2 4dc7ef8e c77f6852 ea9fa9c4 b866f72d block=0689a1130b19d0b3870609016beb7489b2289d96342e20305afd9b28c6a32e020a7b4f7acb0421508d18814fbfc073b18b54ec95b1d4ef065c53d3ef36465c14
EXACT slot=3 key=e87b884c point=51931 v8_index=4273 v7_index=510 w6=910125d2 w5=9dec8c00 c18=eec968bd cv=e87b884c ea985e81 8f85e412 4bd4698f cd17f1d0 0032e4e6 092c30a2 73fdaf46 block=eec71a2f22d1703289eae6ab9bbaff6203b7d1633cfa171acde142fd35cff9b39d9b5874526de6a29769672477d100469e2f11db68fab8e2ee82afdf317a673a
EXACT slot=3 key=47ec4722 point=57281 v8_index=10300 v7_index=27 w6=f2cf301c w5=d96485e0 c18=e290044e cv=47ec4722 64aa4f2d 804b8fa0 6e494854 e8939844 b660fe31 4092624a ed4c4133 block=d72f14599c01372c846ade1435ac1846aac435c233d53ef4e185076ee16016e83bd4a7243771bf841a348c2bf7bbcaae314c4af415438f7f70883ff4ac574d8c
EXACT slot=6 key=80a0ca49 point=61780 v8_index=43739 v7_index=38 w6=46da201e w5=99fc84e0 c18=61ba444c cv=80a0ca49 1eb23472 e14975f9 d45942af b5c1c1fd 5e2899af 2602028d e879f691 block=ee0bd40ae546063179c66e24a4e1d985f59106a36d36bbe357535f16417d9c5408f1d6cf7cd52fa593a14dbbc4923649d9d99b504f2d02017e42f487413b3a15
```


### three batches: aggregate output

```text
samples=3221225472 threads=16 urandom_bytes=206158430208 selftest=pass sample_wall_s=85.123
table_keys=195265888 table_retained=641616343 key_hits=146447722 expected_key_hits=146449416.000 key_z=-0.14328 top8_chisq_255df=251.134 key_mismatch=0
slots_seen=481179546 all_slot_w6=936306 expected_all_slot_w6=939867.690 z=-3.67386 any_w6=479165 w6_mismatch=0
any_w5_low16=7080 any_w5_low20=3509 any_w5_low24=884 any_exact=1 joint_c18=0 uniform_prefix_bounds=[3.461195,3.585311] uniform_joint_lower=0.471180
slot0 w6=284895 w5low16=2248 w5low20=1104 w5low24=272 exact=0
slot1 w6=221100 w5low16=1725 w5low20=860 w5low24=211 exact=1
slot2 w6=127830 w5low16=926 w5low20=430 w5low24=117 exact=0
slot3 w6=114158 w5low16=888 w5low20=452 w5low24=108 exact=0
slot4 w6=56216 w5low16=431 w5low20=225 w5low24=47 exact=0
slot5 w6=52396 w5low16=384 w5low20=197 w5low24=52 exact=0
slot6 w6=40699 w5low16=323 w5low20=151 w5low24=41 exact=0
slot7 w6=39012 w5low16=311 w5low20=141 w5low24=41 exact=0
key_group_hist1=32908668
key_group_hist2=47722277
key_group_hist3=7295182
key_group_hist4=29741700
key_group_hist5=1685702
key_group_hist6=6207965
key_group_hist7=792146
key_group_hist8=20094082
```


### three batches: exact-prefix records

```text
EXACT slot=1 key=4a4d1c8f point=52855 v8_index=17768 v7_index=298 w6=6dce023a w5=1adc8289 c18=fb5be78e cv=4a4d1c8f 4f3ff527 10eb78d6 c4219825 6b25b3ba 2f340eed 6a450f45 cda89cfa block=a69d08c1dfa2261e4f7b98e6552240745904ccc7e6a6fd51a9d77e7d4d2c05b1dc2dd70a60c47d624fe715aebcf0e4c6580933e2be64c64628182c24b1425a63
```


### up to eight follow-up batches: aggregate output

```text
samples=2816700416 requested=8589934592 stopped_on_joint=1 threads=16 urandom_bytes=180268826624 selftest=pass sample_wall_s=70.152
table_keys=195265888 table_retained=641616343 key_hits=128057516 expected_key_hits=128058136.432 key_z=-0.05612 top8_chisq_255df=280.430 key_mismatch=0
slots_seen=420826008 all_slot_w6=822277 expected_all_slot_w6=821838.066 z=0.48418 any_w6=420529 w6_mismatch=0
any_w5_low16=6322 any_w5_low20=3137 any_w5_low24=803 any_exact=8 joint_c18=1 uniform_prefix_bounds=[3.026534,3.135063] uniform_joint_lower=0.412009
slot0 w6=250070 w5low16=1927 w5low20=966 w5low24=256 exact=2
slot1 w6=193383 w5low16=1548 w5low20=739 w5low24=184 exact=3
slot2 w6=112480 w5low16=915 w5low20=447 w5low24=96 exact=0
slot3 w6=99844 w5low16=781 w5low20=369 w5low24=86 exact=1
slot4 w6=49533 w5low16=365 w5low20=186 w5low24=55 exact=1
slot5 w6=46472 w5low16=360 w5low20=187 w5low24=42 exact=1
slot6 w6=35969 w5low16=272 w5low20=139 w5low24=41 exact=0
slot7 w6=34526 w5low16=282 w5low20=142 w5low24=45 exact=0
key_group_hist1=28756824
key_group_hist2=41734636
key_group_hist3=6383097
key_group_hist4=26010248
key_group_hist5=1472447
key_group_hist6=5431759
key_group_hist7=691200
key_group_hist8=17577305
```


### up to eight follow-up batches: exact-prefix records

```text
EXACT slot=1 key=6cdaf49a point=40827 v8_index=12310 v7_index=198 w6=051023ba w5=54758fe8 c18=547ad011 cv=6cdaf49a 34ecefb4 fe6b204c bb96549c 39e550f8 3e0ecf65 bd407838 cabc4bd1 block=bb45e2802ce35f028e33123805b29194e7ba61d0330678836471507c3da2acced839c16ff990ffb8b8ac0270b1360564ba0242e464238b01fad54e9690ed62c7
GROUP key=6cdaf49a selected_slot=1 count=3 entries=40827:12246:198,40827:12310:198,40827:12378:198
EXACT slot=1 key=576be8e7 point=3125 v8_index=533 v7_index=62 w6=adc47138 w5=89fe8400 c18=4aba4556 cv=576be8e7 68f8c40b faaaa113 c4380831 d09a8792 61dce33b a6005684 e36a8f63 block=95ea10d498f2d7180d9a7d1dab2113f684026e829872f23bd32b9368debbb2f8a9a9307c104a7a49ff78f6528e6ca70be0998aca0308d70e33ec8574a51135d6
GROUP key=576be8e7 selected_slot=1 count=8 entries=3125:529:62,3125:533:62,3125:593:46,3125:597:46,3125:661:62,3125:665:62,3125:729:46,3125:733:46
EXACT slot=5 key=f52c03d3 point=46519 v8_index=20502 v7_index=240 w6=c4dd4450 w5=ca668381 c18=9e462545 cv=f52c03d3 5f852ad5 774db478 22833aab be55c366 ffefb2c8 65ab3742 bed8c332 block=5ed64842fbbfa794a0a1e8a48a1c4f47806340cbb4e4b74929273a2f61b1bbf87cafc847153b0beb8b8a58cf367d482ee5362b7a252b4fe3a0de7764d541962f
GROUP key=f52c03d3 selected_slot=5 count=8 entries=46519:18194:240,46519:18198:240,46519:18202:240,46519:18206:240,46519:20498:240,46519:20502:240,46519:20506:240,46519:20510:240
EXACT slot=0 key=e5537f05 point=50567 v8_index=36714 v7_index=510 w6=a19425d0 w5=671389c8 c18=7d1ed103 cv=e5537f05 0a149fcf beff1cf7 3b8c687f a1a59869 c1bb3b76 c8494303 3f7cb0b5 block=ceea555d6c28161e02bdbbd1f91bb1a6e806b36ed500062ceecb238f3a5993f0e47aec94876ad3376a9e2ffbaccd731101ea06e98a50652da3b50165ab908c6e
GROUP key=e5537f05 selected_slot=0 count=5 entries=50567:36714:510,50567:37738:510,50567:38762:510,50567:47978:510,50567:49002:510
EXACT slot=4 key=b4c2ca0b point=3361 v8_index=8448 v7_index=87 w6=b89615d6 w5=6d328d89 c18=cb05f5ad cv=b4c2ca0b 0c81366e 91102abd 87e336fc 2f72a0c8 01d1156f abd7ae8a 1fa9ecfa block=b6109534826892bc9949955702615e8ec21866a3871c9f82b2aae046c4b542dad9dab5a172a52908acd7f2a83b1f43a7a529079e86b6a3b2b7e75a05c5c1d8a7
GROUP key=b4c2ca0b selected_slot=4 count=8 entries=3361:6400:87,3361:6432:87,3361:6912:87,3361:6944:87,3361:8448:87,3361:8480:87,3361:8960:87,3361:8992:87
EXACT slot=1 key=2af1f2ae point=29712 v8_index=48338 v7_index=247 w6=dd5c2658 w5=94dd8e01 c18=6ca0a149 cv=2af1f2ae b731530c e5aaccbb f738a91a 40241477 b15e126f ef94bf30 4d92e196 block=b4fb2d91f8ef1b6e1c25a5d5a41d063893135de27ee11310f687e7cc1eb0f86fae3d7df2b6e4bfb055a3d5d86cd237fec9cf86a427dd7d29c85d47b967053b40
GROUP key=2af1f2ae selected_slot=1 count=2 entries=29712:48082:247,29712:48338:247
EXACT slot=0 key=01ae91f4 point=28572 v8_index=8041 v7_index=138 w6=cdcb7472 w5=e5038d00 c18=2a0da76c cv=01ae91f4 5b86d929 002354ef 73c63bfa 0ace21df afbf8c94 58b36396 69afe168 block=cba92257857200ba339f8828983a2b991281367957564766e7e5fbaf2eff340375c7e81ffa3eb112eb6a5710104a06e8df88bfde6abe4f18eecfe324af430b5a
GROUP key=01ae91f4 selected_slot=0 count=4 entries=28572:8041:138,28572:8169:138,28572:8553:138,28572:8681:138
JOINT slot=3 key=8b6504bf point=54058 v8_index=13786 v7_index=362 w6=f80860bc w5=58648729 c18=9c793744 cv=8b6504bf a058c712 a35cd3cb 0a3cc99a 047c4b65 5eda04fc b3f4978e 40ecf21d block=5cb6239263375b741224f73781998bab32cc55cdbfec2124e7e6f61b59952a0b7734302c0966fee39f8aa3b199734e0175371bfc64b857fd6e8932d3dbb80cd5
GROUP key=8b6504bf selected_slot=3 count=8 entries=54058:12754:362,54058:12762:362,54058:13778:362,54058:13786:362,54058:14802:362,54058:14810:362,54058:15826:362,54058:15834:362
```
