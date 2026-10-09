#!/usr/bin/env python3
# vt38.py - variant-table collision attack on 38-step SHA-256 (sha256-r38-prefix-v1): reference construction,
# the counted online program (an op-counting 256-bit word-RAM interpreter running the exact online code), the
# organizer experiments (stdin JSON -> stdout JSON) and a self-test (argument "selftest").  Python 3.9+, stdlib.
# Characteristic, two-bit conditions and semi-free-start pair: Li, Zhang, Li, Liu, Qian, Zhu, "Pushing Collision
# Attacks on SHA-2 to 39 Steps", IACR ePrint 2026/1120 (CC BY), Tables 3-5, as transcribed in earlier public
# HashSmash packages (proof.md Section 2).  Everything else is this package's (proof.md Sections 3-8).
import sys, json, hashlib, struct, math, random, zlib, base64

M = 0xffffffff
K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,
     0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,
     0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
     0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb]
IV = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
R = 38
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def compress(cv, w16):
    w = list(w16)
    for i in range(16, R): w.append((s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16]) & M)
    a, b, c, d, e, f, g, h = cv
    for i in range(R):
        t1 = (h + S1(e) + CH(e, f, g) + K[i] + w[i]) & M; t2 = (S0(a) + MAJ(a, b, c)) & M
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    return [(x + y) & M for x, y in zip(cv, (a, b, c, d, e, f, g, h))]

def digest(msg):
    n = len(msg); p = msg + b'\x80' + b'\x00' * ((55 - n) % 64) + struct.pack('>Q', 8 * n); cv = list(IV)
    for i in range(0, len(p), 64): cv = compress(cv, struct.unpack('>16I', p[i:i+64]))
    return struct.pack('>8I', *cv)

def trace(cv, w16):
    """A[i], E[i] (i = -4..R-1) and W[0..R-1]; step i: E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH + K_i + W_i,
    A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3})."""
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = list(w16)
    for i in range(16, R): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M)
    for i in range(R):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
    return A, E, W

# ePrint 2026/1120 Table 3 (38 steps), MSB first; unlisted rows are all '='.  Member x = the message printed second.
# 'u' = (x, y) bits (1, 0), 'n' = (0, 1), '0'/'1' fixed equal, '=' equal; '+' in rows i-1 and i: E_i[b] = E_{i-1}[b].
CHAR = dict(
 A={7:'=nu=============================',8:'=========n=====n====n======u====',11:'====================u=======un==',
    12:'=u===n====n======u===nu=======n=',13:'==n============n================',14:'====u=========nn========u==u====',
    15:'======n=u=======n===============',17:'==u============================='},
 E={5:'+++=============================',6:'+++=1====0==+1=====0+===1==1====',7:'uuu=0+1=11=0+00====1+===0==00=01',
    8:'100=u+010n=1nu01=01nu=00n11u1=01',9:'11000u1=n11u0000101101110=01u0uu',10:'==1010=01u00001u=010u=101==10111',
    11:'1=n000=0111100101unn00011+111u10',12:'01nuuu=110n111nu000100100+010u1n',13:'00110101110=000u00111nuu+nnnu1n1',
    14:'=010n0===00===1n=11+0100+1110001',15:'=1==1=1==0=1==11===+u011n1011=1=',16:'=u==10===n===+u1===n0=u=1==+====',
    17:'=0=====+00===+0=+==01=0=0==+====',18:'=0=====+01===n1=+==1==1===0u====',19:'==11===nn====1==n===010===11==0=',
    20:'==1====00====1==0==========1====',21:'==u====10=======1===10==========',22:'==0=============================',
    23:'==1============================='},
 W={7:'==n=============================',8:'=====u===u==========n===========',9:'==u=============================',
    10:'=====n=u=======n===n==n=n=n=u=u=',11:'============u======u=u==========',15:'=====u===n==========n===========',
    16:'==u=============================',23:'=====1=uu=====1=u=1=============',25:'==n============================='})
# Table 4 two-bit conditions with a word in rows >= 16 (member x), W25[4]=W25[9] read as W25[4]=W25[6].
TWOBIT = [('A',14,15,0,'A',16,15),('A',14,23,0,'A',16,23),('A',14,25,0,'A',16,25),('A',15,4,0,'A',16,4),('A',15,7,0,'A',16,7),
    ('A',15,16,1,'A',16,16),('A',15,17,0,'A',16,17),('A',15,27,0,'A',16,27),('A',15,29,0,'A',16,29),('A',16,15,0,'A',17,15),
    ('A',16,23,0,'A',17,23),('A',16,25,0,'A',17,25),('A',17,9,0,'A',17,20),('A',17,6,0,'A',17,18),('A',17,8,0,'A',17,17),
    ('A',16,29,0,'A',18,29),('A',18,29,0,'A',19,29),('E',16,4,1,'E',16,23),('E',16,3,1,'E',16,8),('E',16,14,0,'E',16,28),
    ('E',16,4,0,'E',17,4),('E',16,18,0,'E',17,18),('E',18,0,1,'E',18,13),('E',17,15,0,'E',18,15),('E',17,24,0,'E',18,24),
    ('E',19,6,1,'E',19,19),('E',19,20,0,'E',19,2),('E',21,2,0,'E',21,16),('W',16,1,1,'W',16,12),('W',16,20,1,'W',16,27),
    ('W',16,8,0,'W',16,25),('W',16,14,0,'W',16,18),('W',16,4,1,'W',16,6),('W',16,22,1,'W',16,31),('W',23,0,1,'W',23,30),
    ('W',23,1,1,'W',23,31),('W',23,14,0,'W',23,21),('W',23,16,0,'W',23,25),('W',25,4,0,'W',25,6),('W',25,22,0,'W',25,31),
    ('W',25,20,0,'W',25,27)]
def _h(s): return [int(t, 16) for t in s.split()]
# Table 5: chaining value, M (printed first = member y), M' (printed second = member x).
PCV = _h('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e')
PMY = _h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb')
PMX = _h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb')

def cell(s):
    m = v = d = p = 0
    for c, y in enumerate(s):
        b = 31 - c
        if y in '01un': m |= 1 << b
        if y in '1u': v |= 1 << b
        if y in 'un': d |= 1 << b
        if y == '+': p |= 1 << b
    return m, v, d, p
CELL = {k: [cell(CHAR[k].get(i, '=' * 32)) for i in range(R)] for k in 'AEW'}
PLUS = [0] + [CELL['E'][i][3] & CELL['E'][i-1][3] for i in range(1, R)]
XROW = {}
for c in TWOBIT: XROW.setdefault(max(c[1], c[5]), []).append(c)

