"""
Data Classification Utilities
=============================

Provides utilities to load, validate and summarize the data
classification policy defined for the LGPD Data Protection Pipeline.
"""

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


# ============================================================
# CONSTANTS
# ============================================================

VALID_CLASSIFICATIONS = {
    "non_personal_data",
    "personal_data",
    "sensitive_personal_data",
}

VALID_IDENTIFICATION_TYPES = {
    "direct",
    "indirect",
    "none",
}

VALID_PROTECTION_LEVELS = {
    "low",
    "medium",
    "high",
    "critical",
}

VALID_PROTECTION_ACTIONS = {
    "retain",
    "remove",
    "pseudonymize",
    "generalize",
    "mask",
}


# ============================================================
# LOAD CLASSIFICATION CONFIG
# ============================================================

def load_classification_config(
    config_path: Path,
) -> dict[str, Any]:
    """
    Loads the data classification configuration from YAML.

    Args:
        config_path:
            Path to the classification YAML file.

    Returns:
        Dictionary containing the classification configuration.

    Raises:
        FileNotFoundError:
            If the configuration file does not exist.

        ValueError:
            If the YAML structure is invalid.
    """

    if not config_path.exists():
        raise FileNotFoundError(
            f"Classification config not found: {config_path}"
        )

    with config_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            "Classification configuration must be a YAML object."
        )

    if "columns" not in config:
        raise ValueError(
            "Classification configuration must contain "
            "a 'columns' section."
        )

    if not isinstance(config["columns"], dict):
        raise ValueError(
            "'columns' must be a YAML object."
        )

    return config


# ============================================================
# LOAD DATASET SCHEMA
# ============================================================

def load_dataset(
    dataset_path: Path,
) -> pd.DataFrame:
    """
    Loads the Raw Parquet dataset.

    Args:
        dataset_path:
            Path to the Raw dataset.

    Returns:
        Raw customer DataFrame.
    """

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {dataset_path}"
        )

    return pd.read_parquet(dataset_path)


# ============================================================
# COLUMN COVERAGE VALIDATION
# ============================================================

def validate_column_coverage(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:
    """
    Validates whether the dataset columns and classification
    configuration are aligned.

    Returns:
        List containing validation errors.
    """

    errors = []

    dataset_columns = set(dataframe.columns)
    classified_columns = set(config["columns"].keys())

    missing_classification = (
        dataset_columns - classified_columns
    )

    unknown_columns = (
        classified_columns - dataset_columns
    )

    for column in sorted(missing_classification):
        errors.append(
            f"Column '{column}' exists in the dataset "
            "but has no classification."
        )

    for column in sorted(unknown_columns):
        errors.append(
            f"Column '{column}' exists in the classification "
            "configuration but not in the dataset."
        )

    return errors


# ============================================================
# CLASSIFICATION RULE VALIDATION
# ============================================================

def validate_classification_rules(
    config: dict[str, Any],
) -> list[str]:
    """
    Validates classification metadata and protection rules.

    Returns:
        List containing validation errors.
    """

    errors = []

    for column, metadata in config["columns"].items():

        if not isinstance(metadata, dict):
            errors.append(
                f"Column '{column}' has invalid metadata."
            )
            continue

        classification = metadata.get(
            "classification"
        )

        identification = metadata.get(
            "identification"
        )

        protection_level = metadata.get(
            "protection_level"
        )

        purpose = metadata.get(
            "purpose",
            {},
        )

        protection = metadata.get(
            "protection",
            {},
        )

        action = protection.get(
            "action"
        )

        # ----------------------------------------------------
        # Classification
        # ----------------------------------------------------

        if classification not in VALID_CLASSIFICATIONS:
            errors.append(
                f"Column '{column}' has invalid classification: "
                f"'{classification}'."
            )

        # ----------------------------------------------------
        # Identification
        # ----------------------------------------------------

        if identification not in VALID_IDENTIFICATION_TYPES:
            errors.append(
                f"Column '{column}' has invalid identification "
                f"type: '{identification}'."
            )

        # ----------------------------------------------------
        # Protection level
        # ----------------------------------------------------

        if protection_level not in VALID_PROTECTION_LEVELS:
            errors.append(
                f"Column '{column}' has invalid protection "
                f"level: '{protection_level}'."
            )

        # ----------------------------------------------------
        # Purpose
        # ----------------------------------------------------

        if "required" not in purpose:
            errors.append(
                f"Column '{column}' does not define "
                "'purpose.required'."
            )

        elif not isinstance(
            purpose["required"],
            bool,
        ):
            errors.append(
                f"Column '{column}' has invalid "
                "'purpose.required'. Expected boolean."
            )

        # ----------------------------------------------------
        # Protection action
        # ----------------------------------------------------

        if action not in VALID_PROTECTION_ACTIONS:
            errors.append(
                f"Column '{column}' has invalid protection "
                f"action: '{action}'."
            )

        # ----------------------------------------------------
        # Generalization
        # ----------------------------------------------------

        if action == "generalize":

            if not protection.get("method"):
                errors.append(
                    f"Column '{column}' uses generalization "
                    "but does not define a method."
                )

            if not protection.get("output_column"):
                errors.append(
                    f"Column '{column}' uses generalization "
                    "but does not define an output column."
                )

        # ----------------------------------------------------
        # Pseudonymization
        # ----------------------------------------------------

        if action == "pseudonymize":

            if not protection.get("method"):
                errors.append(
                    f"Column '{column}' uses pseudonymization "
                    "but does not define a method."
                )

    return errors


# ============================================================
# CLASSIFICATION SUMMARY
# ============================================================

def build_classification_summary(
    config: dict[str, Any],
) -> pd.DataFrame:
    """
    Creates a tabular summary of the classification policy.

    Returns:
        DataFrame containing one row per classified column.
    """

    records = []

    for column, metadata in config["columns"].items():

        purpose = metadata.get(
            "purpose",
            {},
        )

        protection = metadata.get(
            "protection",
            {},
        )

        records.append(
            {
                "column": column,
                "classification": metadata.get(
                    "classification"
                ),
                "identification": metadata.get(
                    "identification"
                ),
                "protection_level": metadata.get(
                    "protection_level"
                ),
                "required": purpose.get(
                    "required"
                ),
                "action": protection.get(
                    "action"
                ),
                "method": protection.get(
                    "method"
                ),
                "output_column": protection.get(
                    "output_column"
                ),
            }
        )

    return pd.DataFrame(records)


# ============================================================
# VALIDATION
# ============================================================

def validate_classification(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:
    """
    Executes all classification validations.

    Returns:
        List containing all validation errors.
    """

    errors = []

    errors.extend(
        validate_column_coverage(
            dataframe=dataframe,
            config=config,
        )
    )

    errors.extend(
        validate_classification_rules(
            config=config,
        )
    )

    return errors