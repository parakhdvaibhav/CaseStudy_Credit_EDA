"""
Reusable visualization helpers for the Credit EDA case study.
All functions return the Figure/Axes so callers can customize further.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from src.config import FIGURE_SIZE, PALETTE_DEFAULT, PALETTE_TARGET, TARGET_COLUMN


def plot_distribution(
    df: pd.DataFrame,
    column: str,
    hue: str | None = TARGET_COLUMN,
    bins: int = 30,
    figsize: tuple = FIGURE_SIZE,
) -> plt.Figure:
    """Plot the distribution of a numerical column, optionally split by *hue*.

    Parameters
    ----------
    df:
        Source DataFrame.
    column:
        Numerical column to plot.
    hue:
        Categorical column used to split distributions.
    bins:
        Number of histogram bins.
    figsize:
        Figure size ``(width, height)`` in inches.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    if hue and hue in df.columns:
        for val, grp in df.groupby(hue):
            ax.hist(grp[column].dropna(), bins=bins, alpha=0.6, label=f"{hue}={val}", density=True)
        ax.legend()
    else:
        ax.hist(df[column].dropna(), bins=bins, color="steelblue", alpha=0.8)
    ax.set_xlabel(column)
    ax.set_ylabel("Density")
    ax.set_title(f"Distribution of {column}")
    plt.tight_layout()
    return fig


def plot_default_analysis(
    df: pd.DataFrame,
    feature: str,
    top_n: int = 10,
    figsize: tuple = FIGURE_SIZE,
) -> plt.Figure:
    """Bar chart showing default rate (TARGET=1 %) for each category of *feature*.

    Parameters
    ----------
    df:
        DataFrame containing *feature* and TARGET_COLUMN.
    feature:
        Categorical feature column name.
    top_n:
        Show only the top-N categories by default rate.
    figsize:
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    default_rate = (
        df.groupby(feature)[TARGET_COLUMN]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .head(top_n)
    )
    fig, ax = plt.subplots(figsize=figsize)
    default_rate.plot(kind="bar", color=sns.color_palette(PALETTE_DEFAULT, len(default_rate)), ax=ax)
    ax.set_title(f"Default Rate (%) by {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("Default Rate (%)")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(
    df: pd.DataFrame,
    figsize: tuple = (14, 10),
    method: str = "pearson",
) -> plt.Figure:
    """Correlation heatmap for numerical columns of *df*.

    Parameters
    ----------
    df:
        Source DataFrame (only numerical columns are used).
    figsize:
        Figure size.
    method:
        Correlation method: ``'pearson'``, ``'spearman'``, or ``'kendall'``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr(method=method)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        corr,
        mask=mask,
        annot=False,
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title(f"Correlation Heatmap ({method.capitalize()})")
    plt.tight_layout()
    return fig


def plot_count_by_target(
    df: pd.DataFrame,
    feature: str,
    figsize: tuple = FIGURE_SIZE,
) -> plt.Figure:
    """Side-by-side count plots split by TARGET (0 vs 1).

    Parameters
    ----------
    df:
        Source DataFrame.
    feature:
        Categorical column to plot.
    figsize:
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    for ax, target_val in zip(axes, [0, 1]):
        subset = df[df[TARGET_COLUMN] == target_val]
        counts = subset[feature].value_counts().head(10)
        counts.plot(kind="bar", ax=ax, color=PALETTE_TARGET[target_val], alpha=0.85)
        ax.set_title(f"{feature} | TARGET={target_val}")
        ax.set_xlabel(feature)
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


def plot_violin(
    df: pd.DataFrame,
    x: str,
    y: str,
    figsize: tuple = FIGURE_SIZE,
) -> plt.Figure:
    """Violin plot of *y* grouped by *x*.

    Parameters
    ----------
    df:
        Source DataFrame.
    x:
        Categorical grouping column (e.g. TARGET).
    y:
        Numerical column to show distribution for.
    figsize:
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    sns.violinplot(data=df, x=x, y=y, palette=PALETTE_DEFAULT, ax=ax)
    ax.set_title(f"Distribution of {y} by {x}")
    plt.tight_layout()
    return fig
