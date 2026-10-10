#!/usr/bin/env python3
# vt38.py - sha256-r38-sp: variant-table collision attack on 38-step SHA-256 (target sha256-r38-prefix-v1).  Standard library only.
# Contents: the reference construction, the counted online program (an op-counting 256-bit word-RAM interpreter running the exact
# online code), the organizer experiments (stdin JSON -> stdout JSON) and a self-test (argument "selftest").
# Characteristic, two-bit conditions and the semi-free-start pair: Li, Zhang, Li, Liu, Qian, Zhu, "Pushing Collision Attacks on SHA-2 to
# 39 Steps", IACR ePrint 2026/1120, Tables 3-5 (our transcription, verified against the published pair).  The construction (dense-part
# variants A0, A1, A2 of the published dense part and a row-16 table keyed by (Y, Z0)) is that of the public packages c99df2dc (qkniep) and
# 0ae69bcb (0xshikhar); this code and every count below were written and measured independently for this package (proof.md Section 2).
import sys, json, hashlib, struct, zlib, base64

M = 0xffffffff
NR = 38
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be,
     0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa,
     0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85,
     0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def trace(cv, w16, n=NR):
    """A[i], E[i] for i = -4..n-1 (dicts) and W[0..n-1] of the first n steps from the chaining value cv."""
    W = list(w16)
    for i in range(16, n): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M)
    A = {-1-i: cv[i] for i in range(4)}; E = {-1-i: cv[4+i] for i in range(4)}
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
    return A, E, W

def compress(cv, w16):
    A, E, W = trace(cv, w16)
    f = [A[37], A[36], A[35], A[34], E[37], E[36], E[35], E[34]]
    return [(cv[i] + f[i]) & M for i in range(8)]

# ---- ePrint 2026/1120 Tables 3-5 (member x = the message printed second) ----
# Cells per kind (A, E, W) and row: (mask, x-value, x^y difference, '+' mask); unlisted rows have no cell.  PQ[i]: bits where E_i = E_{i-1}.
# Two-bit conditions with a word in rows >= 16 (kind 0 A, 1 E, 2 W): (k1, i1, b1, equal, k2, i2, b2, row), keyed at the later row.
PCV = [0xcd278980, 0x1b12a052, 0xb87cc8a6, 0xa9e059c5, 0xc9c3db85, 0x6ca4b5b5, 0x63d13ac1, 0xc0329f1e]
PMX = [0x48fc271b, 0x9fca20cd, 0xcc89f96f, 0xfc40396f, 0x8b328cb4, 0x6b91ef78, 0x97f9b767, 0xc2450045, 0x3f416758, 0xfe9804cb, 0x63a88c0f,
       0x0ceb1f8d, 0xa28cd15a, 0x77a1e994, 0xd28e48a0, 0x9f1f65bb]
PMY = [0x48fc271b, 0x9fca20cd, 0xcc89f96f, 0xfc40396f, 0x8b328cb4, 0x6b91ef78, 0x97f9b767, 0xe2450045, 0x3b016f58, 0xde9804cb, 0x66a99ea5,
       0x0ce30b8d, 0xa28cd15a, 0x77a1e994, 0xd28e48a0, 0x9b5f6dbb]

# Cells (mask, x-value, x^y difference, '+' mask) of A, E, W by row; '+' masks E_i[b] = E_{i-1}[b] are the 4th entries (the E rows' PQ below is their AND).
_CH = [{7: (1610612736, 536870912, 1610612736, 0), 8: (4261904, 16, 4261904, 0), 11: (2060, 2056, 2060, 0), 12: (1142965762, 1073758720, 1142965762, 0), 13: (536936448, 0, 536936448, 0), 14: (134414480, 134217872, 134414480, 0), 15: (41975808, 8388608, 41975808, 0), 17: (536870912, 536870912, 536870912, 0)}, {5: (0, 0, 0, 3758096384), 6: (138678416, 134480016, 0, 3758622720), 7: (3939897499, 3804237825, 3758096384, 67635200), 8: (3957292027, 2299865209, 139204752, 67108864), 9: (4278190015, 3329275675, 76546059, 0), 10: (1040153503, 683879063, 4261888, 0), 11: (3187670975, 2163392958, 536899588, 64), 12: (4261412799, 1570574870, 1008926725, 64), 13: (4293918591, 901856013, 67450, 128), 14: (2086891391, 537027697, 134283264, 4224), 15: (1246957562, 1242762074, 2176, 4096), 16: (1279466112, 1208156800, 1078071808, 262160), 17: (1086462592, 2048, 0, 17072144), 18: (1086722608, 4330000, 262160, 16809984), 19: (830770738, 805569584, 25198592, 0), 20: (562331664, 537133072, 0, 0), 21: (562072576, 553682944, 536870912, 0), 22: (536870912, 0, 0, 0), 23: (536870912, 536870912, 0, 0)}, {7: (536870912, 0, 536870912, 0), 8: (71305216, 71303168, 71305216, 0), 9: (536870912, 536870912, 536870912, 0), 10: (83956394, 16777226, 83956394, 0), 11: (529408, 529408, 529408, 0), 15: (71305216, 67108864, 71305216, 0), 16: (536870912, 536870912, 536870912, 0), 23: (92446720, 92446720, 25198592, 0), 25: (536870912, 0, 536870912, 0)}]
CELLS = [[(0, 0, 0, 0)] * NR for _ in range(3)]
for _k in range(3):
    for _i, _c in _CH[_k].items(): CELLS[_k][_i] = _c