def rowok(tx, ty, i, wcell=True):
    """Row i of the pair: A/E cells (x-values, XOR differences), '+' pairs, W cell if wcell, two-bit conditions
    keyed at row i on member x."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    for k, x, y in (('A', Ax[i], Ay[i]), ('E', Ex[i], Ey[i])) + ((('W', Wx[i], Wy[i]),) if wcell else ()):
        m, v, d, _ = CELL[k][i]
        if x & m != v or x ^ y != d: return False
    if (Ex[i] ^ Ex[i-1]) & PLUS[i]: return False
    V = {'A': Ax, 'E': Ex, 'W': Wx}
    for k1, i1, b1, ne, k2, i2, b2 in XROW.get(i, ()):
        if ((V[k1][i1] >> b1) ^ (V[k2][i2] >> b2)) & 1 != ne: return False
    return True

# Published dense part S* (rows 0..15 of both members) and derived constants.
TX = trace(PCV, PMX); TY = trace(PCV, PMY)
D7 = 0x20000000; T7 = 0x03bff800; DW16 = 0x20000000
def inF7(w): return (s0((w + D7) & M) - s0(w)) & M == T7
GBASE, GFREE = 0x35f29010, (0, 2, 10, 13, 19)
G = sorted(GBASE | sum(1 << b for j, b in enumerate(GFREE) if (k >> j) & 1) for k in range(32))
DIFF = {i: ((TX[2][i] - TY[2][i]) & M, (s0(TX[2][i]) - s0(TY[2][i])) & M) for i in (8, 9, 10, 11)}

# Embedded data (zlib + base64, little-endian): the 768 A2 values (proof.md 4.2, A.3), the 256 A0 values (4.3, A.2), one
# valid (A1, A2 index) per A0, 512 variants (A0 index, A1, A2 index): the first 512 of the uniform sample (6.2), and
# four semi-free-start successes of the preregistered SMC (A0, A1, A2, CV1, M1, M1') for the self-test.
A2_B64 = 'eNoNzt3NgloCBdBCbAGS+zbzcQrwJ0zCm0oDIg2INCDSgAgFiLRwGvAm2tOsh/2ws7OT9Umn//wrX/nJ53+6fOUnnzTaoz3ao12Xr/zkk6z++6985Seff3T5yk8+uS5f+cmn0OUrP/kkwT/4B//gr8tXfvLJdfnKTz6FLl/5ySed/vj/+P/4//j/+P/4//j/+O3RHu3Rrgu/XU9WGX/Gn/Fn/Bl/xp/xZ/wZf8af8Wf8GX/Gn/Fn/P7BP/gHf134/fVcF35/vdCF319PpzX/mn/Nv+Zf86/51/xrfnu0R3u068Jv15PVhn/Dv+Hf8G/4N/wb/g3/hn/Dv+Hf8G/4N/wb/g2/f/AP/sFfF35/PdeF318vdOH319Npy7/l3/Jv+bf8W/4t/5bfHu3RHu268Nv1ZLXj3/Hv+Hf8O/4d/45/x7/j3/Hv+Hf8O/4d/45/x+8f/IN/8NeF31/PdeH31wtd+P31dNrz7/n3/Hv+Pf+ef8+/57dHe7RHuy78dj1ZHfgP/Af+A/+B/8B/4D/wH/gP/Af+A/+B/8B/4D/w+wf/4B/8deH313Nd+P31Qhd+fz2djvxH/iP/kf/If+Q/8h/57dEe7dGuC79dT1Ylf8lf8pf8JX/JX/KX/CV/yV/yl/wlf8lf8pf8/sE/+Ad/Xfj99VwXfn+90IXfX0+nE/+J/8R/4j/xn/hP/Cd+e7RHe7Trwm/Xk1XFX/FX/BV/xV/xV/wVf8Vf8Vf8FX/FX/FX/BW/f/AP/sFfF35/PdeF318vdOH319PpzH/mP/Of+c/8Z/4z/5nfHu3RHu268Nv1ZFXz1/w1f81f89f8NX/NX/PX/DV/zV/z1/w1f83vH/yDf/DXhd9fz3Xh99cLXfj99XS68F/4L/wX/gv/hf/Cf+G3R3u0R7su/HY9WTX8DX/D3/A3/A1/w9/wN/wNf8Pf8Df8DX/D3/D7B//gH/x14ffXc134/fVCF35/PZ2u/Ff+K/+V/8p/5b/yX/nt0R7t0a4Lv11PVi1/y9/yt/wtf8vf8rf8LX/L3/K3/C1/y9/yt/z+wT/4B39d+P31XBd+f73Qhd9fT6cb/43/xn/jv/Hf+G/8N357tEd7tOvCb9eTVcff8Xf8HX/H3/F3/B1/x9/xd/wdf8ff8Xf8Hb9/8A/+wV8Xfn8914XfXy904ffX0+nOf+e/89/57/x3/jv/nd8e7dEe7brw2/Vk1fP3/D1/z9/z9/w9f8/f8/f8PX/P3/P3/D1/z+8f/IN/8NeF31/PdeH31wtd+P31dHrwP/gf/A/+B/+D/8H/4LdHe7RHuy78dj1ZDfwD/8A/8A/8A//AP/AP/AP/wD/wD/wD/8A/8PsH/+Af/HXh99dzXfj99UIXfn89nZ78T/4n/5P/yf/kf/I/+e3RHu3Rrgu/XU9WI//IP/KP/CP/yD/yj/wj/8g/8o/8I//IP/KP/P7BP/gHf134/fVcF35/vdCF319Ppxf/i//F/+J/8b/4X/wvfnu0R3u068Jv15PVzD/zz/wz/8w/88/8M//MP/PP/DP/zD/zz/wzv3/wD/7BXxd+fz3Xhd9fL3Th99fT6c3/5n/zv/nf/G/+N/+b3x7t0R7tuvDb9WS18C/8C//Cv/Av/Av/wr/wL/wL/8K/8C/8C//C7x/8g3/w14XfX8914ffXC134/cPyf6pJa8w='
A0_B64 = 'eNol09GJKzEMheFK0kbepgMjFmOMGSaQ3X1J0sOUkjb0NqWklIH7ee/Dzxkiy5KOlfH5uX5NDrx/rmOnGDeKsVCMC8U4v69fGB+KcVCMN8XYKcaNYiwU40Ixzrv8+6yZ6qUa6f50f35Nzu90b7pTHPt3uss5ulC4y1l63p2/5zjc958cn3n3XX8v+tIfxXjTye77RieL7wudnE85Tzk48MbutxvFWCjGhWKcDzmPa+ddoPMv0HkXE951vgU63wKdb4HOt0DnW6DzLdD5Fuh8C3S+BTrfAp1vMb07HnM+PuF4pdl4hd33jWIsFObjFT2fvHryh04O32862XHD4rcLnZwPOd78/Jsh9Z/6T/2mPjMm3kSPqcfUozPUe+gxK08qPyovKi8qHyoPqvmr2au5q5mreatZqzmrGav5VmdX51ZnVvFVfBVfxddzvi3v0WdvE+/d/979kc7lOuvrWb1UJ9VINfwGPaqRTX9Nf01/TX9Nzaa/pm7TX1O76a+p39Rv6jf1m/pFbpFb5Ba5RW6RW+QWuUVukVvkFrlFbpFb5G7ObuKb2Ca2iW1i2zlneJkF9jXsatjRsKNhP7v9DLsZdrPby5jYy24nA91OBrqdjL+99F+4/NrV3+vKmzo98h+JyfQO43xd/wF46Z2l'
A0P_B64 = 'eNoNVHlUzQkY/b5PQlHSE+MtP1la0bSheotJYizjWCamjmYxjcJMg2NkZKnMUJ4ootcmodIQ5bV5vfcwaGiMsZ3I7/d7qUgmjKaFesu8/++5597v3u/6zMgIbKOi54f0q8Gwb5LeE1xrK1gHvGOvNi9A09uDhpdwqWZEyypcFR+gc4Ic22K+Fcxt+0Q/0VWnQtEeOu4Twv0D0QO/SLpxQ52nYRTaRim0oyEi6Ygkm77oOc+54PwHVwYa0BB4iquDVi8/7gVMztaxJbCxPrg9AwfCq7Qe8KixhhnAeR7+zFckjD0h9qXJs7z4J4CPcmU3KXq8kC+Dj3Id6yPA5Wo+XwveajveGS9Gqs84wU4XeX8hft14gP0bXicwPA+qVKW0kvIv5OpD4fxwfy4Bni+RSj6mlPdDZW9pzcMs6Ut6FepoicWMDcUB1+hJjwPfBTcNIyeyZBs+VZJH27sKDMnwLFJp2YWaTAdZBVUoZ4gy6a8dtlZ81odhEltKeqiVvaehR8ZNa6U5ooDmGHDuH9WzG8OHpNWPh5p+tV4MX3vUiT1o2zHVzEZKj/VR6GhYkL84nqaXhlpve8TDm4miW+rDfDG87n7BtkC1rqzLD22xhi+EFcpKeR1FTnE1X0dVf5VlM2Z5K3WhsOxduLkMv7/QYt6Mw9QhTBztOj1BPJsqGuxMVzBHFSyOpbPbFVoBDJUI+kPwcc9R0Q/0xi59MAV3emmYz8mms9wYjPEdx3RhwGhzeMDUhlSdL5RePMy/hBFu/m8D8azMhm+DTs/mpyq4xB6S1lLMDgFbAfWLcVYrxYQr5TfI0FAp6yO399IChAWDgQYbjPrutPEmHqwdr10BeSv8ZJVU6CASZ1P+tXpLENrMPBXwnrYH2WudQPm9QvIVrRUfVbyioG/SOcSCjgJrauUx+dIWiigJqo+G+zfaFbfpr7XjGAEtU3uarmHFXZHiIc2c6CVOI8P6E+Zb6IYfGyrhaWe5Xgifhcn5CZi1NKPXDzffmMKeA/8uJXcWPvRdMOagSr3fEooxq6b8m4x3E0RyLZUcC1FoSB/s2x6D1UaF40S6e0hgyAWnAZklD5fPzeP2Ax+SyWbCsezJPGGcyzjeBe99OYPZQEmaQ5ZG3OOby7XA2tJsRT0NM+sl31BEZekHd3w+mOfzlML8/E3NeOaqTORNrsI6JoMW7Txv8sN53qgdC8+up3BJ8HbB0Tff4icNcu4AHHiRP1NNHQYBk0hbYl3+3AvvTrla1uAp11TDZfC5ltufib2JGaIR1EbOTDat3JolMmJXj61Vp406Uz8ajD372EQwfHdcvwBqTka1SDEwXGqZixOra433MevTvaYszNoRKHGiJ0NOuzfRyj8uaeeAU2S6rJP2lZ4Ve9LuR4xWCHHue7ndMHR9FTsWp64b23seW5oONvVBUrWfWE5zjqaJc+jZ+hmWbSiM1upGg+DWSfMV5FJS5XcpfiBJMptUNn5MPDlEBg+kYP0sgayHxk11tm6LnNFYM7KscjZvRTftLNF+sjOoLQl4cts564emtbtbXSwN9Gft0eSVZCiCd7PLZDrqCHA2rsOnj4foP4disR2XBveWxtRFQ0yvzCzHhcVFTDdG3K6VrKSGxxorJrn9hMSBFq9zHJyMCYW+lxHmjnBTtFFc03QrW8XP6ZafsFuVzQwn3y1i69Z1F6RaNRTN07FKaLC353+DxnvJlgxUlAGvgagl/pL/cIzHR3Izhf+q4ROhLydEdpumxToMeOOOPzV6J9jSe84Sh9LXedaeLFoTxiXDMqFK9juFxRXwF+HB3hZTGZ7o0LGt0L26SjifnrlP4kvA+6a0Q46/JZZzY3D3FC9mI21SXOdNIHxRohsPTYPPFY/J8YPAuBnPbZpvvo93mn0sGzAlsqpqORyefkB2mUZn5rGFUE1/t32LXKqH1dHxueXyN3THbMf/A4Nh7uxI/PHISekftHDrfA1CXVEa2wn3m0f1zcH/Aad/j7A='
VS_B64 = 'eNoNl3kg1Fsbx8/z1LVT9m1+M1yyZYlrZ0aLNtXbokvUWzflttCl7apc91U32ZJQZImLbBVhjCwzg6tS1KWdmJkWKolWSc3y/v46f51znud8n+/neU7txkRt/iaSaaqWTlmhVcaUoNmFHHKxbBXVk+0Wtxw4/2IJ0znf9BXs5tfYWrXg9lU2DEEwqfHJ9RqiYJ3qaw5nEm+saK3is4jprIy8thAS92HWfMlzcjOMn6KYBxom7CLfJnyepmHTNpsUR3twxZUkNiREg2GPJm0Gs6UPwfx8VKPfG9wzd9pdcRCC0iO6fpQie42Z15MOcvDx6uviUWKQH+HGDyHGeUdKRSpQ+vDlWXEZuZJleIypgII/DzG8qzFnzSEDxQV4nZxQ5f4ddxnpFLaZkYyohFxGKLqORRiK1eGG/r4cyRGibdsULxaSX99UVr7sgW6L2wW+37FBcL1BFgV1gxtOiEvIgovLvYf04O1YrJ2ohaSPFplYD6LZ+XT96VoQbR528GvBkv7QPM4XLDjaVcCk8LMHU49yweRFAm2hDsk9t7+RWo8nLQNnyvKgLs68yrcZZepVJRIlyNN/qUGlYY6T9SW2ELccHNIT6cKE77jWqyNQUSz8UdYJ0mVuqlIxzLtrnSFCKBkZ+tn0LKqd2mJwVYPYn1x4daCXBB4+zuMvJeQffztJA+m/U1Uq3keEp64Z00nrZfsVUbuxO+VY0/ghOBz0nUGHFLpLvdPECQe0W8zl18Ck57Hp+F9wJfqUh0gHtIvP2En6SWW4xFc8QI7auvNFF8j7z8H27JdYmDEjXTIDMtY+86U24peywwayDJhdv81Ndhtu3THI5DuSLM98M0UkfHm1VY/WvfxZ1QwRBRbd3tn2TTgWvz6XOoE5D7rnyk9D08EbPFEVCbp22ZZSQdbhnTxZN/yzmqtGa3vtxSMf1k/42kS/03QE5Lu25gztJ5G6HIaoiYRuYXPEKWToeXkzJQV53/0U8QnSHpNF2G2Y8KfwvCSFzHPad1xymLi+MEhpW07OPO1JZkVjbGxjnmSM/MmpTBVpAG9Pf458AXTvzneR58Hd+mHNV79Dk2V0kcgEcrzYPLp2+Wd3eMgzYPFqQ2fLdzgzfaxadJ/0PY1fdtGBpH7OUWFP4FzehAb9ngnNOrPb5pOq0Q1MWRXsTW1KliSQvB1qbYwTuFgw4TCnCR9NxZSJReSP6251imVgzVkyS9YPKrf60ph5uGMKveXnQD0iM5G3gFx/EcCl1uIKTfsGphpylRKb+UaksfN8qTQMlK722iuq4Nfgzih+AJHsVPIwGYW/lu6jmLkYfLA8b847TPN3s+PUomOSmfl0IsSLzez5oaT9vn0ruwPrY5Ycn/MRmaLgNlkkOB41bBDzyYLJh3p0SGE/xZ1hrMO9I18KRCdJgJ1SieUEzo/JzKP9IFVNzpVVA68+Rdn0GUT3clMYZ1Ga5PTsyWVycORrje9tnN7ukc+Mxs/+V1Xcb2NMSkImQwMNBJfVFIdA2CLxVdSCypPOmvFT8AMHjOSZQD5NJbKi8JndBXXLdozKPP+CroK6yWsmTpM4Gs9VlyA0m89M8ONi4fo1xyTxpOHzrmrJPWKmbsCR3YX11Uey5D2w1u0NSxYDGr3LCxhz0ZWrouM3jXpn958YDQLTHeOW7Dqc3nqW8n2PWy8Husv74VsHI18xAAdU1xlOHgFVsYmufijqBarNc3yGvJqvFYN3yOPeyZPSQTDJuq2suARXkpXqGH7YNmev75AOlFGidOoTjIwrtDzu4ptrq7UEocS9cYYmFY8XbHSL6RyoJ9Oq1DlUt2F7mb6Alpsmlm8jYUtvV5JbCT76j5eFaB/JFHzj0JVV1BeYyXoPrbtX+gz0kN2mlbMlB0gNK+CkYCMx1TVM01fGlRGzaiw7cOJm4Fy/Pny1LS6vLYAY13QJWJFYJ+pUlYfDDwlRcxrtyEQTL58mUZfyfVvqAwi6bmYM/U48Ly66IjaBJ0p+PyqiYX/LyCxRA7kri3AQXySCh4xjskuQvfXGJeooBklPZzK+gcfG6mRqK9pWz2rxe4Sft3znDy+E11WQyojA66tPs8WlRL71hM+rFcDB+Y1DRhDgxtMW9ZEJm5pU6T9QcX97ue8N/NNFWY/Bwb/+F5UmMYbNmw6kKWpgU9OEIRWKxdJHSZqIsw12zRE4kuavMdbMApwd2l0ndwcrB28uP4jUrbmdSx8W32t0WhEOv14ZoCR9pCv9SCPDActVd+rJesGnK0lL2gmeWhdOs9bjhqxhfaoQ4+7u82O349e9Pg3sZqxjz7FlRqHGvBFGxVIy72zESTpOxYcgL6ElCb/E8pbUk1hNboqeClreMXF8dJwEudS3NM8ihaFOljW25IvTdgGVidJDj7P4liTYYN+ZskDiM3bAyW8cV8dO81lOqLS4r5DThPovlQSK7XA/1plLzcDXxu12sm3QvlBhoXgC25NcimlYDdZl60kPQH7em8LhHkgtvZgvdCTX7+qry/+FTg+nmZxWDD9skUqp4lQIN5/ep1bxsdD1Ew4IdmpSO7HXdK7rcCxoXOrX5f9MbvRmOst9YO3AizPiFyRov2mWVz/6/TZdI5xPsvc/dZI/gePc2SJbHm5f0GkvaSXs8Hccq25UNSg9yl9HyoWZleP54BDVo8LKwAfzOq/07iHNOQlOMn+46GKQXraIfNOyLzZ+Aauox6rMX3CrkR7SfToOtBpcv2J9xRInUQ0xT+TF08BtvHqELe2DhwvmuljVY5JtZLnfTbx/otzuqhEZeilvYajhWtZRJ9+P+PZM7kIWB612ubvQLg4WL68oW0HWXwvSpVnAWKqpLUolbzSN69idKP53kZ7kK1HNsC1hpqD21FzdRiC2Fs58gSmJu/pbl6wY5j926+AHk8g4xQk2F68ydhWxu1GncaBCPh/8Y3KLxMpg/9HyOMsOqXDdUnETWdaVVUn5YIooxIAyx50hVSWiBJKZlZAsEhMb4fPzbz0hYziPTQWhO2uQIZkFXKXjBeLnpODoYp6VAvMfJFvJ2+HvuKcOn3OhcSYv1f0bbr7yvcjtIu63qzIW/0mCYzqt5EGw6n7FApEp3Btz1RHFkqRfTySy3+PK5ekXh1JI9qiS9RCPFL/l5skXgrvOG4bYAB7e0m6UHCNbGgIplga2LrfLUORAyJY/mlmhqL37aQ6nBaselhlbybB7sJkwc1D4wkNbWgSao47GoufkfVVLPusTLMi7pk9D58hP3NnsWxit5V8uNCGPOwxK6SfILvItpceRTzdXJgtmE+XSASUhi0Qq5za3bSAmLDeQqMPvzmtdqDBkq1jrfE+AqcGeFvF90jujMku6DcJe5xYJgsjbu23nWLHoueiBkeQuuSeUXmLsRM3yqktSVxhtesf2q8fStvBGeQCcfBBx3K8by1QcnD3e4wfL7w4yd5jqLs1nHEOXR7kX6aX2Wb+BNALCDjQ0i58QSytWPec1rgwfFzYGkIPPC9slRvCSSjSU6EJK3NE2gTl5G3Y5d6CDLMuMPyULg9+bQ7JFfGL1vLBJVgmemV1pPEcS3LmpmmWDrQNtJ6uVyZPEK8dkpaATEZBhALirz/M45wZe+ONxvOBHklgfJm5dQtZoHj7O+ATk83LuhWBy7kCe0uQNUD7/yU9oR3Z6nmtgZKPZjnmqsl1QNl+fw7DCmCkdB99nqP7uTjYjGd3DwqppSjFb9ytPJkKES5/JcAZ4mauclv0CujYsl2ptcntvms+QCXTN+DqTPYmHdDU96aFmYulSKw4fR96rtckyoYcXOYvTjgHhOg76Zngu/qAjLbjNx/neomiiFrO3hlbzSEJlh9wTvBKnNOV+8DVudwWNQ5+CbmO1MVB7YuSt6Iba0k1+dH0q7TlzTPYHxHesaJCuB7HZaEKrMnkpeVpNX2Qx5aoqvQ6NWSrWskdw2MloWJJGNA09LygqYKlqoK20HQxX2V+W3gP35dmZsp3g+TBLTcyAYVuVSkUZTFU11vn9g9E7HqswP0Dg15UsxjmExopLHmI0Xp3TquiBzQ/WarbZkJjqw1r0gDXVkac+shK402sYrCTEf6UqMm/4e8NgnricqEy5zZzKgptzWwltw/+qdzoP1ZJXOYnzaQNFRq966MlH5ar0mXSn7My+USJYQrbcXDdnTgv+4m9oL2CSx++sLaXFcOU0r1ZgRGrTrDIpD8TfEj3kZ+Dsmf40/mayOymEL9aDdp8HCYxcLHLi6HFodEVV2LBbcL/zzwspgkveBagptsJq5S8U/R1YHOIxPLkEvNcl/S29Df9NkOUrBuEj9wdzpj1anQ+qlz6AOVljNePLwVR3/U9tFmS12NrVVYjMiMslkmSyZDfjEj2eR6cG+DPn4laPbWeEa0jlWuS1mRPrluFEsRYoBfxgwf8PWZL7zlfUTzbXziqRZJPNZFCbbny5106yaIxGbjTfW+tPXr1+M6K4B0sFfW7MbzDyPtCZmoeH947xhJ7k9KuFfFESGek+dHYwimwf9iphf0Hzop9V5c7gGbVnCbUNlXU9suzvIHfNppESQ1Lywc+SpY8rxSk28kK4/8j/2NR2sCjvsBpSgYr/VZjLhbAzaZ8r7b//A6XKB2E='
SFS_B64 = 'eNoL2JtgxiSl/f+EjnTGcofp6ne1fxul3nGbrXnowanH+cGMxbIKwSJiHFOdrISP7n5m9IvP+p/AXzYfD+k/LvqG5yQf5P9+EZwTGbwte+b02Oit9cdW2kbu5V+r4dwr/5on6mLPoikvF5Yv8Oi7tDtVfj4B/bXRe+0PAfXPXbpf062X+zGq/tz42RGymdusOxftP+sjbbX0UAHXts95N23s/NW3f8uQ5YmIvrYnOCfqQkEgm9ShgD0bDFYs/edwQNm1N8H1WqWN8ZyZniujYpneF+f3Mapq5pxQd4lzyVv3cBdXr0YhNrcS0P9C3UfOAah/1oL5miXY3BpQm7ktOcx+/9kAaQul7RPSKybwHY8oXDCtT3Sz4LyOaRtFrm64aiomaVR7niVXoMxh+dtNNnNO9G1ii+v/+/bhnqKHlhtvZU79tjjQUV/d9/uXNDe3py57uTo1irG5lYD+3O9/1JyA+ucumK1ZhtWtexO3lT23sz8RYL1qqrqVlpiC/IMIdp3LM3krKj/qZj0RO1g10fxX0M4W52fyec8OvZEKn8CVxMRnZb8t6LeD44LHP755Kv7yYHu/1e3yrM+BfkdMQ1yt+Ts5GLG5lYD+XZ8j+Q4A9Usvnc3Jgs2tAClfS+E='

def _dec(s): return zlib.decompress(base64.b64decode(s))
EMB = {}
def emb():
    if not EMB:
        EMB['A2'] = list(struct.unpack('<768I', _dec(A2_B64)))
        EMB['A0'] = list(struct.unpack('<256I', _dec(A0_B64)))
        b = _dec(A0P_B64); EMB['A0P'] = [struct.unpack_from('<IH', b, 6 * k) for k in range(256)]
        b = _dec(VS_B64); EMB['VS'] = [struct.unpack_from('<BIH', b, 7 * k) for k in range(len(b) // 7)]
        b = _dec(SFS_B64); EMB['SFS'] = [struct.unpack_from('<43I', b, 172 * k) for k in range(len(b) // 172)]
    return EMB

def variant(a0, a1, a2):
    """Dense part with A0..A2 replaced (rows 0..6 carry no difference): per member (A[0..15], E[4..15],
    W[8..15]); E4..E6 and W8..W10 recomputed; and c7 (W7x = c7 - A_{-1})."""
    out = []
    for (A_, E_, W_) in (TX, TY):
        A = {i: A_[i] for i in range(16)}; A[0], A[1], A[2] = a0, a1, a2
        E = {i: E_[i] for i in range(4, 16)}
        for i in (4, 5, 6): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        W = {i: W_[i] for i in range(8, 16)}
        for i in (8, 9, 10): W[i] = (E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M
        out.append((A, E, W))
    (A, E, _), _ = out
    c7 = (E[7] - 2 * A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0]) - S1(E[6]) - CH(E[6], E[5], E[4]) - K[7]) & M
    return out, c7

def valid(var):
    """Validity: E cells of rows 4..8 ('+' pairs included) and unchanged dW_i, ds0(W_i) for i = 8..11."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = var
    for i in range(4, 9):
        m, v, d, _ = CELL['E'][i]
        if Ex[i] & m != v or Ex[i] ^ Ey[i] != d or (PLUS[i] and (Ex[i] ^ Ex[i-1]) & PLUS[i]): return False
    return all(((Wx[i] - Wy[i]) & M, (s0(Wx[i]) - s0(Wy[i])) & M) == DIFF[i] for i in (8, 9, 10, 11))

