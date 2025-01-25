from dash import html, dcc
import dash_bootstrap_components as dbc
from data_loader import load_data

# Load data
br_df,p_df,recs_df = load_data()

def create_layout():
    return dbc.Container(
        [
            create_data_summary(br_df,p_df),
            create_weighting_controls(),
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

def create_weighting_controls():
    return dbc.Container(
        [
            html.H2("Adjust Weights"),
            html.P("Use the sliders below to adjust the weights for the ranking calculation."),
            
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("14-Day Median Profit Rank (40%)"),
                            dcc.Slider(
                                id="weight-median-profit",
                                min=0,
                                max=100,
                                step=1,
                                value=40,  # Default weight
                                marks={i: f"{i}%" for i in range(0, 101, 10)},
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.Label("Success Ratio Rank (25%)"),
                            dcc.Slider(
                                id="weight-success-ratio",
                                min=0,
                                max=100,
                                step=1,
                                value=25,  # Default weight
                                marks={i: f"{i}%" for i in range(0, 101, 10)},
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Spread Rank (15%)"),
                            dcc.Slider(
                                id="weight-spread",
                                min=0,
                                max=100,
                                step=1,
                                value=15,  # Default weight
                                marks={i: f"{i}%" for i in range(0, 101, 10)},
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.Label("Non-Trigger Rank (10%)"),
                            dcc.Slider(
                                id="weight-non-trigger",
                                min=0,
                                max=100,
                                step=1,
                                value=10,  # Default weight
                                marks={i: f"{i}%" for i in range(0, 101, 10)},
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Predictions Rank (10%)"),
                            dcc.Slider(
                                id="weight-predictions",
                                min=0,
                                max=100,
                                step=1,
                                value=10,  # Default weight
                                marks={i: f"{i}%" for i in range(0, 101, 10)},
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                id="ranked-container"
            ),
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )

