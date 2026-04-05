"""
Data loading and validation utilities for the Credit EDA case study.
"""

import os
import pandas as pd

from src.config import (
    DATA_RAW_PATH,
    DATA_PROCESSED_PATH,
    APPLICATION_DATA_FILE,
    PREVIOUS_APPLICATION_FILE,
    MISSING_VALUE_THRESHOLD,
    DAYS_COLUMNS,
)


def load_application_data(filepath: str | None = None) -> pd.DataFrame:
    """Load the main application dataset.

    Parameters
    ----------
    filepath:
        Absolute path to the CSV file.  Defaults to the configured raw-data
        location when *None*.

    Returns
    -------
    pd.DataFrame
        Raw application data.
    """
    if filepath is None:
        filepath = os.path.join(DATA_RAW_PATH, APPLICATION_DATA_FILE)
    df = pd.read_csv(filepath)
    print(f"[data_loader] Loaded application data: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def load_previous_application(filepath: str | None = None) -> pd.DataFrame:
    """Load the previous application dataset.

    Parameters
    ----------
    filepath:
        Absolute path to the CSV file.  Defaults to the configured raw-data
        location when *None*.

    Returns
    -------
    pd.DataFrame
        Raw previous application data.
    """
    if filepath is None:
        filepath = os.path.join(DATA_RAW_PATH, PREVIOUS_APPLICATION_FILE)
    df = pd.read_csv(filepath)
    print(f"[data_loader] Loaded previous application data: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def validate_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Print a data-quality summary for *df*.

    Reports:
    - Shape
    - Missing-value percentages per column (top 20 worst)
    - Duplicate row count
    - Data types

    Parameters
    ----------
    df:
        DataFrame to inspect.

    Returns
    -------
    pd.DataFrame
        The same DataFrame (unchanged) so the function can be used inline.
    """
    print(f"Shape          : {df.shape}")
    print(f"Duplicate rows : {df.duplicated().sum():,}")
    missing = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    missing = missing[missing > 0]
    if missing.empty:
        print("Missing values : None")
    else:
        print(f"\nTop missing columns (threshold={MISSING_VALUE_THRESHOLD*100:.0f}%):")
        print(missing.head(20).to_string())
    return df


def drop_high_missing_columns(
    df: pd.DataFrame,
    threshold: float = MISSING_VALUE_THRESHOLD,
) -> pd.DataFrame:
    """Remove columns whose missing-value ratio exceeds *threshold*.

    Parameters
    ----------
    df:
        Input DataFrame.
    threshold:
        Maximum allowed fraction of missing values (default from config).

    Returns
    -------
    pd.DataFrame
        DataFrame with high-missing columns removed.
    """
    missing_ratio = df.isnull().sum() / len(df)
    cols_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()
    if cols_to_drop:
        print(f"[data_loader] Dropping {len(cols_to_drop)} columns with >{threshold*100:.0f}% missing: {cols_to_drop}")
    return df.drop(columns=cols_to_drop)


def convert_days_to_years(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Convert negative-day columns to positive age values in years.

    The source data stores durations as negative days relative to the
    application date.  This helper makes those columns human-readable.

    Parameters
    ----------
    df:
        Input DataFrame.
    columns:
        List of column names to convert.  Defaults to ``DAYS_COLUMNS`` from
        config.

    Returns
    -------
    pd.DataFrame
        DataFrame with converted columns (mutated in place, also returned).
    """
    if columns is None:
        columns = [c for c in DAYS_COLUMNS if c in df.columns]
    for col in columns:
        new_col = col.replace("DAYS_", "YEARS_")
        df[new_col] = (df[col].abs() / 365).round(1)
    return df


def save_processed(df: pd.DataFrame, filename: str) -> None:
    """Persist a cleaned DataFrame to the processed data directory.

    Parameters
    ----------
    df:
        DataFrame to save.
    filename:
        Target filename (e.g. ``"application_cleaned.csv"``).
    """
    os.makedirs(DATA_PROCESSED_PATH, exist_ok=True)
    filepath = os.path.join(DATA_PROCESSED_PATH, filename)
    df.to_csv(filepath, index=False)
    print(f"[data_loader] Saved processed data → {filepath}")
