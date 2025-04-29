# general libraries
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# libs imported using requirements.tx
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import numpy as np
import pandas as pd

# custom libraries
from utils.model_training import get_missing_dates, get_initial_df, shift_ahead, generate_lead_features, prep_train_test_data, evaluate_models
from utils.build_results import increment_predictions, increment_non_trigger_evals
from utils.data_transfer import read_from_s3,write_to_s3
 
# Steps to operationalize
# Identify the ideal buying price that is just not the last closing wprice to optimize profit

# 1. Move to working on evaluation automation
# 2. Have the check_price process run to evaluate the results of these predictions for dates where the end date of the prediction is less than today and is greater than the last day in the Summary results

# -------------------------------
# Later
# If stock ticker is added, then collect the data from 365 days ago and add
# Only keep the last 365 days of data for all stocks
# Create a different script to purge the dates that fall out of this evaluation window time
# Include other models to train and test data
# Add additional lead features to evaluate effectivness
# Automate to run daily in the morning z



# dates=pd.read_csv('./working_weekdays_2024.csv')
def lambda_handler(event, context):
    missing_dates=get_missing_dates()
    # missing_dates=['2025-02-17']

    # print(missing_dates)

    total_results=[]

    for date in missing_dates:
        
        # Get the current date in YYYY-MM-DD format
        current_date = datetime.strptime(date,'%Y-%m-%d').date()
        # current_date = date[1]['date']
        # year = date[1]['year']
        # month = date[1]['month'] 
        # day = date[1]['day']
        # print(current_date)


        # Define the path to the new folder within the home directory
        # home_directory = os.path.expanduser('~/Code/stock_predictions/10_day_ahead_close/stock_performance')
        # new_folder_path = os.path.join(home_directory, str(current_date))
        s3_folder='10_day_ahead_close/stock_performance'

        # Create the folder if it doesn't already exist
        # if not os.path.exists(new_folder_path):
        #     os.makedirs(new_folder_path)
        #     print(f"Folder created: {new_folder_path}")
        # else:
        #     print(f"Folder already exists: {new_folder_path}")


        # Fetching historical data for GOOG
        tickers = ['AAPL'
                ,'GOOG'
                ,'SAN'
                # ,'BGC'
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
                ,'AZ'
                ,'ADPT'
                ,'AEVA'
                ,'ASPI'
                ,'AVAH'
                ,'ASM'
                ,'CMRX'
                ,'CURI'
                ,'QBTS'
                ,'XGN'
                ,'MBOT'
                ,'NAK'
                ,'TOI'
                ,'WOOF'
                ]
        end_date = current_date
        # end_date = datetime(year, month, day)
        start_date = (current_date - timedelta(days=125 * 1)).strftime('%Y-%m-%d')
        days_ahead=10

        prediction_results=[] 
        detailed_results=[]

        completed=[]
            
        for ticker in tickers:
            try: 
                if ticker not in completed:
                    completed.append(ticker)
                
                    print(ticker)
                    
                    data= shift_ahead (
                            get_initial_df(ticker,start_date,end_date)
                            ,days_ahead
                            )
                    

                    lead_features_df=pd.concat(generate_lead_features(data,days_ahead), axis=1)
                    # print(lead_features_df)

                    # print(lead_features_df)
                    # print(pd.concat([data, lead_features_df]))
                    # print(data.columns)
                    # print(lead_features_df.columns)

                    data = pd.concat([data, lead_features_df], axis=1)
                    
                    # print('hi')


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
                    print(feature_cols)
                    
                    
                    # get the main columns for the current day that aren't shifted. These need to be included to gauge the latest days information to include in the model
                    # main_cols=['Open','High','Low','Close','Adj Close','Volume','ALMA','Stochastic_RSI','Williams_%R','ROC']
                    main_cols=['Open','High','Low','Close','Volume','ALMA','Williams_%R','ROC']
                    for col in main_cols:
                        feature_cols.append(col)
                        

                        
                    X_train_selected_df,X_test_selected_df,y_train,y_test,selected_feature_names =prep_train_test_data(data,feature_cols,target_col)

                    # # # List of models to train
                    models = {
                        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
                        'LinearRegression': LinearRegression(),
                        'XGBoost': XGBRegressor(objective='reg:squarederror', random_state=42),
                        'GradientBoosting': GradientBoostingRegressor(random_state=42)
                    }
                    
                    # # # Evaluate the model's predicted values vs the actual values for past predictions
                    predictions_df = data.copy()
                    # print(predictions_df)
                    results,predictions_df=evaluate_models(models.items()
                                                        ,days_ahead
                                                        ,X_train_selected_df
                                                        ,X_test_selected_df
                                                        ,y_train
                                                        ,y_test
                                                        ,predictions_df)
                        
                    # # Select the best model
                    best_model_name = min(results, key=results.get)
                    best_model = models[best_model_name]

                    # print(f'\nBest model: {best_model_name} with RMSE: {results[best_model_name]}')
                    
                    evaluation_df=predictions_df[['Close',target_col, f'{best_model_name}_Predicted_Close_{days_ahead}d_ahead']]
                    # print(evaluation_df)
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
                    print(total_predictions)
                    total_correct_predictions = evaluation_df['Prediction_Correct'].sum()
                    predicted_higher_correct = evaluation_df[evaluation_df['Predicted_Higher'] & evaluation_df['Prediction_Correct']].shape[0]
                    total_predicted_higher = evaluation_df['Predicted_Higher'].sum()
                    average_act_vs_pred_diff=evaluation_df['Actual_vs_Predicted_Diff %'].mean()
                    median_act_vs_pred_diff=evaluation_df['Actual_vs_Predicted_Diff %'].median()

                    # Calculating success rates
                    overall_success_rate = total_correct_predictions / total_predictions
                    print(predicted_higher_correct)
                    predicted_higher_success_rate = predicted_higher_correct / total_predicted_higher if total_predicted_higher != 0 else 0
                    print(predicted_higher_success_rate)
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
                    # if ticker =='XLU':
                    #     print(latest_features)
                    predicted_price_10_days_ahead = best_model.predict(latest_features)[0]

                    # Step 3: Output the prediction
                    pred_results['last_date_for_prediction']=last_row.index[0]
                    pred_results['prediction_price']=predicted_price_10_days_ahead
                    
                    adj_prediction_price=predicted_price_10_days_ahead*(1+(average_act_vs_pred_diff+median_act_vs_pred_diff)/2)
                    pred_results['adj_prediction_price']=adj_prediction_price
                    # pred_results['adj_prediction_higher']=adj_prediction_price>last_row['Close'][0]
                    pred_results['stop_loss']=full['stop_loss'].min()
                    # print(f"Adj Price {adj_prediction_price}")
                    # print(f"Adj Price w/high {adj_prediction_price*(1+ data['close_high_avg'].max())}")
                    pred_results['adj_prediction_price_w_high_inc']=adj_prediction_price*(1+ data['close_high_avg'].max())
                    pred_results['adj_prediction_higher']=adj_prediction_price*(1+ data['close_high_avg'].max())>last_row['Close'][0]

                    
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
                    
                    # new_folder_path = os.path.join(home_directory,str(current_date) ,'tickers')

                    # # Create the folder if it doesn't already exist
                    # if not os.path.exists(new_folder_path):
                    #     os.makedirs(new_folder_path)
                    #     print(f"Folder created: {new_folder_path}")
                    # else:
                    #     pass
                    #     # print(f"Folder already exists: {new_folder_path}")

                    # Saving the dataframe for future reference
                    # evaluation_df.to_csv(f'{new_folder_path}/{ticker}_model_performance_analysis.csv')
                    # full.reset_index()[['Date','Open','High','Low','Close','Volume','stop_loss']].to_csv(f'{new_folder_path}/{ticker}_data.csv')
                    write_to_s3(evaluation_df,f'{s3_folder}/{current_date}/{ticker}_model_performance_analysis.csv')
                    detailed_results.append(evaluation_df)
                    
                    # print(full.iloc[-1:])
            except:
                print('No Data')
        # print(pd.DataFrame(prediction_results))
        all_results=pd.DataFrame(prediction_results).sort_values('predicted_higher_success_rate', ascending=False)
        # all_results.to_csv(f'{new_folder_path}/all_results.csv')
        write_to_s3(all_results,f'{s3_folder}/{date}/all_results.csv')               
        # all_results.to_csv('~/Code/stock_predictions/dash/latest_results.csv')
        # pd.concat(detailed_results).to_csv(f'{new_folder_path}/detailed_results.csv')
        write_to_s3(pd.concat(detailed_results),f'{s3_folder}/{date}/detailed_results.csv')
        
        # print(new_folder_path)
        
        # total_results.append(all_results)
        
        increment_predictions(all_results,read_from_s3('predictions_table.csv'))
    
        increment_non_trigger_evals(all_results,read_from_s3('non_trigger_stocks.csv'))
        
        # At this point we will run backtesting.py
    
        
    # pd.concat(total_results).to_csv(f'{new_folder_path}/total_results.csv')
    return "success","run backtesting"