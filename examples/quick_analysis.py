#!/usr/bin/env python
"""
Quick end-to-end example for the CaseStudy_Credit_EDA project.

This script demonstrates how to:
- run the reusable EDA pipeline on the real dataset
- fall back to a synthetic dataset when no real data is provided

Usage:
    python examples/quick_analysis.py --data data/raw/application_data.csv
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

from src.analysis import calculate_default_rate_by_category  # noqa: E402
from src.pipeline import run_full_eda  # noqa: E402
from src.visualizations import (  # noqa: E402
    plot_age_vs_default,
    plot_correlation_heatmap,
    plot_default_by_income,
    plot_distribution,
)


def make_synthetic_data(n: int = 500) -> pd.DataFrame:
    """
    Create a synthetic dataset that roughly mirrors the real schema.
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


def save_figure(fig, output_path: Path) -> None:
    """Save a matplotlib figure to disk."""
    fig.savefig(output_path, dpi=100)
    print(f"Saved: {output_path}")


def run_synthetic_demo(output_dir: str = "reports") -> None:
    """
    Run a lightweight demo using synthetic data when no real dataset is available.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Real data file not found. Using synthetic dataset instead.")
    df = make_synthetic_data()
    print(f"Dataset shape: {df.shape}")

    defaults = int((df["TARGET"] == 1).sum())
    total = len(df)
    default_rate = defaults / total if total else 0.0

    print("\nDefault Statistics")
    print(f"  Total applications:      {total:,}")
    print(f"  Defaults:                {defaults:,}")
    print(f"  Non-defaults:            {total - defaults:,}")
    print(f"  Default rate:            {default_rate:.2%}")

    income_rates = calculate_default_rate_by_category(df, "NAME_INCOME_TYPE")
    print("\nDefault Rates by Income Type")
    print(income_rates.to_string(index=False))

    fig = plot_distribution(df, "AMT_INCOME_TOTAL")
    save_figure(fig, output_path / "income_distribution.png")

    fig = plot_default_by_income(df)
    save_figure(fig, output_path / "default_by_income.png")

    fig = plot_age_vs_default(df)
    save_figure(fig, output_path / "age_vs_default.png")

    fig = plot_correlation_heatmap(
        df, columns=["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
    )
    save_figure(fig, output_path / "correlation_heatmap.png")

    print("\nSynthetic quick analysis complete.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
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

    if args.data and os.path.exists(args.data):
        result = run_full_eda(args.data, args.output)
        print("EDA pipeline completed successfully.")
        print(f"Dataset shape: {result['shape']}")
        print(f"Saved files: {len(result['saved_files'])}")
        for file_path in result["saved_files"]:
            print(f"Saved: {file_path}")
    else:
        run_synthetic_demo(args.output)
