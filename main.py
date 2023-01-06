from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.cloud import bigquery
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        next_seven_days = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'

        print('Getting all upcoming events in the next 7 days')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              timeMax=next_seven_days, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        event_names_list = []
        event_time_list = []

        for event in events:
            if "[GS]" in event['summary']:
                event_time = event['start'].get('dateTime', event['start'].get('date'))
                event_date = datetime.fromisoformat(event_time).date()
                event_date = datetime.strptime(str(event_date), "%Y-%m-%d").strftime("%m-%d-%Y")
                event_names_list.append(str(event['summary']) + ":" + str(event_date))
                event_time_list.append(str(datetime.fromisoformat(event_time)))

        event_df = pd.DataFrame(event_names_list)
        event_df.columns = ['event_name']
        event_df['event_time'] = event_time_list
        event_df['week_remind'] = False
        event_df['twoday_remind'] = False
        event_df['morningof_remind'] = False
        event_df['hour_remind'] = False
        event_df['tenmin_remind'] = False
        
        # Add the new dataframe to BigQuery
        BQclient = bigquery.Client()
        # Check if the calendar event name is aleady inside BigQuery by making a copy of the current table
        # Then we do our merge/insert based on the event name
        project = "ks-reminder-bot"
        dataset_id = "gs_event_data"
        dataset_ref = bigquery.DatasetReference(project, dataset_id)
        table_ref = dataset_ref.table("gs-event-df")
        table = BQclient.get_table(table_ref)
        prod_df = BQclient.list_rows(table).to_dataframe()
        # Take the union and remove rows with duplicate event_name and event_time values (so we keep new events)
        tables = [event_df, prod_df]
        union_df = pd.concat(tables)
        union_df.drop_duplicates(
            subset = ['event_name', 'event_time'],
            keep = False, inplace = True).reset_index(drop = True)
        BQclient.insert_rows_from_dataframe(table, union_df)  
        

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()