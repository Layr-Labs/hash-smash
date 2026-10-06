# Five-round SHA3-256 collision: byte-aligned port of the Guo–Liao–Liu–Liu–Qiao–Song connector attack

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This exploratory package targets sha3-256-r5-prefix-v1. It proposes a classical
randomized algorithm with claimed success probability at least 1/2, total
charged time below 2^50 target-compression units, and peak memory below 2^30
bytes under collision-frontier-v5. The claimed scalar is 50.

The algorithm is the published practical collision attack of Guo, Liao, Liu,
Liu, Qiao and Song, "Practical Collision Attacks against Round-Reduced SHA-3",
Journal of Cryptology 33 (2020), 228-270, also available as IACR ePrint
2019/147, restricted to a byte-aligned message domain. No novelty over the
published literature is claimed; the contribution of this package is a careful
re-derivation of the attack's cost under this track's byte-string message
domain, its padding rule, and its scoring units.

## 1. Exact complete hash

Each message produced by the attack is exactly 135 bytes, of bit length
1080 < 2^64. The sponge state is 1600 bits arranged as 25 lanes A[x,y] of
64 bits indexed x + 5y, initialized to zero.

H pads m to one 136-byte rate block

    m || 0x86,

where 0x86 is the SHA3 domain suffix 0x06 with the pad10*1 final bit OR-ed
into the same last byte; since len(m) = 135 = rate - 1, the suffix and both
padding bits land inside byte 135. The 17 little-endian 8-byte lanes of the
block are XORed into A[0],...,A[16]; the remaining eight capacity lanes stay
zero. Rounds 0,1,2,3,4 are applied in order; each round computes, with all
coordinates modulo 5:

    C[x] = XOR over y of A[x,y]
    D[x] = C[x-1] XOR ROT64(C[x+1],1)
    A[x,y] = A[x,y] XOR D[x]
    B[y,2x+3y] = ROT64(A[x,y],rho[x,y])
    A[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] XOR RC[round].

The rho offsets (rows y, columns x) are

    0   1  62  28  27
   36  44   6  55  20
    3  10  43  25  39
   41  45  15  21   8
   18   2  61  56  14

and the five round constants are 0000000000000001, 0000000000008082,
800000000000808a, 8000000080008000, 000000000000808b. After round 4,
H(m) = LE8(A[0])||LE8(A[1])||LE8(A[2])||LE8(A[3]), the first 32 squeeze bytes.
This is the profile's complete hash: standard FIPS 202 padding and domain
suffix, all-zero 1600-bit IV, prefix rounds 0-4 (not Keccak-p's last-round
convention), full 256-bit output. Each complete hash costs exactly one
selected five-round permutation.

## 2. The published attack

Dinur, Dunkelman and Shamir (FSE 2012/2013) introduced the connector
framework: combine a low-round differential trail with a connector that
algebraically produces messages reaching the trail's input difference.
Guo et al. extended connectors to two and three rounds by linearizing the
Keccak chi S-box in the first round(s): restricting message values to
suitable affine subspaces of dimension at most 2 per S-box turns the
nonlinear equations into linear ones, after which connector solutions are
solutions of a GF(2) linear system. For 5-round SHA3-256 they combine a
2-round connector (rounds 0-1) with a 3-round differential trail
(rounds 2-4) whose input difference alpha_2 equals the connector's output
difference.

Their results for this instance (their Table 6): differential trail core
No. 3 (reproduced in Section 3 below), connector construction cost Tc =
428.8 CPU core-hours, connector output space dimension DF = 37, trail weight
w = 36.70 accounting for multiple trails over the last two rounds, and a
collision-search time Tb = 45.6 core-hours on three GTX970 GPUs. Their
footnote states that usual computers evaluate around 2^20-2^22 Keccak
evaluations per second. The published pair is a real collision from the
all-zero IV on the standard sponge, not a free-start or compression-only
result; their Table 17 prints the two one-block padded message states and
the common 256-bit digest.

## 3. Trail core No. 3 and the published witness

Trail core No. 3 is the 4-round core (beta_2, beta_3, beta_4) used for both
5-round SHA3-224 and 5-round SHA3-256. The paper lists it as a 5x5 lane
table with '-' denoting zero nibble; the full table is transcribed in
Appendix D of the paper. Its key parameters, which this package relies on:

    per-round transition weight product gives w = 36.70
    (24 for beta_2 -> alpha_3, 19 for beta_3 -> alpha_4, and the final
    round is free since alpha_5 only needs zero difference in the digest
    lanes; the 36.70 exponent already aggregates multiple compatible
    last-round trails).

