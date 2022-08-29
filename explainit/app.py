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
import copy
import json
import logging
import os

import dash
import pandas as pd
import plotly
from colorama import Fore
from colorama import Style
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from explainit.banner import build_banner
from explainit.banner import generate_section_banner
from explainit.correlation import correlation_data_table
from explainit.dashboard import DriftDashboard
from explainit.header import generate_metric_list_header
from explainit.header import generate_metric_row_helper
from explainit.tabs import build_tabs
from explainit.tabs import data_quality_tabs
from explainit.utils import get_distr_graph_data
from explainit.utils import get_drift_graph_data
from explainit.utils import get_json_data
from explainit.utils import get_small_hist_data
from explainit.utils import get_stats_data
from explainit.utils import target_data_copy
from explainit.workflow import generate_modal
from explainit.workflow import generate_workflow
from plotly.graph_objects import Figure

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


def build(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    target_column_name: str,
    target_column_type: str,
    host: str = "0.0.0.0",
    port: int = 8050,
):
    app = dash.Dash(
        __name__,
        url_base_pathname=os.getenv("ROUTE") or "/",
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
    )

    app.title = "Explainit"
    app.server
    app.config["suppress_callback_exceptions"] = True

    JSON_DATA = DriftDashboard(
        reference_data,
        current_data,
        target_column_name,
        target_column_type,
    ).calculate()

    (
        drift_data,
        target_data,
        data_summary,
        feature_summary,
        correlation_data,
    ) = get_json_data(JSON_DATA)

    del JSON_DATA

    print(
        f"Initiating {Style.BRIGHT + Fore.GREEN}Explainit App{Style.RESET_ALL}...[5/5]"
    )

    small_hist_data_cur = get_small_hist_data(drift_data, "f4")
    small_hist_data_ref = get_small_hist_data(drift_data, "f3")
    stats_data = get_stats_data(drift_data)
    drift_graph_data = get_drift_graph_data(drift_data)
    distr_graph_data = get_distr_graph_data(drift_data)
    tdd_copy = target_data_copy(target_data)

    @app.callback(
        Output("graph1", "figure"),
        Output("graph2", "figure"),
        Input("feature", "value"),
        Input("std-dropdown", "value"),
    )
    def generate_graph(item, std_dropdown):
        """
        Creates Drift Graph and Distribution graph for the choosen column.

        This method uses the distr_graph_data and drift_graph_data in order to create graphs.
        It will be interactive and updates the graph if you changes the std_dropdown value.

        Args:
            item: A String column which will be generated from the dropdown.
            std_dropdown: Standard deviation value choosen from the dropdown.
        Return:
            Returns a Graph which contains a Drift graph and a Distribution graph for the choosen feature based on Current Data.
        """

        fig1: Figure
        fig2: Figure

        # Distribution Plot
        for key in list(distr_graph_data.keys()):
            if item in key:
                graph_data_distr = copy.deepcopy(distr_graph_data[key])
                json_object = json.dumps(graph_data_distr)
                json_object = json_object.replace("#4d4d4d", "#1E90FF")
                fig1 = plotly.io.from_json(json_object)
                fig1.update_layout(
                    title={
                        "text": f"{item} Distribution".upper(),
                        "y": 0.9,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top",
                    }
                )

        # Drift plot
        for key in list(drift_graph_data.keys()):
            if item in key:
                graph_data = copy.deepcopy(drift_graph_data[key])
                mean = graph_data["layout"]["shapes"][1]["y0"]
                std = mean - graph_data["layout"]["shapes"][0]["y0"]
                graph_data["layout"]["shapes"][0]["y0"] = mean + (
                    float(std_dropdown) * std
                )
                graph_data["layout"]["shapes"][0]["y1"] = mean - (
                    float(std_dropdown) * std
                )

                json_object = json.dumps(graph_data)
                fig2 = plotly.io.from_json(json_object)
                fig2.update_layout(
                    title={
                        "text": f"{item} Drift".upper(),
                        "y": 0.9,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top",
                    }
                )
        return fig1, fig2

    @app.callback(
        Output("graph-content", "children"),
        Input("my_dropdown", "value"),
    )
    def generategraph(dropdown):
        """Method which will generate the behaviour of the target column based on the choosen feature from the dropdown.

        Args:
            my_dropdown: Column name which will be generated when you change the dropdown.
        Returns:
            Returns a graph which contains the target behaviour based on the choosen feature for both Reference and Current data.
        """
        if not dropdown:
            return html.Div(
                dcc.Graph(
                    id="basic-interactions",
                    figure=tdd_copy[0]["params"],
                    config={"displayModeBar": False},
                )
            )
        for feature in tdd_copy:
            if dropdown in feature["id"]:
                json_object = json.dumps(feature["params"])
                json_object = json_object.replace("#636efa", "#00BFFF")
                json_object = json_object.replace("#EF553B", "#FF1493")
                json_object = json.loads(json_object)
                return html.Div(
                    dcc.Graph(
                        id="basic-interactions",
                        figure=json_object,
                        config={"displayModeBar": False},
                    ),
                )

    app.layout = html.Div(
        id="big-app-container",
        children=[
            build_banner(),
            html.Div(
                id="app-container",
                children=[
                    build_tabs(),
                    html.Hr(),
                    html.Div(id="app-content"),
                    generate_workflow(),
                    generate_modal(),
                ],
            ),
        ],
    )

    @app.callback(
        Output("markdown2", "style"),
        [Input("how-it-works", "n_clicks"), Input("workflow_close", "n_clicks")],
    )
    def update_click_output(button_click, close_click):
        """
        Callback which will get triggered when user clicks on the how-it-works button from the UI.

        Args:
            button_click: Button value when it is clicked to open the pop-up window.
            close_click: Button value when it is clicked to close the pop-up window.

        Returns:
            A pop-up window which contains basic instructions about the usability of the Application.
        """
        ctx = dash.callback_context

        if ctx.triggered:
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if prop_id == "how-it-works":
                return {"display": "block"}

        return {"display": "none"}

    @app.callback(
        Output("markdown", "style"),
        [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
    )
    def update_how_it_works(button_click, close_click):
        """
        Callback which will get triggered when user clicks on the STATS-TESTS button from the UI.

        Args:
            button_click: Button value when it is clicked to open the pop-up window.
            close_click: Button value when it is clicked to close the pop-up window.

        Returns:
            A pop-up window which contains basic information regarding the Statistical Tests that are used inside the Application.
        """
        ctx = dash.callback_context

        if ctx.triggered:
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if prop_id == "learn-more-button":
                return {"display": "block"}

        return {"display": "none"}

    @app.callback(
        Output("feature-summary-content", "children"),
        Input("feature-dropdown", "value"),
    )
    def feature_summary_content(feature_summary_dropdown):
        """
        A method which will take the value of a dropdown which is a column name and returns the summary of that choosen column.

        Args:
            feature_summary_dropdown: Feature name will be generated from the dropdown.

        Returns:
            Provides two types of info in the summary. Feature summary as a data table and a graph which contains the distribution of the choosen feature.
        """

        for feature in feature_summary:
            if feature_summary_dropdown == feature["params"]["header"]:
                feat_summary_df = pd.DataFrame(feature["params"]["metrics"])
                feat_summary_df = pd.concat(
                    [
                        feat_summary_df,
                        pd.DataFrame(
                            feat_summary_df["values"].to_list(),
                            columns=["Reference Data", "Current Data"],
                        ),
                    ],
                    axis=1,
                )[["label", "Reference Data", "Current Data"]]
                graph_data = feature["params"]["graph"]
        return [
            html.Div(
                html.H6(
                    f"{feature_summary_dropdown.capitalize()} Summary",
                    style={"textAlign": "center"},
                )
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="six columns",
                        children=[
                            dash_table.DataTable(
                                data=feat_summary_df.to_dict("records"),
                                columns=[
                                    {"id": c, "name": c}
                                    for c in feat_summary_df.columns
                                ],
                                style_cell={"textAlign": "left"},
                                style_as_list_view=True,
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
                                style_table={"minWidth": "100%"},
                                style_header={
                                    "border": "1px solid black",
                                    "backgroundColor": "black",
                                    "color": "white",
                                    "fontWeight": "bold",
                                },
                            ),
                        ],
                        style={
                            "width": "30%",
                            "margin-top": "100px",
                            "margin-left": "30px",
                        },
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            dcc.Graph(
                                id="basic-interactions",
                                figure=graph_data,
                                config={"displayModeBar": False},
                                style={"width": "110vh", "height": "70vh"},
                            )
                        ],
                        style={
                            "width": "30%",
                            "margin-left": "100px",
                            "margin-top": "0px",
                        },
                    ),
                ],
                style=dict(display="flex"),
            ),
        ]

    @app.callback(
        Output("target-feature-title", "children"), Input("my_dropdown", "value")
    )
    def target_feature_title(dropdown):
        """
        A method which will generate header for the choosen feature value from the dropdown.

        Args:
            dropdown: Feature name which will be generated from the dropdown.

        Returns:
            HTML header(H6) with the given column name.
        """
        return html.H6(
            f"Target behaviour based on {dropdown.capitalize()}",
            style={"textAlign": "center"},
        )

    @app.callback(
        Output("correlation-graph", "children"),
        Input("correlation-radio-button", "value"),
    )
    def correlation_graph(radio_item):
        """
        Generates a Correlation Heatmap for the choosen correlation type.

        Args:
            correlation-radio-button: value of the choosen correlation type.

        Returns:
            Heatmap which contains the correlation information of the Reference and Current data for the selected correlation type.
        """
        for key in correlation_data["additionalGraphs"]:
            if radio_item.lower() == key["id"]:
                return html.Div(
                    children=[
                        html.H6(
                            f"{radio_item.capitalize()} Correlation Heatmap",
                            style={"textAlign": "center"},
                        ),
                        dcc.Graph(
                            id="correlation-id",
                            figure=key["params"],
                            style={"width": "180vh", "height": "100vh"},
                            config={"displayModeBar": False},
                        ),
                    ]
                )

    @app.callback(Output("quality-content", "children"), Input("quality-tabs", "value"))
    def render_quality_content(quality_tab_switch):
        """
        Renders the tab content with the selected tab value.

        Args:
            quality_tab_switch: value of the tab switch which will be generated when user selected the tab from the application UI.

        Returns:
            renders the tab content based on the user selected tab value.
        """
        if quality_tab_switch == "quality-tab2":
            return (
                html.Div(
                    children=[
                        html.H5(
                            "Select Feature",
                            style={"font-size": "18px", "font-weight": "bold"},
                        ),
                        html.Div(
                            dcc.Dropdown(
                                id="feature-dropdown",
                                options=list(stats_data.keys()),
                                value=list(stats_data.keys())[0],
                                placeholder="Choose data",
                                clearable=False,
                                searchable=True,
                            ),
                            style={
                                "width": "30%",
                                "margin-top": "15px",
                                "margin-left": "10px",
                            },
                        ),
                        html.Div(id="feature-summary-content"),
                    ]
                ),
            )
        if quality_tab_switch == "quality-tab3":

            return [
                html.Div(
                    id="correlation-data-table",
                    children=correlation_data_table(correlation_data),
                    style={
                        "margin-top": "25px",
                        "margin-right": "35px",
                        "margin-left": "35px",
                    },
                ),
                html.Div(
                    dcc.RadioItems(
                        id="correlation-radio-button",
                        options=["PEARSON", "SPEARMAN", "KENDALL"],
                        value="PEARSON",
                        inline=True,
                    )
                ),
                html.Div(id="correlation-graph"),
            ]
        return [
            html.Div(
                dash_table.DataTable(
                    data=data_summary[0],
                    columns=[
                        {"name": c, "id": c} for c in list(data_summary[0][0].keys())
                    ],
                    style_cell={"textAlign": "left"},
                    style_as_list_view=True,
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
                style={
                    "margin-top": "25px",
                    "margin-right": "35px",
                    "margin-left": "35px",
                },
            )
        ]

    @app.callback(Output("app-content", "children"), Input("app-tabs", "value"))
    def render_tab_content(tab_switch):
        """
        Renders the tab content for the main tabs in the Application.

        Args:
            tab_switch: value of the tab switch which will be generated when user selected the tab from the application UI.

        Returns:
            renders the tab content based on the user selected tab value.

        """

        if tab_switch == "tab1":
            return [
                html.Div(
                    children=[
                        generate_section_banner("Drift Info. for Every Feature"),
                        generate_metric_list_header(),
                        html.Div(
                            id="metric-rows",
                            children=[
                                generate_metric_row_helper(
                                    key,
                                    stats_data,
                                    small_hist_data_cur,
                                    small_hist_data_ref,
                                )
                                for key in list(stats_data.keys())
                            ],
                        ),
                        html.Hr(),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="six columns",
                                    children=[
                                        html.H5(
                                            "Select Feature",
                                            style={
                                                "font-size": "18px",
                                                "font-weight": "bold",
                                            },
                                        )
                                    ],
                                    style={"width": "30%", "margin-left": "10px"},
                                ),
                                html.Div(
                                    className="six columns",
                                    children=[
                                        html.H5(
                                            "Choose Standard Deviation",
                                            style={
                                                "font-size": "18px",
                                                "font-weight": "bold",
                                            },
                                        )
                                    ],
                                    style={"width": "30%", "margin-left": "350px"},
                                ),
                            ],
                            style=dict(display="flex"),
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="six columns",
                                    children=[
                                        dcc.Dropdown(
                                            id="feature",
                                            options=list(stats_data.keys())[1:],
                                            value=list(stats_data.keys())[1:][0],
                                            placeholder="Choose feature",
                                            clearable=False,
                                            searchable=True,
                                        )
                                    ],
                                    style={"width": "30%", "margin-left": "10px"},
                                ),
                                html.Div(
                                    className="six columns",
                                    children=[
                                        dcc.Dropdown(
                                            id="std-dropdown",
                                            options=[0.5, 1, 1.5, 2, 2.5, 3],
                                            placeholder="Select standard deviation",
                                            value=1.5,
                                            clearable=False,
                                            searchable=True,
                                        )
                                    ],
                                    style={"width": "30%", "margin-left": "350px"},
                                ),
                            ],
                            style=dict(display="flex"),
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    id="graph-style",
                                    className="parent",
                                    children=[
                                        dcc.Graph(
                                            id="graph1",
                                            className="plot",
                                            config={"displayModeBar": False},
                                        ),
                                        html.Div(className="spacer"),
                                        dcc.Graph(
                                            id="graph2",
                                            className="plot",
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ]

        if tab_switch == "tab2":

            return [
                html.Div(
                    id="target-drift-content",
                    children=[
                        html.H6(target_data["widgets"][0]["title"]),
                        html.Div(
                            dcc.Graph(
                                id="target-main-graph",
                                figure=target_data["widgets"][0]["params"],
                                config={"displayModeBar": False},
                            ),
                            style={
                                "width": "150vh",
                                "height": "60vh",
                                "display": "flex",
                                "justify-content": "center",
                                "margin-left": "230px",
                                "border": "3px #5c5c5c solid",
                                "padding-left": "1px",
                                "overflow": "hidden",
                            },
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H5(
                                    "Select Feature",
                                    style={"font-size": "18px", "font-weight": "bold"},
                                ),
                                dcc.Dropdown(
                                    id="my_dropdown",
                                    options=[
                                        data["id"][:-14]
                                        if "target" in data["id"]
                                        else data["id"][:-7]
                                        for data in tdd_copy
                                    ],
                                    value=tdd_copy[0]["id"][:-14]
                                    if "target" in tdd_copy[0]["id"]
                                    else tdd_copy[0]["id"][:-7],
                                    multi=False,
                                    clearable=True,
                                    style={"width": "50%"},
                                ),
                                html.Div(id="target-feature-title"),
                                html.Div(id="graph-content"),
                            ]
                        ),
                    ],
                )
            ]

        if tab_switch == "tab3":
            return [data_quality_tabs(), html.Div(id="quality-content")]

    app.run_server(debug=False, host=host, port=port)
