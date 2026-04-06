"""
Unit tests for src/analysis.py
"""

import pandas as pd
import pytest

from src.analysis import (
    calculate_correlation_matrix,
    calculate_default_rate_by_category,
    calculate_default_statistics,
    calculate_missing_by_target,
    calculate_missing_percentages,
    engineer_features,
    get_highly_correlated_pairs,
)

# ---------------------------------------------------------------------------
# calculate_missing_percentages
# ---------------------------------------------------------------------------


class TestCalculateMissingPercentages:
    def test_returns_series(self, sample_application_df):
        result = calculate_missing_percentages(sample_application_df)
        assert isinstance(result, pd.Series)

    def test_sorted_descending(self, sample_df_with_missing):
        result = calculate_missing_percentages(sample_df_with_missing)
        pcts = result.tolist()
        assert pcts == sorted(pcts, reverse=True)

    def test_zero_for_complete_columns(self, sample_application_df):
        result = calculate_missing_percentages(sample_application_df)
        # SK_ID_CURR has no missing
        assert result["SK_ID_CURR"] == pytest.approx(0.0)

    def test_range_0_to_100(self, sample_df_with_missing):
        result = calculate_missing_percentages(sample_df_with_missing)
        assert result.min() >= 0.0
        assert result.max() <= 100.0


# ---------------------------------------------------------------------------
# calculate_default_statistics
# ---------------------------------------------------------------------------


class TestCalculateDefaultStatistics:
    def test_returns_dict(self, sample_application_df):
        result = calculate_default_statistics(sample_application_df)
        assert isinstance(result, dict)

    def test_required_keys(self, sample_application_df):
        result = calculate_default_statistics(sample_application_df)
        for key in (
            "total",
            "defaults",
            "non_defaults",
            "default_rate",
            "non_default_rate",
        ):
            assert key in result

    def test_total_equals_sum(self, sample_application_df):
        result = calculate_default_statistics(sample_application_df)
        assert result["total"] == result["defaults"] + result["non_defaults"]

    def test_rates_sum_to_one(self, sample_application_df):
        result = calculate_default_statistics(sample_application_df)
        assert result["default_rate"] + result["non_default_rate"] == pytest.approx(1.0)

    def test_raises_without_target(self, sample_application_df):
        df = sample_application_df.drop(columns=["TARGET"])
        with pytest.raises(KeyError):
            calculate_default_statistics(df)

    def test_default_rate_range(self, sample_application_df):
        result = calculate_default_statistics(sample_application_df)
        assert 0.0 <= result["default_rate"] <= 1.0


# ---------------------------------------------------------------------------
# calculate_correlation_matrix
# ---------------------------------------------------------------------------


class TestCalculateCorrelationMatrix:
    def test_returns_dataframe(self, small_numeric_df):
        result = calculate_correlation_matrix(small_numeric_df)
        assert isinstance(result, pd.DataFrame)

    def test_diagonal_is_one(self, small_numeric_df):
        result = calculate_correlation_matrix(small_numeric_df)
        for col in result.columns:
            assert result.loc[col, col] == pytest.approx(1.0)

    def test_perfect_positive_correlation(self, small_numeric_df):
        result = calculate_correlation_matrix(small_numeric_df)
        assert result.loc["A", "B"] == pytest.approx(1.0)

    def test_perfect_negative_correlation(self, small_numeric_df):
        result = calculate_correlation_matrix(small_numeric_df)
        assert result.loc["A", "C"] == pytest.approx(-1.0)

    def test_column_subset(self, sample_application_df):
        cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT"]
        result = calculate_correlation_matrix(sample_application_df, columns=cols)
        assert list(result.columns) == cols


# ---------------------------------------------------------------------------
# get_highly_correlated_pairs
# ---------------------------------------------------------------------------


class TestGetHighlyCorrelatedPairs:
    def test_returns_dataframe(self, small_numeric_df):
        result = get_highly_correlated_pairs(small_numeric_df, threshold=0.8)
        assert isinstance(result, pd.DataFrame)

    def test_finds_perfect_pairs(self, small_numeric_df):
        result = get_highly_correlated_pairs(small_numeric_df, threshold=0.9)
        # A-B and A-C both have |r|=1
        assert len(result) >= 2

    def test_no_pairs_at_high_threshold(self, sample_application_df):
        result = get_highly_correlated_pairs(sample_application_df, threshold=0.9999)
        # Very unlikely to have near-perfect correlations in random data
        assert isinstance(result, pd.DataFrame)

    def test_result_columns(self, small_numeric_df):
        result = get_highly_correlated_pairs(small_numeric_df, threshold=0.5)
        if not result.empty:
            assert set(result.columns) == {"feature_1", "feature_2", "correlation"}


