import csv
import os

from twilio.rest import Client


def twilo_sendmsg(message = "Test"):
    # Account SID from twilio.com/console
    account_sid = "AC4878955fa4507e782386ab45829e7824"
    #account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # Auth Token from twilio.com/console
    auth_token  = "e69a1cd59fb765a22211d7ff6842289d"
    #auth_token  = "your_auth_token"
    # Host Phone Number
    host_number = "+19382224809"
    numbers = []
    country_code = "+1"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.csv")
    with open(file_path) as f:
        for number in f:
            number = number.strip()
            number = number.replace("-","")
            print(number)
            if number[0] == "+":
                numbers.append(number)
            else:
                numbers.append(country_code+number)
    client = Client(account_sid, auth_token)
    for number in numbers:
        print("sending messages to:", number)
        message = client.messages.create(
            to=number, 
            from_=host_number,
            body=message)
    print("done")

twilo_sendmsg("TEST FROM TWILLO")