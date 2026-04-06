from __future__ import annotations

from pathlib import Path

from src.config import (
    NUMERIC_COLUMNS_NOTEBOOK,
    CleaningConfig,
    Paths,
    default_cleaning_config,
)


class TestPaths:
    def test_paths_defaults(self):
        paths = Paths()

        assert paths.repo_root == Path(".")
        assert paths.data_raw == Path("data/raw")
        assert paths.data_processed == Path("data/processed")
        assert paths.reports == Path("reports")
        assert paths.notebooks == Path("notebooks")


class TestCleaningConfig:
    def test_default_cleaning_config_returns_config(self):
        cfg = default_cleaning_config()

        assert isinstance(cfg, CleaningConfig)

    def test_days_to_years_map_contains_expected_keys(self):
        cfg = default_cleaning_config()

        expected = {
            "DAYS_BIRTH": "AGE_CLIENT",
            "DAYS_EMPLOYED": "WORK_EX_CLIENT",
            "DAYS_REGISTRATION": "YEARS_REGISTRATION",
            "DAYS_ID_PUBLISH": "YEARS_ID_PUBLISH",
        }

        assert cfg.days_to_years_map == expected

    def test_outlier_quantile_in_valid_range(self):
        cfg = default_cleaning_config()

        assert 0 < cfg.outlier_quantile < 1

    def test_bin_lengths_match_labels(self):
        cfg = default_cleaning_config()

        assert len(cfg.income_bins) == len(cfg.income_labels) + 1
        assert len(cfg.loan_bins) == len(cfg.loan_labels) + 1


class TestNumericColumnsNotebook:
    def test_contains_expected_columns(self):
        expected_columns = {
            "TARGET",
            "AMT_INCOME_TOTAL",
            "AMT_CREDIT",
            "AMT_ANNUITY",
            "AGE_CLIENT",
            "WORK_EX_CLIENT",
        }

        assert expected_columns.issubset(set(NUMERIC_COLUMNS_NOTEBOOK))
