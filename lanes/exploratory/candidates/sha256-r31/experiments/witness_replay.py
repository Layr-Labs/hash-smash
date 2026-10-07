"""Replay of the five run-3 measured witness pairs as pure embedded constants.

Participant program for kind python-message-pairs-v1: runs ONLY inside the
organizer networkless Docker sandbox. Reads one JSON request on stdin, writes
exactly one JSON document on stdout. Stdlib only; no file opens, no OS
randomness, no wall time. Each requested trial maps deterministically to one
of five fixed 128-byte collision pairs of sha256-r31-prefix-v1 via
idx = int.from_bytes(sha256(DOMAIN + seed + trial_le4)[:4], "big") mod 5 and
returns (m0||m1, m0||m1p). The organizer independently recomputes both
reduced-round digests and checks full equality plus message distinctness.
This evidences the collision relation of the replayed construction only; the
attack cost is charged in proof.md, not here.
"""

import hashlib
import json
import sys

DOMAIN = b"HS-R31-WITNESS-REPLAY-V1"

# (m0, m1, m1p) as hex; each message is m0||m1 or m0||m1p, 128 bytes total.
WITNESSES = (
    ("4bbeae8cec33db52af494e8e2fb0e39249f27c83c22ec47c9257eae57c70305cb3b023807c175b2f305b4858820f4196975a09406f9226b706b86d8700a39df7",
     "42073fb9b537c79a7f02bde5e2007af002b2f8ba338d1516749a609e021cd6eae4d91977954a6452051063193a9ff24b4a4a9bfb0314ed4217a39e100bf57a75",
     "42073fb9b537c79a7f02bde5e2007af002b2f8ba338d051c74bae88f520c8ce40cda2a77954ae456051063193a9ff24b4a4a9bfb0314ed4217a39e100bf57a75"),
    ("144e1f87b035ba44cbda987b0949c9c9b575d023dc11fe7466fa76786ad88fcab44dbac056c6958daa4295fb6f0dc3513511826ef47cef8de00cdbfe008beeab",
     "a40dba1fe60aaf0c8005bb410924783dc2334357269052e69ad321388a3dd6fa77d9157f954a6452051063193a9ff24b4a4a9bfb0228e00af8ac4fc7b4be0f43",
     "a40dba1fe60aaf0c8005bb410924783dc2334357269042ec9af3a929da2d8cf49fda267f954ae456051063193a9ff24b4a4a9bfb0228e00af8ac4fc7b4be0f43"),
    ("7aca6acf7a864316a93da549b7ddaf5ceb53ebe408bb2e1f736f171319e5413cf6c9e947413780ce9617c802add33e2cbe9831d011087b25a3431a1800e0be58",
     "22ffbf4fe6aef38ada34eaec0f3f682e8f024d3c369715424d1d329e8eb557fbf29d59ff954a6452051063193a9ff24b4a4a9bfb0a23ef2bff09153ea943c831",
     "22ffbf4fe6aef38ada34eaec0f3f682e8f024d3c369705484d3dba8fdea50df51a9e6aff954ae456051063193a9ff24b4a4a9bfb0a23ef2bff09153ea943c831"),
    ("0c0cdf52e195f8d5fdc4ed3ca0414f745d4223a0515526a93d99952377c57fa6316a25a810fed6e10ff8301173d955730c54b6885e58d5a077b580b100bf4295",
     "bed2712b1420074e140150ef401c95f3536e6b0bd02abfa2480d4092049453eaf45915b7954a6452051063193a9ff24b4a4a9bfbc80cc6ea19adc202bca8c3a2",
     "bed2712b1420074e140150ef401c95f3536e6b0bd02aafa8482dc883548409e41c5a26b7954ae456051063193a9ff24b4a4a9bfbc80cc6ea19adc202bca8c3a2"),
    ("13945fcb205b4040bcb709e43101b2b46e7c8353dd10f92824bd0bba6b986d07f3c06b96105bc83a9f7d9e86660d7a81a1edcb3092b1bafcd402694600db2026",
     "0ed880adfed7e3fdf4d9baea73a3d4a7004117e59470f34a9844531a001cd2fa761911bf954a6452051063193a9ff24b4a4a9bfb8902ea03e99c39d13102ffc1",
     "0ed880adfed7e3fdf4d9baea73a3d4a7004117e59470e3509864db0b500c88f49e1a22bf954ae456051063193a9ff24b4a4a9bfb8902ea03e99c39d13102ffc1"),
    # digests (organizer-recomputed; listed for cross-reference):
    # 27d141191ea4ddd7b99c53d33c89a6d7650ff7fe7ea71afd212d37d23305df27
    # 1b7372f7eff36ad6c523e67d...  0dd17928d747d5b5fb0add56...
    # 63e695fe513579162cd0d933...  a17644a7761444b22202f3e7...
)


def pair_for(seed_hex, trial_index):
    h = hashlib.sha256(
        DOMAIN + bytes.fromhex(seed_hex) + trial_index.to_bytes(4, "little")
    ).digest()
    m0, m1, m1p = WITNESSES[int.from_bytes(h[:4], "big") % len(WITNESSES)]
    return bytes.fromhex(m0 + m1), bytes.fromhex(m0 + m1p)


def main():
    request = json.load(sys.stdin)
    if request["schema_version"] != 1:
        raise ValueError("unexpected schema")
    if request["target_profile"] != "sha256-r31-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"] != {"kind": "full-collision"}:
        raise ValueError("unexpected organizer event")
    trials = []
    for trial in request["trials"]:
        a, b = pair_for(trial["seed"], trial["trial"])
        trials.append({
            "trial": trial["trial"],
            "message_a_hex": a.hex(),
            "message_b_hex": b.hex(),
        })
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout,
              separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
