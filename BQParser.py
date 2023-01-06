# This script will go through the BigQuery Table and identify events that meet our criteria of:
# 1. One week before
# 2. 48 Hours Before
# 3. The morning of
# 4. An hour before
# 5. Ten minutes before

from google.cloud import bigquery
from datetime import datetime 

# Grab the dataframe from BigQuery
client = bigquery.Client()
table_id = "ks-reminder-bot.gs_event_data.gs-event-df"
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

    # One Week
    if diff_in_seconds < 60*60*24*7:
        print("add the df check for flag")
        print("add twilio api here")
    # 48 Hours before
    if diff_in_seconds < 60*60*24*2:
        print("add the df check for flag")
        print("add twilio api here")
    # The Morning of
    if (diff_in_seconds < 60*60 
        and str(prod_time_val.strftime("%Y-%m-%d")) == str(now.strftime("%Y-%m-%d"))
        and (now - (construct_9_am_same_day_here) > 0)
        ):
        print("add the df check for flag and construct the 9 am datetime object")
        print("add twilio api here")
    # An hour before
    if diff_in_seconds < 60*60:
        print("add the df check for flag")
        print("add twilio api here")
    if diff_in_seconds < 60*10:
        print("add the df check for flag")
        print("add twilio api here")