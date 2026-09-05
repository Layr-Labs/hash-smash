"""Shared paired-lane schema and intake limits."""

SCHEMA_VERSION = 1
ATTACK_CLASS = "ordinary-collision"
MINIMUM_SUCCESS_PROBABILITY = 0.39

CLAIM_PATH = "claim.json"
PROOF_PATH = "proof.md"
MANIFEST_PATH = "certificates/manifest.json"

# Limits are intentionally smaller than Yukon's outer submission limit.  The workflow
# should retain both layers so an oversized submission is rejected before model calls.
MAX_CLAIM_BYTES = 64 * 1024
MAX_PROOF_BYTES = 512 * 1024
MAX_MANIFEST_BYTES = 64 * 1024
MAX_CERTIFICATE_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 4 * 1024 * 1024
MAX_CERTIFICATES = 16
