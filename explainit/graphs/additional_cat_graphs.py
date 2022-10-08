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


def generate_additional_graph_cat_feature(name, reference_data, production_data):

    fig1 = go.Figure()
    feature_ref_data = reference_data.dropna()
    feature_prod_data = production_data.dropna()
    reference_data_to_plot = list(
        reversed(list(map(list, zip(*feature_ref_data.value_counts().items()))))
    )
    production_data_to_plot = list(
        reversed(list(map(list, zip(*feature_prod_data.value_counts().items()))))
    )
    fig1.add_trace(
        go.Bar(
            x=reference_data_to_plot[1],
            y=reference_data_to_plot[0],
            marker_color="#2ECC71",
            opacity=0.6,
            name="Reference",
        )
    )

    fig1.add_trace(
        go.Bar(
            x=production_data_to_plot[1],
            y=production_data_to_plot[0],
            marker_color="#ed0400",
            opacity=0.6,
            name="Production",
        )
    )
    fig1.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=name,
        yaxis_title="Share",
    )
    fig1.update_layout(
        title={
            "text": f"{name} Distribution".upper(),
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        }
    )

    # Pie Chart Graph.
    prod_labels = production_data.value_counts().sort_index().index.tolist()
    prod_values = production_data.value_counts().sort_index().values.tolist()
    ref_labels = reference_data.value_counts().sort_index().index.tolist()
    ref_values = reference_data.value_counts().sort_index().values.tolist()

    fig2 = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
    )
    fig2.add_trace(go.Pie(labels=ref_labels, values=ref_values, name="Reference"), 1, 1)
    fig2.add_trace(
        go.Pie(labels=prod_labels, values=prod_values, name="Production"), 1, 2
    )

    # Use `hole` to create a donut-like pie chart
    fig2.update_traces(hole=0.4, hoverinfo="label+percent+name")

    fig2.update_layout(
        #     title_text="Grade ",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text="Reference", x=0.16, y=0.5, font_size=20, showarrow=False),
            dict(text="Production", x=0.825, y=0.5, font_size=20, showarrow=False),
        ]
    )

    # distr_graph, pie_graph
    return fig_to_json(fig1), fig_to_json(fig2)
