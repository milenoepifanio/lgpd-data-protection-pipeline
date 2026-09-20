"""
Data Protection Pipeline
========================

Applies the protection policy defined in the data
classification configuration to the Raw customer dataset.

The resulting dataset is written to the Protected layer.
"""

import os

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
# MAIN
# ============================================================

def main() -> None:
    """
    Executes the data protection pipeline.
    """

    print("=" * 60)
    print("LGPD DATA PROTECTION PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # Environment
    # --------------------------------------------------------

    load_dotenv()

    secret_key = os.getenv(
        "PSEUDONYMIZATION_KEY"
    )

    if not secret_key:
        raise ValueError(
            "PSEUDONYMIZATION_KEY is not configured."
        )

    # --------------------------------------------------------
    # Load resources
    # --------------------------------------------------------

    print()
    print(f"Raw dataset: {RAW_CUSTOMERS_PATH}")
    print(
        f"Protection policy: "
        f"{CLASSIFICATION_CONFIG_PATH}"
    )

    dataframe = load_dataset(
        dataset_path=RAW_CUSTOMERS_PATH,
    )

    config = load_classification_config(
        config_path=CLASSIFICATION_CONFIG_PATH,
    )

    print()
    print(
        f"Raw dataset loaded: "
        f"{len(dataframe):,} rows / "
        f"{len(dataframe.columns)} columns"
    )

    # --------------------------------------------------------
    # Validate policy
    # --------------------------------------------------------

    errors = validate_classification(
        dataframe=dataframe,
        config=config,
    )

    if errors:

        print()
        print("CLASSIFICATION VALIDATION FAILED")
        print("-" * 60)

        for error in errors:
            print(f"[ERROR] {error}")

        raise SystemExit(1)

    print()
    print("Classification policy validated successfully.")

    # --------------------------------------------------------
    # Apply protection
    # --------------------------------------------------------

    protected_dataframe = protect_dataset(
        dataframe=dataframe,
        config=config,
        secret_key=secret_key,
    )

    # --------------------------------------------------------
    # Save Protected dataset
    # --------------------------------------------------------

    save_dataset(
        dataframe=protected_dataframe,
        output_path=PROTECTED_CUSTOMERS_PATH,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("DATA PROTECTION COMPLETED")
    print("-" * 60)

    print(
        f"Raw columns: "
        f"{len(dataframe.columns)}"
    )

    print(
        f"Protected columns: "
        f"{len(protected_dataframe.columns)}"
    )

    print()
    print("Protected schema:")

    for column in protected_dataframe.columns:
        print(f"  - {column}")

    print()
    print(
        f"Protected dataset: "
        f"{PROTECTED_CUSTOMERS_PATH}"
    )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()