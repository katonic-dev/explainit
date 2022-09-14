from typing import Tuple

import pandas as pd
from scipy.stats import ks_2samp


def ks_stat_test(
    reference_data: pd.Series, current_data: pd.Series, threshold: float
) -> Tuple[float, bool, float]:
    """Run the two-sample Kolmogorov-Smirnov test of two samples. Alternative: two-sided
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: level of significance
    Returns:
        p_value: two-tailed p-value
        test_result: whether the drift is detected
    """
    p_value = ks_2samp(reference_data, current_data)[1]
    return p_value, p_value <= threshold, threshold
