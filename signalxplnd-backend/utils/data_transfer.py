import boto3
from io import StringIO
import pandas as pd
import re

def read_from_s3(key):
    s3 = boto3.client('s3')

    bucket_name = 'signalxplnd'
    # key = 'backtest_results.csv'

    response = s3.get_object(Bucket=bucket_name, Key=key)
    csv_data = response['Body'].read().decode('utf-8')

    df = pd.read_csv(StringIO(csv_data))

    return df

def write_to_s3(df, key):
    
    # Validate that all 'ticker' values are strings with at least one letter
    if 'ticker' in df.columns:
        is_valid_ticker = df['ticker'].apply(
            lambda x: isinstance(x, str) and bool(re.search(r'[A-Za-z]', x))
        )

        if not is_valid_ticker.all():
            raise ValueError("All values in the 'ticker' column must be strings containing at least one letter.")

    s3 = boto3.client('s3')
    bucket_name = 'signalxplnd'

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())
    
    
    print(f'{key} written to {bucket_name}')
    

