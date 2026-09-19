"""
Data Classification Summary
===========================

Creates tabular summaries from the data classification policy.
"""

from typing import Any

import pandas as pd


def build_classification_summary(
    config: dict[str, Any],
) -> pd.DataFrame:
    """
    Creates a tabular summary of the classification policy.
    """

    records = []

    for column, metadata in config["columns"].items():

        purpose = metadata.get(
            "purpose",
            {},
        )

        protection = metadata.get(
            "protection",
            {},
        )

        records.append(
            {
                "column": column,
                "classification": metadata.get(
                    "classification"
                ),
                "identification": metadata.get(
                    "identification"
                ),
                "protection_level": metadata.get(
                    "protection_level"
                ),
                "required": purpose.get(
                    "required"
                ),
                "action": protection.get(
                    "action"
                ),
                "method": protection.get(
                    "method"
                ),
                "output_column": protection.get(
                    "output_column"
                ),
            }
        )

    return pd.DataFrame(records)