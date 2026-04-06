from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Paths:
    """Default project paths (relative to repo root)."""

    repo_root: Path = Path(".")
    data_raw: Path = Path("data/raw")
    data_processed: Path = Path("data/processed")
    reports: Path = Path("reports")
    notebooks: Path = Path("notebooks")


@dataclass(frozen=True)
class CleaningConfig:
    """
    Cleaning / preprocessing knobs taken from the notebook logic.
    """

    # Drop columns with >50% nulls
    high_null_threshold_pct: float = 50.0

    # Outlier trimming at 99th percentile for these numeric columns
    outlier_quantile: float = 0.99
    outlier_columns: Tuple[str, ...] = (
        "AMT_INCOME_TOTAL",
        "WORK_EX_CLIENT",
        "AMT_GOODS_PRICE",
        "CNT_CHILDREN",
        "AMT_CREDIT",
    )

    # Income and loan binning (as used in notebook)
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

    # Columns dropped in the notebook using "starts with" patterns
    drop_prefixes: Tuple[str, ...] = (
        "OBS_",
        "DEF_",
        "AMT_REQ_CREDIT",
        "EXT_",
        "DAYS_LAST_PHONE",
        "FLOORSMAX_",
        "YEARS_BEGINEXPLUATATION_",
    )

    # Columns dropped explicitly in notebook
    drop_explicit: Tuple[str, ...] = (
        # binary flags / contact flags / process time columns etc.
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
        # special-case drops from notebook list
        "TOTALAREA_MODE",
        "EMERGENCYSTATE_MODE",
    )

    # Columns that should be converted from negative days to positive years
    days_to_years_map: Dict[str, str] = None  # set in __post_init__


def default_cleaning_config() -> CleaningConfig:
    cfg = CleaningConfig(
        days_to_years_map={
            "DAYS_BIRTH": "AGE_CLIENT",
            "DAYS_EMPLOYED": "WORK_EX_CLIENT",
            "DAYS_REGISTRATION": "YEARS_REGISTRATION",
            "DAYS_ID_PUBLISH": "YEARS_ID_PUBLISH",
        }
    )
    return cfg


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