# Copyright 2022 The Explainit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY aIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
