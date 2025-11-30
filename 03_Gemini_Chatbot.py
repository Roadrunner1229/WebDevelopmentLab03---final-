
import streamlit as st
import pandas as pd
from utils.api_client import fetch_weather
from utils.gemini_client import get_gemini_client

st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", layout="wide")
st.title("💬 Gemini Chatbot — Ask About the Forecast")

with st.expander("Setup (one-time)"):
    st.write("Ensure GEMINI_API_KEY is set in your environment variables on Streamlit Cloud.")

# "Memory" of conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

lat = st.number_input("Latitude", value=33.7756)
lon = st.number_input("Longitude", value=-84.3963)
days = st.slider("Forecast Days", 1, 7, 3)

user_q = st.text_input("Ask a question (e.g., is it good for a picnic tomorrow?)")

def ground_context_text(df: pd.DataFrame) -> str:
    # Produce a brief textual grounding from the latest 24 hours
    cols = [c for c in df.columns if c != "time"]
    df2 = df.dropna().copy()
    if "time" in df2.columns:
        df2["time"] = df2["time"].astype(str)
    # Keep it compact
    head = df2.head(24).to_dict(orient="records")
    return f"Recent hourly weather sample (first ~24 rows): {head[:12]} ..."

if st.button("Send"):
    try:
        df = fetch_weather(lat, lon, hourly="temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m", forecast_days=days)
        context = ground_context_text(df)
        model = get_gemini_client()

        # Build conversation
        chat = model.start_chat(history=[
            {"role": "user", "parts": "You are a concise weather assistant grounded only in the provided context."},
            {"role": "model", "parts": "Understood. I will answer briefly using the context."},
            *st.session_state.chat_history
        ])

        prompt = f"""
        CONTEXT (weather data):
        {context}

        USER QUESTION:
        {user_q}

        INSTRUCTIONS:
        - Answer only using the context and general knowledge of weather best practices.
        - If the context is insufficient, ask a specific follow-up.
        - Keep answers under 120 words.
        """

        resp = chat.send_message(prompt)
        st.session_state.chat_history.extend([
            {"role": "user", "parts": user_q},
            {"role": "model", "parts": resp.text}
        ])

    except Exception as e:
        st.error(f"Chat failed safely: {e}")

# Render convo
for turn in st.session_state.chat_history[-10:]:
    if turn["role"] == "user":
        st.chat_message("user").markdown(turn["parts"])
    else:
        st.chat_message("assistant").markdown(turn["parts"])

