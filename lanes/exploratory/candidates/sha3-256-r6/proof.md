# SHA3-256 round 6: resynthesized register step and compact checkpoint search

## 1. Claim and resources

This package prices an ordinary distinguished-point birthday search for two distinct 128-byte messages with the same `sha3-256-r6-prefix-v1` digest. It claims no weakness in full SHA3-256. Under H1 in Section 6, one bounded attempt succeeds with probability at least 0.39.

The exact ledger has N = 35340637101563815954524310135853372908247 word operations. One target compression costs C = 1626, so `log2(N/C) = 124.0313403016559599495104660773756646797426833930963673227770422992653193463892615999117885213722905852741814098787989923370938489303439141855638236827301055386516200003444180057103442220223942162253276928916592193637215` and the upward-rounded claim is **124.03135**. Peak memory is 710251 bytes. Preprocessing is 184030978853888 word operations and no nonuniform advice.

Under `hashsmash-scalar-tm-v1` the rank is `time_log2 + max(0, memory_log2_bytes - 20)`
with one-MiB memory units floored at one unit. Peak memory is 710,251 bytes, below
2^20 = 1,048,576, so the memory term is zero and the projected scalar score equals the time
bound, **124.03135**. The `collision-frontier-v5` score metric is `timeLog2` and that model
records memory as a reviewed metric with no scalar contribution, so both readings agree
here. The promoted incumbent on this track stands at 124.03648; this package is 0.00513
lower. The 0.00102 bit under the previous filing of this package is the 19 NOTs that
`NOT(NOT(x))` folding removes from the emitted step. `baseline_improved` names the organizer nominal reference and asserts no improvement
over it: at 6 of 24 rounds this bound is above the nominal 128-bit reference and the
construction is an ordinary distinguished-point birthday search.

## 2. Target and chain function

Write the 256-bit point as four little-endian lanes u0..u3. The one-block message has lanes 1, 6, 11 equal to `u0, u1, u0 xor u1 xor K11`; lanes 4, 9, 14 equal to `u2, u3, u2 xor u3 xor K14`; all other rate lanes are fixed. The remaining absorbed state includes SHA3 suffix `0x06` and pad10*1. This map is injective. Define `g(u) = SHA3-256-r6(m(u)) xor PD`. Equal values of g for different points give equal digests for different messages because the common PD cancels.

The 25 lane constants in lane order are:

`0000000000000000 0000000000000000 e612b8e44c9e9b1c 0000000000000000 0000000000000000 ffffffffffffffff 0000000000000000 0000000000000000 0000000000000000 0000000000000000 ffffffffffffffff b984ae391327a6c1 0000000000000000 9cc2571c8993d363 8cf6a38dd9b0b271 ffffffffffffffff 8000000000000006 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000`

PD is `77858ceb7afeef63 2a754023590aaa98 007820040d081089 8808331404011015`. The normative emitter in `experiments/compact.py` derives PD again from the emitted circuit and rejects a mismatch.

## 3. Bit-sliced register step

One 256-bit register word carries one bit plane for 256 walks. Round 0 and the theta of round 1 are affine in the point. Later theta columns are built in z order, chi rows use the cheapest exact complement subset and optional 10-gate dependency, and the last round retains only four digest lanes. The frozen plan contains the C/D complements and compact chi decisions for every row. It is bound by SHA-256 `bc0efa7a784bb0eedabe0b682baa64b1ab0532bd850efffe37bc5ada6f05c0be`.

The emitted straight-line register program has 26508 operations: 19147 XOR, 3577 AND, 3079 OR and 705 NOT. Complement folds `NOT(NOT(x))` to `x` before a node is allocated, which deletes 19 NOTs that round 1 used to emit; the scalar digest is unchanged. Lowest-free last-use allocation names registers 0..1928. It contains 368 14-bit, 16774 25-bit and 9366 36-bit encoded records, 16805 with destination equal to the first operand. Its measured stored size is 95210 bytes and SHA-256 is `2b1eec1753cefed6d1839719754253a0e5ddc4cfa7f0a065c0ce0fd8a5ba1e31`.

### 3.6 Registers and code encoding (machine conventions H_reg and H_code)

**Registers.** Input and digest plane j use register j. Each other value receives the lowest free register allowed by its last use. Values in registers above 255 are dead between steps and may be reused by handlers. The straight line uses registers 0 through 1928; persistent search state begins at register 1929. The declared file has 1940 words, or 62080 bytes, all included in Section 5.

**H_reg (declared machine convention, role supporting in claim.json).** The cost model and target profile fix no register count. This package uses the 256-bit word RAM of collision-frontier-v5 with the declared 1940-register file above. An operation on register operands costs one word operation, with no load or store. Every load and store in the assembled other code is an explicit charged word operation. H_reg affects the time and memory ledgers, not the success bound.

**H_code (declared code-memory charging convention, role supporting in claim.json).** The cost model and target profile fix no code encoding.

- **Encoding.** Each straight-line instruction has register operands only. Bits 0..1 give XOR, AND, OR or NOT and bit 2 flags destination equal to the first operand. With that flag, NOT carries one 11-bit register and a binary operation carries two; without it, NOT carries destination and source while a binary operation carries destination and two sources. Commutative operations swap operands when the destination equals the second. Records are packed without inter-record padding in a little-endian bit stream. The straight-line file is 95210 bytes. The separate prefilter is a 15-operation OR chain from digest planes 240 through 255 into register 1933: first `OR R_PREFILTER,240,241`, then `OR R_PREFILTER,R_PREFILTER,plane`. It uses the same encoding, occupies 49 bytes, and has SHA-256 `9d37c799e6735d7583803750971187fe83f8ee186f5b3c9b9313b928bd45ce49`. The two files occupy 95259 bytes under H_code.
- **Other code.** Setup, loop control, handlers, restart, replay and output are assembled as 1002 fixed 8-byte instruction words followed by 12 distinct 32-byte literal words, 8400 bytes total, SHA-256 `0026e7ffc96cc4ded46b98e040e743596254f8c9b64e46a2e9cebe33140454ca`. A word has a 5-bit opcode, one literal flag, three 11-bit register fields and a 25-bit immediate or literal index. The assembled operations are model primitives; each is charged as the word operation it performs, except PERM at C operations. Loads and stores are explicit among those instructions.
- **Time ledger.** The straight line contributes one charged word operation for each logical XOR, AND, OR or NOT under H_reg. H_code determines only the stored code bytes charged in memory. The bounded C emitters and organizer experiment reconstruct the encodings, hashes and functional program.

### Construction campaign

The construction first builds the exact chained-chi table. For each of 32 input polarities and 32 requested output polarities it enumerates every complement subset, every trick mask except the five-cycle, and every mixed-term polarity mask. A non-trick output anchors the row; outputs are then built backward, and a trick reads the already computed next output using `(not out[k]) and b[k+1] = (not b[k]) and b[k+1]`. Before use, the builder evaluates each selected entry on all 32 concrete row inputs and requires ordinary chi and the requested output polarity. The 1,024-entry C and Python tables have the same FNV-1a checksum `c8fa4bd9170966dc`.

The generator then builds all 512 S3-04 trials without annealing and retains the lowest eight counts. Each retained trial runs deterministic one-round-lookahead annealing for 200,000,000 iterations per planned round. A state move flips one C complement, one D complement, or an output-polarity subset. Current and lookahead row costs come from the verified chained table. The objective is 16 times current exact row cost plus 3 times the next-round lower bound. For `x = -3.1780538303479458*i/200000000`, the declared temperature is `19.2*E(x)`, where `E(x) = (1+y+y^2/2+y^3/6+y^4/24)^64` and `y=x/64`; acceptance uses the same deterministic bounded exponential. Ties retain the earlier deterministic choice. That campaign ran at nr = 20, where trial 1333 wins with 118445 operations. This package reuses the resulting frozen plan at nr = 6 without re-running the search: plan rows `FG 2` through `FG 5` are live, rows `FG 6` through `FG 19` are inert and are never read by the emitter, and round 5 becomes the last round, so its complement masks and chi decisions were searched in a non-last-round context. The masks are representation choices and the emitter compensates polarity symbolically, so the circuit is correct at this nr: the self-test re-derives PD and every hash, and the organizer experiment checks two chained bit-sliced steps against scalar selected-round Keccak. It is not plan-optimal, and a fresh search at this nr would likely emit fewer operations. The operation count stated in Section 3 above is this package's own emitted count, not trial 1333's nr = 20 count. Lowest-free allocation and the two-address packer then emit the frozen program. The charged ledger below totals the chained-table build and verification, every cheap build, every TOPK process, every annealing move, and the separate emitter, hashing and verification work.

## 4. Search, table, and controller

The attempt starts 256 walks from `rho + trail_number`. It advances all walks through the step, applies a 15-OR prefilter, and handles exact distinguished points with probability `630 * 2^-121`. The table has 16488 256-bit words and 82440 slots. Each word has five 51-bit slots: written bit followed by 50 endpoint bits. The word and slot position encode the trail number, so no trail number is stored in a slot. The 256 live walks use one packed word apiece: low 128 bits are the start step and high 128 bits are the positional trail number.

On a prefilter hit, 256 stores copy the carried planes to a scratch matrix. Charged indexed loops gather or replace one lane; 256 fixed loads restore the planes. A matching endpoint starts the final replay. Replay measures the stored trail while keeping every `G = ceil(LRC/(S-1)) = 2687423885757092749185025704247`-th point in the now-free table, advances the other trail to alignment, locates the merge segment by checkpoints, then lock-steps only that segment. With `e = C+29 = 1655`, at most one replay costs `(2e+17)LRC + (3e+20)G + 17*nck + e + 93 = 147424640958166104101746264353840690602` operations.

The assembled controller and handlers have the H_code size and hash stated in Section 3.6. Their register-register, immediate, compare, branch, jump, load, store and random-word instructions each contribute their explicit word operation; PERM contributes C. The step peaks at register 1928; the controller places its first persistent register at 1929 and declares 1940 words, so the lifetimes do not overlap. The controller permits at most HMAX = 49488991847959593483692939797331969 prefilter hits and aborts on hit 49488991847959593483692939797331970; that exact abort value is a checked controller literal and the input to F5 below.

Setup initializes `remaining = Tb = 1326445901334107559259970314262544384`. Every continuation path executes `remaining -= 1`, branches to the step only while the result is nonzero, and otherwise reaches HALT. The exact-byte experiment starts `remaining` at three, supplies only no-DP prefilter results, requires exactly two back-edges, and then requires the charged-limit HALT. Thus every path stops by the batch bound or at an earlier charged halt.

## 5. Exact operation and memory ledgers

`BSTEP = 26508 + 15 + 2 + 2 = 26527`. The added terms are the emitted prefilter ORs, its compare and branch, then the count-down subtract and conditional back-edge. Main work is `35186630424689871224489232526442514874368`, this package's own `Tb * BSTEP`. Replay is `147424640958166104101746264353840690602`, the closed form of Section 4 evaluated at this round's `e = C + 29 = 1655`. The hit, DP, probe, restart, setup, cap and final-halt paths contribute `6582035915778625933331161026038489389` and preprocessing contributes `184030978853888`; those two terms are carried from the r20 package and Section 9 shows that each bounds this package's own figure. Their sum is N above.

| preprocessing phase | class | word operations |
|---|---|---:|
| 512-trial cheap constant scan | word operations | 2199023255552 |
| eight sequential full graph campaigns | word operations | 67276367724544 |
| eight sequential annealing campaigns | word operations | 111411200000000 |
| chained row-table candidate evaluations in ten sequential processes | word operations | 1300234240 |
| chained row-table exhaustive truth checks in ten sequential processes | word operations | 83886080 |
| row-table setup and deterministic selection | word operations | 10485760 |
| constant derivation and comparisons | word operations | 524288 |
| structured affine basis | word operations | 16777216 |
| native parameter scan bins and fixed work | word operations | 3074137325568 |
| normative step, prefilter and controller emission | word operations | 30582272 |
| streaming SHA-256 of basis, step and controller | word operations | 56950784 |
| construction-time step parsing, field, and ledger verification | word operations | 31630848 |
| exact Decimal certificate and package rendering | word operations | 68719476736 |

The search memory is:

| region | bytes |
|---|---:|
| step program (H_code) | 95210 |
| prefilter (H_code) | 49 |
| other code and literal pool (H_code) | 8400 |
| register file | 62080 |
| table | 527616 |
| transpose scratch | 8192 |
| packed walk words | 8192 |
| data image | 512 |
| online stack | 0 |
| replay checkpoints (alias table) | 0 |
| **search total** | **710251** |

The online controller uses link registers and zero stack. Replay checkpoints alias the table after a match, when the ordinary endpoint table is no longer needed. Construction phases run sequentially before the search; their measured memory ledger follows the search table and their lifetimes do not overlap it.

| sequential construction phase | image bytes | stack reserve | measured VmHWM | retained input/output | charged peak |
|---|---:|---:|---:|---:|---:|
| 512-trial cheap scan | 329527 | 262144 | 417792 | 18432 | 610103 |
| TOPK full build 1 | 329527 | 262144 | 417792 | 51625 | 643296 |
| TOPK full build 2 | 329527 | 262144 | 413696 | 51625 | 643296 |
| TOPK full build 3 | 329527 | 262144 | 413696 | 51625 | 643296 |
| TOPK full build 4 | 329527 | 262144 | 417792 | 51625 | 643296 |
| TOPK full build 5 | 329527 | 262144 | 417792 | 51625 | 643296 |
| TOPK full build 6 | 329527 | 262144 | 417792 | 51625 | 643296 |
| TOPK full build 7 | 329527 | 262144 | 413696 | 51625 | 643296 |
| TOPK full build 8 | 329527 | 262144 | 413696 | 51625 | 643296 |
| structured-basis file verification | 9766 | 16384 | 32768 | 22999 | 55767 |
| native finite parameter scan | 12286 | 16384 | 28672 | 73 | 28745 |
| streaming native step emission | 423581 | 98304 | 438272 | 413080 | 934965 |
| streaming step SHA-256 | 9766 | 16384 | 24576 | 413080 | 439230 |
| construction-time step parsing, field, and ledger verification | 9298 | 16384 | 24576 | 413080 | 438762 |
| native 15-OR prefilter emission | 8254 | 16384 | 24576 | 49 | 24687 |
| streaming prefilter SHA-256 | 9766 | 16384 | 28672 | 49 | 28721 |
| native8 controller emission | 50645 | 16384 | 57344 | 8400 | 75429 |
| streaming controller SHA-256 | 9766 | 16384 | 28672 | 8400 | 37072 |

Every phase ran alone under `prlimit --as=1048576` and its listed stack cap. The charged peak is `max(VmHWM,image+stack)+retained input/output`; this deliberately charges an entire generated program even though the emitters stream it. Construction peaks at 934965 bytes, measured on the r20 emission of the inherited campaign; this package's straight line is smaller, so that row bounds it. Search peaks at 710251 bytes. The claimed peak is their maximum, 710251 bytes.

## 6. Probability space, H1, and success

The real attempt samples one uniform 256-bit rho. Everything afterward is deterministic. H1 is the following single aggregate comparison:

H1 is one premise. Let A_g be this bounded attempt on the fixed deterministic walk g. In the real algorithm's probability space, only the fresh uniform word r is random. Let F be a uniformly random function on 256-bit values, independent of r, and let P_F = Pr_(r,F)[A_F succeeds] for the same attempt with each g evaluation replaced by lazy sampling from F. H1 asserts only the aggregate comparison Pr_r[A_g succeeds] >= P_F. Appendix A proves P_F >= 0.39. The following clauses are properties of comparator F used by that proof, not additional premises about g: outputs at distinct fresh inputs are uniform and independent; its iterates have the random-mapping first-collision law; a fresh output satisfies the exact distinguished-point predicate with its stated probability independently of prior collision bookkeeping; and after any lazy-sampling history, a fresh input maps to any fixed earlier output with probability 2^-256. H1 assigns no per-history conditional probability to deterministic g because the history determines r and hence all later g outputs. The aggregate success comparison is the only heuristic step.

### Lazy-sampling order and first coincidence

Let `M = 2^256`, `L = 256`, `theta = 630 / 2^121`, `q = 1-theta`, and `E = L*Tb`. Comparator F starts undefined. Evaluations are ordered first by batch and then by lane. A fresh input is one not queried earlier in that order; it receives a new independent uniform image and stores it. A repeated input returns its stored image and consumes no new random value. For bookkeeping, attach an independent candidate image `V_t` to every evaluation position and use it exactly when that position's input is fresh. Its DP indicator is Bernoulli(theta), independently across t.

This also proves the restart domination used by F2. A fresh-input DP uses one Bernoulli indicator. A DP returned at a repeated input was already the endpoint of the earlier trail that first exposed it, so the table lookup finds that record and enters replay instead of consuming a new trail number. Thus the number of DP restarts is at most the number of DP indicators among `V_1..V_E`.

Outside the start part of F4, every queried input before the first image coincidence is fresh. If the first m images are distinct, the next fresh uniform image avoids them with probability `1-m/M`. Hence `pi_e = product_(m=0)^(e-1)(1-m/M)` is the exact no-coincidence probability through e fresh evaluations, and the first coincidence is a stopping time with mass `pi_(e-1)*(e-1)/M = pi_(e-1)-pi_e`. In particular `1-pi_e >= B(e) = 1-exp(-e(e-1)/(2M))`, using `1-x <= exp(-x)` term by term. No independence is asserted for the fixed target g.

### Conditional DP-tail lemma

Suppose the first coincidence occurs at evaluation t with earlier partner s. The two trails then follow a common functional-graph path. Let l be the number of further evaluations on that path before its first DP. Without conditioning on firstness, `Pr[l>=j]=q^j`. Firstness reveals that the preceding images were distinct, so the following comparison controls the conditioning rather than assuming independence.

Given the first `m=t-1` DP indicators, with fewer than U ones outside F2, images are uniform within the `theta*M` DP values and the `(1-theta)*M` non-DP values. Comparing their without-replacement products with `pi_m` bounds the relative deviation by

`Delta = U*E/M + E^2*theta/(2M) + U^2/(2*theta*M) = 4.8359525202541534942256638908983861189812216092296326327469927043306618689838140446698686739029671634505904273141193730875134601124695369175502232142857142857142857142857142857142857142857142857142857E-34`.

Appendix A checks `Delta < 2^-109`. The upper product ratio is `(1-E/M)^(-U) = 1.0000000000000000000000000000000002417623121883373883523121065861231479941112815674869928863810458190162276186634375402114863411630772211512665212377381081531418584113949255108916440248011359197646072` and the Bayes ratio is at most `R=(1-E/M)^(-U)/(1-Delta) = 1.0000000000000000000000000000000007253575642137527377748784956759621106717075169816032968875288411101453066137556446764280627573300624436159937317896489962949806680099993161223792475321929788645303965 <= 1+2^-108`. This requires the checked nonempty DP and non-DP partitions and `E/M <= 1/2`.

The Bayes calculation uses a masked filtration: it reveals the equality structure and the indicators of other walks but integrates over the DP indicators on the suffix currently selected by the common path. This is a probability calculation over comparator F; the operational run may already have exposed that suffix.

For the base case, write the first coincidence as `V_t=V_s`, `s<t`, with s on the older walk A. Evaluations of one continuing lane occur 256 indices apart. Therefore A evaluates each later common-path point first: its relevant indices are `s+256, s+2*256, ...`, all before B reaches the same respective points at `t+256, t+2*256, ...`. The tail length l is the first `k>=1` with `xi_(s+256k)=1`. For every fixed completion of these suffix indicators, the equality `V_t=V_s` has probability exactly `1/M`; fresh `V_t` is uniform after `V_s` is fixed. The event that `(t,s)` is the first pair differs between indicator completions only through D, the distinctness of `V_1..V_(t-1)`. The product bounds above place `Pr[D | indicators]` between `pi_m*(1-Delta)` and `pi_m*(1-E/M)^(-U)`. Bayes' formula thus bounds the conditional law of A's masked suffix by R times its iid Bernoulli(theta) law, proving `Pr[l>=j | first pair (t,s), masked history] <= R*q^j`.

The induction invariant is the same likelihood-ratio bound R for the masked suffix of the older trail at every later merge. Suppose the common path enters a point p whose continuation belongs to a third trail C, first evaluated at index u. The filtration records p and the merge equality but withholds the indicators `xi_(u+256), xi_(u+2*256), ...` of C's selected continuation. At the fresh evaluation that created the merge, equality with fixed p has conditional probability exactly `1/M` for every completion of those withheld indicators. That common factor cancels in Bayes' numerator and denominator. No new firstness event is imposed after `(t,s)`, so the distinct-prefix ratio R is not multiplied. This proves the inductive step. Repeating it over every merge preserves `Pr[l>=j] <= R*q^j`; a DP ends the path and can only shorten l.

The excess `R-1 <= 2^-108` adds at most `2^-108` to a bin sum whose weights total at most one and at most `2^-108*F6` to the replay-tail subtraction. These enter once as `FL = 2^-108*(1+F6)`. This product-comparison and masked-suffix argument follows the structure published by credited entry `20eb70ca-366a-4fbd-9594-4fa85f158a0b` and is re-derived here with this package's U, E, theta and LRC.

For bin `j = 1..J`, the common tail l lies in `((j-1)W,jW]` with iid reference mass `q^((j-1)W)-q^(jW)`. Put `n_j = L*(Tb-jW)`. If the first coincidence occurs among those `n_j` positions, the tail finishes by the deadline. The covered term is therefore

`Pcov = sum_(j=1)^J (q^((j-1)W)-q^(jW))*B(n_j)`.

Here `J = 69905`, `W = 633825300114114700748351602688`, and `J*W = LRC = 44307557604477188155813518785904640`. The experiment asserts that equality and recomputes every term in order.

### Failure bounds F2 through F6

F1 is the covered event counted by `Pcov`. The remaining named terms are upper bounds subtracted from it.

- F2, table exhaustion. The restart domination above gives `X <= Binomial(E,theta)` with mean `mu = E*theta = 80471.219251155853271484375000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`. Starting the `(U-L+1)`-st replacement trail needs at least `k=U-L=82184` such fresh DP outputs. For `k>mu`, the exponential-moment Chernoff bound is `Pr[X>=k] <= exp(-mu+k*(1+ln(mu/k)))`. Appendix A asserts its strict precondition.
- F3, a coincidence within one trail. If a trail has geometric length A, then a union bound over its input pairs is `A*(A-1)/(2M)`. Since `E[A*(A-1)/2]=q/theta^2 <= 1/theta^2`, at most U trails contribute `F3=U/(theta^2*M)`.
- F4, starts/replay boundaries and endpoint aliases. The U starts are fixed distinct translations of rho. Comparing them with at most E exposed inputs and images, plus the four selected replay boundary values, gives the explicit union bound `2*U*(E+4)/M = 4.8352462437667477670462421317224623754419370582498990814927230813382754327931946096474217243136157821895862753833613701827336862869004353118121215130336462613549020765741460548339802905104534147540107E-34 <= 2^-90`. Replay otherwise re-evaluates already exposed trail points and creates no new F sample. For aliases, conditioning on the DP predicate leaves the low 50 stored bits uniform. Fewer than `U*(U-1)/2` pairs therefore contribute less than `U^2*2^-51`.
- F5, hit-cap abort. Let X' count steps in which at least one fresh input has a 16-bit-prefilter image. Conditional on every prior adaptive choice, its one-step probability is at most `1-(1-2^-16)^256 = 0.00389866021631819777212921699057604228934907591347168173766934280389107431763886868964603102771424503147662168070206359168124436875563141323855886959184928433004874414589474610857484934350677083543632 < 2^-8`. Outside F4, a hit not counted by X' requires a repeated input and therefore occurs only after the first coincidence. Outside F6 the attempt stops within LRC later steps, so `hits <= X'+LRC`. Abort at hit 49488991847959593483692939797331970 therefore requires `X' >= h-LRC = 5181434243482405327879421011427330`. For the supermartingale `exp(s*X'_t-(exp(s)-1)*t/256)`, multiplicative Chernoff with `mu'=Tb/256=5181429302086357653359259040088064.00000000` and `delta=9.536743164062500000000000003859938799502057693648455539806599680402885584762688388210490300376409036908642326109783193224630242747329317517912407024974779477769136700328977714010890654473991469E-7>2^-20` gives exponent `-mu'*delta^2/(2+delta) = -2356240125386426341793.5359356231991878161194442580232028034535217093261954979668872426316278284684093874687837187587059103902305952787444210257610465136849859332688481405455145756998361839143745607314`. This is below `-1000*ln(2)`, so F5 is safely rounded up to `2^-1000`.
- F6, replay-cap refusal for the first-collision pair. Define an evaluation's age as its position in its current trail. Before the first coincidence, `Pr[age>=a] <= q^(a-1)`. Put `g(a)=min(1,q^(LRC+1-a))`. Summation by parts gives `E[g(age)] <= q^LRC + LRC*theta*q^LRC = G6`, where `G6=0.00031667206278890493147751918392665261643025029051423959929495529161996152885454777106180254515383109569845280083703091648398449619236172968257429797443421883287732836229703531009720296887137848883417358`. For a first-collision pair with ages a and b, refusal is bounded by `g(max(a,b)) <= g(a)+g(b)`, producing `2*G6`. Given fewer than U DPs, the distinct-prefix conditioning costs `(1-E/M)^(-U)`. Summing first-collision mass telescopes because `(t-1)*pi_(t-1)/M=pi_(t-1)-pi_t`. Finally `ln(1-x)>=-x-x^2` for `0<=x<=1/2` gives `1-pi_E <= 1-exp(-E^2/(2M)-E^3/(3M^2)) = 0.39219986422859216320962855998398785803227971663134774250643564775962471000143379649294346888946237469869803372998891745365223677793563949099743849731381176095656876178781085455829312578928410618143810`. Hence `F6=2*G6*(1-exp(-E^2/(2M)-E^3/(3M^2)))*(1-E/M)^(-U)`.

The conditioning lemma contributes `2^-108*(1+F6)` after the same lazy-sampling exposure, and `2^-60` covers all numerical approximation and bin-boundary rounding. A union bound gives

`P_F >= Pcov - F2 - F3 - 2^-90 - U^2/2^51 - F5 - F6 - 2^-108*(1+F6) - 2^-60`.

