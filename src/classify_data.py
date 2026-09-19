"""
Data Classification Validator
=============================

Validates the Raw customer dataset against the LGPD data
classification policy.

The validation ensures that:

- every Raw column has a classification;
- no unknown columns exist in the classification policy;
- classification values are valid;
- protection levels are valid;
- analytical necessity is defined;
- every column has a protection action;
- transformation rules contain the required configuration.
"""

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


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """
    Executes the data classification validation.
    """

    print("=" * 60)
    print("LGPD DATA CLASSIFICATION VALIDATION")
    print("=" * 60)

    print()
    print(f"Dataset: {RAW_CUSTOMERS_PATH}")
    print(
        f"Classification policy: "
        f"{CLASSIFICATION_CONFIG_PATH}"
    )

    # --------------------------------------------------------
    # Load resources
    # --------------------------------------------------------

    dataframe = load_dataset(
        dataset_path=RAW_CUSTOMERS_PATH,
    )

    config = load_classification_config(
        config_path=CLASSIFICATION_CONFIG_PATH,
    )

    print()
    print(
        f"Dataset loaded: "
        f"{len(dataframe):,} rows / "
        f"{len(dataframe.columns)} columns"
    )

    # --------------------------------------------------------
    # Validate classification
    # --------------------------------------------------------

    errors = validate_classification(
        dataframe=dataframe,
        config=config,
    )

    if errors:

        print()
        print("VALIDATION FAILED")
        print("-" * 60)

        for error in errors:
            print(f"[ERROR] {error}")

        raise SystemExit(1)

    # --------------------------------------------------------
    # Build classification summary
    # --------------------------------------------------------

    summary = build_classification_summary(
        config=config,
    )

    print()
    print("VALIDATION SUCCESSFUL")
    print("-" * 60)

    print(
        "All dataset columns have valid "
        "classification and protection rules."
    )

    print()
    print("Classification summary:")
    print()

    print(
        summary.to_string(
            index=False,
        )
    )

    # --------------------------------------------------------
    # Classification statistics
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Protection statistics
    # --------------------------------------------------------

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

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()