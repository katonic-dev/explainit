from typing import Any
from typing import Dict
from typing import Union

import numpy as np
import pandas as pd


def feature_stats(feature, feature_type):
    def get_percentage_from_all_values(value: Union[int, float]):
        return np.round(100 * value / all_values_count, 2)

    result: Dict[str, Any] = {}

    missing_count = int(feature.isnull().sum())
    result["count"] = int(feature.count())
    all_values_count = feature.shape[0]
    value_counts = feature.value_counts(dropna=False)
    missing_percentage = np.round(100 * missing_count / all_values_count, 2)
    result["missing"] = f"{missing_count} ({missing_percentage}%)"
    unique_count: int = feature.nunique()
    result["unique_count"] = unique_count
    result[
        "unique"
    ] = f"{unique_count} ({get_percentage_from_all_values(unique_count)}%)"
    most_common_value = value_counts.index[0]
    result[
        "most_common"
    ] = f"{most_common_value} ({get_percentage_from_all_values(value_counts.iloc[0])}%)"

    if result["count"] > 0 and pd.isnull(most_common_value):
        result["most_common_not_null_value"] = value_counts.index[1]
        result[
            "most_common_not_null_value_percentage"
        ] = get_percentage_from_all_values(value_counts.iloc[1])

    if feature_type == "num":
        # round most common feature value for numeric features to 1e-5
        if not np.issubdtype(feature, np.number):
            feature = feature.astype(float)
        result["most_common_value"] = np.round(most_common_value, 5)
        infinite_count = int(np.sum(np.isinf(feature)))
        infinite_percentage = get_percentage_from_all_values(infinite_count)
        result["infinite"] = f"{infinite_count} ({infinite_percentage}%)"
        result["max"] = np.round(feature.max(), 2)
        result["min"] = np.round(feature.min(), 2)
        common_stats = dict(feature.describe())
        std = common_stats["std"]
        result["std"] = np.round(std, 2)
        result["mean"] = np.round(common_stats["mean"], 2)
        result["percentile_25"] = np.round(common_stats["25%"], 2)
        result["percentile_50"] = np.round(common_stats["50%"], 2)
        result["percentile_75"] = np.round(common_stats["75%"], 2)

    return result


def additional_cur_cat_stats(ref_feature_data, cur_feature_data, cur_cat_feature_stats):
    cur_feature_stats = cur_cat_feature_stats[ref_feature_data.name]
    current_values_set = set(cur_feature_data.unique())

    reference_values_set = set(ref_feature_data.unique())

    unique_in_current = current_values_set - reference_values_set
    new_in_current_values_count: int = len(unique_in_current)
    unique_in_reference = reference_values_set - current_values_set
    unused_in_current_values_count: int = len(unique_in_reference)
    cur_feature_stats.update(
        {"new_in_current_values_count": new_in_current_values_count}
    )
    cur_feature_stats.update(
        {"unused_in_current_values_count": unused_in_current_values_count}
    )
    return cur_cat_feature_stats


def make_feature_stats_dataframe(
    column_name, cur_cat_stats, cur_num_stats, ref_cat_stats, ref_num_stats
):
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
