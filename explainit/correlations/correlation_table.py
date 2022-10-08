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

import numpy as np
import pandas as pd


def get_df_corr_features_sorted(df_corr: pd.DataFrame) -> pd.DataFrame:
    df_corr = df_corr.stack().reset_index()
    df_corr.columns = ["col_1", "col_2", "value"]
    df_corr["value"] = np.round(df_corr["value"], 3)
    df_corr["abs_value"] = np.abs(df_corr["value"])
    df_corr = df_corr.sort_values(["col_1", "col_2"])
    df_corr["keep"] = df_corr["col_1"].str.get(0) < df_corr["col_2"].str.get(0)
    df_corr = df_corr[df_corr["keep"]]
    df_corr = df_corr.sort_values("abs_value", ascending=False)
    df_corr["features"] = df_corr["col_1"] + ", " + df_corr["col_2"]
    return df_corr[["features", "value"]]


def get_rel_diff_corr_features_sorted(
    ref_corr: pd.DataFrame, prod_corr: pd.DataFrame
) -> pd.DataFrame:
    ref_corr = get_df_corr_features_sorted(ref_corr).rename(
        columns={"value": "value_ref"}
    )
    prod_corr = get_df_corr_features_sorted(prod_corr).rename(
        columns={"value": "value_prod"}
    )
    com_corr = ref_corr.merge(prod_corr, on="features", how="left")
    com_corr["value_diff"] = np.round(
        (com_corr["value_ref"] - com_corr["value_prod"]), 3
    )
    com_corr["abs_value_diff"] = np.abs(com_corr["value_diff"])
    com_corr = com_corr.sort_values("abs_value_diff", ascending=False)
    return com_corr[["features", "value_ref", "value_prod", "value_diff"]]


def make_metrics(
    reference_correlations: Dict[str, pd.DataFrame],
    production_correlations: Dict[str, pd.DataFrame],
):
    metrics = []
    if reference_correlations["spearman"].shape[0] > 1:
        com_num_corr = get_rel_diff_corr_features_sorted(
            reference_correlations["spearman"], production_correlations["spearman"]
        )
    else:
        com_num_corr = pd.DataFrame()
    if reference_correlations["cramer_v"].shape[0] > 1:
        com_cat_corr = get_rel_diff_corr_features_sorted(
            reference_correlations["cramer_v"], production_correlations["cramer_v"]
        )
    else:
        com_cat_corr = pd.DataFrame()
    for i in range(5):
        values = ["-", "-", "-", "-", "-", "-", "-", "-"]
        if i < com_cat_corr.shape[0]:
            values[0] = com_cat_corr.iloc[i, 0]
            values[1] = com_cat_corr.iloc[i, 1]
            values[2] = com_cat_corr.iloc[i, 2]
            values[3] = com_cat_corr.iloc[i, 3]
        if i < com_num_corr.shape[0]:
            values[4] = com_num_corr.iloc[i, 0]
            values[5] = com_num_corr.iloc[i, 1]
            values[6] = com_num_corr.iloc[i, 2]
            values[7] = com_num_corr.iloc[i, 3]
        metrics.append(
            {"label": "", "values": values},
        )
    return metrics