Every exponential and logarithm is evaluated with 200-digit Decimal arithmetic. The certificate counts at most 4478016 final-scale rounded operations. Recurrence multipliers lie in `[0,1]`; all other probability-scale intermediates are below four; integer products through `E^2` are exact and the only larger power is divided by `M^2`. The subtraction `q=1-theta` has absolute error below `1e-199`; on the live domain `q>1/2`, logarithm propagation and multiplication by `LRC<1e36` remain below `2e-163`. The audited `1e-140` final-scale allowance per counted operation is therefore conservative. Its accumulated bound is `4.478016E-134 < 2^-200`, strictly below the subtracted `2^-60` numerical term. Appendix A records 200-digit values and outward intervals by moving every endpoint one representable value outward. Its computed comparator-F bound is `0.39000000100893169635571528749243769938549682679120376397273046820937097830053366886552323272984604902280450211507298764194915861683568901882430340090679603824923948337297548455813900594513814919182329`, a margin of `1.00893169635571528749243769938549682679120376397273046820937097830053366886552323272984604902280450211507298764194915861683568901882430340090679603824923948337297548455813900594513814919182329E-9` above 0.39. The outward-rounded lower endpoint is `0.39000000100893169635571528749243769938549682679120376397273046820937097830053366886552323272984604902280450211507298764194915861683568901882430340090679603824923948337297548455813900594513814919182328 >= 0.39`; the preceding allowed Tb grid point is `0.38999999988001382652894024974508532215440647359061991312544547090451464667561690534994773597454350304807242064782681088349536179823691528039343902551835580590058295390677655147066760098685970719551153 < 0.39`.

Support for H1 is positive and specific. The algorithm is the parallel collision search of Paul C. van Oorschot and Michael J. Wiener, "Parallel Collision Search with Cryptanalytic Applications", Journal of Cryptology 12(1):1-28, 1999, DOI 10.1007/PL00003816. Generic entries in this track use the same random-function premise. The six-lane affine embedding separates circuit savings from the generic collision law. A collision-hazard deficit can be priced by scaling the comparator hazard and rerunning Appendix A. The emitted-program, scalar target, table, restart and replay checks test consistency of the exact program used by the ledger.

## 7. Organizer experiments

`experiments/compact.py` contains compressed source text, not prebuilt program bytes. It invokes the step emitter and controller emitter, checks their counts, lengths and hashes, parses the exact emitted streams as experiment tooling, and executes the reconstructed programs. It tests the upper and rejected boundaries of every 11-bit step field, every 8-byte-code register and 25-bit immediate/literal field, the literal pool, all five 51-bit slots, and the first invalid table position. It checks two chained bit-sliced steps against scalar selected-round Keccak, evalF against scalar g, gather/setwalk, all slot probe positions, restart packing, replay success, replay refusal, and the all-no-DP limit halt. The `success-certificate` experiment also recomputes Appendix A at 200-digit precision. Each response row returns the same projected pair derived from the first request seed. The projection probe evaluates 512 seed-derived points and returns the first pair whose chain images agree on the declared 12-bit mask; the birthday expectation is 512*511/2/4096 = 31.9, so a pair is found with probability above 1 - 2^-45 and the sentence above holds for effectively every organizer seed. This probe is a scaled-down demonstration of the chain and the masked event, not a measurement of the attack: the full search is the Tb-step distinguished-point run priced in Section 5.

## 8. Credit

This is a credited derivative of `fe76bfc4-6a5b-4883-b428-50796e22c9a3`, the direct round-20 incumbent. `20eb70ca-366a-4fbd-9594-4fa85f158a0b` supplies the wider one-round-lookahead S3-04 generator, lowest-free allocation, two-address encoding, positional five-slot table, one-word walk and checkpoint replay; for round 10 it is also the direct incumbent and is credited only once. `d258ba65-054d-4098-bbac-0b974fee36c8` supplies the chained-chi identity and pinned-output row minimization used at every round in this family. This package independently integrates that identity into the free C/D lookahead search and exhaustively verifies its own table. It also credits `3509abf0-ecab-457b-8d5d-ea8aec5d5e8c` for the structured-constant lineage and `911bffce-8e7a-4502-90ab-c69a473fff48` for our compact-controller lineage. Credit is not an endorsement and none of those authors reviewed this package.

## Appendix A. Outward-rounded success certificate

```json
{
  "computed_bound": "0.39000000100893169635571528749243769938549682679120376397273046820937097830053366886552323272984604902280450211507298764194915861683568901882430340090679603824923948337297548455813900594513814919182329",
  "computed_previous": "0.38999999988001382652894024974508532215440647359061991312544547090451464667561690534994773597454350304807242064782681088349536179823691528039343902551835580590058295390677655147066760098685970719551153",
  "covered_success": {
    "lower": "0.39026410805702264388024168816391629386521325955252999671897150378721582852899605728402154787948264219227102271210953848710526589534322817598325799789076806322889331607587475711881598826640465915542857",
    "upper": "0.39026410805702264388024168816391629386521325955252999671897150378721582852899605728402154787948264219227102271210953848710526589534322817598325799789076806322889331607587475711881598826640465915542859"
  },
  "failure_intervals": {
    "endpoint_alias": {
      "lower": "0.0000030181873000856285216286778450012207031249999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999",
      "upper": "0.0000030181873000856285216286778450012207031250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
    },
    "hit_cap_F5": {
      "lower": "9.3326361850321887899008954472381716961709144637170802462171433979596691097577563445444032709788110235959498993032424262421548752135403239484152081720393075623441066613832515027399507598590183151110048E-302",
      "upper": "9.3326361850321887899008954472381716961709144637170802462171433979596691097577563445444032709788110235959498993032424262421548752135403239484152081720393075623441066613832515027399507598590183151110050E-302"
    },
    "lemma_conditioning": {
      "lower": "3.0822533448515148916196899124384346839659164097164955383001063496233598379080379206450709380789429643628351818586443157338372545444807376994334601834853146616378167422719216641231686356727380109414975E-33",
      "upper": "3.0822533448515148916196899124384346839659164097164955383001063496233598379080379206450709380789429643628351818586443157338372545444807376994334601834853146616378167422719216641231686356727380109414977E-33"
    },
    "numeric_rounding": {
      "lower": "8.6736173798840354720596224069595336914062499999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999E-19",
      "upper": "8.6736173798840354720596224069595336914062500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001E-19"
    },
    "replay_cap_F6": {
      "lower": "0.00024839748006159345339076688438166839005899097330434186624086613215455955100887153697241887437598705662887424323276502344096440167034952401407131633108251234454081687480021672312260948439635925184666765",
      "upper": "0.00024839748006159345339076688438166839005899097330434186624086613215455955100887153697241887437598705662887424323276502344096440167034952401407131633108251234454081687480021672312260948439635925184666767"
    },
    "self_coincidence_F3": {
      "lower": "0.000012677597080498866213151927437641723356009070294784580498866213151927437641723356009070294784580498866213151927437641723356009070294784580498866213151927437641723356009070294784580498866213151927437641",
      "upper": "0.000012677597080498866213151927437641723356009070294784580498866213151927437641723356009070294784580498866213151927437641723356009070294784580498866213151927437641723356009070294784580498866213151927437643"
    },
    "start_replay_collision": {
      "lower": "8.0779356694631608874161005084957309918536338955163955688476562499999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999E-28",
      "upper": "8.0779356694631608874161005084957309918536338955163955688476562500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001E-28"
    },
    "table_exhaustion_F2": {
      "lower": "1.3783648768709039114385614086739975126765272066619390765612491007771762520145212900874126402254133525163955703109053707924802532013382525770124003747942926811734390552082586307023342299743088913226467E-8",
      "upper": "1.3783648768709039114385614086739975126765272066619390765612491007771762520145212900874126402254133525163955703109053707924802532013382525770124003747942926811734390552082586307023342299743088913226469E-8"
    }
  },
  "hit_abort": 49488991847959593483692939797331970,
  "hit_limit": 49488991847959593483692939797331969,
  "key_bits": 50,
  "margin_above_target": "1.00893169635571528749243769938549682679120376397273046820937097830053366886552323272984604902280450211507298764194915861683568901882430340090679603824923948337297548455813900594513814919182329E-9",
  "parameters": {
    "DK": 10,
    "DPLO": 145,
    "DT": 630,
    "HF": 111,
    "HIT_ABORT": 49488991847959593483692939797331970,
    "HMAX": 49488991847959593483692939797331969,
    "J": 69905,
    "LRC": 44307557604477188155813518785904640,
    "NR": 20,
    "PFLO": 240,
    "PFN": 16,
    "S": 16488,
    "SB": 15,
    "Tb": 1326445901334107559259970314262544384,
    "U": 82440,
    "W": 633825300114114700748351602688
  },
  "preconditions": {
    "available_gt_mean": true,
    "bins_cover_replay_cap": true,
    "conditioning_delta_lt_2^-109": true,
    "conditioning_ratio_le_1_plus_2^-108": true,
    "dp_partition_nonempty": true,
    "evaluation_fraction_le_half": true,
    "fresh_hit_delta_gt_2^-20": true,
    "fresh_hit_threshold_gt_mean": true,
    "fresh_step_probability_lt_2^-8": true,
    "hit_threshold_equals_abort_minus_lrc": true,
    "replay_cap_below_deadline": true,
    "start_replay_bound_le_2^-90": true,
    "table_has_initial_walks": true
  },
  "probability_inputs": {
    "age_g6": "0.00031667206278890493147751918392665261643025029051423959929495529161996152885454777106180254515383109569845280083703091648398449619236172968257429797443421883287732836229703531009720296887137848883417358",
    "available_restarts": 82184,
    "coincidence_upper": "0.39219986422859216320962855998398785803227971663134774250643564775962471000143379649294346888946237469869803372998891745365223677793563949099743849731381176095656876178781085455829312578928410618143810",
    "conditioning_delta": "4.8359525202541534942256638908983861189812216092296326327469927043306618689838140446698686739029671634505904273141193730875134601124695369175502232142857142857142857142857142857142857142857142857142857E-34",
    "conditioning_dp_term": "1.2383859224625986893939656578934064069517807235807262844619732903136569543026520737579890659877232142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857E-34",
    "conditioning_inflation": "1.0000000000000000000000000000000002417623121883373883523121065861231479941112815674869928863810458190162276186634375402114863411630772211512665212377381081531418584113949255108916440248011359197646072",
    "conditioning_partition_term": "1.1799434759081809213085771671437485243369509859512362481353319072506377959102767888899338272536902226333109522382613931767991743981838226318359375E-34",
    "conditioning_ratio": "1.0000000000000000000000000000000007253575642137527377748784956759621106717075169816032968875288411101453066137556446764280627573300624436159937317896489962949806680099993161223792475321929788645303965",
    "conditioning_start_term": "2.417623121883373883523121065861231187692489899697670100149687506766367118770885182021945780661553726531565189361572265625E-34",
    "evaluations": 339570150741531535170552400451211362304,
    "fresh_hit_delta": "9.536743164062500000000000003859938799502057693648455539806599680402885584762688388210490300376409036908642326109783193224630242747329317517912407024974779477769136700328977714010890654473991469E-7",
    "fresh_hit_mean_upper": "5181429302086357653359259040088064.00000000",
    "fresh_hit_threshold": 5181434243482405327879421011427330,
    "fresh_step_probability_exact": "0.00389866021631819777212921699057604228934907591347168173766934280389107431763886868964603102771424503147662168070206359168124436875563141323855886959184928433004874414589474610857484934350677083543632",
    "fresh_step_probability_upper": "0.00390625",
    "hit_chernoff_exponent": "-2356240125386426341793.5359356231991878161194442580232028034535217093261954979668872426316278284684093874687837187587059103902305952787444210257610465136849859332688481405455145756998361839143745607314",
    "mean_dp": "80471.219251155853271484375000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "prefilter_bits": 16,
    "start_replay_union_bound": "4.8352462437667477670462421317224623754419370582498990814927230813382754327931946096474217243136157821895862753833613701827336862869004353118121215130336462613549020765741460548339802905104534147540107E-34",
    "theta_denominator_bits": 121,
    "theta_numerator": 630
  },
  "round": 20,
  "rounding": "200-digit Decimal; every interval moved one representable value outward",
  "rounding_audit": {
    "accumulated_absolute_bound": "4.478016E-134",
    "accumulated_lt_2^-200": true,
    "charged_numeric_term": "8.67361737988403547205962240695953369140625E-19",
    "operation_bound": 4478016,
    "per_operation_absolute_bound": "1E-140",
    "precision_digits": 200
  },
  "schema": "hashsmash-random-function-success-v1",
  "target": "0.39",
  "trails": 82440,
  "union_lower": "0.39000000100893169635571528749243769938549682679120376397273046820937097830053366886552323272984604902280450211507298764194915861683568901882430340090679603824923948337297548455813900594513814919182328"
}
```

## Appendix B. Bounded construction sources

These are the complete sources used for the measured sequential phases in Section 5. They use no participant executable. The freestanding binaries were linked without libc.

### freestanding_runtime.c

```c
/* Minimal x86-64 Linux runtime for the charged construction binaries. */
#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long i64;
static i64 sc3(i64 n,i64 a,i64 b,i64 c){i64 r;__asm__ volatile("syscall":"=a"(r):"a"(n),"D"(a),"S"(b),"d"(c):"rcx","r11","memory");return r;}

__asm__(".global _start\n_start:\n xor %rbp,%rbp\n mov (%rsp),%rdi\n lea 8(%rsp),%rsi\n and $-16,%rsp\n call main\n mov %rax,%rdi\n mov $60,%rax\n syscall\n");

FILE *stdin=(FILE*)1,*stdout=(FILE*)2,*stderr=(FILE*)3;
int errno;

static int fdof(FILE *f){return (int)(intptr_t)f-1;}
static FILE *fileof(int fd){return (FILE*)(intptr_t)(fd+1);}
static long write_all(int fd,const void *data,size_t length){
    const unsigned char *p=data;size_t done=0;
    while(done<length){long n=sc3(1,fd,(i64)(p+done),(i64)(length-done));if(n<=0)return -1;done+=(size_t)n;}
    return (long)done;
}

long construction_vmhwm_bytes(void){
    static char status[4096];long fd=sc3(2,(i64)"/proc/self/status",0,0);if(fd<0)return -1;
    long n=sc3(0,fd,(i64)status,sizeof(status)-1);sc3(3,fd,0,0);if(n<=0)return -1;status[n]=0;
    for(long i=0;i+6<n;i++)if(status[i]=='V'&&status[i+1]=='m'&&status[i+2]=='H'&&status[i+3]=='W'&&status[i+4]=='M'){
        long j=i+5;while(status[j]==' '||status[j]=='\t'||status[j]==':')j++;long value=0;
        while(status[j]>='0'&&status[j]<='9')value=value*10+(status[j++]-'0');return value*1024;
    }
    return -1;
}

long construction_read_file(const char *path,void *buffer,size_t capacity){
    long fd=sc3(2,(i64)path,0,0);if(fd<0)return -1;size_t used=0;
    while(used<capacity){long n=sc3(0,fd,(i64)((unsigned char*)buffer+used),(i64)(capacity-used));if(n<0){sc3(3,fd,0,0);return -1;}if(!n)break;used+=(size_t)n;}
    sc3(3,fd,0,0);return (long)used;
}

void *memset(void *d,int c,size_t n){unsigned char *p=d;while(n--)*p++=(unsigned char)c;return d;}
void *memcpy(void *d,const void *s,size_t n){unsigned char *p=d;const unsigned char *q=s;while(n--)*p++=*q++;return d;}
int memcmp(const void *a,const void *b,size_t n){const unsigned char *p=a,*q=b;while(n--){if(*p!=*q)return *p-*q;p++;q++;}return 0;}
size_t strlen(const char *s){const char *p=s;while(*p)p++;return (size_t)(p-s);}
int strcmp(const char *a,const char *b){while(*a&&*a==*b){a++;b++;}return (unsigned char)*a-(unsigned char)*b;}
char *getenv(const char *name){(void)name;return 0;}
int atoi(const char *s){int v=0;while(*s>='0'&&*s<='9')v=v*10+(*s++-'0');return v;}
long strtol(const char *s,char **end,int base){long v=0;(void)base;while(*s>='0'&&*s<='9')v=v*10+(*s++-'0');if(end)*end=(char*)s;return v;}

FILE *fopen(const char *path,const char *mode){
    int flags=(mode&&mode[0]=='r')?0:(1|64|512);long fd=sc3(2,(i64)path,flags,0644);
    return fd<0?0:fileof((int)fd);
}
int fclose(FILE *f){return (int)sc3(3,fdof(f),0,0);}
int fflush(FILE *f){(void)f;return 0;}
size_t fwrite(const void *p,size_t size,size_t count,FILE *f){size_t n=size*count;return write_all(fdof(f),p,n)<0?0:count;}
size_t fread(void *p,size_t size,size_t count,FILE *f){size_t want=size*count,done=0;while(done<want){long n=sc3(0,fdof(f),(i64)((unsigned char*)p+done),(i64)(want-done));if(n<=0)break;done+=(size_t)n;}return size?done/size:0;}
int fputc(int c,FILE *f){unsigned char b=(unsigned char)c;return write_all(fdof(f),&b,1)<0?EOF:c;}
int fgetc(FILE *f){unsigned char b;long n=sc3(0,fdof(f),(i64)&b,1);return n==1?b:EOF;}

static void emit_char(char **dst,size_t *left,FILE *f,char c,int *total){
    if(dst){if(*left>1){**dst=c;(*dst)++;(*left)--;}}
    else fputc((unsigned char)c,f);
    (*total)++;
}
static void emit_text(char **dst,size_t *left,FILE *f,const char *s,int *total){while(*s)emit_char(dst,left,f,*s++,total);}
static void emit_uint(char **dst,size_t *left,FILE *f,unsigned long long v,unsigned base,int width,int zero,int *total){
    char buf[32];int n=0;do{unsigned d=(unsigned)(v%base);buf[n++]=(char)(d<10?'0'+d:'a'+d-10);v/=base;}while(v);
    while(n<width){emit_char(dst,left,f,zero?'0':' ',total);width--;}
    while(n)emit_char(dst,left,f,buf[--n],total);
}
static int vformat(char *out,size_t cap,FILE *f,const char *fmt,va_list ap){
    char *dst=out;size_t left=cap;int total=0;
    while(*fmt){
        if(*fmt!='%'){emit_char(out?&dst:0,out?&left:0,f,*fmt++,&total);continue;}
        fmt++;if(*fmt=='%'){emit_char(out?&dst:0,out?&left:0,f,*fmt++,&total);continue;}
        int zero=0,width=0,longness=0;if(*fmt=='0'){zero=1;fmt++;}while(*fmt>='0'&&*fmt<='9')width=width*10+(*fmt++-'0');
        if(*fmt=='z'){longness=1;fmt++;}else if(*fmt=='l'){longness=1;fmt++;if(*fmt=='l'){longness=2;fmt++;}}
        char kind=*fmt++;if(kind=='s'){emit_text(out?&dst:0,out?&left:0,f,va_arg(ap,const char*),&total);}
        else if(kind=='c'){emit_char(out?&dst:0,out?&left:0,f,(char)va_arg(ap,int),&total);}
        else if(kind=='d'||kind=='i'){
            long long v=longness?va_arg(ap,long):va_arg(ap,int);if(v<0){emit_char(out?&dst:0,out?&left:0,f,'-',&total);v=-v;}emit_uint(out?&dst:0,out?&left:0,f,(unsigned long long)v,10,width,zero,&total);
        }else if(kind=='u'||kind=='x'){
            unsigned long long v=longness?va_arg(ap,unsigned long):va_arg(ap,unsigned int);emit_uint(out?&dst:0,out?&left:0,f,v,kind=='x'?16:10,width,zero,&total);
        }else{emit_char(out?&dst:0,out?&left:0,f,'?',&total);}
    }
    if(out&&cap){*dst=0;}
    return total;
}
int fprintf(FILE *f,const char *fmt,...){va_list ap;va_start(ap,fmt);int n=vformat(0,0,f,fmt,ap);va_end(ap);return n;}
int printf(const char *fmt,...){va_list ap;va_start(ap,fmt);int n=vformat(0,0,stdout,fmt,ap);va_end(ap);return n;}
int snprintf(char *out,size_t cap,const char *fmt,...){va_list ap;va_start(ap,fmt);int n=vformat(out,cap,0,fmt,ap);va_end(ap);return n;}
void perror(const char *s){fprintf(stderr,"%s\n",s);}
char *strerror(int value){(void)value;return "runtime error";}
void exit(int code){sc3(60,code,0,0);for(;;){}}
void abort(void){exit(134);}

```

### plan_search_local.c

