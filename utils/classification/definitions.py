"""
Data Classification Definitions
===============================

Defines the supported classification, identification,
protection levels and protection actions used by the
LGPD Data Protection Pipeline.
"""


# DATA CLASSIFICATIONS

VALID_CLASSIFICATIONS = {
    "non_personal_data",
    "personal_data",
    "sensitive_personal_data",
}


# IDENTIFICATION TYPES

VALID_IDENTIFICATION_TYPES = {
    "direct",
    "indirect",
    "none",
}


# PROTECTION LEVELS

VALID_PROTECTION_LEVELS = {
    "low",
    "medium",
    "high",
    "critical",
}


# PROTECTION ACTIONS

VALID_PROTECTION_ACTIONS = {
    "retain",
    "remove",
    "pseudonymize",
    "generalize",
    "mask",
}