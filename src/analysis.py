"""
Analysis utilities for the credit EDA project.

This module contains:
- Legacy test-compatible analytics helpers
- Missingness and default-rate analytics
- Correlation helpers
- A legacy feature engineering helper used by tests
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

<<<<<<< HEAD
=======
from src.config import CORRELATION_THRESHOLD, TARGET_COLUMN

logger = logging.getLogger(__name__)

>>>>>>> main

def calculate_missing_percentages(df: pd.DataFrame) -> pd.Series:
    """
    Return missing percentage (0-100) per column as a Series, sorted descending.
    """
    missing_pct = df.isnull().mean() * 100.0
    return missing_pct.sort_values(ascending=False)


def calculate_default_statistics(df: pd.DataFrame, target_col: str = "TARGET") -> dict:
    """
    Return summary statistics about default target.

    Expected keys (per tests):
      - total
      - defaults
      - non_defaults
      - default_rate
      - non_default_rate

    Raises:
      - KeyError if target column is missing.
    """
    if target_col not in df.columns:
        raise KeyError(target_col)

    total = int(len(df))
    defaults = int((df[target_col] == 1).sum())
    non_defaults = int((df[target_col] == 0).sum())

    default_rate = float(defaults / total) if total else 0.0
    non_default_rate = float(non_defaults / total) if total else 0.0

    return {
        "total": total,
        "defaults": defaults,
        "non_defaults": non_defaults,
        "default_rate": default_rate,
        "non_default_rate": non_default_rate,
    }


def calculate_default_rate_by_category(
    df: pd.DataFrame,
    category_col: str,
    target_col: str = "TARGET",
) -> pd.DataFrame:
    """
    Default rate (mean of TARGET) grouped by a categorical column.

    Returns a dataframe with columns:
      - <category_col>
      - default_rate
      - count

    Sorted by default_rate descending (per tests).
    """
    if target_col not in df.columns:
        raise KeyError(target_col)
    if category_col not in df.columns:
        raise KeyError(category_col)

    grouped = df.groupby(category_col)[target_col].agg(["mean", "count"]).reset_index()
    grouped = grouped.rename(columns={"mean": "default_rate", "count": "count"})
    return grouped.sort_values("default_rate", ascending=False).reset_index(drop=True)


def calculate_correlation_matrix(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    drop_cols: Tuple[str, ...] = ("SK_ID_CURR", "TARGET"),
) -> pd.DataFrame:
    """
    Return correlation matrix for numeric columns (or provided subset).

    The test suite calls:
        calculate_correlation_matrix(df, columns=[...])
    """
    if columns is None:
        columns = list(df.select_dtypes(include=["int64", "float64"]).columns)

    numeric_cols = set(df.select_dtypes(include=["int64", "float64"]).columns)
    cols = [c for c in columns if c in numeric_cols and c not in drop_cols]

    if not cols:
        return pd.DataFrame()

    return df[cols].corr(numeric_only=True)


def get_highly_correlated_pairs(df: pd.DataFrame, threshold: float = 0.8) -> pd.DataFrame:
    """
    Compute correlations on numeric columns and return highly correlated feature pairs.

    Tests pass a *dataframe* (not a precomputed correlation matrix).

    Returns columns:
      - feature_1
      - feature_2
      - correlation
    """
    num = df.select_dtypes(include=["int64", "float64"])
    if num.shape[1] < 2:
        return pd.DataFrame(columns=["feature_1", "feature_2", "correlation"])

    corr = num.corr(numeric_only=True)

    cols = list(corr.columns)
    rows: list[dict] = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
<<<<<<< HEAD
            c1, c2 = cols[i], cols[j]
            val = corr.iloc[i, j]
            if pd.notna(val) and abs(val) >= threshold:
                rows.append({"feature_1": c1, "feature_2": c2, "correlation": float(val)})
=======
            val = corr_matrix.iloc[i, j]
            if abs(val) >= threshold:
                pairs.append(
                    {"feature_1": cols[i], "feature_2": cols[j], "correlation": val}
                )
>>>>>>> main

    out = pd.DataFrame(rows, columns=["feature_1", "feature_2", "correlation"])
    if not out.empty:
        out = out.sort_values("correlation", ascending=False).reset_index(drop=True)
    return out


def calculate_missing_by_target(df: pd.DataFrame, target_col: str = "TARGET") -> pd.DataFrame:
    """
<<<<<<< HEAD
    Long-format missing % by target.
