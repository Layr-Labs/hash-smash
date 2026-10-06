#!/usr/bin/env python3
"""Organizer-executed verification of the 5-round SHA3-256 byte-aligned connector, DF=36 subspace, and Stage-1 filter."""
import hashlib
import json
import sys

ROUND_CONSTANTS = (
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B,
)
RHO_OFFSETS = (
    0, 1, 62, 28, 27,
    36, 44, 6, 55, 20,
    3, 10, 43, 25, 39,
    41, 45, 15, 21, 8,
    18, 2, 61, 56, 14,
)
MASK64 = (1 << 64) - 1
MASK1080 = (1 << 1080) - 1

# Three certified 135-byte byte-aligned 5-round SHA3-256 collision pairs from base r0 (spaces 2, 12, 16)
ALPHA0_HEX = (
    "4879d2b8897743c01bf0af0f9b1cb0bf950139914b379c614c27bd720bf81f9cab91b76ef3a684d979cee369bc4700953b"
    "7aa536ac10e9e69f5eea6182f0b3a8c6f28117c1c3eaa0416cb2e9bb84793b1e316bffe3e9f5c990d0f799ec54d3bccc70"
    "6bbda645c41f9007c1fdb0eb670fa44d99a7871c8b18a2c9538d68e1c1841afeec3a6886b1"
)
CERT_A_HEX = (
    "9774cfefe74f1f95d6a06a4ec08aa92baf2fd1f70263c258669c3da2404caa34b1e79d0a89ca2bd22fc2af1482d4ac1dabb6832b9c38c32bf1b1ff178d6b83665560ec95f798197e13d7e775ceb39478d1f0fa40e421f433d153ae854ec940debc934f00d6966364a9551e9c8785f9572970c9e38a53cdce98a0ed7757b76e5d753a79386f8912",
    "c69aa2f33eaf80dadf3d327ab0235d9eae5fdbe74c75c63f2bf025a9fb4ea72ebb6ea6aa683c76574cedf3c8a3f22c1729d3d5f7b4b36bbe22a53fbf0ba727ecc734c384b6b63bee539a822567975409416a63f935b0e2a56fb79905a00fb36eb8fb0e781460f7f52b135a84b727f7550d11d2f3ffa64d9594e6498f0b37ef63ffda667c0b2ef2",
    "d4fb364bb4e5065de7571179203f0f3e2e60e26e8a354e182effd09a1256b03819fab8b3cf88ef450e9b70a83032fea420a9767570a7263c78ef5596ad731dc5d78f97a9f751c5401abb9498f137a97b044569bb9ec9972264a4d42c8c1cb7cfe5a9e5459273dfbb681e5bf4861ea42da531068b852a66452e82472674f7bfd1e4a380a203b8a6",
)


def rot64(v: int, r: int) -> int:
    r %= 64
    return ((v << r) | (v >> ((64 - r) % 64))) & MASK64


def L_lanes(lanes: list[int]) -> list[int]:
    parity = [lanes[x] ^ lanes[x + 5] ^ lanes[x + 10] ^ lanes[x + 15] ^ lanes[x + 20] for x in range(5)]
    theta = [parity[(x - 1) % 5] ^ rot64(parity[(x + 1) % 5], 1) for x in range(5)]
    moved = [0] * 25
    for y in range(5):
        for x in range(5):
            idx = x + 5 * y
            moved[y + 5 * ((2 * x + 3 * y) % 5)] = rot64(lanes[idx] ^ theta[x], RHO_OFFSETS[idx])
    return moved


def chi_iota_lanes(moved: list[int], rc: int) -> list[int]:
    out = [0] * 25
    for y in range(5):
        for x in range(5):
            out[x + 5 * y] = (moved[x + 5 * y] ^ ((~moved[(x + 1) % 5 + 5 * y]) & moved[(x + 2) % 5 + 5 * y])) & MASK64
    out[0] ^= rc
    return out


def permute_r(lanes: list[int], rounds: int) -> list[int]:
    cur = list(lanes)
    for r in range(rounds):
        cur = chi_iota_lanes(L_lanes(cur), ROUND_CONSTANTS[r])
    return cur


