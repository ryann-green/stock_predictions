from dash import html,dcc
import dash_bootstrap_components as dbc

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
