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
import pathlib

import pandas as pd
from dash import dash_table
from dash import dcc
from dash import html


stats_df = pd.read_csv(
    f"{pathlib.Path(__file__).parent.absolute()}/assets/stat-tests-conditions.csv",
    index_col=None,
)


def generate_workflow():
    return html.Div(
        id="markdown2",
        className="modal",
        children=(
            html.Div(
                id="markdown-container2",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "X",
                            id="workflow_close",
                            n_clicks=0,
                            className="closeButton",
                            style={"font-size": "25px"},
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### What is this app about?
                        This is a Business Intelligence Web Application for Monitoring and Understanding How your Data and Target is.

                        ###### What does this app shows?
                        1. Data Drift
                        2. Target Drift
                        3. Data Quality, for both Training & Production/Current Data
                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )


def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "X",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                            style={"font-size": "25px"},
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=[
                            dash_table.DataTable(
                                data=stats_df.to_dict("records"),
                                columns=[
                                    {"id": c, "name": c} for c in stats_df.columns
                                ],
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
                                    "backgroundColor": "rgb(210, 210, 210)",
                                    "color": "black",
                                    "fontWeight": "bold",
                                },
                            ),
                            html.Hr(),
                        ],
                    ),
                ],
            )
        ),
    )
