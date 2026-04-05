# CaseStudy_Credit_EDA

> **Exploratory Data Analysis of credit-risk data to identify key drivers of loan default**  
> *by [Vaibhav Parakh](https://github.com/parakhdvaibhav) & [Sankalp Seksaria](https://github.com/sankalpseksaria)*

---

## Executive Summary — Key Findings

| # | Finding | Business Impact |
|---|---------|----------------|
| 1 | Applicants with **secondary education only** default most frequently | Add education weight to credit scoring |
| 2 | **Unemployed / Maternity leave** income types show highest default rates | Flag for manual underwriting |
| 3 | Loan band **₹1L–₹5L** drives the highest absolute default count | Stricter debt-to-income checks in this band |
| 4 | Applicants aged **20–30 with < 3 yrs experience** default most | Cap initial credit limits for this segment |
| 5 | **Cash loans** default more than revolving loans | Promote revolving products for moderate-risk applicants |
| 6 | History of **Refused / Cancelled** previous applications predicts current default | Integrate prior status into decision engine |

📄 Full findings: [`docs/FINDINGS.md`](docs/FINDINGS.md)

---

## Business Understanding

Consumer finance companies face a two-sided risk when approving loans:

- **False Negative** (approving a defaulter) → financial loss
- **False Positive** (rejecting a creditworthy applicant) → lost business

This study uses EDA to identify patterns in ~307,000 loan applications that distinguish clients who repay on time from those who experience payment difficulties.

### Four Possible Application Outcomes

| Status | Description |
|--------|-------------|
| **Approved** | Loan application accepted |
| **Cancelled** | Client withdrew during approval |
| **Refused** | Lender rejected — client did not meet requirements |
| **Unused offer** | Client cancelled at a different stage |

---

## Dataset

| File | Rows | Description |
|------|------|-------------|
| `application_data.csv` | ~307,000 | Current loan applications with TARGET label |
| `previous_application.csv` | ~1.67M | Historical loan records per client |

Source: [Home Credit Default Risk — Kaggle](https://www.kaggle.com/c/home-credit-default-risk)

📖 Feature descriptions: [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md)

---

## Repository Structure

```
CaseStudy_Credit_EDA/
├── data/
│   ├── raw/                          # Place source CSVs here (git-ignored)
│   └── processed/                    # Cleaned datasets (git-ignored)
├── notebooks/
│   ├── 01_data_exploration.ipynb     # Data loading, QA, cleaning
│   ├── 02_detailed_analysis.ipynb    # Uni/bivariate/multivariate analysis
│   └── 03_insights_recommendations.ipynb  # Business findings & recommendations
├── src/
│   ├── __init__.py
│   ├── config.py                     # Paths, thresholds, analysis parameters
│   ├── data_loader.py                # Load & validate datasets
│   ├── eda_utils.py                  # Convenience re-exports
│   ├── visualizations.py             # Reusable plotting functions
│   └── analysis.py                   # Statistical analysis functions
├── docs/
│   ├── DATA_DICTIONARY.md            # Feature descriptions
│   ├── METHODOLOGY.md                # Analysis approach & techniques
│   └── FINDINGS.md                   # Key insights & recommendations
├── reports/                          # Generated report outputs
├── CREDIT_EDA_Group Assignment_Sankalp & Vaibhav.ipynb  # Original notebook
├── Credit EDA Case Study - Sankalp & Vaibhav.pdf        # PDF report
├── requirements.txt
└── .gitignore
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- `pip`

### Install dependencies

```bash
# Clone the repository
git clone https://github.com/parakhdvaibhav/CaseStudy_Credit_EDA.git
cd CaseStudy_Credit_EDA

# (Recommended) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows

# Install required packages
pip install -r requirements.txt
```

### Add the datasets

Download `application_data.csv` and `previous_application.csv` from the
[Kaggle competition page](https://www.kaggle.com/c/home-credit-default-risk/data)
and place them in `data/raw/`.

---

## How to Run

Run notebooks in order from the `notebooks/` directory:

```bash
cd notebooks
jupyter notebook
```

| Notebook | Purpose |
|----------|---------|
| `01_data_exploration.ipynb` | Load raw data, assess quality, clean & save |
| `02_detailed_analysis.ipynb` | Uni/bivariate/multivariate analysis |
| `03_insights_recommendations.ipynb` | Business insights & recommendations |

> **Note**: Run Notebook 1 first — it produces `data/processed/application_cleaned.csv`
> which is required by Notebooks 2 and 3.

---

## Analysis Methodology

1. **Data Quality** — Missing-value audit; drop columns > 50% missing
2. **Cleaning** — Day-column conversion, IQR outlier capping
3. **Univariate Analysis** — Distributions for categorical & numerical features
4. **Bivariate Analysis** — Default rate by category; violin plots for numerical features
5. **Multivariate Analysis** — Pearson correlation heatmap; high-correlation pairs
6. **Merged Analysis** — Join with previous application history for richer context

📋 Full methodology: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)

---

## PDF Report

The slide-style summary report is available at:
[`Credit EDA Case Study - Sankalp & Vaibhav.pdf`](Credit%20EDA%20Case%20Study%20-%20Sankalp%20%26%20Vaibhav.pdf)

---

## Authors

- **Vaibhav Parakh** — [GitHub](https://github.com/parakhdvaibhav)
- **Sankalp Seksaria** — [GitHub](https://github.com/sankalpseksaria)
