"""
CaseStudy_Credit_EDA reusable utilities.

<<<<<<< HEAD
This package contains small, testable functions extracted from the original
notebook (now archived in notebooks/archive/00_original_credit_eda.ipynb).
"""
=======
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
>>>>>>> main
