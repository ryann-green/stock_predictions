from dash import html, dcc
import dash_bootstrap_components as dbc
from data_loader import load_data

# Load data
br_df,p_df = load_data()

def create_layout():
    return dbc.Container(
        [
            create_data_summary(br_df,p_df),
            dbc.Row(
                [
                    dbc.Col(create_filtered_table(br_df), width=6),  # Container 3: Filtered Data Table
                    dbc.Col(create_scatter_plot(p_df), width=6),  # Container 2: Scatter Plot
                    
                ]
            ),
        ],
        fluid=True,
    )

def create_data_summary(br_df,p_df):
    return dbc.Container(
        [
            html.H2("Container 1: Data Summary"),
            html.P("This section provides a summary of the backtest results dataset."),
            html.Ul(
                [
                    html.Li(f"Number of records: {br_df.shape[0]}"),
                    html.Li(f"Number of columns: {br_df.shape[1]}"),
                    html.Li(f"Columns: {', '.join(br_df.columns)}"),
                ]
            ),
            html.Br(),
            
            html.P("This section provides a summary of the predictions results dataset."),
            html.Ul(
                [
                    html.Li(f"Number of records: {p_df.shape[0]}"),
                    html.Li(f"Number of columns: {p_df.shape[1]}"),
                    html.Li(f"Columns: {', '.join(p_df.columns)}"),
                ]
            ),
            
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )

def create_scatter_plot(df):
    return dbc.Container(
        [
            html.H2("Container 3: Scatter Plot"),
            dcc.Dropdown(
                id="date-filter",
                options=[{"label": date, "value": date} for date in df["last_date_for_prediction"].unique()],
                value=max(df["last_date_for_prediction"].unique()),
                clearable=True,
                className="mb-3",
            ),
            html.Div(id="scatter-container")

        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )

def create_filtered_table(df):
    return dbc.Container(
        [
            html.H2("Container 2: Filtered Data Table"),
            dcc.Dropdown(
                id="ticker-filter",
                options=[{"label": ticker, "value": ticker} for ticker in df["ticker"].unique()],
                value=df["ticker"].unique()[0],
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

