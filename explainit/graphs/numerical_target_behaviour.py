import json

import plotly.graph_objs as go
from plotly.subplots import make_subplots


def numerical_target_behaviour_on_features(
    reference_feature_data,
    current_feature_data,
    reference_target_data,
    current_target_data,
):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

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
            x=current_feature_data.tolist(),
            y=current_target_data.tolist(),
            mode="markers",
            name="Target (curr)",
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
    fig_json = json.loads(fig.to_json())
    return fig_json
