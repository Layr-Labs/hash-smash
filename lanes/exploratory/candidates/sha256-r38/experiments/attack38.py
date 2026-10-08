"""Organizer experiment for the sha256-r38 attack package (ePrint 2026/1120's 38-step attack).

Per trial (seeded by the organizer), the program draws 128 independent uniform 64-byte first blocks M0 from a
SHA-256 counter stream of the trial seed, and for each one:
  - computes CV1 = f38(IV, M0) (the target's 38-step compression with feed-forward) and the target digest of the
    64-byte message M0 (CV1, then the identical padding block);
  - runs Step 2 of the attack: from CV1 and the published Step-1 words it derives E3 (and E2) and W7 (and W6) and
    tests their conditions; a passing block is "valid";
  - for every valid block and every element of S, derives W0..W5, W16 and the step-16 words E16 and A16 of the
    unprimed message and tests: the W16-only conditions, the value symbols of E16, and the full pair test of
    steps 14..16 (value symbols, relations, exact XOR differences of both messages).
Observations (untrusted, organizer-executed): blocks, valid, w16, e16, pair16; trial 0 also re-checks, on a valid first block, that every
element of S passes steps 14 and 15 exactly and that the paper's SFS pair (as transcribed) collides.
Returned pair: two of the trial's first blocks whose target digests agree on the declared 12-bit mask (a
birthday pair among the 128 blocks), or nulls. The organizer recomputes the digests, so the checked event
confirms that this program evaluates the selected target. Deep steps (17..37) are far below sandbox scale.
"""
import hashlib
import json
import sys

