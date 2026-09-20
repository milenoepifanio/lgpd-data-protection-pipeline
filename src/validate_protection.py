
"""
Protected Layer Validation
==========================

Validates the LGPD protection process by combining:

- Raw vs Protected transformation validation;
- Great Expectations data quality validation.
"""

import great_expectations as gx

import os

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

load_dotenv()

secret_key = os.getenv("PSEUDONYMIZATION_KEY")

if not secret_key:
    raise ValueError(
        "HMAC secret key is missing."
    )
# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """
    Executes the Protected layer validation.
    """

    print("=" * 60)
    print("LGPD PROTECTION VALIDATION")
    print("=" * 60)

    # ========================================================
    # LOAD RESOURCES
    # ========================================================

    raw_dataframe = load_dataset(
        dataset_path=RAW_CUSTOMERS_PATH,
    )

    protected_dataframe = load_dataset(
        dataset_path=PROTECTED_CUSTOMERS_PATH,
    )

    config = load_classification_config(
        config_path=CLASSIFICATION_CONFIG_PATH,
    )

    print()
    print(
        f"Raw: "
        f"{len(raw_dataframe):,} rows / "
        f"{len(raw_dataframe.columns)} columns"
    )

    print(
        f"Protected: "
        f"{len(protected_dataframe):,} rows / "
        f"{len(protected_dataframe.columns)} columns"
    )

    # ========================================================
    # RAW VS PROTECTED VALIDATION
    # ========================================================

    print()
    print("Protection transformation validation")
    print("-" * 60)

    errors = validate_protection_transformation(
    raw_dataframe=raw_dataframe,
    protected_dataframe=protected_dataframe,
    config=config,
    secret_key=secret_key,
)

    if errors:

        for error in errors:
            print(f"[FAILED] {error}")

        print()
        print("PROTECTION TRANSFORMATION VALIDATION FAILED")

        raise SystemExit(1)

    print(
        "[PASSED] Protection transformations "
        "match the configured policy."
    )

    # ========================================================
    # EXPECTED PROTECTED SCHEMA
    # ========================================================

    expected_columns = build_protected_schema(
        config=config,
    )

    # ========================================================
    # GREAT EXPECTATIONS SETUP
    # ========================================================

    print()
    print("Great Expectations validation")
    print("-" * 60)

    context = gx.get_context(
        mode="ephemeral",
    )

    data_source = context.data_sources.add_pandas(
        name="protected_pandas_source",
    )

    data_asset = data_source.add_dataframe_asset(
        name="protected_customers",
    )

    batch_definition = (
        data_asset.add_batch_definition_whole_dataframe(
            "protected_customers_batch"
        )
    )

    # ========================================================
    # EXPECTATION SUITE
    # ========================================================

    suite = build_protected_expectation_suite(
        expected_columns=expected_columns,
    )

    # ========================================================
    # BATCH VALIDATION
    # ========================================================

    batch = batch_definition.get_batch(
        batch_parameters={
            "dataframe": protected_dataframe,
        },
    )

    validation_result = batch.validate(
        suite,
    )

    # ========================================================
    # VALIDATION RESULTS
    # ========================================================

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

        print(
            "GREAT EXPECTATIONS VALIDATION FAILED"
        )

        raise SystemExit(1)

    print(
        "GREAT EXPECTATIONS VALIDATION SUCCESSFUL"
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 60)
    print("PROTECTION VALIDATION SUCCESSFUL")
    print("=" * 60)


if __name__ == "__main__":
    main()