# Lead Drop Engine

An automated voice and lead-capture engine built with **FastAPI**, **Twilio**, and **Supabase**. It handles incoming voice webhooks, dispatches instant follow-up SMS messages to callers, and logs lead activity directly to a PostgreSQL database.

---

## Features

* **Voice Webhook Handling:** Answers inbound calls and responds with dynamic TwiML instructions.
* **Instant SMS Follow-Ups:** Automatically triggers personalized SMS notifications to callers upon call completion.
* **Database Persistence:** Logs caller phone numbers, call status, and message delivery states into Supabase in real time.
* **Production Ready:** Configured for lightweight deployment on Render with automated environment variable binding.

---

## Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Telephony & Messaging:** Twilio Voice & SMS APIs
* **Database:** Supabase (PostgreSQL)
* **Deployment:** Render / ngrok (Local tunneling)

---

## Getting Started

### 1. Clone & Install Dependencies
```bash
git clone [https://github.com/YOUR_USERNAME/lead-drop-engine.git](https://github.com/YOUR_USERNAME/lead-drop-engine.git)
cd lead-drop-engine
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
