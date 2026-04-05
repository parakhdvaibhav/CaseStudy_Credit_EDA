# Data Dictionary — Home Credit Default Risk

## application_data.csv

This is the primary dataset containing information about each loan application.  
**Rows:** 307,511 | **Columns:** 122 | **Target:** `TARGET`

---

### Target Variable

| Column | Type | Description |
|--------|------|-------------|
| `TARGET` | int (0/1) | **1** = client had payment difficulties (late 30+ DPD at least once); **0** = all payments on time |

---

### Identification

| Column | Type | Description |
|--------|------|-------------|
| `SK_ID_CURR` | int | Unique loan application ID |

---

### Contract & Loan Attributes

| Column | Type | Description |
|--------|------|-------------|
| `NAME_CONTRACT_TYPE` | object | Loan type: *Cash loans* or *Revolving loans* |
| `AMT_CREDIT` | float | Total credit amount of the loan |
| `AMT_ANNUITY` | float | Loan annuity (monthly payment × term) |
| `AMT_GOODS_PRICE` | float | Price of goods for which the loan was given |
| `AMT_DOWN_PAYMENT` | float | Down payment on the loan |
| `WEEKDAY_APPR_PROCESS_START` | object | Day of week the application was submitted |
| `HOUR_APPR_PROCESS_START` | int | Hour of day the application was submitted |

---

### Applicant Demographics

| Column | Type | Description |
|--------|------|-------------|
| `CODE_GENDER` | object | Applicant gender: *M* / *F* / *XNA* |
| `FLAG_OWN_CAR` | object | Does the applicant own a car? (Y/N) |
| `FLAG_OWN_REALTY` | object | Does the applicant own real estate? (Y/N) |
| `CNT_CHILDREN` | int | Number of children |
| `AMT_INCOME_TOTAL` | float | Applicant's annual income |
| `NAME_INCOME_TYPE` | object | Income source (Working, Commercial associate, Pensioner, State servant, Unemployed, Student, Maternity leave, Businessman) |
| `NAME_EDUCATION_TYPE` | object | Highest education level |
| `NAME_FAMILY_STATUS` | object | Marital status |
| `NAME_HOUSING_TYPE` | object | Housing situation |
| `REGION_POPULATION_RELATIVE` | float | Population density of the applicant's region |
| `DAYS_BIRTH` | int | Age in days (negative; divide by −365 for years) |
| `DAYS_EMPLOYED` | int | Employment duration in days (negative = employed; 365243 = pensioner / not working) |
| `DAYS_REGISTRATION` | float | Days since last registration change |
| `DAYS_ID_PUBLISH` | int | Days since ID document was issued |
| `OCCUPATION_TYPE` | object | Occupation of the applicant (many missing) |
| `CNT_FAM_MEMBERS` | float | Number of family members |
| `REGION_RATING_CLIENT` | int | Credit bureau region rating (1–3) |
| `REGION_RATING_CLIENT_W_CITY` | int | Region rating adjusted for city |
| `ORGANIZATION_TYPE` | object | Type of employer organization |

---

### Contact & Document Flags

| Column | Type | Description |
|--------|------|-------------|
| `FLAG_MOBIL` | int | Is mobile phone provided? (1/0) |
| `FLAG_EMP_PHONE` | int | Is work phone provided? |
| `FLAG_WORK_PHONE` | int | Is work phone reachable? |
| `FLAG_CONT_MOBILE` | int | Is mobile reachable? |
| `FLAG_PHONE` | int | Is home phone provided? |
| `FLAG_EMAIL` | int | Is email provided? |
| `FLAG_DOCUMENT_2` … `FLAG_DOCUMENT_21` | int | Flags for various supporting documents submitted |

---

### External Data & Scores

| Column | Type | Description |
|--------|------|-------------|
| `EXT_SOURCE_1` | float | Normalised score from external data source 1 |
| `EXT_SOURCE_2` | float | Normalised score from external data source 2 |
| `EXT_SOURCE_3` | float | Normalised score from external data source 3 |

