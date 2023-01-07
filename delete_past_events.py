from google.cloud import bigquery

# Grab the dataframe from BigQuery
client = bigquery.Client()
table_id = "ks-reminder-bot.gs_event_data.gs-event-df"
prod_df = client.list_rows(table_id).to_dataframe()

# Want to remove all rows where the flags are 'True' which indicates the event has fired and passed
# Until we figure out definitively on the str/varchar values for the event_time column, we will delete rows where
# all reminders have been made; but deleting by past event times, regardless of reminders done makes more sense
dml_statement = (
    "DELETE gs_event_data.gs-event-df"
    "WHERE week_remind = TRUE"
    "AND twoday_remind = TRUE"
    "AND morningof_remind = TRUE"
    "AND hour_remind = TRUE"
    "AND tenmin_remind = TRUE"
)
query_job = client.query(dml_statement)
query_job.result()