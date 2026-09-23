
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
    TARGET_HEALTH_CONDITIONS,
)

from utils.analytics.validator import (
    validate_analytics_data,
    validate_input_schema,
)


# AGGREGATION

def aggregate_customers(
    dataframe: pd.DataFrame,
    dimensions: list[str],
) -> pd.DataFrame:
    """
    Aggregates commercial metrics by a selected dimension.
    """

    aggregated = (
        dataframe
        .groupby(
            dimensions,
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
        *dimensions,
        *METRIC_COLUMNS,
    ]

    return (
        aggregated[output_columns]
        .sort_values(
            by=dimensions,
        )
        .reset_index(
            drop=True,
        )
    )


# ANALYTICAL PRODUCTS

def filter_health_cohort(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Keeps only the configured health analytics cohort."""

    return dataframe.loc[
        dataframe["condicao_saude"].isin(
            TARGET_HEALTH_CONDITIONS
        )
    ].copy()

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

    validate_analytics_data(silver_dataframe)

    health_cohort = filter_health_cohort(
        silver_dataframe
    )

    if health_cohort.empty:
        raise ValueError(
            "No customers found in the target health cohort."
        )

    validate_analytics_data(health_cohort)

    products = {}

    for product_name, dimensions in (
        ANALYTICS_PRODUCTS.items()
    ):

        products[product_name] = aggregate_customers(
            dataframe=health_cohort,
            dimensions=dimensions,
        )

    return products