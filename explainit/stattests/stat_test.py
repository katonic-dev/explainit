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
from typing import Dict
from typing import List

import numpy as np
import pandas as pd
from explainit.stattests.chi2_test import chi_stat_test
from explainit.stattests.jensenshannon_test import jensenshannon_stat_test
from explainit.stattests.ks_test import ks_stat_test
from explainit.stattests.wasserstein_distance_test import wasserstein_distance_stat_test
from explainit.stattests.z_test import z_stat_test


def get_statistical_info(
    feature_test: Dict[str, List[str]],
    reference_data: pd.DataFrame,
    production_data: pd.DataFrame,
):
    test_info = {}

    for feature in list(feature_test.keys()):
        ref_feature = (
            reference_data[feature].replace([-np.inf, np.inf], np.nan).dropna()
        )
        prod_feature = (
            production_data[feature].replace([-np.inf, np.inf], np.nan).dropna()
        )
        if feature_test[feature][0] == "ks_stat_test":
            p_value, drift, threshold = ks_stat_test(
                ref_feature, prod_feature, threshold=0.05
            )

        if feature_test[feature][0] == "z_stat_test":
            p_value, drift, threshold = z_stat_test(
                ref_feature, prod_feature, threshold=0.05
            )

        if feature_test[feature][0] == "chi_stat_test":
            p_value, drift, threshold = chi_stat_test(
                ref_feature, prod_feature, threshold=0.05
            )

        if feature_test[feature][0] == "jensenshannon_stat_test":
            p_value, drift, threshold = jensenshannon_stat_test(
                ref_feature, prod_feature, feature_test[feature][1], threshold=0.1
            )

        if feature_test[feature][0] == "wasserstein_stat_test":
            p_value, drift, threshold = wasserstein_distance_stat_test(
                ref_feature, prod_feature, threshold=0.1
            )
        test_info[feature] = {
            "feature_name": feature,
            "threshold": threshold,
            "stattest": feature_test[feature],
            "p_value": p_value,
            "drift": drift,
        }
        if feature_test[feature][1] == "num":
            test_info[feature]["prod_hist_data"] = (
                [
                    t.tolist()
                    for t in np.histogram(
                        production_data[feature][np.isfinite(production_data[feature])],
                        bins=10,
                        density=True,
                    )
                ],
            )
            test_info[feature]["ref_hist_data"] = [
                t.tolist()
                for t in np.histogram(
                    reference_data[feature][np.isfinite(reference_data[feature])],
                    bins=10,
                    density=True,
                )
            ]
        if feature_test[feature][1] == "cat":
            ref_counts = ref_feature.value_counts(sort=False)
            prod_counts = prod_feature.value_counts(sort=False)
            keys = set(ref_counts.keys()).union(set(prod_counts.keys()))
            for key in keys:
                if key not in ref_counts:
                    ref_counts[key] = 0
                if key not in prod_counts:
                    prod_counts[key] = 0
            test_info[feature]["ref_hist_data"] = list(
                reversed(
                    list(
                        map(list, zip(*sorted(ref_counts.items(), key=lambda x: x[0])))  # type: ignore
                    )
                )
            )
            test_info[feature]["prod_hist_data"] = list(
                reversed(
                    list(
                        map(list, zip(*sorted(prod_counts.items(), key=lambda x: x[0])))  # type: ignore
                    )
                )
            )
            # test_info[feature]["prod_hist_data"] = prod_small_hist
            # test_info[feature]["ref_hist_data"] = ref_small_hist
    return test_info


def get_stattest(
    feature_type: str, ref_feature: pd.Series, prod_feature: pd.Series
) -> str:
    n_values = pd.concat([ref_feature, prod_feature]).nunique()
    if ref_feature.shape[0] <= 1000:
        if feature_type == "num":
            if n_values <= 5:
                return "chi_stat_test" if n_values > 2 else "z_stat_test"
            elif n_values > 5:
                return "ks_stat_test"
        elif feature_type == "cat":
            return "chi_stat_test" if n_values > 2 else "z_stat_test"
    elif ref_feature.shape[0] > 1000:
        if feature_type == "num":
            if n_values <= 5:
                return "jensenshannon_stat_test"
            elif n_values > 5:
                return "wasserstein_stat_test"
        elif feature_type == "cat":
            return "jensenshannon_stat_test"
    raise ValueError(f"Unexpected feature_type {feature_type}")


def recognize_task(target_name: str, reference_data: pd.DataFrame) -> str:
    """Try to guess about the target type:
    if the target has a numeric type and number of unique values > 5: task == ‘regression’
    in all other cases task == ‘classification’.

    Args:
        target_name: name of target column.
        reference_data: usually the data which you used in reference.

    Returns:
        Task parameter.
    """
    return (
        "regression"
        if (
            pd.api.types.is_numeric_dtype(reference_data[target_name])
            and reference_data[target_name].nunique() >= 5
        )
        else "classification"
    )
