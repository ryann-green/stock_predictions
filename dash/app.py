import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Sample data for the plot 
# df = px.data.iris()
df = pd.read_csv('latest_results.csv')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout with three containers
app.layout = dbc.Container(
    [
        dbc.Container(
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
       ,
        
        dbc.Container(
            [
                html.H2("Container 2: Scatter Plot"),
                dcc.Graph(
                    figure=px.scatter(
                        df, x="predicted_higher_success_rate", y="overall_success_rate", color="predicted_higher_correct",hover_name='ticker',
                        title="Predicter Higher Success vs Overall Success"
                    )
                ),
            ],
            fluid=True,
            className="my-3 p-3 bg-light border rounded",
        ),
        
        dbc.Container(
            [
                html.H2("Container 3: Filtered Data Table"),
                dcc.Dropdown(
                    id="ticker-filter",
                    options=[{"label": ticker, "value": ticker} for ticker in df["ticker"].unique()],
                    value="setosa",
                    clearable=False,
                    className="mb-3",
                ),
                html.Div(id="table-container"),
            ],
            fluid=True,
            className="my-3 p-3 bg-light border rounded",
        ),
    ],
    fluid=True,
)

# Callback to update the table based on selected species
@app.callback(
    dash.Output("table-container", "children"),
    [dash.Input("ticker-filter", "value")]
)
def update_table(selected_ticker):
    filtered_df = df[df["ticker"] == selected_ticker]
    return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)

if __name__ == "__main__":
    app.run_server(debug=True)
