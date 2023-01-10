# reminder-bot

Making a reminder bot to notify people of any events that may soon occur 

### Goal

We want to create a script that can be triggered automatically and manually. This script will remind people through text.

We will determine when this script will fire by checking a Google Calendar for a specific event. This script will fire off 72 hours before, 24 hour, three hours before, and thirty minutes before the event starts.  

### Design

We run a script (explorer) to identify all calendar events within seven days with the appropriate tag. These events and their start times are identified and filtered so that events occuring within the selected criteria listed in the goal section are kept. This information is then saved into a BigQuery table, along with boolean variables serving as flags representing the reminder times listed in the goal section times, initialized to False. The explorer script will run every day at midnight. 

A second script (reminder) that is set to run every 15 minutes will then go through the BigQuery table and identify all of the events occuring at the set reminder times. This will be done by a date and time calculation and a check to make sure that the particular boolean flag is "False". Thus is done to ensure we do not repeat reminders for a particular event. The reminder script will then text a list of recipients using the Twilio/Text service API and change the flag for that particular reminder to True. 

At the end of each day, a third script (clean-up) will run and delete all rows containing past events. This check will be done by looking at the date of the event. 

All three scripts will be triggered by Pub/Sub messages through Cloud Composer and will be hosted on Cloud Functions. 