from dash import html
import dash_bootstrap_components as dbc

# Function to create a line chart
def create_line_chart():
    return dbc.Container(
        [
            html.H2("Line Chart"),
            html.Div(id="line-container")
    
        ]
    )