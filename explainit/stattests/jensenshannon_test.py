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
from scipy.spatial import distance


def get_binned_data(
    reference: pd.Series,
    production: pd.Series,
    feature_type: str,
    n: int,
    feel_zeroes: bool = True,
):
    """Split variable into n buckets based on reference quantiles
    Args:
        reference: reference data
        production: production data
        feature_type: feature type
        n: number of quantiles
    Returns:
        reference_percents: % of records in each bucket for reference
        production_percents: % of records in each bucket for reference
    """
    n_vals = reference.nunique()
    if feature_type == "num" and n_vals > 20:

        bins = np.histogram_bin_edges(
            list(reference) + list(production), bins="sturges"
        )

        reference_percents = np.histogram(reference, bins)[0] / len(reference)
        production_percents = np.histogram(production, bins)[0] / len(production)

    else:
        keys = list((set(reference.unique()) | set(production.unique())) - {np.nan})

        ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference.value_counts())}
        production_feature_dict = {
            **dict.fromkeys(keys, 0),
            **dict(production.value_counts()),
        }

        reference_percents = np.array(
            [ref_feature_dict[key] / len(reference) for key in keys]
        )
        production_percents = np.array(
            [production_feature_dict[key] / len(production) for key in keys]
        )
    if feel_zeroes:
        np.place(reference_percents, reference_percents == 0, 0.0001)
        np.place(production_percents, production_percents == 0, 0.0001)

    return reference_percents, production_percents


def jensenshannon_stat_test(
    reference_data: pd.Series,
    production_data: pd.Series,
    feature_type: str,
    threshold: float,
    n_bins: int = 30,
) -> Tuple[float, bool, float]:
    """Compute the Jensen-Shannon distance between two arrays
    Args:
        reference_data: reference data
        production_data: production data
        feature_type: feature type
        threshold: all values above this threshold means data drift
        n_bins: number of bins
    Returns:
        jensenshannon: calculated Jensen-Shannon distance
        test_result: whether the drift is detected
        threshold: threshold for reference
    """
    reference_percents, production_percents = get_binned_data(
        reference_data, production_data, feature_type, n_bins, False
    )
    jensenshannon_value = distance.jensenshannon(
        reference_percents, production_percents
    )
    return jensenshannon_value, jensenshannon_value >= threshold, threshold
