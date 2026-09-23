
"""
Data Protection Pipeline
========================

Applies the protection policy defined in the data
classification configuration to the Raw customer dataset.

The resulting dataset is written to the Protected layer.

Security requirements:
    - The pseudonymization key must be configured;
    - The classification policy must be valid;
    - The secret key must never be printed or persisted;
    - The Protected dataset is not considered anonymous.
"""

import os

from pathlib import Path
from typing import Any

import pandas as pd

from dotenv import load_dotenv

from utils.classification.loader import (
    load_classification_config,
)
from utils.classification.validator import (
    validate_classification,
)
from utils.config import (
    CLASSIFICATION_CONFIG_PATH,
    PROTECTED_CUSTOMERS_PATH,
    RAW_CUSTOMERS_PATH,
)
from utils.dataset import (
    load_dataset,
    save_dataset,
)
from utils.protection.processor import (
    protect_dataset,
)


# ============================================================
# CONSTANTS
# ============================================================

PROCESS_NAME = "LGPD DATA PROTECTION PIPELINE"
RAW_PATH = Path(RAW_CUSTOMERS_PATH)
CONFIG_PATH = Path(CLASSIFICATION_CONFIG_PATH)
PROTECTED_PATH = Path(PROTECTED_CUSTOMERS_PATH)
SECRET_KEY_ENV = "PSEUDONYMIZATION_KEY"
SEPARATOR = "=" * 60
SECTION_SEPARATOR = "-" * 60

class DataProtectionPipeline:
    """
    Orchestrates the protection of the Raw customer dataset
    according to the configured LGPD classification policy.
    """

    def __init__(
        self,
        raw_path: Path = RAW_PATH,
        config_path: Path = CONFIG_PATH,
        protected_path: Path = PROTECTED_PATH,
    ) -> None:
        """
        Initializes the pipeline paths.
        """

        self.raw_path = Path(raw_path)

        self.config_path = Path(config_path)

        self.protected_path = Path(protected_path)

    def load_secret_key(self) -> str:
        """
        Loads and validates the pseudonymization key.

        The key is never included in logs or error messages.
        """

        load_dotenv()

        secret_key = os.getenv(
            SECRET_KEY_ENV
        )

        if not secret_key:
            raise ValueError(
                f"{SECRET_KEY_ENV} is not configured."
            )

        return secret_key

    def load_resources(
        self,
    ) -> tuple[pd.DataFrame, dict[str, Any]]:
        """
        Loads the Raw dataset and the classification policy.
        """

        dataframe = load_dataset(
            dataset_path=self.raw_path,
        )

        config = load_classification_config(
            config_path=self.config_path,
        )

        return dataframe, config

    def validate_policy(
        self,
        dataframe: pd.DataFrame,
        config: dict[str, Any],
    ) -> None:
        """
        Validates the classification policy against the Raw dataset.

        Raises:
            ValueError: If any classification rule is invalid.
        """

        errors = validate_classification(
            dataframe=dataframe,
            config=config,
        )

        if errors:

            error_details = "\n".join(
                f"[ERROR] {error}"
                for error in errors
            )

            raise ValueError(
                "Classification validation failed:\n"
                f"{error_details}"
            )

    def apply_protection(
        self,
        dataframe: pd.DataFrame,
        config: dict[str, Any],
        secret_key: str,
    ) -> pd.DataFrame:
        """
        Applies the configured protection transformations.
        """

        return protect_dataset(
            dataframe=dataframe,
            config=config,
            secret_key=secret_key,
        )

    def save(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Persists the resulting dataset in the Protected layer.
        """

        save_dataset(
            dataframe=dataframe,
            output_path=self.protected_path,
        )

    def print_summary(
        self,
        raw_dataframe: pd.DataFrame,
        protected_dataframe: pd.DataFrame,
    ) -> None:
        """
        Displays the protection results without exposing
        customer records or the pseudonymization key.
        """

        print()
        print("DATA PROTECTION COMPLETED")
        print(SECTION_SEPARATOR)

        print(
            f"[PASSED] Raw rows: "
            f"{len(raw_dataframe):,}"
        )

        print(
            f"[PASSED] Protected rows: "
            f"{len(protected_dataframe):,}"
        )

        print(
            f"[PASSED] Raw columns: "
            f"{len(raw_dataframe.columns)}"
        )

        print(
            f"[PASSED] Protected columns: "
            f"{len(protected_dataframe.columns)}"
        )

        print()
        print("Protected schema:")

        for column in protected_dataframe.columns:
            print(f"  - {column}")

        print()
        print(
            f"[PASSED] Output: "
            f"{self.protected_path}"
        )

        print()
        print(SEPARATOR)

        print(
            "DATA PROTECTION PIPELINE SUCCESSFULLY COMPLETED"
        )

    def run(self) -> None:
        """
        Executes the complete Raw-to-Protected workflow.
        """

        print(SEPARATOR)
        print(PROCESS_NAME)
        print(SEPARATOR)

        secret_key = self.load_secret_key()

        print()
        print("[PASSED] Pseudonymization key configured.")

        print()
        print(f"Raw dataset: {self.raw_path}")
        print(f"Protection policy: {self.config_path}")

        dataframe, config = self.load_resources()

        print()
        print(
            f"[PASSED] Raw dataset loaded: "
            f"{len(dataframe):,} rows / "
            f"{len(dataframe.columns)} columns"
        )

        try:
            self.validate_policy(
                dataframe=dataframe,
                config=config,
            )

        except ValueError as error:

            print()
            print("CLASSIFICATION VALIDATION FAILED")
            print(SECTION_SEPARATOR)

            print(error)

            raise SystemExit(1) from error

        print()
        print("[PASSED] Classification policy validated.")

        protected_dataframe = self.apply_protection(
            dataframe=dataframe,
            config=config,
            secret_key=secret_key,
        )

        print("[PASSED] Protection transformations applied.")

        self.save(
            dataframe=protected_dataframe,
        )

        self.print_summary(
            raw_dataframe=dataframe,
            protected_dataframe=protected_dataframe,
        )


def main() -> None:
    """
    Application entry point.
    """

    pipeline = DataProtectionPipeline()

    pipeline.run()


if __name__ == "__main__":
    main()