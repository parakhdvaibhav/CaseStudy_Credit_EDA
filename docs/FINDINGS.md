# Key Findings & Business Recommendations

## Executive Summary

This EDA study analysed ~307,000 loan applications to identify patterns that predict customer payment difficulties (default). Five key drivers were identified that the credit-risk team can immediately incorporate into scoring and approval policies.

---

## Finding 1 — Education Level is a Strong Default Predictor

- Applicants with **Secondary / Special secondary** education are the largest group both by application volume and by absolute default count.
- Applicants with **Academic / higher degrees** default significantly less often in relative terms.
- **Chi-square test**: statistically significant association (p < 0.001).

**Recommendation**: Add education-level risk weighting to the credit score model; consider offering higher loan limits only to degree holders for amounts above ₹5L.

---

## Finding 2 — Employment Type Drives Risk

- **Maternity leave** and **Unemployed** income types show disproportionately high default rates.
- **Working** class is the most common applicant type; **Pensioners** have among the lowest default rates.

**Recommendation**: Flag Maternity leave and Unemployed applicants for manual underwriting review. Consider income documentation requirements for higher-risk income types.

---

## Finding 3 — Loan Amount Band ₹1L–₹5L Has Most Defaults

- The ₹1L–₹5L loan group accounts for the highest number of defaults in absolute terms.
- Loans above ₹10L have a lower relative default rate, likely due to stricter pre-approval scrutiny.

**Recommendation**: Apply stricter debt-to-income ratio checks for the ₹1L–₹5L band. Consider a mandatory co-signer policy for first-time borrowers in this range.

---

## Finding 4 — Age & Work Experience Correlate Negatively with Default

- Applicants aged **20–30** and those with **0–10 years** of work experience are most likely to default.
- Default risk decreases consistently with both age and employment tenure.

**Recommendation**:
- For applicants under 30 with < 3 years' work history, cap initial credit limits.
- Introduce a step-up credit product: start with a smaller loan and increase the limit upon timely repayment.

---

## Finding 5 — Contract Type: Cash Loans Have Higher Default Rate

- Cash loans dominate the default segment; revolving loans have a lower relative default rate.
- This may indicate that revolving credit attracts more financially disciplined customers who manage ongoing credit utilisation.

**Recommendation**: Consider promoting revolving credit products to moderate-risk segments as an alternative to large one-off cash loans.

---

## Finding 6 — Previous Loan Behaviour is Predictive

From the merged dataset analysis:

- Applicants whose previous applications were **Refused** or **Cancelled** show elevated default rates on new applications.
- High-yield (high interest rate) previous products correlate with higher default rates on current applications.

**Recommendation**: Integrate previous application status into the real-time credit decision engine as a direct feature input.

---

## Summary Risk Matrix

| Risk Factor | Direction | Relative Impact |
|-------------|-----------|-----------------|
| Education: Secondary only | ↑ default | High |
| Income: Unemployed / Maternity | ↑ default | High |
| Loan band: ₹1L–₹5L | ↑ default | Medium-High |
| Age < 30 & tenure < 3 yrs | ↑ default | Medium |
| Contract: Cash loan | ↑ default | Medium |
| Previous loan: Refused/Cancelled | ↑ default | Medium-High |
| Education: Higher degree | ↓ default | High |
| Income: Pensioner | ↓ default | Medium |
| Contract: Revolving | ↓ default | Medium |

---

## Next Steps

1. **Predictive modelling**: Use the identified features to train a logistic regression or gradient-boosting classifier.
2. **Segment-based pricing**: Implement risk-based interest rate tiers aligned with the findings above.
3. **Data enrichment**: Collect richer employment history and credit bureau data for the ₹1L–₹5L applicant band.
4. **Model monitoring**: Track default rates quarterly by segment to detect distribution shift.
