import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Input data for multiple stocks
stocks_data = pd.read_csv('total_results.csv')

# Function to determine which trigger got hit first
def check_first_trigger(ticker, buy_price,overall_success_rate,predicted_higher_success_rate,last_date, adj_prediction_price, adj_price_higher,stop_loss, latest_close):
    last_date_dt = datetime.strptime(last_date, "%Y-%m-%d")
    end_date_dt = last_date_dt + timedelta(days=15)  # Adding buffer for non-trading days
    start_date = (last_date_dt + timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = end_date_dt.strftime("%Y-%m-%d")
    
    # Fetch stock data from Yahoo Finance
    stock = yf.Ticker(ticker)
    historical_data = stock.history(start=start_date, end=end_date)
    
    if historical_data.empty:
        return {"ticker": ticker, "status": "No data available"}
    
    # Calculate stop_loss threshold
    stop_loss_price = latest_close + (latest_close * stop_loss)
    
    # Find dates for triggers
    adj_price_dates = historical_data[historical_data['High'] > adj_prediction_price]
    stop_loss_dates = historical_data[historical_data['Low'] < stop_loss_price]
    
    # Determine first occurrence
    first_trigger = None
    first_trigger_date = None
    first_trigger_price = None
    
    if not adj_price_dates.empty:
        first_adj_date = adj_price_dates.index[0]
        first_adj_price = adj_price_dates.loc[first_adj_date, 'High']
    else:
        first_adj_date, first_adj_price = None, None
    
    if not stop_loss_dates.empty:
        first_stop_date = stop_loss_dates.index[0]
        first_stop_price = stop_loss_dates.loc[first_stop_date, 'Low']
    else:
        first_stop_date, first_stop_price = None, None
    
    # Compare dates
    if first_adj_date and (not first_stop_date or first_adj_date < first_stop_date):
        first_trigger = "target_price"
        first_trigger_date = first_adj_date.strftime("%Y-%m-%d")
        first_trigger_price = first_adj_price
    elif first_stop_date:
        first_trigger = "stop_loss"
        first_trigger_date = first_stop_date.strftime("%Y-%m-%d")
        first_trigger_price = first_stop_price
        
    if first_trigger_price is not None:
        profit=first_trigger_price-buy_price
        profit_pct=profit/buy_price
        
        return {
        "ticker": ticker,
        "pred_date": last_date,
        "overall_success_rate":overall_success_rate,
        "predicted_higher_success_rate":predicted_higher_success_rate,
        "predicted_price_higher":adj_price_higher,
        "first_trigger": first_trigger,
        "first_trigger_date": first_trigger_date,
        "first_trigger_price": first_trigger_price,
        "profit_per_stock":profit,
        "profit_pct_per_stock":profit_pct
    }
    else:
        pass
    
    
  

# Process all stocks
results = []


for stocks in stocks_data.iterrows():
    
    stock=stocks[1]
    
    # print(stock[0])
    
    result = check_first_trigger(
        ticker=stock[1],
        overall_success_rate=stock[4],
        predicted_higher_success_rate=stock[7],
        buy_price=stock[9],
        last_date=stock[10],
        adj_prediction_price=stock[12],
        adj_price_higher=stock[13],
        stop_loss=stock[14],
        latest_close=stock[9],
    )
    
    if result:
        results.append(result)
    else:
        pass

# Display results
# for res in results:
#     print(res)

pd.DataFrame(results).to_csv('summary_results.csv')
    
print(pd.DataFrame(results))
