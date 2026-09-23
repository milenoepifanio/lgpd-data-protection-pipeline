
"""
Analytics Layer Processor
=========================

Builds aggregated commercial analytics from Silver data.
"""

import pandas as pd

from utils.analytics.definitions import (
    ANALYTICS_PRODUCTS,
    METRIC_COLUMNS,
    MIN_GROUP_SIZE,
)

from utils.analytics.validator import (
    validate_analytics_data,
    validate_input_schema,
)


# AGGREGATION

def aggregate_customers(
    dataframe: pd.DataFrame,
    dimension: str,
) -> pd.DataFrame:
    """
    Aggregates commercial metrics by a selected dimension.
    """

    aggregated = (
        dataframe
        .groupby(
            dimension,
            dropna=False,
            as_index=False,
        )
        .agg(
            quantidade_clientes=(
                "customer_id",
                "nunique",
            ),
            receita_total=(
                "valor_total_compras",
                "sum",
            ),
            quantidade_compras=(
                "quantidade_compras",
                "sum",
            ),
        )
    )

    # MINIMUM GROUP SIZE

    aggregated = aggregated.loc[
        aggregated["quantidade_clientes"]
        >= MIN_GROUP_SIZE
    ].copy()

    # WEIGHTED AVERAGE ORDER VALUE

    aggregated["ticket_medio"] = 0.0

    has_purchases = (
        aggregated["quantidade_compras"] > 0
    )

    aggregated.loc[
        has_purchases,
        "ticket_medio",
    ] = (
        aggregated.loc[
            has_purchases,
            "receita_total",
        ]
        /
        aggregated.loc[
            has_purchases,
            "quantidade_compras",
        ]
    )

    # OUTPUT SCHEMA

    output_columns = [
        dimension,
        *METRIC_COLUMNS,
    ]

    return (
        aggregated[output_columns]
        .sort_values(
            by=dimension,
        )
        .reset_index(
            drop=True,
        )
    )


# ANALYTICAL PRODUCTS

def build_analytics(
    silver_dataframe: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    Builds all analytical products from Silver.

    Returns:
        Dictionary containing one DataFrame per product.
    """

    validate_input_schema(
        silver_dataframe
    )

    validate_analytics_data(
        silver_dataframe
    )

    products = {}

    for product_name, dimension in (
        ANALYTICS_PRODUCTS.items()
    ):

        products[product_name] = aggregate_customers(
            dataframe=silver_dataframe,
            dimension=dimension,
        )

    return products