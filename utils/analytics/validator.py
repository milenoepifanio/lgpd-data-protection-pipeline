
"""
Analytics Layer Validation
==========================

Validates the Silver dataset before analytical aggregation.
"""

import numpy as np
import pandas as pd

from utils.analytics.definitions import (
    ANALYTICS_PRODUCTS,
    REQUIRED_COLUMNS,
)


# INPUT SCHEMA VALIDATION

def validate_input_schema(
    dataframe: pd.DataFrame,
) -> None:
    """
    Checks whether all required columns are available.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns in Silver: "
            f"{missing_columns}"
        )


# ANALYTICAL DATA VALIDATION

def validate_analytics_data(
    dataframe: pd.DataFrame,
) -> None:
    """
    Validates the attributes required by analytical products.
    """

    if dataframe["customer_id"].isna().any():
        raise ValueError(
            "customer_id contains null values."
        )

    if dataframe["customer_id"].duplicated().any():
        raise ValueError(
            "customer_id contains duplicate values."
        )

    dimensions = {
        dimension
        for product_dimensions in ANALYTICS_PRODUCTS.values()
        for dimension in product_dimensions
    }

    for dimension in dimensions:

        if dataframe[dimension].isna().any():
            raise ValueError(
                f"{dimension} contains null values."
            )

    numeric_columns = [
        "quantidade_compras",
        "valor_total_compras",
    ]

    for column in numeric_columns:

        if dataframe[column].isna().any():
            raise ValueError(
                f"{column} contains null values."
            )

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            raise ValueError(
                f"{column} must be numeric."
            )

        if not np.isfinite(
            dataframe[column].to_numpy(
                dtype="float64"
            )
        ).all():
            raise ValueError(
                f"{column} contains non-finite values."
            )

        if (dataframe[column] < 0).any():
            raise ValueError(
                f"{column} contains negative values."
            )