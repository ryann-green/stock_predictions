from dash.dash_table import DataTable
from data.data_loader import recs_df  
from dash.dependencies import Input, Output



def register_ranking_callbacks(app):
    @app.callback(
        Output("ranked-container", "children"),
         Output("ticker-filter", "value"),
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
        recs_df["weighted_rank"] = round((
            recs_df["14_day_median_profit_rank"] * normalized_weights["14_day_median_profit_rank"]
            + recs_df["success_ratio_rank"] * normalized_weights["success_ratio_rank"]
            + recs_df["spread_rank"] * normalized_weights["spread_rank"]
            + recs_df["non_trigger_rank"] * normalized_weights["non_trigger_rank"]
            + recs_df["predictions_rank"] * normalized_weights["predictions_rank"]
        ))
        ranked_df = recs_df.sort_values(by="weighted_rank",ascending=False).reset_index(drop=True)

        formatted_ranked_df=ranked_df[['ticker'
                            , 'last_date_for_prediction'
                            ,'weighted_rank'
                            #   ,'14_day_median_profit_rank'
                            #   ,'success_ratio_rank'
                            #   ,'spread_rank'
                            #   ,'non_trigger_rank'
                            #   ,'predictions_rank'
                              ,'latest_close'
                              ,'stop_loss_amt'
                              ,'adj_prediction_price_w_high_inc']]
        formatted_ranked_df.iloc[:, -3:] = formatted_ranked_df.iloc[:, -3:].round(2)
        formatted_ranked_df.rename(columns={'ticker': 'Ticker'
                                            , 'last_date_for_prediction': 'Prediction Date'
                                            , 'weighted_rank': 'Rank'
                                            ,'latest_close': 'Close'
                                            , 'stop_loss_amt': 'Stop-Loss'
                                            , 'adj_prediction_price_w_high_inc': 'Prediction Price'}
                                   , inplace=True)
        
                
        first_ticker=formatted_ranked_df["Ticker"].unique()[0]
        
        # Return the updated table
        return DataTable(
            id="ranked-table",
            columns=[
                {"name": col, "id": col} for col in formatted_ranked_df.columns
            ],
            data=formatted_ranked_df.to_dict("records"),
            sort_action="native",
            page_action="native",
            page_size=15,
            style_table={
                "overflowX": "auto",
                "maxHeight": "500px",
                "overflowY": "auto",
            },
            style_cell={"textAlign": "center", "padding": "5px"},
            style_data={
            'color': 'black',
            'backgroundColor': 'white'
            },
            style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            }

        ), first_ticker
     
    @app.callback(
    Output("weight-alert", "is_open"),
    [
        Input("weight-median-profit", "value"),
        Input("weight-success-ratio", "value"),
        Input("weight-spread", "value"),
        Input("weight-non-trigger", "value"),
        Input("weight-predictions", "value"),
    ]
    )
    def validate_weights(median_profit, success_ratio, spread, non_trigger, predictions):
        total_weight = median_profit + success_ratio + spread + non_trigger + predictions
        return total_weight != 100  # Show alert if total is not 100