The published collision (their Table 17) transcribed as two 5x5 lane
states, lanes written as 64-bit hexadecimal lane values, capacity lanes
17-24 all zero:

    M1 rows y=0..4:
    FECA67BD2D3F021A BD10A64A4C2B774F F8EF6FF82DD21FC7 6F4BA4D964A78764 0F4FD1C92A24BC6E
    FB4B8C0A11C64088 EDA7B9EBC05F50A8 0A71DD08E7F1EB5B 5342D2AE78A8BFB5 6591A9B0CC2E7CE9
    52A3DD827F4EF6DC 9D89B18362B80DE4 FEA719A1875BFFF7 49A2B95AD7B7D147 B23784B72EB9260A
    187AEFD07295FD59 EE806366EF9D09FF 0000000000000000 0000000000000000 0000000000000000
    0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000

    M2 rows y=0..4:
    16F97050842C2D17 A731EE935A43480A 6D8E356BDBD7CBE9 D62C0B356FFA158A 4FAD968080C7F8C8
    7C83B8E1C61BC5AB 7E3FCA22B5E29305 5888D4DBE848C840 236DE21CCEF77B8A 69D59EF589070E60
    E87FCD2BF2C6CCE1 B1E28B821FD93ABC AD5D6FB1860CB45C AB8FC7D1015975D5 24C6B737EE96CC23
    D3BFB5957965A447 EE31D3F5269F254F 0000000000000000 0000000000000000 0000000000000000
    0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000

    digest: 65017C2E8B6040B4 344FF8BB933B4BD6 C6A3F13368BE2003 AB427B4B33435ACB

We verified this transcription directly against the organizer's reference
permutation (verifier/keccak.py, which is the referenced implementation for
this profile): loading each table as the 25-lane sponge state and applying
the pinned prefix permutation with rounds=5 produces, for both M1 and M2,
first four output lanes 65017c2e8b6040b4 344ff8bb933b4bd6 c6a3f13368be2003
ab427b4b33435acb, i.e. the printed digest, in standard little-endian lane
serialization. This is a permutation-level check that the states and round
convention match this profile exactly; it is reproduced in minutes by the
snippet in Section 7.

## 4. The padding caveat, analyzed exactly

The published padded blocks are not byte-level padded messages under FIPS
202. Their last rate byte (byte 135, the high byte of lane 16) is 0xEE in
both messages. Reading bits LSB-first gives [0,1,1,1, 0,1,1,1]: four free
message bits, the two-bit SHA3 suffix '01', and the compressed pad '11'.
So each published message has 1084 bits = 135 bytes + 4 bits. This target's
message domain is finite byte strings; a 1084-bit string is not a byte
string, and no choice of byte-level message length recreates the tabulated
block, because the verifier always places the suffix at a byte boundary.

Concretely: for a one-block padded input the last rate byte must equal
either 0x80 (message at most 134 bytes, byte 134 = 0x06 suffix and the
interior zero) or 0x86 (exactly 135 bytes). The tabulated 0xEE satisfies
neither, so the published states are not reachable as single-block padded
byte messages. Multi-block rewrites cannot rescue them either: after the
first permutation the capacity lanes are nonzero and pseudorandom, the
final absorbed block only XORs the rate, so a pre-permutation state with
zero capacity (as tabulated) is unreachable except after the first block.

The correct byte-aligned variant therefore fixes byte 135 to 0x86, i.e.
messages of exactly 135 bytes. Relative to the paper's construction this
adds four fixed bits to the connector's constraints: their construction
fixed the last nibble '1110' and left the other four bits free, while the
byte-aligned version fixes all eight bits of byte 135.

## 5. Byte-aligned algorithm

The claimed algorithm is the paper's construction with the tighter padding
constraint:

1. Connector preprocessing. Repeat the 2-round connector construction of
   Guo et al. Section 4 with the message domain restricted to 135-byte
   messages (byte 135 fixed to 0x86, i.e. eight fixed bits). Each solve
   returns an affine subspace of message pairs whose post-connector
   difference equals alpha_2 of trail core No. 3.
2. Collision search. Sample pairs uniformly from each returned subspace;
   for each pair, evaluate the remaining three rounds and test whether the
   256-bit digests agree. Expected trials per collision: 2^36.70.
3. On the first digest collision, return the two messages; they are
   distinct byte strings hashing to the same complete 256-bit output.

Degrees of freedom. The paper's SHA3-256 connector returned DF = 37 free
dimensions with four padding bits fixed. Fixing four more input bits can
remove at most four dimensions (fixed bits constrain input freedom, and
constraints are linear over GF(2)), so the byte-aligned space has estimated
dimension DF' between 33 and 37; we use DF' = 33 as the nominal estimate
and disclose the downside sensitivity explicitly below. A linear
constraint can also interact with the S-box linearization choices, which
could reduce DF' further; the claimed bound contains slack for that.

## 6. Resource accounting under collision-frontier-v5

One selected five-round permutation costs one unit; every other listed
256-bit RAM operation costs 1/1355 units. All phases, including failed
connector solves and failed pair trials, are charged.

