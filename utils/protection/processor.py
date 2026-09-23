
"""
Data Protection Processor
=========================

Applies data protection rules defined in the classification
policy to a dataset.

Supported actions:
- retain
- remove
- pseudonymize
- generalize
"""

from typing import Any

import pandas as pd

from utils.protection.generalization import (
    generalize_age,
    generalize_cep,
    generalize_income,
)
from utils.protection.pseudonymization import (
    hmac_sha256,
)

# GENERALIZATION METHODS

GENERALIZATION_METHODS = {
    "age_range": generalize_age,
    "cep_region": generalize_cep,
    "income_range": generalize_income,
}

# EXPECTED OUTPUT SCHEMA

def build_protected_schema(
    config: dict[str, Any],
) -> list[str]:
    """
    Builds the expected Protected schema from the
    configured protection policy.

    Rules:
    - retain: preserves the original column;
    - remove: excludes the original column;
    - pseudonymize: preserves the original column name;
    - generalize: replaces the original column with
      the configured output column.

    Preserves the order defined in the classification policy.
    """

    protected_columns: list[str] = []

    for column, metadata in config["columns"].items():

        protection = metadata.get(
            "protection",
            {},
        )

        action = protection.get("action")

        # REMOVE

        if action == "remove":
            continue


        # GENERALIZE


        if action == "generalize":

            protected_columns.append(
                protection["output_column"]
            )

            continue


        # RETAIN / PSEUDONYMIZE


        if action in {
            "retain",
            "pseudonymize",
        }:

            protected_columns.append(column)

            continue


        # UNKNOWN ACTION


        raise ValueError(
            f"Unsupported protection action "
            f"'{action}' for column '{column}'."
        )

    return protected_columns


# DATA PROTECTION

def protect_dataset(
    dataframe: pd.DataFrame,
    config: dict[str, Any],
    secret_key: str,
) -> pd.DataFrame:
    """
    Applies the configured protection rules to a dataset.

    Args:
        dataframe:
            Source dataset.

        config:
            Data classification and protection configuration.

        secret_key:
            Secret key used for pseudonymization.

    Returns:
        Protected DataFrame with the expected output schema.
    """

    protected_dataframe = dataframe.copy()

    for column, metadata in config["columns"].items():

        protection = metadata.get(
            "protection",
            {},
        )

        action = protection.get("action")

        # RETAIN

        if action == "retain":
            continue

        # REMOVE

        if action == "remove":

            protected_dataframe.drop(
                columns=[column],
                inplace=True,
            )

            continue

        # PSEUDONYMIZE

        if action == "pseudonymize":

            method = protection.get("method")

            if method != "hmac_sha256":

                raise ValueError(
                    f"Unsupported pseudonymization "
                    f"method: '{method}'."
                )

            protected_dataframe[column] = (
                protected_dataframe[column].apply(
                    lambda value: hmac_sha256(
                        value=value,
                        secret_key=secret_key,
                    )
                )
            )

            continue

        # GENERALIZE

        if action == "generalize":

            method = protection.get("method")

            output_column = protection.get(
                "output_column"
            )

            generalization_function = (
                GENERALIZATION_METHODS.get(method)
            )

            if generalization_function is None:

                raise ValueError(
                    f"Unsupported generalization "
                    f"method: '{method}'."
                )

            protected_dataframe[output_column] = (
                protected_dataframe[column].apply(
                    generalization_function
                )
            )

            protected_dataframe.drop(
                columns=[column],
                inplace=True,
            )

            continue


        # UNKNOWN ACTION


        raise ValueError(
            f"Unsupported protection action "
            f"'{action}' for column '{column}'."
        )

    # OUTPUT SCHEMA ORDER

    expected_columns = build_protected_schema(
        config=config,
    )

    protected_dataframe = protected_dataframe[
        expected_columns
    ]

    return protected_dataframe