R = 38
M32 = 0xFFFFFFFF
B = 128
MASK = 1218444920556476648522760
K = (1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051)
IV = (1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225)
COND = {'A-4': (0, 0, 0), 'E-4': (0, 0, 0), 'A-3': (0, 0, 0), 'E-3': (0, 0, 0), 'A-2': (0, 0, 0), 'E-2': (0, 0, 0), 'A-1': (0, 0, 0), 'E-1': (0, 0, 0), 'A0': (0, 0, 0), 'E0': (0, 0, 0), 'W0': (0, 0, 0), 'A1': (0, 0, 0), 'E1': (0, 0, 0), 'W1': (0, 0, 0), 'A2': (0, 0, 0), 'E2': (0, 0, 0), 'W2': (0, 0, 0), 'A3': (0, 0, 0), 'E3': (0, 0, 0), 'W3': (0, 0, 0), 'A4': (0, 0, 0), 'E4': (0, 0, 0), 'W4': (0, 0, 0), 'A5': (0, 0, 0), 'E5': (0, 0, 0), 'W5': (0, 0, 0), 'A6': (0, 0, 0), 'E6': (138678416, 134480016, 0), 'W6': (0, 0, 0), 'A7': (1610612736, 536870912, 1610612736), 'E7': (3939897499, 3804237825, 3758096384), 'W7': (536870912, 0, 536870912), 'A8': (4261904, 16, 4261904), 'E8': (3957292027, 2299865209, 139204752), 'W8': (71305216, 71303168, 71305216), 'A9': (0, 0, 0), 'E9': (4278190015, 3329275675, 76546059), 'W9': (536870912, 536870912, 536870912), 'A10': (0, 0, 0), 'E10': (1040153503, 683879063, 4261888), 'W10': (83956394, 16777226, 83956394), 'A11': (2060, 2056, 2060), 'E11': (3187670975, 2163392958, 536899588), 'W11': (529408, 529408, 529408), 'A12': (1142965762, 1073758720, 1142965762), 'E12': (4261412799, 1570574870, 1008926725), 'W12': (0, 0, 0), 'A13': (536936448, 0, 536936448), 'E13': (4293918591, 901856013, 67450), 'W13': (0, 0, 0), 'A14': (134414480, 134217872, 134414480), 'E14': (2086891391, 537027697, 134283264), 'W14': (0, 0, 0), 'A15': (41975808, 8388608, 41975808), 'E15': (1246957562, 1242762074, 2176), 'W15': (71305216, 67108864, 71305216), 'A16': (0, 0, 0), 'E16': (1279466112, 1208156800, 1078071808), 'W16': (536870912, 536870912, 536870912), 'A17': (536870912, 536870912, 536870912), 'E17': (1086462592, 2048, 0), 'W17': (0, 0, 0), 'A18': (0, 0, 0), 'E18': (1086722608, 4330000, 262160), 'W18': (0, 0, 0), 'A19': (0, 0, 0), 'E19': (830770738, 805569584, 25198592), 'W19': (0, 0, 0), 'A20': (0, 0, 0), 'E20': (562331664, 537133072, 0), 'W20': (0, 0, 0), 'A21': (0, 0, 0), 'E21': (562072576, 553682944, 536870912), 'W21': (0, 0, 0), 'A22': (0, 0, 0), 'E22': (536870912, 0, 0), 'W22': (0, 0, 0), 'A23': (0, 0, 0), 'E23': (536870912, 536870912, 0), 'W23': (92446720, 92446720, 25198592), 'A24': (0, 0, 0), 'E24': (0, 0, 0), 'W24': (0, 0, 0), 'A25': (0, 0, 0), 'E25': (0, 0, 0), 'W25': (536870912, 0, 536870912), 'A26': (0, 0, 0), 'E26': (0, 0, 0), 'W26': (0, 0, 0), 'A27': (0, 0, 0), 'E27': (0, 0, 0), 'W27': (0, 0, 0), 'A28': (0, 0, 0), 'E28': (0, 0, 0), 'W28': (0, 0, 0), 'A29': (0, 0, 0), 'E29': (0, 0, 0), 'W29': (0, 0, 0), 'A30': (0, 0, 0), 'E30': (0, 0, 0), 'W30': (0, 0, 0), 'A31': (0, 0, 0), 'E31': (0, 0, 0), 'W31': (0, 0, 0), 'A32': (0, 0, 0), 'E32': (0, 0, 0), 'W32': (0, 0, 0), 'A33': (0, 0, 0), 'E33': (0, 0, 0), 'W33': (0, 0, 0), 'A34': (0, 0, 0), 'E34': (0, 0, 0), 'W34': (0, 0, 0), 'A35': (0, 0, 0), 'E35': (0, 0, 0), 'W35': (0, 0, 0), 'A36': (0, 0, 0), 'E36': (0, 0, 0), 'W36': (0, 0, 0), 'A37': (0, 0, 0), 'E37': (0, 0, 0), 'W37': (0, 0, 0)}
REL = [['A', 14, 15, '=', 'A', 16, 15], ['A', 14, 23, '=', 'A', 16, 23], ['A', 14, 25, '=', 'A', 16, 25], ['A', 15, 4, '=', 'A', 16, 4], ['A', 15, 7, '=', 'A', 16, 7], ['A', 15, 16, '!=', 'A', 16, 16], ['A', 15, 17, '=', 'A', 16, 17], ['A', 15, 27, '=', 'A', 16, 27], ['A', 15, 29, '=', 'A', 16, 29], ['A', 16, 15, '=', 'A', 17, 15], ['A', 16, 23, '=', 'A', 17, 23], ['A', 16, 25, '=', 'A', 17, 25], ['A', 17, 9, '=', 'A', 17, 20], ['A', 17, 6, '=', 'A', 17, 18], ['A', 17, 8, '=', 'A', 17, 17], ['A', 16, 29, '=', 'A', 18, 29], ['A', 18, 29, '=', 'A', 19, 29], ['E', 16, 4, '!=', 'E', 16, 23], ['E', 16, 3, '!=', 'E', 16, 8], ['E', 16, 14, '=', 'E', 16, 28], ['E', 16, 4, '=', 'E', 17, 4], ['E', 16, 18, '=', 'E', 17, 18], ['E', 18, 0, '!=', 'E', 18, 13], ['E', 17, 15, '=', 'E', 18, 15], ['E', 17, 24, '=', 'E', 18, 24], ['E', 19, 6, '!=', 'E', 19, 19], ['E', 19, 20, '=', 'E', 19, 2], ['E', 21, 2, '=', 'E', 21, 16], ['W', 7, 8, '!=', 'W', 7, 25], ['W', 7, 14, '!=', 'W', 7, 18], ['W', 7, 1, '=', 'W', 7, 12], ['W', 8, 0, '!=', 'W', 8, 28], ['W', 8, 30, '!=', 'W', 8, 9], ['W', 8, 1, '=', 'W', 8, 18], ['W', 16, 1, '!=', 'W', 16, 12], ['W', 16, 20, '!=', 'W', 16, 27], ['W', 16, 8, '=', 'W', 16, 25], ['W', 16, 14, '=', 'W', 16, 18], ['W', 16, 4, '!=', 'W', 16, 6], ['W', 16, 22, '!=', 'W', 16, 31], ['W', 23, 0, '!=', 'W', 23, 30], ['W', 23, 1, '!=', 'W', 23, 31], ['W', 23, 14, '=', 'W', 23, 21], ['W', 23, 16, '=', 'W', 23, 25], ['W', 25, 4, '=', 'W', 25, 6], ['W', 25, 22, '=', 'W', 25, 31], ['W', 25, 20, '=', 'W', 25, 27]]
STEP2W = [7]
S = [[3532540064, 2669635003]]
A1 = (3076370033, 3664524768, 1201360328, 3547640024, 3748924566, 518386035, 2144980683, 1040281219, 3064378873, 1052816132, 3167247756, 634637465, 1212609240, 3269198913)
E1 = (1652338785, 511997571, 203171001, 3806966277, 2570398841, 3329275675, 1757653655, 3270689214, 1604129302, 901856013)
W1 = (1061250904, 4271375563, 1671990287, 216735629, 2727137626, 2007099796)
SFS = ((3441920384, 454205522, 3095185574, 2850052549, 3385056133, 1822733749, 1674656449, 3224543006), (1224484635, 2680824013, 3431594351, 4232067439, 2335345844, 1804726136, 2549725031, 3259301957, 1061250904, 4271375563, 1671990287, 216735629, 2727137626, 2007099796, 3532540064, 2669635003), (1224484635, 2680824013, 3431594351, 4232067439, 2335345844, 1804726136, 2549725031, 3796172869, 989949784, 3734504651, 1722392229, 216206221, 2727137626, 2007099796, 3532540064, 2606722491))


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M32


