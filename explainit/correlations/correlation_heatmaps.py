import json
from typing import Dict

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_correlation_figure(
    kind: str,
    reference_correlations: Dict[str, pd.DataFrame],
    current_correlations: Dict[str, pd.DataFrame],
):
    columns = reference_correlations[kind].columns
    heatmap_text = None
    heatmap_texttemplate = None
    cols = 2
    subplot_titles = ["training", "testing"]

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
    if current_correlations is not None:
        if len(columns) < 15:
            heatmap_text = np.round(current_correlations[kind], 2).astype(str)
            heatmap_texttemplate = "%{text}"

        trace = go.Heatmap(
            z=current_correlations[kind],
            x=columns,
            y=columns,
            text=heatmap_text,
            texttemplate=heatmap_texttemplate,
            coloraxis="coloraxis",
        )
        fig.append_trace(trace, 1, 2)
    fig.update_layout(coloraxis={"colorscale": "RdBu_r"})
    return json.loads(fig.to_json())  # Correlation Graph Data
