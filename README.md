
# Google Calendar Assistant 📅

An AI-powered assistant for viewing and booking events on a Google Calendar. The assistant uses the Google Calendar API for scheduling and Gemini (Generative AI) for natural language understanding and conversational responses. The assistant is intentionally restricted to only answer Google Calendar related queries.

---

## 🎥 Demo Video

Check out the Smart Meeting Assistant in action:

<video src="https://github.com/user-attachments/assets/9cb5b150-964c-439f-8b7e-7f820ae8b072" width="100%" controls>
  Your browser does not support the video tag.
</video>

---

## 🚀 Features

- **Natural Language Booking:** Book meetings by simply asking the assistant.
- **Availability Check:** View available and booked slots for any given date.
- **Event Management:** Clear upcoming events easily.
- **Context-Aware:** The assistant is restricted to calendar-related queries to ensure accuracy.

---

## 🐳 Docker Setup (Recommended)

Running the project with Docker is the quickest way to get started.

### 1. Prerequisites
- Docker and Docker Compose installed.
- Google Cloud Service Account JSON (`service_account.json`).
- Gemini API Key.

### 2. Configuration
Create a `.env` file in the root directory:
```env
GOOGLE_CALENDAR_ID=your_calendar_id@group.calendar.google.com
GEMINI_API_KEY=your_gemini_api_key
```
Place your `service_account.json` in `src/credentials/service_account.json`.

### 3. Run the App
```bash
docker-compose up --build
```
Once the containers are running:
- **Frontend:** [http://localhost:8501](http://localhost:8501)
- **Backend:** [http://localhost:8000](http://localhost:8000)

---

## 🛠 Manual Setup (UV)

If you prefer to run the project locally without Docker:

### 1. Virtual Environment
```powershell
uv init .
uv venv
.venv\Scripts\activate
uv add -r requirements.txt
```

### 2. Start Services
Open two terminals:

**Terminal 1 (Backend):**
```powershell
cd src
uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```powershell
cd src
streamlit run app.py
```

---

## 🔑 Credentials Setup

1. **Google Calendar API:**
   - Enable the API in [Google Cloud Console](https://console.cloud.google.com).
   - Create a Service Account and download the JSON key as `service_account.json`.
   - Share your Google Calendar with the Service Account email (Permission: "Make changes and manage sharing").
   - Copy the Calendar ID from the calendar settings.

2. **Gemini API:**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

---

## 📡 API Endpoints

- `GET /` — Health check
- `GET /slots` — View availability
- `POST /book` — Book a meeting
- `POST /chat` — Conversational calendar assistant
