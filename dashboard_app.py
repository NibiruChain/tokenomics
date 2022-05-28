#%%
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.express.colors import sequential
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List


class GenericTokenDistributionPlotter:

    token_amount_df: pd.DataFrame
    token_cumulative_distrib_df: pd.DataFrame

    total_supply = 1.5e9
    category_pct_map: Dict[str, float] = {
        "Team": 0.17,
        "Treasury": 0.04,
        "Private": 0.12,
        "Seed": 0.07,
        "Community": 0.6,
    }

    colors: List[str] = [
        "#" + c for c in 
        ["005d5d", "9f1853", "570408", "6929c4", "1192e8"]
        ]
    category_color_map: Dict[str, str]

    def __init__(self):
        self.category_color_map = {
            cat: self.colors[idx] for idx, cat in enumerate(self.category_pct_map)
        }
        ...

    def plot_token_distrib_area(
        self, 
        save: bool = False,
        save_types: List[str] = ["svg"],
        ) -> go.Figure:

        time_points = int(1e5)

        four_year_vest_cats: List[str] = ["Team", "Treasury", "Private", "Seed"]

        four_year_vest_map: Dict[str, np.ndarray] = {
            cat: np.linspace(
                start=0,
                stop=self.total_supply * self.category_pct_map[cat],
                num=time_points // 2,
            )
            for cat in four_year_vest_cats
        }
        ones_tail = np.ones(time_points // 2, dtype=float)
        for cat, head in four_year_vest_map.items():
            four_year_vest_map[cat] = np.concatenate([head, ones_tail * head[-1]])
        assert all([arr.shape[0] == time_points for arr in four_year_vest_map.values()])

        """
        >>> yp
        array([17.35483871, 12.09677419,  10.87096774,  8.06451613,  8.06451613,
                7.25806452,  6.4516129 ,  5.64516129,  4.83870968,  4.03225806,
                3.22580645,  2.41935484,  2.82258065,  2.41935484,  2.41935484,
                2.01612903])
        >>> yp.sum()
        100.0
        """
        # Juno opts for 30-17-9-6 over 12 phases
        eight_year_vest_cats: List[str] = ["Community"]
        incentive_phases: List[float] = [
            17.35483871,
            12.09677419,
            10.87096774,
            8.06451613,
            8.06451613,
            7.25806452,
            6.4516129,
            5.64516129,
            4.83870968,
            4.03225806,
            3.22580645,
            2.41935484,
            2.82258065,
            2.41935484,
            2.41935484,
            2.01612903,
        ]
        community_allocation = []
        start = 0
        category: str = "Community"
        for idx, phase_pct in enumerate(np.array(incentive_phases).cumsum()):
            stop = (phase_pct / 100) * self.total_supply * self.category_pct_map[category]
            community_allocation.append(
                np.linspace(
                    start,
                    stop=stop,
                    num=int(time_points / 16),
                )
            )
            start = stop
        eight_year_vest_map = {category: np.concatenate(community_allocation)}
        assert all(
            [arr.shape[0] == time_points for arr in eight_year_vest_map.values()]
        )

        fyvm, eyvm = four_year_vest_map, eight_year_vest_map

        time_axis = np.linspace(start=0, stop=8, num=time_points)

        # x = ["a", "b", "c", "d"]
        x = time_axis
        colors = self.colors

        layout = go.Layout(
            {
                "showlegend": True,
                "xaxis": {"title": "Time (years)"},
                "yaxis": {"title": "NIBI amount"},
            }
        )
        fig = go.Figure(layout=layout)

        for idx, cat in enumerate(fyvm):
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=fyvm[cat],
                    hoverinfo="x+y",
                    mode="lines",
                    line=dict(width=0.5, color=colors[idx]),
                    stackgroup="one",  # define stack group
                    name=cat
                )
            )

        for new_idx, cat in enumerate(eyvm):
            new_idx = idx + new_idx + 1
            assert new_idx <= len(colors)
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=eyvm[cat],
                    hoverinfo="x+y",
                    mode="lines",
                    line=dict(width=0.5, color=colors[new_idx]),
                    stackgroup="one",
                    name=cat
                ),
            )

        fig.update_layout(
            font_family="IBM Plex Mono",
            # font_family="Consolas",
            # font_family="Courier New",
        )

        plot_fname = "token_release_area"
        if save:
            for save_type in save_types:
                self.save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig

    def plot_final_token_supply(
        self, save: bool = False, save_types: List[str] = ["svg"], pie_type: str = "pie"
    ) -> go.Figure:

        title: str = "Cumulative token distribution 8 years after protocol launch"
        subtitle: str = ""
        # subtitle: str = "Cumulative token distribution 8 years after protocol launch"

        final_distrib: Dict[str, float] = self.category_pct_map
        names: List[str] = list(final_distrib.keys())
        names = [s.upper() for s in names]
        values = [v for v in final_distrib.values()]

        # 'final_distrib' columns: Group, Tokens, Category, Category_sum
        final_distrib: pd.DataFrame = pd.DataFrame(dict(Group=names, Tokens=values))

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(
                f"Invalid 'pie_type': {pie_type}." " Must be pie or sunburst"
            )
        if pie_type == "pie":
            fig: go.Figure = px.pie(
                data_frame=final_distrib,
                values="Tokens",
                names="Group",
                color="Group",
                color_discrete_sequence=self.colors,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo="percent", textposition="outside")
        if pie_type == "sunburst":
            fig: go.Figure = px.sunburst(
                data_frame=final_distrib,
                path=["Category", "Group"],
                values="Tokens",
                color_discrete_sequence=px.colors.qualitative.Safe,
                title=f"{title}<br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(insidetextorientation="radial")
            plot_margin: int = 25
            fig.update_layout(
                margin=dict(t=2 * plot_margin, l=plot_margin, r=plot_margin, b=0)
            )

        fig.update_layout(
            font_family="IBM Plex Mono",
            # font_family="Consolas",
            # font_family="Courier New",
        )

        plot_fname: str = "final_token_supply"
        if save:
            for save_type in save_types:
                self.save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig


    @staticmethod
    def save_figure(fig: go.Figure, plot_fname: str, file_type: str):
        if not os.path.exists(os.path.join("plots")):
            os.mkdir(os.path.join("plots"))

        if file_type == "html":
            fig.write_html(os.path.join("plots", f"{plot_fname}.{file_type}"))
        else:
            fig.write_image(os.path.join("plots", f"{plot_fname}.{file_type}"))


class TokenDistributionPlotter:

    token_supply_df: pd.DataFrame
    token_distrib_df: pd.DataFrame

    def __init__(self) -> None:
        df = pd.read_csv(os.path.join("data", "token_distribution.csv"))
        df.month = df.month.apply(self.parse_month)

        token_supply_columns: List[str] = ["month", "total_supply", "pct_max_supply"]
        self.token_supply_df = df[token_supply_columns].copy(deep=True)
        self.token_supply_df = self.token_supply_df.set_index("month")

        token_distrib_columns: List[str] = [
            "month",
            "seed",
            "team",
            "treasury",
            "insurance_fund",
            "stakers",
            "LPs",
            "LA_incentives",
            "IA_incentives",
            "staking_airdrop",
            "IDO",
        ]
        self.token_distrib_df = df[token_distrib_columns].copy(deep=True)
        self.token_distrib_df = self.token_distrib_df.set_index("month")

    @staticmethod
    def parse_month(month: str) -> pd.Timestamp:
        month = month.lstrip("(").rstrip(")")
        numbers_in_month: List[int] = [int(num) for num in month.split(",")]
        year, month, day = numbers_in_month[:3]
        month: str = f"{year}-{month}-{day}"
        return pd.Timestamp(month)

    @staticmethod
    def save_figure(fig: go.Figure, plot_fname: str, file_type: str):
        if not os.path.exists(os.path.join("plots")):
            os.mkdir(os.path.join("plots"))

        if file_type == "html":
            fig.write_html(os.path.join("plots", f"{plot_fname}.{file_type}"))
        else:
            fig.write_image(os.path.join("plots", f"{plot_fname}.{file_type}"))

    def plot_token_release_schedule_line(
        self,
        save: bool = False,
        save_types: List[str] = ["svg"],
    ) -> go.Figure:

        token_release_schedule: pd.DataFrame = self.token_distrib_df.cumsum()

        fig: go.Figure = px.line(
            data_frame=token_release_schedule,
            title="Token Release Schedule",
            labels=dict(value="Tokens", month="Date", variable="Group"),
        )

        plot_fname = "token_release_schedule"
        if save:
            for save_type in save_types:
                self.save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)

        return fig

    def plot_token_release_schedule_area(
        self,
    ) -> go.Figure:
        df = self.token_distrib_df
        x = df.index  # dates
        fig = go.Figure()
        breakpoint()
        fig.add_trace(x=x, y=df)

        return fig

    def plot_genesis_supply(
        self, save: bool = False, save_types: List[str] = ["svg"], pie_type: str = "pie"
    ) -> go.Figure:

        title: str = "Genesis Supply"
        subtitle: str = "Token distribution at the time of protocol launch"

        genesis_distrib: pd.Series = self.token_distrib_df.cumsum().iloc[0, :]
        names: List[str] = list(genesis_distrib.index)
        names = [s.upper() for s in names]
        values = genesis_distrib.values
        genesis_distrib: pd.DataFrame = pd.DataFrame(dict(Group=names, Tokens=values))
        genesis_distrib = genesis_distrib[genesis_distrib != 0]
        print(f"Genesis supply: {genesis_distrib.sum()}")

        # Append "Category" column
        category_map: dict[str, str] = dict(
            SEED="Early Backers",
            TEAM="Core Team",
            TREASURY="Community",
            INSURANCE_FUND="Community",
            STAKERS="Community",
            LPS="Community",
            LA_INCENTIVES="Community",
            IA_INCENTIVES="Community",
            STAKING_AIRDROP="Community",
            IDO="Early Backers",
        )
        genesis_distrib["Category"] = genesis_distrib.Group.apply(
            lambda g: category_map[g]
        )
        genesis_distrib["Category_sum"] = genesis_distrib.Category.apply(
            lambda c: genesis_distrib.Tokens[genesis_distrib.Category == c].sum()
        )

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(
                f"Invalid 'pie_type': {pie_type}." " Must be pie or sunburst"
            )
        if pie_type == "pie":
            fig: go.Figure = px.pie(
                data_frame=genesis_distrib,
                values="Tokens",
                names="Group",
                color="Group",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo="percent", textposition="outside")
        if pie_type == "sunburst":
            fig: go.Figure = px.sunburst(
                data_frame=genesis_distrib,
                path=["Category", "Group"],
                values="Tokens",
                color_discrete_sequence=px.colors.qualitative.Safe,
                title=f"{title}<br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(insidetextorientation="radial")
            plot_margin: int = 25
            fig.update_layout(
                margin=dict(t=2 * plot_margin, l=plot_margin, r=plot_margin, b=0)
            )

        plot_fname: str = "genesis_supply"
        if save:
            for save_type in save_types:
                self.save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig

    def plot_final_token_supply(
        self, save: bool = False, save_types: List[str] = ["svg"], pie_type: str = "pie"
    ) -> go.Figure:

        title: str = "Final Token Supply"
        subtitle: str = "Cumulative token distribution 4 years after protocol launch"

        final_distrib: pd.Series = self.token_distrib_df.cumsum().iloc[-1, :]
        names: List[str] = list(final_distrib.index)
        names = [s.upper() for s in names]
        values = final_distrib.values
        # 'final_distrib' columns: Group, Tokens, Category, Category_sum
        final_distrib: pd.DataFrame = pd.DataFrame(dict(Group=names, Tokens=values))

        # Append "Category" column
        category_map: dict[str, str] = dict(
            SEED="Early Backers",
            TEAM="Core Team",
            TREASURY="Community",
            INSURANCE_FUND="Community",
            STAKERS="Community",
            LPS="Community",
            LA_INCENTIVES="Community",
            IA_INCENTIVES="Community",
            STAKING_AIRDROP="Community",
            IDO="Early Backers",
        )
        final_distrib["Category"] = final_distrib.Group.apply(lambda g: category_map[g])
        final_distrib["Category_sum"] = final_distrib.Category.apply(
            lambda c: final_distrib.Tokens[final_distrib.Category == c].sum()
        )

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(
                f"Invalid 'pie_type': {pie_type}." " Must be pie or sunburst"
            )
        if pie_type == "pie":
            fig: go.Figure = px.pie(
                data_frame=final_distrib,
                values="Tokens",
                names="Group",
                color="Group",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo="percent", textposition="outside")
        if pie_type == "sunburst":
            fig: go.Figure = px.sunburst(
                data_frame=final_distrib,
                path=["Category", "Group"],
                values="Tokens",
                color_discrete_sequence=px.colors.qualitative.Safe,
                title=f"{title}<br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(insidetextorientation="radial")
            plot_margin: int = 25
            fig.update_layout(
                margin=dict(t=2 * plot_margin, l=plot_margin, r=plot_margin, b=0)
            )

        plot_fname: str = "final_token_supply"
        if save:
            for save_type in save_types:
                self.save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig


class CustomPlotter:
    def plot_foo(self) -> go.Figure:
        data: List[dict] = [
            dict(name="Buybacks", pct=55),
            dict(name="Perp EF", pct=30),
            dict(name="Community Grants", pct=15),
        ]
        plot_df = pd.DataFrame(data, columns=["name", "pct"])
        fig: go.Figure = px.pie(
            plot_df,
            values="pct",
            color="name",
            names="name",
            color_discrete_sequence=[
                "darkblue",
                "royalblue",
                "lightcyan",
                "cyan",
            ],
        )
        fig.update_traces(textinfo="percent+label", textposition="inside")
        return fig


if __name__ == "__main__":
    tdp = TokenDistributionPlotter()
    # custom = CustomPlotter()
    gtdp = GenericTokenDistributionPlotter()

    app = dash.Dash()
    app.layout = html.Div(
        children=[
            # dcc.Graph(figure=tdp.plot_token_release_schedule_area()),
            # dcc.Graph(figure=tdp.plot_token_release_schedule_line(save=True)),
            # dcc.Graph(figure=tdp.plot_genesis_supply(save=True, pie_type="sunburst")),
            # dcc.Graph(figure=custom.plot_foo()),
            dcc.Graph(
                figure=gtdp.plot_final_token_supply(save=True, pie_type="pie")
            ),
            dcc.Graph(figure=gtdp.plot_token_distrib_area(save=True)),
        ]
    )

    app.run_server(debug=True, use_reloader=False)
