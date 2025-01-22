import pandas as pd

def load_data():
    # Centralized function to load and preprocess data
    try:
        df = pd.read_csv('predictions/backtest_results.csv')
        # Additional preprocessing steps can go here
        return df
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found. Ensure 'predictions/backtest_results.csv' exists.")
