
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

from utils.silver.processor import (
    build_silver,
)

PROCESS_NAME = "BUILDING SILVER LAYER"

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

SEPARATOR = "=" * 60

SECTION_SEPARATOR = "-" * 60

class SilverLayerBuilder:
    """
    Orchestrates the construction of the Silver layer
    from the Protected customer dataset.
    """

    def __init__(
        self,
        input_path: Path = INPUT_PATH,
        output_path: Path = OUTPUT_PATH,
    ) -> None:
        """
        Initializes the Silver layer paths.
        """

        self.input_path = Path(input_path)

        self.output_path = Path(output_path)

    def load(self) -> pd.DataFrame:
        """
        Loads the Protected dataset.
        """

        return pd.read_parquet(
            self.input_path
        )

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Applies the Silver transformation and validation rules.
        """

        return build_silver(
            dataframe
        )

    def save(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Persists the Silver dataset as Parquet.
        """

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_parquet(
            self.output_path,
            index=False,
        )

    def print_summary(
        self,
        protected_dataframe: pd.DataFrame,
        silver_dataframe: pd.DataFrame,
    ) -> None:
        """
        Displays the Silver layer execution results.
        """

        print()
        print("SILVER LAYER BUILD COMPLETED")
        print(SECTION_SEPARATOR)

        print(
            f"[PASSED] Input rows: "
            f"{len(protected_dataframe):,}"
        )

        print(
            f"[PASSED] Silver rows: "
            f"{len(silver_dataframe):,}"
        )

        print(
            f"[PASSED] Silver columns: "
            f"{len(silver_dataframe.columns)}"
        )

        print(
            f"[PASSED] Output: "
            f"{self.output_path}"
        )

        print()
        print(SEPARATOR)

        print(
            "SILVER LAYER SUCCESSFULLY BUILT"
        )

    def run(self) -> None:
        """
        Executes the complete Protected-to-Silver workflow.
        """

        print(SEPARATOR)
        print(PROCESS_NAME)
        print(SEPARATOR)

        protected_dataframe = self.load()

        print()
        print(
            f"[PASSED] Protected dataset loaded: "
            f"{len(protected_dataframe):,} rows"
        )

        silver_dataframe = self.transform(
            dataframe=protected_dataframe,
        )

        print(
            "[PASSED] Silver transformations applied."
        )

        self.save(
            dataframe=silver_dataframe,
        )

        self.print_summary(
            protected_dataframe=protected_dataframe,
            silver_dataframe=silver_dataframe,
        )


def main() -> None:
    """
    Application entry point.
    """

    builder = SilverLayerBuilder()

    builder.run()


if __name__ == "__main__":
    main()