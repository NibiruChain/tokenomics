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
from typing import List

class TokenDistributionPlotter:

    token_supply_df: pd.DataFrame
    token_distrib_df: pd.DataFrame

    def __init__(self) -> None:
        df = pd.read_csv(os.path.join("data", "token_distribution.csv"))
        df.month = df.month.apply(self.parse_month)

        token_supply_columns: List[str] = [
            "month", "total_supply", "pct_max_supply"]
        self.token_supply_df = df[token_supply_columns].copy(deep=True)
        self.token_supply_df = self.token_supply_df.set_index("month")

        token_distrib_columns: List[str] = [
            "month", "seed", "team", "treasury", "insurance_fund", "stakers", 
            "LPs", "LA_incentives", "IA_incentives", "staking_airdrop", "IDO"]
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
            fig.write_html(os.path.join(
                "plots", f"{plot_fname}.{file_type}"))
        else:
            fig.write_image(os.path.join(
                "plots", f"{plot_fname}.{file_type}"))


    def plot_token_release_schedule(self,
                                    save: bool = False, 
                                    save_types: List[str] = ["svg"], 
                                    ) -> go.Figure:

        token_release_schedule: pd.DataFrame = self.token_distrib_df.cumsum()

        fig: go.Figure = px.line(
            data_frame=token_release_schedule, 
            title="Token Release Schedule",
            labels=dict(value="Tokens", month="Date", variable="Group")
            )


        plot_fname = "token_release_schedule"
        if save:
            for save_type in save_types:
                self.save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type)

        return fig
    
    def plot_genesis_supply(self, 
                            save: bool = False, 
                            save_types: List[str] = ["svg"], 
                            pie_type: str = "pie") -> go.Figure:

        title: str = "Genesis Supply"
        subtitle: str = "Token distribution at the time of protocol launch"

        genesis_distrib: pd.Series = self.token_distrib_df.cumsum().iloc[0, :]
        names: List[str] = list(genesis_distrib.index)
        names = [s.upper() for s in names]
        values = genesis_distrib.values
        genesis_distrib: pd.DataFrame = pd.DataFrame(
            dict(Group=names, Tokens=values))
        genesis_distrib = genesis_distrib[genesis_distrib != 0]
        print(f"Genesis supply: {genesis_distrib.sum()}")

        # Append "Category" column
        category_map: dict[str, str] = dict(
            SEED="Early Backers", TEAM="Core Team", TREASURY="Community", 
            INSURANCE_FUND="Community", STAKERS="Community", LPS="Community", 
            LA_INCENTIVES="Community", IA_INCENTIVES="Community", 
            STAKING_AIRDROP="Community", IDO="Early Backers")
        genesis_distrib["Category"] = genesis_distrib.Group.apply(
            lambda g: category_map[g])
        genesis_distrib["Category_sum"] = genesis_distrib.Category.apply(
            lambda c: genesis_distrib.Tokens[genesis_distrib.Category == c].sum() 
        )

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(f"Invalid 'pie_type': {pie_type}." 
                             " Must be pie or sunburst")
        if pie_type == "pie":
            fig: go.Figure = px.pie(
                data_frame=genesis_distrib, values="Tokens", names="Group", 
                color="Group",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo='percent', textposition='outside')
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
                margin = dict(t=2 * plot_margin, l=plot_margin, r=plot_margin, 
                              b=0)
            )

        plot_fname: str = "genesis_supply"
        if save:
            for save_type in save_types:
                self.save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig

    def plot_final_token_supply(self,
                                save: bool = False, 
                                save_types: List[str] = ["svg"], 
                                pie_type:str = "pie") -> go.Figure:

        title: str = "Final Token Supply"
        subtitle: str = "Cumulative token distribution 4 years after protocol launch"

        final_distrib: pd.Series = self.token_distrib_df.cumsum().iloc[-1, :]
        names: List[str] = list(final_distrib.index)
        names = [s.upper() for s in names]
        values = final_distrib.values
        final_distrib: pd.DataFrame = pd.DataFrame(
            dict(Group=names, Tokens=values))
        
        # Append "Category" column
        category_map: dict[str, str] = dict(
            SEED="Early Backers", TEAM="Core Team", TREASURY="Community", 
            INSURANCE_FUND="Community", STAKERS="Community", LPS="Community", 
            LA_INCENTIVES="Community", IA_INCENTIVES="Community", 
            STAKING_AIRDROP="Community", IDO="Early Backers")
        final_distrib["Category"] = final_distrib.Group.apply(
            lambda g: category_map[g])
        final_distrib["Category_sum"] = final_distrib.Category.apply(
            lambda c: final_distrib.Tokens[final_distrib.Category == c].sum() 
        )

        if not pie_type in ["pie", "sunburst"]:
            raise ValueError(f"Invalid 'pie_type': {pie_type}." 
                             " Must be pie or sunburst")
        if pie_type == "pie":
            fig: go.Figure = px.pie(
                data_frame=final_distrib, values="Tokens", names="Group", 
                color="Group",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"{title}<br><br><sup>{subtitle}</sup>",
            )
            # fig.update_traces(textinfo='percent+label', textposition='inside')
            fig.update_traces(textinfo='percent', textposition='outside')
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
                margin = dict(t=2 * plot_margin, l=plot_margin, r=plot_margin, 
                              b=0)
            )

        plot_fname: str = "final_token_supply"
        if save:
            for save_type in save_types:
                self.save_figure(
                    fig=fig, plot_fname=plot_fname, file_type=save_type)
        return fig


if __name__ == "__main__":
    tdp = TokenDistributionPlotter()

    app = dash.Dash()
    app.layout = html.Div(children=[
        dcc.Graph(figure=tdp.plot_token_release_schedule(save=True)), 
        dcc.Graph(figure=tdp.plot_genesis_supply(save=True, pie_type="sunburst")), 
        dcc.Graph(figure=tdp.plot_final_token_supply(save=True, pie_type="sunburst"))
    ])

    app.run_server(debug=True, use_reloader=False)