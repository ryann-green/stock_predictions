import pandas as pd

# Remove duplicates based on `ticker` and `pred_date`, keeping the first occurrence
df_cleaned = pd.read_csv('summary_results.csv').drop_duplicates(subset=["ticker", "pred_date"], keep="first")

# Display the cleaned DataFrame
print(df_cleaned)

# Optionally save the cleaned data to a CSV
df_cleaned.to_csv("summary_results_cleaned.csv", index=False)