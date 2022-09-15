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

import numpy as np
import pandas as pd
from scipy.stats import chisquare


def chi_stat_test(
    reference_data: pd.Series, current_data: pd.Series, threshold: float
) -> Tuple[float, bool, float]:
    #  TODO: simplify ignoring NaN values here, in z_stat_test and data_drift_analyzer
    keys = list((set(reference_data) | set(current_data)) - {np.nan})

    ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data.value_counts())}
    current_feature_dict = {
        **dict.fromkeys(keys, 0),
        **dict(current_data.value_counts()),
    }

    k_norm = current_data.shape[0] / reference_data.shape[0]

    f_exp = [ref_feature_dict[key] * k_norm for key in keys]
    f_obs = [current_feature_dict[key] for key in keys]
    p_value = chisquare(f_obs, f_exp)[1]
    return p_value, p_value <= threshold, threshold
