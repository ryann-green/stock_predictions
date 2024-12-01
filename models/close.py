import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np
import os
from datetime import datetime

# Steps to operationalize
# Identify the ideal buying price that is just not the last closing price to optimize profit

# 1. Find the dates between the  max_date of total results csv and today
# 2. Those should be the dates read into the "dates" variable below to get the data caught up to curent date
# 3. append the results of this scrript to the latest tota results csv/file
# 4. Have the check_price process run to evaluate the results of these predictions for dates where the end date of the prediction is less than today and is greater than the last day in the Summary results

# -------------------------------
# Later
# If stock ticker is added, then collect the data from 365 days ago and add
# Only keep the last 365 days of data for all stocks
# Create a different script to purge the dates that fall out of this evaluation window time
# Include other models to train and test data
# Add additional lead features to evaluate effectivness
# Automate to run daily in the morning z



dates=pd.read_csv('./working_weekdays_2024.csv')

# print(dates)

total_results=[]
  
for date in dates.iterrows():
    

    # Get the current date in YYYY-MM-DD format
    # current_date = datetime.now().strftime('%Y-%m-%d')
    current_date = date[1]['date']
    year = date[1]['year']
    month = date[1]['month']
    day = date[1]['day']
    # print(current_date)


    # Define the path to the new folder within the home directory
    home_directory = os.path.expanduser('~/Code/stock_predictions/10_day_ahead_close/stock_performance')
    new_folder_path = os.path.join(home_directory, current_date)

    # Create the folder if it doesn't already exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")


    # Fetching historical data for GOOG
    tickers = ['AAPL'
            ,'GOOG'
            ,'DRI'
            ,'PAYX'
            ,'SBUX'
            ,'VAC'
            ,'KR'
            ,'CMI'
            ,'MA'
            ,'PG'
            ,'HPE'
            ,'CAT'
            ,'AMZN'
            ,'KO'
            ,'CSCO'
            ,'JCI'
            ,'BFIN'
            ,'XLK'
            ,'XLI'
            ,'XLY'
            ,'XLF'
            ,'XLRE'
            ,'XLU'
            ,'XLB'
            ,'XLP'
            ,'XLV'
            ,'XLE'
            ,'XLC'
            ,'NVDA'
            ,'EA'
            ,'ADBE'
            ,'AFG'
            ,'ARCC'
            ,'ADP'
            ,'AVNT'
            ,'AXS'
            ,'BAX'
            ,'CPB'
            ,'CNI'
            ,'KO'
            ,'CTBI'
            ,'EMR'
            ,'PRU'
            ,'QSR'
            ,'SUN'
            ,'TRN'
            ,'UNP'
            ,'WSO'
            ,'NSC'
            ,'SYY'
            ,'DDOG'
            ,'PLTR'
            ,'AMD'
            ]
    # tickers = ['AAPL','GOOG','DRI','PAYX','SBUX','VAC','KR','CMI']
    # end_date = datetime.now().strftime('%Y-%m-%d')
    end_date = datetime(year, month, day)
    # start_date = (datetime.now() - timedelta(days=125 * 1)).strftime('%Y-%m-%d')
    start_date = (end_date- timedelta(days=125 * 1)).strftime('%Y-%m-%d')
    days_ahead=10

    prediction_results=[]
    detailed_results=[]

    def get_initial_df (ticker):
        data = yf.download(ticker, start=start_date, end=end_date)
        # Calculate leading technical indicators
        data['ALMA'] = ta.alma(data['Close'])
        stoch_rsi = ta.stochrsi(data['Close'])
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
            
            cols=['Close', 'ALMA', 'Stochastic_RSI', 'Williams_%R', 'ROC']
            
            # add each day close and volume change as additional columns to evaluate for features
            for n in range(1, days_ahead):
                cols.append(f'{n}_Day Close Change')
                cols.append(f'{n}_Day Volume Change')
            
            leads = data[cols].shift(i)
            leads.columns = [f'{col}_lead_{i}' for col in leads.columns]
            lead_features.append(leads)
            
            return lead_features

    def prep_train_test_data(data,feature_cols,target_col):
            # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(data[feature_cols], data[target_col], test_size=0.2, random_state=42)

        # # # Feature selection using SelectKBest
        k_best_features = SelectKBest(f_regression, k=10)
        
    
        X_train_selected = k_best_features.fit_transform(X_train, y_train)
        X_test_selected = k_best_features.transform(X_test)

        # # # Get the selected feature names
        selected_feature_names = [feature_cols[i] for i in k_best_features.get_support(indices=True)]
        print(selected_feature_names)

        # # # Convert X_train_selected and X_test_selected back to DataFrames for easier manipulation
        X_train_selected_df = pd.DataFrame(X_train_selected, index=X_train.index, columns=selected_feature_names).sort_index(ascending=True)
        # print(X_train_selected_df)
        X_test_selected_df = pd.DataFrame(X_test_selected, index=X_test.index, columns=selected_feature_names).sort_index(ascending=True)
        
        return X_train_selected_df,X_test_selected_df,y_train,y_test,selected_feature_names

    def train_model (model_items,days_ahead,X_train_selected_df,X_test_selected_df,y_train,y_test,predictions_df):
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
            print(f'{model_name} RMSE: {rmse}')
            
        return results, predictions_df

    completed=[]
        
    for ticker in tickers:
        
        if ticker not in completed:
            completed.append(ticker)
        
            print(ticker)
            
            data= shift_ahead (
                    get_initial_df(ticker)
                    ,days_ahead
                    )

            lead_features_df=pd.concat(generate_lead_features(data,days_ahead), axis=1)

            # print(lead_features_df)
            data = pd.concat([data, lead_features_df], axis=1)
            
            data.dropna(inplace=True)
            
            # print(data)

            # Make a copy of the dataset before adding the column needed for a target for the closing price 30 days in the future for training the model
            train_data=data.iloc[:-1]
            full=data.copy()
            # print(train_data)

            # # Create target column by shifting the close price by -target days (closing price from target days in the future)
            data[f'Close_{days_ahead}d_ahead'] = data['Close'].shift(-days_ahead)

            # print(data)
            
            # this will get rid of the data form the last 30 trading days to train the model
            data.dropna(inplace=True)

            # identify target column
            target_col = f'Close_{days_ahead}d_ahead'
            
            # Define feature columns (past target days of technical indicators)
            feature_cols = lead_features_df.columns.tolist()
            
            # print(feature_cols)
            
            # get the main columns for the current day that aren't shifted. These need to be included to gauge the latest days information to include in the model
            main_cols=['Open','High','Low','Close','Adj Close','Volume','ALMA','Stochastic_RSI','Williams_%R','ROC']
            
            for col in main_cols:
                feature_cols.append(col)
            
            X_train_selected_df,X_test_selected_df,y_train,y_test,selected_feature_names =prep_train_test_data(data,feature_cols,target_col)

            # # # List of models to train
            models = {
                'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
                'LinearRegression': LinearRegression(),
                'XGBoost': XGBRegressor(objective='reg:squarederror', random_state=42)
            }
            
            # # # Evaluate the model's predicted values vs the actual values for past predictions
            predictions_df = data.copy()
            results,predictions_df=train_model(models.items(),days_ahead,X_train_selected_df,X_test_selected_df,y_train,y_test,predictions_df)
                
            # # Select the best model
            best_model_name = min(results, key=results.get)
            best_model = models[best_model_name]

            # print(f'\nBest model: {best_model_name} with RMSE: {results[best_model_name]}')
            
            evaluation_df=predictions_df[['Close',target_col, f'{best_model_name}_Predicted_Close_{days_ahead}d_ahead']]

            # # Drop rows with NaN values before calculating RMSE
            evaluation_df = evaluation_df.dropna()
            evaluation_df['Actual_vs_Predicted_Diff %'] = (evaluation_df[target_col] - evaluation_df[f'{best_model_name}_Predicted_Close_{days_ahead}d_ahead'])/evaluation_df[f'{best_model_name}_Predicted_Close_{days_ahead}d_ahead']
            evaluation_rmse = np.sqrt(mean_squared_error(evaluation_df[target_col], evaluation_df[f'{best_model_name}_Predicted_Close_{days_ahead}d_ahead']))
           

            # Adding columns to indicate if the predicted close is higher and if the actual future close is higher
            evaluation_df['Predicted_Higher'] = evaluation_df[f'{best_model_name}_Predicted_Close_{days_ahead}d_ahead'] > evaluation_df['Close']
            evaluation_df['Actual_Higher'] = evaluation_df[target_col] > evaluation_df['Close']

            # Adding column to indicate if the model's prediction was correct
            evaluation_df['Prediction_Correct'] = evaluation_df['Predicted_Higher'] == evaluation_df['Actual_Higher']
            
            evaluation_df['ticker']=ticker

            # print(evaluation_df)

            # Aggregating the data
            total_predictions = len(evaluation_df)
            total_correct_predictions = evaluation_df['Prediction_Correct'].sum()
            predicted_higher_correct = evaluation_df[evaluation_df['Predicted_Higher'] & evaluation_df['Prediction_Correct']].shape[0]
            total_predicted_higher = evaluation_df['Predicted_Higher'].sum()
            average_act_vs_pred_diff=evaluation_df['Actual_vs_Predicted_Diff %'].mean()
            median_act_vs_pred_diff=evaluation_df['Actual_vs_Predicted_Diff %'].median()

            # Calculating success rates
            overall_success_rate = total_correct_predictions / total_predictions
            predicted_higher_success_rate = predicted_higher_correct / total_predicted_higher if total_predicted_higher != 0 else 0

            pred_results={}
            pred_results['ticker']=ticker
            pred_results['total_predictions']=total_predictions
            pred_results['total_correct_predicions']=total_correct_predictions
            pred_results['overall_success_rate']=overall_success_rate
            pred_results['predicted_higher_correct']=predicted_higher_correct
            pred_results['total_predicted_higher']=total_predicted_higher
            pred_results['predicted_higher_success_rate']=predicted_higher_success_rate
            # pred_results['average_act_vs_pred_diff']=average_act_vs_pred_diff
            # pred_results['median_act_vs_pred_diff']=median_act_vs_pred_diff
            pred_results['adj_sell_vs_pred_pct']=(average_act_vs_pred_diff+median_act_vs_pred_diff)/2
            
            last_row = full.iloc[-1:]
            pred_results['latest_close']=last_row['Close'][0]

            # Extract the features used for model training from the last row
            # Ensure that `selected_feature_names` are the features selected during training
            latest_features = last_row[selected_feature_names].values.reshape(1, -1)

            # Step 2: Use the best model to predict the closing price 10 days in advance
            if ticker =='XLU':
                print(latest_features)
            predicted_price_10_days_ahead = best_model.predict(latest_features)[0]

            # Step 3: Output the prediction
            pred_results['last_date_for_prediction']=last_row.index[0]
            pred_results['prediction_price']=predicted_price_10_days_ahead
            
            adj_prediction_price=predicted_price_10_days_ahead*(1+(average_act_vs_pred_diff+median_act_vs_pred_diff)/2)
            pred_results['adj_prediction_price']=adj_prediction_price
            pred_results['adj_prediction_higher']=adj_prediction_price>last_row['Close'][0]
            pred_results['stop_loss ']=full['stop_loss'].min()
            # print(f"Adj Price {adj_prediction_price}")
            # print(f"Adj Price w/high {adj_prediction_price*(1+ data['close_high_avg'].max())}")
            pred_results['adj_prediction_price_w_high_inc']=adj_prediction_price*(1+ data['close_high_avg'].max())

            
            
            
            
            
            # Output the results
            # print(f"Total Predictions: {total_predictions}")
            # print(f"Total Correct Predictions: {total_correct_predictions}")
            # print(f"Overall Success Rate: {overall_success_rate:.2%}")
            # print(f"Predicted Higher Correct: {predicted_higher_correct}")
            # print(f"Total Predicted Higher: {total_predicted_higher}")
            # print(f"Predicted Higher Success Rate: {predicted_higher_success_rate:.2%}")
            # print(f"Predicted closing price 10 days ahead of {last_row.index[0]}: {predicted_price_10_days_ahead}")
            # print(f"Adjusted Predicted closing price 10 days ahead of {last_row.index[0]}: {adj_prediction_price}")
            
            
            
            prediction_results.append(pred_results)
            
            new_folder_path = os.path.join(home_directory,current_date ,'tickers')

            # Create the folder if it doesn't already exist
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                print(f"Folder created: {new_folder_path}")
            else:
                pass
                # print(f"Folder already exists: {new_folder_path}")

            # Saving the dataframe for future reference
            evaluation_df.to_csv(f'{new_folder_path}/{ticker}_model_performance_analysis.csv')
            full.reset_index()[['Date','Open','High','Low','Close','Adj Close','Volume','stop_loss']].to_csv(f'{new_folder_path}/{ticker}_data.csv')
            
            detailed_results.append(evaluation_df)
            
            print(full.iloc[-1:])

    all_results=pd.DataFrame(prediction_results).sort_values('predicted_higher_success_rate', ascending=False)
    all_results.to_csv(f'{new_folder_path}/all_results.csv')
    all_results.to_csv('~/Code/stock_predictions/dash/latest_results.csv')
    pd.concat(detailed_results).to_csv(f'{new_folder_path}/detailed_results.csv')
    
    total_results.append(all_results)
    
pd.concat(total_results).to_csv(f'{new_folder_path}/total_results.csv')

