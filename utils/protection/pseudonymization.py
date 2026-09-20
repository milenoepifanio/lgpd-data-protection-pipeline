"""
Data Pseudonymization
=====================

Provides pseudonymization mechanisms used to protect
identifiers in the LGPD Data Protection Pipeline.
"""

import hashlib
import hmac


# ============================================================
# HMAC SHA-256
# ============================================================

def hmac_sha256(
    value: object,
    secret_key: str,
) -> str:
    """
    Pseudonymizes a value using HMAC-SHA256.

    Args:
        value:
            Value to pseudonymize.

        secret_key:
            Secret key used by the HMAC algorithm.

    Returns:
        Hexadecimal HMAC-SHA256 digest.
    """

    if value is None:
        return None

    normalized_value = str(value).encode(
        "utf-8"
    )

    encoded_key = secret_key.encode(
        "utf-8"
    )

    return hmac.new(
        encoded_key,
        normalized_value,
        hashlib.sha256,
    ).hexdigest()