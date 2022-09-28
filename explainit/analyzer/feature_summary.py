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
from typing import Any
from typing import Dict
from typing import Union

import numpy as np
import pandas as pd


def feature_summary_stats(feature: pd.Series, feature_type: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {}

    def get_percentage_from_all_values(value: Union[int, float]):
        all_values_count = feature.shape[0]
        return np.round(100 * value / all_values_count, 2)

    missing_count = int(feature.isnull().sum())
    value_counts = feature.value_counts(dropna=False)
    missing_percentage = np.round(100 * missing_count / feature.shape[0], 2)
    result["count"] = int(feature.count())
    result["missing"] = f"{missing_count} ({missing_percentage}%)"
    result["unique_count"] = feature.nunique()
    result["unique_count (%)"] = f"{get_percentage_from_all_values(feature.nunique())}%"
    most_common_value = value_counts.index[0]
    result[
        "most_common"
    ] = f"{most_common_value} ({get_percentage_from_all_values(value_counts.iloc[0])}%)"

    if result["count"] > 0 and pd.isnull(most_common_value):
        result[
            "2nd_most_common"
        ] = f"{value_counts.index[1]} ({get_percentage_from_all_values(value_counts.iloc[1])}%)"

    if feature_type == "num":
        # round most common feature value for numeric features to 1e-5
        if not np.issubdtype(feature, np.number):
            feature = feature.astype(float)
        infinite_count = int(np.sum(np.isinf(feature)))
        infinite_percentage = get_percentage_from_all_values(infinite_count)
        result["infinite"] = f"{infinite_count} ({infinite_percentage}%)"
        result["max"] = np.round(feature.max(), 4)
        result["min"] = np.round(feature.min(), 4)
        common_stats = dict(feature.describe())
        result["std"] = np.round(common_stats["std"], 4)
        result["mean"] = np.round(common_stats["mean"], 4)
        result["percentile_25"] = np.round(common_stats["25%"], 4)
        result["percentile_50"] = np.round(common_stats["50%"], 4)
        result["percentile_75"] = np.round(common_stats["75%"], 4)

    # TODO: Add categorical properties
    return result


def additional_cat_stats(
    ref_feature_data: pd.Series,
    cur_feature_data: pd.Series,
    cat_feature_stats: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    feature_stats: Dict[str, Any] = cat_feature_stats[ref_feature_data.name]

    current_values_set = set(cur_feature_data.unique())
    reference_values_set = set(ref_feature_data.unique())
    unique_in_current = current_values_set - reference_values_set
    unique_in_reference = reference_values_set - current_values_set

    feature_stats["new_in_current_values_count"] = len(
        unique_in_current
    )  # new_in_current_values_count
    feature_stats["unused_in_current_values_count"] = len(
        unique_in_reference
    )  # unused_in_current_values_count

    return feature_stats


def make_feature_stats_dataframe(
    column_name, cur_cat_stats, cur_num_stats, ref_cat_stats, ref_num_stats
) -> pd.DataFrame:
    if column_name in cur_cat_stats.keys() and ref_cat_stats.keys():
        feats_df = pd.concat(
            [
                pd.DataFrame(ref_cat_stats[column_name], index=[0]),
                pd.DataFrame(cur_cat_stats[column_name], index=[0]),
            ]
        ).T
        feats_df.columns = ["Training", "Testing"]
        return feats_df
    if column_name in cur_num_stats.keys() and ref_num_stats.keys():
        feats_df = pd.concat(
            [
                pd.DataFrame(ref_num_stats[column_name], index=[0]),
                pd.DataFrame(cur_num_stats[column_name], index=[0]),
            ]
        ).T
        feats_df.columns = ["Training", "Testing"]
        return feats_df
