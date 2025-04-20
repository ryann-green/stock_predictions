from dash import html,dcc
import dash_bootstrap_components as dbc

def create_weighting_controls():
    return dbc.Container(
        [
            html.H2("Adjust Weights"),
            html.P("Use the dropdowns below to adjust the weights for the ranking calculation."),
            
            # Alert (Initially Hidden)
            dbc.Alert(
                "Error: The total weight must sum to 100%. Please adjust the values.",
                id="weight-alert",
                color="danger",
                dismissable=True,
                is_open=False,
            ),

            dbc.Row(
                [dbc.Col(
                        [
                            html.Label("Success Ratio Rank"),
                            dcc.Dropdown(
                                id="weight-success-ratio",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=50,
                                clearable=False
                            ),
                        ],
                        width=4
                    ),
                 dbc.Col(
                        [
                            html.Label("Non-Trigger Rank"),
                            dcc.Dropdown(
                                id="weight-non-trigger",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=35,
                                clearable=False
                            ),
                        ],
                        width=4),
                    dbc.Col(
                        [
                            html.Label("14-Day Median Profit Rank"),
                            dcc.Dropdown(
                                id="weight-median-profit",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=5,
                                clearable=False
                            ),
                        ],
                        width=4
                    ),
                    
                    
                ],
                className="mb-3"
            ),

            dbc.Row(
                [dbc.Col(
                        [
                            html.Label("Spread Rank"),
                            dcc.Dropdown(
                                id="weight-spread",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=5,
                                clearable=False
                            ),
                        ],
                        width=4
                    ),
                    
                    
                    dbc.Col(
                        [
                            html.Label("Predictions Rank"),
                            dcc.Dropdown(
                                id="weight-predictions",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=5,
                                clearable=False
                            ),
                        ],
                        width=4
                    ),
                ],
                className="mb-3"
            ),
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )