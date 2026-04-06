from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple


@dataclass(frozen=True)
class Paths:
    """Default project paths relative to the repository root."""

    repo_root: Path = Path(".")
    data_raw: Path = Path("data/raw")
    data_processed: Path = Path("data/processed")
    reports: Path = Path("reports")
    notebooks: Path = Path("notebooks")


@dataclass(frozen=True)
class CleaningConfig:
    """
    Configuration for the credit EDA cleaning and preprocessing pipeline.

    This includes:
    - missing-value thresholds
    - outlier filtering settings
    - feature binning definitions
    - column drop rules
    - day-to-year conversion mappings
    """

    high_null_threshold_pct: float = 50.0

    outlier_quantile: float = 0.99
    outlier_columns: Tuple[str, ...] = (
        "AMT_INCOME_TOTAL",
        "WORK_EX_CLIENT",
        "AMT_GOODS_PRICE",
        "CNT_CHILDREN",
        "AMT_CREDIT",
    )

    income_bins: Tuple[int, ...] = (0, 100000, 200000, 300000, 400000, 500000)
    income_labels: Tuple[str, ...] = (
        "0-100000",
        "100000-200000",
        "200000-300000",
        "300000-400000",
        "400000-500000",
    )

    loan_bins: Tuple[int, ...] = (0, 100000, 500000, 1000000, 1500000, 2000000)
    loan_labels: Tuple[str, ...] = (
        "0-100000",
        "100000-500000",
        "500000-1000000",
        "1000000-1500000",
        "1500000-2000000",
    )

    drop_prefixes: Tuple[str, ...] = (
        "OBS_",
        "DEF_",
        "AMT_REQ_CREDIT",
        "EXT_",
        "DAYS_LAST_PHONE",
        "FLOORSMAX_",
        "YEARS_BEGINEXPLUATATION_",
    )

    drop_explicit: Tuple[str, ...] = (
        "FLAG_MOBIL",
        "FLAG_EMP_PHONE",
        "FLAG_WORK_PHONE",
        "FLAG_CONT_MOBILE",
        "FLAG_PHONE",
        "FLAG_EMAIL",
        "WEEKDAY_APPR_PROCESS_START",
        "HOUR_APPR_PROCESS_START",
        "REG_REGION_NOT_LIVE_REGION",
        "REG_REGION_NOT_WORK_REGION",
        "LIVE_REGION_NOT_WORK_REGION",
        "REG_CITY_NOT_LIVE_CITY",
        "REG_CITY_NOT_WORK_CITY",
        "LIVE_CITY_NOT_WORK_CITY",
        "TOTALAREA_MODE",
        "EMERGENCYSTATE_MODE",
    )

    days_to_years_map: dict[str, str] = field(
        default_factory=lambda: {
            "DAYS_BIRTH": "AGE_CLIENT",
            "DAYS_EMPLOYED": "WORK_EX_CLIENT",
            "DAYS_REGISTRATION": "YEARS_REGISTRATION",
            "DAYS_ID_PUBLISH": "YEARS_ID_PUBLISH",
        }
    )


def default_cleaning_config() -> CleaningConfig:
    """Return the default cleaning configuration for the project."""
    return CleaningConfig()


NUMERIC_COLUMNS_NOTEBOOK: List[str] = [
    "TARGET",
    "CNT_CHILDREN",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "REGION_POPULATION_RELATIVE",
    "AGE_CLIENT",
    "WORK_EX_CLIENT",
    "YEARS_REGISTRATION",
    "YEARS_ID_PUBLISH",
    "CNT_FAM_MEMBERS",
    "REGION_RATING_CLIENT",
    "REGION_RATING_CLIENT_W_CITY",
]