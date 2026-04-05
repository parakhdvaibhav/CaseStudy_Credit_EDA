# Data Dictionary — Credit EDA Case Study

This document describes the features present in the two datasets used in this analysis.

---

## `application_data.csv` — Current Loan Applications

| Column | Type | Description |
|--------|------|-------------|
| `SK_ID_CURR` | int | Unique loan application ID |
| `TARGET` | int | 1 = payment difficulty (default), 0 = all other cases |
| `NAME_CONTRACT_TYPE` | str | Type of loan contract: *Cash loans* or *Revolving loans* |
| `CODE_GENDER` | str | Applicant gender: M / F |
| `FLAG_OWN_CAR` | str | Whether the applicant owns a car (Y/N) |
| `FLAG_OWN_REALTY` | str | Whether the applicant owns real estate (Y/N) |
| `CNT_CHILDREN` | int | Number of children |
| `AMT_INCOME_TOTAL` | float | Annual income (INR) |
| `AMT_CREDIT` | float | Loan credit amount (INR) |
| `AMT_ANNUITY` | float | Loan annuity amount |
| `AMT_GOODS_PRICE` | float | Price of the goods for which the loan is granted |
| `NAME_TYPE_SUITE` | str | Who accompanied the client when applying |
| `NAME_INCOME_TYPE` | str | Income source: *Working*, *Commercial associate*, *Pensioner*, etc. |
| `NAME_EDUCATION_TYPE` | str | Education level: *Higher education*, *Secondary / special secondary*, etc. |
| `NAME_FAMILY_STATUS` | str | Marital status |
| `NAME_HOUSING_TYPE` | str | Housing situation: *House / apartment*, *Rented apartment*, etc. |
| `REGION_POPULATION_RELATIVE` | float | Normalised population of the region |
| `DAYS_BIRTH` | int | Negative days since birth (relative to application date) |
| `DAYS_EMPLOYED` | int | Negative days in current employment |
| `DAYS_REGISTRATION` | int | Negative days since the applicant changed registration |
| `DAYS_ID_PUBLISH` | int | Negative days since applicant changed identity document |
| `OWN_CAR_AGE` | float | Age of the applicant's car (years) |
| `FLAG_MOBIL` | int | Flag: mobile phone provided |
| `FLAG_EMP_PHONE` | int | Flag: work phone provided |
| `FLAG_WORK_PHONE` | int | Flag: work phone reachable |
| `FLAG_CONT_MOBILE` | int | Flag: mobile phone reachable |
| `FLAG_PHONE` | int | Flag: home phone provided |
| `FLAG_EMAIL` | int | Flag: email provided |
| `OCCUPATION_TYPE` | str | Occupation category |
| `CNT_FAM_MEMBERS` | float | Number of family members |
| `REGION_RATING_CLIENT` | int | Region rating (1 best, 3 worst) |
| `REGION_RATING_CLIENT_W_CITY` | int | Region rating adjusted for city |
| `WEEKDAY_APPR_PROCESS_START` | str | Day of week when application was submitted |
| `HOUR_APPR_PROCESS_START` | int | Hour of day when application was submitted |
| `EXT_SOURCE_1` | float | Normalised score from external data source 1 |
| `EXT_SOURCE_2` | float | Normalised score from external data source 2 |
| `EXT_SOURCE_3` | float | Normalised score from external data source 3 |
| `APARTMENTS_AVG` | float | Normalised information about the building (avg) |
| `DEF_30_CNT_SOCIAL_CIRCLE` | float | Defaults in applicant's social circle (30-day DPD) |
| `DEF_60_CNT_SOCIAL_CIRCLE` | float | Defaults in applicant's social circle (60-day DPD) |
| `DAYS_LAST_PHONE_CHANGE` | float | Days since last phone change |
| `AMT_REQ_CREDIT_BUREAU_*` | float | Number of credit bureau enquiries over various windows |

> **Derived columns** added during cleaning:
> - `YEARS_BIRTH` — age in years (from `DAYS_BIRTH`)
> - `YEARS_EMPLOYED` — tenure in years (from `DAYS_EMPLOYED`)
> - `LOAN_GROUP` — binned credit amount
> - `AGE_GROUP` — binned age

---

## `previous_application.csv` — Previous Loan Applications

| Column | Type | Description |
|--------|------|-------------|
| `SK_ID_PREV` | int | Unique previous application ID |
| `SK_ID_CURR` | int | Foreign key linking to `application_data` |
| `NAME_CONTRACT_TYPE` | str | Previous loan type |
| `AMT_ANNUITY` | float | Previous annuity |
| `AMT_APPLICATION` | float | How much the applicant applied for |
| `AMT_CREDIT` | float | Final credit amount approved |
| `AMT_DOWN_PAYMENT` | float | Down payment |
| `AMT_GOODS_PRICE` | float | Goods price |
| `WEEKDAY_APPR_PROCESS_START` | str | Day application started |
| `HOUR_APPR_PROCESS_START` | int | Hour application started |
| `FLAG_LAST_APPL_PER_CONTRACT` | str | Was this the last application for the contract |
| `NFLAG_LAST_APPL_IN_DAY` | int | Was this the last application on the day |
| `RATE_DOWN_PAYMENT` | float | Rate of down payment |
| `RATE_INTEREST_PRIMARY` | float | Primary interest rate |
| `RATE_INTEREST_PRIVILEGED` | float | Privileged interest rate |
| `NAME_CASH_LOAN_PURPOSE` | str | Purpose of the cash loan |
| `NAME_CONTRACT_STATUS` | str | Status: *Approved*, *Cancelled*, *Refused*, *Unused offer* |
| `DAYS_DECISION` | int | Days before application date when decision was made |
| `NAME_PAYMENT_TYPE` | str | Method of payment |
| `CODE_REJECT_REASON` | str | Reason for rejection |
| `NAME_TYPE_SUITE` | str | Who accompanied the client |
| `NAME_CLIENT_TYPE` | str | New or Returning client |
| `NAME_GOODS_CATEGORY` | str | Category of goods |
| `NAME_PORTFOLIO` | str | Portfolio type |
| `NAME_PRODUCT_TYPE` | str | Product type |
| `CHANNEL_TYPE` | str | Acquisition channel |
| `SELLERPLACE_AREA` | float | Area of the seller's place |
| `NAME_SELLER_INDUSTRY` | str | Industry of seller |
| `CNT_PAYMENT` | float | Term of previous credit |
| `NAME_YIELD_GROUP` | str | Grouped interest rate bucket |
| `PRODUCT_COMBINATION` | str | Combination of product features |
| `DAYS_FIRST_DRAWING` | float | Earliest possible drawing date |
| `DAYS_FIRST_DUE` | float | First repayment due |
| `DAYS_LAST_DUE_1ST_VERSION` | float | Last due date (first version) |
| `DAYS_LAST_DUE` | float | Last due date |
| `DAYS_TERMINATION` | float | Expected termination date |
| `NFLAG_INSURED_ON_APPROVAL` | float | Was the client insured at approval |
