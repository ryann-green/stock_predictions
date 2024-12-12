import pandas as pd
from datetime import datetime, timedelta

def get_missing_dates():
    # use this to rebuild predictions when needed
    # last_data_date = datetime(2023, 12, 31).date()

    last_data_date= datetime.strptime(max(pd.read_csv('predictions_table.csv')['last_date_for_prediction']),'%Y-%m-%d').date()
    current_date=datetime.now().date()
    # print(current_date-last_data_date)

    # Generate all dates between the last date and current date
    date_list = []
    while last_data_date < current_date:
        last_data_date += timedelta(days=1)
        date_list.append(last_data_date.strftime('%Y-%m-%d'))

    # Print the dates
    print("Dates between last date in file and current date:")
    for date in date_list:
        print(date)
        
    return (date_list)
