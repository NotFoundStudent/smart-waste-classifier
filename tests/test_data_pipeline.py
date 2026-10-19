
import pandas as pd
import pytest

from ml.data_pipeline import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    load_dataset,
    split_features_and_labels,
)


def test_load_dataset_returns_expected_columns_and_rows():
    df = load_dataset()

    assert len(df) == 32
    assert list(df.columns) == FEATURE_COLUMNS + [TARGET_COLUMN]


def test_split_features_and_labels():
    df = load_dataset()

    X, y = split_features_and_labels(df)

    assert list(X.columns) == FEATURE_COLUMNS
    assert y.name == TARGET_COLUMN
    assert len(X) == len(y) == 32


def test_missing_dataset_file_raises_error(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_dataset(missing_file)


def test_missing_required_column_is_rejected(tmp_path):
    csv_path = tmp_path / "missing_column.csv"
    pd.DataFrame(
        {
            "weight_g": [10],
            "moisture_pct": [20],
            "category": ["plastic"],
        }
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="missing columns"):
        load_dataset(csv_path)


def test_missing_values_are_rejected(tmp_path):
    csv_path = tmp_path / "missing_values.csv"
    pd.DataFrame(
        {
            "weight_g": [10],
            "moisture_pct": [20],
            "magnetic": [0],
            "category": [None],
        }
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="missing values"):
        load_dataset(csv_path)


def test_unknown_category_is_rejected(tmp_path):
    csv_path = tmp_path / "unknown_category.csv"
    pd.DataFrame(
        {
            "weight_g": [10],
            "moisture_pct": [20],
            "magnetic": [0],
            "category": ["glass"],
        }
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="unknown category"):
        load_dataset(csv_path)
