"""
'tokenomics_app' is script that generates plots most commonly seen in cryptocurrency 
token economics writeups. 

Classes: 
    AllocationGroup
    TokenomicsPlotterV1: Plotter for Tokenomics v1 (2022-05-29)
    TokenomicsPlotterV0: Plotter from Feb., 2022
"""
# mypy: ignore_missing_imports = True
import os
import dataclasses
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.express.colors import sequential
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# FONT_FAMILY: str = "IBM Plex Mono"
FONT_FAMILY: str = "Consolas"
# FONT_FAMILY: str = "Courier New"


@dataclasses.dataclass
class AllocationGroup:
    name: str
    pct: float  # e.g. 20 for 20%
    color: str


def save_figure(fig: go.Figure, plot_fname: str, file_type: str):
    if not os.path.exists(os.path.join("plots")):
        os.mkdir(os.path.join("plots"))

    if file_type == "html":
        fig.write_html(os.path.join("plots", f"{plot_fname}.{file_type}"))
    else:
        fig.write_image(os.path.join("plots", f"{plot_fname}.{file_type}"))


class TokenomicsPlotterV1:
    """Plotter for Tokenomics v1 (2022-05-29)
    
    Methods: 
        setup_token_distrib_area
        plot_token_distrib_area
        plot_final_token_supply
    """

    token_amount_df: pd.DataFrame
    token_cumulative_distrib_df: pd.DataFrame

    total_supply = 1.5e9
    category_pct_map: Dict[str, float] = {
        "Team": 0.17,
        "Treasury": 0.04,
        "Private": 0.12,
        "Seed": 0.07,
        "Community": 0.60,
    }
    category_order: List[str]

    colors: List[str] = [
        "#" + c for c in ["005d5d", "9f1853", "570408", "6929c4", "1192e8"]
    ]
    category_color_map: Dict[str, str]

    def __init__(self):
        self.category_color_map = {
            category: self.colors[idx]
            for idx, category in enumerate(self.category_pct_map)
        }
        self.category_order = None

    def setup_token_distrib_area(
        self,
        num_time_points: int = int(1e5),
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
        """_summary_

        Args:
            num_time_points (int, optional): _description_. Defaults to int(1e5).

        Returns:
            Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
                category_vest_map, eight_year_vest_map
        """

        # Set allocation for "Team"
        genesis_cliff_categories: List[str] = ["Treasury"]
        category_vest_map: Dict[str, np.ndarray] = {
            category: np.linspace(
                start=self.total_supply * self.category_pct_map[category] * 0.25,
                stop=self.total_supply * self.category_pct_map[category],
                num=num_time_points * 4 // 8,
            )
            for category in genesis_cliff_categories
        }
        ones_tail = np.ones(num_time_points // 2, dtype=float)
        for category, head in category_vest_map.items():
            category_vest_map[category] = np.concatenate([head, ones_tail * head[-1]])
        assert all(
            [arr.shape[0] == num_time_points for arr in category_vest_map.values()]
        )

        # Set allocation for other linear vesters
        four_year_vest_categories: List[str] = ["Team", "Private", "Seed"]
        for category in four_year_vest_categories:
            category_vest_map[category] = np.linspace(
                start=self.total_supply * self.category_pct_map[category] * 0.25,
                stop=self.total_supply * self.category_pct_map[category],
                num=num_time_points * 3 // 8,
            )

        ones_tail = np.ones(num_time_points // 2, dtype=float)
        for category, head in category_vest_map.items():
            if category not in genesis_cliff_categories:
                zeros_before_head = np.zeros(num_time_points // 8, dtype=float)
                head = np.concatenate([zeros_before_head, head])
                category_vest_map[category] = np.concatenate(
                    [head, ones_tail * head[-1]]
                )

        assert all(
            [arr.shape[0] == num_time_points for arr in category_vest_map.values()]
        )

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
        category = "Community"
        for idx, phase_pct in enumerate(np.array(incentive_phases).cumsum()):
            stop = (
                (phase_pct / 100) * self.total_supply * self.category_pct_map[category]
            )
            community_allocation.append(
                np.linspace(
                    start,
                    stop=stop,
                    num=int(num_time_points / 16),
                )
            )
            start = stop
        eight_year_vest_map = {category: np.concatenate(community_allocation)}
        assert all(
            [arr.shape[0] == num_time_points for arr in eight_year_vest_map.values()]
        )

        return category_vest_map, eight_year_vest_map

    def plot_token_distrib_area(
        self,
        save: bool = False,
        save_types: List[str] = ["svg"],
    ) -> go.Figure:
        """_summary_

        Args:
            save (bool, optional): _description_. Defaults to False.
            save_types (List[str], optional): _description_. Defaults to ["svg"].

        Returns:
            go.Figure: _description_
        """
        cvm: Dict[str, np.ndarray]
        eyvm: Dict[str, np.ndarray]
        cvm, eyvm = self.setup_token_distrib_area()

        num_time_points: int = [v for v in cvm.values()][0].size
        time_axis = np.linspace(start=0, stop=8, num=num_time_points)
        x = time_axis
        layout = go.Layout(
            {
                "showlegend": True,
                "xaxis": {"title": "Time (years)"},
                "yaxis": {"title": "NIBI amount"},
            }
        )
        fig = go.Figure(layout=layout)

        self.category_order = []
        for idx, category in enumerate(eyvm):
            self.category_order.append(category)

            assert idx <= len(self.colors)
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=eyvm[category],
                    hoverinfo="x+y",
                    mode="lines",
                    line=dict(width=0.5, color=self.category_color_map[category]),
                    stackgroup="one",
                    name=category.upper(),
                ),
            )

        for new_idx, category in enumerate(cvm):
            self.category_order.append(category)
            new_idx = idx + new_idx + 1
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=cvm[category],
                    hoverinfo="x+y",
                    mode="lines",
                    line=dict(width=0.5, color=self.category_color_map[category]),
                    stackgroup="one",  # define stack group
                    name=category.upper(),
                )
            )

        title: str = "NIBI’s 8-year token release schedule"
        fig.update_layout(
            title=title,
            template="none",
            font_family=FONT_FAMILY,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )

        plot_fname = "token_release_area"
        if save:
            for save_type in save_types:
                save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type
                )
        return fig

    def plot_final_token_supply(
        self, save: bool = False, save_types: List[str] = ["svg"], pie_type: str = "pie"
    ) -> go.Figure:

        title: str = "NIBI’s token distribution at maturity, 8-years after launch"
        subtitle: str = ""

        final_distrib: Dict[str, float] = self.category_pct_map
        names: List[str] = list(final_distrib.keys())
        names = [s.upper() for s in names]
        values = [v for v in final_distrib.values()]

        # 'final_distrib_df' columns: Group, Tokens, Category, Category_sum
        final_distrib_df: pd.DataFrame = pd.DataFrame(dict(Group=names, Tokens=values))

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(
                f"Invalid 'pie_type': {pie_type}." " Must be pie or sunburst"
            )
        fig: go.Figure
        if pie_type == "pie":
            fig = px.pie(
                data_frame=final_distrib_df,
                values="Tokens",
                names="Group",
                color="Group",
                color_discrete_sequence=self.colors,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo="percent", textposition="outside")
        if pie_type == "sunburst":
            fig = px.sunburst(
                data_frame=final_distrib_df,
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
            template="none",
            font_family=FONT_FAMILY,
        )

        plot_fname: str = "final_token_supply"
        if save:
            for save_type in save_types:
                save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type
                )
        return fig


