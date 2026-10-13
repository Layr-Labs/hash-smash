#!/usr/bin/env python3
# vt38n.py - sha256-r38: variant-table collision attack on 38-step SHA-256 (target sha256-r38-prefix-v1) instantiated with the
# characteristic NEW3 (proof.md Section 3).  Standard library only.
# Contents: the reference construction, the counted online program (an op-counting 256-bit word-RAM interpreter running the exact
# online code), the organizer experiments (stdin JSON -> stdout JSON) and a self-test (argument "selftest").
# Derived from experiments/vt38.py of the variant-table lineage (aa0496d3, aed05522, 1db43310; c99df2dc, 0ae69bcb); the NEW3 tables,
# index widths, validity rule, A17 relation and pass rule are new (proof.md 5.3 lists every change).
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

# ---- NEW3 (proof.md Section 3): member x = M, member y = M'.  PCV/PMX/PMY: the explicit 38-step semi-free-start pair of NEW3, whose
# rows 0..15 are the dense part S*.
# Cells per kind (A, E, W) and row: (mask, x-value, x^y difference, 0): the signed trail with the one-bit conditions merged in.
# PQ[i]: bits where E_i = E_{i-1}.  X2: the other two-bit conditions (k1, i1, b1, equal, k2, i2, b2, row), member x.
# VC: the dense-part validity conditions of the variants (refs (kind, row, bit), allowed truth table), member x.
PCV = [365776084, 416637107, 3093859485, 3329917462, 602891679, 1989763280, 1550661105, 1226807753]
PMX = [3371712535, 1847034379, 167429563, 3432945346, 1648605982, 1556157841, 2232496615, 1981902488, 3542846464, 1353725948, 1855542832, 3765977126, 1319324216, 3686152971, 3904604025, 2153250138]
PMY = [3371712535, 1847034379, 167429563, 3432945346, 1648605982, 1556157841, 2232496615, 1445031576, 3614147584, 1890596860, 1805141146, 3765457958, 1319324216, 3686152971, 3904604025, 2216162650]
_CH = [{7:(1610612736,1073741824,1610612736,0),8:(4261904,4261888,4261904,0),11:(2060,4,2060,0),12:(1142965762,69207042,1142965762,0),13:(536936448,536936448,536936448,0),14:(134414480,196608,134414480,0),15:(41975808,33587200,41975808,0),17:(536870912,0,536870912,0)},{6:(138678288,134479888,0,0),7:(3896774672,4198400,3758096384,0),8:(3897301136,1615335552,139204752,0),9:(76546059,8388608,76546059,0),10:(4261888,0,4261888,0),11:(536899588,536883200,536899588,0),12:(1008926725,539099137,1008926725,0),13:(67450,1138,67450,0),14:(134283264,134283264,134283264,0),15:(2176,128,2176,0),16:(1212357248,138481792,1078071808,0),17:(1086462592,8390656,0,0),18:(1086722576,4592128,262160,0),19:(25460752,25460752,25198592,0),20:(25460752,262160,0,0),21:(562069504,16809984,536870912,0),22:(536870912,0,0,0),23:(536870912,536870912,0,0)},{7:(536870912,536870912,536870912,0),8:(71305216,2048,71305216,0),9:(536870912,0,536870912,0),10:(83956394,67179040,83956394,0),11:(529408,524288,529408,0),15:(71305216,4196352,71305216,0),16:(536870912,0,536870912,0),23:(42115072,8519680,41975808,0),25:(536870912,536870912,536870912,0)}]
PQ = [0,0,0,0,0,0,3758096384,526464,0,0,0,0,0,0,0,0,0,262160,16809984,0,536870912,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
X2 = [(1,16,7,0,1,16,26,16),(1,16,14,1,1,16,28,16),(0,15,4,1,0,16,4,16),(1,16,11,0,1,16,16,16),(0,15,7,1,0,16,7,16),(0,14,15,1,0,16,15,16),(0,15,16,0,0,16,16,16),(0,15,17,1,0,16,17,16),(0,14,23,1,0,16,23,16),(0,14,25,1,0,16,25,16),(0,15,27,1,0,16,27,16),(1,16,3,1,1,16,8,16),(1,16,4,1,1,16,23,16),(0,17,9,1,0,17,20,17),(2,16,20,0,2,16,27,16),(2,16,22,0,2,16,31,16),(0,16,15,1,0,17,15,17),(0,17,6,1,0,17,18,17),(2,16,4,1,2,16,6,16),(0,16,23,1,0,17,23,17),(0,16,25,1,0,17,25,17),(0,17,8,1,0,17,17,17),(0,15,29,1,0,16,29,16),(1,18,0,0,1,18,13,18),(1,18,17,1,1,18,22,18),(1,18,5,1,1,18,23,18),(0,16,29,1,0,18,29,18),(1,18,9,0,1,18,23,18),(1,19,10,1,1,19,29,19),(1,19,2,1,1,19,20,19),(1,19,5,1,1,19,18,19),(1,19,6,0,1,19,19,19),(1,19,10,1,1,19,28,19),(1,19,11,0,1,19,29,19),(1,19,1,1,1,19,28,19),(0,18,29,1,0,19,29,19),(1,19,4,0,1,19,9,19),(1,19,5,0,1,19,10,19),(1,21,10,0,1,21,15,21),(1,21,11,1,1,21,24,21),(1,21,2,1,1,21,16,21),(2,23,14,1,2,23,21,23),(2,23,22,0,2,23,24,23),(2,23,18,1,2,23,27,23),(2,23,0,1,2,23,30,23),(2,23,0,0,2,23,2,23),(2,25,20,1,2,25,27,25),(2,25,22,1,2,25,31,25),(2,25,4,0,2,25,6,25),(2,16,14,1,2,16,18,16),(2,16,8,1,2,16,25,16),(2,16,1,0,2,16,12,16)]
VC = [([(1,6,29),(1,5,29)],9),([(1,6,30),(1,5,30)],9),([(1,6,31),(1,5,31)],9),([(1,7,4),(1,6,4)],4),([(1,7,7),(1,6,7)],9),([(1,7,11),(1,6,11)],9),([(1,7,12),(1,6,12)],2),([(1,7,18),(1,6,18)],4),([(1,7,19),(1,6,19)],9),([(1,7,22),(1,6,22)],2),([(1,7,27),(1,6,27)],4),([(1,8,29),(1,6,29)],10),([(1,8,30),(1,6,30)],10),([(1,8,31),(1,6,31)],5)]
GL = [1213096050,1213096146,1213097074,1213097170,1220960379,1220960382,1220960383,1220960475,1220960478,1220960479,1220961403,1220961406,1220961407,1220961499,1220961502,1220961503,3366346875,3366346878,3366346879,3366346971,3366346974,3366346975,3366347899,3366347902,3366347903,3366347995,3366347998,3366347999,3366871163,3366871166,3366871167,3366871259,3366871262,3366871263,3366872187,3366872190,3366872191,3366872283,3366872286,3366872287]
A0_B64 = 'eNoBAAH//gSCVc1gr8QOwp/JCPhgRQ/kUbyojG1VouS/VH6jQMwfEG3Vpj6B0mfQUMaGaKI9L5jMVQKkj8UBMr/QdIoMybESfblYqD3WoToTSejc8tQmcF88z9uhRiGeTskMjYDAdqwc1R8GEELTz95E2j9txNfs+FSOzAxOI7xdzXe8DkXsTAvVGRYOyCC64crLjn3SCuwhPG8P8r45xLFVkmdQ1S09jsgYzWBJXMbPOS8yB9Dt8m1HMGvOzPYfzdTtvW5RE2K8UcSLD9MfudzK4Gj+vIizPdXRdeJQVWSRPfXPTsa8BxG9vVTdRpbyQDj+86tUPZtKVrV7f1SRaIu8aLDPxpux+4QI'
A2_B64 = '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'
S512_B64 = 'eNoNlmk4FPoCh/+ryNhmxjKjQXbDDIPJzGQpWY+lBUVZWqxFTqWSSIu2U0fdbnuKtFGHLKFdZMuSSkJlCRPCUadTXZW6ffx9/D3P+zzvK0pc+jqrizjzfOqe9QEQ8DS6Igywcwb15GqQabP9r5tRgHVqZVtFApgVad7+5BtAeYqykgigUdUy2qRKeQ7WNQvvYu7KGyaTFKtG1j7vWUYVzWu65RJqUP9peEBGUU6Oz5YQwilID11lSExXLRK7pyCbqykVg2yoh9/3ebdiEB3iL9FDGhaGG3YkE/7jiYCS/UBgOONVmjeRECtenTJVunL4SOxPrKW2bKo+H1hape+sqCSSK6HymlECo1OL8u4QHcmPc2884Oyrf2b/1om5F8IC2wbBrC2xg1WAMpvU1RfOQrb5sX9dbyHKHt9Xd6dTx9Nn45bziODwABl0pbLs7vJtvkRhm258/Eesd4R349xi4Hw7NbJ4IzC12O4dqkYEuf607jIQ7zxyRR4OUTpT3kCoU1uhl081nl7wQGsFjzAe/NFqn4JdjG592htPnI+q6JSeJsxDWpnFO4Bu6pjR3CfYqPUVZ3QBVdqceM+lA4uiBOfarahlEeOR+DCevv6GfVkncdksYS5uxwYButde+UGrvUl/jDhRhyuZJbv2E7XsYwGlSwHqKS0TqSPlQutP0SeQ1Z+wq22C2KdPnAgwRuBK59RMgDS8GTVdbtR2nUvtywBoxfxfCLcBujTkZT0pAdznA7lbzYF2EjpZ8ZowZ45oLtcmHO/0f6x3YDOliPHAIcxpDMhoug/oMqnVb7cxZ1cJd4sC4PT1r1utTExuInZJDuHI1j8ax1BdNzNkxQukzb/32PkWNsuJ8l4Sh/hspdSb/yUuHKWL5TXEPtdfWxSHgfGl+GEpFK1RrXw0AmTrp0SPvxOWR9kml21o9rVbW72asPW8Tx0lIYAbaTw2kEaNLo0OLxIilYhPjk++EI0ZD2b3O1Jx1EC25y9sUsRnY54ivrv30DIOEbLWxk2WQt1B3yu2p7Hufmc3uRPlqwZajYRD69avnW6tmHW1bPaQH7VhXzzz0JxaKPj7iEOwtP23gIVpyD6AHex2Cyttu62b5kdkg7F5LVNE8O9F6jyK0cGdV5cfRCID/XvcIUj3hl0ZCKG6Y0qbqyiFix09opyJnk7aeGAXFnGTKn8BJlnCPNlN4LTvET8W1GOFkuRVj/8mVpmlj+a+xi5/PFuW0I5mH/h7x4u7QD8N1dZ8IpLcoN0OfdDyhkpcTA+Cu1f+G2NBnPZ0admdwWaTXpnWQ5DhPFlY/QAI097V+VkiydfUZ+UhQP256fOFzZgFdv+VmkGI//OwmbUQu7ubvfWhCjWNHoWVRG3oz4yV7/H0S1fZG6ewSXjApX4x5Gu+aS2/TniDB8/3L6NawfJEt8dYvzjuQvQXrJwY0qJHEDtH/0TZOSD+/dKn6DxkrXyomt8IyVtV94Egym4tCRw3h+SYV1iXjOo9yO5v16Gzm6HUIRVL1/ij7rnUMS3/c8cYcNi+70LNNKppyvXqcqZadVkWb1Wg2cB1HbkHVT5Zc7/eiqqOjTwK2ows064ZhzOIQlt8TIsOdczNnFtXDwQsgeuv5VwW/7toCeZ4gdw1EqLx8KQo9w6RhnnRKgZ1WZh/9GUK5d6MD+lLptYF1Wt7TKHi+lZLG20EjSYitzoDo9+HireqAOcHv/1c3oW4TiamfZZQzImwjShH0zo06XAQhYX/qokHoE5T9xrP+9hgc6ZxCCQ6qRbhaglQ+Do+pCcMMtgZ2L0FG9rfL4vsQhqer+5W5wP+ts4Z3s2Yqbdus2QtlnTYefldxo7S7bIpKbZRPqk2LoMmRctZRV2E29yYXrwYsDuuj7UVA35m5tmB1dR2T6pbpyE1+rjOsKib8Pt4vEUiZCbkbNDXQWprxeKxpdSqg8kfDYDM2h19rhMY7Vy3LyWOaPUuOlFxhwDhcZc4BzJtoOt4Xxhk/9M1Y5EjctgYNVl4CijczOgak1Jdqf547U9CC/I3fbfD04JzN62eQXCD4sk+AXTU9GFW7AZKIT8/1epSGjC59+EIAQGdr8QxGEJjtWRlQrz3xxddIgK9DyfLVwMBzzL5iQLFjFHbGC7RHvqvxD8cadU8Co3JQWoKt649+wLEHxpOJG8lShaurHda0PyxsG75WSTLfj+t2ZxquuUve8WCrJLP54d9oMPZlbfS4gjrUUZzvC2x9bOaNvkPmu6Vt6q2CJg/OxhedhAQ25IDRcsANoCsingguWchHnKHMy9eS0/ZQ/i3TDIrW4Byhuu2okICkgyo+wh2SKoKffiNoNz5PV8/IfbnzIKAh1ia5vvc1weZBM+lrnewgXlL6AITpJtk0VN+hihbuXUvXILM3omd2ifI7GfS9EoNyi3Yr1RyCph4MkcrzgKV+PD0BUOYoWjqXHKLaAbnz2tWpryMgxeSZxPzBn7PGzaE3LCxt3ZQ9UxSz43jhBHsmfRwnKiLsr/5CNAsy1tnyl/+ukmW/5iJDTQFhY21wD72wLGUDcTlSOLVVyFQ8T/jp50qsUJnuNaLQaJwWpIl2oU5vhkTvtFIoTZOPUaViH22mPWvoeLwbqPytcBZeb7zVgsg3JP2JWI/kglTfh/3pUYbrL8xD0P9rJ3Wc/uwrsvSq88NqSDPIMH9PmZGTmdWTxCXY7GrxZsw++PN7q/fkaD14xNhP5zNki2We0Idn8S2knriwIv44BGGVN9Ufh9zgaqet+WDEmrUuPbuHDnWGA22t+Mhx6r65MUvMWNk/9U2K6p7qFTjZSydriHgTaRQm0ELTXE4hkX79KMcCGd708b4OuTQnl1UeJQI/wi1T8hCRkJdsPwEkux6/U3SBS25NjHRmkRR+7FpnRyw9G3dq1uA4j+tn93mIx1d6cY1L5H5rAp/z7+xrLDwnJ8JMnUvaNoSTKZL3Fhpuwmv1fF0FIuoSqo/88ahtRn3fdgLpJop7rXmIJt1jI9p1kAq9WssP0LYezvif9lJsUYQUN8L+HHVRgtuYu3tSl+iDQnc0Wu+5DZW3nLR6EgiUTt55WjTBJEuDsnqlVE473H8D33M2OA/lioAThd7Y3A+VInPG5/KhZSdUFqtRHkjLj1FYcDuwUBEaTpQHVG8UD9MZgUU3Qt8hCVDxb2FLQSvu/9xjg+SOj46uCQBWb3fdz4gCFkNaK4oPk0UxtNkvsOYqXm5oryJzELszucPgCjhR3pjPWCXJCYUHgVmybuSe02gxo79V5c6Eo2PFRcP7SOGefN8BjygZlY2v5lJDYLyu+0OYwcLV0+/Eozv5m+KOYpMZRp3u5IoP9E/7OsmqO6QdtH1Cbbe2PzKPQgxGf3zii8SJ/XYOW+kVMdi7JzXDeyg2OA7dRDy9wqDaq8BM0VFs78XUbMmp6HCfGL7sfDPrzMwjxfJKnpN1EcO3Mk/T/S4y2hwJEJlKzttorDiU76j9yZkp3D97/6lkP/zpI9nGZb5PI28fg6wvgqCpkaR/Yofaf0xVJE83jmQSI2O6bvNm8Ds+n9Ux+OoearCQNUocRJB0S9dc5Z2ejz9TvCFJG5RAsClk3vyyoglO2ejx0bEUPztWK0cCG21c7u9qO6CA5l1ulQ1x7UnvgUZmyvojSfSGSW664bMoPb17oFofWL2jHlo8iJUcZ5NBkRQOyVr8sZrMsvdPaHjG9B7m6zfdhdImEFvo18jxxdr36zgED7DeyigEEsz9NpDC5BVp1fFr2Q0GrPyi5xBRBzL+UuuYsN/r6yPNiLsO/ZqX4VY3TTwXvB3bH6pyrg/jert23Ys4QvWDW54XhwKoE7zHjkTzmxYXVe8HvBy7wa+UYAcNf+Dg67QMKdhldyPqg3G9ja1A+GANehZTYXm71TGPanyPLZWqgQYHu/S3BpHxD80RHIvKG5l3x4zh7ocA+u5LVjYODksfAsdtEoGor7jGY/V9pedAjOaXgRm9RJOzUj2OykFxXmL66YAK377/2pvA/3mqK3RUmKHy9pSDhKut/nKl65UufNa89tUqndHR9l3AuslpFcUNhGHR7Vn6ysBI25vzrPvRMD/plT5L1B7r2cSW4AUg0YDOthUySVQPjyfos+nuFt+xXNp8LjoA2T0FFitvIPop3tuk7ugaWObk2QJtrvZs/eNErR533Cg8j4w97McssNINf4vrXgnohDYtKfXmXJiWM0prmBmIXfiCYtqr9jWGHocOZ2PjPkaBTVFO11W3keywrMLA6/j6TcNW34ZgaMyb9zDGaFIMjznL2zMDcoY8oLaT/pvb0kk1oNVPfJQypgfNvUwH4DsI1P3PhDNn2q3pgyw1ixJhFwDWmnfzvRag4RuYxFVE4AMbltotxzPql8va/kCdPvLEuTOVFvU+/PtXOhydN6qFEdgnicvKF0Bph3effwZm+JpotBKPtXJPVveqk4Fl7suD7Gg8Xjk/nczoVAjVta1CMouC2ubfzV0uvBYwzvikBrnWLEQuHieSnxeBTRss1LPxwCN3Aqt0iziojJnyq0B2yRtS3RPR3pzqvXbeVTzZMOHBA0iFfScubEPOCz0yb5+lDCqzg1O/kTKalzzsmzioJ5hdCMOOK3iLV12GLEuawTUCymLYez/g4dhwsNA62HoHOazpIlJrQU+96s7gP7AsSFfXzRdiZ4uyCP/B/NVZiw='
E64_B64 = 'eNoBgAF//pFhOmMLBOD/7LSmBNd1G+s8BR4TNed1BRzfCDjgAT+V2MPvBJ9b3tevAHlDc1hGAqmM0jGLA2Wkq3lpBHyotLepBApZx+tfBY+b4+I1BRX+pmATBH6b0s8IBa2NqmrLAmecGbK+BCW/5FNuAqM230luAummFegZAa60PEl0AnRoBMnyBOQoHDfqAcnCVOJJAQ66e22NArJ489tIBf481mLfAjypFEDMA/UMXrCHAAGHY4RNBGBNtV64AiWqUz0tAqpuXVkWBDN5juJ1BefY3TbfAVzIlOU4AbLTB66WADTmjT/lA3BCWtkxBXRJ7q5/AHArb+A2BV9zw+djBWJ7IEjPA9vTtU7pAzkegG01BAp8LEKzA7SqBO0NAZzpRkOzA0LY/P3/AtmEsP2BAQY2f8j9BJSIPzIeAqqUiXlpBBITBbWVAAL4kM25AK8PUcD1ALbcNWU8BBZZHJ/cBBrS5UF7Ahaa78YdBccPgs/yAFDp8cL7BCgIhaHFBLN5G0TKA9pMpkY='
CELLS = [[(0, 0, 0, 0)] * NR for _ in range(3)]
for _k in range(3):
    for _i, _c in _CH[_k].items(): CELLS[_k][_i] = _c

_tx = trace(PCV, PMX); _ty = trace(PCV, PMY)       # S*: rows 0..15 of the semi-free-start pair (= the dense part)
SAX = [_tx[0][i] for i in range(-4, 16)]; SAY = [_ty[0][i] for i in range(-4, 16)]; SEX = [_tx[1][i] for i in range(-4, 16)]; SEY = [_ty[1][i] for i in range(-4, 16)]
SWX = list(PMX); SWY = list(PMY)
DW = [(_ty[2][i] - _tx[2][i]) & M for i in range(NR)]; DS0 = [(s0(_ty[2][i]) - s0(_tx[2][i])) & M for i in range(NR)]
DW16 = (-DW[16]) & M       # W16y = W16x - DW16
DA17 = (_ty[0][17] - _tx[0][17]) & M       # A17y - A17x on the trail (every row-17 cell holding)
A0L = list(struct.unpack('<64I', zlib.decompress(base64.b64decode(A0_B64))))       # the 64 A0 values (advice; proof.md Section 5)
A2L = list(struct.unpack('<1408I', zlib.decompress(base64.b64decode(A2_B64))))     # the 1408-value A2 list (exhaustive scan)
NA0 = len(A0L)
GSET = {g: k for k, g in enumerate(GL)}

def cellok(k, i, x, y):
    m, v, d, _ = CELLS[k][i]
    return (x & m) == v and (x ^ y) == d

def rowok(tx, ty, i):
    """Row i of both traces: (proof.md 5.3)"""
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
    """The dense-part conditions VC (member x: (proof.md 5.3)"""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = var
    for refs, al in VC:
        idx = 0
        for q, (k, i, b) in enumerate(refs): idx |= (((Ax if k == 0 else Ex)[i] >> b) & 1) << q
        if not (al >> idx) & 1: return False
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
    """Reference outcome of variant (a0, a1, a2) on cv: (proof.md 5.3)"""
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


# The counted online program: 256-bit word RAM, cost 1 per executed add, sub, rsub, and, or, xor, shl, shr, ld, ldi, sti, st, li, rand, jmp;
# 2 per conditional branch; f38 (one target compression) costs 1 unit; obs, mark, succ, halt are observers and cost nothing.  32-bit values
# live in the low half of a register; bits above bit 31 are garbage unless stated (additions and subtractions carry upward only; a value
# is masked before any rotation, address use or comparison with a mask-free word).
WORD = (1 << 256) - 1
TAG = lambda t: t << 150
HDR, ENT, A2T, GT = TAG(1), TAG(2), TAG(3), TAG(4)
SENT = (1 << 34) + (1 << 32)       # sentinel word 0 of an entry: SENT - a lies in (2^34, 2^34 + 2^32] -> F7 table value 2
EMPTY = ENT                         # address of the shared sentinel entry (empty bucket)
ESZ = 2                             # words per entry: c7 + 2^32 | packed variant+g fields (mkent)

class Asm:
    def __init__(s): s.c = []; s.lab = {}; s.n = 0
    def __call__(s, *ins): s.c.append(ins)
    def L(s, nm): s.lab[nm] = len(s.c)
    def new(s, p='L'): s.n += 1; return '%s%d' % (p, s.n)

def rot32(a, d, x, n1, n2, n3, shr3=False, t1='t1', t2='t2', D='D'):
    """d = ROTR(x,n1) ^ ROTR(x,n2) ^ (SHR(x,n3) if shr3 else ROTR(x,n3)) in the low 32 bits (garbage above); (proof.md 5.3)"""
    a('shl', D, x, 32); a('or', D, D, x)
    a('shr', t1, D, n1); a('shr', t2, D, n2); a('xor', t1, t1, t2)
    a('shr', t2, x if shr3 else D, n3); a('xor', d, t1, t2)

# Records served by the preprocessing (tables of the machine): A2 records (2 words) and G records (8 words).
def tables(a2list=None, glist=None):
    """A2 record i at A2T + 2i: (proof.md 5.3)"""
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
    """G record for W16x = g: (proof.md 5.3)"""
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
_g0 = grec(0, GL[0]); _b0 = gaddr(0)
MEI, VEI, MAI, VAI = _g0[_b0 + 1], _g0[_b0 + 2], _g0[_b0 + 4], _g0[_b0 + 5]
# NEW3: E17[4] = E16[4] with E16[4] depending on the G word.  Such bits (EVAR) leave the first E17 test (the shared immediate masks)
# and are checked in the deep path against the loaded E16 of the entry's G record.
EVAR = 0
for _i, _g in enumerate(GL):
    _r = grec(_i, _g); _b = gaddr(_i)
    assert (_r[_b + 1], _r[_b + 4], _r[_b + 5]) == (MEI, MAI, VAI); EVAR |= _r[_b + 2] ^ VEI
assert EVAR & ~PQ[17] == 0
MEI &= ~EVAR; VEI &= ~EVAR
def gw(gi): r = grec(gi, GL[gi]); b = gaddr(gi); return (r[b] << 224) | (r[b + 3] << 192) | (gi << 144)
def mkent(a0, a1, a2, a2i, gi):
    """Entry (2 words): (proof.md 5.3)"""
    v = variant(a0, a1, a2); u = (a2 - S0(a1) - K[2] - (a1 & a0)) & M; k = (v[0][2][10] + s1(SWX[15]) + a1) & M
    e1a = (a1 - S0(a0) + 1) & M
    eb = a1 | u << 32 | (a1 ^ a0) << 64 | S0(a1) << 96 | a2i << 128 | e1a << 160 | k << 224
    return c7of(v) + (1 << 32), (eb + gw(gi)) & WORD

# internal conditions of row 17 between bits of A17 only (both operands at row 17, kind A)
def a17int():
    r = [(b1, b2, eq) for (k1, i1, b1, eq, k2, i2, b2, row) in X2 if row == 17 and i1 == 17 and i2 == 17 and k1 == 0 and k2 == 0]
    return r

assert sorted((min(b1, b2), max(b1, b2), eq) for (b1, b2, eq) in a17int()) == [(6, 18, 1), (8, 17, 1), (9, 20, 1)]

def f7_value(addr):
    if addr < (1 << 33): return 1 if inF7(addr & M) else 0
    if (1 << 34) < addr <= SENT: return 2
    raise ValueError('bad F7-region address %x' % addr)

# The program.
def gen_prologue(a):
    """Group prologue: two random words -> M0 (16 words), CV1 = F38(IV, M0), per-CV values."""
    a('rand', 'r0'); a('rand', 'r1')
    for k in range(16):
        r = 'r0' if k < 8 else 'r1'; s_ = 32 * (k % 8)
        if s_:
            a('shr', 'm%d' % k, r, s_)
            if k % 8 != 7: a('and', 'm%d' % k, 'm%d' % k, M)
        else: a('and', 'm%d' % k, r, M)
    a('f38', ['m%d' % k for k in range(16)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    # hh = d - S0(a) - MAJ(a,b,c)
    rot32(a, 'S0a', 'a', 2, 13, 22)
    a('xor', 'abx', 'a', 'b'); a('and', 't2', 'abx', 'c'); a('and', 'aba', 'a', 'b'); a('xor', 't2', 't2', 'aba')
    a('add', 'S0a', 'S0a', 't2'); a('sub', 'hh', 'd', 'S0a')
    # y0p_s = ((hh - d - h - S1(e) - CH(e,f,g) + s1(W14) - K0) & M) << 32  (Z0 = (y0p_s >> 32) + A0)
    rot32(a, 'S1e', 'e', 6, 11, 25)
    a('xor', 't1', 'f', 'g'); a('and', 't1', 't1', 'e'); a('xor', 't1', 't1', 'g')
    a('add', 'S0a', 'S0a', 'h'); a('add', 'S0a', 'S0a', 'S1e'); a('add', 'S0a', 'S0a', 't1')
    a('rsub', 'y0p_s', (s1(SWX[14]) - K[0]) & M, 'S0a'); a('shl', 'y0p_s', 'y0p_s', 32); a('and', 'y0p_s', 'y0p_s', M << 32)
    a('xor', 'nabx', 'abx', M)
    a('xor', 'efx', 'e', 'f'); a('xor', 'nf', 'f', M)
    a('sub', 'c_aba', 'c', 'aba')
    a('add', 'g_aba', 'g', 'aba')
    a('and', 'hhm', 'hh', M)
    # broadcast of the per-CV values into the four 64-bit lanes of a register (lane k = block 4q + k)
    for src, dst in (('hhm', 'hh_v'), ('y0p_s', 'y0p_sv'), ('nabx', 'nabx_v'), ('efx', 'efx_v'), ('nf', 'nf_v'), ('g_aba', 'g_aba_v')):
        a('shl', 'bt', src, 64); a('or', dst, src, 'bt'); a('shl', 'bt', dst, 128); a('or', dst, dst, 'bt')
    # per-CV values of the deep path

LM = sum(M << (64 * k) for k in range(4)); LM64 = (1 << 64) - 1; LM_HI = sum(M << (64 * k + 32) for k in range(4))

def gen_group(a, js, rare):
    """Up to four consecutive A0 blocks (lane k = block js[k]). (proof.md 5.3)"""
    a0s = [A0L[j] for j in js]
    pk = lambda vals: sum(v << (64 * k) for k, v in enumerate(vals))
    a0v = pk(a0s); na0v = pk([x ^ M for x in a0s]); nsb = pk([((-S0(x) - K[1] + 2) & M) + (3 << 32) for x in a0s]); a0sv = pk([x << 32 for x in a0s])
    a('add', 'E0v', 'hh_v', a0v); a('and', 'E0v', 'E0v', LM)
    rot32(a, 'S1v', 'E0v', 6, 11, 25); a('and', 'S1v', 'S1v', LM)
    a('and', 'Chv', 'E0v', 'efx_v'); a('xor', 'Chv', 'Chv', 'nf_v')
    a('or', 'Mjv', 'nabx_v', na0v)
    a('rsub', 'Yv', nsb, 'S1v'); a('add', 'Yv', 'Yv', 'Mjv'); a('add', 'Yv', 'Yv', 'Chv'); a('sub', 'Yv', 'Yv', 'g_aba_v'); a('and', 'Yv', 'Yv', LM)
    a('add', 'Zsv', 'y0p_sv', a0sv); a('and', 'Zsv', 'Zsv', LM_HI)
    a('or', 'Vv', 'Zsv', 'Yv')
    for k, j in enumerate(js):
        loop, pas = a.new('loop'), a.new('pass')
        if k == 0: a('and', 'I', 'Vv', LM64)
        elif k == 3: a('shr', 'I', 'Vv', 192)
        else: a('shr', 'I', 'Vv', 64 * k); a('and', 'I', 'I', LM64)
        a('add', 'I', 'I', HDR | (j << 64)); a('ld', 'OFF', 'I'); a('sub', 'NE', 'NE', 'OFF')
        a.L(loop)
        a('ld', 'EN', 'OFF'); a('sub', 'W7', 'EN', 'a'); a('ld', 'FL', 'W7'); a('add', 'OFF', 'OFF', ESZ); a('bz', 'FL', loop)
        a('bne', 'FL', 2, pas)
        a('add', 'NE', 'NE', 'OFF')
        rare.append((j, a0s[k], pas, loop, k))

def gen_rare(a, j, a0, pas, loop, lane):
    a.L(pas); a('add', 'NW', 'NW', 1); a('mark', 'W7')
    for dst, src in (('Y_s', 'Yv'), ('Mj_s', 'Mjv'), ('E0_s', 'E0v')):
        a('shr', dst, src, 64 * lane) if lane else a('add', dst, src, 0)
    a('sub', 't1', 'OFF', 1); a('ld', 'w1', 't1')                       # entry fields (mkent)
    a('shr', 'E1', 'w1', 160); a('add', 'E1', 'E1', 'c_aba'); a('add', 'E1', 'E1', 'Mj_s'); a('and', 'E1', 'E1', M)
    rot32(a, 'S1E1', 'E1', 6, 11, 25)
    a('xor', 't1', 'E0_s', 'e'); a('and', 't1', 't1', 'E1'); a('xor', 'ChE1', 't1', 'e')
    a('shr', 't2', 'w1', 64); a('and', 't2', 't2', 'a')                # MAJ(A1, A0, a) = (a & Q) + (A1 & A0)
    a('shr', 'W2', 'w1', 32); a('sub', 'W2', 'W2', 't2'); a('sub', 'W2', 'W2', 'f'); a('sub', 'W2', 'W2', 'S1E1'); a('sub', 'W2', 'W2', 'ChE1'); a('and', 'W2', 'W2', M)
    rot32(a, 's0W2', 'W2', 7, 18, 3, shr3=True)
    a('shr', 't1', 'w1', 224); a('add', 'E17', 's0W2', 't1'); a('add', 'E17', 'E17', 'Y_s'); a('obs', 'E17')
    a('and', 't1', 'E17', MEI); a('bne', 't1', VEI, loop)
    a('mark', 'E17')
    a('add', 'N1', 'N1', 1)
    a('shr', 't1', 'w1', 192); a('add', 'A17', 'E17', 't1')
    a('and', 't1', 'A17', MAI); a('bne', 't1', VAI, loop)
    a('mark', 'A17')
    # A17 internal conditions A17[b1] = A17[b2] for (b1, b2) = (9, 20), (6, 18), (8, 17) (NEW3: the same three, asserted below):
    a('shl', 't3', 'A17', 9); a('and', 't1', 't3', 1 << 17)
    a('shl', 't3', 't3', 2); a('and', 't2', 't3', 1 << 20); a('or', 't1', 't1', 't2')
    a('shl', 't3', 't3', 1); a('and', 't2', 't3', 1 << 18); a('or', 't1', 't1', 't2')
    a('and', 't3', 'A17', (1 << 20) | (1 << 18) | (1 << 17))
    a('bne', 't1', 't3', loop)
    a('mark', 'A17int'); a('add', 'N2', 'N2', 1)
    gen_deep(a, j, a0, loop)

def gen_deep(a, j, a0, loop):
    """Rows 18..37 of both members. (proof.md 5.3)"""
    S = lambda m, k, i: (6 << 150) | (256 * m + 64 * k + i + 8)      # m member, k 0:A 1:E 2:W, i row
    def st(r, m, k, i): a('sti', S(m, k, i), r)
    def ld(r, m, k, i): a('ldi', r, S(m, k, i))
    def imm_st(v, m, k, i): st(v, m, k, i)
    A0 = lambda i: sa(i)
    a('and', 'E0_s', 'E0_s', M)
    a('shr', 'PG', 'w1', 144); a('and', 'PG', 'PG', 63); a('shl', 'PG', 'PG', 4); a('add', 'PG', 'PG', GT); a('ld', 'cG', 'PG')
    a('shr', 'P2', 'w1', 128); a('and', 'P2', 'P2', 2047); a('shl', 'P2', 'P2', 1); a('add', 'P2', 'P2', A2T); a('ld', 'A2r', 'P2')
    a('and', 'A1', 'w1', M); a('and', 'A2', 'A2r', M)
    a('shr', 'S0A1', 'w1', 96); a('shr', 't2', 'w1', 64); a('and', 't2', 't2', 'a'); a('and', 't1', 'A1', a0)
    a('sub', 'E2x', 'A2r', 'S0A1'); a('sub', 'E2x', 'E2x', 't2'); a('sub', 'E2x', 'E2x', 't1'); a('sub', 'W17', 'E17', 'cG')
    a('and', 'W17', 'W17', M); a('and', 'E17', 'E17', M); a('and', 'A17', 'A17', M)
    # E2 = A2 + b - S0(A1) - MAJ(A1,A0,a), masked; E3, E4, E5, E6
    a('add', 'E2', 'E2x', 'b'); a('and', 'E2', 'E2', M)
    a('shr', 'S0A2', 'A2r', 64)
    a('xor', 't2', 'A1', a0); a('and', 't2', 't2', 'A2'); a('xor', 't1', 't2', 't1')   # MAJ(A2,A1,A0) reusing t1 = A1 & a0
    a('add', 'E3', 'a', A0(3)); a('sub', 'E3', 'E3', 'S0A2'); a('sub', 'E3', 'E3', 't1'); a('and', 'E3', 'E3', M)
    def wstep(dst, Ei, Ai4, Ei4, Em1, Em2, Em3, k):
        rot32(a, 'S1t', Em1, 6, 11, 25)
        a('xor', 't3', Em2, Em3); a('and', 't3', 't3', Em1); a('xor', 't3', 't3', Em3)
        a('sub', dst, Ei, Ai4); a('sub', dst, dst, Ei4); a('sub', dst, dst, 'S1t'); a('sub', dst, dst, 't3')
        a('add', dst, dst, (-K[k]) & M); a('and', dst, dst, M)
    wstep('W3', 'E3', 'a', 'e', 'E2', 'E1', 'E0_s', 3)
    a('xor', 't1', 'A1', A0(3)); a('and', 't1', 't1', 'A2'); a('and', 't2', 'A1', A0(3)); a('xor', 't1', 't1', 't2')
    a('rsub', 'E4', (A0(4) + a0 - S0(A0(3))) & M, 't1'); a('and', 'E4', 'E4', M)
    wstep('W4', 'E4', a0, 'E0_s', 'E3', 'E2', 'E1', 4)
    a('shr', 'E5', 'A2r', 128); a('add', 'E5', 'E5', 'A1'); a('and', 'E5', 'E5', M)
    wstep('W5', 'E5', 'A1', 'E1', 'E4', 'E3', 'E2', 5)
    a('shr', 'E6', 'A2r', 96); a('and', 'E6', 'E6', M)
    wstep('W6', 'E6', 'A2', 'E2', 'E5', 'E4', 'E3', 6)
    a('and', 'W7x', 'W7', M)
    # W8 of member x = E8 - A4 - E4 - S1(E7) - CH(E7,E6,E5) - K8
    a('xor', 't3', 'E6', 'E5'); a('and', 't3', 't3', sex(7)); a('xor', 't3', 't3', 'E5')
    a('rsub', 't1', (sex(8) - sa(4) - S1(sex(7)) - K[8]) & M, 'E4'); a('sub', 't1', 't1', 't3'); a('and', 'W8x', 't1', M)
    a('add', 'P3', 'P2', 1); a('ld', 'A2r2', 'P3')               # c9x | c9y << 32 | W10x << 64 | W10y << 96
    a('sub', 'W9x', 'A2r2', 'A1'); a('and', 'W9x', 'W9x', M)
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
        if m == 0 and EVAR: a('xor', 't1', 'u1', 'E17'); a('and', 't1', 't1', EVAR); a('bnz', 't1', loop)     # E17[b] = E16[b], b in EVAR
    st('A17', 0, 0, 17); st('E17', 0, 1, 17); st('E17', 1, 1, 17)
    a('add', 'u1', 'A17', DA17); a('and', 'u1', 'u1', M); st('u1', 1, 0, 17)
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

def gen_epilogue(a, caps):
    """After every group: halt when a work counter exceeds its cap; group counter; loop."""
    halt = a.new('halt')
    for k, (r, cap) in enumerate(zip(('NE', 'NW', 'N1', 'N2'), caps)):
        d_ = 't1' if k == 0 else 't2'
        a('rsub', d_, cap, r)
        if k: a('or', 't1', 't1', 't2')
    a('shr', 't1', 't1', 255); a('bnz', 't1', halt)
    a('add', 'NG', 'NG', 1)
    a.pending = halt

def build_program(js, caps=(1 << 200,) * 4, ngroups=1):
    a = Asm(); a.L('group'); gen_prologue(a); rare = []
    js = list(js)
    for q in range(0, len(js), 4): gen_group(a, js[q:q + 4], rare)
    gen_epilogue(a, caps)
    a('bne', 'NG', ngroups, 'group'); a.L(a.pending); a('halt_ok',)
    for r in rare: gen_rare(a, *r)
    return a

class Machine:
    def __init__(s, randwords, bucket, tabmem, cvforce=None):
        s.rw = list(randwords); s.bucket = bucket; s.tab = dict(tabmem); s.cvforce = cvforce
        s.r = {}; s.ops = 0; s.units = 0; s.mem = {}; s.ent = {}; s.nent = 0; s.succ = None; s.cv = None; s.obs = []
        s.marks = []; s.trace = []; s.opc = {}; s.mark_ops = []; s.succ_ops = None
        s.ent[EMPTY] = SENT; s.ent[EMPTY + 1] = 0; s.nent = ESZ
    def store(s, addr, val): s.mem[addr] = val
    def load(s, addr):
        t = addr >> 150
        if t == 0: return f7_value(addr)
        if t == 1:
            j, idx = (addr >> 64) & ((1 << 86) - 1), addr & ((1 << 64) - 1)
            es = s.bucket(j, idx & M, idx >> 32); s.trace.append((j, idx & M, idx >> 32, len(es)))
            if not es: return EMPTY
            base = ENT + s.nent
            for k, e in enumerate(es):
                for w in range(ESZ): s.ent[base + ESZ * k + w] = e[w]
            end = base + ESZ * len(es)
            s.ent[end] = SENT; s.ent[end + 1] = 0
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
        if op == 'jmp': succ.append((lab[ins[1]],))
        elif op in ('bz', 'bnz'): succ.append((pc + 1, lab[ins[2]]))
        elif op == 'bne': succ.append((pc + 1, lab[ins[3]]))
        elif op in ('succ', 'halt_ok'): succ.append(())
        else: succ.append((pc + 1,) if pc + 1 < n else ())
    du = [_du(ins) for ins in c]; vs = sorted({x for d, u in du for x in d + u}); vi = {v: 1 << i for i, v in enumerate(vs)}
    dm = [sum(vi[x] for x in d) for d, _ in du]; um = [sum(vi[x] for x in u) for _, u in du]
    live = [0] * (n + 1); ch = 1
    while ch:
        ch = 0
        for pc in range(n - 1, -1, -1):
            sc = succ[pc]; out = live[sc[0]] if len(sc) == 1 else (live[sc[0]] | live[sc[1]] if sc else 0)
            inp = (out & ~dm[pc]) | um[pc]
            if inp != live[pc]: live[pc] = inp; ch = 1
    adj = {v: 0 for v in vs}
    for pc in range(n):
        sc = succ[pc]; out = live[sc[0]] if len(sc) == 1 else (live[sc[0]] | live[sc[1]] if sc else 0)
        for d in du[pc][0]: adj[d] |= out & ~vi[d]
    for v in vs:
        m = adj[v]
        for u in vs:
            if m & vi[u]: adj[u] |= vi[v]
    col = {}
    for v in sorted(vs, key=lambda v: (-bin(adj[v]).count('1'), v)):
        used = {col[u] for u in vs if (adj[v] & vi[u]) and u in col}
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

def allocated_program(js, caps=(1 << 200,) * 4, ngroups=1, _cache={}):
    if 'map' not in _cache:
        t = build_program(list(range(8))); _cache['map'] = regalloc(t)
    return rename(build_program(js, caps, ngroups), _cache['map']), _cache['map']




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
    b = dec(E64_B64); return [struct.unpack_from('<IH', b, 6 * k) for k in range(NA0)]                  # per A0 index: (A1, A2 index) valid

def rebuild(P, v, w23):
    """Rebuild a tail success into a real semi-free-start pair: (proof.md 5.3)"""
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
def erow_plan(i, cm, pq):
    """Bits of E_i imposed on a row-i proposal: (proof.md 5.3)"""
    imp = cm | pq; prev = []; inner = []
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != i or k1 != 1 or k2 != 1 or i2 != i: continue
        fl = 0 if eq else 1
        if i1 < i:
            if not (imp >> b2) & 1: prev.append((i1, b1, b2, fl)); imp |= 1 << b2
        elif not (imp >> b2) & 1: inner.append((b1, b2, fl)); imp |= 1 << b2
        elif not (imp >> b1) & 1: inner.append((b2, b1, fl)); imp |= 1 << b1
    # an inner source must not be imposed after its use: order sources before targets, drop a cycle into 'checked'
    done = cm | pq | sum(1 << b2 for (_, _, b2, _) in prev); out = []; todo = list(inner)
    while todo:
        nxt = [t for t in todo if (done >> t[0]) & 1 or not any(u[1] == t[0] for u in todo)]
        if not nxt: imp &= ~sum(1 << t[1] for t in todo); break
        for t in nxt: out.append(t); done |= 1 << t[1]; todo.remove(t)
    return imp, prev, out

def smc_replicate(rng, VAR):
    """One replicate: (proof.md 5.3)"""
    lg = [__import__('math').log2(len(GL)) - 32]; P = []; VW = {}
    for _ in range(NP_R):
        w = GL[rng.below(len(GL))]; Ax = {i: sa(i) for i in range(16)}; Ex = {i: sex(i) for i in range(16)}; Wx = {i: SWX[i] for i in range(16)}
        Ay = {i: say(i) for i in range(16)}; Ey = {i: sey(i) for i in range(16)}; Wy = {i: SWY[i] for i in range(16)}
        Wx[16] = w; Wy[16] = (w + DW[16]) & M
        for (A, E, W) in ((Ax, Ex, Wx), (Ay, Ey, Wy)): step_row(A, E, W, 16)
        P.append((Ax, Ex, Wx, Ay, Ey, Wy))
    for i in range(17, 23):
        cm, cvv, _, _ = CELLS[1][i]; pq = PQ[i] & ~cm; Mi = CH_R[i - 17]; surv = []
        imp, prev, inner = erow_plan(i, cm, pq); f = bin(imp).count('1')
        for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
            rx = (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i]) & M
            ry = (Ay[i-4] + Ey[i-4] + S1(Ey[i-1]) + CH(Ey[i-1], Ey[i-2], Ey[i-3]) + K[i]) & M
            fixed = cvv | (Ex[i-1] & pq)
            for (i1, b1, b2, fl) in prev: fixed |= (((Ex[i1] >> b1) & 1) ^ fl) << b2
            for _ in range(Mi):
                e = (rng.u32() & ~imp & M) | fixed
                for (bs, bd, fl) in inner: e = (e & ~(1 << bd)) | (((e >> bs) & 1) ^ fl) << bd
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

COSTS_EXPECTED = (89, 13, 75, 6, 41, 58, 3297)     # executed counts (proof.md 5.3)
Q3_THRESH = -100.0        # log2 threshold of the pass rule on the mean of 20 replicate estimates = q3_model (proof.md 10.1; fixed from
                          # 1,200 development replicates, mean 2^-99.7997, before any validation run)
def near_term(cv, a0, a1, a2):
    """Pair term, near part: (proof.md 5.3)"""
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
    for tr in req['trials']: groups.setdefault(tr['trial'] % 2, []).append(tr)
    res = {}
    for g in range(2):
        if not groups.get(g): continue
        js = [(32 * g + k) % NA0 for k in range(32)]; prog, _ = allocated_program(js)       # blocks 32 t .. 32 t + 31 (mod 64), 8 four-lane groups
        for tr in groups[g]: res[tr['trial']] = ram_trial(req['experiment_id'], tr, js, prog, EV, tab)
        del prog
    return dict(schema_version=1, trials=[res[tr['trial']] for tr in req['trials']])

def ram_trial(eid, tr, js, prog, EV, tab):
    rng = Shake(eid + '|' + tr['seed']); r0, r1 = rng.word(), rng.word()
    M0 = [(r0 >> (32 * k)) & M for k in range(8)] + [(r1 >> (32 * k)) & M for k in range(8)]
    cv = compress(IV, M0); reqs = []; ents = {}
    for j in js:
        a1, a2i = EV[j]; var = variant(A0L[j], a1, A2L[a2i]); wx = step2(cv, var)[0]
        ents[j] = mkent(A0L[j], a1, A2L[a2i], a2i, 0)
    def bucket(j, y, z): reqs.append((j, y, z)); return [ents[j]]
    m = Machine([r0, r1], bucket, tab); m.run(prog)
    bad = 0; w7p = 0; exp17 = []
    bad += m.cv != cv or m.m0 != M0
    bad += reqs != [(j,) + yz0(cv, A0L[j]) for j in js]
    for j in js:
        a1, a2i = EV[j]; var = variant(A0L[j], a1, A2L[a2i]); wx = step2(cv, var)[0]
        if inF7(wx[7]): w7p += 1; exp17.append(trace(cv, wx)[2][17])
    bad += [(x - tab[GT]) & M for x in m.obs] != exp17 or m.marks.count('W7') != w7p
    rec = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None, observations=dict(blocks=len(js), w7_passes=w7p, mismatches=int(bad), ops=m.ops, units=m.units))
    if not bad:
        j = js[0]; a1, a2i = EV[j]; var = variant(A0L[j], a1, A2L[a2i]); wx, wy = step2(cv, var)
        rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
    return rec

def run_request(req):
    eid = req['experiment_id']
    return ram_experiment(req) if 'ram' in eid else q3_experiment(req)


def selftest():
    import random
    rr = random.Random(5); ok = True
    def chk(name, cond, extra=''):
        nonlocal ok; ok = ok and bool(cond); print('%-58s %s %s' % (name, 'ok' if cond else 'FAIL', extra), flush=True)
    # 1 the NEW3 semi-free-start pair collides and its dense part S* is a valid variant
    chk('1 NEW3 pair collides, M != M\'', compress(PCV, PMX) == compress(PCV, PMY) and PMX != PMY)
    tx, ty = trace(PCV, PMX), trace(PCV, PMY)
    chk('  it holds every cell, + pair and two-bit condition of rows 0..37 (W cells of rows 7..10 excepted), W7 in F7', all(rowok(tx, ty, i) for i in range(NR)) and inF7(PMX[7]))
    o = variant(SAX[4], SAX[5], SAX[6]); chk('  S* is a valid variant', valid(o))
    # 2 advice: G (row 16 as a function of W16), the A2 list conditions, the variants
    def g_hold(w):
        A = {i: sa(i) for i in range(16)}; E = {i: sex(i) for i in range(16)}; W = {i: SWX[i] for i in range(16)}
        B = {i: say(i) for i in range(16)}; F = {i: sey(i) for i in range(16)}; V = {i: SWY[i] for i in range(16)}
        W[16] = w; V[16] = (w + DW[16]) & M; step_row(A, E, W, 16); step_row(B, F, V, 16)
        return row_hold((A, E, W), (B, F, V), 16)
    cand = list(GL) + [rr.getrandbits(32) for _ in range(20000)] + [g ^ (1 << b) for g in GL for b in range(32)]
    chk('2 G: the 40 words hold row 16; 20,000 random words and the 1,280 bit-flip neighbours agree with G', all(g_hold(w) == (w in GSET) for w in cand), '(exhaustive count over 2^32: 40)')
    a2only = [(refs, al) for refs, al in VC if all((k == 0 and i >= 2) or (k == 1 and i >= 6) for k, i, b in refs)]
    def a2_ok(x):
        e6 = (sa(6) + x - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M
        val = lambda k, i: (x if i == 2 else sa(i)) if k == 0 else (e6 if i == 6 else sex(i))
        if any(not (al >> sum(((val(k, i) >> b) & 1) << q for q, (k, i, b) in enumerate(refs))) & 1 for refs, al in a2only): return False
        w10 = lambda m: (((sey if m else sex)(10)) - (say if m else sa)(6) - S1((sey if m else sex)(9)) - CH((sey if m else sex)(9), (sey if m else sex)(8), (sey if m else sex)(7)) - K[10] - e6) & M
        return (w10(1) - w10(0)) & M == DW[10] and (s0(w10(1)) - s0(w10(0))) & M == DS0[10]
    chk('  A2 list: 1408 sorted values, all satisfy the A2-only conditions; 30,000 random values none', A2L == sorted(set(A2L)) and len(A2L) == 1408 and all(a2_ok(x) for x in A2L) and not any(a2_ok(rr.getrandbits(32)) for _ in range(30000)))
    SV = sample_variants(); chk('  512 embedded variants valid; 64 entry variants valid', all(valid(variant(A0L[a], b, A2L[c])) for a, b, c in SV) and all(valid(variant(A0L[j], *(a, A2L[c]))) for j, (a, c) in enumerate(entry_variants())))
    # 3 Lemma 5: W16 closed form against the full trace, Step-2 words, c7
    bad = 0
    for _ in range(40):
        cv = [rr.getrandbits(32) for _ in range(8)]; a, b, c = SV[rr.randrange(512)]; v = (A0L[a], b, A2L[c]); var = variant(*v)
        wx = step2(cv, var)[0]; t = trace(cv, wx)
        bad += t[2][16] != w16_closed(cv, *v) or wx[7] != (c7of(var) - cv[0]) & M or not all(rowok(t_, u_, i) for t_, u_ in [pair_traces(cv, var)[:2]] for i in range(-4, 16)) or any(((pair_traces(cv, var)[3][i] - wx[i]) & M) != DW[i] for i in range(16))
    chk('3 Lemma 3 (rows -4..15 hold, DW_i for i < 16) and Lemma 5 (W16 closed form, W7 = c7 - A_-1), 40 chaining values', bad == 0)
    # 4 the counted program
    prog, mp = allocated_program(list(range(8))); regs = len(set(mp.values()))
    chk('4 program: registers after allocation <= 64', regs <= 64, '(%d)' % regs)
    cs = prog_costs(); print('   costs:', cs)
    chk('  ledger constants P0, epilogue, four blocks, iteration, E17, A17, success (proof.md 5.3)', (cs['P0'], cs['EPI'], cs['GROUP4'], cs['ITER'], cs['X_E17'], cs['X_A17int'], cs['X_SUCC']) == COSTS_EXPECTED, str(cs))
    a0, a1, a2 = SAX[4], SAX[5], SAX[6]; tab = tables(a2list=[a2]); found = 0
    for lane in range(4):
        A0L[lane], save = a0, A0L[lane]
        ent = mkent(a0, a1, a2, 0, GSET[w16_closed(PCV, a0, a1, a2)])
        m = Machine([1, 2], lambda j, y, z: [ent] if j == lane else [], tab, cvforce=PCV); m.run(allocated_program([0, 1, 2, 3])[0]); found += bool(m.succ and m.succ[0] == lane); A0L[lane] = save
    chk('  published pair: the program finds it in each of the 4 lanes', found == 4)
    # 5 replicate of the estimator and replay of its pairs in the counted program
    rng = Shake('selftest'); z, pairs, bad = smc_replicate(rng, SV); tab = tables(); fnd = 0
    for cv, mx, my, (a0, a1, a2) in pairs:
        j = A0L.index(a0); a2i = A2L.index(a2); q = j // 4; ent = mkent(a0, a1, a2, a2i, GSET[w16_closed(cv, a0, a1, a2)])
        dec_ = (ent[0] ^ 0x5a5a5, ent[1]); m = Machine([1, 2], lambda jj, y, z: [dec_, ent] if jj == j else [], tab, cvforce=cv); m.run(allocated_program(list(range(4 * q, 4 * q + 4)))[0]); fnd += bool(m.succ and m.succ[0] == j)
    chk('5 replicate: estimate, accepted pairs (rebuilt, verified), failed rebuilds 0', z is not None and bad == 0 and fnd == len(pairs), '(log2 %s, %d pairs, %d found by the counted program)' % (None if z is None else round(z, 3), len(pairs), fnd))
    # 6 organizer experiments
    r = ram_experiment(dict(experiment_id='vt-ram-r38', trials=[dict(trial=t, seed='%064x' % t) for t in range(8)]))
    chk('6 vt-ram-r38 (8 trials): mismatches 0, pairs returned 8', all(t['observations']['mismatches'] == 0 and t['message_a_hex'] for t in r['trials']), str([t['observations']['w7_passes'] for t in r['trials']]))
    print('SELFTEST', 'PASSED' if ok else 'FAILED'); return ok

def prog_costs():
    cv = [1, 2, 3, 4, 5, 6, 7, 8]; run = lambda js, bk, cvf=cv, tb=None: (lambda m: (m.run(allocated_program(js)[0]), m)[1])(Machine([5, 6], bk, tb if tb is not None else tables(), cvforce=cvf))
    P0EPI = run([], lambda j, y, z: []).ops; g4 = run([0, 1, 2, 3], lambda j, y, z: []); w = 12345
    while inF7(w & M): w += 1
    e0 = ((((w + cv[0]) & M) + (1 << 32)), 0); it = run([0, 1, 2, 3], lambda j, y, z: [e0] if j == 0 else []).ops - g4.ops
    a0, a1, a2 = SAX[4], SAX[5], SAX[6]; tab = tables(a2list=[a2]); save = list(A0L); ent = mkent(a0, a1, a2, 0, GSET[w16_closed(PCV, a0, a1, a2)])
    xs = []
    for lane in range(4):
        A0L[lane] = a0; m = run([0, 1, 2, 3], lambda j, y, z: [ent] if j == lane else [], PCV, tab); A0L[:] = save
        d = dict(m.mark_ops); b = d['W7'] - 1; xs.append((d['E17'] - b, d['A17int'] - b, m.succ_ops - b))
    return dict(P0=P0EPI - 13, EPI=13, GROUP4=g4.ops - P0EPI, ITER=it, X_E17=max(x[0] for x in xs), X_A17int=max(x[1] for x in xs), X_SUCC=max(x[2] for x in xs))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
