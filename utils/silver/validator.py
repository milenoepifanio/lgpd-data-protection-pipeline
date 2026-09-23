
"""
Silver Layer Validation
=======================

Validates the input schema and business consistency rules.
"""

import pandas as pd

from utils.silver.definitions import SILVER_COLUMNS


# INPUT SCHEMA VALIDATION

def validate_input_schema(
    dataframe: pd.DataFrame,
) -> None:
    """
    Checks whether all required columns are available.
    """

    missing_columns = [
        column
        for column in SILVER_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns in Protected: "
            f"{missing_columns}"
        )


# BUSINESS RULES VALIDATION

def validate_business_rules(
    dataframe: pd.DataFrame,
) -> None:
    """
    Validates basic consistency rules for customer data.
    """

    if dataframe["customer_id"].isna().any():
        raise ValueError(
            "customer_id contains null values."
        )

    if dataframe["customer_id"].duplicated().any():
        raise ValueError(
            "customer_id contains duplicate values."
        )

    if dataframe["quantidade_compras"].isna().any():
        raise ValueError(
            "quantidade_compras contains null values."
        )

    if dataframe["valor_total_compras"].isna().any():
        raise ValueError(
            "valor_total_compras contains null values."
        )

    if (
        dataframe["quantidade_compras"] < 0
    ).any():
        raise ValueError(
            "quantidade_compras contains negative values."
        )

    if (
        dataframe["valor_total_compras"] < 0
    ).any():
        raise ValueError(
            "valor_total_compras contains negative values."
        )