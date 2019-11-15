# Twilio API
from twilio.rest import Client

# Twilio setup
account_sid = 'ACf67acf4d28c0179345cff20994e926ea' # Found on Twilio Console Dashboard
auth_token = '2cd0a78dc75c752be2066351ecdaf7d2' # Found on Twilio Console Dashboard
#myPhone = '+17788997644' # Phone number you used to verify your Twilio account
TwilioNumber = '+19073187478' # Phone number given to you by Twilio
client = Client(account_sid, auth_token)

def textUser(phoneNumber, trackingID):
    client.messages.create(
        to=phoneNumber,
        from_=TwilioNumber,
        body='Your order: ' + trackingID + 'has arrived! ' u'\U0001f680'
    )