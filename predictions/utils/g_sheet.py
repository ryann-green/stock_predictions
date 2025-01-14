import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
# from access import get_creds


def get_credentials():
    SERVICE_ACCOUNT_FILE = 'C:/Users/datax/Code/stock_predictions/predictions/utils/service_account.json'

    # print(SERVICE_ACCOUNT_FILE)

    # Scopes required for accessing Google Sheets
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file", 
            "https://www.googleapis.com/auth/drive"]

    # Authenticate using the service account
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # print(credentials)
    # Authorize the gspread client
    client = gspread.authorize(credentials)
    
    return client


def get_sheet_data (client,spreadsheet_name):
    
    # Open the Google Sheet by name
    sheet = client.open(spreadsheet_name).sheet1  # Access the first sheet (Sheet1)

    # Read all data from the sheet
    data = sheet.get_all_values()

    # Print the data
    print("Google Sheet Data:")
    df=pd.DataFrame(data)
    df.columns = df.iloc[0]  # Set the first row as the header
    df = df[1:]
    # 
    # print(df)
    
    return df

# needed to increment predictions & non_trigger evals on main.py
# needed to increment backtesting csv on backtesting.py

def add_sheet_data (client,spreadsheet_name,new_data):
    
    # Open the Google Sheet by name
    sheet = client.open(spreadsheet_name).sheet1  # Access the first sheet (Sheet1)

    # Data to append (each inner list represents a row)
    
    # Append the data to the sheet
    for row in new_data:
        sheet.append_row(row)

    print("Data appended successfully!")
    # 
    # print(df)
    
    return 'Data Appended successfully'

# after backtesting.py runs and increments the backtesting gsheet, need to delete the sheet data
# then need to run add_sheet_data for non_trigger_evals sheet for the remaining results not captured
def delete_sheet_data():
    return 'data deleted'


        
if __name__ == "__main__":
    data_to_append = [
    ['Alice', 30],
    ['Bob', 25]
    ]
    result=add_sheet_data(get_credentials(),'test',data_to_append)
    print(result)