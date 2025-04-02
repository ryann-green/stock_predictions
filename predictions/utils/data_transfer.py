import boto3
from io import StringIO
import subprocess
import sys 
import pandas as pd

def read_from_s3(key):
    s3 = boto3.client('s3')

    bucket_name = 'signalxplnd'
    # key = 'backtest_results.csv'

    response = s3.get_object(Bucket=bucket_name, Key=key)
    csv_data = response['Body'].read().decode('utf-8')

    df = pd.read_csv(StringIO(csv_data))

    return df

def write_to_s3(df, key):
    s3 = boto3.client('s3')
    bucket_name = 'signalxplnd'

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())
    
    
    print(f'{key} writtern to {bucket_name}')
    

