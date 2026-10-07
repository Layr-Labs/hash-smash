"""Evidence adapter for proof.md's 24/25-byte RAM construction.

Only the organizer's validated networkless executor may run this file.
Python and JSON work are not the claimed primitive-RAM operation count.
"""
import json
import sys


def pair(seed):
    f = (1 << 32) - 1
    q = (1 << 128) - 1
    k = (0x3C6EF372 + 0x1F83D9AB) & f
    x = k & 1
    xp = x + 1
    r = int.from_bytes(bytes.fromhex(seed), "little")
    p = r & q
    aw = p | (x << 128)
    bw = p | (xp << 128) | (f << 160)
    a = (k + x) & f
    ap = (k + xp) & f
    e = ((a ^ 24) ^ (ap ^ 25)) | (a ^ ((ap + f) & f))
    if not (24 != 25) or e != 0:
        return None, None
    return aw.to_bytes(32, "little")[:24].hex(), bw.to_bytes(32, "little")[:25].hex()


def main():
    request = json.load(sys.stdin)
    trials = []
    for trial in request["trials"]:
        a, b = pair(trial["seed"])
        trials.append({"trial": trial["trial"], "message_a_hex": a,
                       "message_b_hex": b, "observations": {}})
    print(json.dumps({"schema_version": 1, "trials": trials}, sort_keys=True))


if __name__ == "__main__":
    main()
