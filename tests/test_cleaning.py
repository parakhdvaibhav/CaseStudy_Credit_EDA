from __future__ import annotations

import numpy as np
import pandas as pd

from src.cleaning import (
    add_income_and_loan_groups,
    cast_numeric_columns,
    clean_current_application,
    convert_negative_days_to_years,
    drop_columns_by_prefix,
    drop_explicit_columns,
    drop_flag_document_columns,
    drop_high_null_columns,
    fix_gender_xna,
    trim_outliers_quantile,
)
from src.config import default_cleaning_config


def make_cleaning_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "TARGET": [0, 1, 0, 1],
            "CODE_GENDER": ["M", "XNA", "F", "M"],
            "DAYS_BIRTH": [-10000, -12000, -15000, -20000],
            "DAYS_EMPLOYED": [-1000, 365243, -3000, -4000],
            "DAYS_REGISTRATION": [-100, -200, -300, -400],
            "DAYS_ID_PUBLISH": [-10, -20, -30, -40],
            "AMT_INCOME_TOTAL": [50000, 150000, 250000, 450000],
            "AMT_CREDIT": [80000, 300000, 700000, 1400000],
            "AMT_GOODS_PRICE": [70000, 250000, 650000, 1300000],
            "AMT_ANNUITY": [5000, 10000, 15000, 20000],
            "CNT_CHILDREN": [0, 1, 2, 3],
            "CNT_FAM_MEMBERS": [1, 2, 3, 4],
            "FLAG_DOCUMENT_2": [0, 1, 0, 1],
            "OBS_30_CNT_SOCIAL_CIRCLE": [1, 2, 3, 4],
            "EXT_SOURCE_1": [0.1, 0.2, 0.3, 0.4],
            "FLAG_MOBIL": [1, 1, 1, 1],
            "UNUSED_COL": [1, np.nan, np.nan, np.nan],
        }
    )


class TestDropHighNullColumns:
    def test_drops_columns_above_threshold(self):
        df = make_cleaning_df()
        out = drop_high_null_columns(df, threshold_pct=50.0)

        assert "UNUSED_COL" not in out.columns

    def test_keeps_columns_below_threshold(self):
        df = make_cleaning_df()
        out = drop_high_null_columns(df, threshold_pct=90.0)

        assert "UNUSED_COL" in out.columns


class TestDropColumnsByPrefix:
    def test_drops_matching_prefix_columns(self):
        df = make_cleaning_df()
        out = drop_columns_by_prefix(df, prefixes=("OBS_", "EXT_"))

        assert "OBS_30_CNT_SOCIAL_CIRCLE" not in out.columns
        assert "EXT_SOURCE_1" not in out.columns


class TestDropFlagDocumentColumns:
    def test_drops_flag_document_columns(self):
        df = make_cleaning_df()
        out = drop_flag_document_columns(df)

        assert "FLAG_DOCUMENT_2" not in out.columns


class TestDropExplicitColumns:
    def test_drops_explicit_columns(self):
        df = make_cleaning_df()
        out = drop_explicit_columns(df, columns=("FLAG_MOBIL",))

        assert "FLAG_MOBIL" not in out.columns


class TestConvertNegativeDaysToYears:
    def test_converts_and_renames_column(self):
        df = make_cleaning_df()
        out = convert_negative_days_to_years(df, "DAYS_BIRTH", "AGE_CLIENT")

        assert "AGE_CLIENT" in out.columns
        assert "DAYS_BIRTH" not in out.columns
        assert (out["AGE_CLIENT"] >= 0).all()


class TestFixGenderXna:
    def test_replaces_xna_with_f(self):
        df = make_cleaning_df()
        out = fix_gender_xna(df)

        assert "XNA" not in set(out["CODE_GENDER"])
        assert "F" in set(out["CODE_GENDER"])


class TestTrimOutliersQuantile:
    def test_removes_rows_above_quantile(self):
        df = pd.DataFrame({"A": [1, 2, 3, 100]})
        out = trim_outliers_quantile(df, columns=("A",), quantile=0.75)

        assert len(out) < len(df)
        assert 100 not in set(out["A"])


class TestAddIncomeAndLoanGroups:
    def test_adds_group_columns(self):
        df = make_cleaning_df()
        cfg = default_cleaning_config()

        out = add_income_and_loan_groups(
            df,
            income_bins=cfg.income_bins,
            income_labels=cfg.income_labels,
            loan_bins=cfg.loan_bins,
            loan_labels=cfg.loan_labels,
        )

        assert "INCOME_GROUP" in out.columns
        assert "LOAN_GROUP" in out.columns

    def test_inserts_income_group_near_front(self):
        df = make_cleaning_df()
        cfg = default_cleaning_config()

        out = add_income_and_loan_groups(
            df,
            income_bins=cfg.income_bins,
            income_labels=cfg.income_labels,
            loan_bins=cfg.loan_bins,
            loan_labels=cfg.loan_labels,
        )

        assert out.columns[2] == "INCOME_GROUP"


class TestCastNumericColumns:
    def test_casts_string_columns_to_numeric(self):
        df = pd.DataFrame({"A": ["1", "2", "3"], "B": ["x", "y", "z"]})
        out = cast_numeric_columns(df, columns=("A",))

        assert pd.api.types.is_numeric_dtype(out["A"])
        assert list(out["A"]) == [1, 2, 3]


class TestCleanCurrentApplication:
    def test_returns_dataframe(self):
        df = make_cleaning_df()
        out = clean_current_application(df)

        assert isinstance(out, pd.DataFrame)

    def test_applies_expected_transformations(self):
        df = make_cleaning_df()
        out = clean_current_application(df)

        assert "AGE_CLIENT" in out.columns
        assert "WORK_EX_CLIENT" in out.columns
        assert "INCOME_GROUP" in out.columns
        assert "LOAN_GROUP" in out.columns
        assert "FLAG_DOCUMENT_2" not in out.columns
        assert "FLAG_MOBIL" not in out.columns
        assert "OBS_30_CNT_SOCIAL_CIRCLE" not in out.columns
        assert "EXT_SOURCE_1" not in out.columns

    def test_fixes_gender_values(self):
        df = make_cleaning_df()
        out = clean_current_application(df)

        if "CODE_GENDER" in out.columns:
            assert "XNA" not in set(out["CODE_GENDER"])

    def test_does_not_mutate_original(self):
        df = make_cleaning_df()
        original = df.copy(deep=True)

        clean_current_application(df)

        pd.testing.assert_frame_equal(df, original)
