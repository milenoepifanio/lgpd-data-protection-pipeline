"""
Classification Resource Loaders
===============================

Provides functions to load datasets and data classification
configuration files.
"""

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


# CLASSIFICATION CONFIG

def load_classification_config(
    config_path: Path,
) -> dict[str, Any]:
    """
    Loads the data classification configuration from YAML.
    """

    if not config_path.exists():
        raise FileNotFoundError(
            f"Classification config not found: {config_path}"
        )

    with config_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            "Classification configuration must be a YAML object."
        )

    if "columns" not in config:
        raise ValueError(
            "Classification configuration must contain "
            "a 'columns' section."
        )

    if not isinstance(config["columns"], dict):
        raise ValueError(
            "'columns' must be a YAML object."
        )

    return config


# DATASET

def load_dataset(
    dataset_path: Path,
) -> pd.DataFrame:
    """
    Loads a Parquet dataset.
    """

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {dataset_path}"
        )

    return pd.read_parquet(
        dataset_path
    )