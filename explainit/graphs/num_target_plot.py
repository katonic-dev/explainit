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
import plotly.figure_factory as ff
from explainit.graphs.additional_num_graphs import fig_to_json


def num_target_main_graph(reference_data_to_plot, production_data_to_plot):

    output_distr = ff.create_distplot(
        [reference_data_to_plot, production_data_to_plot],
        ["Reference", "Production"],
        colors=["#4d4d4d", "#ed0400"],
        show_rug=True,
    )

    output_distr.update_layout(
        xaxis_title="Value",
        yaxis_title="Share",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig_data = fig_to_json(output_distr)
    fig_data["data"][2]["y"] = fig_data["data"][2]["y"].tolist()
    fig_data["data"][3]["y"] = fig_data["data"][3]["y"].tolist()
    return fig_data
