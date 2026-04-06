# Methodology — Credit EDA Pipeline

## Overview

This document describes the end-to-end analytical pipeline used to explore the Home Credit Default Risk dataset, from raw data ingestion through insight generation. The pipeline is modular, reproducible, and implemented using reusable utilities in the `src/` directory.

---

## Pipeline Flow

The overall pipeline follows this sequence:

1. Data Ingestion (`data_loader.py`)
2. Data Cleaning (`cleaning.py`)
3. Exploratory Analysis (`analysis.py`)
4. Visualization (`visualizations.py`)
5. Feature Engineering (`analysis.py`)
6. Insight Generation (Notebooks + Reports)

This modular design improves maintainability, testing, and reproducibility.

---

## 1. Data Ingestion

**Tool:** `src/data_loader.py`

**Steps:**
1. Load `application_data.csv` using `pandas.read_csv`
2. Validate dataset structure and required columns
3. Validate that `TARGET` column exists and contains only {0, 1}
4. Run `validate_data_quality()` to produce a structured quality report:
   - Missing value counts and percentages per column
   - Columns exceeding the missing-value threshold
   - Duplicate row count
   - Basic dataset shape and column metadata

**Configuration:** Paths and thresholds are managed in `src/config.py`.

---

## 2. Data Cleaning

Cleaning operations are designed to be idempotent and reusable across analysis workflows.

**Tool:** `src/cleaning.py`

| Step | Description |
|------|-------------|
| Drop high-missing columns | Remove columns exceeding configured missing threshold |
| Handle sentinel values | Replace anomalous values such as `365243` in `DAYS_EMPLOYED` |
| Convert day-based variables | Convert negative day values to human-readable units |
| Remove duplicates | Drop duplicate records |
| Standardize numeric features | Handle invalid or extreme values |

---

## 3. Exploratory Data Analysis

### 3.1 Univariate Analysis

**Tool:** `src/analysis.py`

- Overall default rate calculation (`TARGET.mean()`)
- Distribution plots for numeric variables
- Frequency tables for categorical variables
- Missing value analysis

### 3.2 Bivariate Analysis

**Tool:** `src/analysis.py`, `src/visualizations.py`

- Numerical vs Target analysis
- Categorical vs Target analysis
- Default rate by key demographic and financial features

Key engineered ratios:

- `CREDIT_TO_INCOME`
- `ANNUITY_TO_INCOME`
- `INCOME_PER_PERSON`

### 3.3 Multivariate Analysis

**Tool:** `src/analysis.py`

- Correlation matrix for numeric features
- Identification of multicollinearity
- Feature grouping and redundancy detection

### 4. Exploratory Statistical Analysis

| Test | Purpose | Implementation |
|------|---------|---------------|
| **Chi-squared test** | Assess association between categorical features and `TARGET` | `scipy.stats.chi2_contingency` |
| **Point-biserial correlation** | Measure correlation between continuous features and binary `TARGET` | `scipy.stats.pointbiserialr` |
| **Cramér's V** | Effect size for categorical associations | Computed from chi² statistic |

**Significance threshold:** p < 0.05.  All tests are exploratory (no multiplicity correction applied; adjustments should be made in a production model).

---

## 5. Feature Engineering

**Tool:** `src/analysis.py`

| Feature | Formula | Rationale |
|---------|---------|-----------|
| `CREDIT_TO_INCOME` | `AMT_CREDIT / AMT_INCOME_TOTAL` | Debt burden relative to income |
| `ANNUITY_TO_INCOME` | `AMT_ANNUITY / AMT_INCOME_TOTAL` | Monthly payment affordability |
| `INCOME_PER_PERSON` | `AMT_INCOME_TOTAL / CNT_FAM_MEMBERS` | Per-capita income |
| `AGE_YEARS` | `abs(DAYS_BIRTH) / 365` | Human-readable age |
| `EMPLOYMENT_YEARS` | `abs(DAYS_EMPLOYED) / 365` | Employment tenure |

Division-by-zero is handled: `CNT_FAM_MEMBERS` defaults to 1 where zero or missing.

---

## 6. Visualization Pipeline

**Tool:** `src/visualizations.py`

Visualization utilities generate:

- Distribution plots
- Target distribution plots
- Default rate by demographic variables
- Correlation heatmap
- Age vs default plots
- Credit-to-income visualizations

Plots are generated using matplotlib and seaborn and saved to `reports/`.

---

## 7. Notebook Structure

The analysis is split into three focused notebooks to separate concerns:

| Notebook | Focus | Key Outputs |
|----------|-------|------------|
| `01_data_exploration.ipynb` | Data loading, shape inspection, missing values | Quality report, missing-value heatmap |
| `02_detailed_analysis.ipynb` | Bivariate & multivariate analysis, statistical tests | Correlation matrix, default-rate charts |
| `03_insights_recommendations.ipynb` | Feature engineering, summary findings, business recommendations | Engineered features, FINDINGS summary |

---

## 8. Reproducibility

All analysis steps are reproducible by:

1. Installing exact dependencies: `pip install -r requirements.txt`
2. Placing raw data in `data/raw/`
3. Running `python examples/quick_analysis.py` for a synthetic demonstration
4. Running notebooks in order: 01 → 02 → 03
5. Running `pytest tests/ -v --cov=src` to validate all utility functions

Random seeds are not required because this pipeline contains no stochastic operations.

---

## 9. Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| EDA only; no predictive model built | Cannot quantify feature importance precisely | Use findings to design features for ML model |
| Class imbalance (~8% default rate) | Visualizations can overstate non-default patterns | Reported separately for each class; SMOTE recommended for modeling |
| Missing data (65 cols > 30% missing) | Imputation may introduce bias | Conservative approach: dropped >50% missing; flagged >30% missing |
| No temporal validation | Patterns may shift over time | Recommend time-based train/test split in production 