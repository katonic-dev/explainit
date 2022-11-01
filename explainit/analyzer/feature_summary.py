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
    result["Count"] = int(feature.count())
    result["Missing"] = f"{missing_count} ({missing_percentage}%)"
    result["Unique_count"] = feature.nunique()
    result["Unique_count (%)"] = f"{get_percentage_from_all_values(feature.nunique())}%"
    most_common_value = value_counts.index[0]
    result[
        "Most_common"
    ] = f"{most_common_value} ({get_percentage_from_all_values(value_counts.iloc[0])}%)"

    if result["Count"] > 0 and pd.isnull(most_common_value):
        result[
            "2nd_most_common"
        ] = f"{value_counts.index[1]} ({get_percentage_from_all_values(value_counts.iloc[1])}%)"

    if feature_type == "num":
        # round most common feature value for numeric features to 1e-5
        if not np.issubdtype(feature, np.number):
            feature = feature.astype(float)
        infinite_count = int(np.sum(np.isinf(feature)))
        infinite_percentage = get_percentage_from_all_values(infinite_count)
        result["Infinite"] = f"{infinite_count} ({infinite_percentage}%)"
        result["Max"] = np.round(feature.max(), 4)
        result["Min"] = np.round(feature.min(), 4)
        common_stats = dict(feature.describe())
        result["Std"] = np.round(common_stats["std"], 4)
        result["Mean"] = np.round(common_stats["mean"], 4)
        result["Percentile_25"] = np.round(common_stats["25%"], 4)
        result["Percentile_50"] = np.round(common_stats["50%"], 4)
        result["Percentile_75"] = np.round(common_stats["75%"], 4)

    # TODO: Add categorical properties
    return result


def additional_cat_stats(
    ref_feature_data: pd.Series,
    prod_feature_data: pd.Series,
    cat_feature_stats: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    feature_stats: Dict[str, Any] = cat_feature_stats[ref_feature_data.name]

    production_values_set = set(prod_feature_data.unique())
    reference_values_set = set(ref_feature_data.unique())
    unique_in_production = production_values_set - reference_values_set
    unique_in_reference = reference_values_set - production_values_set

    feature_stats["new_in_production_values_count"] = len(
        unique_in_production
    )  # new_in_production_values_count
    feature_stats["unused_in_production_values_count"] = len(
        unique_in_reference
    )  # unused_in_production_values_count

    return feature_stats


def make_feature_stats_dataframe(
    column_name: str,
    prod_cat_stats: Dict[str, Dict[str, Any]],
    prod_num_stats: Dict[str, Dict[str, Any]],
    ref_cat_stats: Dict[str, Dict[str, Any]],
    ref_num_stats: Dict[str, Dict[str, Any]],
) -> pd.DataFrame:
    if column_name in prod_cat_stats and column_name in ref_cat_stats:
        feats_df = pd.concat(
            [
                pd.DataFrame(ref_cat_stats[column_name], index=[0]),
                pd.DataFrame(prod_cat_stats[column_name], index=[0]),
            ]
        ).T
        feats_df.columns = ["Reference", "Production"]
    if column_name in prod_num_stats and column_name in ref_num_stats:
        feats_df = pd.concat(
            [
                pd.DataFrame(ref_num_stats[column_name], index=[0]),
                pd.DataFrame(prod_num_stats[column_name], index=[0]),
            ]
        ).T
        feats_df.columns = ["Reference", "Production"]
    feats_df.reset_index(inplace=True)
    feats_df.rename(columns={"index": "Metrics"}, inplace=True)
    return feats_df

    # TODO: Add else condition for feature stats.
