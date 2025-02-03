from dash import html, dcc
import dash_bootstrap_components as dbc
from data_loader import load_data
from datetime import datetime,date
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output


# Load data
br_df,p_df,recs_df = load_data()
current_date = datetime.now().date()

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.NavbarBrand("SignalXplnd", className="text-white"),
                href="#",
                style={"textDecoration": "none"}
            ),
            dbc.Nav(
                dbc.NavItem(dbc.Button("Contact Us", href="mailto:data.xplnd@gmail.com", color="light")),
                className="ms-auto"
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4"
)


def create_layout():
    return dbc.Container(
        [   create_welcome_section(),
            # create_data_summary(br_df,p_df),
            dbc.Row(
                [
                    dbc.Col(create_weighting_controls(), width=12),
                 ]
            ),
            dbc.Row(
                [
                    dbc.Col(create_ranked_table(),width=7),
                     dbc.Col(create_scatter_plot(p_df), width=5),
                    
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(create_filtered_table(br_df), width=6),  # Container 3: Filtered Data Table
                    dbc.Col(
                    dbc.Container(
                        [
                            create_line_chart(),
                            create_column_chart(),
                           
                        ],
                        className="my-3 p-3 bg-light border rounded"
                    ),
                    width=6,  # Left side: Charts stacked
            ),
                     # Container 2: Scatter Plot
                    
                ]   
            ),
        ],
        fluid=True,
        className="p-2 mt-2 mb-2",  # Adds padding and margin
        style={"maxWidth": "1400px", "margin": "auto"}  # Centers content
    )

def create_welcome_section():
    return html.Div(
    [
        navbar,  # Navbar at the top

        # Welcome Message
        html.H2("Welcome to SignalXplnd – Your Data-Driven Edge in Stock Predictions", className="text-primary"),
        html.P(
            "Unlock the power of predictive analytics with SignalXplnd, a cutting-edge stock prediction platform "
            "designed to help you make informed investment decisions. Our ranking system is meticulously crafted to "
            "identify stocks with strong profit potential based on historical performance and predictive modeling."
        ),

        # Collapsible Section: How Our Ranking System Works
        dbc.Button("How Our Ranking System Works", id="ranking-button", color="primary", className="mt-3"),
        dbc.Collapse(
            html.Div(
                [
                    html.P("Each stock is ranked using a proprietary scoring model that blends multiple performance indicators:"),
                    html.Ul(
                        [
                            html.Li("14-Day Median Profit Percentage: Measures the median percentage return over the past 14 days based on backtesting results."),
                            html.Li("Target Price Success Ratio: Tracks how often the stock has historically reached its predicted target price."),
                            html.Li("14-30 Day Profit Spread: Evaluates the consistency of profit potential within a 14-30 day window."),
                            html.Li("Non-Trigger Rate: Assesses how frequently a stock remains untriggered, helping gauge reliability."),
                            html.Li("Latest Predicted Performance: Prioritizes stocks projected to move higher, factoring in short-term momentum."),
                        ],
                        className="mt-2"
                    ),
                ],
                className="mt-3"
            ),
            id="ranking-collapse",
            is_open=False
        ),

        # Collapsible Section: Key Features & What to Know Before You Start
        dbc.Button("Key Features & What to Know Before You Start", id="features-button", color="secondary", className="mt-3"),
        dbc.Collapse(
            html.Div(
                [
                    html.Ul(
                        [
                            html.Li("Reducing Room for Error: Ranked results only show current predictions where the price is expected to be higher in 10 days."),
                            html.Li("Backtested for Accuracy: Our models are rigorously tested against historical data to refine and improve predictions."),
                            html.Li("Dynamic & Adaptive: Rankings adjust in real-time as new market data emerges."),
                            html.Li("No Guarantees, Just Insights: While our analytics help identify strong opportunities, all investments carry risk. Use our rankings as a powerful tool, not a certainty."),
                            html.Li("Explore & Customize: Filter stocks based on criteria that matter most to you—whether it's consistency, volatility, or breakout potential."),
                        ],
                        className="mt-2"
                    ),
                ],
                className="mt-3"
            ),
            id="features-collapse",
            is_open=False
        ),

        html.P(
            "Whether you're a trader seeking short-term opportunities or a long-term investor looking for smart entry points, "
            "SignalXplnd empowers you with data-driven insights to navigate the markets confidently.",
            className="mt-4"
        ),

        html.Hr(),
        # html.P("🚀 Start exploring now and discover your next winning trade!", className="fw-bold text-center"),
    ],
    style={"padding": "20px"}
)
    
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
                [
                    dbc.Col(
                        [
                            html.Label("14-Day Median Profit Rank"),
                            dcc.Dropdown(
                                id="weight-median-profit",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=40,
                                clearable=False
                            ),
                        ],
                        width=4
                    ),
                    dbc.Col(
                        [
                            html.Label("Success Ratio Rank"),
                            dcc.Dropdown(
                                id="weight-success-ratio",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=25,
                                clearable=False
                            ),
                        ],
                        width=4
                    ),
                    dbc.Col(
                        [
                            html.Label("Spread Rank"),
                            dcc.Dropdown(
                                id="weight-spread",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=15,
                                clearable=False
                            ),
                        ],
                        width=4
                    ),
                ],
                className="mb-3"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Non-Trigger Rank"),
                            dcc.Dropdown(
                                id="weight-non-trigger",
                                options=[{"label": f"{i}%", "value": i} for i in range(0, 101, 5)],
                                value=10,
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
                                value=10,
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


def create_ranked_table():
    return dbc.Container(
        [
            html.H2(f"Ranked Results as of {current_date}"),
            html.P("Adjust the weight sliders above to customize the ranking calculations to your liking. A higher rank score indicates a stronger predicted outcome. Only results where the predicted higher price is expected to be higher than the latest close price are displayed."),
            html.Div(
                id="ranked-container"
            ),
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )

# Future Release
def create_scatter_plot(df):
    return dbc.Container(
        [
            html.H2("Scatter Plot of Latest Predictions"),
            html.P("Analyze the model's accuracy in predicting the correct direction of the ticker trend."),
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

def create_column_chart():
    return dbc.Container(
        [
            html.H2("Column Chart"),
            html.Div(id="column-container")
    
        ]
    )
    
# Function to create a line chart
def create_line_chart():
    return dbc.Container(
        [
            html.H2("Line Chart"),
            html.Div(id="line-container")
    
        ]
    )
   
    
    