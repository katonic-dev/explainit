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
from typing import Callable
from typing import List
from typing import Union

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


def select_features_for_corr(
    num_feats: List[str], cat_feats: List[str], ref_feat_stats
) -> List[List[str]]:
    """Define which features should be used for calculating correlation matrices:
        - for pearson, spearman, and kendall correlation matrices we select numerical features which have > 1
            unique values;
        - for kramer_v correlation matrix, we select categorical features which have > 1 unique values.
    Args:
        num_feats: all numeric features
        cat_feats: all categorical features
        ref_feat_stats: all features data quality metrics.
    Returns:
        num_for_corr: list of feature names for pearson, spearman, and kendall correlation matrices.
        cat_for_corr: list of feature names for kramer_v correlation matrix.
    """
    num_for_corr = []
    for feature in num_feats:
        unique_count = ref_feat_stats[feature]["unique_count"]
        if unique_count and unique_count > 1:
            num_for_corr.append(feature)
    cat_for_corr = []
    for feature in cat_feats:
        unique_count = ref_feat_stats[feature]["unique_count"]
        if unique_count and unique_count > 1:
            cat_for_corr.append(feature)

    return [num_for_corr, cat_for_corr]


def cramer_v(x: pd.Series, y: pd.Series) -> Union[float, Any]:
    """Calculate Cramér's V: a measure of association between two nominal variables.
    Args:
        x: The array of observed values.
        y: The array of observed values.
    Returns:
        Value of the Cramér's V
    """
    arr = pd.crosstab(x, y).values
    chi2_stat = chi2_contingency(arr, correction=False)
    phi2 = chi2_stat[0] / arr.sum()
    n_rows, n_cols = arr.shape
    return (
        np.nan
        if min(n_cols - 1, n_rows - 1) == 0
        else np.sqrt(phi2 / min(n_cols - 1, n_rows - 1))
    )


def corr_matrix(
    df: pd.Series, func: Callable[[pd.Series, pd.Series], float]
) -> pd.DataFrame:
    """Compute pairwise correlation of columns
    Args:
        df: initial data frame.
        func: function for computing pairwise correlation.
    Returns:
        Correlation matrix.
    """
    K = df.shape[1]
    if K <= 1:
        return pd.DataFrame()

    corr_array = np.eye(K)
    columns = df.columns
    for i in range(K):
        for j in range(K):
            if i <= j:
                continue
            c = func(df[columns[i]], df[columns[j]])
            corr_array[i, j] = c
            corr_array[j, i] = c
    return pd.DataFrame(data=corr_array, columns=columns, index=columns)


def calculate_correlations(
    df: pd.DataFrame, num_for_corr: List[str], cat_for_corr: List[str], kind: str
):
    """Calculate correlation matrix depending on the kind parameter
    Args:
        df: initial data frame.
        num_for_corr: list of feature names for pearson, spearman, and kendall correlation matrices.
        cat_for_corr: list of feature names for kramer_v correlation matrix.
        kind: Method of correlation:
            - pearson - standard correlation coefficient
            - kendall - Kendall Tau correlation coefficient
            - spearman - Spearman rank correlation
            - cramer_v - Cramer’s V measure of association
    Returns:
        Correlation matrix.
    """
    if kind == "cramer_v":
        return corr_matrix(df[cat_for_corr], cramer_v)
    elif kind == "kendall":
        return df[num_for_corr].corr("kendall")
    elif kind == "pearson":
        return df[num_for_corr].corr("pearson")
    elif kind == "spearman":
        return df[num_for_corr].corr("spearman")
