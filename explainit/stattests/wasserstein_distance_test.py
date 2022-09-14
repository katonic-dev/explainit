from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance


def wasserstein_distance_stat_test(
    reference_data: pd.Series, current_data: pd.Series, threshold: float
) -> Tuple[float, bool, float]:
    """Compute the first Wasserstein distance between two arrays normed by std of reference data
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
    Returns:
        wasserstein_distance_norm: normed Wasserstein distance
        test_result: whether the drift is detected
    """
    norm = max(np.std(reference_data), 0.001)
    wd_norm_value = wasserstein_distance(reference_data, current_data) / norm
    return wd_norm_value, wd_norm_value >= threshold, threshold
