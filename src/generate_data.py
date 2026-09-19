from utils.config import RAW_CUSTOMERS_PATH
from utils.dataset import (
    generate_dataset,
    save_dataset,
)

"""
Synthetic Customer Data Generator
=================================

Generates a fictitious customer dataset for the LGPD & Data Protection
Pipeline project.

The generated data is entirely synthetic and is intended exclusively
for educational purposes.

Output:
    data/raw/customers.csv
"""

def main() -> None:
    """
    Generates and persists the synthetic Raw customer dataset.
    """

    dataframe = generate_dataset()

    save_dataset(
        dataframe=dataframe,
        output_path=RAW_CUSTOMERS_PATH,
    )

    print()
    print("Dataset generation completed.")
    print(f"Rows: {len(dataframe):,}")
    print(f"Columns: {len(dataframe.columns)}")


if __name__ == "__main__":
    main()