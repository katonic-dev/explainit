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
import numpy as np
import plotly.graph_objs as go

DEFAULT_CONF_INTERVAL_SIZE = 1


def fig_to_json(figure: go.Figure):
    result = figure.to_plotly_json()
    result["layout"].pop("template", None)
    return result


def generate_additional_graph_num_feature(
    feature_name, reference_data, current_data, date_column=None
):
    fig1 = go.Figure()

    fig1.add_trace(
        go.Histogram(
            x=reference_data.tolist(),
            marker_color="#48DD2D",
            opacity=0.6,
            xbins=None,
            nbinsx=10,
            name="Training",
            histnorm="probability",
        )
    )

    fig1.add_trace(
        go.Histogram(
            x=current_data.tolist(),
            marker_color="#ed0400",
            opacity=0.6,
            xbins=None,
            nbinsx=10,
            name="Testing",
            histnorm="probability",
        )
    )
    fig1.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=feature_name,
        yaxis_title="Share",
    )

    fig1.update_layout(
        title={
            "text": f"{feature_name} Distribution".upper(),
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        }
    )

    # Plot Drift

    reference_mean = np.mean(reference_data[np.isfinite(reference_data)])
    reference_std = np.std(reference_data[np.isfinite(reference_data)], ddof=1)
    x_title = "Timestamp" if date_column else "Index"

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scattergl(
            x=date_column.to_list() if date_column else current_data.index.tolist(),
            y=current_data.tolist(),
            mode="markers",
            name="Testing Data Points",
            marker=dict(size=6, color="#ed0400"),
        )
    )

    if date_column:
        x0 = date_column.sort_values()[1].tolist()
    else:
        x0 = current_data.index.sort_values()[1].tolist()

    fig2.add_trace(
        go.Scattergl(
            x=[x0, x0],
            y=[
                reference_mean - DEFAULT_CONF_INTERVAL_SIZE * reference_std,
                reference_mean + DEFAULT_CONF_INTERVAL_SIZE * reference_std,
            ],
            mode="markers",
            name="Testing",
            marker=dict(size=0.01, color="white", opacity=0.005),
            showlegend=False,
        )
    )

    fig2.update_layout(
        xaxis_title=x_title,
        yaxis_title=feature_name,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        shapes=[
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="paper",
                # y-reference is assigned to the plot paper [0,1]
                yref="y",
                x0=0,
                y0=reference_mean - DEFAULT_CONF_INTERVAL_SIZE * reference_std,
                x1=1,
                y1=reference_mean + DEFAULT_CONF_INTERVAL_SIZE * reference_std,
                fillcolor="#48DD2D",
                opacity=0.5,
                layer="below",
                line_width=0,
            ),
            dict(
                type="line",
                name="Training",
                xref="paper",
                yref="y",
                x0=0,  # min(testset_agg_by_date.index),
                y0=reference_mean,
                x1=1,  # max(testset_agg_by_date.index),
                y1=reference_mean,
                line=dict(color="green", width=3),
            ),
        ],
    )

    # distr_figure, drift_figure
    return fig_to_json(fig1), fig_to_json(fig2)