---

### Address & Region Flags

| Column | Type | Description |
|--------|------|-------------|
| `REG_REGION_NOT_LIVE_REGION` | int | Permanent address ≠ contact address region? |
| `REG_REGION_NOT_WORK_REGION` | int | Permanent address ≠ work address region? |
| `LIVE_REGION_NOT_WORK_REGION` | int | Contact address ≠ work address region? |
| `REG_CITY_NOT_LIVE_CITY` | int | Permanent address ≠ contact address city? |
| `REG_CITY_NOT_WORK_CITY` | int | Permanent address ≠ work address city? |
| `LIVE_CITY_NOT_WORK_CITY` | int | Contact address ≠ work address city? |

---

### Property & Building Details

| Column | Type | Description |
|--------|------|-------------|
| `APARTMENTS_AVG` … `YEARS_BUILD_MEDI` | float | Normalised building/apartment metrics (many missing) |
| `EMERGENCYSTATE_MODE` | object | Building emergency state |

---

### Enquiries (Credit Bureau Requests)

| Column | Type | Description |
|--------|------|-------------|
| `AMT_REQ_CREDIT_BUREAU_HOUR` | float | Credit enquiries in last hour |
| `AMT_REQ_CREDIT_BUREAU_DAY` | float | Credit enquiries in last day |
| `AMT_REQ_CREDIT_BUREAU_WEEK` | float | Credit enquiries in last week |
| `AMT_REQ_CREDIT_BUREAU_MON` | float | Credit enquiries in last month |
| `AMT_REQ_CREDIT_BUREAU_QRT` | float | Credit enquiries in last quarter |
| `AMT_REQ_CREDIT_BUREAU_YEAR` | float | Credit enquiries in last year |

---

## previous_application.csv

Contains historical loan applications for the same clients.  
**Rows:** ~1,670,214 | **Key join column:** `SK_ID_CURR`

| Column | Type | Description |
|--------|------|-------------|
| `SK_ID_PREV` | int | Unique previous application ID |
| `SK_ID_CURR` | int | Client ID (links to application_data) |
| `NAME_CONTRACT_TYPE` | object | Previous contract type |
| `AMT_ANNUITY` | float | Previous annuity |
| `AMT_APPLICATION` | float | Requested loan amount |
| `AMT_CREDIT` | float | Approved loan amount |
| `NAME_CONTRACT_STATUS` | object | Outcome: *Approved*, *Cancelled*, *Refused*, *Unused offer* |
| `DAYS_DECISION` | int | Days before current application that decision was made |
| `CNT_PAYMENT` | float | Number of payment instalments |

---

## Engineered Features (created in `src/analysis.py`)

| Column | Formula | Interpretation |
|--------|---------|---------------|
| `CREDIT_TO_INCOME` | `AMT_CREDIT / AMT_INCOME_TOTAL` | Credit-to-income ratio; values >8 are high-risk |
| `ANNUITY_TO_INCOME` | `AMT_ANNUITY / AMT_INCOME_TOTAL` | Monthly burden relative to income |
| `INCOME_PER_PERSON` | `AMT_INCOME_TOTAL / CNT_FAM_MEMBERS` | Per-capita household income |
| `AGE_YEARS` | `DAYS_BIRTH / -365` | Applicant age in years |
| `EMPLOYMENT_YEARS` | `DAYS_EMPLOYED / -365` | Employment tenure (negative = employed) |

---

## Known Data Quality Issues

| Issue | Affected Columns | Recommended Action |
|-------|-----------------|-------------------|
| ~65 columns have >30% missing values | Various building/apartment metrics | Drop or impute carefully |
| `DAYS_EMPLOYED = 365243` encodes non-workers | `DAYS_EMPLOYED` | Flag as `IS_PENSIONER = True`, replace with NaN |
| Extreme outliers in income | `AMT_INCOME_TOTAL` | Cap at 99th percentile or log-transform |
| Gender code `XNA` | `CODE_GENDER` | Treat as separate category or drop (<0.1%) |
