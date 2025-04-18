from dash import html
import dash_bootstrap_components as dbc
from .navbar import navbar

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
    