```c
#include <errno.h>
#include <inttypes.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Independent generator for the r24 S3-04 / look-ahead / eight-body step.
 *
 * The graph builder descends from our sha3-r6 generator.  The structured
 * constants and the high-level polarity and loop constructions are transcribed
 * from the public proofs, not from executable participant source.
 */

enum { O_IN = 0, O_XOR = 1, O_AND = 2, O_OR = 3, O_NOT = 4 };
enum {
    NC = -1,
    MAX_NODES = 9000,
    MAX_FORMS = 2048,
    CONS_SIZE = 1 << 14,
    FORM_SIZE = 1 << 12,
    NREG = 4096,
    PLAN_ROWS = 320,
    PLAN_BITS = 320,
};

typedef struct {
    uint8_t op;
    uint8_t k;
    int16_t a, b, lin;
} Node;

typedef struct {
    uint64_t mask[4];
    int node;
} Form;

typedef struct {
    int n;
    uint8_t p;
} Value;

typedef struct {
    uint8_t op;
    uint16_t d, a, b;
} Insn;

typedef struct {
    uint8_t subset;
    uint8_t tricks;
    uint8_t select_mask;
    uint8_t cost;
} Decision;

typedef struct {
    uint8_t cnot[PLAN_BITS];
    uint8_t dnot[PLAN_BITS];
    uint8_t target[PLAN_ROWS];
    uint64_t ib;
} Plan;

_Static_assert(sizeof(Decision) == 4, "Decision must have a stable byte encoding");
_Static_assert(sizeof(Plan) == 968, "Plan must have a stable byte encoding");

static Node nodes[MAX_NODES];
static Form forms[MAX_FORMS];
static uint16_t cons_table[CONS_SIZE];
static uint16_t form_table[FORM_SIZE];
static int node_count, form_count;
static Decision row_table[32][32];
static uint8_t row_min_cost[32];
static uint8_t row_min_target[32];

static const uint64_t RC[24] = {
    UINT64_C(0x0000000000000001), UINT64_C(0x0000000000008082),
    UINT64_C(0x800000000000808a), UINT64_C(0x8000000080008000),
    UINT64_C(0x000000000000808b), UINT64_C(0x0000000080000001),
    UINT64_C(0x8000000080008081), UINT64_C(0x8000000000008009),
    UINT64_C(0x000000000000008a), UINT64_C(0x0000000000000088),
    UINT64_C(0x0000000080008009), UINT64_C(0x000000008000000a),
    UINT64_C(0x000000008000808b), UINT64_C(0x800000000000008b),
    UINT64_C(0x8000000000008089), UINT64_C(0x8000000000008003),
    UINT64_C(0x8000000000008002), UINT64_C(0x8000000000000080),
    UINT64_C(0x000000000000800a), UINT64_C(0x800000008000000a),
    UINT64_C(0x8000000080008081), UINT64_C(0x8000000000008080),
    UINT64_C(0x0000000080000001), UINT64_C(0x8000000080008008),
};

static const int ROT[5][5] = {
    {0, 36, 3, 41, 18}, {1, 44, 10, 45, 2}, {62, 6, 43, 15, 61},
    {28, 55, 25, 21, 56}, {27, 20, 39, 8, 14},
};

/* S3-04 trial 1230.  Lanes 1, 4, 6 and 9 are overwritten by the point. */
static uint64_t KL[25] = {
    UINT64_C(0x0000000000000000), UINT64_C(0x0000000000000000),
    UINT64_C(0x2d58eceb83b21614), UINT64_C(0x0000000000000000),
    UINT64_C(0x0000000000000000), UINT64_C(0xffffffffffffffff),
    UINT64_C(0x0000000000000000), UINT64_C(0x0000000000000000),
    UINT64_C(0x0000000000000000), UINT64_C(0x0000000000000000),
    UINT64_C(0xffffffffffffffff), UINT64_C(0x8b563b3ae0ec8583),
    UINT64_C(0x0000000000000000), UINT64_C(0x85ab1d9d707642c2),
    UINT64_C(0xe953898a3e26f4f5), UINT64_C(0xffffffffffffffff),
    UINT64_C(0x8000000000000006), 0, 0, 0, 0, 0, 0, 0, 0,
};

static void fail(const char *msg) {
    fprintf(stderr, "gen_combined: %s\n", msg);
    exit(1);
}

static uint64_t read_u64_le(FILE *f) {
    uint8_t bytes[8];
    if (fread(bytes, 1, sizeof(bytes), f) != sizeof(bytes))
        fail("short constant record");
    uint64_t value = 0;
    for (int i = 0; i < 8; i++) value |= (uint64_t)bytes[i] << (8 * i);
    return value;
}

static void validate_kl(const uint64_t kl[25]) {
    static const int variable_lanes[4] = {1, 4, 6, 9};
    for (int i = 0; i < 4; i++) if (kl[variable_lanes[i]])
        fail("constant record overwrites a direct point lane");
    if (kl[16] != UINT64_C(0x8000000000000006))
        fail("constant record has invalid SHA3 padding lane");
    for (int lane = 17; lane < 25; lane++) if (kl[lane])
        fail("constant record has nonzero capacity lane");
}

static void load_kl_record(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) fail("cannot open constant record");
    for (int lane = 0; lane < 25; lane++) KL[lane] = read_u64_le(f);
    if (fgetc(f) != EOF || fclose(f)) fail("constant record has trailing data");
    validate_kl(KL);
}

static uint64_t mix64(uint64_t x) {
    x ^= x >> 30;
    x *= UINT64_C(0xbf58476d1ce4e5b9);
    x ^= x >> 27;
    x *= UINT64_C(0x94d049bb133111eb);
    return x ^ (x >> 31);
}

static uint64_t rng_next(uint64_t *state) {
    uint64_t x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *state = x;
    return x;
}

static uint64_t node_hash(int op, int a, int b) {
    return mix64((uint64_t)(uint32_t)op * UINT64_C(0x9e3779b97f4a7c15) ^
                 (uint64_t)(uint32_t)a * UINT64_C(0x85ebca77c2b2ae63) ^
                 (uint64_t)(uint32_t)b * UINT64_C(0x27d4eb2f165667c5));
}

static uint64_t form_hash(const uint64_t m[4]) {
    return mix64(m[0] ^ mix64(m[1]) ^ (m[2] << 1) ^ (m[2] >> 63) ^
                 (m[3] << 7) ^ (m[3] >> 57));
}

static int new_node(int op, int a, int b) {
    if (node_count >= MAX_NODES) fail("node capacity exceeded");
    int n = node_count++;
    nodes[n] = (Node){(uint8_t)op, 0, a, b, -1};
    return n;
}

static int cons_node(int op, int a, int b) {
    if (op != O_NOT && a > b) {
        int t = a;
        a = b;
        b = t;
    }
    size_t h = (size_t)node_hash(op, a, b) & (CONS_SIZE - 1);
    for (;;) {
        int e = cons_table[h];
        if (!e) break;
        int n = e - 1;
        if (nodes[n].op == op && nodes[n].a == a && nodes[n].b == b) return n;
        h = (h + 1) & (CONS_SIZE - 1);
    }
    int n = new_node(op, a, b);
    cons_table[h] = n + 1;
    return n;
}

static int mask_zero(const uint64_t m[4]) {
    return (m[0] | m[1] | m[2] | m[3]) == 0;
}

static int find_form(const uint64_t m[4]) {
    size_t h = (size_t)form_hash(m) & (FORM_SIZE - 1);
    for (;;) {
        int e = form_table[h];
        if (!e) return -1;
        int f = e - 1;
        if (!memcmp(forms[f].mask, m, sizeof(forms[f].mask))) return f;
        h = (h + 1) & (FORM_SIZE - 1);
    }
}

static int add_form(const uint64_t m[4], int node) {
    if (form_count >= MAX_FORMS) fail("linear-form capacity exceeded");
    int f = form_count++;
    memcpy(forms[f].mask, m, sizeof(forms[f].mask));
    forms[f].node = node;
    size_t h = (size_t)form_hash(m) & (FORM_SIZE - 1);
    while (form_table[h]) h = (h + 1) & (FORM_SIZE - 1);
    form_table[h] = f + 1;
    return f;
}

static Value val(int n, int p) { return (Value){n, (uint8_t)(p & 1)}; }
static Value constant(int p) { return val(NC, p); }

static Value xor_value(Value a, Value b) {
    if (a.n == NC) return val(b.n, b.p ^ a.p);
    if (b.n == NC) return val(a.n, a.p ^ b.p);
    if (a.n == b.n) return constant(a.p ^ b.p);
    int la = nodes[a.n].lin, lb = nodes[b.n].lin;
    if (la >= 0 && lb >= 0) {
        uint64_t m[4];
        for (int i = 0; i < 4; i++) m[i] = forms[la].mask[i] ^ forms[lb].mask[i];
        int k = nodes[a.n].k ^ nodes[b.n].k;
        if (mask_zero(m)) return constant(k ^ a.p ^ b.p);
        int f = find_form(m);
        if (f >= 0) {
            int n = forms[f].node;
            return val(n, k ^ a.p ^ b.p ^ nodes[n].k);
        }
        int n = cons_node(O_XOR, a.n, b.n);
        nodes[n].k = (uint8_t)k;
        nodes[n].lin = add_form(m, n);
        return val(n, a.p ^ b.p);
    }
    return val(cons_node(O_XOR, a.n, b.n), a.p ^ b.p);
}

static Value complement_representation(Value a) {
    if (a.n == NC) return a;
    int before = node_count;
    int n = cons_node(O_NOT, a.n, 0);
    if (node_count > before && nodes[a.n].lin >= 0) {
        nodes[n].lin = nodes[a.n].lin;
        nodes[n].k = nodes[a.n].k ^ 1;
    }
    return val(n, a.p ^ 1);
}

static Value and_value(Value a, Value b, int select_polarity) {
    if (a.n == NC) return a.p ? b : constant(0);
    if (b.n == NC) return b.p ? a : constant(0);
    if (a.n == b.n) return a.p == b.p ? a : constant(0);
    if (!a.p && !b.p) return val(cons_node(O_AND, a.n, b.n), 0);
    if (a.p && b.p) return val(cons_node(O_OR, a.n, b.n), 1);
    int A = !a.p ? a.n : b.n;
    int B = !a.p ? b.n : a.n;
    if (select_polarity) {
        Value na = complement_representation(val(A, 0));
        return val(cons_node(O_OR, na.n, B), 1);
    }
    int t = cons_node(O_AND, A, B);
    return xor_value(val(A, 0), val(t, 0));
}

static int term_cost(Value a, Value b) {
    if (a.n == NC || b.n == NC || a.n == b.n) return 0;
    return ((a.p ^ 1) == b.p) ? 1 : 2;
}

static void reset_graph(int inputs, int affine_inputs) {
    memset(cons_table, 0, sizeof(cons_table));
    memset(form_table, 0, sizeof(form_table));
    node_count = form_count = 0;
    for (int j = 0; j < inputs; j++) {
        int n = new_node(O_IN, 0, 0);
        if (affine_inputs) {
            uint64_t m[4] = {0, 0, 0, 0};
            if (j >= 256) fail("too many affine inputs");
            m[j >> 6] = UINT64_C(1) << (j & 63);
            nodes[n].lin = add_form(m, n);
        }
    }
}

static void choose_dynamic_row(const Value b[5], int need, int *subset, int *trick) {
    int distinct = 1;
    for (int x = 0; x < 5; x++) {
        if (b[x].n == NC) distinct = 0;
        for (int y = x + 1; y < 5; y++) if (b[x].n == b[y].n) distinct = 0;
    }
    int best_subset = -1, best_trick = -1, best_cost = 1 << 30;
    int jmax = distinct ? 5 : 0;
    for (int j = -1; j < jmax; j++) {
        if (j >= 0 && (!((need >> j) & 1) || !((need >> ((j + 1) % 5)) & 1))) continue;
        for (int s = 0; s < 32; s++) {
            Value bb[5];
            memcpy(bb, b, sizeof(bb));
            int cost = 0;
            for (int x = 0; x < 5; x++) if ((s >> x) & 1) {
                if (b[x].n == NC) cost = 1 << 29;
                else { bb[x].p ^= 1; cost++; }
            }
            for (int x = 0; x < 5; x++) if ((need >> x) & 1) {
                if (x == j) {
                    int k = (j + 1) % 5;
                    Value p1 = bb[(k + 1) % 5], p2 = bb[(k + 2) % 5];
                    if ((p1.p ^ 1) == p2.p) {
                        Value bk = bb[k];
                        bk.p ^= (p1.p ^ 1);
                        cost += term_cost(bk, bb[(x + 2) % 5]);
                    } else {
                        cost++;
                    }
                } else {
                    cost += term_cost(bb[(x + 1) % 5], bb[(x + 2) % 5]);
                }
            }
            if (cost < best_cost) {
                best_cost = cost;
                best_subset = s;
                best_trick = j;
            }
        }
    }
    *subset = best_subset;
    *trick = best_trick;
}

static void build_dynamic_row(Value b[5], int need, Value out[5]) {
    int subset, trick;
    choose_dynamic_row(b, need, &subset, &trick);
    for (int x = 0; x < 5; x++) if ((subset >> x) & 1)
        b[x] = complement_representation(b[x]);
    int k = (trick + 1) % 5;
    if (trick >= 0) {
        Value t = and_value(val(b[(k + 1) % 5].n, b[(k + 1) % 5].p ^ 1),
                            b[(k + 2) % 5], 0);
        out[k] = xor_value(b[k], t);
    }
    for (int x = 0; x < 5; x++) if ((need >> x) & 1) {
        if (trick >= 0 && x == k) continue;
        Value t1 = x == trick ? out[k] : b[(x + 1) % 5];
        Value t = and_value(val(t1.n, t1.p ^ 1), b[(x + 2) % 5], 0);
        out[x] = xor_value(b[x], t);
    }
}

static int sim_term(int pa, int pb, int select, int *pout) {
    if (pa == pb) {
        *pout = pa;
        return 1;
    }
    *pout = select;
    return 2;
}

static void make_row_table(void) {
    for (int pin = 0; pin < 32; pin++) {
        int min_cost = 255, min_target = 0;
        for (int target = 0; target < 32; target++) {
            Decision best = {0, 0, 0, 255};
            for (int subset = 0; subset < 32; subset++) {
                int bp[5];
                for (int x = 0; x < 5; x++) bp[x] = ((pin >> x) & 1) ^ ((subset >> x) & 1);
                for (int trick = -1; trick < 5; trick++) {
                    for (int sel = 0; sel < 32; sel++) {
                        int op[5] = {0, 0, 0, 0, 0};
                        int cost = __builtin_popcount((unsigned)subset);
                        int k = (trick + 1) % 5;
                        if (trick >= 0) {
                            int tp;
                            cost += sim_term(bp[(k + 1) % 5] ^ 1, bp[(k + 2) % 5],
                                             (sel >> k) & 1, &tp) + 1;
                            op[k] = bp[k] ^ tp;
                        }
                        for (int x = 0; x < 5; x++) {
                            if (trick >= 0 && x == k) continue;
                            int first = x == trick ? op[k] : bp[(x + 1) % 5];
                            int tp;
                            cost += sim_term(first ^ 1, bp[(x + 2) % 5],
                                             (sel >> x) & 1, &tp) + 1;
                            op[x] = bp[x] ^ tp;
                        }
                        int got = 0;
                        for (int x = 0; x < 5; x++) got |= op[x] << x;
                        if (got == target && cost < best.cost) {
                            best = (Decision){(uint8_t)subset, (uint8_t)(trick + 1),
                                              (uint8_t)sel, (uint8_t)cost};
                        }
                    }
                }
            }
            if (best.cost == 255) fail("unreachable row target polarity");
            row_table[pin][target] = best;
            if (best.cost < min_cost) {
                min_cost = best.cost;
                min_target = target;
            }
        }
        row_min_cost[pin] = (uint8_t)min_cost;
        row_min_target[pin] = (uint8_t)min_target;
    }
}

static void build_target_row(Value b[5], int target, Value out[5]) {
    int pin = 0;
    for (int x = 0; x < 5; x++) pin |= b[x].p << x;
    Decision d = row_table[pin][target];
    for (int x = 0; x < 5; x++) if ((d.subset >> x) & 1)
        b[x] = complement_representation(b[x]);
    int trick = (int)d.tricks - 1;
    int k = (trick + 1) % 5;
    if (trick >= 0) {
        Value t = and_value(val(b[(k + 1) % 5].n, b[(k + 1) % 5].p ^ 1),
                            b[(k + 2) % 5], (d.select_mask >> k) & 1);
        out[k] = xor_value(b[k], t);
    }
    for (int x = 0; x < 5; x++) {
        if (trick >= 0 && x == k) continue;
        Value t1 = x == trick ? out[k] : b[(x + 1) % 5];
        Value t = and_value(val(t1.n, t1.p ^ 1), b[(x + 2) % 5],
                            (d.select_mask >> x) & 1);
        out[x] = xor_value(b[x], t);
    }
    int got = 0;
    for (int x = 0; x < 5; x++) got |= out[x].p << x;
    if (got != target) fail("row-table construction mismatch");
}

static void row_patterns(const uint8_t state[1600], const uint8_t cnot[320],
                         const uint8_t dnot[320], uint8_t patterns[320]) {
    uint8_t cp[320], dp[320];
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++) {
        int p = 0;
        for (int y = 0; y < 5; y++) p ^= state[64 * (x + 5 * y) + z];
        cp[64 * x + z] = (uint8_t)(p ^ cnot[64 * x + z]);
    }
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++)
        dp[64 * x + z] = (uint8_t)(cp[64 * ((x + 4) % 5) + z] ^
            cp[64 * ((x + 1) % 5) + ((z + 63) & 63)] ^ dnot[64 * x + z]);
    for (int Y = 0; Y < 5; Y++) for (int z = 0; z < 64; z++) {
        int pin = 0;
        for (int X = 0; X < 5; X++) {
            int y = X, x = (3 * Y + X) % 5;
            int zz = (z - ROT[x][y]) & 63;
            int p = state[64 * (x + 5 * y) + zz] ^ dp[64 * x + zz];
            pin |= p << X;
        }
        patterns[64 * Y + z] = (uint8_t)pin;
    }
}

static void targets_to_state(const uint8_t target[320], uint8_t state[1600]) {
    for (int Y = 0; Y < 5; Y++) for (int z = 0; z < 64; z++)
        for (int X = 0; X < 5; X++)
            state[64 * (X + 5 * Y) + z] = (target[64 * Y + z] >> X) & 1;
}

static void state_to_targets(const uint8_t state[1600], uint8_t target[320]) {
    for (int Y = 0; Y < 5; Y++) for (int z = 0; z < 64; z++) {
        int t = 0;
        for (int X = 0; X < 5; X++) t |= state[64 * (X + 5 * Y) + z] << X;
        target[64 * Y + z] = (uint8_t)t;
    }
}

static int current_cost(const uint8_t input[1600], const Plan *p) {
    uint8_t patterns[320];
    row_patterns(input, p->cnot, p->dnot, patterns);
    int cost = 3200;
    for (int i = 0; i < 320; i++) {
        int target = p->target[i] ^ (i < 64 && ((p->ib >> i) & 1));
        cost += p->cnot[i] + p->dnot[i] + row_table[patterns[i]][target].cost;
    }
    return cost;
}

static int next_estimate(const Plan *p) {
    static const uint8_t zero[320] = {0};
    uint8_t state[1600], patterns[320];
    targets_to_state(p->target, state);
    row_patterns(state, zero, zero, patterns);
    int cost = 3200;
    for (int i = 0; i < 320; i++) cost += row_min_cost[patterns[i]];
    return cost;
}

static int fixed_next_estimate(const Plan *p, const uint8_t fixed_output[1600]) {
    static const uint8_t zero[320] = {0};
    uint8_t state[1600], patterns[320], targets[320];
    targets_to_state(p->target, state);
    state_to_targets(fixed_output, targets);
    row_patterns(state, zero, zero, patterns);
    int cost = 3200;
    for (int i = 0; i < 320; i++) cost += row_table[patterns[i]][targets[i]].cost;
    return cost;
}

static int output_distance(const Plan *p, const uint8_t reference[1600]) {
    uint8_t state[1600];
    targets_to_state(p->target, state);
    int distance = 0;
    for (int i = 0; i < 1600; i++) distance += state[i] != reference[i];
    return distance;
}

static int objective(const uint8_t input[1600], const Plan *p,
                     const uint8_t next_fixed_output[1600],
                     const uint8_t bridge_reference[1600]) {
    int tail = bridge_reference ? 16 * output_distance(p, bridge_reference) :
        next_fixed_output ? 16 * fixed_next_estimate(p, next_fixed_output) :
                            3 * next_estimate(p);
    return 16 * current_cost(input, p) + tail;
}

static int free_output_cost(const uint8_t input[1600], const Plan *p) {
    uint8_t patterns[320];
    row_patterns(input, p->cnot, p->dnot, patterns);
    int cost = 3200;
    for (int i = 0; i < 320; i++)
        cost += p->cnot[i] + p->dnot[i] + row_min_cost[patterns[i]];
    return cost;
}

static void optimize_plan(const uint8_t input[1600], const uint8_t fixed_output[1600],
                          const uint8_t next_fixed_output[1600],
                          const uint8_t bridge_reference[1600], uint64_t ib,
                          uint64_t seed,
                          int iterations, Plan *result) {
    Plan cur = {0}, best;
    cur.ib = ib;
    uint8_t patterns[320];
    if (!fixed_output) {
        int free_cur = free_output_cost(input, &cur), free_best = free_cur;
        Plan free_plan = cur;
        int free_iterations = iterations < 10000 ? 10000 : iterations;
        for (int it = 0; it < free_iterations; it++) {
            uint64_t r = rng_next(&seed);
            int kind = (int)(r & 1), index = (int)((r >> 8) % 320);
            uint8_t *bit = kind ? &cur.dnot[index] : &cur.cnot[index];
            *bit ^= 1;
            int trial = free_output_cost(input, &cur);
            int diff = trial - free_cur;
            int temp = 1 + (free_iterations - it) * 24 / free_iterations;
            uint64_t denom = (uint64_t)temp + (uint64_t)(diff > 0 ? diff * 12 : 0);
            int accept = diff <= 0 || (rng_next(&seed) % denom) < (uint64_t)temp;
            if (accept) {
                free_cur = trial;
                if (trial < free_best) {
                    free_best = trial;
                    free_plan = cur;
                }
            } else {
                *bit ^= 1;
            }
        }
        cur = free_plan;
        for (int sweep = 0; sweep < 3; sweep++)
            for (int kind = 0; kind < 2; kind++) for (int i = 0; i < 320; i++) {
                uint8_t *bit = kind ? &cur.dnot[i] : &cur.cnot[i];
                int before = free_output_cost(input, &cur);
                *bit ^= 1;
                if (free_output_cost(input, &cur) > before) *bit ^= 1;
            }
    }
    row_patterns(input, cur.cnot, cur.dnot, patterns);
    if (fixed_output) state_to_targets(fixed_output, cur.target);
    else for (int i = 0; i < 320; i++) cur.target[i] = row_min_target[patterns[i]];
    int cur_obj = objective(input, &cur, next_fixed_output, bridge_reference), best_obj = cur_obj;
    best = cur;
    for (int it = 0; it < iterations; it++) {
        uint64_t r = rng_next(&seed);
        int kind = fixed_output ? (int)(r & 1) : 2, index, old;
        if (kind == 0) {
            index = (int)((r >> 8) % 320);
            old = cur.cnot[index];
            cur.cnot[index] ^= 1;
        } else if (kind == 1) {
            index = (int)((r >> 8) % 320);
            old = cur.dnot[index];
            cur.dnot[index] ^= 1;
        } else if (!fixed_output) {
            index = (int)((r >> 8) % 320);
            old = cur.target[index];
            cur.target[index] ^= (uint8_t)(1 + ((r >> 24) % 31));
        } else {
            continue;
        }
        int trial = objective(input, &cur, next_fixed_output, bridge_reference);
        int diff = trial - cur_obj;
        int temp = 1 + (iterations - it) * 96 / (iterations ? iterations : 1);
        uint64_t denom = (uint64_t)temp + (uint64_t)(diff > 0 ? diff * 24 : 0);
        int accept = diff <= 0 || (rng_next(&seed) % denom) < (uint64_t)temp;
        if (accept) {
            cur_obj = trial;
            if (trial < best_obj) {
                best_obj = trial;
                best = cur;
            }
        } else if (kind == 0) cur.cnot[index] = (uint8_t)old;
        else if (kind == 1) cur.dnot[index] = (uint8_t)old;
        else cur.target[index] = (uint8_t)old;
    }
    cur = best;
    cur_obj = best_obj;
    for (int sweep = 0; sweep < 2; sweep++) {
        if (fixed_output)
            for (int kind = 0; kind < 2; kind++) for (int i = 0; i < 320; i++) {
                uint8_t *bit = kind ? &cur.dnot[i] : &cur.cnot[i];
                *bit ^= 1;
                int trial = objective(input, &cur, next_fixed_output, bridge_reference);
                if (trial <= cur_obj) cur_obj = trial;
                else *bit ^= 1;
            }
        if (!fixed_output) for (int i = 0; i < 320; i++) {
            int old = cur.target[i], chosen = old, chosen_obj = cur_obj;
            for (int t = 0; t < 32; t++) {
                cur.target[i] = (uint8_t)t;
                int trial = objective(input, &cur, next_fixed_output, bridge_reference);
                if (trial < chosen_obj) {
                    chosen_obj = trial;
                    chosen = t;
                }
            }
            cur.target[i] = (uint8_t)chosen;
            cur_obj = chosen_obj;
        }
    }
    *result = cur;
}

static void theta_graph(Value S[25][64], Value D[5][64], const uint8_t *cnot,
                        const uint8_t *dnot) {
    Value C[5][64];
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++) {
        Value s = S[x][z];
        for (int y = 1; y < 5; y++) s = xor_value(s, S[x + 5 * y][z]);
        if (cnot && cnot[64 * x + z]) s = complement_representation(s);
        C[x][z] = s;
    }
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++) {
        Value d = xor_value(C[(x + 4) % 5][z], C[(x + 1) % 5][(z + 63) & 63]);
        if (dnot && dnot[64 * x + z]) d = complement_representation(d);
        D[x][z] = d;
    }
}

static Value lazy_c(Value S[25][64], Value C[5][64], uint8_t have_c[320],
                    const uint8_t *cnot, int x, int z) {
    int index = 64 * x + z;
    if (!have_c[index]) {
        Value s = S[x][z];
        for (int y = 1; y < 5; y++) s = xor_value(s, S[x + 5 * y][z]);
        if (cnot && cnot[index]) s = complement_representation(s);
        C[x][z] = s;
        have_c[index] = 1;
    }
    return C[x][z];
}

static Value lazy_d(Value S[25][64], Value C[5][64], Value D[5][64],
                    uint8_t have_c[320], uint8_t have_d[320],
                    const uint8_t *cnot, const uint8_t *dnot, int x, int z) {
    int index = 64 * x + z;
    if (!have_d[index]) {
        Value a = lazy_c(S, C, have_c, cnot, (x + 4) % 5, z);
        Value b = lazy_c(S, C, have_c, cnot, (x + 1) % 5, (z + 63) & 63);
        Value d = xor_value(a, b);
        if (dnot && dnot[index]) d = complement_representation(d);
        D[x][z] = d;
        have_d[index] = 1;
    }
    return D[x][z];
}

static void build_prefix_graph(const Plan *prefix_plan, int outputs[1600],
                               uint8_t output_p[1600]) {
    Value S[25][64], NS[25][64], D[5][64];
    reset_graph(256, 1);
    for (int l = 0; l < 25; l++) for (int z = 0; z < 64; z++)
        S[l][z] = constant((KL[l] >> z) & 1);
    for (int z = 0; z < 64; z++) {
        S[1][z] = val(z, 0);
        S[6][z] = val(64 + z, 0);
        S[4][z] = val(128 + z, 0);
        S[9][z] = val(192 + z, 0);
        S[11][z] = xor_value(xor_value(val(z, 0), val(64 + z, 0)),
                             constant((KL[11] >> z) & 1));
        S[14][z] = xor_value(xor_value(val(128 + z, 0), val(192 + z, 0)),
                             constant((KL[14] >> z) & 1));
    }
    for (int round = 0; round < 2; round++) {
        theta_graph(S, D, round == 1 ? prefix_plan->cnot : NULL,
                    round == 1 ? prefix_plan->dnot : NULL);
        memcpy(NS, S, sizeof(NS));
        for (int Y = 0; Y < 5; Y++) for (int z = 0; z < 64; z++) {
            Value b[5], out[5];
            for (int X = 0; X < 5; X++) {
                int y = X, x = (3 * Y + X) % 5;
                int zz = (z - ROT[x][y]) & 63;
                b[X] = xor_value(S[x + 5 * y][zz], D[x][zz]);
            }
            build_dynamic_row(b, 0x1f, out);
            for (int X = 0; X < 5; X++) NS[X + 5 * Y][z] = out[X];
        }
        for (int z = 0; z < 64; z++) NS[0][z].p ^= (RC[round] >> z) & 1;
        memcpy(S, NS, sizeof(S));
    }
    for (int q = 0; q < 1600; q++) {
        Value v = S[q >> 6][q & 63];
        if (v.n == NC) fail("constant prefix output");
        outputs[q] = v.n;
        output_p[q] = v.p;
    }
}

static int live_operation_count(const int *outputs, int output_count, int input_count) {
    static uint8_t live_storage[MAX_NODES];
    uint8_t *live = live_storage;
    memset(live, 0, (size_t)node_count);
    for (int j = 0; j < output_count; j++) live[outputs[j]] = 1;
    int count = 0;
    for (int i = node_count - 1; i >= input_count; i--) if (live[i]) {
        count++;
        live[nodes[i].a] = 1;
        if (nodes[i].op != O_NOT) live[nodes[i].b] = 1;
    }
    return count;
}

static void optimize_prefix(Plan *plan, int outputs[1600], uint8_t output_p[1600]) {
    memset(plan, 0, sizeof(*plan));
    build_prefix_graph(plan, outputs, output_p);
    int best = live_operation_count(outputs, 1600, 256);
    int gain = 0;
    for (int sweep = 0; sweep < 3; sweep++) {
        for (int kind = 0; kind < 2; kind++) for (int i = 0; i < 320; i++) {
            uint8_t *bit = kind ? &plan->dnot[i] : &plan->cnot[i];
            *bit ^= 1;
            build_prefix_graph(plan, outputs, output_p);
            int trial = live_operation_count(outputs, 1600, 256);
            if (trial < best) {
                gain += best - trial;
                best = trial;
            } else {
                *bit ^= 1;
            }
        }
    }
    build_prefix_graph(plan, outputs, output_p);
    if (live_operation_count(outputs, 1600, 256) != best)
        fail("prefix greedy count mismatch");
    printf("prefix-round1-greedy-gain %d\n", gain);
}

static void optimize_prefix_from_seed(Plan *plan, int outputs[1600],
                                      uint8_t output_p[1600]) {
    build_prefix_graph(plan, outputs, output_p);
    int best = live_operation_count(outputs, 1600, 256);
    int gain = 0;
    for (int sweep = 0; sweep < 3; sweep++) {
        int improved = 0;
        for (int kind = 0; kind < 2; kind++) for (int i = 0; i < 320; i++) {
            uint8_t *bit = kind ? &plan->dnot[i] : &plan->cnot[i];
            *bit ^= 1;
            build_prefix_graph(plan, outputs, output_p);
            int trial = live_operation_count(outputs, 1600, 256);
            if (trial < best) {
                gain += best - trial;
                best = trial;
                improved = 1;
            } else {
                *bit ^= 1;
            }
        }
        if (!improved) break;
    }
    build_prefix_graph(plan, outputs, output_p);
    if (live_operation_count(outputs, 1600, 256) != best)
        fail("seeded prefix greedy count mismatch");
    printf("prefix-round1-seeded-greedy-gain %d\n", gain);
}

static void build_body_graph(const uint8_t input_p[1600], const Plan *plan,
                             int outputs[1600], uint8_t output_p[1600]) {
    Value S[25][64], NS[25][64], C[5][64], D[5][64];
    uint8_t have_c[320] = {0}, have_d[320] = {0};
    reset_graph(1600, 0);
    for (int q = 0; q < 1600; q++) S[q >> 6][q & 63] = val(q, input_p[q]);
    memcpy(NS, S, sizeof(NS));
    for (int Y = 0; Y < 5; Y++) for (int z = 0; z < 64; z++) {
        Value b[5], out[5];
        for (int X = 0; X < 5; X++) {
            int y = X, x = (3 * Y + X) % 5;
            int zz = (z - ROT[x][y]) & 63;
            Value d = lazy_d(S, C, D, have_c, have_d, plan->cnot, plan->dnot, x, zz);
            b[X] = xor_value(S[x + 5 * y][zz], d);
        }
        int target = plan->target[64 * Y + z] ^
            (Y == 0 && ((plan->ib >> z) & 1));
        build_target_row(b, target, out);
        for (int X = 0; X < 5; X++) NS[X + 5 * Y][z] = out[X];
    }
    for (int q = 0; q < 1600; q++) {
        Value v = NS[q >> 6][q & 63];
        outputs[q] = v.n;
        output_p[q] = v.p ^ (q < 64 && ((plan->ib >> q) & 1));
    }
}

static void build_end_graph(const uint8_t input_p[1600], int outputs[256],
                            uint8_t output_p[256]) {
    Value S[25][64], C[5][64], D[5][64];
    uint8_t have_c[320] = {0}, have_d[320] = {0};
    reset_graph(1600, 0);
    for (int q = 0; q < 1600; q++) S[q >> 6][q & 63] = val(q, input_p[q]);
    for (int z = 0; z < 64; z++) {
        Value b[5], out[5];
        for (int X = 0; X < 5; X++) {
            int y = X, x = X;
            int zz = (z - ROT[x][y]) & 63;
            Value d = lazy_d(S, C, D, have_c, have_d, NULL, NULL, x, zz);
            b[X] = xor_value(S[x + 5 * y][zz], d);
        }
        build_dynamic_row(b, 0x0f, out);
        for (int X = 0; X < 4; X++) {
            Value v = out[X];
            if (X == 0) v.p ^= (RC[23] >> z) & 1;
            int j = 64 * X + z;
            outputs[j] = v.n;
            output_p[j] = v.p;
        }
    }
}

static Insn *allocate_block(const int *outputs, const int *output_regs, int output_count,
                            const int *input_regs, int input_count, size_t *program_count,
                            int counts[5], int *high_reg) {
    uint8_t *live = calloc((size_t)node_count, 1);
    uint16_t *last = calloc((size_t)node_count, sizeof(*last));
    uint16_t *reg = calloc((size_t)node_count, sizeof(*reg));
    uint16_t *out_index = malloc((size_t)node_count * sizeof(*out_index));
    uint16_t *free_regs = malloc(NREG * sizeof(*free_regs));
    uint8_t *busy = calloc(NREG, 1);
    uint8_t *reserved = calloc(NREG, 1);
    Insn *prog = malloc((size_t)node_count * sizeof(*prog));
    if (!live || !last || !reg || !out_index || !free_regs || !busy || !reserved || !prog)
        fail("allocator memory failure");
    memset(out_index, 0xff, (size_t)node_count * sizeof(*out_index));
    memset(counts, 0, 5 * sizeof(*counts));
    for (int j = 0; j < output_count; j++) {
        if (outputs[j] < input_count || out_index[outputs[j]] != UINT16_MAX)
            fail("invalid/shared block output");
        live[outputs[j]] = 1;
        out_index[outputs[j]] = j;
        reserved[output_regs[j]] = 1;
    }
    for (int i = node_count - 1; i >= input_count; i--) if (live[i]) {
        live[nodes[i].a] = 1;
        if (nodes[i].op != O_NOT) live[nodes[i].b] = 1;
    }
    for (int i = input_count; i < node_count; i++) if (live[i]) {
        last[nodes[i].a] = i;
        if (nodes[i].op != O_NOT) last[nodes[i].b] = i;
    }
    for (int j = 0; j < output_count; j++) last[outputs[j]] = UINT16_MAX;
    for (int j = 0; j < input_count; j++) {
        reg[j] = input_regs[j];
        if (last[j]) busy[input_regs[j]] = 1;
    }
    int free_count = 0;
    for (int r = NREG - 1; r >= 0; r--)
        if (!busy[r] && !reserved[r]) free_regs[free_count++] = r;
    size_t pc = 0;
    int high = 0;
    for (int j = 0; j < input_count; j++) if (input_regs[j] + 1 > high) high = input_regs[j] + 1;
    for (int j = 0; j < output_count; j++) if (output_regs[j] + 1 > high) high = output_regs[j] + 1;
    for (int i = input_count; i < node_count; i++) if (live[i]) {
        int op = nodes[i].op, a = nodes[i].a, b = op == O_NOT ? a : nodes[i].b;
        if (last[a] == i) {
            int r = reg[a];
            busy[r] = 0;
            if (!reserved[r]) free_regs[free_count++] = r;
        }
        if (b != a && last[b] == i) {
            int r = reg[b];
            busy[r] = 0;
            if (!reserved[r]) free_regs[free_count++] = r;
        }
        int d;
        if (out_index[i] != UINT16_MAX) {
            d = output_regs[out_index[i]];
            if (busy[d]) fail("fixed output register busy");
        } else {
            if (!free_count) fail("register file exhausted");
            d = free_regs[--free_count];
        }
        busy[d] = 1;
        reg[i] = d;
        if (d + 1 > high) high = d + 1;
        uint8_t enc = op == O_XOR ? 0 : op == O_AND ? 1 : op == O_OR ? 2 : 3;
        prog[pc++] = (Insn){enc, (uint16_t)d, (uint16_t)reg[a],
                           (uint16_t)(op == O_NOT ? 0 : reg[nodes[i].b])};
        counts[op]++;
    }
    free(live); free(last); free(reg); free(out_index); free(free_regs); free(busy); free(reserved);
    *program_count = pc;
    *high_reg = high;
    return prog;
}

#ifndef PACKED_ONLY
static void write_program(const char *path, const Insn *prog, size_t n) {
    FILE *f = fopen(path, "wb");
    if (!f) {
        fprintf(stderr, "gen_combined: fopen %s: %s\n", path, strerror(errno));
        exit(1);
    }
    for (size_t i = 0; i < n; i++) {
        uint64_t w = (uint64_t)prog[i].op | (uint64_t)prog[i].d << 3 |
                     (uint64_t)prog[i].a << 15 | (uint64_t)prog[i].b << 27;
        uint8_t out[5];
        for (int j = 0; j < 5; j++) out[j] = (uint8_t)(w >> (8 * j));
        if (fwrite(out, 1, 5, f) != 5) fail("program write failed");
    }
    if (fclose(f)) fail("program close failed");
}
#endif

static void write_packed_program(const char *path, const Insn *prog, size_t n) {
    size_t bytes = (39 * n + 7) / 8;
    uint8_t *packed = calloc(bytes ? bytes : 1, 1);
    if (!packed) fail("packed-program allocation failure");
    for (size_t i = 0; i < n; i++) {
        uint64_t w = (uint64_t)prog[i].op | (uint64_t)prog[i].d << 3 |
                     (uint64_t)prog[i].a << 15 | (uint64_t)prog[i].b << 27;
        size_t bit = 39 * i;
        for (int k = 0; k < 39; k++)
            packed[(bit + (size_t)k) >> 3] |= (uint8_t)(((w >> k) & 1) << ((bit + (size_t)k) & 7));
    }
    FILE *f = fopen(path, "wb");
    if (!f || (bytes && fwrite(packed, 1, bytes, f) != bytes) || fclose(f))
        fail("packed program write failed");
    free(packed);
}

static size_t emit_block(const char *dir, const char *name, const int *outputs,
                         int output_count, int input_count, int input_base,
                         int output_base, int *highest) {
    int *input_regs = malloc((size_t)input_count * sizeof(*input_regs));
    int *output_regs = malloc((size_t)output_count * sizeof(*output_regs));
    if (!input_regs || !output_regs) fail("register-map allocation failure");
    for (int i = 0; i < input_count; i++) input_regs[i] = input_base + i;
    for (int i = 0; i < output_count; i++) output_regs[i] = output_base + i;
    size_t n;
    int mix[5], high;
    Insn *prog = allocate_block(outputs, output_regs, output_count, input_regs,
                                input_count, &n, mix, &high);
    char path[4096];
#ifndef PACKED_ONLY
    if (snprintf(path, sizeof(path), "%s/%s.bin", dir, name) >= (int)sizeof(path))
        fail("output path too long");
    write_program(path, prog, n);
#endif
    if (snprintf(path, sizeof(path), "%s/%s.p39", dir, name) >= (int)sizeof(path))
        fail("packed output path too long");
    write_packed_program(path, prog, n);
    printf("block %s XOR %d AND %d OR %d NOT %d total %zu highest-register+1 %d\n",
           name, mix[O_XOR], mix[O_AND], mix[O_OR], mix[O_NOT], n, high);
    if (high > *highest) *highest = high;
    free(prog); free(input_regs); free(output_regs);
    return n;
}

static size_t emit_bridge(const char *dir, const uint8_t from[1600],
                          const uint8_t to[1600]) {
    Insn *prog = malloc(1600 * sizeof(*prog));
    if (!prog) fail("bridge allocation failure");
    size_t n = 0;
    for (int q = 0; q < 1600; q++) if (from[q] != to[q])
        prog[n++] = (Insn){3, (uint16_t)(256 + q), (uint16_t)(256 + q), 0};
    char path[4096];
#ifndef PACKED_ONLY
    if (snprintf(path, sizeof(path), "%s/G.bin", dir) >= (int)sizeof(path))
        fail("output path too long");
    write_program(path, prog, n);
#endif
    if (snprintf(path, sizeof(path), "%s/G.p39", dir) >= (int)sizeof(path))
        fail("packed bridge path too long");
    write_packed_program(path, prog, n);
    printf("block G XOR 0 AND 0 OR 0 NOT %zu total %zu highest-register+1 1856\n", n, n);
    free(prog);
    return n;
}

static void write_regeneration_data(const char *path, const Plan *prefix_plan,
                                    const Plan best_chain[8],
                                    const uint8_t best_cycle[1600]) {
    static const uint8_t magic[8] = {'H', 'S', '2', '4', 'P', 'L', 'N', '1'};
    FILE *f = fopen(path, "wb");
    if (!f || fwrite(magic, sizeof(magic), 1, f) != 1 ||
        fwrite(prefix_plan, sizeof(*prefix_plan), 1, f) != 1 ||
        fwrite(best_chain, sizeof(*best_chain), 8, f) != 8 ||
        fwrite(best_cycle, 1600, 1, f) != 1 ||
        fwrite(row_table, sizeof(row_table), 1, f) != 1 || fclose(f))
        fail("cannot write regeneration data");
}

static void read_seed_plan(const char *path, Plan *prefix_plan,
                           Plan chain[8], uint8_t cycle[1600]) {
    static const uint8_t expected[8] = {'H', 'S', '2', '4', 'O', 'P', 'T', '1'};
    uint8_t magic[8];
    FILE *f = fopen(path, "rb");
    if (!f || fread(magic, sizeof(magic), 1, f) != 1 ||
        memcmp(magic, expected, sizeof(magic)))
        fail("cannot read seed-plan header");
    memset(prefix_plan, 0, sizeof(*prefix_plan));
    if (fread(prefix_plan->cnot, 320, 1, f) != 1 ||
        fread(prefix_plan->dnot, 320, 1, f) != 1 ||
        fread(cycle, 1600, 1, f) != 1)
        fail("cannot read seed prefix");
    for (int b = 0; b < 8; b++) {
        memset(&chain[b], 0, sizeof(chain[b]));
        if (fread(chain[b].cnot, 320, 1, f) != 1 ||
            fread(chain[b].dnot, 320, 1, f) != 1 ||
            fread(chain[b].target, 320, 1, f) != 1 ||
            fread(&chain[b].ib, sizeof(chain[b].ib), 1, f) != 1)
            fail("cannot read seed body");
    }
    if (fgetc(f) != EOF || fclose(f)) fail("seed plan has trailing data");
}

static long long chain_cost(const Plan chain[8], const uint8_t cycle[1600]) {
    static const int runs[8] = {3, 3, 3, 3, 3, 2, 2, 2};
    uint8_t input[1600];
    memcpy(input, cycle, sizeof(input));
    long long total = 0;
    for (int b = 0; b < 8; b++) {
        total += (long long)runs[b] * current_cost(input, &chain[b]);
        targets_to_state(chain[b].target, input);
    }
    if (memcmp(input, cycle, sizeof(input))) fail("polished chain does not close");
    return total;
}

static long long body_pair_cost(const Plan chain[8], const uint8_t cycle[1600],
                                int body) {
    static const int runs[8] = {3, 3, 3, 3, 3, 2, 2, 2};
    uint8_t input[1600];
    if (body == 0) memcpy(input, cycle, sizeof(input));
    else targets_to_state(chain[body - 1].target, input);
    long long total = (long long)runs[body] * current_cost(input, &chain[body]);
    if (body < 7) {
        uint8_t next[1600];
        targets_to_state(chain[body].target, next);
        total += (long long)runs[body + 1] * current_cost(next, &chain[body + 1]);
    }
    return total;
}

static long long weighted_body_cost(const Plan chain[8], const uint8_t cycle[1600],
                                    int body) {
    uint8_t input[1600];
    if (body == 0) memcpy(input, cycle, sizeof(input));
    else targets_to_state(chain[body - 1].target, input);
    return (long long)(body < 5 ? 3 : 2) * current_cost(input, &chain[body]);
}

static long long global_polish(Plan chain[8], const uint8_t cycle[1600],
                               int max_sweeps) {
    long long total = chain_cost(chain, cycle);
    for (int sweep = 0; sweep < max_sweeps; sweep++) {
        int improvements = 0;
        for (int b = 0; b < 8; b++) {
            uint8_t input[1600];
            if (b == 0) memcpy(input, cycle, sizeof(input));
            else targets_to_state(chain[b - 1].target, input);
            int before = current_cost(input, &chain[b]);
            for (int kind = 0; kind < 2; kind++) for (int i = 0; i < 320; i++) {
                uint8_t *bit = kind ? &chain[b].dnot[i] : &chain[b].cnot[i];
                *bit ^= 1;
                int after = current_cost(input, &chain[b]);
                if (after < before) {
                    total += (long long)(after - before) *
                        (b < 5 ? 3 : 2);
                    before = after;
                    improvements++;
                } else {
                    *bit ^= 1;
                }
            }
        }
        for (int b = 0; b < 7; b++) for (int i = 0; i < 320; i++) {
            int old = chain[b].target[i], chosen = old;
            long long before = body_pair_cost(chain, cycle, b), best = before;
            for (int target = 0; target < 32; target++) {
                chain[b].target[i] = (uint8_t)target;
                long long trial = body_pair_cost(chain, cycle, b);
                if (trial < best) {
                    best = trial;
                    chosen = target;
                }
            }
            chain[b].target[i] = (uint8_t)chosen;
            if (best < before) {
                total += best - before;
                improvements++;
            }
        }
        long long checked = chain_cost(chain, cycle);
        if (checked != total) fail("global polish delta mismatch");
        printf("global polish sweep %d operations %lld improvements %d\n",
               sweep, total, improvements);
        if (!improvements) break;
    }
    return total;
}

static long long global_anneal(Plan chain[8], const uint8_t cycle[1600],
                               int iterations, uint64_t seed) {
    Plan best[8];
    long long total = chain_cost(chain, cycle), best_cost = total;
    memcpy(best, chain, sizeof(best));
    for (int it = 0; it < iterations; it++) {
        uint64_t r = rng_next(&seed);
        int body = (int)((r >> 8) & 7);
        int kind = (int)(r % (body < 7 ? 3 : 2));
        int index = (int)((r >> 16) % 320);
        int old;
        long long before = kind == 2 ? body_pair_cost(chain, cycle, body) :
            weighted_body_cost(chain, cycle, body);
        if (kind == 0) {
            old = chain[body].cnot[index];
            chain[body].cnot[index] ^= 1;
        } else if (kind == 1) {
            old = chain[body].dnot[index];
            chain[body].dnot[index] ^= 1;
        } else {
            old = chain[body].target[index];
            chain[body].target[index] ^= (uint8_t)(1 + ((r >> 32) % 31));
        }
        long long after = kind == 2 ? body_pair_cost(chain, cycle, body) :
            weighted_body_cost(chain, cycle, body);
        long long diff = after - before;
        double progress = iterations ? (double)it / iterations : 1.0;
        double temperature = 24.0 * exp(-5.5 * progress) + 0.05;
        double uniform = (double)(rng_next(&seed) >> 11) * (1.0 / 9007199254740992.0);
        int accept = diff <= 0 || uniform < exp(-(double)diff / temperature);
        if (accept) {
            total += diff;
            if (total < best_cost) {
                best_cost = total;
                memcpy(best, chain, sizeof(best));
            }
        } else if (kind == 0) chain[body].cnot[index] = (uint8_t)old;
        else if (kind == 1) chain[body].dnot[index] = (uint8_t)old;
        else chain[body].target[index] = (uint8_t)old;
    }
    memcpy(chain, best, sizeof(best));
    if (chain_cost(chain, cycle) != best_cost) fail("global anneal mismatch");
    return best_cost;
}

int main(int argc, char **argv) {
    int rebase_seed = 0;
    if (argc >= 3 && !strcmp(argv[1], "--kl")) {
        load_kl_record(argv[2]);
        argc -= 2;
        argv += 2;
    }
    if (argc >= 2 && !strcmp(argv[1], "--rebase")) {
        rebase_seed = 1;
        argc--;
        argv++;
    }
    const char *dir = argc > 1 ? argv[1] : ".";
    int iterations = argc > 2 ? atoi(argv[2]) : 30000;
    int trials = argc > 3 ? atoi(argv[3]) : 4;
    uint64_t seed_offset = argc > 6 ? strtoull(argv[6], NULL, 0) : 0;
    int perturbations = argc > 7 ? atoi(argv[7]) : 0;
    if (iterations < 0 || trials < 1 || trials > 32) fail("invalid optimizer settings");
    make_row_table();

    int prefix_nodes[1600], body_nodes[1600], end_nodes[256];
    uint8_t prefix_p[1600], out_p[1600], end_p[256];
    Plan prefix_plan, seed_chain[8];
    uint8_t seed_cycle[1600];
    int have_seed = argc > 5;
    if (rebase_seed && !have_seed) fail("--rebase requires a seed plan");
    if (have_seed) {
        read_seed_plan(argv[5], &prefix_plan, seed_chain, seed_cycle);
        if (rebase_seed) {
            optimize_prefix_from_seed(&prefix_plan, prefix_nodes, prefix_p);
            memcpy(seed_cycle, prefix_p, sizeof(seed_cycle));
            state_to_targets(seed_cycle, seed_chain[7].target);
            printf("rebased seed plan %s onto loaded constants\n", argv[5]);
        } else {
            build_prefix_graph(&prefix_plan, prefix_nodes, prefix_p);
            if (memcmp(prefix_p, seed_cycle, 1600)) fail("seed prefix polarity mismatch");
            printf("loaded seed plan %s\n", argv[5]);
        }
    } else {
        optimize_prefix(&prefix_plan, prefix_nodes, prefix_p);
    }
    int prefix_node_count = node_count;
    Node *prefix_copy = malloc((size_t)node_count * sizeof(*prefix_copy));
    Form *form_copy = malloc((size_t)form_count * sizeof(*form_copy));
    int prefix_form_count = form_count;
    if (!prefix_copy || !form_copy) fail("prefix snapshot allocation failure");
    memcpy(prefix_copy, nodes, (size_t)node_count * sizeof(*nodes));
    memcpy(form_copy, forms, (size_t)form_count * sizeof(*forms));

    static const int runs[8] = {3, 3, 3, 3, 3, 2, 2, 2};
    Plan best_chain[8], chain[8], scratch[8];
    uint8_t best_cycle[1600];
    long long best_weighted = -1;
    if (have_seed) {
        uint8_t input[1600];
        memcpy(input, seed_cycle, sizeof(input));
        long long weighted = 0;
        for (int b = 0; b < 8; b++) {
            int cost = current_cost(input, &seed_chain[b]);
            weighted += (long long)runs[b] * cost;
            targets_to_state(seed_chain[b].target, input);
        }
        if (memcmp(input, seed_cycle, sizeof(input))) fail("seed cycle does not close");
        printf("seed body operations %lld\n", weighted);
        best_weighted = weighted;
        memcpy(best_chain, seed_chain, sizeof(best_chain));
        memcpy(best_cycle, seed_cycle, sizeof(best_cycle));
        long long polished = global_polish(best_chain, best_cycle, 8);
        if (polished < best_weighted) best_weighted = polished;
        for (int trial = 0; trial < trials && iterations > 0; trial++) {
            Plan candidate[8];
            memcpy(candidate, seed_chain, sizeof(candidate));
            uint64_t seed = UINT64_C(0x6a09e667f3bcc909) ^
                (uint64_t)(trial + 1 + seed_offset) * UINT64_C(0x9e3779b97f4a7c15);
            for (int move = 0; move < perturbations; move++) {
                uint64_t r = rng_next(&seed);
                int body = (int)((r >> 8) & 7);
                int kind = (int)(r % (body < 7 ? 3 : 2));
                int index = (int)((r >> 16) % 320);
                if (kind == 0) candidate[body].cnot[index] ^= 1;
                else if (kind == 1) candidate[body].dnot[index] ^= 1;
                else candidate[body].target[index] ^=
                    (uint8_t)(1 + ((r >> 32) % 31));
            }
            long long annealed = global_anneal(candidate, seed_cycle, iterations, seed);
            long long candidate_cost = global_polish(candidate, seed_cycle, 4);
            printf("global trial %d annealed %lld polished %lld\n",
                   trial, annealed, candidate_cost);
            if (candidate_cost < best_weighted) {
                best_weighted = candidate_cost;
                memcpy(best_chain, candidate, sizeof(best_chain));
            }
        }
    }
    if (!have_seed) for (int trial = 0; trial < trials; trial++) {
        uint8_t cycle[1600], input[1600];
        memcpy(cycle, prefix_p, sizeof(cycle));
        int derivations = trial % 3;
        for (int outer = 0; outer < derivations; outer++) {
            memcpy(input, cycle, sizeof(input));
            for (int b = 0; b < 7; b++) {
                uint64_t seed = UINT64_C(0x243f6a8885a308d3) ^
                    (uint64_t)(trial + 1) * UINT64_C(0xd1b54a32d192ed03) ^
                    (uint64_t)(outer + 1) * UINT64_C(0x9e3779b97f4a7c15) ^
                    (uint64_t)(b + 1) * UINT64_C(0x94d049bb133111eb);
                optimize_plan(input, NULL, NULL, NULL,
                              have_seed ? seed_chain[b].ib : 0,
                              seed, iterations, &scratch[b]);
                targets_to_state(scratch[b].target, input);
            }
            uint64_t seed = UINT64_C(0x13198a2e03707344) ^
                (uint64_t)(trial + 1) * UINT64_C(0x94d049bb133111eb) ^
                (uint64_t)(outer + 1) * UINT64_C(0xd1b54a32d192ed03);
            optimize_plan(input, NULL, NULL, prefix_p,
                          have_seed ? seed_chain[7].ib : 0,
                          seed, iterations, &scratch[7]);
            targets_to_state(scratch[7].target, cycle);
        }

        memcpy(input, cycle, sizeof(input));
        long long weighted = 0;
        for (int b = 0; b < 8; b++) {
            const uint8_t *fixed = b == 7 ? cycle : NULL;
            uint64_t seed = UINT64_C(0x9e3779b97f4a7c15) ^
                (uint64_t)(trial + 1) * UINT64_C(0xd1b54a32d192ed03) ^
                (uint64_t)(b + 1) * UINT64_C(0x94d049bb133111eb);
            const uint8_t *next_fixed = b == 6 ? cycle : NULL;
            optimize_plan(input, fixed, next_fixed, NULL,
                          have_seed ? seed_chain[b].ib : 0,
                          seed, iterations, &chain[b]);
            int cost = current_cost(input, &chain[b]);
            weighted += (long long)runs[b] * cost;
            targets_to_state(chain[b].target, input);
        }
        int bridge = 0;
        for (int i = 0; i < 1600; i++) bridge += cycle[i] != prefix_p[i];
        weighted += bridge;
        printf("optimizer trial %d body-plus-bridge-operations %lld bridge %d\n",
               trial, weighted, bridge);
        if (best_weighted < 0 || weighted < best_weighted) {
            best_weighted = weighted;
            memcpy(best_chain, chain, sizeof(best_chain));
            memcpy(best_cycle, cycle, sizeof(best_cycle));
        }
    }

    if (argc > 4)
        write_regeneration_data(argv[4], &prefix_plan, best_chain, best_cycle);

    int highest = 0;
    memcpy(nodes, prefix_copy, (size_t)prefix_node_count * sizeof(*nodes));
    memcpy(forms, form_copy, (size_t)prefix_form_count * sizeof(*forms));
    node_count = prefix_node_count;
    form_count = prefix_form_count;
    free(prefix_copy);
    free(form_copy);
    size_t stored = emit_block(dir, "P", prefix_nodes, 1600, 256, 0, 256, &highest);
    size_t prefix_count = stored;
    size_t bridge_count = emit_bridge(dir, prefix_p, best_cycle);
    stored += bridge_count;

    uint8_t input[1600];
    memcpy(input, best_cycle, sizeof(input));
    size_t body_count[8];
    for (int b = 0; b < 8; b++) {
        build_body_graph(input, &best_chain[b], body_nodes, out_p);
        int expected = current_cost(input, &best_chain[b]);
        int in_base = (b & 1) ? 1856 : 256;
        int out_base = (b & 1) ? 256 : 1856;
        char name[8];
        snprintf(name, sizeof(name), "B%d", b + 1);
        body_count[b] = emit_block(dir, name, body_nodes, 1600, 1600, in_base,
                                   out_base, &highest);
        if ((int)body_count[b] != expected) fail("body count differs from polarity ledger");
        stored += body_count[b];
        memcpy(input, out_p, sizeof(input));
    }
    if (memcmp(input, best_cycle, sizeof(input))) fail("eight-body polarity cycle does not close");

    uint8_t round22_p[1600];
    targets_to_state(best_chain[4].target, round22_p);
    build_end_graph(round22_p, end_nodes, end_p);
    size_t end_count = emit_block(dir, "E", end_nodes, 256, 1600, 1856, 0, &highest);
    stored += end_count;

    int iota = 0;
    for (int r = 2; r <= 22; r++) {
        int b = (r - 2) & 7;
        iota += __builtin_popcountll(RC[r] ^ best_chain[b].ib);
    }
    int driver = 2 * 21 + iota;
    long long executed = (long long)prefix_count + bridge_count + end_count + driver;
    for (int b = 0; b < 8; b++) executed += (long long)runs[b] * body_count[b];
    uint64_t pd[4] = {0, 0, 0, 0};
    for (int j = 0; j < 256; j++) pd[j >> 6] |= (uint64_t)end_p[j] << (j & 63);
    char pd_path[4096];
    if (snprintf(pd_path, sizeof(pd_path), "%s/PD.bin", dir) >= (int)sizeof(pd_path))
        fail("PD path too long");
    FILE *pd_file = fopen(pd_path, "wb");
    if (!pd_file || fwrite(pd, sizeof(pd), 1, pd_file) != 1 || fclose(pd_file))
        fail("cannot write PD.bin");

    printf("stored-block-instructions %zu\n", stored);
    printf("iota-xors %d\n", iota);
    printf("driver %d\n", driver);
    printf("TOTAL %lld\n", executed);
    printf("highest-register+1 %d\n", highest);
    printf("PD %016" PRIx64 " %016" PRIx64 " %016" PRIx64 " %016" PRIx64 "\n",
           pd[0], pd[1], pd[2], pd[3]);
    printf("optimizer iterations-per-body %d trials %d\n", iterations, trials);
    return highest > 4096 ? 2 : 0;
}

```

