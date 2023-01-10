# The reminder script will fire off: 
# 72 hours before
# 24 hours before
# Three hours before 
# Thirty minutes before 

from google.cloud import bigquery
from datetime import datetime 

# Grab the dataframe from BigQuery
client = bigquery.Client()
table_id = "your.table-id.here"
prod_df = client.list_rows(table_id).to_dataframe()

times_list = prod_df['event_time']

for time in times_list:
    prod_time_val = datetime.fromisoformat(time).strftime("%Y-%m-%d %H:%M:%S")
    prod_time_val = datetime.strptime(prod_time_val, "%Y-%m-%d %H:%M:%S")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

    diff = prod_time_val - now
    diff_in_seconds = diff.total_seconds()

    # A series of checks to see if the difference meets our criteria 
    # 72 Hours
    if diff_in_seconds < 60*60*72:
        print("add the df check for flag")
        print("add twilio api here")
    # 24 Hours before
    if diff_in_seconds < 60*60*24:
        print("add the df check for flag")
        print("add twilio api here")
    # 3 Hours Before
    if diff_in_seconds < 60*60*3: 
        print("add the df check for flag")
        print("add twilio api here")
    # 30 Minutes Before
    if diff_in_seconds < 60*30:
        print("add the df check for flag")
        print("add twilio api here")