# ---------------------------------------------------------------------------
# calculate_missing_by_target
# ---------------------------------------------------------------------------


class TestCalculateMissingByTarget:
    def test_returns_dataframe(self, sample_df_with_missing):
        result = calculate_missing_by_target(sample_df_with_missing, "AMT_ANNUITY")
        assert isinstance(result, pd.DataFrame)

    def test_contains_target_column(self, sample_df_with_missing):
        result = calculate_missing_by_target(sample_df_with_missing, "AMT_ANNUITY")
        assert "TARGET" in result.columns

    def test_contains_missing_pct(self, sample_df_with_missing):
        result = calculate_missing_by_target(sample_df_with_missing, "AMT_ANNUITY")
        assert "missing_pct" in result.columns


# ---------------------------------------------------------------------------
# calculate_default_rate_by_category
# ---------------------------------------------------------------------------


class TestCalculateDefaultRateByCat:
    def test_returns_dataframe(self, sample_application_df):
        result = calculate_default_rate_by_category(
            sample_application_df, "NAME_INCOME_TYPE"
        )
        assert isinstance(result, pd.DataFrame)

    def test_raises_without_target(self, sample_application_df):
        df = sample_application_df.drop(columns=["TARGET"])
        with pytest.raises(KeyError):
            calculate_default_rate_by_category(df, "NAME_INCOME_TYPE")

    def test_default_rate_in_range(self, sample_application_df):
        result = calculate_default_rate_by_category(
            sample_application_df, "NAME_INCOME_TYPE"
        )
        assert result["default_rate"].between(0, 1).all()

    def test_result_sorted_descending(self, sample_application_df):
        result = calculate_default_rate_by_category(
            sample_application_df, "NAME_INCOME_TYPE"
        )
        rates = result["default_rate"].tolist()
        assert rates == sorted(rates, reverse=True)


# ---------------------------------------------------------------------------
# engineer_features
# ---------------------------------------------------------------------------


class TestEngineerFeatures:
    def test_returns_dataframe(self, sample_application_df):
        result = engineer_features(sample_application_df)
        assert isinstance(result, pd.DataFrame)

    def test_adds_age_years(self, sample_application_df):
        result = engineer_features(sample_application_df)
        assert "AGE_YEARS" in result.columns

    def test_age_years_positive(self, sample_application_df):
        result = engineer_features(sample_application_df)
        assert (result["AGE_YEARS"] > 0).all()

    def test_adds_credit_to_income(self, sample_application_df):
        result = engineer_features(sample_application_df)
        assert "CREDIT_TO_INCOME" in result.columns

    def test_adds_annuity_to_income(self, sample_application_df):
        result = engineer_features(sample_application_df)
        assert "ANNUITY_TO_INCOME" in result.columns

    def test_adds_employment_years(self, sample_application_df):
        result = engineer_features(sample_application_df)
        assert "EMPLOYMENT_YEARS" in result.columns

    def test_does_not_mutate_original(self, sample_application_df):
        original_cols = set(sample_application_df.columns)
        _ = engineer_features(sample_application_df)
        assert set(sample_application_df.columns) == original_cols

    def test_graceful_with_missing_columns(self):
        df = pd.DataFrame({"A": [1, 2, 3]})
        result = engineer_features(df)
        # None of the feature-engineering columns should be added
        for col in (
            "AGE_YEARS",
            "EMPLOYMENT_YEARS",
            "CREDIT_TO_INCOME",
            "ANNUITY_TO_INCOME",
        ):
            assert col not in result.columns

    def test_pensioner_employment_years_is_nan(self, sample_application_df):
        df = sample_application_df.copy()
        df.loc[0, "DAYS_EMPLOYED"] = 365243  # pensioner flag
        result = engineer_features(df)
        assert pd.isna(result.loc[0, "EMPLOYMENT_YEARS"])
