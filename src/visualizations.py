"""
Reusable visualization functions for the Credit EDA project.
"""

import logging
from typing import List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.config import (
    COLOR_PALETTE,
    DEFAULT_COLOR,
    FIGURE_SIZE,
    HEATMAP_FIGURE_SIZE,
    NON_DEFAULT_COLOR,
    TARGET_COLUMN,
)

matplotlib.use("Agg")  # Non-interactive backend – safe for CI / headless environments
# Must be called before any other matplotlib imports that trigger the backend load.

logger = logging.getLogger(__name__)


def plot_distribution(
    data: pd.DataFrame,
    column: str,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = FIGURE_SIZE,
) -> plt.Figure:
    """Plot a histogram + KDE for a single numeric column.

    Parameters
    ----------
    data:
        Source DataFrame.
    column:
        Column to plot.
    title:
        Plot title.  Defaults to ``"Distribution of <column>"``.
    figsize:
        Figure dimensions ``(width, height)``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    if column not in data.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    fig, ax = plt.subplots(figsize=figsize)
    plot_data = data[column].dropna()

    sns.histplot(plot_data, kde=True, ax=ax, color="steelblue")
    ax.set_title(title or f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    plt.tight_layout()
    return fig


def plot_default_analysis(
    data: pd.DataFrame,
    feature: str,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = FIGURE_SIZE,
) -> plt.Figure:
    """Bar chart showing default vs non-default counts for a categorical feature.

    Parameters
    ----------
    data:
        Source DataFrame containing both ``TARGET`` and *feature*.
    feature:
        Categorical feature to analyse.
    title:
        Plot title.
    figsize:
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
    """
    if TARGET_COLUMN not in data.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in DataFrame.")
    if feature not in data.columns:
        raise ValueError(f"Feature '{feature}' not found in DataFrame.")

    fig, ax = plt.subplots(figsize=figsize)

    grouped = (
        data.groupby([feature, TARGET_COLUMN]).size().reset_index(name="count")
    )
    grouped[TARGET_COLUMN] = grouped[TARGET_COLUMN].map({0: "No Default", 1: "Default"})

    sns.barplot(
        data=grouped,
        x=feature,
        y="count",
        hue=TARGET_COLUMN,
        palette=[NON_DEFAULT_COLOR, DEFAULT_COLOR],
        ax=ax,
    )
    ax.set_title(title or f"Default Analysis by {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = "Correlation Heatmap",
    figsize: Tuple[int, int] = HEATMAP_FIGURE_SIZE,
) -> plt.Figure:
    """Plot a Pearson correlation heatmap.

    Parameters
    ----------
    data:
        Source DataFrame.
    columns:
        Subset of columns to include.  Defaults to all numeric columns.
    title:
        Plot title.
    figsize:
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
    """
    if columns is not None:
        data = data[columns]

    numeric_data = data.select_dtypes(include=[np.number])

    if numeric_data.empty:
        raise ValueError("No numeric columns available for correlation heatmap.")

    corr = numeric_data.corr()

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_default_by_income(
    data: pd.DataFrame,
    income_column: str = "NAME_INCOME_TYPE",
    title: str = "Default Rate by Income Type",
    figsize: Tuple[int, int] = FIGURE_SIZE,
) -> plt.Figure:
    """Bar chart of default rates grouped by income type.

    Parameters
    ----------
    data:
        Source DataFrame.
    income_column:
        Categorical column representing income type.
    title:
        Plot title.
    figsize:
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
    """
    if TARGET_COLUMN not in data.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in DataFrame.")
    if income_column not in data.columns:
        raise ValueError(f"Column '{income_column}' not found in DataFrame.")

    default_rates = (
        data.groupby(income_column)[TARGET_COLUMN].mean().sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=figsize)
    default_rates.plot(kind="bar", color=DEFAULT_COLOR, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(income_column)
    ax.set_ylabel("Default Rate")
    ax.axhline(y=data[TARGET_COLUMN].mean(), color="navy", linestyle="--", label="Overall Mean")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig


def plot_age_vs_default(
    data: pd.DataFrame,
    age_column: str = "DAYS_BIRTH",
    bins: int = 10,
    title: str = "Default Rate by Age Group",
    figsize: Tuple[int, int] = FIGURE_SIZE,
) -> plt.Figure:
    """Plot default rate across age brackets.

    Parameters
    ----------
    data:
        Source DataFrame.
    age_column:
        Column containing age in days (negative values as stored in the raw data).
        If the column contains positive values they are treated as years directly.
    bins:
        Number of age bins.
    title:
        Plot title.
    figsize:
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
    """
    if TARGET_COLUMN not in data.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in DataFrame.")
    if age_column not in data.columns:
        raise ValueError(f"Column '{age_column}' not found in DataFrame.")

    temp = data[[age_column, TARGET_COLUMN]].dropna().copy()

    # Convert negative days to positive years if necessary
    if temp[age_column].mean() < 0:
        temp["AGE_YEARS"] = -temp[age_column] / 365
    else:
        temp["AGE_YEARS"] = temp[age_column]

    temp["AGE_GROUP"] = pd.cut(temp["AGE_YEARS"], bins=bins)
    default_by_age = temp.groupby("AGE_GROUP")[TARGET_COLUMN].mean()

    fig, ax = plt.subplots(figsize=figsize)
    default_by_age.plot(kind="bar", color="steelblue", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Default Rate")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig
