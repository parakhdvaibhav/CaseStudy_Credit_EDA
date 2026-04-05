"""
Statistical analysis helpers for the Credit EDA case study.
"""

import pandas as pd
import numpy as np
from scipy import stats

from src.config import TARGET_COLUMN, CORRELATION_THRESHOLD, OUTLIER_IQR_MULTIPLIER


def summarise_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Return a sorted DataFrame summarising missing values per column.

    Parameters
    ----------
    df:
        Source DataFrame.

    Returns
    -------
    pd.DataFrame
        Columns: ``count``, ``percent``.
    """
    missing_count = df.isnull().sum()
    missing_pct = missing_count / len(df) * 100
    summary = pd.DataFrame({"count": missing_count, "percent": missing_pct})
    return summary[summary["count"] > 0].sort_values("percent", ascending=False)


def detect_outliers_iqr(
    df: pd.DataFrame,
    column: str,
    multiplier: float = OUTLIER_IQR_MULTIPLIER,
) -> pd.Series:
    """Return a boolean mask indicating outlier rows using the IQR method.

    Parameters
    ----------
    df:
        Source DataFrame.
    column:
        Numerical column to inspect.
    multiplier:
        IQR multiplier for the whisker boundaries (default 1.5).

    Returns
    -------
    pd.Series[bool]
        ``True`` where the value is an outlier.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    return (df[column] < lower) | (df[column] > upper)


def cap_outliers(
    df: pd.DataFrame,
    column: str,
    multiplier: float = OUTLIER_IQR_MULTIPLIER,
) -> pd.DataFrame:
    """Cap outliers at the IQR whisker boundaries (winsorisation).

    Parameters
    ----------
    df:
        Source DataFrame (mutated in place, also returned).
    column:
        Numerical column to treat.
    multiplier:
        IQR multiplier.

    Returns
    -------
    pd.DataFrame
        DataFrame with capped values.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    df[column] = df[column].clip(lower=lower, upper=upper)
    return df


def high_correlation_pairs(
    df: pd.DataFrame,
    threshold: float = CORRELATION_THRESHOLD,
    method: str = "pearson",
) -> pd.DataFrame:
    """Return pairs of columns whose absolute correlation exceeds *threshold*.

    Parameters
    ----------
    df:
        Source DataFrame (only numerical columns are used).
    threshold:
        Minimum absolute correlation to include.
    method:
        Correlation method.

    Returns
    -------
    pd.DataFrame
        Columns: ``feature_1``, ``feature_2``, ``correlation``.
    """
    corr = df.select_dtypes(include=[np.number]).corr(method=method).abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    pairs = (
        upper.stack()
        .reset_index()
        .rename(columns={"level_0": "feature_1", "level_1": "feature_2", 0: "correlation"})
    )
    return pairs[pairs["correlation"] >= threshold].sort_values("correlation", ascending=False)


def default_rate_by_category(
    df: pd.DataFrame,
    feature: str,
    target: str = TARGET_COLUMN,
) -> pd.DataFrame:
    """Compute default rate and counts for each category of *feature*.

    Parameters
    ----------
    df:
        Source DataFrame.
    feature:
        Categorical column name.
    target:
        Binary target column name.

    Returns
    -------
    pd.DataFrame
        Columns: ``total``, ``defaults``, ``default_rate_pct``.
    """
    summary = df.groupby(feature)[target].agg(
        total="count",
        defaults="sum",
    )
    summary["default_rate_pct"] = (summary["defaults"] / summary["total"] * 100).round(2)
    return summary.sort_values("default_rate_pct", ascending=False)


def chi_square_test(
    df: pd.DataFrame,
    feature: str,
    target: str = TARGET_COLUMN,
    significance: float = 0.05,
) -> dict:
    """Perform a chi-square test of independence between *feature* and *target*.

    Parameters
    ----------
    df:
        Source DataFrame.
    feature:
        Categorical column to test.
    target:
        Target column.
    significance:
        Alpha level for significance decision.

    Returns
    -------
    dict
        Keys: ``chi2``, ``p_value``, ``dof``, ``significant``.
    """
    contingency = pd.crosstab(df[feature], df[target])
    chi2, p_value, dof, _ = stats.chi2_contingency(contingency)
    return {
        "chi2": round(chi2, 4),
        "p_value": round(p_value, 6),
        "dof": dof,
        "significant": p_value < significance,
    }


def descriptive_stats(df: pd.DataFrame, by: str | None = TARGET_COLUMN) -> pd.DataFrame:
    """Return descriptive statistics for numerical columns, optionally grouped.

    Parameters
    ----------
    df:
        Source DataFrame.
    by:
        Column to group by before computing stats.  Pass ``None`` for overall.

    Returns
    -------
    pd.DataFrame
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if by and by in df.columns:
        return numeric_df.groupby(df[by]).describe().T
    return numeric_df.describe().T
