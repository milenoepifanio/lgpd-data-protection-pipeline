
"""
Protected Layer Validation
==========================

Validates the LGPD protection process by combining:
    - Raw vs Protected transformation validation;
    - Great Expectations data quality validation.

The validation ensures that the Protected dataset follows
the configured classification and protection policy.

Security requirements:
    - The pseudonymization key must be configured;
    - The secret key must never be printed or persisted;
    - The validation must not modify the source datasets.
"""

import os

from pathlib import Path
from typing import Any

import great_expectations as gx
import pandas as pd

from dotenv import load_dotenv

from utils.classification.loader import (
    load_classification_config,
)
from utils.config import (
    CLASSIFICATION_CONFIG_PATH,
    PROTECTED_CUSTOMERS_PATH,
    RAW_CUSTOMERS_PATH,
)
from utils.dataset import (
    load_dataset,
)
from utils.protection.processor import (
    build_protected_schema,
)
from utils.validation.comparator import (
    validate_protection_transformation,
)
from utils.validation.expectations import (
    build_protected_expectation_suite,
)

# CONSTANTS

PROCESS_NAME = "LGPD PROTECTION VALIDATION"

RAW_PATH = Path(RAW_CUSTOMERS_PATH)

PROTECTED_PATH = Path(PROTECTED_CUSTOMERS_PATH)

CONFIG_PATH = Path(CLASSIFICATION_CONFIG_PATH)

SECRET_KEY_ENV = "PSEUDONYMIZATION_KEY"

GX_DATA_SOURCE_NAME = "protected_pandas_source"

GX_DATA_ASSET_NAME = "protected_customers"

GX_BATCH_NAME = "protected_customers_batch"

SEPARATOR = "=" * 60

SECTION_SEPARATOR = "-" * 60

# PROTECTED LAYER VALIDATOR

