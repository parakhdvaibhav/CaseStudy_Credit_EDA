"""
Unit tests for src/data_loader.py
"""

import os

import numpy as np
import pandas as pd
import pytest

from src.data_loader import (
    drop_high_missing_columns,
    get_missing_summary,
    load_application_data,
    load_previous_application,
    validate_data_quality,
)


# ---------------------------------------------------------------------------
# load_application_data
# ---------------------------------------------------------------------------


class TestLoadApplicationData:
    def test_loads_valid_csv(self, tmp_csv, sample_application_df):
        df = load_application_data(tmp_csv)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_application_df)

    def test_raises_for_missing_file(self, tmp_path):
        missing = str(tmp_path / "nonexistent.csv")
        with pytest.raises(FileNotFoundError):
            load_application_data(missing)

    def test_raises_for_empty_file(self, tmp_path):
        empty_csv = tmp_path / "empty.csv"
        # Write header-only CSV → pandas reads 0 rows
        empty_csv.write_text("SK_ID_CURR,TARGET\n")
        with pytest.raises(ValueError, match="empty"):
            load_application_data(str(empty_csv))

    def test_returns_dataframe(self, tmp_csv):
        df = load_application_data(tmp_csv)
        assert isinstance(df, pd.DataFrame)

    def test_columns_are_preserved(self, tmp_csv, sample_application_df):
        df = load_application_data(tmp_csv)
        assert set(sample_application_df.columns) == set(df.columns)


# ---------------------------------------------------------------------------
# load_previous_application
# ---------------------------------------------------------------------------


class TestLoadPreviousApplication:
    def test_loads_valid_csv(self, tmp_path):
        data = pd.DataFrame(
            {
                "SK_ID_PREV": [1, 2, 3],
                "SK_ID_CURR": [10, 11, 12],
                "AMT_CREDIT": [100000, 200000, 300000],
            }
        )
        path = tmp_path / "previous_application.csv"
        data.to_csv(path, index=False)
        df = load_previous_application(str(path))
        assert len(df) == 3

    def test_raises_for_missing_file(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_previous_application(str(tmp_path / "no_file.csv"))


# ---------------------------------------------------------------------------
# validate_data_quality
# ---------------------------------------------------------------------------


class TestValidateDataQuality:
    def test_returns_dict(self, sample_application_df):
        report = validate_data_quality(sample_application_df)
        assert isinstance(report, dict)

    def test_report_keys(self, sample_application_df):
        report = validate_data_quality(sample_application_df)
        expected_keys = {
            "shape",
            "missing_counts",
            "missing_percentages",
            "high_missing_columns",
            "duplicate_rows",
            "dtypes",
            "has_target",
        }
        assert expected_keys.issubset(report.keys())

    def test_detects_target_column(self, sample_application_df):
        report = validate_data_quality(sample_application_df)
        assert report["has_target"] is True

    def test_missing_target_column(self, sample_application_df):
        df_no_target = sample_application_df.drop(columns=["TARGET"])
        report = validate_data_quality(df_no_target)
        assert report["has_target"] is False

    def test_detects_high_missing_columns(self, sample_df_with_missing):
        report = validate_data_quality(sample_df_with_missing)
        # OCCUPATION_TYPE has ~60 % missing so should appear in high_missing
        assert "OCCUPATION_TYPE" in report["high_missing_columns"]

    def test_shape_is_correct(self, sample_application_df):
        report = validate_data_quality(sample_application_df)
        assert report["shape"] == sample_application_df.shape

    def test_no_duplicates_in_clean_data(self, sample_application_df):
        report = validate_data_quality(sample_application_df)
        assert report["duplicate_rows"] == 0


# ---------------------------------------------------------------------------
# get_missing_summary
# ---------------------------------------------------------------------------


class TestGetMissingSummary:
    def test_returns_dataframe(self, sample_df_with_missing):
        summary = get_missing_summary(sample_df_with_missing)
        assert isinstance(summary, pd.DataFrame)

    def test_only_includes_missing_columns(self, sample_application_df):
        # The fixture has no NaN in most columns (except OCCUPATION_TYPE which
        # may already have some None values from the choice list)
        df = sample_application_df.copy()
        df["ALL_PRESENT"] = 1
        summary = get_missing_summary(df)
        assert "ALL_PRESENT" not in summary.index

    def test_sorted_descending(self, sample_df_with_missing):
        summary = get_missing_summary(sample_df_with_missing)
        pcts = summary["missing_percentage"].tolist()
        assert pcts == sorted(pcts, reverse=True)

    def test_columns_present(self, sample_df_with_missing):
        summary = get_missing_summary(sample_df_with_missing)
        assert "missing_count" in summary.columns
        assert "missing_percentage" in summary.columns


# ---------------------------------------------------------------------------
# drop_high_missing_columns
# ---------------------------------------------------------------------------


class TestDropHighMissingColumns:
    def test_drops_columns_above_threshold(self, sample_df_with_missing):
        # OCCUPATION_TYPE has ~60 % missing → should be dropped at 50 % threshold
        result = drop_high_missing_columns(sample_df_with_missing, threshold=0.50)
        assert "OCCUPATION_TYPE" not in result.columns

    def test_keeps_columns_below_threshold(self, sample_df_with_missing):
        result = drop_high_missing_columns(sample_df_with_missing, threshold=0.50)
        # AMT_ANNUITY has ~30 % missing → should be kept
        assert "AMT_ANNUITY" in result.columns

    def test_returns_dataframe(self, sample_application_df):
        result = drop_high_missing_columns(sample_application_df)
        assert isinstance(result, pd.DataFrame)

    def test_no_columns_dropped_when_none_exceed_threshold(self, sample_application_df):
        original_cols = set(sample_application_df.columns)
        result = drop_high_missing_columns(sample_application_df, threshold=1.0)
        assert set(result.columns) == original_cols
