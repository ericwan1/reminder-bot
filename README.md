# reminder-bot

Making a reminder bot to notiify people of any events that may soon occur 

### Goal

We want to create a script that can be triggered automatically and manually. This script will remind people through the following platforms:

- Text 
- Groupme

We will determine when this script will fire by checking a Google Calendar for a specific event. This script will fire off a week before, 48 hours before, the morning of, an hour before, and ten minutes before the event starts.  

### Structure

We run a script (explorer) to identify all calendar events within seven days with the appropriate tag. These events and their start times are identified and filtered so that events occuring within the selected criteria listed in the goal section are kept. These events and start times are then saved into a BigQuery table, along with boolean variables serving as flags representing the reminder times listed in the goal section times, initialized to False. 

A second script (reminder) that is set to run every 15 minutes will then go through the BigQuery table and identify all of the events occuring at the set reminder times. This will be done by a date and time calculation and a check to make sure that the particular boolean flag is "False". Thus is done to ensure we do not repeat reminders for a particular event. The reminder script will then text a list of recipients using the Twilio API and change the flag for that particular reminder to True. 

At the end of each day, a third script will run and delete all rows containing past events. 

All three scripts will be triggered by Pub/Sub messages through Cloud Composer and hosted on Cloud Functions. 