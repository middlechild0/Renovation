"""
Security utilities: safe env loading, secret masking, rotation stubs
"""

import os
from typing import Optional

SAFE_ENV_KEYS = {
    # Known keys (extend as needed)
    "FOURSQUARE_API_KEY",
    "TOMTOM_API_KEY",
    "YELP_API_KEY",
    "STRIPE_SECRET_KEY",
}


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Safely get environment variable without logging its value."""
    try:
        return os.getenv(key, default)
    except Exception:
        return default


def mask_secret(value: str, keep: int = 4) -> str:
    """Return masked representation of a secret for logging (first/last few chars)."""
    if not value:
        return "<empty>"
    value = str(value)
    if len(value) <= keep * 2:
        return "*" * len(value)
    return value[:keep] + ("*" * (len(value) - keep * 2)) + value[-keep:]


def log_env_status() -> None:
    """Log presence of environment keys without exposing the full values."""
    for key in sorted(SAFE_ENV_KEYS):
        val = os.getenv(key)
        print(f"ENV {key}: {'set' if val else 'missing'}")
        if val:
            print(f"  masked: {mask_secret(val)}")


def rotate_api_key(service: str) -> bool:
    """
    Stub for API key rotation; integrate with provider APIs.
    Returns False until implemented with provider-specific rotation.
    """
    print(f"[rotation] Key rotation requested for service={service}. Implement provider API.")
    return False
