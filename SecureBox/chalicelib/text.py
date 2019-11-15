import os
from dotenv import load_dotenv

# Twilio API
from twilio.rest import Client

# Twilio setup
load_dotenv()
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_NUM = os.getenv("TWILIO_NUM")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def textUser(phoneNumber, trackingID):
    client.messages.create(
        to=phoneNumber,
        from_=TWILIO_NUM,
        body='Your order: ' + trackingID + ' has arrived. \nIt is safe with SecureBox!'
    )

