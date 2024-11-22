import os
from datetime import datetime

# Get the current date in YYYY-MM-DD format
current_date = datetime.now().strftime('%Y-%m-%d')

# Define the path to the new folder within the home directory
home_directory = os.path.expanduser('~/Code/stock_predictions')
new_folder_path = os.path.join(home_directory, current_date)

# Create the folder if it doesn't already exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Folder created: {new_folder_path}")
else:
    print(f"Folder already exists: {new_folder_path}")
