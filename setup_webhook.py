import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")

# active ngrok URL
NGROK_BASE_URL = "https://lead-drop-engine.onrender.com"

client = Client(account_sid, auth_token)

# Fetch active incoming numbers
incoming_numbers = client.incoming_phone_numbers.list(phone_number=twilio_phone)

if not incoming_numbers:
    print(f"No phone number found matching {twilio_phone}")
else:
    number_sid = incoming_numbers[0].sid
    client.incoming_phone_numbers(number_sid).update(
        voice_url=f"{NGROK_BASE_URL}/voice",
        voice_method="POST",
        status_callback=f"{NGROK_BASE_URL}/call-status",
        status_callback_method="POST"
    )
    print(f"Successfully configured webhooks for {twilio_phone}!")