### step_search.c

```c
#define main r24_library_main
#define make_row_table inherited_make_row_table
#define build_target_row inherited_build_target_row
#include "plan_search_local.c"
#undef build_target_row
#undef make_row_table
#undef main
#include "s3_basis.h"
#ifndef FREESTANDING
#include <time.h>
#endif

static double bounded_exp(double x){
    if(x < -40.0) return 0.0;
    double y=x/64.0;
    double e=1.0+y+y*y/2.0+y*y*y/6.0+y*y*y*y/24.0;
    for(int i=0;i<6;i++)e*=e;
    return e;
}

static const int S3_LANES[12]={0,2,3,5,7,8,10,12,13,15,11,14};

static void chain_order(int tricks,int order[5]){
    int start=0;while((tricks>>start)&1)start++;
    for(int i=0;i<5;i++)order[i]=(start-i+5)%5;
}

static void eval_native_row(int pin,int subset,int tricks,int selected,
                            int *cost_out,int *target_out){
    int bp[5],op[5]={0,0,0,0,0},order[5],cost=__builtin_popcount((unsigned)subset);
    for(int x=0;x<5;x++)bp[x]=((pin>>x)&1)^((subset>>x)&1);
    chain_order(tricks,order);
    for(int i=0;i<5;i++){
        int x=order[i],a=((tricks>>x)&1)?op[(x+1)%5]^1:bp[(x+1)%5]^1,b=bp[(x+2)%5],tp;
        cost+=sim_term(a,b,(selected>>x)&1,&tp)+1;op[x]=bp[x]^tp;
    }
    int target=0;for(int x=0;x<5;x++)target|=op[x]<<x;*cost_out=cost;*target_out=target;
}

static void verify_native_row(int pin,int target,Decision d){
    int order[5];chain_order(d.tricks,order);
    for(int bits=0;bits<32;bits++){
        int w[5],p[5],ow[5]={0,0,0,0,0},op[5]={0,0,0,0,0};
        for(int x=0;x<5;x++){w[x]=((bits>>x)&1)^((pin>>x)&1);p[x]=(pin>>x)&1;if((d.subset>>x)&1){w[x]^=1;p[x]^=1;}}
        for(int i=0;i<5;i++){
            int x=order[i],lw,lp;if((d.tricks>>x)&1){lw=ow[(x+1)%5];lp=op[(x+1)%5]^1;}else{lw=w[(x+1)%5];lp=p[(x+1)%5]^1;}
            int rw=w[(x+2)%5],rp=p[(x+2)%5],tw,tp;
            if(lp==rp){if(!lp){tw=lw&rw;tp=0;}else{tw=lw|rw;tp=1;}}
            else{int pw=lp?rw:lw,other=lp?lw:rw;if((d.select_mask>>x)&1){tw=(pw^1)|other;tp=1;}else{tw=pw^(pw&other);tp=0;}}
            ow[x]=w[x]^tw;op[x]=p[x]^tp;
        }
        int got_p=0;for(int x=0;x<5;x++){int logical=ow[x]^op[x],truth=((bits>>x)&1)^((((bits>>((x+1)%5))&1)^1)&((bits>>((x+2)%5))&1));if(logical!=truth)fail("chained row truth mismatch");got_p|=op[x]<<x;}
        if(got_p!=target)fail("chained row polarity mismatch");
    }
}

static void make_row_table(void){
    for(int pin=0;pin<32;pin++){
        for(int target=0;target<32;target++)row_table[pin][target]=(Decision){0,0,0,255};
        for(int subset=0;subset<32;subset++)for(int tricks=0;tricks<31;tricks++)for(int selected=0;selected<32;selected++){
            int cost,target;eval_native_row(pin,subset,tricks,selected,&cost,&target);Decision best=row_table[pin][target];
            Decision candidate={(uint8_t)subset,(uint8_t)tricks,(uint8_t)selected,(uint8_t)cost};
            int better=candidate.cost<best.cost;
            if(candidate.cost==best.cost){int ct=__builtin_popcount((unsigned)candidate.tricks),bt=__builtin_popcount((unsigned)best.tricks),cs=__builtin_popcount((unsigned)candidate.subset),bs=__builtin_popcount((unsigned)best.subset);better=ct<bt||(ct==bt&&(cs<bs||(cs==bs&&(candidate.subset<best.subset||(candidate.subset==best.subset&&(candidate.tricks<best.tricks||(candidate.tricks==best.tricks&&candidate.select_mask<best.select_mask)))))));}
            if(better)row_table[pin][target]=candidate;
        }
        int min_cost=255,min_target=0;
        for(int target=0;target<32;target++){
            Decision best=row_table[pin][target];
            if(best.cost==255)fail("unreachable native row target polarity");
            verify_native_row(pin,target,best);row_table[pin][target]=best;
            if(best.cost<min_cost){min_cost=best.cost;min_target=target;}
        }
        row_min_cost[pin]=(uint8_t)min_cost;row_min_target[pin]=(uint8_t)min_target;
    }
}

static uint64_t chained_table_checksum(void){uint64_t h=UINT64_C(1469598103934665603);for(int p=0;p<32;p++)for(int q=0;q<32;q++){Decision d=row_table[p][q];uint8_t bytes[4]={d.subset,d.tricks,d.select_mask,d.cost};for(int i=0;i<4;i++){h^=bytes[i];h*=UINT64_C(1099511628211);}}return h;}

static void build_target_row(Value b[5],int target,Value out[5]){
    int pin=0;for(int x=0;x<5;x++)pin|=b[x].p<<x;
    Decision d=row_table[pin][target];int order[5];chain_order(d.tricks,order);
    for(int x=0;x<5;x++)if((d.subset>>x)&1)b[x]=complement_representation(b[x]);
    for(int i=0;i<5;i++){
        int x=order[i];Value first=((d.tricks>>x)&1)?out[(x+1)%5]:b[(x+1)%5];
        Value t=and_value(val(first.n,first.p^1),b[(x+2)%5],(d.select_mask>>x)&1);out[x]=xor_value(b[x],t);
    }
    int got=0;for(int x=0;x<5;x++)got|=out[x].p<<x;
    if(got!=target)fail("native row construction mismatch");
}

static uint16_t emitter_decisions[24][320];static uint8_t emitter_has_decisions[24];
static void build_encoded_row(Value b[5],uint16_t word,Value out[5]){
    int subset=word&31,tricks=(word>>5)&31,selected=(word>>10)&31,order[5];chain_order(tricks,order);
    for(int x=0;x<5;x++)if((subset>>x)&1)b[x]=complement_representation(b[x]);
    for(int i=0;i<5;i++){int x=order[i];Value first=((tricks>>x)&1)?out[(x+1)%5]:b[(x+1)%5];Value t=and_value(val(first.n,first.p^1),b[(x+2)%5],(selected>>x)&1);out[x]=xor_value(b[x],t);}
}

static void set_s3_trial(int trial){
    memset(KL,0,sizeof(KL)); KL[16]=UINT64_C(0x8000000000000006);
    uint64_t s=UINT64_C(0x9e3779b97f4a7c15)*(uint64_t)trial+1;
    for(int i=0;i<11;i++) rng_next(&s);
    uint64_t selector=s;
    for(int i=0;i<12;i++){
        uint64_t value=S3_KB0[i];
        for(int bit=0;bit<64;bit++) if((selector>>bit)&1) value^=S3_KBV[bit][i];
        KL[S3_LANES[i]]=value;
    }
}

static void make_min_plan(const uint8_t input[1600],int round,Plan *p){
    memset(p,0,sizeof(*p)); p->ib=RC[round];
    uint8_t patterns[320]; row_patterns(input,p->cnot,p->dnot,patterns);
    for(int i=0;i<320;i++) p->target[i]=(uint8_t)(row_min_target[patterns[i]] ^
        (i<64 && ((RC[round]>>i)&1)));
}

static void exact_round(Value state[25][64],int round,int last,const Plan *plan,
                        int *outputs,uint8_t *output_p){
    Value next[25][64],column[5][64],delta[5][64]; memcpy(next,state,sizeof(next));
    const uint8_t *cn=plan?plan->cnot:NULL,*dn=plan?plan->dnot:NULL;
    for(int x=0;x<5;x++){
        Value s=state[x][63];
        for(int y=1;y<5;y++) s=xor_value(s,state[x+5*y][63]);
        if(cn&&cn[64*x+63]) s=complement_representation(s);
        column[x][63]=s;
    }
    for(int z=0;z<64;z++){
        if(z<63) for(int x=0;x<5;x++){
            Value s=state[x][z];
            for(int y=1;y<5;y++) s=xor_value(s,state[x+5*y][z]);
            if(cn&&cn[64*x+z]) s=complement_representation(s);
            column[x][z]=s;
        }
        for(int x=0;x<5;x++){
            Value d=xor_value(column[(x+4)%5][z],column[(x+1)%5][(z+63)&63]);
            if(dn&&dn[64*x+z]) d=complement_representation(d);
            delta[x][z]=d;
        }
    }
    int ny=last?1:5;
    for(int Y=0;Y<ny;Y++)for(int z=0;z<64;z++){
        Value b[5],out[5];for(int X=0;X<5;X++){int y=X,x=(3*Y+X)%5,zz=(z-ROT[x][y])&63;b[X]=xor_value(state[x+5*y][zz],delta[x][zz]);}
        if(plan&&plan->ib==RC[round]&&!last){
            if(emitter_has_decisions[round])build_encoded_row(b,emitter_decisions[round][64*Y+z],out);
            else{int target=plan->target[64*Y+z]^(Y==0&&((RC[round]>>z)&1));build_target_row(b,target,out);}
        }
        else build_dynamic_row(b,last?15:31,out);
        for(int X=0;X<(last?4:5);X++)next[X+5*Y][z]=out[X];
    }
    for(int z=0;z<64;z++)next[0][z].p^=(RC[round]>>z)&1;
    memcpy(state,next,sizeof(next));
    int count=last?256:1600;
    for(int q=0;q<count;q++){Value v=state[q>>6][q&63];outputs[q]=v.n;output_p[q]=v.p;}
}

static void build_prefix_exact(const Plan *prefix,int outputs[1600],uint8_t output_p[1600]){
    Value state[25][64];reset_graph(256,1);
    for(int l=0;l<25;l++)for(int z=0;z<64;z++)state[l][z]=constant((KL[l]>>z)&1);
    for(int z=0;z<64;z++){state[1][z]=val(z,0);state[6][z]=val(64+z,0);state[4][z]=val(128+z,0);state[9][z]=val(192+z,0);
        state[11][z]=xor_value(xor_value(val(z,0),val(64+z,0)),constant((KL[11]>>z)&1));
        state[14][z]=xor_value(xor_value(val(128+z,0),val(192+z,0)),constant((KL[14]>>z)&1));}
    uint8_t scratch[1600];int nodes[1600];exact_round(state,0,0,NULL,nodes,scratch);exact_round(state,1,0,prefix,nodes,scratch);
    memcpy(outputs,nodes,sizeof(nodes));memcpy(output_p,scratch,1600);
}

static void build_body_exact(const uint8_t input[1600],int round,const Plan *plan,int outputs[1600],uint8_t output_p[1600]){
    Value state[25][64];reset_graph(1600,0);for(int q=0;q<1600;q++)state[q>>6][q&63]=val(q,input[q]);
    exact_round(state,round,0,plan,outputs,output_p);
}

static void build_last_generic(const uint8_t input[1600],int round,int outputs[256],uint8_t output_p[256]){
    Value S[25][64],C[5][64],D[5][64]; uint8_t hc[320]={0},hd[320]={0};
    reset_graph(1600,0); for(int q=0;q<1600;q++) S[q>>6][q&63]=val(q,input[q]);
    for(int z=0;z<64;z++){
        Value b[5],out[5];
        for(int X=0;X<5;X++){ int x=X,y=X,zz=(z-ROT[x][y])&63;
            Value d=lazy_d(S,C,D,hc,hd,NULL,NULL,x,zz); b[X]=xor_value(S[x+5*y][zz],d); }
        build_dynamic_row(b,15,out);
        for(int X=0;X<4;X++){ Value v=out[X]; if(X==0)v.p^=(RC[round]>>z)&1;
            outputs[64*X+z]=v.n; output_p[64*X+z]=v.p; }
    }
}

static long straight_count(int rounds,int full,Plan *prefix,Plan plans[24],uint8_t inputs[24][1600]){
    int nodes1600[1600],nodes256[256]; uint8_t polarity[1600],lastp[256]; long total=0;
    if(!full) memset(prefix,0,sizeof(*prefix));
    build_prefix_exact(prefix,nodes1600,polarity);
    long part=live_operation_count(nodes1600,1600,256);total+=part;
    if(full&&getenv("STEP_DEBUG"))fprintf(stderr,"segment 0-1 %ld\n",part);
    memcpy(inputs[2],polarity,1600);
    for(int r=2;r<rounds-1;r++){
        if(full) build_body_exact(polarity,r,&plans[r],nodes1600,polarity);
        else {
            make_min_plan(polarity,r,&plans[r]);
            build_body_exact(polarity,r,&plans[r],nodes1600,polarity);
        }
        part=live_operation_count(nodes1600,1600,1600);total+=part;
        if(full&&getenv("STEP_DEBUG"))fprintf(stderr,"segment %d %ld\n",r,part);
        memcpy(inputs[r+1],polarity,1600);
    }
    build_last_generic(polarity,rounds-1,nodes256,lastp);
    part=live_operation_count(nodes256,256,1600);total+=part;
    if(full&&getenv("STEP_DEBUG"))fprintf(stderr,"segment %d %ld\n",rounds-1,part);
    return total;
}

static int last_row_cost[32];

/* Static streaming allocator used by the charged emitter.  One graph segment
   is live at a time and the packed program is written as records are made. */
enum { EMIT_REGS=1936, EMIT_BUFFER=4096 };
static uint8_t ea_live[MAX_NODES],ea_busy[EMIT_REGS];
static uint16_t ea_last[MAX_NODES],ea_reg[MAX_NODES],ea_out_index[MAX_NODES];
static uint16_t ea_input_regs[1600];
static uint16_t ea_final_last[1600],ea_final_output[256];
static uint8_t ea_buffer[EMIT_BUFFER];static int ea_length,ea_bits;static uint64_t ea_acc;
static FILE *ea_file;static long ea_ops,ea_short,ea_forms[3],ea_mix[4];static int ea_peak;

static void ea_flush(void){if(ea_length&&fwrite(ea_buffer,1,(size_t)ea_length,ea_file)!=(size_t)ea_length)fail("step program write");ea_length=0;}
static void ea_byte(uint8_t value){ea_buffer[ea_length++]=value;if(ea_length==EMIT_BUFFER)ea_flush();}
static void ea_record(int op,int d,int a,int b){
    if(op<0||op>3||d<0||a<0||b<0||d>=2048||a>=2048||b>=2048)fail("native step field overflow");
    if(d==b&&op!=3){int t=a;a=b;b=t;}
    uint64_t word;int width,same=d==a;
    if(same){word=(uint64_t)op|4|((uint64_t)a<<3);width=op==3?14:25;if(op!=3)word|=(uint64_t)b<<14;ea_short++;}
    else{word=(uint64_t)op|((uint64_t)d<<3)|((uint64_t)a<<14);width=op==3?25:36;if(op!=3)word|=(uint64_t)b<<25;}
    ea_forms[width==14?0:width==25?1:2]++;ea_mix[op]++;ea_ops++;
    ea_acc|=word<<ea_bits;ea_bits+=width;while(ea_bits>=8){ea_byte((uint8_t)ea_acc);ea_acc>>=8;ea_bits-=8;}
}

static void ea_segment(const int *outputs,int output_count,int input_count,int round,int rounds,int final){
    long before_ops=ea_ops;int expected_ops=live_operation_count(outputs,output_count,input_count);
    memset(ea_live,0,(size_t)node_count);memset(ea_last,0,(size_t)node_count*sizeof(*ea_last));
    memset(ea_out_index,0xff,(size_t)node_count*sizeof(*ea_out_index));memset(ea_busy,0,sizeof(ea_busy));
    for(int j=0;j<output_count;j++){int node=outputs[j];if(node<input_count||ea_out_index[node]!=UINT16_MAX)fail("shared state output");ea_live[node]=1;ea_out_index[node]=(uint16_t)j;}
    for(int i=node_count-1;i>=input_count;i--)if(ea_live[i]){ea_live[nodes[i].a]=1;if(nodes[i].op!=O_NOT)ea_live[nodes[i].b]=1;}
    for(int i=input_count;i<node_count;i++)if(ea_live[i]){ea_last[nodes[i].a]=(uint16_t)i;if(nodes[i].op!=O_NOT)ea_last[nodes[i].b]=(uint16_t)i;}
    for(int j=0;j<output_count;j++)ea_last[outputs[j]]=UINT16_MAX;
    for(int i=0;i<input_count;i++){ea_reg[i]=ea_input_regs[i];if(ea_last[i])ea_busy[ea_input_regs[i]]=1;}
    for(int i=input_count;i<node_count;i++)if(ea_live[i]){
        int op=nodes[i].op,a=nodes[i].a,b=op==O_NOT?a:nodes[i].b,ra=ea_reg[a],rb=op==O_NOT?0:ea_reg[b];
        if(ea_last[a]==i)ea_busy[ra]=0;
        if(b!=a&&ea_last[b]==i)ea_busy[rb]=0;
        int destination=-1;
        if(final&&ea_out_index[i]!=UINT16_MAX){destination=ea_out_index[i];if(ea_busy[destination])fail("digest destination busy");}
        else for(int physical=0;physical<EMIT_REGS;physical++){
            if(ea_busy[physical])continue;
            if(!final&&round==rounds-2&&physical<256&&ea_out_index[i]!=UINT16_MAX){int state_index=ea_out_index[i];if(ea_final_output[physical]<ea_final_last[state_index])continue;}
            if(final&&physical<256){int output_node=outputs[physical];if(output_node!=i&&ea_last[i]>output_node)continue;}
            destination=physical;break;
        }
        if(destination<0)fail("emitter register exhausted");
        ea_busy[destination]=1;ea_reg[i]=(uint16_t)destination;
        if(destination+1>ea_peak)ea_peak=destination+1;
        int code=op==O_XOR?0:op==O_AND?1:op==O_OR?2:3;ea_record(code,destination,ra,rb);
    }
    for(int j=0;j<output_count;j++)ea_input_regs[j]=ea_reg[outputs[j]];
    for(int r=0;r<EMIT_REGS;r++){
        int expected=0;for(int j=0;j<output_count;j++)if(ea_input_regs[j]==r){expected=1;break;}
        if((int)ea_busy[r]!=expected)fail("emitter boundary live set");
    }
    if(ea_ops-before_ops!=expected_ops){fprintf(stderr,"segment round=%d emitted=%ld expected=%d nodes=%d\n",round,ea_ops-before_ops,expected_ops,node_count);fail("emitter DCE mismatch");}
}

static void emit_straight(const char *path,int rounds,Plan *prefix,Plan plans[24]){
    ea_file=fopen(path,"wb");if(!ea_file)fail("step output");ea_length=ea_bits=0;ea_acc=0;ea_ops=ea_short=0;ea_peak=256;
    memset(ea_forms,0,sizeof(ea_forms));memset(ea_mix,0,sizeof(ea_mix));for(int i=0;i<256;i++)ea_input_regs[i]=(uint16_t)i;
    int nodes1600[1600],nodes256[256];uint8_t polarity[1600],lastp[256];
    /* Prebuild the final graph to identify state inputs that remain live past
       the first digest definition.  Those inputs may not occupy low digest
       registers at the preceding boundary. */
    build_prefix_exact(prefix,nodes1600,polarity);
    for(int r=2;r<rounds-1;r++)build_body_exact(polarity,r,&plans[r],nodes1600,polarity);
    build_last_generic(polarity,rounds-1,nodes256,lastp);
    memset(ea_live,0,(size_t)node_count);memset(ea_last,0,(size_t)node_count*sizeof(*ea_last));for(int j=0;j<256;j++)ea_live[nodes256[j]]=1;
    for(int i=node_count-1;i>=1600;i--)if(ea_live[i]){ea_live[nodes[i].a]=1;if(nodes[i].op!=O_NOT)ea_live[nodes[i].b]=1;}
    for(int i=1600;i<node_count;i++)if(ea_live[i]){ea_last[nodes[i].a]=(uint16_t)i;if(nodes[i].op!=O_NOT)ea_last[nodes[i].b]=(uint16_t)i;}
    for(int q=0;q<1600;q++)ea_final_last[q]=ea_last[q];
    for(int j=0;j<256;j++)ea_final_output[j]=(uint16_t)nodes256[j];
    /* Rebuild and emit from round zero. */
    build_prefix_exact(prefix,nodes1600,polarity);ea_segment(nodes1600,1600,256,1,rounds,0);
    for(int r=2;r<rounds-1;r++){build_body_exact(polarity,r,&plans[r],nodes1600,polarity);ea_segment(nodes1600,1600,1600,r,rounds,0);}
    build_last_generic(polarity,rounds-1,nodes256,lastp);ea_segment(nodes256,256,1600,rounds-1,rounds,1);
    if(ea_bits)ea_byte((uint8_t)ea_acc);
    ea_flush();if(fclose(ea_file))fail("step close");
    uint64_t pd[4]={0,0,0,0};for(int bit=0;bit<256;bit++)pd[bit>>6]|=(uint64_t)(lastp[bit]&1)<<(bit&63);
    fprintf(stderr,"emitted step_ops=%ld peak=%d bytes=%ld forms14=%ld forms25=%ld forms36=%ld short=%ld mix=%ld,%ld,%ld,%ld pd=%016lx,%016lx,%016lx,%016lx\n",
        ea_ops,ea_peak,(ea_forms[0]*14+ea_forms[1]*25+ea_forms[2]*36+7)/8,ea_forms[0],ea_forms[1],ea_forms[2],ea_short,
        ea_mix[0],ea_mix[1],ea_mix[2],ea_mix[3],
        (unsigned long)pd[0],(unsigned long)pd[1],(unsigned long)pd[2],(unsigned long)pd[3]);
}

/* Cost of a last-round chi row, where only outputs 0..3 are live. */
static void make_last_row_cost(void){
    for(int pin=0;pin<32;pin++){
        int best=1<<30;
        for(int subset=0;subset<32;subset++){
            int bp[5];
            for(int x=0;x<5;x++) bp[x]=((pin>>x)&1)^((subset>>x)&1);
            for(int trick=-1;trick<5;trick++){
                int k=(trick+1)%5;
                if(trick>=0 && (!((15>>trick)&1)||!((15>>k)&1))) continue;
                int cost=__builtin_popcount((unsigned)subset),op[5]={0,0,0,0,0};
                if(trick>=0){
                    int a=bp[(k+1)%5]^1,b=bp[(k+2)%5];
                    int tp=a==b?a:0;
                    cost+=(a==b?1:2)+1; op[k]=bp[k]^tp;
                }
                for(int x=0;x<5;x++) if((15>>x)&1){
                    if(trick>=0&&x==k) continue;
                    int a=(x==trick?op[k]:bp[(x+1)%5])^1,b=bp[(x+2)%5];
                    cost+=(a==b?1:2)+1;
                }
                if(cost<best) best=cost;
            }
        }
        last_row_cost[pin]=best;
    }
}

/* One-round-lookahead annealer.  Each move updates only the affected chi rows,
   so the charged 200,000,000-iteration campaign is practical and auditable. */
static void anneal_straight(const uint8_t input[1600],int round,int rounds,long iterations,Plan *result){
    uint8_t zero[320]={0},pat0[320],pat1[320],outv[320];
    uint8_t cnot[320]={0},dnot[320]={0},bestc[320]={0},bestd[320]={0},besto[320];
    uint16_t vrow[5][64][5]; uint8_t vbit[5][64][5];
    row_patterns(input,zero,zero,pat0);
    for(int i=0;i<320;i++) outv[i]=row_min_target[pat0[i]];
    uint8_t next[1600]; targets_to_state(outv,next);
    for(int z=0;z<64;z++) next[z]^=(uint8_t)((RC[round]>>z)&1);
    row_patterns(next,zero,zero,pat1);
    for(int x=0;x<5;x++) for(int zz=0;zz<64;zz++) for(int y=0;y<5;y++){
        int Y=(2*(x-y)+10)%5,z=(zz+ROT[x][y])&63;
        vrow[x][zz][y]=(uint16_t)(64*Y+z); vbit[x][zz][y]=(uint8_t)(1<<y);
    }
    int next_last=round+1==rounds-1;
    #define COST0(i) ((int)row_table[pat0[(i)]][outv[(i)]].cost)
    #define COST1(i) (next_last? ((i)<64?last_row_cost[pat1[(i)]]:0) : (int)row_min_cost[pat1[(i)]])
    long a0=0,a1=0;
    for(int i=0;i<320;i++){a0+=COST0(i);a1+=COST1(i);}
    long cost=16*a0+3*a1,best=cost;
    memcpy(besto,outv,sizeof(besto));
    uint64_t seed=UINT64_C(0x2545f4914f6cdd1d)^(uint64_t)round*UINT64_C(0x9e3779b97f4a7c15)^UINT64_C(0x1234567);
    #define FLIP0(rw,bit) do{cost-=16*COST0(rw);pat0[(rw)]^=(uint8_t)(bit);cost+=16*COST0(rw);}while(0)
    #define FLIPD0(xx,zz) do{for(int kk=0;kk<5;kk++){int rw=vrow[(xx)][(zz)][kk];FLIP0(rw,vbit[(xx)][(zz)][kk]);}}while(0)
    #define FLIP1(rw,bit) do{cost-=3*COST1(rw);pat1[(rw)]^=(uint8_t)(bit);cost+=3*COST1(rw);}while(0)
    #define FLIPD1(xx,zz) do{for(int kk=0;kk<5;kk++){int rw=vrow[(xx)][(zz)][kk];FLIP1(rw,vbit[(xx)][(zz)][kk]);}}while(0)
    for(long it=0;it<iterations;it++){
        uint64_t random=rng_next(&seed);int move=(int)(random%5),x=(int)((random>>3)%5),z=(int)((random>>8)&63),Y=(int)((random>>16)%5);
        if(move>=2)move=2;
        int mask=((random>>24)&1)?(int)(1+((random>>28)%31)):(1<<x);
        long before=cost;
        #define APPLY_MOVE() do{ \
            if(move==0){FLIPD0(x,z);dnot[64*x+z]^=1;cost+=dnot[64*x+z]?16:-16;} \
            else if(move==1){int x1=(x+1)%5,x2=(x+4)%5,z2=(z+1)&63;FLIPD0(x1,z);FLIPD0(x2,z2);cnot[64*x+z]^=1;cost+=cnot[64*x+z]?16:-16;} \
            else{int rw=64*Y+z;cost-=16*COST0(rw);outv[rw]^=(uint8_t)mask;cost+=16*COST0(rw); \
                for(int X=0;X<5;X++)if((mask>>X)&1){int x1=(X+1)%5,x2=(X+4)%5,z2=(z+1)&63,rw1=vrow[X][z][Y];FLIP1(rw1,vbit[X][z][Y]);FLIPD1(x1,z);FLIPD1(x2,z2);}} \
        }while(0)
        APPLY_MOVE(); long difference=cost-before;
        double temperature=19.2*bounded_exp(-3.1780538303479458*(double)it/(double)(iterations?iterations:1));
        double uniform=(double)(rng_next(&seed)>>11)*(1.0/9007199254740992.0);
        int accept=difference<=0||uniform<bounded_exp(-(double)difference/temperature);
        if(accept){if(cost<best){best=cost;memcpy(bestc,cnot,sizeof(bestc));memcpy(bestd,dnot,sizeof(bestd));memcpy(besto,outv,sizeof(besto));}}
        else APPLY_MOVE();
    }
    memset(result,0,sizeof(*result));result->ib=RC[round];
    memcpy(result->cnot,bestc,320);memcpy(result->dnot,bestd,320);
    for(int i=0;i<320;i++) result->target[i]=(uint8_t)(besto[i]^(i<64&&((RC[round]>>i)&1)));
    #undef APPLY_MOVE
    #undef FLIPD1
    #undef FLIP1
    #undef FLIPD0
    #undef FLIP0
    #undef COST1
    #undef COST0
}

static void hex_bytes(FILE *f,const uint8_t *data,int n){
    static const char h[]="0123456789abcdef"; for(int i=0;i<n;i++){fputc(h[data[i]>>4],f);fputc(h[data[i]&15],f);}
}

static void hex_bits(FILE *f,const uint8_t *bits,int n){
    uint8_t packed[200]={0};
    if(n>(int)(8*sizeof(packed))) fail("bitset too wide");
    for(int i=0;i<n;i++) packed[i>>3]|=(uint8_t)((bits[i]&1)<<(i&7));
    hex_bytes(f,packed,(n+7)/8);
}

static void write_plan_file(const char *path,int rounds,int trial,const Plan *prefix,Plan plans[24],uint8_t inputs[24][1600]){
    FILE *f=fopen(path,"w"); if(!f)fail("plan output");
    fprintf(f,"trial %d\nnr %d optmode 4 chained 1 lasttrick 1 notfold 0\n",trial,rounds);
    fprintf(f,"F1 ");hex_bits(f,prefix->dnot,320);fprintf(f,"\nG1 ");hex_bits(f,prefix->cnot,320);fputc('\n',f);
    for(int r=2;r<rounds;r++){ fprintf(f,"FG %d ",r);hex_bits(f,plans[r].dnot,320);fputc(' ',f);hex_bits(f,plans[r].cnot,320);fputc('\n',f); }
    for(int r=0;r<rounds;r++){ fprintf(f,"PHI %d ",r);for(int i=0;i<200;i++)fprintf(f,"00");fputc('\n',f); }
    for(int r=2;r<rounds;r++){fprintf(f,"POL %d ",r);hex_bits(f,inputs[r],1600);fputc('\n',f);}
    for(int r=2;r<rounds-1;r++){
        uint8_t patterns[320];row_patterns(inputs[r],plans[r].cnot,plans[r].dnot,patterns);fprintf(f,"DEC %d ",r);
        for(int i=0;i<320;i++){int target=plans[r].target[i]^(i<64&&((RC[r]>>i)&1));Decision d=row_table[patterns[i]][target];
            uint16_t word=(uint16_t)(d.subset|d.tricks<<5|d.select_mask<<10);fprintf(f,"%02x%02x",word&255,word>>8);}
        fputc('\n',f);
        fprintf(f,"TGT %d ",r);hex_bytes(f,plans[r].target,320);fputc('\n',f);
    }
    if(fclose(f))fail("plan close");
}

static void usage(void){fprintf(stderr,"usage: step_search cheap ROUNDS | full ROUNDS TRIAL ITERATIONS PLAN | multi TRIAL ITERATIONS OUTDIR [R,R,...]\n");exit(2);}

#ifndef EMITTER_ONLY
int generator_work(int argc,char **argv){
    if(argc<3)usage();
    make_row_table(); make_last_row_cost();
    fprintf(stderr,"chained-table entries=1024 candidate_evaluations=1015808 truth_checks=32768 bytes=%zu checksum=%016lx\n",sizeof(row_table),(unsigned long)chained_table_checksum());
    if(!strcmp(argv[1],"multi")){
        if(argc!=5&&argc!=6)usage();
        int trial=atoi(argv[2]);long iterations=strtol(argv[3],NULL,10);const char *outdir=argv[4];
        int wanted[25]={0},max_round=0;
        if(argc==5){const int defaults[7]={9,13,17,19,20,21,22};for(int j=0;j<7;j++){wanted[defaults[j]]=1;max_round=defaults[j];}}
        else{
            const char *p=argv[5];
            while(*p){char *end=NULL;long value=strtol(p,&end,10);if(end==p||value<7||value>24)usage();wanted[value]=1;if(value>max_round)max_round=(int)value;p=end;if(*p==',')p++;else if(*p)usage();}
        }
        set_s3_trial(trial);Plan prefix={0},plans[24]={0};uint8_t inputs[24][1600]={{0}};
        int nodes[1600];uint8_t polarity[1600];
        optimize_prefix(&prefix,nodes,polarity);build_prefix_exact(&prefix,nodes,polarity);memcpy(inputs[2],polarity,1600);
        for(int r=2;r<=max_round-2;r++){
            int target_rounds=wanted[r+2]?r+2:0;
            if(target_rounds&&r<max_round-2){
                Plan candidate[24];uint8_t candidate_inputs[24][1600];uint8_t tail_polarity[1600];
                memcpy(candidate,plans,sizeof(candidate));memcpy(candidate_inputs,inputs,sizeof(candidate_inputs));
                anneal_straight(polarity,r,target_rounds,iterations,&candidate[r]);
                memcpy(tail_polarity,polarity,1600);build_body_exact(tail_polarity,r,&candidate[r],nodes,tail_polarity);
                memcpy(candidate_inputs[r+1],tail_polarity,1600);
                char path[4096];snprintf(path,sizeof(path),"%s/r%d-t%d.plan",outdir,target_rounds,trial);
                long count=straight_count(target_rounds,1,&prefix,candidate,candidate_inputs);
                fprintf(stderr,"trial=%d rounds=%d iterations=%ld step_ops=%ld\n",trial,target_rounds,iterations,count);
                write_plan_file(path,target_rounds,trial,&prefix,candidate,candidate_inputs);
            }
            anneal_straight(polarity,r,max_round,iterations,&plans[r]);
            build_body_exact(polarity,r,&plans[r],nodes,polarity);memcpy(inputs[r+1],polarity,1600);
            if(target_rounds&&r==max_round-2){
                char path[4096];snprintf(path,sizeof(path),"%s/r%d-t%d.plan",outdir,max_round,trial);
                long count=straight_count(max_round,1,&prefix,plans,inputs);
                fprintf(stderr,"trial=%d rounds=%d iterations=%ld step_ops=%ld\n",trial,max_round,iterations,count);
                write_plan_file(path,max_round,trial,&prefix,plans,inputs);
            }
        }
        return 0;
    }
    int rounds=atoi(argv[2]);
    if(rounds<7||rounds>24)usage();
    if(!strcmp(argv[1],"cheap")){
        for(int trial=1000;trial<1512;trial++){set_s3_trial(trial);Plan prefix={0},plans[24]={0};uint8_t inputs[24][1600]={{0}};
            long count=straight_count(rounds,0,&prefix,plans,inputs);printf("{\"trial\":%d,\"cheap_count\":%ld}\n",trial,count);fflush(stdout);}return 0;
    }
    if(!strcmp(argv[1],"full")){
        if(argc!=6&&argc!=7)usage();
        int trial=atoi(argv[3]);long iterations=strtol(argv[4],NULL,10);set_s3_trial(trial);
        Plan prefix={0},plans[24]={0};uint8_t inputs[24][1600]={{0}};int nodes[1600];uint8_t polarity[1600];
        optimize_prefix(&prefix,nodes,polarity);build_prefix_exact(&prefix,nodes,polarity);memcpy(inputs[2],polarity,1600);
        for(int r=2;r<rounds-1;r++){anneal_straight(polarity,r,rounds,iterations,&plans[r]);build_body_exact(polarity,r,&plans[r],nodes,polarity);memcpy(inputs[r+1],polarity,1600);}
        long count=straight_count(rounds,1,&prefix,plans,inputs);fprintf(stderr,"trial=%d rounds=%d iterations=%ld step_ops=%ld\n",trial,rounds,iterations,count);
        write_plan_file(argv[5],rounds,trial,&prefix,plans,inputs);if(argc==7)emit_straight(argv[6],rounds,&prefix,plans);return 0;
    }
    usage();return 2;
}

#ifdef FREESTANDING
extern long construction_vmhwm_bytes(void);
int main(int argc,char **argv){
    int status=generator_work(argc,argv);
    fprintf(stderr,"construction VmHWM %ld bytes\n",construction_vmhwm_bytes());
    return status;
}
#else
int main(int argc,char **argv){return generator_work(argc,argv);}
#endif
#else
extern long construction_vmhwm_bytes(void);
extern long construction_read_file(const char *,void *,size_t);
static uint8_t plan_text[65536];
static int hex_digit(int c){if(c>='0'&&c<='9')return c-'0';if(c>='a'&&c<='f')return c-'a'+10;if(c>='A'&&c<='F')return c-'A'+10;return -1;}
static void parse_hex_field(const char *text,uint8_t *output,int bytes){
    for(int i=0;i<bytes;i++){int high=hex_digit(text[2*i]),low=hex_digit(text[2*i+1]);if(high<0||low<0)fail("plan hex");output[i]=(uint8_t)(high*16+low);}
    if(text[2*bytes]&&text[2*bytes]!=' '&&text[2*bytes]!='\n'&&text[2*bytes]!='\r')fail("plan hex length");
}
static void parse_bit_field(const char *text,uint8_t *output,int bits){uint8_t packed[200];int bytes=(bits+7)/8;parse_hex_field(text,packed,bytes);for(int i=0;i<bits;i++)output[i]=(packed[i>>3]>>(i&7))&1;}
static char *skip_word(char *p){while(*p&&*p!=' '&&*p!='\n')p++;while(*p==' ')p++;return p;}
static int parse_number(char **cursor){char *p=*cursor;int value=0;if(*p<'0'||*p>'9')fail("plan number");while(*p>='0'&&*p<='9')value=value*10+(*p++-'0');while(*p==' ')p++;*cursor=p;return value;}
static void parse_emitter_plan(const char *path,int expected_rounds,int *trial,Plan *prefix,Plan plans[24]){
    long length=construction_read_file(path,plan_text,sizeof(plan_text)-1);if(length<=0||length>=(long)sizeof(plan_text))fail("plan read");plan_text[length]=0;
    memset(prefix,0,sizeof(*prefix));memset(plans,0,24*sizeof(*plans));memset(emitter_has_decisions,0,sizeof(emitter_has_decisions));for(int r=0;r<24;r++)plans[r].ib=RC[r];
    int seen_nr=0,seen_f1=0,seen_g1=0,seen_target[24]={0};char *line=(char*)plan_text;
    while(*line){char *end=line;while(*end&&*end!='\n')end++;char saved=*end;*end=0;
        char *p=line;
        if(!memcmp(p,"trial ",6)){p+=6;*trial=parse_number(&p);}
        else if(!memcmp(p,"nr ",3)){p+=3;int nr=parse_number(&p);if(nr!=expected_rounds)fail("plan round count");seen_nr=1;}
        else if(!memcmp(p,"F1 ",3)){parse_bit_field(p+3,prefix->dnot,320);seen_f1=1;}
        else if(!memcmp(p,"G1 ",3)){parse_bit_field(p+3,prefix->cnot,320);seen_g1=1;}
        else if(!memcmp(p,"FG ",3)){p+=3;int r=parse_number(&p);if(r<2||r>=expected_rounds)fail("FG round");parse_bit_field(p,plans[r].dnot,320);p=skip_word(p);parse_bit_field(p,plans[r].cnot,320);}
        else if(!memcmp(p,"DEC ",4)){p+=4;int r=parse_number(&p);if(r<2||r>=expected_rounds-1)fail("DEC round");uint8_t raw[640];parse_hex_field(p,raw,640);for(int i=0;i<320;i++)emitter_decisions[r][i]=(uint16_t)(raw[2*i]|raw[2*i+1]<<8);}
        else if(!memcmp(p,"TGT ",4)){p+=4;int r=parse_number(&p);if(r<2||r>=expected_rounds-1)fail("TGT round");parse_hex_field(p,plans[r].target,320);seen_target[r]=1;}
        *end=saved;line=saved?end+1:end;
    }
    if(!seen_nr||!seen_f1||!seen_g1)fail("incomplete plan header");for(int r=2;r<expected_rounds-1;r++)if(!seen_target[r])fail("missing target plan");
}
int main(int argc,char **argv){
    if(argc!=4)fail("usage: construction_emitter ROUNDS PLAN PROGRAM");int rounds=atoi(argv[1]),trial=0;if(rounds<7||rounds>24)fail("rounds");
    make_row_table();make_last_row_cost();fprintf(stderr,"chained-table entries=1024 candidate_evaluations=1015808 truth_checks=32768 bytes=%zu checksum=%016lx\n",sizeof(row_table),(unsigned long)chained_table_checksum());static Plan prefix,plans[24];parse_emitter_plan(argv[2],rounds,&trial,&prefix,plans);set_s3_trial(trial);emit_straight(argv[3],rounds,&prefix,plans);
    fprintf(stderr,"construction emitter trial=%d VmHWM %ld bytes\n",trial,construction_vmhwm_bytes());return 0;
}
#endif

```

