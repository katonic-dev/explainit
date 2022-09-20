import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go


def choose_agg_period(
    date_column: str, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame]
) -> str:
    optimal_points = 150
    prefix_dict = {
        "A": "year",
        "Q": "quarter",
        "M": "month",
        "W": "week",
        "D": "day",
        "H": "hour",
    }
    datetime_feature = reference_data[date_column]
    if current_data is not None:
        datetime_feature = datetime_feature.append(current_data[date_column])
    days = (datetime_feature.max() - datetime_feature.min()).days
    time_points = pd.Series(
        index=["A", "Q", "M", "W", "D", "H"],
        data=[
            abs(optimal_points - days / 365),
            abs(optimal_points - days / 90),
            abs(optimal_points - days / 30),
            abs(optimal_points - days / 7),
            abs(optimal_points - days),
            abs(optimal_points - days * 24),
        ],
    )
    prefix_dict[time_points.idxmin()]
    return str(time_points.idxmin())


def plot_feature_stats(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    feature_name: str,
    feature_type: str,
):
    if feature_type == "num":
        if current_data is None:
            trace1 = go.Histogram(
                x=reference_data[feature_name], marker_color="#ed0400"
            )
            trace2 = go.Histogram(
                x=np.log10(
                    reference_data.loc[reference_data[feature_name] > 0, feature_name]
                ),
                marker_color="#ed0400",
                visible=False,
            )
            data = [trace1, trace2]
            updatemenus = [
                dict(
                    type="buttons",
                    direction="right",
                    x=1.0,
                    yanchor="top",
                    buttons=list(
                        [
                            dict(
                                label="Linear Scale",
                                method="update",
                                args=[{"visible": [True, False]}],
                            ),
                            dict(
                                label="Log Scale",
                                method="update",
                                args=[{"visible": [False, True]}],
                            ),
                        ]
                    ),
                )
            ]

        else:
            trace1 = go.Histogram(
                x=reference_data[feature_name],
                marker_color="#4d4d4d",
                name="reference",
            )
            trace2 = go.Histogram(
                x=np.log10(
                    reference_data.loc[reference_data[feature_name] > 0, feature_name]
                ),
                marker_color="#4d4d4d",
                visible=False,
                name="reference",
            )
            trace3 = go.Histogram(
                x=current_data[feature_name], marker_color="#ed0400", name="current"
            )
            trace4 = go.Histogram(
                x=np.log10(
                    current_data.loc[current_data[feature_name] > 0, feature_name]
                ),
                marker_color="#ed0400",
                visible=False,
                name="current",
            )
            data = [trace1, trace2, trace3, trace4]

            updatemenus = [
                dict(
                    type="buttons",
                    direction="right",
                    x=1.0,
                    yanchor="top",
                    buttons=list(
                        [
                            dict(
                                label="Linear Scale",
                                method="update",
                                args=[{"visible": [True, False, True, False]}],
                            ),
                            dict(
                                label="Log Scale",
                                method="update",
                                args=[{"visible": [False, True, False, True]}],
                            ),
                        ]
                    ),
                )
            ]
        layout = dict(updatemenus=updatemenus)

        fig = go.Figure(data=data, layout=layout)

    elif feature_type == "cat":
        fig = go.Figure()
        cats = list(reference_data[feature_name].value_counts().index.astype(str))
        if "other" in cats:
            cats.remove("other")
            cats = cats + ["other"]
        if current_data is None:
            fig.add_trace(
                go.Histogram(x=reference_data[feature_name], marker_color="#ed0400")
            )
        else:
            fig.add_trace(
                go.Histogram(
                    x=reference_data[feature_name],
                    marker_color="#4d4d4d",
                    name="reference",
                )
            )
            fig.add_trace(
                go.Histogram(
                    x=current_data[feature_name],
                    marker_color="#ed0400",
                    name="current",
                )
            )
        fig.update_xaxes(categoryorder="array", categoryarray=cats)

    elif feature_type == "datetime":
        freq = choose_agg_period(feature_name, reference_data, current_data)
        tmp_ref = reference_data[feature_name].dt.to_period(freq=freq)
        tmp_ref = tmp_ref.value_counts().reset_index()
        tmp_ref.columns = [feature_name, "number_of_items"]
        tmp_ref[feature_name] = tmp_ref[feature_name].dt.to_timestamp()
        fig = go.Figure()
        if current_data is None:
            fig.add_trace(
                go.Scatter(
                    x=tmp_ref.sort_values(feature_name)[feature_name],
                    y=tmp_ref.sort_values(feature_name)["number_of_items"],
                    line=dict(color="#ed0400", shape="spline"),
                )
            )
        else:
            tmp_curr = current_data[feature_name].dt.to_period(freq=freq)
            tmp_curr = tmp_curr.value_counts().reset_index()
            tmp_curr.columns = [feature_name, "number_of_items"]
            tmp_curr[feature_name] = tmp_curr[feature_name].dt.to_timestamp()

            max_ref_date = tmp_ref[feature_name].max()
            min_curr_date = tmp_curr[feature_name].min()
            if max_ref_date == min_curr_date:
                if (
                    tmp_curr.loc[
                        tmp_curr[feature_name] == min_curr_date, "number_of_items"
                    ].iloc[0]
                    > tmp_ref.loc[
                        tmp_ref[feature_name] == max_ref_date, "number_of_items"
                    ].iloc[0]
                ):
                    tmp_curr.loc[
                        tmp_curr[feature_name] == min_curr_date, "number_of_items"
                    ] = (
                        tmp_curr.loc[
                            tmp_curr[feature_name] == min_curr_date, "number_of_items"
                        ]
                        + tmp_ref.loc[
                            tmp_ref[feature_name] == max_ref_date, "number_of_items"
                        ]
                    )
                    tmp_ref = tmp_ref[tmp_ref[feature_name] != max_ref_date]
                else:
                    tmp_ref.loc[
                        tmp_ref[feature_name] == max_ref_date, "number_of_items"
                    ] = (
                        tmp_ref.loc[
                            tmp_ref[feature_name] == max_ref_date, "number_of_items"
                        ]
                        + tmp_curr.loc[
                            tmp_curr[feature_name] == min_curr_date, "number_of_items"
                        ]
                    )
                    tmp_curr = tmp_curr[tmp_curr[feature_name] != min_curr_date]

            fig.add_trace(
                go.Scatter(
                    x=tmp_ref.sort_values(feature_name)[feature_name],
                    y=tmp_ref.sort_values(feature_name)["number_of_items"],
                    line=dict(color="#4d4d4d", shape="spline"),
                    name="reference",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=tmp_curr.sort_values(feature_name)[feature_name],
                    y=tmp_curr.sort_values(feature_name)["number_of_items"],
                    line=dict(color="#ed0400", shape="spline"),
                    name="current",
                )
            )
    else:
        return {}

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_main_distr = json.loads(fig.to_json())
    return fig_main_distr
