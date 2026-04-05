# CaseStudy_Credit_EDA

![CI](https://github.com/parakhdvaibhav/CaseStudy_Credit_EDA/actions/workflows/ci.yml/badge.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

Exploratory data analysis of Home Credit loan application data to identify patterns that indicate customer payment difficulties.

---

## Executive Summary

Using a dataset of **307,511 loan applications** (122 features each), we applied comprehensive EDA to uncover the key drivers of loan default.

**Headline findings:**
* Overall default rate is approximately **8.1%** — highly imbalanced.
* **Younger applicants (20–30 yrs)** default at roughly 2× the rate of applicants aged 40–50.
* **Maternity-leave** and **unemployed** income types carry the highest default rates.
* The `CREDIT_TO_INCOME` ratio is a strong risk signal — applicants above **8×** are disproportionately represented among defaults.
* `AMT_CREDIT` and `AMT_GOODS_PRICE` are near-perfectly correlated (r ≈ 0.99) and carry redundant information.
* ~65 columns have >30% missing values; 49 have >50% and can be dropped safely.

---

## Dataset Overview

| Property | Value |
|----------|-------|
| Source | [Home Credit Default Risk – Kaggle](https://www.kaggle.com/c/home-credit-default-risk) |
| Main file | `application_data.csv` |
| Rows | 307,511 |
| Columns | 122 |
| Target column | `TARGET` (1 = default, 0 = no default) |
| Supplementary file | `previous_application.csv` (1.67 M rows) |

---

## Repository Structure

```
CaseStudy_Credit_EDA/
├── .github/workflows/
│   ├── ci.yml                   # CI: lint → test → coverage gate
│   └── notebook-validation.yml  # Validate notebook format
├── data/
│   ├── raw/                     # Raw CSVs (not committed)
│   └── processed/               # Cleaned data (not committed)
├── notebooks/                   # Jupyter notebooks
├── src/                         # Reusable Python utilities
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── analysis.py
│   ├── visualizations.py
│   └── eda_utils.py
├── tests/                       # pytest test suite
│   ├── conftest.py
│   ├── test_data_loader.py
│   ├── test_visualizations.py
│   └── test_analysis.py
├── examples/
│   └── quick_analysis.py        # Runnable end-to-end example
├── docs/
│   ├── API_REFERENCE.md
│   ├── QUICK_START.md
│   └── VISUALIZATIONS.md
├── reports/                     # Generated charts / outputs
├── .gitignore
├── config.yaml
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/parakhdvaibhav/CaseStudy_Credit_EDA.git
cd CaseStudy_Credit_EDA

# 2. Install
pip install -r requirements.txt

# 3. Run example (uses synthetic data if real data is absent)
python examples/quick_analysis.py

# 4. Run tests
pytest tests/ -v --cov=src
```

See [docs/QUICK_START.md](docs/QUICK_START.md) for the full 5-minute setup guide.

---

## Using the Utilities

```python
from src.data_loader import load_application_data, validate_data_quality
from src.analysis import calculate_default_statistics, engineer_features
from src.visualizations import plot_default_by_income

df = load_application_data("data/raw/application_data.csv")
report = validate_data_quality(df)

df = engineer_features(df)
stats = calculate_default_statistics(df)
print(f"Default rate: {stats['default_rate']:.2%}")

fig = plot_default_by_income(df)
fig.savefig("reports/default_by_income.png")
```

Full function documentation: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)

---

## Key Insights

| Finding | Business Action |
|---------|----------------|
| Young applicants (20–30) default at 2× average rate | Apply age-based risk tiers |
| Unemployed / maternity-leave income types are highest risk | Require additional collateral or guarantor |
| Credit-to-income > 8× strongly predicts default | Hard cap or higher interest for high-ratio loans |
| Missing occupation data correlates with default | Treat missing occupation as a separate risk category |
| AMT_CREDIT ↔ AMT_GOODS_PRICE near-perfectly correlated | Use only one in predictive models |

---

## Visualizations

See [docs/VISUALIZATIONS.md](docs/VISUALIZATIONS.md) for the full chart gallery with business commentary.

---

## Running CI Locally

```bash
# Lint
pip install black flake8
black --check src/ tests/ examples/
flake8 src/ tests/ examples/ --max-line-length=100

# Test with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Business Understanding

The loan-providing company faces two types of risk:

1. **Lost business** – rejecting an applicant who would have repaid the loan.
2. **Financial loss** – approving an applicant who defaults.

Four possible outcomes exist for each application: *Approved*, *Cancelled*, *Refused*, *Unused offer*.  This EDA focuses on identifying applicant attributes that are strong predictors of default so that the company can:

* Deny high-risk loans
* Adjust loan amounts or interest rates for borderline applicants
* Retain creditworthy customers who might otherwise be incorrectly rejected

---

## Business Objectives

Identify patterns in applicant and loan attributes that indicate payment difficulties.  The driving factors (driver variables) discovered through EDA can feed directly into credit-scoring and portfolio-risk models.

---

## Co-collaborator

[Sankalp Seksaria](https://github.com/sankalpseksaria)
