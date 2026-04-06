from __future__ import annotations

from typing import Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_target_count(df: pd.DataFrame, target_col: str = "TARGET"):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x=target_col, data=df, ax=ax)
    ax.set_title("Target distribution")
    return fig


def plot_uni_categorical(target_0: pd.DataFrame, target_1: pd.DataFrame, column_name: str):
    """
    Notebook-style side-by-side countplots for a categorical feature.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

    sns.countplot(x=column_name, data=target_0, ax=axes[0])
    axes[0].tick_params(axis="x", rotation=90)
    axes[0].set_title("Target = 0")

    sns.countplot(x=column_name, data=target_1, ax=axes[1])
    axes[1].tick_params(axis="x", rotation=90)
    axes[1].set_title("Target = 1")

    fig.tight_layout()
    return fig


def plot_outlier_box_violin(df: pd.DataFrame, column: str, log_scale: bool = False):
    fig, axes = plt.subplots(2, 1, figsize=(6, 6))

    sns.boxplot(y=df[column], palette="rainbow", orient="v", ax=axes[0])
    axes[0].set_title(column)

    sns.violinplot(y=df[column], palette="Set1", orient="v", ax=axes[1])
    axes[1].set_title(column)

    if log_scale:
        axes[0].set_yscale("log")
        axes[1].set_yscale("log")

    fig.tight_layout()
    return fig


def plot_correlation_heatmaps(cor0: pd.DataFrame, cor1: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(30, 10))
    sns.heatmap(cor0, cmap="twilight", annot=False, ax=axes[0])
    axes[0].set_title("Correlation: Target=0")

    sns.heatmap(cor1, cmap="twilight", annot=False, ax=axes[1])
    axes[1].set_title("Correlation: Target=1")

    fig.tight_layout()
    return fig