import plotly.graph_objs as go
from explainit.graphs.additional_num_graphs import fig_to_json


def cat_target_main_graph(ref_target_data, cur_target_data):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=ref_target_data.tolist(),
            marker_color="#48DD2D",
            opacity=0.6,
            nbinsx=10,
            name="Training",
            histnorm="probability",
        )
    )

    fig.add_trace(
        go.Histogram(
            x=cur_target_data.tolist(),
            marker_color="#ed0400",
            opacity=0.6,
            nbinsx=10,
            name="Testing",
            histnorm="probability",
        )
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=ref_target_data.name,
        yaxis_title="Share",
    )
    return fig_to_json(fig)
