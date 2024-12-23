import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import warnings
import time

warnings.filterwarnings("ignore")

# steps to operationalize
# 1. For stocks that don't meet the high or low triggers, add them to a separate csv with ticker and prediction date for future analysis
# 2. Check to see the latest date for prediction date for each stock in the Summary results csv file. Find the results in the total_results csv that are greater than the ticker+pred_date from the summary file, and use those values to start this price evaluation script.
# 3. Create different segments in sheets to evaluate success of stocks
# 4. Identify top stock to trade on a day of the week based on best chance of profitability within 15 days
    #segment by best combination of
    # day of week success
    # overall success rate
    # predicted higher success rate
    # predicted higher boolean flag .. validation whether or not my prediction prices actually give me the best chance of success based on subsequent high and low prices    
# 5. Based on suggestion above, Figure out stock to trade on next possible trading day based on the latest daste in the "total results" csv file.


# Input data for multiple stocks
# stocks_data = pd.read_csv('total_results.csv')  
stocks_data = pd.read_csv('predictions_table.csv')

 
# Function to determine which trigger got hit first
def check_first_trigger(historical_data, ticker, buy_price, overall_success_rate, predicted_higher_success_rate, last_date, adj_prediction_price, adj_price_higher, stop_loss, latest_close):
    if historical_data.empty:
        return {"ticker": ticker, "status": "No data available"}
    
    # Calculate stop_loss threshold
    stop_loss_price = latest_close + (latest_close * stop_loss)
    
    pd.to_datetime(historical_data.reset_index()['Date'],format='%Y-%m-%d').dt.date
    
    h_data=historical_data.reset_index()
    
    # Find dates for triggers
    # print(ticker)
    # print(last_date)
    # print(buy_price)
    # print(adj_prediction_price)
    # print(stop_loss_price)
    # print(datetime.strptime(last_date,'%Y-%m-%d').date())
    # print(historical_data.reset_index()['Date'].dt.date)
    # print(h_data['Date'])
    # print(historical_data['High'] > adj_prediction_price)
    # print(datetime.strptime(last_date,'%Y-%m-%d').date() < h_data['Date'].dt.date)
    # adj_price_dates = historical_data[(historical_data['High'] > adj_prediction_price) & (datetime.strptime(last_date,'%Y-%m-%d').date() < h_data['Date'].dt.date)]
    adj_price_dates = h_data[((h_data['High'] > adj_prediction_price) & (datetime.strptime(last_date,'%Y-%m-%d').date() < h_data['Date'].dt.date)) ]
    # print(adj_price_dates)
    stop_loss_dates = h_data[((h_data['Low'] < stop_loss_price) & (datetime.strptime(last_date,'%Y-%m-%d').date()< h_data['Date'].dt.date))]
    # print(stop_loss_dates)

    # Determine first occurrence
    first_trigger = None
    first_trigger_date = None
    first_trigger_price = None
    
    # if high ptice is reached, do assignments to predicted price
    if not adj_price_dates.empty:
        first_adj_index = adj_price_dates.index[0]
        first_adj_date=adj_price_dates.loc[first_adj_index, 'Date']
        first_adj_price = adj_price_dates.loc[first_adj_index, 'High']
    else:
        first_adj_date, first_adj_price = None, None
    
    if not stop_loss_dates.empty:
        first_stop_index = stop_loss_dates.index[0]
        first_stop_date = stop_loss_dates.loc[first_stop_index, 'Date']
        first_stop_price = stop_loss_dates.loc[first_stop_index, 'Low']
    else:
        first_stop_date, first_stop_price = None, None
    
    # Compare dates
    if first_adj_date and (not first_stop_date or first_adj_date < first_stop_date):
        first_trigger = "target_price"
        first_trigger_date = first_adj_date
        first_trigger_price = adj_prediction_price
    elif first_stop_date:
        first_trigger = "stop_loss"
        first_trigger_date = first_stop_date
        first_trigger_price = stop_loss_price
        
    if first_trigger_price is not None:
        profit = first_trigger_price - buy_price
        profit_pct = profit / buy_price
        
        return {
            "ticker": ticker,
            "pred_date": last_date,
            "overall_success_rate": overall_success_rate,
            "predicted_higher_success_rate": predicted_higher_success_rate,
            "predicted_price_higher": adj_price_higher,
            "first_trigger": first_trigger,
            "first_trigger_date": first_trigger_date,
            "first_trigger_price": first_trigger_price,
            "profit_per_stock": profit,
            "profit_pct_per_stock": profit_pct
        }
    return None

# Fetch data for all tickers in one batch
def fetch_historical_data(stocks_data):
    tickers = stocks_data['ticker'].unique()
    start_date = (datetime.strptime(stocks_data['last_date_for_prediction'].min(), "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    print(start_date)

    end_date = (datetime.strptime(stocks_data['last_date_for_prediction'].max(), "%Y-%m-%d") + timedelta(days=15)).strftime("%Y-%m-%d")
    print(end_date )
    
    print("Fetching historical data for all tickers...")
    all_data=[]
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', progress=False)
        data['ticker']=ticker
        all_data.append(data)
        # print(all_data)
        
    return pd.concat(all_data)

# Process all stocks
def process_stocks(stocks_data, historical_data):
    results = []
    # completed_dates=[]
    for _, stock in stocks_data.iterrows():
        
        ticker=stock[2]
        
        ticker_data = historical_data.loc[historical_data['ticker']==ticker]
        
        # print(ticker_data)

        if ticker_data is not None:
            
            ticker_date=stock[11]
            
            result = check_first_trigger(historical_data=ticker_data,
                ticker=ticker,
                buy_price=stock[10],
                overall_success_rate=stock[5],
                predicted_higher_success_rate=stock[8],
                last_date=ticker_date,
                adj_prediction_price=stock[16], 
                adj_price_higher=stock[14],
                stop_loss=stock[15],
                latest_close=stock[10]
            )
            
            if result :
                # if ticker_date not in completed_dates:
                # +rint(ticker_date)
                results.append(result)
                    # completed_dates.append(ticker_date)
        time.sleep(1)  # Optional: Add delay to prevent rapid processing
        # print(results)
    return results

# Main execution
if __name__ == "__main__":
    historical_data = fetch_historical_data(stocks_data)
    processed_results = process_stocks(stocks_data, historical_data)
    # print(processed_results)
    results_df = pd.DataFrame(processed_results)
    results_df.to_csv('summary_results.csv', index=False)
    # print(results_df)
