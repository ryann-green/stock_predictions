from dash import html
import dash_bootstrap_components as dbc

def create_column_chart():
    return dbc.Container(
        [
            html.H2("Column Chart"),
            html.Div(id="column-container")
    
        ]
    )