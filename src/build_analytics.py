
"""
Build Analytics Layer
=====================

Reads the Silver dataset and generates aggregated
commercial analytics.

Input:
    data/silver/customers.parquet

Outputs:
    data/analytics/customers_by_state.parquet
    data/analytics/customers_by_age.parquet
    data/analytics/customers_by_income.parquet
    data/analytics/customers_by_channel.parquet
"""

from pathlib import Path

import pandas as pd

from utils.analytics.definitions import MIN_GROUP_SIZE
from utils.analytics.processor import build_analytics


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "customers.parquet"
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "analytics"
)


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print(
        "BUILDING ANALYTICS LAYER"
    )

    silver_dataframe = pd.read_parquet(
        INPUT_PATH
    )

    analytics_products = build_analytics(
        silver_dataframe
    )

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"[PASSED] Input rows: "
        f"{len(silver_dataframe)}"
    )

    print(
        f"[INFO] Minimum group size: "
        f"{MIN_GROUP_SIZE}"
    )

    for product_name, dataframe in (
        analytics_products.items()
    ):

        output_path = (
            OUTPUT_DIRECTORY
            / f"{product_name}.parquet"
        )

        dataframe.to_parquet(
            output_path,
            index=False,
        )

        print(
            f"[PASSED] {product_name}: "
            f"{len(dataframe)} groups"
        )

        print(
            f"         Output: {output_path}"
        )

    print(
        "ANALYTICS LAYER SUCCESSFULLY BUILT"
    )


if __name__ == "__main__":
    main()