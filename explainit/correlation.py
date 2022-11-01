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
from dash import dash_table
from dash import html


def correlation_data_table(corr_df):
    """
    A method which will generate a Dash data table with correlation data.

    Args:
        Data which contains all the information correlation inside the reference and production data.

    Returns:
        Dash Data table with correlation data.
    """

    return [
        html.Div(
            html.H6(
                "Correlations Table",
                style={"textAlign": "center", "font-weight": "bold"},
            )
        ),
        html.Div(
            children=[
                dash_table.DataTable(
                    data=corr_df.to_dict("records"),
                    columns=[{"id": c, "name": c} for c in corr_df.columns],
                    style_cell={"textAlign": "left"},
                    style_cell_conditional=[
                        {"if": {"column_id": c}, "textAlign": "left"}
                        for c in ["Date", "Region", "Tests"]
                    ],
                    style_data={
                        "border": "1px solid black",
                        "color": "black",
                        "backgroundColor": "white",
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgb(220, 220, 220)",
                        }
                    ],
                    style_header={
                        "border": "1px solid black",
                        "backgroundColor": "black",
                        "color": "white",
                        "fontWeight": "bold",
                    },
                ),
            ],
            style={"margin-top": "10px", "justify": "center"},
        ),
        html.Hr(),
    ]
