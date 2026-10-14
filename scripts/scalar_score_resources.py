"""Read existing v5 resource bounds without choosing a scalar scoring policy.

This module does not authenticate an artifact or establish qualification. Callers
must obtain metrics from an independently verified official score. Historical
artifact bindings and reviewed bounds remain unchanged; no candidate or judge
reconstruction is consulted here.

The original scalar scorer and offline plan filler share this helper. Its source
is explicitly included in the target's implementation fingerprint.
"""

from __future__ import annotations

import math
from typing import Any, Mapping

from verifier.errors import VerificationError


def read_v5_score_resources(metrics: Mapping[str, Any]) -> tuple[float, float]:
    """Return (timeLog2, memoryLog2Bytes) from compatible official metrics.

    These are log2 target-compression equivalents and log2 bytes respectively,
    independent of scalar normalization. Missing memory is never
    synthesized. Existing scalar, declared bounds and reconstruction fields are
    deliberately ignored, including after a reviewed time rescore.
    """
    if not isinstance(metrics, Mapping):
        raise VerificationError("official score metrics must be an object")
    if metrics.get("costModelId") != "collision-frontier-v5":
        raise VerificationError("official score metrics require collision-frontier-v5")
    if metrics.get("timeUnit") != "target-compressions":
        raise VerificationError("official score metrics require target-compressions")

    def bound(name: str) -> float:
        value = metrics.get(name)
        try:
            valid = type(value) in (int, float) and math.isfinite(value) and value >= 0
        except OverflowError:
            valid = False
        if not valid:
            raise VerificationError(f"official score metrics.{name} must be a finite nonnegative number")
        return float(value)

    return bound("timeLog2"), bound("memoryLog2Bytes")