### s3_basis.h

```c
#ifndef S3_BASIS_H
#define S3_BASIS_H
static const uint64_t S3_KB0[12]={UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0xffffffffffffffff),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0xffffffffffffffff),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0xffffffffffffffff),UINT64_C(0x8000000000000006),UINT64_C(0xffffffffffffffff)};
static const uint64_t S3_KBV[64][12]={
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000001),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x2000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x4000000000000000),UINT64_C(0x8000000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x4000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x8000000000000000),UINT64_C(0x0000000000000001)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000004),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x8000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000001),UINT64_C(0x0000000000000002)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000008),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000001),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000004)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000010),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000004),UINT64_C(0x0000000000000008)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000020),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000004),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000008),UINT64_C(0x0000000000000010)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000040),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000008),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000010),UINT64_C(0x0000000000000020)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000080),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000010),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000020),UINT64_C(0x0000000000000040)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000100),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000020),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000040),UINT64_C(0x0000000000000080)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000200),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000040),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000080),UINT64_C(0x0000000000000100)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000400),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000080),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000100),UINT64_C(0x0000000000000200)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000800),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000100),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000200),UINT64_C(0x0000000000000400)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000001000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000200),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000400),UINT64_C(0x0000000000000800)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000002000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000400),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000800),UINT64_C(0x0000000000001000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000004000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000800),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000001000),UINT64_C(0x0000000000002000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000008000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000001000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000002000),UINT64_C(0x0000000000004000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000010000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000002000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000004000),UINT64_C(0x0000000000008000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000020000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000004000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000008000),UINT64_C(0x0000000000010000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000040000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000008000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000010000),UINT64_C(0x0000000000020000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000080000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000010000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000020000),UINT64_C(0x0000000000040000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000100000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000020000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000040000),UINT64_C(0x0000000000080000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000200000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000040000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000080000),UINT64_C(0x0000000000100000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000400000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000080000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000100000),UINT64_C(0x0000000000200000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000000800000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000100000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000200000),UINT64_C(0x0000000000400000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000001000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000200000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000400000),UINT64_C(0x0000000000800000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000002000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000400000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000800000),UINT64_C(0x0000000001000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000004000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000800000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000001000000),UINT64_C(0x0000000002000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000008000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000001000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000002000000),UINT64_C(0x0000000004000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000010000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000002000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000004000000),UINT64_C(0x0000000008000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000020000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000004000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000008000000),UINT64_C(0x0000000010000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000040000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000008000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000010000000),UINT64_C(0x0000000020000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000080000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000010000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000020000000),UINT64_C(0x0000000040000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000100000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000020000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000040000000),UINT64_C(0x0000000080000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000200000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000040000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000080000000),UINT64_C(0x0000000100000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000400000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000080000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000100000000),UINT64_C(0x0000000200000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000000800000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000100000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000200000000),UINT64_C(0x0000000400000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000001000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000200000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000400000000),UINT64_C(0x0000000800000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000002000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000400000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000800000000),UINT64_C(0x0000001000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000004000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000800000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000001000000000),UINT64_C(0x0000002000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000008000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000001000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000002000000000),UINT64_C(0x0000004000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000010000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000002000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000004000000000),UINT64_C(0x0000008000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000020000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000004000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000008000000000),UINT64_C(0x0000010000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000040000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000008000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000010000000000),UINT64_C(0x0000020000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000080000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000010000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000020000000000),UINT64_C(0x0000040000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000100000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000020000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000040000000000),UINT64_C(0x0000080000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000200000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000040000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000080000000000),UINT64_C(0x0000100000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000400000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000080000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000100000000000),UINT64_C(0x0000200000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0000800000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000100000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000200000000000),UINT64_C(0x0000400000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0001000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000200000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000400000000000),UINT64_C(0x0000800000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0002000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000400000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000800000000000),UINT64_C(0x0001000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0004000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000800000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0001000000000000),UINT64_C(0x0002000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0008000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0001000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0002000000000000),UINT64_C(0x0004000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0010000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0002000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0004000000000000),UINT64_C(0x0008000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0020000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0004000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0008000000000000),UINT64_C(0x0010000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0040000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0008000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0010000000000000),UINT64_C(0x0020000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0080000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0010000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0020000000000000),UINT64_C(0x0040000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0100000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0020000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0040000000000000),UINT64_C(0x0080000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0200000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0040000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0080000000000000),UINT64_C(0x0100000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0400000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0080000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0100000000000000),UINT64_C(0x0200000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x0800000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0100000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0200000000000000),UINT64_C(0x0400000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x1000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0200000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0400000000000000),UINT64_C(0x0800000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x2000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0400000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0800000000000000),UINT64_C(0x1000000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x4000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0800000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x1000000000000000),UINT64_C(0x2000000000000000)},
 {UINT64_C(0x0000000000000000),UINT64_C(0x8000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x1000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x2000000000000000),UINT64_C(0x4000000000000000)},
};
#endif

```

