# This script will go through the BigQuery Table and identify events that meet our criteria of:
# 1. One week before
# 2. 48 Hours Before
# 3. The morning of
# 4. An hour before
# 5. Ten minutes before

from google.cloud import bigquery
from datetime import datetime 

# Add the new dataframe to BigQuery
# client = bigquery.Client()
# table_id = "ks-reminder-bot.gs_event_data.gs-event-df"
# prod_df = client.list_rows(table_id).to_dataframe()

# times_list = prod_df['event_time']

# for time in times_list:
    
test_val = '2023-01-07 15:35:00-06:00'

# print(datetime.strptime(test_val, '%Y-%m-%d %H:%M:%S'))