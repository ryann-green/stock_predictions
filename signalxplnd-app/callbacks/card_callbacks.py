from dash import Input, Output, html
from data.data_loader import   recs_df,success_ratio
from dash.dependencies import Input, Output, State

def register_card_callbacks(app):
    @app.callback(
        Output("profit_ratio", "children"),
        Output("success_ratio", "children"),
        # Output("etv", "children"),
        # Output("time_days", "children"),
        Output("backtest_total", "children"),
        Output("backtest_correct", "children"),
        [
            Input("ticker-filter", "value"),
        ],
    )
    
    def update_cards(ticker):
        
        current_ticker_df=recs_df.loc[recs_df['ticker']==ticker]
        
        # print(current_ticker_df)
        
        latest_close=current_ticker_df['latest_close']
        stop_loss_pct=current_ticker_df['stop_loss']
        stop_loss_price=latest_close*(1-stop_loss_pct)
        prediction_price=current_ticker_df['adj_prediction_price_w_high_inc']
        est_gain=(prediction_price-latest_close)/latest_close
        profit_ratio=round(abs(est_gain/stop_loss_pct),2)
        # print(profit_ratio)
        # print(profit_ratio.iloc[0] )
        
        current_ticker_success_df=success_ratio.loc[success_ratio['ticker']==ticker]
        succesful_triggers=current_ticker_success_df['trigger_count']
        all_true_higher_predictions=current_ticker_success_df['total_count']
        success_ra=round(current_ticker_success_df['success_ratio'],2)
        # print(success_ra.iloc[0] )
        
        expected_trade_value=success_ra.iloc[0] *profit_ratio.iloc[0]
        # print(expected_trade_value)


        
        # Return the updated table
        return html.H2(profit_ratio),html.H2(success_ra),html.H2(all_true_higher_predictions),html.H2(succesful_triggers)