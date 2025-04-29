from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime
from pytz import timezone

tz = timezone('EST')
current_date = datetime.now(tz).date()

def create_ranked_table():
    return dbc.Container(
        [
            html.H2(f"Ranked Results as of {current_date}"),
            html.P("Adjust the sliders to customize your ranking preferences:"),
            html.Ul([
                html.Li("Adjust the weight sliders above to customize the ranking calculations to your liking."),
                html.Li("A higher success ratio indicates a stronger predicted outcome."),
                html.Li("Only results where the predicted higher price is expected to be greater than the latest close price are displayed."),
            ]),
            html.Div(id="ranked-container"),
        ],
        fluid=True,
        className="my-3 p-3 bg-light border rounded",
    )