def words(cv, A, E):
    """Step-2 equations: W0..W7 connecting cv to the variant's A0..A7, E4..E7."""
    A = dict(A); E = dict(E)
    for j in range(4): A[-1-j] = cv[j]; E[-1-j] = cv[4+j]
    for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
    return [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(8)]

def pair(cv, var):
    (Ax, Ex, Wx), (Ay, Ey, Wy) = var
    return words(cv, Ax, Ex) + [Wx[i] for i in range(8, 16)], words(cv, Ay, Ey) + [Wy[i] for i in range(8, 16)]

def yz0(cv, a0):
    """Y = W1 - A1 and Z0 = W0 + s1(W14) for chaining value cv and A0 (independent of A1, A2)."""
    a, b, c, d, e, f, g, h = cv
    hh = (d - S0(a) - MAJ(a, b, c)) & M; e0 = (a0 + hh) & M
    Y = (-S0(a0) - MAJ(a0, a, b) - g - S1(e0) - CH(e0, e, f) - K[1]) & M
    W0 = (a0 + hh - d - h - S1(e) - CH(e, f, g) - K[0]) & M
    return Y, (W0 + s1(TX[2][14])) & M

def c9x(a2):
    e6 = (TX[0][6] + a2 - S0(TX[0][5]) - MAJ(TX[0][5], TX[0][4], TX[0][3])) & M
    A, E = TX[0], TX[1]
    return (E[9] - 2 * A[5] + S0(A[4]) + MAJ(A[4], A[3], a2) - S1(E[8]) - CH(E[8], E[7], e6) - K[9]) & M

