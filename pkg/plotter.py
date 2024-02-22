"""
'tokenomics_app' is script that generates plots most commonly seen in cryptocurrency 
token economics writeups. 

Classes: 
    AllocationGroup
    PlotterTokenomicsV1: Plotter for Tokenomics v1 (2022-05-29)
    PlotterTokenomicsV0: Plotter from Feb., 2022
    PlotterCustom: 
"""

import dataclasses
import os
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pkg import vesting
from pkg.const import TOKEN_SUPPLY_YEARS


class FontFamily:
    """An enum class for font families. Not all font families are supported by
    plotly dash.
    """

    IbmPlexMono = "IBM Plex Mono"
    Consolas = "Consolas"
    CourierNew = "Courier New"
    Main = "Inter"
    # Main = "DM Sans" # Seems to not be available


@dataclasses.dataclass
class AllocationGroup:
    name: str
    pct: float  # e.g. 20 for 20%
    color: str
    vi: vesting.VestingInfo = None


def save_figure(fig: go.Figure, plot_fname: str, file_type: str):
    """Save the given figure to a file.

    Args:
      fig (go.Figure): Graph object for the plot.
      plot_fname: File name for the plot.
      file_type: Ex: "svg", "png", "html".
    """
    if not os.path.exists(os.path.join("plots")):
        os.mkdir(os.path.join("plots"))

    if file_type == "html":
        fig.write_html(os.path.join("plots", f"{plot_fname}.{file_type}"))
    else:
        fig.write_image(os.path.join("plots", f"{plot_fname}.{file_type}"))


class Colors:
    PURPLE = "rgb(100, 80, 194)"
    SKY_BLUE = "rgb(96, 156, 212)"
    PINK = "rgb(200, 124, 226)"
    GOLD = "rgb(213, 175, 96)"
    GREEN = "rgb(130, 207, 179)"
    RED = "rgb(255, 0, 0)"
    YELLOW = "rgb(255, 255, 0)"

    LOGO_PINK = "rgb(255, 212, 229)"
    LOGO_TURQUOISE = "rgb(83, 77, 224)"
    LOGO_YELLOW = "rgb(255, 243, 204)"
    LOGO_BLACK = "rgb(7, 0, 19)"


class Group:
    TEAM = "Core Contributors"
    POST_SEED = "Investors (Post-Seed Bridge Round)"
    SEED = "Investors (Seed)"
    COMMUNITY = "Community"
    PUBLIC_SALE = "Public Sale"  # CoinList
    STRATEGIC_ADVISORS = "Strategic Advisors"
    FLEX = "Flex"