### construction_prefilter.c

```c
/* Freestanding emitter for the separate native 15-OR digest prefilter. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

extern long construction_vmhwm_bytes(void);

typedef struct { FILE *out; uint64_t pending; int used; long bytes; } Writer;

static void put(Writer *w,uint64_t value,int width){
    w->pending|=value<<w->used;w->used+=width;
    while(w->used>=8){uint8_t byte=(uint8_t)w->pending;if(fwrite(&byte,1,1,w->out)!=1)exit(2);w->bytes++;w->pending>>=8;w->used-=8;}
}

int main(int argc,char **argv){
    if(argc!=3){fprintf(stderr,"usage: construction_prefilter REGISTER OUTPUT\n");return 2;}
    int d=atoi(argv[1]);if(d<0||d>=2048)return 2;FILE *out=fopen(argv[2],"wb");if(!out)return 2;Writer w={out,0,0,0};
    put(&w,2|((uint64_t)d<<3)|((uint64_t)240<<14)|((uint64_t)241<<25),36);
    for(int plane=242;plane<256;plane++)put(&w,2|4|((uint64_t)d<<3)|((uint64_t)plane<<14),25);
    if(w.used){uint8_t byte=(uint8_t)w.pending;if(fwrite(&byte,1,1,out)!=1)return 2;w.bytes++;}
    if(fclose(out)||w.bytes!=49)return 2;
    fprintf(stderr,"prefilter instructions=15 bytes=%ld register=%d VmHWM %ld bytes\n",w.bytes,d,construction_vmhwm_bytes());return 0;
}

```

### construction_scan_template.c

```c
/* Freestanding float mirror for the charged finite parameter scan. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "scan_candidates.h"
extern long construction_vmhwm_bytes(void);
static const long double LN2=0.693147180559945309417232121458176568L,M=1.1579208923731619542357098500868790785e77L,GRID=2.475880078570760549798248448e27L,W=6.33825300114114700748351602688e29L;
static uint64_t scan_evaluations,scan_bins;
static long double lexp(long double x){if(x<-11000.0L)return 0.0L;int k=(int)(x/LN2);if((long double)k*LN2>x)k--;long double r=x-(long double)k*LN2,term=1.0L,sum=1.0L;for(int i=1;i<=32;i++){term*=r/(long double)i;sum+=term;}while(k>0){sum*=2.0L;k--;}while(k<0){sum*=0.5L;k++;}return sum;}
static long double llog(long double x){if(!(x>0))return -1.0L/0.0L;int e=0;while(x>=2.0L){x*=0.5L;e++;}while(x<1.0L){x*=2.0L;e--;}long double y=(x-1.0L)/(x+1.0L),p=y*y,term=y,sum=0;for(int k=1;k<=101;k+=2){sum+=term/(long double)k;term*=p;}return 2.0L*sum+(long double)e*LN2;}
static long double success(uint64_t t,const Candidate *c){
 scan_evaluations++;scan_bins+=c->j;
 long double tb=(long double)t*GRID,theta=(long double)c->dt/2.658455991569831744e36L,logq=-theta,qstep=lexp(W*logq),previous=1.0L,covered=0.0L;
 long double delta=256.0L*W,first=256.0L*(tb-W),collision=lexp(-first*(first-1.0L)/(2.0L*M));
 long double ratio=lexp((2.0L*first*delta-delta*delta-delta)/(2.0L*M)),ratio_step=lexp(-delta*delta/M);
 for(uint32_t j=1;j<=c->j;j++){long double current=previous*qstep;if(tb>(long double)j*W)covered+=(previous-current)*(1.0L-collision);previous=current;collision*=ratio;ratio*=ratio_step;}
 long double n=256.0L*tb,mean=n*theta,available=(long double)(5*c->table-256);if(!(available>mean))return -1.0L;
 long double f2=lexp(-mean+available*(1.0L+llog(mean/available))),f3=(long double)(5*c->table)/(theta*theta*M),alias=(long double)(5*c->table)*(long double)(5*c->table)/2251799813685248.0L;
 long double trails=(long double)(5*c->table),lrc=(long double)c->j*W,g6=lexp(lrc*logq)*(1.0L+lrc*theta),coincidence=1.0L-lexp(-n*n/(2.0L*M)-n*n*n/(3.0L*M*M));
 long double inflation=lexp(-trails*llog(1.0L-n/M));
 long double f6=2.0L*g6*coincidence*inflation;
 return covered-(f2+f3+alias+8.077935669463161e-28L+f6+8.673617379884035e-19L+3.0814879110195774e-33L*(1.0L+f6));
}
static uint64_t least_tb(const Candidate *c){uint64_t lo=HINT_T>SPAN?HINT_T-SPAN:1,hi=HINT_T+SPAN;long double theta=(long double)c->dt/2.658455991569831744e36L;uint64_t domain=(uint64_t)(((long double)(5*c->table-256)/(256.0L*theta))/GRID);if(hi>=domain)hi=domain-1;if(hi<=lo||success(hi,c)<0.39L)return 0;while(success(lo,c)>=0.39L&&lo>SPAN)lo-=SPAN;while(hi-lo>1){uint64_t mid=(lo+hi)/2;if(success(mid,c)>=0.39L)hi=mid;else lo=mid;}return hi;}
static long double total_cost(const Candidate *c,uint64_t t){long double tb=(long double)t*GRID,lrc=(long double)c->j*W,hit=tb*(1.0L+1.0L/1048576.0L)/256.0L+1.0L+lrc;long double gap=(lrc+(long double)c->table-2.0L)/(long double)(c->table-1),nck=(lrc-1.0L)/gap+1.0L;long double replay=(long double)c->replay_rate*lrc+(long double)c->replay_g*gap+(long double)c->replay_nck*nck+(long double)c->replay_const;long double trails=5.0L*c->table;long double rare=(hit+1.0L)*c->hit+(trails-255.0L)*(c->dp_fixed+c->probe_word*c->table)+(trails-256.0L)*(c->restart+3)+c->restart_halt+c->deadline+c->setup;return tb*(STEP_OPS+19.0L)+replay+rare+PREPROCESSING;}
int main(void){int best=-1;uint64_t best_t=0;long double best_cost=0;for(unsigned i=0;i<sizeof(candidates)/sizeof(candidates[0]);i++){uint64_t t=least_tb(&candidates[i]);if(!t)continue;long double cost=total_cost(&candidates[i],t);if(best<0||cost<best_cost){best=(int)i;best_t=t;best_cost=cost;}}if(best<0){printf("no candidate hint_success_scaled=%ld\n",(long)(success(HINT_T,&candidates[0])*1000000000000.0L));return 2;}const Candidate *c=&candidates[best];printf("candidate=%d table=%d dt=%d j=%u tb_grid=%lu memory=%d\n",best,c->table,c->dt,c->j,(unsigned long)best_t,c->memory);fprintf(stderr,"scan candidates=%lu evaluations=%lu bins=%lu VmHWM %ld bytes\n",(unsigned long)(sizeof(candidates)/sizeof(candidates[0])),(unsigned long)scan_evaluations,(unsigned long)scan_bins,construction_vmhwm_bytes());return 0;}

```

