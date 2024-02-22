# import matplotlib
import pprint
from dataclasses import dataclass
from typing import List

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go

from pkg import decay, plotter

SUPPLY_AT_MATURITY = 807_735_000


@dataclass
class DecayResult:
    times: np.ndarray
    normal_f_t: np.ndarray

    def pprint(self):
        print("times:")
        pprint.pprint(self.times)
        print("normal_f(t) := f(t) / f(t).sum()")
        pprint.pprint(self.normal_f_t)

        print("normal_f(t) as a list for excel")
        for f in self.normal_f_t:
            print(f)

    def plot_polynomial(self) -> go.Figure:
        x = self.times
        y_target = self.normal_f_t * SUPPLY_AT_MATURITY
        poly_coefs = np.polyfit(x, y_target, 8)
        y_poly = np.poly1d(poly_coefs)(x)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y_poly, mode='lines', name='Polynomial Fit'))
        fig.add_trace(go.Scatter(x=x, y=y_target, mode='lines', name='Target Vector'))

        coef_display = [f"{c:.6}" for c in poly_coefs]
        fig.update_layout(
            title='Polynomial Fit and Target Vector',
            xaxis_title='Time',
            yaxis_title='Value',
            font=dict(family="Inter"),
            annotations=[
                dict(
                    xref="paper",
                    yref="paper",
                    x=0.9,
                    y=0.9,
                    showarrow=False,
                    text=f"Polynomial Coefs:\n{coef_display}",
                    align="right",
                ),
                dict(
                    xref="paper",
                    yref="paper",
                    x=0.9,
                    y=0.8,
                    showarrow=False,
                    text=f"Supply (Fit Line):{round(y_poly.sum()):.6f}",
                    align="right",
                ),
                dict(
                    xref="paper",
                    yref="paper",
                    x=0.9,
                    y=0.7,
                    showarrow=False,
                    text=f"Supply (Target Line):{y_target.sum():.6f}",
                    align="right",
                ),
            ],
        )

        # Show the figure
        return fig


def do_decay(decay_rate=0.5, time_years=8) -> DecayResult:
    print("\n————————————————————————————————————————")
    print(f"decay_rate: {decay_rate}")

    # in months
    months = np.arange(1, time_years * 12 + 1, 1)
    # times = np.linspace(start=0, stop=time_span, num=time_span) # in years
    print(f"months: {months}")

    f_t = decay.exponential_decay(
        amt_start=100, decay_rate=decay_rate, times=months
    )
    normalized_f_t = f_t / f_t.sum()
    print(f"norm_f_t: {normalized_f_t}")
    print(f"norm_f_t.sum(): {normalized_f_t.sum()}")

    return DecayResult(normal_f_t=normalized_f_t, times=months)


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    # plotter_v0 = plotter.PlotterTokenomicsV0()
    plotter_v1 = plotter.PlotterTokenomicsV1()
    # custom = plotter.CustomPlotter()

    d = do_decay(decay_rate=0.2)
    # d.pprint()

    app = dash.Dash()
    figures: List[go.Figure] = [
        plotter_v1.plot_token_distrib_area(save=True, save_types=["png", "svg"]),
        plotter_v1.plot_final_token_supply(save=False, pie_type="pie"),
        d.plot_polynomial(),
        # plotter_v0.plot_token_release_schedule_area()),
        # plotter_v0.plot_token_release_schedule_line(save=True)),
        # plotter_v0.plot_genesis_supply(save=True, pie_type="sunburst")),
        # custom.plot_foo()),
    ]
    app.layout = html.Div(children=[dcc.Graph(figure=figure) for figure in figures])

    app.run_server(debug=True, use_reloader=False)
