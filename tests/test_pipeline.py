from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.pipeline import run_full_eda


def make_pipeline_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "SK_ID_CURR": [1, 2, 3, 4, 5, 6],
            "TARGET": [0, 1, 0, 1, 0, 0],
            "AMT_INCOME_TOTAL": [50000, 100000, 150000, 200000, 250000, 300000],
            "AMT_CREDIT": [80000, 120000, 180000, 220000, 260000, 310000],
            "AMT_ANNUITY": [5000, 6000, 7000, 8000, 9000, 10000],
            "AMT_GOODS_PRICE": [75000, 115000, 170000, 210000, 255000, 305000],
            "DAYS_BIRTH": [-10000, -12000, -15000, -20000, -18000, -16000],
            "DAYS_EMPLOYED": [-1000, -2000, -1500, -3000, -2500, -2200],
            "NAME_INCOME_TYPE": [
                "Working",
                "Pensioner",
                "Working",
                "State servant",
                "Commercial associate",
                "Working",
            ],
            "CODE_GENDER": ["M", "F", "F", "M", "F", "M"],
        }
    )


class TestRunFullEda:
    def test_returns_expected_keys(self, tmp_path):
        df = make_pipeline_df()
        csv_path = tmp_path / "application_data.csv"
        df.to_csv(csv_path, index=False)

        result = run_full_eda(str(csv_path), output_dir=str(tmp_path / "reports"))

        assert isinstance(result, dict)
        assert "shape" in result
        assert "quality_report" in result
        assert "default_statistics" in result
        assert "income_rates" in result
        assert "saved_files" in result

    def test_creates_output_files(self, tmp_path):
        df = make_pipeline_df()
        csv_path = tmp_path / "application_data.csv"
        output_dir = tmp_path / "reports"
        df.to_csv(csv_path, index=False)

        result = run_full_eda(str(csv_path), output_dir=str(output_dir))

        assert output_dir.exists()
        assert len(result["saved_files"]) >= 1

        for file_path in result["saved_files"]:
            assert Path(file_path).exists()

    def test_returns_correct_shape(self, tmp_path):
        df = make_pipeline_df()
        csv_path = tmp_path / "application_data.csv"
        df.to_csv(csv_path, index=False)

        result = run_full_eda(str(csv_path), output_dir=str(tmp_path / "reports"))

        assert result["shape"][0] == len(df)
        assert result["shape"][1] >= len(df.columns)

    def test_default_statistics_contains_expected_values(self, tmp_path):
        df = make_pipeline_df()
        csv_path = tmp_path / "application_data.csv"
        df.to_csv(csv_path, index=False)

        result = run_full_eda(str(csv_path), output_dir=str(tmp_path / "reports"))
        stats = result["default_statistics"]

        assert stats["total"] == len(df)
        assert stats["defaults"] == 2
        assert 0 <= stats["default_rate"] <= 1
