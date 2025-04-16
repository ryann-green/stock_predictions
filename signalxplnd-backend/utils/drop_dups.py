import pandas as pd
from data_transfer import read_from_s3, write_to_s3

def clean_file(file,date_col):

    results=read_from_s3(file)
    print(results)

    duplicates = results[results.duplicated(subset=["ticker", date_col], keep=False)].sort_values(by=["ticker", date_col])

    # Display duplicates
    print(f"\nDuplicate Rows based on ['ticker', {date_col}] in {file}:")
    print(duplicates)
    
    if duplicates.empty == False:

        # Remove duplicates based on `ticker` and `pred_date`, keeping the first occurrence
        df_cleaned = results.drop_duplicates(subset=["ticker", f"{date_col}"], keep="first")

        # Confirm there are no more duplicates
        print('These are the remaining duplicates')
        print(df_cleaned[df_cleaned.duplicated(subset=["ticker", f"{date_col}"], keep=False)])
        
        write_to_s3(df_cleaned,file)
        
    else:
        print('there are no duplicates')


