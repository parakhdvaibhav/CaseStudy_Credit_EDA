from __future__ import annotations

from typing import Dict, List, Tuple

import pandas as pd


def split_by_target(df: pd.DataFrame, target_col: str = "TARGET") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the dataframe into (target_0_df, target_1_df).
    """
    if target_col not in df.columns:
        raise ValueError(f"'{target_col}' column not found")
    return df.loc[df[target_col] == 0].copy(), df.loc[df[target_col] == 1].copy()


def target_distribution(df: pd.DataFrame, target_col: str = "TARGET") -> Dict[str, float]:
    """
    Return distribution percentages for target 0 and 1.
    """
    if target_col not in df.columns:
        raise ValueError(f"'{target_col}' column not found")

    total = len(df)
    if total == 0:
        return {"target_0_pct": 0.0, "target_1_pct": 0.0}

    t0 = (df[target_col] == 0).sum()
    t1 = (df[target_col] == 1).sum()
    return {
        "target_0_pct": 100.0 * t0 / total,
        "target_1_pct": 100.0 * t1 / total,
    }


def correlation_matrices(
    target_0: pd.DataFrame,
    target_1: pd.DataFrame,
    drop_cols: Tuple[str, ...] = ("SK_ID_CURR", "TARGET"),
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build correlation matrices for numeric columns for target_0 and target_1.
    Mirrors the notebook's approach (drop SK_ID_CURR and TARGET from correlation set).
    """
    num_cols = list(target_1.select_dtypes(include=["int64", "float64"]).columns)
    for c in drop_cols:
        if c in num_cols:
            num_cols.remove(c)

    cor0 = target_0[num_cols].corr(numeric_only=True)
    cor1 = target_1[num_cols].corr(numeric_only=True)
    return cor0, cor1