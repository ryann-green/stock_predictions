from dash import Input, Output, dcc
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from data_loader import load_data  
from dash.dependencies import Input, Output, State
import plotly.express as px


# Load the data globally
# br_df = backtesting results
# p_df = prediction results
br_df, p_df, recs_df = load_data()

def register_callbacks(app):
    
    
    @app.callback(
        Output("table-container", "children"),  # Use "children" for DataTable
        Output("column-container", "children"),
         Output("line-container", "children"),
        [Input("ticker-filter", "value")]
    )
    def update_table(selected_ticker):
        # Filter the globally loaded data
        filtered_df = br_df[br_df["ticker"] == selected_ticker].sort_values('pred_date',ascending=False)
        
        filtered_df.rename(columns={'ticker': 'Ticker'
                                            , 'pred_date': 'Prediction Date'
                                            , 'overall_success_rate': 'OSR'
                                            ,'predicted_higher_success_rate': 'PHSR'
                                            , 'predicted_price_higher': 'Predicted Higher?'
                                            , 'first_trigger': 'Trigger'
                                            ,'first_trigger_date': 'Trigger Date'
                                            , 'first_trigger_price': 'Trigger Price'
                                            , 'profit_per_stock': '$ Gain/Loss'
                                            , 'profit_pct_per_stock': '% Gain/Loss'}
                                   , inplace=True)
        
        pass_through_df=filtered_df[['Prediction Date'
                                     ,'OSR'
                                     ,'PHSR'
                                     ,'Predicted Higher?'
                                     ,'Trigger'
                                     ,'Trigger Date'
                                     ,'Trigger Price'
                                     ,'$ Gain/Loss'
                                     ,'% Gain/Loss']]
        
        pass_through_df.iloc[:, 1] = pass_through_df.iloc[:, 1].round(2)
        pass_through_df.iloc[:, 2] = pass_through_df.iloc[:, 2].round(2)
        pass_through_df.iloc[:, 6] = pass_through_df.iloc[:, 6].round(2)
        pass_through_df.iloc[:, 7] = pass_through_df.iloc[:, 7].round(2)
        pass_through_df.iloc[:, 8] = pass_through_df.iloc[:, 8].round(2)


        
        # sum_gain=pass_through_df.groupby('Trigger').sum('$ Gain/Loss')
        graph_df= filtered_df[filtered_df["Predicted Higher?"] == True]
        bar_df=graph_df.groupby('Trigger', as_index=False).sum('$ Gain/Loss')
        
        col = px.bar(
                bar_df,
                x="Trigger",
                y="$ Gain/Loss",
                color="Trigger",
                title=f"Amount Gained vs Lost by {selected_ticker}",
                # labels={"14_day_median_profit": "Median Profit (%)"},
            )
            
        col.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,  # Adjust height for stacking
        )
        
        line = px.line(
            graph_df,
            x="Prediction Date",
            y="% Gain/Loss",
            # color="Ticker",
            title=f"% Gain/Loss Over Time for {selected_ticker}",
            # labels={"rank_score": "Ranking Score", "last_date_for_prediction": "Date"},
        )

        line.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,  # Adjust height for stacking
        )
        
        # Return a DataTable instead of raw data
        return DataTable(
            id="data-table",
            columns=[
                {"name": col, "id": col, "hideable": True} for col in pass_through_df.columns
            ],
            data=pass_through_df.to_dict("records"),
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_size=10,  # Show 10 rows per page
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

        ), dcc.Graph(figure=col), dcc.Graph(figure=line)
    
    @app.callback(
        Output("scatter-container", "children"),  # Use "children" for dcc.Graph
        [Input("date-filter", "value")]
    )
    def update_scatter(selected_date):

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
         Output("ticker-filter", "value"),
        [
            Input("weight-median-profit", "value"),
            Input("weight-success-ratio", "value"),
            Input("weight-spread", "value"),
            Input("weight-non-trigger", "value"),
            Input("weight-predictions", "value"),
        ],
    )
    
    # def update_filter_ticker(ticker):
    #     @app.callback(
    #         Output("ticker-filter", "value"),  # Use "children" for DataTable
    #         [Input( ticker)])
        
    #     def return_ticker ():
    #         return ticker
    
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
        
        # def update_filter_ticker(ticker):
        #     @app.callback(
        #         Output("ticker-filter", "value"),  # Use "children" for DataTable
        #         [Input( ticker)])
            
        #     def return_ticker ():
                
        first_ticker=formatted_ranked_df["Ticker"].unique()[0]

                
        
        # update_filter_ticker(first_ticker)
        
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
        
    # Callbacks to toggle collapsible sections
    @app.callback(
        Output("ranking-collapse", "is_open"),
        Input("ranking-button", "n_clicks"),
        State("ranking-collapse", "is_open"),
        prevent_initial_call=True
    )
    def toggle_ranking(n_clicks, is_open):
        return not is_open  # Toggle between open and closed

    @app.callback(
        Output("features-collapse", "is_open"),
        Input("features-button", "n_clicks"),
        State("features-collapse", "is_open"),
        prevent_initial_call=True
    )
    def toggle_features(n_clicks, is_open):
        return not is_open  # Toggle between open and closed
    
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

        