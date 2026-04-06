"""
Data loading and data quality helpers for the credit EDA project.
"""

from __future__ import annotations

from typing import Tuple, Union

import pandas as pd

PathLike = Union[str, "os.PathLike[str]"]


def load_csv(path: PathLike) -> pd.DataFrame:
    # Let pandas raise FileNotFoundError naturally if missing.
    return pd.read_csv(path)


def load_application_data(path: PathLike) -> pd.DataFrame:
    """
    Load the main application_data CSV.

    Tests require:
      - FileNotFoundError for missing file
      - ValueError with 'empty' in message for header-only CSV
    """
    df = load_csv(path)
    if df.empty:
        raise ValueError("empty")
    return df


def load_previous_application(path: PathLike) -> pd.DataFrame:
    """
    Load previous_application CSV.
    """
    return load_csv(path)


def drop_high_missing_columns(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Drop columns with missing fraction > threshold (threshold in [0,1]).
    """
    missing_frac = df.isnull().mean()
    to_drop = list(missing_frac[missing_frac > threshold].index)
    return df.drop(columns=to_drop, errors="ignore")


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return missingness summary.

    Tests expect columns:
      - column
      - missing_count
      - missing_percentage
    Sorted descending by missing_percentage.
    """
    missing_count = df.isnull().sum()
    missing_percentage = df.isnull().mean() * 100.0

    out = (
        pd.DataFrame(
            {
                "column": missing_count.index,
                "missing_count": missing_count.values,
                "missing_percentage": missing_percentage.values,
            }
        )
        .sort_values("missing_percentage", ascending=False)
        .reset_index(drop=True)
    )
    return out


def validate_data_quality(df: pd.DataFrame, high_missing_threshold: float = 50.0) -> dict:
    """
    Return a data quality report dict.

    Tests expect keys:
      - shape
      - missing_counts
      - missing_percentages
      - high_missing_columns
      - duplicate_rows
      - dtypes
      - has_target
    """
    missing_counts = df.isnull().sum()
    missing_percentages = df.isnull().mean() * 100.0
    high_missing_columns = list(missing_percentages[missing_percentages > high_missing_threshold].index)

    report = {
        "shape": df.shape,
        "missing_counts": missing_counts,
        "missing_percentages": missing_percentages,
        "high_missing_columns": high_missing_columns,
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": df.dtypes,
        "has_target": ("TARGET" in df.columns),
    }
    return report


def validate_required_columns(df: pd.DataFrame, required_columns: Tuple[str, ...]) -> None:
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def load_credit_datasets(application_path: PathLike, previous_path: PathLike) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience loader used by your pipeline.
    """
    return load_application_data(application_path), load_previous_application(previous_path)