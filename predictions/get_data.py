import pandas_ta as ta
import yfinance as yf
import pandas as pd

def get_initial_df (ticker,start_date,end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        # Calculate leading technical indicators
        data['ALMA'] = ta.alma(data['Close'])
        stoch_rsi = pd.series(ta.stochrsi(data['Close']))
        print('this is data close')
        print(data['Close'])
        print('this is stoch_rsi')
        print(stoch_rsi)
        data['Stochastic_RSI'] = stoch_rsi['STOCHRSIk_14_14_3_3']
        data['Williams_%R'] = ta.willr(data['High'], data['Low'], data['Close'])
        data['ROC'] = ta.roc(data['Close'])
        data['low_close_spread']= (data['Low']-data['Close'])/data['Low']
        data['close_high_spread']= (data['High']-data['Close'])/data['Close']
        
        data['stop_loss']=data['low_close_spread'].min()
        # print(f"Mean: {data['close_high_spread'].mean()}")
        # print(f"Median: {data['close_high_spread'].median()}")
        # print(f"Mean_Median Avg: {(data['close_high_spread'].mean()+data['close_high_spread'].median())/2}")
        data['close_high_avg']= (data['close_high_spread'].mean()+data['close_high_spread'].median())/2
        
        return data