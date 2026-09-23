
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

from utils.analytics.definitions import (
    MIN_GROUP_SIZE,
)
from utils.analytics.processor import (
    build_analytics,
)

PROCESS_NAME = "BUILDING ANALYTICS LAYER"

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

SEPARATOR = "=" * 60

SECTION_SEPARATOR = "-" * 60


class AnalyticsLayerBuilder:
    """
    Orchestrates the construction of aggregated
    analytical products from the Silver dataset.
    """

    def __init__(
        self,
        input_path: Path = INPUT_PATH,
        output_directory: Path = OUTPUT_DIRECTORY,
    ) -> None:
        """
        Initializes the Analytics layer paths.
        """

        self.input_path = Path(input_path)

        self.output_directory = Path(output_directory)

    def load(self) -> pd.DataFrame:
        """
        Loads the Silver customer dataset.
        """

        return pd.read_parquet(
            self.input_path
        )

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, pd.DataFrame]:
        """
        Validates the Silver dataset and builds
        the configured analytical products.
        """

        return build_analytics(
            dataframe
        )

    def save(
        self,
        analytics_products: dict[str, pd.DataFrame],
    ) -> dict[str, Path]:
        """
        Persists all analytical products as Parquet files.

        Returns:
            Dictionary mapping each product name
            to its output path.
        """

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_paths: dict[str, Path] = {}

        for product_name, dataframe in analytics_products.items():

            output_path = (
                self.output_directory
                / f"{product_name}.parquet"
            )

            dataframe.to_parquet(
                output_path,
                index=False,
            )

            output_paths[product_name] = output_path

        return output_paths

    def print_summary(
        self,
        silver_dataframe: pd.DataFrame,
        analytics_products: dict[str, pd.DataFrame],
        output_paths: dict[str, Path],
    ) -> None:
        """
        Displays the Analytics layer execution results.
        """

        print()
        print("ANALYTICS LAYER BUILD COMPLETED")
        print(SECTION_SEPARATOR)

        print(
            f"[PASSED] Input rows: "
            f"{len(silver_dataframe):,}"
        )

        print(
            f"[INFO] Minimum group size: "
            f"{MIN_GROUP_SIZE}"
        )

        print()
        print("Analytical products:")

        for product_name, dataframe in analytics_products.items():

            print()
            print(
                f"[PASSED] {product_name}: "
                f"{len(dataframe)} groups"
            )

            print(
                f"         Output: "
                f"{output_paths[product_name]}"
            )

        print()
        print(SEPARATOR)

        print(
            "ANALYTICS LAYER SUCCESSFULLY BUILT"
        )

    def run(self) -> None:
        """
        Executes the complete Silver-to-Analytics workflow.
        """

        print(SEPARATOR)
        print(PROCESS_NAME)
        print(SEPARATOR)

        silver_dataframe = self.load()

        print()
        print(
            f"[PASSED] Silver dataset loaded: "
            f"{len(silver_dataframe):,} rows"
        )

        analytics_products = self.transform(
            dataframe=silver_dataframe,
        )

        print(
            "[PASSED] Analytical products built."
        )

        output_paths = self.save(
            analytics_products=analytics_products,
        )

        self.print_summary(
            silver_dataframe=silver_dataframe,
            analytics_products=analytics_products,
            output_paths=output_paths,
        )

def main() -> None:
    """
    Application entry point.
    """

    builder = AnalyticsLayerBuilder()

    builder.run()


if __name__ == "__main__":
    main()