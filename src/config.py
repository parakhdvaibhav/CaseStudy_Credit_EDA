"""
Configuration parameters for the Credit EDA case study.
Centralises all paths, thresholds, and analysis settings.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")
REPORTS_PATH = os.path.join(BASE_DIR, "reports")

# Expected dataset filenames inside DATA_RAW_PATH
APPLICATION_DATA_FILE = "application_data.csv"
PREVIOUS_APPLICATION_FILE = "previous_application.csv"
COLUMNS_DESCRIPTION_FILE = "columns_description.csv"

# ---------------------------------------------------------------------------
# Data quality thresholds
# ---------------------------------------------------------------------------
MISSING_VALUE_THRESHOLD = 0.50   # Drop columns with >50% missing values
OUTLIER_IQR_MULTIPLIER = 1.5     # IQR multiplier for outlier detection

# ---------------------------------------------------------------------------
# Analysis parameters
# ---------------------------------------------------------------------------
CORRELATION_THRESHOLD = 0.70     # Minimum correlation to flag as high
TARGET_COLUMN = "TARGET"         # Binary target: 1 = payment difficulty
DAYS_COLUMNS = [                 # Negative-day columns to convert to years
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "DAYS_REGISTRATION",
    "DAYS_ID_PUBLISH",
]
LOAN_AMT_BINS = [0, 100_000, 500_000, 1_000_000, 2_000_000, float("inf")]
LOAN_AMT_LABELS = ["<1L", "1L-5L", "5L-10L", "10L-20L", ">20L"]

INCOME_BINS = [0, 100_000, 150_000, 200_000, 300_000, float("inf")]
INCOME_LABELS = ["<1L", "1L-1.5L", "1.5L-2L", "2L-3L", ">3L"]

# ---------------------------------------------------------------------------
# Visualisation defaults
# ---------------------------------------------------------------------------
FIGURE_SIZE = (12, 6)
PALETTE_DEFAULT = "Set2"
PALETTE_TARGET = {0: "#2ecc71", 1: "#e74c3c"}  # green = no default, red = default
