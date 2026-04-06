from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from .config import NUMERIC_COLUMNS_NOTEBOOK, CleaningConfig, default_cleaning_config


def drop_high_null_columns(df: pd.DataFrame, threshold_pct: float) -> pd.DataFrame:
    """
    Drop columns whose percentage of null values is > threshold_pct.
    """
    null_pct = df.isnull().mean() * 100
    to_drop = list(null_pct[null_pct > threshold_pct].index)
    return df.drop(columns=to_drop, errors="ignore")


def drop_columns_by_prefix(df: pd.DataFrame, prefixes: Sequence[str]) -> pd.DataFrame:
    """
    Drop columns starting with any of the provided prefixes.
    """
    cols = list(df.columns)
    to_drop = [c for c in cols if any(c.startswith(p) for p in prefixes)]
    return df.drop(columns=to_drop, errors="ignore")


def drop_flag_document_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop FLAG_DOCUMENT_* columns (the notebook drops these as not useful for analysis).
    """
    cols = [c for c in df.columns if c.startswith("FLAG_DOCUMENT_")]
    return df.drop(columns=cols, errors="ignore")


def drop_explicit_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    return df.drop(columns=list(columns), errors="ignore")


def convert_negative_days_to_years(
    df: pd.DataFrame, days_column: str, new_column: str
) -> pd.DataFrame:
    """
    Notebook logic:
      - take abs() of DAYS_* columns
      - integer divide by 365
      - round
      - rename to new semantic column
    """
    out = df.copy()
    if days_column not in out.columns:
        return out

    out[days_column] = out[days_column].abs()
    out[days_column] = (out[days_column] // 365).round()
    out = out.rename(columns={days_column: new_column})
    return out


def fix_gender_xna(df: pd.DataFrame) -> pd.DataFrame:
    """
    Notebook logic: replace CODE_GENDER=='XNA' with 'F'.
    """
    out = df.copy()
    if "CODE_GENDER" in out.columns:
        out.loc[out["CODE_GENDER"] == "XNA", "CODE_GENDER"] = "F"
    return out


def trim_outliers_quantile(
    df: pd.DataFrame, columns: Sequence[str], quantile: float = 0.99
) -> pd.DataFrame:
    """
    Remove rows above quantile for each column (iteratively) as per notebook.
    """
    out = df.copy()
    for col in columns:
        if col not in out.columns:
            continue
        q = out[col].quantile(quantile)
        out = out[out[col] < q]
    return out


def add_income_and_loan_groups(
    df: pd.DataFrame,
    income_bins: Sequence[float],
    income_labels: Sequence[str],
    loan_bins: Sequence[float],
    loan_labels: Sequence[str],
) -> pd.DataFrame:
    """
    Add INCOME_GROUP and LOAN_GROUP columns via pd.cut and insert them
    near the start of the dataframe (matching notebook intent).
    """
    out = df.copy()

    if "AMT_INCOME_TOTAL" in out.columns:
        out["INCOME_GROUP"] = pd.cut(
            x=out["AMT_INCOME_TOTAL"], bins=list(income_bins), labels=list(income_labels)
        )
        # insert after TARGET if present
        if "TARGET" in out.columns:
            mid = out["INCOME_GROUP"]
            out = out.drop(columns=["INCOME_GROUP"])
            out.insert(2, "INCOME_GROUP", mid)

    if "AMT_CREDIT" in out.columns:
        out["LOAN_GROUP"] = pd.cut(
            x=out["AMT_CREDIT"], bins=list(loan_bins), labels=list(loan_labels)
        )
        if "INCOME_GROUP" in out.columns:
            mid = out["LOAN_GROUP"]
            out = out.drop(columns=["LOAN_GROUP"])
            # after INCOME_GROUP (which is at index 2)
            out.insert(3, "LOAN_GROUP", mid)

    return out


def cast_numeric_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    out = df.copy()
    cols_present = [c for c in columns if c in out.columns]
    if cols_present:
        out[cols_present] = out[cols_present].apply(pd.to_numeric, errors="coerce")
    return out


def clean_current_application(
    curr_appl: pd.DataFrame, cfg: Optional[CleaningConfig] = None
) -> pd.DataFrame:
    """
    End-to-end cleaning pipeline for current application dataset,
    based on the original notebook.
    """
    cfg = cfg or default_cleaning_config()

    df = curr_appl.copy()

    # Step 1: Drop columns with > 50% nulls
    df = drop_high_null_columns(df, threshold_pct=cfg.high_null_threshold_pct)

    # Step 2: Drop columns by prefix pattern (OBS_, DEF_, AMT_REQ_CREDIT..., EXT_..., etc.)
    df = drop_columns_by_prefix(df, prefixes=cfg.drop_prefixes)

    # Step 3: Drop FLAG_DOCUMENT_* columns
    df = drop_flag_document_columns(df)

    # Step 4: Drop explicit columns listed in notebook
    df = drop_explicit_columns(df, cfg.drop_explicit)

    # Step 5: Convert negative day columns to years + rename
    for days_col, new_col in cfg.days_to_years_map.items():
        df = convert_negative_days_to_years(df, days_col, new_col)

    # Step 6: Fix gender
    df = fix_gender_xna(df)

    # Step 7: Outlier trimming
    df = trim_outliers_quantile(df, cfg.outlier_columns, quantile=cfg.outlier_quantile)

    # Step 8: Create bins
    df = add_income_and_loan_groups(
        df,
        income_bins=cfg.income_bins,
        income_labels=cfg.income_labels,
        loan_bins=cfg.loan_bins,
        loan_labels=cfg.loan_labels,
    )

    # Step 9: Cast numerics
    df = cast_numeric_columns(df, NUMERIC_COLUMNS_NOTEBOOK)

    return df