class PlotterTokenomicsV1:
    """Plotter for Tokenomics v2 (2024-01-26)
    Tokenomics v1 (2022-05-29)

    Methods:
        setup_token_distrib_area
        plot_token_distrib_area
        plot_final_token_supply
    """

    token_amount_df: pd.DataFrame
    token_cumulative_distrib_df: pd.DataFrame

    total_supply = 1.5e9
    category_pct_map: Dict[str, float]
    category_color_map: Dict[str, str]
    category_order: List[str]
    category_color_map: Dict[str, str]

    def __init__(self):
        self.groups = [
            # Team
            AllocationGroup(
                Group.TEAM,
                0.1535,
                Colors.PINK,
                vi=vesting.VestingInfo(
                    cliff_pct=0.1, vest_start_month=9, vest_end_month=24
                ),
            ),
            # SEED
            AllocationGroup(
                Group.SEED,
                0.08132871,
                Colors.SKY_BLUE,
                vi=vesting.VestingInfo(
                    cliff_pct=0.25, vest_start_month=9, vest_end_month=45
                ),
            ),
            # Bridge round
            AllocationGroup(
                Group.POST_SEED,
                0.04102564,
                Colors.GOLD,
                vi=vesting.VestingInfo(
                    cliff_pct=0, vest_start_month=6, vest_end_month=36
                ),
            ),
            # Strategic Advisors
            AllocationGroup(
                Group.STRATEGIC_ADVISORS,
                0.035,
                Colors.RED,
                vi=vesting.VestingInfo(
                    cliff_pct=0.25, vest_start_month=9, vest_end_month=39
                ),
            ),
            # Coinlist
            AllocationGroup(
                Group.PUBLIC_SALE,
                0.08,
                Colors.GREEN,
                vi=vesting.VestingInfo(
                    cliff_pct=0.1, vest_start_month=0, vest_end_month=12
                ),
            ),
            # Flex
            AllocationGroup(
                Group.FLEX,
                0.00530307,
                Colors.YELLOW,
                vi=vesting.VestingInfo(
                    cliff_pct=0, vest_start_month=0, vest_end_month=36
                ),
            ),
            # Community
            AllocationGroup(Group.COMMUNITY, 0.60, Colors.PURPLE),
        ]
        self.category_color_map = {g.name: g.color for g in self.groups}
        self.category_pct_map = {g.name: g.pct for g in self.groups}
        self.category_order = None

    def setup_token_distrib_area(
        self,
        num_time_points: int = int(1e5),
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
        """_summary_

        Args:
            num_time_points (int, optional): Number of data points on the time
                axis. Using a larger number gives more fine granularity at the
                cost of performance. Defaults to int(1e5).

        Returns:
            dist_map_by_category (Dict[str, np.ndarray])
            dist_map_full_duration (Dict[str, np.ndarray]):
        """

        # Set allocation for "Team"
        genesis_cliff_categories: List[str] = ["Treasury"]
        """
        dist_map_by_category: Dict[str, np.ndarray] = {
            category: np.linspace(
                start=self.total_supply * self.category_pct_map[category] * 0.25,
                stop=self.total_supply * self.category_pct_map[category],
                num=num_time_points * 4 // 8,
            )
            for category in genesis_cliff_categories
        }
        ones_tail = np.ones(num_time_points // 2, dtype=float)
        for category, head in dist_map_by_category.items():
            dist_map_by_category[category] = np.concatenate([head, ones_tail * head[-1]])
        assert all(
            [arr.shape[0] == num_time_points for arr in dist_map_by_category.values()]
        )
        """
        dist_map_by_category: Dict[str, np.ndarray] = {}

        for group in self.groups:
            if group.vi is None:
                continue
            dist_map_by_category[group.name] = group.vi.distrib_vec(
                group_pct=self.category_pct_map[group.name]
            )

        # category = GroupType.PUBLIC_SALE
        # vi = vesting.VestingInfo(
        #     cliff_pct=0.1, vest_start_month=0, vest_end_month=12)
        # dist_map_by_category[category] = vi.distrib_vec(
        #     group_pct=self.category_pct_map[category])

        # category = GroupType.PRIVATE
        # vi = vesting.VestingInfo(
        #     cliff_pct=0, vest_start_month=0, vest_end_month=36)
        # dist_map_by_category[category] = vi.distrib_vec(
        #     group_pct=self.category_pct_map[category])

        # category = GroupType.SEED
        # vi = vesting.VestingInfo(
        #     cliff_pct=0.25, vest_start_month=9, vest_end_month=45)
        # dist_map_by_category[category] = vi.distrib_vec(
        #     group_pct=self.category_pct_map[category])

        # category = GroupType.TEAM
        # vi = vesting.VestingInfo(
        #     cliff_pct=0.25, vest_start_month=12, vest_end_month=24)
        # dist_map_by_category[category] = vi.distrib_vec(
        #     group_pct=self.category_pct_map[category])

        assert all(
            [arr.shape[0] == num_time_points for arr in dist_map_by_category.values()]
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
        #
        incentive_phases: List[float] = (
            [17.35483871, 12.09677419, 10.87096774, 8.06451613]
            + [8.06451613, 7.25806452, 6.4516129, 5.64516129]
            + [4.83870968, 4.03225806, 3.22580645, 2.82258065]
            + [2.41935484, 2.41935484, 2.41935484, 2.01612903]
        )
        """incentive_phases (List[float]): A breakdown of percentages of the 
        community distribution. 
        - Q: Why are there 16 phases?
          Each incentive phase lasts 6 months. Since the community distribution
          comes out across a time span of 8 years, there are 16 phases.
        """
        assert abs(np.array(incentive_phases).sum() - 100) <= 0.01
        community_allocation: List[np.ndarray] = []
        start_supply_pct = 0
        group = "Community"
        for idx, phase_pct in enumerate(np.array(incentive_phases).cumsum()):
            phase_pct: float
            stop_supply_pct = (
                (phase_pct / 100) * self.total_supply * self.category_pct_map[group]
            )
            community_allocation.append(
                np.linspace(
                    start=start_supply_pct,
                    stop=stop_supply_pct,
                    num=int(num_time_points / TOKEN_SUPPLY_YEARS / 2),
                )
            )
            start_supply_pct = stop_supply_pct
        dist_map_full_duration: Dict[str : np.ndarray] = {
            group: np.concatenate(community_allocation)
        }
        assert all(
            [arr.shape[0] == num_time_points for arr in dist_map_full_duration.values()]
        )

        return dist_map_by_category, dist_map_full_duration

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
        dist_map_by_category: Dict[str, np.ndarray]
        dist_map_full_duration: Dict[str, np.ndarray]
        dist_map_by_category, dist_map_full_duration = self.setup_token_distrib_area()

        num_time_points: int = [v for v in dist_map_by_category.values()][0].size
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
        for idx, category in enumerate(dist_map_full_duration):
            self.category_order.append(category)

            assert idx <= len(self.category_color_map)
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=dist_map_full_duration[category],
                    hoverinfo="x+y",
                    mode="lines",
                    line=dict(width=0.5, color=self.category_color_map[category]),
                    stackgroup="one",
                    name=category.upper(),
                ),
            )

        for new_idx, category in enumerate(dist_map_by_category):
            self.category_order.append(category)
            new_idx = idx + new_idx + 1
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=dist_map_by_category[category],
                    hoverinfo="x+y",
                    mode="lines",
                    line=dict(width=0.5, color=self.category_color_map[category]),
                    stackgroup="one",  # define stack group
                    name=category.upper(),
                )
            )

        title: str = "Nibiru Chain (NIBI) Token Release Schedule"
        fig.update_layout(
            title=title,
            template="none",
            font_family=FontFamily.Main,
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
                save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig

    def plot_final_token_supply(
        self, save: bool = False, save_types: List[str] = ["svg"], pie_type: str = "pie"
    ) -> go.Figure:
        """Creates a pie or sunburst chart for the token supply splits at
        maturity.

        Args:
            save (bool, optional): _description_. Defaults to False.
            save_types (List[str], optional): _description_. Defaults to ["svg"].
            pie_type (str, optional): _description_. Defaults to "pie".

        Raises:
            ValueError: _description_

        Returns:
            go.Figure: _description_
        """

        title: str = "Nibiru Chain (NIBI) Token Distribution at Maturity"
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
                color_discrete_sequence=[v for v in self.category_color_map.values()],
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
            font_family=FontFamily.Main,
        )

        plot_fname: str = "final_token_supply"
        if save:
            for save_type in save_types:
                save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig


class PlotterTokenomicsV0:
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
                save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)

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
            TEAM="Team",
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
                save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
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
                save_figure(fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig


class PlotterCustom:
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
