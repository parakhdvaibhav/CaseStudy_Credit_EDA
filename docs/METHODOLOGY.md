# Methodology — Credit EDA Pipeline

## Overview

This document describes the end-to-end analytical pipeline used to explore the Home Credit Default Risk dataset, from raw data ingestion through to insight generation.

---

## 1. Data Ingestion

**Tool:** `src/data_loader.py`

**Steps:**
1. Load `application_data.csv` and (optionally) `previous_application.csv` using `pandas.read_csv`.
2. Assert minimum shape requirements: ≥ 100 rows, ≥ 5 columns.
3. Validate that `TARGET` column exists and contains only {0, 1}.
4. Run `validate_data_quality()` to produce a structured quality report:
   - Missing value counts and percentages per column
   - Columns exceeding the 50% missing-value threshold (`DEFAULT_MISSING_THRESHOLD`)
   - Duplicate row count

**Configuration:** All paths and thresholds are managed centrally in `src/config.py`.

---

## 2. Data Cleaning

**Tool:** `src/data_loader.py → clean_data()`

| Step | Description |
|------|-------------|
| Drop high-missing columns | Remove columns where `missing_pct > DEFAULT_MISSING_THRESHOLD` (default 50%) |
| Encode `DAYS_EMPLOYED` anomaly | Replace `365243` (pensioner sentinel value) with `NaN`; add `IS_PENSIONER` flag |
| Handle negative day values | `DAYS_BIRTH`, `DAYS_EMPLOYED` are stored as negative integers — convert to positive for readability |
| Remove duplicates | Drop fully duplicate rows |

---

## 3. Exploratory Data Analysis

### 3.1 Univariate Analysis

**Tool:** `src/analysis.py → calculate_default_statistics()`

- Overall default rate calculation (`TARGET.mean()`)
- Distribution plots for all `KEY_NUMERIC_COLUMNS` (histograms + KDE)
- Frequency tables for all `KEY_CATEGORICAL_COLUMNS`
- Missing-value heatmap across all 122 columns

### 3.2 Bivariate Analysis

**Tool:** `src/analysis.py`, `src/eda_utils.py`

- **Numerical vs. Target:** Box plots and violin plots comparing defaulters vs. non-defaulters across all numeric features
- **Categorical vs. Target:** Grouped bar charts showing default rate by category
- **Key computed ratios:**
  - `CREDIT_TO_INCOME = AMT_CREDIT / AMT_INCOME_TOTAL`
  - `ANNUITY_TO_INCOME = AMT_ANNUITY / AMT_INCOME_TOTAL`
  - `INCOME_PER_PERSON = AMT_INCOME_TOTAL / CNT_FAM_MEMBERS`

### 3.3 Multivariate Analysis

**Tool:** `src/analysis.py → compute_correlation_matrix()`

- Pearson correlation matrix for all numeric features
- Flag pairs with |r| > `CORRELATION_THRESHOLD` (default 0.70) as candidates for removal
- Notable finding: `AMT_CREDIT` ↔ `AMT_GOODS_PRICE` (r ≈ 0.99)

---

## 4. Statistical Tests

| Test | Purpose | Implementation |
|------|---------|---------------|
| **Chi-squared test** | Assess association between categorical features and `TARGET` | `scipy.stats.chi2_contingency` |
| **Point-biserial correlation** | Measure correlation between continuous features and binary `TARGET` | `scipy.stats.pointbiserialr` |
| **Cramér's V** | Effect size for categorical associations | Computed from chi² statistic |

**Significance threshold:** p < 0.05.  All tests are exploratory (no multiplicity correction applied; adjustments should be made in a production model).

---

## 5. Feature Engineering

**Tool:** `src/analysis.py → engineer_features()`

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

All plot functions:
- Accept a DataFrame and return a `matplotlib.figure.Figure`
- Use project-wide style constants from `src/config.py` (`FIGURE_SIZE`, `COLOR_PALETTE`)
- Are independently testable (no global state)

| Function | Chart Type | Purpose |
|----------|-----------|---------|
| `plot_missing_values()` | Horizontal bar | Missing-value audit |
| `plot_target_distribution()` | Pie / donut | Class imbalance overview |
| `plot_numerical_distributions()` | Histogram grid | Understand spread and skew |
| `plot_default_by_income()` | Bar + error bars | Default rate by income type |
| `plot_correlation_heatmap()` | Heatmap | Feature correlation matrix |
| `plot_age_vs_default()` | Line chart | Age cohort risk profile |
| `plot_credit_to_income()` | Box plot | Credit-to-income distribution |

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
| Class imbalance (~8% default rate) | Visualisations can overstate non-default patterns | Reported separately for each class; SMOTE recommended for modelling |
| Missing data (65 cols > 30% missing) | Imputation may introduce bias | Conservative approach: dropped >50% missing; flagged >30% missing |
| No temporal validation | Patterns may shift over time | Recommend time-based train/test split in production |
