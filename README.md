# CaseStudy_Credit_EDA

Exploratory Data Analysis of Home Credit loan applications to identify risk drivers of customer default and generate business-actionable insights.

---

## Executive Summary

Using 307,511 loan applications (122 features), this project performs a structured exploratory data analysis to uncover the strongest drivers of loan default.

### Headline Findings

- Overall default rate: ~8.1% (highly imbalanced dataset)
- Younger applicants (20–30) default at ~2× the rate of applicants aged 40–50
- Maternity leave and unemployed income types show highest default risk
- CREDIT_TO_INCOME > 8× strongly correlates with default
- AMT_CREDIT and AMT_GOODS_PRICE show near-perfect correlation (r ≈ 0.99)
- ~65 columns have >30% missing values; 49 can be safely dropped

This analysis provides direct business recommendations for credit risk policy.

---

## Dataset Overview

- **Source:** [Home Credit Default Risk — Kaggle](https://www.kaggle.com/c/home-credit-default-risk)
- **Main file:** `application_data.csv`
- **Rows:** 307,511
- **Columns:** 122
- **Target column:** `TARGET`
- **Supplementary file:** `previous_application.csv`

---

## Repository Structure

```
CaseStudy_Credit_EDA
│
├── .github/workflows
├── data
│   ├── raw
│   └── processed
├── notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_detailed_analysis.ipynb
│   └── 03_insights_recommendations.ipynb
├── src
│   ├── config.py
│   ├── data_loader.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── visualizations.py
│   ├── pipeline.py
│   └── eda_utils.py
├── tests
├── examples
│   └── quick_analysis.py
├── docs
├── reports
├── requirements.txt
└── README.md
```

---

## Quick Start

**Clone repository**

```bash
git clone https://github.com/parakhdvaibhav/CaseStudy_Credit_EDA.git
cd CaseStudy_Credit_EDA
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run example**

```bash
python examples/quick_analysis.py
```

**Run tests**

```bash
pytest tests/ -v --cov=src
```

---

## Run Full EDA Pipeline

```python
from src.pipeline import run_full_eda

result = run_full_eda(
    "data/raw/application_data.csv",
    output_dir="reports"
)

print(result["default_statistics"])
```

This runs:

- Data loading
- Data quality validation
- Feature engineering
- Default statistics
- Visualizations
- Report generation

---

## Generated Outputs

```
reports/
    income_distribution.png
    default_by_income.png
    age_vs_default.png
    correlation_heatmap.png
```

---

## Using the Utilities

```python
from src.data_loader import load_application_data
from src.analysis import calculate_default_statistics

df = load_application_data("data/raw/application_data.csv")
stats = calculate_default_statistics(df)

print(stats)
```

---

## Key Insights

| Finding | Recommendation |
|---|---|
| Young applicants default more frequently | Age-based risk scoring |
| Unemployed applicants are higher risk | Require collateral |
| Credit-to-income > 8× is risky | Apply credit caps |
| Missing occupation correlates with default | Treat missing as risk signal |
| Credit & goods price are redundant | Remove multicollinearity |

---

## Methodology

Pipeline:

1. Data ingestion
2. Data cleaning
3. Exploratory analysis
4. Statistical testing
5. Feature engineering
6. Visualization
7. Insight generation

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md)

---

## Business Context

The company faces two types of risk:

| Risk Type | Description |
|---|---|
| **Lost Business** | Rejecting a customer who would repay |
| **Financial Loss** | Approving a customer who defaults |

EDA helps:

- Improve loan approval decisions
- Reduce default risk
- Increase profitable approvals

---

## Why This Project Matters

This project demonstrates:

- End-to-end data science workflow
- Production-ready Python utilities
- Test-driven development
- Reusable analytics pipeline
- Business-focused insights

---

## Testing

```bash
pytest tests/ -v --cov=src
```

81 tests currently passing.

---

## Documentation

| File | Description |
|---|---|
| [QUICK_START.md](docs/QUICK_START.md) | Setup guide |
| [API_REFERENCE.md](docs/API_REFERENCE.md) | Functions |
| [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) | Feature descriptions |
| [METHODOLOGY.md](docs/METHODOLOGY.md) | Pipeline explanation |
| [FINDINGS.md](docs/FINDINGS.md) | Business insights |
| [VISUALIZATIONS.md](docs/VISUALIZATIONS.md) | Chart gallery |

---

## Co-Collaborator

[Sankalp Seksaria](https://github.com/sankalpseksaria)

---

## Future Improvements

- Predictive model
- Feature importance
- SHAP explainability
- Dashboard (Streamlit)
