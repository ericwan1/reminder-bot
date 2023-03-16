import pandas as pd
import os

from twilio.rest import Client


def twilo_sendmsg(message_to_send = "Hello $name$"):
    # Account SID from twilio.com/console
    account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # Auth Token from twilio.com/console
    auth_token  = "your_auth_token"
    # Host Phone Number
    host_number = "+1999999999"
    numbers = []
    country_code = "+1"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.csv")
    users_df = pd.read_csv(file_path)
    client = Client(account_sid, auth_token)
    for user,phone_number in zip(users_df["name"],users_df["phone_number"]):
        if "$name$" in message_to_send:
            message_to_send = message_to_send.replace("$name$", str(user))
        message = client.messages.create(
            to=phone_number, 
            from_=host_number,
            body=message_to_send)
    

# twilo_sendmsg("TEST FROM TWILLO")