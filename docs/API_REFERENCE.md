# API Reference

Complete reference for all public utility functions in the `src/` package.

---

## `src.data_loader`

### `load_application_data(filepath=None)`

Load the main application dataset from a CSV file.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filepath` | `str` | `None` | Path to CSV file. Defaults to `data/raw/application_data.csv`. |

**Returns:** `pd.DataFrame`

**Raises:** `FileNotFoundError` if the file is missing; `ValueError` if the DataFrame is empty.

```python
from src.data_loader import load_application_data
df = load_application_data("data/raw/application_data.csv")
```

---

### `load_previous_application(filepath=None)`

Load the previous-application dataset.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filepath` | `str` | `None` | Path to CSV file. Defaults to `data/raw/previous_application.csv`. |

**Returns:** `pd.DataFrame`

---

### `validate_data_quality(df)`

Run data-quality checks and return a summary report.

| Parameter | Type | Description |
|-----------|------|-------------|
| `df` | `pd.DataFrame` | DataFrame to validate. |

**Returns:** `dict` with keys `shape`, `missing_counts`, `missing_percentages`, `high_missing_columns`, `duplicate_rows`, `dtypes`, `has_target`.

```python
from src.data_loader import validate_data_quality
report = validate_data_quality(df)
print(report["duplicate_rows"])
```

---

### `get_missing_summary(df)`

Return a sorted DataFrame of missing-value statistics (missing count and percentage).

**Returns:** `pd.DataFrame` with columns `missing_count`, `missing_percentage`.

---

### `drop_high_missing_columns(df, threshold=None)`

Drop columns whose missing percentage exceeds `threshold`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | Input DataFrame. |
| `threshold` | `float` | `0.50` | Fraction (0–1) above which a column is dropped. |

**Returns:** `pd.DataFrame`

---

## `src.analysis`

### `calculate_missing_percentages(df)`

Return missing-value percentage per column, sorted descending.

**Returns:** `pd.Series`

---

### `calculate_default_statistics(df)`

Compute default/non-default counts and rates.

**Returns:** `dict` with keys `total`, `defaults`, `non_defaults`, `default_rate`, `non_default_rate`.

**Raises:** `KeyError` if `TARGET` column is absent.

```python
from src.analysis import calculate_default_statistics
stats = calculate_default_statistics(df)
print(f"Default rate: {stats['default_rate']:.2%}")
```

---

### `calculate_correlation_matrix(df, columns=None)`

Return the Pearson correlation matrix for numeric columns.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `pd.DataFrame` | — | Input DataFrame. |
| `columns` | `list[str]` | `None` | Column subset. All numeric columns used if `None`. |

**Returns:** `pd.DataFrame`

---

### `get_highly_correlated_pairs(df, threshold=None)`

Return feature pairs with absolute correlation above `threshold`.

**Returns:** `pd.DataFrame` with columns `feature_1`, `feature_2`, `correlation`.

---

### `calculate_default_rate_by_category(df, category_column)`

Compute default rate for each level of a categorical column.

**Returns:** `pd.DataFrame` sorted descending by `default_rate`.

---

### `engineer_features(df)`

Add derived features: `AGE_YEARS`, `EMPLOYMENT_YEARS`, `CREDIT_TO_INCOME`, `ANNUITY_TO_INCOME`.

**Returns:** `pd.DataFrame` (does not mutate the input).

```python
from src.analysis import engineer_features
df = engineer_features(df)
print(df[["AGE_YEARS", "CREDIT_TO_INCOME"]].head())
```

---

## `src.visualizations`

All functions return a `matplotlib.figure.Figure` and do **not** call `plt.show()`.

### `plot_distribution(data, column, title=None, figsize=...)`

Histogram + KDE for a numeric column.

```python
from src.visualizations import plot_distribution
fig = plot_distribution(df, "AMT_INCOME_TOTAL")
fig.savefig("reports/income_dist.png")
```

---

### `plot_default_analysis(data, feature, title=None, figsize=...)`

Grouped bar chart of default vs non-default counts for a categorical feature.

---

### `plot_correlation_heatmap(data, columns=None, title=..., figsize=...)`

Annotated Pearson correlation heatmap.

---

### `plot_default_by_income(data, income_column=..., title=..., figsize=...)`

Bar chart of default rates grouped by income type, with an overall-mean reference line.

---

### `plot_age_vs_default(data, age_column=..., bins=10, title=..., figsize=...)`

Default rate across equal-width age brackets. Accepts both negative-days and positive-years encodings.

---

## `src.eda_utils`

### `describe_dataframe(df)`

Extended `describe()` with `missing_pct` and `dtype` columns added.

---

### `identify_outliers_iqr(df, column)`

Return rows where `column` is an IQR outlier.

---

### `get_value_counts_with_pct(df, column)`

Value counts with percentage for a categorical column.

---

### `flag_anomalous_employment(df)`

Add `IS_PENSIONER` boolean column for `DAYS_EMPLOYED == 365243`.

---

### `get_categorical_default_rates(df, columns=None)`

Compute per-category default rates for multiple categorical columns simultaneously.

**Returns:** `dict[str, pd.Series]`
