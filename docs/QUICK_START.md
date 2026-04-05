# Quick Start Guide

Get the Credit EDA project running in under 5 minutes.

---

## Prerequisites

* Python 3.8 or newer
* `git`

---

## 1. Clone the Repository

```bash
git clone https://github.com/parakhdvaibhav/CaseStudy_Credit_EDA.git
cd CaseStudy_Credit_EDA
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Add the Dataset

Download the Home Credit Default Risk dataset from Kaggle and place the CSV files in `data/raw/`:

```
data/
└── raw/
    ├── application_data.csv
    └── previous_application.csv
```

> **No data yet?** The example script works without real data — it generates a synthetic dataset automatically.

---

## 4. Run the Quick Analysis

```bash
python examples/quick_analysis.py --data data/raw/application_data.csv
```

Charts are saved to `reports/`.  To use the synthetic dataset instead:

```bash
python examples/quick_analysis.py
```

---

## 5. Explore the Notebooks

```bash
jupyter notebook notebooks/
```

Open the notebooks in order:

1. `01_data_exploration.ipynb` – Initial EDA and data quality checks
2. `02_detailed_analysis.ipynb` – Pattern discovery and feature analysis
3. `03_insights_recommendations.ipynb` – Business conclusions

---

## Use the Utilities in Your Own Code

```python
from src.data_loader import load_application_data, validate_data_quality
from src.analysis import calculate_default_statistics, engineer_features
from src.visualizations import plot_default_by_income

# Load data
df = load_application_data("data/raw/application_data.csv")

# Quality check
report = validate_data_quality(df)
print(f"Duplicate rows: {report['duplicate_rows']}")

# Enrich with derived features
df = engineer_features(df)

# Summarise defaults
stats = calculate_default_statistics(df)
print(f"Default rate: {stats['default_rate']:.2%}")

# Visualise
fig = plot_default_by_income(df)
fig.savefig("reports/default_by_income.png")
```

---

## Run the Tests

```bash
pytest tests/ -v --cov=src
```