PQ = [0, 0, 0, 0, 0, 0, 3758096384, 526336, 67108864, 0, 0, 0, 64, 0, 128, 4096, 0, 262160, 16809984, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X2 = [(0, 14, 15, 1, 0, 16, 15, 16), (0, 14, 23, 1, 0, 16, 23, 16), (0, 14, 25, 1, 0, 16, 25, 16), (0, 15, 4, 1, 0, 16, 4, 16), (0, 15, 7, 1, 0, 16, 7, 16), (0, 15, 16, 0, 0, 16, 16, 16), (0, 15, 17, 1, 0, 16, 17, 16), (0, 15, 27, 1, 0, 16, 27, 16), (0, 15, 29, 1, 0, 16, 29, 16), (0, 16, 15, 1, 0, 17, 15, 17), (0, 16, 23, 1, 0, 17, 23, 17), (0, 16, 25, 1, 0, 17, 25, 17), (0, 17, 9, 1, 0, 17, 20, 17), (0, 17, 6, 1, 0, 17, 18, 17), (0, 17, 8, 1, 0, 17, 17, 17), (0, 16, 29, 1, 0, 18, 29, 18), (0, 18, 29, 1, 0, 19, 29, 19), (1, 16, 4, 0, 1, 16, 23, 16), (1, 16, 3, 0, 1, 16, 8, 16), (1, 16, 14, 1, 1, 16, 28, 16), (1, 16, 4, 1, 1, 17, 4, 17), (1, 16, 18, 1, 1, 17, 18, 17), (1, 18, 0, 0, 1, 18, 13, 18), (1, 17, 15, 1, 1, 18, 15, 18), (1, 17, 24, 1, 1, 18, 24, 18), (1, 19, 6, 0, 1, 19, 19, 19), (1, 19, 20, 1, 1, 19, 2, 19), (1, 21, 2, 1, 1, 21, 16, 21), (2, 7, 8, 0, 2, 7, 25, 7), (2, 7, 14, 0, 2, 7, 18, 7), (2, 7, 1, 1, 2, 7, 12, 7), (2, 8, 0, 0, 2, 8, 28, 8), (2, 8, 30, 0, 2, 8, 9, 8), (2, 8, 1, 1, 2, 8, 18, 8), (2, 16, 1, 0, 2, 16, 12, 16), (2, 16, 20, 0, 2, 16, 27, 16), (2, 16, 8, 1, 2, 16, 25, 16), (2, 16, 14, 1, 2, 16, 18, 16), (2, 16, 4, 0, 2, 16, 6, 16), (2, 16, 22, 0, 2, 16, 31, 16), (2, 23, 0, 0, 2, 23, 30, 23), (2, 23, 1, 0, 2, 23, 31, 23), (2, 23, 14, 1, 2, 23, 21, 23), (2, 23, 16, 1, 2, 23, 25, 23), (2, 25, 4, 1, 2, 25, 6, 25), (2, 25, 22, 1, 2, 25, 31, 25), (2, 25, 20, 1, 2, 25, 27, 25)]

_tx = trace(PCV, PMX); _ty = trace(PCV, PMY)       # S*: the published dense part and the published differences
SAX = [_tx[0][i] for i in range(-4, 16)]; SAY = [_ty[0][i] for i in range(-4, 16)]; SEX = [_tx[1][i] for i in range(-4, 16)]; SEY = [_ty[1][i] for i in range(-4, 16)]
SWX = list(PMX); SWY = list(PMY)
DW = [(_ty[2][i] - _tx[2][i]) & M for i in range(NR)]; DS0 = [(s0(_ty[2][i]) - s0(_tx[2][i])) & M for i in range(NR)]
DW16 = 0x20000000          # W16y = W16x - DW16 (= -DW[16], DW[16] being y minus x)
A0_B64 = 'eNol09GJKzEMheFK0kbepgMjFmOMGSaQ3X1J0sOUkjb0NqWklIH7ee/Dzxkiy5KOlfH5uX5NDrx/rmOnGDeKsVCMC8U4v69fGB+KcVCMN8XYKcaNYiwU40Ixzrv8+6yZ6qUa6f50f35Nzu90b7pTHPt3uss5ulC4y1l63p2/5zjc958cn3n3XX8v+tIfxXjTye77RieL7wudnE85Tzk48MbutxvFWCjGhWKcDzmPa+ddoPMv0HkXE951vgU63wKdb4HOt0DnW6DzLdD5Fuh8C3S+BTrfAp1vMb07HnM+PuF4pdl4hd33jWIsFObjFT2fvHryh04O32862XHD4rcLnZwPOd78/Jsh9Z/6T/2mPjMm3kSPqcfUozPUe+gxK08qPyovKi8qHyoPqvmr2au5q5mreatZqzmrGav5VmdX51ZnVvFVfBVfxddzvi3v0WdvE+/d/979kc7lOuvrWb1UJ9VINfwGPaqRTX9Nf01/TX9Nzaa/pm7TX1O76a+p39Rv6jf1m/pFbpFb5Ba5RW6RW+QWuUVukVvkFrlFbpFb5G7ObuKb2Ca2iW1i2zlneJkF9jXsatjRsKNhP7v9DLsZdrPby5jYy24nA91OBrqdjL+99F+4/NrV3+vKmzo98h+JyfQO43xd/wF46Z2l'
A2_B64 = 'eNoNzt3NgloCBdBCbAGS+zbzcQrwJ0zCm0oDIg2INCDSgAgFiLRwGvAm2tOsh/2ws7OT9Umn//wrX/nJ53+6fOUnnzTaoz3ao12Xr/zkk6z++6985Seff3T5yk8+uS5f+cmn0OUrP/kkwT/4B//gr8tXfvLJdfnKTz6FLl/5ySed/vj/+P/4//j/+P/4//j/+O3RHu3Rrgu/XU9WGX/Gn/Fn/Bl/xp/xZ/wZf8af8Wf8GX/Gn/Fn/P7BP/gHf134/fVcF35/vdCF319PpzX/mn/Nv+Zf86/51/xrfnu0R3u068Jv15PVhn/Dv+Hf8G/4N/wb/g3/hn/Dv+Hf8G/4N/wb/g2/f/AP/sFfF35/PdeF318vdOH319Npy7/l3/Jv+bf8W/4t/5bfHu3RHu268Nv1ZLXj3/Hv+Hf8O/4d/45/x7/j3/Hv+Hf8O/4d/45/x+8f/IN/8NeF31/PdeH31wtd+P31dNrz7/n3/Hv+Pf+ef8+/57dHe7RHuy78dj1ZHfgP/Af+A/+B/8B/4D/wH/gP/Af+A/+B/8B/4D/w+wf/4B/8deH313Nd+P31Qhd+fz2djvxH/iP/kf/If+Q/8h/57dEe7dGuC79dT1Ylf8lf8pf8JX/JX/KX/CV/yV/yl/wlf8lf8pf8/sE/+Ad/Xfj99VwXfn+90IXfX0+nE/+J/8R/4j/xn/hP/Cd+e7RHe7Trwm/Xk1XFX/FX/BV/xV/xV/wVf8Vf8Vf8FX/FX/FX/BW/f/AP/sFfF35/PdeF318vdOH319PpzH/mP/Of+c/8Z/4z/5nfHu3RHu268Nv1ZFXz1/w1f81f89f8NX/NX/PX/DV/zV/z1/w1f83vH/yDf/DXhd9fz3Xh99cLXfj99XS68F/4L/wX/gv/hf/Cf+G3R3u0R7su/HY9WTX8DX/D3/A3/A1/w9/wN/wNf8Pf8Df8DX/D3/D7B//gH/x14ffXc134/fVCF35/PZ2u/Ff+K/+V/8p/5b/yX/nt0R7t0a4Lv11PVi1/y9/yt/wtf8vf8rf8LX/L3/K3/C1/y9/yt/z+wT/4B39d+P31XBd+f73Qhd9fT6cb/43/xn/jv/Hf+G/8N357tEd7tOvCb9eTVcff8Xf8HX/H3/F3/B1/x9/xd/wdf8ff8Xf8Hb9/8A/+wV8Xfn8914XfXy904ffX0+nOf+e/89/57/x3/jv/nd8e7dEe7brw2/Vk1fP3/D1/z9/z9/w9f8/f8/f8PX/P3/P3/D1/z+8f/IN/8NeF31/PdeH31wtd+P31dHrwP/gf/A/+B/+D/8H/4LdHe7RHuy78dj1ZDfwD/8A/8A/8A//AP/AP/AP/wD/wD/wD/8A/8PsH/+Af/HXh99dzXfj99UIXfn89nZ78T/4n/5P/yf/kf/I/+e3RHu3Rrgu/XU9WI//IP/KP/CP/yD/yj/wj/8g/8o/8I//IP/KP/P7BP/gHf134/fVcF35/vdCF319Ppxf/i//F/+J/8b/4X/wvfnu0R3u068Jv15PVzD/zz/wz/8w/88/8M//MP/PP/DP/zD/zz/wzv3/wD/7BXxd+fz3Xhd9fL3Th99fT6c3/5n/zv/nf/G/+N/+b3x7t0R7tuvDb9WS18C/8C//Cv/Av/Av/wr/wL/wL/8K/8C/8C//C7x/8g3/w14XfX8914ffXC134/cPyf6pJa8w='
S512_B64 = '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'
E256_B64 = 'eNoN0/tX0wUYx/HneXCUGJkhl2T7fuMmoUDQuKm7mBIahkUWCcfs4qUEb4V2zA6pQGMokIxA5KKQsgFZCM4LsEuIIKYoBZmDbV+UBI8nwiStYN+t/QPPD8/781q/p4gbBtfpBca1MDC8404TFnW3WRXgxRWKiAb5DXHXyCU2gEmli+ZcjtCr0odfiR/f39HkDYxmDr8UuebDFsTopqPsfrqaHsw3YMOZxfbX8LjXPG4ClkS024ZwU1i2wQcSL7fbDmNZT6vjGxQPaCzt8OxYtHEdXDnfKteSIKxBcpFCzp5mIsi0qthcA6fWhfuOY/DuaFkH5V/xltwnh9hNFEKfPKv9px6T/tVJ/6DMM7UOE+p3FTkvq25L+RrkB/yZFNq3UyOZJhf3UOEhSrNEW7PhncwCJocM8Tq2gpomC23JmNH7giiZ8tMLWaBj3eXSO1TbX8P605vBzXNTaLS7kC2gL+eH2HswsrWdj8GsyQJbIia1urASuuHZYAiBkNjnHFtxARdmdsNVu7skevqgtEK0nvwiT1nuQ55HjLkOostX2AfQbfnvovdJZpJZ+6BN2cyG0uoDKvkUxSZfkt2mFwJDW91BMOcMvxhNJSWSe7Qlc4UZcKvAcnImjBzSnEW4nKa3ZyGKPXSJkJig439EzUw3JoM2iYv5Cqx72CU8SLXFw5KfyL33KKuiTs9Kfgc+KPV91IN6aYGsk24NPuPYhfsfl3KjcKtEYVZDQ8cx++f4yXs3hr4HpYeGa4HJqmauHmZPfW29A0viXa2NUF5ywlaB59xf6pqJofnnjUshNUhl+QpiXRexbmQaCXIk4YXQRj4O3yoMFD1Az47vmSVU7RMQeIVaVArBGlooj7obh5x6ni4eIp9vdBZJzW6TtZPHJo0VcN+3cfYfcdi7xcLguHcra8fRzWd14dD73W3pFGVORlmGIOnT7j8Tcey7lw1rwFVdflMJB6dbGYa+Tb8s05LfkmUWBYh8tIwd9RUx1pswcU/i6Efrh4W8CiPSE8Z/Q0FYI5+I0rme3H7o2F1oS8cZJ2tNH8G+VZ2GSBgckQS2ULW7m1BJCYpuixbGdrmLNlGXp+G8P6zxipNN0nWFSBhBIz9N8MfwHXmBU0de/QkuF6q3FNhewRvHnrfdwtQO42gGrhgrlV6iQK9z1gF4WFbku5w6Ak6yT5D/XzrfVdSzWuesXOVTxG6m2nsCLgvqRtlHHG6rFBtTQZLf5iwY5urrbH28+0VDGhRjIP8qXusRc4C/HZz/9GOsmYpxelmYIRA9xrm9B4QqOqSedV0NxkVaSz1seNWTldGO1gJRGgk9lE5NoZFD0914YXuTYS1Mb9HYtuO8COF/eWjaqJ7tRzsnjtiW4boj/rZBvOrhJzeS4kScrIfEIXPsZZgyg9i1ZLsSbG2DC+IT5pOgWBnEWSFso0GfBAP9GkcV2vrKnEZe2lXq/OcXdYtk16jvjTn2w/jkGwflpyk5r4r1oxHlImY7xeIPlmxoTDj3pwz947z+Xonr9xu5PuiaV21MgcJyFyMDOeENvAmbe4876jFdoNUJIaRMbY/Hx50zRbmkytGab0LF5qi7m7E085wwhT5rkztXGpTmF9xNl7IU4/2Yo5Lrl0NYn9zig2frVdwz6BKu1SXDr/f0xjRIryl3at1z/+mmIFiz2GMiCW99UNcUAG92tjHZFOt+3CbG516vMi6DR8pvDEuhy5Md34hH9kYFPaJ3/5D8XY5f1rXZElDBuQoXUNFXdebfYWTqB6GArCuPiLaS6e4p7gDk1LY7Oz7leVFiIKkyQd5F/TMWWpTw2vX62Q8xb34l+z4xLbMmirHaaohpp7wN2rFAPP2AkfxLN4Tif/bi1bh4ezn2BsYzs0jU8fPgebhzJn9Mj83xRfZtOBwrtp6CFdKtvuEkWL7Aufah00cnMtA7qtJSBxF71ZwZ5Fm55l9gT4mQeYB9bzdac2FGv9rqhjtXR1ncMGDbJfvP+D9oQo+0'
A0L = list(struct.unpack('<256I', zlib.decompress(base64.b64decode(A0_B64))))      # the 256 A0 values (advice, credit c99df2dc)
A2L = list(struct.unpack('<768I', zlib.decompress(base64.b64decode(A2_B64))))      # the 768-value A2 list (recomputed by an exhaustive scan)
GL = sorted(0x35f29010 | sum(1 << b for j, b in enumerate((0, 2, 10, 13, 19)) if (k >> j) & 1) for k in range(32))   # the 32 words of G
GSET = {g: k for k, g in enumerate(GL)}

def cellok(k, i, x, y):
    m, v, d, _ = CELLS[k][i]
    return (x & m) == v and (x ^ y) == d

def rowok(tx, ty, i):
    """Row i of both traces: A, E, W cells, '+' pair, and two-bit conditions keyed at row i (member x).
    Rows < 0 have no cells.  W cells of rows 7..10 are not part of the event (W7: F7; W8..W10: modular differences)."""
    if i < 0: return True
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    if not cellok(0, i, Ax[i], Ay[i]): return False
    if not cellok(1, i, Ex[i], Ey[i]): return False
    if (i < 7 or i > 10) and not cellok(2, i, Wx[i], Wy[i]): return False
    if (Ex[i] ^ Ex[i-1]) & PQ[i]: return False
    if i >= 16:
        for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
            if row == i:
                v1 = (tx[k1][i1] >> b1) & 1; v2 = (tx[k2][i2] >> b2) & 1
                if (v1 ^ v2) != (0 if eq else 1): return False
    return True

# ---- dense-part variants: v = (A0, A1, A2) ----
D7 = DW[7]; T7 = DS0[7]
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7
def sa(i): return SAX[i+4]
def say(i): return SAY[i+4]
def sex(i): return SEX[i+4]
def sey(i): return SEY[i+4]

def variant(a0, a1, a2):
    """Per member: A[0..15], E[4..15], W[8..15] (x: member x); E4..E6 and W8..W10 recomputed from (A0,A1,A2)."""
    out = []
    for (Aa, Ee, Ww) in ((SAX, SEX, SWX), (SAY, SEY, SWY)):
        A = {i: Aa[i+4] for i in range(16)}; A[0], A[1], A[2] = a0, a1, a2
        E = {i: Ee[i+4] for i in range(0, 16)}
        for i in (4, 5, 6): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        W = {i: Ww[i] for i in range(8, 16)}
        for i in (8, 9, 10): W[i] = (E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M
        out.append((A, E, W))
    return out

def valid(var):
    """E cells of rows 4..8 (both members, '+' pairs) and the published dW_i, ds0(W_i), i = 8..11."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = var
    for i in range(4, 9):
        if not cellok(1, i, Ex[i], Ey[i]): return False
        if (Ex[i] ^ Ex[i-1]) & PQ[i]: return False
        if i >= 5 and (Ey[i] ^ Ey[i-1]) & PQ[i]: return False
    for i in range(8, 12):
        if (Wy[i] - Wx[i]) & M != DW[i]: return False
        if (s0(Wy[i]) - s0(Wx[i])) & M != DS0[i]: return False
    return True

def c7of(var):
    """W7x = c7 - A_{-1}  (A_{-1} = first word of the chaining value)."""
    (A, E, _), _ = var
    return (E[7] - 2 * A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0]) - S1(E[6]) - CH(E[6], E[5], E[4]) - K[7]) & M

def step2(cv, var):
    """Message words W0..W15 of both members connecting cv to the variant (W0..W7 from Step 2)."""
    res = []
    for m in (0, 1):
        A, E, W = var[m]; A = dict(A); E = dict(E)
        for j in range(4): A[-1-j] = cv[j]; E[-1-j] = cv[4+j]
        for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        w = [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(8)]
        res.append(w + [W[i] for i in range(8, 16)])
    wx, wy = res
    return wx, wy

def yz0(cv, a0):
    """Lemma 5: Y, Z0 for chaining value cv and A0."""
    a, b, c, d, e, f, g, h = cv
    hh = (d - S0(a) - MAJ(a, b, c)) & M; E0 = (a0 + hh) & M
    Y = (-S0(a0) - MAJ(a0, a, b) - g - S1(E0) - CH(E0, e, f) - K[1]) & M
    W0 = (a0 + hh - d - h - S1(e) - CH(e, f, g) - K[0]) & M
    return Y, (W0 + s1(SWX[14])) & M

def c9x_of(a2):
    A6 = sa(6); E6 = (A6 + a2 - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M
    return (sex(9) - 2 * sa(5) + S0(sa(4)) + MAJ(sa(4), sa(3), a2) - S1(sex(8)) - CH(sex(8), sex(7), E6) - K[9]) & M

def w16_closed(cv, a0, a1, a2):
    Y, Z0 = yz0(cv, a0)
    return (s0((Y + a1) & M) - a1 + Z0 + c9x_of(a2)) & M

def pair_traces(cv, var):
    wx, wy = step2(cv, var)
    return trace(cv, wx), trace(cv, wy), wx, wy

def outcome(cv, a0, a1, a2, rows=NR):
    """Reference outcome of variant (a0, a1, a2) on cv: dict(r16, w7, deep, tx, ty, wx, wy); deep = last row reached
    (row 15 if row 16 fails)."""
    var = variant(a0, a1, a2)
    tx, ty, wx, wy = pair_traces(cv, var)
    r16 = rowok(tx, ty, 16)
    deep = 15
    if r16:
        deep = 16
        for i in range(17, rows):
            if not rowok(tx, ty, i): break
            deep = i
    return dict(r16=r16, w7=inF7(wx[7]), deep=deep, tx=tx, ty=ty, wx=wx, wy=wy, var=var)

def digest_words(msg2blocks): raise NotImplementedError


# ---------------------------------------------------------------------------------------------------------------
# The counted online program: 256-bit word RAM, cost 1 per executed add, sub, rsub, and, or, xor, shl, shr, ld, ldi, sti, st, li, rand, jmp;
# 2 per conditional branch; f38 (one target compression) costs 1 unit; obs, mark, succ, halt are observers and cost nothing.  32-bit values
# live in the low half of a register; bits above bit 31 are garbage unless stated (additions and subtractions carry upward only; a value
# is masked before any rotation, address use or comparison with a mask-free word).
WORD = (1 << 256) - 1
TAG = lambda t: t << 150
HDR, ENT, A2T, GT = TAG(1), TAG(2), TAG(3), TAG(4)
SENT = (1 << 34) + (1 << 32)       # sentinel word 0 of an entry: SENT - a lies in (2^34, 2^34 + 2^32] -> F7 table value 2
EMPTY = ENT                         # address of the shared sentinel entry (empty bucket)
ESZ = 3                             # words per entry: c7 + 2^32 | A1 + S0(A1) << 32 + A2-record address << 64 | G-record address

class Asm:
    def __init__(s): s.c = []; s.lab = {}; s.n = 0
    def __call__(s, *ins): s.c.append(ins)
    def L(s, nm): s.lab[nm] = len(s.c)
    def new(s, p='L'): s.n += 1; return '%s%d' % (p, s.n)

def rot32(a, d, x, n1, n2, n3, shr3=False, t1='t1', t2='t2', D='D'):
    """d = ROTR(x,n1) ^ ROTR(x,n2) ^ (SHR(x,n3) if shr3 else ROTR(x,n3)) in the low 32 bits (garbage above); x masked.
    The doubled word D = x | x << 32 makes a rotation one shift: 7 operations."""
    a('shl', D, x, 32); a('or', D, D, x)
    a('shr', t1, D, n1); a('shr', t2, D, n2); a('xor', t1, t1, t2)
    a('shr', t2, x if shr3 else D, n3); a('xor', d, t1, t2)

# ---------------------------------------------------------------------------------------------------------------
# Records served by the preprocessing (tables of the machine): A2 records (2 words) and G records (8 words).
def tables(a2list=None, glist=None):
    """A2 record i at A2T + 2i: word 0 = A2 | (W10x + s1(W15x)) << 32 | S0(A2) << 64 | E6 << 96 | (E5 - A1) << 128;
    word 1 = c9x | c9y << 32 | W10x << 64 | W10y << 96.  G record g at GT + 8g: c17, mE, vE, a17, mA, vA, e16/a16 of
    member x (e16, a16), of member y (e16y, a16y) (see gen below)."""
    a2list = A2L if a2list is None else a2list; glist = GL if glist is None else glist
    mem = {}
    for k, a2 in enumerate(a2list):
        var = variant(sa(0), sa(1), a2); (Ax, Ex, Wx), (Ay, Ey, Wy) = var
        e5b = (sa(5) - S0(sa(4)) - MAJ(sa(4), sa(3), a2)) & M
        cx = c9x_of(a2); cy = (cx + DW[9]) & M
        mem[A2T + 2*k] = a2 | ((Wx[10] + s1(SWX[15])) & M) << 32 | S0(a2) << 64 | Ex[6] << 96 | e5b << 128
        mem[A2T + 2*k + 1] = cx | cy << 32 | Wx[10] << 64 | Wy[10] << 96
    for gi, g in enumerate(glist): mem.update(grec(gi, g))
    return mem

def grec(gi, g):
    """G record for W16x = g: row-16 states, the E17/A17 tests of member x.  Conditions of row 17 that tie it to row 16
    (two-bit conditions with an operand at row 16, the '+' pair) become masks over E17/A17."""
    rec = []
    for m, (Aa, Ee) in enumerate(((SAX, SEX), (SAY, SEY))):
        A = lambda i: Aa[i+4]; E = lambda i: Ee[i+4]
        w16 = g if m == 0 else (g - DW16) & M
        e16 = (A(12) + E(12) + S1(E(15)) + CH(E(15), E(14), E(13)) + K[16] + w16) & M
        a16 = (e16 - A(12) + S0(A(15)) + MAJ(A(15), A(14), A(13))) & M
        c17 = (A(13) + E(13) + S1(e16) + CH(e16, E(15), E(14)) + K[17]) & M
        a17 = (-A(13) + S0(a16) + MAJ(a16, A(15), A(14))) & M
        rec.append((e16, a16, c17, a17))
    (e16, a16, c17, a17), (e16y, a16y, _, _) = rec
    mE, vE, dE, _ = CELLS[1][17]; mA, vA, dA, _ = CELLS[0][17]
    assert dE == 0
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == 17 and i1 == 16 and i2 == 17:
            bit = (((e16 if k1 == 1 else a16) >> b1) & 1) ^ (0 if eq else 1)
            if k2 == 1:
                assert not (mE >> b2) & 1 or (vE >> b2) & 1 == bit, 'conflicting E17 conditions'
                mE |= 1 << b2; vE |= bit << b2
            else:
                assert not (mA >> b2) & 1 or (vA >> b2) & 1 == bit, 'conflicting A17 conditions'
                mA |= 1 << b2; vA |= bit << b2
    p = PQ[17]; assert not (mE & p) or (vE & p) == (e16 & p & mE), 'conflicting E17 pair'
    mE |= p; vE |= e16 & p
    base = GT + 16 * gi
    return {base: c17, base+1: mE, base+2: vE, base+3: a17, base+4: mA, base+5: vA, base+6: g, base+7: 0,
            base+8: a16, base+9: e16, base+10: a16y, base+11: e16y}

def gaddr(gi): return GT + 16 * gi

# internal conditions of row 17 between bits of A17 only (both operands at row 17, kind A)
def a17int():
    r = [(b1, b2, eq) for (k1, i1, b1, eq, k2, i2, b2, row) in X2 if row == 17 and i1 == 17 and i2 == 17 and k1 == 0 and k2 == 0]
    return r

def f7_value(addr):
    if addr < (1 << 33): return 1 if inF7(addr & M) else 0
    if (1 << 34) < addr <= SENT: return 2
    raise ValueError('bad F7-region address %x' % addr)

# ---------------------------------------------------------------------------------------------------------------
# The program.
def gen_prologue(a):
    """Group prologue: two random words -> M0 (16 words), CV1 = F38(IV, M0), per-CV values."""
    a('rand', 'r0'); a('rand', 'r1')
    for k in range(16):
        r = 'r0' if k < 8 else 'r1'; s_ = 32 * (k % 8)
        if s_: a('shr', 'm%d' % k, r, s_); a('and', 'm%d' % k, 'm%d' % k, M)
        else: a('and', 'm%d' % k, r, M)
    a('f38', ['m%d' % k for k in range(16)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    # hh = d - S0(a) - MAJ(a,b,c)
    rot32(a, 'S0a', 'a', 2, 13, 22)
    a('and', 't1', 'a', 'b'); a('or', 't2', 'a', 'b'); a('and', 't2', 't2', 'c'); a('or', 't1', 't1', 't2')
    a('sub', 'hh', 'd', 'S0a'); a('sub', 'hh', 'hh', 't1')
    # y0p = hh - d - h - S1(e) - CH(e,f,g) + s1(W14) - K0  (Z0 = y0p + A0)
    rot32(a, 'S1e', 'e', 6, 11, 25)
    a('xor', 't1', 'f', 'g'); a('and', 't1', 't1', 'e'); a('xor', 't1', 't1', 'g')
    a('sub', 'y0p', 'hh', 'd'); a('sub', 'y0p', 'y0p', 'h'); a('sub', 'y0p', 'y0p', 'S1e'); a('sub', 'y0p', 'y0p', 't1')
    a('add', 'y0p', 'y0p', (s1(SWX[14]) - K[0]) & M); a('and', 'y0p', 'y0p', M)
    a('xor', 'abx', 'a', 'b'); a('and', 'aba', 'a', 'b'); a('xor', 'efx', 'e', 'f')
    a('add', 'gk', 'g', K[1]); a('and', 'gk', 'gk', M); a('add', 'fk', 'f', K[2])
    a('and', 'hhm', 'hh', M)
    # broadcast of the per-CV values into the four 64-bit lanes of a register (lane k = block 4q + k)
    for src, dst in (('hhm', 'hh_v'), ('y0p', 'y0p_v'), ('abx', 'abx_v'), ('aba', 'aba_v'), ('efx', 'efx_v'), ('f', 'f_v'), ('gk', 'gk_v')):
        a('shl', 'bt', src, 64); a('or', dst, src, 'bt'); a('shl', 'bt', dst, 128); a('or', dst, dst, 'bt')
    # per-CV values of the deep path

LM = sum(M << (64 * k) for k in range(4)); LM64 = (1 << 64) - 1

def gen_group(a, js, rare):
    """Up to four consecutive A0 blocks (lane k = block js[k]).  The per-CV values are broadcast into the lanes of 256-bit
    registers; E0, S1(E0), CH, MAJ, Y, Z0 and the header index (Y << 32 | Z0) of all lanes cost 23 operations
    (additions cannot carry across lanes: lane values stay below 2^36 thanks to a bias on the subtractions).  Each lane then
    extracts its header address, loads the header and scans its bucket (3 words per entry, sentinel-terminated)."""
    a0s = [A0L[j] for j in js]
    pk = lambda vals: sum(v << (64 * k) for k, v in enumerate(vals))
    a0v = pk(a0s); nsb = pk([((-S0(x)) & M) + (1 << 35) for x in a0s])
    a('add', 'E0v', 'hh_v', a0v); a('and', 'E0v', 'E0v', LM)
    rot32(a, 'S1v', 'E0v', 6, 11, 25); a('and', 'S1v', 'S1v', LM)
    a('and', 'Chv', 'E0v', 'efx_v'); a('xor', 'Chv', 'Chv', 'f_v')
    a('and', 'Mjv', 'abx_v', a0v); a('xor', 'Mjv', 'Mjv', 'aba_v')
    a('rsub', 'Yv', nsb, 'Mjv'); a('sub', 'Yv', 'Yv', 'S1v'); a('sub', 'Yv', 'Yv', 'Chv'); a('sub', 'Yv', 'Yv', 'gk_v'); a('and', 'Yv', 'Yv', LM)
    a('add', 'Zv', 'y0p_v', a0v); a('and', 'Zv', 'Zv', LM)
    a('shl', 'Vv', 'Yv', 32); a('or', 'Vv', 'Vv', 'Zv')
    for k, j in enumerate(js):
        loop, pas = a.new('loop'), a.new('pass')
        if k == 0: a('and', 'I', 'Vv', LM64)
        elif k == 3: a('shr', 'I', 'Vv', 192)
        else: a('shr', 'I', 'Vv', 64 * k); a('and', 'I', 'I', LM64)
        a('add', 'I', 'I', HDR | (j << 64)); a('ld', 'H', 'I')
        a('add', 'OFF', 'H', 0)
        a.L(loop)
        a('ld', 'EN', 'OFF'); a('sub', 'W7', 'EN', 'a'); a('ld', 'FL', 'W7'); a('add', 'OFF', 'OFF', ESZ); a('bz', 'FL', loop)
        a('sub', 'T', 'FL', 1); a('bz', 'T', pas)
        a('sub', 'T', 'OFF', 'H'); a('add', 'NE', 'NE', 'T')
        rare.append((j, a0s[k], pas, loop, k))

def lane_get(a, dst, src, k):
    """dst = 32-bit value of lane k of the clean vector register src"""
    if k == 0: a('and', dst, src, M)
    elif k == 3: a('shr', dst, src, 192)
    else: a('shr', dst, src, 64 * k); a('and', dst, dst, M)

def gen_rare(a, j, a0, pas, loop, lane):
    a.L(pas); a('add', 'NW', 'NW', 1); a('mark', 'W7')
    lane_get(a, 'Y', 'Yv', lane); lane_get(a, 'Mj', 'Mjv', lane); lane_get(a, 'E0', 'E0v', lane)
    a('sub', 't1', 'OFF', 2); a('ld', 'w1', 't1')                       # A1 | S0(A1) << 32 | A2-record address << 64
    a('shr', 'P2', 'w1', 64); a('ld', 'A2r', 'P2')
    a('add', 'W1', 'Y', 'w1')                                           # W1 = Y + A1 (garbage above bit 31)
    a('add', 'E1', 'w1', 'c'); a('sub', 'E1', 'E1', 'Mj'); a('add', 'E1', 'E1', (-S0(a0)) & M); a('and', 'E1', 'E1', M)
    rot32(a, 'S1E1', 'E1', 6, 11, 25)
    a('xor', 't1', 'E0', 'e'); a('and', 't1', 't1', 'E1'); a('xor', 'ChE1', 't1', 'e')
    a('shr', 'S0A1', 'w1', 32)
    a('xor', 't1', 'a', a0); a('and', 't1', 't1', 'w1'); a('and', 't2', 'a', a0); a('xor', 'MjA1', 't1', 't2')
    a('sub', 'E2x', 'A2r', 'S0A1'); a('sub', 'E2x', 'E2x', 'MjA1')     # E2 - b = A2 - S0(A1) - MAJ(A1, A0, A_-1)
    a('sub', 'W2', 'E2x', 'fk'); a('sub', 'W2', 'W2', 'S1E1'); a('sub', 'W2', 'W2', 'ChE1'); a('and', 'W2', 'W2', M)
    rot32(a, 's0W2', 'W2', 7, 18, 3, shr3=True)
    a('shr', 'K10', 'A2r', 32)
    a('add', 'W17', 's0W2', 'K10'); a('add', 'W17', 'W17', 'W1')
    a('obs', 'W17')
    a('sub', 't1', 'OFF', 1); a('ld', 'PG', 't1')                      # G record address
    a('ld', 'cG', 'PG'); a('add', 'E17', 'W17', 'cG'); a('obs', 'E17')
    a('add', 't1', 'PG', 1); a('ld', 'mE', 't1'); a('add', 't1', 'PG', 2); a('ld', 'vE', 't1')
    a('and', 't1', 'E17', 'mE'); a('bne', 't1', 'vE', loop)
    a('mark', 'E17')
    a('add', 'N1', 'N1', 1)
    a('add', 't1', 'PG', 3); a('ld', 't1', 't1'); a('add', 'A17', 'E17', 't1')
    a('add', 't1', 'PG', 4); a('ld', 'mA', 't1'); a('add', 't1', 'PG', 5); a('ld', 'vA', 't1')
    a('and', 't1', 'A17', 'mA'); a('bne', 't1', 'vA', loop)
    a('mark', 'A17')
    # A17 internal conditions A17[b1] = A17[b2]: OR of the three xors tested once
    for n_, (b1, b2, eq) in enumerate(a17int()):
        d_ = 't3' if n_ == 0 else 't1'
        a('shr', d_, 'A17', b1 - b2) if b1 >= b2 else a('shl', d_, 'A17', b2 - b1)
        a('xor', d_, d_, 'A17'); a('and', d_, d_, 1 << b2)
        if not eq: a('xor', d_, d_, 1 << b2)
        if n_: a('or', 't3', 't3', 't1')
    a('bnz', 't3', loop)
    a('mark', 'A17int')
    gen_deep(a, j, a0, loop)

def gen_deep(a, j, a0, loop):
    """Rows 18..37 of both members.  Member y: W_i^y = W_i^x + dW_i (modular differences of valid variants), rows 16/17
    from the G record (A17^y = A17^x - 2^29).  Words go through scratch memory (direct addresses)."""
    S = lambda m, k, i: (6 << 150) | (256 * m + 64 * k + i + 8)      # m member, k 0:A 1:E 2:W, i row
    def st(r, m, k, i): a('sti', S(m, k, i), r)
    def ld(r, m, k, i): a('ldi', r, S(m, k, i))
    def imm_st(v, m, k, i): st(v, m, k, i)
    A0 = lambda i: sa(i)
    a('and', 'A1', 'w1', M); a('and', 'A2', 'A2r', M)
    a('and', 'W17', 'W17', M); a('and', 'E17', 'E17', M); a('and', 'A17', 'A17', M)
    # E2 = A2 + b - S0(A1) - MAJ(A1,A0,a), masked; E3, E4, E5, E6
    a('and', 'S0A1', 'S0A1', M)
    a('add', 'E2', 'E2x', 'b'); a('and', 'E2', 'E2', M)
    a('shr', 'S0A2', 'A2r', 64); a('and', 'S0A2', 'S0A2', M)
    a('xor', 't1', 'A1', a0); a('and', 't1', 't1', 'A2'); a('and', 't2', 'A1', a0); a('xor', 't1', 't1', 't2')   # MAJ(A2,A1,A0) up to the shared bitwise form
    # MAJ(A2,A1,A0) = (A2 & (A1^A0)) ^ (A1 & A0)
    a('add', 'E3', 'a', A0(3)); a('sub', 'E3', 'E3', 'S0A2'); a('sub', 'E3', 'E3', 't1'); a('and', 'E3', 'E3', M)
    def wstep(dst, Ei, Ai4, Ei4, Em1, Em2, Em3, k):
        rot32(a, 'S1t', Em1, 6, 11, 25)
        a('xor', 't3', Em2, Em3); a('and', 't3', 't3', Em1); a('xor', 't3', 't3', Em3)
        a('sub', dst, Ei, Ai4); a('sub', dst, dst, Ei4); a('sub', dst, dst, 'S1t'); a('sub', dst, dst, 't3')
        a('add', dst, dst, (-K[k]) & M); a('and', dst, dst, M)
    wstep('W3', 'E3', 'a', 'e', 'E2', 'E1', 'E0', 3)
    a('xor', 't1', 'A1', A0(3)); a('and', 't1', 't1', 'A2'); a('and', 't2', 'A1', A0(3)); a('xor', 't1', 't1', 't2')
    a('rsub', 'E4', (A0(4) + a0 - S0(A0(3))) & M, 't1'); a('and', 'E4', 'E4', M)
    wstep('W4', 'E4', a0, 'E0', 'E3', 'E2', 'E1', 4)
    a('shr', 'E5', 'A2r', 128); a('and', 'E5', 'E5', M); a('add', 'E5', 'E5', 'A1'); a('and', 'E5', 'E5', M)
    wstep('W5', 'E5', 'A1', 'E1', 'E4', 'E3', 'E2', 5)
    a('shr', 'E6', 'A2r', 96); a('and', 'E6', 'E6', M)
    wstep('W6', 'E6', 'A2', 'E2', 'E5', 'E4', 'E3', 6)
    a('sub', 'W7x', 'EN', 'a'); a('and', 'W7x', 'W7x', M)
    # W8 of member x = E8 - A4 - E4 - S1(E7) - CH(E7,E6,E5) - K8
    a('xor', 't3', 'E6', 'E5'); a('and', 't3', 't3', sex(7)); a('xor', 't3', 't3', 'E5')
    a('rsub', 't1', (sex(8) - sa(4) - S1(sex(7)) - K[8]) & M, 'E4'); a('sub', 't1', 't1', 't3'); a('and', 'W8x', 't1', M)
    a('add', 'P3', 'P2', 1); a('ld', 'A2r2', 'P3')               # c9x | c9y << 32 | W10x << 64 | W10y << 96
    a('and', 'W9x', 'A2r2', M); a('sub', 'W9x', 'W9x', 'A1'); a('and', 'W9x', 'W9x', M)
    a('shr', 'W10x', 'A2r2', 64); a('and', 'W10x', 'W10x', M)
    # scratch: W2..W17, E/A rows 14..17 of both members
    ws = {2: 'W2', 3: 'W3', 4: 'W4', 5: 'W5', 6: 'W6', 7: 'W7x', 8: 'W8x', 9: 'W9x', 10: 'W10x'}
    for i, r in ws.items():
        st(r, 0, 2, i)
        if DW[i] == 0: st(r, 1, 2, i)
        else: a('add', 'u0', r, DW[i]); a('and', 'u0', 'u0', M); st('u0', 1, 2, i)
    for i in range(11, 16):
        imm_st(SWX[i], 0, 2, i); imm_st(SWY[i], 1, 2, i)
    a('add', 'P3', 'PG', 6); a('ld', 'u1', 'P3'); st('u1', 0, 2, 16); a('add', 'u1', 'u1', DW[16]); a('and', 'u1', 'u1', M); st('u1', 1, 2, 16)
    st('W17', 0, 2, 17); st('W17', 1, 2, 17)
    for m, (Aa, Ee) in enumerate(((SAX, SEX), (SAY, SEY))):
        for i in (14, 15):
            imm_st(Aa[i+4], m, 0, i); imm_st(Ee[i+4], m, 1, i)
        a('add', 'P3', 'PG', 8 + 2 * m); a('ld', 'u1', 'P3'); st('u1', m, 0, 16)
        a('add', 'P3', 'PG', 9 + 2 * m); a('ld', 'u1', 'P3'); st('u1', m, 1, 16)
    st('A17', 0, 0, 17); st('E17', 0, 1, 17); st('E17', 1, 1, 17)
    a('sub', 'u1', 'A17', DW16); a('and', 'u1', 'u1', M); st('u1', 1, 0, 17)
    for i in range(18, NR):
        a('mark', ('row', i))
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
            if m == 0:
                # member x tests that need no member y: x-value cells, '+' pair, two-bit conditions
                for k, xr in ((0, 'ai'), (1, 'ei'), (2, 'wi')):
                    msk, val, _, _ = CELLS[k][i]
                    if msk:
                        a('and', 't1', xr, msk)
                        a('bne', 't1', val, loop) if val else a('bnz', 't1', loop)
                if PQ[i]:
                    ld('t2', 0, 1, i - 1); a('xor', 't1', 'ei', 't2'); a('and', 't1', 't1', PQ[i]); a('bnz', 't1', loop)
                for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
                    if row != i: continue
                    ld('t1', 0, k1, i1); ld('t2', 0, k2, i2)
                    a('shr', 't1', 't1', b1); a('shr', 't2', 't2', b2); a('xor', 't1', 't1', 't2'); a('and', 't1', 't1', 1)
                    a('bne', 't1', 0 if eq else 1, loop) if not eq else a('bnz', 't1', loop)
                a('add', 'xa', 'ai', 0); a('add', 'xe', 'ei', 0); a('add', 'xw', 'wi', 0)
        # XOR differences x^y of row i
        for k, xr, yr in ((0, 'xa', 'ai'), (1, 'xe', 'ei'), (2, 'xw', 'wi')):
            d = CELLS[k][i][2]
            a('xor', 't1', xr, yr)
            a('bne', 't1', d, loop) if d else a('bnz', 't1', loop)
    a('succ', j, 'EN')

# ---------------------------------------------------------------------------------------------------------------
def gen_epilogue(a, caps):
    """After every group: halt when a work counter exceeds its cap; group counter; loop."""
    halt = a.new('halt')
    for r, cap in zip(('NE', 'NW', 'N1'), caps):
        a('rsub', 't1', cap, r); a('shr', 't1', 't1', 255); a('bnz', 't1', halt)
    a('add', 'NG', 'NG', 1)
    a.pending = halt

def build_program(js, caps=(1 << 200,) * 3, ngroups=1):
    a = Asm(); a.L('group'); gen_prologue(a); rare = []
    js = list(js)
    for q in range(0, len(js), 4): gen_group(a, js[q:q + 4], rare)
    gen_epilogue(a, caps)
    a('bne', 'NG', ngroups, 'group'); a.L(a.pending); a('halt_ok',)
    for r in rare: gen_rare(a, *r)
    return a

class Machine:
    def __init__(s, randwords, bucket, tabmem, cvforce=None, a0map=None):
        s.rw = list(randwords); s.bucket = bucket; s.tab = dict(tabmem); s.cvforce = cvforce
        s.r = {}; s.ops = 0; s.units = 0; s.mem = {}; s.ent = {}; s.nent = 0; s.succ = None; s.cv = None; s.obs = []
        s.marks = []; s.trace = []; s.opc = {}; s.mark_ops = []; s.succ_ops = None
        s.ent[EMPTY] = SENT; s.ent[EMPTY + 1] = 0; s.ent[EMPTY + 2] = 0; s.nent = ESZ
    def store(s, addr, val): s.mem[addr] = val
    def load(s, addr):
        t = addr >> 150
        if t == 0: return f7_value(addr)
        if t == 1:
            j, idx = (addr >> 64) & ((1 << 86) - 1), addr & ((1 << 64) - 1)
            es = s.bucket(j, idx >> 32, idx & M); s.trace.append((j, idx >> 32, idx & M, len(es)))
            if not es: return EMPTY
            base = ENT + s.nent
            for k, e in enumerate(es):
                for w in range(ESZ): s.ent[base + ESZ * k + w] = e[w]
            end = base + ESZ * len(es)
            s.ent[end] = SENT; s.ent[end + 1] = 0; s.ent[end + 2] = 0
            s.nent += ESZ * (len(es) + 1); return base
        if t == 2: return s.ent[addr]
        if t in (3, 4): return s.tab[addr]
        raise ValueError('load %x' % addr)
    def run(s, code, maxops=None):
        c, lab, r = code.c, code.lab, s.r; pc = 0; n = len(c); mem = s.mem
        def v(x): return x if isinstance(x, int) else r.get(x, 0)
        ops = 0
        while pc < n:
            ins = c[pc]; op = ins[0]; pc += 1
            if op == 'add': r[ins[1]] = (v(ins[2]) + v(ins[3])) & WORD; ops += 1
            elif op == 'sub': r[ins[1]] = (v(ins[2]) - v(ins[3])) & WORD; ops += 1
            elif op == 'rsub': r[ins[1]] = (ins[2] - v(ins[3])) & WORD; ops += 1
            elif op == 'and': r[ins[1]] = v(ins[2]) & v(ins[3]); ops += 1
            elif op == 'or': r[ins[1]] = v(ins[2]) | v(ins[3]); ops += 1
            elif op == 'xor': r[ins[1]] = v(ins[2]) ^ v(ins[3]); ops += 1
            elif op == 'shl': r[ins[1]] = (v(ins[2]) << ins[3]) & WORD; ops += 1
            elif op == 'shr': r[ins[1]] = v(ins[2]) >> ins[3]; ops += 1
            elif op == 'ld': r[ins[1]] = s.load(v(ins[2])); ops += 1
            elif op == 'ldi': r[ins[1]] = mem.get(ins[2], 0); ops += 1
            elif op == 'sti': mem[ins[1]] = v(ins[2]); ops += 1
            elif op == 'li': r[ins[1]] = ins[2]; ops += 1
            elif op == 'st': s.store(v(ins[1]), v(ins[2])); ops += 1
            elif op == 'bz': ops += 2; pc = lab[ins[2]] if v(ins[1]) == 0 else pc
            elif op == 'bnz': ops += 2; pc = lab[ins[2]] if v(ins[1]) != 0 else pc
            elif op == 'bne': ops += 2; pc = lab[ins[3]] if v(ins[1]) != v(ins[2]) else pc
            elif op == 'jmp': ops += 1; pc = lab[ins[1]]
            elif op == 'rand': r[ins[1]] = s.rw.pop(0); ops += 1
            elif op == 'f38':
                s.units += 1; m0 = [r[x] for x in ins[1]]; s.m0 = m0
                cv = s.cvforce if s.cvforce is not None else compress(IV, m0); s.cv = cv
                for x, y in zip(ins[2], cv): r[x] = y
            elif op == 'succ': s.succ = (ins[1], v(ins[2])); s.succ_ops = s.ops + ops; break
            elif op == 'halt_ok': break
            elif op == 'obs': s.obs.append(v(ins[1]))
            elif op == 'mark': s.marks.append(ins[1]); s.mark_ops.append((ins[1], s.ops + ops))
            elif op == 'succ_': pass
            else: raise ValueError(op)
        s.ops += ops

# ---------------------------------------------------------------------------------------------------------------
# Register allocation: liveness on the control-flow graph, greedy colouring with k registers.
def _du(ins):
    op = ins[0]; S = lambda x: [x] if isinstance(x, str) else []
    if op in ('add', 'sub', 'and', 'or', 'xor'): return [ins[1]], S(ins[2]) + S(ins[3])
    if op == 'rsub': return [ins[1]], S(ins[3])
    if op in ('shl', 'shr', 'ld'): return [ins[1]], S(ins[2])
    if op in ('ldi', 'rand', 'li'): return [ins[1]], []
    if op == 'sti': return [], S(ins[2])
    if op == 'st': return [], S(ins[1]) + S(ins[2])
    if op in ('bz', 'bnz'): return [], [ins[1]]
    if op == 'bne': return [], S(ins[1]) + S(ins[2])
    if op == 'f38': return list(ins[2]), list(ins[1])
    if op in ('succ',): return [], S(ins[2])
    if op == 'obs': return [], S(ins[1])
    return [], []

def regalloc(a, k=64):
    c, lab = a.c, a.lab; n = len(c); succ = []
    for pc, ins in enumerate(c):
        op = ins[0]
        if op == 'jmp': succ.append([lab[ins[1]]])
        elif op in ('bz', 'bnz'): succ.append([pc + 1, lab[ins[2]]])
        elif op == 'bne': succ.append([pc + 1, lab[ins[3]]])
        elif op in ('succ', 'halt_ok'): succ.append([])
        else: succ.append([pc + 1] if pc + 1 < n else [])
    du = [_du(ins) for ins in c]; live = [frozenset()] * (n + 1); changed = True
    while changed:
        changed = False
        for pc in range(n - 1, -1, -1):
            out = set().union(*[live[s_] for s_ in succ[pc]]) if succ[pc] else set()
            d, u = du[pc]; inn = frozenset((out - set(d)) | set(u))
            if inn != live[pc]: live[pc] = inn; changed = True
    adj = {}
    for pc in range(n):
        out = set().union(*[live[s_] for s_ in succ[pc]]) if succ[pc] else set()
        for d in du[pc][0]:
            adj.setdefault(d, set())
            for x in out:
                if x != d: adj[d].add(x); adj.setdefault(x, set()).add(d)
        for u in du[pc][1]: adj.setdefault(u, set())
    col = {}
    for v in sorted(adj, key=lambda v: (-len(adj[v]), v)):
        used = {col[x] for x in adj[v] if x in col}
        col[v] = min(r for r in range(k + 1) if r not in used)
        if col[v] >= k: raise ValueError('more than %d registers needed' % k)
    return {v: 'R%d' % r for v, r in col.items()}

def rename(a, mp):
    b = Asm(); b.lab = dict(a.lab); b.n = a.n
    def rn(x): return mp.get(x, x) if isinstance(x, str) else x
    for ins in a.c:
        if ins[0] == 'mark': b.c.append(ins); continue
        b.c.append(tuple([ins[0]] + [([rn(y) for y in x] if isinstance(x, list) else rn(x)) for x in ins[1:]]))
    return b

def allocated_program(js, caps=(1 << 200,) * 3, ngroups=1, _cache={}):
    if 'map' not in _cache:
        t = build_program(list(range(8))); _cache['map'] = regalloc(t)
    return rename(build_program(js, caps, ngroups), _cache['map']), _cache['map']



# ---------------------------------------------------------------------------------------------------------------
# Organizer experiments.  Randomness: SHAKE-256 of (experiment id | trial seed).
class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def word(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def u32(self): return self.word() & M
    def below(self, n): return self.word() % n

def dec(b64): return zlib.decompress(base64.b64decode(b64))
def sample_variants():
    b = dec(S512_B64); return [struct.unpack_from('<BIH', b, 7 * k) for k in range(len(b) // 7)]       # (A0 index, A1, A2 index)
def entry_variants():
    b = dec(E256_B64); return [struct.unpack_from('<IH', b, 6 * k) for k in range(256)]                  # per A0 index: (A1, A2 index) valid

def rebuild(P, v, w23):
    """Rebuild a tail success into a real semi-free-start pair: W0..W6 by the inverse expansion, CV1 by inverting steps 7..0 of the
    variant.  Returns (cv, mx, my) iff F38(CV1, M1) = F38(CV1, M1'), M1 != M1', the pair holds every cell of rows 0..37 (the W cells of rows
    7..10 excepted: they reach rows >= 16 only through the modular differences), W7 is in F7 and the Step-2 words of (CV1, variant) are
    W0..W7."""
    a0, a1, a2 = v
    var = variant(a0, a1, a2); (A, E, Wv), (Ay_, Ey_, Wvy) = var
    W = {i: Wv[i] for i in range(8, 16)}
    for i in range(16, 23): W[i] = P[2][i]
    W[23] = w23; W[7] = (W[23] - s1(W[21]) - W[16] - s0(W[8])) & M; W[6] = (W[22] - s1(W[20]) - W[15] - s0(W[7])) & M
    W[5] = (W[21] - s1(W[19]) - W[14] - s0(W[6])) & M; W[4] = (W[20] - s1(W[18]) - W[13] - s0(W[5])) & M
    W[3] = (W[19] - s1(W[17]) - W[12] - s0(W[4])) & M; W[2] = (W[18] - s1(W[16]) - W[11] - s0(W[3])) & M
    W[1] = (W[17] - s1(W[15]) - W[10] - s0(W[2])) & M; W[0] = (W[16] - s1(W[14]) - W[9] - s0(W[1])) & M
    Aa = {i: A[i] for i in range(8)}; Ea = {i: E[i] for i in range(4, 8)}
    for i in range(7, -1, -1):
        Aa[i-4] = (Ea[i] - Aa[i] + S0(Aa[i-1]) + MAJ(Aa[i-1], Aa[i-2], Aa[i-3])) & M
        Ea[i-4] = (Ea[i] - Aa[i-4] - S1(Ea[i-1]) - CH(Ea[i-1], Ea[i-2], Ea[i-3]) - K[i] - W[i]) & M
    cv = [Aa[-1], Aa[-2], Aa[-3], Aa[-4], Ea[-1], Ea[-2], Ea[-3], Ea[-4]]
    mx = [W[i] for i in range(16)]; my = list(mx)
    for i in range(7, 16): my[i] = (mx[i] + DW[i]) & M
    if mx == my or compress(cv, mx) != compress(cv, my) or not inF7(mx[7]): return None
    tx, ty = trace(cv, mx), trace(cv, my)
    if not all(rowok(tx, ty, i) for i in range(NR)): return None
    if step2(cv, var)[0][:8] != mx[:8]: return None
    return cv, mx, my

# ---- vt-q3-smc-r38: a reduced replicate of the preregistered SMC estimator of q3 ----
NP_R, CH_R, NT_R = 64, (128, 4, 4, 1, 1, 1), 512
def smc_replicate(rng, VAR):
    """One replicate: row 16 exact (32 words of G), rows 17..22 by proposals with the E-cell and '+' bits imposed, tail with the W23
    x-value cells imposed and W7 in F7, rows 23..37 deterministic.  Returns (log2 estimate or None, accepted pairs, failed rebuilds)."""
    lg = [-27.0]; P = []; VW = {}
    for _ in range(NP_R):
        w = GL[rng.below(32)]; Ax = {i: sa(i) for i in range(16)}; Ex = {i: sex(i) for i in range(16)}; Wx = {i: SWX[i] for i in range(16)}
        Ay = {i: say(i) for i in range(16)}; Ey = {i: sey(i) for i in range(16)}; Wy = {i: SWY[i] for i in range(16)}
        Wx[16] = w; Wy[16] = (w + DW[16]) & M
        for (A, E, W) in ((Ax, Ex, Wx), (Ay, Ey, Wy)): step_row(A, E, W, 16)
        P.append((Ax, Ex, Wx, Ay, Ey, Wy))
    for i in range(17, 23):
        cm, cvv, _, _ = CELLS[1][i]; pq = PQ[i]; imp = cm | pq; f = bin(imp).count('1'); Mi = CH_R[i - 17]; surv = []
        xs = [x for x in X2 if x[7] == i]
        for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
            rx = (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i]) & M
            ry = (Ay[i-4] + Ey[i-4] + S1(Ey[i-1]) + CH(Ey[i-1], Ey[i-2], Ey[i-3]) + K[i]) & M
            fixed = cvv | (Ex[i-1] & pq & ~cm & M)
            for _ in range(Mi):
                e = (rng.u32() & ~imp & M) | fixed
                Wxi = (e - rx) & M; Wyi = (Wxi + DW[i]) & M
                nA = {**Ax}; nE = {**Ex}; nW = {**Wx}; mA = {**Ay}; mE = {**Ey}; mW = {**Wy}
                nW[i] = Wxi; mW[i] = Wyi; step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if nE[i] == e and row_hold((nA, nE, nW), (mA, mE, mW), i): surv.append((nA, nE, nW, mA, mE, mW))
        if not surv: return None, [], 0
        lg.append(__import__('math').log2(len(surv) / (len(P) * Mi)) - f)
        P = [surv[rng.below(len(surv))] for _ in range(NP_R)]
    cm, cvv, _, _ = CELLS[2][23]; rel23 = [x for x in X2 if x[7] == 23]
    # W23 is proposed uniformly among the words that hold the x-value cell and the four two-bit conditions of row 23 (f imposed bits)
    imposed = cm; plan = []
    for (k1, i1, b1, eq, k2, i2, b2, row) in rel23:
        if not (imposed >> b2) & 1: plan.append((b1, b2, 0 if eq else 1)); imposed |= 1 << b2
        elif not (imposed >> b1) & 1: plan.append((b2, b1, 0 if eq else 1)); imposed |= 1 << b1
        else: raise ValueError('over-determined row-23 condition')
    tailw = 2.0 ** (32 - bin(imposed).count('1')) / 287309824
    pairs = []; bad = 0; succ = 0
    for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
        for _ in range(NT_R):
            v = VAR[rng.below(len(VAR))]; vv = (A0L[v[0]], v[1], A2L[v[2]])
            if v not in VW: VW[v] = variant(*vv)[0][2]
            vW = VW[v]
            w23 = (rng.u32() & ~cm & M) | cvv
            for (bs, bd, fl) in plan: w23 = (w23 & ~(1 << bd)) | (((w23 >> bs) & 1) ^ fl) << bd
            w7 = (w23 - s1(Wx[21]) - Wx[16] - s0(vW[8])) & M
            if not inF7(w7): continue
            nA = {**Ax}; nE = {**Ex}; nW = {**Wx}; mA = {**Ay}; mE = {**Ey}; mW = {**Wy}
            for i in (8, 9, 10): nW[i] = vW[i]; mW[i] = (vW[i] + DW[i]) & M
            nW[7] = w7; mW[7] = (w7 + DW[7]) & M; ok = True
            for i in range(23, NR):
                nW[i] = w23 if i == 23 else (s1(nW[i-2]) + nW[i-7] + s0(nW[i-15]) + nW[i-16]) & M
                mW[i] = (s1(mW[i-2]) + mW[i-7] + s0(mW[i-15]) + mW[i-16]) & M
                step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if not row_hold((nA, nE, nW), (mA, mE, mW), i): ok = False; break
            if ok:
                succ += 1; r = rebuild((None, None, Wx), vv, w23)
                if r: pairs.append(r + (vv,))
                else: bad += 1
    if succ == 0: return None, pairs, bad
    lg.append(__import__('math').log2(succ * tailw / (NP_R * NT_R)))
    return sum(lg), pairs, bad

def step_row(A, E, W, i):
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M

def row_hold(tx, ty, i):
    """rowok on dict states ((A, E, W) per member): cells, '+' and two-bit conditions of row i (member x)."""
    for k in range(3):
        m, v, d, _ = CELLS[k][i]
        if (tx[k][i] & m) != v or (tx[k][i] ^ ty[k][i]) != d: return False
    if (tx[1][i] ^ tx[1][i-1]) & PQ[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True

Q3_THRESH = -101.35       # log2 threshold of the pass rule on the mean of 20 replicate estimates (proof.md 10.1)
def near_term(cv, a0, a1, a2):
    """Pair term, near part: every other A2' of the list with the same (A0, A1) tried on the same chaining value:
    (valid variants, row-16 co-hits, W7 passes of those, of them the first row-17 test (E17 mask) passes, of them all rows hold)."""
    nv = nh = nw = n17 = ns = 0
    for b2 in A2L:
        if b2 == a2: continue
        var = variant(a0, a1, b2)
        if not valid(var): continue
        nv += 1
        if w16_closed(cv, a0, a1, b2) not in GSET: continue
        nh += 1; o = outcome(cv, a0, a1, b2)
        if not o['w7']: continue
        nw += 1; (tx, ty) = (o['tx'], o['ty'])
        ok = cellok(1, 17, tx[1][17], ty[1][17]) and not (tx[1][17] ^ tx[1][16]) & PQ[17] and all(((tx[1][i1] >> b1) ^ (tx[1][i2] >> b2)) & 1 == (0 if eq else 1) for (k1, i1, b1, eq, k2, i2, b2, row) in X2 if row == 17 and k1 == 1 and k2 == 1)
        n17 += ok; ns += o['deep'] == NR - 1
    return nv, nh, nw, n17, ns

def q3_experiment(req):
    VAR = sample_variants(); out = []; est = []; allok = True; firsts = []
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < 20:
            rng = Shake(req['experiment_id'] + '|' + tr['seed']); z, pairs, bad = smc_replicate(rng, VAR)
            obs = dict(log2_estimate=z, accepted_pairs=len(pairs), failed_rebuilds=bad)
            nt = [sum(x) for x in zip((0,) * 5, *[near_term(p[0], *p[3]) for p in pairs[:2]])]
            obs.update(near_variants=nt[0], near_row16=nt[1], near_w7=nt[2], near_first17=nt[3], near_cosuccess=nt[4])
            est.append(z); allok = allok and z is not None and bad == 0 and len(pairs) > 0
            if pairs:
                cv, mx, my = pairs[0][:3]; firsts.append(pairs[-1])
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
            rec['observations'] = obs
        elif t == 20 and len(est) == 20:
            if allok:
                mean = sum(2.0 ** z for z in est) / 20; lz = __import__('math').log2(mean)
                rec['observations'] = dict(log2_pooled_mean=lz, pass_threshold=Q3_THRESH)
                if lz >= Q3_THRESH:
                    cv, mx, my = firsts[-1][:3]
                    rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
            else: rec['observations'] = dict(log2_pooled_mean=None)
        out.append(rec)
    return dict(schema_version=1, trials=out)

# ---- vt-ram-r38: the counted program against the reference on real first blocks ----
def ram_experiment(req):
    EV = entry_variants(); tab = tables(); out = []; groups = {}
    for tr in req['trials']: groups.setdefault(tr['trial'] % 8, []).append(tr)
    res = {}
    for g in range(8):
        if not groups.get(g): continue
        js = [(32 * g + k) % 256 for k in range(32)]; prog, _ = allocated_program(js)       # blocks 32 t .. 32 t + 31 (mod 256), 8 four-lane groups
        for tr in groups[g]: res[tr['trial']] = ram_trial(req['experiment_id'], tr, js, prog, EV, tab)
        del prog
    return dict(schema_version=1, trials=[res[tr['trial']] for tr in req['trials']])

def ram_trial(eid, tr, js, prog, EV, tab):
    rng = Shake(eid + '|' + tr['seed']); r0, r1 = rng.word(), rng.word()
    M0 = [(r0 >> (32 * k)) & M for k in range(8)] + [(r1 >> (32 * k)) & M for k in range(8)]
    cv = compress(IV, M0); reqs = []; ents = {}
    for j in js:
        a1, a2i = EV[j]; var = variant(A0L[j], a1, A2L[a2i]); wx = step2(cv, var)[0]
        ents[j] = ((c7of(var) + (1 << 32)), a1 | S0(a1) << 32 | (A2T + 2 * a2i) << 64, gaddr(0))
    def bucket(j, y, z): reqs.append((j, y, z)); return [ents[j]]
    m = Machine([r0, r1], bucket, tab); m.run(prog)
    bad = 0; w7p = 0; exp17 = []
    bad += m.cv != cv or m.m0 != M0
    bad += reqs != [(j,) + yz0(cv, A0L[j]) for j in js]
    for j in js:
        a1, a2i = EV[j]; var = variant(A0L[j], a1, A2L[a2i]); wx = step2(cv, var)[0]
        if inF7(wx[7]): w7p += 1; exp17.append(trace(cv, wx)[2][17])
    bad += [x & M for x in m.obs[0::2]] != exp17 or m.marks.count('W7') != w7p
    rec = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None, observations=dict(blocks=len(js), w7_passes=w7p, mismatches=int(bad), ops=m.ops, units=m.units))
    if not bad:
        j = js[0]; a1, a2i = EV[j]; var = variant(A0L[j], a1, A2L[a2i]); wx, wy = step2(cv, var)
        rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
    return rec

def run_request(req):
    eid = req['experiment_id']
    return ram_experiment(req) if 'ram' in eid else q3_experiment(req)


# ---------------------------------------------------------------------------------------------------------------
def selftest():
    import random
    rr = random.Random(5); ok = True
    def chk(name, cond, extra=''):
        nonlocal ok; ok = ok and bool(cond); print('%-58s %s %s' % (name, 'ok' if cond else 'FAIL', extra))
    # 1 the published pair is a semi-free-start collision with the published dense part
    chk('1 published pair collides, M != M\'', compress(PCV, PMX) == compress(PCV, PMY) and PMX != PMY)
    o = variant(SAX[4], SAX[5], SAX[6]); chk('  published dense part is a valid variant', valid(o))
    # 2 advice: G (row 16 as a function of W16), the A2 list conditions, the variants
    def g_hold(w):
        A = {i: sa(i) for i in range(16)}; E = {i: sex(i) for i in range(16)}; W = {i: SWX[i] for i in range(16)}
        B = {i: say(i) for i in range(16)}; F = {i: sey(i) for i in range(16)}; V = {i: SWY[i] for i in range(16)}
        W[16] = w; V[16] = (w + DW[16]) & M; step_row(A, E, W, 16); step_row(B, F, V, 16)
        return row_hold((A, E, W), (B, F, V), 16)
    cand = list(GL) + [rr.getrandbits(32) for _ in range(20000)] + [g ^ (1 << b) for g in GL for b in range(32)]
    chk('2 G: the 32 words hold row 16; 20,000 random words and the 1,024 bit-flip neighbours agree with G', all(g_hold(w) == (w in GSET) for w in cand), '(exhaustive count over 2^32: 32)')
    def a2_ok(x):
        e6 = (sa(6) + x - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M
        return cellok(1, 6, e6, e6) and not ((e6 ^ sex(7)) & PQ[7] or (e6 ^ sey(7)) & PQ[7]) and ((s0((sey(10) - say(6) - S1(sey(9)) - CH(sey(9), sey(8), sey(7)) - K[10] - e6) & M)
              - s0((sex(10) - sa(6) - S1(sex(9)) - CH(sex(9), sex(8), sex(7)) - K[10] - e6) & M)) & M) == DS0[10]
    chk('  A2 list: 768 sorted values, all satisfy the A2-only conditions', A2L == sorted(set(A2L)) and len(A2L) == 768 and all(a2_ok(x) for x in A2L) and not any(a2_ok(rr.getrandbits(32)) for _ in range(30000)))
    SV = sample_variants(); chk('  512 embedded variants valid; 256 entry variants valid', all(valid(variant(A0L[a], b, A2L[c])) for a, b, c in SV) and all(valid(variant(A0L[j], *(a, A2L[c]))) for j, (a, c) in enumerate(entry_variants())))
    # 3 Lemma 5: W16 closed form against the full trace, Step-2 words, c7
    bad = 0
    for _ in range(40):
        cv = [rr.getrandbits(32) for _ in range(8)]; a, b, c = SV[rr.randrange(512)]; v = (A0L[a], b, A2L[c]); var = variant(*v)
        wx = step2(cv, var)[0]; t = trace(cv, wx)
        bad += t[2][16] != w16_closed(cv, *v) or wx[7] != (c7of(var) - cv[0]) & M or not all(rowok(t_, u_, i) for t_, u_ in [pair_traces(cv, var)[:2]] for i in range(-4, 16)) or any(((pair_traces(cv, var)[3][i] - wx[i]) & M) != DW[i] for i in range(16))
    chk('3 Lemma 3 (rows -4..15 hold, DW_i for i < 16) and Lemma 5 (W16 closed form, W7 = c7 - A_-1), 40 chaining values', bad == 0)
    # 4 the counted program
    prog, mp = allocated_program(list(range(256))); regs = len(set(mp.values()))
    chk('4 program: registers after allocation <= 64', regs <= 64, '(%d)' % regs)
    cs = prog_costs(); print('   costs:', cs)
    chk('  ledger constants P0 96, epilogue 15, four blocks 85, iteration 6, E17 58, success 3210', (cs['P0'], cs['EPI'], cs['GROUP4'], cs['ITER'], cs['X_E17'], cs['X_SUCC']) == (96, 15, 85, 6, 58, 3210))
    a0, a1, a2 = SAX[4], SAX[5], SAX[6]; tab = tables(a2list=[a2]); found = 0
    for lane in range(4):
        A0L[lane], save = a0, A0L[lane]
        ent = ((c7of(variant(a0, a1, a2)) + (1 << 32)), a1 | S0(a1) << 32 | A2T << 64, gaddr(GSET[w16_closed(PCV, a0, a1, a2)]))
        m = Machine([1, 2], lambda j, y, z: [ent] if j == lane else [], tab, cvforce=PCV); m.run(allocated_program([0, 1, 2, 3])[0]); found += bool(m.succ and m.succ[0] == lane); A0L[lane] = save
    chk('  published pair: the program finds it in each of the 4 lanes', found == 4)
    # 5 replicate of the estimator and replay of its pairs in the counted program
    rng = Shake('selftest'); z, pairs, bad = smc_replicate(rng, SV); tab = tables(); fnd = 0
    for cv, mx, my, (a0, a1, a2) in pairs:
        j = A0L.index(a0); a2i = A2L.index(a2); q = j // 4; ent = ((c7of(variant(a0, a1, a2)) + (1 << 32)), a1 | S0(a1) << 32 | (A2T + 2 * a2i) << 64, gaddr(GSET[w16_closed(cv, a0, a1, a2)]))
        dec_ = (ent[0] ^ 0x5a5a5, ent[1], ent[2]); m = Machine([1, 2], lambda jj, y, z: [dec_, ent] if jj == j else [], tab, cvforce=cv); m.run(allocated_program(list(range(4 * q, 4 * q + 4)))[0]); fnd += bool(m.succ and m.succ[0] == j)
    chk('5 replicate: estimate, accepted pairs (rebuilt, verified), failed rebuilds 0', z is not None and bad == 0 and fnd == len(pairs), '(log2 %s, %d pairs, %d found by the counted program)' % (None if z is None else round(z, 3), len(pairs), fnd))
    # 6 organizer experiments
    r = ram_experiment(dict(experiment_id='vt-ram-r38', trials=[dict(trial=t, seed='%064x' % t) for t in range(8)]))
    chk('6 vt-ram-r38 (8 trials): mismatches 0, pairs returned 8', all(t['observations']['mismatches'] == 0 and t['message_a_hex'] for t in r['trials']), str([t['observations']['w7_passes'] for t in r['trials']]))
    print('SELFTEST', 'PASSED' if ok else 'FAILED'); return ok

def prog_costs():
    cv = [1, 2, 3, 4, 5, 6, 7, 8]; run = lambda js, bk, cvf=cv, tb=None: (lambda m: (m.run(allocated_program(js)[0]), m)[1])(Machine([5, 6], bk, tb if tb is not None else tables(), cvforce=cvf))
    P0EPI = run([], lambda j, y, z: []).ops; g4 = run([0, 1, 2, 3], lambda j, y, z: []); w = 12345
    while inF7(w & M): w += 1
    e0 = ((((w + cv[0]) & M) + (1 << 32)), 0, 0); it = run([0, 1, 2, 3], lambda j, y, z: [e0] if j == 0 else []).ops - g4.ops
    a0, a1, a2 = SAX[4], SAX[5], SAX[6]; tab = tables(a2list=[a2]); save = list(A0L); ent = ((c7of(variant(a0, a1, a2)) + (1 << 32)), a1 | S0(a1) << 32 | A2T << 64, gaddr(GSET[w16_closed(PCV, a0, a1, a2)]))
    xs = []
    for lane in range(4):
        A0L[lane] = a0; m = run([0, 1, 2, 3], lambda j, y, z: [ent] if j == lane else [], PCV, tab); A0L[:] = save
        d = dict(m.mark_ops); b = d['W7'] - 1; xs.append((d['E17'] - b, m.succ_ops - b))
    return dict(P0=P0EPI - 15, EPI=15, GROUP4=g4.ops - P0EPI, ITER=it, X_E17=max(x[0] for x in xs), X_SUCC=max(x[1] for x in xs))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
