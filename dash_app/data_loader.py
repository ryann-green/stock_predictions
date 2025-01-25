import pandas as pd

def load_data():
    # Centralized function to load and preprocess data
    try:
        br_df = pd.read_csv('predictions/backtest_results.csv')

        p_df = pd.read_csv('predictions/predictions_table.csv')
        recs_df = pd.read_csv('rankings/latest_recs.csv')

        # Additional preprocessing steps can go here
        return br_df,p_df, recs_df
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found. Ensure 'predictions/backtest_results.csv' exists.")
