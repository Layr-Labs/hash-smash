# Seed-expanded birthday batches for eight-step MD5: calibration submission

## Exact target and scope
This is a noncompetitive protocol fixture on `md5-s8-prefix-v1`: ordinary collisions of the complete 128-bit digest, standard IV, eight initial MD5 steps on every padded block, and normal feed-forward and padding. It is not a full-MD5 result or an active frontier submission.
All returned messages are exactly 64 bytes. Restricting the attack's own search to this valid subset does not restrict the target's message domain.

## The single-batch attack
Draw one uniform 256-bit seed S. For j=0,...,255 in order, compute x_j as the little-endian integer in the first two bytes of full SHA-256(`HS-BATCH-v1` || S || uint16le(j)).
Keep preceding x values in an ordered list and scan it for equality. At the first repeated value x_i=x_j, i<j, return M(x_i,i) and M(x_j,j). If no value repeats, return failure. There is no restart, adaptive stopping rule, or selection of a favorable seed.
Define M(x,j) as 16 little-endian 32-bit words: word0=x, words1..7=0, word8=j, words9..15=0. The Python program is a direct experimental implementation of this algorithm; it returns every requested trial, including failure.

## Exact correctness of each returned witness
The messages differ at word8 because i<j. Their words0..7 are equal.
The first eight MD5 steps read only words0..7. Starting from the same IV, both first-block executions and their feed-forward states are identical.
Both messages have length64 bytes. Their additional padding block has word0=0x80, words1..13=0, word14=512, word15=0. Hence their second-block inputs are equal, and the already-equal states remain equal through compression and feed-forward.
Their complete 128-bit digests are therefore equal. No assumption about MD5 output uniformity is used in this witness argument.
The first-round schedule and padding follow [RFC1321 sections3.1-3.4](https://www.rfc-editor.org/rfc/rfc1321.html#section-3.4); the selected prefix convention is the organizer's explicit profile.
No fixed collision is stored, no previously solved message pair is replayed intentionally, and preprocessing/advice supplies no collision.

## The score-critical success heuristic H-birthday-seed-expansion
For the specified concrete seed expansion, assume the probability of at least one repeated x among the 256 counters is at least0.39 over uniformly random S. This is the sole unestablished population premise.
The motivating iid-uniform model gives exactly p_ideal = 1 - product_{j=0}^{255}(1-j/65536), approximately0.39267752673178724.
This product is exact for independent uniform 16-bit draws, not a theorem that truncated, counter-keyed SHA-256 values have that joint distribution. SHA-256 is a fixed deterministic function; a uniformly random seed does not itself prove independence of its outputs.
Every repeated value gives a valid collision by the preceding argument. Thus, conditional on the concrete probability premise, this single bounded batch succeeds with probability at least0.39. The heuristic concerns the attack's algorithmic success probability, not a model's epistemic confidence.
The experiment `birthday-batches` runs this exact batch algorithm for256 organizer-selected seeds, with target hashes recomputed by the host and all failures retained. The observed fraction is relevant evidence for this premise; source inspection checks which algorithm was sampled.
The runner's fixed public seeds provide reproducibility, not independent ideal coins or an after-commitment blinded holdout. No favorable-seed search, model of adaptive hypothesis selection, confidence lower bound, or exhaustive count over all seeds is supplied.
The source's simplicity and a finite frequency near the birthday prediction can support plausibility. They do not independently certify the0.39 lower bound, statistical independence, or ordinary-rigor sufficiency. The judge must decide whether this evidence discharges the claim's required obligation under each lane.
If the true probability is below0.39, this particular stated single-batch claim fails the required success threshold. The reported time does not silently add restarts. Nothing is extrapolated to more MD5 steps, another target, or larger batches.

## Resource accounting in collision-frontier-v3
The bounds concern a direct logical256-bit word-RAM implementation of the stated algorithm, not CPython, JSON transport, experiment orchestration, or observed wall time. The experiment is evidence for the algorithm, not a runtime certificate.
All full SHA-256 seed-expansion work is charged as primitive word operations. A non-target SHA-256 compression is not a free or unit-cost MD5 target compression.
Each expansion input has45 bytes (11-byte domain,32-byte seed,2-byte counter), hence one SHA-256 padded block. A direct implementation of its64 rounds and48 expanded words, including masking32-bit arithmetic on the256-bit RAM, has fewer than2^14 primitive operations per hash: budget128 per round,64 per schedule word, and2048 for input/output and setup gives13312<16384.
At most256 hashes therefore cost less than2^22 operations. Each budget includes loads, stores, comparisons, branches, shifts, masks, additions, Boolean operations, and loop control. SHA-256's concrete schedule is the standard FIPS180-4 one; there are no oracle calls.
There are at most256*255/2=32640 list comparisons. Allow16 primitive operations per inspected entry for index arithmetic, loads, equality, branch, and loop control: fewer than2^19 operations. Fixed table allocation, construction of two64-byte messages, seed acquisition, and output/checking receive an additional2^18-operation budget.
Two final target hash verifications take four selected-target compressions. They are optional because witness correctness is exact; charging them cannot increase the stated bound materially. The total is less than2^22+2^19+2^18+4<2^23 charged units for every seed, including failed batches.
Peak logical memory is below2^17 bytes:256 stored values at32 bytes each=8192 bytes, at most128 words of SHA-256 working/constant storage=4096 bytes, messages/seed/counters/stack at most8192 bytes, and at most65536 bytes of fixed machine code and constants. These sum86016<131072. Reuse scratch space between hashes; do not retain all digest states or experiment batches.
Code-size budget65536 bytes can hold this bounded loop-based arithmetic implementation; it is not uncharged nonuniform advice. No precomputed collision, input-specific table, or hidden data is used. All table initialization occurs online and is included above.
`data_log2=8` conservatively permits256 internally generated message descriptions per batch, though at most two complete target messages are returned. There is no external data. `preprocessing_log2=0` and `nonuniform_advice_log2_bytes=0` mean no separate preprocessing or advice; the nonnegative log schema represents the absent categories by their unit upper bounds.
The submitted scalar is23+17=40. Both exponents are conservative upper bounds, not an optimized cost or Pareto claim. A lower model-reconstructed bound must not silently change the submitted score.

## Interpretation and noncompetitiveness
This construction deliberately uses an inefficient randomized search where deterministic ignored-word collisions are easy. It creates no cryptanalytic advance; it isolates whether the protocol connects a genuine full-collision experiment to a genuinely heuristic success claim.
The target is a test-only paired instance of the existing local eight-step MD5 definition. No registered frontier target or qualified baseline is replaced. Any score is an isolated diagnostic artifact, not a leaderboard result.
The scientific obligations are deliberately separable: returned witness correctness is algebraic and mechanically checked; bounded resource accounting is explicit; the population success threshold depends on a disclosed seed-expansion heuristic; the lane policy decides how far finite evidence carries that heuristic.

## Sources and implementation limits
[FIPS180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) defines the SHA-256 expansion primitive; it does not prove this fixture's iid approximation.
The participant program's returned messages are independently checked; the host does not verify the absence of a repeated value in a failed trial, the entire hidden counter trace, or the resource ledger. Source review and the numerical experiment have different scopes.
This submission does not claim a statistical confidence interval. The256 finite observations are not256 proofs about unseen seeds.
The seed-expansion premise is testable further with independently selected seeds or exact counting on a smaller seed domain, but neither has been substituted for the actual256-bit population claim here.
No statement here licenses a conditional claim on legacy `unconditional-v1` tracks; this is exclusively the organizer-declared paired-lane calibration instance.

End of the frozen fixture description.
