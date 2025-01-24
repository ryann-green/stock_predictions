from dash import Input, Output, dcc
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from data_loader import load_data  # Import here once

# Load the data globally
# br_df = backtesting results
# p_df = prediction results
br_df, p_df = load_data()

def register_callbacks(app):
    @app.callback(
        Output("table-container", "children"),  # Use "children" for DataTable
        [Input("ticker-filter", "value")]
    )
    def update_table(selected_ticker):
        # Filter the globally loaded data
        filtered_df = br_df[br_df["ticker"] == selected_ticker]
        
        # Return a DataTable instead of raw data
        return DataTable(
            id="data-table",
            columns=[
                {"name": col, "id": col, "hideable": True} for col in filtered_df.columns
            ],
            data=filtered_df.to_dict("records"),
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_size=10,  # Show 10 rows per page
            style_table={
                "overflowX": "auto",
                "maxHeight": "400px",
                "overflowY": "auto",
            },
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
            },
        )
    
    @app.callback(
        Output("scatter-container", "children"),  # Use "children" for dcc.Graph
        [Input("date-filter", "value")]
    )
    def update_scatter(selected_date):
        import plotly.express as px

        # Filter the globally loaded data
        filtered_df = p_df[p_df["last_date_for_prediction"] == selected_date]
        
        # Generate the scatter plot
        fig = px.scatter(
            data_frame=filtered_df,
            x="predicted_higher_success_rate",
            y="overall_success_rate",
            color="adj_prediction_higher",
            hover_name="ticker",
            title=f"Predicted Higher Success vs Overall Success for {selected_date}",
        )

        fig.update_layout(transition_duration=500)
        
        # Return a Graph component
        return dcc.Graph(figure=fig)
