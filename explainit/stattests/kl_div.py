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
from explainit.stattests.utils import get_binned_data
from scipy.stats import entropy


def kl_div_stat_test(
    reference_data: pd.Series,
    production_data: pd.Series,
    feature_type: str,
    threshold: float,
    n_bins: int = 30,
) -> Tuple[float, bool, float]:
    """Compute the Kullback-Leibler divergence between two arrays
    Args:
        reference_data: reference data
        production_data: production data
        feature_type: feature type
        threshold: all values above this threshold means data drift
        n_bins: number of bins
    Returns:
        kl_div: calculated Kullback-Leibler divergence value
        test_result: whether the drift is detected
        threshold: threshold for reference
    """
    reference_percents, current_percents = get_binned_data(
        reference_data, production_data, feature_type, n_bins
    )
    kl_div_value = entropy(reference_percents, current_percents)
    return kl_div_value, kl_div_value >= threshold, threshold