=======
    result = (
        df.groupby(TARGET_COLUMN)[column]
        .apply(
            lambda s: pd.Series({"missing_count": s.isnull().sum(), "total": len(s)})
        )
        .reset_index()
    )
    result.columns = [TARGET_COLUMN, "stat", "value"]
    result = result.pivot(
        index=TARGET_COLUMN, columns="stat", values="value"
    ).reset_index()
    result["missing_pct"] = (result["missing_count"] / result["total"]) * 100
    return result
>>>>>>> main

    IMPORTANT (per tests):
      - result must include a column literally named "TARGET"
      - result must include "missing_pct"

    Note: Even if caller passes a different target_col, we still output the column name "TARGET".
    """
    if target_col not in df.columns:
        raise KeyError(target_col)

    rows: list[dict] = []
    targets = sorted(df[target_col].dropna().unique().tolist())

    for t in targets:
        sub = df[df[target_col] == t]
        miss = sub.isnull().mean() * 100.0
        for feature, pct in miss.items():
            rows.append({"TARGET": t, "feature": feature, "missing_pct": float(pct)})

    return pd.DataFrame(rows)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Legacy feature engineering function expected by tests.

    Must add:
      - AGE_YEARS
      - EMPLOYMENT_YEARS
      - CREDIT_TO_INCOME
      - ANNUITY_TO_INCOME

    And: for Pensioners / special employed code, EMPLOYMENT_YEARS should be NaN.
    """
    out = df.copy()

    # AGE_YEARS from DAYS_BIRTH
    if "DAYS_BIRTH" in out.columns:
        out["AGE_YEARS"] = (out["DAYS_BIRTH"].abs() / 365).astype(float)

    # EMPLOYMENT_YEARS from DAYS_EMPLOYED
    if "DAYS_EMPLOYED" in out.columns:
        out["EMPLOYMENT_YEARS"] = (out["DAYS_EMPLOYED"].abs() / 365).astype(float)

    # Mark pensioners / special value as NaN for employment years
    if "EMPLOYMENT_YEARS" in out.columns:
        pensioner_mask = pd.Series(False, index=out.index)

        if "NAME_INCOME_TYPE" in out.columns:
            pensioner_mask = pensioner_mask | (
                out["NAME_INCOME_TYPE"].astype(str).str.lower() == "pensioner"
            )

        # Common Home Credit special value meaning "not employed" / anomaly
        if "DAYS_EMPLOYED" in out.columns:
            pensioner_mask = pensioner_mask | (out["DAYS_EMPLOYED"] == 365243)

        out.loc[pensioner_mask, "EMPLOYMENT_YEARS"] = np.nan

    # Ratios
    if "AMT_CREDIT" in out.columns and "AMT_INCOME_TOTAL" in out.columns:
        denom = out["AMT_INCOME_TOTAL"].replace(0, np.nan)
        out["CREDIT_TO_INCOME"] = out["AMT_CREDIT"] / denom

    if "AMT_ANNUITY" in out.columns and "AMT_INCOME_TOTAL" in out.columns:
        denom = out["AMT_INCOME_TOTAL"].replace(0, np.nan)
        out["ANNUITY_TO_INCOME"] = out["AMT_ANNUITY"] / denom

    return out


# ---------------------------------------------------------------------------
# Extra helpers (kept because they may be used elsewhere in your repo)
# ---------------------------------------------------------------------------

def split_by_target(df: pd.DataFrame, target_col: str = "TARGET") -> tuple[pd.DataFrame, pd.DataFrame]:
    if target_col not in df.columns:
        raise KeyError(target_col)
    return df[df[target_col] == 0].copy(), df[df[target_col] == 1].copy()


def target_distribution(df: pd.DataFrame, target_col: str = "TARGET") -> dict:
    if target_col not in df.columns:
        raise KeyError(target_col)
    total = len(df)
    t0 = int((df[target_col] == 0).sum())
    t1 = int((df[target_col] == 1).sum())
    return {
        "total": total,
        "target_0": t0,
        "target_1": t1,
        "target_0_pct": (t0 / total * 100.0) if total else 0.0,
        "target_1_pct": (t1 / total * 100.0) if total else 0.0,
    }


def correlation_matrices(target_0: pd.DataFrame, target_1: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    cor0 = calculate_correlation_matrix(target_0)
    cor1 = calculate_correlation_matrix(target_1)
    return cor0, cor1