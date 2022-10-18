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
import warnings
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import dash
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
from colorama import Fore
from colorama import Style
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from explainit.analyzer.data_summary import data_summary_stats
from explainit.analyzer.feature_summary import additional_cat_stats
from explainit.analyzer.feature_summary import feature_summary_stats
from explainit.analyzer.feature_summary import make_feature_stats_dataframe
from explainit.banner import build_banner
from explainit.banner import generate_section_banner
from explainit.correlation import correlation_data_table
from explainit.correlations.correlation_heatmaps import plot_correlation_figure
from explainit.correlations.correlation_table import make_metrics
from explainit.correlations.correlations import calculate_correlations
from explainit.graphs.additional_cat_graphs import generate_additional_graph_cat_feature
from explainit.graphs.additional_num_graphs import fig_to_json
from explainit.graphs.additional_num_graphs import generate_additional_graph_num_feature
from explainit.graphs.cat_target_plot import cat_target_main_graph
from explainit.graphs.feature_stats_plots import plot_feature_stats
from explainit.graphs.num_target_plot import num_target_main_graph
from explainit.graphs.numerical_target_behaviour import (
    numerical_target_behaviour_on_features,
)
from explainit.header import generate_metric_list_header
from explainit.header import generate_metric_row_helper
from explainit.stattests.stat_test import get_statistical_info
from explainit.stattests.stat_test import get_stattest
from explainit.tabs import build_tabs
from explainit.tabs import data_quality_tabs
from explainit.workflow import generate_modal
from explainit.workflow import generate_workflow
from plotly.graph_objects import Figure

warnings.filterwarnings("ignore")

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


