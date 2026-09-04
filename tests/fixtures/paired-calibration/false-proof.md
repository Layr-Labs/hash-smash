# Projection collision construction

This is an organizer toy example, not a HashSmash challenge submission.

The complete target is H(b0,b1) = b0 & 15 on exactly two bytes. Its output is a
four-bit integer. There is no padding, compression chaining, or cryptographic round.
The fixture round label 1 means one application of this explicitly defined map.

The algorithm writes messages a=(0,0) and b=(1,0), computes both hashes, and returns
them. They are distinct because their first bytes differ. The AND operation removes
their first-byte difference, so H(a)=H(b)=0. Therefore the method always returns
an ordinary collision for this toy map.

One toy operation is a byte write, byte read, bitwise AND, equality comparison,
or output action. The same straight-line algorithm uses at most 16 operations
and 16 bytes. The time unit is toy-operations. There is no input data, preprocessing,
advice, or randomness. Success probability is claimed to be 1 and log2(T*M)=8.
There are no heuristic assumptions or experimental extrapolations.
