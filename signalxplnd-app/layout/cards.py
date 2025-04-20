from dash import html
import dash_bootstrap_components as dbc

def create_cards():
    return dbc.Container(
        [
    dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Profit Ratio", className="card-title"),
                    
                    html.Div(
                        
                        className="card-text",
                        id="profit_ratio"                    ),
                    # dbc.Button("Click here", color="success", className="mt-auto"),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Success Ratio", className="card-title"),
                    html.Div(
                        className="card-text",
                        id="success_ratio"                    ),
                    # dbc.Button("Click here", color="warning", className="mt-auto"),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Estimated Trade Value", className="card-title"),
                    html.Div(
                        className="card-text",
                        id="etv"                    ),
                    # dbc.Button("Click here", color="danger", className="mt-auto"),
                ]
            )
        ),
    ]
),
    dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Median Trigger Time", className="card-title"),
                    html.Div(
                        className="card-text",
                        id="time_days"                    ),
                    # dbc.Button("Click here", color="success", className="mt-auto"),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("# of times Predicted Higher", className="card-title"),
                    html.Div(
                        className="card-text",
                        id="backtest_total"                    ),
                    # dbc.Button("Click here", color="warning", className="mt-auto"),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Predicted Higher Success", className="card-title"),
                    html.Div(
                        className="card-text",
                        id="backtest_correct" ),
                    # dbc.Button("Click here", color="danger", className="mt-auto"),
                ]
            )
        ),
    ]
)
    ],
        fluid=False,
        className="my-3 p-3 bg-light border rounded",
        )
