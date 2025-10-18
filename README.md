
# Google Calendar Assistant

An AI-powered assistant for viewing and booking events on a Google Calendar. The assistant uses Google Calendar API for scheduling and Gemini (Generative AI) for natural language understanding and conversational responses. The assistant is intentionally restricted to only answer Google Calendar related queries.

## Demo Video :


https://github.com/user-attachments/assets/9cb5b150-964c-439f-8b7e-7f820ae8b072



## Features

- View available and booked slots for a given date
- Book 1-hour meetings
- Clear upcoming events
- Conversational agent that only responds to calendar-related requests

## Quick Start

Prerequisites
- Python 3.10+
- A Google Cloud project with Calendar API enabled
- A service account JSON key with access to the calendar
- Gemini API key

## 🛠 Setup Instructions

### 1️⃣ Get Your Google Calendar Credentials

1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable Google Calendar API
4. Create a Service Account
5. Generate a JSON key and download it as `service_account.json`
6. Copy the service account email (e.g. `xyz@project.iam.gserviceaccount.com`)
7. Log in to your Google Calendar
8. On the left side, under "Other calendars", click `+` → **Create new calendar**
9. After creating the calendar, go to its Settings
10. Under "Share with specific people", click **Add people**
11. Add the service account email and set permission to "Make changes and manage sharing"
12. Scroll down to "Integrate calendar" and copy the Calendar ID

Use this Calendar ID as your `GOOGLE_CALENDAR_ID` in your config.py

---

### 2️⃣ Get Your Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy the key and paste it in your `.env` file or set it in `config/config.py`

---

## Configuration

The project reads configuration from `config/config.py`. You can set values via environment variables or edit the config file directly for local testing:

- `GOOGLE_CALENDAR_ID` - your calendar id
- `GEMINI_API_KEY` - your Gemini API key
- `BACKEND_URL` - backend URL used by the Streamlit app (default: http://localhost:8000)

Place the `service_account.json` file in `src/credentials/service_account.json` or set the `SERVICE_ACCOUNT_FILE` environment variable to its absolute path.

## API Endpoints

Short list of endpoints:

- GET / — Health check (backend running)
- GET /slots — Return available or booked slots for a date
- POST /book — Book a 1-hour meeting
- POST /chat — Send a message to the calendar assistant (Gemini-powered)


## UV project setup

1. Create a virtual environment and install dependencies:

```powershell
 uv init .
 uv venv
 .venv\Scripts\activate
 uv add -r requirements.txt
```
2. Change to the project src directory:

```powershell
cd src
```

3. Start the FastAPI backend using uvicorn (development, auto-reload enabled):

```powershell
uvicorn main:app --reload
```

4. Start the Streamlit frontend (in another terminal):

```powershell
streamlit run app.py
```



