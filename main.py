import pprint
import io
import numpy as np
from pkg import plotter
from pkg import decay
from typing import List, Union

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go

from dataclasses import dataclass

SUPPLY_AT_MATURITY = 800_000_000


@dataclass
class DecayResult:
    f_t: np.ndarray
    times: np.ndarray
    normal_f_t: np.ndarray

    def pprint(self):
        out_buffer = io.StringIO()

        out_buffer.write("times:\n")
        pprint.pprint(self.times, stream=out_buffer)
        out_buffer.write("normal_f(t) := f(t) / f(t).sum()\n")
        pprint.pprint(self.normal_f_t, stream=out_buffer)

        out_buffer.write("Polynomial coefficients (decreasing order, "
                         + "the last coefficient is the intercept.):\n")
        pprint.pprint(self.poly_coefs(), stream=out_buffer)

        out_buffer.write("normal_f(t) as a list for excel\n")
        for f in self.normal_f_t:
            out_buffer.write(str(f) + "\n")

        pretty_str = out_buffer.getvalue()
        out_buffer.close()
        return pretty_str

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
        decay.pprint()

        app = dash.Dash()
        figures: List[go.Figure] = [
            # plot: Token release schedule
            plotter_v1.plot_token_distrib_area(save=True, save_types=["png",
                                                                      "svg"]),
            # plot: Token distribution at maturity
            plotter_v1.plot_final_token_supply(save=False, pie_type="pie"),
            # plot: Polynomial comparison
            decay.plot_polynomial(),
            # ----------------------- V0 Plots -----------------------
            # plotter_v0.plot_token_release_schedule_area()),
            # plotter_v0.plot_token_release_schedule_line(save=True)),
            # plotter_v0.plot_genesis_supply(save=True, pie_type="sunburst")),
            # custom.plot_foo()),
        ]

        def parse_figure(
            fig: Union[go.Figure, dcc.Markdown],
        ) -> Union[dcc.Graph, dcc.Markdown]:
            try:
                return dcc.Graph(figure=fig)
            except BaseException:
                assert isinstance(fig, dcc.Markdown)
                return fig

        app.layout = html.Div([
            html.Div(children=[parse_figure(fig=figure)
                     for figure in figures]),
            html.P(f"{decay.pprint()}"),
            # dcc.Markdown("""
            #                 # Hello there
            #                 """),
        ])

        app.run_server(debug=True, use_reloader=False)

    def do_decay(decay_factor=0.5, time_years=8) -> DecayResult:
        time_years = np.linspace(start=0, stop=time_years,
                                 num=time_years * 12)  # in months
        # times = np.linspace(start=0, stop=time_span, num=time_span) # in years
        f_t = decay.ExponentialDecay.decay_amts(
            amt_start=100, decay_factor=decay_factor, times=time_years
        )
        print("\n————————————————————————————————————————")
        print(f"decay_factor: {decay_factor}")
        norm_f_t = f_t / f_t.sum()

        times = [t for t, _ in enumerate(norm_f_t)]
        return DecayResult(f_t=f_t, times=times, normal_f_t=norm_f_t)

    plotting()

# %%