def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def IF(x, y, z): return ((x & y) ^ (~x & z)) & M32
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)


def compress(cv, m):
    w = list(m)
    a, b, c, d, e, f, g, h = cv
    for i in range(R):
        if i >= 16:
            w.append((s1(w[i - 2]) + w[i - 7] + s0(w[i - 15]) + w[i - 16]) & M32)
        t1 = (h + S1(e) + IF(e, f, g) + K[i] + w[i]) & M32
        t2 = (S0(a) + MAJ(a, b, c)) & M32
        h, g, f, e, d, c, b, a = g, f, e, (d + t1) & M32, c, b, a, (t1 + t2) & M32
    return [(x + y) & M32 for x, y in zip((a, b, c, d, e, f, g, h), cv)]


PAD64 = [0x80000000] + [0] * 14 + [512]


def ok_word(name, v):
    vm, vv, dm = COND[name]
    return (v & vm) == vv


def ok_rel(vals, maxidx):
    for (w1, i1, b1, op, w2, i2, b2) in REL:
        if max(i1, i2) != maxidx:
            continue
        k1, k2 = '%s%d' % (w1, i1), '%s%d' % (w2, i2)
        if k1 not in vals or k2 not in vals:
            continue
        eq = ((vals[k1] >> b1) & 1) == ((vals[k2] >> b2) & 1)
        if eq != (op == '='):
            return False
    return True


