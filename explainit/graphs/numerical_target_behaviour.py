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
import json

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def numerical_target_behaviour_on_features(
    reference_feature_data: pd.Series,
    production_feature_data: pd.Series,
    reference_target_data: pd.Series,
    production_target_data: pd.Series,
):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Production"))

    fig.add_trace(
        go.Scattergl(
            x=reference_feature_data.tolist(),
            y=reference_target_data.tolist(),
            mode="markers",
            name="Target (ref)",
            marker=dict(size=6, color="#ed0400"),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=production_feature_data.tolist(),
            y=production_target_data.tolist(),
            mode="markers",
            name="Target (prod)",
            marker=dict(size=6, color="#ed0400"),
        ),
        row=1,
        col=2,
    )

    # Update xaxis properties
    fig.update_xaxes(
        title_text=reference_feature_data.name, showgrid=True, row=1, col=1
    )
    fig.update_xaxes(
        title_text=reference_feature_data.name, showgrid=True, row=1, col=2
    )

    # Update yaxis properties
    fig.update_yaxes(title_text="Value", showgrid=True, row=1, col=1)
    fig.update_yaxes(title_text="Value", showgrid=True, row=1, col=2)
    return json.loads(fig.to_json())
