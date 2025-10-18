import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from pathlib import Path
from config.config import Config

# Resolve service account file:
# 1. Allow explicit override via SERVICE_ACCOUNT_FILE env var.
# 2. If running on Render (container), use the mounted secret path.
# 3. Otherwise, resolve the credentials file relative to this backend package.
env_path = os.getenv("SERVICE_ACCOUNT_FILE")
if env_path:
    SERVICE_ACCOUNT_FILE = env_path
elif os.getenv("RENDER"):
    SERVICE_ACCOUNT_FILE = "/etc/secrets/service_account.json"
else:
    # Path relative to this file: .. / credentials / service_account.json
    base_dir = Path(__file__).resolve().parent
    SERVICE_ACCOUNT_FILE = str((base_dir / "credentials" / "service_account.json").resolve())

SCOPES = ['https://www.googleapis.com/auth/calendar']

CALENDAR_ID = Config.GOOGLE_CALENDAR_ID
# CALENDAR_ID = "486a89479cc4d3ca1da0d7e6f41db6d695f8d9f3520380541ffde4963598385c@group.calendar.google.com"


if not CALENDAR_ID:
    raise RuntimeError(
        "Environment variable GOOGLE_CALENDAR_ID is not set. "
        "Set it to your calendar ID (for example: 'your-calendar-id@group.calendar.google.com') "
        "or share the calendar with the service account. In PowerShell: `" +
        "$env:GOOGLE_CALENDAR_ID = 'your-calendar-id@group.calendar.google.com'`"
    )

# Fail fast with a clear message if the file doesn't exist.
if not Path(SERVICE_ACCOUNT_FILE).is_file():
    raise FileNotFoundError(
        f"Service account file not found at '{SERVICE_ACCOUNT_FILE}'.\n"
        "Provide the file at backend/credentials/service_account.json or set the SERVICE_ACCOUNT_FILE "
        "environment variable to its absolute path. On Windows PowerShell: $env:SERVICE_ACCOUNT_FILE = 'C:\\\\full\\\\path\\\\service_account.json'"
    )

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def get_available_slots(date: str):
    start_of_day = f"{date}T00:00:00Z"
    end_of_day = f"{date}T23:59:59Z"
    
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    booked_times = []
    booked_slots = []
    for event in events:
        start_time = event["start"].get("dateTime", "")
        if start_time:
            booked_times.append(start_time[:16])
            # Store booked slot with meeting name
            meeting_name = event.get("summary", "No Title")
            booked_slots.append({
                "time": start_time[:16],
                "meeting_name": meeting_name
            })

    # Define working hours
    working_hours = [f"{date}T{hour:02d}:00" for hour in range(1, 24)]  # 1AM to 11PM

    available_slots = []
    for slot in working_hours:
        if slot not in booked_times:
            available_slots.append(slot)

    return {
        "available_slots": available_slots,
        "booked_slots": booked_slots
    }


def book_slot(start_time: str, summary: str = "Booking"):
    start = datetime.fromisoformat(start_time)
    end = start + timedelta(hours=1)
    
    event = {
        'summary': summary,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event.get('htmlLink')

def clear_calendar():
    now = datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    for event in events:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
    return f"Cleared {len(events)} upcoming events."
