"""
Restricted identity tracking data.

Builds the mapping required to link original identifiers to their
pseudonymized values without exposing the mapping in the Protected layer.
"""

from typing import Any

import pandas as pd


def build_restricted_tracking(
    raw_dataframe: pd.DataFrame,
    protected_dataframe: pd.DataFrame,
    config: dict[str, Any],
) -> pd.DataFrame:
    """
    Builds a restricted customer registry with the original attributes
    and the pseudonymized identifiers used by downstream layers.

    The mapping is intentionally kept separate from Protected data and
    must be stored with stricter access controls.
    """

    if len(raw_dataframe) != len(protected_dataframe):
        raise ValueError(
            "Raw and Protected datasets must have the same row count."
        )

    tracking_dataframe = raw_dataframe.reset_index(drop=True).copy()

    pseudonymized_columns: list[str] = []

    for column, metadata in config["columns"].items():
        protection = metadata.get("protection", {})

        if protection.get("action") != "pseudonymize":
            continue

        if column not in raw_dataframe.columns:
            raise ValueError(
                f"Original pseudonymized column '{column}' is missing."
            )

        if column not in protected_dataframe.columns:
            raise ValueError(
                f"Protected pseudonymized column '{column}' is missing."
            )

        protected_column = f"{column}_protected"

        if protected_column in tracking_dataframe.columns:
            raise ValueError(
                f"Restricted tracking column '{protected_column}' already exists."
            )

        tracking_dataframe[protected_column] = (
            protected_dataframe[column].reset_index(drop=True)
        )
        pseudonymized_columns.append(protected_column)

    if not pseudonymized_columns:
        raise ValueError(
            "No pseudonymized columns were configured for tracking."
        )

    for protected_column in pseudonymized_columns:
        if tracking_dataframe[protected_column].duplicated().any():
            raise ValueError(
                f"Restricted identifier '{protected_column}' contains duplicates."
            )

    return tracking_dataframe
