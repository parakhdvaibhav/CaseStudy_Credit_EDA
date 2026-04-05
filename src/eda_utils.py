"""
General EDA utility helpers for the Credit EDA project.
"""

import logging
from typing import List, Optional

import numpy as np
import pandas as pd

from src.config import DEFAULT_MISSING_THRESHOLD, TARGET_COLUMN

logger = logging.getLogger(__name__)


def describe_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return an extended descriptive statistics table.

    Adds ``missing_pct`` and ``dtype`` columns to the standard
    ``pd.DataFrame.describe()`` output.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        Descriptive statistics for numeric columns with extra metadata rows.
    """
    desc = df.describe(include=[np.number]).T
    desc["missing_pct"] = (df.isnull().sum() / len(df) * 100).round(2)
    desc["dtype"] = df.dtypes.astype(str)
    return desc


def identify_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return rows where *column* is an outlier by the IQR method.

    Parameters
    ----------
    df:
        Input DataFrame.
    column:
        Numeric column to check for outliers.

    Returns
    -------
    pd.DataFrame
        Subset of *df* containing outlier rows.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return df[(df[column] < lower) | (df[column] > upper)]


def get_value_counts_with_pct(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return value counts with percentage for a categorical column.

    Parameters
    ----------
    df:
        Input DataFrame.
    column:
        Categorical column.

    Returns
    -------
    pd.DataFrame
        Columns: ``count``, ``percentage``.
    """
    counts = df[column].value_counts()
    pct = (counts / len(df) * 100).round(2)
    return pd.DataFrame({"count": counts, "percentage": pct})


def flag_anomalous_employment(df: pd.DataFrame) -> pd.DataFrame:
    """Add a boolean column ``IS_PENSIONER`` for DAYS_EMPLOYED == 365243.

    The raw dataset encodes pensioners / unemployed applicants with
    ``DAYS_EMPLOYED = 365243``.  This helper flags them explicitly.

    Parameters
    ----------
    df:
        DataFrame that may contain ``DAYS_EMPLOYED``.

    Returns
    -------
    pd.DataFrame
        Copy with ``IS_PENSIONER`` column added (or original if column absent).
    """
    df = df.copy()
    if "DAYS_EMPLOYED" in df.columns:
        df["IS_PENSIONER"] = df["DAYS_EMPLOYED"] == 365243
    return df


def get_categorical_default_rates(
    df: pd.DataFrame, columns: Optional[List[str]] = None
) -> dict:
    """Compute per-category default rates for a list of categorical columns.

    Parameters
    ----------
    df:
        DataFrame containing ``TARGET`` and categorical columns.
    columns:
        Columns to analyse.  If ``None``, all object/category columns are used.

    Returns
    -------
    dict
        Mapping ``{column_name: pd.Series(default_rate by category)}``.
    """
    if TARGET_COLUMN not in df.columns:
        raise KeyError(f"Target column '{TARGET_COLUMN}' not found in DataFrame.")

    if columns is None:
        columns = df.select_dtypes(include=["object", "category"]).columns.tolist()

    result = {}
    for col in columns:
        if col in df.columns:
            result[col] = df.groupby(col)[TARGET_COLUMN].mean().sort_values(ascending=False)

    return result
