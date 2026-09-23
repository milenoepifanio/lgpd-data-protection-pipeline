
"""
Synthetic Customer Data Generator
=================================

Generates and persists a synthetic customer dataset for the
LGPD & Data Protection Pipeline project.

The generated data is entirely synthetic and intended
exclusively for educational purposes.

Output:
    data/raw/customers.parquet
"""

from pathlib import Path

import pandas as pd

from utils.config import RAW_CUSTOMERS_PATH
from utils.dataset import (
    generate_dataset,
    save_dataset,
)


OUTPUT_PATH = Path(RAW_CUSTOMERS_PATH)

PROCESS_NAME = "SYNTHETIC CUSTOMER DATA GENERATION"


class CustomerDataGenerator:
    """
    Orchestrates the generation and persistence of the synthetic Raw customer dataset.
    """

    def __init__(
        self,
        output_path: Path = OUTPUT_PATH,
    ) -> None:
        """
        Initializes the generator configuration.
        """

        self.output_path = Path(output_path)

    def generate(self) -> pd.DataFrame:
        """
        Generates the synthetic customer dataset.
        """

        return generate_dataset()

    def save(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Persists the generated dataset in the Raw layer.
        """

        save_dataset(
            dataframe=dataframe,
            output_path=self.output_path,
        )

    def run(self) -> None:
        """
        Executes the complete dataset generation workflow.
        """

        print(PROCESS_NAME)

        dataframe = self.generate()

        self.save(dataframe)

        print(
            f"[PASSED] Generated rows: "
            f"{len(dataframe):,}"
        )

        print(
            f"[PASSED] Generated columns: "
            f"{len(dataframe.columns)}"
        )

        print(
            f"[PASSED] Output: "
            f"{self.output_path}"
        )

        print(
            "DATASET GENERATION SUCCESSFULLY COMPLETED"
        )

def main() -> None:
    """
    Application entry point.
    """

    generator = CustomerDataGenerator()

    generator.run()


if __name__ == "__main__":
    main()