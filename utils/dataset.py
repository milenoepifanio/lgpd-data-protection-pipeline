from pathlib import Path

import pandas as pd

from utils.config import NUM_RECORDS
from utils.generators import generate_customer


# DATASET GENERATION

def generate_dataset(
    num_records: int = NUM_RECORDS,
) -> pd.DataFrame:
    """
    Generates a synthetic customer dataset.

    Args:
        num_records:
            Number of customer records to generate.

    Returns:
        DataFrame containing the generated customer data.
    """

    print(
        f"Generating {num_records:,} synthetic customer records..."
    )

    customers = [
        generate_customer()
        for _ in range(num_records)
    ]

    return pd.DataFrame(customers)


# DATASET PERSISTENCE

def save_dataset(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Saves a dataset as a CSV file.

    Args:
        dataframe:
            Dataset to persist.

        output_path:
            Destination path for the CSV file.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_parquet(
    output_path,
    index=False,
    engine="pyarrow",
    compression="snappy",
)

    print(
        f"Dataset saved successfully: {output_path}"
    )
    
    
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