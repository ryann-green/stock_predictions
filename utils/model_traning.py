import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas_ta as ta
import yfinance as yf 
from datetime import datetime, timedelta
from utils.data_transfer import read_from_s3

def get_missing_dates():
    # use this to rebuild predictions when needed
    # last_data_date = datetime(2023, 12, 31).date()

    last_data_date= datetime.strptime(max(read_from_s3('predictions_table.csv')['last_date_for_prediction']),'%Y-%m-%d').date()
    current_date=datetime.now().date()
    # print(current_date-last_data_date)

    # Generate all dates between the last date and current date
    date_list = []
    while last_data_date < current_date:
        last_data_date += timedelta(days=1)
        date_list.append(last_data_date.strftime('%Y-%m-%d'))

    # Print the dates
    print("Dates between last date in file and current date:")
    for date in date_list:
        print(date)
        
    return (date_list)


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

def shift_ahead (data,days_ahead):
        
        for i in range(1, days_ahead):
            data[f'{i}_Day Close Change'] = (data['Close'] - data['Close'].shift(i))/data['Close'].shift(i)
            data[f'{i}_Day Volume Change'] = data['Volume'] - data['Volume'].shift(i)
            
        # Drop any rows with NaN values generated by indicator calculations
        data.dropna(inplace=True)
        
        return data
    
def generate_lead_features (data,days_ahead):
        
            # # Generate lead features for the past 30 days
        # Shift (i) positive means that the data from the previous "i" day prior to the current row will be reflected in the lead_i column 
        lead_features = []

        for i in range(1, days_ahead):
            
            # cols=['Close', 'ALMA', 'Stochastic_RSI', 'Williams_%R', 'ROC']
            cols=['Close', 'ALMA', 'Williams_%R', 'ROC']
            
            # add each day close and volume change as additional columns to evaluate for features
            for n in range(1, days_ahead):
                cols.append(f'{n}_Day Close Change')
                cols.append(f'{n}_Day Volume Change')
            
            leads = data[cols].shift(i)
            # print('before')
            # print(leads)

            leads.columns = [f'{col}_lead_{i}' for col in leads.columns]
            # print('after')
            # print(leads)
            lead_features.append(leads)
            # print(lead_features)
            return lead_features

def prep_train_test_data(data,feature_cols,target_col):
    
        # Split the data into training and testing sets
    # [print(col) for col in feature_cols if col not in data.columns  ]
    # print(feature_cols)
    # print(target_col)
    try:
        # print(feature_cols)
        # print(data.columns)
        train_test_split(data, data, test_size=0.2, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(data[feature_cols], data[target_col], test_size=0.2, random_state=42)

        # print(X_train, X_test, y_train, y_test)
    except:
        print('error')

    
    # # # Feature selection using SelectKBest
    k_best_features = SelectKBest(f_regression, k=10)
    

    X_train_selected = k_best_features.fit_transform(X_train, y_train)
    X_test_selected = k_best_features.transform(X_test)

    # # # Get the selected feature names
    selected_feature_names = [feature_cols[i] for i in k_best_features.get_support(indices=True)]
    # print(selected_feature_names)

    # # # Convert X_train_selected and X_test_selected back to DataFrames for easier manipulation
    X_train_selected_df = pd.DataFrame(X_train_selected, index=X_train.index, columns=selected_feature_names).sort_index(ascending=True)
    # # print(X_train_selected_df)
    X_test_selected_df = pd.DataFrame(X_test_selected, index=X_test.index, columns=selected_feature_names).sort_index(ascending=True)
    
    return X_train_selected_df,X_test_selected_df,y_train,y_test,selected_feature_names

def evaluate_models (model_items,days_ahead,X_train_selected_df,X_test_selected_df,y_train,y_test,predictions_df):
        # # # Train and evaluate each model
        results = {}
        
        for model_name, model in model_items:
        
            model.fit(X_train_selected_df, y_train)
            predictions = model.predict(X_test_selected_df)
            
        #     # Create a DataFrame for predictions with the same index as the training set
            predictions_train = pd.DataFrame(model.predict(X_train_selected_df), index=X_train_selected_df.index, columns=[f'{model_name}_Predicted_Close_{days_ahead}d_ahead'])
            # print(predictions_train)

        #     # Merge the predictions with the predictions_df DataFrame
            predictions_df = predictions_df.merge(predictions_train, left_index=True,right_index=True, how='left')
            
            mse = mean_squared_error(y_test, predictions)
            rmse = np.sqrt(mse)
            results[model_name] = rmse
            # print(f'{model_name} RMSE: {rmse}')
            
        return results, predictions_df
    


