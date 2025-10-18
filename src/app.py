import streamlit as st
import requests
from config.config import Config
from style import CSS

st.set_page_config(
    page_title="Smart Meeting Assistant",
    page_icon="📅",
    layout="centered"
)

# API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_URL = Config.BACKEND_URL


st.markdown("""
            <div class="main-header">
    <h1> Google Calendar Assistant 🗓️</h1>
    <p>Your AI-powered meeting assistant</p>
</div>
   """, unsafe_allow_html=True)

st.markdown(CSS, unsafe_allow_html=True)


st.divider()



if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Welcome to **Smart Meeting Assistant✨**!\n\nI can help you book meetings or check availability. Try something like:\n- *Book a meeting tomorrow at 3 PM*\n- *Show available slots on Friday*"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

user_input = st.chat_input("Ask me to book or check meetings...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(f"{API_URL}/chat", json={"message": user_input}, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    bot_reply = data.get("response", "Unexpected response from server.")
                else:
                    bot_reply = "Server busy. Please try again shortly."
            except requests.exceptions.Timeout:
                bot_reply = "⏱Server timed out. Please try again later."
            except requests.exceptions.ConnectionError:
                bot_reply = "Cannot connect to server. Make sure FastAPI is running."
            except Exception as e:
                bot_reply = f"An error occurred: {str(e)}"

            st.markdown(bot_reply, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# st.divider()
# Add clear chat button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "👋 Welcome to **Smart Meeting Assistant✨**!\n\nI can help you book meetings or check availability. Try something like:\n- *Book a meeting tomorrow at 3 PM*\n- *Show available slots on Friday*"
        })    
        st.rerun()