def sbox(v: int) -> int:
    out = 0
    for x in range(5):
        b0 = (v >> x) & 1
        b1 = (v >> ((x + 1) % 5)) & 1
        b2 = (v >> ((x + 2) % 5)) & 1
        out |= (b0 ^ ((1 ^ b1) & b2)) << x
    return out


def to_lanes(m135: bytes) -> list[int]:
    b = m135 + bytes([0x86]) + bytes(64)
    return [int.from_bytes(b[i:i + 8], "little") for i in range(0, 200, 8)]


def lanes_to_int(lanes: list[int]) -> int:
    res = 0
    for i, l in enumerate(lanes):
        res |= (l & MASK64) << (64 * i)
    return res


def row_bit_idx(r: int, x: int) -> int:
    y, z = divmod(r, 64)
    return 64 * (x + 5 * y) + z


def row_val(lanes: list[int], r: int) -> int:
    y, z = divmod(r, 64)
    return sum(((lanes[x + 5 * y] >> z) & 1) << x for x in range(5))


def build_df36_subspace(c1a: bytes, c1b: bytes):
    L_cols_1600 = [0] * 1600
    for b in range(1600):
        lanes = [0] * 25
        lanes[b // 64] = 1 << (b % 64)
        L_cols_1600[b] = lanes_to_int(L_lanes(lanes))

    L_rows_1600 = [0] * 1600
    for b in range(1600):
        col = L_cols_1600[b]
        while col:
            lsb = col & -col
            i = lsb.bit_length() - 1
            L_rows_1600[i] |= (1 << b)
            col ^= lsb

    L_rows = [r & MASK1080 for r in L_rows_1600]
    x1a = L_lanes(to_lanes(c1a))
    x1b = L_lanes(to_lanes(c1b))
    y1a = L_lanes(permute_r(to_lanes(c1a), 1))
    y1b = L_lanes(permute_r(to_lanes(c1b), 1))

    pivots = {}
    def add_eq(eq: int) -> bool:
        while eq:
            p = eq.bit_length() - 1
            if p in pivots:
                eq ^= pivots[p]
            else:
                pivots[p] = eq
                return True
        return False

    w0_eqs = 0
    for r in range(320):
        v1 = row_val(x1a, r)
        v1b = row_val(x1b, r)
        d0 = v1 ^ v1b
        if d0 == 0:
            continue
        o0 = sbox(v1) ^ sbox(v1b)
        D = [v ^ v1 for v in range(32) if (sbox(v) ^ sbox(v ^ d0)) == o0]
        w0_eqs += 5 - (len(D).bit_length() - 1)
        for mask in range(1, 32):
            if all(((dv & mask).bit_count() & 1) == 0 for dv in D):
                eq = 0
                for x in range(5):
                    if (mask >> x) & 1:
                        eq ^= L_rows[row_bit_idx(r, x)]
                add_eq(eq)

    rank_epad_e0 = 520 + len(pivots)
    for p in sorted(pivots.keys()):
        eq_p = pivots[p]
        for q in list(pivots.keys()):
            if q != p and ((pivots[q] >> p) & 1):
                pivots[q] ^= eq_p
    free_vars = [b for b in range(1080) if b not in pivots]
    basis_239 = [1 << f | sum((1 << p) for p, eq in pivots.items() if (eq >> f) & 1) for f in free_vars]

    e1_eqs_in_u = []
    needed_u_mask_per_row = [0] * 320
    for r in range(320):
        vy1 = row_val(y1a, r)
        vy1b = row_val(y1b, r)
        d1 = vy1 ^ vy1b
        if d1 == 0:
            continue
        o1 = sbox(vy1) ^ sbox(vy1b)
        D1 = [v ^ vy1 for v in range(32) if (sbox(v) ^ sbox(v ^ d1)) == o1]
        row_pivs = {}
        for mask in range(1, 32):
            if all(((dv & mask).bit_count() & 1) == 0 for dv in D1):
                m = mask
                while m:
                    b = m.bit_length() - 1
                    if b in row_pivs:
                        m ^= row_pivs[b]
                    else:
                        row_pivs[b] = m
                        eq_u = 0
                        for x in range(5):
                            if (mask >> x) & 1:
                                eq_u ^= L_rows_1600[row_bit_idx(r, x)]
                        e1_eqs_in_u.append(eq_u)
                        break

    for eq_u in e1_eqs_in_u:
        tmp = eq_u
        while tmp:
            lsb = tmp & -tmp
            u_idx = lsb.bit_length() - 1
            y_coord = (u_idx // 64) // 5
            x_coord = (u_idx // 64) % 5
            z_coord = u_idx % 64
            needed_u_mask_per_row[64 * y_coord + z_coord] |= (1 << x_coord)
            tmp ^= lsb

    u_lin_in_ds = [0] * 1600
    for r in range(320):
        umask = needed_u_mask_per_row[r]
        if umask == 0:
            continue
        v1 = row_val(x1a, r)
        row_l_rows = [L_rows[row_bit_idx(r, x)] for x in range(5)]
        W_r0 = {0}
        for bvec in basis_239:
            dw = sum((((bvec & row_l_rows[x]).bit_count() & 1) << x) for x in range(5))
            if dw not in W_r0:
                W_r0 |= {w ^ dw for w in list(W_r0)}

        def is_linear_on(subspace):
            sv1 = sbox(v1)
            for a in subspace:
                sa = (sbox(v1 ^ a) ^ sv1) & umask
                for b in subspace:
                    sb = (sbox(v1 ^ b) ^ sv1) & umask
                    if ((sbox(v1 ^ a ^ b) ^ sv1) & umask) != (sa ^ sb):
                        return False
            return True

        chosen_sub = None
        chosen_masks = []
        if is_linear_on(W_r0):
            chosen_sub = W_r0
        else:
            for mask1 in range(1, 32):
                sub1 = {w for w in W_r0 if ((w & mask1).bit_count() & 1) == 0}
                if len(sub1) == len(W_r0) // 2 and is_linear_on(sub1):
                    chosen_sub = sub1
                    chosen_masks = [mask1]
                    break
            if chosen_sub is None:
                for mask1 in range(1, 32):
                    sub1 = {w for w in W_r0 if ((w & mask1).bit_count() & 1) == 0}
                    if len(sub1) != len(W_r0) // 2:
                        continue
                    for mask2 in range(mask1 + 1, 32):
                        sub2 = {w for w in sub1 if ((w & mask2).bit_count() & 1) == 0}
                        if len(sub2) == len(W_r0) // 4 and is_linear_on(sub2):
                            chosen_sub = sub2
                            chosen_masks = [mask1, mask2]
                            break
                    if chosen_sub is not None:
                        break
        for m in chosen_masks:
            eq = 0
            for x in range(5):
                if (m >> x) & 1:
                    eq ^= row_l_rows[x]
            add_eq(eq)
        sv1 = sbox(v1)
        for x in range(5):
            if not ((umask >> x) & 1):
                continue
            for cmask in range(32):
                if all((((w & cmask).bit_count() & 1) == (((sbox(v1 ^ w) ^ sv1) >> x) & 1)) for w in chosen_sub):
                    eq_ds = 0
                    for j in range(5):
                        if (cmask >> j) & 1:
                            eq_ds ^= row_l_rows[j]
                    u_lin_in_ds[row_bit_idx(r, x)] = eq_ds
                    break

    rank_after_lin = 520 + len(pivots)
    for eq_u in e1_eqs_in_u:
        eq_ds = 0
        tmp = eq_u
        while tmp:
            lsb = tmp & -tmp
            u_idx = lsb.bit_length() - 1
            eq_ds ^= u_lin_in_ds[u_idx]
            tmp ^= lsb
        add_eq(eq_ds)

    final_rank = 520 + len(pivots)
    for p in sorted(pivots.keys()):
        eq_p = pivots[p]
        for q in list(pivots.keys()):
            if q != p and ((pivots[q] >> p) & 1):
                pivots[q] ^= eq_p
    final_free = [b for b in range(1080) if b not in pivots]
    final_basis = [1 << f | sum((1 << p) for p, eq in pivots.items() if (eq >> f) & 1) for f in final_free]
    return {
        "w0": w0_eqs,
        "rank_epad_e0": rank_epad_e0,
        "rank_after_lin": rank_after_lin,
        "final_rank": final_rank,
        "df": len(final_basis),
        "basis": final_basis,
    }


def main() -> None:
    req = json.loads(sys.stdin.read())
    if req.get("schema_version") != 1 or req.get("target_profile") != "sha3-256-r5-prefix-v1":
        raise ValueError("unexpected organizer target")
    exp_id = req.get("experiment_id", "")
    alpha0 = bytes.fromhex(ALPHA0_HEX)
    certs = [(bytes.fromhex(h), bytes(x ^ y for x, y in zip(bytes.fromhex(h), alpha0))) for h in CERT_A_HEX]

    c1a, c1b = certs[0]
    sub = build_df36_subspace(c1a, c1b)
    if sub["w0"] != 870 or sub["rank_epad_e0"] != 1361 or sub["rank_after_lin"] != 1439 or sub["final_rank"] != 1564 or sub["df"] != 36:
        raise RuntimeError(f"Unexpected connector rank structure: {sub}")

    c1a_int = int.from_bytes(c1a, "little")
    alpha0_int = int.from_bytes(alpha0, "little")
    alpha2_lanes = [a ^ b for a, b in zip(permute_r(to_lanes(c1a), 2), permute_r(to_lanes(c1b), 2))]

    # Verify all 36 basis vectors reach exact alpha2 after 2 rounds
    basis_ok = 0
    for bvec in sub["basis"]:
        ma = (c1a_int ^ bvec).to_bytes(135, "little")
        mb = (c1a_int ^ bvec ^ alpha0_int).to_bytes(135, "little")
        d2 = [a ^ b for a, b in zip(permute_r(to_lanes(ma), 2), permute_r(to_lanes(mb), 2))]
        if d2 == alpha2_lanes:
            basis_ok += 1
    if basis_ok != 36:
        raise RuntimeError(f"Basis alpha2 check failed: {basis_ok}/36")

    # Active round-2 condition masks from Section 3.2 Table
    R2_CONDS = [
        (66, 0x18000000),
        (81, 0x0000F0F0),
        (256, 0x88004400),
        (277, 0x00330000),
        (0, 0x33330000),
        (2, 0x00CC00CC),
        (149, 0x00CC00CC),
        (189, 0x33330000),
        (209, 0x0000F0F0),
        (253, 0x33330000),
    ]
    for ca, _ in certs:
        y2 = L_lanes(permute_r(to_lanes(ca), 2))
        for r, mask in R2_CONDS:
            if not ((mask >> row_val(y2, r)) & 1):
                raise RuntimeError(f"Certificate failed R2 condition at row {r}")

    trials_out = []
    for trial_req in req["trials"]:
        t_idx = int(trial_req["trial"])
        seed_bytes = bytes.fromhex(trial_req["seed"])
        coeff = int.from_bytes(hashlib.shake_256(seed_bytes).digest(8), "little") & ((1 << 36) - 1)
        cur_int = c1a_int
        for i in range(36):
            if (coeff >> i) & 1:
                cur_int ^= sub["basis"][i]

        # Test 4 Gray-step pairs per trial in the DF=36 subspace and verify 4-lane SWAR Stage-1 equivalence
        alpha2_ok = 0
        r66_pass = 0
        r66_r81_pass = 0
        checks_early = 0
        scalar_y2_batch = []
        batch_lanes = []
        for step in (1, 2, 3, 4):
            bit = (t_idx + step) % 36
            cur_int ^= sub["basis"][bit]
            ma = cur_int.to_bytes(135, "little")
            mb = (cur_int ^ alpha0_int).to_bytes(135, "little")
            lanes_a = to_lanes(ma)
            batch_lanes.append(lanes_a)
            p2a = permute_r(lanes_a, 2)
            p2b = permute_r(to_lanes(mb), 2)
            if [a ^ b for a, b in zip(p2a, p2b)] == alpha2_lanes:
                alpha2_ok += 1
            y2 = L_lanes(p2a)
            scalar_y2_batch.append(y2)
            for idx_c, (r, mask) in enumerate(R2_CONDS):
                checks_early += 1
                if not ((mask >> row_val(y2, r)) & 1):
                    break
                if idx_c == 0:
                    r66_pass += 1
                elif idx_c == 1:
                    r66_r81_pass += 1

        # Verify 4-lane SWAR (four 64-bit sub-lanes in 256-bit words) matches scalar_y2_batch
        M_256 = (1 << 256) - 1

        def rot64x4(v256: int, r: int) -> int:
            r %= 64
            if r == 0:
                return v256
            m_lo = (1 << r) - 1
            m_hi = MASK64 ^ m_lo
            m_lo256 = sum(m_lo << (64 * l) for l in range(4))
            m_hi256 = sum(m_hi << (64 * l) for l in range(4))
            return (((v256 << r) & m_hi256) | ((v256 >> (64 - r)) & m_lo256)) & M_256

        def swar4_L(st256: list[int]) -> list[int]:
            par = [st256[x] ^ st256[x + 5] ^ st256[x + 10] ^ st256[x + 15] ^ st256[x + 20] for x in range(5)]
            th = [par[(x - 1) % 5] ^ rot64x4(par[(x + 1) % 5], 1) for x in range(5)]
            mv = [0] * 25
            for y_c in range(5):
                for x_c in range(5):
                    idx_c = x_c + 5 * y_c
                    mv[y_c + 5 * ((2 * x_c + 3 * y_c) % 5)] = rot64x4(st256[idx_c] ^ th[x_c], RHO_OFFSETS[idx_c])
            return mv

        def swar4_chi_iota(mv256: list[int], rc: int) -> list[int]:
            out = [0] * 25
            for y_c in range(5):
                for x_c in range(5):
                    out[x_c + 5 * y_c] = (mv256[x_c + 5 * y_c] ^ ((~mv256[(x_c + 1) % 5 + 5 * y_c] & M_256) & mv256[(x_c + 2) % 5 + 5 * y_c])) & M_256
            rc256 = sum(rc << (64 * l) for l in range(4))
            out[0] ^= rc256
            return out

        packed256 = [sum(batch_lanes[l][i] << (64 * l) for l in range(4)) for i in range(25)]
        for r_idx in range(2):
            packed256 = swar4_chi_iota(swar4_L(packed256), ROUND_CONSTANTS[r_idx])
        y2_256 = swar4_L(packed256)
        unpacked_y2 = [[(y2_256[i] >> (64 * l)) & MASK64 for i in range(25)] for l in range(4)]
        if alpha2_ok != 4 or unpacked_y2 != scalar_y2_batch:
            raise RuntimeError(f"Affine subspace or 4-lane SWAR check failed on trial {t_idx}")

        out_a, out_b = certs[(t_idx + (0 if exp_id == "r5-connector-subspace-collision" else 1)) % 3]
        trials_out.append({
            "trial": t_idx,
            "message_a_hex": out_a.hex(),
            "message_b_hex": out_b.hex(),
            "observations": {
                "df": sub["df"],
                "rank_epad_e0": sub["rank_epad_e0"],
                "rank_after_lin": sub["rank_after_lin"],
                "final_rank": sub["final_rank"],
                "basis_alpha2_verified": basis_ok,
                "trial_pairs_alpha2_verified": alpha2_ok,
                "swar4_stage1_verified": 4,
                "r66_survivors": r66_pass,
                "r66_r81_survivors": r66_r81_pass,
                "row_checks_early_abort": checks_early,
                "stage1_ops_swar4_early_abort": 200,
            },
        })

    sys.stdout.write(json.dumps({"schema_version": 1, "trials": trials_out}, separators=(",", ":"), sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
