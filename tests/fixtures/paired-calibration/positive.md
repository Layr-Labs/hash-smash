# Projection collision construction

This is an organizer toy example, not a HashSmash challenge submission.

The complete target is H(b0,b1) = b0 & 15 on exactly two bytes. Its output is a
four-bit integer. There is no padding, compression chaining, or cryptographic round.
The fixture round label 1 means one application of this explicitly defined map.

The algorithm writes messages a=(0,0) and b=(16,0), computes both hashes, and returns
them. They are distinct because their first bytes differ. H(a)=0 & 15=0 and
H(b)=16 & 15=0, so this always returns an ordinary collision for this toy map.

One toy operation is a byte write, byte read, bitwise AND, equality comparison,
or output action. Allocate two two-byte arrays and two one-byte digest registers:
four writes, two reads and two ANDs, one comparison of distinctness, one digest
comparison, and one output action cost at most 11 operations. A loop-free
implementation using four additional one-byte scratch registers uses at most
10 bytes. The submitted conservative bounds are 16 operations and 16 bytes.
The time unit is toy-operations. There is no input data, preprocessing, advice,
or randomness. Success probability is exactly 1, and log2(T*M)=4+4=8.

No heuristic or empirical extrapolation is required. The elementary algebra above
establishes the result independently of running an experiment.
