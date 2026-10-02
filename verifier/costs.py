"""Public operation prices in target-compression equivalents."""

import math

from .errors import VerificationError

UNIT_WEIGHTS = {"target_compression": 1, "word_operation": 1}


def validate_weights(weights):
    if not isinstance(weights, dict) or set(weights) != set(UNIT_WEIGHTS):
        raise VerificationError("operation weights must price target_compression and word_operation")
    for value in weights.values():
        try:
            valid = type(value) in (int, float) and math.isfinite(value) and value > 0
        except OverflowError:
            valid = False
        if not valid:
            raise VerificationError("operation weights must be finite and positive")
    if weights["target_compression"] != 1:
        raise VerificationError("one target compression must remain one score unit")
    return weights
