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
from typing import Dict

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_correlation_figure(
    kind: str,
    reference_correlations: Dict[str, pd.DataFrame],
    production_correlations: Dict[str, pd.DataFrame],
):
    columns = reference_correlations[kind].columns
    heatmap_text = None
    heatmap_texttemplate = None
    cols = 2
    subplot_titles = ["reference", "production"]

    fig = make_subplots(
        rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True
    )
    if len(columns) < 15:
        heatmap_text = np.round(reference_correlations[kind], 2).astype(str)
        heatmap_texttemplate = "%{text}"

    trace = go.Heatmap(
        z=reference_correlations[kind],
        x=columns,
        y=columns,
        text=heatmap_text,
        texttemplate=heatmap_texttemplate,
        coloraxis="coloraxis",
    )
    fig.append_trace(trace, 1, 1)
    if production_correlations is not None:
        if len(columns) < 15:
            heatmap_text = np.round(production_correlations[kind], 2).astype(str)
            heatmap_texttemplate = "%{text}"

        trace = go.Heatmap(
            z=production_correlations[kind],
            x=columns,
            y=columns,
            text=heatmap_text,
            texttemplate=heatmap_texttemplate,
            coloraxis="coloraxis",
        )
        fig.append_trace(trace, 1, 2)
    fig.update_layout(coloraxis={"colorscale": "RdBu_r"})
    return json.loads(fig.to_json())  # Correlation Graph Data
