# Orchard Poseidon constants and official vectors

Upstream crate: `halo2_poseidon` 0.2.0, from
[zcash/halo2](https://github.com/zcash/halo2/tree/halo2_poseidon-0.2.0) at tag
`halo2_poseidon-0.2.0`. This is the version the `orchard` crate depends on, and
its constants are unchanged since May 2022, before NU5 activated.

The instance is `P128Pow5T3` over the Pallas base field: width 3 with rate 2
and capacity 1, S-box `x^5`, `R_F = 8` full rounds and `R_P = 56` partial
rounds. It matches the Zcash Protocol Specification, section 5.4.1.10.

## Encoding

Every field element in this file, including the round constants and MDS
entries, is its canonical 32-byte little-endian encoding as lowercase hex.
That is the deployed encoding for messages and digests, so one rule covers the
whole fixture. `field_modulus_hex` and `capacity_element_hex` are instead
written as plain hex integers, because neither is a field element.

## Constants

`round_constants` holds 64 rows of 3 values, so 192 constants in deployed
order, and `mds` holds the 3x3 matrix. Both were read directly from
[`halo2_poseidon/src/fp.rs`](https://github.com/zcash/halo2/blob/halo2_poseidon-0.2.0/halo2_poseidon/src/fp.rs),
whose `from_raw` limbs are plain little-endian 64-bit limbs of the integer
value. That file records that the values are reproducible by running the
Poseidon v1.1 reference generator from
[pasta-hadeshash](https://github.com/daira/pasta-hadeshash) as

```text
sage generate_parameters_grain.sage 1 0 255 3 8 56 0x40000000000000000000000000000000224698fc094cf91b992d30ed00000001
```

Round `i` of the deployed schedule uses row `i`. A reduced instance under the
prefix convention uses the first `r` rows unchanged and the same MDS matrix.

## Vectors

The 11 permutation vectors and 11 hash vectors were read from
[`halo2_poseidon/src/test_vectors.rs`](https://github.com/zcash/halo2/blob/halo2_poseidon-0.2.0/halo2_poseidon/src/test_vectors.rs).
That file records them as the official Zcash vectors from
[zcash/zcash-test-vectors](https://github.com/zcash/zcash-test-vectors), whose
`orchard_poseidon.rs` and `orchard_poseidon_hash.rs` carry the same values.

`permutation_vectors` give a full 64-round permutation applied to an explicit
three-element state. `hash_vectors` give the deployed `ConstantLength<2>`
hash: `message` is the 64-byte concatenation of the two input elements and
`digest` is the single output element. Upstream's own `orchard_spec_equivalence`
test asserts that this hash equals permuting `[m0, m1, 2^65]` and taking
element 0, which is the relation the Python implementation reproduces.

All expected values here come from the upstream Rust sources. The Python
implementation under test did not generate its own expected answers.

## Reduced rounds

Upstream publishes vectors only for the full 64 rounds, so no official vector
exists for rounds 1 or 2. The tests instead recompute those prefixes from the
round definition independently of the implementation, and check that each
prefix differs from the others and from the full permutation.
