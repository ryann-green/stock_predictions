from dash import html, dcc
import dash_bootstrap_components as dbc
from data_loader import load_data

# Load data
df = load_data()

def create_layout():
    return dbc.Container(
        [
            create_data_summary(df),
            create_scatter_plot(df),
            create_filtered_table(df),
        ],
        fluid=True,
    )

def create_data_summary(df):
    return dbc.Container(
        [
            html.H2("Container 1: Data Summary"),
            html.P("This section provides a summary of the dataset."),
            html.Ul(
                [
                    html.Li(f"Number of records: {df.shape[0]}"),
                    html.Li(f"Number of columns: {df.shape[1]}"),
                    html.Li(f"Columns: {', '.join(df.columns)}"),
                ]
            ),
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )

def create_scatter_plot(df):
    return dbc.Container(
        [
            html.H2("Container 2: Scatter Plot"),
            html.Div(id="scatter-container")

        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )

def create_filtered_table(df):
    return dbc.Container(
        [
            html.H2("Container 3: Filtered Data Table"),
            dcc.Dropdown(
                id="ticker-filter",
                options=[{"label": ticker, "value": ticker} for ticker in df["ticker"].unique()],
                value=df["ticker"].unique()[0],
                clearable=True,
                className="mb-3",
            ),
            html.Div(id="table-container"),
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )
