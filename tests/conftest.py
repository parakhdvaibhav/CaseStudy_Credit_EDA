"""
Pytest fixtures and shared mock data for the Credit EDA test suite.
"""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_application_df():
    """Minimal application DataFrame that mirrors the real dataset schema."""
    np.random.seed(42)
    n = 100

    data = {
        "SK_ID_CURR": range(1, n + 1),
        "TARGET": np.random.choice([0, 1], size=n, p=[0.92, 0.08]),
        "NAME_CONTRACT_TYPE": np.random.choice(
            ["Cash loans", "Revolving loans"], size=n
        ),
        "CODE_GENDER": np.random.choice(["M", "F"], size=n),
        "AMT_INCOME_TOTAL": np.random.uniform(50000, 500000, size=n),
        "AMT_CREDIT": np.random.uniform(100000, 1000000, size=n),
        "AMT_ANNUITY": np.random.uniform(5000, 50000, size=n),
        "AMT_GOODS_PRICE": np.random.uniform(90000, 900000, size=n),
        "NAME_INCOME_TYPE": np.random.choice(
            ["Working", "Commercial associate", "Pensioner", "State servant"], size=n
        ),
        "NAME_EDUCATION_TYPE": np.random.choice(
            ["Secondary / secondary special", "Higher education", "Incomplete higher"],
            size=n,
        ),
        "NAME_FAMILY_STATUS": np.random.choice(
            ["Married", "Single / not married", "Civil marriage"], size=n
        ),
        "NAME_HOUSING_TYPE": np.random.choice(
            ["House / apartment", "Rented apartment", "With parents"], size=n
        ),
        "DAYS_BIRTH": np.random.randint(-25000, -6000, size=n),
        "DAYS_EMPLOYED": np.random.randint(-10000, -100, size=n),
        "CNT_CHILDREN": np.random.randint(0, 5, size=n),
        "OCCUPATION_TYPE": np.random.choice(
            ["Laborers", "Core staff", "Managers", None], size=n
        ),
    }

    df = pd.DataFrame(data)
    return df


@pytest.fixture
def sample_df_with_missing(sample_application_df):
    """Application DataFrame with intentional missing values."""
    df = sample_application_df.copy()
    # Introduce ~30 % missing in AMT_ANNUITY and ~60 % missing in OCCUPATION_TYPE
    rng = np.random.default_rng(0)
    df.loc[rng.choice(df.index, size=30, replace=False), "AMT_ANNUITY"] = np.nan
    df.loc[rng.choice(df.index, size=60, replace=False), "OCCUPATION_TYPE"] = np.nan
    return df


@pytest.fixture
def small_numeric_df():
    """Tiny numeric DataFrame for testing correlation and statistics helpers."""
    return pd.DataFrame(
        {
            "A": [1.0, 2.0, 3.0, 4.0, 5.0],
            "B": [2.0, 4.0, 6.0, 8.0, 10.0],  # Perfect positive correlation with A
            "C": [5.0, 4.0, 3.0, 2.0, 1.0],  # Perfect negative correlation with A
            "TARGET": [0, 1, 0, 1, 0],
        }
    )


@pytest.fixture
def tmp_csv(tmp_path, sample_application_df):
    """Write sample_application_df to a temporary CSV and return its path."""
    path = tmp_path / "application_data.csv"
    sample_application_df.to_csv(path, index=False)
    return str(path)
