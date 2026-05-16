from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import run_gemini_agent
from calendar_utils import get_available_slots, book_slot
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is Running"}

@app.get("/slots")
def get_slots(date: str = None, booked: bool = False):
    """Return available slots or booked event details when `booked=true`.

    Query params:
    - date: YYYY-MM-DD (defaults to tomorrow)
    - booked: if true, return booked event details for the date instead of available slots
    """
    if not date:
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    slots = get_available_slots(date)
    return {"date": date, "slots": slots}

class BookingRequest(BaseModel):
    start_time: str
    summary: str = "Meeting"

@app.post("/book")
def book_meeting(req: BookingRequest):
    link = book_slot(req.start_time, req.summary)
    return {"status": "booked", "link": link}

@app.post("/chat")
def chat_with_bot(request: dict):
    message = request.get("message")
    response = run_gemini_agent(message)
    return {"response": response}