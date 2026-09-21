
"""
Build Silver Layer
==================

Reads the Protected dataset, applies Silver transformations,
and saves the result as Parquet.

Input:
    data/protected/customers.parquet

Output:
    data/silver/customers.parquet
"""

from pathlib import Path

import pandas as pd

from utils.silver.processor import build_silver


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "protected"
    / "customers.parquet"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "customers.parquet"
)


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print(
        "BUILDING SILVER LAYER"
    )

    protected_dataframe = pd.read_parquet(
        INPUT_PATH
    )

    silver_dataframe = build_silver(
        protected_dataframe
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    silver_dataframe.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"[PASSED] Input rows: "
        f"{len(protected_dataframe)}"
    )

    print(
        f"[PASSED] Silver rows: "
        f"{len(silver_dataframe)}"
    )

    print(
        f"[PASSED] Silver columns: "
        f"{len(silver_dataframe.columns)}"
    )

    print(
        f"[PASSED] Output: {OUTPUT_PATH}"
    )

    print(
        "SILVER LAYER SUCCESSFULLY BUILT"
    )


if __name__ == "__main__":
    main()