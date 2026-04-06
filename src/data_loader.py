from __future__ import annotations

from pathlib import Path
from typing import Tuple, Union

import pandas as pd


PathLike = Union[str, Path]


def load_csv(path: PathLike) -> pd.DataFrame:
    """
    Load a CSV into a DataFrame.

    This is intentionally tiny so it is easy to test/mocks cleanly.
    """
    return pd.read_csv(Path(path))


def load_credit_datasets(
    application_csv: PathLike,
    previous_application_csv: PathLike,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load current application and previous application datasets.

    Notebook expects:
      - application_data.csv
      - previous_application.csv
    """
    curr = load_csv(application_csv)
    prev = load_csv(previous_application_csv)
    return curr, prev


def validate_required_columns(df: pd.DataFrame, required: Tuple[str, ...]) -> None:
    """
    Raise ValueError if any required columns are missing.
    """
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")