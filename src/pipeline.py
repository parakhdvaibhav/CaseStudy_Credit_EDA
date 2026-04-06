"""
End-to-end pipeline helpers for the credit EDA project.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .analysis import (
    calculate_default_rate_by_category,
    calculate_default_statistics,
    engineer_features,
)
from .data_loader import load_application_data, validate_data_quality
from .visualizations import (
    plot_age_vs_default,
    plot_correlation_heatmap,
    plot_default_by_income,
    plot_distribution,
)


def save_figure(fig, output_path: Path) -> None:
    """Save a matplotlib figure to disk."""
    fig.savefig(output_path, dpi=100)


def run_full_eda(data_path: str, output_dir: str = "reports") -> dict:
    """
    Run the end-to-end exploratory data analysis workflow.

    Args:
        data_path: Path to the application dataset CSV.
        output_dir: Directory where output charts will be saved.

    Returns:
        dict: Summary of pipeline outputs and key analytical results.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df = load_application_data(data_path)
    quality = validate_data_quality(df)
    stats = calculate_default_statistics(df)
    df = engineer_features(df)

    income_rates = None
    if "NAME_INCOME_TYPE" in df.columns:
        income_rates = calculate_default_rate_by_category(df, "NAME_INCOME_TYPE")

    numeric_cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
    existing_numeric = [col for col in numeric_cols if col in df.columns]

    saved_files: list[str] = []

    if existing_numeric:
        file_path = output_path / "income_distribution.png"
        fig = plot_distribution(df, existing_numeric[0])
        save_figure(fig, file_path)
        saved_files.append(str(file_path))

    if "NAME_INCOME_TYPE" in df.columns:
        file_path = output_path / "default_by_income.png"
        fig = plot_default_by_income(df)
        save_figure(fig, file_path)
        saved_files.append(str(file_path))

    if "DAYS_BIRTH" in df.columns:
        file_path = output_path / "age_vs_default.png"
        fig = plot_age_vs_default(df)
        save_figure(fig, file_path)
        saved_files.append(str(file_path))

    if len(existing_numeric) >= 2:
        file_path = output_path / "correlation_heatmap.png"
        fig = plot_correlation_heatmap(df, columns=existing_numeric)
        save_figure(fig, file_path)
        saved_files.append(str(file_path))

    return {
        "shape": df.shape,
        "quality_report": quality,
        "default_statistics": stats,
        "income_rates": income_rates,
        "saved_files": saved_files,
    }