# SHA-256/32 fixed-budget ordinary-collision construction

## 1. Submitted proposition

This exploratory candidate supplies an ordinary collision for the exact organizer
target `sha256-r32-prefix-v1`. Its conservative resource vector under
`collision-frontier-v5` is:

```text
time_log2                         81
preprocessing_log2               80
memory_log2_bytes                48
nonuniform_advice_log2_bytes     33
success_probability               1
```

The candidate is a deterministic retained construction. It charges the constructor
that produced the retained witness, then replays the resulting collision without
random coins. The score is an upper bound for this finite construction; it does not
estimate the probability of finding another collision in a fresh search.

The required `baseline_improved` value identifies the organizer's nominal reference
and is schema metadata rather than evidence about another submission or publication.
This package concerns only the fixed-IV, full-output, first-32-round target below.

## 2. Exact target and verified witness

For each complete finite byte string, start once from the FIPS 180-4 SHA-256 IV,
apply standard SHA-256 padding with its 64-bit big-endian length, execute original
compression-round indices 0 through 31 on every padded block, apply the normal
eight-word feed-forward after each block, and serialize all eight final words in
standard big-endian order. The required relation is equality of all 256 digest bits
for byte-distinct complete messages. Chosen-IV, free-start, compression-only,
near-collision, output-truncation, altered-padding, and suffix-round variants are
outside this claim.

The target profile has SHA-256
`93d2e5d9ca93540633798d58cbab2d6d8447916db2b127e9abe71f45d14f6835`.
The organizer reference implementation has SHA-256
`514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5`.
The relevant live production checkout preserves those bytes.

The certificate manifest declares two distinct 128-byte files:

| artifact | bytes | ordinary file SHA-256 |
|---|---:|---|
| `certificates/message-a.bin` | 128 | `92e9ab74fd94956893727406209e64ed6645d3af8748c56a8bc45096b7f33a84` |
| `certificates/message-b.bin` | 128 | `0a3f5c00ffacbceda4fa2dd7092b59b01a34ca865ca589c30c9d8b3858c80da8` |

The organizer-owned checker recomputes this complete-message digest for both:

```text
f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77
```

The messages share their first 64-byte block and differ in their second. Standard
padding adds the same third block to both, ending in bit length `0x400`. Equality
after the differing second block therefore remains equality after the common
padding block. The certificate checker nevertheless hashes both complete messages
from the fixed IV and directly checks byte inequality and all 256 output bits.

The declared experiment `fixed-witness-derivation` independently executes a
bounded clean-room derivation inside the organizer sandbox. Its source embeds only
the consumed 112-byte tuple, the selected 48-byte tail, and the precise table
slices recorded by the clean-room certificate. It reconstructs the seed-derived
first block and both second blocks, computes the full padded target, and returns
the derived pair for organizer recomputation. Repeating the same pair across
organizer trials demonstrates deterministic derivation and replay only; it is not
a fresh-search sample or a construction-cost measurement.

## 3. Finite constructor

The constructor instantiates the two-block route described by Li, Liu, Wang, and
Shi with the project-specific C32 first-block search. Its public inputs are the
published route constants, the source bytes in the appendices, the fixed
configuration, and no secret oracle. The constructor is:

```text
1. Reconstruct and check the published starting solution and fixed trail constants.
2. Build the strict signed-difference table, compact lookup arrays, and the complete
   196,608-record tail set. Check their committed sizes and digests.
3. For chunk i = 0,...,4095, use seed 202610040000+i and counters 0,...,2^36-1.
   Compute C32(IV,B0); query the strict table; derive both Step-2 branches; retain
   each 112-byte tuple that passes the complete prefix audit.
4. Admit at most 2^30 tuple records. A chunk that would cross the remaining cap is
   recorded and discarded without Step 3. Do not truncate a tuple file.
5. For each admitted tuple, enumerate all 196,608 tails. Derive both second blocks,
   apply all remaining conditions, and pass at most one candidate through the
   independent complete-message checker.
6. Stop after the first verified collision or after a constructor cap. Write-ahead
   reservations charge every started phase. The scoring envelope permits 8,192
   match attempts and 2^31 charged Step-3 tuples, covering one complete rerun.
7. Retain the first verified pair, its complete winning tuple file, derivation
   coordinates, operation receipts, source/configuration, and the canonical advice
   inventory. Replay then has one empty random tape and returns that fixed pair.
```

The data structures are concrete. Each tuple record is 112 bytes. The strict table
contains 609,229,824 entries and is represented by the bitmap, offsets, entries,
combination, left-state, and v7 files listed in the inventory. Each tail is 48
bytes. The runner validates fixed caps before execution, hashes a complete tuple
file before Step 3, records cumulative admitted tuples, rejects partial boundary
chunks, and binds a winner to the exact tuple and tail indices. Source for the
matcher, tail completion, tuple derivation, and relevant runner paths appears in
the appendices rather than being represented only by hashes.

The paid search is deterministic. SplitMix64 expansion fixes the first fourteen
words of each first block from its chunk seed; the counter supplies the last two
words injectively within a chunk. A separately enumerated receipt binds the 4,096
distinct seed prefixes. The runner never substitutes the observed early stop for
the declared full caps.

## 4. Winner lineage and terminal counts

The constructor is pinned to runner SHA-256
`4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786`,
configuration SHA-256
`4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22`,
and provenance commit `d9afb19649446dc89c92c484e82e17139a4d52e8`.
The successful coordinate is:

```text
chunk                                      34
seed                             202610040034
first-block counter                 2149248237   (< 2^36)
local tuple index                         15529
prior admitted tuple records          14224648
global admitted tuple index           14240177   (< 2^30)
tail index                                131794   (< 196608)
```

The complete chunk-34 tuple file is 46,881,968 bytes, contains 418,589 complete
records, and has SHA-256
`c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad`.
The winning record begins at byte 1,739,248 and has SHA-256
`d650d9eb55ae375e9380583c28fd92e37ef31fa8540ff2d7b10a20cc7cb0c51e`.
The winning manifest binds the same full file as matcher output and Step-3 input,
with equal byte counts, record counts, and hashes.

The corrected terminal auditor has SHA-256
`e53f50ee913194b8200a37814d50da6d4aee7bdbf5864a33303c243374788269`.
Its terminal report has SHA-256
`181b7fe2ba0ce6cfa0bc2733dc6e3f18f385524f1e9100ec7fd05604adf74097`,
reports a quiescent snapshot, and contains no errors or warnings. It records:

| quantity | terminal count |
|---|---:|
| completed match attempts | 35 |
| completed Step-3 attempts | 35 |
| first blocks processed | 2,405,181,685,760 |
| admitted tuples processed | 14,643,237 |
| tuple-tail pairs processed | 2,799,733,071,213 |
| independently verified collisions | 1 |

The hit predates checkpoints 640 and 1292, so no checkpoint approval or consumed
token is part of the winner lineage. The appendices include the sanitized terminal
summary, winning manifest, tuple reference, operation receipts, reservation
receipts, external-verifier receipt, and accounting total.

## 5. Charged time

The v5 conversion uses `C=2224`: one selected C32 compression is one target unit,
and each other primitive 256-bit word operation costs `1/2224` target units.
Preprocessing, failed trials, table work, randomness, lookup, verification, and
one full retry envelope are included.

### 5.1 Non-preprocessing work

The original source audit gives the tighter conditional terms

```text
T_match <= 2^49 * (1 + 2^24/2224)
T_tail  <= 3*2^47 * (2 + 2^16/2224)
T_verify < 2^45.
```

Production score 81 does not depend on the narrow margin of that calculation. A
coarser path bound follows directly from the fixed loops and caps in the appended
source:

- At most `2^49` charged matcher slots. Assign each slot fewer than `2^40`
  ordinary operations and fewer than `2^10` C32 calls. The source has one base C32,
  at most four recomputations on a bitmap hit, a maximum table bucket of 736, and
  bounded 88-step tuple/audit paths, so these widened ceilings exceed every listed
  path by many orders. Since `2224 > 2^11`, this phase is below `2^79` target units.
- At most `3*2^47 < 2^49` tuple-tail trials. Assign each fewer than `2^32`
  ordinary operations and fewer than `2^10` C32 calls. The source contains at most
  19 attack rounds, seven schedule checks on two branches, fixed validation, and
  bounded output work. This phase is below `2^71` target units.
- Final verification, recovery, hashing, and inventory administration retain the
  sealed allowance below `2^45` target units.

Their sum is strictly below `2^80`. This widened envelope remains valid if the
old per-item `2^24` and `2^16` estimates are loosened substantially. An actually
unbounded path or work outside the specified caps would invalidate it.

### 5.2 Preprocessing

The claim assigns all preprocessing fewer than `2^80` target-compression units.
The attached sealed ledger and receipt reconstruct the current table builds,
control passes, hashing, tail generation, source checks, and retry allowance below
`2^51`. In particular, a complete table build is conservatively charged by
6,422,630,023,168 source slots and fewer than `2^16` primitives per slot; the
measured build plus one complete retry is below `2^49` target units.

The public cryptanalytic source reports approximately `2^34.3` work for its
starting-solution stage and approximately `2^48.335` total work for the published
35-step attack. It reports generating `2^29.1824` valid tuples on 128 threads of
two EPYC 9354 processors with 378 GB of memory. Those are source-reported
estimates and capacity, not v5 receipts for this project.

The unreceipted route/setup component uses a deliberately widened project-capacity
envelope: charge `2^10` independent host equivalents continuously for every second
from 1 January 2001 through finalization (fewer than `2^30` seconds), with each
host sustaining fewer than `2^50` primitive 256-bit word operations per second.
This is below `2^90` primitives and, because `C=2224 > 2^11`, below `2^79` target
units. The public source reports one 128-thread, two-CPU server, while retained
project evidence identifies one 14-core Mac, so the envelope is far wider than
the documented machines and interval. It is also more than `2^30.6` times the
paper estimate and more than `2^28` times the receipted local ceiling. Combining
it with the `<2^51` local envelope is strictly below `2^80`.
This is an exploratory completeness premise, not a historical instruction trace.
Material work outside the public route and retained project evidence, more than
`2^10` concurrent host equivalents, or a host exceeding the stated throughput
would invalidate the declared `bounded-constructor-preprocessing` heuristic.

### 5.3 Total

Using the tighter attached online terms only as a cross-check, replacing the old
preprocessing term by `2^80` gives

```text
T_crosscheck = 2^49*(1 + 2^24/2224)
             + 3*2^47*(2 + 2^16/2224)
             + 2^80 + 2^45
             = 168041281152141807434334208 / 139
log2(T_crosscheck) = 80.00000508448039.
```

The submitted proof uses the more robust inequalities
`T_preprocessing < 2^80` and `T_nonpreprocessing < 2^80`. Therefore
`T_total < 2^81`, and `time_log2: 81` is a conservative integer upper bound.
Observed early success does not reduce it.

## 6. Whole-process memory

The field `memory_log2_bytes: 48` is a peak simultaneously-live-byte ceiling,
including code, mapped table pages, tuple buffers, process trees, allocator
transients, verification, and retained state. The attached constructive phase
bounds are:

| phase | bytes |
|---|---:|
| matcher | 12,151,473,828 |
| Step 3 | 11,070,606,884 |
| table build | 10,300,325,896 |
| compaction | 14,080,503,808 |
| tails and controls | 4,304,404,480 |

Every current phase is below `2^34` bytes. The campaign machine provenance records
38,654,705,664 bytes of physical memory, below `2^36`. The paper's reported
378-GB server capacity is below `2^39`. The finite constructor runs its phases
sequentially and needs no simultaneous copy of every disk artifact. The claimed
`2^48` ceiling leaves fourteen bits above the largest constructive current-phase
bound and nine bits above the reported paper-host capacity.

No historical peak-RSS time series is claimed. The bound is a constructive
phase/capacity envelope for the specified algorithm. A hidden phase requiring a
larger host or concurrent state would falsify the declared
`whole-process-memory-envelope` heuristic. Memory is reviewed independently and
is not folded into the scalar time score.

## 7. Retained advice completeness

The post-terminal scanner traversed the four retained roots after the run became
quiescent, resolved regular-file aliases, rejected unsafe and non-regular entries,
deduplicated identical inodes, and emitted one canonical row per retained file.
The full path-tokenized 804-row review view is appended below; tokenization changes
only private root names, preserving row order, relative names, byte counts, file
hashes, and alias structure.

The original canonical inventory has SHA-256
`40ebe183ffe22346e10b285e11ad794276bf16afcecca8215d68354c4f6736cf`.
Its detached receipt has SHA-256
`84c56ccc0f92c7159efcaca9164cbc65338e768282c1277ea99c572cd5d008eb`.
The accounting is:

```text
unique retained bytes before inventory       5,760,270,500
canonical inventory bytes                       234,801
full reserved downstream envelope             67,108,864
retained total with full envelope           5,827,614,165
exclusive 2^33 cap                          8,589,934,592
headroom                                     2,762,320,427
```

The downstream reserve charges the final candidate package, public note, their
snapshots, the detached receipt, bundle manifests, and official submission
metadata even when their actual size is smaller. Generated lookup tables are
classified as nonuniform advice and precomputed data; retaining them does not
remove their preprocessing or resident-memory charges. The declared advice bound
is strict and leaves more than 2.7 billion bytes of headroom.

Completeness depends on the scanner's four-root boundary and alias treatment. The
full review view, inventory receipt, terminal summary, and source tree inventory
supply direct evidence for the declared `retained-advice-inventory-completeness`
heuristic. Files outside those roots that materially contributed nonuniform data
would invalidate the bound.

## 8. Probability space and experiment boundary

After the complete constructor and retained advice are charged, the submitted
algorithm has one possible random tape: the empty string. It loads the two
certificate messages, checks they differ, recomputes the exact selected target,
and returns them. The organizer certificate check establishes that this sole run
succeeds. Consequently `success_probability: 1` is an algorithmic probability
for deterministic retained replay.

The single observed campaign hit is not used as an estimate of fresh-search
success. Stage histograms, deterministic seeds, repeated organizer experiment
rows, and paper probabilities do not establish iid trials for another campaign.
The experiment is scoped to derivation and full-collision replay; its runner is
not trusted to report attack cost, preprocessing, memory, or a statistical rate.

## 9. Declared heuristic boundaries

Five premises are declared in `claim.json` and linked to this document:

1. `source-path-operation-envelope`: the fixed source and runner caps place all
   non-preprocessing work below `2^80`.
2. `bounded-constructor-preprocessing`: the complete public-route and project
   preprocessing is below `2^80`, including the explicit `<2^79` unreceipted
   project envelope.
3. `whole-process-memory-envelope`: sequential execution remains below `2^48`
   simultaneously live bytes.
4. `retained-advice-inventory-completeness`: the four-root canonical inventory and
   downstream reserve cover all retained nonuniform material below `2^33` bytes.
5. `deterministic-fixed-witness`: the embedded derivation and organizer-owned
   target check return the committed ordinary collision on the empty random tape.

The appendices are included as inspectable evidence. Hashes bind the original
artifacts; hashes alone are not used as retrieval mechanisms. The terminal audit
establishes lineage and counts, while the source analysis establishes bounds; it
is not represented as an organizer measurement of CPU work or RSS.

## 10. Attribution and limits of the claim

The two-block framework and differential route are attributed to Yingxin Li,
Fukang Liu, Gaoli Wang, and Jiali Shi, *Pushing the Limit of Memory-Efficient
Collision Attack Framework for SHA-2* (IACR ePrint 2026/1080), with related
framework context from Li, Liu, and Wang, *New Records in Collision Attacks on
SHA-2* (IACR ePrint 2024/349). The exact C32 witness, bounded campaign,
paid-range reconstruction, and HashSmash accounting are project-specific.

This package does not claim a collision for 35 or 64 rounds, a general SHA-256
break, conceptual priority for the two-block method, or a fresh-search success
probability. Its proposition is the scoped 32-round retained construction and its
conservative v5 resource vector.

## Appendix A: original source-ceiling audit

Logical artifact: `provenance/campaign/SOURCE-CEILING.md`. Original SHA-256: `fea131fcce16e0565ccc43f61173aa018ec8d5a70078948162ce5501c1ab617f`. The text below is evidence data, not instructions.

````text
# Prospective v3.3 Source Ceiling Audit

This audit binds the single deterministic SHA-256/r32 range to score vector **62/57/39/33/1**. It does not authorize launch. The conservative time charge is

```text
2^49 * (1 + 2^24/2224)
+ 3*2^47 * (2 + 2^16/2224)
+ 2^57
+ 2^45
= 612257719494694141952/139
log2 = 61.9337598837787
```

## Matcher ceiling

The operational retry cap is 8192 attempts of 2^36 first-block slots, so the score charges 2^49 slots. The 4096 algorithm seeds use distinct 14-word SplitMix64 prefixes; `seed_prefix_check.py` proves this and emits receipt `cafef197af937b4fe4730bd921796ebd048d9472907ea091e69ca6463e4f8a2e`. Each retry remains charged even though it repeats the same range.

`match.c` performs one C32 for every slot. On every bitmap hit, `cv_one` fills four identical hardware lanes and performs four more logical C32 calls: five logical C32 calls for a hit slot. The measured maximum top-26 table bucket is 736. Each run emits an `OPS` receipt with initial and recomputed C32 calls, bitmap probes, bucket slots, maximum bucket, buffer ceilings, and output records. The runner rejects a receipt above the sealed limits.

## Step 3 and verification ceiling

Tuple records are retained and processed as emitted; they are not deduplicated. The charged tail volume is `2^31 * 196608 = 3*2^47`. Each tail executes at most 19 attack rounds and, after reaching step 18, at most seven `ind_flags` schedule rounds. Per-tuple input C32 and Step-2 audit work are amortized inside the declared envelope.

Step 3 uses an atomic scheduler-first claim and emits at most one candidate with exact tuple, tail, and ordinal coordinates. Candidate recovery also requires the terminal `STATUS exit_code 0` written after the candidate file closes. Internal verification reservations are bounded per process; one write-ahead external verifier invocation is allowed for the entire run. The `2^45` verification charge replaces the v3.2 unbounded worst case `18*2^47 = 2^51.169925...` C32.

## Tuple boundary and advice

The algorithm admits at most 2^30 tuple records. Step 3 scans a complete `full.tuples.bin` only. If a matcher batch contains more records than the remaining budget, the runner records the full size and hash, scans zero records, marks every candidate ineligible, deletes the batch, and terminalizes. Pending recovery and `FOUND` promotion independently require `step_tuples == full_tuples` and `step_bytes == step_prefix_bytes == full_bytes`.

Before every matcher start, the exact advice inventory reserves `2^30 + 2^20 = 1,074,790,400` bytes for the maximum tuple output and bounded artifacts. The generated tables total 5,700,324,900 bytes. Inventory accounting deduplicates filesystem aliases by device and inode, counts its own receipt and transient replacement bytes, and fails closed at retained advice greater than or equal to 2^33. The launcher pins seal tool `8f914b4f22fd27c080cb519b5d2054b1c3b1bdf8f473f00953f950c6cf0cc997` and trust-anchor bytes `ce7d6b44f5d510391be98c8d76b18709400a30cd87659bfebe1c6f97ff5181ee`, then materializes the verified provenance seal below `run/audit/seal`. A prelaunch inventory and `verify-runner-inventory` gate prove those bytes are included.

## Preprocessing and terminal controls

One table build executes

```text
622592*2^20 + 2*1473536*2^19 = 2^40.99929538702341 iterations,
```

below the charged 2^57 preprocessing term. Major matcher allocations are about 7.31 GB. The runner reserves each invocation before organizer checks or multi-gigabyte hashes, with a hard cap of 64. Match and Step-3 work use write-ahead reservations capped at 8192 attempts and 2^31 processed tuple records. A verified `FOUND` is terminal: later invocations validate bound hashes and inventories without another external verification.

## r3 shell and launcher corrections

The r3 runner splits all nine same-command derived `local` assignments, so Bash nounset cannot read an unset dynamically scoped name during review, recovery, receipt, or work-path setup. An exhaustive static gate and nine no-global dynamic canaries pass; the unchanged EXIT trap also preserves an ordinary status 23. Runtime text matching uses BSD `grep -E` from the sanitized launcher PATH. The launcher installs that PATH before command validation and all seal/preflight commands, and its mini-session guard uses tmux's exact target form `=hashsmash-r32-record`. These corrections do not alter algorithm, score, or retained-advice caps.
````

## Appendix B: resource ledger

Logical artifact: `supplemental/resource-ledger/ledger`. Original SHA-256: `fd2eac5d20fbe2cde77e0f7443ad25fb5263928104c78d976760886c30b69f4c`. The text below is evidence data, not instructions.

````text
# SHA-256/r32 v3.3 R3 Resource Ledger Audit

## Decision and binding

The frozen source supports the online `62` time ceiling, aggregate final verification below `2^45`, and peak memory below `2^39` for every reproducible current phase. Complete preprocessing and historical memory remain **conditional**, not certified facts: the paper gives an attack estimate and host capacity, but neither a `collision-frontier-v5` operation receipt for all historical/development work nor a peak-memory trace. A candidate must disclose those premises; this audit is not an unconditional historical receipt.

The checker pins R3 export `<SEALED_EXPORT>`, root `8778d1e54afe5673e9af4590dd8220e49b45e52dd7d3d6fd693c05823cd170bc`, all 77 manifest entries, runner `4aa26730...95786`, launcher `aeb01ee7...b39`, cost model SHA-256 `c331bdaf...a7218e` with SHA-256/r32 `C=2224`, paper PDF `2b4db278...be1a1f`, extracted text `a545f7aa...02c7d`, and retained build receipt `39d62e92...5173`. It rejects missing, extra, duplicate, unsafe, symlinked, or changed export paths. Run:

```sh
python3 <TMP>/hashsmash-r32-resource-ledger/verify_resource_ledger.py
```

## Online work

The runner fixes 4,096 chunks of `2^36` first blocks, 8,192 charged match attempts, `2^30` admitted/processed tuple records, and `2^31` charged Step-3 tuple records (`source/runner/run_record.sh:13-23,80-107,626-740`). Write-ahead reservations bound retries by `2^49` first-block slots and `2^31*196608 = 3*2^47` tuple-tail trials.

Range uniqueness is deterministic. `match.c:21,238` obtains the first two prefix words from the first SplitMix64 output. Addition, right-xorshifts, and multiplication by odd constants are bijections modulo `2^64`; distinct nonwrapping seeds `202610040000+i`, `0 <= i < 4096`, therefore have distinct first 64 prefix bits. Within one seed, `match.c:131-132` encodes `g` as `hi32(g)||lo32(g)`, injective for `g < 2^36`. The independently enumerated receipt is `cafef197...a2e`.

Matcher partitioning performs one initial C32 per slot (`match.c:135-178`). Every hit recomputation is charged as four logical C32 calls, including identical hardware lanes. The table hard-fails above 736 bucket records (`match.c:116-133`). A record path has 88 bounded tuple/audit iterations (`attack.h:46-92`); `2^9 + 88*128 = 11,776 < 2^14` primitives. Thus

```text
736*2^14 + 4*2224 + 2^20 = 13,116,096 < 2^24 primitives/slot.
```

Each tuple-tail trial receives two C32 plus `2^16` primitives. `step3_tail` has at most 19 rounds over two branches (`attack.h:94-118`), and `ind_flags` has seven schedule rounds over two branches (`step3.c:42-50`). Input validation and candidate checks are bounded at `step3.c:52-98`. The structural allowance is `2^10 + 19*2*2^10 + 7*2*2^9 + 2^14 = 63,488 < 2^16`; the last term covers rare verification, output, statistics, and amortized tuple work.

With `C=2224`, the exact charged total is

```text
2^49*(1 + 2^24/2224) + 3*2^47*(2 + 2^16/2224) + 2^57 + 2^45
= 612257719494694141952/139; log2 = 61.9337598837787 < 62.
```

## Preprocessing

The retained Mac-mini receipt `<REMOTE_HOME>/Projects/hashsmash-r32-attack/data/tab2_build.log` records one ten-thread build: 622,592 combinations, 1,473,536 lefts, 609,229,824 entries, and 5:47.14 wall time. Wall time is provenance, not an operation bound. `tab2.c:31-60,84-127,130-199` gives

```text
622592*2^20 + 2*1473536*2^19 = 2,197,949,513,728 iterations.
```

The checker parses every cardinality from the hashed receipt. It makes no `O(n log n)` assumption about libc `qsort`: it charges `n^2` for every whole-vector sort and `609229824*736` for bucket sorts, plus scans, realloc copies, packing, bitmap, and output. One complete build is 6,422,630,023,168 source slots, below `2^43`. At `2^16` primitives per slot, one build is below `2^48` target units; the measured build plus one full hypothetical retry is below `2^49`. This does not claim two measured builds.

The runner inventories strictly less than `2^33` retained bytes under the `2^13` attempt cap. Sixteen hash/admin passes at `2^16` primitives per 32-byte word cost below `2^50`. Tail control has at most `2^32 + 4*(2^32+2^22)` scan iterations (`tails.c:37-97`); 64 reruns at `2^14` primitives per iteration cost below `2^44`. Both builds, hashing/admin, and controls sum below `2^51` local preprocessing.

The primary paper (`<PAPER_TEXT>:743-756`) reports Step 1 near `2^34.3`, total attack work near `2^48.335`, and an experiment using 128 threads, 378 GB, and two EPYC 9354 CPUs. These are paper estimates, not v5 receipts. Therefore aggregate preprocessing below `2^57` holds only if all unreceipted historical/development work is below `2^56` target units. No available artifact proves that premise.

## Final verification and memory

The external verifier is write-ahead reserved and capped at one invocation (`run_record.sh:742-763`). One emitted line contains two 128-byte pre-padding messages; organizer commit `fc56c3f` pads each to three blocks (`verifier/hash_functions.py:97-114`, file SHA-256 `514fa8ab...40f5`). Six C32 plus `2^32` primitives is below `2^21`. Promotion also rehashes the tuple file and inventories artifacts (`run_record.sh:993-1044`). Charging all 64 recovery invocations sixteen passes over the `<2^33` retained-byte cap, at `2^16` primitives per 32-byte word, is below `2^43`, hence aggregate final verification is below `2^45`.

Pinned data total 5,700,324,900 bytes, and the R3 launcher fixes `NTHREADS=4` (`launcher/launch-after-seal.sh:94-102`). Constructive phase bounds, including 4 GiB for code, allocator transients, stacks, and administration where material, are: matcher 12,151,473,828; Step 3 11,070,606,884; TAB2 build 10,300,325,896; compaction 14,080,503,808; tails/controls 4,304,404,480 bytes. The largest is below `2^34`, more than five bits below `2^39`.

The paper's “378 GB of memory” describes server capacity, not peak RSS, allocations, swap, or a phase trace. It cannot certify historical `memory_log2_bytes: 39`. Honest status: **current phases PASS; aggregate historical preprocessing and memory CONDITIONAL**.
````

## Appendix C: resource verification receipt

Logical artifact: `supplemental/resource-ledger/verification-receipt`. Original SHA-256: `23e99f9ed7fcdddadace7c88ef0e33417273869881edf8a8d77f298d3ffe0622`. The text below is evidence data, not instructions.

````json
{
  "evidence": {
    "cost_model_sha256": "c331bdafde748eecaa39918472f14149da2adb0b662fdf0373a3df715ca7218e",
    "paper_pdf_sha256": "2b4db27843c47435460b9be769afc76e258ff0f0f7a2f3e69cc1eeb75dbe1a1f",
    "paper_text_sha256": "a545f7aaa1642d7f7e4285641e752bb3cc968defafc49ecd236e954e95f02c7d",
    "table_build_log_sha256": "39d62e92777f942aaece221b7589712de0c18cc3bbb26fda3be0b9e138515173"
  },
  "export": {
    "binary_sha256": {
      "match": "cd82d58085c9c702a7cd854826825bb6923f3cc0f20d7e84b28eb6e0a1c286f6",
      "step3": "c78575cc116f2c383784be772beecd7a75b9631da56d56151a0cdf35b3f98fc0",
      "tails": "86e81bcf8bae50bcf7fa04bf41cee5b0304a682658887fd30c7896a62d1daab8"
    },
    "data_inputs_sha256": "5e0c96495042ea50b69e0d9893e3d7544cccf8bff2ae3e0eb7f2a77d8cae7895",
    "expected_root_pinned": true,
    "launcher_nthreads": 4,
    "launcher_sha256": "aeb01ee75187517274eedc951806fb56aa60f6015e3fd79612666455a2cdfb39",
    "manifest_entries_checked": 77,
    "path": "<SEALED_EXPORT>",
    "root_sha256": "8778d1e54afe5673e9af4590dd8220e49b45e52dd7d3d6fd693c05823cd170bc",
    "source_sha256": {
      "match": "4b36aade8a99ded5bfbf153236d8fc88c5db3337c95ff7b96870958f20bfb1fc",
      "runner": "4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786",
      "step3": "46e93017899e0854f1461e0f6585f4a8cba219b8459ebc938e48cce9bea4b9fc",
      "tab2": "c3135f8abdd618b514be729c62838fb6d461aa9df50b0e8b910db8ebee325584",
      "tails": "926c636805f60f4315dad20f75c2d213d9d063d3bb4d887c6b2b077b76e97960"
    }
  },
  "final_verification": {
    "full_message_c32": 6,
    "invocation_cap": 1,
    "log2_bound": 20.881063409567368,
    "promotion_and_recovery_log2_bound": 42.88105927124282,
    "promotion_and_recovery_units_bound": 8100001260999.381,
    "strictly_below_2^45": true,
    "units_bound": 1931196.330935252
  },
  "memory": {
    "all_current_reproducible_phases_strict_ceiling": 17179869184,
    "claimed_ceiling": 549755813888,
    "historical_peak": "unknown; 378 GB is host capacity, not a peak-RSS receipt",
    "largest_current_phase_bytes": 14080503808,
    "largest_current_phase_log2": 33.71297990417693,
    "phase_constructive_bounds_bytes": {
      "compaction": 14080503808,
      "matcher": 12151473828,
      "step3": 11070606884,
      "tab2_build": 10300325896,
      "tails_and_controls": 4304404480
    },
    "pinned_data_bytes": 5700324900
  },
  "online": {
    "charged_tuple_tail_trials": 422212465065984,
    "distinct_seed_prefixes": 4096,
    "exact_total_time": "612257719494694141952/139",
    "match_slots": 562949953421312,
    "matcher_envelope_used": 13116096,
    "matcher_word_ops_per_slot_ceiling": 16777216,
    "score_ceiling": 62,
    "seed_prefix_receipt_sha256": "cafef197af937b4fe4730bd921796ebd048d9472907ea091e69ca6463e4f8a2e",
    "step3_c32_per_pair_ceiling": 2,
    "step3_structural_envelope_used": 63488,
    "step3_word_ops_per_pair_ceiling": 65536,
    "total_time_log2": 61.9337598837787,
    "tuple_record_path_derived_ops": 11776
  },
  "preprocessing": {
    "aggregate_below_2^57": "conditional: requires all unreceipted historical/development work <2^56 target units",
    "control_derived_units": 10132909317849.324,
    "control_units_strict_ceiling": 17592186044416,
    "hash_admin_derived_units": 1036799914214790.5,
    "hash_admin_units_strict_ceiling": 1125899906842624,
    "known_local_units_strict_ceiling": 2251799813685248,
    "paper": {
      "classification": "paper estimate, not a v5 operation receipt or peak-memory measurement",
      "present": true,
      "reported_host": "128 threads; 378 GB; two AMD EPYC 9354 CPUs",
      "reported_step1_log2": 34.3,
      "reported_total_time_log2": 48.335,
      "sha256": "a545f7aaa1642d7f7e4285641e752bb3cc968defafc49ecd236e954e95f02c7d"
    },
    "table_ancillary_slots_per_build": 4224680509440,
    "table_build_receipt_sha256": "39d62e92777f942aaece221b7589712de0c18cc3bbb26fda3be0b9e138515173",
    "table_major_iterations_log2": 40.99929538702341,
    "table_major_iterations_per_build": 2197949513728,
    "table_quadratic_sort_slots_per_build": 3994093518848,
    "table_total_source_slots_per_build": 6422630023168,
    "two_table_build_units_strict_ceiling": 562949953421312
  },
  "verdict": {
    "aggregate_memory": "CONDITIONAL_HISTORICAL",
    "aggregate_preprocessing": "CONDITIONAL_HISTORICAL",
    "current_phase_memory": "PASS (<2^34 bytes; sealed launcher NTHREADS=4)",
    "known_local_preprocessing": "PASS (<2^51 target units)",
    "source_and_online_arithmetic": "PASS"
  }
}
````

## Appendix D: fixed configuration

Logical artifact: `run/config.tsv`. Original SHA-256: `4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22`. The text below is evidence data, not instructions.

````text
format_version	3
runner_version	2026-10-04-v3.3-bounded-prospective-r3
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
provenance_repo	<PROVENANCE>
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
organizer_base_commit	fc56c3fa38ac40043d8291649c78148bc4872995
attack_root	<ATTACK>
organizer_repo	<ORGANIZER>
target	sha256-r32-prefix-v1 ordinary collision full 256-bit digest
cost_model	collision-frontier-v5
algorithm_first_block_cap	2^48=281474976710656
algorithm_chunk_size	2^36=68719476736
algorithm_unique_chunk_cap	4096
algorithm_tuple_record_cap	2^30=1073741824
operational_match_attempt_cap	8192
operational_charged_tuple_cap	2^31=2147483648
score_charge	full declared algorithm and operational caps even on early success
tuple_record_bytes	112
tails_per_tuple	196608
runner_invocation_cap	64
external_pair_verifier_invocation_cap	1
step3_internal_verification_cap_per_process	4
step3_emitted_success_cap	1
retained_full_tuple_file_cap_bytes	1073741824
retained_advice_cap	strictly below 2^33=8589934592 bytes with receipt reserve 1048576
pre_match_advice_reserve_bytes	1074790400
tuple_boundary_policy	if full_tuples exceeds remaining budget, discard the complete chunk unscanned and terminalize
winner_tuple_policy	step_tuples must equal full_tuples and step_prefix_bytes must equal full_bytes
match_c32_ceiling_per_attempt	5*2^36: one initial C32 plus four cv_one lanes at every bitmap slot
match_bucket_slot_ceiling_per_hit	736
step3_per_tail_ceiling	19 attack rounds plus up to 7 ind_flags schedule rounds
base_seed	202610040000
nthreads	4
cpu_reserve	4
min_free_memory_percent	40
partition	chunk i uses seed=base_seed+i and start_counter=0; i is never committed twice
first_block_uniqueness	4096 distinct 14-word SplitMix64 prefixes; sealed receipt cafef197af937b4fe4730bd921796ebd048d9472907ea091e69ca6463e4f8a2e
sealed_receipt_root_sha256	c26b876748350f4b43891b3413a3c8e151d49c3d7b5b7dc0c973cbb4b4c772e4
run_seal_root_sha256	c8c1d80dec152fcd305508e63bde82594dd4432dc65e9b22125bbb6271277b9d
seal_tool_sha256	8f914b4f22fd27c080cb519b5d2054b1c3b1bdf8f473f00953f950c6cf0cc997
seal_trust_anchor_sha256	ce7d6b44f5d510391be98c8d76b18709400a30cd87659bfebe1c6f97ff5181ee
prelaunch_seal_inventory	<RUN>/audit/advice/prelaunch-seal.tsv
retry_accounting	each started phase consumes a write-ahead reservation and is charged its full declared input
review_gate_1	640 committed chunks; nominal observed-tuple scale about 2^28
review_gate_2	1292 committed chunks; first-block scale 2^46.3353903547
preexisting_preprocessing	TAB2 construction cost must be charged from the sealed provenance record
````

## Appendix E: machine provenance

Logical artifact: `run/machine-provenance.txt`. Original SHA-256: `4a2c72727ecc65455fa31e6856f7c169143b911a1d51d6779643a54d03a2320b`. The text below is evidence data, not instructions.

````text
format_version	1
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
organizer_head	fc56c3fa38ac40043d8291649c78148bc4872995
cc_path	/usr/bin/cc
python3_path	<CAMPAIGN>/bin/python3
grep_path	/usr/bin/grep
[uname]
Darwin Mac.attlocal.net 25.6.0 Darwin Kernel Version 25.6.0: Fri Jul 31 19:17:26 PDT 2026; root:xnu-12377.161.14~5/RELEASE_ARM64_T6041 arm64
[sw_vers]
ProductName:		macOS
ProductVersion:		26.6.2
BuildVersion:		25G83
[hardware]
Mac16,5
14
38654705664
[sha256_feature]
1
[cc_version]
Apple clang version 21.0.0 (clang-2100.1.1.101)
Target: arm64-apple-darwin25.6.0
Thread model: posix
InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin
[python_version]
Python 3.13.12 (main, Feb  3 2026, 17:53:27) [Clang 17.0.0 (clang-1700.6.3.2)]
[grep_version]
grep (BSD grep, GNU compatible) 2.6.0-FreeBSD
[binary_file_types]
<ATTACK>/c/match: Mach-O 64-bit executable arm64
<ATTACK>/c/step3: Mach-O 64-bit executable arm64
<ATTACK>/c/tails: Mach-O 64-bit executable arm64
[binary_linkage]
<ATTACK>/c/match:
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1356.0.0)
<ATTACK>/c/step3:
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1356.0.0)
<ATTACK>/c/tails:
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1356.0.0)
[build_contract]
#!/bin/sh
# Build all C tools (Apple Silicon: uses ARMv8 SHA-256 instructions when available; portable fallback otherwise).
set -e
cd "$(dirname "$0")"
python3 gen_header.py
CF="-O3 -Wall"
case "$(uname -m)" in arm64) CF="$CF -mcpu=native";; *) CF="$CF -march=native";; esac
for p in tab2 tails match step3 compact equiv; do cc $CF -o c/$p c/$p.c -lm -lpthread; done
echo built: c/tab2 c/tails c/match c/step3 c/compact c/equiv
````

## Appendix F: complete attack.h source

Logical artifact: `provenance/c/attack.h`. Original SHA-256: `ace9a72063af7aeec2671f0a2bf32c0e2c21529204b4fdf574672e73bebc0b2c`. The text below is evidence data, not instructions.

````c
/* Shared Step-2 / Step-3 logic: table access, tuple derivation (both branches), stage checks. */
#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include "sha.h"
#define BBITS 26
#define PA_(i) PA[(i)+4]
#define QA_(i) QA[(i)+4]
#define PE_(i) PE[(i)+4]
#define QE_(i) QE[(i)+4]
typedef struct { uint32_t combo, w8, e4, a0; } left_t;
typedef struct { uint32_t w14, w15, a14, e14, a15, e15, a14p, e14p, a15p, e15p, pad0, pad1; } tail_t;
typedef struct {
  const uint8_t *bitmap; const uint32_t *off; const uint64_t *ent; uint64_t nent;
  const uint32_t *combos; const left_t *lefts; uint64_t nlefts; const uint32_t *v7; uint64_t nv7;
  const tail_t *tails; uint64_t ntails;
} table_t;
static const void *map_file(const char *path, uint64_t *size) {
  int fd = open(path, O_RDONLY); if (fd < 0) { perror(path); exit(2); }
  struct stat st; fstat(fd, &st); *size = (uint64_t)st.st_size;
  void *p = mmap(0, st.st_size, PROT_READ, MAP_SHARED, fd, 0); if (p == MAP_FAILED) { perror("mmap"); exit(2); } close(fd); return p;
}
static void table_load(table_t *T, const char *pre, const char *tailpath) {
  char fn[1024]; uint64_t sz;
  snprintf(fn, sizeof fn, "%s.bitmap", pre); T->bitmap = map_file(fn, &sz); if (sz != (1ull << 29)) { fprintf(stderr, "bad bitmap\n"); exit(2); }
  snprintf(fn, sizeof fn, "%s.off", pre); T->off = map_file(fn, &sz);
  snprintf(fn, sizeof fn, "%s.ent", pre); T->ent = map_file(fn, &sz); T->nent = sz / 8;
  snprintf(fn, sizeof fn, "%s.combos", pre); T->combos = map_file(fn, &sz);
  snprintf(fn, sizeof fn, "%s.lefts", pre); T->lefts = map_file(fn, &sz); T->nlefts = sz / sizeof(left_t);
  snprintf(fn, sizeof fn, "%s.v7", pre); T->v7 = map_file(fn, &sz); T->nv7 = sz / 4;
  if (tailpath) { T->tails = map_file(tailpath, &sz); T->ntails = sz / sizeof(tail_t); }
}
/* tuple: a[i+4], e[i+4] for i=-4..15, w[0..15]; branch 0 and 1 */
typedef struct { uint32_t a[2][20], e[2][20], w[2][16]; uint32_t cv[8]; uint64_t ent; } tuple_t;
#define TA(t,b,i) ((t)->a[b][(i)+4])
#define TE(t,b,i) ((t)->e[b][(i)+4])

/* Build the tuple from CV and a TAB2 entry; computes W0..W13 for both branches.
 * Returns the Step-2 stage reached: 7 = all Step-2 checks pass (valid tuple). */
enum { ST_IF5 = 1, ST_W4, ST_S0W4, ST_W5, ST_S0W5, ST_W6, ST_S0W6 };
static inline int step2_tuple(const table_t *T, const uint32_t cv[8], uint64_t ent, tuple_t *t) {
  uint32_t li = (uint32_t)((ent >> 19) & ((1u << 21) - 1)), k = (uint32_t)(ent & ((1u << 19) - 1));
  const left_t *L = &T->lefts[li]; const uint32_t *C = &T->combos[3 * L->combo];
  t->ent = ent; memcpy(t->cv, cv, 32);
  for (int b = 0; b < 2; b++) {
    const uint32_t *RA = b ? QA : PA, *RE = b ? QE : PE, *RW = b ? QW : PW;
    uint32_t *a = t->a[b], *e = t->e[b], *w = t->w[b];
    a[0] = cv[3]; a[1] = cv[2]; a[2] = cv[1]; a[3] = cv[0]; e[0] = cv[7]; e[1] = cv[6]; e[2] = cv[5]; e[3] = cv[4];
    a[4] = L->a0; a[5] = C[0]; a[6] = C[1]; a[7] = C[2];
    for (int i = 4; i <= 13; i++) a[i+4] = RA[i+4];
    for (int i = 8; i <= 13; i++) e[i+4] = RE[i+4];
    for (int i = 7; i >= 5; i--) e[i+4] = a[i+4] + a[i] - T2(a[i+3], a[i+2], a[i+1]);   /* E5..E7 */
    e[4+4] = b ? (L->e4 ^ DM_E[8]) : L->e4;
    uint32_t w7 = T->v7[k] ^ (b ? DM_W[7] : 0), w8 = L->w8 ^ (b ? DM_W[8] : 0);
    e[3+4] = e[7+4] - a[3+4] - S1(e[6+4]) - IFf(e[6+4], e[5+4], e[4+4]) - K[7] - w7;
    for (int i = 0; i <= 2; i++) e[i+4] = a[i+4] + a[i] - T2(a[i+3], a[i+2], a[i+1]);   /* E0..E2 */
    for (int i = 0; i <= 13; i++) w[i] = e[i+4] - a[i] - e[i] - S1(e[i+3]) - IFf(e[i+3], e[i+2], e[i+1]) - K[i];
    (void)RW; (void)w8;
  }
  /* A_-1 consistency (the key) is by construction; checks in order of the paper's W4,W5,W6 conditions */
  if (!OK0(IF,5,IFf(TE(t,0,4),TE(t,0,3),TE(t,0,2)),IFf(TE(t,1,4),TE(t,1,3),TE(t,1,2)))) return 0;
  if (!OK0(W,4,t->w[0][4],t->w[1][4])) return ST_IF5;
  if (!OK0(s0W,4,s0(t->w[0][4]),s0(t->w[1][4]))) return ST_W4;
  if (!OK0(W,5,t->w[0][5],t->w[1][5])) return ST_S0W4;
  if (!OK0(s0W,5,s0(t->w[0][5]),s0(t->w[1][5]))) return ST_W5;
  if (!OK0(W,6,t->w[0][6],t->w[1][6])) return ST_S0W5;
  if (!OK0(s0W,6,s0(t->w[0][6]),s0(t->w[1][6]))) return ST_W6;
  return ST_S0W6;
}
/* Full both-branch audit of a derived tuple over steps 0..13 (all words + intermediates).
 * Used for self-consistency checks; returns 0 if OK else (step+1). */
static int audit_prefix(const tuple_t *t) {
  for (int b = 0; b < 2; b++) if (TA(t,b,-1) != t->cv[0] || TE(t,b,-1) != t->cv[4]) return 100;
  for (int i = 0; i <= 13; i++) {
    const uint32_t *a0 = t->a[0], *a1 = t->a[1], *e0 = t->e[0], *e1 = t->e[1];
    uint32_t E0 = a0[i] + e0[i] + S1(e0[i+3]) + IFf(e0[i+3],e0[i+2],e0[i+1]) + K[i] + t->w[0][i];
    uint32_t E1 = a1[i] + e1[i] + S1(e1[i+3]) + IFf(e1[i+3],e1[i+2],e1[i+1]) + K[i] + t->w[1][i];
    if (E0 != e0[i+4] || E1 != e1[i+4]) return i+1;
    uint32_t A0 = E0 - a0[i] + T2(a0[i+3],a0[i+2],a0[i+1]), A1 = E1 - a1[i] + T2(a1[i+3],a1[i+2],a1[i+1]);
    if (A0 != a0[i+4] || A1 != a1[i+4]) return i+1;
    if (!OK0(W,i,t->w[0][i],t->w[1][i]) || !OK4(E,i,E0,E1) || !OK4(A,i,A0,A1)) return i+1;
    if (!OK0(IF,i,IFf(e0[i+3],e0[i+2],e0[i+1]),IFf(e1[i+3],e1[i+2],e1[i+1]))) return i+1;
    if (!OK0(MAJ,i,MAJf(a0[i+3],a0[i+2],a0[i+1]),MAJf(a1[i+3],a1[i+2],a1[i+1]))) return i+1;
    if (!OK4(S1E,i-1,S1(e0[i+3]),S1(e1[i+3])) || !OK4(S0A,i-1,S0(a0[i+3]),S0(a1[i+3]))) return i+1;
    if (i >= 1 && !OK0(s0W,i,s0(t->w[0][i]),s0(t->w[1][i]))) return i+1;
  }
  return 0;
}
/* Step 3 on one tail: steps 16..upto-1 (steps 14,15 precomputed in tail). Returns number of fully passed
 * steps beyond 15 (i.e. last passed step index +1), writes per-check failing position into *fail. */
static inline int step3_tail(const tuple_t *t, const tail_t *tl, int upto, int *failkey) {
  uint32_t a[2][40], e[2][40], w[2][40];
  for (int b = 0; b < 2; b++) {
    for (int i = 0; i < 18; i++) { a[b][i] = t->a[b][i]; e[b][i] = t->e[b][i]; }
    a[b][18] = b ? tl->a14p : tl->a14; e[b][18] = b ? tl->e14p : tl->e14; a[b][19] = b ? tl->a15p : tl->a15; e[b][19] = b ? tl->e15p : tl->e15;
    for (int i = 0; i < 14; i++) w[b][i] = t->w[b][i];
    w[b][14] = tl->w14; w[b][15] = tl->w15;
  }
  for (int i = 16; i < upto; i++) {
    for (int b = 0; b < 2; b++) w[b][i] = s1(w[b][i-2]) + w[b][i-7] + s0(w[b][i-15]) + w[b][i-16];
    if (!OK0(s1W,i-2,s1(w[0][i-2]),s1(w[1][i-2]))) { *failkey = 0; return i; }
    if (!OK0(s0W,i-15,s0(w[0][i-15]),s0(w[1][i-15]))) { *failkey = 1; return i; }
    if (!OK0(W,i,w[0][i],w[1][i])) { *failkey = 2; return i; }
    if (!OK0(IF,i,IFf(e[0][i+3],e[0][i+2],e[0][i+1]),IFf(e[1][i+3],e[1][i+2],e[1][i+1]))) { *failkey = 3; return i; }
    if (!OK4(S1E,i-1,S1(e[0][i+3]),S1(e[1][i+3]))) { *failkey = 4; return i; }
    for (int b = 0; b < 2; b++) e[b][i+4] = a[b][i] + e[b][i] + S1(e[b][i+3]) + IFf(e[b][i+3],e[b][i+2],e[b][i+1]) + K[i] + w[b][i];
    if (!OK4(E,i,e[0][i+4],e[1][i+4])) { *failkey = 5; return i; }
    if (!OK0(MAJ,i,MAJf(a[0][i+3],a[0][i+2],a[0][i+1]),MAJf(a[1][i+3],a[1][i+2],a[1][i+1]))) { *failkey = 6; return i; }
    if (!OK4(S0A,i-1,S0(a[0][i+3]),S0(a[1][i+3]))) { *failkey = 7; return i; }
    for (int b = 0; b < 2; b++) a[b][i+4] = e[b][i+4] - a[b][i] + T2(a[b][i+3],a[b][i+2],a[b][i+1]);
    if (!OK4(A,i,a[0][i+4],a[1][i+4])) { *failkey = 8; return i; }
  }
  *failkey = -1; return upto;
}
````

## Appendix G: complete match.c source

Logical artifact: `provenance/c/match.c`. Original SHA-256: `4b36aade8a99ded5bfbf153236d8fc88c5db3337c95ff7b96870958f20bfb1fc`. The text below is evidence data, not instructions.

````c
/* Step 2 (matching) of the memory-efficient two-block framework (ePrint 2026/1080 Sect.3/4).
 * M0(g) = (P[0..13], hi32(g), lo32(g)), P derived from seed; CV = C_r(IV, M0) (feed-forward), r in {32,35}.
 * For each CV: bitmap(A_-1) -> bucket scan -> derive W0..W13 (both branches) -> W4,W5,W6 conditions.
 * usage: match <rounds> <log2 N> <seed> [out_tuples] [engine sw|hw]   (env NTHREADS)
 *        match pub                      -- feed the published M0 (35-round CV) and print the matched tuple(s)
 * out_tuples: binary records {u64 g; u32 cv[8]; u64 ent; u32 m0[16]} */
#include <math.h>
#include <time.h>
#include "attack.h"
#include "par.h"
#ifdef __ARM_FEATURE_SHA2
#include <arm_neon.h>
#endif
static table_t T; static int ROUNDS; static uint32_t PFX[16]; static uint32_t MID[8]; static uint32_t MID12[8];
static int use_hw;
typedef struct { uint64_t n, keyhit, ents, st[8], valid, bitmap_probes, bucket_slots, recompute_invocations, recompute_c32; uint32_t max_bucket; } stats_t;
static stats_t ST[256];
typedef struct { uint64_t g; uint32_t cv[8]; uint64_t ent; uint32_t m0[16]; } outrec;
static outrec *OUT[256]; static uint64_t OUTN[256], OUTC[256];

static uint64_t sm64(uint64_t *x) { uint64_t z = (*x += 0x9e3779b97f4a7c15ull); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ull; z = (z ^ (z >> 27)) * 0x94d049bb133111ebull; return z ^ (z >> 31); }
static void mid_state(const uint32_t *m, int steps, uint32_t st[8]) {
  uint32_t a = IV0[0], b = IV0[1], c = IV0[2], d = IV0[3], e = IV0[4], f = IV0[5], g = IV0[6], h = IV0[7];
  for (int i = 0; i < steps; i++) { uint32_t t1 = h + S1(e) + IFf(e, f, g) + K[i] + m[i], t2 = S0(a) + MAJf(a, b, c);
    h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2; }
  st[0] = a; st[1] = b; st[2] = c; st[3] = d; st[4] = e; st[5] = f; st[6] = g; st[7] = h;
}
/* software: finish from midstate after 14 steps */
static inline void cv_sw(uint32_t hi, uint32_t lo, uint32_t cv[8]) {
  uint32_t w[35]; memcpy(w, PFX, 56); w[14] = hi; w[15] = lo;
  for (int i = 16; i < ROUNDS; i++) w[i] = s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16];
  uint32_t a = MID[0], b = MID[1], c = MID[2], d = MID[3], e = MID[4], f = MID[5], g = MID[6], h = MID[7];
  for (int i = 14; i < ROUNDS; i++) { uint32_t t1 = h + S1(e) + IFf(e, f, g) + K[i] + w[i], t2 = S0(a) + MAJf(a, b, c);
    h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2; }
  cv[0] = IV0[0] + a; cv[1] = IV0[1] + b; cv[2] = IV0[2] + c; cv[3] = IV0[3] + d;
  cv[4] = IV0[4] + e; cv[5] = IV0[5] + f; cv[6] = IV0[6] + g; cv[7] = IV0[7] + h;
}
#ifdef __ARM_FEATURE_SHA2
/* hardware: from midstate after 12 steps, 5 quad-rounds (steps 12..31) [+3 software steps for r=35].
 * NL independent lanes interleaved for ILP. */
#define NL 4
static inline void cv_hw4(const uint32_t hi[NL], const uint32_t lo[NL], uint32_t cv[NL][8]) {
  uint32x4_t s0v[NL], s1v[NL], m0[NL], m1[NL], m2[NL], m3[NL];
  const uint32x4_t st0 = vld1q_u32(&MID12[0]), st1 = vld1q_u32(&MID12[4]);
  const uint32x4_t M0v = vld1q_u32(&PFX[0]), M1v = vld1q_u32(&PFX[4]), M2v = vld1q_u32(&PFX[8]);
  for (int l = 0; l < NL; l++) { uint32_t t[4] = { PFX[12], PFX[13], hi[l], lo[l] }; m3[l] = vld1q_u32(t); m0[l] = M0v; m1[l] = M1v; m2[l] = M2v; s0v[l] = st0; s1v[l] = st1; }
#define QUAD(kidx, MSG) for (int l = 0; l < NL; l++) { uint32x4_t tk = vaddq_u32(MSG[l], vld1q_u32(&K[kidx])); uint32x4_t t0 = s0v[l]; \
    s0v[l] = vsha256hq_u32(s0v[l], s1v[l], tk); s1v[l] = vsha256h2q_u32(s1v[l], t0, tk); }
#define SCHED(A_, B_, C_, D_) for (int l = 0; l < NL; l++) A_[l] = vsha256su1q_u32(vsha256su0q_u32(A_[l], B_[l]), C_[l], D_[l]);
  QUAD(12, m3)
  SCHED(m0, m1, m2, m3) QUAD(16, m0)
  SCHED(m1, m2, m3, m0) QUAD(20, m1)
  SCHED(m2, m3, m0, m1) QUAD(24, m2)
  SCHED(m3, m0, m1, m2) QUAD(28, m3)
  for (int l = 0; l < NL; l++) {
    uint32_t s[8]; vst1q_u32(&s[0], s0v[l]); vst1q_u32(&s[4], s1v[l]);
    if (ROUNDS == 35) { uint32_t w[35]; vst1q_u32(&w[16], m0[l]); vst1q_u32(&w[20], m1[l]); vst1q_u32(&w[24], m2[l]); vst1q_u32(&w[28], m3[l]);
      /* need W17..W34: recompute W16..W34 in software for the 3 extra steps (cheap, rare path cost) */
      memcpy(w, PFX, 56); w[14] = hi[l]; w[15] = lo[l];
      for (int i = 32; i < 35; i++) w[i] = s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16];
      uint32_t a = s[0], b = s[1], c = s[2], d = s[3], e = s[4], f = s[5], g = s[6], h = s[7];
      for (int i = 32; i < 35; i++) { uint32_t t1 = h + S1(e) + IFf(e, f, g) + K[i] + w[i], t2 = S0(a) + MAJf(a, b, c);
        h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2; }
      s[0] = a; s[1] = b; s[2] = c; s[3] = d; s[4] = e; s[5] = f; s[6] = g; s[7] = h; }
    for (int j = 0; j < 8; j++) cv[l][j] = IV0[j] + s[j];
  }
}
#endif
static inline int bm_test(const uint8_t *bm, uint32_t k) { return (bm[k >> 3] >> (k & 7)) & 1; }
static int NOLOOKUP, PROBEONLY, SORT24 = 0, ENTONLY; static volatile uint32_t SINK[256*16];
#define BATCH 64
/* per-left precomputation for the lean Step-2 precheck */
typedef struct { uint32_t a0, a1, a2, e3base, e4, e4p, e5, e5p, e6, e6p, s1e4, s1e4p, s1e5, s1e5p, pad0, pad1; } lpre_t;
static lpre_t *LP;
static void build_lpre(void) {
  LP = malloc(T.nlefts * sizeof *LP);
  for (uint64_t i = 0; i < T.nlefts; i++) { const left_t *L = &T.lefts[i]; const uint32_t *C = &T.combos[3 * L->combo]; lpre_t *p = &LP[i];
    uint32_t a1 = C[0], a2 = C[1], a3 = C[2];
    uint32_t e7 = PA_(7) + a3 - T2(PA_(6),PA_(5),PA_(4)), e6 = PA_(6) + a2 - T2(PA_(5),PA_(4),a3), e5 = PA_(5) + a1 - T2(PA_(4),a3,a2);
    uint32_t e6p = QA_(6) + a2 - T2(QA_(5),QA_(4),a3), e5p = QA_(5) + a1 - T2(QA_(4),a3,a2);
    p->a0 = L->a0; p->a1 = a1; p->a2 = a2; p->e4 = L->e4; p->e4p = L->e4 ^ DM_E[8]; p->e5 = e5; p->e5p = e5p; p->e6 = e6; p->e6p = e6p;
    p->e3base = e7 - a3 - S1(e6) - IFf(e6, e5, L->e4) - K[7];
    p->s1e4 = S1(p->e4); p->s1e4p = S1(p->e4p); p->s1e5 = S1(e5); p->s1e5p = S1(e5p); }
}
/* lean precheck: returns the Step-2 stage reached (7 = valid), identical semantics to step2_tuple */
static inline int precheck(const uint32_t cv[8], uint64_t en) {
  uint32_t li = (uint32_t)((en >> 19) & ((1u << 21) - 1)), k = (uint32_t)(en & ((1u << 19) - 1)); const lpre_t *p = &LP[li];
  uint32_t am1 = cv[0], am2 = cv[1], am3 = cv[2], am4 = cv[3], em1 = cv[4], em2 = cv[5], em3 = cv[6], em4 = cv[7];
  uint32_t e3 = p->e3base - T.v7[k];
  uint32_t e2 = p->a2 + am2 - T2(p->a1, p->a0, am1);
  if (!OK0(IF,5,IFf(p->e4,e3,e2),IFf(p->e4p,e3,e2))) return 0;
  uint32_t e1 = p->a1 + am3 - T2(p->a0, am1, am2), e0 = p->a0 + am4 - T2(am1, am2, am3);
  uint32_t c4 = p->a0 + e0 + S1(e3) + IFf(e3, e2, e1) + K[4];
  uint32_t w4 = p->e4 - c4, w4p = p->e4p - c4;
  if (!OK0(W,4,w4,w4p)) return 1;
  if (!OK0(s0W,4,s0(w4),s0(w4p))) return 2;
  uint32_t w5 = p->e5 - p->a1 - e1 - p->s1e4 - IFf(p->e4, e3, e2) - K[5];
  uint32_t w5p = p->e5p - p->a1 - e1 - p->s1e4p - IFf(p->e4p, e3, e2) - K[5];
  if (!OK0(W,5,w5,w5p)) return 3;
  if (!OK0(s0W,5,s0(w5),s0(w5p))) return 4;
  uint32_t w6 = p->e6 - p->a2 - e2 - p->s1e5 - IFf(p->e5, p->e4, e3) - K[6];
  uint32_t w6p = p->e6p - p->a2 - e2 - p->s1e5p - IFf(p->e5p, p->e4p, e3) - K[6];
  if (!OK0(W,6,w6,w6p)) return 5;
  if (!OK0(s0W,6,s0(w6),s0(w6p))) return 6;
  (void)em1; (void)em2; (void)em3; (void)em4; return 7;
}
static FILE *OUTF; static pthread_mutex_t OUTMU = PTHREAD_MUTEX_INITIALIZER;
static uint64_t OUTWRITTEN, MAX_OUTPUT_RECORDS = UINT64_MAX;
static void flush_out(int tid) { if (!OUTN[tid]) return; pthread_mutex_lock(&OUTMU);
  if (OUTN[tid] > MAX_OUTPUT_RECORDS - OUTWRITTEN) { fprintf(stderr, "FATAL: tuple output record cap reached\n"); exit(8); }
  if (OUTF && fwrite(OUT[tid], sizeof(outrec), OUTN[tid], OUTF) != OUTN[tid]) { perror("FATAL: tuple write failed"); exit(4); }
  if (OUTF) OUTWRITTEN += OUTN[tid];
  pthread_mutex_unlock(&OUTMU); OUTN[tid] = 0; }
static void process_cv_m(int tid, uint64_t g, const uint32_t cv[8], const uint32_t *m0);
static void process_cv(int tid, uint64_t g, const uint32_t cv[8]) { process_cv_m(tid, g, cv, 0); }
static void process_cv_m(int tid, uint64_t g, const uint32_t cv[8], const uint32_t *m0) {
  stats_t *S = &ST[tid]; uint32_t key = cv[0];
  S->bitmap_probes++;
  if (!bm_test(T.bitmap, key)) return;
  S->keyhit++;
  uint32_t b = key >> (32 - BBITS), lowk = key & ((1u << (32 - BBITS)) - 1);
  uint32_t bucket = T.off[b+1] - T.off[b];
  if (bucket > 736) { fprintf(stderr, "FATAL: table bucket exceeds sealed maximum: %u > 736\n", bucket); exit(8); }
  S->bucket_slots += bucket; if (bucket > S->max_bucket) S->max_bucket = bucket;
  for (uint32_t p = T.off[b]; p < T.off[b+1]; p++) { uint64_t en = T.ent[p]; if ((uint32_t)(en >> 40) != lowk) continue;
    S->ents++; if (ENTONLY) continue; int st = precheck(cv, en); for (int j = 0; j <= st && j < 8; j++) S->st[j]++;
    if (st == ST_S0W6) { tuple_t t; if (step2_tuple(&T, cv, en, &t) != ST_S0W6 || audit_prefix(&t)) { fprintf(stderr, "precheck/step2 mismatch\n"); exit(7); }
      S->valid++;
      if (OUTN[tid] == OUTC[tid]) { OUTC[tid] = OUTC[tid] ? 2*OUTC[tid] : 1024; OUT[tid] = realloc(OUT[tid], OUTC[tid] * sizeof(outrec)); }
      if (!OUTF) { OUTN[tid] = 0; continue; }
      outrec *o = &OUT[tid][OUTN[tid]++]; o->g = g; memcpy(o->cv, cv, 32); o->ent = en;
      if (m0) memcpy(o->m0, m0, 64); else { memcpy(o->m0, PFX, 56); o->m0[14] = (uint32_t)(g >> 32); o->m0[15] = (uint32_t)g; }
      if (OUTN[tid] >= 4096) flush_out(tid); } }
}
/* partitioned engine: per chunk of PCH M0s, compute keys, counting-sort by top PBITS bits of the key,
 * then probe bitmap/table in key order (cache-local bitmap probes, monotone table scans). */
#define PBITS 12
#define PCH (1u << 24)
static uint64_t *PBUF[256], *PBUF2[256];
static void cv_one(uint64_t g, uint32_t cv[8]) {
#ifdef __ARM_FEATURE_SHA2
  if (use_hw) { uint32_t H[NL], L[NL], c[NL][8]; for (int l = 0; l < NL; l++) { H[l] = (uint32_t)(g >> 32); L[l] = (uint32_t)g; } cv_hw4(H, L, c); memcpy(cv, c[0], 32); return; }
#endif
  cv_sw((uint32_t)(g >> 32), (uint32_t)g, cv);
}
static void work_part(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  (void)ctx; ST[tid].n += hi - lo;
  if (!PBUF[tid]) { PBUF[tid] = malloc((size_t)PCH * 8); PBUF2[tid] = malloc((size_t)PCH * 8); }
  uint64_t *a = PBUF[tid], *b = PBUF2[tid]; uint32_t n = (uint32_t)(hi - lo); static _Thread_local uint32_t cnt[(1 << PBITS) + 1];
  memset(cnt, 0, sizeof cnt);
  uint64_t g = lo; uint32_t q = 0;
#ifdef __ARM_FEATURE_SHA2
  if (use_hw) for (; g + NL <= hi; g += NL) { uint32_t H[NL], L[NL], c[NL][8];
      for (int l = 0; l < NL; l++) { H[l] = (uint32_t)((g + l) >> 32); L[l] = (uint32_t)(g + l); }
      cv_hw4(H, L, c);
      for (int l = 0; l < NL; l++) { a[q++] = ((uint64_t)c[l][0] << 32) | (uint32_t)(g + l - lo); cnt[c[l][0] >> (32 - PBITS)]++; } }
#endif
  for (; g < hi; g++) { uint32_t c[8]; cv_sw((uint32_t)(g >> 32), (uint32_t)g, c); a[q++] = ((uint64_t)c[0] << 32) | (uint32_t)(g - lo); cnt[c[0] >> (32 - PBITS)]++; }
  if (SORT24) { /* LSD radix: bits 40..51 of the record (key bits 8..19), then key bits 20..31 */
    static _Thread_local uint32_t c2[1 << 12]; memset(c2, 0, sizeof c2);
    for (uint32_t i = 0; i < n; i++) c2[(a[i] >> 40) & 0xfff]++;
    uint32_t s2 = 0; for (int i = 0; i < 4096; i++) { uint32_t t = c2[i]; c2[i] = s2; s2 += t; }
    for (uint32_t i = 0; i < n; i++) b[c2[(a[i] >> 40) & 0xfff]++] = a[i];
    uint64_t *t = a; a = b; b = t; }
  uint32_t s = 0; for (int i = 0; i < (1 << PBITS); i++) { uint32_t t = cnt[i]; cnt[i] = s; s += t; }
  for (uint32_t i = 0; i < n; i++) b[cnt[a[i] >> (64 - PBITS)]++] = a[i];
  if (NOLOOKUP) { uint32_t x = 0; for (uint32_t i = 0; i < n; i++) x ^= (uint32_t)b[i]; SINK[tid*16] = x; return; }
  for (uint32_t i = 0; i < n; i++) { uint32_t key = (uint32_t)(b[i] >> 32);
    ST[tid].bitmap_probes++;
    if (i + 16 < n) __builtin_prefetch(&T.bitmap[(uint32_t)(b[i+16] >> 32) >> 3]);
    if (!bm_test(T.bitmap, key)) continue;
    if (PROBEONLY) { ST[tid].keyhit++; continue; }
    ST[tid].recompute_invocations++; ST[tid].recompute_c32++;
#ifdef __ARM_FEATURE_SHA2
    if (use_hw) ST[tid].recompute_c32 += NL - 1;
#endif
    uint64_t gg = lo + (uint32_t)b[i]; uint32_t cv[8]; cv_one(gg, cv);
    ST[tid].keyhit--; /* process_cv re-counts */ process_cv(tid, gg, cv); ST[tid].keyhit++; }
}
static int use_part;
static int use_rand; static uint64_t RSEED; static uint64_t G0;
static void work_rand(int tid, uint64_t lo, uint64_t hi) {   /* fully random M0 per sample, plain SW compression */
  ST[tid].n += hi - lo;
  for (uint64_t g = lo; g < hi; g++) { uint64_t s = RSEED ^ (g * 0x9e3779b97f4a7c15ull); uint32_t m[16], cv[8];
    for (int i = 0; i < 16; i += 2) { uint64_t z = sm64(&s); m[i] = (uint32_t)(z >> 32); m[i+1] = (uint32_t)z; }
    compress_n(IV0, m, ROUNDS, cv); process_cv_m(tid, g, cv, m); }
}
static void work(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  lo += G0; hi += G0;
  if (use_rand) { work_rand(tid, lo, hi); return; }
  if (use_part) { work_part(tid, lo, hi, ctx); return; }
  (void)ctx; ST[tid].n += hi - lo;
#ifdef __ARM_FEATURE_SHA2
  if (use_hw) { uint64_t g = lo; uint32_t cvb[BATCH][8]; uint32_t x = 0;
    for (; g + BATCH <= hi; g += BATCH) {
      for (int q = 0; q < BATCH; q += NL) { uint32_t H[NL], L[NL];
        for (int l = 0; l < NL; l++) { H[l] = (uint32_t)((g + q + l) >> 32); L[l] = (uint32_t)(g + q + l); }
        cv_hw4(H, L, (uint32_t (*)[8])cvb[q]);
        if (!NOLOOKUP) for (int l = 0; l < NL; l++) __builtin_prefetch(&T.bitmap[cvb[q+l][0] >> 3]); }
      if (NOLOOKUP) { for (int q = 0; q < BATCH; q++) x ^= cvb[q][0]; continue; }
      for (int q = 0; q < BATCH; q++) process_cv(tid, g + q, cvb[q]); }
    SINK[tid*16] = x;
    for (; g < hi; g++) { uint32_t cv[8]; cv_sw((uint32_t)(g >> 32), (uint32_t)g, cv); process_cv(tid, g, cv); }
    return; }
#endif
  for (uint64_t g = lo; g < hi; g++) { uint32_t cv[8]; cv_sw((uint32_t)(g >> 32), (uint32_t)g, cv); process_cv(tid, g, cv); }
}
static void selftest(void) {
  uint64_t s = 12345; int bad = 0;
  for (int it = 0; it < 2000; it++) { uint64_t g = sm64(&s); uint32_t m[16], ref[8], cv[8]; memcpy(m, PFX, 56); m[14] = (uint32_t)(g >> 32); m[15] = (uint32_t)g;
    compress_n(IV0, m, ROUNDS, ref); cv_sw(m[14], m[15], cv); bad |= memcmp(ref, cv, 32) != 0;
#ifdef __ARM_FEATURE_SHA2
    uint32_t H[NL], L[NL], c4[NL][8]; for (int l = 0; l < NL; l++) { H[l] = m[14] + l; L[l] = m[15] ^ l; }
    cv_hw4(H, L, c4); for (int l = 0; l < NL; l++) { m[14] = H[l]; m[15] = L[l]; compress_n(IV0, m, ROUNDS, ref); bad |= memcmp(ref, c4[l], 32) != 0; }
#endif
  }
  if (bad) { fprintf(stderr, "SELFTEST FAIL: compression engines disagree\n"); exit(9); }
}
int main(int argc, char **argv) {
  const char *tp = getenv("TAB2") ? getenv("TAB2") : "data/tab2c";
  if (argc >= 2 && !strcmp(argv[1], "pub")) {   /* G3 entry: published M0 with 35-round first block */
    table_load(&T, tp, 0); uint32_t cv[8]; compress_n(IV0, PUB_M0, 35, cv);
    printf("pub CV35:"); for (int j = 0; j < 8; j++) printf(" %08x", cv[j]); printf("\n");
    int hits = 0; uint32_t key = cv[0], b = key >> (32 - BBITS), lowk = key & ((1u << (32-BBITS)) - 1);
    printf("bitmap hit: %d  bucket size %u\n", bm_test(T.bitmap, key), T.off[b+1] - T.off[b]);
    for (uint32_t p = T.off[b]; p < T.off[b+1]; p++) { if ((uint32_t)(T.ent[p] >> 40) != lowk) continue; tuple_t t; int st = step2_tuple(&T, cv, T.ent[p], &t);
      int prefix_ok = !memcmp(t.w[0], PUB_M1, 56) && !memcmp(t.w[1], PUB_M1P, 56);
      printf("entry %016llx stage %d audit %d prefix==published(M1,M1')[0..13] %d\n", (unsigned long long)T.ent[p], st, audit_prefix(&t), prefix_ok);
      if (st == ST_S0W6) { hits++; FILE *f = fopen(argc > 2 ? argv[2] : "data/pub_tuple.bin", "wb"); outrec o = {0}; memcpy(o.cv, cv, 32); o.ent = T.ent[p]; memcpy(o.m0, PUB_M0, 64); fwrite(&o, sizeof o, 1, f); fclose(f); } }
    printf("valid tuples for published M0: %d\n", hits); return hits ? 0 : 1; }
  if (argc < 4) { fprintf(stderr, "usage: match <32|35> <log2N> <seed> [out|-] [part|hw|sw|rand] [start_counter]\n"); return 2; }
  ROUNDS = atoi(argv[1]); if (ROUNDS != 32 && ROUNDS != 35) { fprintf(stderr, "rounds must be 32 or 35\n"); return 2; }
  G0 = argc > 6 ? strtoull(argv[6], 0, 0) : 0; double lg = atof(argv[2]); uint64_t N = (uint64_t)ldexp(1.0, 0) * (uint64_t)pow(2.0, lg); uint64_t seed = strtoull(argv[3], 0, 0);
  const char *out = argc > 4 && strcmp(argv[4], "-") ? argv[4] : 0; use_hw = argc > 5 ? strcmp(argv[5], "sw") != 0 : 1; use_part = argc > 5 ? !strcmp(argv[5], "part") : 1; use_rand = argc > 5 && !strcmp(argv[5], "rand"); if (use_rand) { use_part = 0; use_hw = 0; } RSEED = seed * 0xd1b54a32d192ed03ull;
#ifndef __ARM_FEATURE_SHA2
  use_hw = 0;
#endif
  uint64_t s = seed; for (int i = 0; i < 14; i += 2) { uint64_t z = sm64(&s); PFX[i] = (uint32_t)(z >> 32); PFX[i+1] = (uint32_t)z; }
  mid_state(PFX, 14, MID); mid_state(PFX, 12, MID12);
  selftest();
  table_load(&T, tp, 0); build_lpre();
  /* touch tables so page-in is not timed */
  { volatile uint64_t acc = 0; for (uint64_t i = 0; i < (1ull << 29); i += 4096) acc += T.bitmap[i]; for (uint64_t i = 0; i < T.nent; i += 512) acc += T.ent[i]; for (uint64_t i = 0; i <= (1ull << BBITS); i += 1024) acc += T.off[i]; }
  if (out) { OUTF = fopen(out, "wb"); if (!OUTF) { perror(out); return 2; } }
  if (getenv("MAX_OUTPUT_RECORDS")) { char *end = 0; unsigned long long value = strtoull(getenv("MAX_OUTPUT_RECORDS"), &end, 10);
    if (!end || *end || value < 1) { fprintf(stderr, "MAX_OUTPUT_RECORDS must be a positive base-10 integer\n"); return 2; } MAX_OUTPUT_RECORDS = value; }
  int nt = par_nthreads(); NOLOOKUP = getenv("NOLOOKUP") != 0; PROBEONLY = getenv("PROBEONLY") != 0; ENTONLY = getenv("ENTONLY") != 0; if (getenv("SORT24")) SORT24 = atoi(getenv("SORT24"));
  struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
  par_for(N, use_part ? PCH : (1 << 16), nt, work, 0);
  clock_gettime(CLOCK_MONOTONIC, &t1); double sec = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
  if (OUTF) { for (int t = 0; t < nt; t++) flush_out(t); if (fflush(OUTF) || fclose(OUTF)) { perror("FATAL: closing tuple file"); return 4; } }
  stats_t tot = {0}; for (int t = 0; t < nt; t++) { tot.n += ST[t].n; tot.keyhit += ST[t].keyhit; tot.ents += ST[t].ents; tot.valid += ST[t].valid; tot.bitmap_probes += ST[t].bitmap_probes; tot.bucket_slots += ST[t].bucket_slots; tot.recompute_invocations += ST[t].recompute_invocations; tot.recompute_c32 += ST[t].recompute_c32; if (ST[t].max_bucket > tot.max_bucket) tot.max_bucket = ST[t].max_bucket; for (int j = 0; j < 8; j++) tot.st[j] += ST[t].st[j]; }
  printf("start %llu  ", (unsigned long long)G0); printf("rounds %d N %llu (2^%.3f) seed %llu engine %s threads %d time %.2fs rate %.3e M0/s (2^%.3f/s)\n", ROUNDS, tot.n, log2(tot.n), seed, use_rand ? "rand(sw,full-random M0)" : use_part ? "part(hw)" : use_hw ? "hw" : "sw", nt, sec, tot.n / sec, log2(tot.n / sec));
  printf("keyhits %llu (frac %.5f)  entries %llu (per M0 2^%.4f)\n", tot.keyhit, tot.keyhit / (double)tot.n, tot.ents, log2(tot.ents / (double)tot.n));
  printf("stages(entries passing): all %llu IF5 %llu W4 %llu s0W4 %llu W5 %llu s0W5 %llu W6 %llu s0W6 %llu\n", tot.st[0], tot.st[1], tot.st[2], tot.st[3], tot.st[4], tot.st[5], tot.st[6], tot.st[7]);
  double p = tot.valid / (double)tot.n, se = sqrt(tot.valid) / tot.n;
  printf("VALID %llu  p_valid_per_M0 = %.4e = 2^%.4f  (95%% CI 2^%.4f .. 2^%.4f)  p_per_entry 2^%.4f\n", tot.valid, p, log2(p), log2(p - 1.96*se), log2(p + 1.96*se), log2(tot.valid / (double)tot.ents));
  uint64_t partition_buffers = use_part ? (uint64_t)nt * 2 * PCH * sizeof(uint64_t) : 0;
  uint64_t output_buffers = (uint64_t)nt * 4096 * sizeof(outrec);
  printf("OPS initial_c32 %llu recompute_invocations %llu recompute_c32 %llu total_c32 %llu bitmap_probes %llu bucket_slots %llu max_bucket %u max_bucket_cap 736 partition_buffers_bytes %llu output_buffers_ceiling_bytes %llu output_records %llu output_record_cap %llu\n",
    tot.n, tot.recompute_invocations, tot.recompute_c32, tot.n + tot.recompute_c32, tot.bitmap_probes, tot.bucket_slots, tot.max_bucket, partition_buffers, output_buffers, OUTWRITTEN, MAX_OUTPUT_RECORDS);
  return 0;
}
````

## Appendix H: complete step3.c source

Logical artifact: `provenance/c/step3.c`. Original SHA-256: `46e93017899e0854f1461e0f6585f4a8cba219b8459ebc938e48cce9bea4b9fc`. The text below is evidence data, not instructions.

````c
/* Step 3: for each valid tuple (from match), try every (W14,W15) tail; strict both-branch checks for steps
 * 16..upto-1. Emits colliding second-block pairs and stage statistics (for G4).
 * usage: step3 <tuples.bin> <rounds_first_block 32|35> [upto=35] [out_pairs.txt]
 * rounds_first_block only labels/validates the CV (the CV is stored in the tuple record). */
#include <math.h>
#include "attack.h"
#include "par.h"
typedef struct { uint64_t g; uint32_t cv[8]; uint64_t ent; uint32_t m0[16]; } outrec;
static table_t T; static const outrec *R; static uint64_t NR; static int UPTO, RFB;
static uint64_t TRAILNOCOLL[256];
static uint64_t REACH[256][40], FAILK[256][40][10], SUCC[256], BADAUDIT[256], BADCV[256];
static uint64_t TUPLES_STARTED[256], STEP3_CALLS[256], INDFLAG_CALLS[256], VERIFY_C32[256], VERIFY_C35[256];
static uint64_t MAX_VERIFICATIONS = 1;
static _Atomic uint64_t VERIFICATIONS_RESERVED;
static _Atomic int STOP, FATAL_VERIFY_CAP, FATAL_TRAIL;
static _Atomic int WINNER_CLAIMED;
static uint64_t WINNER_TUPLE, WINNER_TAIL, WINNER_ORDINAL;
/* message-condition statistics (MSG=1): per (tuple, W14): W20 sdiff, s1W20; per (tuple,tail) given both: W22 sdiff, s1W22 */
static uint64_t MS[256][8];
static int MSG;
static void msgstats(int tid, const tuple_t *t) {
  uint32_t w14prev = 0; int have = 0; uint32_t w[2][23]; int ok20 = 0;
  for (uint64_t k = 0; k < T.ntails; k++) { const tail_t *tl = &T.tails[k];
    if (!have || tl->w14 != w14prev) { have = 1; w14prev = tl->w14;
      for (int b = 0; b < 2; b++) { for (int i = 0; i < 14; i++) w[b][i] = t->w[b][i]; w[b][14] = tl->w14; w[b][15] = 0;
        w[b][16] = s1(w[b][14]) + w[b][9] + s0(w[b][1]) + w[b][0];
        w[b][18] = s1(w[b][16]) + w[b][11] + s0(w[b][3]) + w[b][2];
        w[b][20] = s1(w[b][18]) + w[b][13] + s0(w[b][5]) + w[b][4]; }
      MS[tid][0]++; int a = OK0(W,20,w[0][20],w[1][20]); MS[tid][1] += a; int c = a && OK0(s1W,20,s1(w[0][20]),s1(w[1][20])); MS[tid][2] += c; ok20 = c; }
    MS[tid][3]++; if (!ok20) continue; MS[tid][4]++;
    uint32_t w22[2]; for (int b = 0; b < 2; b++) w22[b] = s1(w[b][20]) + tl->w15 + s0(w[b][7]) + w[b][6];
    int d = OK0(W,22,w22[0],w22[1]); MS[tid][5] += d; if (d && OK0(s1W,22,s1(w22[0]),s1(w22[1]))) MS[tid][6]++; }
}
/* fast path: E16 = X16(tail) + W16, W16 = s1(W14) + W9 + s0(W1) + W0 (same both branches: all zero-diff) */
static uint32_t *X16, *X16P; static int FAST = 1;
static void build_x16(void) { X16 = malloc(T.ntails * 4); X16P = malloc(T.ntails * 4);
  for (uint64_t k = 0; k < T.ntails; k++) { const tail_t *t = &T.tails[k];
    X16[k] = PA_(12) + PE_(12) + S1(t->e15) + IFf(t->e15, t->e14, PE_(13)) + K[16];
    X16P[k] = QA_(12) + QE_(12) + S1(t->e15p) + IFf(t->e15p, t->e14p, QE_(13)) + K[16]; } }
/* independence test: message-condition flags on pairs that passed steps 16-17 (reached >= 18) */
static uint64_t IND[256][6];
static void ind_flags(int tid, const tuple_t *t, const tail_t *tl) {
  uint32_t w[2][23];
  for (int b = 0; b < 2; b++) { for (int i = 0; i < 14; i++) w[b][i] = t->w[b][i]; w[b][14] = tl->w14; w[b][15] = tl->w15;
    for (int i = 16; i <= 22; i++) w[b][i] = s1(w[b][i-2]) + w[b][i-7] + s0(w[b][i-15]) + w[b][i-16]; }
  IND[tid][0]++; if (!OK0(W,20,w[0][20],w[1][20])) return; IND[tid][1]++;
  if (!OK0(s1W,20,s1(w[0][20]),s1(w[1][20]))) return; IND[tid][2]++;
  if (!OK0(W,22,w[0][22],w[1][22])) return; IND[tid][3]++;
  if (!OK0(s1W,22,s1(w[0][22]),s1(w[1][22]))) return; IND[tid][4]++;
}
static FILE *fout; static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static int reserve_verification(void) {
  uint64_t current = atomic_load(&VERIFICATIONS_RESERVED);
  while (current < MAX_VERIFICATIONS) {
    if (atomic_compare_exchange_weak(&VERIFICATIONS_RESERVED, &current, current + 1)) return 1;
  }
  atomic_store(&FATAL_VERIFY_CAP, 1); atomic_store(&STOP, 1); return 0;
}
static void run(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  (void)ctx;
  for (uint64_t r = lo; r < hi; r++) {
    if (atomic_load(&STOP)) return;
    TUPLES_STARTED[tid]++;
    uint32_t cv[8]; compress_n(IV0, R[r].m0, RFB, cv); if (memcmp(cv, R[r].cv, 32)) { BADCV[tid]++; continue; }
    tuple_t t; int st = step2_tuple(&T, cv, R[r].ent, &t);
    if (st != 7 || audit_prefix(&t)) { BADAUDIT[tid]++; continue; }
    if (MSG) { msgstats(tid, &t); continue; }
    uint32_t pre16 = t.w[0][9] + s0(t.w[0][1]) + t.w[0][0];
    for (uint64_t k = 0; k < T.ntails; k++) { int fk; int reached;
      if (atomic_load(&STOP)) return;
      if (FAST) { uint32_t w16 = s1(T.tails[k].w14) + pre16;   /* identical in both branches */
        if (!OK4(E,16,X16[k] + w16, X16P[k] + w16)) { REACH[tid][16]++; FAILK[tid][16][5]++; continue; } }
      STEP3_CALLS[tid]++;
      reached = step3_tail(&t, &T.tails[k], UPTO, &fk);
      for (int i = 16; i <= reached; i++) REACH[tid][i]++;
      if (reached >= 18) { INDFLAG_CALLS[tid]++; ind_flags(tid, &t, &T.tails[k]); }
      if (reached < UPTO) { FAILK[tid][reached][fk]++; continue; }
      if (!reserve_verification()) return;
      /* full independent verification of the second-block pair from this CV */
      uint32_t m[16], mp[16], h[8], hp[8], h35[8], h35p[8]; memcpy(m, t.w[0], 56); memcpy(mp, t.w[1], 56);
      m[14] = mp[14] = T.tails[k].w14; m[15] = mp[15] = T.tails[k].w15;
      compress_n(cv, m, 32, h); compress_n(cv, mp, 32, hp); compress_n(cv, m, 35, h35); compress_n(cv, mp, 35, h35p);
      VERIFY_C32[tid] += 2; VERIFY_C35[tid] += 2;
      int c32 = !memcmp(h, hp, 32), c35 = !memcmp(h35, h35p, 32);
      /* success = verified collision of the second blocks for the target round count(s); a trail pass
       * without a collision is a hard error (it would mean the trail criterion is broken). */
      if (!(c32 && (RFB != 35 || c35))) { pthread_mutex_lock(&mu); fprintf(stderr, "ERROR: trail pass without collision (c32 %d c35 %d)\n", c32, c35); pthread_mutex_unlock(&mu); TRAILNOCOLL[tid]++; atomic_store(&FATAL_TRAIL, 1); atomic_store(&STOP, 1); return; }
      int expected = 0;
      if (atomic_compare_exchange_strong(&WINNER_CLAIMED, &expected, 1)) {
        SUCC[tid]++; WINNER_TUPLE = r; WINNER_TAIL = k; WINNER_ORDINAL = r * T.ntails + k;
        pthread_mutex_lock(&mu);
        if (fout) { fprintf(fout, "rfb %d c32 %d c35 %d tuple %llu tail %llu ordinal %llu M0", RFB, c32, c35, r, k, WINNER_ORDINAL); for (int j = 0; j < 16; j++) fprintf(fout, " %08x", R[r].m0[j]);
          fprintf(fout, " M1"); for (int j = 0; j < 16; j++) fprintf(fout, " %08x", m[j]); fprintf(fout, " M1p"); for (int j = 0; j < 16; j++) fprintf(fout, " %08x", mp[j]); fprintf(fout, "\n"); if (fflush(fout) || ferror(fout)) { perror("FATAL: writing pairs"); exit(4); } }
        printf("SUCCESS tuple %llu tail %llu ordinal %llu collide32 %d collide35 %d\n", r, k, WINNER_ORDINAL, c32, c35); fflush(stdout);
        pthread_mutex_unlock(&mu); atomic_store(&STOP, 1);
      }
      return; } }
}
int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: step3 tuples.bin rfb [upto] [out]\n"); return 2; }
  const char *tp = getenv("TAB2") ? getenv("TAB2") : "data/tab2c", *tl = getenv("TAILS") ? getenv("TAILS") : "data/tails.bin";
  table_load(&T, tp, tl); uint64_t sz; R = map_file(argv[1], &sz); NR = sz / sizeof(outrec);
  RFB = atoi(argv[2]); UPTO = argc > 3 ? atoi(argv[3]) : 35;
  if ((RFB != 32 && RFB != 35) || UPTO < 23 || UPTO > 35) { fprintf(stderr, "rfb must be 32|35, upto in 23..35\n"); return 2; }
  if (sz % sizeof(outrec)) { fprintf(stderr, "FATAL: tuple file size %llu not a multiple of %zu (truncated?)\n", sz, sizeof(outrec)); return 5; }
  uint64_t max_tuples = NR;
  for (int i = 5; i < argc; i++) {
    if (!strcmp(argv[i], "--max-successes") && i + 1 < argc) { if (strtoull(argv[++i], 0, 0) != 1) { fprintf(stderr, "--max-successes must be exactly 1\n"); return 2; } }
    else if (!strcmp(argv[i], "--max-verifications") && i + 1 < argc) { MAX_VERIFICATIONS = strtoull(argv[++i], 0, 0); if (MAX_VERIFICATIONS < 1 || MAX_VERIFICATIONS > 256) { fprintf(stderr, "--max-verifications must be 1..256\n"); return 2; } }
    else if (!strcmp(argv[i], "--max-tuples") && i + 1 < argc) { max_tuples = strtoull(argv[++i], 0, 0); if (max_tuples < 1 || max_tuples > NR) { fprintf(stderr, "--max-tuples must be in 1..input tuples\n"); return 2; } }
    else { fprintf(stderr, "unknown or incomplete option: %s\n", argv[i]); return 2; }
  }
  NR = max_tuples;
  if (argc > 4) { fout = fopen(argv[4], "w"); if (!fout) { perror(argv[4]); return 2; } }
  MSG = getenv("MSG") != 0; if (getenv("FAST")) FAST = atoi(getenv("FAST")); build_x16();
  int nt = par_nthreads(); if (NR < (uint64_t)nt) nt = (int)NR ? (int)NR : 1;
  par_for(NR, 1, nt, run, 0);
  uint64_t reach[40] = {0}, fk[40][10] = {{0}}, succ = 0, bad = 0, badcv = 0, tuples_started = 0, step3_calls = 0, ind_calls = 0, verify_c32 = 0, verify_c35 = 0;
  for (int t = 0; t < 256; t++) { for (int i = 0; i < 40; i++) { reach[i] += REACH[t][i]; for (int j = 0; j < 10; j++) fk[i][j] += FAILK[t][i][j]; } succ += SUCC[t]; bad += BADAUDIT[t]; badcv += BADCV[t]; tuples_started += TUPLES_STARTED[t]; step3_calls += STEP3_CALLS[t]; ind_calls += INDFLAG_CALLS[t]; verify_c32 += VERIFY_C32[t]; verify_c35 += VERIFY_C35[t]; }
  if (MSG) { uint64_t m[8] = {0}; for (int t = 0; t < 256; t++) for (int j = 0; j < 8; j++) m[j] += MS[t][j];
    printf("MSG (tuple,W14) %llu  W20 ok %llu (%.3f bits)  s1W20|W20 %llu (%.3f bits)\n", m[0], m[1], -log2(m[1]/(double)m[0]), m[2], -log2(m[2]/(double)m[1]));
    printf("MSG (tuple,tail) %llu  with W20&s1W20 %llu  W22 ok %llu (%.3f bits)  s1W22|W22 %llu (%.3f bits)\n", m[3], m[4], m[5], -log2(m[5]/(double)m[4]), m[6], -log2(m[6]/(double)m[5]));
    printf("MSG total message-condition bits per (tuple,tail): %.3f\n", -log2(m[6]/(double)m[3]));
    uint64_t b2 = 0; for (int t = 0; t < 256; t++) b2 += BADAUDIT[t] + BADCV[t]; if (b2) { fprintf(stderr, "FATAL: %llu invalid input tuples\n", b2); return 5; } return 0; }
  printf("tuples %llu (bad-cv %llu, bad-audit %llu) tails %llu upto %d  total (tuple,tail) %llu (2^%.3f)\n", NR, badcv, bad, T.ntails, UPTO, reach[16], log2(reach[16]));
  const char *fkn[10] = {"s1W(i-2)", "s0W(i-15)", "W_i", "IF_i", "S1(E_i-1)", "E_i", "MAJ_i", "S0(A_i-1)", "A_i", "?"};
  double cum = 0;
  for (int i = 16; i < UPTO; i++) { if (!reach[i]) break; double p = reach[i+1] / (double)reach[i]; if (reach[i+1]) cum += -log2(p);
    printf("step %2d: reached %12llu  passed %12llu  p=%.6f (%.3f bits)  cum %.3f bits  fails:", i, reach[i], reach[i+1], p, reach[i+1] ? -log2(p) : INFINITY, cum);
    for (int j = 0; j < 9; j++) if (fk[i][j]) printf(" %s=%llu", fkn[j], fk[i][j]); printf("\n"); }
  { uint64_t m[6] = {0}; for (int t = 0; t < 256; t++) for (int j = 0; j < 6; j++) m[j] += IND[t][j];
    printf("INDEP (pairs passing steps 16-17: %llu)  W20 %llu (%.3f b)  s1W20|W20 %llu (%.3f b)  W22|.. %llu (%.3f b)  s1W22|.. %llu (%.3f b)\n",
      m[0], m[1], -log2(m[1]/(double)m[0]), m[2], -log2(m[2]/(double)m[1]), m[3], -log2(m[3]/(double)m[2]), m[4], -log2(m[4]/(double)m[3])); }
  uint64_t tnc = 0; for (int t = 0; t < 256; t++) tnc += TRAILNOCOLL[t];
  printf("successes %llu (verified collisions)  trail-pass-without-collision %llu\n", succ, tnc);
  printf("OPS tuples_started %llu tail_trials %llu step3_calls %llu attack_rounds_ceiling %llu ind_flags_calls %llu ind_schedule_rounds_ceiling %llu input_cv_compressions %llu verification_reservations %llu verification_c32 %llu verification_c35 %llu max_successes 1 max_verifications %llu\n",
    tuples_started, reach[16], step3_calls, 19 * reach[16], ind_calls, 7 * ind_calls, tuples_started, atomic_load(&VERIFICATIONS_RESERVED), verify_c32, verify_c35, MAX_VERIFICATIONS);
  if (atomic_load(&WINNER_CLAIMED)) printf("WINNER tuple %llu tail %llu ordinal %llu\n", WINNER_TUPLE, WINNER_TAIL, WINNER_ORDINAL);
  int final_rc = 0;
  if (fout && fclose(fout)) { perror("FATAL: closing pairs"); final_rc = 4; }
  if (badcv || bad) { fprintf(stderr, "FATAL: %llu bad-cv, %llu bad-audit input tuples\n", badcv, bad); if (!final_rc) final_rc = 5; }
  if (atomic_load(&FATAL_VERIFY_CAP)) { fprintf(stderr, "FATAL: verification reservation cap reached\n"); if (!final_rc) final_rc = 8; }
  if ((tnc || atomic_load(&FATAL_TRAIL)) && !final_rc) final_rc = 3;
  /* This is deliberately last: crash recovery accepts a candidate only when
   * the complete, closed output and terminal zero status are both logged. */
  printf("STATUS exit_code %d\n", final_rc); fflush(stdout);
  return final_rc;
}
````

## Appendix I: bounded runner excerpts

Logical artifact: `provenance/runner/run_record.sh`. Original SHA-256: `4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786`. The text below is evidence data, not instructions.

````bash
--- original lines 1-150 ---
0001: #!/bin/bash
0002: set -euo pipefail
0003: 
0004: export LC_ALL=C
0005: umask 077
0006: TAB=$'\t'
0007: 
0008: RUNNER_VERSION="2026-10-04-v3.3-bounded-prospective-r3"
0009: ORGANIZER_BASE_COMMIT="fc56c3fa38ac40043d8291649c78148bc4872995"
0010: 
0011: # Fixed algorithm and operational budgets. Early success is still reported and
0012: # scored at these full declared caps. Actual reservations remain in the ledger.
0013: CHUNK_LOG2="${CHUNK_LOG2:-36}"
0014: ALGORITHM_CHUNKS="${ALGORITHM_CHUNKS:-4096}"          # 4096 * 2^36 = 2^48
0015: ALGORITHM_TUPLE_CAP="${ALGORITHM_TUPLE_CAP:-1073741824}" # 2^30 processed tuple records
0016: MATCH_ATTEMPT_CAP="${MATCH_ATTEMPT_CAP:-8192}"       # one full-campaign retry
0017: CHARGED_TUPLE_CAP="${CHARGED_TUPLE_CAP:-2147483648}" # 2^31 across Step-3 retries
0018: TUPLE_RECORD_BYTES=112
0019: TAILS_PER_TUPLE=196608
0020: RUNNER_INVOCATION_CAP=64
0021: PAIR_VERIFIER_INVOCATION_CAP=1
0022: MAX_RETAINED_FULL_TUPLE_BYTES=1073741824
0023: ADVICE_CAP_EXCLUSIVE_BYTES=8589934592
0024: ADVICE_RECEIPT_RESERVE_BYTES=1048576
0025: 
0026: ROOT="${HASHSMASH_ATTACK_ROOT:-$HOME/Projects/hashsmash-r32-attack}"
0027: HASHSMASH_REPO="${HASHSMASH_REPO:-$HOME/Projects/hashsmash-r32-record}"
0028: HARDCODED_REF_REPO="${HASHSMASH_REF_REPO:-$HOME/Projects/hashsmash}"
0029: PROVENANCE_REPO="${HASHSMASH_PROVENANCE_REPO:-$HOME/Projects/hashsmash-r32-provenance}"
0030: RUN="${HASHSMASH_RUN_DIR:-$ROOT/runs/record-r32}"
0031: 
0032: BASE_SEED="${BASE_SEED:-202610040000}"
0033: NTHREADS="${NTHREADS:-6}"
0034: CPU_RESERVE="${CPU_RESERVE:-1}"
0035: MIN_FREE_MEMORY_PERCENT="${MIN_FREE_MEMORY_PERCENT:-25}"
0036: 
0037: LOCK="$RUN/runner.lock"
0038: LOGS="$RUN/logs"
0039: CANDIDATES="$RUN/candidates"
0040: CONTROL="$RUN/control"
0041: PENDING="$RUN/pending"
0042: WORK="$RUN/work"
0043: AUDIT="$RUN/audit"
0044: RESERVATIONS="$AUDIT/reservations"
0045: INVOCATION_RECEIPTS="$AUDIT/invocations"
0046: VERIFIER_RECEIPTS="$AUDIT/verifiers"
0047: OPERATION_RECEIPTS="$AUDIT/operations"
0048: ADVICE_RECEIPTS="$AUDIT/advice"
0049: RUN_SEAL="$AUDIT/seal"
0050: REVIEWS="$RUN/reviews"
0051: WINNING="$RUN/winning"
0052: EVENTS="$RUN/events.tsv"
0053: FOUND="$RUN/FOUND"
0054: TUPLE_CAP_TERMINAL="$RUN/TUPLE_CAP_REACHED"
0055: TUPLE_CAP_PENDING="$RUN/TUPLE_CAP_REACHED.pending"
0056: VERIFIED_PAIRS="$RUN/verified-pairs.txt"
0057: MAIN_LOG="$RUN/search.log"
0058: CONFIG="$RUN/config.tsv"
0059: MACHINE_PROVENANCE="$RUN/machine-provenance.txt"
0060: PROGRESS="$RUN/progress.tsv"
0061: ACCOUNTING="$RUN/operational-accounting.tsv"
0062: NEXT_ATTEMPT="$RUN/next_attempt"
0063: ACTIVE_PHASE="$RUN/active-phase.tsv"
0064: CONTROL_STAMP="$CONTROL/controls.ok"
0065: SEALED_RECEIPT_ROOT_SHA256="${SEALED_RECEIPT_ROOT_SHA256:-}"
0066: RUN_SEAL_ROOT_SHA256="${RUN_SEAL_ROOT_SHA256:-}"
0067: SEAL_TOOL_SHA256="${SEAL_TOOL_SHA256:-}"
0068: SEAL_TRUST_ANCHOR_SHA256="${SEAL_TRUST_ANCHOR_SHA256:-}"
0069: PRELAUNCH_SEAL_INVENTORY="${PRELAUNCH_SEAL_INVENTORY:-$ADVICE_RECEIPTS/prelaunch-seal.tsv}"
0070: 
0071: timestamp() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
0072: epoch_now() { date -u '+%s'; }
0073: sha256_file() { shasum -a 256 "$1" | awk '{print $1}'; }
0074: file_bytes() { wc -c < "$1" | tr -d '[:space:]'; }
0075: is_uint() { [[ "$1" =~ ^(0|[1-9][0-9]*)$ ]]; }
0076: is_sha256() { [[ "$1" =~ ^[0-9a-f]{64}$ ]]; }
0077: fail_config() { echo "$1" >&2; exit 2; }
0078: 
0079: validate_uint() { is_uint "$2" || fail_config "$1 must be an unsigned base-10 integer"; }
0080: validate_uint CHUNK_LOG2 "$CHUNK_LOG2"
0081: validate_uint ALGORITHM_CHUNKS "$ALGORITHM_CHUNKS"
0082: validate_uint ALGORITHM_TUPLE_CAP "$ALGORITHM_TUPLE_CAP"
0083: validate_uint MATCH_ATTEMPT_CAP "$MATCH_ATTEMPT_CAP"
0084: validate_uint CHARGED_TUPLE_CAP "$CHARGED_TUPLE_CAP"
0085: validate_uint BASE_SEED "$BASE_SEED"
0086: validate_uint NTHREADS "$NTHREADS"
0087: validate_uint CPU_RESERVE "$CPU_RESERVE"
0088: validate_uint MIN_FREE_MEMORY_PERCENT "$MIN_FREE_MEMORY_PERCENT"
0089: [ "$CHUNK_LOG2" -eq 36 ] || fail_config "this campaign requires CHUNK_LOG2=36"
0090: [ "$ALGORITHM_CHUNKS" -eq 4096 ] || fail_config "this campaign requires exactly 4096 deterministic chunks"
0091: [ "$ALGORITHM_TUPLE_CAP" -eq 1073741824 ] || fail_config "this campaign requires a 2^30 Step-3 tuple-record cap"
0092: [ "$MATCH_ATTEMPT_CAP" -eq 8192 ] || fail_config "this campaign requires an 8192 match-attempt cap"
0093: [ "$CHARGED_TUPLE_CAP" -eq 2147483648 ] || fail_config "this campaign requires a 2^31 charged Step-3 tuple cap"
0094: [ "$TAILS_PER_TUPLE" -eq 196608 ] || fail_config "this campaign requires exactly 196608 tails per tuple"
0095: [ "$RUNNER_INVOCATION_CAP" -eq 64 ] || fail_config "this campaign requires a 64-invocation runner cap"
0096: [ "$PAIR_VERIFIER_INVOCATION_CAP" -eq 1 ] || fail_config "this campaign requires one external pair-verifier invocation"
0097: [ "$MAX_RETAINED_FULL_TUPLE_BYTES" -eq 1073741824 ] || fail_config "this campaign requires a 2^30-byte retained tuple-file cap"
0098: [ "$ADVICE_CAP_EXCLUSIVE_BYTES" -eq 8589934592 ] || fail_config "this campaign requires retained advice below 2^33 bytes"
0099: [ "$NTHREADS" -ge 1 ] && [ "$NTHREADS" -le 256 ] || fail_config "NTHREADS must be in 1..256"
0100: [ "$CPU_RESERVE" -le 256 ] || fail_config "CPU_RESERVE must be in 0..256"
0101: [ "$MIN_FREE_MEMORY_PERCENT" -ge 0 ] && [ "$MIN_FREE_MEMORY_PERCENT" -le 100 ] \
0102:   || fail_config "MIN_FREE_MEMORY_PERCENT must be in 0..100"
0103: [ "$BASE_SEED" -le 9000000000000000000 ] || fail_config "BASE_SEED is too large for safe shell arithmetic"
0104: is_sha256 "$SEALED_RECEIPT_ROOT_SHA256" || fail_config "SEALED_RECEIPT_ROOT_SHA256 must be 64 lowercase hex characters"
0105: is_sha256 "$RUN_SEAL_ROOT_SHA256" || fail_config "RUN_SEAL_ROOT_SHA256 must be 64 lowercase hex characters"
0106: is_sha256 "$SEAL_TOOL_SHA256" || fail_config "SEAL_TOOL_SHA256 must be 64 lowercase hex characters"
0107: is_sha256 "$SEAL_TRUST_ANCHOR_SHA256" || fail_config "SEAL_TRUST_ANCHOR_SHA256 must be 64 lowercase hex characters"
0108: [ "$PRELAUNCH_SEAL_INVENTORY" = "$ADVICE_RECEIPTS/prelaunch-seal.tsv" ] \
0109:   || fail_config "PRELAUNCH_SEAL_INVENTORY must use the canonical run-local path"
0110: case "$ROOT$HASHSMASH_REPO$HARDCODED_REF_REPO$PROVENANCE_REPO$RUN$PRELAUNCH_SEAL_INVENTORY" in
0111:   *$'\n'*|*$'\t'*) fail_config "configured paths must not contain tabs or newlines" ;;
0112: esac
0113: 
0114: expected_chunk_n=$((1 << CHUNK_LOG2))
0115: expected_first_block_cap=$((ALGORITHM_CHUNKS * expected_chunk_n))
0116: [ "$expected_first_block_cap" -eq 281474976710656 ] || fail_config "internal 2^48 cap calculation failed"
0117: 
0118: [ -f "$RUN_SEAL/receipts/RECEIPT-MANIFEST.sha256" ] \
0119:   && [ "$(sha256_file "$RUN_SEAL/receipts/RECEIPT-MANIFEST.sha256")" = "$SEALED_RECEIPT_ROOT_SHA256" ] \
0120:   && [ "$(cat "$RUN_SEAL/receipts/RECEIPT-ROOT.sha256")" = "$SEALED_RECEIPT_ROOT_SHA256  RECEIPT-MANIFEST.sha256" ] \
0121:   || fail_config "run-local sealed receipt manifest/root is missing or mismatched"
0122: [ -f "$RUN_SEAL/RUN-SEAL-MANIFEST.sha256" ] \
0123:   && [ "$(sha256_file "$RUN_SEAL/RUN-SEAL-MANIFEST.sha256")" = "$RUN_SEAL_ROOT_SHA256" ] \
0124:   && [ "$(cat "$RUN_SEAL/RUN-SEAL-ROOT.sha256")" = "$RUN_SEAL_ROOT_SHA256  RUN-SEAL-MANIFEST.sha256" ] \
0125:   || fail_config "run-local seal manifest/root is missing or mismatched"
0126: [ -f "$RUN_SEAL/tools/seal.py" ] && [ "$(sha256_file "$RUN_SEAL/tools/seal.py")" = "$SEAL_TOOL_SHA256" ] \
0127:   || fail_config "run-local seal verifier does not match the pinned tool hash"
0128: [ -f "$RUN_SEAL/tools/digicert-trusted-root-g4.pem" ] \
0129:   && [ "$(sha256_file "$RUN_SEAL/tools/digicert-trusted-root-g4.pem")" = "$SEAL_TRUST_ANCHOR_SHA256" ] \
0130:   || fail_config "run-local timestamp trust anchor does not match the pinned hash"
0131: [ -f "$PRELAUNCH_SEAL_INVENTORY" ] || fail_config "prelaunch seal advice inventory is missing"
0132: 
0133: runner_sha="$(sha256_file "$0")"
0134: [ -d "$PROVENANCE_REPO/.git" ] || fail_config "missing sealed provenance git repo: $PROVENANCE_REPO"
0135: [ -z "$(git -C "$PROVENANCE_REPO" status --porcelain --untracked-files=all)" ] \
0136:   || fail_config "sealed provenance repo is dirty"
0137: PROVENANCE_COMMIT="$(git -C "$PROVENANCE_REPO" rev-parse HEAD)"
0138: sealed_runner_sha="$(git -C "$PROVENANCE_REPO" show HEAD:runner/run_record.sh | shasum -a 256 | awk '{print $1}')"
0139: [ "$sealed_runner_sha" = "$runner_sha" ] \
0140:   || fail_config "running script does not match runner/run_record.sh in sealed provenance commit $PROVENANCE_COMMIT"
0141: [ "$(sha256_file "$PROVENANCE_REPO/runner/run_record.sh")" = "$runner_sha" ] \
0142:   || fail_config "provenance working-tree runner differs from both HEAD and the running script"
0143: 
0144: mkdir -p "$RUN"
0145: if ! mkdir "$LOCK" 2>/dev/null; then
0146:   echo "runner lock exists at $LOCK; refusing a second process or unaudited stale-lock recovery" >&2
0147:   [ ! -f "$LOCK/pid" ] || echo "recorded pid: $(cat "$LOCK/pid")" >&2
0148:   exit 3
0149: fi
0150: printf '%s\n' "$$" > "$LOCK/pid"
--- original lines 600-764 ---
0600: read_accounting_cache() {
0601:   [ -f "$ACCOUNTING" ] || return 1
0602:   [ "$(tsv_get "$ACCOUNTING" version)" = 1 ] \
0603:     && [ "$(tsv_get "$ACCOUNTING" config_sha256)" = "$CONFIG_SHA" ] \
0604:     && [ "$(tsv_get "$ACCOUNTING" match_attempt_cap)" = "$MATCH_ATTEMPT_CAP" ] \
0605:     && [ "$(tsv_get "$ACCOUNTING" step3_tuple_cap)" = "$CHARGED_TUPLE_CAP" ] \
0606:     || { echo "operational-accounting cache fingerprint mismatch" >&2; exit 7; }
0607:   CACHE_MATCH="$(tsv_get "$ACCOUNTING" match_attempts_reserved)" || exit 7
0608:   CACHE_STEP="$(tsv_get "$ACCOUNTING" step3_tuples_reserved)" || exit 7
0609:   is_uint "$CACHE_MATCH" && is_uint "$CACHE_STEP" || { echo "invalid operational-accounting cache" >&2; exit 7; }
0610: }
0611: 
0612: write_accounting_cache() {
0613:   local match_count="$1" step_count="$2" tmp="$ACCOUNTING.$$"
0614:   cat > "$tmp" <<EOF
0615: version${TAB}1
0616: config_sha256${TAB}$CONFIG_SHA
0617: match_attempts_reserved${TAB}$match_count
0618: step3_tuples_reserved${TAB}$step_count
0619: match_attempt_cap${TAB}$MATCH_ATTEMPT_CAP
0620: step3_tuple_cap${TAB}$CHARGED_TUPLE_CAP
0621: updated_at${TAB}$(timestamp)
0622: EOF
0623:   mv "$tmp" "$ACCOUNTING"
0624: }
0625: 
0626: reconcile_accounting() {
0627:   local f kind config amount attempt file_attempt next_attempt_value match_count=0 step_count=0 old_match=0 old_step=0 max_attempt=0
0628:   for f in "$RESERVATIONS"/*; do
0629:     [ -e "$f" ] || continue
0630:     case "$(basename "$f")" in match-attempt-*.tsv|step3-attempt-*.tsv) ;; *) echo "unknown reservation artifact: $f" >&2; exit 7;; esac
0631:     kind="$(tsv_get "$f" kind)" || exit 7
0632:     config="$(tsv_get "$f" config_sha256)" || exit 7
0633:     amount="$(tsv_get "$f" amount)" || exit 7
0634:     attempt="$(tsv_get "$f" attempt)" || exit 7
0635:     is_uint "$amount" && is_uint "$attempt" || { echo "invalid reservation record: $f" >&2; exit 7; }
0636:     [ "$config" = "$CONFIG_SHA" ] || { echo "reservation config mismatch: $f" >&2; exit 7; }
0637:     file_attempt="$(basename "$f" .tsv | sed -E 's/^(match|step3)-attempt-//')"
0638:     [ "$file_attempt" = "$attempt" ] || { echo "reservation filename mismatch: $f" >&2; exit 7; }
0639:     [ "$attempt" -gt "$max_attempt" ] && max_attempt="$attempt"
0640:     case "$kind" in
0641:       match) [[ "$(basename "$f")" = match-attempt-* ]] && [ "$amount" -eq 1 ] \
0642:         && [ ! -e "$RESERVATIONS/step3-attempt-$attempt.tsv" ] \
0643:         || { echo "invalid or cross-kind duplicate match reservation" >&2; exit 7; }; match_count=$((match_count + 1)) ;;
0644:       step3) [[ "$(basename "$f")" = step3-attempt-* ]] \
0645:         && [ ! -e "$RESERVATIONS/match-attempt-$attempt.tsv" ] \
0646:         || { echo "invalid or cross-kind duplicate Step-3 reservation" >&2; exit 7; }; step_count=$((step_count + amount)) ;;
0647:       *) echo "invalid reservation kind in $f" >&2; exit 7 ;;
0648:     esac
0649:   done
0650:   [ "$match_count" -le "$MATCH_ATTEMPT_CAP" ] && [ "$step_count" -le "$CHARGED_TUPLE_CAP" ] \
0651:     || { echo "write-ahead reservations exceed operational caps" >&2; exit 8; }
0652:   if read_accounting_cache; then
0653:     old_match="$CACHE_MATCH"; old_step="$CACHE_STEP"
0654:     [ "$old_match" -le "$match_count" ] && [ "$old_step" -le "$step_count" ] \
0655:       || { echo "accounting cache exceeds immutable reservation ledger" >&2; exit 7; }
0656:     if [ "$old_match" -ne "$match_count" ] || [ "$old_step" -ne "$step_count" ]; then
0657:       append_event - - ACCOUNTING RECOVERED \
0658:         "old_match=$old_match;reserved_match=$match_count;old_step3=$old_step;reserved_step3=$step_count"
0659:     fi
0660:   fi
0661:   if [ ! -f "$ACCOUNTING" ] || [ "$old_match" -ne "$match_count" ] || [ "$old_step" -ne "$step_count" ]; then
0662:     write_accounting_cache "$match_count" "$step_count"
0663:   fi
0664:   MATCH_RESERVED="$match_count"
0665:   STEP3_RESERVED="$step_count"
0666:   next_attempt_value="$(tr -d '[:space:]' < "$NEXT_ATTEMPT")"
0667:   is_uint "$next_attempt_value" && [ "$next_attempt_value" -gt "$max_attempt" ] \
0668:     || { echo "next_attempt does not exceed every immutable reservation ID" >&2; exit 7; }
0669: }
0670: 
0671: reservation_set_sha256() {
0672:   local f
0673:   {
0674:     for f in "$RESERVATIONS"/match-attempt-*.tsv "$RESERVATIONS"/step3-attempt-*.tsv; do
0675:       [ -e "$f" ] || continue
0676:       printf '%s  %s\n' "$(sha256_file "$f")" "$(basename "$f")"
0677:     done
0678:   } | shasum -a 256 | awk '{print $1}'
0679: }
0680: 
0681: reserve_match_attempt() {
0682:   local attempt="$1" chunk="$2" receipt tmp
0683:   receipt="$RESERVATIONS/match-attempt-$attempt.tsv"
0684:   reconcile_accounting
0685:   [ "$MATCH_RESERVED" -lt "$MATCH_ATTEMPT_CAP" ] || {
0686:     append_event "$attempt" "$chunk" OPERATIONAL_CAP MATCH_ATTEMPT_CAP_REACHED "reserved=$MATCH_RESERVED;cap=$MATCH_ATTEMPT_CAP"
0687:     echo "match-attempt cap reached before starting work" >&2; exit 8
0688:   }
0689:   [ ! -e "$receipt" ] || { echo "duplicate match reservation for attempt $attempt" >&2; exit 7; }
0690:   tmp="$AUDIT/match-reservation-attempt-$attempt.tmp.$$"
0691:   cat > "$tmp" <<EOF
0692: version${TAB}1
0693: kind${TAB}match
0694: attempt${TAB}$attempt
0695: chunk${TAB}$chunk
0696: amount${TAB}1
0697: first_blocks_charged${TAB}$expected_chunk_n
0698: config_sha256${TAB}$CONFIG_SHA
0699: runner_sha256${TAB}$runner_sha
0700: provenance_commit${TAB}$PROVENANCE_COMMIT
0701: reserved_at${TAB}$(timestamp)
0702: EOF
0703:   mv "$tmp" "$receipt"
0704:   reconcile_accounting
0705:   append_event "$attempt" "$chunk" RESERVATION MATCH \
0706:     "receipt_sha256=$(sha256_file "$receipt");match_attempts_reserved=$MATCH_RESERVED;first_blocks_charged=$expected_chunk_n"
0707: }
0708: 
0709: reserve_step3_tuples() {
0710:   local attempt="$1" chunk="$2" amount="$3" input_sha="$4"
0711:   local receipt="$RESERVATIONS/step3-attempt-$attempt.tsv" tmp after
0712:   is_uint "$amount" && [ "$amount" -gt 0 ] || { echo "invalid Step-3 reservation amount" >&2; exit 7; }
0713:   reconcile_accounting
0714:   after=$((STEP3_RESERVED + amount))
0715:   [ "$after" -le "$CHARGED_TUPLE_CAP" ] || {
0716:     append_event "$attempt" "$chunk" OPERATIONAL_CAP STEP3_TUPLE_CAP_WOULD_EXCEED \
0717:       "reserved=$STEP3_RESERVED;requested=$amount;cap=$CHARGED_TUPLE_CAP"
0718:     echo "charged Step-3 tuple cap would be exceeded; refusing work" >&2; exit 8
0719:   }
0720:   [ ! -e "$receipt" ] || { echo "duplicate Step-3 reservation for attempt $attempt" >&2; exit 7; }
0721:   tmp="$AUDIT/step3-reservation-attempt-$attempt.tmp.$$"
0722:   cat > "$tmp" <<EOF
0723: version${TAB}1
0724: kind${TAB}step3
0725: attempt${TAB}$attempt
0726: chunk${TAB}$chunk
0727: amount${TAB}$amount
0728: step_input_sha256${TAB}$input_sha
0729: charged_before${TAB}$STEP3_RESERVED
0730: charged_after${TAB}$after
0731: config_sha256${TAB}$CONFIG_SHA
0732: runner_sha256${TAB}$runner_sha
0733: provenance_commit${TAB}$PROVENANCE_COMMIT
0734: reserved_at${TAB}$(timestamp)
0735: EOF
0736:   mv "$tmp" "$receipt"
0737:   reconcile_accounting
0738:   append_event "$attempt" "$chunk" RESERVATION STEP3 \
0739:     "receipt_sha256=$(sha256_file "$receipt");tuples_this_attempt=$amount;step3_tuples_reserved=$STEP3_RESERVED"
0740: }
0741: 
0742: verify_pair_file_once() {
0743:   local candidate="$1" verify_log="$2" attempt="$3" chunk="$4" receipt begin rc
0744:   receipt="$VERIFIER_RECEIPTS/verifier-attempt-$attempt.tsv"
0745:   [ -s "$candidate" ] || return 1
0746:   [ "$(awk 'END { print NR+0 }' "$candidate")" -eq 1 ] \
0747:     || { echo "candidate must contain exactly one record" >&2; exit 6; }
0748:   awk 'NF && ($1 != "rfb" || $2 != 32) { bad=1 } END { exit bad }' "$candidate" || { echo "candidate contains a non-r32 record: $candidate" >&2; exit 6; }
0749:   begin="$(python3 "$ROOT/audit_guard.py" verifier-begin --dir "$VERIFIER_RECEIPTS" \
0750:     --cap "$PAIR_VERIFIER_INVOCATION_CAP" --attempt "$attempt" --chunk "$chunk" --candidate "$candidate" \
0751:     --runner-sha "$runner_sha" --config-sha "$CONFIG_SHA" --provenance "$PROVENANCE_COMMIT")" \
0752:     || { echo "pair-verifier reservation failed closed" >&2; exit 8; }
0753:   echo "$begin"
0754:   if [[ "$begin" == *"status=completed"* ]]; then return 0; fi
0755:   cd "$ROOT"
0756:   set +e
0757:   python3 verify_pairs.py "$candidate" > "$verify_log" 2>&1
0758:   rc=$?
0759:   set -e
0760:   cat "$verify_log"
0761:   python3 "$ROOT/audit_guard.py" verifier-complete --receipt "$receipt" --log "$verify_log" --exit-code "$rc" \
0762:     || { echo "pair-verifier completion receipt failed closed" >&2; exit 8; }
0763:   [ "$rc" -eq 0 ] || exit 6
0764: }
--- original lines 950-1085 ---
0950:   fi
0951:   if [ -s "$ACTIVE_PHASE" ]; then
0952:     active_attempt="$(tsv_get "$ACTIVE_PHASE" attempt)"; active_chunk="$(tsv_get "$ACTIVE_PHASE" chunk)"; active_phase="$(tsv_get "$ACTIVE_PHASE" phase)"
0953:     [ "$active_attempt" = "$attempt" ] && [ "$active_chunk" = "$chunk" ] && [ "$active_phase" = MATCH ] \
0954:       || { echo "boundary tuple-cap receipt conflicts with active phase" >&2; exit 8; }
0955:     mv "$ACTIVE_PHASE" "$AUDIT/boundary-active-attempt-$attempt-$INVOCATION_ID.tsv"
0956:   fi
0957:   append_event "$attempt" "$chunk" ALGORITHM_CAP TUPLE_CAP_BOUNDARY_DISCARDED \
0958:     "processed_tuple_records=$pre;remaining=$remaining;discarded_full_tuple_records=$full_tuples;full_sha256=$full_sha;step3_scanned=0;candidate_eligible=false;receipt_sha256=$(sha256_file "$TUPLE_CAP_TERMINAL")"
0959:   echo "$(timestamp) boundary chunk exceeded the remaining tuple budget; entire chunk discarded unscanned and campaign terminalized"
0960:   exit 0
0961: }
0962: 
0963: record_found() {
0964:   local candidate="$1" chunk="$2" attempt="$3" dir manifest
0965:   dir="$PENDING/chunk-$chunk"
0966:   manifest="$dir/manifest.tsv"
0967:   local full_name step_name full_sha step_sha full_bytes full_tuples step_bytes step_prefix_bytes step_tuples pair_hash receipt winning_manifest_sha active_attempt active_chunk active_phase
0968:   local operation_receipt verifier_receipt reference reference_tmp final_inventory final_inventory_sha final_inventory_total
0969:   verify_pending_dir "$dir" "$chunk"
0970:   full_name="$(tsv_get "$manifest" full_file)"; step_name="$(tsv_get "$manifest" step_file)"
0971:   full_sha="$(tsv_get "$manifest" full_sha256)"; step_sha="$(tsv_get "$manifest" step_sha256)"
0972:   full_bytes="$(tsv_get "$manifest" full_bytes)"; full_tuples="$(tsv_get "$manifest" full_tuples)"
0973:   step_bytes="$(tsv_get "$manifest" step_bytes)"; step_prefix_bytes="$(tsv_get "$manifest" step_prefix_bytes)"
0974:   step_tuples="$(tsv_get "$manifest" step_tuples)"
0975:   [ "$full_name" = "$step_name" ] && [ "$full_sha" = "$step_sha" ] \
0976:     || { echo "winning full and Step-3 inputs must be one physical file" >&2; exit 8; }
0977:   campaign_require_untruncated_tuple_contract \
0978:     "$full_bytes" "$full_tuples" "$step_bytes" "$step_prefix_bytes" "$step_tuples" "$TUPLE_RECORD_BYTES" \
0979:     || { echo "truncated boundary prefixes are ineligible for winner promotion" >&2; exit 8; }
0980:   operation_receipt="$OPERATION_RECEIPTS/step3-attempt-$attempt.tsv"
0981:   [ -f "$operation_receipt" ] \
0982:     && [ "$(tsv_get "$operation_receipt" candidate_sha256)" = "$(sha256_file "$candidate")" ] \
0983:     && [ "$(tsv_get "$operation_receipt" pending_manifest_sha256)" = "$(sha256_file "$manifest")" ] \
0984:     || { echo "candidate is not bound to its Step-3 operation receipt" >&2; exit 8; }
0985:   receipt="$RESERVATIONS/step3-attempt-$attempt.tsv"
0986:   [ -f "$receipt" ] \
0987:     && [ "$(tsv_get "$receipt" kind)" = step3 ] \
0988:     && [ "$(tsv_get "$receipt" chunk)" = "$chunk" ] \
0989:     && [ "$(tsv_get "$receipt" amount)" = "$step_tuples" ] \
0990:     && [ "$(tsv_get "$receipt" step_input_sha256)" = "$step_sha" ] \
0991:     || { echo "candidate is not bound to its Step-3 write-ahead reservation" >&2; exit 6; }
0992:   reconcile_accounting
0993:   verify_pair_file_once "$candidate" "$RUN/verification-attempt-$attempt.log" "$attempt" "$chunk"
0994:   verifier_receipt="$VERIFIER_RECEIPTS/verifier-attempt-$attempt.tsv"
0995:   [ "$(tsv_get "$verifier_receipt" status)" = completed ] && [ "$(tsv_get "$verifier_receipt" exit_code)" = 0 ] \
0996:     || { echo "pair-verifier receipt is not completed successfully" >&2; exit 8; }
0997: 
0998:   if [ -e "$VERIFIED_PAIRS" ]; then cmp -s "$candidate" "$VERIFIED_PAIRS" || { echo "verified pair changed during recovery" >&2; exit 8; }
0999:   else cp "$candidate" "$VERIFIED_PAIRS.tmp.$$"; mv "$VERIFIED_PAIRS.tmp.$$" "$VERIFIED_PAIRS"; fi
1000:   pair_hash="$(sha256_file "$VERIFIED_PAIRS")"
1001:   if [ -e "$WINNING/chunk-$chunk.manifest.tsv" ]; then cmp -s "$manifest" "$WINNING/chunk-$chunk.manifest.tsv" || { echo "winning manifest changed during recovery" >&2; exit 8; }
1002:   else cp "$manifest" "$WINNING/chunk-$chunk.manifest.tsv.tmp.$$"; mv "$WINNING/chunk-$chunk.manifest.tsv.tmp.$$" "$WINNING/chunk-$chunk.manifest.tsv"; fi
1003:   winning_manifest_sha="$(sha256_file "$WINNING/chunk-$chunk.manifest.tsv")"
1004:   reference="$WINNING/chunk-$chunk.tuple-reference.tsv"; reference_tmp="$reference.tmp.$$"
1005:   cat > "$reference_tmp" <<EOF
1006: version${TAB}1
1007: tuple_path${TAB}$dir/$full_name
1008: tuple_bytes${TAB}$full_bytes
1009: tuple_sha256${TAB}$full_sha
1010: pending_manifest_sha256${TAB}$(sha256_file "$manifest")
1011: step3_operation_receipt_sha256${TAB}$(sha256_file "$operation_receipt")
1012: verifier_receipt_sha256${TAB}$(sha256_file "$verifier_receipt")
1013: EOF
1014:   if [ -e "$reference" ]; then cmp -s "$reference" "$reference_tmp" || { echo "winning tuple reference changed during recovery" >&2; exit 8; }; rm -f "$reference_tmp"
1015:   else mv "$reference_tmp" "$reference"; fi
1016:   [ "$(sha256_file "$dir/$full_name")" = "$full_sha" ] && [ "$(file_bytes "$dir/$full_name")" -eq "$full_bytes" ] || exit 7
1017:   if [ -n "$(find "$WINNING" -type f -name '*.bin' -print -quit)" ]; then echo "winning directory contains a duplicate binary input" >&2; exit 8; fi
1018: 
1019:   if [ -s "$ACTIVE_PHASE" ]; then
1020:     active_attempt="$(tsv_get "$ACTIVE_PHASE" attempt)"; active_chunk="$(tsv_get "$ACTIVE_PHASE" chunk)"; active_phase="$(tsv_get "$ACTIVE_PHASE" phase)"
1021:     [ "$active_attempt" = "$attempt" ] && [ "$active_chunk" = "$chunk" ] && [ "$active_phase" = STEP3 ] \
1022:       || { echo "verified collision conflicts with unrelated active phase" >&2; exit 7; }
1023:     mv "$ACTIVE_PHASE" "$AUDIT/recovered-winning-active-attempt-$attempt.tsv"
1024:   fi
1025: 
1026:   final_inventory="$ADVICE_RECEIPTS/final-found-attempt-$attempt.tsv"
1027:   run_advice_inventory "final-found-attempt-$attempt" "$final_inventory"
1028:   final_inventory_sha="$(sha256_file "$final_inventory")"
1029:   final_inventory_total="$(awk -F '\t' '$1 == "total_unique_bytes" { n++; value=$2 } END { if (n != 1 || value !~ /^(0|[1-9][0-9]*)$/) exit 2; print value }' "$final_inventory")" || exit 8
1030: 
1031:   cat > "$FOUND.tmp.$$" <<EOF
1032: verified_at${TAB}$(timestamp)
1033: chunk${TAB}$chunk
1034: attempt${TAB}$attempt
1035: pairs_sha256${TAB}$pair_hash
1036: full_tuple_chunk_sha256${TAB}$full_sha
1037: step3_input_sha256${TAB}$step_sha
1038: winning_manifest_sha256${TAB}$winning_manifest_sha
1039: winning_tuple_reference_sha256${TAB}$(sha256_file "$reference")
1040: step3_operation_receipt_sha256${TAB}$(sha256_file "$operation_receipt")
1041: verifier_receipt_sha256${TAB}$(sha256_file "$verifier_receipt")
1042: final_advice_inventory_sha256${TAB}$final_inventory_sha
1043: final_advice_inventory_total_bytes${TAB}$final_inventory_total
1044: final_advice_cap_exclusive_bytes${TAB}$ADVICE_CAP_EXCLUSIVE_BYTES
1045: step3_input_tuples_this_attempt${TAB}$step_tuples
1046: algorithm_processed_tuple_records_before_chunk${TAB}$PROCESSED_TUPLES
1047: algorithm_unique_first_blocks_through_chunk${TAB}$(((chunk + 1) * expected_chunk_n))
1048: actual_match_attempts_reserved${TAB}$MATCH_RESERVED
1049: actual_step3_tuples_reserved${TAB}$STEP3_RESERVED
1050: declared_score_match_attempt_cap${TAB}$MATCH_ATTEMPT_CAP
1051: declared_score_step3_tuple_cap${TAB}$CHARGED_TUPLE_CAP
1052: declared_score_unique_first_block_cap${TAB}$expected_first_block_cap
1053: declared_score_tuple_record_cap${TAB}$ALGORITHM_TUPLE_CAP
1054: score_policy${TAB}charge full declared caps even on early success
1055: runner_sha256${TAB}$runner_sha
1056: config_sha256${TAB}$CONFIG_SHA
1057: provenance_commit${TAB}$PROVENANCE_COMMIT
1058: machine_provenance_sha256${TAB}$MACHINE_PROVENANCE_SHA
1059: organizer_base_commit${TAB}$ORGANIZER_BASE_COMMIT
1060: EOF
1061:   mv "$FOUND.tmp.$$" "$FOUND"
1062:   append_event "$attempt" "$chunk" COLLISION VERIFIED \
1063:     "pairs_sha256=$pair_hash;full_tuple_sha256=$full_sha;step3_input_sha256=$step_sha;full_caps_charged_for_score=yes"
1064:   echo "$(timestamp) independently verified SHA-256/r32 collision recorded; winning tuple chunk preserved"
1065: }
1066: 
1067: recover_candidates_or_found() {
1068:   if [ -e "$FOUND" ]; then
1069:     [ -s "$VERIFIED_PAIRS" ] || { echo "FOUND exists without verified pairs" >&2; exit 6; }
1070:     local pairs_sha full_sha step_sha manifest_sha chunk attempt found_runner found_config found_provenance receipt step_tuples
1071:     local pending_manifest tuple_path operation_receipt verifier_receipt inventory inventory_sha inventory_total reference reference_sha
1072:     pairs_sha="$(tsv_get "$FOUND" pairs_sha256)" || exit 6; full_sha="$(tsv_get "$FOUND" full_tuple_chunk_sha256)" || exit 6
1073:     step_sha="$(tsv_get "$FOUND" step3_input_sha256)" || exit 6; manifest_sha="$(tsv_get "$FOUND" winning_manifest_sha256)" || exit 6
1074:     chunk="$(tsv_get "$FOUND" chunk)" || exit 6; attempt="$(tsv_get "$FOUND" attempt)" || exit 6
1075:     found_runner="$(tsv_get "$FOUND" runner_sha256)" || exit 6; found_config="$(tsv_get "$FOUND" config_sha256)" || exit 6
1076:     found_provenance="$(tsv_get "$FOUND" provenance_commit)" || exit 6
1077:     is_uint "$chunk" && is_uint "$attempt" && [ "$chunk" -lt "$ALGORITHM_CHUNKS" ] \
1078:       && [ "$found_runner" = "$runner_sha" ] && [ "$found_config" = "$CONFIG_SHA" ] && [ "$found_provenance" = "$PROVENANCE_COMMIT" ] \
1079:       || { echo "FOUND identity/fingerprint mismatch" >&2; exit 6; }
1080:     [ "$(sha256_file "$VERIFIED_PAIRS")" = "$pairs_sha" ] || { echo "FOUND pair hash mismatch" >&2; exit 6; }
1081:     pending_manifest="$PENDING/chunk-$chunk/manifest.tsv"; verify_pending_dir "$PENDING/chunk-$chunk" "$chunk"
1082:     tuple_path="$PENDING/chunk-$chunk/$(tsv_get "$pending_manifest" full_file)"
1083:     [ "$(sha256_file "$tuple_path")" = "$full_sha" ] && [ "$full_sha" = "$step_sha" ] || { echo "winning tuple hash mismatch" >&2; exit 6; }
1084:     [ "$(sha256_file "$WINNING/chunk-$chunk.manifest.tsv")" = "$manifest_sha" ] || { echo "winning manifest hash mismatch" >&2; exit 6; }
1085:     step_tuples="$(tsv_get "$WINNING/chunk-$chunk.manifest.tsv" step_tuples)" || exit 6
--- original lines 1366-1455 ---
1366: ensure_pending_for_chunk() {
1367:   local chunk="$1" dir other
1368:   dir="$PENDING/chunk-$chunk"
1369:   local attempt seed build_dir tuple log start end rc tee_rc bytes tuples tuple_sha remaining pipe_status
1370:   local step_name step_bytes step_prefix_bytes step_sha manifest match_operation_receipt advice_receipt pre_match_reserve
1371:   if [ -d "$dir" ]; then verify_pending_dir "$dir" "$chunk"; return; fi
1372:   for other in "$PENDING"/chunk-*; do
1373:     [ -e "$other" ] || continue
1374:     echo "unexpected pending transaction $other while state requires chunk $chunk" >&2; exit 7
1375:   done
1376: 
1377:   wait_for_capacity
1378:   advice_receipt="$ADVICE_RECEIPTS/pre-match-current.tsv"
1379:   pre_match_reserve=$((MAX_RETAINED_FULL_TUPLE_BYTES + ADVICE_RECEIPT_RESERVE_BYTES))
1380:   run_advice_inventory "pre-match-chunk-$chunk" "$advice_receipt" "$pre_match_reserve"
1381:   attempt="$(allocate_attempt "$chunk" MATCH)"
1382:   reserve_match_attempt "$attempt" "$chunk"
1383:   [ ! -e "$RUN/STOP" ] || { append_event "$attempt" "$chunk" STOP_GATE STOPPED_AFTER_RESERVATION "match_reservation_charged=yes"; exit 0; }
1384:   seed=$((BASE_SEED + chunk))
1385:   build_dir="$WORK/pending-build-chunk-$chunk-attempt-$attempt"
1386:   mkdir "$build_dir"
1387:   tuple="$build_dir/full.tuples.bin"
1388:   log="$LOGS/attempt-$attempt-chunk-$chunk.match.log"
1389:   start="$(epoch_now)"
1390:   set_active_phase "$attempt" "$chunk" MATCH "$log" - "$tuple" yes "first_blocks=$expected_chunk_n;algorithm_chunk=$chunk"
1391:   append_event "$attempt" "$chunk" MATCH START \
1392:     "seed=$seed;start_counter=0;first_blocks_charged=$expected_chunk_n;reservation=$(basename "$RESERVATIONS/match-attempt-$attempt.tsv")"
1393:   echo "$(timestamp) chunk=$chunk attempt=$attempt seed=$seed match begin"
1394:   cd "$ROOT"
1395:   set +e
1396:   env NTHREADS="$NTHREADS" MAX_OUTPUT_RECORDS="$((MAX_RETAINED_FULL_TUPLE_BYTES / TUPLE_RECORD_BYTES))" \
1397:     nice -n 10 ./c/match 32 "$CHUNK_LOG2" "$seed" "$tuple" part 0 2>&1 | tee "$log"
1398:   pipe_status=("${PIPESTATUS[@]}"); rc=${pipe_status[0]}; tee_rc=${pipe_status[1]}
1399:   set -e
1400:   end="$(epoch_now)"; bytes=0; tuples=0; tuple_sha=-
1401:   if [ -f "$tuple" ]; then
1402:     bytes="$(file_bytes "$tuple")"; tuple_sha="$(sha256_file "$tuple")"
1403:     if [ $((bytes % TUPLE_RECORD_BYTES)) -eq 0 ]; then tuples=$((bytes / TUPLE_RECORD_BYTES)); fi
1404:   fi
1405:   append_event "$attempt" "$chunk" MATCH "EXIT_$rc" \
1406:     "tee_rc=$tee_rc;elapsed_seconds=$((end-start));log_sha256=$(sha256_file "$log");output_sha256=$tuple_sha;output_bytes=$bytes;output_tuples=$tuples;first_blocks_charged=$expected_chunk_n"
1407:   [ "$rc" -eq 0 ] && [ "$tee_rc" -eq 0 ] || exit 5
1408:   grep -Eq "start 0 +rounds 32 N $expected_chunk_n " "$log" \
1409:     && grep -Eq "seed $seed " "$log" && grep -Eq "threads $NTHREADS " "$log" \
1410:     || { echo "match log does not bind the intended range" >&2; exit 5; }
1411:   [ $((bytes % TUPLE_RECORD_BYTES)) -eq 0 ] || { echo "tuple file has invalid size: $bytes" >&2; exit 5; }
1412:   [ "$bytes" -le "$MAX_RETAINED_FULL_TUPLE_BYTES" ] || { echo "retained full tuple file exceeds the sealed 2^30-byte cap" >&2; exit 8; }
1413:   write_match_operation_receipt "$attempt" "$chunk" "$log" "$tuple"
1414:   match_operation_receipt="$OPERATION_RECEIPTS/match-attempt-$attempt.tsv"
1415:   remaining=$((ALGORITHM_TUPLE_CAP - PROCESSED_TUPLES))
1416:   if campaign_boundary_exceeds_remaining "$tuples" "$remaining"; then
1417:     [ ! -e "$TUPLE_CAP_PENDING" ] && [ ! -e "$TUPLE_CAP_TERMINAL" ] \
1418:       || { echo "tuple-cap terminal receipt already exists" >&2; exit 8; }
1419:     cat > "$TUPLE_CAP_PENDING.tmp.$$" <<EOF
1420: version${TAB}1
1421: reason${TAB}boundary_chunk_exceeds_remaining_unscanned
1422: chunk${TAB}$chunk
1423: match_attempt${TAB}$attempt
1424: processed_tuple_records_before${TAB}$PROCESSED_TUPLES
1425: remaining_tuple_record_budget${TAB}$remaining
1426: full_bytes${TAB}$bytes
1427: full_tuples${TAB}$tuples
1428: full_sha256${TAB}$tuple_sha
1429: step3_tuples_scanned${TAB}0
1430: candidate_eligible${TAB}false
1431: tuple_file_disposition${TAB}discarded_unscanned
1432: match_reservation_sha256${TAB}$(sha256_file "$RESERVATIONS/match-attempt-$attempt.tsv")
1433: match_operation_receipt_sha256${TAB}$(sha256_file "$match_operation_receipt")
1434: pre_match_advice_inventory_sha256${TAB}$(sha256_file "$advice_receipt")
1435: config_sha256${TAB}$CONFIG_SHA
1436: runner_sha256${TAB}$runner_sha
1437: provenance_commit${TAB}$PROVENANCE_COMMIT
1438: created_at${TAB}$(timestamp)
1439: EOF
1440:     mv "$TUPLE_CAP_PENDING.tmp.$$" "$TUPLE_CAP_PENDING"
1441:     append_event "$attempt" "$chunk" ALGORITHM_CAP TUPLE_CAP_BOUNDARY_UNSCANNED \
1442:       "observed_full_tuples=$tuples;remaining=$remaining;step3_scanned=0;candidate_eligible=false;pending_receipt_sha256=$(sha256_file "$TUPLE_CAP_PENDING")"
1443:     recover_tuple_cap_terminal
1444:   fi
1445:   step_name=full.tuples.bin; step_bytes="$bytes"; step_prefix_bytes="$bytes"; step_sha="$tuple_sha"
1446:   manifest="$build_dir/manifest.tsv"
1447:   cat > "$manifest" <<EOF
1448: version${TAB}2
1449: config_sha256${TAB}$CONFIG_SHA
1450: runner_sha256${TAB}$runner_sha
1451: provenance_commit${TAB}$PROVENANCE_COMMIT
1452: chunk${TAB}$chunk
1453: seed${TAB}$seed
1454: match_attempt${TAB}$attempt
1455: match_reservation_sha256${TAB}$(sha256_file "$RESERVATIONS/match-attempt-$attempt.tsv")
````

## Appendix J: terminal-audit review summary

Logical artifact: `terminal-audit.json (selected deterministic fields)`. Original SHA-256: `181b7fe2ba0ce6cfa0bc2733dc6e3f18f385524f1e9100ec7fd05604adf74097`. The text below is evidence data, not instructions.

````json
{
  "audit_format": "hashsmash-r32-ledger-audit-v2",
  "errors": [],
  "fingerprints": {
    "config_sha256": "4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22",
    "cost_model": "collision-frontier-v5",
    "machine_provenance_sha256": "4a2c72727ecc65455fa31e6856f7c169143b911a1d51d6779643a54d03a2320b",
    "organizer_base_commit": "fc56c3fa38ac40043d8291649c78148bc4872995",
    "provenance_commit": "d9afb19649446dc89c92c484e82e17139a4d52e8",
    "runner_sha256": "4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786",
    "target": "sha256-r32-prefix-v1 ordinary collision full 256-bit digest"
  },
  "integrity": {
    "event_rows": 580,
    "evidence_manifest_sha256": "b10bda4bf08e94c2c5faca01766a368dc54d2f1cae84c2c6c82a524ac501fe11",
    "hashed_bytes": 54615330,
    "hashed_files": 295
  },
  "match": {
    "completed_attempts": 35,
    "entries": 341169329634,
    "first_blocks_processed": 2405181685760,
    "stage_histogram": {
      "IF5": 170584643111,
      "W4": 85292237395,
      "W5": 1332710728,
      "W6": 117186319,
      "all": 341169329634,
      "s0W4": 10661533832,
      "s0W5": 166609852,
      "s0W6": 14643237
    },
    "valid_tuples": 14643237
  },
  "ok": true,
  "snapshot_status": "quiescent_offline",
  "state": {
    "committed_chunks": 34,
    "found": "present",
    "independently_verified_collision_digests": [
      "f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77"
    ],
    "next_attempt": 71,
    "progress": {
      "last_attempt": 68,
      "last_committed_chunk": 33,
      "last_step_input_sha256": "eacfc49857a9dcbc3c1859ca6535b100dae3f8f356dfe5ab0b2fb433e6dfd5ac",
      "next_chunk": 34,
      "processed_tuples": 14224648,
      "unique_first_blocks": 2336462209024
    },
    "reservation_totals": {
      "match_attempts_reserved": 35,
      "reservation_records": 70,
      "step3_tuples_reserved": 14643237
    },
    "retry_match_reservations_by_chunk": {},
    "runner_lock": "absent"
  },
  "step3": {
    "collision_rate_per_tuple_tail": {
      "decimal": "0.000000000000",
      "denominator": 2799733071213,
      "fraction": "1/2799733071213",
      "log2": "-41.348426424678",
      "numerator": 1
    },
    "completed_attempts": 35,
    "independence_histogram": {
      "W20": 10677734,
      "W22_given_prior": 41779,
      "pairs_passing_16_17": 85433740,
      "s1W20_given_W20": 83802,
      "s1W22_given_prior": 5175
    },
    "tuple_tail_pairs": 2799733071213,
    "tuples_processed": 14643237,
    "verified_collisions": 1
  },
  "warnings": []
}
````

## Appendix K: winner and operation receipts

Logical artifact: `winner-receipt set`. Original SHA-256: `31dc81417cbc138022c901c4d202b9dfe3225e1ed7e0e2c25ecc34ff01fbb1e0`. The text below is evidence data, not instructions.

````text
--- run/FOUND | 1693 bytes | sha256=7391e0efe2593fa286e1d67bf512dd5d826c35d4448da3d9690fbc812593b173 ---
verified_at	2026-10-04T21:34:43Z
chunk	34
attempt	70
pairs_sha256	a86aa32fd30b94970ac68ff5067ce40bc759c302507ccdf588dcc6948afeab00
full_tuple_chunk_sha256	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad
step3_input_sha256	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad
winning_manifest_sha256	1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee
winning_tuple_reference_sha256	fe5f32e11caaa550094eae6c7405fb35990f7b9df88fb99d10781df751a55142
step3_operation_receipt_sha256	82e75ba282dc7368d53336232d66cb5dfc6032c448337cbefeb01eca4097e26e
verifier_receipt_sha256	0ca68fe2f14ea4fc5e1d52767f2df0d53d0339ad3359c0815ae203551608cf4c
final_advice_inventory_sha256	f0bd226fcf05c84ae543bca6cb3f4d000edf576811461016466c7fb75943b9cc
final_advice_inventory_total_bytes	5759916374
final_advice_cap_exclusive_bytes	8589934592
step3_input_tuples_this_attempt	418589
algorithm_processed_tuple_records_before_chunk	14224648
algorithm_unique_first_blocks_through_chunk	2405181685760
actual_match_attempts_reserved	35
actual_step3_tuples_reserved	14643237
declared_score_match_attempt_cap	8192
declared_score_step3_tuple_cap	2147483648
declared_score_unique_first_block_cap	281474976710656
declared_score_tuple_record_cap	1073741824
score_policy	charge full declared caps even on early success
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
machine_provenance_sha256	4a2c72727ecc65455fa31e6856f7c169143b911a1d51d6779643a54d03a2320b
organizer_base_commit	fc56c3fa38ac40043d8291649c78148bc4872995
--- run/operational-accounting.tsv | 229 bytes | sha256=f052b575ad717e13d9ff681ba15d89311e7a8e1315725891be40c71475c88670 ---
version	1
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
match_attempts_reserved	35
step3_tuples_reserved	14643237
match_attempt_cap	8192
step3_tuple_cap	2147483648
updated_at	2026-10-04T21:34:31Z
--- run/winning/chunk-34.manifest.tsv | 861 bytes | sha256=1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee ---
version	2
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
chunk	34
seed	202610040034
match_attempt	69
match_reservation_sha256	670bfc68651b64cda8a7b9893e7bc90022dafa51197028cedfe8447fd64f84fc
match_operation_receipt_sha256	ed7336bd1e1563e32e6e480182910d724403e8804ecbc4b007a8e11e5c76a11f
full_file	full.tuples.bin
full_bytes	46881968
full_tuples	418589
full_sha256	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad
step_file	full.tuples.bin
step_bytes	46881968
step_prefix_bytes	46881968
step_tuples	418589
step_sha256	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad
processed_tuple_records_before	14224648
tuple_cap	1073741824
created_at	2026-10-04T21:33:21Z
--- run/winning/chunk-34.tuple-reference.tsv | 496 bytes | sha256=fe5f32e11caaa550094eae6c7405fb35990f7b9df88fb99d10781df751a55142 ---
version	1
tuple_path	<RUN>/pending/chunk-34/full.tuples.bin
tuple_bytes	46881968
tuple_sha256	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad
pending_manifest_sha256	1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee
step3_operation_receipt_sha256	82e75ba282dc7368d53336232d66cb5dfc6032c448337cbefeb01eca4097e26e
verifier_receipt_sha256	0ca68fe2f14ea4fc5e1d52767f2df0d53d0339ad3359c0815ae203551608cf4c
--- run/audit/reservations/match-attempt-69.tsv | 333 bytes | sha256=670bfc68651b64cda8a7b9893e7bc90022dafa51197028cedfe8447fd64f84fc ---
version	1
kind	match
attempt	69
chunk	34
amount	1
first_blocks_charged	68719476736
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
reserved_at	2026-10-04T21:26:40Z
--- run/audit/reservations/step3-attempt-70.tsv | 435 bytes | sha256=9dddcab5f11bde9d399eb61ed634269b622e64511caa2d334867fa3986a27af7 ---
version	1
kind	step3
attempt	70
chunk	34
amount	418589
step_input_sha256	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad
charged_before	14224648
charged_after	14643237
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
reserved_at	2026-10-04T21:34:28Z
--- run/audit/operations/match-attempt-69.tsv | 757 bytes | sha256=ed7336bd1e1563e32e6e480182910d724403e8804ecbc4b007a8e11e5c76a11f ---
version	1
kind	match_operations
attempt	69
chunk	34
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
log_sha256	bf4cfef74acf5b361ffa834daa20617164a939d9a4b1cc4e069756848bdd2a1d
output_sha256	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad
output_bytes	46881968
initial_c32	68719476736
recompute_invocations	3096312444
recompute_c32	12385249776
total_c32	81104726512
bitmap_probes	71815789180
bucket_slots	148018261212
max_bucket	736
max_bucket_cap	736
partition_buffers_bytes	1073741824
output_buffers_ceiling_bytes	1835008
output_records	418589
output_record_cap	9586980
--- run/audit/operations/step3-attempt-70.tsv | 872 bytes | sha256=82e75ba282dc7368d53336232d66cb5dfc6032c448337cbefeb01eca4097e26e ---
version	1
kind	step3_operations
attempt	70
chunk	34
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
pending_manifest_sha256	1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee
log_sha256	0353283abad6ed1a08fd02f725ead9956b23eb07f191015b9287919a03531b13
candidate_sha256	a86aa32fd30b94970ac68ff5067ce40bc759c302507ccdf588dcc6948afeab00
candidate_bytes	504
terminal_exit_code	0
tuples_started	15532
tail_trials	3053477229
step3_calls	381685000
attack_rounds_ceiling	58016067351
ind_flags_calls	93323
ind_schedule_rounds_ceiling	653261
input_cv_compressions	15532
verification_reservations	1
verification_c32	2
verification_c35	2
winner_tuple	15529
winner_tail	131794
winner_ordinal	3053257426
--- run/audit/verifiers/verifier-attempt-70.tsv | 714 bytes | sha256=0ca68fe2f14ea4fc5e1d52767f2df0d53d0339ad3359c0815ae203551608cf4c ---
version	1
kind	pair_verifier
status	completed
attempt	70
chunk	34
candidate_path	<RUN>/candidates/attempt-70-chunk-34.pairs
candidate_bytes	504
candidate_sha256	a86aa32fd30b94970ac68ff5067ce40bc759c302507ccdf588dcc6948afeab00
runner_sha256	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786
config_sha256	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22
provenance_commit	d9afb19649446dc89c92c484e82e17139a4d52e8
exit_code	0
log_path	<RUN>/verification-attempt-70.log
log_bytes	582
log_sha256	c2d4e24dfcfefc3ab6e9aed7b58a42e3ff7602a120a547ab02a42d012f66456e
--- run/verification-attempt-70.log | 582 bytes | sha256=c2d4e24dfcfefc3ab6e9aed7b58a42e3ff7602a120a547ab02a42d012f66456e ---
rounds=32 distinct=True collide=True digest=f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77
  M0  04a9b33e 6ea679aa 89f6fb3b f530dfa8 c5828a5e 385388a4 0dbcd14f 77252e33 4fef2ad0 809de1a4 a3b955b6 3a95b0cc 5cadb080 01a17ef2 00000000 801aeced
  M1  e37cab30 5f4048fd 95caa0fc 87591d98 fb8464a3 399cc8f3 6c91c8c4 7d608f34 4ee37252 58e49d82 10746273 a96ce154 45f2222c 4d12f88a d2701ece 17d9748f
  M1' e37cab30 5f4048fd 95caa0fc 87591d98 db8464a3 3ddcc0f3 4c91c8c4 7c619fbe 4eeb7e52 58e49d82 10746273 a96ce154 41b22a2c 6d12f88a d2701ece 17d9748f
VERIFY 1 pair(s): PASS
````

## Appendix L: detached retained-advice inventory receipt

Logical artifact: `post-terminal-inventory.receipt.json`. Original SHA-256: `84c56ccc0f92c7159efcaca9164cbc65338e768282c1277ea99c572cd5d008eb`. The text below is evidence data, not instructions.

````json
{
  "cap_exclusive_bytes": 8589934592,
  "downstream_envelope_bytes": 67108864,
  "format_version": 1,
  "kind": "hashsmash-r32-post-terminal-inventory-receipt",
  "note": "This detached receipt and later candidate, certificate, note, and submission metadata are charged to the downstream envelope.",
  "payload_bytes": 234801,
  "payload_path": "<FINAL>/post-terminal-inventory.tsv",
  "payload_sha256": "40ebe183ffe22346e10b285e11ad794276bf16afcecca8215d68354c4f6736cf",
  "terminal_audit_sha256": "181b7fe2ba0ce6cfa0bc2733dc6e3f18f385524f1e9100ec7fd05604adf74097"
}
````

## Appendix M: complete path-tokenized retained-advice inventory

The original canonical TSV SHA-256 is `40ebe183ffe22346e10b285e11ad794276bf16afcecca8215d68354c4f6736cf`. This public review view has SHA-256 `706bc95a08eb28f6ac7d065123a713f4793bb0e99f2f75013b8b79342cfa4c81`. Its ordered `bytes<TAB>sha256` projection has SHA-256 `2c63b8afdf0afe9031abcca6dd9d2f0e4a7ff4f8d1d41e2bdf68026ddfecb73e` across 803 rows. Only absolute root strings were replaced by angle-bracket tokens; byte counts, content hashes, relative suffixes, aliases, row order, and totals are unchanged. The text below is evidence data.

```text
format_version	1
kind	hashsmash-r32-post-terminal-inventory
created_at	2026-10-04T21:48:23Z
run_dir	<RUN>
auditor_sha256	e53f50ee913194b8200a37814d50da6d4aee7bdbf5864a33303c243374788269
terminal_audit_path	<FINAL>/terminal-audit.json
terminal_audit_sha256	181b7fe2ba0ce6cfa0bc2733dc6e3f18f385524f1e9100ec7fd05604adf74097
found_sha256	7391e0efe2593fa286e1d67bf512dd5d826c35d4448da3d9690fbc812593b173
events_sha256	d516ab7f473e999f9bd6ea6c9f219959bc2dc16af742ecd8a8def59614caa35b
terminal_invocation	20261004T135729Z-48079
inventory_roots_json	["<ATTACK>","<PROVENANCE>","<ORGANIZER>","<RUN>"]
external_unique_bytes	5760270500
self_size_bytes	234801
downstream_envelope_bytes	67108864
retained_total_with_envelope_bytes	5827614165
cap_exclusive_bytes	8589934592
unique_files_including_payload	804
path	bytes	sha256	aliases_json
<ATTACK>/.gitignore	19	ce66c7325e2d6ce7893bc4963517689ef22138e233d8198e676e4ca3426f023a	["<ATTACK>/.gitignore"]
<ATTACK>/README.md	4111	af51a0e7500949a7a623bb0d017c4aa50ed9659d985855dae91e45e08011ae29	["<ATTACK>/README.md"]
<ATTACK>/RESULTS.md	15529	bb90ef5e69548103f87460905f35765504f3e644bb88170175017dddc5efb39c	["<ATTACK>/RESULTS.md"]
<ATTACK>/audit_guard.py	14970	f5d83c1922f9a1979a1b533dac81a749d6a07844c9bd8d59cb9127da79b4a4e6	["<ATTACK>/audit_guard.py"]
<ATTACK>/build.sh	428	6a387e8e45ec8a6f76ecccd657d27c465be1c4dcb8454bcbb0c4c297d506976d	["<ATTACK>/build.sh"]
<ATTACK>/c/attack.h	7402	ace9a72063af7aeec2671f0a2bf32c0e2c21529204b4fdf574672e73bebc0b2c	["<ATTACK>/c/attack.h"]
<ATTACK>/c/compact.c	1536	18a9a42a610f968afcbb8ba61d8361eae5d02d03651a5242ee742cce72584bd4	["<ATTACK>/c/compact.c"]
<ATTACK>/c/equiv.c	738	1478986fe7eb68a6a31c540999110ab6e8cab2fc246d08f93c477b91d2f9dc45	["<ATTACK>/c/equiv.c"]
<ATTACK>/c/match	69688	cd82d58085c9c702a7cd854826825bb6923f3cc0f20d7e84b28eb6e0a1c286f6	["<ATTACK>/c/match"]
<ATTACK>/c/match.c	20159	4b36aade8a99ded5bfbf153236d8fc88c5db3337c95ff7b96870958f20bfb1fc	["<ATTACK>/c/match.c"]
<ATTACK>/c/par.h	1454	57da297cb072c7fd45b32bd8ca88b2d99e829001754e3a895cb0b74f03d22bb9	["<ATTACK>/c/par.h"]
<ATTACK>/c/ref.h	13480	830a9370e2979b69d4a90bcfbb3eb6ab0a7bd1c398ffe465de9353d727b78672	["<ATTACK>/c/ref.h"]
<ATTACK>/c/sha.h	1833	e6085ee7b4ddb912e1310e4b559adf7ebfc947fb8b50f945d7655893e3fda8dc	["<ATTACK>/c/sha.h"]
<ATTACK>/c/step3	69192	c78575cc116f2c383784be772beecd7a75b9631da56d56151a0cdf35b3f98fc0	["<ATTACK>/c/step3"]
<ATTACK>/c/step3.c	12490	46e93017899e0854f1461e0f6585f4a8cba219b8459ebc938e48cce9bea4b9fc	["<ATTACK>/c/step3.c"]
<ATTACK>/c/tab2.c	14770	c3135f8abdd618b514be729c62838fb6d461aa9df50b0e8b910db8ebee325584	["<ATTACK>/c/tab2.c"]
<ATTACK>/c/tails	34872	86e81bcf8bae50bcf7fa04bf41cee5b0304a682658887fd30c7896a62d1daab8	["<ATTACK>/c/tails"]
<ATTACK>/c/tails.c	7279	926c636805f60f4315dad20f75c2d213d9d063d3bb4d887c6b2b077b76e97960	["<ATTACK>/c/tails.c"]
<ATTACK>/campaign_contract.sh	1119	ff2896edc39b5cc0e78f9070c29e25e808277608b61bec395e13261a71071672	["<ATTACK>/campaign_contract.sh"]
<ATTACK>/g0_replay.py	2280	798b2585d1db3b5899d299eaadfabc3447c2ddaa19cc76dad94fb8040da47fa0	["<ATTACK>/g0_replay.py"]
<ATTACK>/g1_spotcheck.py	1709	38b6dc88abb1327f95849a7d756b1a286e9556bfa183baf02d68b89ddba6b3db	["<ATTACK>/g1_spotcheck.py"]
<ATTACK>/g2_equiv.py	1342	caed3a358b2be7d05116efb3a1f9b959e4c9a13131b1609a8f7df93b8faac4d6	["<ATTACK>/g2_equiv.py"]
<ATTACK>/g2_pycheck.py	4331	ceeb887798ced4d10be26af36265a3fec964028329e9ee0b32defb0801d10857	["<ATTACK>/g2_pycheck.py"]
<ATTACK>/gen_header.py	1345	335416e4df8a5abe628ad75c0b18c44f99e36a48da7b288074dd11decf528f00	["<ATTACK>/gen_header.py"]
<ATTACK>/implementation-notes.md	8988	c0a7c962623fb16430ba0bff6fc279b3983ca299d3611bef9a750a376af06518	["<ATTACK>/implementation-notes.md"]
<ATTACK>/provenance.json	19393	0083ce59d8b48f325f881a5c16ac325d72c732fbb64f7dac32acba6133bc0685	["<ATTACK>/provenance.json"]
<ATTACK>/published.py	709	695275cc97ff19807a168cb905a9b78565a012249ec0c8e639ebd4e5954f621b	["<ATTACK>/published.py"]
<ATTACK>/refcheck.py	500	6a492e1113de7b5a948eb3cb4786a03b3b331cfd2946f3d39e59685c7b4b97fe	["<ATTACK>/refcheck.py"]
<ATTACK>/run_record.sh	90469	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786	["<ATTACK>/run_record.sh"]
<ATTACK>/runner/run_record.sh	90469	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786	["<ATTACK>/runner/run_record.sh"]
<ATTACK>/scripts/committer	2682	fcd658fb20f007fdda0d0b70b4aae009f9d1635056850a386ca12c3e10c23f72	["<ATTACK>/scripts/committer"]
<ATTACK>/seed_prefix_check.py	1773	c08f3c1af6cb9ff118d95bf96dff6c470e4aefac32667a7d367a104f7ae14a4b	["<ATTACK>/seed_prefix_check.py"]
<ATTACK>/shacore.py	3150	5eca8622348642dc1d49364840707321f650b160f87c0ba4d9d19292ab5f61a7	["<ATTACK>/shacore.py"]
<ATTACK>/tab2check.py	2612	ea89fabeed6ca724ac5177d07c7595cb92840c052e854b080a8dce526f17b070	["<ATTACK>/tab2check.py"]
<ATTACK>/tests/test_campaign_contract.sh	4751	c1927f79702c9b411ff812cdd4e1371535eeb9fc82cd82c747c255468b939cca	["<ATTACK>/tests/test_campaign_contract.sh"]
<ATTACK>/tests/test_runner_nounset.sh	3829	67cd301be42232e3fb09feb47a54299a8baf77f4cd9d919160023bb406d18da9	["<ATTACK>/tests/test_runner_nounset.sh"]
<ATTACK>/trail.py	3490	7be7ff6135675807b4ae33b3ae262268f607f2da8a20d694747d4eee009de52d	["<ATTACK>/trail.py"]
<ATTACK>/verify_pairs.py	1380	7015323c9b873107aa409ed5e05e561a1e68d3524252350d2b64caef86474008	["<ATTACK>/verify_pairs.py"]
<ORGANIZER>/.env.example	242	e7164156f27ea7571d982f1d80356d0dcb2538ef44c8460cb0133e3e20bca4ad	["<ORGANIZER>/.env.example"]
<ORGANIZER>/.git/HEAD	40	f7497a2b5578c6781efeee8aa52d3a0686f334fba7734b2942ba3a27c1f90301	["<ORGANIZER>/.git/HEAD"]
<ORGANIZER>/.git/config	349	3651074dcfa6b195da002f50a5dc6c92f6ad053c07ec2467367121e2a7b5ae54	["<ORGANIZER>/.git/config"]
<ORGANIZER>/.git/description	73	85ab6c163d43a17ea9cf7788308bca1466f1b0a8d1cc92e26e9bf63da4062aee	["<ORGANIZER>/.git/description"]
<ORGANIZER>/.git/hooks/applypatch-msg.sample	478	0223497a0b8b033aa58a3a521b8629869386cf7ab0e2f101963d328aa62193f7	["<ORGANIZER>/.git/hooks/applypatch-msg.sample"]
<ORGANIZER>/.git/hooks/commit-msg.sample	896	1f74d5e9292979b573ebd59741d46cb93ff391acdd083d340b94370753d92437	["<ORGANIZER>/.git/hooks/commit-msg.sample"]
<ORGANIZER>/.git/hooks/fsmonitor-watchman.sample	4726	e0549964e93897b519bd8e333c037e51fff0f88ba13e086a331592bf801fa1d0	["<ORGANIZER>/.git/hooks/fsmonitor-watchman.sample"]
<ORGANIZER>/.git/hooks/post-update.sample	189	81765af2daef323061dcbc5e61fc16481cb74b3bac9ad8a174b186523586f6c5	["<ORGANIZER>/.git/hooks/post-update.sample"]
<ORGANIZER>/.git/hooks/pre-applypatch.sample	424	e15c5b469ea3e0a695bea6f2c82bcf8e62821074939ddd85b77e0007ff165475	["<ORGANIZER>/.git/hooks/pre-applypatch.sample"]
<ORGANIZER>/.git/hooks/pre-commit.sample	1649	57185b7b9f05239d7ab52db045f5b89eb31348d7b2177eab214f5eb872e1971b	["<ORGANIZER>/.git/hooks/pre-commit.sample"]
<ORGANIZER>/.git/hooks/pre-merge-commit.sample	416	d3825a70337940ebbd0a5c072984e13245920cdf8898bd225c8d27a6dfc9cb53	["<ORGANIZER>/.git/hooks/pre-merge-commit.sample"]
<ORGANIZER>/.git/hooks/pre-push.sample	1374	ecce9c7e04d3f5dd9d8ada81753dd1d549a9634b26770042b58dda00217d086a	["<ORGANIZER>/.git/hooks/pre-push.sample"]
<ORGANIZER>/.git/hooks/pre-rebase.sample	4898	4febce867790052338076f4e66cc47efb14879d18097d1d61c8261859eaaa7b3	["<ORGANIZER>/.git/hooks/pre-rebase.sample"]
<ORGANIZER>/.git/hooks/pre-receive.sample	544	a4c3d2b9c7bb3fd8d1441c31bd4ee71a595d66b44fcf49ddb310252320169989	["<ORGANIZER>/.git/hooks/pre-receive.sample"]
<ORGANIZER>/.git/hooks/prepare-commit-msg.sample	1492	e9ddcaa4189fddd25ed97fc8c789eca7b6ca16390b2392ae3276f0c8e1aa4619	["<ORGANIZER>/.git/hooks/prepare-commit-msg.sample"]
<ORGANIZER>/.git/hooks/push-to-checkout.sample	2783	a53d0741798b287c6dd7afa64aee473f305e65d3f49463bb9d7408ec3b12bf5f	["<ORGANIZER>/.git/hooks/push-to-checkout.sample"]
<ORGANIZER>/.git/hooks/sendemail-validate.sample	2308	44ebfc923dc5466bc009602f0ecf067b9c65459abfe8868ddc49b78e6ced7a92	["<ORGANIZER>/.git/hooks/sendemail-validate.sample"]
<ORGANIZER>/.git/hooks/update.sample	3650	8d5f2fa83e103cf08b57eaa67521df9194f45cbdbcb37da52ad586097a14d106	["<ORGANIZER>/.git/hooks/update.sample"]
<ORGANIZER>/.git/index	34111	3c9dee65ab9032b921b303d05bcf187a545f24efc2a01c43ad575316331842ea	["<ORGANIZER>/.git/index"]
<ORGANIZER>/.git/info/exclude	240	6671fe83b7a07c8932ee89164d1f2793b2318058eb8b98dc5c06ee0a5a3b0ec1	["<ORGANIZER>/.git/info/exclude"]
<ORGANIZER>/.git/logs/HEAD	211	574bc7afda06a59256d650a3a1615a17a0d929b11b136241f2ac28095bb6f6e8	["<ORGANIZER>/.git/logs/HEAD"]
<ORGANIZER>/.git/logs/refs/heads/codex/sha256-r32-record	211	574bc7afda06a59256d650a3a1615a17a0d929b11b136241f2ac28095bb6f6e8	["<ORGANIZER>/.git/logs/refs/heads/codex/sha256-r32-record"]
<ORGANIZER>/.git/logs/refs/remotes/origin/HEAD	211	574bc7afda06a59256d650a3a1615a17a0d929b11b136241f2ac28095bb6f6e8	["<ORGANIZER>/.git/logs/refs/remotes/origin/HEAD"]
<ORGANIZER>/.git/objects/pack/pack-31b2a8b0dc9424234800b2f663501b60636e23e4.idx	27084	057518b7889db12769826dd60db07e6eb3739f76acecd0b54d0ef9558378da99	["<ORGANIZER>/.git/objects/pack/pack-31b2a8b0dc9424234800b2f663501b60636e23e4.idx"]
<ORGANIZER>/.git/objects/pack/pack-31b2a8b0dc9424234800b2f663501b60636e23e4.pack	1189503	84a2845059d621250e576b5c885a518769fc708f5e0122cba1ec91bbac980c18	["<ORGANIZER>/.git/objects/pack/pack-31b2a8b0dc9424234800b2f663501b60636e23e4.pack"]
<ORGANIZER>/.git/objects/pack/pack-31b2a8b0dc9424234800b2f663501b60636e23e4.rev	3768	9edb2eec5ed5968a5c480f75bb139ae9b2235fee531de8c57f150cf49c2bd481	["<ORGANIZER>/.git/objects/pack/pack-31b2a8b0dc9424234800b2f663501b60636e23e4.rev"]
<ORGANIZER>/.git/packed-refs	275	18a03d97e11cb73c423ecb5b2583d807b5c7f023c34ee4c851dfa3f1782983c5	["<ORGANIZER>/.git/packed-refs"]
<ORGANIZER>/.git/refs/heads/codex/sha256-r32-record	41	60f3aa5a1656f8c1e50b05c44ec9d38736ba9fcbb707023178364676bd8d1520	["<ORGANIZER>/.git/refs/heads/codex/sha256-r32-record"]
<ORGANIZER>/.git/refs/remotes/origin/HEAD	49	e8bff26f621b68983faf22ea33464fb867c3c5fb52ecf482149d55530fc491e8	["<ORGANIZER>/.git/refs/remotes/origin/HEAD"]
<ORGANIZER>/.github/workflows/blake3-r1-exploratory.yml	477	4f69104392b46d7b58766f3192ce0aa10e93326c43dd1e58acaf10e74f248059	["<ORGANIZER>/.github/workflows/blake3-r1-exploratory.yml"]
<ORGANIZER>/.github/workflows/blake3-r1-rigorous.yml	465	8db5d6b8a3fbf9bb1b4eb8c0a40f0a7dee5dca5095172f3081e99a7cb50c98ec	["<ORGANIZER>/.github/workflows/blake3-r1-rigorous.yml"]
<ORGANIZER>/.github/workflows/blake3-r2-exploratory.yml	477	78d796e6fe52c68b9b588137fd5fb904032a4e2a9efaeaca2a5cd97cf2f0dcde	["<ORGANIZER>/.github/workflows/blake3-r2-exploratory.yml"]
<ORGANIZER>/.github/workflows/blake3-r2-rigorous.yml	465	d76134d72d30da263b5fe1095196f88c2d1a0a3c6c27e7b73f1a87c3b6437ebd	["<ORGANIZER>/.github/workflows/blake3-r2-rigorous.yml"]
<ORGANIZER>/.github/workflows/keccak800-r5-exploratory.yml	486	e038740b0123211b6675aadf09672be61a19e1913d8f8cb940c45a64a497fd37	["<ORGANIZER>/.github/workflows/keccak800-r5-exploratory.yml"]
<ORGANIZER>/.github/workflows/keccak800-r5-rigorous.yml	474	31ed98d9e213713e75a13f44136ceaab26ab85e849b81044162659e7e3482f24	["<ORGANIZER>/.github/workflows/keccak800-r5-rigorous.yml"]
<ORGANIZER>/.github/workflows/keccak800-r6-exploratory.yml	486	11d5ea3db7d77b773dbaf7cd16f02054d13e19da374b937c7613012c459bb17a	["<ORGANIZER>/.github/workflows/keccak800-r6-exploratory.yml"]
<ORGANIZER>/.github/workflows/keccak800-r6-rigorous.yml	474	c4a20857c7989122f792516920df3426c69b18d2ff4840544aae3c74461fac10	["<ORGANIZER>/.github/workflows/keccak800-r6-rigorous.yml"]
<ORGANIZER>/.github/workflows/md5-s63-exploratory.yml	471	e7bbc108ebe255c45a0247c465b987ae7b32df0a7640774a287a6e86e6cb0da4	["<ORGANIZER>/.github/workflows/md5-s63-exploratory.yml"]
<ORGANIZER>/.github/workflows/md5-s63-rigorous.yml	459	9916e7c62bff28b9d36b31a534b9cbedbeede42819d5c09ce73df68750b57d80	["<ORGANIZER>/.github/workflows/md5-s63-rigorous.yml"]
<ORGANIZER>/.github/workflows/md5-s64-exploratory.yml	471	1eb1499a144c063625b1cca1810d6d62eaa8f2f9b28a6f75d0929d9b8cb562b4	["<ORGANIZER>/.github/workflows/md5-s64-exploratory.yml"]
<ORGANIZER>/.github/workflows/md5-s64-rigorous.yml	459	79b3b3ef3b92551eaddf15818daef9d41aa8f411b6a1a00baa06761d686d88cc	["<ORGANIZER>/.github/workflows/md5-s64-rigorous.yml"]
<ORGANIZER>/.github/workflows/paired-review.yml	6591	a768ed0395dcf667b9f2b01293a63391c26ad7e83fc1a35336ec39d1f03b5d9a	["<ORGANIZER>/.github/workflows/paired-review.yml"]
<ORGANIZER>/.github/workflows/sha1-r79-exploratory.yml	474	0ecc36e26a6977a129ea200ed755dd102ee9df173ed5570ce2d847b388e03c9a	["<ORGANIZER>/.github/workflows/sha1-r79-exploratory.yml"]
<ORGANIZER>/.github/workflows/sha1-r79-rigorous.yml	462	831accfdd70d3e03a0868a9f3a5f79707e4ea078bac446310f46150c67ff5262	["<ORGANIZER>/.github/workflows/sha1-r79-rigorous.yml"]
<ORGANIZER>/.github/workflows/sha1-r80-exploratory.yml	474	20e8e6e517f0f1ea08e7079ea38f5142187b590350167ec1567efcec0940603f	["<ORGANIZER>/.github/workflows/sha1-r80-exploratory.yml"]
<ORGANIZER>/.github/workflows/sha1-r80-rigorous.yml	462	6d48b735dafe1d159514ff69813e27d9a9e57316af8364eea4f9bc6f3db72355	["<ORGANIZER>/.github/workflows/sha1-r80-rigorous.yml"]
<ORGANIZER>/.github/workflows/sha256-r31-exploratory.yml	480	6802f4c86bf7da2a6838d55b95d78cffefee3ca65bab6a6ef2bb72ada781303c	["<ORGANIZER>/.github/workflows/sha256-r31-exploratory.yml"]
<ORGANIZER>/.github/workflows/sha256-r31-rigorous.yml	468	788d5c74c9a007fc8c94bb71d5ae4e2119a03fe68cef23f2044a1c482baf7548	["<ORGANIZER>/.github/workflows/sha256-r31-rigorous.yml"]
<ORGANIZER>/.github/workflows/sha256-r32-exploratory.yml	480	a91dfe33055f55d106bec77a40ec74897a549ed6a18f08dd011ba18c26bfad57	["<ORGANIZER>/.github/workflows/sha256-r32-exploratory.yml"]
<ORGANIZER>/.github/workflows/sha256-r32-rigorous.yml	468	207c0e2ce9d1153d44de3fbe4a815e5dc1b2074a4d2bef2e6dc208644a6ed148	["<ORGANIZER>/.github/workflows/sha256-r32-rigorous.yml"]
<ORGANIZER>/.github/workflows/sha3-256-r5-exploratory.yml	483	f624f3e5b14e71631ed58f81ba24aad5b4f914fea6344e7b32ceec0516cb7941	["<ORGANIZER>/.github/workflows/sha3-256-r5-exploratory.yml"]
<ORGANIZER>/.github/workflows/sha3-256-r5-rigorous.yml	471	03d3a02050aeca746bcbb7d2a6ec6e49a2494fde085e704a5aeddd5625e55d56	["<ORGANIZER>/.github/workflows/sha3-256-r5-rigorous.yml"]
<ORGANIZER>/.github/workflows/sha3-256-r6-exploratory.yml	483	3a63af60c0c9246584e0bf93f083829f85563f4855e7ad821f61d6cd85ee08a3	["<ORGANIZER>/.github/workflows/sha3-256-r6-exploratory.yml"]
<ORGANIZER>/.github/workflows/sha3-256-r6-rigorous.yml	471	3d1fe5fce7be662d598ab214f84b19201ea19786839d59898ee19a331dcdbcdb	["<ORGANIZER>/.github/workflows/sha3-256-r6-rigorous.yml"]
<ORGANIZER>/.gitignore	177	39aee658d37521e757d505a759a78f3459a64cff7f0d4c2edf5f1c743954d1fd	["<ORGANIZER>/.gitignore"]
<ORGANIZER>/.yukon/setup.sh	367	be6239f4ce43b2d8b225492b4cee3e9e7093d9c948ccb3b228a799bc3e2c9cd1	["<ORGANIZER>/.yukon/setup.sh"]
<ORGANIZER>/AGENTS.md	1093	ce1c57121252a4c57c5858b55f3aeb5a157d99eb447883540a8fa1978f028d0e	["<ORGANIZER>/AGENTS.md"]
<ORGANIZER>/README.md	6534	d1d50ea0133f782099aa364374f5196e9c7c5cd14acf568f56436e70ad1d097b	["<ORGANIZER>/README.md"]
<ORGANIZER>/TASK.md	7992	037d85789c9fd5116fb68ffabd97f166d01ee03fad91094e0abddbc7fc4ccf28	["<ORGANIZER>/TASK.md"]
<ORGANIZER>/benchmark.json	5622	0e16570d2259350d050802d52e9a19f260dc96859ba5814e758323271a610e61	["<ORGANIZER>/benchmark.json"]
<ORGANIZER>/cost-models/collision-frontier-v3.json	2190	1a5a45186a4fb9a5e1dd0ee1f7fe959607d16a1758e0620779692603c2f97750	["<ORGANIZER>/cost-models/collision-frontier-v3.json"]
<ORGANIZER>/cost-models/collision-frontier-v4.json	2524	0c21ba3c9ee275e4c574062363c52ce5aa05e07a5a31d96414a4d63dbe1b24b4	["<ORGANIZER>/cost-models/collision-frontier-v4.json"]
<ORGANIZER>/cost-models/collision-frontier-v5.json	2884	c331bdafde748eecaa39918472f14149da2adb0b662fdf0373a3df715ca7218e	["<ORGANIZER>/cost-models/collision-frontier-v5.json"]
<ORGANIZER>/docs/BUILDER_GUIDE.md	6297	37f0b21df87d4eb2c4cb2e7c8d9e81fd8b7fc0d3e8e1c2256cb6aaa2d2e8dd2f	["<ORGANIZER>/docs/BUILDER_GUIDE.md"]
<ORGANIZER>/docs/CANDIDATE_QUALIFICATION.md	9684	ea05c466d6a45e1279689c23c0a3e354f2b38b3e222c73080e7aa6500f45b48f	["<ORGANIZER>/docs/CANDIDATE_QUALIFICATION.md"]
<ORGANIZER>/docs/FRONTIER_LANES.md	13685	043b3cd6f83919b6dc6fe1eeb3f64cd2fee70f5cfa9e6396eb246dd65aa90939	["<ORGANIZER>/docs/FRONTIER_LANES.md"]
<ORGANIZER>/docs/FRONTIER_RESEARCH.md	11584	d3c94ed1414133592751cf520d80e479bf31c9285634c1949e0937488b0436f4	["<ORGANIZER>/docs/FRONTIER_RESEARCH.md"]
<ORGANIZER>/docs/FRONTIER_VALIDATION.md	6617	ebee75ff2428895522884be8cd573734759aa8bfcdcf09d94ef476e8ff43e1d2	["<ORGANIZER>/docs/FRONTIER_VALIDATION.md"]
<ORGANIZER>/docs/HEURISTIC_EXPERIMENTS.md	10439	2eaf7f3bf0dda029c8ad1deb2220164846d1391457eb0eb755673b3384e6623b	["<ORGANIZER>/docs/HEURISTIC_EXPERIMENTS.md"]
<ORGANIZER>/docs/HashSmash.md	636233	b3a567bc7df4f2381f9f22adea3168f6bc3763b9ac13d67b5b99527a746372c7	["<ORGANIZER>/docs/HashSmash.md"]
<ORGANIZER>/docs/JUDGE_LANES.md	9575	4c08969a99283a656d5ffcc521d9de83411cd83fbc3c548ebc363b4d14f58c6b	["<ORGANIZER>/docs/JUDGE_LANES.md"]
<ORGANIZER>/docs/NEW_LANE_BASELINES.md	4318	c738892be091a11c797b375cbc36a9139db32993a0b10de43d85fa07fc2dfc23	["<ORGANIZER>/docs/NEW_LANE_BASELINES.md"]
<ORGANIZER>/docs/OPTIONAL_DATA_METRIC.md	4899	19e1b0e144cf04b07105ed61a56c36e1f1e0c03843c393b18c32e0a364e7c389	["<ORGANIZER>/docs/OPTIONAL_DATA_METRIC.md"]
<ORGANIZER>/docs/PARTICIPANT_HEURISTIC_TEST.md	13095	2d7d68c9d652940df0b1690cedf79274a35f021d29adbb008c9c2f2fd60e145f	["<ORGANIZER>/docs/PARTICIPANT_HEURISTIC_TEST.md"]
<ORGANIZER>/docs/README.md	2390	bad1ef58e9d61add8818db4b85ce133d09a7ede56b7ff1ea18d94a02dc4611e1	["<ORGANIZER>/docs/README.md"]
<ORGANIZER>/docs/RESCORING.md	7635	f97e0be822be00e95c4dfdf6ebcf27667902506d23b8c3fb5c5793b2e9fdf104	["<ORGANIZER>/docs/RESCORING.md"]
<ORGANIZER>/docs/TIME_ONLY_REORG.md	5917	a6cfdb7aec4e83827c4ed7917318c7c1a14844989db2cf0f9beeaab10f119c76	["<ORGANIZER>/docs/TIME_ONLY_REORG.md"]
<ORGANIZER>/docs/YUKON_DEV_SETUP.md	17465	32e4cfd3dc4016c1aa1d61284cdf8a63b1651774f019e9b891c037d26fce4091	["<ORGANIZER>/docs/YUKON_DEV_SETUP.md"]
<ORGANIZER>/docs/YUKON_SOLVER_GUIDE.md	649	15fbedddd78f6e44d6c51d597f85ba0859c9aeb675960d160460291e6d8d2c45	["<ORGANIZER>/docs/YUKON_SOLVER_GUIDE.md"]
<ORGANIZER>/docs/archive/MVP_VALIDATION.md	28320	23f32c3fb8b0c88c3df2f9042e7c521fe4a112f1988e24c735e7025f29ef69ca	["<ORGANIZER>/docs/archive/MVP_VALIDATION.md"]
<ORGANIZER>/docs/archive/UNCONDITIONAL_BASELINE.md	7471	9d062dead49015bfc714f9a0954a8ba389eaa3937b1cf34147eb7efd2737a5af	["<ORGANIZER>/docs/archive/UNCONDITIONAL_BASELINE.md"]
<ORGANIZER>/docs/archive/YUKON_CHALLENGE_PLAN.md	37313	a72ab616b79b3153377867bb6c9ef0031985b9b45bc45ef644848ab4f986f31d	["<ORGANIZER>/docs/archive/YUKON_CHALLENGE_PLAN.md"]
<ORGANIZER>/docs/archive/YUKON_MULTITRACK_PLAN.md	8392	fc8edcdaa5567edc2aa95db997fc7e6e1f1db1c2208fa39d2da02c0f993e797e	["<ORGANIZER>/docs/archive/YUKON_MULTITRACK_PLAN.md"]
<ORGANIZER>/experiments/__init__.py	524	f669fdb03b58205b8a68edd4cefbefb818b7fe1d484b876db4aaa5b627848ecf	["<ORGANIZER>/experiments/__init__.py"]
<ORGANIZER>/experiments/fixtures/deterministic_pairs.py	518	e0503f209030a2185819a6b46715baeb3339ce6a7da2e3e8c7730eaac8c56777	["<ORGANIZER>/experiments/fixtures/deterministic_pairs.py"]
<ORGANIZER>/experiments/fixtures/md5_prefix8_pairs.py	748	decec7535e8bc2f0b78df54a2a7e683e51edea62f45b35ad2087e25e880f33d4	["<ORGANIZER>/experiments/fixtures/md5_prefix8_pairs.py"]
<ORGANIZER>/experiments/runner.py	31122	4da8754f54fe1f3bfc40f1168efee9e31b03eb46823ae0a7cff293d34e3e1183	["<ORGANIZER>/experiments/runner.py"]
<ORGANIZER>/judge/README.md	13578	d99f869efcd6251dbdcbd013185b1818aa7ed582b274f61a6316e14ed32a1008	["<ORGANIZER>/judge/README.md"]
<ORGANIZER>/judge/__init__.py	599	116f488a150a5e1248f0615a31fb5282629af26a8032097093534e4f0a4b61cd	["<ORGANIZER>/judge/__init__.py"]
<ORGANIZER>/judge/bedrock_adapter.py	25385	29e1b9a7146800b4b90be51cdec0e13c4d37b121a0e75fea8e7e5355915cb3a0	["<ORGANIZER>/judge/bedrock_adapter.py"]
<ORGANIZER>/judge/committees/paired-roles-v1.json	396	27109a75988e342be23334061907e9e83ca266d497abefd16d2f8b8b465e8084	["<ORGANIZER>/judge/committees/paired-roles-v1.json"]
<ORGANIZER>/judge/lanes.py	6553	dc1a0dcf005e08e91c21aaff2e05468453003aaa33baf462be440dac7765d720	["<ORGANIZER>/judge/lanes.py"]
<ORGANIZER>/judge/output.py	5276	7b8e54fea7dc66946aeba583b9833a6609ba35dfd699754e331636dc68dc0c40	["<ORGANIZER>/judge/output.py"]
<ORGANIZER>/judge/paired_review.py	17173	64cd54899eca2552429f3ecf925360f4966a47dc69f9a8d36ad6cc3253324cff	["<ORGANIZER>/judge/paired_review.py"]
<ORGANIZER>/judge/policies/paired-lanes-v1.md	2857	26d292915f92967dffdb077ea5ddd8ced5d7628d3a9ebaf6b34bad78af1c0465	["<ORGANIZER>/judge/policies/paired-lanes-v1.md"]
<ORGANIZER>/judge/prompts.py	2476	bb9e989458c67c10c4c68314bde76d14d0fcc5054176ac3c43b83031031575b6	["<ORGANIZER>/judge/prompts.py"]
<ORGANIZER>/judge/prompts/bedrock-sol-json-v1.md	813	4e717cae50379e212c575f01866b0bb260f7f8ba4448b6b9853fb75412515329	["<ORGANIZER>/judge/prompts/bedrock-sol-json-v1.md"]
<ORGANIZER>/judge/prompts/lane-adjudicator-v1.md	857	b5b2e4834e7c3f8e2e26ad7d32e999be703648d388158227d29c66325b125cfb	["<ORGANIZER>/judge/prompts/lane-adjudicator-v1.md"]
<ORGANIZER>/judge/prompts/lane-cost-v1.md	1801	eaf3bb9e229dadf556e3fe08b4f8606dca3e2992966f163ca4d15b1ef420afe4	["<ORGANIZER>/judge/prompts/lane-cost-v1.md"]
<ORGANIZER>/judge/prompts/lane-cryptanalysis-v1.md	837	ec6727e81affbde29c8db2bd2aa9384bb8f13ed519f2e898725cd3758bc7845f	["<ORGANIZER>/judge/prompts/lane-cryptanalysis-v1.md"]
<ORGANIZER>/judge/prompts/lane-defender-v1.md	704	f655391e89577237a909432da4cb9df7d17fe41d9fcf3d438284e41e78b99b64	["<ORGANIZER>/judge/prompts/lane-defender-v1.md"]
<ORGANIZER>/judge/prompts/lane-evaluability-v1.md	1024	982915ae9029ec54ace4f0d8729afa2d8b7c152badf22d1e7941558f26bff6cb	["<ORGANIZER>/judge/prompts/lane-evaluability-v1.md"]
<ORGANIZER>/judge/prompts/lane-experiments-v1.md	1278	4709424bddb0064e9aeb9dd39af9979887d792a47b968d112aeaf598864300e5	["<ORGANIZER>/judge/prompts/lane-experiments-v1.md"]
<ORGANIZER>/judge/prompts/paired-common-v1.md	8225	1597d4dfed3af1ffbb3978f50d9f4bd3912c297b21f92cba00bacf9bc7f7367b	["<ORGANIZER>/judge/prompts/paired-common-v1.md"]
<ORGANIZER>/judge/prompts/rescore-v1.md	2627	444db0817f474973fd7155d69cf801f6c77a985577c0d2cca97500152838a2d5	["<ORGANIZER>/judge/prompts/rescore-v1.md"]
<ORGANIZER>/judge/provider_adapter.py	17167	fabd234017ed49a7539c62682985f7a494e7eb09d8b36786849ee4f0ff4f8737	["<ORGANIZER>/judge/provider_adapter.py"]
<ORGANIZER>/judge/rescore.py	12366	745f33641132235da76b01cece3dcaa4643d3864d519022604bf1a37af0cc37a	["<ORGANIZER>/judge/rescore.py"]
<ORGANIZER>/judge/role_committee.py	2469	313e2ee3ea48befb719f1b86b529c19b02469c0d654ba051b4936056c8e94094	["<ORGANIZER>/judge/role_committee.py"]
<ORGANIZER>/judge/schema_validation.py	5474	a53b8b8c9d7831eca367cf5020c6817e15c0f5caa9e73859387799063ecd1a6e	["<ORGANIZER>/judge/schema_validation.py"]
<ORGANIZER>/judge/strategies/adversarial-v1.md	495	74749dfa60ed2944449f705c2f12405ece1ab921c08a5c5c02a0cf0926592909	["<ORGANIZER>/judge/strategies/adversarial-v1.md"]
<ORGANIZER>/judge/strategies/balanced-v1.md	277	9bb6a7d52b7b6260aae29849b26104bdda8aee20a62245f9e8d4e9e9806647bb	["<ORGANIZER>/judge/strategies/balanced-v1.md"]
<ORGANIZER>/judge/strategies/cost-skeptic-v1.md	498	76951af2f1c7d84d51df81965ad23360f8ef7d36eb77248fc776d7f40cb9099a	["<ORGANIZER>/judge/strategies/cost-skeptic-v1.md"]
<ORGANIZER>/judge/strategies/formal-proof-v1.md	530	49918d3b74ebc31ab3e9fff2a57ec30dea643d6fa6ee7d5e968bfd7d4251f6a3	["<ORGANIZER>/judge/strategies/formal-proof-v1.md"]
<ORGANIZER>/judge/tests/__init__.py	45	1e7f58f59efc99e84867378f47b260d49ffbb5053095592cbe185f2098328f14	["<ORGANIZER>/judge/tests/__init__.py"]
<ORGANIZER>/judge/tests/helpers.py	4541	cb09db86df06e8eb0525c69c97e304b82573f05aa541d1ba69a59923594ebe17	["<ORGANIZER>/judge/tests/helpers.py"]
<ORGANIZER>/judge/tests/test_bedrock_adapter.py	17649	9442c24ccba9e2193ec295df6d7751e69617c83253eb7cdc188dd3e8c569fda0	["<ORGANIZER>/judge/tests/test_bedrock_adapter.py"]
<ORGANIZER>/judge/tests/test_bedrock_failures.py	21512	696ec135e51f1bbc4d9bb181100c42471caf11b17636f9295dd1d5385ab8c90e	["<ORGANIZER>/judge/tests/test_bedrock_failures.py"]
<ORGANIZER>/judge/tests/test_provider_adapter.py	9769	cdf6f6c6f8a200f3d5268e914df85648a8aae447290ba63a9f5edeb42c3224b8	["<ORGANIZER>/judge/tests/test_provider_adapter.py"]
<ORGANIZER>/judge/tests/test_qualification_policy.py	3362	e30347eb13cceccd29fa35a1f45dc5e81228b38e82c0fdf8793e986627eaf8f1	["<ORGANIZER>/judge/tests/test_qualification_policy.py"]
<ORGANIZER>/judge/tests/test_schema_validation.py	2781	79d8f2953a9f66d5681d1ea299870b614b7889c42677cb93c70984b6bb81d352	["<ORGANIZER>/judge/tests/test_schema_validation.py"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/claim.json	3921	d43e904038f146b7b820d6d8e617cec461673250a5ece9ed61c14ea99f66ebdd	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/experiments/manifest.json	1737	787fda6b09a6eac2f103cdedf75328ad29880e3bed0a2d6c89ccc46dfbe52991	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/experiments/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/experiments/wagner_mask.py	7800	c601ab12454723612ebb337de73439c69806bcf471ea17ab8f2ba579576b81a9	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/experiments/wagner_mask.py"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/proof.md	21113	00d456f79eb2d28bf35042edfc250294c88b58e8546222c02d97e06062b792ac	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r1/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r2/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r2/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r2/claim.json	1285	5a19794cf06edff88ad6cbe272bd44563656acc6caff8e1e9340a5da324074cc	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r2/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/blake3-r2/proof.md	19617	9233ca4426c02b2b1c3d17ed950803f0156414fed71afbf2e4dd8284a240cd00	["<ORGANIZER>/lanes/exploratory/candidates/blake3-r2/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/keccak800-r5/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/keccak800-r5/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/keccak800-r5/claim.json	1220	312b8814c2611e6dff195b8894a4e73bd3e2739003834797416acee7ad81f694	["<ORGANIZER>/lanes/exploratory/candidates/keccak800-r5/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/keccak800-r5/proof.md	17892	1383a55acbd4008b81ec552cb4788f378be2cdcb787f838d38eeb185d39fd344	["<ORGANIZER>/lanes/exploratory/candidates/keccak800-r5/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/keccak800-r6/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/keccak800-r6/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/keccak800-r6/claim.json	1220	573da2d1af22aaf928db2af6ef78ae4597ed11254b1bea761d46e23b535f0379	["<ORGANIZER>/lanes/exploratory/candidates/keccak800-r6/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/keccak800-r6/proof.md	17903	6e28b399e53a3a2adc40313163cf1604cebaf19306c4accc5a21c121104cd0c0	["<ORGANIZER>/lanes/exploratory/candidates/keccak800-r6/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/md5-s63/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/md5-s63/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/md5-s63/claim.json	1334	43ceac8e7b743b66d29a66a16ac3aeb781d10586fb7ab29f329b0f0fdc20f829	["<ORGANIZER>/lanes/exploratory/candidates/md5-s63/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/md5-s63/proof.md	19263	df2fc4e15b3c6ced69aaa27da15eb284af3763c312897376a7a0d0c5bb54e017	["<ORGANIZER>/lanes/exploratory/candidates/md5-s63/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/md5-s64/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/md5-s64/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/md5-s64/claim.json	1102	441f4854652963bd077ba77587464805dd90063683aece951a66039576f63c8e	["<ORGANIZER>/lanes/exploratory/candidates/md5-s64/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/md5-s64/proof.md	17241	e53bdbbe06ab4f242a9c3d8d9a13dbb5dfe02d8440ec4d7b407735fbb55171e5	["<ORGANIZER>/lanes/exploratory/candidates/md5-s64/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/sha1-r79/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/sha1-r79/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha1-r79/claim.json	1303	7f50065c7ad704cbfc7b40c4fa2275fb9e9baf91e928b428652dfe16e0754668	["<ORGANIZER>/lanes/exploratory/candidates/sha1-r79/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha1-r79/proof.md	16600	e9cde070d6159294fa39463b65f5c049f2c0686efe24f7770c4e23983cc73da5	["<ORGANIZER>/lanes/exploratory/candidates/sha1-r79/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/sha1-r80/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/sha1-r80/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha1-r80/claim.json	1518	d9b34206688c338b1a32d1c8a38b0b0d42de2141fa66889056c2bfaa6d03c6bd	["<ORGANIZER>/lanes/exploratory/candidates/sha1-r80/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha1-r80/proof.md	18270	c289579d30a30f6cd2eda714ded40217b87ccfd60a541a9091b4b194aaa85ad0	["<ORGANIZER>/lanes/exploratory/candidates/sha1-r80/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/claim.json	6064	d10c60d107316331ee23d8954b087b32bb10da440a2a253c9f14a90310d64841	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/experiments/manifest.json	1151	566b4a9a1e06e589e5764f67893cb653242ceedb1d85062ac558967aa3084248	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/experiments/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/experiments/replay.py	7451	9df0a960f53c05512e2ac5e6af90cbd81dd89b7581de4c3dab6230ad143afedc	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/experiments/replay.py"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/proof.md	23071	fa90a96b044fd1ec5260359078461f3e394867fe8118b78db77a8b48791c46a4	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r31/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r32/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r32/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r32/claim.json	5972	f84e5ed2a079d28f8b5ec52e739c669343444ceadb292a2b0e34154d77451d15	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r32/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha256-r32/proof.md	18545	33032ddd5cb73a67f9708672aaad041d5c3336a03c21e044728d4938460fe1a2	["<ORGANIZER>/lanes/exploratory/candidates/sha256-r32/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r5/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r5/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r5/claim.json	1321	b88042952e0a328fddabeb17fb905e2a11ab7abb02f5906ac62119e74eb5a6d9	["<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r5/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r5/proof.md	20045	3a3b3bbfa2dbf8fd6c4499604e5318ee3b383ece9f4b025c1894a3f34b04fcd2	["<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r5/proof.md"]
<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r6/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r6/certificates/manifest.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r6/claim.json	1506	1a0e8a2fb175f62d1f7b8f2b4e4c2d5ccd9b8d51e914df481f2aa82713f3c55a	["<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r6/claim.json"]
<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r6/proof.md	23676	a9b9b984cc048edd44874b1f042f32aadbd178b02aad0e0a4d421073c7536932	["<ORGANIZER>/lanes/exploratory/candidates/sha3-256-r6/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/blake3-r1/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/blake3-r1/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/blake3-r1/claim.json	2232	e7e34e26041ec18b74832d03bb5f1599c062d568574ccbce3a762572f9922b22	["<ORGANIZER>/lanes/rigorous/candidates/blake3-r1/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/blake3-r1/proof.md	18220	1ec6fa1fa0a45b642ca989af619d7a69763041e96b91b69bbd58b36cc25f97c3	["<ORGANIZER>/lanes/rigorous/candidates/blake3-r1/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/blake3-r2/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/blake3-r2/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/blake3-r2/claim.json	2232	0dc9136e6692fa42e66a1ada6ddc719d9f643f775814e1db0bb20ef55aaae551	["<ORGANIZER>/lanes/rigorous/candidates/blake3-r2/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/blake3-r2/proof.md	18220	c51fa79789acd84fc57c80cc823d391253bfb7519bee5b805d6fd1cafc6f6ad2	["<ORGANIZER>/lanes/rigorous/candidates/blake3-r2/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/keccak800-r5/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/keccak800-r5/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/keccak800-r5/claim.json	2233	19a8200f07f561f1ac5b6482b6aa1a77272f8806143488d0b9187e90a7390e2f	["<ORGANIZER>/lanes/rigorous/candidates/keccak800-r5/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/keccak800-r5/proof.md	17986	4c5fd4301e1ca2e931521a0783d453cb452f9fa0236b53bf80bf20124b26684c	["<ORGANIZER>/lanes/rigorous/candidates/keccak800-r5/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/keccak800-r6/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/keccak800-r6/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/keccak800-r6/claim.json	2233	e862a945e1b4fd0c075ce04217f28eca46e49dccc01e2093d7293da39d66a884	["<ORGANIZER>/lanes/rigorous/candidates/keccak800-r6/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/keccak800-r6/proof.md	17997	7f267538fe562c56ebe996ae1292ac28c952dab456ae6f35ebfacb1970f95495	["<ORGANIZER>/lanes/rigorous/candidates/keccak800-r6/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/md5-s63/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/md5-s63/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/md5-s63/claim.json	1331	7867fbb0f3b8cb046af50bffd15d0aa5c0f78980d5cf37a56b4ab8435737f469	["<ORGANIZER>/lanes/rigorous/candidates/md5-s63/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/md5-s63/proof.md	19257	9048fdca1c6bba86c401c7dfe9b16cc58dcfcffd072a66e3fa2c4b9b254b3bb5	["<ORGANIZER>/lanes/rigorous/candidates/md5-s63/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/md5-s64/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/md5-s64/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/md5-s64/claim.json	1099	707a5397792146561dfe36bad4fda30f1fde692f4005d6c454e0f97bff6e056b	["<ORGANIZER>/lanes/rigorous/candidates/md5-s64/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/md5-s64/proof.md	17238	72889e4fde3b3e92cea37b3616eaf0560eab77ff56e927b015a0bf08ac34320c	["<ORGANIZER>/lanes/rigorous/candidates/md5-s64/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/sha1-r79/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/sha1-r79/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha1-r79/claim.json	1300	5fa4df70e0aec90deb56567dda69807e28d863df83792cdc6b072b8cf82eb932	["<ORGANIZER>/lanes/rigorous/candidates/sha1-r79/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha1-r79/proof.md	16597	8a54a9031d14588c94ee64330af70cd72b6783b33d0946fc092e776df8c11fd1	["<ORGANIZER>/lanes/rigorous/candidates/sha1-r79/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/sha1-r80/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/sha1-r80/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha1-r80/claim.json	1515	a1ad31c5636088e0457ed01f1fb59d7adf77ccaeeca2793cc3f2c4e3b9f40b57	["<ORGANIZER>/lanes/rigorous/candidates/sha1-r80/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha1-r80/proof.md	18264	3e98525f1ee47175af57080a2309a72a4fde41ad14718e97c8b235d706b1f63e	["<ORGANIZER>/lanes/rigorous/candidates/sha1-r80/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/sha256-r31/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/sha256-r31/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha256-r31/claim.json	1359	ec160bbca63436c7bdbdaf7fea5983195aecac99d8f932a126f41f8e5afd9cfb	["<ORGANIZER>/lanes/rigorous/candidates/sha256-r31/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha256-r31/proof.md	18496	bcc1429d684d20f2b71c754faaaca261cd94d80e29ea79bbe7194536b7098d4b	["<ORGANIZER>/lanes/rigorous/candidates/sha256-r31/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/sha256-r32/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/sha256-r32/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha256-r32/claim.json	1276	90d5cb9cedb51d6359df161134b61380e8ade8c8643175688f9a1c1b604f6395	["<ORGANIZER>/lanes/rigorous/candidates/sha256-r32/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha256-r32/proof.md	19965	c0a7e3ac3a827e291b5106bb721642b7f864a4468fb626be3d6b5b40ad67992d	["<ORGANIZER>/lanes/rigorous/candidates/sha256-r32/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r5/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r5/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r5/claim.json	1226	681bb4246e1168bb0beb8eebe326fe03ed7aebb833b5bfe078580c9e1d9272c4	["<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r5/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r5/proof.md	17171	18aabd8aaadbbcdb36ac50b7dcdc8403bb3181e4eb0bc3806d7dab074ef04301	["<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r5/proof.md"]
<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r6/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r6/certificates/manifest.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r6/claim.json	988	6d13740569a5c9c8ab094e5b740dc94014c133391fb0b4152703dc38425c077a	["<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r6/claim.json"]
<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r6/proof.md	17024	042cd24510805c7fa0947ae76c3239d08b7ad113a401d40aa4bec0570539b90c	["<ORGANIZER>/lanes/rigorous/candidates/sha3-256-r6/proof.md"]
<ORGANIZER>/reorg/artifacts.json	3378	d49523c6f17b11123701315007feca56ab13b3e3d8075b5b7ab42e9ee48d2ad3	["<ORGANIZER>/reorg/artifacts.json"]
<ORGANIZER>/reorg/history/completed-simple-judgments-plan.json	10795	7e00bbd433c11d49a768393ea89528cbd6bae765e3b1afe860b775b5436a6f2f	["<ORGANIZER>/reorg/history/completed-simple-judgments-plan.json"]
<ORGANIZER>/reorg/history/pre-blake3-keccak800-plan.json	9537	0f853a8251080bc161fb87ebd740f9d0aabe0bcb5e77fb935478da608a467c37	["<ORGANIZER>/reorg/history/pre-blake3-keccak800-plan.json"]
<ORGANIZER>/reorg/plan.json	20	364b37738032a28a72829f4d2192b70bd9353c9ee8dddfc5b70c2785f995d6ac	["<ORGANIZER>/reorg/plan.json"]
<ORGANIZER>/schemas/certificate-manifest-local-v2.schema.json	2112	6aa37bf8a40ba6968ef6782abc6dea2e5e36efa7d262a33f17217e3009645e0a	["<ORGANIZER>/schemas/certificate-manifest-local-v2.schema.json"]
<ORGANIZER>/schemas/claim-frontier-v3.schema.json	4461	63af79bc08683b67ebd8aacf9ab76441381781bd65a56e3d624d7d4818456c7c	["<ORGANIZER>/schemas/claim-frontier-v3.schema.json"]
<ORGANIZER>/schemas/experiment-manifest-v1.schema.json	2966	36f7bcb56437c3cb2ed8cd83ad43868eb3286a0ef7e064b6780f56cedc1e43fd	["<ORGANIZER>/schemas/experiment-manifest-v1.schema.json"]
<ORGANIZER>/schemas/review-lanes-v1.schema.json	5500	b410a3905a2e5508c666059eedc3cd767a9a205cacaf020a13a8d510b9e7acc5	["<ORGANIZER>/schemas/review-lanes-v1.schema.json"]
<ORGANIZER>/schemas/review-rescore-v2.schema.json	649	ff01aa65b3fd40cdb710a50c023479408fba3d2bd9a6a344f3e4aa382ec2a7a0	["<ORGANIZER>/schemas/review-rescore-v2.schema.json"]
<ORGANIZER>/scripts/archive_review.py	2682	1fe470d134cdea796886e6af34dfb280162230fd36be442c6690da2eef9e60b8	["<ORGANIZER>/scripts/archive_review.py"]
<ORGANIZER>/scripts/calibrate_paired_judges.py	12736	db943ffbfb90a35265364b482dab07bfe779a1e21e8b1f629baf1a2000facd88	["<ORGANIZER>/scripts/calibrate_paired_judges.py"]
<ORGANIZER>/scripts/check-frontier-surface.py	2468	09b3a800c6a2582e93572507280a29c6776be91e53b68009bf17ea5f979b429b	["<ORGANIZER>/scripts/check-frontier-surface.py"]
<ORGANIZER>/scripts/hashsmash_pipeline.py	19208	d8c040649a415e8db2baa5e5fb5f24b9f1070f5cf69ca7884e212cec0c0f8221	["<ORGANIZER>/scripts/hashsmash_pipeline.py"]
<ORGANIZER>/scripts/import_yukon_dev.py	8963	781ad50f6ce9b8dfea8e7046c2539c5216182798fdc24266cffc8e00944f2c1e	["<ORGANIZER>/scripts/import_yukon_dev.py"]
<ORGANIZER>/scripts/local_state.py	1848	e1da3d830ee6acf8e79713ee6338a6a171d028f88cc70fe2b5c0c7baa60524ef	["<ORGANIZER>/scripts/local_state.py"]
<ORGANIZER>/scripts/local_tracks.py	4529	5c4661c51e69ab9c0319c5759690974a1cbf4d0bbaa0ce309943b397754f642e	["<ORGANIZER>/scripts/local_tracks.py"]
<ORGANIZER>/scripts/prepare_experiment_image.py	1326	6c0e5e386a6240c9e8f565671b09099a18e334dfc90478d4f96e61f9883188f7	["<ORGANIZER>/scripts/prepare_experiment_image.py"]
<ORGANIZER>/scripts/reference_operation_costs.py	2356	01a445640ffc4b7b39a127dcdd44f14d7661190b010308e40837d160d59c2e1e	["<ORGANIZER>/scripts/reference_operation_costs.py"]
<ORGANIZER>/scripts/rescore_artifacts.py	5379	15dd2bf5ca452035611bc2b160fc4bd43c67b49dea4c6ae35aec311e99637b68	["<ORGANIZER>/scripts/rescore_artifacts.py"]
<ORGANIZER>/scripts/run-bedrock-smoke.sh	434	75ba79ff6fe87b2a0a4c743ed298a8d212bdda109e2b45f0afe5a6086f425132	["<ORGANIZER>/scripts/run-bedrock-smoke.sh"]
<ORGANIZER>/scripts/run-local-track.sh	891	81fa19dd4139b42192cecdc9f541912081495c27232664fab4fe4fc7088ac09f	["<ORGANIZER>/scripts/run-local-track.sh"]
<ORGANIZER>/scripts/run-openrouter-smoke.sh	421	5c5683efcc362bb8a3fca1252ebdacb5b7b39b44e5efc41f11802152950b8c9b	["<ORGANIZER>/scripts/run-openrouter-smoke.sh"]
<ORGANIZER>/scripts/run-paired-calibration.sh	456	7bfb8386169ab801e30b4ffb4b19a4f7b7a53afce820759a7f08adace72a9a39	["<ORGANIZER>/scripts/run-paired-calibration.sh"]
<ORGANIZER>/scripts/run-participant-heuristic.sh	1817	b9f654193dd4c2fd5c83d17a818e535ccee65da2e07e0c570727415627aeab25	["<ORGANIZER>/scripts/run-participant-heuristic.sh"]
<ORGANIZER>/scripts/smoke-bedrock.py	2940	27aef82ded9def70606f41a260ad29e80e5c8564a693b40a59dc75bec6d9954a	["<ORGANIZER>/scripts/smoke-bedrock.py"]
<ORGANIZER>/scripts/smoke-openrouter.py	2785	2373537be4bc5f23ba8a05d9334750c1f40e897c6e837bfffb110bf1f111edf0	["<ORGANIZER>/scripts/smoke-openrouter.py"]
<ORGANIZER>/scripts/stage_yukon_score.py	3025	07f22da82f25dee9dbecab7b17b94f4ca413e207972b4f76430435e25493a016	["<ORGANIZER>/scripts/stage_yukon_score.py"]
<ORGANIZER>/scripts/test_participant_heuristic.py	17966	bc2ad06c806776a84926ad0bc3381e4262032206001d99f80decf1e486c6fab8	["<ORGANIZER>/scripts/test_participant_heuristic.py"]
<ORGANIZER>/scripts/validate_frontier_config.py	4384	9f86d85680693fb293aab2e29ee7e23705ad2103fb12dc9f58b80e4a9edc6939	["<ORGANIZER>/scripts/validate_frontier_config.py"]
<ORGANIZER>/target-profiles/blake3-r1-prefix-v1.json	2195	397b4f2a9fea980b1307d66b1136d5addc32f76e9857430358420216482601b6	["<ORGANIZER>/target-profiles/blake3-r1-prefix-v1.json"]
<ORGANIZER>/target-profiles/blake3-r2-prefix-v1.json	2195	7f1cc0d4e162d066685fbec94eab23d0b5715b1f4f51851f9423bd52fc36a735	["<ORGANIZER>/target-profiles/blake3-r2-prefix-v1.json"]
<ORGANIZER>/target-profiles/keccak800-r5-prefix-v1.json	1721	1f23d4b79a1310fc908ac0b35d651fe251dc13b932ec8bc4db037eec42b1f0ba	["<ORGANIZER>/target-profiles/keccak800-r5-prefix-v1.json"]
<ORGANIZER>/target-profiles/keccak800-r6-prefix-v1.json	1721	cd653306efa03de016b785f965256f7a34564c998d8c7eb34bc60b762478a9a3	["<ORGANIZER>/target-profiles/keccak800-r6-prefix-v1.json"]
<ORGANIZER>/target-profiles/md5-s63-prefix-v1.json	1784	e2e96196ff0a209271ca5f8d7716d36d237a5efe3ee87919cde53b0a935b18c7	["<ORGANIZER>/target-profiles/md5-s63-prefix-v1.json"]
<ORGANIZER>/target-profiles/md5-s64-prefix-v1.json	1807	ca50e9227017e8d4d82fcf87b4724f6b7eb4b7fe28458e68aaba48d226eef8af	["<ORGANIZER>/target-profiles/md5-s64-prefix-v1.json"]
<ORGANIZER>/target-profiles/md5-s8-prefix-v1.json	1803	efb37499e55d4a4fba532c0da6c08f92b05cff24422e92790a504a7f114f8939	["<ORGANIZER>/target-profiles/md5-s8-prefix-v1.json"]
<ORGANIZER>/target-profiles/sha1-r79-prefix-v1.json	1784	f9597f46528f3289c0c154b5aae1553b0a1c95d1448c96bf8020e8cd96c86492	["<ORGANIZER>/target-profiles/sha1-r79-prefix-v1.json"]
<ORGANIZER>/target-profiles/sha1-r80-prefix-v1.json	1807	661832134db46d3d2806cabe5413adc5a3e8f591a6b7cacf7264cd0e4e074ead	["<ORGANIZER>/target-profiles/sha1-r80-prefix-v1.json"]
<ORGANIZER>/target-profiles/sha256-r31-prefix-v1.json	1792	02d8c776c0f2c241bea610ac1f6132c6a7028bea793c89be40667a3fa7caa820	["<ORGANIZER>/target-profiles/sha256-r31-prefix-v1.json"]
<ORGANIZER>/target-profiles/sha256-r32-prefix-v1.json	1792	93d2e5d9ca93540633798d58cbab2d6d8447916db2b127e9abe71f45d14f6835	["<ORGANIZER>/target-profiles/sha256-r32-prefix-v1.json"]
<ORGANIZER>/target-profiles/sha3-256-r5-prefix-v1.json	1620	0209f0a18ecebcdb07b5ad0b084a1f5d1b235dc51e429d8410f995744ea99e58	["<ORGANIZER>/target-profiles/sha3-256-r5-prefix-v1.json"]
<ORGANIZER>/target-profiles/sha3-256-r6-prefix-v1.json	1620	c4f0e09d81337ee75936b7d08d55af4687cbf0baf83ae5a1641f7e5371f560e4	["<ORGANIZER>/target-profiles/sha3-256-r6-prefix-v1.json"]
<ORGANIZER>/tests/__init__.py	42	3acd3785b7bf41aabfcfe914c0180716cb634e74b9530d28d6d28346afd2e73f	["<ORGANIZER>/tests/__init__.py"]
<ORGANIZER>/tests/fixtures/blake3-vectors.json	8458	f4dc3ee47915a6cf983197e53919938448a1b846848f2ac7e405b4c011594390	["<ORGANIZER>/tests/fixtures/blake3-vectors.json"]
<ORGANIZER>/tests/fixtures/blake3-vectors.md	1301	b72477bfaad8085bb2d1ea3278b8e7a2e29d4a790e5f625a93716020b012975d	["<ORGANIZER>/tests/fixtures/blake3-vectors.md"]
<ORGANIZER>/tests/fixtures/paired-calibration/README.md	1240	9266b75a613c16b844322901f30022df887582a74eb238df084cc559b1ef9225	["<ORGANIZER>/tests/fixtures/paired-calibration/README.md"]
<ORGANIZER>/tests/fixtures/paired-calibration/false-proof.md	1035	bd50da7afe4b07d4e91c8f0c278847a931e1cc1ffe9b30abec734e79a706d778	["<ORGANIZER>/tests/fixtures/paired-calibration/false-proof.md"]
<ORGANIZER>/tests/fixtures/paired-calibration/heuristic.md	2794	6131ccfd6b7bfb317b584e3f496378fbe36f8e54130cdac1f99fa5649433aae4	["<ORGANIZER>/tests/fixtures/paired-calibration/heuristic.md"]
<ORGANIZER>/tests/fixtures/paired-calibration/positive.md	1404	8b6bb1063762fd90334f30619be4d5249c510f033808761925668606ac25ffbc	["<ORGANIZER>/tests/fixtures/paired-calibration/positive.md"]
<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/certificates/manifest.json	48	a3c78779269ab224b0a36cc0cc075aaebdfb496a3a695bce1e743cf7bd45c4c8	["<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/certificates/manifest.json"]
<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/claim.json	1692	62f08a847e7afb52fed166169d58612cc6ec49dac7e941f84c736f59d451b11e	["<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/claim.json"]
<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/experiments/birthday.py	1782	a9e6fed56cec966f4709d3234efb130bfa735394c6a597a60094120aa2499f1d	["<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/experiments/birthday.py"]
<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/experiments/manifest.json	675	1b3780bfbceb8bede9a89818b4b730366758a5ea0c856b0871330fbb7f798221	["<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/experiments/manifest.json"]
<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/proof.md	9080	7425a3ef0c3d8f1fcffc70bdee5317c816376f3f25ec21f145fc047f5258ea11	["<ORGANIZER>/tests/fixtures/participant-heuristic/candidate/proof.md"]
<ORGANIZER>/tests/helpers.py	712	3b07a743dc9bad340dfb84e88425c261e9acc846e13a12a9d046c273ebe2a30a	["<ORGANIZER>/tests/helpers.py"]
<ORGANIZER>/tests/test_blake3.py	1993	d98732a23582b4952eae22e9faf69fe864670d299da26f9ed4ddd70efb60f972	["<ORGANIZER>/tests/test_blake3.py"]
<ORGANIZER>/tests/test_experiments.py	14527	5fdfdff65d53bd5ad48fca6bef309185b35f2ea187fea901e1568955eb2b8f13	["<ORGANIZER>/tests/test_experiments.py"]
<ORGANIZER>/tests/test_frontier_pipeline.py	31078	8efc78915e602313dc7ad3064f872fbe88e8f336555b873c198e5e65a6879c38	["<ORGANIZER>/tests/test_frontier_pipeline.py"]
<ORGANIZER>/tests/test_frontier_surface.py	3251	352bdb2ada7f4e1f1dc8514e2c552c1e3ba26ff9bfdd1d03a2d613ae03d59511	["<ORGANIZER>/tests/test_frontier_surface.py"]
<ORGANIZER>/tests/test_hash_functions.py	4247	5982bb7994e77c0a30c676cbe576086494b86da1158267144ff7c83a03b7968a	["<ORGANIZER>/tests/test_hash_functions.py"]
<ORGANIZER>/tests/test_judge_output_reliability.py	5698	10d8575b6c6901fa356bb816c5c329e2f66e28a077f68e96afcf7236164ff25f	["<ORGANIZER>/tests/test_judge_output_reliability.py"]
<ORGANIZER>/tests/test_keccak.py	5884	91aa24617e192c6a757ab535fcfa5975987573f8252843d6901199e205d5c2c2	["<ORGANIZER>/tests/test_keccak.py"]
<ORGANIZER>/tests/test_local_tracks.py	6049	b2e77e5c9f0b02bb6db54dff3b51f295ae06b67a38ddbaa4676b4f0e9395fa33	["<ORGANIZER>/tests/test_local_tracks.py"]
<ORGANIZER>/tests/test_paired_calibration.py	9781	8655559304228a299f1a62a19ccaf3fcc05a83382bf671970f6797469d06ca4c	["<ORGANIZER>/tests/test_paired_calibration.py"]
<ORGANIZER>/tests/test_paired_judges.py	19355	a2cfd91c60af58584b439d3bdbe8c243461d6855088a073ff40b45253539a0f1	["<ORGANIZER>/tests/test_paired_judges.py"]
<ORGANIZER>/tests/test_participant_heuristic.py	15882	e9267fdaf536dd0eec2b8ef103f8b8501ed02fa2c2d937137e323a90f9fac62d	["<ORGANIZER>/tests/test_participant_heuristic.py"]
<ORGANIZER>/tests/test_participant_heuristic_boundary.py	4002	15aade8789673e19f6a9825d9dbbde5bd68f6942fb28febda39e94a490a0d697	["<ORGANIZER>/tests/test_participant_heuristic_boundary.py"]
<ORGANIZER>/tests/test_pipeline.py	4534	f06a7be560c898cb40471ee97783379645491163b2198fe0e0d33c6e105756a5	["<ORGANIZER>/tests/test_pipeline.py"]
<ORGANIZER>/tests/test_rescoring.py	26504	4286a66a7cc82d1a85d0f198bbdd80df157871f7a22523e4309b11534a75c2a1	["<ORGANIZER>/tests/test_rescoring.py"]
<ORGANIZER>/tests/test_yukon_contract.py	3227	6e26dbc49489a6ff7ec927b0c6ae69afee6b424b9bc12c023214c32f56f985b7	["<ORGANIZER>/tests/test_yukon_contract.py"]
<ORGANIZER>/tests/test_yukon_setup.py	10925	32f16e0f479cb66ad800fc677909b4169b36aa97780846d6f75543dbe09bc801	["<ORGANIZER>/tests/test_yukon_setup.py"]
<ORGANIZER>/tracks/blake3-r1-exploratory/TASK.md	1533	13538dae9ae3a0da25cbf813894cc687c6659cee4489ab649b979e6c27d252f5	["<ORGANIZER>/tracks/blake3-r1-exploratory/TASK.md"]
<ORGANIZER>/tracks/blake3-r1-rigorous/TASK.md	1536	c53b3394263081c2e2cb737d9b0ef43f052e949c6800fdc2f87c266dfc4c2cdf	["<ORGANIZER>/tracks/blake3-r1-rigorous/TASK.md"]
<ORGANIZER>/tracks/blake3-r2-exploratory/TASK.md	1533	c8ce612d1e981f1bb90466d876708a68e89131bb1a622edd140cd947909201ff	["<ORGANIZER>/tracks/blake3-r2-exploratory/TASK.md"]
<ORGANIZER>/tracks/blake3-r2-rigorous/TASK.md	1536	0d4cd1c5b37cd2f7b67a71a55ad27e40d3936a4a4724cfea206e89ac10c8ad81	["<ORGANIZER>/tracks/blake3-r2-rigorous/TASK.md"]
<ORGANIZER>/tracks/frontier-v1.json	3823	588ddcb4b09d065eb298134a50662a918f7b59cb8f949e56d61a4055303d4600	["<ORGANIZER>/tracks/frontier-v1.json"]
<ORGANIZER>/tracks/keccak800-r5-exploratory/TASK.md	1551	fa78c461506af3f7e39ad1f1ddfae231f525914e7195e21c4130a64054b79088	["<ORGANIZER>/tracks/keccak800-r5-exploratory/TASK.md"]
<ORGANIZER>/tracks/keccak800-r5-rigorous/TASK.md	1554	986fa4dca4d20b7e116d8057bd9a13c6c15f7d583952bc319448130abaa302a7	["<ORGANIZER>/tracks/keccak800-r5-rigorous/TASK.md"]
<ORGANIZER>/tracks/keccak800-r6-exploratory/TASK.md	1551	79b719d0358d289f6ebdb9ea6f87f329748433d9109982fa4d198f20ab0048e8	["<ORGANIZER>/tracks/keccak800-r6-exploratory/TASK.md"]
<ORGANIZER>/tracks/keccak800-r6-rigorous/TASK.md	1554	c7f09fdc31bf60ba241898fa09f1861485f8468d3ed227de40ac064b5401ff62	["<ORGANIZER>/tracks/keccak800-r6-rigorous/TASK.md"]
<ORGANIZER>/tracks/md5-s63-exploratory/TASK.md	1374	40f7549664e5946e8443c8c972e49109f9d41abd6fc82c3faa7031a57c2dbbd8	["<ORGANIZER>/tracks/md5-s63-exploratory/TASK.md"]
<ORGANIZER>/tracks/md5-s63-rigorous/TASK.md	1356	45eed223dd5feef452deffd4898f186e405c5ab7155a434533fa28e83b5ffed3	["<ORGANIZER>/tracks/md5-s63-rigorous/TASK.md"]
<ORGANIZER>/tracks/md5-s64-exploratory/TASK.md	1374	2a4c7043fdd4df9673c37ac341da6c948a98cd53cbe6e8addea116c0dd712c78	["<ORGANIZER>/tracks/md5-s64-exploratory/TASK.md"]
<ORGANIZER>/tracks/md5-s64-rigorous/TASK.md	1356	cbeb53648121eb10d67f935f2c7b593f04b90ccb9f7116e430853fd73138b9d4	["<ORGANIZER>/tracks/md5-s64-rigorous/TASK.md"]
<ORGANIZER>/tracks/sha1-r79-exploratory/TASK.md	1380	a513a8b56708dff81aa03bccf09fbe2f168f7779e25398c60b113d987ca908aa	["<ORGANIZER>/tracks/sha1-r79-exploratory/TASK.md"]
<ORGANIZER>/tracks/sha1-r79-rigorous/TASK.md	1362	37e9ad4f82a04c690a713c67dd1d3cf5c4986f23b417b12e7d895286f20b62c5	["<ORGANIZER>/tracks/sha1-r79-rigorous/TASK.md"]
<ORGANIZER>/tracks/sha1-r80-exploratory/TASK.md	1380	fce51565bc73c4254a72806eabfd8b5294ba58dab54ab92e4e884fffe24e7efc	["<ORGANIZER>/tracks/sha1-r80-exploratory/TASK.md"]
<ORGANIZER>/tracks/sha1-r80-rigorous/TASK.md	1362	b9bbff4d6d74e6aa796eb91957fb766982f67c12079763f10f397aa6660846ad	["<ORGANIZER>/tracks/sha1-r80-rigorous/TASK.md"]
<ORGANIZER>/tracks/sha256-r31-exploratory/TASK.md	1393	ae78203d12fefc6d4533ff3c12af5aecc6c93a261591e6c4d9fa256d7db6d192	["<ORGANIZER>/tracks/sha256-r31-exploratory/TASK.md"]
<ORGANIZER>/tracks/sha256-r31-rigorous/TASK.md	1375	63b35b7e93047f1a11265c07b7aec2406a80ee8d3eb455fa42bf837ac2355267	["<ORGANIZER>/tracks/sha256-r31-rigorous/TASK.md"]
<ORGANIZER>/tracks/sha256-r32-exploratory/TASK.md	1393	3840f80329856ce52a0d5a60e19271403346a4f6128b3c614fa4ee0920f92807	["<ORGANIZER>/tracks/sha256-r32-exploratory/TASK.md"]
<ORGANIZER>/tracks/sha256-r32-rigorous/TASK.md	1375	4ed24ed93c9d75852e674e9a4fb608801503f943f6d28c6e6e7e58903a176a07	["<ORGANIZER>/tracks/sha256-r32-rigorous/TASK.md"]
<ORGANIZER>/tracks/sha3-256-r5-exploratory/TASK.md	1399	edc4115a9b8a74ebdc010cc96e8c33a85893f6371b1f50709613326e05f3ed2f	["<ORGANIZER>/tracks/sha3-256-r5-exploratory/TASK.md"]
<ORGANIZER>/tracks/sha3-256-r5-rigorous/TASK.md	1381	14987d82b3bb421cdd6b14440b9ec26265d614bf4dcb42371ecd9e8844a6a60b	["<ORGANIZER>/tracks/sha3-256-r5-rigorous/TASK.md"]
<ORGANIZER>/tracks/sha3-256-r6-exploratory/TASK.md	1399	930afd34301d3e82ea280ec32c5d8efbba12a63150133b99837f4cf1ae65e13d	["<ORGANIZER>/tracks/sha3-256-r6-exploratory/TASK.md"]
<ORGANIZER>/tracks/sha3-256-r6-rigorous/TASK.md	1381	0f098894222d6f974ddba3449f8b4a48ead22a9cc7749e210b9425965b827490	["<ORGANIZER>/tracks/sha3-256-r6-rigorous/TASK.md"]
<ORGANIZER>/validation/new-lanes-20260913.json	4399	a4d379376e0dbed35bb5e8a070d29328904dec03210d74c37c8f02f539aa2a47	["<ORGANIZER>/validation/new-lanes-20260913.json"]
<ORGANIZER>/validation/participant-heuristic-20260904.json	5292	05937a1f4f7d84d81660920a34920560c5982ce5d9f63bb6ead31bb3488c5115	["<ORGANIZER>/validation/participant-heuristic-20260904.json"]
<ORGANIZER>/verifier/README.md	3176	84d7e42885a662b4a575192c8e45d8fa088ed15307e960f3af22a18555b0a395	["<ORGANIZER>/verifier/README.md"]
<ORGANIZER>/verifier/__init__.py	342	421b7f2cfea7ebf877a6daae52c7967f057dcc905b7798c27b25784f3b02183d	["<ORGANIZER>/verifier/__init__.py"]
<ORGANIZER>/verifier/__main__.py	48	935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d	["<ORGANIZER>/verifier/__main__.py"]
<ORGANIZER>/verifier/__pycache__/__init__.cpython-313.pyc	513	6112a6899fefea3353b2eea93151ed3cb6a9302868858325bfcf9e36e98ca5c8	["<ORGANIZER>/verifier/__pycache__/__init__.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/__init__.cpython-314.pyc	510	eb695e2c7111f51612ed84a539cd3622a7e51ccae3f0519f2a5cdf202002a38c	["<ORGANIZER>/verifier/__pycache__/__init__.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/certificates.cpython-313.pyc	5143	f5b10f210da48adfeff850d7a82f6428420489f1e92d0050c28eabaef534698e	["<ORGANIZER>/verifier/__pycache__/certificates.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/certificates.cpython-314.pyc	5654	7208716e6dd57564a8bce58c472ee921ba5834ef3b8d02aa03d0b5dacaa31347	["<ORGANIZER>/verifier/__pycache__/certificates.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/constants.cpython-313.pyc	679	dcfa486809a12194da849ac2d69d736653ffbb7ba2245ba323840991a6d9fc3d	["<ORGANIZER>/verifier/__pycache__/constants.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/constants.cpython-314.pyc	671	e88b69f6c53359dd0fea8d70d78b3239ae638829eedf8dc8b7f1bd9be417f6ae	["<ORGANIZER>/verifier/__pycache__/constants.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/costs.cpython-314.pyc	1433	eb9be547c224cb479a3a0546b1901a24283b7fb1c31107ebba1ec5c5182eb6a3	["<ORGANIZER>/verifier/__pycache__/costs.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/errors.cpython-313.pyc	544	734af9482d66a8f3283d75d447b5e5c9f2f87f0ed949b9cb134676e0493a1e63	["<ORGANIZER>/verifier/__pycache__/errors.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/errors.cpython-314.pyc	543	902c60d1ecbf351fcf61680743d6f37359d063c868cb350e5c67c1bf1a74e9cc	["<ORGANIZER>/verifier/__pycache__/errors.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/frontier_tracks.cpython-313.pyc	15143	4f6092ed46a8438b9b91f23004155d19b512c03a14f66b9fc09fe02390e7cefd	["<ORGANIZER>/verifier/__pycache__/frontier_tracks.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/frontier_tracks.cpython-314.pyc	18740	625f383483f20452f3e928a01470d000547b6a7e2758e252c3688cf74463d14b	["<ORGANIZER>/verifier/__pycache__/frontier_tracks.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/hash_functions.cpython-313.pyc	7569	30243b0b6323f5f3cc8dcf1998c10bf7f81a3586d92e8f9c63038ff94d6c6dc6	["<ORGANIZER>/verifier/__pycache__/hash_functions.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/hash_functions.cpython-314.pyc	9217	d399a9100aa9b48c366b1a3cd22706d90f5f030a598c088fee19797e4201c0d2	["<ORGANIZER>/verifier/__pycache__/hash_functions.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/intake.cpython-313.pyc	14545	746ba739998a2464d9e51d94259b06d4a4d95a9a55d59ca90bdb93c405f4c04c	["<ORGANIZER>/verifier/__pycache__/intake.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/intake.cpython-314.pyc	15770	ddea5e8e00602731d3592b5fcdc51347cf2e2c88c81497a915d6ce10bcdb6530	["<ORGANIZER>/verifier/__pycache__/intake.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/io.cpython-313.pyc	5272	e8982579145dde301189f491ac8a0a2f0d18b6bfb04219691168af8ea598159f	["<ORGANIZER>/verifier/__pycache__/io.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/io.cpython-314.pyc	6277	65d186243bd6df764bcf5d7bdeabe3b22d1f300f5559fafccbe1a97df7ee1b96	["<ORGANIZER>/verifier/__pycache__/io.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/schema_validation.cpython-313.pyc	12350	1095081f9b11d7f6b534e7ca6c489ec06ada163e988f97fbbfc786136a865b73	["<ORGANIZER>/verifier/__pycache__/schema_validation.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/schema_validation.cpython-314.pyc	14299	11d233299bc639db0a1f75ea113f6f5fffb567ec3048ddfb9f963aa6ec896fcc	["<ORGANIZER>/verifier/__pycache__/schema_validation.cpython-314.pyc"]
<ORGANIZER>/verifier/__pycache__/score.cpython-313.pyc	7027	75ae96379952d5be05f3e3df453cfa614f3d13a8d6e2e87f44a44dfb25987be2	["<ORGANIZER>/verifier/__pycache__/score.cpython-313.pyc"]
<ORGANIZER>/verifier/__pycache__/score.cpython-314.pyc	7507	f4e24a187f18c1d6a14faf5332367f54aa1e4e3d747e47fe9b8b20ec41128ffe	["<ORGANIZER>/verifier/__pycache__/score.cpython-314.pyc"]
<ORGANIZER>/verifier/blake3.py	3457	bf67aca295b45b06621891d9219c71166e5855b1afd0464a87d1dbb1314f0237	["<ORGANIZER>/verifier/blake3.py"]
<ORGANIZER>/verifier/certificates.py	4745	b3277bf84ea3d18ef42857f8b5026e0bbc4d285473f7c2b465bda652767d75b8	["<ORGANIZER>/verifier/certificates.py"]
<ORGANIZER>/verifier/cli.py	2744	e27c4315e393ee4ab16267b8e51cf3e349cd04930a0aceb15dd60da78401bf3f	["<ORGANIZER>/verifier/cli.py"]
<ORGANIZER>/verifier/constants.py	597	345ac4325f54dedcf004eebf73e223d5199c654b0226906ebd2bc65fe06bdd64	["<ORGANIZER>/verifier/constants.py"]
<ORGANIZER>/verifier/costs.py	835	3efbf6d44d76801136df11871779a9acea9315842b943a58c66612689cf42e8b	["<ORGANIZER>/verifier/costs.py"]
<ORGANIZER>/verifier/errors.py	139	337157f909054c433f74347119a542adf50dee47486c3e4638723261b9c757fa	["<ORGANIZER>/verifier/errors.py"]
<ORGANIZER>/verifier/experiment_evidence.py	4402	aa2722e658bc650b55c480c79ccb1e9b7984ab71901868eaad9f078181129b1c	["<ORGANIZER>/verifier/experiment_evidence.py"]
<ORGANIZER>/verifier/frontier_tracks.py	10542	8f7aecc24e2480b29a9ac05d48282a150d2492b2750a37ac82bf5a8539f4f72e	["<ORGANIZER>/verifier/frontier_tracks.py"]
<ORGANIZER>/verifier/hash_functions.py	5749	514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5	["<ORGANIZER>/verifier/hash_functions.py"]
<ORGANIZER>/verifier/intake.py	11450	3ac3964b9cf291bbda7b708d029dddde5fa57faaab8358b046b29464fb4111a7	["<ORGANIZER>/verifier/intake.py"]
<ORGANIZER>/verifier/io.py	2524	bef5b9617c6bf30d167dae95c12f02099c967a7e48edb9e6894754dc1a530f3f	["<ORGANIZER>/verifier/io.py"]
<ORGANIZER>/verifier/keccak.py	4959	95ce77dff0476301c05057e01296f3e3507c4926423257540cfc3e5fd36ee0ae	["<ORGANIZER>/verifier/keccak.py"]
<ORGANIZER>/verifier/schema_validation.py	9713	96a6561e62bc1ecd62def6873edb7b9d84f3ce8622fa4b522b47b8965f7b4ab5	["<ORGANIZER>/verifier/schema_validation.py"]
<ORGANIZER>/verifier/score.py	6407	6409133e63a4967ff462cbdc687336242c19cfa2fd5353ab8a0fca681a6ec925	["<ORGANIZER>/verifier/score.py"]
<ORGANIZER>/verifier/tests/__init__.py	32	3fd7c47432fc4bbc263a6b45784d0185cd85592c169f863f210eb7132d701e0c	["<ORGANIZER>/verifier/tests/__init__.py"]
<ORGANIZER>/verifier/tests/common.py	1315	4871994aacb963b742d666b0f5af9aae6318588264fa94594fcd37f9e364e2b2	["<ORGANIZER>/verifier/tests/common.py"]
<ORGANIZER>/verifier/tests/test_certificates.py	4232	7a91a1d0437c33f2c6970368579fbe7bb0715545a959208a27f62b2542cadfff	["<ORGANIZER>/verifier/tests/test_certificates.py"]
<ORGANIZER>/verifier/tests/test_intake.py	12077	e23c96abcb96bcc40364fdb26de8504fd90b51949a291c021c5f4cc70793976f	["<ORGANIZER>/verifier/tests/test_intake.py"]
<ORGANIZER>/verifier/tests/test_score_cli.py	8592	3387728eb66952b5c5247cef540c68b9e3606938219fdb34e08e90041f60dfdb	["<ORGANIZER>/verifier/tests/test_score_cli.py"]
<PROVENANCE>/.git/COMMIT_EDITMSG	49	ac804c6ecb84b086bba95eb98f9cb742e0ca407e54e524e85ce0d2b8b490cf62	["<PROVENANCE>/.git/COMMIT_EDITMSG"]
<PROVENANCE>/.git/HEAD	21	28d25bf82af4c0e2b72f50959b2beb859e3e60b9630a5e8c603dad4ddb2b6e80	["<PROVENANCE>/.git/HEAD"]
<PROVENANCE>/.git/config	137	cae33efdb02cf774435c1ff9cb16bcc1014606908530c6e1dc727615fe3e8cda	["<PROVENANCE>/.git/config"]
<PROVENANCE>/.git/description	73	85ab6c163d43a17ea9cf7788308bca1466f1b0a8d1cc92e26e9bf63da4062aee	["<PROVENANCE>/.git/description"]
<PROVENANCE>/.git/hooks/applypatch-msg.sample	478	0223497a0b8b033aa58a3a521b8629869386cf7ab0e2f101963d328aa62193f7	["<PROVENANCE>/.git/hooks/applypatch-msg.sample"]
<PROVENANCE>/.git/hooks/commit-msg.sample	896	1f74d5e9292979b573ebd59741d46cb93ff391acdd083d340b94370753d92437	["<PROVENANCE>/.git/hooks/commit-msg.sample"]
<PROVENANCE>/.git/hooks/fsmonitor-watchman.sample	4726	e0549964e93897b519bd8e333c037e51fff0f88ba13e086a331592bf801fa1d0	["<PROVENANCE>/.git/hooks/fsmonitor-watchman.sample"]
<PROVENANCE>/.git/hooks/post-update.sample	189	81765af2daef323061dcbc5e61fc16481cb74b3bac9ad8a174b186523586f6c5	["<PROVENANCE>/.git/hooks/post-update.sample"]
<PROVENANCE>/.git/hooks/pre-applypatch.sample	424	e15c5b469ea3e0a695bea6f2c82bcf8e62821074939ddd85b77e0007ff165475	["<PROVENANCE>/.git/hooks/pre-applypatch.sample"]
<PROVENANCE>/.git/hooks/pre-commit.sample	1649	57185b7b9f05239d7ab52db045f5b89eb31348d7b2177eab214f5eb872e1971b	["<PROVENANCE>/.git/hooks/pre-commit.sample"]
<PROVENANCE>/.git/hooks/pre-merge-commit.sample	416	d3825a70337940ebbd0a5c072984e13245920cdf8898bd225c8d27a6dfc9cb53	["<PROVENANCE>/.git/hooks/pre-merge-commit.sample"]
<PROVENANCE>/.git/hooks/pre-push.sample	1374	ecce9c7e04d3f5dd9d8ada81753dd1d549a9634b26770042b58dda00217d086a	["<PROVENANCE>/.git/hooks/pre-push.sample"]
<PROVENANCE>/.git/hooks/pre-rebase.sample	4898	4febce867790052338076f4e66cc47efb14879d18097d1d61c8261859eaaa7b3	["<PROVENANCE>/.git/hooks/pre-rebase.sample"]
<PROVENANCE>/.git/hooks/pre-receive.sample	544	a4c3d2b9c7bb3fd8d1441c31bd4ee71a595d66b44fcf49ddb310252320169989	["<PROVENANCE>/.git/hooks/pre-receive.sample"]
<PROVENANCE>/.git/hooks/prepare-commit-msg.sample	1492	e9ddcaa4189fddd25ed97fc8c789eca7b6ca16390b2392ae3276f0c8e1aa4619	["<PROVENANCE>/.git/hooks/prepare-commit-msg.sample"]
<PROVENANCE>/.git/hooks/push-to-checkout.sample	2783	a53d0741798b287c6dd7afa64aee473f305e65d3f49463bb9d7408ec3b12bf5f	["<PROVENANCE>/.git/hooks/push-to-checkout.sample"]
<PROVENANCE>/.git/hooks/sendemail-validate.sample	2308	44ebfc923dc5466bc009602f0ecf067b9c65459abfe8868ddc49b78e6ced7a92	["<PROVENANCE>/.git/hooks/sendemail-validate.sample"]
<PROVENANCE>/.git/hooks/update.sample	3650	8d5f2fa83e103cf08b57eaa67521df9194f45cbdbcb37da52ad586097a14d106	["<PROVENANCE>/.git/hooks/update.sample"]
<PROVENANCE>/.git/index	3387	e052356591ac082273fdb46d459feaeb5204dba4ab935c5d19c27028de824f5a	["<PROVENANCE>/.git/index"]
<PROVENANCE>/.git/info/exclude	240	6671fe83b7a07c8932ee89164d1f2793b2318058eb8b98dc5c06ee0a5a3b0ec1	["<PROVENANCE>/.git/info/exclude"]
<PROVENANCE>/.git/logs/HEAD	220	f8fcc053a08149338d3d296c6b37b39b6f021daedfe75df05be23a85a1a372bf	["<PROVENANCE>/.git/logs/HEAD"]
<PROVENANCE>/.git/logs/refs/heads/main	220	f8fcc053a08149338d3d296c6b37b39b6f021daedfe75df05be23a85a1a372bf	["<PROVENANCE>/.git/logs/refs/heads/main"]
<PROVENANCE>/.git/objects/01/1214448b2533d66d1d32e6d8764d7270339a29	752	418acd741209bcfd7ccc735adf194460618d6945186a60dd8c3db94f44d52ac1	["<PROVENANCE>/.git/objects/01/1214448b2533d66d1d32e6d8764d7270339a29"]
<PROVENANCE>/.git/objects/0f/b7e00d0b8f93e18ca5cb5124e24f5d695e9d49	2922	42b819e732ea6cb84ceda862f482b6d9cbca6ad21aabc350d6ce53284f820a63	["<PROVENANCE>/.git/objects/0f/b7e00d0b8f93e18ca5cb5124e24f5d695e9d49"]
<PROVENANCE>/.git/objects/10/8bff671f05c7f3d9662c3e331fffac49aa00c9	54	53bea9e3fc0a154eb96816f1b77643c90ddaead6961c893484c376f14be3b9bf	["<PROVENANCE>/.git/objects/10/8bff671f05c7f3d9662c3e331fffac49aa00c9"]
<PROVENANCE>/.git/objects/12/0f8a5711e4e1409fa31bcf0cb7d994243dd2c6	923	100079fa9bdc4f7be78cf1975dff6134c15c0da9b326577a74a68d142106f3b1	["<PROVENANCE>/.git/objects/12/0f8a5711e4e1409fa31bcf0cb7d994243dd2c6"]
<PROVENANCE>/.git/objects/17/13e2e108adcdd9173d3fa137ed41667a358746	324	22c38d4ca5e13fc0ba2b37685c9a488abf0aa1823ace64ecf449b1ad52c24ee1	["<PROVENANCE>/.git/objects/17/13e2e108adcdd9173d3fa137ed41667a358746"]
<PROVENANCE>/.git/objects/1f/767d1880ed5b7341bf233adefceddcf27be5f7	2054	5d2c584b19357d184becd67ae2650ddea4bd7894ab442f7c2138eec7d3a736ef	["<PROVENANCE>/.git/objects/1f/767d1880ed5b7341bf233adefceddcf27be5f7"]
<PROVENANCE>/.git/objects/22/901bfe2f22730be99c2e98fefdab8f0408232b	1222	d69a044d700b6bed2ac08a01fc1581181b3a15882100e563c84692284d1628d5	["<PROVENANCE>/.git/objects/22/901bfe2f22730be99c2e98fefdab8f0408232b"]
<PROVENANCE>/.git/objects/23/1054486d9273b2bc3b84ffe1b2254e35dc454a	428	13f915ac6df4a858e5a7ee12e552d91be5b7f193391d00de381bff9f2d1da477	["<PROVENANCE>/.git/objects/23/1054486d9273b2bc3b84ffe1b2254e35dc454a"]
<PROVENANCE>/.git/objects/25/4b4b1a6596c1dd6721ee6cfcd2ca71ef7e1075	309	7fc0cbd2da64b615431f79c04aef0d5de1e2d4d7786acb788a52d96ca808ef91	["<PROVENANCE>/.git/objects/25/4b4b1a6596c1dd6721ee6cfcd2ca71ef7e1075"]
<PROVENANCE>/.git/objects/27/3f2cde0bdc3ef85fc86972cd2a34f4427b56b3	3116	1d6bbfe8ec82563f5cd326a154e02d65b09ae4ec823f004b4681f20c770ecedc	["<PROVENANCE>/.git/objects/27/3f2cde0bdc3ef85fc86972cd2a34f4427b56b3"]
<PROVENANCE>/.git/objects/2a/77831e7d46378c7c9081f9a1be05ff3ff0b20f	4669	0e2b7612fc3c7577bbb14297c071e1a6cf43e1faef93282531169c2256774ff7	["<PROVENANCE>/.git/objects/2a/77831e7d46378c7c9081f9a1be05ff3ff0b20f"]
<PROVENANCE>/.git/objects/2f/9b0f42e92eb18641a9d8fb2e5b3168b15d0661	1640	443fb478953f87f08a9531f6a7d3bbc84e9dbb4c668c98f91f5c83081637aba4	["<PROVENANCE>/.git/objects/2f/9b0f42e92eb18641a9d8fb2e5b3168b15d0661"]
<PROVENANCE>/.git/objects/30/640bba312a9ceb1c900b98d0eea6b9359c3cb1	743	74ec7ca0ea8cf63a3e3cbfe757158ad3fab4cab8a737c1b89c6c21f5ca2974c0	["<PROVENANCE>/.git/objects/30/640bba312a9ceb1c900b98d0eea6b9359c3cb1"]
<PROVENANCE>/.git/objects/36/c58ff34405fbc668871321b53fac19683971cb	1060	1da81fed6a4b4062026b6d2dfcb9e95d69f7a9b37006c6fd2f57aa9503fa2917	["<PROVENANCE>/.git/objects/36/c58ff34405fbc668871321b53fac19683971cb"]
<PROVENANCE>/.git/objects/39/0f5ef95941ac2a3c095a6de5e7840b2d515702	886	4d7a1cb89a018808b9c81a737068ddad8c9f0ed2191efe1be5b36d8b5c66f975	["<PROVENANCE>/.git/objects/39/0f5ef95941ac2a3c095a6de5e7840b2d515702"]
<PROVENANCE>/.git/objects/3c/87a04f9b10ddd8d960c1d41811ded0c95915ff	2088	ed681bdd826bf46937feda29e0a7cb212a24ac4fb50950e885d644da81cecbc0	["<PROVENANCE>/.git/objects/3c/87a04f9b10ddd8d960c1d41811ded0c95915ff"]
<PROVENANCE>/.git/objects/46/aa95b6f0837ef962408b809abc275edb395643	515	51a08065dd0d0185d66e6232af1ea1918ac989e62f3ae5a8a7ba9d536ac190f6	["<PROVENANCE>/.git/objects/46/aa95b6f0837ef962408b809abc275edb395643"]
<PROVENANCE>/.git/objects/4d/53ac7ece4c38834313871b160f9c34d208844f	770	eb18d7d48e134b61e7ef190539c50d6db21eff7cec8e33e5d97a2b995c42101c	["<PROVENANCE>/.git/objects/4d/53ac7ece4c38834313871b160f9c34d208844f"]
<PROVENANCE>/.git/objects/55/fd958594c6aa2aefa2332d187a06aeac368ac6	1133	43403bf2614c66b93fd1ace491fd7f0548fb8134aff6b7012afeafecc9d0012d	["<PROVENANCE>/.git/objects/55/fd958594c6aa2aefa2332d187a06aeac368ac6"]
<PROVENANCE>/.git/objects/57/297eefe0530499631ed459b1bd3a6bc6ca6176	5506	2aaa3e9efe2493d5c27aa5dea996ee5cca3daa2f2a351cec1f387a6c25b1857f	["<PROVENANCE>/.git/objects/57/297eefe0530499631ed459b1bd3a6bc6ca6176"]
<PROVENANCE>/.git/objects/58/d5117176f1cc9fa5eba1b66e9e82bab6663ce9	1617	ab5041d29d6e9125481eabed1e28e0069e8ea44abe0400db5657e95003507491	["<PROVENANCE>/.git/objects/58/d5117176f1cc9fa5eba1b66e9e82bab6663ce9"]
<PROVENANCE>/.git/objects/5e/8a187df8408e7c45c52ae23436e797a97e3c7b	7573	ad5eccb6d26d5099a328c1f3425e43f1255609f47b15d33b194fb7464da3d8d7	["<PROVENANCE>/.git/objects/5e/8a187df8408e7c45c52ae23436e797a97e3c7b"]
<PROVENANCE>/.git/objects/63/184965ac4bbd0db496f8c06440aac56a928d36	717	fa59f0e0eed121578c8132441a00a33319e0c7d229d234763b58c7cece59a799	["<PROVENANCE>/.git/objects/63/184965ac4bbd0db496f8c06440aac56a928d36"]
<PROVENANCE>/.git/objects/64/464afc55c840672c32391fb8f13350e04bc74e	2428	6eb8a9191456aaffd9115a8acf59bc28d80189371c9a33f55456f26962a98da9	["<PROVENANCE>/.git/objects/64/464afc55c840672c32391fb8f13350e04bc74e"]
<PROVENANCE>/.git/objects/68/b631167714cba6f1894d57db9e6a0d34b78e05	1680	c3943b628a343b3a878ad7cc98691a96bb393f3b0bd39289246175e2e01e4fba	["<PROVENANCE>/.git/objects/68/b631167714cba6f1894d57db9e6a0d34b78e05"]
<PROVENANCE>/.git/objects/75/a8beaf204913d85fa95a63927f05206d3d75d4	733	72f96b127f6d714db99eb6fa01870f32963ad5b3655b30da57110c454b89094f	["<PROVENANCE>/.git/objects/75/a8beaf204913d85fa95a63927f05206d3d75d4"]
<PROVENANCE>/.git/objects/79/71f2bfa9f89fdca5a8745fe347493a656727a2	109	9aa0969773875f5b8253ae7d80b6b11340efca3d7cdaac4d5344eaf219738c58	["<PROVENANCE>/.git/objects/79/71f2bfa9f89fdca5a8745fe347493a656727a2"]
<PROVENANCE>/.git/objects/83/508f35ff2192c073088c516433ff05fec1e06d	2853	6c516d859bee729ceadf90fc4c5f2e43a364b5c95003df0deb0c4c30a665b9f3	["<PROVENANCE>/.git/objects/83/508f35ff2192c073088c516433ff05fec1e06d"]
<PROVENANCE>/.git/objects/85/f33679d9add6c6b33cdbf0f5dc155a9ba9e424	35	5eab18dce8f7fd5d9c9ab1b7f1d3033da2b8ea8e0895adb2b7d136dce03f9acb	["<PROVENANCE>/.git/objects/85/f33679d9add6c6b33cdbf0f5dc155a9ba9e424"]
<PROVENANCE>/.git/objects/97/cd022364c761d421b40f54f4249e0b9561e99d	221	8987e973a329f1f542a80dfe436cf3a0bf095af1dbfd4ce513cd6f42550da7cf	["<PROVENANCE>/.git/objects/97/cd022364c761d421b40f54f4249e0b9561e99d"]
<PROVENANCE>/.git/objects/9c/82981fb83927e0836db7b1a32b926d7782399f	224	5b765a7e7a07386716f91135cb192768203bde0dcc7accfd61421ae12871ee1c	["<PROVENANCE>/.git/objects/9c/82981fb83927e0836db7b1a32b926d7782399f"]
<PROVENANCE>/.git/objects/9e/fabeb3f85c98d7ceae21d5623311886d097105	4858	f610e7201283dd8898433a7f3a79c7506ea0b6426d0dc48ee2f0cccaeb6ff02d	["<PROVENANCE>/.git/objects/9e/fabeb3f85c98d7ceae21d5623311886d097105"]
<PROVENANCE>/.git/objects/a1/47b0758d61e3bedb557215f4151d2f32cbba0a	7837	c303f6224cab73c22d0cd517058aec244a582d8eff5c25f12f14266d3d728768	["<PROVENANCE>/.git/objects/a1/47b0758d61e3bedb557215f4151d2f32cbba0a"]
<PROVENANCE>/.git/objects/a5/8e9328b523070af0fa00399a8f566296a14380	317	dd332d662e23422153195c1602cca9a107b6d416a57a37a9b8b3b051257db04a	["<PROVENANCE>/.git/objects/a5/8e9328b523070af0fa00399a8f566296a14380"]
<PROVENANCE>/.git/objects/ad/904b066bd057131f96407139d94aef89e24af2	411	1c21053e2dbeddf2806dad13e84d37e91713d717919ec9f0799e14a4f1da2a1c	["<PROVENANCE>/.git/objects/ad/904b066bd057131f96407139d94aef89e24af2"]
<PROVENANCE>/.git/objects/ae/bca27c56a6b49212f411f619073f62a3bf538f	58	89dfe7352090d9a8746c2a5292f5a904e0ef40e8dea5a366437279d5679f8d30	["<PROVENANCE>/.git/objects/ae/bca27c56a6b49212f411f619073f62a3bf538f"]
<PROVENANCE>/.git/objects/b7/49b4cd50d53e0a3ea2fd73c5390ecd0e746c5a	2010	17cffa782fa16445682f76a032689989a1559d6af627faf15b038eff82dd13b1	["<PROVENANCE>/.git/objects/b7/49b4cd50d53e0a3ea2fd73c5390ecd0e746c5a"]
<PROVENANCE>/.git/objects/b7/518c1c53794b029cc8396f48bc0e2e9752c0cb	2760	9bc97fc37c4b0da5ca414490e52ec23024f311faf020b2db31d12775cf269fd4	["<PROVENANCE>/.git/objects/b7/518c1c53794b029cc8396f48bc0e2e9752c0cb"]
<PROVENANCE>/.git/objects/ca/5121a4ba93774a1bb21414fdad0586f7b02cca	4845	aafb6216a568135477d65cac07b6da33926e332eb45cb1f2514083dba022c17e	["<PROVENANCE>/.git/objects/ca/5121a4ba93774a1bb21414fdad0586f7b02cca"]
<PROVENANCE>/.git/objects/d5/784dad172900c579497121dd45480e64d02f32	850	3a6f8f9b56ee229b2eb540273e669542d51bace4bb6286ec385cfb3f1f247283	["<PROVENANCE>/.git/objects/d5/784dad172900c579497121dd45480e64d02f32"]
<PROVENANCE>/.git/objects/d9/afb19649446dc89c92c484e82e17139a4d52e8	175	5052898313b45acabaa1d677709aae8b4dc5849c4f6b3ff3fe3037603e14a9f4	["<PROVENANCE>/.git/objects/d9/afb19649446dc89c92c484e82e17139a4d52e8"]
<PROVENANCE>/.git/objects/e1/7bd90367c25ba3a719349bfc4dd82f414c4aad	715	045d040feb8203ae2767f4224414ab253191c06d5eac56e3ca591b1a758a83d2	["<PROVENANCE>/.git/objects/e1/7bd90367c25ba3a719349bfc4dd82f414c4aad"]
<PROVENANCE>/.git/objects/e2/6ca18922920ff6da690758e4207800996c4286	8164	6cb2de6f2ddd8eb58ab9344d8e657d27539387dde380964e096b1d78d7a81a35	["<PROVENANCE>/.git/objects/e2/6ca18922920ff6da690758e4207800996c4286"]
<PROVENANCE>/.git/objects/e8/079c9aab97cbb142c8d72183cc828ba8fef3e4	27178	14b9c56e453806dca97d026985008d18baa02ba5f70abbaebe98971b0afa92a8	["<PROVENANCE>/.git/objects/e8/079c9aab97cbb142c8d72183cc828ba8fef3e4"]
<PROVENANCE>/.git/objects/f4/91c55a679fc82e404b8cd33afc6bc4d7e261f6	431	a6a60ba65cc6a5825ca446bfb1ccf42c3aef8fe29e8656e479a62122728bc803	["<PROVENANCE>/.git/objects/f4/91c55a679fc82e404b8cd33afc6bc4d7e261f6"]
<PROVENANCE>/.git/objects/f5/057ed4d2cc0050bf49d0954c5b2abe5ffecd1e	3372	82f579de96b23c748c75e53ed96cb3b4864dffc9d42b61c7b95521d4c2587f50	["<PROVENANCE>/.git/objects/f5/057ed4d2cc0050bf49d0954c5b2abe5ffecd1e"]
<PROVENANCE>/.git/refs/heads/main	41	844091f226ac9b3e263d6cc7b14e4f2a86df7afb4a2259cdb027c22ae5de00bb	["<PROVENANCE>/.git/refs/heads/main"]
<PROVENANCE>/.gitignore	19	ce66c7325e2d6ce7893bc4963517689ef22138e233d8198e676e4ca3426f023a	["<PROVENANCE>/.gitignore"]
<PROVENANCE>/README.md	4111	af51a0e7500949a7a623bb0d017c4aa50ed9659d985855dae91e45e08011ae29	["<PROVENANCE>/README.md"]
<PROVENANCE>/RESULTS.md	15529	bb90ef5e69548103f87460905f35765504f3e644bb88170175017dddc5efb39c	["<PROVENANCE>/RESULTS.md"]
<PROVENANCE>/audit_guard.py	14970	f5d83c1922f9a1979a1b533dac81a749d6a07844c9bd8d59cb9127da79b4a4e6	["<PROVENANCE>/audit_guard.py"]
<PROVENANCE>/build.sh	428	6a387e8e45ec8a6f76ecccd657d27c465be1c4dcb8454bcbb0c4c297d506976d	["<PROVENANCE>/build.sh"]
<PROVENANCE>/c/attack.h	7402	ace9a72063af7aeec2671f0a2bf32c0e2c21529204b4fdf574672e73bebc0b2c	["<PROVENANCE>/c/attack.h"]
<PROVENANCE>/c/compact.c	1536	18a9a42a610f968afcbb8ba61d8361eae5d02d03651a5242ee742cce72584bd4	["<PROVENANCE>/c/compact.c"]
<PROVENANCE>/c/equiv.c	738	1478986fe7eb68a6a31c540999110ab6e8cab2fc246d08f93c477b91d2f9dc45	["<PROVENANCE>/c/equiv.c"]
<PROVENANCE>/c/match.c	20159	4b36aade8a99ded5bfbf153236d8fc88c5db3337c95ff7b96870958f20bfb1fc	["<PROVENANCE>/c/match.c"]
<PROVENANCE>/c/par.h	1454	57da297cb072c7fd45b32bd8ca88b2d99e829001754e3a895cb0b74f03d22bb9	["<PROVENANCE>/c/par.h"]
<PROVENANCE>/c/ref.h	13480	830a9370e2979b69d4a90bcfbb3eb6ab0a7bd1c398ffe465de9353d727b78672	["<PROVENANCE>/c/ref.h"]
<PROVENANCE>/c/sha.h	1833	e6085ee7b4ddb912e1310e4b559adf7ebfc947fb8b50f945d7655893e3fda8dc	["<PROVENANCE>/c/sha.h"]
<PROVENANCE>/c/step3.c	12490	46e93017899e0854f1461e0f6585f4a8cba219b8459ebc938e48cce9bea4b9fc	["<PROVENANCE>/c/step3.c"]
<PROVENANCE>/c/tab2.c	14770	c3135f8abdd618b514be729c62838fb6d461aa9df50b0e8b910db8ebee325584	["<PROVENANCE>/c/tab2.c"]
<PROVENANCE>/c/tails.c	7279	926c636805f60f4315dad20f75c2d213d9d063d3bb4d887c6b2b077b76e97960	["<PROVENANCE>/c/tails.c"]
<PROVENANCE>/campaign/DATA-INPUTS.tsv	637	5e0c96495042ea50b69e0d9893e3d7544cccf8bff2ae3e0eb7f2a77d8cae7895	["<PROVENANCE>/campaign/DATA-INPUTS.tsv"]
<PROVENANCE>/campaign/SEALED-EXPORT.tsv	384	ddb2417104b3e8a157dacecba6dbd1502b2068555d11c89be1c6637bbfe13e0e	["<PROVENANCE>/campaign/SEALED-EXPORT.tsv"]
<PROVENANCE>/campaign/SOURCE-CEILING.md	4467	fea131fcce16e0565ccc43f61173aa018ec8d5a70078948162ce5501c1ab617f	["<PROVENANCE>/campaign/SOURCE-CEILING.md"]
<PROVENANCE>/campaign/V3.3-CONTRACT.tsv	6195	07e71d5949f51e1d333bdc35ba6f109261707e2cfe8c12393dc494553cb5f206	["<PROVENANCE>/campaign/V3.3-CONTRACT.tsv"]
<PROVENANCE>/campaign/launch-after-seal.sh	6805	aeb01ee75187517274eedc951806fb56aa60f6015e3fd79612666455a2cdfb39	["<PROVENANCE>/campaign/launch-after-seal.sh"]
<PROVENANCE>/campaign_contract.sh	1119	ff2896edc39b5cc0e78f9070c29e25e808277608b61bec395e13261a71071672	["<PROVENANCE>/campaign_contract.sh"]
<PROVENANCE>/g0_replay.py	2280	798b2585d1db3b5899d299eaadfabc3447c2ddaa19cc76dad94fb8040da47fa0	["<PROVENANCE>/g0_replay.py"]
<PROVENANCE>/g1_spotcheck.py	1709	38b6dc88abb1327f95849a7d756b1a286e9556bfa183baf02d68b89ddba6b3db	["<PROVENANCE>/g1_spotcheck.py"]
<PROVENANCE>/g2_equiv.py	1342	caed3a358b2be7d05116efb3a1f9b959e4c9a13131b1609a8f7df93b8faac4d6	["<PROVENANCE>/g2_equiv.py"]
<PROVENANCE>/g2_pycheck.py	4331	ceeb887798ced4d10be26af36265a3fec964028329e9ee0b32defb0801d10857	["<PROVENANCE>/g2_pycheck.py"]
<PROVENANCE>/gen_header.py	1345	335416e4df8a5abe628ad75c0b18c44f99e36a48da7b288074dd11decf528f00	["<PROVENANCE>/gen_header.py"]
<PROVENANCE>/implementation-notes.md	8988	c0a7c962623fb16430ba0bff6fc279b3983ca299d3611bef9a750a376af06518	["<PROVENANCE>/implementation-notes.md"]
<PROVENANCE>/provenance.json	19393	0083ce59d8b48f325f881a5c16ac325d72c732fbb64f7dac32acba6133bc0685	["<PROVENANCE>/provenance.json"]
<PROVENANCE>/published.py	709	695275cc97ff19807a168cb905a9b78565a012249ec0c8e639ebd4e5954f621b	["<PROVENANCE>/published.py"]
<PROVENANCE>/refcheck.py	500	6a492e1113de7b5a948eb3cb4786a03b3b331cfd2946f3d39e59685c7b4b97fe	["<PROVENANCE>/refcheck.py"]
<PROVENANCE>/runner/run_record.sh	90469	4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786	["<PROVENANCE>/runner/run_record.sh"]
<PROVENANCE>/scripts/committer	2682	fcd658fb20f007fdda0d0b70b4aae009f9d1635056850a386ca12c3e10c23f72	["<PROVENANCE>/scripts/committer"]
<PROVENANCE>/seed_prefix_check.py	1773	c08f3c1af6cb9ff118d95bf96dff6c470e4aefac32667a7d367a104f7ae14a4b	["<PROVENANCE>/seed_prefix_check.py"]
<PROVENANCE>/shacore.py	3150	5eca8622348642dc1d49364840707321f650b160f87c0ba4d9d19292ab5f61a7	["<PROVENANCE>/shacore.py"]
<PROVENANCE>/tab2check.py	2612	ea89fabeed6ca724ac5177d07c7595cb92840c052e854b080a8dce526f17b070	["<PROVENANCE>/tab2check.py"]
<PROVENANCE>/tests/test_campaign_contract.sh	4751	c1927f79702c9b411ff812cdd4e1371535eeb9fc82cd82c747c255468b939cca	["<PROVENANCE>/tests/test_campaign_contract.sh"]
<PROVENANCE>/tests/test_runner_nounset.sh	3829	67cd301be42232e3fb09feb47a54299a8baf77f4cd9d919160023bb406d18da9	["<PROVENANCE>/tests/test_runner_nounset.sh"]
<PROVENANCE>/trail.py	3490	7be7ff6135675807b4ae33b3ae262268f607f2da8a20d694747d4eee009de52d	["<PROVENANCE>/trail.py"]
<PROVENANCE>/verify_pairs.py	1380	7015323c9b873107aa409ed5e05e561a1e68d3524252350d2b64caef86474008	["<PROVENANCE>/verify_pairs.py"]
<RUN>/FOUND	1693	7391e0efe2593fa286e1d67bf512dd5d826c35d4448da3d9690fbc812593b173	["<RUN>/FOUND"]
<RUN>/audit/advice/.inventory-cap.lock	0	e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855	["<RUN>/audit/advice/.inventory-cap.lock"]
<RUN>/audit/advice/final-found-attempt-70.tsv	233060	f0bd226fcf05c84ae543bca6cb3f4d000edf576811461016466c7fb75943b9cc	["<RUN>/audit/advice/final-found-attempt-70.tsv"]
<RUN>/audit/advice/pre-match-current.tsv	228294	2abddb26eecf85c14c26b9172942a573d56c2d32503153f50661b5cb98bf95c0	["<RUN>/audit/advice/pre-match-current.tsv"]
<RUN>/audit/advice/pre-step3-chunk-0.tsv	161915	0434de5d56fc5696b1b1e3158c0a3c93385051ed00e95fd5e4a60648b9b50d9a	["<RUN>/audit/advice/pre-step3-chunk-0.tsv"]
<RUN>/audit/advice/pre-step3-chunk-1.tsv	163904	74f95d18dc94f782f32df186ba51bdcfb9fd2a35152bf081ab1fe72abf6761f3	["<RUN>/audit/advice/pre-step3-chunk-1.tsv"]
<RUN>/audit/advice/pre-step3-chunk-10.tsv	181865	94fe74c7ddea3bfcaf8bd52387198e3559866976965b82877099df27514115e5	["<RUN>/audit/advice/pre-step3-chunk-10.tsv"]
<RUN>/audit/advice/pre-step3-chunk-11.tsv	183870	5056df7c385b1fbb086b0ea297b9f1e5e3d6bcc6389e1336955fa8ab24d80e29	["<RUN>/audit/advice/pre-step3-chunk-11.tsv"]
<RUN>/audit/advice/pre-step3-chunk-12.tsv	185875	1114eebccc79b277b2a4d9341ea2e82b718dcf74a0c4ee6cc852daa0cd76c48e	["<RUN>/audit/advice/pre-step3-chunk-12.tsv"]
<RUN>/audit/advice/pre-step3-chunk-13.tsv	187880	8838dd3150526a759d8a73160a655d9dbdfe3d25f5b4f33e9b2fbc745a6c2922	["<RUN>/audit/advice/pre-step3-chunk-13.tsv"]
<RUN>/audit/advice/pre-step3-chunk-14.tsv	189885	2a92076d541398ef7b0c84c7f29c886eb58cad1111a7106c97b946f558d1e4a0	["<RUN>/audit/advice/pre-step3-chunk-14.tsv"]
<RUN>/audit/advice/pre-step3-chunk-15.tsv	191890	1a5593359927f20322c41cfef31300736f0885f7ed6d481869a6570ca77f6f38	["<RUN>/audit/advice/pre-step3-chunk-15.tsv"]
<RUN>/audit/advice/pre-step3-chunk-16.tsv	193895	bc8b2b6b89570b8cacdd18af0b0ecafaf9aa11baf5042cbdfb811c3dd8c7e9e3	["<RUN>/audit/advice/pre-step3-chunk-16.tsv"]
<RUN>/audit/advice/pre-step3-chunk-17.tsv	195900	c21244362c8571d589885cfe8450a55d967bd6332233a22a16a854b8aee6b805	["<RUN>/audit/advice/pre-step3-chunk-17.tsv"]
<RUN>/audit/advice/pre-step3-chunk-18.tsv	197905	622f8ae240cd2b167e973ef8b25f5954b923c24ca07fb3d3112c854100a544cb	["<RUN>/audit/advice/pre-step3-chunk-18.tsv"]
<RUN>/audit/advice/pre-step3-chunk-19.tsv	199910	716aff43999cf8fde67b568854321e10e47c866f98a3917d049b66cfc1a52b9d	["<RUN>/audit/advice/pre-step3-chunk-19.tsv"]
<RUN>/audit/advice/pre-step3-chunk-2.tsv	165891	bda761532380f34539d9bd983eecc6671aafa9472a367c72b75ee6cd6c403581	["<RUN>/audit/advice/pre-step3-chunk-2.tsv"]
<RUN>/audit/advice/pre-step3-chunk-20.tsv	201915	08f77a9d4b0b7806f15df37a3e0aa85ed761c72daa3633e0547de63273c9a57b	["<RUN>/audit/advice/pre-step3-chunk-20.tsv"]
<RUN>/audit/advice/pre-step3-chunk-21.tsv	203920	d246ff4c1e12e56bf25b6e359766177e9f19603cec3116770458db0fb366a49c	["<RUN>/audit/advice/pre-step3-chunk-21.tsv"]
<RUN>/audit/advice/pre-step3-chunk-22.tsv	205926	7d76da020de314a35d71b5e7097ea45849e94fbfb816f3cffb6f4c79bba00bdb	["<RUN>/audit/advice/pre-step3-chunk-22.tsv"]
<RUN>/audit/advice/pre-step3-chunk-23.tsv	207931	0789a727d77d035f12799ac64f556903e0e6b6a2ec5371a53bd0c46ced611361	["<RUN>/audit/advice/pre-step3-chunk-23.tsv"]
<RUN>/audit/advice/pre-step3-chunk-24.tsv	209936	52a257524f97821c71128520656c33ad59b7dd8d3ee7d4de4d7b91a42591366d	["<RUN>/audit/advice/pre-step3-chunk-24.tsv"]
<RUN>/audit/advice/pre-step3-chunk-25.tsv	211941	06c15f08c702663e99a6050922e8f0adab7c12f424e7cab26a32452dfbe937be	["<RUN>/audit/advice/pre-step3-chunk-25.tsv"]
<RUN>/audit/advice/pre-step3-chunk-26.tsv	213946	ce61dde7b99abd1c38984b7d4dce955d6d3bb3c6761d41925b749a871cfef7bc	["<RUN>/audit/advice/pre-step3-chunk-26.tsv"]
<RUN>/audit/advice/pre-step3-chunk-27.tsv	215951	a5ff245559ff74eac4fe737bf70378cbc3d74f153a9b38808368c3872348c2da	["<RUN>/audit/advice/pre-step3-chunk-27.tsv"]
<RUN>/audit/advice/pre-step3-chunk-28.tsv	217957	12e3d57e5f2709cffc2a6e127a1353c011732eed84b577a8e2f0c323c6726cb0	["<RUN>/audit/advice/pre-step3-chunk-28.tsv"]
<RUN>/audit/advice/pre-step3-chunk-29.tsv	219962	ad5bf49d9c0dcf6cbe46ef53d17a56da0eda53dfb79defb7e34f4eea68f5f1dc	["<RUN>/audit/advice/pre-step3-chunk-29.tsv"]
<RUN>/audit/advice/pre-step3-chunk-3.tsv	167878	18df9171795f7f3093b6a47a02002ff8343c71e5534e11fe428654c3eb892215	["<RUN>/audit/advice/pre-step3-chunk-3.tsv"]
<RUN>/audit/advice/pre-step3-chunk-30.tsv	221967	9976209be073991a8a938f5e01a3c82c326e1361fda97fce624a0b789e957d08	["<RUN>/audit/advice/pre-step3-chunk-30.tsv"]
<RUN>/audit/advice/pre-step3-chunk-31.tsv	223972	6b7e8c2cfd3cf9a509b8bf68c6ce244741b0c8c898b55988ec1023353e2a1f1c	["<RUN>/audit/advice/pre-step3-chunk-31.tsv"]
<RUN>/audit/advice/pre-step3-chunk-32.tsv	225977	0a5d24fcac4639a56a166913e64e5b9a7d5724fda31c43ad7ddbce10b44276d3	["<RUN>/audit/advice/pre-step3-chunk-32.tsv"]
<RUN>/audit/advice/pre-step3-chunk-33.tsv	227982	d1cb0090ecdd8969ed3c4ac220221332f05fdb0b93528426f0c6709c21055f81	["<RUN>/audit/advice/pre-step3-chunk-33.tsv"]
<RUN>/audit/advice/pre-step3-chunk-34.tsv	229987	bb55cc9a050a2d14c1c376e7345345e718d361bd50f8877efa2b4dd10df365f6	["<RUN>/audit/advice/pre-step3-chunk-34.tsv"]
<RUN>/audit/advice/pre-step3-chunk-4.tsv	169865	5da9750f87bcef5804fe0f587bcfb9a550061386f2dcf7f635edf8a8b25d7f40	["<RUN>/audit/advice/pre-step3-chunk-4.tsv"]
<RUN>/audit/advice/pre-step3-chunk-5.tsv	171864	582f5f6e90738c60196fb044e55134c59eafa00f669a479b54f45986a29ea4b8	["<RUN>/audit/advice/pre-step3-chunk-5.tsv"]
<RUN>/audit/advice/pre-step3-chunk-6.tsv	173863	10d83f499ba77da67d29b78da72fe88b21812dc6d21d51f8c31a4926b751663d	["<RUN>/audit/advice/pre-step3-chunk-6.tsv"]
<RUN>/audit/advice/pre-step3-chunk-7.tsv	175862	ae658c61ee954afaea6efd4c8a555161f59b7fdc47b14d6227cacdf3bb450f9b	["<RUN>/audit/advice/pre-step3-chunk-7.tsv"]
<RUN>/audit/advice/pre-step3-chunk-8.tsv	177861	90b5eb06e0023c54ab5ed095ef467c5c713ec76af6f63b680ae3688707d3d87e	["<RUN>/audit/advice/pre-step3-chunk-8.tsv"]
<RUN>/audit/advice/pre-step3-chunk-9.tsv	179860	89867af63da3c3f8aa9627ccdcb5052694f67dc74fa80df9c036c720e69fcb5c	["<RUN>/audit/advice/pre-step3-chunk-9.tsv"]
<RUN>/audit/advice/prelaunch-seal.tsv	154192	c9877dad39329ff33b74274dcc0bcee7810184f662b58508617fc67001910a07	["<RUN>/audit/advice/prelaunch-seal.tsv"]
<RUN>/audit/invocation-20261004T135729Z-48079.txt	1007	67c2a2d7d36075e3139758796be9b0140ca42801c9da4c4acf6b23cfe7864be1	["<RUN>/audit/invocation-20261004T135729Z-48079.txt"]
<RUN>/audit/invocations/.invocation-cap.lock	0	e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855	["<RUN>/audit/invocations/.invocation-cap.lock"]
<RUN>/audit/invocations/invocation-20261004T135729Z-48079.tsv	303	cb20c95cf46981d0edc2e5665d2f5e2f4245b024d3a09efc195d6e8100fc1f76	["<RUN>/audit/invocations/invocation-20261004T135729Z-48079.tsv"]
<RUN>/audit/migration/mini-post-retire-v3.2-zero-work.json	2343	87c363ac3227af5cf68fece6735265cec82659d3016ecb9a990b98702cc91272	["<RUN>/audit/migration/mini-post-retire-v3.2-zero-work.json"]
<RUN>/audit/migration/mini-range-release.tsv	359	63cd400e41e436005c90c8759b8124cffed1a25b9bf90abb471f0609401f382f	["<RUN>/audit/migration/mini-range-release.tsv"]
<RUN>/audit/operations/match-attempt-1.tsv	755	2df2026c9a5721dd968835a7944ed50b930e34915b8817d4fec95ef18a219ea9	["<RUN>/audit/operations/match-attempt-1.tsv"]
<RUN>/audit/operations/match-attempt-11.tsv	756	851150fbe0aa8055578f6a53a23b11a5d80a09b63996b2710cb2ce1b3e066d87	["<RUN>/audit/operations/match-attempt-11.tsv"]
<RUN>/audit/operations/match-attempt-13.tsv	756	1824025b7722bbe2e5578709428da1e613b18def5ccf922893ec77263b4a8ff1	["<RUN>/audit/operations/match-attempt-13.tsv"]
<RUN>/audit/operations/match-attempt-15.tsv	756	d31e17cbe856cafa0ede3efe99327c383975668f8b2f349a103c10e3d39780c4	["<RUN>/audit/operations/match-attempt-15.tsv"]
<RUN>/audit/operations/match-attempt-17.tsv	756	c1d7ee9aef71f8985bd7f453a79b13a957164e8ed43e403e86a120b4b75065b9	["<RUN>/audit/operations/match-attempt-17.tsv"]
<RUN>/audit/operations/match-attempt-19.tsv	756	b98b0511583b1d7f9a75a9471ebbc5e4fbab9b3bf2a65283ec67ee9e001661eb	["<RUN>/audit/operations/match-attempt-19.tsv"]
<RUN>/audit/operations/match-attempt-21.tsv	757	22f999279b0283ecb98e675638da438f41df3f4ca45e28dd2d5cac277aa66ca8	["<RUN>/audit/operations/match-attempt-21.tsv"]
<RUN>/audit/operations/match-attempt-23.tsv	757	ea0027f1446eba1720614574b535ae3932c3970602e1009f87bd0bea481ef59a	["<RUN>/audit/operations/match-attempt-23.tsv"]
<RUN>/audit/operations/match-attempt-25.tsv	757	e373a8c6b9d555d87995305e722b9ade5bdf1798aabcc8cf89cd77ca0e0bb89f	["<RUN>/audit/operations/match-attempt-25.tsv"]
<RUN>/audit/operations/match-attempt-27.tsv	757	ab9aba7026451822fea7f3e09240855be2c1b21bcc059ddd04559a324ea7e1c5	["<RUN>/audit/operations/match-attempt-27.tsv"]
<RUN>/audit/operations/match-attempt-29.tsv	757	174c8799e65c514e8f2e74cb87897b5191e20941993f3c51b8f600cd4ddc8158	["<RUN>/audit/operations/match-attempt-29.tsv"]
<RUN>/audit/operations/match-attempt-3.tsv	755	55837d632f9b6d7d797e342a49ebcc1db0dfbb0bf98db78d4b4ace7594d3044b	["<RUN>/audit/operations/match-attempt-3.tsv"]
<RUN>/audit/operations/match-attempt-31.tsv	757	51e4d62f5d4e43e1e4323ea96ea961fd30e6227dc9a6ad72fb6662723d2418f4	["<RUN>/audit/operations/match-attempt-31.tsv"]
<RUN>/audit/operations/match-attempt-33.tsv	757	4909b13e7794cae5f7fb912b14e467d87b95c5a95ff275b0de76f937c7128b6f	["<RUN>/audit/operations/match-attempt-33.tsv"]
<RUN>/audit/operations/match-attempt-35.tsv	757	a0896b1d2065aa7e6a3b4ad5864f34981f2f0971efcdce8548877192318e83de	["<RUN>/audit/operations/match-attempt-35.tsv"]
<RUN>/audit/operations/match-attempt-37.tsv	757	9802489f4b28f5ce7ef71719089fd7c3e604b87772650312ff8aed21cc96c3ad	["<RUN>/audit/operations/match-attempt-37.tsv"]
<RUN>/audit/operations/match-attempt-39.tsv	757	6b3b1969faf36b399092f0fd0f044f9e5d1e7c8c9fd6464cd6d56b57ed411750	["<RUN>/audit/operations/match-attempt-39.tsv"]
<RUN>/audit/operations/match-attempt-41.tsv	757	887f6acd1dd00a41a4c448c8b1315d5c466bd6a7645b579f63faa953ac4773f1	["<RUN>/audit/operations/match-attempt-41.tsv"]
<RUN>/audit/operations/match-attempt-43.tsv	757	fe825b50ec2b011dd3b3c4abd5b03796fd7d2742919555951afee03a42690ab4	["<RUN>/audit/operations/match-attempt-43.tsv"]
<RUN>/audit/operations/match-attempt-45.tsv	757	f2211fcf53bf4d779c371a48e71778638ef9ddbf419415506a88e91fbd12ccca	["<RUN>/audit/operations/match-attempt-45.tsv"]
<RUN>/audit/operations/match-attempt-47.tsv	757	00f150fabd30927342d2b912b3730c14696df6fa6c41e33031d700af04b1367f	["<RUN>/audit/operations/match-attempt-47.tsv"]
<RUN>/audit/operations/match-attempt-49.tsv	757	e3f2904b06e193879b2f052d549af1888d94051237fc357e544be089bb9b53fe	["<RUN>/audit/operations/match-attempt-49.tsv"]
<RUN>/audit/operations/match-attempt-5.tsv	755	0acdfc89c5d3eba020b0dc2bf339f8797a3485c0ff401486510c64f7f6ec9efe	["<RUN>/audit/operations/match-attempt-5.tsv"]
<RUN>/audit/operations/match-attempt-51.tsv	757	dc46851ef90131e234258fefb30b1535e8585a1f4b6985888071b59cdefafb24	["<RUN>/audit/operations/match-attempt-51.tsv"]
<RUN>/audit/operations/match-attempt-53.tsv	757	13abbdc14ccc20194661ac03ffd293868c231c7142834c3ea443c68baa8b24ed	["<RUN>/audit/operations/match-attempt-53.tsv"]
<RUN>/audit/operations/match-attempt-55.tsv	757	c39a3176dc1270ed779974435e4f18ffc8a2a49ead80c9a80421289025fad3b8	["<RUN>/audit/operations/match-attempt-55.tsv"]
<RUN>/audit/operations/match-attempt-57.tsv	757	f45e8f092e5a0eed5fb83a54155c13c436cdd84bcc3e9cb5d314862a4ba9e369	["<RUN>/audit/operations/match-attempt-57.tsv"]
<RUN>/audit/operations/match-attempt-59.tsv	757	2f8a73bbf9ae013e764d62ea9aa9d13d66d124e2dbbcdcc681236c061ef57d8c	["<RUN>/audit/operations/match-attempt-59.tsv"]
<RUN>/audit/operations/match-attempt-61.tsv	757	633419d9ef8df048dec0f31899c3ea5b5cc35cc31674c08899ff04ea7163ef1b	["<RUN>/audit/operations/match-attempt-61.tsv"]
<RUN>/audit/operations/match-attempt-63.tsv	757	951ceff96eb8400232c77dd8cc0154f475fc183fc085cd759d7cda564b829cb7	["<RUN>/audit/operations/match-attempt-63.tsv"]
<RUN>/audit/operations/match-attempt-65.tsv	757	72dffd657f635b43e38eca8d68b60dcad01b22018a6e82af4b3665f7d85cc6f3	["<RUN>/audit/operations/match-attempt-65.tsv"]
<RUN>/audit/operations/match-attempt-67.tsv	757	5467e87a9d2a70e46cdfaefe4719f98c07a16672f252a141baf46989cfb4a7a8	["<RUN>/audit/operations/match-attempt-67.tsv"]
<RUN>/audit/operations/match-attempt-69.tsv	757	ed7336bd1e1563e32e6e480182910d724403e8804ecbc4b007a8e11e5c76a11f	["<RUN>/audit/operations/match-attempt-69.tsv"]
<RUN>/audit/operations/match-attempt-7.tsv	755	192c0bce6023fd8925e849306e536576f15bc927bdc4378f5c73e98eefbcca23	["<RUN>/audit/operations/match-attempt-7.tsv"]
<RUN>/audit/operations/match-attempt-9.tsv	755	e8cdef38e20c1ff2cc45558eae2594d28dbc6fccfbcee649edaa4b82a5e5c6fa	["<RUN>/audit/operations/match-attempt-9.tsv"]
<RUN>/audit/operations/step3-attempt-10.tsv	862	68d15a329af7619faa7652b4dba77f46ffce292c83a0239a84334b6ae0701da4	["<RUN>/audit/operations/step3-attempt-10.tsv"]
<RUN>/audit/operations/step3-attempt-12.tsv	862	77fe369a3e13afaa4a94218d8efed44cc4230b9cfe6ec74c9f28df59bcf80609	["<RUN>/audit/operations/step3-attempt-12.tsv"]
<RUN>/audit/operations/step3-attempt-14.tsv	862	eb7b4148a3f5e1cc0b5e688cc4da16eb17e0a188dc3a248aeac60071d2958b34	["<RUN>/audit/operations/step3-attempt-14.tsv"]
<RUN>/audit/operations/step3-attempt-16.tsv	862	fc8db2df8d2b5e1e5a1b4104bf724836fd37a0acc1473b976fe11299b3528ccc	["<RUN>/audit/operations/step3-attempt-16.tsv"]
<RUN>/audit/operations/step3-attempt-18.tsv	862	029883b35dab05b46436ad044071a44a28cb47746a29692d0b60dab34a92d969	["<RUN>/audit/operations/step3-attempt-18.tsv"]
<RUN>/audit/operations/step3-attempt-2.tsv	861	203ae25290fe228d87d9982b47728d7f1eea1f018f972ca939562f6879ca978d	["<RUN>/audit/operations/step3-attempt-2.tsv"]
<RUN>/audit/operations/step3-attempt-20.tsv	862	aec208402578f471b3b20cfe44486a427317b343d27f6b79f4a58db48793586d	["<RUN>/audit/operations/step3-attempt-20.tsv"]
<RUN>/audit/operations/step3-attempt-22.tsv	863	8e2961d71632c68abd5ebeb7da97d0af4a34e6e61ca984e0e14fc0a51da189a9	["<RUN>/audit/operations/step3-attempt-22.tsv"]
<RUN>/audit/operations/step3-attempt-24.tsv	863	8d49f1309d02cf737aba08428ef1364f0c935402695a317a4cac89c7b5e8fb11	["<RUN>/audit/operations/step3-attempt-24.tsv"]
<RUN>/audit/operations/step3-attempt-26.tsv	863	1eb8eb5ddf0b036266de86808e4730abb201b6fe417482d5ffe7909ae1a4a34e	["<RUN>/audit/operations/step3-attempt-26.tsv"]
<RUN>/audit/operations/step3-attempt-28.tsv	863	a888a49cb57c8c76f9b60cb99dbb25b57e04679ecefe55cfb594843eb55afa97	["<RUN>/audit/operations/step3-attempt-28.tsv"]
<RUN>/audit/operations/step3-attempt-30.tsv	863	03822a536fb3f8fdc3772a36cb72d2483f882397e8f81548bd18525dc44f3de8	["<RUN>/audit/operations/step3-attempt-30.tsv"]
<RUN>/audit/operations/step3-attempt-32.tsv	863	3a7e04b31b3985da50223d7b52443357c1e573978234afe853e7d990c143042f	["<RUN>/audit/operations/step3-attempt-32.tsv"]
<RUN>/audit/operations/step3-attempt-34.tsv	863	0443082263ff97c9ed58010a11f7071b9928bdf25a4edc2074595525ec076046	["<RUN>/audit/operations/step3-attempt-34.tsv"]
<RUN>/audit/operations/step3-attempt-36.tsv	863	c8ece986bc8fea351bcee0c15c1623e58fdfbad03f416d865e63d786c232c892	["<RUN>/audit/operations/step3-attempt-36.tsv"]
<RUN>/audit/operations/step3-attempt-38.tsv	863	f8759969081960d5824b7cecfb05c60b4247a850175565fe311d9a1a041f6b48	["<RUN>/audit/operations/step3-attempt-38.tsv"]
<RUN>/audit/operations/step3-attempt-4.tsv	861	61d3c7d8f638383d201885d2df88027eff0fbb92b13e32c663844bc9e58b2c80	["<RUN>/audit/operations/step3-attempt-4.tsv"]
<RUN>/audit/operations/step3-attempt-40.tsv	863	93232b9f4a02c54880362051a7a26cbba3376f632a2001557fdcfc2cf112afeb	["<RUN>/audit/operations/step3-attempt-40.tsv"]
<RUN>/audit/operations/step3-attempt-42.tsv	863	2e003ee5f31c9190b7f3d4fbea799a82a5ed3e5eeba7405907f80a10808bd9b6	["<RUN>/audit/operations/step3-attempt-42.tsv"]
<RUN>/audit/operations/step3-attempt-44.tsv	863	2b18a3b16bec626be25a3128294edd851d2ddd5da615f89fef60ba5aa40bf114	["<RUN>/audit/operations/step3-attempt-44.tsv"]
<RUN>/audit/operations/step3-attempt-46.tsv	863	47ee24d5405da7bca704ac71f12fd379c7bc16e6451f635f9cc18c91fe1a8638	["<RUN>/audit/operations/step3-attempt-46.tsv"]
<RUN>/audit/operations/step3-attempt-48.tsv	863	c91b4768e92d67313cbe847be2dad70faab390d99e5fc77ec41876da6861e69b	["<RUN>/audit/operations/step3-attempt-48.tsv"]
<RUN>/audit/operations/step3-attempt-50.tsv	863	81fa0e00cf6e2c442babc3a6927d0a9324838c551ff2739c1d015f4d3d879189	["<RUN>/audit/operations/step3-attempt-50.tsv"]
<RUN>/audit/operations/step3-attempt-52.tsv	863	09040bb58285076888341e6de320b7f631ebe3ab26b4fe14ecfc3576b1f2852e	["<RUN>/audit/operations/step3-attempt-52.tsv"]
<RUN>/audit/operations/step3-attempt-54.tsv	863	9b6e3d8a21d597f72a0fc3f4185341ff73b82f8ec1333e33a3c29d52d703a09c	["<RUN>/audit/operations/step3-attempt-54.tsv"]
<RUN>/audit/operations/step3-attempt-56.tsv	863	eb5920267e2be6d553763bc932b3e2c776c72da8993d5bba9d65329be13aa53a	["<RUN>/audit/operations/step3-attempt-56.tsv"]
<RUN>/audit/operations/step3-attempt-58.tsv	863	382169077e748e847378c546cd542a5a6ff057243fa2ed67dbbc5bf92dc8ca48	["<RUN>/audit/operations/step3-attempt-58.tsv"]
<RUN>/audit/operations/step3-attempt-6.tsv	861	1b6bc2df5274e642249e38f6f75bcc9c1c91953ae6fcfb0620e24befa39dc6a1	["<RUN>/audit/operations/step3-attempt-6.tsv"]
<RUN>/audit/operations/step3-attempt-60.tsv	863	1a3446c02de7120b20ce9195e80b17476c9f10c02c781fab3880e84dcd990469	["<RUN>/audit/operations/step3-attempt-60.tsv"]
<RUN>/audit/operations/step3-attempt-62.tsv	863	53993d7440f4d86a601a497492edde1e7e8526576d26fb2d6688c06227d043db	["<RUN>/audit/operations/step3-attempt-62.tsv"]
<RUN>/audit/operations/step3-attempt-64.tsv	863	730c5faf097663f5fe72beab273e92090a439df649b235a1800020d552314cb0	["<RUN>/audit/operations/step3-attempt-64.tsv"]
<RUN>/audit/operations/step3-attempt-66.tsv	863	2984e4dd9b897afb9f36086945deb8e55aaa2a20b9048b7f3d87a59183398a07	["<RUN>/audit/operations/step3-attempt-66.tsv"]
<RUN>/audit/operations/step3-attempt-68.tsv	863	9d103cca238170540fdc614773b86df78f9783bbff0ee1b1f11fea0df04324d0	["<RUN>/audit/operations/step3-attempt-68.tsv"]
<RUN>/audit/operations/step3-attempt-70.tsv	872	82e75ba282dc7368d53336232d66cb5dfc6032c448337cbefeb01eca4097e26e	["<RUN>/audit/operations/step3-attempt-70.tsv"]
<RUN>/audit/operations/step3-attempt-8.tsv	861	7bae02f7a1dfd68da9b6b26c5953ab8406096e45540c933a13467cd97dcb2d3d	["<RUN>/audit/operations/step3-attempt-8.tsv"]
<RUN>/audit/reservations/match-attempt-1.tsv	331	65308855dd2d6bc2fc679414509e19a811f63672fe0025588c5fe09647c8bb81	["<RUN>/audit/reservations/match-attempt-1.tsv"]
<RUN>/audit/reservations/match-attempt-11.tsv	332	75a3a6fb22f1274ee5bf70ea9cf70e56d07f3366f5850d6b38bedf7681565333	["<RUN>/audit/reservations/match-attempt-11.tsv"]
<RUN>/audit/reservations/match-attempt-13.tsv	332	aacbf652339de76ca4cee2445d5a80946306fb7bb1c6d707fbdb152dba8aab46	["<RUN>/audit/reservations/match-attempt-13.tsv"]
<RUN>/audit/reservations/match-attempt-15.tsv	332	494c684112ed52960758cd21a9f0600da5706019119c882551e207db2221ca35	["<RUN>/audit/reservations/match-attempt-15.tsv"]
<RUN>/audit/reservations/match-attempt-17.tsv	332	6fbd8b2b0abc139e83c4335f296d8c652b96c7fcfcd87e8fbb6bb757132835e5	["<RUN>/audit/reservations/match-attempt-17.tsv"]
<RUN>/audit/reservations/match-attempt-19.tsv	332	680762b0627aebd664ed09bef6481399fb4aac5947899b5983d61b8805da0f5b	["<RUN>/audit/reservations/match-attempt-19.tsv"]
<RUN>/audit/reservations/match-attempt-21.tsv	333	b9ad89673e10a00f7d9e8bb9fd5759398e39b14c4b0421c63211ddeac75c24dd	["<RUN>/audit/reservations/match-attempt-21.tsv"]
<RUN>/audit/reservations/match-attempt-23.tsv	333	9bf15dc4816384920c8123c68200ac93fc7e715f0657a44da2ae8b1065cce044	["<RUN>/audit/reservations/match-attempt-23.tsv"]
<RUN>/audit/reservations/match-attempt-25.tsv	333	0253f5c2e0909a5494b2937abedf79a4c18931ba24e4183984a0c307b523b7b8	["<RUN>/audit/reservations/match-attempt-25.tsv"]
<RUN>/audit/reservations/match-attempt-27.tsv	333	0588740c875dc28f142fb1077932b89d361dacf2c06bc788ccce527329557d90	["<RUN>/audit/reservations/match-attempt-27.tsv"]
<RUN>/audit/reservations/match-attempt-29.tsv	333	451326766223412246c23ccc683a72ba742e99a96a9771e03b4434aa9ce60995	["<RUN>/audit/reservations/match-attempt-29.tsv"]
<RUN>/audit/reservations/match-attempt-3.tsv	331	3174522cc33acdbddee23cfa406cce0b6786e2f0a2ae144561f5192cd4b4d33c	["<RUN>/audit/reservations/match-attempt-3.tsv"]
<RUN>/audit/reservations/match-attempt-31.tsv	333	2e4c749d2cc28a9baf01b77d833ff1f795a784ab147d45ba3ec35eda69e438c8	["<RUN>/audit/reservations/match-attempt-31.tsv"]
<RUN>/audit/reservations/match-attempt-33.tsv	333	deccd3bc356260f8e8eef17b3f5d7d1e6962ad614cd959bf49f921a4da230046	["<RUN>/audit/reservations/match-attempt-33.tsv"]
<RUN>/audit/reservations/match-attempt-35.tsv	333	d2f93afd3c31fd1f5ceba89168016064bb23df68615df52b534679fee01ecbb3	["<RUN>/audit/reservations/match-attempt-35.tsv"]
<RUN>/audit/reservations/match-attempt-37.tsv	333	e9e5a686fd891eb3468957a325ad6a3604d8a204f878834d29c2de31e0b94b06	["<RUN>/audit/reservations/match-attempt-37.tsv"]
<RUN>/audit/reservations/match-attempt-39.tsv	333	7e5d332bd99d9c84c25e11d5f17040e6c070276298647b84f97b1ef88676e36b	["<RUN>/audit/reservations/match-attempt-39.tsv"]
<RUN>/audit/reservations/match-attempt-41.tsv	333	d734dbaff4d7a90cf1752e1aa9bd966f7a8898a5ca2f05b42936323f1432c942	["<RUN>/audit/reservations/match-attempt-41.tsv"]
<RUN>/audit/reservations/match-attempt-43.tsv	333	c02c46d3800351bd6696ce19ec5884658a8b63d2bfbe2ef31e8234a1d49798cb	["<RUN>/audit/reservations/match-attempt-43.tsv"]
<RUN>/audit/reservations/match-attempt-45.tsv	333	32543a79688f354dd33b99bce0adf6276af0ef973aa52491c000d0ef5d845872	["<RUN>/audit/reservations/match-attempt-45.tsv"]
<RUN>/audit/reservations/match-attempt-47.tsv	333	e7d4000db88bb5f1e51120a50ff023af3ab7aaa94958d2062d117fc9e78d0bc1	["<RUN>/audit/reservations/match-attempt-47.tsv"]
<RUN>/audit/reservations/match-attempt-49.tsv	333	12ad097e01a9194661cec289dcba6821585d4a87c0255f2e044bdba537d551e3	["<RUN>/audit/reservations/match-attempt-49.tsv"]
<RUN>/audit/reservations/match-attempt-5.tsv	331	9baabbc49e43ef29b349fc55fc82d6812589b89e1a4d558c097c62e7ba1d2073	["<RUN>/audit/reservations/match-attempt-5.tsv"]
<RUN>/audit/reservations/match-attempt-51.tsv	333	ec54e912e600693b440f2b38e81aef160257712b446d0fefa85fdf2728528bc5	["<RUN>/audit/reservations/match-attempt-51.tsv"]
<RUN>/audit/reservations/match-attempt-53.tsv	333	8c2155966971e576cfeeaf62046e56647f4bafeab063318e9e4cc5852e388c48	["<RUN>/audit/reservations/match-attempt-53.tsv"]
<RUN>/audit/reservations/match-attempt-55.tsv	333	6aab9791c99696c6648e86a9d4a8f63a7a4a8e59a131f9b5cdbac661db7fa1db	["<RUN>/audit/reservations/match-attempt-55.tsv"]
<RUN>/audit/reservations/match-attempt-57.tsv	333	932717349de657b8c44d90ac3bc25da99039bfdc386aea1c21c55d50ea1cb3b0	["<RUN>/audit/reservations/match-attempt-57.tsv"]
<RUN>/audit/reservations/match-attempt-59.tsv	333	a664c0d3ec86d0b2fd8bd24768410a3b5ed275c35196c32f49782320dde5ee98	["<RUN>/audit/reservations/match-attempt-59.tsv"]
<RUN>/audit/reservations/match-attempt-61.tsv	333	dfd12819598fdb7d032e3c560600c9915cdb8e625c5317e1669b4fcfb369bc05	["<RUN>/audit/reservations/match-attempt-61.tsv"]
<RUN>/audit/reservations/match-attempt-63.tsv	333	a0b8e2078208047e88ff09ccddab002414064c678ad02dca6d7fb733562f76fd	["<RUN>/audit/reservations/match-attempt-63.tsv"]
<RUN>/audit/reservations/match-attempt-65.tsv	333	1390220ff867fb8c2c5e2a1237e5792432d2544b097ce6ed61e929586b29d9eb	["<RUN>/audit/reservations/match-attempt-65.tsv"]
<RUN>/audit/reservations/match-attempt-67.tsv	333	2e76673415fef5aeb1c2e4e2d71375cb48e4fe03dc8b3f073b59fb84f91ee9d4	["<RUN>/audit/reservations/match-attempt-67.tsv"]
<RUN>/audit/reservations/match-attempt-69.tsv	333	670bfc68651b64cda8a7b9893e7bc90022dafa51197028cedfe8447fd64f84fc	["<RUN>/audit/reservations/match-attempt-69.tsv"]
<RUN>/audit/reservations/match-attempt-7.tsv	331	57cbf14fb9caa97bbe0983a12dd6f5458a0d04ba09e7e01433e863a80bc63a32	["<RUN>/audit/reservations/match-attempt-7.tsv"]
<RUN>/audit/reservations/match-attempt-9.tsv	331	5fc3b933e84bc29c120f1b41a12aeeb22a30a207e05da6261ab771149314f682	["<RUN>/audit/reservations/match-attempt-9.tsv"]
<RUN>/audit/reservations/step3-attempt-10.tsv	432	ca4a2ecb36a1c460ad987ecb8135543843d338c447fc82f22837966233335ff5	["<RUN>/audit/reservations/step3-attempt-10.tsv"]
<RUN>/audit/reservations/step3-attempt-12.tsv	432	2a01632f657bcb83775afd445a88d8381964910878f738e2513050628616acb2	["<RUN>/audit/reservations/step3-attempt-12.tsv"]
<RUN>/audit/reservations/step3-attempt-14.tsv	432	5ce29fe2d5f1274ffe94a8623a4d7a64eeaf05d9df486c02fce0ae5f850d028c	["<RUN>/audit/reservations/step3-attempt-14.tsv"]
<RUN>/audit/reservations/step3-attempt-16.tsv	432	3a86e17a35df07dc89a5c58aa36a95ba7ac62bd47c9221c1de6e1c26364dcb4f	["<RUN>/audit/reservations/step3-attempt-16.tsv"]
<RUN>/audit/reservations/step3-attempt-18.tsv	432	fb5561005e46182150801815b89cb61196db3fb646f38d4a7e40ebe6b4c504a2	["<RUN>/audit/reservations/step3-attempt-18.tsv"]
<RUN>/audit/reservations/step3-attempt-2.tsv	424	06efcdabf42b784c6d3d9b178f45f0aecfd555f0a7724b9bf1d316e8a155a1ee	["<RUN>/audit/reservations/step3-attempt-2.tsv"]
<RUN>/audit/reservations/step3-attempt-20.tsv	432	5b4c415693c0875ce95984873ad275c96ed66a4f57c1cd47835e42295eb41598	["<RUN>/audit/reservations/step3-attempt-20.tsv"]
<RUN>/audit/reservations/step3-attempt-22.tsv	433	7d8e623b3e17f7573976ad577b4b6af4a2b07ed8d4425cf9dd145ee71b19c4fa	["<RUN>/audit/reservations/step3-attempt-22.tsv"]
<RUN>/audit/reservations/step3-attempt-24.tsv	433	816e079a6485b1bd1380f3fe25d80e8ba7ee3ec2ed1ffa0ad9c87c9092d39586	["<RUN>/audit/reservations/step3-attempt-24.tsv"]
<RUN>/audit/reservations/step3-attempt-26.tsv	433	ae73f250d85ba99fa6b62b8dd4b394233aa83a3d0425015a68ced0a3d7879e6b	["<RUN>/audit/reservations/step3-attempt-26.tsv"]
<RUN>/audit/reservations/step3-attempt-28.tsv	433	5b3d680262dda5efc4f7b862a3c131f9f9cc76ee3ccc3c7cdc25700d9c9a7536	["<RUN>/audit/reservations/step3-attempt-28.tsv"]
<RUN>/audit/reservations/step3-attempt-30.tsv	433	10f2a41bc9119eaed9c5086903062914d83e9351c46d958b7961d9ad3ab896af	["<RUN>/audit/reservations/step3-attempt-30.tsv"]
<RUN>/audit/reservations/step3-attempt-32.tsv	433	2d258aa5726248acc49bb6c414634d6c7ea74397ab45b898223cef5eaa36cb11	["<RUN>/audit/reservations/step3-attempt-32.tsv"]
<RUN>/audit/reservations/step3-attempt-34.tsv	433	fe3e6190c6422f88109eb32bbd4276ae0c7ca6bbf9cde3af741215a95e1a1f9c	["<RUN>/audit/reservations/step3-attempt-34.tsv"]
<RUN>/audit/reservations/step3-attempt-36.tsv	433	bd41557c046fd103cb794c4b69f572e46f8c1078910fa220e3d4c7df4493ac8a	["<RUN>/audit/reservations/step3-attempt-36.tsv"]
<RUN>/audit/reservations/step3-attempt-38.tsv	433	faabd36d0520d2887688d4d76cd66d09c4c0a0d5ed9c520d54c3fcdfc233e86e	["<RUN>/audit/reservations/step3-attempt-38.tsv"]
<RUN>/audit/reservations/step3-attempt-4.tsv	429	37ff655639acac01da40e5e7868f712f00eb9305dce38f43848da4d642af1362	["<RUN>/audit/reservations/step3-attempt-4.tsv"]
<RUN>/audit/reservations/step3-attempt-40.tsv	433	888c344e4f44a8f0744cddaf45ec1d45bb68134f53f04aa7f10b500520dce5f6	["<RUN>/audit/reservations/step3-attempt-40.tsv"]
<RUN>/audit/reservations/step3-attempt-42.tsv	433	409d99c5e4d0e3575b756b780929c44f16707f2ae67945931d216c7562cac1b4	["<RUN>/audit/reservations/step3-attempt-42.tsv"]
<RUN>/audit/reservations/step3-attempt-44.tsv	433	af3192b8c330b873e834f9c4eb2a2fc3a909ce7ba6978328c250c68c8af2b836	["<RUN>/audit/reservations/step3-attempt-44.tsv"]
<RUN>/audit/reservations/step3-attempt-46.tsv	433	846219253d520c1f628e2a4721b98ac3219a24345b90285e53dcdeeafd0e0404	["<RUN>/audit/reservations/step3-attempt-46.tsv"]
<RUN>/audit/reservations/step3-attempt-48.tsv	434	66f10d67463e1cf08d2896acdb0cb4a913e52533178e1f9ac248ba4a99ad7838	["<RUN>/audit/reservations/step3-attempt-48.tsv"]
<RUN>/audit/reservations/step3-attempt-50.tsv	435	a8791285b81c68d78f91288c3ba33c18ba70d18cf690225f25e1b616b359996d	["<RUN>/audit/reservations/step3-attempt-50.tsv"]
<RUN>/audit/reservations/step3-attempt-52.tsv	435	778b0a41074afb55cb65d3b93159da8d5d972629d5362692b120eb314532aa2e	["<RUN>/audit/reservations/step3-attempt-52.tsv"]
<RUN>/audit/reservations/step3-attempt-54.tsv	435	9e83c586fdabc08491e595ae6bca02a1e14c14b9a10026045b2ec5c60181ee3c	["<RUN>/audit/reservations/step3-attempt-54.tsv"]
<RUN>/audit/reservations/step3-attempt-56.tsv	435	93ac83142d37f307b44d1e3102922a1feb72e4a7a6dabf8578ab0a073b6b247b	["<RUN>/audit/reservations/step3-attempt-56.tsv"]
<RUN>/audit/reservations/step3-attempt-58.tsv	435	09370bcfc5a40f97c83693cc858aeb0094bf9ab5cf0f5894f9ec23259e19fff5	["<RUN>/audit/reservations/step3-attempt-58.tsv"]
<RUN>/audit/reservations/step3-attempt-6.tsv	430	de91fde8330a9c5bfb9a4e630c25e592646607e3401bf2a63e11c6723475d22b	["<RUN>/audit/reservations/step3-attempt-6.tsv"]
<RUN>/audit/reservations/step3-attempt-60.tsv	435	a36467c70ddfd47aa2acfb87c1919c6bcc003b02bc0d332a2234e35fd3e3e947	["<RUN>/audit/reservations/step3-attempt-60.tsv"]
<RUN>/audit/reservations/step3-attempt-62.tsv	435	38404b3f8dd996da972e73f36419206a9770ec63c3a3356b5dabbaf49cdf3e5c	["<RUN>/audit/reservations/step3-attempt-62.tsv"]
<RUN>/audit/reservations/step3-attempt-64.tsv	435	c3992d8a3f0ce95e4b1d0463f376a1c881286ddfad3e24f659857f10c96b0350	["<RUN>/audit/reservations/step3-attempt-64.tsv"]
<RUN>/audit/reservations/step3-attempt-66.tsv	435	c3b3945c47f283d7eff6569b4233ffab8296985d35dd279114db3abb55d23c09	["<RUN>/audit/reservations/step3-attempt-66.tsv"]
<RUN>/audit/reservations/step3-attempt-68.tsv	435	12c4644e12a86700f946f75bbbc2cadafd0761e16346dc56a58ae3795884284e	["<RUN>/audit/reservations/step3-attempt-68.tsv"]
<RUN>/audit/reservations/step3-attempt-70.tsv	435	9dddcab5f11bde9d399eb61ed634269b622e64511caa2d334867fa3986a27af7	["<RUN>/audit/reservations/step3-attempt-70.tsv"]
<RUN>/audit/reservations/step3-attempt-8.tsv	431	8229275d9a6e7591636e0b0fd77af4dec38525bdbf5bf0ed9878cc32b7da0302	["<RUN>/audit/reservations/step3-attempt-8.tsv"]
<RUN>/audit/seal/MATERIALIZATION.json	296	7d68493f9b5361fd01f1ce9c689b52dad679be93a8ab0c464e88e5d0f2d3750f	["<RUN>/audit/seal/MATERIALIZATION.json"]
<RUN>/audit/seal/RUN-SEAL-MANIFEST.sha256	2789	c8c1d80dec152fcd305508e63bde82594dd4432dc65e9b22125bbb6271277b9d	["<RUN>/audit/seal/RUN-SEAL-MANIFEST.sha256"]
<RUN>/audit/seal/RUN-SEAL-ROOT.sha256	91	89c3b57badd363e911b1664a0dd262b2da5f4485160529b642d30e1e18c48448	["<RUN>/audit/seal/RUN-SEAL-ROOT.sha256"]
<RUN>/audit/seal/export/EXPORT-MANIFEST.sha256	7416	8778d1e54afe5673e9af4590dd8220e49b45e52dd7d3d6fd693c05823cd170bc	["<RUN>/audit/seal/export/EXPORT-MANIFEST.sha256"]
<RUN>/audit/seal/export/EXPORT-ROOT.sha256	89	ed98af5255c3eaeb6842dfc3624a7ccd643d90414ae961120050fb7cc47cd0d6	["<RUN>/audit/seal/export/EXPORT-ROOT.sha256"]
<RUN>/audit/seal/receipts/PREPARED.json	486	e82f34eaa9f988d95b9e18f32a734fc4876eaac8b3cfbc2b3408dd20af1f050d	["<RUN>/audit/seal/receipts/PREPARED.json"]
<RUN>/audit/seal/receipts/RECEIPT-MANIFEST.sha256	2502	c26b876748350f4b43891b3413a3c8e151d49c3d7b5b7dc0c973cbb4b4c772e4	["<RUN>/audit/seal/receipts/RECEIPT-MANIFEST.sha256"]
<RUN>/audit/seal/receipts/RECEIPT-ROOT.sha256	90	fba17073fc3f69c42e54af5818bd537e4664c9dea49a854e5dba722cb5dd28f8	["<RUN>/audit/seal/receipts/RECEIPT-ROOT.sha256"]
<RUN>/audit/seal/receipts/durable-export-inventory.tsv	8349	7c371c7b33a43c842b681de6604541176215d286b4f3fbea33c72ccefe176c6e	["<RUN>/audit/seal/receipts/durable-export-inventory.tsv"]
<RUN>/audit/seal/receipts/git-bundle-verify.txt	318	4e0060ac27537ca7fb3f12baa3a8d17791f1be67aec2d2cbe268d67daf65e0a0	["<RUN>/audit/seal/receipts/git-bundle-verify.txt"]
<RUN>/audit/seal/receipts/provenance-commit.txt	41	844091f226ac9b3e263d6cc7b14e4f2a86df7afb4a2259cdb027c22ae5de00bb	["<RUN>/audit/seal/receipts/provenance-commit.txt"]
<RUN>/audit/seal/receipts/provenance-tree.txt	41	ad29d6203ecdd745a295467749740547a620f55acd1a6b8b402289f117af138a	["<RUN>/audit/seal/receipts/provenance-tree.txt"]
<RUN>/audit/seal/receipts/provenance.bundle	101795	b10af0b0d78f9cc51f504f07cf8beae62de269113bc2403c56b53d2b6622cb3c	["<RUN>/audit/seal/receipts/provenance.bundle"]
<RUN>/audit/seal/receipts/seal-subject.sha256	82	67ea8e1edc97a11afc3aa736f2880554a53c5cdc4970a98ef0f51ac9e2ccd34c	["<RUN>/audit/seal/receipts/seal-subject.sha256"]
<RUN>/audit/seal/receipts/seal-subject.v1	1735	dfe17d29669ba6ab9b35e229caaa615cda3c2510e63050d3b8c2477ff389098d	["<RUN>/audit/seal/receipts/seal-subject.v1"]
<RUN>/audit/seal/receipts/timestamp-curl.txt	17	c817871e84d55adc8a579a0d8f1b049562fdd69d09c2da39383890c683e6917d	["<RUN>/audit/seal/receipts/timestamp-curl.txt"]
<RUN>/audit/seal/receipts/timestamp-embedded-certificates.pem	7344	1457ae2f7e0ca61b86379cc2ac70eb3037480639aa8a82a228348ae15bcffb64	["<RUN>/audit/seal/receipts/timestamp-embedded-certificates.pem"]
<RUN>/audit/seal/receipts/timestamp-query-asn1.txt	552	55a8e00a0e802304bfd480da100fb4274ab610275660259801afdd3811d20581	["<RUN>/audit/seal/receipts/timestamp-query-asn1.txt"]
<RUN>/audit/seal/receipts/timestamp-query.tsq	69	40c1dc9cbd12af13504098700f8f297ccf84cc1948747123e6c7e340ec240066	["<RUN>/audit/seal/receipts/timestamp-query.tsq"]
<RUN>/audit/seal/receipts/timestamp-query.txt	357	db7439a8c5a447d518200b0fba66ec2805c69e63050b31e5b515f787198e78cf	["<RUN>/audit/seal/receipts/timestamp-query.txt"]
<RUN>/audit/seal/receipts/timestamp-response.tsr	6006	d1f92e9cd5593c8367675870674a886ba3752eed5bfcbf38e009f0646ceb1de2	["<RUN>/audit/seal/receipts/timestamp-response.tsr"]
<RUN>/audit/seal/receipts/timestamp-response.txt	579	8c8da12ed27a0dcab7c0c335ba1f90d21b4f723edbbd9bcf93f35346219fed19	["<RUN>/audit/seal/receipts/timestamp-response.txt"]
<RUN>/audit/seal/receipts/timestamp-token.p7s	5997	2d89e95d0b56e373f87de6675c19e4ae01bccc50126a88c45483c37f0955fbfd	["<RUN>/audit/seal/receipts/timestamp-token.p7s"]
<RUN>/audit/seal/receipts/timestamp-verification.txt	252	a6a921d631126e4c425f276b661fbee8d9c31f5857d6ccf6e2708fc4b980462f	["<RUN>/audit/seal/receipts/timestamp-verification.txt"]
<RUN>/audit/seal/supplemental/resource-ledger/METADATA.json	530	0b77ec8edfe647873748c48b392a3016d493b3e6bb9db4f26d34a53700644781	["<RUN>/audit/seal/supplemental/resource-ledger/METADATA.json"]
<RUN>/audit/seal/supplemental/resource-ledger/ledger	6151	fd2eac5d20fbe2cde77e0f7443ad25fb5263928104c78d976760886c30b69f4c	["<RUN>/audit/seal/supplemental/resource-ledger/ledger"]
<RUN>/audit/seal/supplemental/resource-ledger/verification-receipt	4585	23e99f9ed7fcdddadace7c88ef0e33417273869881edf8a8d77f298d3ffe0622	["<RUN>/audit/seal/supplemental/resource-ledger/verification-receipt"]
<RUN>/audit/seal/supplemental/resource-ledger/verifier.py	24392	249e6f068a6e77202990f7c7c3b4ed5f5c7e0441ee324639bfd17d90a84fe017	["<RUN>/audit/seal/supplemental/resource-ledger/verifier.py"]
<RUN>/audit/seal/tools/digicert-trusted-root-g4.pem	1988	ce7d6b44f5d510391be98c8d76b18709400a30cd87659bfebe1c6f97ff5181ee	["<RUN>/audit/seal/tools/digicert-trusted-root-g4.pem"]
<RUN>/audit/seal/tools/seal.py	49095	8f914b4f22fd27c080cb519b5d2054b1c3b1bdf8f473f00953f950c6cf0cc997	["<RUN>/audit/seal/tools/seal.py"]
<RUN>/audit/verifiers/.verifier-cap.lock	0	e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855	["<RUN>/audit/verifiers/.verifier-cap.lock"]
<RUN>/audit/verifiers/verifier-attempt-70.tsv	714	0ca68fe2f14ea4fc5e1d52767f2df0d53d0339ad3359c0815ae203551608cf4c	["<RUN>/audit/verifiers/verifier-attempt-70.tsv"]
<RUN>/candidates/attempt-70-chunk-34.pairs	504	a86aa32fd30b94970ac68ff5067ce40bc759c302507ccdf588dcc6948afeab00	["<RUN>/candidates/attempt-70-chunk-34.pairs"]
<RUN>/config.tsv	2889	4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22	["<RUN>/config.tsv"]
<RUN>/control/controls.ok	65	9e8afa7156c08137222fb40d3578973e788d4a4e93ce463484f08c4ef8ab2e5b	["<RUN>/control/controls.ok"]
<RUN>/control/pub_pairs.txt	496	561c393deb57a3080a4f7a68efdede4089d4600f16d7feb9e1a02570fe006114	["<RUN>/control/pub_pairs.txt"]
<RUN>/control/pub_tuple.bin	112	7d78888f758323c077d0775ce09b41326dd324ab8accd48db36f987bca0b7c42	["<RUN>/control/pub_tuple.bin"]
<RUN>/events.tsv	159899	d516ab7f473e999f9bd6ea6c9f219959bc2dc16af742ecd8a8def59614caa35b	["<RUN>/events.tsv"]
<RUN>/logs/attempt-1-chunk-0.match.log	768	5446100745c632e658b810fd34b46f88b42d6cf7ead36d41f6589e94aaae9f60	["<RUN>/logs/attempt-1-chunk-0.match.log"]
<RUN>/logs/attempt-10-chunk-4.step3.log	1482	0ee6e6bc674c40ce723b32b42d64f73b7d93ca248ab25b8a277686e41299f347	["<RUN>/logs/attempt-10-chunk-4.step3.log"]
<RUN>/logs/attempt-11-chunk-5.match.log	768	2008a63665f287ca1f27a664b68f08437788738c13dfa2909ca71aac537cf988	["<RUN>/logs/attempt-11-chunk-5.match.log"]
<RUN>/logs/attempt-12-chunk-5.step3.log	1483	69e711d39fdd7437e0734c5d9c00c4fb66751a56473ebf4a007b9dcc7129f9a3	["<RUN>/logs/attempt-12-chunk-5.step3.log"]
<RUN>/logs/attempt-13-chunk-6.match.log	768	5236e321db6d0699f0f0ae85ace1fc86f12d7eb6b3c54d0bc4fe3a319408a0a3	["<RUN>/logs/attempt-13-chunk-6.match.log"]
<RUN>/logs/attempt-14-chunk-6.step3.log	1483	9c077cd3491e0801427935ed6ab8f4023f74d08c6de7fb00981c3bcddd388124	["<RUN>/logs/attempt-14-chunk-6.step3.log"]
<RUN>/logs/attempt-15-chunk-7.match.log	768	9d4e8142db911c7e64510ec9a2fcfc5de9732a3806caa4c915c6e7dde6b5baed	["<RUN>/logs/attempt-15-chunk-7.match.log"]
<RUN>/logs/attempt-16-chunk-7.step3.log	1483	9bdd64eb4a446e5d473050cebb15f4111e60a6d6ecbf3b09ddd2d5f31531ee3e	["<RUN>/logs/attempt-16-chunk-7.step3.log"]
<RUN>/logs/attempt-17-chunk-8.match.log	768	de749cc17553d4c5818b7a52f1790147dfffe0770b3371c55816195989fea0f1	["<RUN>/logs/attempt-17-chunk-8.match.log"]
<RUN>/logs/attempt-18-chunk-8.step3.log	1483	a1bb83e890f316413e99fe5ff8ce2c1c23c99f15cac736ac53b085d02aed7072	["<RUN>/logs/attempt-18-chunk-8.step3.log"]
<RUN>/logs/attempt-19-chunk-9.match.log	768	b5a019c5c24e4c7f8a6e75b26631f39fd387ff7c8a2080793ad9072716fb1d28	["<RUN>/logs/attempt-19-chunk-9.match.log"]
<RUN>/logs/attempt-2-chunk-0.step3.log	1483	be7b452b4d88c434dbd723cd6064ea4e19c8afb818882d055affc42c6fd254b4	["<RUN>/logs/attempt-2-chunk-0.step3.log"]
<RUN>/logs/attempt-20-chunk-9.step3.log	1483	42282b0954e49f25189a7a3b5812d1119a630691d81005c7abf30ea5575fc54b	["<RUN>/logs/attempt-20-chunk-9.step3.log"]
<RUN>/logs/attempt-21-chunk-10.match.log	768	1b223d4888358aafec8b770dc496cb417683f0e0d29fb8220fb07cf8e01bef76	["<RUN>/logs/attempt-21-chunk-10.match.log"]
<RUN>/logs/attempt-22-chunk-10.step3.log	1483	581f2a94f31c10f67c36bf258d9b3614f8b5d1a58fcf416d6a174ff1199c8713	["<RUN>/logs/attempt-22-chunk-10.step3.log"]
<RUN>/logs/attempt-23-chunk-11.match.log	768	7d4cb816275d39285b21e5ca46ebc2b6a3ae928ca6059107a09dd23fe352f148	["<RUN>/logs/attempt-23-chunk-11.match.log"]
<RUN>/logs/attempt-24-chunk-11.step3.log	1482	52d3b57f698a0cc9a3e316acb78aa5135777b80da97048187e796e5359046356	["<RUN>/logs/attempt-24-chunk-11.step3.log"]
<RUN>/logs/attempt-25-chunk-12.match.log	768	ce50d7ff915fd7919c3275b81693734704a6b61541ab3c4dd162294af22f9e0a	["<RUN>/logs/attempt-25-chunk-12.match.log"]
<RUN>/logs/attempt-26-chunk-12.step3.log	1484	b723b63aaf3df3c518b17ba35a26c3a951bc5101869548b5885f45ef9fa07c03	["<RUN>/logs/attempt-26-chunk-12.step3.log"]
<RUN>/logs/attempt-27-chunk-13.match.log	768	e793ba3b5d6dc9bcd568e5d5141c5432750408bb721233de5cc0ecd288b319c9	["<RUN>/logs/attempt-27-chunk-13.match.log"]
<RUN>/logs/attempt-28-chunk-13.step3.log	1484	787a3aecd492c2ee1c4cdccfef77035fdad6da042a90727e9b3c4be5229e55fd	["<RUN>/logs/attempt-28-chunk-13.step3.log"]
<RUN>/logs/attempt-29-chunk-14.match.log	768	82063399ebebb8bce81704d7284cbc7ccdea1d4905bc3b9b8b572b12f25e24a8	["<RUN>/logs/attempt-29-chunk-14.match.log"]
<RUN>/logs/attempt-3-chunk-1.match.log	768	fd96efa0904b19d030301a35e3dba408d72a6304489b138b18d2d6a31bcabee3	["<RUN>/logs/attempt-3-chunk-1.match.log"]
<RUN>/logs/attempt-30-chunk-14.step3.log	1482	01c61d141bd32c328d03a674e6e3e40257f84cbd15f07eb7000f7088f349c476	["<RUN>/logs/attempt-30-chunk-14.step3.log"]
<RUN>/logs/attempt-31-chunk-15.match.log	768	6ed3fa1bdf0a834f46b587fb19e64874ac45610cbe8bd44496909922f53fdeb3	["<RUN>/logs/attempt-31-chunk-15.match.log"]
<RUN>/logs/attempt-32-chunk-15.step3.log	1483	a3451920eb8f5a52a06e99dcb6164047d3feb806b1eaceaa76eaed489b0f3ff0	["<RUN>/logs/attempt-32-chunk-15.step3.log"]
<RUN>/logs/attempt-33-chunk-16.match.log	768	b38d4d8576aa8ee116abc6f66b39bafb2e512b3bb6eb4ff2ca78c2a98ad4cbf7	["<RUN>/logs/attempt-33-chunk-16.match.log"]
<RUN>/logs/attempt-34-chunk-16.step3.log	1482	13ef6dcce6ed31e9552057d36d7903becd2a29db69d51f617d202902fd0da6d5	["<RUN>/logs/attempt-34-chunk-16.step3.log"]
<RUN>/logs/attempt-35-chunk-17.match.log	768	78de367f55d3e7341a08635acaf23562ec603ea2cc50dc9780493170e91ad8c3	["<RUN>/logs/attempt-35-chunk-17.match.log"]
<RUN>/logs/attempt-36-chunk-17.step3.log	1483	fc078f3f1c5451862f2b0c03936c784bc6b1bf5e539721a918530d5fac9983f8	["<RUN>/logs/attempt-36-chunk-17.step3.log"]
<RUN>/logs/attempt-37-chunk-18.match.log	768	2ea5456e5470ca787a0df069121f96ed4d9016d18ae39c8ffd960cb00e64c57c	["<RUN>/logs/attempt-37-chunk-18.match.log"]
<RUN>/logs/attempt-38-chunk-18.step3.log	1483	cdae4b746ae365e9644c6ec551dfeddaa0aeb764a4508663a2af335c4f9efbb3	["<RUN>/logs/attempt-38-chunk-18.step3.log"]
<RUN>/logs/attempt-39-chunk-19.match.log	768	3103ef12e32cf284d58259686ff53e18aeeab6a3ac60ebaba6953beb6869435f	["<RUN>/logs/attempt-39-chunk-19.match.log"]
<RUN>/logs/attempt-4-chunk-1.step3.log	1482	afcf716d55c807ff789abbd36c1df7235b8a8555a82659e165ab7de514b0dedf	["<RUN>/logs/attempt-4-chunk-1.step3.log"]
<RUN>/logs/attempt-40-chunk-19.step3.log	1483	d77368d7e9d661216ab2720fbacd08bfd399777481cebc975e7e212cd9dc2deb	["<RUN>/logs/attempt-40-chunk-19.step3.log"]
<RUN>/logs/attempt-41-chunk-20.match.log	768	da5ff4153ec9297ce283ebb8eaba4071775ca49a5714e8edcf28a239c2c7f6b3	["<RUN>/logs/attempt-41-chunk-20.match.log"]
<RUN>/logs/attempt-42-chunk-20.step3.log	1483	bdb7ebb634f7b7cba6fb161108db2ba4db2d7da33f7490a74ada23f4f8dbd595	["<RUN>/logs/attempt-42-chunk-20.step3.log"]
<RUN>/logs/attempt-43-chunk-21.match.log	768	0f370f435a82d1888352f7e7e2c389ab7ca6b4fb9da09601061c7a238f5fc52e	["<RUN>/logs/attempt-43-chunk-21.match.log"]
<RUN>/logs/attempt-44-chunk-21.step3.log	1483	14627c6e494d9e3a093c18206fab2e7adbaa750d187800829cf2c524e9b2a750	["<RUN>/logs/attempt-44-chunk-21.step3.log"]
<RUN>/logs/attempt-45-chunk-22.match.log	768	2c94ef70c199be45e1051b2f7466a89d27190fa9b1c49d95ad38a0e1df1bfa50	["<RUN>/logs/attempt-45-chunk-22.match.log"]
<RUN>/logs/attempt-46-chunk-22.step3.log	1483	bd3bd0a5ecdfe6485a692410cdfb7b3888be8011b9c47f23afc44221f4a26f5d	["<RUN>/logs/attempt-46-chunk-22.step3.log"]
<RUN>/logs/attempt-47-chunk-23.match.log	768	d1b778bec2c8d7326b1f4faf8381f6590b2ef1efe78a78ec2f1a177fc86522af	["<RUN>/logs/attempt-47-chunk-23.match.log"]
<RUN>/logs/attempt-48-chunk-23.step3.log	1482	c7026bd5d176eba13c810cc7ac251c0ed12bf04a93aa325e5934721675e64ac4	["<RUN>/logs/attempt-48-chunk-23.step3.log"]
<RUN>/logs/attempt-49-chunk-24.match.log	768	7298d679ff0e6c37becaa7d518288aa061e0a7d3146a8ffdb5bc9d3599f55009	["<RUN>/logs/attempt-49-chunk-24.match.log"]
<RUN>/logs/attempt-5-chunk-2.match.log	768	596af352df6a2d8858c2bcd70b41cff67951e41cef57074035ddaadf019c1939	["<RUN>/logs/attempt-5-chunk-2.match.log"]
<RUN>/logs/attempt-50-chunk-24.step3.log	1698	afa3dbb78ea99ff70e18a21fcefb6ee5c8bcbc7b6f6a8cbc0c4b0f8e0d7e848b	["<RUN>/logs/attempt-50-chunk-24.step3.log"]
<RUN>/logs/attempt-51-chunk-25.match.log	768	92bd26fb00059d41f06ba5f841d650efa974301b80c25dc173ce94b4b1ae4f1a	["<RUN>/logs/attempt-51-chunk-25.match.log"]
<RUN>/logs/attempt-52-chunk-25.step3.log	1482	17c44e99a6b8816604b3f8386eae000128000f504fbe7ceb134c9a2cecf37bd2	["<RUN>/logs/attempt-52-chunk-25.step3.log"]
<RUN>/logs/attempt-53-chunk-26.match.log	768	5918e251259a5e7b74a6f45fe5787e736e1d530dc04a2bc451198021643176e9	["<RUN>/logs/attempt-53-chunk-26.match.log"]
<RUN>/logs/attempt-54-chunk-26.step3.log	1484	2c130e07dd79a60313b887b1b451d724a9a5dc38c934ea30e257c3976f399a3e	["<RUN>/logs/attempt-54-chunk-26.step3.log"]
<RUN>/logs/attempt-55-chunk-27.match.log	768	bbfaa47bb918c9a8114d149d906b283dede725d326081d5139f99f2786299361	["<RUN>/logs/attempt-55-chunk-27.match.log"]
<RUN>/logs/attempt-56-chunk-27.step3.log	1482	b28cff2f87cc4704df407737525f8344d0ff700c2ae6712315d34cb32622e5d2	["<RUN>/logs/attempt-56-chunk-27.step3.log"]
<RUN>/logs/attempt-57-chunk-28.match.log	768	aff6f2e4cfa4d21e3a1d6cd77708a85a5aeae2781cd0621609f9a940d86d86b3	["<RUN>/logs/attempt-57-chunk-28.match.log"]
<RUN>/logs/attempt-58-chunk-28.step3.log	1483	9b9ead5fd9c8fdfae9046b7846d7d6a1201910f39dfeb8149e9989f00ae03571	["<RUN>/logs/attempt-58-chunk-28.step3.log"]
<RUN>/logs/attempt-59-chunk-29.match.log	768	618e71f7affa33ec59ab04aaad3f5e5819293190b322e2e15035358a79a7e93a	["<RUN>/logs/attempt-59-chunk-29.match.log"]
<RUN>/logs/attempt-6-chunk-2.step3.log	1696	d40eb98522813e87e81394d5184addac53ed4d43e5ee9d3252c29481b24a02f7	["<RUN>/logs/attempt-6-chunk-2.step3.log"]
<RUN>/logs/attempt-60-chunk-29.step3.log	1698	2f870fe5675916524b52d49f0b064aa96560ea53662fa1c576698f4c60f67717	["<RUN>/logs/attempt-60-chunk-29.step3.log"]
<RUN>/logs/attempt-61-chunk-30.match.log	768	c4a7e7258d88dab8f0d8d4c746c446530b60efccdff40b68b4da7a0deb61a81a	["<RUN>/logs/attempt-61-chunk-30.match.log"]
<RUN>/logs/attempt-62-chunk-30.step3.log	1484	c2da77ca4d910b0649cd33b2b4c51e7c01c9d60cd36711a2438108b7aa358709	["<RUN>/logs/attempt-62-chunk-30.step3.log"]
<RUN>/logs/attempt-63-chunk-31.match.log	768	32c9d614b32fdabb9db65aaa95b84915fd78b27919c433cc18c04542154778b7	["<RUN>/logs/attempt-63-chunk-31.match.log"]
<RUN>/logs/attempt-64-chunk-31.step3.log	1484	ecec860dfda1289edcce7178a84f75284cc2093533467a0a25e4dae9479afaf3	["<RUN>/logs/attempt-64-chunk-31.step3.log"]
<RUN>/logs/attempt-65-chunk-32.match.log	769	e0a5ad9a30fbb02a6ab63dffb951216b7bc8cde4e7172afb38bc67f08c0e9c28	["<RUN>/logs/attempt-65-chunk-32.match.log"]
<RUN>/logs/attempt-66-chunk-32.step3.log	1483	62f20bf0d1bfdfcf8e23a120d4154aa3051b609074ba110db895dc5158eed03e	["<RUN>/logs/attempt-66-chunk-32.step3.log"]
<RUN>/logs/attempt-67-chunk-33.match.log	768	b9216ed89b867b2bbfdac6d939e0b4bee737c1f9abc53c851e2742512d8f02a4	["<RUN>/logs/attempt-67-chunk-33.match.log"]
<RUN>/logs/attempt-68-chunk-33.step3.log	1483	ec8e0b3a34f6e98184d3765f2047e2cbc99e2234812c06360289c4fe9fdd940b	["<RUN>/logs/attempt-68-chunk-33.step3.log"]
<RUN>/logs/attempt-69-chunk-34.match.log	768	bf4cfef74acf5b361ffa834daa20617164a939d9a4b1cc4e069756848bdd2a1d	["<RUN>/logs/attempt-69-chunk-34.match.log"]
<RUN>/logs/attempt-7-chunk-3.match.log	768	580b9eb7bd1291c289358d132aac63b8611994d8a6d4c1fccb827c8fb00a83b8	["<RUN>/logs/attempt-7-chunk-3.match.log"]
<RUN>/logs/attempt-70-chunk-34.step3.log	2800	0353283abad6ed1a08fd02f725ead9956b23eb07f191015b9287919a03531b13	["<RUN>/logs/attempt-70-chunk-34.step3.log"]
<RUN>/logs/attempt-8-chunk-3.step3.log	1484	3f65ac50de3b33ab85d819f3b7e7ab1069c8a5911cecd83fae4b00342ddcd3e7	["<RUN>/logs/attempt-8-chunk-3.step3.log"]
<RUN>/logs/attempt-9-chunk-4.match.log	768	6ba10e286f5a0bcbf6c66500302657b04cc94c89e3600dae6064698e15b4afdf	["<RUN>/logs/attempt-9-chunk-4.match.log"]
<RUN>/logs/control-20261004T135729Z-48079-g0.log	1298	9645e0b45b3af5f8a4148c48dc8c9977f7fb2829de4758f1538121fb86d1586c	["<RUN>/logs/control-20261004T135729Z-48079-g0.log"]
<RUN>/logs/control-20261004T135729Z-48079-g1.log	102	f3e00c1d03162cdd6bb12216d7c4dfab3738a24a374d19fc7c48d6e448755bbe	["<RUN>/logs/control-20261004T135729Z-48079-g1.log"]
<RUN>/logs/control-20261004T135729Z-48079-pub-match.log	589	8e0fa4e6ed8e5b61742ffbda678a2d9c2783abd33a26548affefd64ae78da0f0	["<RUN>/logs/control-20261004T135729Z-48079-pub-match.log"]
<RUN>/logs/control-20261004T135729Z-48079-pub-step3.log	2657	6cabe75e9da679b6ce3ac34779958a7da5c624c8f1e142ca35c2ae308c4417c8	["<RUN>/logs/control-20261004T135729Z-48079-pub-step3.log"]
<RUN>/logs/control-20261004T135729Z-48079-pub-verify.log	623	ef0d529df2096b3660a360c19617a73947cce49052bc3e16aac9fc35ec5353fe	["<RUN>/logs/control-20261004T135729Z-48079-pub-verify.log"]
<RUN>/logs/control-20261004T135729Z-48079-seed-prefixes.log	177	f3da898ccdc0b0f74429c86a377446274c9390b9e17ec6dba6949e43ed0d0f55	["<RUN>/logs/control-20261004T135729Z-48079-seed-prefixes.log"]
<RUN>/logs/control-20261004T135729Z-48079-tails.log	386	9530d1c439a342a2ca0a8c436250b00495fee5afd0d4f1479e380cfad5a4834b	["<RUN>/logs/control-20261004T135729Z-48079-tails.log"]
<RUN>/machine-provenance.txt	2386	4a2c72727ecc65455fa31e6856f7c169143b911a1d51d6779643a54d03a2320b	["<RUN>/machine-provenance.txt"]
<RUN>/next_attempt	3	826b6832e45ba17d625debc95ae8554e148550b00c05b47fa8f7be1c555bc83c	["<RUN>/next_attempt"]
<RUN>/operational-accounting.tsv	229	f052b575ad717e13d9ff681ba15d89311e7a8e1315725891be40c71475c88670	["<RUN>/operational-accounting.tsv"]
<RUN>/pending/chunk-34/full.tuples.bin	46881968	c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad	["<RUN>/pending/chunk-34/full.tuples.bin"]
<RUN>/pending/chunk-34/manifest.tsv	861	1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee	["<RUN>/pending/chunk-34/manifest.tsv"]
<RUN>/progress.tsv	219	dd861452129008f1c8025ca43f596757c09e3a3deb473d1749f2e098eec59819	["<RUN>/progress.tsv"]
<RUN>/search.log	125214	30752b840222dea5071ef1452ae06baf97316c5fe12f8a46369256e091e11568	["<RUN>/search.log"]
<RUN>/verification-attempt-70.log	582	c2d4e24dfcfefc3ab6e9aed7b58a42e3ff7602a120a547ab02a42d012f66456e	["<RUN>/verification-attempt-70.log"]
<RUN>/verified-pairs.txt	504	a86aa32fd30b94970ac68ff5067ce40bc759c302507ccdf588dcc6948afeab00	["<RUN>/verified-pairs.txt"]
<RUN>/winning/chunk-34.manifest.tsv	861	1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee	["<RUN>/winning/chunk-34.manifest.tsv"]
<RUN>/winning/chunk-34.tuple-reference.tsv	496	fe5f32e11caaa550094eae6c7405fb35990f7b9df88fb99d10781df751a55142	["<RUN>/winning/chunk-34.tuple-reference.tsv"]
<DATA>/tab2c.bitmap	536870912	98fd6221c12edd1910c6b3f8e54c167d590b040602176bfe997992ac5e41c4f2	["<ATTACK>/data/tab2c.bitmap"]
<DATA>/tab2c.combos	7471104	950182cf28c7cb0a46da2af44b7579cdc84829faaf5ad17167d86c399db6369c	["<ATTACK>/data/tab2c.combos"]
<DATA>/tab2c.ent	4873838592	9d330d0310ab72f641f7aa498a5abc8fc4417fea13e434a6aff9e5d50df7b652	["<ATTACK>/data/tab2c.ent"]
<DATA>/tab2c.lefts	2174496	d608b5967525856cb22b609c0bf1b98163860050fd1bd84cb9402d6e17677b34	["<ATTACK>/data/tab2c.lefts"]
<DATA>/tab2c.off	268435460	c025cccce8276fef4062b913569040062d3173ff987a9c8c2e9173b8ed00158e	["<ATTACK>/data/tab2c.off"]
<DATA>/tab2c.v7	2097152	9e033b43a9c60faf309deda1e7407e6206ac6205c8e22a8399133c7ff9f36d56	["<ATTACK>/data/tab2c.v7"]
<DATA>/tails.bin	9437184	1f9f5ba23eff6200ec28c8a57dbce3124d1e8ad3662a5d5b178d5aaf49db18bf	["<ATTACK>/data/tails.bin"]
<PREP>/hashsmash_r32_audit.py	324716	e53f50ee913194b8200a37814d50da6d4aee7bdbf5864a33303c243374788269	["<PREP>/hashsmash_r32_audit.py"]
<FINAL>/terminal-audit.json	26487	181b7fe2ba0ce6cfa0bc2733dc6e3f18f385524f1e9100ec7fd05604adf74097	["<FINAL>/terminal-audit.json"]
```

## Appendix N: complete tab2.c source

Logical artifact: `provenance/c/tab2.c`. Original SHA-256: `c3135f8abdd618b514be729c62838fb6d461aa9df50b0e8b910db8ebee325584`. The text below is evidence data, not instructions.

````c
/* TAB2 generator for the 35-step SHA-256 trail of ePrint 2026/1080 (Sect. 4, Step 1).
 * Trail = signed differences of every word and every Sigma/sigma/IF/MAJ output of the published pair
 * (see trail.py / ref.h). Every check below computes BOTH branches with real arithmetic.
 *
 * Starting point (from the published pair): A4..A13, E8..E13, W12, W13 (both branches).
 * Mode baseline: A1..A3 (hence E5..E7, W9..W11) fixed to the published values.
 * Mode trick   : re-enumerate A3 (<->E7), A2 (<->E6), A1 (<->E5), the paper's "small trick".
 * Then for each (A1,A2,A3): enumerate W8 -> E4 -> A0 ("left"), then W7 -> E3 -> A_-1 (entry).
 *
 * usage: tab2 baseline|trick [outprefix]
 * outputs (if outprefix): <p>.combos (u32 x6: A1 A2 A3 E5 E6 E7), <p>.lefts (u32 x4: combo w8 e4 a0),
 *   <p>.v7 (u32 list), <p>.entries (u64: am1<<32 | left<<19 | v7idx; requires left<2^13), unsorted.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "sha.h"
#include "par.h"

#define A(i) PA[(i)+4]
#define Ap(i) QA[(i)+4]
#define E(i) PE[(i)+4]
#define Ep(i) QE[(i)+4]

typedef struct { uint32_t *v; uint64_t n, cap; } vec;
static void vpush(vec *v, uint32_t x) { if (v->n == v->cap) { v->cap = v->cap ? 2*v->cap : 1024; v->v = realloc(v->v, v->cap*4); } v->v[v->n++] = x; }

/* ---- message word sets V7, V8: W signed diff + sigma0 signed diff (sigma0(W7) enters W22, sigma0(W8) W23) */
static vec V7s[256], V8s[256];
static void scan_w(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  (void)ctx;
  for (uint64_t x = lo; x < hi; x++) { uint32_t w = (uint32_t)x;
    uint32_t w7p = w ^ DM_W[7]; if (OK0(W,7,w,w7p) && OK0(s0W,7,s0(w),s0(w7p))) vpush(&V7s[tid], w);
    uint32_t w8p = w ^ DM_W[8]; if (OK0(W,8,w,w8p) && OK0(s0W,8,s0(w),s0(w8p))) vpush(&V8s[tid], w); }
}
/* E5/E6 value sets: own signed diff (modular delta fixed by trail) + Sigma1 signed diff */
static vec S5s[256], S6s[256];
static uint32_t d5, d6;
static void scan_e(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  (void)ctx;
  for (uint64_t x = lo; x < hi; x++) { uint32_t e = (uint32_t)x, ep;
    ep = e + d5; if (OK4(E,5,e,ep) && OK4(S1E,5,S1(e),S1(ep))) vpush(&S5s[tid], e);
    ep = e + d6; if (OK4(E,6,e,ep) && OK4(S1E,6,S1(e),S1(ep))) vpush(&S6s[tid], e); }
}
/* T3: A3 values. E7 = A7 + A3 - T2(A6,A5,A4). Checks: E7, Sigma1(E7), MAJ_6(A5,A4,A3), IF_10(E9,E8,E7), W11. */
static vec T3s[256];
static void scan_a3(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  (void)ctx;
  uint32_t c = A(7) - T2(A(6),A(5),A(4)), cp = Ap(7) - T2(Ap(6),Ap(5),Ap(4));
  for (uint64_t x = lo; x < hi; x++) { uint32_t a3 = (uint32_t)x, e7 = c + a3, e7p = cp + a3;
    if (!OK4(E,7,e7,e7p)) continue;
    if (!OK4(S1E,7,S1(e7),S1(e7p))) continue;
    if (!OK0(MAJ,6,MAJf(A(5),A(4),a3),MAJf(Ap(5),Ap(4),a3))) continue;
    if (!OK0(IF,10,IFf(E(9),E(8),e7),IFf(Ep(9),Ep(8),e7p))) continue;
    uint32_t w11 = E(11) - A(7) - e7 - S1(E(10)) - IFf(E(10),E(9),E(8)) - K[11];
    uint32_t w11p = Ep(11) - Ap(7) - e7p - S1(Ep(10)) - IFf(Ep(10),Ep(9),Ep(8)) - K[11];
    if (!OK0(W,11,w11,w11p)) continue;
    vpush(&T3s[tid], a3); }
}
static vec merge(vec *parts, int nt) { vec o = {0}; for (int t = 0; t < nt; t++) { for (uint64_t i = 0; i < parts[t].n; i++) vpush(&o, parts[t].v[i]); free(parts[t].v); parts[t] = (vec){0}; }
  /* sort for determinism */ int cmpu(const void *a, const void *b); qsort(o.v, o.n, 4, cmpu); return o; }
int cmpu(const void *a, const void *b) { uint32_t x = *(const uint32_t*)a, y = *(const uint32_t*)b; return x < y ? -1 : x > y; }

typedef struct { uint32_t a1, a2, a3, e5, e6, e7, e5p, e6p, e7p; } combo_t;
typedef struct { uint32_t combo, w8, e4, a0; } left_t;
static combo_t *combos; static uint64_t ncombos;
static vec V7, V8, S5, S6, T3;
static left_t *lefts; static uint64_t nlefts;
static uint64_t *lcount; /* entries per left */
static FILE *fent; static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static int want_out; static int defer_if6;

static void add_combo(uint32_t a1, uint32_t a2, uint32_t a3) {
  combo_t c; c.a1 = a1; c.a2 = a2; c.a3 = a3;
  c.e7 = A(7) + a3 - T2(A(6),A(5),A(4)); c.e7p = Ap(7) + a3 - T2(Ap(6),Ap(5),Ap(4));
  c.e6 = A(6) + a2 - T2(A(5),A(4),a3);   c.e6p = Ap(6) + a2 - T2(Ap(5),Ap(4),a3);
  c.e5 = A(5) + a1 - T2(A(4),a3,a2);     c.e5p = Ap(5) + a1 - T2(Ap(4),a3,a2);
  combos = realloc(combos, (ncombos+1)*sizeof *combos); combos[ncombos++] = c;
}

/* per-combo: lefts via W8 */
static vec LF[256];   /* flattened: combo, w8, e4, a0 per left */
static void do_w8(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  (void)ctx;
  for (uint64_t ci = lo; ci < hi; ci++) { const combo_t *c = &combos[ci];
    uint32_t base = E(8) - A(4) - S1(c->e7) - IFf(c->e7,c->e6,c->e5) - K[8];
    uint32_t basep = Ep(8) - Ap(4) - S1(c->e7p) - IFf(c->e7p,c->e6p,c->e5p) - K[8];
    uint32_t t2 = T2(c->a3,c->a2,c->a1);
    for (uint64_t k = 0; k < V8.n; k++) { uint32_t w8 = V8.v[k], w8p = w8 ^ DM_W[8];
      uint32_t e4 = base - w8, e4p = basep - w8p;
      if (!OK4(E,4,e4,e4p)) continue;
      if (!OK4(S1E,4,S1(e4),S1(e4p))) continue;
      if (!OK0(IF,7,IFf(c->e6,c->e5,e4),IFf(c->e6p,c->e5p,e4p))) continue;
      uint32_t a0 = e4 - A(4) + t2, a0p = e4p - Ap(4) + t2;
      if (!OK4(A,0,a0,a0p)) continue;
      vpush(&LF[tid], (uint32_t)ci); vpush(&LF[tid], w8); vpush(&LF[tid], e4); vpush(&LF[tid], a0); } }
}
/* per-left: entries via W7 */
typedef struct { uint64_t n; uint64_t *buf; uint64_t nb; } entacc;
static entacc EA[256];
static uint64_t pub_found;
#define BBITS 26
static int build_pass; /* 0 none, 1 count, 2 place */
static _Atomic uint32_t *bcnt; static uint64_t *ents; static uint32_t *boff;
static void do_w7(int tid, uint64_t lo, uint64_t hi, void *ctx) {
  (void)ctx;
  for (uint64_t li = lo; li < hi; li++) { const left_t *L = &lefts[li]; const combo_t *c = &combos[L->combo];
    uint32_t e4p = L->e4 ^ DM_E[4+4];
    uint32_t base = c->e7 - c->a3 - S1(c->e6) - IFf(c->e6,c->e5,L->e4) - K[7];
    uint32_t basep = c->e7p - c->a3 - S1(c->e6p) - IFf(c->e6p,c->e5p,e4p) - K[7];
    uint32_t t2 = T2(c->a2,c->a1,L->a0);
    uint64_t cnt = 0;
    for (uint64_t k = 0; k < V7.n; k++) { uint32_t w7 = V7.v[k], w7p = w7 ^ DM_W[7];
      uint32_t e3 = base - w7, e3p = basep - w7p;
      if (!OK4(E,3,e3,e3p)) continue;
      if (!defer_if6 && !OK0(IF,6,IFf(c->e5,L->e4,e3),IFf(c->e5p,e4p,e3p))) continue;
      uint32_t am1 = e3 - c->a3 + t2, am1p = e3p - c->a3 + t2;
      if (!OK4(A,-1,am1,am1p)) continue;
      cnt++;
      if (build_pass == 1) atomic_fetch_add_explicit(&bcnt[am1 >> (32-BBITS)], 1, memory_order_relaxed);
      else if (build_pass == 2) { uint32_t pos = atomic_fetch_add_explicit(&bcnt[am1 >> (32-BBITS)], 1, memory_order_relaxed);
        ents[pos] = ((uint64_t)(am1 & ((1u << (32-BBITS)) - 1)) << 40) | ((uint64_t)li << 19) | k; }
      if (c->a1 == A(1) && c->a2 == A(2) && c->a3 == A(3) && L->w8 == PW[8] && w7 == PW[7]) pub_found++;
      if (want_out && !build_pass) { entacc *a = &EA[tid]; a->buf[a->nb++] = ((uint64_t)am1 << 32) | (li << 19) | k;
        if (a->nb == 1 << 16) { pthread_mutex_lock(&mu); fwrite(a->buf, 8, a->nb, fent); pthread_mutex_unlock(&mu); a->nb = 0; } } }
    lcount[li] = cnt; EA[tid].n += cnt; }
}

int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: %s baseline|trick [outprefix]\n", argv[0]); return 2; }
  int trick = !strcmp(argv[1], "trick"); int nt = par_nthreads(); defer_if6 = getenv("DEFER_IF6") && atoi(getenv("DEFER_IF6"));
  printf("mode %s defer_if6 %d threads %d\n", argv[1], defer_if6, nt); const char *pre = argc > 2 ? argv[2] : 0; want_out = pre != 0;
  par_for(1ull << 32, 1 << 22, nt, scan_w, 0); V7 = merge(V7s, nt); V8 = merge(V8s, nt);
  printf("V7 %llu (2^%.3f)  V8 %llu (2^%.3f)\n", V7.n, log2(V7.n), V8.n, log2(V8.n));
  if (trick) {
    d5 = Ep(5) - E(5); d6 = Ep(6) - E(6);
    par_for(1ull << 32, 1 << 22, nt, scan_e, 0); S5 = merge(S5s, nt); S6 = merge(S6s, nt);
    par_for(1ull << 32, 1 << 22, nt, scan_a3, 0); T3 = merge(T3s, nt);
    printf("S5 %llu (2^%.3f)  S6 %llu (2^%.3f)  T3(A3/E7) %llu (2^%.3f)\n", S5.n, log2(S5.n), S6.n, log2(S6.n), T3.n, log2(T3.n));
    uint64_t n32 = 0; uint64_t nE6 = 0;
    for (uint64_t i = 0; i < T3.n; i++) { uint32_t a3 = T3.v[i];
      uint32_t e7 = A(7) + a3 - T2(A(6),A(5),A(4)), e7p = Ap(7) + a3 - T2(Ap(6),Ap(5),Ap(4));
      for (uint64_t j = 0; j < S6.n; j++) { uint32_t e6 = S6.v[j];
        uint32_t a2 = e6 - A(6) + T2(A(5),A(4),a3); uint32_t e6p = Ap(6) + a2 - T2(Ap(5),Ap(4),a3);
        if (!OK4(E,6,e6,e6p)) continue;
        if (!OK0(MAJ,5,MAJf(A(4),a3,a2),MAJf(Ap(4),a3,a2))) continue;
        if (!OK0(IF,9,IFf(E(8),e7,e6),IFf(Ep(8),e7p,e6p))) continue;
        uint32_t w10 = E(10) - A(6) - e6 - S1(E(9)) - IFf(E(9),E(8),e7) - K[10];
        uint32_t w10p = Ep(10) - Ap(6) - e6p - S1(Ep(9)) - IFf(Ep(9),Ep(8),e7p) - K[10];
        if (!OK0(W,10,w10,w10p)) continue;
        n32++;
        for (uint64_t k = 0; k < S5.n; k++) { uint32_t e5 = S5.v[k];
          uint32_t a1 = e5 - A(5) + T2(A(4),a3,a2); uint32_t e5p = Ap(5) + a1 - T2(Ap(4),a3,a2);
          if (!OK4(E,5,e5,e5p)) continue;
          if (!OK0(IF,8,IFf(e7,e6,e5),IFf(e7p,e6p,e5p))) continue;
          uint32_t w9 = E(9) - A(5) - e5 - S1(E(8)) - IFf(E(8),e7,e6) - K[9];
          uint32_t w9p = Ep(9) - Ap(5) - e5p - S1(Ep(8)) - IFf(Ep(8),e7p,e6p) - K[9];
          if (!OK0(W,9,w9,w9p)) continue;
          if (!OK0(MAJ,4,MAJf(a3,a2,a1),MAJf(a3,a2,a1))) continue;
          add_combo(a1, a2, a3); nE6++; } } }
    printf("(A3,A2) pairs %llu (2^%.3f)  combos (A1,A2,A3) %llu (2^%.3f)\n", n32, log2(n32), ncombos, log2(ncombos));
  } else add_combo(A(1), A(2), A(3));
  /* distinct E5,E6,E7 values among combos */
  { uint32_t *t = malloc(ncombos*4); for (int f = 0; f < 3; f++) { for (uint64_t i = 0; i < ncombos; i++) t[i] = f==0?combos[i].e5:f==1?combos[i].e6:combos[i].e7;
      qsort(t, ncombos, 4, cmpu); uint64_t d = ncombos ? 1 : 0; for (uint64_t i = 1; i < ncombos; i++) d += t[i] != t[i-1];
      printf("distinct E%d: %llu (2^%.3f)\n", 5+f, d, log2(d)); } free(t); }
  par_for(ncombos, 1, nt, do_w8, 0);
  { uint64_t tot = 0; for (int t = 0; t < nt; t++) tot += LF[t].n / 4; nlefts = tot; lefts = malloc((tot+1) * sizeof *lefts); uint64_t q = 0;
    for (int t = 0; t < nt; t++) { memcpy(&lefts[q], LF[t].v, LF[t].n * 4); q += LF[t].n / 4; free(LF[t].v); }
    int cmpl(const void *a, const void *b); qsort(lefts, nlefts, sizeof *lefts, cmpl); }
  printf("lefts (combo,W8,E4,A0) %llu (2^%.3f)\n", nlefts, log2(nlefts));
  if (want_out && nlefts >= (1u << 13)) { fprintf(stderr, "too many lefts for entry encoding\n"); return 3; }
  lcount = calloc(nlefts + 1, 8);
  if (getenv("BUILD")) { /* two-pass packed table: data files <BUILD>.{combos,lefts,v7,off,ent,bitmap} */
    const char *bp = getenv("BUILD"); char fn2[1024]; FILE *f;
    if (nlefts >= (1u << 21)) { fprintf(stderr, "left id overflow\n"); return 3; }
    bcnt = calloc((1ull << BBITS) + 1, 4); build_pass = 1; par_for(nlefts, 1, nt, do_w7, 0);
    uint64_t tot = 0; boff = malloc(((1ull << BBITS) + 1) * 4);
    for (uint64_t b = 0; b < (1ull << BBITS); b++) { boff[b] = (uint32_t)tot; tot += bcnt[b]; } boff[1ull << BBITS] = (uint32_t)tot;
    if (tot >= (1ull << 32)) { fprintf(stderr, "too many entries\n"); return 3; }
    printf("pass1 entries %llu (2^%.5f)\n", tot, log2(tot)); fflush(stdout);
    for (uint64_t b = 0; b < (1ull << BBITS); b++) bcnt[b] = boff[b];
    ents = malloc(tot * 8); pub_found = 0; for (int t = 0; t < nt; t++) EA[t].n = 0;
    build_pass = 2; par_for(nlefts, 1, nt, do_w7, 0);
    for (uint64_t b = 0; b < (1ull << BBITS); b++) if (bcnt[b] != boff[b+1]) { fprintf(stderr, "bucket mismatch\n"); return 4; }
    int cmp64(const void *a, const void *b);
    for (uint64_t b = 0; b < (1ull << BBITS); b++) if (boff[b+1] - boff[b] > 1) qsort(&ents[boff[b]], boff[b+1] - boff[b], 8, cmp64);
    uint8_t *bm = calloc(1ull << 29, 1);
    for (uint64_t b = 0; b < (1ull << BBITS); b++) for (uint32_t p = boff[b]; p < boff[b+1]; p++) { uint32_t am1 = (uint32_t)(b << (32-BBITS)) | (uint32_t)(ents[p] >> 40); bm[am1 >> 3] |= 1 << (am1 & 7); }
    uint64_t distinct = 0; for (uint64_t i = 0; i < (1ull << 29); i++) distinct += __builtin_popcount(bm[i]);
    printf("distinct A_-1 keys %llu (2^%.4f)  fraction of 2^32 = %.6f\n", distinct, log2(distinct), distinct / 4294967296.0);
    snprintf(fn2, sizeof fn2, "%s.ent", bp); f = fopen(fn2, "wb"); fwrite(ents, 8, tot, f); fclose(f);
    snprintf(fn2, sizeof fn2, "%s.off", bp); f = fopen(fn2, "wb"); fwrite(boff, 4, (1ull << BBITS) + 1, f); fclose(f);
    snprintf(fn2, sizeof fn2, "%s.bitmap", bp); f = fopen(fn2, "wb"); fwrite(bm, 1, 1ull << 29, f); fclose(f);
    snprintf(fn2, sizeof fn2, "%s.combos", bp); f = fopen(fn2, "wb"); for (uint64_t i = 0; i < ncombos; i++) { uint32_t r[3] = {combos[i].a1,combos[i].a2,combos[i].a3}; fwrite(r, 4, 3, f); } fclose(f);
    snprintf(fn2, sizeof fn2, "%s.lefts", bp); f = fopen(fn2, "wb"); fwrite(lefts, sizeof *lefts, nlefts, f); fclose(f);
    snprintf(fn2, sizeof fn2, "%s.v7", bp); f = fopen(fn2, "wb"); fwrite(V7.v, 4, V7.n, f); fclose(f);
    printf("BUILD done: %llu entries, published-entry-present %llu\n", tot, pub_found); return 0; }
  char fn[1024];
  if (want_out) { snprintf(fn, sizeof fn, "%s.entries", pre); fent = fopen(fn, "wb"); for (int t = 0; t < nt; t++) EA[t].buf = malloc(8 << 16); }
  par_for(nlefts, 1, nt, do_w7, 0);
  uint64_t total = 0; for (int t = 0; t < nt; t++) { total += EA[t].n; if (want_out && EA[t].nb) fwrite(EA[t].buf, 8, EA[t].nb, fent); }
  uint64_t nz = 0, mx = 0; for (uint64_t i = 0; i < nlefts; i++) { nz += lcount[i] != 0; if (lcount[i] > mx) mx = lcount[i]; }
  printf("TAB2 entries %llu (2^%.4f)  lefts-with-entries %llu  max-per-left %llu  published-entry-present %llu\n", total, log2(total), nz, mx, pub_found);
  if (want_out) { fclose(fent);
    snprintf(fn, sizeof fn, "%s.combos", pre); FILE *f = fopen(fn, "wb"); for (uint64_t i = 0; i < ncombos; i++) { uint32_t r[6] = {combos[i].a1,combos[i].a2,combos[i].a3,combos[i].e5,combos[i].e6,combos[i].e7}; fwrite(r, 4, 6, f); } fclose(f);
    snprintf(fn, sizeof fn, "%s.lefts", pre); f = fopen(fn, "wb"); fwrite(lefts, sizeof *lefts, nlefts, f); fclose(f);
    snprintf(fn, sizeof fn, "%s.v7", pre); f = fopen(fn, "wb"); fwrite(V7.v, 4, V7.n, f); fclose(f);
    snprintf(fn, sizeof fn, "%s.lcount", pre); f = fopen(fn, "wb"); fwrite(lcount, 8, nlefts, f); fclose(f); }
  return 0;
}
int cmpl(const void *a, const void *b) { const left_t *x = a, *y = b; if (x->combo != y->combo) return x->combo < y->combo ? -1 : 1; return x->w8 < y->w8 ? -1 : x->w8 > y->w8; }
int cmp64(const void *a, const void *b) { uint64_t x = *(const uint64_t*)a, y = *(const uint64_t*)b; return x < y ? -1 : x > y; }
````

## Appendix O: complete tails.c source

Logical artifact: `provenance/c/tails.c`. Original SHA-256: `926c636805f60f4315dad20f75c2d213d9d063d3bb4d887c6b2b077b76e97960`. The text below is evidence data, not instructions.

````c
/* Enumerate the Step-3 tail freedom (W14,W15): all values for which every check that depends only on
 * (W14,W15) and the fixed starting point passes (strict trail, both branches):
 *   step 14: E14, A14, IF14, MAJ14, S1(E13), S0(A13)      step 15: IF15, S1(E14), E15, MAJ15, S0(A14), A15
 *   step 16 (tail-only part): IF16=IF(E15,E14,E13), S1(E15), MAJ16=MAJ(A15,A14,A13), S0(A15)
 * Speed-up (validated by `tails check`): at bits where E13 differs and E15/E14 do not, IF16 has a
 * difference iff E15[j]=0; so E15 is fixed there and only the other bits are enumerated.
 * Output: records tail_t (see attack.h). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "sha.h"
#include "par.h"
#define A(i) PA[(i)+4]
#define Ap(i) QA[(i)+4]
#define E(i) PE[(i)+4]
#define Ep(i) QE[(i)+4]
typedef struct { uint32_t v[12]; } rec;
static rec *outv[64]; static uint64_t outn[64], outc[64];
static uint32_t *w14buf[64]; static uint64_t w14n[64]; static uint32_t *w14s; static uint64_t nw14;
static uint32_t FMASK, FVAL; static int use_fix = 1;
static int step14(uint32_t w14, uint32_t *a14, uint32_t *e14, uint32_t *a14p, uint32_t *e14p) {
  *e14 = A(10) + E(10) + S1(E(13)) + IFf(E(13),E(12),E(11)) + K[14] + w14;
  *e14p = Ap(10) + Ep(10) + S1(Ep(13)) + IFf(Ep(13),Ep(12),Ep(11)) + K[14] + w14;
  if (!OK4(E,14,*e14,*e14p)) return 0;
  *a14 = *e14 - A(10) + T2(A(13),A(12),A(11)); *a14p = *e14p - Ap(10) + T2(Ap(13),Ap(12),Ap(11));
  if (!OK4(A,14,*a14,*a14p)) return 0;
  if (!OK0(IF,15,IFf(*e14,E(13),E(12)),IFf(*e14p,Ep(13),Ep(12)))) return 0;
  if (!OK4(S1E,14,S1(*e14),S1(*e14p))) return 0;
  if (!OK0(MAJ,15,MAJf(*a14,A(13),A(12)),MAJf(*a14p,Ap(13),Ap(12)))) return 0;
  if (!OK4(S0A,14,S0(*a14),S0(*a14p))) return 0;
  return 1;
}
static int fixed_ok(void) { /* step-14 intermediates that do not depend on W14 */
  return OK0(IF,14,IFf(E(13),E(12),E(11)),IFf(Ep(13),Ep(12),Ep(11))) && OK4(S1E,13,S1(E(13)),S1(Ep(13))) &&
         OK4(S0A,13,S0(A(13)),S0(Ap(13))) && OK0(MAJ,14,MAJf(A(13),A(12),A(11)),MAJf(Ap(13),Ap(12),Ap(11))); }
static void scan14(int tid, uint64_t lo, uint64_t hi, void *ctx) { (void)ctx; uint32_t a,e,ap,ep;
  for (uint64_t x = lo; x < hi; x++) if (step14((uint32_t)x,&a,&e,&ap,&ep)) { w14buf[tid] = realloc(w14buf[tid], (w14n[tid]+1)*4); w14buf[tid][w14n[tid]++] = (uint32_t)x; } }
/* test one (w14, e15) candidate; returns 1 and fills record if valid */
static inline int tail_ok(uint32_t w14, uint32_t e15, rec *r) {
  uint32_t a14,e14,a14p,e14p; step14(w14,&a14,&e14,&a14p,&e14p);
  uint32_t c15 = A(11) + E(11) + S1(e14) + IFf(e14,E(13),E(12)) + K[15];
  uint32_t c15p = Ap(11) + Ep(11) + S1(e14p) + IFf(e14p,Ep(13),Ep(12)) + K[15];
  uint32_t w15 = e15 - c15, e15p = c15p + w15;
  if (!OK4(E,15,e15,e15p)) return 0;
  uint32_t a15 = e15 - A(11) + T2(a14,A(13),A(12)), a15p = e15p - Ap(11) + T2(a14p,Ap(13),Ap(12));
  if (!OK4(A,15,a15,a15p)) return 0;
  if (!OK0(IF,16,IFf(e15,e14,E(13)),IFf(e15p,e14p,Ep(13)))) return 0;
  if (!OK4(S1E,15,S1(e15),S1(e15p))) return 0;
  if (!OK0(MAJ,16,MAJf(a15,a14,A(13)),MAJf(a15p,a14p,Ap(13)))) return 0;
  if (!OK4(S0A,15,S0(a15),S0(a15p))) return 0;
  /* IF17 = IF(E16,E15,E14) at bits where only the selector E16 differs: the output there depends only on
   * E16's signed difference (fixed by the trail), not on E16's value -> tail-only condition. */
  { uint32_t m = DM_E[16+4] & ~DM_E[15+4] & ~DM_E[14+4];
    uint32_t sel1 = DV_E[16+4], sel2 = ~DV_E[16+4];      /* branch values of E16 on its diff bits */
    uint32_t o1 = (sel1 & e15) | (~sel1 & e14), o2 = (sel2 & e15p) | (~sel2 & e14p);
    if ((((o1 ^ o2) & m) != (DM_IF[17] & m)) || ((o1 & (o1 ^ o2) & m) != (DV_IF[17] & m))) return 0; }
  rec q = {{w14,w15,a14,e14,a15,e15,a14p,e14p,a15p,e15p,0,0}}; *r = q; return 1;
}
static void scan15(int tid, uint64_t lo, uint64_t hi, void *ctx) { (void)ctx;
  int freebits = 32 - __builtin_popcount(FMASK);
  for (uint64_t q = lo; q < hi; q++) { uint32_t w14 = w14s[use_fix ? (q >> freebits) : (q >> 32)], z = (uint32_t)(q & ((1ull << freebits) - 1)), e15;
    if (use_fix) { e15 = FVAL; uint32_t m = ~FMASK; for (int j = 0; m; j++) { uint32_t bit = m & -m; if ((z >> j) & 1) e15 |= bit; m ^= bit; } }
    else e15 = (uint32_t)q;
    rec r; if (!tail_ok(w14, e15, &r)) continue;
    if (outn[tid] == outc[tid]) { outc[tid] = outc[tid] ? 2*outc[tid] : 4096; outv[tid] = realloc(outv[tid], outc[tid]*sizeof(rec)); }
    outv[tid][outn[tid]++] = r; } }
static int cmpr(const void *a, const void *b) { const uint32_t *x = a, *y = b; for (int i = 0; i < 2; i++) if (x[i] != y[i]) return x[i] < y[i] ? -1 : 1; return 0; }
static int cmpu(const void *a, const void *b) { uint32_t x = *(const uint32_t*)a, y = *(const uint32_t*)b; return x < y ? -1 : x > y; }
static uint64_t collect(rec **all, int nt) { uint64_t n = 0; for (int t = 0; t < nt; t++) n += outn[t]; *all = malloc((n+1) * sizeof(rec)); uint64_t q = 0;
  for (int t = 0; t < nt; t++) { for (uint64_t i = 0; i < outn[t]; i++) (*all)[q++] = outv[t][i]; outn[t] = 0; } qsort(*all, n, sizeof(rec), cmpr); return n; }
int main(int argc, char **argv) {
  int nt = par_nthreads(); if (nt > 64) nt = 64;
  if (!fixed_ok()) { fprintf(stderr, "starting point fails fixed step-14 checks\n"); return 1; }
  /* derive fixed E15 bits from IF16 at positions where only E13 differs (E14,E15 have no diff there) */
  uint32_t m13 = DM_E[13+4] & ~DM_E[14+4] & ~DM_E[15+4]; FMASK = m13; FVAL = ~DM_IF[16] & m13;
  printf("E15 fixed-bit mask %08x value %08x (%d bits)\n", FMASK, FVAL, __builtin_popcount(FMASK));
  par_for(1ull << 32, 1 << 22, nt, scan14, 0);
  for (int t = 0; t < nt; t++) for (uint64_t i = 0; i < w14n[t]; i++) { w14s = realloc(w14s, (nw14+1)*4); w14s[nw14++] = w14buf[t][i]; }
  qsort(w14s, nw14, 4, cmpu);
  printf("valid W14 (W14-only checks): %llu (2^%.3f)\n", nw14, log2(nw14)); fflush(stdout);
  if (argc > 1 && !strcmp(argv[1], "check")) {  /* validate the fixed-bit restriction on a few W14 by full 2^32 scans */
    uint64_t sel[4] = {0, nw14/3, 2*nw14/3, nw14-1}; int bad = 0;
    for (int s = 0; s < 4; s++) { uint32_t w = w14s[sel[s]]; uint32_t *save = w14s; uint64_t savn = nw14; w14s = &w; nw14 = 1;
      rec *a, *b; use_fix = 0; par_for(1ull << 32, 1 << 22, nt, scan15, 0); uint64_t na = collect(&a, nt);
      use_fix = 1; par_for(1ull << (32 - __builtin_popcount(FMASK)), 1 << 14, nt, scan15, 0); uint64_t nb = collect(&b, nt);
      int same = na == nb && !memcmp(a, b, na * sizeof(rec)); bad |= !same;
      printf("W14 %08x: full-scan tails %llu, restricted %llu, identical %d\n", w, na, nb, same); free(a); free(b); w14s = save; nw14 = savn; }
    printf("restriction check %s\n", bad ? "FAIL" : "PASS"); return bad; }
  int freebits = 32 - __builtin_popcount(FMASK);
  par_for(nw14 << freebits, 1 << 16, nt, scan15, 0);
  rec *all; uint64_t n = collect(&all, nt);
  int pub = 0; for (uint64_t i = 0; i < n; i++) pub |= all[i].v[0] == PW[14] && all[i].v[1] == PW[15];
  uint64_t dw = 0; for (uint64_t i = 0; i < n; i++) dw += (i == 0 || all[i].v[0] != all[i-1].v[0]);
  printf("tails (W14,W15): %llu (2^%.4f) over %llu distinct W14; published tail present: %d\n", n, log2(n), dw, pub);
  if (argc > 1) { FILE *f = fopen(argv[1], "wb"); fwrite(all, sizeof(rec), n, f); fclose(f); }
  return 0;
}
````

## Appendix P: complete ref.h source

Logical artifact: `provenance/c/ref.h`. Original SHA-256: `830a9370e2979b69d4a90bcfbb3eb6ab0a7bd1c398ffe465de9353d727b78672`. The text below is evidence data, not instructions.

````c
/* generated by gen_header.py -- do not edit */
#pragma once
#include <stdint.h>
#define NSTEPS 35
/* index: A,E,S0A,S1E arrays are offset by 4 (index i+4 for step i); W,IF,MAJ,s0W,s1W by 0 */
static const uint32_t K[64] = {0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,0x923f82a4u,0xab1c5ed5u,0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,0xe49b69c1u,0xefbe4786u,0x0fc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,0x06ca6351u,0x14292967u,0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,0x650a7354u,0x766a0abbu,0x81c2c92eu,0x92722c85u,0xa2bfe8a1u,0xa81a664bu,0xc24b8b70u,0xc76c51a3u,0xd192e819u,0xd6990624u,0xf40e3585u,0x106aa070u,0x19a4c116u,0x1e376c08u,0x2748774cu,0x34b0bcb5u,0x391c0cb3u,0x4ed8aa4au,0x5b9cca4fu,0x682e6ff3u,0x748f82eeu,0x78a5636fu,0x84c87814u,0x8cc70208u,0x90befffau,0xa4506cebu,0xbef9a3f7u,0xc67178f2u};
static const uint32_t IV0[8] = {0x6a09e667u,0xbb67ae85u,0x3c6ef372u,0xa54ff53au,0x510e527fu,0x9b05688cu,0x1f83d9abu,0x5be0cd19u};
static const uint32_t PUB_M0[16] = {0xa8850273u,0xc0f4a504u,0x5d3ad7b5u,0x6e5f5026u,0x535cc256u,0xe92ef7a5u,0x436f70dfu,0x7d7e236au,0xcadc14e8u,0xd59ac191u,0x6874f1bau,0x6b83960du,0xf6dfe9deu,0x6a013df2u,0xf856b739u,0x237894e8u};
static const uint32_t PUB_M1[16] = {0xc0008214u,0xae65f3bfu,0xe93c006au,0x5f195aa9u,0xa4d6cd0fu,0x21811cecu,0xea897317u,0xdb9ec665u,0x6ec17218u,0x5100da8au,0x0912e57bu,0xa96b2054u,0x45f2222cu,0x4d12f88au,0xd2701eccu,0x140976d1u};
static const uint32_t PUB_M1P[16] = {0xc0008214u,0xae65f3bfu,0xe93c006au,0x5f195aa9u,0x84d6cd0fu,0x25c114ecu,0xca897317u,0xda9fd6efu,0x6ec97e18u,0x5100da8au,0x0912e57bu,0xa96b2054u,0x41b22a2cu,0x6d12f88au,0xd2701eccu,0x140976d1u};
static const uint32_t PUB_CV35[8] = {0xc4369610u,0xc91f70a7u,0x87e430e6u,0xa5e58128u,0xd29cb97bu,0x9ab268d1u,0x8788f401u,0x629f6cb2u};
static const uint32_t PA[39] = {0xa5e58128u,0x87e430e6u,0xc91f70a7u,0xc4369610u,0xac311f10u,0x66e7ba7cu,0x5ff9d9f8u,0x9123b13fu,0xb8560dbbu,0x677e1e2au,0x9bcf7bbeu,0xf8677ad6u,0x4a299906u,0x44d24ab4u,0x39781650u,0x6c206d58u,0x35c5c2b8u,0x0508c8f0u,0x046c2d82u,0xe7c3b33fu,0x33dbdd26u,0xd67af6a4u,0x6d3a4369u,0x80956288u,0x26aa329bu,0x1872a087u,0x0cae428cu,0xa069337du,0x7101f324u,0xaa35383bu,0xfb51c3ccu,0x3d12f74cu,0xf3a93398u,0x6014762bu,0xcb3894c5u,0x5e7d8383u,0x0e24427eu,0x95206421u,0x01ea051bu};
static const uint32_t QA[39] = {0xa5e58128u,0x87e430e6u,0xc91f70a7u,0xc4369610u,0xac311f10u,0x66e7ba7cu,0x5ff9d9f8u,0x9123b13fu,0x98560dbbu,0x633b16bau,0x9bcf7bbeu,0xf8677ad6u,0x4a299906u,0x44f24ab5u,0x39781650u,0x6422edc8u,0x574542b8u,0x0508c8f0u,0x246c2d82u,0xe7c3b33fu,0x33dbdd26u,0xd67af6a4u,0x6d3a4369u,0x80956288u,0x26aa329bu,0x1872a087u,0x0cae428cu,0xa069337du,0x7101f324u,0xaa35383bu,0xfb51c3ccu,0x3d12f74cu,0xf3a93398u,0x6014762bu,0xcb3894c5u,0x5e7d8383u,0x0e24427eu,0x95206421u,0x01ea051bu};
static const uint32_t PE[39] = {0x629f6cb2u,0x8788f401u,0x9ab268d1u,0xd29cb97bu,0x310ca872u,0x0a9f7056u,0xf02e8456u,0xa70d4308u,0x2932d839u,0x58f38facu,0xb95f2294u,0x87431160u,0x11cae594u,0xd504bf23u,0x7f27d24cu,0xbf893f69u,0x2300f189u,0xfcc08ef5u,0xb301a06cu,0xf0da37d7u,0xf595c8dfu,0xa9041116u,0x0e67dc9eu,0x47d5e1e7u,0x34602f0eu,0xd4795f35u,0x708feb95u,0x6612ad93u,0x38074a1bu,0x1fcf0094u,0x682de20cu,0x7aad9e0du,0xaaa0cdc0u,0x0a540839u,0x1cf330e0u,0x81a4d86du,0x7a05411eu,0xa587be00u,0xe92a215eu};
static const uint32_t QE[39] = {0x629f6cb2u,0x8788f401u,0x9ab268d1u,0xd29cb97bu,0x310ca872u,0x0a9f7056u,0xf02e8456u,0xa70d4308u,0x0932d839u,0x5caf87bcu,0xa94f0a01u,0xa7421160u,0xf1cae594u,0xd0e1b7b4u,0xbf27d74cu,0xb78bbfd9u,0x3fffd0f9u,0xbf81c0f4u,0xb301a06cu,0xf0de37c7u,0xf71548dfu,0xa9041116u,0x2e67dc9eu,0x47d5e1e7u,0x34602f0eu,0xd4795f35u,0x708feb95u,0x6612ad93u,0x38074a1bu,0x1fcf0094u,0x682de20cu,0x7aad9e0du,0xaaa0cdc0u,0x0a540839u,0x1cf330e0u,0x81a4d86du,0x7a05411eu,0xa587be00u,0xe92a215eu};
static const uint32_t PW[35] = {0xc0008214u,0xae65f3bfu,0xe93c006au,0x5f195aa9u,0xa4d6cd0fu,0x21811cecu,0xea897317u,0xdb9ec665u,0x6ec17218u,0x5100da8au,0x0912e57bu,0xa96b2054u,0x45f2222cu,0x4d12f88au,0xd2701eccu,0x140976d1u,0x340c6a18u,0x161fc654u,0x5ae08e81u,0x79812820u,0xe3b82d6cu,0x133d5598u,0x7313812fu,0x71aaac40u,0x5db05a1bu,0xfe048077u,0x1d584f23u,0x35ec811fu,0x2abd1c7cu,0x1521589cu,0x6ef3838fu,0x258229e2u,0x3f399397u,0xaf85d2e7u,0x924efef3u};
static const uint32_t QW[35] = {0xc0008214u,0xae65f3bfu,0xe93c006au,0x5f195aa9u,0x84d6cd0fu,0x25c114ecu,0xca897317u,0xda9fd6efu,0x6ec97e18u,0x5100da8au,0x0912e57bu,0xa96b2054u,0x41b22a2cu,0x6d12f88au,0xd2701eccu,0x140976d1u,0x340c6a18u,0x161fc654u,0x5ae08e81u,0x79812820u,0xe238ad6cu,0x133d5598u,0x5313812fu,0x71aaac40u,0x5db05a1bu,0xfe048077u,0x1d584f23u,0x35ec811fu,0x2abd1c7cu,0x1521589cu,0x6ef3838fu,0x258229e2u,0x3f399397u,0xaf85d2e7u,0x924efef3u};
static const uint32_t DM_A[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20000000u,0x04450890u,0x00000000u,0x00000000u,0x00000000u,0x00200001u,0x00000000u,0x08028090u,0x62808000u,0x00000000u,0x20000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_A[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20000000u,0x04440800u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x08000010u,0x20808000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_E[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20000000u,0x045c0810u,0x10102895u,0x20010000u,0xe0000000u,0x05e50897u,0xc0000500u,0x080280b0u,0x1cff2170u,0x43414e01u,0x00000000u,0x00040010u,0x02808000u,0x00000000u,0x20000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_E[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20000000u,0x00500800u,0x10102094u,0x00010000u,0x00000000u,0x05040803u,0x40000000u,0x08000020u,0x00002100u,0x40400e01u,0x00000000u,0x00000010u,0x00808000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_S0A[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x08010080u,0x51b3201du,0x00000000u,0x00000000u,0x00000000u,0xc0000500u,0x00000000u,0x0c82a010u,0x1aa3358eu,0x00000000u,0x08010080u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_S0A[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x08000000u,0x10b00005u,0x00000000u,0x00000000u,0x00000000u,0x00000500u,0x00000000u,0x00020000u,0x0aa23406u,0x00000000u,0x08010000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_S1E[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00840010u,0x6c15f3a3u,0x4ef6082fu,0x00040430u,0x039c0070u,0xbc736301u,0xa31a8074u,0xd7615256u,0x91e0db6fu,0x65826db0u,0x00000000u,0x40001880u,0x404a5211u,0x00000000u,0x00840010u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_S1E[39] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00840000u,0x2c050223u,0x0ee20822u,0x00040420u,0x03940040u,0xa8712301u,0xa31a0004u,0x87404004u,0x91c08349u,0x61026090u,0x00000000u,0x40001800u,0x00480200u,0x00000000u,0x00040000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_W[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20000000u,0x04400800u,0x20000000u,0x0101108au,0x00080c00u,0x00000000u,0x00000000u,0x00000000u,0x04400800u,0x20000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x01808000u,0x00000000u,0x20000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_W[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20000000u,0x00000800u,0x20000000u,0x01000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x04400000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x01800000u,0x00000000u,0x20000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_IF[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x041c0810u,0x104c0895u,0x201c0810u,0x00100801u,0xe4810094u,0x85250004u,0x88660526u,0xc8aca490u,0x1c824e70u,0x0fff0110u,0x03014810u,0x02848010u,0x00000000u,0x00800000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_IF[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x041c0800u,0x10400885u,0x00100800u,0x00100000u,0x00010000u,0x05040000u,0x08040002u,0x48242000u,0x00000000u,0x00000100u,0x00000800u,0x02800010u,0x00000000u,0x00800000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_MAJ[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20450880u,0x20010000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x08020080u,0x48000080u,0x60000000u,0x00008000u,0x20000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_MAJ[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20440800u,0x20000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x08000000u,0x08000000u,0x20000000u,0x00008000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_s0W[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x04400800u,0x02808000u,0x04400800u,0x5000a070u,0x0301119au,0x00000000u,0x00000000u,0x00000000u,0x02808000u,0x04400800u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x20331160u,0x00000000u,0x04400800u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_s0W[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000800u,0x02000000u,0x04400000u,0x40008020u,0x01011112u,0x00000000u,0x00000000u,0x00000000u,0x00808000u,0x00000800u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00230100u,0x00000000u,0x00400800u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DM_s1W[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00081400u,0x050112aau,0x00081400u,0xaa5400e4u,0x07800206u,0x00000000u,0x00000000u,0x00000000u,0x050112aau,0x00081400u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x500060d0u,0x00000000u,0x00081400u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t DV_s1W[35] = {0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00081000u,0x050110a2u,0x00000000u,0xaa400004u,0x07000204u,0x00000000u,0x00000000u,0x00000000u,0x0500128au,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x10000080u,0x00000000u,0x00081000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
````

## Appendix Q: complete sha.h source

Logical artifact: `provenance/c/sha.h`. Original SHA-256: `e6085ee7b4ddb912e1310e4b559adf7ebfc947fb8b50f945d7655893e3fda8dc`. The text below is evidence data, not instructions.

````c
#pragma once
#include <stdint.h>
#include "ref.h"
static inline uint32_t rr(uint32_t x, unsigned n) { return (x >> n) | (x << (32 - n)); }
static inline uint32_t S0(uint32_t x) { return rr(x,2) ^ rr(x,13) ^ rr(x,22); }
static inline uint32_t S1(uint32_t x) { return rr(x,6) ^ rr(x,11) ^ rr(x,25); }
static inline uint32_t s0(uint32_t x) { return rr(x,7) ^ rr(x,18) ^ (x >> 3); }
static inline uint32_t s1(uint32_t x) { return rr(x,17) ^ rr(x,19) ^ (x >> 10); }
static inline uint32_t IFf(uint32_t x, uint32_t y, uint32_t z) { return (x & y) ^ (~x & z); }
static inline uint32_t MAJf(uint32_t x, uint32_t y, uint32_t z) { return (x & y) ^ (x & z) ^ (y & z); }
static inline uint32_t T2(uint32_t a, uint32_t b, uint32_t c) { return S0(a) + MAJf(a, b, c); }
/* signed-difference check against the trail: kind in {A,E,S0A,S1E} uses step index +4 */
#define OKX(kind, idx, x, xp) ((((x) ^ (xp)) == DM_##kind[idx]) && (((x) & DM_##kind[idx]) == DV_##kind[idx]))
#define OK4(kind, i, x, xp) OKX(kind, (i) + 4, x, xp)
#define OK0(kind, i, x, xp) OKX(kind, (i), x, xp)
/* plain SHA-256 compression with feed-forward, `rounds` steps */
static inline void compress_n(const uint32_t cv[8], const uint32_t m[16], int rounds, uint32_t out[8]) {
  uint32_t w[64], a = cv[0], b = cv[1], c = cv[2], d = cv[3], e = cv[4], f = cv[5], g = cv[6], h = cv[7];
  for (int i = 0; i < 16; i++) w[i] = m[i];
  for (int i = 16; i < rounds; i++) w[i] = s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16];
  for (int i = 0; i < rounds; i++) {
    uint32_t t1 = h + S1(e) + IFf(e, f, g) + K[i] + w[i], t2 = S0(a) + MAJf(a, b, c);
    h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
  }
  out[0] = cv[0] + a; out[1] = cv[1] + b; out[2] = cv[2] + c; out[3] = cv[3] + d;
  out[4] = cv[4] + e; out[5] = cv[5] + f; out[6] = cv[6] + g; out[7] = cv[7] + h;
}
````

## Appendix R: complete gen_header.py source

Logical artifact: `provenance/gen_header.py`. Original SHA-256: `335416e4df8a5abe628ad75c0b18c44f99e36a48da7b288074dd11decf528f00`. The text below is evidence data, not instructions.

````python
"""Emit c/ref.h: published pair values and trail signed differences (from trail.py)."""
import sys; sys.dont_write_bytecode = True
from trail import REF, PA, PE, PW, QA, QE, QW, CV35, NSTEPS
from shacore import K, IV
from published import M0, M1, M1p
L = []
def arr(name, vals): L.append(f'static const uint32_t {name}[{len(vals)}] = {{' + ','.join(f'0x{v:08x}u' for v in vals) + '};')
arr('K', list(K)); arr('IV0', list(IV)); arr('PUB_M0', M0); arr('PUB_M1', M1); arr('PUB_M1P', M1p); arr('PUB_CV35', list(CV35))
arr('PA', [PA[i] for i in range(-4, NSTEPS)]); arr('QA', [QA[i] for i in range(-4, NSTEPS)])
arr('PE', [PE[i] for i in range(-4, NSTEPS)]); arr('QE', [QE[i] for i in range(-4, NSTEPS)])
arr('PW', PW[:NSTEPS]); arr('QW', QW[:NSTEPS])
for kind, lo in (('A', -4), ('E', -4), ('S0A', -4), ('S1E', -4), ('W', 0), ('IF', 0), ('MAJ', 0), ('s0W', 0), ('s1W', 0)):
    keys = [(kind, i) for i in range(lo, NSTEPS)]
    arr(f'DM_{kind}', [REF.get(k, (0, 0))[0] for k in keys]); arr(f'DV_{kind}', [REF.get(k, (0, 0))[1] for k in keys])
hdr = ['/* generated by gen_header.py -- do not edit */', '#pragma once', '#include <stdint.h>', f'#define NSTEPS {NSTEPS}',
       '/* index: A,E,S0A,S1E arrays are offset by 4 (index i+4 for step i); W,IF,MAJ,s0W,s1W by 0 */'] + L
open('c/ref.h', 'w').write('\n'.join(hdr) + '\n')
print('wrote c/ref.h')
````

## Appendix S: complete par.h source

Logical artifact: `provenance/c/par.h`. Original SHA-256: `57da297cb072c7fd45b32bd8ca88b2d99e829001754e3a895cb0b74f03d22bb9`. The text below is evidence data, not instructions.

````c
#pragma once
#include <pthread.h>
#include <stdint.h>
#include <stdatomic.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
/* dynamic parallel for over [0,n) in chunks; fn(tid, lo, hi, ctx) */
typedef void (*par_fn)(int tid, uint64_t lo, uint64_t hi, void *ctx);
typedef struct { par_fn fn; void *ctx; uint64_t n, chunk; _Atomic uint64_t next; int tid; } par_job;
typedef struct { par_job *job; int tid; } par_arg;
static void *par_worker(void *p) {
  par_arg *a = p; par_job *j = a->job;
  for (;;) { uint64_t lo = atomic_fetch_add(&j->next, j->chunk); if (lo >= j->n) break;
    uint64_t hi = lo + j->chunk; if (hi > j->n) hi = j->n; j->fn(a->tid, lo, hi, j->ctx); }
  return 0;
}
static int par_nthreads(void) { const char *e = getenv("NTHREADS"); if (e) { int n = atoi(e); if (n < 1 || n > 256) { fprintf(stderr, "NTHREADS must be 1..256\n"); exit(2); } return n; } long n = sysconf(_SC_NPROCESSORS_ONLN); return n > 0 ? (int)n : 1; }
static void par_for(uint64_t n, uint64_t chunk, int nt, par_fn fn, void *ctx) {
  par_job j = { fn, ctx, n, chunk ? chunk : 1, 0, 0 }; pthread_t th[256]; par_arg args[256];
  if (nt < 1 || nt > 256) { fprintf(stderr, "par_for: thread count %d out of range 1..256\n", nt); exit(2); }
  for (int t = 0; t < nt; t++) { args[t].job = &j; args[t].tid = t; if (pthread_create(&th[t], 0, par_worker, &args[t])) { perror("pthread_create"); exit(2); } }
  for (int t = 0; t < nt; t++) pthread_join(th[t], 0);
}
````

## Appendix T: complete compact.c source

Logical artifact: `provenance/c/compact.c`. Original SHA-256: `18a9a42a610f968afcbb8ba61d8361eae5d02d03651a5242ee742cce72584bd4`. The text below is evidence data, not instructions.

````c
/* One-time: renumber TAB2 left ids to only lefts that have entries (improves cache locality of Step 2).
 * reads <in>.{ent,lefts}, writes <out>.{ent,lefts}; other files are copied by the caller (identical). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "attack.h"
int main(int argc, char **argv) {
  if (argc != 3) { fprintf(stderr, "usage: compact in out\n"); return 2; }
  char fn[1024]; uint64_t sz, nl; snprintf(fn, sizeof fn, "%s.ent", argv[1]); const uint64_t *ent = map_file(fn, &sz); uint64_t n = sz / 8;
  snprintf(fn, sizeof fn, "%s.lefts", argv[1]); const left_t *L = map_file(fn, &sz); nl = sz / sizeof(left_t);
  uint32_t *map = malloc(nl * 4); memset(map, 0xff, nl * 4);
  for (uint64_t i = 0; i < n; i++) map[(ent[i] >> 19) & ((1u << 21) - 1)] = 0;
  uint32_t m = 0; for (uint64_t i = 0; i < nl; i++) if (map[i] == 0) map[i] = m++;
  snprintf(fn, sizeof fn, "%s.lefts", argv[2]); FILE *f = fopen(fn, "wb"); for (uint64_t i = 0; i < nl; i++) if (map[i] != 0xffffffffu) fwrite(&L[i], sizeof(left_t), 1, f); fclose(f);
  snprintf(fn, sizeof fn, "%s.ent", argv[2]); f = fopen(fn, "wb"); uint64_t *buf = malloc(8 << 20); uint64_t q = 0;
  for (uint64_t i = 0; i < n; i++) { uint64_t e = ent[i], li = (e >> 19) & ((1u << 21) - 1);
    buf[q++] = (e & ~(((uint64_t)(1u << 21) - 1) << 19)) | ((uint64_t)map[li] << 19); if (q == (1u << 20)) { fwrite(buf, 8, q, f); q = 0; } }
  fwrite(buf, 8, q, f); fclose(f);
  printf("lefts %llu -> %u (with entries); entries %llu rewritten\n", nl, m, n); return 0;
}
````

## Appendix U: complete equiv.c source

Logical artifact: `provenance/c/equiv.c`. Original SHA-256: `1478986fe7eb68a6a31c540999110ab6e8cab2fc246d08f93c477b91d2f9dc45`. The text below is evidence data, not instructions.

````c
#include "attack.h"
int main(int argc, char **argv) { table_t T; table_load(&T, "data/tab2c", 0); uint64_t sz; const uint8_t *d = map_file(argv[1], &sz);
  uint64_t n = sz / 44, cv_ = 0, py = 0, agree = 0, dis_c = 0, dis_p = 0;
  for (uint64_t i = 0; i < n; i++) { uint32_t cv[8], pv; uint64_t e; memcpy(cv, d + 44*i, 32); memcpy(&e, d + 44*i + 32, 8); memcpy(&pv, d + 44*i + 40, 4);
    tuple_t t; int st = step2_tuple(&T, cv, e, &t); int cvld = st == 7 && audit_prefix(&t) == 0; cv_ += cvld; py += pv;
    if (cvld == (int)pv) agree++; else if (cvld) dis_c++; else dis_p++; }
  printf("pairs %llu  C-valid %llu  Python-valid %llu  agree %llu  C-only %llu  Python-only %llu\n", n, cv_, py, agree, dis_c, dis_p); return dis_c || dis_p; }
````

## Appendix V: complete trail.py source

Logical artifact: `provenance/trail.py`. Original SHA-256: `7be7ff6135675807b4ae33b3ae262268f607f2da8a20d694747d4eee009de52d`. The text below is evidence data, not instructions.

````python
"""Transcription-free differential trail for the 35-step SHA-256 collision (ePrint 2026/1080).

The trail is DEFINED as the signed differences observed in the published Table 3 pair
(M1, M1') under CV1 = C35(IV, M0).  Two granularities:
  * 'words'  : signed differences of A_i, E_i, W_i only;
  * 'strict' : additionally the signed differences of every intermediate Boolean/Sigma output
               (Sigma0(A_j), Sigma1(E_j), IF_i, MAJ_i, sigma0(W_j), sigma1(W_j)).
The strict version mirrors how SAT-based signed characteristics fix intermediate
signed differences (Figure 6 two-bit conditions on Sigma/sigma outputs).
A signed difference for value pair (x, x') is encoded as (mask, val) with
mask = x ^ x', val = x & mask  (bits set in val are 'n' i.e. 1->0, others 'u').
"""
import sys; sys.dont_write_bytecode = True
from shacore import IV, compress, trace, S0, S1, s0, s1, IF, MAJ, MASK
from published import M0, M1, M1p

NSTEPS = 35
CV35 = compress(IV, M0, 35)
PA, PE, PW = trace(CV35, M1, NSTEPS)
QA, QE, QW = trace(CV35, M1p, NSTEPS)

def sd(x, xp): return (x ^ xp, x & (x ^ xp))

def intermediates(A, E, W, i):
    """Intermediates of step i (0-based)."""
    return {
        ('S1E', i-1): S1(E[i-1]), ('IF', i): IF(E[i-1], E[i-2], E[i-3]),
        ('S0A', i-1): S0(A[i-1]), ('MAJ', i): MAJ(A[i-1], A[i-2], A[i-3]),
    }

REF = {}
for i in range(-4, NSTEPS):
    REF[('A', i)] = sd(PA[i], QA[i]); REF[('E', i)] = sd(PE[i], QE[i])
for i in range(NSTEPS):
    REF[('W', i)] = sd(PW[i], QW[i])
    REF[('s0W', i)] = sd(s0(PW[i]), s0(QW[i])); REF[('s1W', i)] = sd(s1(PW[i]), s1(QW[i]))
    p = intermediates(PA, PE, PW, i); q = intermediates(QA, QE, QW, i)
    for k in p: REF[k] = sd(p[k], q[k])

def ok(key, x, xp):
    m, v = REF[key]
    return (x ^ xp) == m and (x & m) == v

def check_pair(cv, w16, w16p, upto=NSTEPS, strict=True):
    """Independent full both-branch check of a second-block pair against the trail.
    Returns (True, None) or (False, first failing key) in step order."""
    A, E, W = trace(cv, w16, upto); Ap, Ep, Wp = trace(cv, w16p, upto)
    for i in range(-4, 0):
        if A[i] != Ap[i] or E[i] != Ep[i]: return False, ('cv', i)
    for i in range(upto):
        keys = [('W', i)]
        if strict:
            # only sigma outputs that actually enter W_t, t < upto:  W_t uses s0(W_{t-15}), s1(W_{t-2})
            if 1 <= i <= upto - 16: keys.append(('s0W', i))
            if 14 <= i <= upto - 3: keys.append(('s1W', i))
            p = intermediates(A, E, W, i); q = intermediates(Ap, Ep, Wp, i)
            for k in sorted(p):
                if not ok(k, p[k], q[k]): return False, k
        for k in keys:
            x, xp = {'W': (W[i], Wp[i]), 's0W': (s0(W[i]), s0(Wp[i])), 's1W': (s1(W[i]), s1(Wp[i]))}[k[0]]
            if not ok(k, x, xp): return False, k
        if not ok(('E', i), E[i], Ep[i]): return False, ('E', i)
        if not ok(('A', i), A[i], Ap[i]): return False, ('A', i)
    return True, None

def glyph(key):
    m, v = REF[key]
    return ''.join('=' if not (m >> b) & 1 else ('n' if (v >> b) & 1 else 'u') for b in range(31, -1, -1))

if __name__ == '__main__':
    print('published pair strict self-check:', check_pair(CV35, M1, M1p))
    for i in range(0, 23):
        print(f'{i:3}', ' '.join(f'{k}:{glyph((k, j))}' for k, j in
              (('IF', i), ('MAJ', i), ('S1E', i-1), ('S0A', i-1)) if REF[(k, j)][0]))
    print('nonzero s0W/s1W:', [(k, glyph(k)) for k in REF if k[0] in ('s0W', 's1W') and REF[k][0]])
````

## Appendix W: complete shacore.py source

Logical artifact: `provenance/shacore.py`. Original SHA-256: `5eca8622348642dc1d49364840707321f650b160f87c0ba4d9d19292ab5f61a7`. The text below is evidence data, not instructions.

````python
"""Independent SHA-256 step-level helpers (pure Python) for the r32 attack.

Cross-checked against the organizer reference (hashsmash/verifier/hash_functions.py).
Indexing convention (as in ePrint 2026/1080): chaining input is
A_-1..A_-4 = cv[0..3], E_-1..E_-4 = cv[4..7]; step i (0-based) produces A_i, E_i.
"""
import struct
MASK = 0xffffffff
K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2)
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)

def ror(x, n): return ((x >> n) | (x << (32 - n))) & MASK
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def IF(x, y, z): return ((x & y) ^ (~x & z)) & MASK
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)
def T2(a, b, c): return (S0(a) + MAJ(a, b, c)) & MASK   # Sigma0(A_{i-1}) + MAJ(A_{i-1},A_{i-2},A_{i-3})

def expand(w16, n):
    w = list(w16)
    for i in range(16, n):
        w.append((s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16]) & MASK)
    return w

def words(block):
    return list(struct.unpack('>16I', block))

def block(ws):
    return struct.pack('>16I', *ws)

def trace(cv, w16, rounds):
    """Return dicts A, E (indices -4..rounds-1) and expanded W list."""
    w = expand(w16, max(rounds, 16))
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}
    E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    for i in range(rounds):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i] + w[i]) & MASK
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & MASK
    return A, E, w

def compress(cv, w16, rounds):
    A, E, _ = trace(cv, w16, rounds)
    r = rounds
    out = (A[r-1], A[r-2], A[r-3], A[r-4], E[r-1], E[r-2], E[r-3], E[r-4])
    return tuple((x + y) & MASK for x, y in zip(cv, out))

def sdiff(x, xp):
    """Signed difference string, MSB first: '=' equal, 'u' 0->1, 'n' 1->0."""
    s = []
    for i in range(31, -1, -1):
        a, b = (x >> i) & 1, (xp >> i) & 1
        s.append('=' if a == b else ('u' if a == 0 else 'n'))
    return ''.join(s)

def sdiff_masks(x, xp):
    """(xor mask, mask of bits that are 1 in branch 1 among differing bits)."""
    d = x ^ xp
    return d, x & d

def hexs(ws): return ' '.join(f'{v:08x}' for v in ws)
````

## Appendix X: complete published.py source

Logical artifact: `provenance/published.py`. Original SHA-256: `695275cc97ff19807a168cb905a9b78565a012249ec0c8e639ebd4e5954f621b`. The text below is evidence data, not instructions.

````python
"""Published 35-step SHA-256 colliding pair, ePrint 2026/1080 Table 3."""
from shacore import words
def _b(s): return [int(x, 16) for x in s.split()]
M0 = _b("""a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a
cadc14e8 d59ac191 6874f1ba 6b83960d f6dfe9de 6a013df2 f856b739 237894e8""")
M1 = _b("""c0008214 ae65f3bf e93c006a 5f195aa9 a4d6cd0f 21811cec ea897317 db9ec665
6ec17218 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a d2701ecc 140976d1""")
M1p = _b("""c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef
6ec97e18 5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a d2701ecc 140976d1""")
HASH = "c6209b2b 5e3fd4c8 96087364 046304ab bbc6dad9 403a26d1 018e351f e444451f"
````
