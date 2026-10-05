# blake3-r1: deterministic ordinary collision in 2^0.1 target compressions

## 1. Claim
For the 1-round BLAKE3 hash `blake3-r1-prefix-v1` (standard IV, unkeyed, standard chunk/tree mode, only round 0 kept in every compression), we give a straight-line algorithm that outputs two distinct 64-byte messages with equal digests. Both digests are the all-zero string.
- It uses 236 primitive word operations: 204 arithmetic/logic operations counted as the reference normalization counts them, plus 32 stores of the two 16-word messages. With C = 222 operations per target compression this is 1.063 compressions = 2^0.088. We claim **time_log2 = 0.1**.
- Success probability: 1. Memory: under 2^10 bytes.
- No search, randomness, heuristic or precomputed advice is involved.
- The messages are attached as a `hash-collision-witness-v2` certificate, and the organizer verifier recomputes both digests.

## 2. Target recap
A 64-byte message is one chunk with one block, so its digest is the first 8 output words of a single compression with these inputs:
- h = IV (8 words);
- counter t = 0, block length 64;
- flags = CHUNK_START|CHUNK_END|ROOT = 11.

State: v[0..7] = h, v[8..11] = IV[0..3], v[12..15] = (0, 0, 64, 11). One round runs:
- the column G's col_k = G(k, k+4, k+8, k+12; m_{2k}, m_{2k+1}) for k = 0..3;
- then the diagonal G's Gd0 = G(0,5,10,15; m8,m9), Gd1 = G(1,6,11,12; m10,m11), Gd2 = G(2,7,8,13; m12,m13), Gd3 = G(3,4,9,14; m14,m15).

Digest word i is o_i = v_i ⊕ v_{i+8}, little-endian.

G(a,b,c,d; x,y):
- a1 = a+b+x
- d1 = (d⊕a1)⋙16
- c1 = c+d1
- b1 = (b⊕c1)⋙12
- A = a1+b1+y
- D = (d1⊕A)⋙8
- C = c1+D
- B = (b1⊕C)⋙7

Outputs are (A, B, C, D); all additions are mod 2^32.

## 3. Facts about one G call
Each fact follows by rewriting the G equations one at a time.

- **F1. Outputs (A, D) given inputs (b, c).** Every (A, D) is reached, and it determines B and C:
  - d1 = (D⋘8)⊕A
  - c1 = c+d1
  - C = c1+D
  - b1 = (b⊕c1)⋙12
  - B = (b1⊕C)⋙7

  With the a and d inputs, the message words are x = a1−a−b and y = A−a1−b1, where a1 = (d1⋘16)⊕d.
- **F2. Outputs (B, C) given inputs (b, c).** Every (B, C) is reached, and it determines A and D:
  - b1 = (B⋘7)⊕C
  - c1 = b⊕(b1⋘12)
  - d1 = c1−c
  - D = C−c1
  - A = d1⊕(D⋘8)

  Messages follow as in F1.
- **F3. All four outputs fix the b and c inputs:** with d1 = (D⋘8)⊕A, c1 = C−D and b1 = (B⋘7)⊕C, we get c = c1−d1 and b = (b1⋘12)⊕c1. The a and d inputs only enter the message words.

## 4. Construction
The digest pairs Gd0 with Gd2 (o0 = Gd0.A⊕Gd2.C, o2 = Gd2.A⊕Gd0.C, o5 = Gd0.B⊕Gd2.D, o7 = Gd2.B⊕Gd0.D) and Gd1 with Gd3 (o1, o3, o4, o6). All public choices below are the constant 0.
1. **Columns 1 and 2.** Choose their outputs (B, C) = (0, 0) by F2 from the fixed inputs. This gives v5 = v9 = 0 and v6 = v10 = 0, plus v1, v13, v2, v14 and the words m2..m5.
2. **Gd1 and Gd3.** Choose outputs (A, D) = (0, 0). Their b and c inputs are (v6, v11) = (0, γ) and (v4, v9) = (β, 0), and we also choose β = γ = 0. By F1 all their outputs are 0, so o1 = o3 = o4 = o6 = 0. Their a and d inputs (v1, v12) and (v3, v14) only set m10, m11, m14 and m15.
3. **Gd0.** Its b and c inputs are (v5, v10) = (0, 0). Choose its outputs (A0, D0) freely; F1 gives B0 and C0.
4. **Gd2.** Set its outputs (a, b, c, d) = (C0, D0, A0, B0), so that o0 = o2 = o5 = o7 = 0. F3 gives the b and c inputs it needs, v7* and v8*.
5. **Columns 0 and 3.** Column 0 has inputs (h0, h4, IV0, 0) and outputs (B, C) = (β, v8*) = (0, v8*). Column 3 has inputs (h3, h7, IV3, 11) and outputs (B, C) = (v7*, γ) = (v7*, 0). Both are solved by F2, giving v0, v12, m0, m1 and v3, v15, m6, m7.
6. **Remaining message words.** Gd0 with inputs (v0, 0, 0, v15) gives m8, m9. Gd2 with inputs (v2, v7*, v8*, v13) gives m12, m13.

