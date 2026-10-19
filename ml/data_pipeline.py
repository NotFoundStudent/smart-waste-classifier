from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "waste.csv"

FEATURE_COLUMNS = ["weight_g", "moisture_pct", "magnetic"]
TARGET_COLUMN = "category"
VALID_CATEGORIES = {"plastic", "metal", "paper", "organic"}


def load_dataset(data_path=DEFAULT_DATA_PATH):
    """Load and validate the waste classification dataset."""
    data_path = Path(data_path)

    if not data_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    df = pd.read_csv(data_path)

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {sorted(missing_columns)}")

    df = df[required_columns].copy()

    if df.isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    if df.empty:
        raise ValueError("Dataset is empty.")

    if not set(df[TARGET_COLUMN]).issubset(VALID_CATEGORIES):
        raise ValueError("Dataset contains an unknown category.")

    return df


def split_features_and_labels(df):
    """Separate input features from target labels."""
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X, y
