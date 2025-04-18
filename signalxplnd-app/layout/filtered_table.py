from dash import html,dcc
import dash_bootstrap_components as dbc

def create_filtered_table(df):
    return dbc.Container(
        [
            html.H2("Backtesting Results by Ticker"),
            html.P("View results of previous predictions for any ticker in our database"),
            dcc.Dropdown(
                id="ticker-filter",
                options=[{"label": ticker, "value": ticker} for ticker in df["ticker"].unique()],
                # value=df["ticker"].unique()[0],
                value=" ",
                clearable=True,
                className="mb-3",
            ),
            html.Div(
                id="table-container"
            ),
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )
