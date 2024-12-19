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

# each time the script is ran, need to add the results to the summary.csv file
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
                                              ,'stop_loss '
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
                                              ,'stop_loss '
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


   

def build_evaluations (target):
    return 'build_evaluations'

def fill_missing_evaluations():
    return 'fill_missing_evaluations'


# using for testing functions
# if __name__ == "__main__":
#      predictions_table = build_predictions('10_day_ahead_close/stock_performance')
#     increment_predictions('10_day_ahead_close/stock_performance/2024-12-05/tickers','predictions_table.csv')


#     incremented_table = increment_predictions('10_day_ahead_close/stock_performance/2024-12-06/tickers','predictions_table.csv')
    
    

#     print(incremented_table)