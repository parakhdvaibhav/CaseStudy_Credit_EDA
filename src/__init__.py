"""
CaseStudy_Credit_EDA - Source utilities for credit risk exploratory data analysis.
"""

from src.data_loader import (
    load_application_data,
    load_previous_application,
    validate_data_quality,
)
from src.analysis import (
    calculate_missing_percentages,
    calculate_default_statistics,
    calculate_correlation_matrix,
    calculate_missing_by_target,
)
from src.visualizations import (
    plot_distribution,
    plot_default_analysis,
    plot_correlation_heatmap,
    plot_default_by_income,
    plot_age_vs_default,
)

__all__ = [
    "load_application_data",
    "load_previous_application",
    "validate_data_quality",
    "calculate_missing_percentages",
    "calculate_default_statistics",
    "calculate_correlation_matrix",
    "calculate_missing_by_target",
    "plot_distribution",
    "plot_default_analysis",
    "plot_correlation_heatmap",
    "plot_default_by_income",
    "plot_age_vs_default",
]
