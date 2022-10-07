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
from dash import dcc
from dash import html
from dash_daq import Indicator


SUFFIX_ROW = "_row"
SUFFIX_COLUMN_TYPE = "_column_type"
SUFFIX_SPARKLINE_GRAPH = "_sparkline_graph"
SUFFIX_SPARKLINE_GRAPH2 = "_sparkline_graph2"
SUFFIX_THRESHOLD = "_threshold"
SUFFIX_TEST_NAME = "_test"
SUFFIX_PVALUE = "_Pvalue"
SUFFIX_INDICATOR = "_indicator"


def generate_metric_row(key, style, col1, col2, col3, col4, col5, col6, col7, col8):
    """
    Creates a HTML component with the given key, style and content.

    Args:
        key: id for the html element.
        style: style attribute for the component.
        col1: content for the column section.
        col2: content for the type section.
        col3: content for the Reference Distribution section.
        col4: content for the production Distribution section.
        col5: content for the threshld section.
        col6: content for the Stat-test section.
        col7: content for the P-Value section.
        col8: content for the Drift/No Drift section.

    Returns:
        Returns a Html Division with the provided content and style.
    """
    if style is None:
        style = {
            "height": "6rem",
            "margin": "1rem 0",
            "textAlign": "center",
            "margin-right": "15px",
            "margin-left": "15px",
        }

    return html.Div(
        id=key,
        className="metric-row",
        style=style,
        children=[
            html.Div(
                id=col1["id"],
                className="two columns",
                style={"textAlign": "center"},
                children=col1["children"],
            ),
            html.Div(
                id=col2["id"],
                style={"textAlign": "center"},
                className="one column",
                children=col2["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"height": "100%", "textAlign": "center"},
                className="three columns",
                children=col3["children"],
            ),
            html.Div(
                id=col4["id"],
                style={"height": "100%", "textAlign": "center"},
                className="three columns",
                children=col4["children"],
            ),
            html.Div(
                id=col5["id"],
                style={"textAlign": "center"},
                className="one column",
                children=col5["children"],
            ),
            html.Div(
                id=col6["id"],
                style={"textAlign": "center"},
                className="two columns",
                children=col6["children"],
            ),
            html.Div(
                id=col7["id"],
                style={"textAlign": "center"},
                className="one columns",
                children=col7["children"],
            ),
            html.Div(
                id=col8["id"],
                style={
                    "textAlign": "center",
                    "display": "flex",
                    "justifyContent": "center",
                },
                className="two columns",
                children=col8["children"],
            ),
        ],
    )


# Build header
def generate_metric_list_header():
    return generate_metric_row(
        "metric_header",
        {
            "height": "3rem",
            "margin": "1rem 0",
            "textAlign": "center",
            "margin-right": "15px",
            "margin-left": "15px",
        },
        {"id": "m_header_1", "children": html.Div("Column")},
        {"id": "m_header_2", "children": html.Div("Type")},
        {"id": "m_header_3", "children": html.Div("Reference Distribution")},
        {"id": "m_header_4", "children": html.Div("Production Distribution")},
        {"id": "m_header_5", "children": html.Div("Threshold")},
        {"id": "m_header_6", "children": html.Div("Stat-test")},
        {"id": "m_header_7", "children": html.Div("P-Value")},
        {"id": "m_header_8", "children": html.Div("Drift/No Drift")},
    )


def drift_indicator(drift):
    """
    Generates a colorscale for the given value.

    Args:
        stats_info: string object describing whether drift detected or not detected.

    Returns:
        Colorscale for the given value.
    """
    return "#e5b310" if drift else "#00b25d"


def stat_test_full_name(stattest_name):
    """
    Provides the full statistical test name for the given short-form.

    Args:
        short-form of the Statistical test.
    Returns:
        Full name of the provided statistical test.
    """
    if stattest_name == "ks_stat_test":
        return "Kolmogorov–Smirnov (K-S)"
    if stattest_name == "z_stat_test":
        return "Z-Test"
    if stattest_name == "chi_stat_test":
        return "Chi-Square Test"
    if stattest_name == "jensenshannon_stat_test":
        return "Jensen–Shannon divergence"
    if stattest_name == "wasserstein_stat_test":
        return "Wasserstein Distance"


def generate_metric_row_helper(item, stats_info):
    """
    Args:
        item: name of the feature inside the dataframe.
        stats_info: Statistical information about the data.

    Returns:
        HTML division element with the provided content.
    """
    for feature_data in stats_info.values():
        if feature_data["feature_name"] == item:
            feature_stats_data = feature_data
            ref_x = feature_stats_data["ref_hist_data"][1]
            ref_y = feature_stats_data["ref_hist_data"][0]
            if len(feature_stats_data["prod_hist_data"]) == 1:
                prod_x = feature_stats_data["prod_hist_data"][0][1]
                prod_y = feature_stats_data["prod_hist_data"][0][0]
            else:
                prod_x = feature_stats_data["prod_hist_data"][1]
                prod_y = feature_stats_data["prod_hist_data"][0]

    if "target" not in item:
        div_id = item + SUFFIX_ROW
        column_type_id = item + SUFFIX_COLUMN_TYPE
        sparkline_graph_id = item + SUFFIX_SPARKLINE_GRAPH
        sparkline_graph_id2 = item + SUFFIX_SPARKLINE_GRAPH2
        threshold_id = item + SUFFIX_THRESHOLD
        test_id = item + SUFFIX_TEST_NAME
        pvalue_id = item + SUFFIX_PVALUE
        indicator_id = item + SUFFIX_INDICATOR

        return generate_metric_row(
            div_id,
            None,
            {
                "id": item,
                "className": "metric-row-button-text",
                "children": item,
            },
            {
                "id": column_type_id,
                "children": feature_stats_data["stattest"][1].upper(),
            },
            {
                "id": f"{item}_sparkline",
                "children": dcc.Graph(
                    id=sparkline_graph_id,
                    style={"width": "90%", "height": "100%"},
                    config={
                        "staticPlot": False,
                        "editable": False,
                        "displayModeBar": False,
                    },
                    figure=go.Figure(
                        {
                            "data": [
                                {
                                    "x": ref_x,
                                    "y": ref_y,
                                    "type": "bar",
                                    "name": item,
                                },
                            ],
                            "colorscale": "viridis",
                            "layout": {
                                "uirevision": True,
                                "margin": dict(l=0, r=0, t=0, b=0, pad=0),
                                "xaxis": dict(
                                    showline=False,
                                    showgrid=False,
                                    zeroline=False,
                                    showticklabels=False,
                                ),
                                "yaxis": dict(
                                    showline=False,
                                    showgrid=False,
                                    zeroline=False,
                                    showticklabels=False,
                                ),
                                "paper_bgcolor": "rgba(0,0,0,0)",
                                "plot_bgcolor": "rgba(0,0,0,0)",
                            },
                        },
                    )
                    .add_traces(
                        go.Scatter(
                            x=ref_x,
                            y=ref_y,
                            mode="lines",
                            line=dict(
                                color="rgba(64, 83, 211, 1)",
                                # dash = 'dash'
                                width=1,
                            ),
                            name="normal",
                        )
                    )
                    .update_traces(
                        marker_color="rgba(229,179,16,1)"
                        if feature_stats_data["drift"]
                        else "rgb(0,178,93)"
                    )
                    .update_traces(showlegend=False),
                ),
            },
            {
                "id": f"{item}_sparkline",
                "children": dcc.Graph(
                    id=sparkline_graph_id2,
                    style={"width": "90%", "height": "100%"},
                    config={
                        "staticPlot": False,
                        "editable": False,
                        "displayModeBar": False,
                    },
                    figure=go.Figure(
                        {
                            "data": [
                                {
                                    "x": prod_x,
                                    "y": prod_y,
                                    "type": "bar",
                                    "name": item,
                                },
                            ],
                            "colorscale": "viridis",
                            "layout": {
                                "uirevision": True,
                                "margin": dict(l=0, r=0, t=0, b=0, pad=0),
                                "xaxis": dict(
                                    showline=False,
                                    showgrid=False,
                                    zeroline=False,
                                    showticklabels=False,
                                ),
                                "yaxis": dict(
                                    showline=False,
                                    showgrid=False,
                                    zeroline=False,
                                    showticklabels=False,
                                ),
                                "paper_bgcolor": "rgba(0,0,0,0)",
                                "plot_bgcolor": "rgba(0,0,0,0)",
                            },
                        },
                    )
                    .add_traces(
                        go.Scatter(
                            x=prod_x,
                            y=prod_y,
                            mode="lines",
                            line=dict(
                                color="rgba(64, 83, 211,1)",
                                # dash = 'dash'
                                width=1,
                            ),
                            name="normal",
                        )
                    )
                    .update_traces(
                        marker_color="rgba(229,179,16,1)"
                        if feature_stats_data["drift"]
                        else "rgb(0,178,93)"
                    )
                    .update_traces(showlegend=False),
                ),
            },
            {"id": threshold_id, "children": feature_stats_data["threshold"]},
            {
                "id": test_id,
                "children": stat_test_full_name(feature_stats_data["stattest"][0]),
            },
            {"id": pvalue_id, "children": round(feature_stats_data["p_value"], 4)},
            {
                "id": f"{item}_pf",
                "children": Indicator(
                    id=indicator_id,
                    value=True,
                    color=drift_indicator(feature_stats_data["drift"]),
                    size=12,
                    style={"justify": "center"},
                ),
            },
        )
