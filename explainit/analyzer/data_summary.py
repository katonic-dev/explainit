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


def data_summary_stats(data: pd.DataFrame, target_column=None, date_column=None):
    result: Dict[str, Any] = {}

    def get_percentage_from_all_values(value: Union[int, float]):
        all_values_count = data.shape[0]
        return np.round(100 * value / all_values_count, 2)

    result["Target column"] = target_column
    result["Date column"] = date_column
    result["Number of variables"] = len(data.columns)
    result["Number of observations"] = data.shape[0]
    missing_cells = data.isnull().sum().sum()
    missing_cells_percentage = np.round(
        missing_cells
        / (result["Number of variables"] * result["Number of observations"]),
        2,
    )
    result["Missing cells"] = f"{missing_cells} ({missing_cells_percentage}%)"

    constant_values = pd.Series(
        [
            get_percentage_from_all_values(data[x].value_counts(dropna=False).iloc[0])
            for x in data.columns
        ]
    )
    empty_values = pd.Series(
        [data[x].isnull().sum() / data.shape[0] * 100 for x in data.columns]
    )
    result["Constant features"] = (constant_values == 100).sum()
    result["Empty features"] = (empty_values == 100).sum()
    result["Almost constant features"] = (constant_values >= 95).sum()
    result["Almost empty features"] = (empty_values >= 95).sum()
    return result
