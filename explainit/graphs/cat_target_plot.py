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


def cat_target_main_graph(ref_target_data, prod_target_data):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=ref_target_data.tolist(),
            marker_color="#48DD2D",
            opacity=0.6,
            nbinsx=10,
            name="Reference",
            histnorm="probability",
        )
    )

    fig.add_trace(
        go.Histogram(
            x=prod_target_data.tolist(),
            marker_color="#ed0400",
            opacity=0.6,
            nbinsx=10,
            name="Production",
            histnorm="probability",
        )
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=ref_target_data.name,
        yaxis_title="Share",
    )
    return fig_to_json(fig)
