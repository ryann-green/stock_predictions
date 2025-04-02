import pandas_ta as ta
import yfinance as yf
import pandas as pd

def get_initial_df (ticker,start_date,end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        # print(data)
        
        # Remove the second level of the MultiIndex (the ticker)
        data.columns = data.columns.droplevel(1)

        # Calculate leading technical indicators
        # print(data['Close'])
        data['ALMA'] = ta.alma(data['Close'].squeeze())

        # print('this is data close')
        # print(data['Close'])
        # print('this is stoch_rsi')
        # print(stoch_rsi)
        # data['Stochastic_RSI'] = stoch_rsi['STOCHRSIk_14_14_3_3']
        data['Williams_%R'] = ta.willr(data['High'].squeeze(), data['Low'].squeeze(), data['Close'].squeeze())
        data['ROC'] = ta.roc(data['Close'].squeeze())
        data['low_close_spread']= (data['Low']-data['Close'])/data['Low']
        data['close_high_spread']= (data['High']-data['Close'])/data['Close']
        
        data['stop_loss']=data['low_close_spread'].min()
        # print(f"Mean: {data['close_high_spread'].mean()}")
        # print(f"Median: {data['close_high_spread'].median()}")
        # print(f"Mean_Median Avg: {(data['close_high_spread'].mean()+data['close_high_spread'].median())/2}")
        data['close_high_avg']= (data['close_high_spread'].mean()+data['close_high_spread'].median())/2
        return data

# data=get_initial_df('aapl','2025-01-15','2025-03-07')
# print(data)