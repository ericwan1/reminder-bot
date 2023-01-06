from google.cloud import bigquery

# Grab the dataframe from BigQuery
client = bigquery.Client()
table_id = "ks-reminder-bot.gs_event_data.gs-event-df"
prod_df = client.list_rows(table_id).to_dataframe()

# want to remove all rows where the flags are 'True' which indicates the event has fired and passed