def second_block(cv1, w0_15, primed):
    """run steps 0..16 of the second block from cv1; returns a dict of A_i, E_i, W_i values"""
    vals = {}
    A = {-1: cv1[0], -2: cv1[1], -3: cv1[2], -4: cv1[3]}
    E = {-1: cv1[4], -2: cv1[5], -3: cv1[6], -4: cv1[7]}
    w = list(w0_15)
    if primed:
        w = [x ^ COND['W%d' % i][2] for i, x in enumerate(w)]
    for i in range(17):
        if i >= 16:
            w.append((s1(w[i - 2]) + w[i - 7] + s0(w[i - 15]) + w[i - 16]) & M32)
        E[i] = (A[i - 4] + E[i - 4] + S1(E[i - 1]) + IF(E[i - 1], E[i - 2], E[i - 3]) + K[i] + w[i]) & M32
        A[i] = (E[i] - A[i - 4] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & M32
    for i in range(-4, 17):
        vals['A%d' % i], vals['E%d' % i] = A[i], E[i]
    for i in range(17):
        vals['W%d' % i] = w[i]
    return vals


def pair_ok(u, p, i):
    for n in 'AEW':
        k = '%s%d' % (n, i)
        if k not in u:
            continue
        vm, vv, dm = COND[k]
        if (u[k] & vm) != vv or (u[k] ^ p[k]) != dm:
            return False
    return ok_rel(u, i) is not False


def derive_w(cv1):
    """Step 2: E3..E0 and W7..W0 from CV1 and the Step-1 words"""
    A = {i: A1[i] for i in range(14)}
    E = {i + 4: E1[i] for i in range(10)}
    A[-1], A[-2], A[-3], A[-4] = cv1[0], cv1[1], cv1[2], cv1[3]
    E[-1], E[-2], E[-3], E[-4] = cv1[4], cv1[5], cv1[6], cv1[7]
    for i in range(3, -1, -1):
        E[i] = (A[i] + A[i - 4] - S0(A[i - 1]) - MAJ(A[i - 1], A[i - 2], A[i - 3])) & M32
    w = {}
    for i in range(7, -1, -1):
        w[i] = (E[i] - A[i - 4] - E[i - 4] - S1(E[i - 1]) - IF(E[i - 1], E[i - 2], E[i - 3]) - K[i]) & M32
    return w


def stream(seed):
    ctr = 0
    while True:
        h = hashlib.sha256(('%s:%d' % (seed, ctr)).encode()).digest()
        ctr += 1
        for k in range(8):
            yield int.from_bytes(h[4 * k:4 * k + 4], 'big')


def trial(seed, first):
    rnd = stream(seed)
    obs = {'blocks': 0, 'valid': 0, 'w16': 0, 'e16': 0, 'pair16': 0}
    seen = {}
    pair = None
    last_valid = None
    for _ in range(B):
        m0 = [next(rnd) for _ in range(16)]
        cv1 = compress(IV, m0)
        dig = compress(cv1, PAD64)
        dint = 0
        for x in dig:
            dint = (dint << 32) | x
        key = dint & MASK
        if pair is None and key in seen and seen[key] != m0:
            a = b''.join(x.to_bytes(4, 'big') for x in seen[key])
            b = b''.join(x.to_bytes(4, 'big') for x in m0)
            pair = (a, b)
        seen.setdefault(key, m0)
        obs['blocks'] += 1
        w = derive_w(cv1)
        if not all(ok_word('W%d' % i, w[i]) for i in STEP2W):
            continue
        if not all(ok_rel({'W%d' % i: w[i]}, i) is not False for i in STEP2W):
            continue
        obs['valid'] += 1
        last_valid = (cv1, w)
        for (w14, w15) in S:
            w0_15 = [w[i] for i in range(8)] + list(W1) + [w14, w15]
            u = second_block(cv1, w0_15, False)
            if ok_word('W16', u['W16']) and ok_rel({'W16': u['W16']}, 16) is not False:
                obs['w16'] += 1
            if ok_word('E16', u['E16']):
                obs['e16'] += 1
            pr = second_block([x ^ 0 for x in cv1], w0_15, True)
            if all(pair_ok(u, pr, i) for i in range(0, 17)):
                obs['pair16'] += 1
    if first:
        # every element of S passes steps 14 and 15 exactly, for any chaining value (checked on this trial's last CV1)
        while last_valid is None:      # draw further blocks from the same stream until one is valid
            m0 = [next(rnd) for _ in range(16)]
            c1 = compress(IV, m0)
            w1 = derive_w(c1)
            if all(ok_word('W%d' % i, w1[i]) and ok_rel({'W%d' % i: w1[i]}, i) is not False for i in STEP2W):
                last_valid = (c1, w1)
        cv1, w = last_valid
        good = 0
        for (w14, w15) in S:
            w0_15 = [w[i] for i in range(8)] + list(W1) + [w14, w15]
            u = second_block(cv1, w0_15, False)
            pr = second_block(cv1, w0_15, True)
            good += all(pair_ok(u, pr, i) for i in (14, 15))
        obs['s_steps14_15_ok'] = good
        obs['s_size'] = len(S)
        sfs_cv, sm, smp = SFS
        obs['sfs_pair_collides'] = int(compress(sfs_cv, sm) == compress(sfs_cv, smp) and sm != smp)
    return pair, obs


def main():
    req = json.load(sys.stdin)
    rows = []
    for entry in req['trials']:
        pair, obs = trial(entry['seed'], entry['trial'] == 0)
        rows.append({'trial': entry['trial'], 'message_a_hex': pair[0].hex() if pair else None,
                     'message_b_hex': pair[1].hex() if pair else None, 'observations': obs})
    sys.stdout.write(json.dumps({'schema_version': 1, 'trials': rows}, separators=(',', ':'), sort_keys=True))


if __name__ == '__main__':
    main()
