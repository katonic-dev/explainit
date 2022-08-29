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
import copy


def get_json_data(data):
    """
    Segregate the data into individual chunks.

    Args:
        Dictionary which contains the data.

    Returns:
        Multiple dictionaries containing specific information about the drift and quality of the data.
    """
    drift = data["data_drift"]
    target = data["target_drift"]
    data_info = data["data_summary"]
    feature_info = data["feature_summary"]
    correlation_info = data["correlation"]
    return drift, target, data_info, feature_info, correlation_info


def get_small_hist_data(data, key):
    """
    Extract the data needed to generate the small histogram for the given key.

    Args:
        data: A dictionary containing drift data.
        key: feature name.
    Returns:
        Information regarding histograms.
    """
    small_hist_data = {}
    for feature in data["widgets"][0]["params"]["data"]:
        if "target" not in feature["f1"]:
            small_hist_data.update(
                {feature["f1"]: {"x": feature[key]["x"], "y": feature[key]["y"]}}
            )
        else:
            small_hist_data.update(
                {feature["f1"]: {"x": feature[key]["x"], "y": feature[key]["y"]}}
            )
    return small_hist_data


def get_stats_data(data):
    """
    Extracts only the Statistical tests information from the entire given data.

    Args:
        data: Dictionary which contains the entire information regarding Drift.
    """
    columns_data = data["widgets"][0]["params"]["data"]
    return {
        feature["f1"]: {
            "column_type": feature["f6"],
            "stats_test": feature["stattest_name"],
            "drift": feature["f2"],
            "P-Value": feature["f5"],
        }
        for feature in columns_data
    }


def get_drift_graph_data(data):
    """
    Extracts the only infromation that needed to create the Drift Graphs.
    """
    return {
        feature["id"]: feature["params"]["params"]
        for feature in data["widgets"][0]["additionalGraphs"]
        if "drift" in feature["id"]
    }


def get_distr_graph_data(data):
    """
    Extracts the only infromation that needed to create the Distribution Graphs.
    """
    return {
        feature["id"]: feature["params"]
        for feature in data["widgets"][0]["additionalGraphs"]
        if "distr" in feature["id"]
    }


def target_data_copy(data):
    """
    Creates a copy of the target drift data.
    """
    return (
        copy.deepcopy(data["widgets"][1]["additionalGraphs"])
        if len(data["widgets"]) == 2
        else copy.deepcopy(data["widgets"][3]["additionalGraphs"])
    )
