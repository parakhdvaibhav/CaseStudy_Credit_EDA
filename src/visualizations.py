"""
Visualization utilities for the credit EDA project.

These functions are implemented to satisfy the unit tests in tests/test_visualizations.py.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_distribution(df: pd.DataFrame, column: str, title: str | None = None):
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=df, x=column, kde=False, ax=ax)

    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    ax.set_title(title if title is not None else f"Distribution of {column}")
    fig.tight_layout()
    return fig


def plot_default_analysis(df: pd.DataFrame, feature: str, title: str | None = None, target_col: str = "TARGET"):
    if target_col not in df.columns:
        raise ValueError(f"Missing required column: {target_col}")
    if feature not in df.columns:
        raise ValueError(f"Feature '{feature}' not found")

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.countplot(x=feature, hue=target_col, data=df, ax=ax)

    ax.tick_params(axis="x", rotation=45)
    ax.set_title(title if title is not None else f"Default analysis by {feature}")
    fig.tight_layout()
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, columns: list[str] | None = None, title: str = "Correlation Heatmap"):
    num = df.select_dtypes(include=["int64", "float64"])
    if columns is not None:
        num = num[[c for c in columns if c in num.columns]]

    if num.shape[1] == 0:
        raise ValueError("No numeric columns available for correlation")

    corr = num.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, cmap="twilight", annot=False, ax=ax)

    ax.set_title(title)
    fig.tight_layout()
    return fig


def plot_default_by_income(
    df: pd.DataFrame,
    income_column: str = "INCOME_GROUP",
    title: str | None = None,
    target_col: str = "TARGET",
):
    """
    Plot default rate by income group.

    Behavior required by tests:
      - If TARGET missing -> raise ValueError mentioning TARGET
      - If income_column is default ("INCOME_GROUP") and not present -> fallback to binning AMT_INCOME_TOTAL
      - If income_column is explicitly provided (not "INCOME_GROUP") and missing -> raise ValueError "not found"
    """
    if target_col not in df.columns:
        raise ValueError(f"Missing required column: {target_col}")

    if income_column not in df.columns:
        # Only allow fallback for the default column name
        if income_column == "INCOME_GROUP":
            if "AMT_INCOME_TOTAL" not in df.columns:
                raise ValueError(f"Column '{income_column}' not found")

            tmp = df.copy()
            income_column = "__INCOME_BIN__"
            tmp[income_column] = pd.qcut(tmp["AMT_INCOME_TOTAL"], q=4, duplicates="drop")
            df = tmp
        else:
            raise ValueError(f"Column '{income_column}' not found")

    rates = df.groupby(income_column)[target_col].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=rates, x=income_column, y=target_col, ax=ax)

    ax.tick_params(axis="x", rotation=45)
    ax.set_ylabel("Default rate")
    ax.set_title(title if title is not None else "Default rate by income group")
    fig.tight_layout()
    return fig


def plot_age_vs_default(
    df: pd.DataFrame,
    age_column: str = "AGE_CLIENT",
    title: str | None = None,
    target_col: str = "TARGET",
):
    if target_col not in df.columns:
        raise ValueError(f"Missing required column: {target_col}")

    if age_column not in df.columns:
        if age_column == "AGE_CLIENT" and "DAYS_BIRTH" in df.columns:
            tmp = df.copy()
            age_column = "__AGE_YEARS__"
            tmp[age_column] = (tmp["DAYS_BIRTH"].abs() / 365).astype(float)
            df = tmp
        else:
            raise ValueError(f"Column '{age_column}' not found")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=df, x=age_column, hue=target_col, element="step", ax=ax)

    ax.set_title(title if title is not None else f"{age_column} vs {target_col}")
    fig.tight_layout()
    return fig


def plot_target_count(df: pd.DataFrame, target_col: str = "TARGET", title: str = "Target distribution"):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x=target_col, data=df, ax=ax)
    ax.set_title(title)
    fig.tight_layout()
    return fig