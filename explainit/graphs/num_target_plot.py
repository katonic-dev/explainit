import plotly.figure_factory as ff
from explainit.graphs.additional_num_graphs import fig_to_json


def num_target_main_graph(reference_data_to_plot, current_data_to_plot):
    #     reference_data_to_plot =reference_data_to_plot.tolist()
    #     current_data_to_plot = current_data_to_plot.tolist()
    output_distr = ff.create_distplot(
        [reference_data_to_plot, current_data_to_plot],
        ["Reference", "Current"],
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
