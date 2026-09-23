
"""
Silver Layer Processor
======================

Transforms protected customer data into the Silver layer.
"""

import pandas as pd

from utils.silver.definitions import (
    DATE_COLUMNS,
    SILVER_COLUMNS,
    SILVER_OUTPUT_COLUMNS,
)

from utils.silver.validator import (
    validate_business_rules,
    validate_input_schema,
)


# DATE STANDARDIZATION

def standardize_dates(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Converts date columns to datetime64[ns].

    Invalid non-null dates cause the pipeline to fail.
    """

    for column in DATE_COLUMNS:

        dataframe[column] = pd.to_datetime(
            dataframe[column],
            errors="raise",
        )

    return dataframe


# DERIVED ATTRIBUTES

def derive_analytics_attributes(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Creates customer-level commercial metrics.
    """

    dataframe["ticket_medio"] = 0.0

    has_purchases = (
        dataframe["quantidade_compras"] > 0
    )

    dataframe.loc[
        has_purchases,
        "ticket_medio",
    ] = (
        dataframe.loc[
            has_purchases,
            "valor_total_compras",
        ]
        /
        dataframe.loc[
            has_purchases,
            "quantidade_compras",
        ]
    )

    return dataframe


# SILVER TRANSFORMATION

def build_silver(
    protected_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Transforms the Protected dataset into Silver.
    """

    validate_input_schema(
        protected_dataframe
    )

    silver_dataframe = (
        protected_dataframe[
            SILVER_COLUMNS
        ].copy()
    )

    silver_dataframe = standardize_dates(
        silver_dataframe
    )

    validate_business_rules(
        silver_dataframe
    )

    silver_dataframe = derive_analytics_attributes(
        silver_dataframe
    )

    return silver_dataframe[
        SILVER_OUTPUT_COLUMNS
    ]