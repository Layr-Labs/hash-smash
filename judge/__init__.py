"""HashSmash's untrusted-evidence AI review harness."""

from .aggregate import aggregate_reviews
from .bedrock_adapter import BedrockClient, BedrockConfig
from .provider_adapter import OpenRouterClient, OpenRouterConfig
from .run_review import run_independent_reviews, run_mvp
from .schema_validation import ReviewValidationError, validate_review

__all__ = [
    "BedrockClient",
    "BedrockConfig",
    "OpenRouterClient",
    "OpenRouterConfig",
    "ReviewValidationError",
    "aggregate_reviews",
    "run_independent_reviews",
    "run_mvp",
    "validate_review",
]