Every digest word is 0 for every (A0, D0). Different (A0, D0) give different Gd0 outputs, so the blocks differ. We output (A0, D0) = (0, 0) and (1, 0).

## 5. Operation count (executed program; identities on literal zero constants are skipped)
- **Shared work:**
  - column 1 by F2 with (B, C) = (0, 0): 19;
  - column 2 the same: 20, because its d input 64 is nonzero;
  - Gd1/Gd3 constants: all zero, so m11 = −v12 and m15 = −v14;
  - the m15 negation: 2.
- **Message (A0, D0) = (0, 0):**
  - Gd0's outputs are all 0, hence Gd2's outputs and v7* = v8* = 0;
  - columns 0 and 3 by F2 with (B, C) = (0, 0): about 20 each;
  - message words m8..m14: about 24.
- **Message (1, 0):**
  - Gd0 F1: 9;
  - F3 for Gd2: 14;
  - columns 0 and 3 by F2: 24 and 29;
  - message words: about 30.

The program counts every operation as it runs. **Total: 204 arithmetic/logic operations.** Adding 32 stores (two 16-word messages; IV words are immediates) gives 236 operations, 236/222 = 1.063 target compressions, and log2 = 0.088. The claim of 0.1 rounds up. No target compression is evaluated anywhere in the attack.

## 6. The program (straight-line; rotations and modular operations as above; zero-identity operations omitted)
```
col1: b1=0; c1=h5; d1=h5-IV1; D=0-h5; A=d1^(D<<<8); a1=d1<<<16; m2=a1-h1-h5; m3=A-a1      ; v1=A; v13=D
col2: b1=0; c1=h6; d1=h6-IV2; D=0-h6; A=d1^(D<<<8); a1=(d1<<<16)^64; m4=a1-h2-h6; m5=A-a1 ; v2=A; v14=D
m15 = 0-v14
for (A0,D0) in {(0,0),(1,0)}:
  # Gd0 outputs (A0,D0) with b=c=0, D0=0: d1=A0, c1=A0, C0=A0, b1=A0>>>12, B0=(b1^A0)>>>7
  # Gd2 outputs (C0,D0,A0,B0): d1'=(B0<<<8)^C0; c1'=A0-B0; b1'=A0; v7*=(b1'<<<12)^c1'; v8*=c1'-d1'
  # column 0 with outputs (B,C)=(0,v8*): c1=h4^(v8*<<<12); d1=c1-IV0; D=v8*-c1; A=d1^(D<<<8); a1=d1<<<16
  #   m0=a1-h0-h4; m1=A-a1-v8*                                   ; v0=A; v12=D
  # column 3 with outputs (B,C)=(v7*,0): b1=v7*<<<7; c1=h7^(b1<<<12); d1=c1-IV3; D=0-c1; A=d1^(D<<<8)
  #   a1=(d1<<<16)^11; m6=a1-h3-h7; m7=A-a1-b1                   ; v3=A; v15=D
  # m8=((d1G0<<<16)^v15)-v0; m9=A0-a1G0-b1G0; m10=v12-v1; m11=0-v12
  # m12=((d1'<<<16)^v13)-v2-v7*; m13=C0-a1G2-b1'; m14=v14-v3
  output (m0..m15)
```

## 7. Result
- message A: `1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d13145758d19cde05b1edfe6897f520e519be3c7c58c68059bdaf5d936abd9831f`
- message B: `010a231c8668aad78cc89a63c6ee026b3716478a85d0f8b841747b2cf6ff9df8af514c77e722dedbf953e32ba4dd11af7af3c6c7ac68069bcdee39baabd9831f`
- Both have the blake3-r1 digest `0000000000000000000000000000000000000000000000000000000000000000`.
- The messages differ in 42 of 64 bytes, and their 7-round BLAKE3 digests differ.
- Certificate `r1-free-0` (`certificates/manifest.json`) lets the organizer verifier check the collision mechanically.

## 8. Scope and limitations
- The result is specific to one round. In two rounds every message word is used again (permuted), and F1–F3 no longer decouple the pairs. That case is not claimed here.
- The count is a data-path count in the reference normalization, plus explicit stores of the output. A model that also charged register traffic for every intermediate would at most double the 204 term, which still stays below 3 compressions.
