
"""
Protection Layer Comparator
===========================

Validates transformations between the Raw and Protected
layers according to the data classification policy.

Validation rules:
- Row count and output schema;
- Retained values;
- Removed columns;
- HMAC-SHA256 pseudonymization;
- Generalized values.
"""

from typing import Any

import pandas as pd

from utils.protection.generalization import (
    generalize_age,
    generalize_cep,
    generalize_income,
)
from utils.protection.processor import (
    build_protected_schema,
)
from utils.protection.pseudonymization import (
    hmac_sha256,
)


# ============================================================
# GENERALIZATION METHODS
# ============================================================

GENERALIZATION_METHODS = {
    "age_range": generalize_age,
    "cep_region": generalize_cep,
    "income_range": generalize_income,
}


# ============================================================
# SERIES COMPARISON
# ============================================================

def count_different_values(
    expected: pd.Series,
    actual: pd.Series,
) -> int:
    """
    Counts differences between two equally sized Series.

    Both Series are compared by row position. Matching null
    values are considered equal.
    """

    expected = expected.reset_index(drop=True)
    actual = actual.reset_index(drop=True)

    if len(expected) != len(actual):
        raise ValueError(
            "Cannot compare Series with different row counts."
        )

    equal_values = expected.eq(actual).fillna(False)

    both_null = (
        expected.isna()
        & actual.isna()
    )

    equal_values = equal_values | both_null

    return int((~equal_values).sum())


# ============================================================
# PROTECTION TRANSFORMATION VALIDATION
# ============================================================

def validate_protection_transformation(
    raw_dataframe: pd.DataFrame,
    protected_dataframe: pd.DataFrame,
    config: dict[str, Any],
    secret_key: str,
) -> list[str]:
    """
    Compares Raw and Protected datasets according to
    the configured protection policy.

    The comparison assumes that the protection pipeline
    preserves row order.

    Args:
        raw_dataframe:
            Original dataset.

        protected_dataframe:
            Protected dataset.

        config:
            Classification and protection policy.

        secret_key:
            Same HMAC secret used to generate the Protected
            dataset.

    Returns:
        List of validation errors. An empty list means
        all checks passed.
    """

    errors: list[str] = []

    # ========================================================
    # ROW COUNT
    # ========================================================

    if len(raw_dataframe) != len(protected_dataframe):

        errors.append(
            "Raw and Protected datasets have different "
            "row counts."
        )

        # Value comparisons require matching row counts.
        return errors

    # ========================================================
    # EXPECTED SCHEMA
    # ========================================================

    expected_columns = build_protected_schema(
        config=config,
    )

    actual_columns = protected_dataframe.columns.tolist()

    if actual_columns != expected_columns:

        errors.append(
            "Protected dataset schema does not match "
            "the configured protection policy."
        )

    # ========================================================
    # PROTECTION RULES
    # ========================================================

    for column, metadata in config["columns"].items():

        protection = metadata.get(
            "protection",
            {},
        )

        action = protection.get("action")

        # ----------------------------------------------------
        # SOURCE COLUMN
        # ----------------------------------------------------

        if column not in raw_dataframe.columns:

            errors.append(
                f"Source column '{column}' is missing "
                "from the Raw dataset."
            )

            continue

        # ----------------------------------------------------
        # REMOVE
        # ----------------------------------------------------

        if action == "remove":

            if column in protected_dataframe.columns:

                errors.append(
                    f"Removed column '{column}' still exists "
                    "in the Protected dataset."
                )

            continue

        # ----------------------------------------------------
        # RETAIN
        # ----------------------------------------------------

        if action == "retain":

            if column not in protected_dataframe.columns:

                errors.append(
                    f"Retained column '{column}' is missing "
                    "from the Protected dataset."
                )

                continue

            different_values = count_different_values(
                expected=raw_dataframe[column],
                actual=protected_dataframe[column],
            )

            if different_values > 0:

                errors.append(
                    f"Retained column '{column}' contains "
                    f"{different_values} modified value(s)."
                )

            continue

        # ----------------------------------------------------
        # PSEUDONYMIZE
        # ----------------------------------------------------

        if action == "pseudonymize":

            if column not in protected_dataframe.columns:

                errors.append(
                    f"Pseudonymized column '{column}' is missing "
                    "from the Protected dataset."
                )

                continue

            method = protection.get("method")

            if method != "hmac_sha256":

                errors.append(
                    f"Unsupported pseudonymization method "
                    f"'{method}' for column '{column}'."
                )

                continue

            if not secret_key:

                errors.append(
                    "HMAC secret key is missing. "
                    "Cannot validate pseudonymization."
                )

                continue

            expected_values = raw_dataframe[column].apply(
                lambda value: hmac_sha256(
                    value=value,
                    secret_key=secret_key,
                )
            )

            different_values = count_different_values(
                expected=expected_values,
                actual=protected_dataframe[column],
            )

            if different_values > 0:

                errors.append(
                    f"Pseudonymized column '{column}' contains "
                    f"{different_values} incorrect HMAC value(s)."
                )

            continue

        # ----------------------------------------------------
        # GENERALIZE
        # ----------------------------------------------------

        if action == "generalize":

            method = protection.get("method")

            output_column = protection.get(
                "output_column"
            )

            if column in protected_dataframe.columns:

                errors.append(
                    f"Original generalized column '{column}' "
                    "still exists in the Protected dataset."
                )

            if not output_column:

                errors.append(
                    f"Generalized column '{column}' has no "
                    "configured output column."
                )

                continue

            if output_column not in protected_dataframe.columns:

                errors.append(
                    f"Generalized output column "
                    f"'{output_column}' is missing."
                )

                continue

            generalization_function = (
                GENERALIZATION_METHODS.get(method)
            )

            if generalization_function is None:

                errors.append(
                    f"Unsupported generalization method "
                    f"'{method}' for column '{column}'."
                )

                continue

            expected_values = raw_dataframe[column].apply(
                generalization_function
            )

            different_values = count_different_values(
                expected=expected_values,
                actual=protected_dataframe[output_column],
            )

            if different_values > 0:

                errors.append(
                    f"Generalized column '{output_column}' "
                    f"contains {different_values} incorrect "
                    "value(s)."
                )

            continue

        # ----------------------------------------------------
        # UNKNOWN ACTION
        # ----------------------------------------------------

        errors.append(
            f"Unsupported protection action "
            f"'{action}' for column '{column}'."
        )

    return errors