Connector solves. The paper's measured cost for one SHA3-256 connector
construction is Tc = 428.8 CPU core-hours = 428.8 x 3600 s ~ 1.544e6 s.
Converting at the aggressive end of the paper's own rate figure, 2^22
evaluations per second, gives 2^42.6 evaluations; we charge each reported
evaluation as a full target permutation call, i.e. at most 2^43 units per
solve. This subsumes the GF(2) system assembly, the S-box linearization
bookkeeping, and all restarts inside one solve, since all of that is inside
the reported wall time.

Solve budget. We budget N_s = 64 independent solves. Connector solves are
rerun with fresh random linearization/subspace choices, so returned spaces
are treated as independent samplers of message-pair candidates
(heuristic solve-space-independence). Preprocessing charge: 64 x 2^43 = 2^49
units.

Pair enumeration. Each solve yields at most 2^37 candidate pairs (using
the paper's dimension as the upper bound). Sampling one pair from the
affine subspace and evaluating the three remaining rounds with early
abort, plus loop bookkeeping, costs at most 2 units per pair. Across all
solves this is at most 64 x 2^37 x 2 = 2^44 units; in expectation the
attack stops after about 2^36.7 trials.

Final verification. Two complete hash evaluations and comparisons:
under 2^16 units.

Totals. Charged time

    T <= 2^49 (connector) + 2^44 (enumeration) + 2^16 (verification)
      < 2^50  ->  time_log2 = 50.

preprocessing_log2 = 49 bounds the connector phase alone; it is included
in T, not omitted. memory_log2_bytes = 30: the GF(2) system for a
rate-1088 connector is on the order of 10^6-10^7 bits (a few MB), pair
sampling keeps only the current pair, and all public constants (round
constants, rho offsets, the transcribed trail core, ~2^10 bytes) fit far
below 2^30 bytes. nonuniform_advice_log2_bytes = 0: no stored collision or
target-derived advice is supplied; the published trail core is public
literature charged as constants in memory, and the schema cannot express
log2(0).

## 7. Success probability

Let DF' be the byte-aligned connector dimension and lambda the expected
number of collisions across the budgeted space. Each candidate pair
collides with probability about 2^-36.70 (heuristic trail-probability-carryover),
so

    lambda = N_s x 2^(DF' - 36.70).

For the nominal DF' = 33 and N_s = 64, lambda ~ 9.7 and the probability of
at least one collision is 1 - e^-lambda ~ 0.9999. The claim holds down to
DF' = 30.2, where lambda ~ 0.69 gives probability 0.5. We therefore claim
success_probability = 0.5, covering DF' >= 30.2. If DF' fell below ~30,
the same budget yields lower probability; that regime is a disclosed
limitation, not a hidden assumption, and the scalar 50 remains an upper
bound on charged time.

The probability space is the fresh random coins of the connector solves
and the uniform sampling of pairs from each returned subspace, applied to
the fixed target. This concerns algorithmic success, not confidence in the
underlying heuristic premises, which are declared separately.

## 8. What this package does and does not assert

- The attack construction, trail core, connector machinery, witness pair
  and measured costs are due to Guo, Liao, Liu, Liu, Qiao and Song
  (JoC 2020 / ePrint 2019/147). This package ports that published work to
  this track's byte-string domain and re-expresses its cost under
  collision-frontier-v5. No novelty is asserted.
- The permutation-level verification of Section 3 was performed locally
  against the organizer's own verifier/keccak.py. No byte-string collision
  certificate is supplied: the only published pair is not byte-aligned, so
  it cannot serve as a hash-collision-witness-v2 certificate, and the
  certificate manifest is intentionally empty. The claim rests on the
  published existence proof plus the resource accounting of Section 6.
- The claimed scalar 50 is conservative: it is about 2^3.4 above the
  nominal estimate 46.6 (= 13.6 expected solves x 2^43 + 2^38
  enumeration). Slack covers the DF' sensitivity and the wall-time
  conversion interpretation.
- The residual risk is the byte-aligned connector dimension DF'. If
  DF' < ~30 the claimed success bound would need a larger solve budget;
  that dependency is declared (connector-dof) rather than assumed away.
- This is a reduced-round result on prefix rounds 0-4. It says nothing
  about the full 24-round SHA3-256.

## 9. Verification snippet

The permutation-level check used for Section 3, run against the
organizer's reference implementation:

    from verifier.keccak import permutation
    lanes = [...25 integers transcribed from the table above...]
    state = b"".join(l.to_bytes(8, "little") for l in lanes)
    out = permutation(state, width_bits=1600, rounds=5)
    digest = out[:32]

Both tabulated states give digest (lane order)
65017c2e8b6040b4 344ff8bb933b4bd6 c6a3f13368be2003 ab427b4b33435acb,
serialized 2e7c0165...; equality of the two output prefixes is the
witnessed fact. The check file is not part of the reviewed package; it is
described here so reviewers can reproduce it.
