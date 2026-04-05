"""
Convenience re-exports for the EDA utility package.
Import common helpers directly from `src.eda_utils`.
"""

from src.data_loader import (
    load_application_data,
    load_previous_application,
    validate_data_quality,
    drop_high_missing_columns,
    convert_days_to_years,
    save_processed,
)
from src.visualizations import (
    plot_distribution,
    plot_default_analysis,
    plot_correlation_heatmap,
    plot_count_by_target,
    plot_violin,
)
from src.analysis import (
    summarise_missing,
    detect_outliers_iqr,
    cap_outliers,
    high_correlation_pairs,
    default_rate_by_category,
    chi_square_test,
    descriptive_stats,
)

__all__ = [
    "load_application_data",
    "load_previous_application",
    "validate_data_quality",
    "drop_high_missing_columns",
    "convert_days_to_years",
    "save_processed",
    "plot_distribution",
    "plot_default_analysis",
    "plot_correlation_heatmap",
    "plot_count_by_target",
    "plot_violin",
    "summarise_missing",
    "detect_outliers_iqr",
    "cap_outliers",
    "high_correlation_pairs",
    "default_rate_by_category",
    "chi_square_test",
    "descriptive_stats",
]
