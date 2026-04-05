"""
Data loading and validation utilities for the Credit EDA project.
"""

import logging
import os

import pandas as pd

from src.config import (
    APPLICATION_DATA_FILE,
    DATA_RAW_PATH,
    DEFAULT_MISSING_THRESHOLD,
    PREVIOUS_APPLICATION_FILE,
    TARGET_COLUMN,
)

logger = logging.getLogger(__name__)


def load_application_data(filepath: str = None) -> pd.DataFrame:
    """Load and return the main application dataset.

    Parameters
    ----------
    filepath:
        Path to the CSV file.  Defaults to the configured raw data path.

    Returns
    -------
    pd.DataFrame
        The loaded application data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at *filepath*.
    ValueError
        If the loaded DataFrame is empty.
    """
    if filepath is None:
        filepath = os.path.join(DATA_RAW_PATH, APPLICATION_DATA_FILE)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Application data file not found: {filepath}")

    df = pd.read_csv(filepath)

    if df.empty:
        raise ValueError(f"Loaded DataFrame is empty: {filepath}")

    logger.info("Loaded application data: %d rows, %d columns", *df.shape)
    return df


def load_previous_application(filepath: str = None) -> pd.DataFrame:
    """Load and return the previous application dataset.

    Parameters
    ----------
    filepath:
        Path to the CSV file.  Defaults to the configured raw data path.

    Returns
    -------
    pd.DataFrame
        The loaded previous-application data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at *filepath*.
    ValueError
        If the loaded DataFrame is empty.
    """
    if filepath is None:
        filepath = os.path.join(DATA_RAW_PATH, PREVIOUS_APPLICATION_FILE)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Previous application file not found: {filepath}")

    df = pd.read_csv(filepath)

    if df.empty:
        raise ValueError(f"Loaded DataFrame is empty: {filepath}")

    logger.info("Loaded previous application data: %d rows, %d columns", *df.shape)
    return df


def validate_data_quality(df: pd.DataFrame) -> dict:
    """Run basic data-quality checks and return a summary report.

    Checks performed
    ----------------
    * Shape (rows, columns)
    * Missing-value counts and percentages per column
    * Columns exceeding the configured missing threshold
    * Duplicate row count
    * Data types per column
    * Presence of the target column

    Parameters
    ----------
    df:
        DataFrame to validate.

    Returns
    -------
    dict
        Quality-report dictionary with keys:
        ``shape``, ``missing_counts``, ``missing_percentages``,
        ``high_missing_columns``, ``duplicate_rows``, ``dtypes``,
        ``has_target``.
    """
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100

    high_missing = missing_pct[missing_pct > DEFAULT_MISSING_THRESHOLD * 100].index.tolist()

    report = {
        "shape": df.shape,
        "missing_counts": missing_counts.to_dict(),
        "missing_percentages": missing_pct.to_dict(),
        "high_missing_columns": high_missing,
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "has_target": TARGET_COLUMN in df.columns,
    }

    logger.info(
        "Data quality check: %d high-missing columns, %d duplicates",
        len(high_missing),
        report["duplicate_rows"],
    )
    return report


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a sorted DataFrame of missing-value statistics.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        Columns: ``missing_count``, ``missing_percentage``.
        Sorted descending by ``missing_percentage``, filtered to rows > 0.
    """
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df)) * 100

    summary = pd.DataFrame(
        {"missing_count": missing_count, "missing_percentage": missing_pct}
    )
    summary = summary[summary["missing_count"] > 0].sort_values(
        "missing_percentage", ascending=False
    )
    return summary


def drop_high_missing_columns(df: pd.DataFrame, threshold: float = None) -> pd.DataFrame:
    """Drop columns whose missing-value percentage exceeds *threshold*.

    Parameters
    ----------
    df:
        Input DataFrame.
    threshold:
        Fraction (0–1).  Defaults to ``DEFAULT_MISSING_THRESHOLD``.

    Returns
    -------
    pd.DataFrame
        DataFrame with high-missing columns removed.
    """
    if threshold is None:
        threshold = DEFAULT_MISSING_THRESHOLD

    missing_pct = df.isnull().mean()
    cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()

    if cols_to_drop:
        logger.info("Dropping %d high-missing columns: %s", len(cols_to_drop), cols_to_drop)

    return df.drop(columns=cols_to_drop)
