"""
Configuration parameters for the Credit EDA project.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")
REPORTS_PATH = os.path.join(BASE_DIR, "reports")
NOTEBOOKS_PATH = os.path.join(BASE_DIR, "notebooks")

# Common file names
APPLICATION_DATA_FILE = "application_data.csv"
PREVIOUS_APPLICATION_FILE = "previous_application.csv"
COLUMNS_DESCRIPTION_FILE = "columns_description.csv"

# ---------------------------------------------------------------------------
# Analysis parameters
# ---------------------------------------------------------------------------
DEFAULT_MISSING_THRESHOLD = 0.50  # Drop columns with >50% missing values
CORRELATION_THRESHOLD = 0.70  # Flag highly-correlated feature pairs
TARGET_COLUMN = "TARGET"

# Loan default label mapping
TARGET_LABELS = {0: "No Default", 1: "Default"}

# Numeric columns used in EDA
KEY_NUMERIC_COLUMNS = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "CNT_CHILDREN",
]

# Categorical columns used in EDA
KEY_CATEGORICAL_COLUMNS = [
    "NAME_CONTRACT_TYPE",
    "CODE_GENDER",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE",
]

# ---------------------------------------------------------------------------
# Visualization parameters
# ---------------------------------------------------------------------------
FIGURE_SIZE = (12, 6)
HEATMAP_FIGURE_SIZE = (14, 10)
COLOR_PALETTE = "Set2"
DEFAULT_COLOR = "#e74c3c"
NON_DEFAULT_COLOR = "#2ecc71"
