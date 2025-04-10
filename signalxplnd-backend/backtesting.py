import yfinance as yf
from datetime import datetime, timedelta,date
import pandas as pd
import warnings
import time
from utils.build_results import increment_results
from utils.data_transfer import read_from_s3,write_to_s3

# from aggregate_data import rank_data

def lambda_handler(event, context):


    print(f"Backtesting Starting at {datetime.now()}")

    warnings.filterwarnings("ignore")


    # Get the current date
    current_date = date.today()

    # Input data for multiple stocks
    # stocks_data = pd.read_csv('total_results.csv')  
    #  stocks_data = pd.read_csv('predictions/non_trigger_stocks.csv')
    stocks_data=read_from_s3('non_trigger_stocks.csv')

    # Fetch data for all tickers in one batch within the range of the dataset
    def fetch_historical_data(stocks_data):
        print('beginning fetch_historical_data function')
        tickers = stocks_data['ticker'].unique()
        
        print('retrieved unique tickers from stocks_data')
        
        
        start_date = (datetime.strptime(min(stocks_data['last_date']).strip()[:10], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        print(start_date)

        end_date = (datetime.strptime(max(stocks_data['last_date']).strip()[:10], "%Y-%m-%d")).strftime("%Y-%m-%d")
        print(end_date )
        
        print("Fetching historical data for all tickers...")
        all_data=[]
        for ticker in tickers:
            data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', progress=False,multi_level_index=False)
            data['ticker']=ticker
            all_data.append(data)
            # print(all_data)
            
        return pd.concat(all_data)

    # Function to determine which trigger got hit first
    def check_first_trigger(historical_data, ticker, buy_price, overall_success_rate, predicted_higher_success_rate, last_date, adj_prediction_price, adj_price_higher, stop_loss, latest_close):
        if historical_data.empty:
            return {"ticker": ticker, "status": "No data available"}
        
        # Calculate stop_loss threshold
        stop_loss_price = latest_close + (latest_close * stop_loss)
        
        pd.to_datetime(historical_data.reset_index()['Date'],format='%Y-%m-%d').dt.date
        
        h_data=historical_data.reset_index()
        # print(h_data.columns.droplevel(1))
        
    
        adj_price_dates = h_data[((h_data['High'] > adj_prediction_price) & (datetime.strptime(last_date.strip()[:10],'%Y-%m-%d').date() < h_data['Date'].dt.date)) ]
        # print(adj_price_dates)
        stop_loss_dates = h_data[((h_data['Low'] < stop_loss_price) & (datetime.strptime(last_date.strip()[:10],'%Y-%m-%d').date()< h_data['Date'].dt.date))]
        # print(stop_loss_dates)

        # Determine first occurrence
        first_trigger = None
        first_trigger_date = None
        first_trigger_price = None
        
        # if high price is reached, do assignments to predicted price
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
            
            print(f"{(ticker)} from {(last_date)} has a {first_trigger} trigger price as of {first_trigger_date} for a {profit} profit")
            
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
        else:
            print(f"{(ticker)} from {(last_date)} has no trigger price as of {current_date}")
            
            return None
            
            
            
        return None

    # Process all stocks
    def process_stocks(stocks_data, historical_data):
        results = []
        
        non_triggers=[]
        
        # completed_dates=[]
        for _, stock in stocks_data.iterrows():
            
            ticker=stock['ticker']
            # print(ticker)
            
            # if ticker in 'MA':
            
            ticker_data = historical_data.loc[historical_data['ticker']==ticker]
            
            # print(ticker_data)

            if ticker_data is not None:
                
                ticker_date=stock['last_date']
                
                result = check_first_trigger(historical_data=ticker_data,
                    ticker=ticker,
                    buy_price=stock['buy_price'],
                    overall_success_rate=stock['overall_success_rate'],
                    predicted_higher_success_rate=stock['predicted_higher_success_rate'],
                    last_date=ticker_date,
                    adj_prediction_price=stock['adj_prediction_price'], 
                    adj_price_higher=stock['adj_price_higher'],
                    stop_loss=stock['stop_loss'],
                    latest_close=stock['latest_close']
                )
                
                if result :
                    # if ticker_date not in completed_dates:
                    # print(ticker_date)   
                    results.append(result)
                        # completed_dates.append(ticker_date)
                else:
                    non_tagged_results={}
                    
                    non_tagged_results["ticker"]= ticker
                    non_tagged_results["buy_price"]=stock['buy_price']
                    non_tagged_results["overall_success_rate"]=stock['overall_success_rate']
                    non_tagged_results["predicted_higher_success_rate"]=stock['predicted_higher_success_rate']
                    non_tagged_results["last_date"]=ticker_date
                    non_tagged_results["adj_prediction_price"]=stock['adj_prediction_price']
                    non_tagged_results["adj_price_higher"]=stock['adj_price_higher']
                    non_tagged_results["stop_loss"]=stock['stop_loss']
                    non_tagged_results["latest_close"]=stock['latest_close']
            
                    non_triggers.append(non_tagged_results)
                    
            time.sleep(1)  # Optional: Add delay to prevent rapid processing

        return results,non_triggers

    # Main execution
    # if __name__ == "__main__":
    try:
        historical_data = fetch_historical_data(stocks_data)
        print('Historical Data returned')
    except Exception as e:
        print(e)
        
    try:
        processed_results,non_triggers = process_stocks(stocks_data, historical_data)
        print('Processed results and non_triggers returned')
    except Exception as e:
        print(e)
    # print(processed_results)
    results_df = pd.DataFrame(processed_results)
    increment_results(read_from_s3('backtest_results.csv'),processed_results)
    # print(results_df)
    # results_df.to_csv('summary_results.csv', index=False)
    
    
    # the below should get me a csv file of the trickers and dates that I'd need to check on the next run
    # will need to add a clause that ignores ticker from X period in the past
    non_triggers_df=pd.DataFrame(non_triggers)
    # non_triggers_df.to_csv('predictions/non_trigger_stocks.csv') 
    try:
        write_to_s3(non_triggers_df,'non_trigger_stocks.csv')
    except:
        print('error writing non_trigger_stocks.csv to s3 in backtesting.py')
    
    print(f"Backtesting Ending at {datetime.now()}")

        
        