def build(
    reference_data: pd.DataFrame,
    production_data: pd.DataFrame,
    target_col_name: str,
    target_col_type: str,
    datetime_col_name: Optional[str] = "",
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

    # reference_data.rename(columns={target_col_name: "target"}, inplace=True)
    # production_data.rename(columns={target_col_name: "target"}, inplace=True)

    # ref_data_columns = reference_data.columns.to_list()
    # prod_data_columns = production_data.columns.to_list()
    # if functools.reduce(
    #     lambda x, y: x and y,
    #     map(lambda p, q: p == q, sorted(ref_data_columns), sorted(prod_data_columns)),
    #     True,
    # ):
    #     print("The lists prod_data_columns and ref_data_columns are the same")
    # else:
    #     print("ERROR: The lists prod_data_columns and ref_data_columns are not the same")

    print(f"Initiating {Style.BRIGHT + Fore.GREEN}Explainit App{Style.RESET_ALL}...")

    num_feature_names: List[str] = sorted(
        list(set(reference_data.select_dtypes([np.number]).columns))
    )
    cat_feature_names: List[str] = sorted(
        list(
            set(reference_data.select_dtypes(exclude=[np.number, "datetime"]).columns)
            - set(num_feature_names)
        )
    )
    cat_feature_names.remove(
        datetime_col_name
    ) if datetime_col_name else cat_feature_names
    total_columns = num_feature_names + cat_feature_names
    reference_data = reference_data[total_columns]
    production_data = production_data[total_columns]
    if target_col_name not in total_columns:
        raise ValueError(
            f"Given target column name {Style.BRIGHT + Fore.RED}{target_col_name}{Style.RESET_ALL} does not exist in the data."
        )

    # Finding appropriate Statistical test for Individual feature.
    num_feature_test: Dict[str, List[str]] = {}

    for num_feature_name in num_feature_names:
        feature_type = "num"
        ref_feature = (
            reference_data[num_feature_name].replace([-np.inf, np.inf], np.nan).dropna()
        )
        prod_feature = (
            production_data[num_feature_name]
            .replace([-np.inf, np.inf], np.nan)
            .dropna()
        )
        num_feature_test[num_feature_name] = [
            get_stattest(
                feature_type=feature_type,
                ref_feature=ref_feature,
                prod_feature=prod_feature,
            ),
            feature_type,
        ]

    cat_feature_test: Dict[str, List[str]] = {}

    for cat_feature_name in cat_feature_names:
        feature_type = "cat"
        ref_feature = reference_data[cat_feature_name].dropna()
        prod_feature = production_data[cat_feature_name].dropna()
        cat_feature_test[cat_feature_name] = [
            get_stattest(
                feature_type=feature_type,
                ref_feature=ref_feature,
                prod_feature=prod_feature,
            ),
            feature_type,
        ]

    feature_test = {**num_feature_test, **cat_feature_test}

    # Statistical Information
    statstical_data = get_statistical_info(
        feature_test, reference_data, production_data
    )
    target_drift_title = f"""
                        Target Drift: {"Detected" if statstical_data[target_col_name]["drift"] == True else "Not Detected"},
                        drift score={round(statstical_data[target_col_name]["p_value"], 4)}
                        ({statstical_data[target_col_name]["stattest"][0]})"""

    # Additional Feature Graphs
    additional_graphs_data: Dict[str, Tuple[Dict[str, Any], Dict[str, Any]]] = {}
    for feature in feature_test:
        # plot distributions
        if feature_test[feature][1] == "num":
            additional_graphs_data[feature] = generate_additional_graph_num_feature(
                feature,
                reference_data[feature].dropna(),
                production_data[feature].dropna(),
            )
        elif feature_test[feature][1] == "cat":
            additional_graphs_data[feature] = generate_additional_graph_cat_feature(
                feature,
                reference_data[feature].dropna(),
                production_data[feature].dropna(),
            )

    # Categorical Target Main Graph.

    if target_col_type == "cat":

        categorical_target_main_figure_data = cat_target_main_graph(
            reference_data[target_col_name], production_data[target_col_name]
        )

        # Categorical target behaviour based on individual features
        reference_data_copy = reference_data.copy()
        reference_data_copy["dataset"] = "Reference"

        production_data_copy = production_data.copy()
        production_data_copy["dataset"] = "Production"

        merged_data = pd.concat([reference_data_copy, production_data_copy])
        cat_target_behaviour_graphs = {
            feature: fig_to_json(
                px.histogram(
                    merged_data,
                    x=feature,
                    color=target_col_name,
                    # color_discrete_sequence=["goldenrod", "magenta"],
                    facet_col="dataset",
                    barmode="overlay",
                    category_orders={"dataset": ["Reference", "Production"]},
                )
            )
            for feature in list(feature_test.keys())
        }

    if target_col_type == "num":
        reference_data_to_plot = reference_data[target_col_name].tolist()
        production_data_to_plot = production_data[target_col_name].tolist()

        numerical_target_main_figure_data = num_target_main_graph(
            reference_data_to_plot, production_data_to_plot
        )

        # Numerical target behaviour based on individual features
        reference_data_copy = reference_data.copy()
        production_data_copy = production_data.copy()
        num_target_behaviour_graphs = {
            feature: numerical_target_behaviour_on_features(
                reference_data[feature],
                production_data[feature],
                reference_data[target_col_name],
                production_data[target_col_name],
            )
            for feature in total_columns
        }

    # Data Summary

    reference_data_summary = data_summary_stats(
        reference_data, target_column=target_col_name
    )
    reference_data_summary["Categorical features"] = len(cat_feature_names)
    reference_data_summary["Numeric features"] = len(num_feature_names)

    production_data_summary = data_summary_stats(
        production_data, target_column=target_col_name
    )
    production_data_summary["Categorical features"] = len(cat_feature_names)
    production_data_summary["Numeric features"] = len(num_feature_names)

    data_summary_df = pd.concat(
        [
            pd.DataFrame(reference_data_summary, index=[0]),
            pd.DataFrame(production_data_summary, index=[0]),
        ]
    ).T
    data_summary_df.columns = ["Reference", "Production"]
    data_summary_df.reset_index(inplace=True)
    data_summary_df.rename(columns={"index": "Metrics"}, inplace=True)

    # Feature Summary
    prod_cat_feature_stats: Dict[str, Dict[str, Any]] = {}
    ref_cat_feature_stats: Dict[str, Dict[str, Any]] = {}
    for feature in cat_feature_names:
        feature_type = "cat"
        prod_cat_feature_stats[feature] = feature_summary_stats(
            production_data[feature], feature_type
        )
        ref_cat_feature_stats[feature] = feature_summary_stats(
            reference_data[feature], feature_type
        )

    prod_num_feature_stats: Dict[str, Dict[str, Any]] = {}
    ref_num_feature_stats: Dict[str, Dict[str, Any]] = {}
    for feature in num_feature_names:
        feature_type = "num"
        prod_num_feature_stats[feature] = feature_summary_stats(
            production_data[feature], feature_type
        )
        ref_num_feature_stats[feature] = feature_summary_stats(
            reference_data[feature], feature_type
        )

    for feature in cat_feature_names:
        prod_cat_feature_stats[feature] = additional_cat_stats(
            reference_data[feature], production_data[feature], prod_cat_feature_stats
        )
        ref_cat_feature_stats[feature] = additional_cat_stats(
            reference_data[feature], production_data[feature], ref_cat_feature_stats
        )

    feature_stats_dataframes = {
        feature: make_feature_stats_dataframe(
            feature,
            prod_cat_feature_stats,
            prod_num_feature_stats,
            ref_cat_feature_stats,
            ref_num_feature_stats,
        )
        for feature in list(feature_test.keys())
    }

    # Feature Summary Graphs.
    feature_stats_graphs = {
        **{
            feature: plot_feature_stats(reference_data, production_data, feature, "cat")
            for feature in cat_feature_names
        },
        **{
            feature: plot_feature_stats(reference_data, production_data, feature, "num")
            for feature in num_feature_names
        },
    }

    # Correlations

    reference_feature_stats = {**ref_cat_feature_stats, **ref_num_feature_stats}

    num_for_corr = []
    for feature in num_feature_names:
        if reference_feature_stats[feature]["Unique_count"] > 1:
            num_for_corr.append(feature)

    cat_for_corr = []
    for feature in cat_feature_names:
        if reference_feature_stats[feature]["Unique_count"] > 1:
            cat_for_corr.append(feature)

    reference_correlations = {}
    production_correlations = {}
    for kind in ["pearson", "spearman", "kendall", "cramer_v"]:
        reference_correlations[kind] = calculate_correlations(
            reference_data, num_for_corr, cat_for_corr, kind
        )
        if production_data is not None:
            production_correlations[kind] = calculate_correlations(
                production_data, num_for_corr, cat_for_corr, kind
            )

    metrics = make_metrics(reference_correlations, production_correlations)
    metrics_values_headers = [
        "top 5 correlation diff category (Cramer_V)",
        "value ref",
        "value prod",
        "difference",
        "top 5 correlation diff numerical (Spearman)",
        "value ref",
        "value prod",
        "difference",
    ]

    # Correlations Dataframe
    correlations_df = pd.DataFrame(columns=metrics_values_headers)
    for metric in metrics:
        a_series = pd.Series(metric["values"], index=correlations_df.columns)
        correlations_df = correlations_df.append(a_series, ignore_index=True)

    # Correlations Heatmaps.
    correlation_graphs = {}
    parts = {}
    for kind in ["pearson", "spearman", "kendall", "cramer_v"]:
        if reference_correlations[kind].shape[0] > 1:
            correlation_figure = plot_correlation_figure(
                kind, reference_correlations, production_correlations
            )
            correlation_graphs[kind] = {
                "data": correlation_figure["data"],
                "layout": correlation_figure["layout"],
            }
            parts.update({"title": kind, "id": kind})

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
            Returns a Graph which contains a Drift graph and a Distribution graph for the choosen feature based on production Data.
        """

        fig1: Figure
        fig2: Figure

        # Distribution Plot
        graph_data_distr = copy.deepcopy(additional_graphs_data[item][0])
        json_object = json.dumps(graph_data_distr)
        fig1 = plotly.io.from_json(json_object)

        # Drift plot
        if item in num_feature_names:
            graph_data = copy.deepcopy(additional_graphs_data[item][1])
            mean = graph_data["layout"]["shapes"][1]["y0"]
            std = mean - graph_data["layout"]["shapes"][0]["y0"]
            graph_data["layout"]["shapes"][0]["y0"] = mean + (float(std_dropdown) * std)
            graph_data["layout"]["shapes"][0]["y1"] = mean - (float(std_dropdown) * std)

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
        if item in cat_feature_names:
            pie_chart_graph = copy.deepcopy(additional_graphs_data[item][1])
            json_object = json.dumps(pie_chart_graph)
            fig2 = plotly.io.from_json(json_object)
            fig2.update_layout(
                title={
                    "text": f"{item} Pie Chart".upper(),
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
            Returns a graph which contains the target behaviour based on the choosen feature for both Reference and production data.
        """
        feature_data = (
            copy.deepcopy(cat_target_behaviour_graphs[dropdown])
            if target_col_type == "cat"
            else copy.deepcopy(num_target_behaviour_graphs[dropdown])
        )
        if target_col_type == "cat":
            if len(feature_data["data"]) == 4:
                for i in range(4):
                    feature_data["data"][i]["x"] = feature_data["data"][i]["x"].tolist()
            if len(feature_data["data"]) == 6:
                for i in range(6):
                    feature_data["data"][i]["x"] = feature_data["data"][i]["x"].tolist()
        json_object = json.dumps(feature_data)
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
                    # html.Hr(),
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

        feature_df = feature_stats_dataframes[feature_summary_dropdown]
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
                                data=feature_df.to_dict("records"),
                                columns=[
                                    {"id": c, "name": c} for c in feature_df.columns
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
                                figure=feature_stats_graphs[feature_summary_dropdown],
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
            f"{target_col_name.upper()} behaviour based on {dropdown.capitalize()}",
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
            Heatmap which contains the correlation information of the Reference and production data for the selected correlation type.
        """
        correlation_graph_data = correlation_graphs[radio_item.lower()]
        return html.Div(
            children=[
                html.H6(
                    f"{radio_item.capitalize()} Correlation Heatmap",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="correlation-id",
                    figure=correlation_graph_data,
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
                                options=sorted(total_columns),
                                value=sorted(total_columns)[0],
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
                    children=correlation_data_table(correlations_df),
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
                    data=data_summary_df.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in data_summary_df.columns],
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
                                    statstical_data,
                                )
                                for key in list(statstical_data.keys())
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
                                            options=sorted(total_columns),
                                            value=sorted(total_columns)[0],
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
                        html.H6(target_drift_title),
                        html.Div(
                            dcc.Graph(
                                id="target-main-graph",
                                figure=categorical_target_main_figure_data
                                if target_col_type == "cat"
                                else numerical_target_main_figure_data,
                                config={"displayModeBar": False},
                            ),
                            style={
                                "display": "flex",
                                "justify-content": "center",
                                "border": "3px #5c5c5c solid",
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
                                    options=sorted(total_columns),
                                    value=sorted(total_columns)[0],
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