class ProtectedLayerValidator:
    """
    Orchestrates the validation of the Protected layer
    against the Raw dataset and the LGPD protection policy.
    """

    def __init__(
        self,
        raw_path: Path = RAW_PATH,
        protected_path: Path = PROTECTED_PATH,
        config_path: Path = CONFIG_PATH,
    ) -> None:
        """
        Initializes the validation paths.
        """

        self.raw_path = Path(raw_path)

        self.protected_path = Path(protected_path)

        self.config_path = Path(config_path)

    # ENVIRONMENT CONFIGURATION

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

    # RESOURCE LOADING

    def load_resources(
        self,
    ) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
        """
        Loads the Raw dataset, Protected dataset,
        and classification policy.
        """

        raw_dataframe = load_dataset(
            dataset_path=self.raw_path,
        )

        protected_dataframe = load_dataset(
            dataset_path=self.protected_path,
        )

        config = load_classification_config(
            config_path=self.config_path,
        )

        return (
            raw_dataframe,
            protected_dataframe,
            config,
        )

    # TRANSFORMATION VALIDATION

    def validate_transformations(
        self,
        raw_dataframe: pd.DataFrame,
        protected_dataframe: pd.DataFrame,
        config: dict[str, Any],
        secret_key: str,
    ) -> None:
        """
        Validates the Raw-to-Protected transformations.

        Raises:
            ValueError: If the transformations do not match
                the configured protection policy.
        """

        errors = validate_protection_transformation(
            raw_dataframe=raw_dataframe,
            protected_dataframe=protected_dataframe,
            config=config,
            secret_key=secret_key,
        )

        if errors:

            error_details = "\n".join(
                f"[FAILED] {error}"
                for error in errors
            )

            raise ValueError(
                "Protection transformation validation failed:\n"
                f"{error_details}"
            )

    # EXPECTED SCHEMA

    def build_expected_schema(
        self,
        config: dict[str, Any],
    ) -> list[str]:
        """
        Builds the expected Protected schema
        from the classification policy.
        """

        return build_protected_schema(
            config=config,
        )

    # GREAT EXPECTATIONS VALIDATION

    def validate_data_quality(
        self,
        protected_dataframe: pd.DataFrame,
        expected_columns: list[str],
    ) -> Any:
        """
        Validates the Protected dataset using
        an ephemeral Great Expectations context.

        Returns:
            Great Expectations validation result.
        """

        # ----------------------------------------------------
        # Create ephemeral context
        # ----------------------------------------------------

        context = gx.get_context(
            mode="ephemeral",
        )

        # ----------------------------------------------------
        # Configure Pandas data source
        # ----------------------------------------------------

        data_source = context.data_sources.add_pandas(
            name=GX_DATA_SOURCE_NAME,
        )

        data_asset = data_source.add_dataframe_asset(
            name=GX_DATA_ASSET_NAME,
        )

        batch_definition = (
            data_asset.add_batch_definition_whole_dataframe(
                GX_BATCH_NAME
            )
        )

        # ----------------------------------------------------
        # Build expectation suite
        # ----------------------------------------------------

        suite = build_protected_expectation_suite(
            expected_columns=expected_columns,
        )

        # ----------------------------------------------------
        # Retrieve batch
        # ----------------------------------------------------

        batch = batch_definition.get_batch(
            batch_parameters={
                "dataframe": protected_dataframe,
            },
        )

        # ----------------------------------------------------
        # Execute validation
        # ----------------------------------------------------

        return batch.validate(
            suite,
        )

    # VALIDATION RESULTS

    def print_quality_results(
        self,
        validation_result: Any,
    ) -> None:
        """
        Displays the result of each Great Expectations
        expectation and raises an error if validation fails.
        """

        for result in validation_result.results:

            expectation_name = (
                result.expectation_config.type
            )

            status = (
                "PASSED"
                if result.success
                else "FAILED"
            )

            print(
                f"[{status}] {expectation_name}"
            )

        print()

        if not validation_result.success:

            raise ValueError(
                "GREAT EXPECTATIONS VALIDATION FAILED"
            )

        print(
            "GREAT EXPECTATIONS VALIDATION SUCCESSFUL"
        )

    # PIPELINE EXECUTION

    def run(self) -> None:
        """
        Executes the complete Protected layer validation.
        """

        print(SEPARATOR)
        print(PROCESS_NAME)
        print(SEPARATOR)

        secret_key = self.load_secret_key()

        print()
        print("[PASSED] Pseudonymization key configured.")

        (
            raw_dataframe,
            protected_dataframe,
            config,
        ) = self.load_resources()

        print()
        print(
            f"[PASSED] Raw: "
            f"{len(raw_dataframe):,} rows / "
            f"{len(raw_dataframe.columns)} columns"
        )

        print(
            f"[PASSED] Protected: "
            f"{len(protected_dataframe):,} rows / "
            f"{len(protected_dataframe.columns)} columns"
        )

        print()
        print("Protection transformation validation")
        print(SECTION_SEPARATOR)

        try:
            self.validate_transformations(
                raw_dataframe=raw_dataframe,
                protected_dataframe=protected_dataframe,
                config=config,
                secret_key=secret_key,
            )

        except ValueError as error:

            print()
            print(error)

            raise SystemExit(1) from error

        print(
            "[PASSED] Protection transformations "
            "match the configured policy."
        )

        expected_columns = self.build_expected_schema(
            config=config,
        )

        print()
        print("Great Expectations validation")
        print(SECTION_SEPARATOR)

        validation_result = self.validate_data_quality(
            protected_dataframe=protected_dataframe,
            expected_columns=expected_columns,
        )

        try:
            self.print_quality_results(
                validation_result=validation_result,
            )

        except ValueError as error:

            print(error)

            raise SystemExit(1) from error


        print()
        print(SEPARATOR)

        print(
            "PROTECTION VALIDATION SUCCESSFUL"
        )

        print(SEPARATOR)


# MAIN

def main() -> None:
    """
    Application entry point.
    """

    validator = ProtectedLayerValidator()

    validator.run()


if __name__ == "__main__":
    main()