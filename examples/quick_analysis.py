#!/usr/bin/env python
"""
Quick end-to-end example for the CaseStudy_Credit_EDA project.

This script demonstrates how to:
- load the application dataset
- validate data quality
- generate summary statistics
- engineer analytical features
- create a small set of reusable visualizations

If no real dataset is provided, the script falls back to a synthetic sample
so the pipeline can still be executed end to end.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Ensure the project root is available on the import path when the script
# is executed directly from the examples/ directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import (  # noqa: E402
    calculate_default_rate_by_category,
    calculate_default_statistics,
    engineer_features,
)
from src.data_loader import load_application_data, validate_data_quality  # noqa: E402
from src.visualizations import (  # noqa: E402
    plot_age_vs_default,
    plot_correlation_heatmap,
    plot_default_by_income,
    plot_distribution,
)


def make_synthetic_data(n: int = 500) -> pd.DataFrame:
    """
    Create a synthetic dataset that roughly mirrors the real schema.

    Args:
        n: Number of synthetic rows to generate.

    Returns:
        pd.DataFrame: Synthetic credit application dataset.
    """
    rng = np.random.default_rng(42)

    return pd.DataFrame(
        {
            "SK_ID_CURR": range(1, n + 1),
            "TARGET": rng.choice([0, 1], size=n, p=[0.92, 0.08]),
            "AMT_INCOME_TOTAL": rng.uniform(50_000, 500_000, n),
            "AMT_CREDIT": rng.uniform(100_000, 1_000_000, n),
            "AMT_ANNUITY": rng.uniform(5_000, 50_000, n),
            "AMT_GOODS_PRICE": rng.uniform(90_000, 900_000, n),
            "DAYS_BIRTH": rng.integers(-25_000, -6_000, n),
            "DAYS_EMPLOYED": rng.integers(-10_000, -100, n),
            "NAME_INCOME_TYPE": rng.choice(
                ["Working", "Commercial associate", "Pensioner", "State servant"],
                n,
            ),
            "CODE_GENDER": rng.choice(["M", "F"], n),
        }
    )


def load_input_data(data_path: str | None) -> pd.DataFrame:
    """
    Load the real dataset if available; otherwise return synthetic data.

    Args:
        data_path: Optional path to the application CSV.

    Returns:
        pd.DataFrame: Loaded or synthetic dataframe.
    """
    if data_path and os.path.exists(data_path):
        print(f"Loading data from: {data_path}")
        return load_application_data(data_path)

    print("Real data file not found. Using synthetic dataset instead.")
    return make_synthetic_data()


def save_figure(fig, output_path: Path) -> None:
    """
    Save a matplotlib figure to disk.

    Args:
        fig: Matplotlib figure object.
        output_path: Destination file path.
    """
    fig.savefig(output_path, dpi=100)
    print(f"Saved: {output_path}")


def run(data_path: str | None = None, output_dir: str = "reports") -> None:
    """
    Execute the quick analysis workflow.

    Args:
        data_path: Optional path to the real application dataset.
        output_dir: Directory where output figures will be saved.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    df = load_input_data(data_path)
    print(f"Dataset shape: {df.shape}")

    # 2. Data quality report
    quality = validate_data_quality(df)
    print("\nData Quality Summary")
    print(f"  Rows:                    {quality['shape'][0]:,}")
    print(f"  Columns:                 {quality['shape'][1]}")
    print(f"  Duplicate rows:          {quality['duplicate_rows']}")
    print(f"  High-missing columns:    {len(quality['high_missing_columns'])}")
    print(f"  Target column present:   {quality['has_target']}")

    # 3. Default statistics
    stats = calculate_default_statistics(df)
    print("\nDefault Statistics")
    print(f"  Total applications:      {stats['total']:,}")
    print(f"  Defaults:                {stats['defaults']:,}")
    print(f"  Non-defaults:            {stats['non_defaults']:,}")
    print(f"  Default rate:            {stats['default_rate']:.2%}")

    # 4. Feature engineering
    df = engineer_features(df)
    print(
        "\nEngineered features added: "
        "AGE_YEARS, EMPLOYMENT_YEARS, CREDIT_TO_INCOME, ANNUITY_TO_INCOME"
    )

    # 5. Default rates by income type
    if "NAME_INCOME_TYPE" in df.columns:
        income_rates = calculate_default_rate_by_category(df, "NAME_INCOME_TYPE")
        print("\nDefault Rates by Income Type")
        print(income_rates.to_string(index=False))

    # 6. Visualizations
    numeric_cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
    existing_numeric = [col for col in numeric_cols if col in df.columns]

    if existing_numeric:
        fig = plot_distribution(df, existing_numeric[0])
        save_figure(fig, output_path / "income_distribution.png")

    if "NAME_INCOME_TYPE" in df.columns:
        fig = plot_default_by_income(df)
        save_figure(fig, output_path / "default_by_income.png")

    if "DAYS_BIRTH" in df.columns:
        fig = plot_age_vs_default(df)
        save_figure(fig, output_path / "age_vs_default.png")

    if len(existing_numeric) >= 2:
        fig = plot_correlation_heatmap(df, columns=existing_numeric)
        save_figure(fig, output_path / "correlation_heatmap.png")

    print("\nQuick analysis complete.")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Quick Credit EDA analysis")
    parser.add_argument(
        "--data",
        default=None,
        help="Path to application_data.csv. If omitted, synthetic data is used.",
    )
    parser.add_argument(
        "--output",
        default="reports",
        help="Directory where output charts will be saved.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(data_path=args.data, output_dir=args.output)