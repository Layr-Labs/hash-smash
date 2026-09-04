"""HashSmash's paired-lane untrusted-evidence AI review harness."""

from .bedrock_adapter import BedrockClient, BedrockConfig
from .paired_review import aggregate_paired_reviews, run_paired_review, select_lane_aggregate
from .provider_adapter import OpenRouterClient, OpenRouterConfig
from .schema_validation import ReviewValidationError, validate_review

__all__ = [
    "BedrockClient",
    "BedrockConfig",
    "OpenRouterClient",
    "OpenRouterConfig",
    "ReviewValidationError",
    "aggregate_paired_reviews",
    "run_paired_review",
    "select_lane_aggregate",
    "validate_review",
]
