#!/usr/bin/env python
"""
quick_analysis.py
-----------------
Minimal reproducible example showing how to use the CaseStudy_Credit_EDA
utility modules.

Usage
-----
    python examples/quick_analysis.py --data data/raw/application_data.csv

If no --data flag is provided the script generates a small synthetic dataset
so you can verify the pipeline runs end-to-end without the real data.
"""

import argparse
import os
import sys

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")

# Ensure the project root is on the Python path when running from any directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import (
    calculate_default_statistics,
    calculate_default_rate_by_category,
    engineer_features,
)
from src.data_loader import load_application_data, validate_data_quality
from src.visualizations import (
    plot_age_vs_default,
    plot_correlation_heatmap,
    plot_default_by_income,
    plot_distribution,
)


def _make_synthetic_data(n: int = 500) -> pd.DataFrame:
    """Return a tiny synthetic dataset that mirrors the real schema."""
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
                ["Working", "Commercial associate", "Pensioner", "State servant"], n
            ),
            "CODE_GENDER": rng.choice(["M", "F"], n),
        }
    )


def run(data_path: str = None, output_dir: str = "reports") -> None:
    """Execute the quick analysis workflow."""
    os.makedirs(output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    if data_path and os.path.exists(data_path):
        print(f"Loading data from: {data_path}")
        df = load_application_data(data_path)
    else:
        print("Real data file not found – using synthetic dataset.")
        df = _make_synthetic_data()

    print(f"Dataset shape: {df.shape}")

    # ------------------------------------------------------------------
    # 2. Data quality report
    # ------------------------------------------------------------------
    quality = validate_data_quality(df)
    print(f"\nData Quality Summary")
    print(f"  Rows:            {quality['shape'][0]:,}")
    print(f"  Columns:         {quality['shape'][1]}")
    print(f"  Duplicate rows:  {quality['duplicate_rows']}")
    print(
        f"  High-missing cols (>50%): {len(quality['high_missing_columns'])}"
    )

    # ------------------------------------------------------------------
    # 3. Default statistics
    # ------------------------------------------------------------------
    stats = calculate_default_statistics(df)
    print(f"\nDefault Statistics")
    print(f"  Total applications: {stats['total']:,}")
    print(f"  Defaults:           {stats['defaults']:,}")
    print(f"  Default rate:       {stats['default_rate']:.2%}")

    # ------------------------------------------------------------------
    # 4. Feature engineering
    # ------------------------------------------------------------------
    df = engineer_features(df)
    print("\nEngineered features added: AGE_YEARS, EMPLOYMENT_YEARS, "
          "CREDIT_TO_INCOME, ANNUITY_TO_INCOME")

    # ------------------------------------------------------------------
    # 5. Default rates by income type
    # ------------------------------------------------------------------
    if "NAME_INCOME_TYPE" in df.columns:
        income_rates = calculate_default_rate_by_category(df, "NAME_INCOME_TYPE")
        print("\nDefault Rates by Income Type:")
        print(income_rates.to_string(index=False))

    # ------------------------------------------------------------------
    # 6. Visualizations
    # ------------------------------------------------------------------
    numeric_cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
    existing = [c for c in numeric_cols if c in df.columns]

    if existing:
        fig = plot_distribution(df, existing[0])
        path = os.path.join(output_dir, "income_distribution.png")
        fig.savefig(path, dpi=100)
        print(f"\nSaved: {path}")

    if "NAME_INCOME_TYPE" in df.columns:
        fig = plot_default_by_income(df)
        path = os.path.join(output_dir, "default_by_income.png")
        fig.savefig(path, dpi=100)
        print(f"Saved: {path}")

    if "DAYS_BIRTH" in df.columns:
        fig = plot_age_vs_default(df)
        path = os.path.join(output_dir, "age_vs_default.png")
        fig.savefig(path, dpi=100)
        print(f"Saved: {path}")

    if len(existing) >= 2:
        fig = plot_correlation_heatmap(df, columns=existing)
        path = os.path.join(output_dir, "correlation_heatmap.png")
        fig.savefig(path, dpi=100)
        print(f"Saved: {path}")

    print("\nQuick analysis complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quick Credit EDA analysis")
    parser.add_argument(
        "--data",
        default=None,
        help="Path to application_data.csv (optional; uses synthetic data if absent)",
    )
    parser.add_argument(
        "--output",
        default="reports",
        help="Directory to save output charts (default: reports/)",
    )
    args = parser.parse_args()
    run(data_path=args.data, output_dir=args.output)
