from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

CONFIG_DIR = PROJECT_ROOT / "config"

RAW_DATA_DIR = DATA_DIR / "raw"

PROTECTED_DATA_DIR = DATA_DIR / "protected"

SILVER_DATA_DIR = DATA_DIR / "silver"

ANALYTICS_DATA_DIR = DATA_DIR / "analytics"

RESTRICTED_DATA_DIR = DATA_DIR / "restricted"

# ============================================================
# DATASET CONFIGURATION
# ============================================================

NUM_RECORDS = 10_000

SEED = 42

RAW_CUSTOMERS_PATH = (
    RAW_DATA_DIR / "customers.parquet"
)

# ============================================================
# DATA CLASSIFICATION
# ============================================================

CLASSIFICATION_CONFIG_PATH = (
    CONFIG_DIR / "data_classification.yaml"
)

PROTECTED_DATA_DIR = (
    DATA_DIR / "protected"
)

PROTECTED_CUSTOMERS_PATH = (
    PROTECTED_DATA_DIR / "customers.parquet"
)

RESTRICTED_CUSTOMER_IDENTITY_PATH = (
    RESTRICTED_DATA_DIR / "customer_identity_map.parquet"
)