def outcome(cv, a0, a1, a2):
    """Reference outcome of variant (a0, a1, a2) on cv: (row-16 holds, W7 in F7, deepest row reached >= 16)."""
    var, c7 = variant(a0, a1, a2); wx, wy = pair(cv, var); tx = trace(cv, wx); ty = trace(cv, wy)
    r16 = rowok(tx, ty, 16); deep = 15
    for i in range(16, R):
        if not rowok(tx, ty, i): break
        deep = i
    return r16, inF7(wx[7]), deep, (tx, ty, wx, wy)

# ---------------------------------------------------------------------------------------------------------------
# The counted online program.  Machine: 256-bit words, unbounded memory, registers named by the assembler (the
# self-test checks that at most 64 distinct registers are used).  Cost 1 per executed add, sub, and, or, xor,
# shl, shr, ld/st (register or direct address), rand, jmp; 2 per conditional branch (compare + branch); f38 (one
# target compression) costs 1 unit; immediates and shift amounts are instruction fields.  Values are 32-bit
# words held in 256-bit registers; arithmetic is mod 2^256 and masked with M before any rotation, comparison or
# address use (bits above 31 never reach a used low bit: additions and subtractions carry upward only).
REG = {}   # region bases
for k, nm in enumerate(('HDR', 'ENT', 'F7', 'A2T', 'GT', 'SCR'), 1): REG[nm] = k << 200

class Asm:
    def __init__(s): s.c = []; s.lab = {}; s.n = 0
    def __call__(s, *ins): s.c.append(ins)
    def L(s, nm): s.lab[nm] = len(s.c)
    def new(s, p='L'): s.n += 1; return '%s%d' % (p, s.n)

def rot32(a, d, x, n1, n2, n3, shr3=False, t1='t1', t2='t2', D='D'):
    """d = ROTR(x,n1) ^ ROTR(x,n2) ^ (SHR(x,n3) if shr3 else ROTR(x,n3)) in the low 32 bits (garbage above);
    x must be masked.  5 + 2 operations (doubled word D = x | x << 32)."""
    a('shl', D, x, 32); a('or', D, D, x)
    a('shr', t1, D, n1); a('shr', t2, D, n2); a('xor', t1, t1, t2)
    a('shr', t2, x if shr3 else D, n3); a('xor', d, t1, t2)