class TokenomicsPlotterV0:
    """Plotter from Feb., 2022"""

    token_supply_df: pd.DataFrame
    token_distrib_df: pd.DataFrame

    def __init__(self) -> None:
        df: pd.DataFrame = pd.read_csv(os.path.join("data", "token_distribution.csv"))
        df.month = df.month.apply(self.parse_date_column)

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
    def parse_date_column(date: str) -> pd.Timestamp:
        date = date.lstrip("(").rstrip(")")
        numbers_in_date: List[int] = [int(num) for num in date.split(",")]
        year, month, day = numbers_in_date[:3]
        date = f"{year}-{month}-{day}"
        return pd.Timestamp(date)

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
                save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type
                )

        return fig

    def plot_token_release_schedule_area(
        self,
    ) -> go.Figure:
        df = self.token_distrib_df
        x = df.index  # dates
        fig = go.Figure()
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
        plot_df: pd.DataFrame = pd.DataFrame(dict(Group=names, Tokens=values))
        plot_df = plot_df[plot_df != 0]
        print(f"Genesis supply: {plot_df.sum()}")

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
        plot_df["Category"] = plot_df.Group.apply(lambda g: category_map[g])
        plot_df["Category_sum"] = plot_df.Category.apply(
            lambda c: plot_df.Tokens[plot_df.Category == c].sum()
        )

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(
                f"Invalid 'pie_type': {pie_type}." " Must be pie or sunburst"
            )

        fig: go.Figure
        if pie_type == "pie":
            fig = px.pie(
                data_frame=plot_df,
                values="Tokens",
                names="Group",
                color="Group",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo="percent", textposition="outside")
        if pie_type == "sunburst":
            fig = px.sunburst(
                data_frame=plot_df,
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
                save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type
                )
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
        # 'final_distrib_df' columns: Group, Tokens, Category, Category_sum
        final_distrib_df: pd.DataFrame = pd.DataFrame(dict(Group=names, Tokens=values))

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
        final_distrib_df["Category"] = final_distrib_df.Group.apply(
            lambda g: category_map[g]
        )
        final_distrib_df["Category_sum"] = final_distrib_df.Category.apply(
            lambda c: final_distrib_df.Tokens[final_distrib_df.Category == c].sum()
        )

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(
                f"Invalid 'pie_type': {pie_type}." " Must be pie or sunburst"
            )
        fig: go.Figure
        if pie_type == "pie":
            fig = px.pie(
                data_frame=final_distrib_df,
                values="Tokens",
                names="Group",
                color="Group",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo="percent", textposition="outside")
        if pie_type == "sunburst":
            fig = px.sunburst(
                data_frame=final_distrib_df,
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
                save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type
                )
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
    plotter_v0 = TokenomicsPlotterV0()
    plotter_v1 = TokenomicsPlotterV1()
    # custom = CustomPlotter()

    app = dash.Dash()
    figures: List[go.Figure] = [
        plotter_v1.plot_token_distrib_area(save=True),
        plotter_v1.plot_token_distrib_area(save=True),
        plotter_v1.plot_final_token_supply(save=True, pie_type="pie"),
        # plotter_v0.plot_token_release_schedule_area()),
        # plotter_v0.plot_token_release_schedule_line(save=True)),
        # plotter_v0.plot_genesis_supply(save=True, pie_type="sunburst")),
        # custom.plot_foo()),
    ]
    app.layout = html.Div(children=[dcc.Graph(figure=figure) for figure in figures])

    app.run_server(debug=True, use_reloader=False)
