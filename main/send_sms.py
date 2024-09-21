from twilio.rest import Client
from decouple import config

def send_sms(phone_number, message):

    account_sid = config("ACCOUNT_SID")
    auth_token = config('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='+14158814070',
        to=phone_number #'+250783378349'
        )
    return message.sid

# print(send_sms('+250783378349'))