from pkg import plotter
from pkg import groups
from typing import List

import dash
import dash_core_components as dcc
import plotly.graph_objects as go

if __name__ == "__main__":
    plotter_v0 = plotter.TokenomicsPlotterV0()
    plotter_v1 = plotter.TokenomicsPlotterV1()
    # custom = plotter.CustomPlotter()

    app = dash.Dash()
    figures: List[go.Figure] = [
        plotter_v1.plot_token_distrib_area(save=True),
        plotter_v1.plot_final_token_supply(save=True, pie_type="pie"),
        # plotter_v0.plot_token_release_schedule_area()),
        # plotter_v0.plot_token_release_schedule_line(save=True)),
        # plotter_v0.plot_genesis_supply(save=True, pie_type="sunburst")),
        # custom.plot_foo()),
    ]
    app.layout = html.Div(children=[dcc.Graph(figure=figure) for figure in figures])

    app.run_server(debug=True, use_reloader=False)
