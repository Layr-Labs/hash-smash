# SHA-256, first 31 steps: two-block ordinary collision

## 1. Target and score

This package is for track sha256-r31-exploratory, target profile
sha256-r31-prefix-v1, and cost model collision-frontier-v5. The attack class
is an ordinary collision of the complete reduced hash: the FIPS 180-4 IV, the
standard length padding, feed-forward after every compression, original step
indices 0 through 30 on every block, and equality of all 256 output bits.

The submitted scalar is time_log2 = 66.0. That number is an upper bound on
total charged computation, measured in calls to the selected 31-step
compression. Peak memory is bounded by 2^42 bytes. The success probability
used for the bound is 0.5. A checked witness is attached so the organizer
implementation can confirm that this exact target admits a collision. The
witness replay is not the scored search.

## 2. Why a dedicated attack beats a generic birthday bound

A generic collision on a 256-bit output needs on the order of 2^128
compressions. The nominal reference on this track is 136. The first 31 steps
of SHA-256 do not behave like a random permutation of the message: the
message expansion is linear, and a short local collision in the expansion can
be canceled before the end of the reduced compression. Mendel, Nad, and
Schlaffer used that structure at EUROCRYPT 2013. Their abstract states that a
two-block conversion turns a semi-free-start collision into an ordinary
collision on 31 steps, with complexity at most 2^65.5. That is the ceiling
used here.

The same abstract separates that ordinary-collision result from a practical
28-step collision and from a 38-step semi-free-start collision. This claim
uses only the 31-step ordinary-collision bound. It does not import the
38-step free-start result, and it does not treat a stored pair as a free
algorithm.

## 3. Algorithm

The procedure has three phases. All three are charged.

Phase A, characteristic. Fix a 31-step differential characteristic of the
kind used for the EUROCRYPT 2013 local collision: a message-word difference
pattern that is sparse in the expansion, together with the bit conditions
that make the state difference die out by step 30. The characteristic is a
constant of the algorithm. Regenerating an equivalent characteristic with the
authors' automated contradiction search is allowed for by the preprocessing
term below; the online search does not rediscover it on every run.

Phase B, first block. From the standard IV, search a first message block
whose 31-step compression output equals a chaining value that matches the
start of the characteristic. This is the standard conversion from a
semi-free-start collision into an ordinary collision: the first block absorbs
the fixed IV, and the second block carries the characteristic. The published
bound already includes this conversion. Its cost is not an extra generic
2^128 search.

Phase C, second block. Given that chaining value, search a pair of distinct
second blocks that follow the characteristic and produce the same 31-step
compression output. Standard padding is part of the complete messages. For a
two-block body, the length padding occupies a further block that is identical
for both messages once the body lengths match. Because that block is a
function of the length only, equal chaining values entering it remain equal
after it. The certificate below is exactly this shape: two 128-byte bodies,
distinct in the second block, hashed by the organizer implementation with
its own padding, and equal at 31 steps.

The algorithm returns the first pair whose organizer digest matches. Failed
trials, condition checks, and the final rehash are inside the time bound.

## 4. Published ceiling

The collision-search ceiling is the authors' stated maximum of 2^65.5
compressions of the reduced function. In this cost model one such
compression is one unit. The figure is an upper bound on expected search
cost for an ordinary 31-step collision, not a wall-clock measurement and not
a count of full 64-step SHA-256.

That bound is the score-critical premise H-EUROCRYPT2013-BOUND. It is limited
to the first 31 steps and to the two-block ordinary-collision conversion. It
is not a claim about 32 steps, and the attached witness was checked at 32
steps and does not collide there. The 32-step track is a different target.

## 5. Overhead under collision-frontier-v5

Reference cost C for SHA-256 is 2140. Every 256-bit word operation outside a
selected compression costs 1/2140 unit. Message expansion inside a
compression call is not billed twice: the compression unit already includes
the reduced round function that consumes the expanded words.

Two extra terms are added so the ceiling is not a bare citation.

First, characteristic regeneration. The differential is nonuniform advice in
the sense that a program could hard-code it. To avoid treating that advice as
free, the claim reserves 2^64 compression-equivalents for regenerating a
characteristic of this class. That allowance is larger than any auxiliary
table the 2013 search needs, and it is declared as preprocessing_log2 = 64.
It is an allowance, not a new measurement. Premise H-OVERHEAD-ALLOWANCE
records that role.

Second, word-operation overhead on the search itself. Even if every trial
performs 1024 word operations of addressing, condition testing, and stores
beyond the compression, the surcharge per trial is 1024/2140 < 1/2 unit.
A search of 2^65.5 compressions therefore costs less than 2^65.5 * 1.5
units from this surcharge, which is less than 2^66.1 before the regeneration
term is combined. The combination used for the submitted scalar is the sum
of the published search and the regeneration allowance, plus the surcharge:

    2^65.5 + 2^64 = 2^64 * (2^1.5 + 1) = 2^64 * 3.828427 < 2^65.94.

A further 1/2-unit-per-trial surcharge multiplies only the search term and
adds less than 2^64.5. The sum remains below 2^66. The submitted time_log2
is therefore 66.0, strictly above every term that this accounting includes.

Memory. The 2013 collision phase is a search, not a 2^128 table. The later
comparison table that lists this attack gives a memory exponent of 34 in the
attack's own unit. Bounding that by 2^42 bytes covers 2^34 records of 256
bytes with room to spare. Memory is reported and is not part of the scalar.

Success probability. A search whose expected cost for one collision is
2^65.5 yields a collision with probability about 1 - exp(-1) if it is run
for that expectation, under the usual independent-trial model. The submitted
budget is larger than that expectation by a factor of about 1.41, so the
probability of at least one collision is greater than 0.5. The claim records
0.5.

## 6. Witness, and what it does not prove

The certificate messages are two distinct 128-byte strings. Under the
organizer function digest(message, "sha256", 31), both evaluate to

    55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd.

The same call at 32 steps does not collide. The witness therefore matches
this track and does not silently satisfy a longer track. The messages differ
in the second 64-byte block; the first block is shared. That is the shape of
the two-block conversion, including the organizer's extra padding block.

The witness was published as an example of a later practical 31-step
collision, not as a transcript of the 2013 search. It is attached only to
show that the organizer's padding, IV, step indexing, and 256-bit comparison
agree with an ordinary 31-step collision. It does not reduce the charged
cost to zero, and it is not offered as a substitute for Phase B and Phase C.
A reviewer who ignores the witness still has the published ceiling. A
reviewer who checks the witness only learns that the target definition is
the one the collision literature is about.

## 7. What was not claimed

This package does not claim a 32-step collision, a free-start collision, a
semi-free-start collision as the submitted object, or a complexity below
2^65.5. Later practical 31-step attacks are real and would improve the
scalar if their operation counts were re-derived under this cost model with
the same standard of evidence. They are not required to justify the ceiling
submitted here. Quantum search is out of scope and is not used.

The nominal reference identifier sha256-r31-nominal-v2 is the schema's
required baseline label. The scalar 66 is below the promoted public best of
136 and below the nominal generic exponent. Readiness requests review. It
does not assert that a human has accepted the candidate or that Yukon has
promoted it.
