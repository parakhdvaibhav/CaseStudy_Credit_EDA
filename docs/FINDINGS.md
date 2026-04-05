# Key Findings — Credit EDA

## Executive Summary

Analysis of **307,511 Home Credit loan applications** (122 features) revealed six primary risk drivers that together explain a large portion of the observed **8.1% overall default rate**.

---

## Finding 1: Age is a Strong Predictor of Default

**Observation:** Applicants aged 20–30 default at approximately **twice the rate** of applicants aged 40–50.

| Age Band | Approximate Default Rate |
|----------|--------------------------|
| 20–25 | ~13–15% |
| 25–30 | ~11–12% |
| 30–40 | ~8–9% |
| 40–50 | ~6–7% |
| 50–60 | ~5–6% |
| 60+ | ~4–5% |

**Business Action:** Apply age-based risk tiering; younger applicants should face more stringent income or collateral requirements.

---

## Finding 2: Income Type is Highly Predictive

**Observation:** Income type is one of the strongest categorical predictors of default.

| Income Type | Relative Risk |
|-------------|--------------|
| Maternity leave | Highest |
| Unemployed | Very high |
| Working | Average |
| Commercial associate | Below average |
| Pensioner | Low |
| State servant | Low |
| Student | Insufficient data |

**Business Action:** Require additional collateral, a guarantor, or shorter loan terms for maternity-leave and unemployed applicants.

---

## Finding 3: Credit-to-Income Ratio Drives Default

**Observation:** The ratio `CREDIT_TO_INCOME = AMT_CREDIT / AMT_INCOME_TOTAL` is a powerful engineered feature.

| Ratio Band | Default Rate |
|------------|-------------|
| < 2× | ~5% |
| 2–4× | ~7% |
| 4–6× | ~9% |
| 6–8× | ~11% |
| > 8× | ~14–16% |

**Business Action:** Implement a hard cap at 8× or escalate to senior underwriting review; apply higher interest rates for ratios above 6×.

---

## Finding 4: Missing Occupation Data Signals Risk

**Observation:** Applicants who left `OCCUPATION_TYPE` blank default at a **materially higher rate** than those who provided an occupation.

- Blank `OCCUPATION_TYPE`: default rate ≈ **10–12%**
- Provided `OCCUPATION_TYPE`: default rate ≈ **7–8%**

**Hypothesis:** Missing occupation may indicate informal or unstable employment that applicants are reluctant to disclose.

**Business Action:** Treat "occupation not provided" as its own risk category; do not impute with the mode.

---

## Finding 5: Near-Perfect Collinearity Between AMT_CREDIT and AMT_GOODS_PRICE

**Observation:** `AMT_CREDIT` and `AMT_GOODS_PRICE` have a Pearson correlation of **r ≈ 0.99**, making them essentially redundant.

**Business Action:** Use only one of these columns in predictive models; prefer `AMT_CREDIT` as it is always populated.

---

## Finding 6: Data Quality — 65 Columns Have > 30% Missing Values

**Observation:** A significant portion of the feature set has poor coverage.

| Missing Threshold | Column Count |
|-------------------|-------------|
| > 10% missing | ~80 columns |
| > 30% missing | ~65 columns |
| > 50% missing | ~49 columns |

Columns with > 50% missing values are primarily building and apartment characteristics (e.g., `APARTMENTS_AVG`, `YEARS_BUILD_AVG`) that were not collected for all application types.

**Business Action:**
- Drop the 49 columns > 50% missing for modelling
- Flag the remaining high-missing columns and test imputation strategies
- Consider collecting these fields more consistently in future applications

---

## Summary Risk Driver Table

| # | Finding | Impact | Confidence |
|---|---------|--------|-----------|
| 1 | Young age (20–30) doubles default rate | High | High |
| 2 | Maternity leave / Unemployed income types | High | High |
| 3 | Credit-to-income ratio > 8× | High | High |
| 4 | Missing occupation type | Medium | Medium |
| 5 | AMT_CREDIT ↔ AMT_GOODS_PRICE collinearity | Model quality | High |
| 6 | 49 columns > 50% missing | Data quality | High |

---

## Recommended Next Steps

1. **Build a credit scoring model** using the six risk drivers as primary features
2. **Apply SMOTE or class weights** to address the 8.1% class imbalance
3. **Time-based train/test split** to validate that patterns are stable over time
4. **Collect missing fields** (occupation, building characteristics) more consistently
5. **Monitor deployed model** for drift in age and income-type distributions
