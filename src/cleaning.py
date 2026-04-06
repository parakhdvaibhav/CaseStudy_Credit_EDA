from __future__ import annotations

from typing import Optional, Sequence
import pandas as pd
from .config import NUMERIC_COLUMNS_NOTEBOOK, CleaningConfig, default_cleaning_config


def drop_high_null_columns(df: pd.DataFrame, threshold_pct: float) -> pd.DataFrame:
    """
    Drop columns whose percentage of missing values exceeds the threshold.

    Args:
        df: Input dataframe.
        threshold_pct: Maximum allowed missing-value percentage.

    Returns:
        pd.DataFrame: Dataframe with high-null columns removed.
    """
    null_pct = df.isnull().mean() * 100
    to_drop = list(null_pct[null_pct > threshold_pct].index)
    return df.drop(columns=to_drop, errors="ignore")


def drop_columns_by_prefix(df: pd.DataFrame, prefixes: Sequence[str]) -> pd.DataFrame:
    """
    Drop columns whose names start with any of the provided prefixes.

    Args:
        df: Input dataframe.
        prefixes: Prefix patterns used to identify columns for removal.

    Returns:
        pd.DataFrame: Dataframe with matching columns removed.
    """
    cols = list(df.columns)
    to_drop = [c for c in cols if any(c.startswith(p) for p in prefixes)]
    return df.drop(columns=to_drop, errors="ignore")


def drop_flag_document_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop all columns matching the `FLAG_DOCUMENT_*` pattern.

    These columns are excluded to simplify exploratory analysis.

    Args:
        df: Input dataframe.

    Returns:
        pd.DataFrame: Dataframe without document-flag columns.
    """
    cols = [c for c in df.columns if c.startswith("FLAG_DOCUMENT_")]
    return df.drop(columns=cols, errors="ignore")


def drop_explicit_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """
    Drop a specified list of columns.

    Args:
        df: Input dataframe.
        columns: Columns to remove.

    Returns:
        pd.DataFrame: Dataframe with selected columns removed.
    """
    return df.drop(columns=list(columns), errors="ignore")


def convert_negative_days_to_years(
    df: pd.DataFrame,
    days_column: str,
    new_column: str,
) -> pd.DataFrame:
    """
    Convert a negative day-based column into approximate years and rename it.

    The transformation:
    - converts values to absolute
    - converts days to years using integer division by 365
    - rounds the result
    - renames the source column

    Args:
        df: Input dataframe.
        days_column: Source day-based column.
        new_column: New human-readable column name.

    Returns:
        pd.DataFrame: Transformed dataframe.
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
    Replace anomalous `CODE_GENDER == 'XNA'` values with `'F'`.

    Args:
        df: Input dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    out = df.copy()
    if "CODE_GENDER" in out.columns:
        out.loc[out["CODE_GENDER"] == "XNA", "CODE_GENDER"] = "F"
    return out


def trim_outliers_quantile(
    df: pd.DataFrame,
    columns: Sequence[str],
    quantile: float = 0.99,
) -> pd.DataFrame:
    """
    Remove rows above the specified quantile for each selected column.

    Outlier filtering is applied iteratively column by column.

    Args:
        df: Input dataframe.
        columns: Columns used for outlier trimming.
        quantile: Upper quantile threshold.

    Returns:
        pd.DataFrame: Filtered dataframe.
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
    Add categorical income and loan group columns using predefined bins.

    The derived columns are inserted near the start of the dataframe
    to keep important segmentation variables prominent.

    Args:
        df: Input dataframe.
        income_bins: Bin edges for income grouping.
        income_labels: Labels for income bins.
        loan_bins: Bin edges for loan grouping.
        loan_labels: Labels for loan bins.

    Returns:
        pd.DataFrame: Dataframe with derived grouping columns.
    """
    out = df.copy()

    if "AMT_INCOME_TOTAL" in out.columns:
        out["INCOME_GROUP"] = pd.cut(
            x=out["AMT_INCOME_TOTAL"],
            bins=list(income_bins),
            labels=list(income_labels),
        )
        if "TARGET" in out.columns:
            mid = out["INCOME_GROUP"]
            out = out.drop(columns=["INCOME_GROUP"])
            out.insert(2, "INCOME_GROUP", mid)

    if "AMT_CREDIT" in out.columns:
        out["LOAN_GROUP"] = pd.cut(
            x=out["AMT_CREDIT"],
            bins=list(loan_bins),
            labels=list(loan_labels),
        )
        if "INCOME_GROUP" in out.columns:
            mid = out["LOAN_GROUP"]
            out = out.drop(columns=["LOAN_GROUP"])
            out.insert(3, "LOAN_GROUP", mid)

    return out


def cast_numeric_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """
    Cast selected columns to numeric dtype where possible.

    Non-convertible values are coerced to NaN.

    Args:
        df: Input dataframe.
        columns: Candidate numeric columns.

    Returns:
        pd.DataFrame: Dataframe with numeric casting applied.
    """
    out = df.copy()
    cols_present = [c for c in columns if c in out.columns]
    if cols_present:
        out[cols_present] = out[cols_present].apply(pd.to_numeric, errors="coerce")
    return out


def clean_current_application(
    curr_appl: pd.DataFrame,
    cfg: Optional[CleaningConfig] = None,
) -> pd.DataFrame:
    """
    Run the end-to-end cleaning pipeline for the current application dataset.

    The pipeline performs:
    - high-null column removal
    - prefix-based column removal
    - document flag cleanup
    - explicit column removal
    - conversion of day-based columns into years
    - categorical cleanup for gender anomalies
    - quantile-based outlier trimming
    - creation of income and loan group features
    - numeric type standardization

    Args:
        curr_appl: Raw current application dataframe.
        cfg: Optional cleaning configuration. If omitted, default settings are used.

    Returns:
        pd.DataFrame: Cleaned application dataframe.
    """
    cfg = cfg or default_cleaning_config()

    df = curr_appl.copy()

    df = drop_high_null_columns(df, threshold_pct=cfg.high_null_threshold_pct)
    df = drop_columns_by_prefix(df, prefixes=cfg.drop_prefixes)
    df = drop_flag_document_columns(df)
    df = drop_explicit_columns(df, cfg.drop_explicit)

    for days_col, new_col in cfg.days_to_years_map.items():
        df = convert_negative_days_to_years(df, days_col, new_col)

    df = fix_gender_xna(df)
    df = trim_outliers_quantile(df, cfg.outlier_columns, quantile=cfg.outlier_quantile)

    df = add_income_and_loan_groups(
        df,
        income_bins=cfg.income_bins,
        income_labels=cfg.income_labels,
        loan_bins=cfg.loan_bins,
        loan_labels=cfg.loan_labels,
    )

    df = cast_numeric_columns(df, NUMERIC_COLUMNS_NOTEBOOK)

    return df
