"""
Statistical analysis utilities for the Credit EDA project.
"""

import logging
from typing import List, Optional

import numpy as np
import pandas as pd

from src.config import CORRELATION_THRESHOLD, DEFAULT_MISSING_THRESHOLD, TARGET_COLUMN

logger = logging.getLogger(__name__)


def calculate_missing_percentages(df: pd.DataFrame) -> pd.Series:
    """Return missing-value percentage for every column, sorted descending.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.Series
        Index = column name, values = missing percentage (0–100).
    """
    missing_pct = (df.isnull().sum() / len(df)) * 100
    return missing_pct.sort_values(ascending=False)


def calculate_default_statistics(df: pd.DataFrame) -> dict:
    """Compute summary statistics related to the default target.

    Parameters
    ----------
    df:
        DataFrame that must contain the ``TARGET`` column.

    Returns
    -------
    dict
        Keys: ``total``, ``defaults``, ``non_defaults``, ``default_rate``,
        ``non_default_rate``.

    Raises
    ------
    KeyError
        If ``TARGET`` is not present in *df*.
    """
    if TARGET_COLUMN not in df.columns:
        raise KeyError(f"Target column '{TARGET_COLUMN}' not found in DataFrame.")

    total = len(df)
    defaults = int(df[TARGET_COLUMN].sum())
    non_defaults = total - defaults

    return {
        "total": total,
        "defaults": defaults,
        "non_defaults": non_defaults,
        "default_rate": defaults / total if total > 0 else 0.0,
        "non_default_rate": non_defaults / total if total > 0 else 0.0,
    }


def calculate_correlation_matrix(
    df: pd.DataFrame, columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Return the Pearson correlation matrix for numeric columns.

    Parameters
    ----------
    df:
        Input DataFrame.
    columns:
        Subset of columns to include.  If ``None``, all numeric columns are used.

    Returns
    -------
    pd.DataFrame
        Correlation matrix.
    """
    if columns is not None:
        df = df[columns]

    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.corr()


def get_highly_correlated_pairs(
    df: pd.DataFrame, threshold: float = None
) -> pd.DataFrame:
    """Identify feature pairs with correlation above *threshold*.

    Parameters
    ----------
    df:
        Input DataFrame.
    threshold:
        Absolute correlation threshold.  Defaults to ``CORRELATION_THRESHOLD``.

    Returns
    -------
    pd.DataFrame
        Columns: ``feature_1``, ``feature_2``, ``correlation``.
        Sorted descending by ``|correlation|``.
    """
    if threshold is None:
        threshold = CORRELATION_THRESHOLD

    corr_matrix = calculate_correlation_matrix(df)

    pairs = []
    cols = corr_matrix.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            if abs(val) >= threshold:
                pairs.append({"feature_1": cols[i], "feature_2": cols[j], "correlation": val})

    result = pd.DataFrame(pairs)
    if not result.empty:
        result = result.sort_values("correlation", key=abs, ascending=False)
    return result


def calculate_missing_by_target(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Calculate missing percentage of *column* grouped by the target variable.

    Parameters
    ----------
    df:
        DataFrame containing both ``TARGET`` and *column*.
    column:
        Column whose missing rate is analysed per target class.

    Returns
    -------
    pd.DataFrame
        Columns: ``TARGET``, ``missing_count``, ``total``, ``missing_pct``.
    """
    result = (
        df.groupby(TARGET_COLUMN)[column]
        .apply(lambda s: pd.Series({"missing_count": s.isnull().sum(), "total": len(s)}))
        .reset_index()
    )
    result.columns = [TARGET_COLUMN, "stat", "value"]
    result = result.pivot(index=TARGET_COLUMN, columns="stat", values="value").reset_index()
    result["missing_pct"] = (result["missing_count"] / result["total"]) * 100
    return result


def calculate_default_rate_by_category(
    df: pd.DataFrame, category_column: str
) -> pd.DataFrame:
    """Calculate default rate for each category in *category_column*.

    Parameters
    ----------
    df:
        DataFrame containing ``TARGET`` and *category_column*.
    category_column:
        Categorical column to group by.

    Returns
    -------
    pd.DataFrame
        Columns: the category column, ``total``, ``defaults``, ``default_rate``.
        Sorted descending by ``default_rate``.
    """
    if TARGET_COLUMN not in df.columns:
        raise KeyError(f"Target column '{TARGET_COLUMN}' not found in DataFrame.")

    grouped = (
        df.groupby(category_column)[TARGET_COLUMN]
        .agg(total="count", defaults="sum")
        .reset_index()
    )
    grouped["default_rate"] = grouped["defaults"] / grouped["total"]
    return grouped.sort_values("default_rate", ascending=False)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features useful for credit-risk analysis.

    New columns added (when source columns are present):
    * ``AGE_YEARS`` – applicant age in years (from ``DAYS_BIRTH``)
    * ``EMPLOYMENT_YEARS`` – employment duration in years (from ``DAYS_EMPLOYED``)
    * ``CREDIT_TO_INCOME`` – credit amount divided by annual income
    * ``ANNUITY_TO_INCOME`` – annuity divided by annual income

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with additional feature columns.
    """
    df = df.copy()

    if "DAYS_BIRTH" in df.columns:
        df["AGE_YEARS"] = (-df["DAYS_BIRTH"] / 365).round(1)

    if "DAYS_EMPLOYED" in df.columns:
        # DAYS_EMPLOYED of 365243 flags pensioners / not employed
        # 365243 is a sentinel value used in the raw dataset to indicate that
        # the applicant is a pensioner or has no recorded employment period.
        df["EMPLOYMENT_YEARS"] = np.where(
            df["DAYS_EMPLOYED"] == 365243,
            np.nan,
            (-df["DAYS_EMPLOYED"] / 365).round(1),
        )

    if "AMT_CREDIT" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["CREDIT_TO_INCOME"] = (
            df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"].replace(0, np.nan)
        ).round(2)

    if "AMT_ANNUITY" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["ANNUITY_TO_INCOME"] = (
            df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"].replace(0, np.nan)
        ).round(4)

    return df
