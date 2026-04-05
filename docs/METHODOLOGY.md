# Analysis Methodology — Credit EDA Case Study

## 1. Problem Statement

A consumer finance company needs to identify customers who are likely to default on their loan repayments. The goal is to use Exploratory Data Analysis (EDA) to surface patterns that differentiate:

- **TARGET = 0**: Clients with no payment difficulties
- **TARGET = 1**: Clients with payment difficulties (late payment > X days on at least one of the first Y instalments)

Getting this classification right has two-sided risk:
- Rejecting a creditworthy applicant → lost business
- Approving a likely defaulter → financial loss

---

## 2. Datasets

| Dataset | File | Rows (approx.) | Description |
|---------|------|----------------|-------------|
| Current Applications | `application_data.csv` | ~307,000 | Loan applications with TARGET label |
| Previous Applications | `previous_application.csv` | ~1.67M | Historical loan records per client |

Both datasets are sourced from the [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk) Kaggle competition.

---

## 3. Analysis Pipeline

### Step 1 — Data Loading & Quality Assessment
- Load both CSVs into Pandas DataFrames.
- Inspect shape, data types, duplicate rows.
- Compute per-column missing-value ratios.

### Step 2 — Data Cleaning
- **Drop high-missing columns**: Any column with >50% missing values is removed.
- **Imputation**: Remaining numerical nulls are left for downstream handling in modelling (not imputed in EDA).
- **Day conversion**: Negative-day columns (`DAYS_BIRTH`, `DAYS_EMPLOYED`, `DAYS_REGISTRATION`, `DAYS_ID_PUBLISH`) are converted to positive years to improve readability.
- **Outlier treatment**: IQR-based winsorisation applied to skewed numerical features that would otherwise dominate visualisations.

### Step 3 — Exploratory Analysis

#### 3.1 Target Variable Distribution
- Bar chart of TARGET counts.
- Class imbalance noted: ~92% TARGET=0 vs ~8% TARGET=1.
- Datasets split into `target_0` and `target_1` sub-frames for comparison.

#### 3.2 Univariate Analysis — Categorical
For each key categorical feature, side-by-side count plots are produced separately for TARGET=0 and TARGET=1.

Key features analysed:
- `NAME_CONTRACT_TYPE`, `CODE_GENDER`, `NAME_INCOME_TYPE`
- `NAME_EDUCATION_TYPE`, `NAME_FAMILY_STATUS`, `NAME_HOUSING_TYPE`

#### 3.3 Bivariate Analysis — Categorical vs Default Rate
Default rate (%) is computed for every category within each feature and ranked.  
Chi-square tests of independence confirm statistical significance.

#### 3.4 Univariate Analysis — Numerical
Distribution histograms (with TARGET overlay) for:
- `AMT_INCOME_TOTAL`, `AMT_CREDIT`, `AMT_ANNUITY`
- `YEARS_BIRTH`, `YEARS_EMPLOYED`, `CNT_CHILDREN`

#### 3.5 Bivariate Analysis — Numerical vs TARGET
Violin plots show the spread of each numerical variable for TARGET=0 and TARGET=1 side by side.

#### 3.6 Multivariate / Correlation Analysis
- Pearson correlation heatmap for all numerical features.
- Pairs with |r| > 0.70 flagged for multicollinearity review.

### Step 4 — Merged Dataset Analysis
- `previous_application.csv` merged with cleaned `application_data` on `SK_ID_CURR` (left join).
- Analysis of previous loan behaviour features: `NAME_CONTRACT_STATUS`, `NAME_YIELD_GROUP`, `PRODUCT_COMBINATION`.

---

## 4. Statistical Tests Used

| Test | Purpose |
|------|---------|
| Chi-square test of independence | Confirm whether a categorical feature is significantly associated with TARGET |
| IQR method | Identify and cap numerical outliers |
| Pearson correlation | Measure linear relationships between numerical features |

---

## 5. Tools & Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `pandas` | 2.0.3 | Data manipulation |
| `numpy` | 1.24.3 | Numerical computations |
| `matplotlib` | 3.7.2 | Base plotting |
| `seaborn` | 0.12.2 | Statistical visualisations |
| `scipy` | 1.11.2 | Statistical tests |

---

## 6. Assumptions & Limitations

1. **Class imbalance** — The ~8% minority class means count-based comparisons can be misleading; default-rate % comparisons are preferred.
2. **No modelling** — This is a pure EDA study; no predictive model is built.
3. **Missing data** — Columns with >50% missing values are dropped; the impact of this on completeness is acknowledged.
4. **External sources** — `EXT_SOURCE_1/2/3` are anonymised normalised scores; their methodology is unknown.
5. **Currency** — Monetary values are assumed to be in INR based on context; official documentation does not confirm this.
