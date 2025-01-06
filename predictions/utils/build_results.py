# When different models are created, we will need a way to build ut the final table used for evaluation of the prediction model.
# This script will be used to build and increment on the final table as new predictions are made
import os
import pandas as pd

# when I build other models, I can reuse this function to build the aggregated predictions for that model
def build_predictions(target):
    
    folder = os.path.expanduser(f'~/Code/stock_predictions/{target}')
    
    # Create an empty DataFrame to hold the combined data
    final_table = pd.DataFrame()

    # Loop through all the subdirectories in the parent folder
    for root, dirs, files in os.walk(folder):
        
        # Check if the current directory contains a 'tickers' folder``
        if 'tickers' in dirs:
            
            # Construct the path to the 'tickers' folder
            tickers_folder = os.path.join(root, 'tickers')
            
            # Loop through the files in the 'tickers' folder
            for file_name in os.listdir(tickers_folder):
                file_path = os.path.join(tickers_folder, file_name)
                
                # Check if it's a file and read it into a DataFrame
                if os.path.isfile(file_path):
                    if  'all_results' in file_path :
                        try:
                            # Adjust the reading method based on file format (e.g., CSV, Excel, JSON, etc.)
                            data = pd.read_csv(file_path)  # Replace with pd.read_excel(file_path) for Excel files
                            
                            # print(file_path)
                            
                            # Add data to the final table
                            final_table = pd.concat([final_table, data], ignore_index=True)
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")

    # Save the final combined table to a file (optional)
        
    final_table.to_csv('predictions_table.csv')

    return final_table 

# each time predictions the script is ran, need to add the results to the summary.csv file
def increment_predictions(target,table):
    folder = os.path.expanduser(f'~/Code/stock_predictions/{target}')
    
    #get the DataFrame of the file that I want to append the results to for the predictions
    incremented_summary = pd.read_csv(table)[['ticker'
                                              ,'total_predictions'
                                              ,'total_correct_predicions'
                                              ,'overall_success_rate'
                                              ,'predicted_higher_correct'
                                              ,'total_predicted_higher'
                                              ,'predicted_higher_success_rate'
                                              ,'adj_sell_vs_pred_pct'
                                              ,'latest_close'
                                              ,'last_date_for_prediction'
                                              ,'prediction_price'
                                              ,'adj_prediction_price'
                                              ,'adj_prediction_higher'
                                              ,'stop_loss'
                                              ,'adj_prediction_price_w_high_inc']]
    current_max_date=max(incremented_summary['last_date_for_prediction'])

    # Loop through all the subdirectories in the parent folder
    for root, dirs, files in os.walk(folder):
        
        print(root)
        
        # Check if the current directory contains a 'tickers' folder``
        if 'tickers' in root:
                        
            # Loop through the files in the 'tickers' folder
            for file_name in os.listdir(root):
                file_path = os.path.join(root, file_name)
                
                # Check if it's a file and read it into a DataFrame
                if os.path.isfile(file_path):
                    if  'all_results' in file_path :
                        try:
                            new_data = pd.read_csv(file_path)[['ticker'
                                              ,'total_predictions'
                                              ,'total_correct_predicions'
                                              ,'overall_success_rate'
                                              ,'predicted_higher_correct'
                                              ,'total_predicted_higher'
                                              ,'predicted_higher_success_rate'
                                              ,'adj_sell_vs_pred_pct'
                                              ,'latest_close'
                                              ,'last_date_for_prediction'
                                              ,'prediction_price'
                                              ,'adj_prediction_price'
                                              ,'adj_prediction_higher'
                                              ,'stop_loss'
                                              ,'adj_prediction_price_w_high_inc']]
                            
                            new_date=max(new_data['last_date_for_prediction'])

                            if max(new_data['last_date_for_prediction']) > current_max_date:
                                # Adjust the reading method based on file format (e.g., CSV, Excel, JSON, etc.)
                                
                                print(f"Current max date: {current_max_date}")
                                print(f"New data date: {new_date}")
                                print(f"Length of predictions table: {len(incremented_summary)}")
                                print(f"Length of new data: {len(new_data)}")
                                print(f"Length of combined data after concat {len(pd.concat([incremented_summary,new_data]))}")
                                
                                pd.concat([incremented_summary,new_data]).to_csv(table)
                                
                                print(f'Predictions summary updated with data from {new_date}')
                                
                                return f'Predictions summary updated with data from {new_date}'
                                                        
                            
                            # Add data to the final table
                            # final_table = pd.concat([final_table, data], ignore_index=True)
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
                    else:
                       
                        print(f"All results not in file path")
   
