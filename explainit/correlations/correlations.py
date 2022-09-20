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
        reference_features_stats: all features data quality metrics.
        target_name: name of target column.
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
    if min(n_cols - 1, n_rows - 1) == 0:
        value = np.nan
    else:
        value = np.sqrt(phi2 / min(n_cols - 1, n_rows - 1))

    return value


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
    columns = df.columns
    K = df.shape[1]
    if K <= 1:
        return pd.DataFrame()
    else:
        corr_array = np.eye(K)

        for i in range(K):
            for j in range(K):
                if i <= j:
                    continue
                c = func(df[columns[i]], df[columns[j]])
                corr_array[i, j] = c
                corr_array[j, i] = c
        return pd.DataFrame(data=corr_array, columns=columns, index=columns)


def calculate_correlations(df, num_for_corr, cat_for_corr, kind):
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
    if kind == "pearson":
        return df[num_for_corr].corr("pearson")
    elif kind == "spearman":
        return df[num_for_corr].corr("spearman")
    elif kind == "kendall":
        return df[num_for_corr].corr("kendall")
    elif kind == "cramer_v":
        return corr_matrix(df[cat_for_corr], cramer_v)
