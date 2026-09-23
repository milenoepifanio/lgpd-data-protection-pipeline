"""
Data Classification Validators
==============================

Validates dataset coverage and classification rules defined
for the LGPD Data Protection Pipeline.
"""

from typing import Any

import pandas as pd

from utils.classification.definitions import (
    VALID_CLASSIFICATIONS,
    VALID_IDENTIFICATION_TYPES,
    VALID_PROTECTION_ACTIONS,
    VALID_PROTECTION_LEVELS,
)

# COLUMN COVERAGE

def validate_column_coverage(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:

    errors = []

    dataset_columns = set(
        dataframe.columns
    )

    classified_columns = set(
        config["columns"].keys()
    )

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


# CLASSIFICATION RULES

def validate_classification_rules(
    config: dict[str, Any],
) -> list[str]:

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

        if classification not in VALID_CLASSIFICATIONS:
            errors.append(
                f"Column '{column}' has invalid classification: "
                f"'{classification}'."
            )

        if identification not in VALID_IDENTIFICATION_TYPES:
            errors.append(
                f"Column '{column}' has invalid identification "
                f"type: '{identification}'."
            )

        if protection_level not in VALID_PROTECTION_LEVELS:
            errors.append(
                f"Column '{column}' has invalid protection "
                f"level: '{protection_level}'."
            )

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

        if action not in VALID_PROTECTION_ACTIONS:
            errors.append(
                f"Column '{column}' has invalid protection "
                f"action: '{action}'."
            )

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


        if (
            action == "pseudonymize"
            and not protection.get("method")
        ):
            errors.append(
                f"Column '{column}' uses pseudonymization "
                "but does not define a method."
            )

    return errors


# COMPLETE VALIDATION

def validate_classification(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:

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