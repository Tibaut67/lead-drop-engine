import os
from fastapi import FastAPI, Form, Response
from dotenv import load_dotenv
from twilio.rest import Client
from supabase import create_client, Client as SupabaseClient

load_dotenv()

app = FastAPI(title="Lead Drop Engine")

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: SupabaseClient = create_client(SUPABASE_URL, SUPABASE_KEY)

SMS_REPLY_TEMPLATE = "Hi! Sorry we missed your call. How can we assist you today?"


@app.get("/")
def health_check():
    return {"status": "active", "service": "Lead Drop Engine"}


@app.post("/voice")
async def voice_webhook(
    From: str = Form(...),
    CallSid: str = Form(...),
    CallStatus: str = Form(None),
):
    """Twilio hits this endpoint when a call arrives."""
    # Twilio TwiML: Rings briefly and hangs up so missed-call logic fires
    twiml_response = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>Thanks for calling. We are currently assisting other clients and will text you right away.</Say>
        <Hangup/>
    </Response>
    """
    return Response(content=twiml_response, media_type="application/xml")


@app.post("/call-status")
async def call_status_webhook(
    From: str = Form(...),
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
):
    """Twilio hits this status callback when call ends/fails/is completed."""
    # Check for missed/completed call statuses
    missed_or_handled = CallStatus in ["no-answer", "busy", "canceled", "completed"]

    sms_dispatched = False
    if missed_or_handled:
        try:
            # Send automated text back to the caller
            twilio_client.messages.create(
                body=SMS_REPLY_TEMPLATE,
                from_=TWILIO_PHONE_NUMBER,
                to=From,
            )
            sms_dispatched = True
        except Exception as e:
            print(f"[Error sending SMS]: {e}")

    # Log the lead entry to Supabase
    try:
        supabase.table("leads").insert({
            "caller_phone": From,
            "call_status": CallStatus,
            "sms_sent": sms_dispatched,
            "lead_notes": f"Call SID: {CallSid}"
        }).execute()
    except Exception as e:
        print(f"[Error writing to Supabase]: {e}")

    return {"status": "recorded", "sms_sent": sms_dispatched}