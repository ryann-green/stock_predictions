from dash import Input, Output, dcc
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from data_loader import load_data  # Import here once

# Load the data globally
# br_df = backtesting results
# p_df = prediction results
br_df, p_df, recs_df = load_data()

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
    
    @app.callback(
        Output("ranked-container", "children"),
        [
            Input("weight-median-profit", "value"),
            Input("weight-success-ratio", "value"),
            Input("weight-spread", "value"),
            Input("weight-non-trigger", "value"),
            Input("weight-predictions", "value"),
        ],
    )
    def update_rankings(w_median, w_success, w_spread, w_non_trigger, w_predictions):
        # Normalize weights to sum to 1
        total_weight = w_median + w_success + w_spread + w_non_trigger + w_predictions
        normalized_weights = {
            "14_day_median_profit_rank": w_median / total_weight,
            "success_ratio_rank": w_success / total_weight,
            "spread_rank": w_spread / total_weight,
            "non_trigger_rank": w_non_trigger / total_weight,
            "predictions_rank": w_predictions / total_weight,
        }

        # Calculate weighted rankings
        recs_df["weighted_rank"] = (
            recs_df["14_day_median_profit_rank"] * normalized_weights["14_day_median_profit_rank"]
            + recs_df["success_ratio_rank"] * normalized_weights["success_ratio_rank"]
            + recs_df["spread_rank"] * normalized_weights["spread_rank"]
            + recs_df["non_trigger_rank"] * normalized_weights["non_trigger_rank"]
            + recs_df["predictions_rank"] * normalized_weights["predictions_rank"]
        )
        ranked_df = recs_df.sort_values(by="weighted_rank",ascending=False).reset_index(drop=True)

        # Return the updated table
        return DataTable(
            id="ranked-table",
            columns=[
                {"name": col, "id": col} for col in ranked_df.columns
            ],
            data=ranked_df.to_dict("records"),
            sort_action="native",
            page_action="native",
            page_size=10,
        )
