# import matplotlib
import pandas as pd
import os
import pprint
# os.environ["MPLBACKEND"] = "TKAgg"
import numpy as np
from pkg import plotter
from pkg import groups
from pkg import decay
from typing import List, Tuple

import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html

from dataclasses import dataclass

SUPPLY_AT_MATURITY = 810_600_000


@dataclass
class DecayResult:
    f_t: np.ndarray
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

    def target_vector(self):
        return self.normal_f_t * SUPPLY_AT_MATURITY

    def poly_coefs(self, degree=5):
        snapshots = self.target_vector()
        return np.polyfit(self.times, snapshots, degree)

    def poly_fn(self):
        coefs = self.poly_coefs()
        return np.poly1d(coefs)

    def plot_polynomial(self) -> go.Figure:
        x = self.times

        poly_fn = self.poly_fn()
        y_poly = poly_fn(self.times)
        y_target = self.target_vector()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y_poly, mode='lines', name='Polynomial Fit'))
        fig.add_trace(go.Scatter(x=x, y=y_target,
                      mode='lines', name='Target Vector'))

        coef_display = [f"{c:.3e}" for c in self.poly_coefs()]
        fig.update_layout(
            title='Polynomial Fit and Target Vector',
            xaxis_title='Time',
            yaxis_title='Value',
            font=dict(family="Inter"),
            annotations=[
                dict(xref="paper", yref="paper", x=0.9, y=0.9, showarrow=False,
                     text=f"Polynomial Coefs:\n{coef_display}", align="right"),
                dict(xref="paper", yref="paper", x=0.9, y=0.8, showarrow=False,
                     text=f"Supply (Fit Line):{round(y_poly.sum()):.3e}", align="right"),
                dict(xref="paper", yref="paper", x=0.9, y=0.7, showarrow=False,
                     text=f"Supply (Target Line):{y_target.sum():.3e}", align="right"),
            ],
        )

        # Show the figure
        return fig


if __name__ == "__main__":

    def plotting():
        # plotter_v0 = plotter.PlotterTokenomicsV0()
        plotter_v1 = plotter.PlotterTokenomicsV1()
        # custom = plotter.CustomPlotter()

        decay = do_decay(decay_factor=0.2)
        # decay.pprint()

        app = dash.Dash()
        figures: List[go.Figure] = [
            plotter_v1.plot_token_distrib_area(save=True, save_types=["png",
                                                                      "svg"]),
            plotter_v1.plot_final_token_supply(save=False, pie_type="pie"),
            decay.plot_polynomial(),
            # plotter_v0.plot_token_release_schedule_area()),
            # plotter_v0.plot_token_release_schedule_line(save=True)),
            # plotter_v0.plot_genesis_supply(save=True, pie_type="sunburst")),
            # custom.plot_foo()),
        ]
        app.layout = html.Div(
            children=[dcc.Graph(figure=figure) for figure in figures])

        app.run_server(debug=True, use_reloader=False)

    def do_decay(decay_factor=0.5, time_years=8) -> DecayResult:
        times = np.linspace(start=0, stop=time_years,
                            num=time_years * 12)  # in months
        # times = np.linspace(start=0, stop=time_span, num=time_span) # in years
        f_t = decay.ExponentialDecay.decay_amts(
            amt_start=100, decay_factor=decay_factor, times=times
        )
        print("\n————————————————————————————————————————")
        print(f"decay_factor: {decay_factor}")
        norm_f_t = f_t / f_t.sum()

        return DecayResult(f_t=f_t, times=times, normal_f_t=norm_f_t)

    # do_decay()
    # do_decay(0.4)
    # do_decay(0.3)
    # do_decay(0.1)
    plotting()

# %%
