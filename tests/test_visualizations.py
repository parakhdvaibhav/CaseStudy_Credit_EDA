"""
Unit tests for src/visualizations.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from src.visualizations import (
    plot_age_vs_default,
    plot_correlation_heatmap,
    plot_default_analysis,
    plot_default_by_income,
    plot_distribution,
)

# ---------------------------------------------------------------------------
# plot_distribution
# ---------------------------------------------------------------------------


class TestPlotDistribution:
    def test_returns_figure(self, sample_application_df):
        fig = plot_distribution(sample_application_df, "AMT_INCOME_TOTAL")
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_sets_default_title(self, sample_application_df):
        fig = plot_distribution(sample_application_df, "AMT_INCOME_TOTAL")
        ax = fig.axes[0]
        assert "AMT_INCOME_TOTAL" in ax.get_title()
        plt.close("all")

    def test_custom_title(self, sample_application_df):
        fig = plot_distribution(
            sample_application_df, "AMT_INCOME_TOTAL", title="My Title"
        )
        ax = fig.axes[0]
        assert ax.get_title() == "My Title"
        plt.close("all")

    def test_raises_for_missing_column(self, sample_application_df):
        with pytest.raises(ValueError, match="not found"):
            plot_distribution(sample_application_df, "NONEXISTENT_COL")

    def test_handles_column_with_missing_values(self, sample_df_with_missing):
        # Should not raise even though AMT_ANNUITY has NaN values
        fig = plot_distribution(sample_df_with_missing, "AMT_ANNUITY")
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_axis_labels(self, sample_application_df):
        fig = plot_distribution(sample_application_df, "AMT_CREDIT")
        ax = fig.axes[0]
        assert ax.get_xlabel() == "AMT_CREDIT"
        assert ax.get_ylabel() == "Count"
        plt.close("all")


# ---------------------------------------------------------------------------
# plot_default_analysis
# ---------------------------------------------------------------------------


class TestPlotDefaultAnalysis:
    def test_returns_figure(self, sample_application_df):
        fig = plot_default_analysis(sample_application_df, "NAME_CONTRACT_TYPE")
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_raises_without_target(self, sample_application_df):
        df = sample_application_df.drop(columns=["TARGET"])
        with pytest.raises(ValueError, match="TARGET"):
            plot_default_analysis(df, "NAME_CONTRACT_TYPE")

    def test_raises_for_missing_feature(self, sample_application_df):
        with pytest.raises(ValueError, match="not found"):
            plot_default_analysis(sample_application_df, "MISSING_FEATURE")

    def test_title_contains_feature(self, sample_application_df):
        fig = plot_default_analysis(sample_application_df, "CODE_GENDER")
        ax = fig.axes[0]
        assert "CODE_GENDER" in ax.get_title()
        plt.close("all")

    def test_custom_title(self, sample_application_df):
        fig = plot_default_analysis(
            sample_application_df, "CODE_GENDER", title="Gender Plot"
        )
        ax = fig.axes[0]
        assert ax.get_title() == "Gender Plot"
        plt.close("all")


# ---------------------------------------------------------------------------
# plot_correlation_heatmap
# ---------------------------------------------------------------------------


class TestPlotCorrelationHeatmap:
    def test_returns_figure(self, small_numeric_df):
        fig = plot_correlation_heatmap(small_numeric_df)
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_custom_title(self, small_numeric_df):
        fig = plot_correlation_heatmap(small_numeric_df, title="My Heatmap")
        ax = fig.axes[0]
        assert ax.get_title() == "My Heatmap"
        plt.close("all")

    def test_raises_for_no_numeric_columns(self):
        df = pd.DataFrame({"A": ["x", "y"], "B": ["p", "q"]})
        with pytest.raises(ValueError, match="numeric"):
            plot_correlation_heatmap(df)

    def test_column_subset(self, sample_application_df):
        cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
        fig = plot_correlation_heatmap(sample_application_df, columns=cols)
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_handles_sample_data(self, sample_application_df):
        numeric_cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "DAYS_BIRTH"]
        fig = plot_correlation_heatmap(sample_application_df, columns=numeric_cols)
        assert isinstance(fig, plt.Figure)
        plt.close("all")


# ---------------------------------------------------------------------------
# plot_default_by_income
# ---------------------------------------------------------------------------


class TestPlotDefaultByIncome:
    def test_returns_figure(self, sample_application_df):
        fig = plot_default_by_income(sample_application_df)
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_raises_without_target(self, sample_application_df):
        df = sample_application_df.drop(columns=["TARGET"])
        with pytest.raises(ValueError, match="TARGET"):
            plot_default_by_income(df)

    def test_raises_for_missing_income_column(self, sample_application_df):
        with pytest.raises(ValueError, match="not found"):
            plot_default_by_income(sample_application_df, income_column="NO_SUCH_COL")

    def test_title_is_set(self, sample_application_df):
        fig = plot_default_by_income(sample_application_df, title="Income Default Plot")
        ax = fig.axes[0]
        assert ax.get_title() == "Income Default Plot"
        plt.close("all")


# ---------------------------------------------------------------------------
# plot_age_vs_default
# ---------------------------------------------------------------------------


class TestPlotAgeVsDefault:
    def test_returns_figure(self, sample_application_df):
        fig = plot_age_vs_default(sample_application_df)
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_raises_without_target(self, sample_application_df):
        df = sample_application_df.drop(columns=["TARGET"])
        with pytest.raises(ValueError, match="TARGET"):
            plot_age_vs_default(df)

    def test_raises_for_missing_age_column(self, sample_application_df):
        with pytest.raises(ValueError, match="not found"):
            plot_age_vs_default(sample_application_df, age_column="NO_AGE_COL")

    def test_works_with_positive_age_years(self, sample_application_df):
        df = sample_application_df.copy()
        df["AGE_YEARS"] = (-df["DAYS_BIRTH"] / 365).round(1)
        fig = plot_age_vs_default(df, age_column="AGE_YEARS")
        assert isinstance(fig, plt.Figure)
        plt.close("all")
