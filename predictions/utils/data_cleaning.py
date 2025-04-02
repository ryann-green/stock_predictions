import pandas as pd
from data_transfer import read_from_s3,write_to_s3

# Load the data into a DataFrame (replace 'your_file.csv' with your actual file path)
df = read_from_s3('predictions_table.csv')

# Define the columns to check for anomalies
anomaly_columns = ['adj_prediction_price_w_high_inc', 'adj_prediction_price', 'prediction_price']

# Function to remove rows with anomalies based on the latest_close column
def remove_anomalies_rowwise(df, columns, reference_column):
    def is_row_valid(row):
        for column in columns:
            if abs(row[column] - row[reference_column]) > 2 * row[reference_column]:
                return False
        return True

    return df[df.apply(is_row_valid, axis=1)]

# Apply the function to the DataFrame
cleaned_df = remove_anomalies_rowwise(df, anomaly_columns, 'latest_close')

# Remove duplicate rows based on 'ticker' and 'last_date_for_prediction'
cleaned_df = cleaned_df.drop_duplicates(subset=['ticker', 'last_date_for_prediction'], keep='first')

# Save the cleaned data to a new CSV file
write_to_s3(cleaned_df,'predictions_table.csv')

print("Anomalies removed. Cleaned data saved to 'predictions_table.csv'.")