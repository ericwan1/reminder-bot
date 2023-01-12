# The reminder script will fire off: 
# 72 hours before
# 24 hours before
# Three hours before 
# Thirty minutes before 

from google.cloud import bigquery
from datetime import datetime 
import pandas as pd

# Grab the dataframe from BigQuery
client = bigquery.Client()
table_id = "your.table-id.here"
prod_df = client.list_rows(table_id).to_dataframe()

# Function to apply to all rows:
def calculate_remind_and_check_flags(a_row):
    row_time = a_row['event_time']
    prod_time_val = datetime.fromisoformat(row_time).strftime("%Y-%m-%d %H:%M:%S")
    prod_time_val = datetime.strptime(prod_time_val, "%Y-%m-%d %H:%M:%S")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

    diff = prod_time_val - now
    diff_in_seconds = diff.total_seconds()

    if prod_time_val < now:
        a_row['event_time'] = "past_event"
    else:
        # A series of checks to see if the difference meets our criteria 
        # 72 Hours
        if diff_in_seconds < 60*60*72:
            if a_row['threeday_remind'] == False:
                a_row['threeday_remind'] == True
                print("add twilio integration here")
        # 24 Hours before
        if diff_in_seconds < 60*60*24:
            if a_row['day_remind'] == False:
                a_row['day_remind'] == True
                print("add twilio integration here")
        # 3 Hours Before
        if diff_in_seconds < 60*60*3: 
            if a_row['threehour_remind'] == False:
                a_row['threehour_remind'] == True
                print("add twilio integration here")
        # 30 Minutes Before
        if diff_in_seconds < 60*30:
            if a_row['thirtymin_remind'] == False:
                a_row['thirtymin_remind'] == True
                print("add twilio integration here")
    
    return a_row

# Apply the function to all rows of the dataframe
output_df = prod_df.apply(lambda row: calculate_remind_and_check_flags(row))

# Remove past events 
output_df = output_df[output_df.event_time != "past_event"]

# Delete all rows in BigQuery
dml_statement = (
    f"DELETE FROM `{table_id}` WHERE true;"
)
delete_job = client.query(dml_statement)
delete_job.result

# Upload output_df to BigQuery
errors = client.insert_rows_from_dataframe(table_id, output_df)  
if errors == []:
    print("Data Successfully Uploaded to BigQuery")
else:
    print(errors)


# This should be made redundant by vectorization
# Delete once we confirm the above code works

# for time in times_list:
#     prod_time_val = datetime.fromisoformat(time).strftime("%Y-%m-%d %H:%M:%S")
#     prod_time_val = datetime.strptime(prod_time_val, "%Y-%m-%d %H:%M:%S")

#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

#     diff = prod_time_val - now
#     diff_in_seconds = diff.total_seconds()

#     # A series of checks to see if the difference meets our criteria 
#     # 72 Hours
#     if diff_in_seconds < 60*60*72:
#         print("add the df check for flag")
#         print("add twilio api here")
#     # 24 Hours before
#     if diff_in_seconds < 60*60*24:
#         print("add the df check for flag")
#         print("add twilio api here")
#     # 3 Hours Before
#     if diff_in_seconds < 60*60*3: 
#         print("add the df check for flag")
#         print("add twilio api here")
#     # 30 Minutes Before
#     if diff_in_seconds < 60*30:
#         print("add the df check for flag")
#         print("add twilio api here")