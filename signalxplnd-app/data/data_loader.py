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


def load_data():
    # Centralized function to load and preprocess data
    try:
        br_df = read_from_s3('backtest_results.csv')

        p_df = read_from_s3('predictions_table.csv')
        recs_df = read_from_s3('latest_recs.csv')
        success_ratio=read_from_s3('target_success_ratio.csv')

        # Additional preprocessing steps can go here
        return br_df,p_df, recs_df,success_ratio
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found. Ensure 'predictions/backtest_results.csv' exists.")
