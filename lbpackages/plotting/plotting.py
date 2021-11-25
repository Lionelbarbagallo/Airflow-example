"""Classes and functions to plot stocks data."""
from __future__ import annotations

import os
from typing import Union

import plotly.graph_objects as go
import plotly.offline as po

from lbpackages.models import dbclient
from lbpackages.query_db import query_db


class Button:
    """Represents an abstraction to create buttons used in a plotly plot.

    Attributes
    ----------
    mask: list of bool
        a list of booleans indicating which traces are visible upon selection.
    default_button: boolean
        indicates if these is the default final button of the plot (shows all traces together).
    label: str
        visible label for the trace
    title: str
        plot title when selected  trace.
    """

    def __init__(
        self,
        mask: str,
        ds: str,
        symbol: Union[None, str] = None,
        default_button: bool = False,
    ) -> None:
        """Constructor of the class.

        Parameters
        ----------
        mask: list of bool
            a list of booleans indicating which traces are visible upon selection.
        ds: str
            date of the report that will be used in the title.
        symbol: str
            ticker of the selected trace.
        default_button: boolean
            indicates if these is the default final button of the plot (shows all traces together).
        """
        self.default_button = default_button
        self.mask = mask

        if not self.default_button:
            self.label = f"{symbol}"
            self.title = f"{symbol} quotation time series - Daily report {ds}"
        else:
            self.label = "All Tickers"
            self.title = f"Stocks quotation time series - Daily report {ds}"

    def create_button(self: Button) -> dict:
        """Creates the button object.

        Parameters
        ----------
        self: Button
            a Button type object
        Returns
        -------
        button: dict
            a dictionary with the defined parameters of the button.
        """
        button = dict(
            label=self.label,
            method="update",
            args=[{"visible": self.mask}, {"title": self.title}],
        )
        return button


def create_buttons(grouped, ds):
    """Creates buttons for the given dataset.

    Parameters
    ----------
    grouped: pandas.core.groupby.generic.DataFrameGroupBy
        a stocks DataFramegrouped by "symbol"
    ds: str
        date of the report that will be used in the title.
    Yields
    -------
    dict
        a dictionary with the defined parameters of the button.
    """
    n_tickers = len(grouped)
    visibility = [False] * n_tickers

    for i in range(len(grouped)):
        mask = list(visibility)
        mask[i] = True

        symbol = list(grouped.groups.keys())[i]

        button = Button(mask=mask, symbol=symbol, ds=ds)

        yield button.create_button()

    button = Button(mask=[True] * n_tickers, ds=ds, default_button=True)
    yield button.create_button()


def create_update_menu(grouped, ds):
    """Creates a list with the params. to configurate the updatemenu function of the plot.

    Parameters
    ----------
    grouped: pandas.core.groupby.generic.DataFrameGroupBy
        a stocks DataFramegrouped by "symbol"
    ds: str
        date of the report that will be used in the title.
    Returns
    -------
    updatemenus: list
        list of params. to configurate the updatemenus function of the plot.
    """
    buttons = list(create_buttons(grouped, ds))
    updatemenus = list([dict(active=len(grouped), showactive=False, buttons=buttons)])
    return updatemenus


def create_layout_fig(updatemenus, ds):
    """Creates the plotly figure layout.

    Parameters
    ----------
    updatemenus: list
        list of params. to configurate the updatemenus function of the plot.
    ds: str
        date of the report that will be used in the title.
    Returns
    -------
    plotly.graph_objects.Figure
        a plotly figure with the created layout.
    """
    layout = go.Layout(
        height=800,
        width=1000,
        title=f"Stocks quotation time series - Daily report {ds}",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Price"),
        updatemenus=updatemenus,
    )
    return go.Figure(layout=layout)


def add_traces(fig, grouped):
    """Adds traces to the plot figure.

    Parameters
    ----------
    fig: plotly.graph_objects.Figure
        a figure with a created layout where to add the traces
    grouped: pandas.core.groupby.generic.DataFrameGroupBy
        a stocks DataFramegrouped by "symbol". Each symbol will be represented in one trace and added to the figure.
    """
    for ticker in grouped.groups.keys():
        ticker_data = grouped.get_group(ticker)
        date = ticker_data.date
        price_series = ticker_data.close

        fig.add_traces(go.Scatter(x=date, y=price_series, name=ticker))


def create_plot(df, ds):
    """Creates a plot from a DF with stocks data.

    Parameters
    ----------
    df: pd.DataFrame
        a DataFrame with stocks data to plot.
    ds: str
        date of the report that will be used in the title.
    Returns
    -------
    fig: plotly.graph_objects.Figure
        a plot (figure) drawn from the data of the stocks DataFrame.
    """
    grouped = df.groupby("symbol")

    update_menus = create_update_menu(grouped, ds)
    fig = create_layout_fig(update_menus, ds)
    add_traces(fig, grouped)
    return fig


def save_plot(plot, PATH):
    """Takes a plotly figure and saves it.

    Parameters
    ----------
    plot: plotly.graph_objects.Figure
        the figure to save
    PATH: str
        absolute path to the directory where to save the figure.
    """
    fn = os.path.join(PATH, "stocks_daily_report.html")
    po.plot(plot, filename=fn, auto_open=False)
    print("Plot saved with success")


def plot(DB_KWARGS: dict, PATH: str, ds: str) -> None:
    """Wrapper to query a DB, create and save a plotly figure.

    Parameters
    ----------
    DB_KWARGS: dict
        dict with params. to create a DBClient.
    PATH: str
        absolute path to the directory where to save the figure.
    ds: str
        date of the report that will be used in the title.
    """
    db_client = dbclient.DBClient(**DB_KWARGS)
    df = query_db.query_db(db_client, ds)

    plot = create_plot(df, ds)

    save_plot(plot, PATH)