### scan_candidates.h

```c
#include <stdint.h>
typedef struct{int table,dt;uint32_t j;int memory,hit,dp_fixed,probe_word,restart,restart_halt,deadline,setup,replay_rate,replay_g,replay_nck,replay_const;} Candidate;
#define HINT_T 535758194UL
#define SPAN (1UL<<20)
#define STEP_OPS 118445
#define PREPROCESSING 180956727443456
static const Candidate candidates[]={
 {16360,630,69905,1024025,133,2893,24,2835,3,1,747082,10915,16367,17,5542},
 {16368,630,69905,1024281,133,2893,24,2835,3,1,747093,10915,16367,17,5542},
 {16376,630,69905,1024537,133,2893,24,2835,3,1,747104,10915,16367,17,5542},
 {16384,630,69905,1024793,133,2893,24,2835,3,1,747115,10915,16367,17,5542},
 {16392,630,69905,1025049,133,2893,24,2835,3,1,747126,10915,16367,17,5542},
 {16400,630,69905,1025305,133,2893,24,2835,3,1,747137,10915,16367,17,5542},
 {16408,630,69905,1025561,133,2893,24,2835,3,1,747148,10915,16367,17,5542},
 {16416,630,69905,1025817,133,2893,24,2835,3,1,747159,10915,16367,17,5542},
 {16424,630,69905,1026073,133,2893,24,2835,3,1,747170,10915,16367,17,5542},
 {16432,630,69905,1026329,133,2893,24,2835,3,1,747181,10915,16367,17,5542},
 {16440,630,69905,1026585,133,2893,24,2835,3,1,747192,10915,16367,17,5542},
 {16448,630,69905,1026841,133,2893,24,2835,3,1,747203,10915,16367,17,5542},
 {16456,630,69905,1027097,133,2893,24,2835,3,1,747214,10915,16367,17,5542},
 {16464,630,69905,1027353,133,2893,24,2835,3,1,747225,10915,16367,17,5542},
 {16472,630,69905,1027609,133,2893,24,2835,3,1,747236,10915,16367,17,5542},
 {16480,630,69905,1027865,133,2893,24,2835,3,1,747247,10915,16367,17,5542},
 {16488,630,69905,1028121,133,2893,24,2835,3,1,747258,10915,16367,17,5542},
 {16496,630,69905,1028377,133,2893,24,2835,3,1,747269,10915,16367,17,5542},
 {16504,630,69905,1028633,133,2893,24,2835,3,1,747280,10915,16367,17,5542},
 {16512,630,69905,1028889,133,2893,24,2835,3,1,747291,10915,16367,17,5542},
 {16520,630,69905,1029145,133,2893,24,2835,3,1,747302,10915,16367,17,5542},
 {16528,630,69905,1029401,133,2893,24,2835,3,1,747313,10915,16367,17,5542},
 {16536,630,69905,1029657,133,2893,24,2835,3,1,747324,10915,16367,17,5542},
 {16544,630,69905,1029913,133,2893,24,2835,3,1,747335,10915,16367,17,5542},
 {16552,630,69905,1030169,133,2893,24,2835,3,1,747346,10915,16367,17,5542},
 {16560,630,69905,1030425,133,2893,24,2835,3,1,747357,10915,16367,17,5542},
 {16568,630,69905,1030681,133,2893,24,2835,3,1,747368,10915,16367,17,5542},
 {16576,630,69905,1030937,133,2893,24,2835,3,1,747379,10915,16367,17,5542},
 {16584,630,69905,1031193,133,2893,24,2835,3,1,747390,10915,16367,17,5542},
 {16592,630,69905,1031449,133,2893,24,2835,3,1,747401,10915,16367,17,5542},
 {16600,630,69905,1031705,133,2893,24,2835,3,1,747412,10915,16367,17,5542},
 {16608,630,69905,1031961,133,2893,24,2835,3,1,747423,10915,16367,17,5542},
 {16616,630,69905,1032217,133,2893,24,2835,3,1,747434,10915,16367,17,5542},
};

```

### construction_hash.c

```c
/* Freestanding streaming SHA-256 for charged construction outputs. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

extern long construction_vmhwm_bytes(void);
typedef struct{uint32_t h[8];uint64_t bits;uint8_t block[64];unsigned used;} SHA256;
static const uint32_t K[64]={
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static uint32_t rr(uint32_t x,unsigned n){return(x>>n)|(x<<(32-n));}
static void compress(SHA256 *s,const uint8_t b[64]){
    uint32_t w[64];for(int i=0;i<16;i++)w[i]=(uint32_t)b[4*i]<<24|(uint32_t)b[4*i+1]<<16|(uint32_t)b[4*i+2]<<8|b[4*i+3];
    for(int i=16;i<64;i++){uint32_t a=w[i-15],z=w[i-2];w[i]=(rr(z,17)^rr(z,19)^(z>>10))+w[i-7]+(rr(a,7)^rr(a,18)^(a>>3))+w[i-16];}
    uint32_t a=s->h[0],c=s->h[2],b0=s->h[1],d=s->h[3],e=s->h[4],f=s->h[5],g=s->h[6],h=s->h[7];
    for(int i=0;i<64;i++){uint32_t t1=h+(rr(e,6)^rr(e,11)^rr(e,25))+((e&f)^((~e)&g))+K[i]+w[i];uint32_t t2=(rr(a,2)^rr(a,13)^rr(a,22))+((a&b0)^(a&c)^(b0&c));h=g;g=f;f=e;e=d+t1;d=c;c=b0;b0=a;a=t1+t2;}
    s->h[0]+=a;s->h[1]+=b0;s->h[2]+=c;s->h[3]+=d;s->h[4]+=e;s->h[5]+=f;s->h[6]+=g;s->h[7]+=h;
}
static void init(SHA256 *s){static const uint32_t h[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};for(int i=0;i<8;i++)s->h[i]=h[i];s->bits=0;s->used=0;}
static void update(SHA256 *s,const uint8_t *p,size_t n){s->bits+=(uint64_t)n*8;while(n){unsigned take=64-s->used;if(take>n)take=(unsigned)n;for(unsigned i=0;i<take;i++)s->block[s->used+i]=p[i];s->used+=take;p+=take;n-=take;if(s->used==64){compress(s,s->block);s->used=0;}}}
static void finish(SHA256 *s,uint8_t out[32]){uint64_t bits=s->bits;s->block[s->used++]=0x80;if(s->used>56){while(s->used<64)s->block[s->used++]=0;compress(s,s->block);s->used=0;}while(s->used<56)s->block[s->used++]=0;for(int i=7;i>=0;i--)s->block[s->used++]=(uint8_t)(bits>>(8*i));compress(s,s->block);for(int i=0;i<8;i++)for(int j=0;j<4;j++)out[4*i+j]=(uint8_t)(s->h[i]>>(24-8*j));}
int main(int argc,char **argv){if(argc!=2){fprintf(stderr,"usage: construction_hash FILE\n");return 2;}FILE *f=fopen(argv[1],"rb");if(!f){fprintf(stderr,"open failed\n");return 2;}SHA256 s;init(&s);uint8_t buf[4096],digest[32];size_t n,total=0;while((n=fread(buf,1,sizeof(buf),f))){update(&s,buf,n);total+=n;}fclose(f);finish(&s,digest);for(int i=0;i<32;i++)printf("%02x",digest[i]);printf("  %s\n",argv[1]);fprintf(stderr,"hash bytes=%lu VmHWM %ld bytes\n",(unsigned long)total,construction_vmhwm_bytes());return 0;}

```

### construction_verify.c

```c
/* Freestanding construction-time parser/verifier for the stored step image. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
extern long construction_vmhwm_bytes(void);
typedef struct{FILE *file;uint8_t buffer[4096];size_t length,index;uint64_t bits;int available;long bytes;} Reader;
static int next_byte(Reader *r){if(r->index==r->length){r->length=fread(r->buffer,1,sizeof(r->buffer),r->file);r->index=0;if(!r->length)return -1;}r->bytes++;return r->buffer[r->index++];}
static uint64_t take(Reader *r,int width){while(r->available<width){int value=next_byte(r);if(value<0){fprintf(stderr,"short native step\n");exit(2);}r->bits|=(uint64_t)(unsigned)value<<r->available;r->available+=8;}uint64_t result=r->bits&(((uint64_t)1<<width)-1);r->bits>>=width;r->available-=width;return result;}
int main(int argc,char **argv){
    if(argc!=3){fprintf(stderr,"usage: construction_verify PROGRAM INSTRUCTIONS\n");return 2;}long instructions=atoi(argv[2]);FILE *file=fopen(argv[1],"rb");if(!file)return 2;
    Reader r={0};r.file=file;long forms14=0,forms25=0,forms36=0,shorts=0,mix[4]={0,0,0,0};int high=0;
    for(long i=0;i<instructions;i++){
        int op=(int)take(&r,2),same=(int)take(&r,1),d,a,b=0;if(same){a=(int)take(&r,11);d=a;shorts++;}else{d=(int)take(&r,11);a=(int)take(&r,11);}if(op!=3)b=(int)take(&r,11);
        if(op<0||op>3||d>=2048||a>=2048||b>=2048){fprintf(stderr,"native field overflow at %ld\n",i);return 2;}int width=3+(same?11:22)+(op==3?0:11);if(width==14)forms14++;else if(width==25)forms25++;else if(width==36)forms36++;else return 2;mix[op]++;
        if(d+1>high)high=d+1;if(a+1>high)high=a+1;if(b+1>high)high=b+1;
    }
    if(r.available&&r.bits){fprintf(stderr,"nonzero native padding\n");return 2;}if(next_byte(&r)>=0){fprintf(stderr,"trailing native bytes\n");return 2;}fclose(file);
    printf("instructions=%ld bytes=%ld peak=%d forms14=%ld forms25=%ld forms36=%ld short=%ld mix=%ld,%ld,%ld,%ld\n",instructions,r.bytes,high,forms14,forms25,forms36,shorts,mix[0],mix[1],mix[2],mix[3]);
    fprintf(stderr,"verify VmHWM %ld bytes\n",construction_vmhwm_bytes());return 0;
}

```

### controller_emitter.c

