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
import plotly.graph_objs as go
from explainit.graphs.additional_num_graphs import fig_to_json
from plotly.subplots import make_subplots


def generate_additional_graph_cat_feature(name, reference_data, current_data):

    fig = go.Figure()
    feature_ref_data = reference_data.dropna()
    feature_cur_data = current_data.dropna()
    reference_data_to_plot = list(
        reversed(list(map(list, zip(*feature_ref_data.value_counts().items()))))
    )
    current_data_to_plot = list(
        reversed(list(map(list, zip(*feature_cur_data.value_counts().items()))))
    )
    fig.add_trace(
        go.Bar(
            x=reference_data_to_plot[1],
            y=reference_data_to_plot[0],
            marker_color="#4d4d4d",
            opacity=0.6,
            name="Reference",
        )
    )

    fig.add_trace(
        go.Bar(
            x=current_data_to_plot[1],
            y=current_data_to_plot[0],
            marker_color="#ed0400",
            opacity=0.6,
            name="Current",
        )
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=name,
        yaxis_title="Share",
    )
    fig.update_layout(
        title={
            "text": f"{name} Distribution".upper(),
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        }
    )

    distr_graph = fig_to_json(fig)

    # Pie Chart Graph.
    labels = current_data.value_counts().sort_index().index.tolist()
    cur_values = current_data.value_counts().sort_index().values.tolist()
    ref_values = reference_data.value_counts().sort_index().values.tolist()

    fig = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
    )
    fig.add_trace(go.Pie(labels=labels, values=ref_values, name="Reference"), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=cur_values, name="Current"), 1, 2)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=0.4, hoverinfo="label+percent+name")

    fig.update_layout(
        #     title_text="Grade ",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text="Reference", x=0.125, y=0.5, font_size=20, showarrow=False),
            dict(text="Current", x=0.825, y=0.5, font_size=20, showarrow=False),
        ]
    )

    pie_graph = fig_to_json(fig)

    return distr_graph, pie_graph