# run this everytime the predictions script is ran to add on to non_trigger_stocks for new predictions
def increment_non_trigger_evals (target,table):
    folder = os.path.expanduser(f'~/Code/stock_predictions/{target}')
    
    #get the DataFrame of the file that I want to append the results to for the predictions
    incremented_summary = pd.read_csv(table)[['ticker'
                                              ,'buy_price'
                                              ,'overall_success_rate'
                                              ,'predicted_higher_success_rate'
                                              ,'last_date'
                                              ,'adj_prediction_price'
                                              ,'adj_price_higher'
                                              ,'stop_loss'
                                              ,'latest_close']]
    current_max_date=max(incremented_summary['last_date'])

    # Loop through all the subdirectories in the parent folder
    for root, dirs, files in os.walk(folder):
        
        
        # Check if the current directory contains a 'tickers' folder``
        if 'tickers' in root:
            # print(root)

            # Loop through the files in the 'tickers' folder
            for file_name in os.listdir(root):
                file_path = os.path.join(root, file_name)
                # print(file_path)
                

                # Check if it's a file and read it into a DataFrame
                if os.path.isfile(file_path):
                    if  'all_results' in file_path :
                        
                        print(file_path)
                        try:
                            new_data = pd.read_csv(file_path)[['ticker'
                                              ,'latest_close'
                                              ,'overall_success_rate'
                                              ,'predicted_higher_success_rate'
                                              ,'last_date_for_prediction'
                                              ,'adj_prediction_price_w_high_inc'
                                              ,'adj_prediction_higher'
                                              ,'stop_loss '
                                              ]]
                            
                            new_data['buy_price']=new_data['latest_close']
                            
                            #             'ticker'
                            #                   ,'buy_price'
                            #                   ,'overall_success_rate'
                            #                   ,'predicted_higher_success_rate'
                            #                   ,'last_date'
                            #                   ,'adj_prediction_price'
                            #                   ,'adj_price_higher'
                            #                   ,'stop_loss'
                            #                   ,'latest_close'
                            
                            new_data.rename(columns={"last_date_for_prediction": "last_date"
                                                      , "adj_prediction_price_w_high_inc": "adj_prediction_price"
                                                      , "adj_prediction_higher": "adj_price_higher"
                                                      , "stop_loss ": "stop_loss"}, inplace=True)
                            print(new_data.columns)

                            
                            new_date=max(new_data['last_date'])

                            if new_date > current_max_date:
                                # Adjust the reading method based on file format (e.g., CSV, Excel, JSON, etc.)
                                
                                print(f"Current max date: {current_max_date}")
                                print(f"New data date: {new_date}")
                                print(f"Length of trigger stocks table: {len(incremented_summary)}")
                                print(f"Length of new data: {len(new_data)}")
                                print(f"Length of combined data after concat {len(pd.concat([incremented_summary,new_data]))}")
                                
                                pd.concat([incremented_summary,new_data]).to_csv(table)
                                # print(pd.concat([incremented_summary,new_data]))
                                
                                # print(f'Non-Triggered Stocks updated with data from {new_date}')
                                
                                return f'Non-Triggered Stocks updated with data from {new_date}'
                            else:
                                print('New data is equal to or less than current max date')
                                                        
                            
                            # Add data to the final table
                            # final_table = pd.concat([final_table, data], ignore_index=True)
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
                    # else:
                       
                    #     print(f"All results not in file path")


    return 'increment_non_trigger_evals'

# run this in backtesting to increment to existing backtest results table
def increment_backtest_results(old_results,new_results):
    print('old results')
    print(pd.read_csv(old_results))
    
    print('new_results')
    print(new_results)
    
    
    return 'increment_backtest_resultss'


# using for testing functions
if __name__ == "__main__":
#     # predictions_table = build_predictions('10_day_ahead_close/stock_performance')
#     # increment_non_trigger_evals('10_day_ahead_close/stock_performance/2024-12-05/tickers','predictions_table.csv')

#     # print(pd.read_csv('predictions/non_trigger_stocks.csv'))
#     incremented_table = increment_non_trigger_evals('10_day_ahead_close/stock_performance/2025-01-04/tickers','predictions/non_trigger_stocks.csv')
    increment_backtest_results('predictions/backtest_results.csv')
#     print(incremented_table)