```c
/* Generated native8 assembly source and bounded emitter. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
extern long construction_vmhwm_bytes(void);
typedef struct{uint8_t op;uint16_t d,a,b;uint64_t imm[4];} Record;
static const Record records[]={
 {27,1931,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,1930,0,0,{0x0000000000000100UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,1934,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,1929,0,0,{0x0000000000000000UL,0x00ff76d508000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,1937,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,1932,1937,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,269,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000002UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000003UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000004UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000005UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000006UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,1937,{0x0000000000000007UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,269,269,0,{0x0000000000000008UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {17,264,269,0,{0x0000000000004168UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000007UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,256,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {4,267,1931,256,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,265,256,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,256,265,{0x0000000000004168UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1935,0,0,{0x0000000000000224UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {17,264,256,0,{0x0000000000000100UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000013UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1935,0,0,{0x0000000000000242UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0xffffffffffffffffUL,0xffffffffffffffffUL,0xffffffffffffffffUL,0x0000000000000000UL}},
 {8,264,1933,1932,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000213UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,1934,1934,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {17,264,1934,0,{0x8000000000000002UL,0x000987fee4ff6d50UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000022UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {29,0,0,0,{0x000000000000000aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,145,146,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,147,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,148,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,149,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,150,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,151,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,152,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,153,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,154,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,155,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,156,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,157,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,158,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,159,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,160,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,161,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,162,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,163,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,164,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,165,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,166,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,167,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,168,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,169,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,170,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,171,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,172,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,173,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,174,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,175,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,176,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,177,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,178,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,179,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,180,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,181,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,182,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,183,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,184,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,185,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,186,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,187,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,188,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,189,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,190,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,191,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,192,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,193,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,194,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,195,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,196,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,197,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,198,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,199,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,200,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,201,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,202,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,203,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,204,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,205,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,206,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,207,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,208,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,209,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,210,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,211,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,212,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,213,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,214,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,215,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,216,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,217,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,218,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,219,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,220,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,221,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,222,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,223,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,224,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,225,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,226,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,227,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,228,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,229,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,230,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,231,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,232,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,233,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,234,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,235,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,236,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,237,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,238,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,260,260,239,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,257,1933,260,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,257,257,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,144,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,266,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,144,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,143,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,142,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,141,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,265,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,266,266,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,141,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,140,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,265,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,266,266,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,140,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,139,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,265,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,266,266,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,139,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,138,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,137,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,265,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,266,266,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,137,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,265,136,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,265,257,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,266,266,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,257,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,258,0,0,{0x0000000000000000UL,0x00ff76d508000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,258,258,1929,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,258,258,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,257,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000213UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,0,{0x0000000000004068UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,1,{0x0000000000004069UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,2,{0x000000000000406aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,3,{0x000000000000406bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,4,{0x000000000000406cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,5,{0x000000000000406dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,6,{0x000000000000406eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,7,{0x000000000000406fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,8,{0x0000000000004070UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,9,{0x0000000000004071UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,10,{0x0000000000004072UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,11,{0x0000000000004073UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,12,{0x0000000000004074UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,13,{0x0000000000004075UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,14,{0x0000000000004076UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,15,{0x0000000000004077UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,16,{0x0000000000004078UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,17,{0x0000000000004079UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,18,{0x000000000000407aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,19,{0x000000000000407bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,20,{0x000000000000407cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,21,{0x000000000000407dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,22,{0x000000000000407eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,23,{0x000000000000407fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,24,{0x0000000000004080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,25,{0x0000000000004081UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,26,{0x0000000000004082UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,27,{0x0000000000004083UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,28,{0x0000000000004084UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,29,{0x0000000000004085UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,30,{0x0000000000004086UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,31,{0x0000000000004087UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,32,{0x0000000000004088UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,33,{0x0000000000004089UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,34,{0x000000000000408aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,35,{0x000000000000408bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,36,{0x000000000000408cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,37,{0x000000000000408dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,38,{0x000000000000408eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,39,{0x000000000000408fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,40,{0x0000000000004090UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,41,{0x0000000000004091UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,42,{0x0000000000004092UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,43,{0x0000000000004093UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,44,{0x0000000000004094UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,45,{0x0000000000004095UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,46,{0x0000000000004096UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,47,{0x0000000000004097UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,48,{0x0000000000004098UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,49,{0x0000000000004099UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,50,{0x000000000000409aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,51,{0x000000000000409bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,52,{0x000000000000409cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,53,{0x000000000000409dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,54,{0x000000000000409eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,55,{0x000000000000409fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,56,{0x00000000000040a0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,57,{0x00000000000040a1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,58,{0x00000000000040a2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,59,{0x00000000000040a3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,60,{0x00000000000040a4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,61,{0x00000000000040a5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,62,{0x00000000000040a6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,63,{0x00000000000040a7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,64,{0x00000000000040a8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,65,{0x00000000000040a9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,66,{0x00000000000040aaUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,67,{0x00000000000040abUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,68,{0x00000000000040acUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,69,{0x00000000000040adUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,70,{0x00000000000040aeUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,71,{0x00000000000040afUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,72,{0x00000000000040b0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,73,{0x00000000000040b1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,74,{0x00000000000040b2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,75,{0x00000000000040b3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,76,{0x00000000000040b4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,77,{0x00000000000040b5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,78,{0x00000000000040b6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,79,{0x00000000000040b7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,80,{0x00000000000040b8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,81,{0x00000000000040b9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,82,{0x00000000000040baUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,83,{0x00000000000040bbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,84,{0x00000000000040bcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,85,{0x00000000000040bdUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,86,{0x00000000000040beUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,87,{0x00000000000040bfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,88,{0x00000000000040c0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,89,{0x00000000000040c1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,90,{0x00000000000040c2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,91,{0x00000000000040c3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,92,{0x00000000000040c4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,93,{0x00000000000040c5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,94,{0x00000000000040c6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,95,{0x00000000000040c7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,96,{0x00000000000040c8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,97,{0x00000000000040c9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,98,{0x00000000000040caUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,99,{0x00000000000040cbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,100,{0x00000000000040ccUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,101,{0x00000000000040cdUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,102,{0x00000000000040ceUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,103,{0x00000000000040cfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,104,{0x00000000000040d0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,105,{0x00000000000040d1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,106,{0x00000000000040d2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,107,{0x00000000000040d3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,108,{0x00000000000040d4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,109,{0x00000000000040d5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,110,{0x00000000000040d6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,111,{0x00000000000040d7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,112,{0x00000000000040d8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,113,{0x00000000000040d9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,114,{0x00000000000040daUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,115,{0x00000000000040dbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,116,{0x00000000000040dcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,117,{0x00000000000040ddUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,118,{0x00000000000040deUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,119,{0x00000000000040dfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,120,{0x00000000000040e0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,121,{0x00000000000040e1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,122,{0x00000000000040e2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,123,{0x00000000000040e3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,124,{0x00000000000040e4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,125,{0x00000000000040e5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,126,{0x00000000000040e6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,127,{0x00000000000040e7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,128,{0x00000000000040e8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,129,{0x00000000000040e9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,130,{0x00000000000040eaUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,131,{0x00000000000040ebUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,132,{0x00000000000040ecUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,133,{0x00000000000040edUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,134,{0x00000000000040eeUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,135,{0x00000000000040efUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,136,{0x00000000000040f0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,137,{0x00000000000040f1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,138,{0x00000000000040f2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,139,{0x00000000000040f3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,140,{0x00000000000040f4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,141,{0x00000000000040f5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,142,{0x00000000000040f6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,143,{0x00000000000040f7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,144,{0x00000000000040f8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,145,{0x00000000000040f9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,146,{0x00000000000040faUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,147,{0x00000000000040fbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,148,{0x00000000000040fcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,149,{0x00000000000040fdUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,150,{0x00000000000040feUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,151,{0x00000000000040ffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,152,{0x0000000000004100UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,153,{0x0000000000004101UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,154,{0x0000000000004102UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,155,{0x0000000000004103UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,156,{0x0000000000004104UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,157,{0x0000000000004105UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,158,{0x0000000000004106UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,159,{0x0000000000004107UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,160,{0x0000000000004108UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,161,{0x0000000000004109UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,162,{0x000000000000410aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,163,{0x000000000000410bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,164,{0x000000000000410cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,165,{0x000000000000410dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,166,{0x000000000000410eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,167,{0x000000000000410fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,168,{0x0000000000004110UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,169,{0x0000000000004111UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,170,{0x0000000000004112UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,171,{0x0000000000004113UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,172,{0x0000000000004114UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,173,{0x0000000000004115UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,174,{0x0000000000004116UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,175,{0x0000000000004117UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,176,{0x0000000000004118UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,177,{0x0000000000004119UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,178,{0x000000000000411aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,179,{0x000000000000411bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,180,{0x000000000000411cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,181,{0x000000000000411dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,182,{0x000000000000411eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,183,{0x000000000000411fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,184,{0x0000000000004120UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,185,{0x0000000000004121UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,186,{0x0000000000004122UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,187,{0x0000000000004123UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,188,{0x0000000000004124UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,189,{0x0000000000004125UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,190,{0x0000000000004126UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,191,{0x0000000000004127UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,192,{0x0000000000004128UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,193,{0x0000000000004129UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,194,{0x000000000000412aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,195,{0x000000000000412bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,196,{0x000000000000412cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,197,{0x000000000000412dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,198,{0x000000000000412eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,199,{0x000000000000412fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,200,{0x0000000000004130UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,201,{0x0000000000004131UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,202,{0x0000000000004132UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,203,{0x0000000000004133UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,204,{0x0000000000004134UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,205,{0x0000000000004135UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,206,{0x0000000000004136UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,207,{0x0000000000004137UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,208,{0x0000000000004138UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,209,{0x0000000000004139UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,210,{0x000000000000413aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,211,{0x000000000000413bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,212,{0x000000000000413cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,213,{0x000000000000413dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,214,{0x000000000000413eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,215,{0x000000000000413fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,216,{0x0000000000004140UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,217,{0x0000000000004141UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,218,{0x0000000000004142UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,219,{0x0000000000004143UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,220,{0x0000000000004144UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,221,{0x0000000000004145UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,222,{0x0000000000004146UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,223,{0x0000000000004147UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,224,{0x0000000000004148UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,225,{0x0000000000004149UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,226,{0x000000000000414aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,227,{0x000000000000414bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,228,{0x000000000000414cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,229,{0x000000000000414dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,230,{0x000000000000414eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,231,{0x000000000000414fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,232,{0x0000000000004150UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,233,{0x0000000000004151UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,234,{0x0000000000004152UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,235,{0x0000000000004153UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,236,{0x0000000000004154UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,237,{0x0000000000004155UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,238,{0x0000000000004156UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,239,{0x0000000000004157UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,240,{0x0000000000004158UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,241,{0x0000000000004159UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,242,{0x000000000000415aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,243,{0x000000000000415bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,244,{0x000000000000415cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,245,{0x000000000000415dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,246,{0x000000000000415eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,247,{0x000000000000415fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,248,{0x0000000000004160UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,249,{0x0000000000004161UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,250,{0x0000000000004162UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,251,{0x0000000000004163UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,252,{0x0000000000004164UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,253,{0x0000000000004165UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,254,{0x0000000000004166UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,255,{0x0000000000004167UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,257,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000212UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,256,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,265,257,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0xffffffffffffffffUL,0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001adUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001b2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0x00000000ffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001b7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000020UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000020UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0x000000000000ffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001bcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000010UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000010UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0x00000000000000ffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001c1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000008UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000008UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0x000000000000000fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001c6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000004UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000004UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0x0000000000000003UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001cbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000002UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000002UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,265,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,266,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001d0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,265,265,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,256,256,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {12,266,257,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,257,257,266,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1935,0,0,{0x0000000000000235UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,261,259,0,{0x0003ffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,261,261,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,261,261,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,272,261,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,265,261,0,{0x0000000000000033UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,272,272,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,265,261,0,{0x0000000000000066UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,272,272,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,265,261,0,{0x0000000000000099UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,272,272,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,265,261,0,{0x00000000000000ccUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,272,272,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,262,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,263,262,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,263,263,272,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,265,263,0,{0x0007ffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,265,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000203UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,266,263,0,{0x0000000000000033UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,265,266,0,{0x0007ffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,265,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000206UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,266,263,0,{0x0000000000000066UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,265,266,0,{0x0007ffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,265,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000209UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,266,263,0,{0x0000000000000099UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,265,266,0,{0x0007ffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,265,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x000000000000020cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,266,263,0,{0x00000000000000ccUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,265,266,0,{0x0007ffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,265,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x000000000000020fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,262,262,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,262,0,{0x0000000000004068UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000001e0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,271,256,0,{0x0000000000004168UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,271,271,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,262,271,0,{0x0000000000007fffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,266,271,0,{0x000000000000000fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {6,265,261,266,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,263,262,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,263,263,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,262,263,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,260,258,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000216UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x00000000000001a4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,265,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,265,265,262,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x000000000000037cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,265,0,0,{0x0000000000198000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,265,265,262,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x000000000000037cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,265,0,0,{0x0000000000330000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,265,265,262,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x000000000000037cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,265,0,0,{0x00000000004c8000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,265,265,262,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x000000000000037cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,265,0,0,{0x0000000000660000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,265,265,262,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x000000000000037cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1935,0,0,{0x0000000000000242UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {12,1929,1929,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,1929,0,{0xffffffffffffffffUL,0xffffffffffffffffUL,0xffffffffffffffffUL,0x0000000000000000UL}},
 {29,0,0,0,{0x000000000000000cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,1930,0,{0x00000000007f8000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x0000000000000219UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {29,0,0,0,{0x000000000000000bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,265,1930,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,265,265,260,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,256,265,{0x0000000000004168UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {4,267,1931,1930,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,1930,1930,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,265,1930,0,{0x0000000000007fffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,265,0,{0x0000000000004068UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x0000000000000222UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,1930,1930,0,{0x0000000000193f98UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1935,0,0,{0x0000000000000224UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {26,0,1936,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,273,0,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {6,273,273,256,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {3,268,273,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {21,269,0,0,{0x0000000000004068UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,270,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,265,269,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {1,265,265,268,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {7,266,267,270,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,266,266,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {6,266,266,256,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,265,265,266,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,269,269,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,270,270,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,270,0,{0x0000000000000100UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x0000000000000229UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {26,0,1935,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,259,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {21,269,0,0,{0x0000000000004068UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,270,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,265,269,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {7,265,265,256,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,265,265,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {6,265,265,270,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {2,259,259,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,269,269,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,270,270,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,270,0,{0x0000000000000100UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x0000000000000238UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {26,0,1935,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,0,1937,0,{0x0000000000004068UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,1,1937,0,{0x0000000000004069UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,2,1937,0,{0x000000000000406aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,3,1937,0,{0x000000000000406bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,4,1937,0,{0x000000000000406cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,5,1937,0,{0x000000000000406dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,6,1937,0,{0x000000000000406eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,7,1937,0,{0x000000000000406fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,8,1937,0,{0x0000000000004070UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,9,1937,0,{0x0000000000004071UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,10,1937,0,{0x0000000000004072UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,11,1937,0,{0x0000000000004073UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,12,1937,0,{0x0000000000004074UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,13,1937,0,{0x0000000000004075UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,14,1937,0,{0x0000000000004076UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,15,1937,0,{0x0000000000004077UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,16,1937,0,{0x0000000000004078UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,17,1937,0,{0x0000000000004079UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,18,1937,0,{0x000000000000407aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,19,1937,0,{0x000000000000407bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,20,1937,0,{0x000000000000407cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,21,1937,0,{0x000000000000407dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,22,1937,0,{0x000000000000407eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,23,1937,0,{0x000000000000407fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,24,1937,0,{0x0000000000004080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,25,1937,0,{0x0000000000004081UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,26,1937,0,{0x0000000000004082UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,27,1937,0,{0x0000000000004083UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,28,1937,0,{0x0000000000004084UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,29,1937,0,{0x0000000000004085UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,30,1937,0,{0x0000000000004086UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,31,1937,0,{0x0000000000004087UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,32,1937,0,{0x0000000000004088UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,33,1937,0,{0x0000000000004089UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,34,1937,0,{0x000000000000408aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,35,1937,0,{0x000000000000408bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,36,1937,0,{0x000000000000408cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,37,1937,0,{0x000000000000408dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,38,1937,0,{0x000000000000408eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,39,1937,0,{0x000000000000408fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,40,1937,0,{0x0000000000004090UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,41,1937,0,{0x0000000000004091UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,42,1937,0,{0x0000000000004092UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,43,1937,0,{0x0000000000004093UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,44,1937,0,{0x0000000000004094UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,45,1937,0,{0x0000000000004095UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,46,1937,0,{0x0000000000004096UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,47,1937,0,{0x0000000000004097UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,48,1937,0,{0x0000000000004098UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,49,1937,0,{0x0000000000004099UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,50,1937,0,{0x000000000000409aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,51,1937,0,{0x000000000000409bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,52,1937,0,{0x000000000000409cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,53,1937,0,{0x000000000000409dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,54,1937,0,{0x000000000000409eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,55,1937,0,{0x000000000000409fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,56,1937,0,{0x00000000000040a0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,57,1937,0,{0x00000000000040a1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,58,1937,0,{0x00000000000040a2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,59,1937,0,{0x00000000000040a3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,60,1937,0,{0x00000000000040a4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,61,1937,0,{0x00000000000040a5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,62,1937,0,{0x00000000000040a6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,63,1937,0,{0x00000000000040a7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,64,1937,0,{0x00000000000040a8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,65,1937,0,{0x00000000000040a9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,66,1937,0,{0x00000000000040aaUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,67,1937,0,{0x00000000000040abUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,68,1937,0,{0x00000000000040acUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,69,1937,0,{0x00000000000040adUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,70,1937,0,{0x00000000000040aeUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,71,1937,0,{0x00000000000040afUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,72,1937,0,{0x00000000000040b0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,73,1937,0,{0x00000000000040b1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,74,1937,0,{0x00000000000040b2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,75,1937,0,{0x00000000000040b3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,76,1937,0,{0x00000000000040b4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,77,1937,0,{0x00000000000040b5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,78,1937,0,{0x00000000000040b6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,79,1937,0,{0x00000000000040b7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,80,1937,0,{0x00000000000040b8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,81,1937,0,{0x00000000000040b9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,82,1937,0,{0x00000000000040baUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,83,1937,0,{0x00000000000040bbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,84,1937,0,{0x00000000000040bcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,85,1937,0,{0x00000000000040bdUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,86,1937,0,{0x00000000000040beUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,87,1937,0,{0x00000000000040bfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,88,1937,0,{0x00000000000040c0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,89,1937,0,{0x00000000000040c1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,90,1937,0,{0x00000000000040c2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,91,1937,0,{0x00000000000040c3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,92,1937,0,{0x00000000000040c4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,93,1937,0,{0x00000000000040c5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,94,1937,0,{0x00000000000040c6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,95,1937,0,{0x00000000000040c7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,96,1937,0,{0x00000000000040c8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,97,1937,0,{0x00000000000040c9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,98,1937,0,{0x00000000000040caUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,99,1937,0,{0x00000000000040cbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,100,1937,0,{0x00000000000040ccUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,101,1937,0,{0x00000000000040cdUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,102,1937,0,{0x00000000000040ceUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,103,1937,0,{0x00000000000040cfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,104,1937,0,{0x00000000000040d0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,105,1937,0,{0x00000000000040d1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,106,1937,0,{0x00000000000040d2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,107,1937,0,{0x00000000000040d3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,108,1937,0,{0x00000000000040d4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,109,1937,0,{0x00000000000040d5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,110,1937,0,{0x00000000000040d6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,111,1937,0,{0x00000000000040d7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,112,1937,0,{0x00000000000040d8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,113,1937,0,{0x00000000000040d9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,114,1937,0,{0x00000000000040daUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,115,1937,0,{0x00000000000040dbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,116,1937,0,{0x00000000000040dcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,117,1937,0,{0x00000000000040ddUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,118,1937,0,{0x00000000000040deUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,119,1937,0,{0x00000000000040dfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,120,1937,0,{0x00000000000040e0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,121,1937,0,{0x00000000000040e1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,122,1937,0,{0x00000000000040e2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,123,1937,0,{0x00000000000040e3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,124,1937,0,{0x00000000000040e4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,125,1937,0,{0x00000000000040e5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,126,1937,0,{0x00000000000040e6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,127,1937,0,{0x00000000000040e7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,128,1937,0,{0x00000000000040e8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,129,1937,0,{0x00000000000040e9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,130,1937,0,{0x00000000000040eaUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,131,1937,0,{0x00000000000040ebUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,132,1937,0,{0x00000000000040ecUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,133,1937,0,{0x00000000000040edUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,134,1937,0,{0x00000000000040eeUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,135,1937,0,{0x00000000000040efUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,136,1937,0,{0x00000000000040f0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,137,1937,0,{0x00000000000040f1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,138,1937,0,{0x00000000000040f2UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,139,1937,0,{0x00000000000040f3UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,140,1937,0,{0x00000000000040f4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,141,1937,0,{0x00000000000040f5UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,142,1937,0,{0x00000000000040f6UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,143,1937,0,{0x00000000000040f7UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,144,1937,0,{0x00000000000040f8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,145,1937,0,{0x00000000000040f9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,146,1937,0,{0x00000000000040faUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,147,1937,0,{0x00000000000040fbUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,148,1937,0,{0x00000000000040fcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,149,1937,0,{0x00000000000040fdUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,150,1937,0,{0x00000000000040feUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,151,1937,0,{0x00000000000040ffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,152,1937,0,{0x0000000000004100UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,153,1937,0,{0x0000000000004101UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,154,1937,0,{0x0000000000004102UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,155,1937,0,{0x0000000000004103UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,156,1937,0,{0x0000000000004104UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,157,1937,0,{0x0000000000004105UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,158,1937,0,{0x0000000000004106UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,159,1937,0,{0x0000000000004107UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,160,1937,0,{0x0000000000004108UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,161,1937,0,{0x0000000000004109UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,162,1937,0,{0x000000000000410aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,163,1937,0,{0x000000000000410bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,164,1937,0,{0x000000000000410cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,165,1937,0,{0x000000000000410dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,166,1937,0,{0x000000000000410eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,167,1937,0,{0x000000000000410fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,168,1937,0,{0x0000000000004110UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,169,1937,0,{0x0000000000004111UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,170,1937,0,{0x0000000000004112UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,171,1937,0,{0x0000000000004113UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,172,1937,0,{0x0000000000004114UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,173,1937,0,{0x0000000000004115UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,174,1937,0,{0x0000000000004116UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,175,1937,0,{0x0000000000004117UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,176,1937,0,{0x0000000000004118UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,177,1937,0,{0x0000000000004119UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,178,1937,0,{0x000000000000411aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,179,1937,0,{0x000000000000411bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,180,1937,0,{0x000000000000411cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,181,1937,0,{0x000000000000411dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,182,1937,0,{0x000000000000411eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,183,1937,0,{0x000000000000411fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,184,1937,0,{0x0000000000004120UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,185,1937,0,{0x0000000000004121UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,186,1937,0,{0x0000000000004122UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,187,1937,0,{0x0000000000004123UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,188,1937,0,{0x0000000000004124UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,189,1937,0,{0x0000000000004125UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,190,1937,0,{0x0000000000004126UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,191,1937,0,{0x0000000000004127UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,192,1937,0,{0x0000000000004128UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,193,1937,0,{0x0000000000004129UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,194,1937,0,{0x000000000000412aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,195,1937,0,{0x000000000000412bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,196,1937,0,{0x000000000000412cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,197,1937,0,{0x000000000000412dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,198,1937,0,{0x000000000000412eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,199,1937,0,{0x000000000000412fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,200,1937,0,{0x0000000000004130UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,201,1937,0,{0x0000000000004131UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,202,1937,0,{0x0000000000004132UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,203,1937,0,{0x0000000000004133UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,204,1937,0,{0x0000000000004134UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,205,1937,0,{0x0000000000004135UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,206,1937,0,{0x0000000000004136UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,207,1937,0,{0x0000000000004137UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,208,1937,0,{0x0000000000004138UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,209,1937,0,{0x0000000000004139UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,210,1937,0,{0x000000000000413aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,211,1937,0,{0x000000000000413bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,212,1937,0,{0x000000000000413cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,213,1937,0,{0x000000000000413dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,214,1937,0,{0x000000000000413eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,215,1937,0,{0x000000000000413fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,216,1937,0,{0x0000000000004140UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,217,1937,0,{0x0000000000004141UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,218,1937,0,{0x0000000000004142UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,219,1937,0,{0x0000000000004143UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,220,1937,0,{0x0000000000004144UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,221,1937,0,{0x0000000000004145UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,222,1937,0,{0x0000000000004146UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,223,1937,0,{0x0000000000004147UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,224,1937,0,{0x0000000000004148UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,225,1937,0,{0x0000000000004149UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,226,1937,0,{0x000000000000414aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,227,1937,0,{0x000000000000414bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,228,1937,0,{0x000000000000414cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,229,1937,0,{0x000000000000414dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,230,1937,0,{0x000000000000414eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,231,1937,0,{0x000000000000414fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,232,1937,0,{0x0000000000004150UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,233,1937,0,{0x0000000000004151UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,234,1937,0,{0x0000000000004152UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,235,1937,0,{0x0000000000004153UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,236,1937,0,{0x0000000000004154UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,237,1937,0,{0x0000000000004155UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,238,1937,0,{0x0000000000004156UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,239,1937,0,{0x0000000000004157UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,240,1937,0,{0x0000000000004158UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,241,1937,0,{0x0000000000004159UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,242,1937,0,{0x000000000000415aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,243,1937,0,{0x000000000000415bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,244,1937,0,{0x000000000000415cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,245,1937,0,{0x000000000000415dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,246,1937,0,{0x000000000000415eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,247,1937,0,{0x000000000000415fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,248,1937,0,{0x0000000000004160UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,249,1937,0,{0x0000000000004161UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,250,1937,0,{0x0000000000004162UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,251,1937,0,{0x0000000000004163UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,252,1937,0,{0x0000000000004164UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,253,1937,0,{0x0000000000004165UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,254,1937,0,{0x0000000000004166UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,255,1937,0,{0x0000000000004167UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {26,0,1935,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,300,1937,0,{0x0000000000004268UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,301,1937,0,{0x0000000000004269UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,302,1937,0,{0x000000000000426aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,303,1937,0,{0x000000000000426bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,304,1937,0,{0x000000000000426cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,305,1937,0,{0x000000000000426dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,306,1937,0,{0x000000000000426eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,290,286,0,{0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,291,286,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,291,291,0,{0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,292,286,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,292,292,0,{0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,293,286,0,{0x00000000000000c0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,290,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,300,300,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,291,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,301,301,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,301,301,292,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,293,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,302,302,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,294,290,291,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,294,0,{0x00000000000000c0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,302,302,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,294,292,293,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,294,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,303,303,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {28,0,300,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,289,1937,0,{0x000000000000426fUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,287,300,289,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {26,0,1936,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,300,1937,0,{0x0000000000004268UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,301,1937,0,{0x0000000000004269UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,302,1937,0,{0x000000000000426aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,303,1937,0,{0x000000000000426bUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,304,1937,0,{0x000000000000426cUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,305,1937,0,{0x000000000000426dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,306,1937,0,{0x000000000000426eUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,290,286,0,{0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,291,286,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,291,291,0,{0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,292,286,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,292,292,0,{0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,293,286,0,{0x00000000000000c0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,290,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,300,300,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,291,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,301,301,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,301,301,292,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,293,0,{0x0000000000000040UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,302,302,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,294,290,291,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,294,0,{0x00000000000000c0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,302,302,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,294,292,293,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {13,294,294,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {0,303,303,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {26,0,1936,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,285,256,0,{0x0000000000004168UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {14,266,285,0,{0x0000000000000080UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {15,285,285,0,{0xffffffffffffffffUL,0xffffffffffffffffUL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,285,258,285,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {17,264,285,0,{0x0000000000000001UL,0x0008888800000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000003e9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {4,280,1931,265,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {4,281,1931,266,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,280,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,284,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,269,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,274,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {8,264,284,274,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x000000000000038dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,269,286,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,269,269,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,274,274,0,{0x5d221d192b7e0137UL,0x00000021eb88ef9eUL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000343UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,284,284,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {17,264,287,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000013b00UL,0x0000000000000000UL}},
 {22,0,264,0,{0x0000000000000395UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {17,264,284,0,{0x0000000000000000UL,0x0008888800000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000003e9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,287,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x0000000000000388UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {9,264,284,285,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003adUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,282,284,285,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,275,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,277,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,294,275,0,{0x5d221d192b7e0137UL,0x00000021eb88ef9eUL,0x0000000000000000UL,0x0000000000000000UL}},
 {9,264,282,294,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003a0UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,275,294,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,277,277,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x000000000000039aUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,280,277,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,277,277,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,276,275,0,{0x5d221d192b7e0137UL,0x00000021eb88ef9eUL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,282,282,275,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,282,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003abUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,280,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000343UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,280,287,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {12,282,282,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x00000000000003a4UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,275,284,285,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x00000000000003b8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,282,285,284,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,275,0,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,276,0,0,{0x5d221d192b7e0137UL,0x00000021eb88ef9eUL,0x0000000000000000UL,0x0000000000000000UL}},
 {18,277,0,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,282,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003b8UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,281,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000343UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,281,287,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {12,282,282,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x00000000000003b1UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {8,264,280,281,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003e9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {9,264,276,284,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000003ceUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,279,276,275,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,282,279,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,278,281,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,278,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000343UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,278,287,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {12,282,282,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,282,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {23,0,264,0,{0x00000000000003bfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {19,294,277,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {8,264,294,278,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003cfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,280,294,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,281,278,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,275,276,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,276,276,0,{0x5d221d192b7e0137UL,0x00000021eb88ef9eUL,0x0000000000000000UL,0x0000000000000000UL}},
 {11,277,277,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x00000000000003baUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {5,279,284,275,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {16,264,279,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003e9UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,280,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000343UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,288,287,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,281,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000343UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {8,264,288,287,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {22,0,264,0,{0x00000000000003dcUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,280,288,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,281,287,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {12,279,279,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {24,0,0,0,{0x00000000000003cfUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,280,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000361UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,300,{0x0000000000004270UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,301,{0x0000000000004271UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,302,{0x0000000000004272UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,303,{0x0000000000004273UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {10,286,281,0,{0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {25,1936,0,0,{0x0000000000000361UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,300,{0x0000000000004274UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,301,{0x0000000000004275UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,302,{0x0000000000004276UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {20,0,1937,303,{0x0000000000004277UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {29,0,0,0,{0x0000000000000001UL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}},
 {29,0,0,0,{0x000000000000000dUL,0x0000000000000000UL,0x0000000000000000UL,0x0000000000000000UL}}
};
static uint64_t literals[64][4];static int literal_count;
static int same256(const uint64_t a[4],const uint64_t b[4]){return a[0]==b[0]&&a[1]==b[1]&&a[2]==b[2]&&a[3]==b[3];}
static int literal(const uint64_t value[4]){for(int i=0;i<literal_count;i++)if(same256(literals[i],value))return i;if(literal_count==64){fprintf(stderr,"literal capacity\n");exit(2);}for(int j=0;j<4;j++)literals[literal_count][j]=value[j];return literal_count++;}
int main(int argc,char **argv){if(argc!=2)return 2;FILE *out=fopen(argv[1],"wb");if(!out)return 2;const int count=(int)(sizeof(records)/sizeof(records[0]));
 for(int i=0;i<count;i++){const Record *r=&records[i];if(r->op>29||r->d>=2048||r->a>=2048||r->b>=2048)return 2;int flag=0;uint64_t field=r->imm[0];if(r->imm[1]||r->imm[2]||r->imm[3]||field>=(1UL<<25)){flag=1;field=(uint64_t)literal(r->imm);}if(field>=(1UL<<25))return 2;}
 for(int i=0;i<count;i++){const Record *r=&records[i];int flag=0;uint64_t field=r->imm[0];if(r->imm[1]||r->imm[2]||r->imm[3]||field>=(1UL<<25)){flag=1;field=(uint64_t)literal(r->imm);}uint64_t word=(uint64_t)r->op|((uint64_t)flag<<5)|((uint64_t)r->d<<6)|((uint64_t)r->a<<17)|((uint64_t)r->b<<28)|(field<<39);uint8_t bytes[8];for(int j=0;j<8;j++)bytes[j]=(uint8_t)(word>>(8*j));if(fwrite(bytes,1,8,out)!=8)return 2;}
 for(int i=0;i<literal_count;i++){uint8_t bytes[32];for(int j=0;j<32;j++)bytes[j]=(uint8_t)(literals[i][j>>3]>>(8*(j&7)));if(fwrite(bytes,1,32,out)!=32)return 2;}if(fclose(out))return 2;
 fprintf(stderr,"controller instructions=%d literals=%d bytes=%d VmHWM %ld bytes\n",count,literal_count,8*count+32*literal_count,construction_vmhwm_bytes());return 0;}

```

## Appendix C. Measured construction record

```json
{
  "address_space_limit": 1048576,
  "chained_table": {
    "bytes": 4096,
    "candidate_evaluations": 1015808,
    "checksum": "c8fa4bd9170966dc",
    "entries": 1024,
    "truth_checks": 32768
  },
  "operation_counts": {
    "annealing_rounds_per_process": 17,
    "cheap_builds": 512,
    "controller_bytes": 8400,
    "controller_instructions": 1002,
    "controller_literals": 12,
    "full_processes": 8,
    "iterations_per_round": 200000000,
    "prefilter_bytes": 49,
    "prefilter_instructions": 15,
    "scan_bins": 46906255,
    "scan_evaluations": 671,
    "step_bytes": 413080,
    "step_instructions": 118445,
    "table_processes": 10
  },
  "peak_bytes": 934965,
  "phases": [
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 610103,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "512-trial cheap scan",
      "output_bytes": 18432,
      "retained_input_output_bytes": 18432,
      "seconds": 3.7055015079677105,
      "sequential": true,
      "stack_reserve": 262144,
      "trial": null,
      "vmhwm_bytes": 417792
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121166,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 1",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 336.8171928040683,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118456,
      "trial": 1331,
      "vmhwm_bytes": 417792
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121187,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 2",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 336.3919523428194,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118445,
      "trial": 1333,
      "vmhwm_bytes": 413696
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121187,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 3",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 335.1065367020201,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118466,
      "trial": 1466,
      "vmhwm_bytes": 413696
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121191,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 4",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 331.7827916620299,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118482,
      "trial": 1059,
      "vmhwm_bytes": 417792
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121192,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 5",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 334.0516005018726,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118503,
      "trial": 1215,
      "vmhwm_bytes": 417792
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121193,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 6",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 334.34883660217747,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118483,
      "trial": 1375,
      "vmhwm_bytes": 417792
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121200,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 7",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 333.4790043910034,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118466,
      "trial": 1377,
      "vmhwm_bytes": 413696
    },
    {
      "binary": "construction_generator",
      "charged_peak_bytes": 643296,
      "cheap_count": 121203,
      "image": {
        "bss": 288448,
        "data": 216,
        "image": 329527,
        "text": 40863
      },
      "name": "TOPK full build 8",
      "output_bytes": 51625,
      "retained_best_bytes": 51625,
      "retained_input_output_bytes": 51625,
      "seconds": 331.87462322297506,
      "sequential": true,
      "stack_reserve": 262144,
      "step_ops": 118480,
      "trial": 1184,
      "vmhwm_bytes": 413696
    },
    {
      "binary": "construction_hash",
      "charged_peak_bytes": 55767,
      "image": {
        "bss": 4096,
        "data": 16,
        "image": 9766,
        "text": 5654
      },
      "name": "structured-basis file verification",
      "retained_input_output_bytes": 22999,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 32768
    },
    {
      "binary": "construction_scan",
      "charged_peak_bytes": 28745,
      "image": {
        "bss": 4160,
        "data": 24,
        "image": 12286,
        "text": 8102
      },
      "name": "native finite parameter scan",
      "retained_input_output_bytes": 73,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 28672
    },
    {
      "binary": "construction_emitter",
      "charged_peak_bytes": 934965,
      "image": {
        "bss": 393504,
        "data": 208,
        "image": 423581,
        "text": 29869
      },
      "name": "streaming native step emission",
      "retained_input_output_bytes": 413080,
      "sequential": true,
      "stack_reserve": 98304,
      "vmhwm_bytes": 438272
    },
    {
      "binary": "construction_hash",
      "charged_peak_bytes": 439230,
      "image": {
        "bss": 4096,
        "data": 16,
        "image": 9766,
        "text": 5654
      },
      "name": "streaming step SHA-256",
      "retained_input_output_bytes": 413080,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 24576
    },
    {
      "binary": "construction_verify",
      "charged_peak_bytes": 438762,
      "image": {
        "bss": 4096,
        "data": 16,
        "image": 9298,
        "text": 5186
      },
      "name": "construction-time step parsing, field, and ledger verification",
      "retained_input_output_bytes": 413080,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 24576
    },
    {
      "binary": "construction_prefilter",
      "charged_peak_bytes": 24687,
      "image": {
        "bss": 4128,
        "data": 24,
        "image": 8254,
        "text": 4102
      },
      "name": "native 15-OR prefilter emission",
      "retained_input_output_bytes": 49,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 24576
    },
    {
      "binary": "construction_hash",
      "charged_peak_bytes": 28721,
      "image": {
        "bss": 4096,
        "data": 16,
        "image": 9766,
        "text": 5654
      },
      "name": "streaming prefilter SHA-256",
      "retained_input_output_bytes": 49,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 28672
    },
    {
      "binary": "controller_emitter",
      "charged_peak_bytes": 75429,
      "image": {
        "bss": 6208,
        "data": 24,
        "image": 50645,
        "text": 44413
      },
      "name": "native8 controller emission",
      "retained_input_output_bytes": 8400,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 57344
    },
    {
      "binary": "construction_hash",
      "charged_peak_bytes": 37072,
      "image": {
        "bss": 4096,
        "data": 16,
        "image": 9766,
        "text": 5654
      },
      "name": "streaming controller SHA-256",
      "retained_input_output_bytes": 8400,
      "sequential": true,
      "stack_reserve": 16384,
      "vmhwm_bytes": 28672
    }
  ],
  "round": 20,
  "schema": "hashsmash-construction-memory-v1",
  "sequential": true
}
```

## 9. Provenance of this round count and what was re-derived

This package is a re-targeting of **a3e65dc9-491c-423c-85fc-c2d24ccf4e5e** (0xplemonade), a
submission to the *separate* `mooselumph/hashsmash-pareto/sha3-256` benchmark at round 20
with normalized time 124.45149, to round 6 of this scalar track. The two benchmarks share
the `collision-frontier-v5` cost model and the identical `sha3-256-r<r>-prefix-v1` target
profiles (byte-for-byte apart from the round count and its round-selection sentence), so
the construction transfers; no score, qualification or decision from that benchmark is
carried over, and this package is reviewed afresh here. All credit for the construction campaign, the plan search, the
chained-chi table, the two-address and native8 encodings, the controller, and the 200-digit
success certificate belongs to that lineage; the author of this package contributed the
re-targeting, the re-derived circuit and the ledger below.

**What the round count changes.** The plan header's `nr` field, the emitted straight line
and its hashes, the derived PD, the register peak and the link/prefilter register indices,
the controller's `271 * rounds` permutation price and its round-dependent instruction
counts, the reference operation cost `C = 271 * 6 = 1626`, and every ledger term that
reads `C`.

**What it does not change.** The plan body (the per-round C/D complement masks and compact
chi decisions), the 25 folded lane constants, the chained-chi table and its checksum, the
six-lane embedding, and the search parameters `S = 16488`, `U = 82440`, `Tb`, `LRC`, `J` and the
trail count. Appendix A therefore transfers verbatim: no input of the success argument is a
function of the round count. H1 compares a bounded attempt on the fixed deterministic walk
`g` with the same attempt against a uniformly random comparator `F`, and the comparator
calculation reads only the distinguished-point threshold, the step budget, the replay cap
and the trail count. The r20 and r24 packages of this same family already share one plan
binding and one set of lane constants, so re-targeting the round count is this
construction's own method rather than a new assumption.

**Ledger terms evaluated at this round.** Main work is exact, from this package's own
emitted circuit: `Tb * BSTEP`. Replay is exact too, from the closed form of Section 4 at
this round's `e = C + 29 = 1655`, with `G = ceil(LRC/(S-1)) = 2687423885757092749185025704247` and `nck = S - 1 = 16487`;
it comes to 147424640958166104101746264353840690602, which is 0.3048 of the r20 figure, as the smaller `C`
requires. `preprocessing_log2` is recomputed as an upper bound on `log2(PRE/C)` =
36.71984; the parent's value bounds that ratio only at the parent's larger `C`.

**The one carried term.** The hit, DP, probe, restart, setup, cap and final-halt paths are
charged at the r20 package's figure, 6582035915778625933331161026038489389. That is an upper bound here: those paths are
priced from the emitted controller's own counts, every round-dependent count is strictly
smaller at this round (replay_rate 3,327 against 10,915, replay_g 4,985 against 16,367, replay_const 1,748 against 5,542 and eval_f 1,655 against 5,449), every other count entering them (`hit`, `ctz_clear`,
`record_slot`, `probe_word`, `insert`, `dp_fixed`, `restart`, `restart_halt`,
`deadline_final`, `setup`) is identical to the parent's, and any path charging a permutation
at `C` is cheaper. The term is 0.019% of N, so the conservatism costs under
0.0003 bit. Preprocessing is the same inherited construction campaign and is charged
in full at the parent's figure. Nothing in the ledger is reduced by an unexecuted path.

**Status.** `plausible_not_refuted` under the exploratory policy would not make this a proof
or a human-accepted result, and the claim asserts no weakness in full 24-round SHA3-256: at
round 6 of 24 the bound 124.03135 is above the organizer nominal reference and the whole
attack is an ordinary distinguished-point birthday search whose only gain over the nominal
scaffold is the bit-sliced pricing of the chain under collision-frontier-v5.
