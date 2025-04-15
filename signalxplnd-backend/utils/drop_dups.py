import pandas as pd
from data_transfer import read_from_s3, write_to_s3

def clean_files(file):

    results=read_from_s3(file)
    print(results)

    duplicates = results[results.duplicated(subset=["ticker", "pred_date"], keep=False)].sort_values(by=["ticker", "pred_date"])

    # Display duplicates
    print(f"\nDuplicate Rows based on ['ticker', 'pred_date'] in {file}:")
    print(duplicates)
    
    if duplicates.empty == False:

        # Remove duplicates based on `ticker` and `pred_date`, keeping the first occurrence
        df_cleaned = results.drop_duplicates(subset=["ticker", "pred_date"], keep="first")

        # Confirm there are no more duplicates
        print(df_cleaned[df_cleaned.duplicated(subset=["ticker", "pred_date"], keep=False)])
        
        write_to_s3(df_cleaned,file)
        
    else:
        print('there are no duplicates')

# Optionally save the cleaned data to a CSV
clean_files('backtest_results.csv')