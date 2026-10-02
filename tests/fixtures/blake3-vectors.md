# Independent BLAKE3 vectors

Upstream BLAKE3 revision: `6aab490a26124663329dfd3961b8469f8fdb158b`.

Full-round cases retain the first 32 bytes of `hash` from the official
[test corpus](https://github.com/BLAKE3-team/BLAKE3/blob/6aab490a26124663329dfd3961b8469f8fdb158b/test_vectors/test_vectors.json).
All messages use the official repeating `i % 251` byte pattern.

For prefix cases, the independent upstream
[Rust reference](https://github.com/BLAKE3-team/BLAKE3/blob/6aab490a26124663329dfd3961b8469f8fdb158b/reference_impl/reference_impl.rs)
was compiled with rustc, changing only the seven explicitly unrolled round calls
inside `compress`: retain the first one or two round calls and the message
permutation between them. The chunk state, parent tree, counters, flags,
feed-forward and root-output implementation remain unchanged. Hash each length
listed in the JSON through `Hasher::new()`, `update(message)`, and
`finalize(&mut [0u8; 32])`. This generated the frozen prefix outputs; the Python
implementation under test did not generate its own expected answers.

Boundary lengths include empty input, 63/64/65 bytes, 1023/1024/1025 bytes,
multiple full chunks, and unbalanced trees through 16385 bytes. Tests also
observe compression calls to check reduction on every chunk/parent/root node.
