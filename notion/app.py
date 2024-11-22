import requests
import json

# Replace with your own integration token and database ID
NOTION_TOKEN = "secret_vshHX0kpl7qXN4TowTuF1Nt7wMRYahLkWq7u68CaPYS"
DATABASE_ID = "12504f4ad0b2800da07ae00a6ba66f2e" 

# Headers for the API request
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  # You can check for updates to the API version
}

# Function to retrieve data from a Notion database
def get_database_data(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Fetching data from the Notion database
data = get_database_data(DATABASE_ID)

# Pretty printing the data in JSON format
if data:
    print(json.dumps(data, indent=4))
