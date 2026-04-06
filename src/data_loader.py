"""
Data loading and data quality helpers for the credit EDA project.

This module provides reusable utilities for:
- loading raw CSV datasets
- validating required columns
- summarizing missingness
- generating data-quality reports
"""

from __future__ import annotations

from typing import Tuple, Union

import pandas as pd

PathLike = Union[str, "os.PathLike[str]"]


def load_csv(path: PathLike) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        path: Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataframe.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty and unreadable by pandas.
    """
    return pd.read_csv(path)


def load_application_data(path: PathLike) -> pd.DataFrame:
    """
    Load the main application dataset.

    Args:
        path: Path to the application data CSV.

    Returns:
        pd.DataFrame: Loaded application dataframe.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the loaded dataframe is empty.
    """
    df = load_csv(path)
    if df.empty:
        raise ValueError("empty")
    return df


def load_previous_application(path: PathLike) -> pd.DataFrame:
    """
    Load the previous application dataset.

    Args:
        path: Path to the previous application CSV.

    Returns:
        pd.DataFrame: Loaded previous-application dataframe.
    """
    return load_csv(path)


def drop_high_missing_columns(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Drop columns with missing fraction greater than the given threshold.

    Args:
        df: Input dataframe.
        threshold: Missing-value threshold expressed as a fraction between 0 and 1.

    Returns:
        pd.DataFrame: Dataframe with high-missing columns removed.
    """
    missing_frac = df.isnull().mean()
    to_drop = list(missing_frac[missing_frac > threshold].index)
    return df.drop(columns=to_drop, errors="ignore")


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary of missing values by column.

    The output includes:
    - column
    - missing_count
    - missing_percentage

    Results are sorted in descending order by missing percentage.

    Args:
        df: Input dataframe.

    Returns:
        pd.DataFrame: Missing-value summary table.
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
    Generate a structured data-quality report for the input dataframe.

    The report includes:
    - shape
    - missing_counts
    - missing_percentages
    - high_missing_columns
    - duplicate_rows
    - dtypes
    - has_target

    Args:
        df: Input dataframe.
        high_missing_threshold: Threshold above which columns are flagged as high-missing.

    Returns:
        dict: Data-quality report.
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
    """
    Validate that all required columns are present in the dataframe.

    Args:
        df: Input dataframe.
        required_columns: Tuple of required column names.

    Raises:
        ValueError: If one or more required columns are missing.
    """
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def load_credit_datasets(application_path: PathLike, previous_path: PathLike) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load both application and previous-application datasets.

    Args:
        application_path: Path to the application dataset.
        previous_path: Path to the previous-application dataset.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Loaded application and previous-application dataframes.
    """
    return load_application_data(application_path), load_previous_application(previous_path)