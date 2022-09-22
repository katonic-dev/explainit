from typing import Union

import numpy as np
import pandas as pd


def df_stats(ref_data, columns, target_column=None, date_column=None):
    result = {}

    def get_percentage_from_all_values(value: Union[int, float]):
        all_values_count = ref_data.shape[0]
        return np.round(100 * value / all_values_count, 2)

    if target_column is not None:
        result["target column"] = target_column
    else:
        result["target column"] = target_column
    if date_column:
        result["date column"] = date_column
    else:
        result["date column"] = date_column
    result["number of variables"] = len(columns)
    result["number of observations"] = ref_data.shape[0]
    missing_cells = ref_data[columns].isnull().sum().sum()
    missing_cells_percentage = np.round(
        missing_cells
        / (result["number of variables"] * result["number of observations"]),
        2,
    )
    result["missing cells"] = f"{missing_cells} ({missing_cells_percentage}%)"

    constant_values = pd.Series(
        [
            get_percentage_from_all_values(
                ref_data[x].value_counts(dropna=False).iloc[0]
            )
            for x in columns
        ]
    )
    empty_values = pd.Series(
        [ref_data[x].isnull().sum() / ref_data.shape[0] * 100 for x in columns]
    )
    result["constant features"] = (constant_values == 100).sum()
    result["empty features"] = (empty_values == 100).sum()
    result["almost constant features"] = (constant_values >= 95).sum()
    result["almost empty features"] = (empty_values >= 95).sum()
    return result
