
"""
Data Classification Validator
=============================

Validates the Raw customer dataset against the LGPD data
classification policy.

The validation ensures that:
    - Every Raw column has a classification;
    - No unknown columns exist in the classification policy;
    - Classification values are valid;
    - Protection levels are valid;
    - Analytical necessity is defined;
    - Every column has a protection action;
    - Transformation rules contain the required configuration.
"""

from pathlib import Path

import pandas as pd

from utils.classification.loader import (
    load_classification_config,
)
from utils.classification.summary import (
    build_classification_summary,
)
from utils.classification.validator import (
    validate_classification,
)
from utils.config import (
    CLASSIFICATION_CONFIG_PATH,
    RAW_CUSTOMERS_PATH,
)
from utils.dataset import (
    load_dataset,
)


PROCESS_NAME = "LGPD DATA CLASSIFICATION VALIDATION"

DATASET_PATH = Path(RAW_CUSTOMERS_PATH)

CONFIG_PATH = Path(CLASSIFICATION_CONFIG_PATH)

SEPARATOR = "=" * 60

SECTION_SEPARATOR = "-" * 60


class DataClassificationValidator:
    """
    Orchestrates the validation of the Raw customer dataset
    against the LGPD classification policy.
    """

    def __init__(
        self,
        dataset_path: Path = DATASET_PATH,
        config_path: Path = CONFIG_PATH,
    ) -> None:
        """
        Initializes the classification validation configuration.
        """

        self.dataset_path = Path(dataset_path)

        self.config_path = Path(config_path)

    def load_resources(self) -> tuple[pd.DataFrame, dict]:
        """
        Loads the Raw dataset and its classification policy.
        """

        dataframe = load_dataset(
            dataset_path=self.dataset_path,
        )

        config = load_classification_config(
            config_path=self.config_path,
        )

        return dataframe, config

    def validate(
        self,
        dataframe: pd.DataFrame,
        config: dict,
    ) -> None:
        """
        Validates the dataset against the classification policy.

        Raises:
            ValueError: If classification validation fails.
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

    def build_summary(
        self,
        config: dict,
    ) -> pd.DataFrame:
        """
        Builds the classification and protection summary.
        """

        return build_classification_summary(
            config=config,
        )

    def print_summary(
        self,
        summary: pd.DataFrame,
    ) -> None:
        """
        Displays the classification summary and statistics.
        """

        print()
        print("Classification summary:")
        print()

        print(
            summary.to_string(
                index=False,
            )
        )

        classification_counts = (
            summary["classification"]
            .value_counts()
        )

        print()
        print("Classification counts:")
        print()

        print(
            classification_counts.to_string()
        )

        action_counts = (
            summary["action"]
            .value_counts()
        )

        print()
        print("Protection actions:")
        print()

        print(
            action_counts.to_string()
        )

    def run(self) -> None:
        """
        Executes the complete classification validation workflow.
        """

        print(SEPARATOR)
        print(PROCESS_NAME)
        print(SEPARATOR)

        print()
        print(f"Dataset: {self.dataset_path}")
        print(f"Classification policy: {self.config_path}")

        dataframe, config = self.load_resources()

        print()
        print(
            f"[PASSED] Dataset loaded: "
            f"{len(dataframe):,} rows / "
            f"{len(dataframe.columns)} columns"
        )

        try:
            self.validate(
                dataframe=dataframe,
                config=config,
            )

        except ValueError as error:

            print()
            print("VALIDATION FAILED")
            print(SECTION_SEPARATOR)

            print(error)

            raise SystemExit(1) from error

        summary = self.build_summary(
            config=config,
        )

        print()
        print("VALIDATION SUCCESSFUL")
        print(SECTION_SEPARATOR)

        print(
            "All dataset columns have valid "
            "classification and protection rules."
        )

        self.print_summary(
            summary=summary,
        )

        print()
        print(SEPARATOR)


def main() -> None:
    """
    Application entry point.
    """

    validator = DataClassificationValidator()

    validator.run()


if __name__ == "__main__":
    main()