import os
import google.generativeai as genai
from calendar_utils import get_available_slots, book_slot, clear_calendar
from datetime import datetime
from config.config import Config
import re

api_key = Config.GEMINI_API_KEY
genai.configure(api_key=api_key)


def run_gemini_agent(message: str):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-flash-lite-latest")
        today_str = datetime.today().strftime("%Y-%m-%d")

        # NOTE: This prompt intentionally restricts the assistant to calendar-only behavior.
        # The assistant must refuse any request that is not directly related to viewing,
        # booking, chatting about (short assistant chat), or clearing the Google Calendar.
        # If the user asks anything else, reply exactly with: "I can only assist with google calendar related tasks."
        prompt = f"""
            Today is {today_str}.

            You are a helpful meeting assistant. You MUST ONLY answer questions related to Google Calendar tasks
            (booking meetings, viewing available slots for a date, short calendar-related chat, or clearing events).
            If the user asks any question not related to Google Calendar, you MUST NOT provide an answer to that topic
            and instead respond exactly with the sentence: I can only assist with google calendar related tasks.

            From this user message, extract:

            1. intent: 'view' or 'book' or 'chat' or 'clear'
            2. date: in YYYY-MM-DD format
            3. time: in HH:MM 24hr format (if relevant)
            4. title: short meeting title (if booking), or just say 'NA' if not applicable

            Message: {message}

            Return exactly in this format (use the literal keys and values):
            intent: <book/view/chat/clear>
            date: <YYYY-MM-DD or NA>
            time: <HH:MM or NA>
            title: <Meeting title or NA>
            """


        response = model.generate_content(prompt)
        parsed = response.text.strip()

        # If the model returned the refusal message directly, return it immediately
        if "I can only assist with google calendar related tasks" in parsed:
            return "I can only assist with google calendar related tasks."

        # Extract intent, date, time, title
        intent = re.search(r"intent:\s*(\w+)", parsed)
        date = re.search(r"date:\s*([\d\-]+)", parsed)
        time = re.search(r"time:\s*([\d:]+)", parsed)
        title = re.search(r"title:\s*(.+)", parsed)

        intent = intent.group(1).lower() if intent else "unknown"
        date = date.group(1) if date else today_str
        time = time.group(1) if time else "10:00"
        title = title.group(1).strip() if title else "Booking"

        if title.lower() in ["<optional>", "optional", "na", "none", ""]:
            title = "Booking"

        datetime_str = f"{date}T{time}:00"

        if intent == "book":
            link = book_slot(datetime_str, title)
            return f""" 
                ✅ **Meeting Booked Successfully**

                **Title:** {title}  
                **Date:** `{date}`  
                **Time:** `{time}`  

                🔗 [Click here to view it in your calendar]({link})
                """

        
        elif intent == "chat":
            # Re-prompting with context to ensure the chat response is also restricted to calendar tasks
            chat_prompt = f"""
            You are a Google Calendar assistant. 
            The user said: "{message}"

            Strict Guidelines:
            - Only answer if the request is related to viewing, booking, or managing Google Calendar.
            - If the user asks 'what can you do?', explain that you can view available slots, book meetings, and clear the calendar.
            - For any unrelated topics, respond exactly with: "I can only assist with google calendar related tasks."
            - Keep your response concise and professional.
            """
            chat_res = model.generate_content(chat_prompt).text.strip()
            return chat_res

        elif intent == "view":
            result = get_available_slots(date)
            available_slots = result["available_slots"]
            booked_slots = result["booked_slots"]
            
            response = f"📅 **Calendar for `{date}`**\n\n"
            
            # Show booked slots with meeting names
            if booked_slots:
                response += "🔴 **Booked Meetings:**\n"
                for slot in booked_slots:
                    time_display = slot["time"][-5:]  # Extract HH:MM
                    response += f"• `{time_display}` - **{slot['meeting_name']}**\n"
                response += "\n"
            
            # Show available slots
            if available_slots:
                response += "🟢 **Available Slots:**\n"
                slot_list = "\n".join([f"• `{s[-5:]}`" for s in available_slots])
                response += slot_list
            else:
                response += "🟢 **No available slots on this day.**"
            
            return response
        elif intent == "clear":
            clear_calendar()
            return "🗑️ **All events cleared from the calendar.**"
        else:
            return (
                "I couldn't understand your request.\n\n"
                "Try saying:\n"
                "- `Book a meeting tomorrow at 3 PM`\n"
                "- `Check slots for Friday`"
            )

    except Exception as e:
        return f"❌ **Error:** {str(e)}"
    

# print(model)
# print(run_gemini_agent("hi please clear my calendar for today"))