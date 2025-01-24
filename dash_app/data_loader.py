import pandas as pd

def load_data():
    # Centralized function to load and preprocess data
    try:
        br_df = pd.read_csv('predictions/backtest_results.csv')
        p_df = pd.read_csv('predictions/predictions_table.csv')
        # Additional preprocessing steps can go here
        return br_df,p_df
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found. Ensure 'predictions/backtest_results.csv' exists.")
