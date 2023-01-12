from google.cloud import bigquery

# Grab the dataframe from BigQuery
client = bigquery.Client()
table_id = "ks-reminder-bot.gs_event_data.gs-event-df"
prod_df = client.list_rows(table_id).to_dataframe()

# Want to check the date for each object we have in the BigQuery. 
# If this is not feasible with DML/SQL manipulation, then we may need to just delete/reupload. 
dml_statement = (
)
query_job = client.query(dml_statement)
query_job.result()