def gen_prologue(a):
    """Group prologue: two random words -> M0, CV1 = F(IV, M0), per-CV values."""
    a('rand', 'r0'); a('rand', 'r1')
    for k in range(16):
        r = 'r0' if k < 8 else 'r1'; s_ = 32 * (k % 8)
        if s_: a('shr', 'm%d' % k, r, s_); a('and', 'm%d' % k, 'm%d' % k, M)
        else: a('and', 'm%d' % k, r, M)
    a('f38', ['m%d' % k for k in range(16)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    rot32(a, 'S0a', 'a', 2, 13, 22)
    a('and', 't1', 'a', 'b'); a('or', 't2', 'a', 'b'); a('and', 't2', 't2', 'c'); a('or', 't1', 't1', 't2')
    a('sub', 'hh', 'd', 'S0a'); a('sub', 'hh', 'hh', 't1')
    rot32(a, 'S1e', 'e', 6, 11, 25)
    a('xor', 't1', 'f', 'g'); a('and', 't1', 't1', 'e'); a('xor', 't1', 't1', 'g')
    a('sub', 'y0p', 'hh', 'd'); a('sub', 'y0p', 'y0p', 'h'); a('sub', 'y0p', 'y0p', 'S1e'); a('sub', 'y0p', 'y0p', 't1')
    a('add', 'y0p', 'y0p', (s1(TX[2][14]) - K[0]) & M)
    a('xor', 'abx', 'a', 'b'); a('and', 'aba', 'a', 'b'); a('xor', 'efx', 'e', 'f'); a('add', 'gk', 'g', K[1])

def gen_block(a, j, a0, rare):
    """Per-A0 block: Y, Z0, header, entry loop with the W7 test.  The row-17 and deep paths of this A0 are
    emitted out of line (into `rare`, placed after the last block) so the loop falls through to the next block."""
    nxt, loop, back, r17 = a.new('next'), a.new('loop'), a.new('back'), a.new('r17')
    a('add', 'E0', 'hh', a0); a('and', 'E0', 'E0', M)
    rot32(a, 'S1', 'E0', 6, 11, 25)
    a('and', 'Ch', 'E0', 'efx'); a('xor', 'Ch', 'Ch', 'f')
    a('and', 'Mj', 'abx', a0); a('xor', 'Mj', 'Mj', 'aba')
    a('rsub', 'Y', (-S0(a0)) & M, 'Mj'); a('sub', 'Y', 'Y', 'S1'); a('sub', 'Y', 'Y', 'Ch'); a('sub', 'Y', 'Y', 'gk')
    a('and', 'Y', 'Y', M)
    a('add', 'Z0', 'y0p', a0); a('and', 'Z0', 'Z0', M)
    a('shl', 'I', 'Y', 32); a('or', 'I', 'I', 'Z0'); a('add', 'I', 'I', REG['HDR'] | (j << 64)); a('ld', 'H', 'I')
    a('and', 'CNT', 'H', (1 << 20) - 1); a('shr', 'OFF', 'H', 20); a('add', 'NE', 'NE', 'CNT'); a('bz', 'CNT', nxt)
    a('add', 'END', 'OFF', 'CNT')
    a.L(loop)
    a('ld', 'EN', 'OFF'); a('sub', 'W7', 'EN', 'a'); a('and', 'W7', 'W7', M)
    a('add', 'W7', 'W7', REG['F7']); a('ld', 'FL', 'W7'); a('bnz', 'FL', r17)
    a.L(back)
    a('add', 'OFF', 'OFF', 1); a('bne', 'OFF', 'END', loop)
    a.L(nxt)
    rare.append((j, a0, r17, back))

def gen_rare(a, j, a0, r17, back):
    a.L(r17); a('add', 'NW', 'NW', 1); gen_row17(a, j, a0, back)

def gen_row17(a, j, a0, back):
    deep = a.new('deep')
    a('shr', 'A1', 'EN', 32); a('and', 'A1', 'A1', M)
    a('add', 'W1', 'Y', 'A1'); a('and', 'W1', 'W1', M)
    a('add', 'E1', 'A1', 'c'); a('sub', 'E1', 'E1', 'Mj'); a('add', 'E1', 'E1', (-S0(a0)) & M); a('and', 'E1', 'E1', M)
    rot32(a, 'S1E1', 'E1', 6, 11, 25)
    a('xor', 't1', 'E0', 'e'); a('and', 't1', 't1', 'E1'); a('xor', 'ChE1', 't1', 'e')
    a('shr', 'S0A1', 'EN', 80); a('and', 'S0A1', 'S0A1', M)
    a('xor', 't1', 'a', a0); a('and', 't1', 't1', 'A1'); a('and', 't2', 'a', a0); a('xor', 'MjA1', 't1', 't2')
    a('shr', 'P2', 'EN', 64); a('and', 'P2', 'P2', 1023); a('shl', 'P2', 'P2', 2); a('add', 'P2', 'P2', REG['A2T'])
    a('ld', 'A2r', 'P2'); a('and', 'A2', 'A2r', M)
    a('add', 'E2', 'A2', 'b'); a('sub', 'E2', 'E2', 'S0A1'); a('sub', 'E2', 'E2', 'MjA1')
    a('sub', 'W2', 'E2', 'b'); a('sub', 'W2', 'W2', 'f'); a('sub', 'W2', 'W2', 'S1E1'); a('sub', 'W2', 'W2', 'ChE1')
    a('add', 'W2', 'W2', (-K[2]) & M); a('and', 'W2', 'W2', M)
    rot32(a, 's0W2', 'W2', 7, 18, 3, shr3=True)
    a('shr', 'K10', 'A2r', 32); a('and', 'K10', 'K10', M)
    a('add', 'W17', 's0W2', 'K10'); a('add', 'W17', 'W17', 'W1'); a('and', 'W17', 'W17', M)
    a('obs', 'W17')
    a('shr', 'PG', 'EN', 74); a('and', 'PG', 'PG', 31); a('shl', 'PG', 'PG', 4); a('add', 'PG', 'PG', REG['GT'])
    a('ld', 't1', 'PG'); a('add', 'E17', 'W17', 't1'); a('and', 'E17', 'E17', M)
    a('add', 'P3', 'PG', 1); a('ld', 't1', 'P3'); a('add', 'P3', 'PG', 2); a('ld', 't2', 'P3')
    a('and', 't1', 'E17', 't1'); a('bne', 't1', 't2', back)
    a('add', 'N1', 'N1', 1)
    a('add', 'P3', 'PG', 3); a('ld', 't1', 'P3'); a('add', 'A17', 'E17', 't1'); a('and', 'A17', 'A17', M)
    a('add', 'P3', 'PG', 4); a('ld', 't1', 'P3'); a('add', 'P3', 'PG', 5); a('ld', 't2', 'P3')
    a('and', 't1', 'A17', 't1'); a('bne', 't1', 't2', back)
    a('shr', 't1', 'A17', 11); a('xor', 't1', 't1', 'A17'); a('and', 't1', 't1', 0x200)
    a('shr', 't2', 'A17', 12); a('xor', 't2', 't2', 'A17'); a('and', 't2', 't2', 0x40); a('or', 't1', 't1', 't2')
    a('shr', 't2', 'A17', 9); a('xor', 't2', 't2', 'A17'); a('and', 't2', 't2', 0x100); a('or', 't1', 't1', 't2')
    a('bnz', 't1', back)
    a('jmp', deep)
    a.L(deep); gen_deep(a, j, a0, back)

def gen_deep(a, j, a0, back):
    """Rows 18..37 of both members (member y's row 17 follows from member x's: proof.md 4.6).  All words go
    through scratch memory (direct addresses); every cell, XOR difference, '+' pair and two-bit condition."""
    sx = lambda m, k, i: REG['SCR'] + 256 * m + 64 * k + i + 8      # m member, k 0:A 1:E 2:W, i row (-8..)
    def st(r, m, k, i): a('sti', sx(m, k, i), r)
    def ld(r, m, k, i): a('ldi', r, sx(m, k, i))
    A0r = TX[0]
    # remaining second-block words: E2 masked, E3, W3, E4, W4, E5, W5, E6, W6, W7 (x, y)
    a('and', 'E2', 'E2', M)
    a('shr', 'S0A2', 'A2r', 64); a('and', 'S0A2', 'S0A2', M)
    a('xor', 't1', 'A1', a0); a('and', 't1', 't1', 'A2'); a('and', 't2', 'A1', a0); a('xor', 't1', 't1', 't2')
    a('add', 'E3', 'a', A0r[3]); a('sub', 'E3', 'E3', 'S0A2'); a('sub', 'E3', 'E3', 't1'); a('and', 'E3', 'E3', M)
    def wstep(dst, Ei, Ai4, Ei4, Em1, Em2, Em3, k):
        rot32(a, 'S1t', Em1, 6, 11, 25)
        a('xor', 't3', Em2, Em3); a('and', 't3', 't3', Em1); a('xor', 't3', 't3', Em3)
        a('sub', dst, Ei, Ai4); a('sub', dst, dst, Ei4); a('sub', dst, dst, 'S1t'); a('sub', dst, dst, 't3')
        a('add', dst, dst, (-K[k]) & M); a('and', dst, dst, M)
    wstep('W3', 'E3', 'a', 'e', 'E2', 'E1', 'E0', 3)
    a('xor', 't1', 'A1', A0r[3]); a('and', 't1', 't1', 'A2'); a('and', 't2', 'A1', A0r[3]); a('xor', 't1', 't1', 't2')
    a('rsub', 'E4', (A0r[4] + a0 - S0(A0r[3])) & M, 't1'); a('and', 'E4', 'E4', M)
    wstep('W4', 'E4', a0, 'E0', 'E3', 'E2', 'E1', 4)
    a('shr', 'E5', 'A2r', 128); a('and', 'E5', 'E5', M); a('add', 'E5', 'E5', 'A1'); a('and', 'E5', 'E5', M)
    wstep('W5', 'E5', 'A1', 'E1', 'E4', 'E3', 'E2', 5)
    a('shr', 'E6', 'A2r', 96); a('and', 'E6', 'E6', M)
    wstep('W6', 'E6', 'A2', 'E2', 'E5', 'E4', 'E3', 6)
    a('sub', 'W7', 'EN', 'a'); a('and', 'W7', 'W7', M)
    # message words of both members into scratch: W2..W17 (x, y)
    for i, r in ((2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6')):
        st(r, 0, 2, i); st(r, 1, 2, i)
    st('W7', 0, 2, 7); a('add', 't1', 'W7', D7); a('and', 't1', 't1', M); st('t1', 1, 2, 7)
    for m in (0, 1):   # W8 = E8 - A4 - E4 - S1(E7) - CH(E7, E6, E5) - K8 (E7, E8 per member)
        At, Et = (TX, TY)[m][0], (TX, TY)[m][1]
        a('xor', 't3', 'E6', 'E5'); a('and', 't3', 't3', Et[7]); a('xor', 't3', 't3', 'E5')
        a('rsub', 't1', (Et[8] - At[4] - S1(Et[7]) - K[8]) & M, 'E4'); a('sub', 't1', 't1', 't3'); a('and', 't1', 't1', M)
        st('t1', m, 2, 8)
    a('add', 'P3', 'P2', 1); a('ld', 'A2r2', 'P3')       # record word 1: c9x | c9y<<32 | W10x<<64 | W10y<<96
    for m in (0, 1):
        a('shr', 't1', 'A2r2', 32 * m); a('and', 't1', 't1', M); a('sub', 't1', 't1', 'A1'); a('and', 't1', 't1', M); st('t1', m, 2, 9)
        a('shr', 't1', 'A2r2', 64 + 32 * m); a('and', 't1', 't1', M); st('t1', m, 2, 10)
        for i in range(11, 16): a('sti', sx(m, 2, i), (TX, TY)[m][2][i])
    a('add', 'P3', 'PG', 6); a('ld', 't1', 'P3'); st('t1', 0, 2, 16); a('sub', 't1', 't1', DW16); a('and', 't1', 't1', M); st('t1', 1, 2, 16)
    st('W17', 0, 2, 17); st('W17', 1, 2, 17)
    # states rows 13..17
    for m in (0, 1):
        for i in (13, 14, 15):
            for k in (0, 1): a('sti', sx(m, k, i), (TX, TY)[m][k][i])
        for k in (0, 1):
            a('add', 'P3', 'PG', 7 + 2 * m + k); a('ld', 't1', 'P3'); st('t1', m, k, 16)
    st('A17', 0, 0, 17); st('E17', 0, 1, 17); st('E17', 1, 1, 17)
    a('sub', 't1', 'A17', DW16); a('and', 't1', 't1', M); st('t1', 1, 0, 17)
    # rows 18..37
    for i in range(18, R):
        for m in (0, 1):
            ld('u1', m, 2, i - 2); ld('u2', m, 2, i - 7); ld('u3', m, 2, i - 15); ld('u4', m, 2, i - 16)
            rot32(a, 'v1', 'u1', 17, 19, 10, shr3=True); rot32(a, 'v2', 'u3', 7, 18, 3, shr3=True)
            a('add', 'u2', 'u2', 'v1'); a('add', 'u2', 'u2', 'v2'); a('add', 'u2', 'u2', 'u4'); a('and', 'wi', 'u2', M)
            st('wi', m, 2, i)
            ld('e1', m, 1, i - 1); ld('e2', m, 1, i - 2); ld('e3', m, 1, i - 3); ld('e4', m, 1, i - 4); ld('a4', m, 0, i - 4)
            rot32(a, 'v1', 'e1', 6, 11, 25)
            a('xor', 't3', 'e2', 'e3'); a('and', 't3', 't3', 'e1'); a('xor', 't3', 't3', 'e3')
            a('add', 'ei', 'a4', 'e4'); a('add', 'ei', 'ei', 'v1'); a('add', 'ei', 'ei', 't3'); a('add', 'ei', 'ei', 'wi')
            a('add', 'ei', 'ei', K[i]); a('and', 'ei', 'ei', M); st('ei', m, 1, i)
            ld('b1', m, 0, i - 1); ld('b2', m, 0, i - 2); ld('b3', m, 0, i - 3)
            rot32(a, 'v1', 'b1', 2, 13, 22)
            a('and', 't3', 'b1', 'b2'); a('or', 't4', 'b1', 'b2'); a('and', 't4', 't4', 'b3'); a('or', 't3', 't3', 't4')
            a('sub', 'ai', 'ei', 'a4'); a('add', 'ai', 'ai', 'v1'); a('add', 'ai', 'ai', 't3'); a('and', 'ai', 'ai', M)
            st('ai', m, 0, i)
            if m == 0: ld('xa', 0, 0, i); ld('xe', 0, 1, i); ld('xw', 0, 2, i)
        # checks of row i: x-values, XOR differences, '+', two-bit (member x)
        for k, xr, yr in ((0, 'xa', 'ai'), (1, 'xe', 'ei'), (2, 'xw', 'wi')):
            m_, v_, d_, _ = CELL['AEW'[k]][i]
            if m_: a('and', 't1', xr, m_); a('bne', 't1', v_, back)
            a('xor', 't1', xr, yr); a('bne', 't1', d_, back)
        if PLUS[i]: ld('t2', 0, 1, i - 1); a('xor', 't1', 'xe', 't2'); a('and', 't1', 't1', PLUS[i]); a('bnz', 't1', back)
        for k1, i1, b1, ne, k2, i2, b2 in XROW.get(i, ()):
            ld('t1', 0, 'AEW'.index(k1), i1); ld('t2', 0, 'AEW'.index(k2), i2)
            a('shr', 't1', 't1', b1); a('shr', 't2', 't2', b2); a('xor', 't1', 't1', 't2'); a('and', 't1', 't1', 1)
            a('bne', 't1', ne, back)
    a('succ', j, 'EN')

class Machine:
    """Interpreter for the counted program.  mem: region handlers; ops counted per executed instruction."""
    def __init__(s, randwords, bucket, cvforce=None):
        s.rw = list(randwords); s.bucket = bucket; s.cvforce = cvforce; s.r = {}; s.ops = 0; s.units = 0
        s.mem = {}; s.ent = {}; s.nent = 0; s.succ = None; s.cv = None; s.m0 = None; s.trace = []; s.obs = []
    def load(s, addr):
        reg, off = addr >> 200, addr & ((1 << 200) - 1)
        if reg == 1:
            j, idx = off >> 64, off & ((1 << 64) - 1); es = s.bucket(j, idx >> 32, idx & M)
            base = REG['ENT'] + s.nent
            for k, e in enumerate(es): s.ent[base + k] = e
            s.nent += len(es) + 1; s.trace.append((j, idx >> 32, idx & M, len(es)))
            return (base << 20) | len(es)
        if reg == 2: return s.ent[addr]
        if reg == 3: return 1 if inF7(off) else 0
        if reg == 4: return A2REC[off >> 2][off & 3]
        if reg == 5: return GREC[off >> 4][off & 15]
        return s.mem.get(addr, 0)
    def store(s, addr, val): s.mem[addr] = val
    def run(s, code):
        c, lab, r = code.c, code.lab, s.r; pc = 0; n = len(c); W = (1 << 256) - 1
        def v(x): return x if isinstance(x, int) else r.get(x, 0)   # registers start at zero
        while pc < n:
            ins = c[pc]; op = ins[0]; pc += 1
            if op == 'add': r[ins[1]] = (v(ins[2]) + v(ins[3])) & W; s.ops += 1
            elif op == 'sub': r[ins[1]] = (v(ins[2]) - v(ins[3])) & W; s.ops += 1
            elif op == 'rsub': r[ins[1]] = (ins[2] - v(ins[3])) & W; s.ops += 1
            elif op == 'and': r[ins[1]] = v(ins[2]) & v(ins[3]); s.ops += 1
            elif op == 'or': r[ins[1]] = v(ins[2]) | v(ins[3]); s.ops += 1
            elif op == 'xor': r[ins[1]] = v(ins[2]) ^ v(ins[3]); s.ops += 1
            elif op == 'shl': r[ins[1]] = (v(ins[2]) << ins[3]) & W; s.ops += 1
            elif op == 'shr': r[ins[1]] = v(ins[2]) >> ins[3]; s.ops += 1
            elif op == 'ld': r[ins[1]] = s.load(v(ins[2])); s.ops += 1
            elif op == 'ldi': r[ins[1]] = s.mem.get(ins[2], 0); s.ops += 1
            elif op == 'sti': s.mem[ins[1]] = v(ins[2]); s.ops += 1
            elif op == 'st': s.store(v(ins[1]), v(ins[2])); s.ops += 1
            elif op == 'bz': s.ops += 2; pc = lab[ins[2]] if v(ins[1]) == 0 else pc
            elif op == 'bnz': s.ops += 2; pc = lab[ins[2]] if v(ins[1]) != 0 else pc
            elif op == 'bne': s.ops += 2; pc = lab[ins[3]] if v(ins[1]) != v(ins[2]) else pc
            elif op == 'jmp': s.ops += 1; pc = lab[ins[1]]
            elif op == 'rand': r[ins[1]] = s.rw.pop(0); s.ops += 1
            elif op == 'f38':
                s.units += 1; s.m0 = [r[x] for x in ins[1]]
                cv = s.cvforce if s.cvforce is not None else compress(IV, s.m0); s.cv = cv
                for x, y in zip(ins[2], cv): r[x] = y
            elif op == 'succ': s.succ = (ins[1], v(ins[2])); return
            elif op == 'halt_ok': return
            elif op == 'obs': s.obs.append(v(ins[1]))
            else: raise ValueError(op)

A2REC = []; GREC = []
def tables():
    """A2 records (4 words) and G records (16 words), as stored by the preprocessing."""
    if A2REC: return
    A, E = TX[0], TX[1]
    for a2 in emb()['A2']:
        e6 = (A[6] + a2 - S0(A[5]) - MAJ(A[5], A[4], A[3])) & M
        e5b = (A[5] - S0(A[4]) - MAJ(A[4], A[3], a2)) & M
        var, _ = variant(A[0], A[1], a2); (_, _, Wx), (_, _, Wy) = var
        w0 = a2 | ((Wx[10] + s1(TX[2][15])) & M) << 32 | S0(a2) << 64 | e6 << 96 | e5b << 128
        cx = c9x(a2); cy = (cx - DIFF[9][0]) & M
        A2REC.append((w0, cx | cy << 32 | Wx[10] << 64 | Wy[10] << 96, 0, 0))
    for g in G:
        rec = []
        for m, (A_, E_, W_) in enumerate((TX, TY)):
            w16 = g if m == 0 else (g - DW16) & M
            e16 = (A_[12] + E_[12] + S1(E_[15]) + CH(E_[15], E_[14], E_[13]) + K[16] + w16) & M
            a16 = (e16 - A_[12] + S0(A_[15]) + MAJ(A_[15], A_[14], A_[13])) & M
            rec.append((e16, a16, (A_[13] + E_[13] + S1(e16) + CH(e16, E_[15], E_[14]) + K[17]) & M,
                        (-A_[13] + S0(a16) + MAJ(a16, A_[15], A_[14])) & M))
        (e16, a16, c17, a17), (e16y, a16y, _, _) = rec
        mE, vE, _, _ = CELL['E'][17]; mA, vA, _, _ = CELL['A'][17]
        for k1, i1, b1, ne, k2, i2, b2 in XROW[17]:          # conditions against row 16 fold into masks
            if i1 == 16:
                bit = ((e16 if k1 == 'E' else a16) >> b1 & 1) ^ ne
                if k2 == 'E': mE |= 1 << b2; vE |= bit << b2
                else: mA |= 1 << b2; vA |= bit << b2
        p = PLUS[17]; mE |= p; vE |= e16 & p
        GREC.append((c17, mE, vE, a17, mA, vA, g, a16, e16, a16y, e16y, 0, 0, 0, 0, 0))

def entry(cv, j, a1, a2i):
    """Table entry word for variant (A0_j, a1, A2_{a2i}) in the bucket of cv (g index from W16)."""
    a0 = emb()['A0'][j]; var, c7 = variant(a0, a1, emb()['A2'][a2i]); wx, _ = pair(cv, var)
    w16 = (s1(wx[14]) + wx[9] + s0(wx[1]) + wx[0]) & M
    gi = G.index(w16) if w16 in G else 0
    return c7 | a1 << 32 | a2i << 64 | gi << 74 | S0(a1) << 80

def _du(ins):
    """(defs, uses) of an instruction (register names only)."""
    op = ins[0]; S = lambda x: [x] if isinstance(x, str) else []
    if op in ('add', 'sub', 'and', 'or', 'xor'): return [ins[1]], S(ins[2]) + S(ins[3])
    if op == 'rsub': return [ins[1]], [ins[3]]
    if op in ('shl', 'shr', 'ld'): return [ins[1]], [ins[2]]
    if op in ('ldi', 'rand'): return [ins[1]], []
    if op == 'sti': return [], S(ins[2])
    if op == 'st': return [], [ins[1]] + S(ins[2])
    if op in ('bz', 'bnz'): return [], [ins[1]]
    if op == 'bne': return [], S(ins[1]) + S(ins[2])
    if op == 'f38': return list(ins[2]), list(ins[1])
    if op == 'succ': return [], [ins[2]]
    if op == 'obs': return [], [ins[1]]
    return [], []

def regalloc(a, k=64):
    """Liveness on the control-flow graph, then greedy colouring of the interference graph with k registers;
    returns the renaming (virtual -> 'R<n>').  Raises if k registers do not suffice."""
    c, lab = a.c, a.lab; n = len(c)
    succ = []
    for pc, ins in enumerate(c):
        op = ins[0]
        if op == 'jmp': succ.append([lab[ins[1]]])
        elif op in ('bz', 'bnz'): succ.append([pc + 1, lab[ins[2]]])
        elif op == 'bne': succ.append([pc + 1, lab[ins[3]]])
        elif op in ('succ', 'halt_ok'): succ.append([])
        else: succ.append([pc + 1] if pc + 1 < n else [])
    du = [_du(ins) for ins in c]; live = [set() for _ in range(n + 1)]; changed = True
    while changed:
        changed = False
        for pc in range(n - 1, -1, -1):
            out = set().union(*[live[s] for s in succ[pc]]) if succ[pc] else set()
            d, u = du[pc]; inn = (out - set(d)) | set(u)
            if inn != live[pc]: live[pc] = inn; changed = True
    adj = {}
    for pc in range(n):
        out = set().union(*[live[s] for s in succ[pc]]) if succ[pc] else set()
        for d in du[pc][0]:
            adj.setdefault(d, set())
            for x in out:
                if x != d: adj[d].add(x); adj.setdefault(x, set()).add(d)
        for u in du[pc][1]: adj.setdefault(u, set())
    col = {}
    for v in sorted(adj, key=lambda v: -len(adj[v])):
        used = {col[x] for x in adj[v] if x in col}
        col[v] = min(r for r in range(k + 1) if r not in used)
        if col[v] >= k: raise ValueError('more than %d registers needed' % k)
    return {v: 'R%d' % r for v, r in col.items()}

def rename(a, mp):
    b = Asm(); b.lab = dict(a.lab); b.n = a.n
    for ins in a.c:
        b.c.append(tuple([ins[0]] + [mp.get(x, x) if isinstance(x, str) and x in mp else
                                      ([mp[y] for y in x] if isinstance(x, list) else x) for x in ins[1:]]))
    return b

def gen_epilogue(a, caps):
    """After every group: halt if a work counter exceeds its cap; group counter and loop."""
    halt = a.new('halt')
    for r, cap in zip(('NE', 'NW', 'N1'), caps):
        a('rsub', 't1', cap, r); a('shr', 't1', 't1', 255); a('bnz', 't1', halt)   # cap - r < 0 (two's complement)
    a('add', 'NG', 'NG', 1)
    a.lab_pending = halt

RMAP = {}; PCACHE = {}
CAPS = (1 << 200, 1 << 200, 1 << 200); NGROUPS = 1     # the interpreter runs one group
def program(js, alloc=True):
    key = (tuple(js), alloc)
    if key in PCACHE: return PCACHE[key]
    PCACHE[key] = _program(js, alloc); return PCACHE[key]

def _program(js, alloc=True):
    tables(); a = Asm(); a.L('group'); gen_prologue(a); rare = []
    for j in js: gen_block(a, j, emb()['A0'][j], rare)
    gen_epilogue(a, CAPS)
    a('bne', 'NG', NGROUPS, 'group')                   # group loop (2 operations)
    a.L(a.lab_pending); a('halt_ok',)
    for r in rare: gen_rare(a, *r)
    if not alloc: return a
    if not RMAP:
        t = Asm(); t.L('group'); gen_prologue(t); rr = []
        gen_block(t, 0, emb()['A0'][0], rr); gen_block(t, 1, emb()['A0'][1], rr); gen_epilogue(t, CAPS)
        t('bne', 'NG', NGROUPS, 'group'); t.L(t.lab_pending); t('halt_ok',)
        for r in rr: gen_rare(t, *r)
        RMAP.update(regalloc(t))
    return rename(a, RMAP)


# ---------------------------------------------------------------------------------------------------------------
# Organizer experiment vt-q3-smc-r38: a reduced replica of the preregistered SMC (proof.md 6.2, 10.1).
Q3X = dict(K=20, NP=64, MS={17: 128, 18: 4, 19: 4, 20: 1, 21: 1, 22: 1}, MT=512, POOL_LOG2=-101.45)

def _step(A, E, W, i):
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M

def _sched(W, i): return (s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M

def _base():
    p = []
    for (A_, E_, W_) in (TX, TY):
        A = [0] * R; E = [0] * R; W = [0] * R
        for i in range(12, 16): A[i], E[i] = A_[i], E_[i]
        for i in range(8, 16): W[i] = W_[i]
        p += [A, E, W]
    return p

def _rowok(p, i):
    return rowok((p[0], p[1], p[2]), (p[3], p[4], p[5]), i)

def _copy(p): return [x[:] for x in p]

def smc_replica(rng, variants):
    """One replicate: (estimate, stage survivors, tail successes, verified SFS pairs, failed rebuilds)."""
    NP, MS, MT = Q3X['NP'], Q3X['MS'], Q3X['MT']; est = 32 / 2.0 ** 32; parts = []; stages = []
    for _ in range(NP):
        p = _base(); g = G[rng.randrange(32)]; p[2][16] = g; p[5][16] = (g - DW16) & M
        _step(p[0], p[1], p[2], 16); _step(p[3], p[4], p[5], 16)
        if not _rowok(p, 16): raise AssertionError('G')
        parts.append(p)
    for i in range(17, 23):
        m, v, _, _ = CELL['E'][i]; pq = PLUS[i]; fb = bin(m).count('1') + bin(pq).count('1'); surv = []
        for p in parts:
            for _ in range(MS[i]):
                q = _copy(p); Ax, Ex, Wx, Ay, Ey, Wy = q
                e = (rng.getrandbits(32) & ~m & M) | v
                if pq: e = (e & ~pq & M) | (Ex[i-1] & pq)
                Wx[i] = (e - (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i])) & M
                dw = (s1(Wx[i-2]) - s1(Wy[i-2]) + Wx[i-7] - Wy[i-7] - (T7 if i == 22 else 0)) & M
                Wy[i] = (Wx[i] - dw) & M
                _step(Ax, Ex, Wx, i); _step(Ay, Ey, Wy, i)
                if _rowok(q, i): surv.append(q)
        stages.append(len(surv)); est *= len(surv) / (NP * MS[i]) * 2.0 ** -fb
        if not surv: return 0.0, stages, 0, [], 0
        parts = [surv[rng.randrange(len(surv))] for _ in range(NP)]
    m23, v23, _, _ = CELL['W'][23]
    tb = [(30, 0, 1), (31, 1, 1), (21, 14, 0), (25, 16, 0)]       # W23 two-bit conditions imposed (bit, from, ne)
    f = bin(m23).count('1') + len(tb); wt = 2.0 ** (32 - f) / 287309824; hits = bad = 0; pairs = []
    VW = {}
    for p in parts:
        for _ in range(MT):
            vi = rng.randrange(len(variants)); j, a1, k = variants[vi]; a0, a2 = emb()['A0'][j], emb()['A2'][k]
            if vi not in VW: (_, _, Wvx), (_, _, Wvy) = variant(a0, a1, a2)[0]; VW[vi] = (Wvx, Wvy)
            Wvx, Wvy = VW[vi]
            w = (rng.getrandbits(32) & ~m23 & M) | v23
            for b, c, ne in tb: w = (w & ~(1 << b) & M) | ((((w >> c) & 1) ^ ne) << b)
            w7 = (w - s1(p[2][21]) - p[2][16] - s0(Wvx[8])) & M
            if not inF7(w7): continue
            q = _copy(p); Ax, Ex, Wx, Ay, Ey, Wy = q
            for i in (8, 9, 10): Wx[i], Wy[i] = Wvx[i], Wvy[i]
            Wx[23] = w; Wy[23] = (s1(Wy[21]) + Wy[16] + s0(Wy[8]) + w7 + D7) & M; ok = True
            for i in range(23, R):
                if i > 23: Wx[i] = _sched(Wx, i); Wy[i] = _sched(Wy, i)
                _step(Ax, Ex, Wx, i); _step(Ay, Ey, Wy, i)
                if not _rowok(q, i): ok = False; break
            if not ok: continue
            hits += 1; r_ = rebuild(q, w7, a0, a1, a2)
            if r_ is None: bad += 1
            else: pairs.append(r_)
    stages.append(hits)
    return est * hits * wt / (NP * MT), stages, hits, pairs, bad

def rebuild(q, w7, a0, a1, a2):
    """W0..W7 by the inverse expansion, CV1 by inverting steps 7..0 of the variant; accepted only if it is a
    38-step semi-free-start collision whose Step-2 words map back, with W7 in F7 and every cell of rows -4..37
    holding (A/E cells; W cells of rows >= 16)."""
    Wx = q[2]; W = {7: w7}
    for i in range(8, 16): W[i] = Wx[i]
    W[6] = (Wx[22] - s1(Wx[20]) - W[15] - s0(w7)) & M
    for i in (5, 4, 3, 2, 1, 0): W[i] = (Wx[i+16] - s1(Wx[i+14]) - W[i+9] - s0(W[i+1])) & M
    var, _ = variant(a0, a1, a2); (A, E, _), _ = var; A = dict(A); E = dict(E)
    for i in range(7, -1, -1):
        A[i-4] = (E[i] - A[i] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
        E[i-4] = (E[i] - A[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i] - W[i]) & M
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]
    if not valid(var): return None
    wx, wy = pair(cv, var)
    if wx[:8] != [W[i] for i in range(8)] or wx == wy or compress(cv, wx) != compress(cv, wy) or not inF7(wx[7]): return None
    tx, ty = trace(cv, wx), trace(cv, wy)
    for i in range(-4, R):
        for k in 'AE':
            m, v, d, _ = CELL[k][i] if i >= 0 else (0, 0, 0, 0)
            X = tx['AE'.index(k)][i]; Yv = ty['AE'.index(k)][i]
            if X & m != v or X ^ Yv != d: return None
        if i >= 0 and (tx[1][i] ^ tx[1][i-1]) & PLUS[i]: return None
        if i >= 16 and not rowok(tx, ty, i): return None
    return cv, wx, wy

def q3_experiment(req):
    V = emb()['VS']; K_ = Q3X['K']; rows = []; zs = []; allp = []; okall = True
    for tr in req['trials']:
        t = tr['trial']; row = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < K_:
            seed = bytes.fromhex(tr['seed'])
            rng = random.Random(int.from_bytes(hashlib.shake_256(b'vt-q3' + seed).digest(32), 'big'))
            z, st, hits, pairs, bad = smc_replica(rng, V); zs.append(z); allp += pairs
            good = hits > 0 and bad == 0 and len(pairs) == hits; okall &= good
            row['observations'] = dict([('log2_estimate', math.log2(z) if z > 0 else -1000.0), ('tail_successes', hits),
                ('verified_pairs', len(pairs)), ('failed_rebuilds', bad)] + [('survivors_row%d' % (17 + i), n) for i, n in enumerate(st[:6])])
            if good:
                cv, wx, wy = pairs[0]
                row['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        elif t == K_:
            zbar = sum(zs) / len(zs) if zs else 0.0
            row['observations'] = dict(log2_pooled_mean=math.log2(zbar) if zbar > 0 else -1000.0, replicates=len(zs))
            if okall and len(zs) == K_ and zbar >= 2.0 ** Q3X['POOL_LOG2']:
                cv, wx, wy = allp[-1]
                row['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        rows.append(row)
    return dict(schema_version=1, trials=rows)

# ---------------------------------------------------------------------------------------------------------------
# Organizer experiment vt-ram-r38: the counted program against the reference on real first blocks.
def ram_experiment(req):
    E = emb(); rows = []
    for tr in req['trials']:
        t = tr['trial']; seed = bytes.fromhex(tr['seed'])
        rb = hashlib.shake_256(b'vt-ram' + seed).digest(64)
        rw = [int.from_bytes(rb[:32], 'little'), int.from_bytes(rb[32:], 'little')]
        js = [(32 * t + k) % 256 for k in range(32)]; mach = None; refw7 = []; refw17 = []
        def bucket(j, Y, Z0):
            a1, k = E['A0P'][j]; return [entry(mach.cv, j, a1, k)]
        mach = Machine(rw, bucket); mach.run(program(js))
        m0, cv = mach.m0, mach.cv; mis = 0
        if cv != compress(IV, m0) or m0 != [(rw[k // 8] >> (32 * (k % 8))) & M for k in range(16)]: mis += 1
        for (j, Y, Z0, n), jj in zip(mach.trace, js):
            a1, k = E['A0P'][jj]; var, c7 = variant(E['A0'][jj], a1, E['A2'][k]); wx, wy = pair(cv, var)
            if j != jj or (Y, Z0) != yz0(cv, E['A0'][jj]) or n != 1: mis += 1
            if inF7(wx[7]): refw7.append(jj); refw17.append(trace(cv, wx)[2][17])
        if len(mach.trace) != 32 or mach.obs != refw17: mis += 1
        a1, k = E['A0P'][js[0]]; wx, wy = pair(cv, variant(E['A0'][js[0]], a1, E['A2'][k])[0])
        ok_ = mis == 0
        rows.append(dict(trial=t, message_a_hex=struct.pack('>32I', *(m0 + wx)).hex() if ok_ else None,
                         message_b_hex=struct.pack('>32I', *(m0 + wy)).hex() if ok_ else None,
                         observations=dict(blocks=len(mach.trace), w7_passes=len(refw7), mismatches=mis,
                                           ops=mach.ops, units=mach.units)))
    return dict(schema_version=1, trials=rows)

# ---------------------------------------------------------------------------------------------------------------
# Table construction (preprocessing P6, proof.md 5.1) as counted code.  Table j: header/count words at
# HB_j + (Y << 32 | Z0), fill cursors at CB_j + (Y << 32 | Z0), entries in ENT; the list R_j holds two words per
# variant (entry base word EB = c7 | A1 << 32 | A2 index << 64 | S0(A1) << 80, and c9x).  The passes:
# zero (headers), count, prefix sums (header = offset << 20 | count; cursor = offset), fill.
REG['CUR'] = 7 << 200; REG['RL'] = 8 << 200

def gen_build_pass(a, fill):
    """One pass over v in R_j for a fixed Y (registers Y, YB = header base + (Y << 32), YC = cursor base +
    (Y << 32), P = list pointer, PE = list end).  Count pass: header word += 1 for each of the 32 targets;
    fill pass: store the entry at the target's cursor and advance it."""
    lp = a.new('bl')
    a.L(lp)
    a('ld', 'EB', 'P'); a('add', 'q', 'P', 1); a('ld', 'C9', 'q')
    a('shr', 'A1', 'EB', 32); a('and', 'A1', 'A1', M)
    a('add', 'U', 'Y', 'A1'); a('and', 'U', 'U', M)
    rot32(a, 'sU', 'U', 7, 18, 3, shr3=True)
    a('sub', 'X', 'sU', 'A1'); a('add', 'X', 'X', 'C9')
    for gi, g in enumerate(G):
        a('rsub', 'Z', g, 'X'); a('and', 'Z', 'Z', M)
        if not fill:
            a('add', 'Aw', 'YB', 'Z'); a('ld', 'c', 'Aw'); a('add', 'c', 'c', 1); a('st', 'Aw', 'c')
        else:
            a('add', 'Aw', 'YC', 'Z'); a('ld', 'o', 'Aw'); a('or', 'e', 'EB', gi << 74); a('st', 'o', 'e')
            a('add', 'o', 'o', 1); a('st', 'Aw', 'o')
    a('add', 'P', 'P', 2); a('bne', 'P', 'PE', lp)

def gen_zero(a):
    lp = a.new('zl'); a.L(lp); a('st', 'I', 0); a('add', 'I', 'I', 1); a('bne', 'I', 'IE', lp)

def gen_prefix(a):
    """Dense loop over header addresses I (cursor address J = I + CB - HB): header = OFF << 20 | count."""
    lp = a.new('pl'); a.L(lp)
    a('ld', 'c', 'I'); a('shl', 'h', 'OFF', 20); a('or', 'h', 'h', 'c'); a('st', 'I', 'h'); a('st', 'J', 'OFF')
    a('add', 'OFF', 'OFF', 'c'); a('add', 'I', 'I', 1); a('add', 'J', 'J', 1); a('bne', 'I', 'IE', lp)

def build_selftest(j=0):
    """Toy instance of P6 for A0_j: two values of Y, a list of valid variants including a c9 class sharing W16
    (so buckets have several entries).  Counts and bucket contents are compared with the direct definition
    (Lemma 5); per-item operation counts are measured."""
    E = emb(); a0 = E['A0'][j]; a1, k0 = E['A0P'][j]
    lst = [(a1, k) for k in range(768) if valid(variant(a0, a1, E['A2'][k])[0])]
    lst += [(x1, k) for jj, x1, k in E['VS'] if jj == j]
    words = []
    for x1, k in lst:
        _, c7 = variant(a0, x1, E['A2'][k]); words += [c7 | x1 << 32 | k << 64 | S0(x1) << 80, c9x(E['A2'][k])]
    m = Machine([], None)
    for i, w in enumerate(words): m.mem[REG['RL'] + i] = w
    m.load = lambda addr: m.mem.get(addr, 0)
    HB, CB = REG['HDR'] | (j << 64), REG['CUR'] | (j << 64)
    rng = random.Random(9); Ys = [rng.getrandbits(32) for _ in range(2)]
    ops = {}
    for fill in (False, True):
        a = Asm(); gen_build_pass(a, fill); a('halt_ok',)
        before = m.ops
        for Y in Ys:
            m.r = {'Y': Y, 'YB': HB + (Y << 32), 'YC': CB + (Y << 32), 'P': REG['RL'], 'PE': REG['RL'] + len(words)}
            m.run(a)
        ops['fill' if fill else 'count'] = (m.ops - before) / (len(Ys) * len(lst))
        if not fill:                       # sparse prefix sums over the touched headers (the dense loop is gen_prefix)
            touched = sorted(ad for ad in m.mem if ad >> 200 == 1); off = REG['ENT']
            for ad in touched:
                c = m.mem[ad]; m.mem[ad] = (off << 20) | c; m.mem[CB + (ad - HB)] = off; off += c
    ref = {}
    for Y in Ys:
        for (x1, k) in lst:
            X = (s0((Y + x1) & M) - x1 + c9x(E['A2'][k])) & M
            for gi, g in enumerate(G):
                ref.setdefault(HB + (Y << 32) + ((g - X) & M), []).append(gi)
    bad = 0
    wd = {(x1, k): words[2 * i] for i, (x1, k) in enumerate(lst)}
    for ad, gis in ref.items():
        h = m.mem[ad]; off, cnt = h >> 20, h & ((1 << 20) - 1)
        got = sorted(m.mem[off + i] for i in range(cnt))
        Y = (ad - HB) >> 32; Z0 = (ad - HB) & M; want = []
        for (x1, k) in lst:
            w16 = (s0((Y + x1) & M) - x1 + Z0 + c9x(E['A2'][k])) & M
            if w16 in G: want.append(wd[(x1, k)] | G.index(w16) << 74)
        bad += got != sorted(want) or cnt != len(gis)
    za = Asm(); gen_zero(za); pa = Asm(); gen_prefix(pa)
    cost = lambda asm: sum(2 if i[0] in ('bz', 'bnz', 'bne') else 1 for i in asm.c)
    return dict(variants=len(lst), buckets=len(ref), max_bucket=max(len(v) for v in ref.values()), mismatches=bad,
                count_ops=ops['count'], fill_ops=ops['fill'], zero_ops=cost(za), prefix_ops=cost(pa))

# ---------------------------------------------------------------------------------------------------------------
def selftest():
    """Reference construction and counted program (proof.md Appendix A.1 lists the expected output)."""
    E = emb(); ok = True; rng = random.Random(5)
    tx, ty = trace(PCV, PMX), trace(PCV, PMY)
    c1 = compress(PCV, PMX) == compress(PCV, PMY) and all(rowok(tx, ty, i) for i in range(16, R))
    print('1 published pair collides, rows 16..37 hold:', c1); ok &= c1
    n = 0
    for g in G:
        q = _base()
        for i in range(12, 16):
            for k in range(3): q[k][i], q[3 + k][i] = tx[k][i], ty[k][i]
        q[2][16] = g; q[5][16] = (g - DW16) & M; _step(q[0], q[1], q[2], 16); _step(q[3], q[4], q[5], 16); n += _rowok(q, 16)
    print('2 G: %d values, %d pass row 16' % (len(G), n)); ok &= n == 32
    a2bad = 0
    for a2 in E['A2']:
        (Ax, Ex, Wx), (Ay, Ey, Wy) = variant(TX[0][0], TX[0][1], a2)[0]; m, v, _, _ = CELL['E'][6]
        a2bad += not (Ex[6] & m == v and not (Ex[7] ^ Ex[6]) & PLUS[7] and
                      ((Wx[10] - Wy[10]) & M, (s0(Wx[10]) - s0(Wy[10])) & M) == DIFF[10])
    print('3 A2 list: %d distinct values, %d violate the A2-only conditions' % (len(set(E['A2'])), a2bad)); ok &= a2bad == 0
    pb = sum(not valid(variant(E['A0'][j], a1, E['A2'][k])[0]) for j, (a1, k) in enumerate(E['A0P']))
    vb = sum(not valid(variant(E['A0'][j], a1, E['A2'][k])[0]) for j, a1, k in E['VS'])
    print('4 invalid embedded variants: %d of 256, %d of %d' % (pb, vb, len(E['VS']))); ok &= pb == 0 and vb == 0
    nb = 0
    for t in range(300):
        j, a1, k = E['VS'][rng.randrange(len(E['VS']))]; cv = [rng.getrandbits(32) for _ in range(8)]
        var, c7 = variant(E['A0'][j], a1, E['A2'][k]); wx, wy = pair(cv, var); tx, ty = trace(cv, wx), trace(cv, wy)
        for i in range(16):
            for kk in (0, 1):
                m, v, d, _ = CELL['AE'[kk]][i]
                nb += tx[kk][i] & m != v or tx[kk][i] ^ ty[kk][i] != d
            nb += bool((tx[1][i] ^ tx[1][i-1]) & PLUS[i])
        Y, Z0 = yz0(cv, E['A0'][j]); w16 = (s1(wx[14]) + wx[9] + s0(wx[1]) + wx[0]) & M
        nb += wx[7] != (c7 - cv[0]) & M or wx[1] != (Y + a1) & M or w16 != (s0((Y + a1) & M) - a1 + Z0 + c9x(E['A2'][k])) & M
        nb += any(((tx[2][i] - ty[2][i]) & M, (s0(tx[2][i]) - s0(ty[2][i])) & M) != ((TX[2][i] - TY[2][i]) & M, (s0(TX[2][i]) - s0(TY[2][i])) & M) for i in range(8, 16))
        nb += tx[2][17] != ty[2][17] or (tx[2][16] - ty[2][16]) & M != DW16
    print('5 variant soundness, 300 random chaining values: %d mismatches' % nb); ok &= nb == 0
    a0i = {a: j for j, a in enumerate(E['A0'])}; a2i = {a: k for k, a in enumerate(E['A2'])}; good = 0
    for t in E['SFS']:
        a0, a1, a2 = t[:3]; cv = list(t[3:11]); j, k = a0i[a0], a2i[a2]
        r16, w7, deep, (tx_, ty_, wx, wy) = outcome(cv, a0, a1, a2)
        true = entry(cv, j, a1, k); dec = entry(cv, j, *E['A0P'][j])
        mach = Machine([1, 2], lambda jj, Y, Z0: [dec, true, dec], cvforce=cv); mach.run(program([j]))
        good += r16 and w7 and deep == R - 1 and mach.succ == (j, true) and compress(cv, wx) == compress(cv, wy) and wx != wy
    print('6 counted program on the semi-free-start vectors: %d of %d found and verified' % (good, len(E['SFS']))); ok &= good == len(E['SFS'])
    cv = [rng.getrandbits(32) for _ in range(8)]; a1, k = E['A0P'][0]; e0 = entry(cv, 0, a1, k)
    m0 = Machine([1, 2], lambda j, Y, Z0: [], cvforce=cv); m0.run(program([])); pro = m0.ops
    m1 = Machine([1, 2], lambda j, Y, Z0: [], cvforce=cv); m1.run(program([0]))
    m2 = Machine([1, 2], lambda j, Y, Z0: [e0] * 3, cvforce=cv); m2.run(program([0]))
    w7 = inF7((e0 - cv[0]) & M)
    print('7 ops: group prologue + epilogue + loop %d (+1 unit), empty block %d, block with 3 entries (W7 %s) %d' % (pro, m1.ops - pro, w7, m2.ops - pro))
    regs = {x for ins in program([0, 1, 2]).c for x in ins[1:] for x in (x if isinstance(x, list) else [x])
            if isinstance(x, str) and x[:1] == 'R' and x[1:].isdigit()}
    print('8 physical registers: %d' % len(regs)); ok &= len(regs) <= 64
    for j in (0, 5):
        b = build_selftest(j)
        print('9 table build, toy A0 index %d: %d variants, %d buckets (largest %d), %d mismatches; ops per (Y, variant): '
              'count %g, fill %g; per header: zero %d, prefix %d' % (j, b['variants'], b['buckets'], b['max_bucket'],
              b['mismatches'], b['count_ops'], b['fill_ops'], b['zero_ops'], b['prefix_ops']))
        ok &= b['mismatches'] == 0
    print('SELFTEST', 'OK' if ok else 'FAILED')
    return ok

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    req = json.loads(sys.stdin.read())
    out = q3_experiment(req) if req['experiment_id'].startswith('vt-q3') else ram_experiment(req)
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')))

