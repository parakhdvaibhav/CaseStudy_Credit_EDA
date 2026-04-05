# Visualizations Gallery

This page describes the key visualizations produced by the Credit EDA analysis and the business insights each chart reveals.

---

## 1. Default Distribution by Income Type

**What it shows:** Bar chart of loan-default rates broken down by applicant income type (Working, Pensioner, Commercial Associate, State Servant, etc.).

**Key insight:** Applicants on *Maternity leave* and those classified as *Unemployed* show markedly higher default rates compared to salaried workers.  Commercial associates tend to be lower-risk.

**How to reproduce:**
```python
from src.visualizations import plot_default_by_income
fig = plot_default_by_income(df)
fig.savefig("reports/default_by_income.png")
```

---

## 2. Correlation Heatmap of Key Features

**What it shows:** Pearson correlation matrix for the main numeric features: income, credit amount, annuity, goods price, and derived ratios.

**Key insight:** `AMT_CREDIT` and `AMT_GOODS_PRICE` are strongly correlated (r ≈ 0.99), meaning they carry largely redundant information.  `DAYS_BIRTH` (applicant age) has a weak negative correlation with default, i.e. older applicants default slightly less often.

**How to reproduce:**
```python
from src.visualizations import plot_correlation_heatmap
cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE", "DAYS_BIRTH"]
fig = plot_correlation_heatmap(df, columns=cols)
fig.savefig("reports/correlation_heatmap.png")
```

---

## 3. Age vs Default Patterns

**What it shows:** Default rate plotted across equal-width age brackets (derived from `DAYS_BIRTH`).

**Key insight:** Younger applicants (20–30 years) have notably higher default rates.  Risk decreases steadily until ~50 years and plateaus afterwards.  This suggests age-based risk tiers could improve underwriting decisions.

**How to reproduce:**
```python
from src.visualizations import plot_age_vs_default
fig = plot_age_vs_default(df, bins=10)
fig.savefig("reports/age_vs_default.png")
```

---

## 4. Debt-to-Income (Credit-to-Income) Analysis

**What it shows:** Distribution of the `CREDIT_TO_INCOME` ratio — total credit divided by annual income.

**Key insight:** Applicants with a credit-to-income ratio above ~8× account for a disproportionately large share of defaults.  The overall population median is around 3–4×.

**How to reproduce:**
```python
from src.analysis import engineer_features
from src.visualizations import plot_distribution

df = engineer_features(df)
fig = plot_distribution(df, "CREDIT_TO_INCOME", title="Credit-to-Income Distribution")
fig.savefig("reports/credit_to_income.png")
```

---

## 5. Employment Type Impact

**What it shows:** Default rate for each `OCCUPATION_TYPE` value in the dataset.

**Key insight:** Low-skilled labourers and drivers carry higher default rates; core staff and high-skill professionals have lower rates.  Missing occupation data (`NaN`) correlates with elevated default risk — suggesting that missing data itself can be a predictive signal.

**How to reproduce:**
```python
from src.visualizations import plot_default_analysis
fig = plot_default_analysis(df, "OCCUPATION_TYPE")
fig.savefig("reports/default_by_occupation.png")
```
