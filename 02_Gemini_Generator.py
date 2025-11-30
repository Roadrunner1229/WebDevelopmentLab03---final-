
import streamlit as st
import pandas as pd
from utils.api_client import fetch_weather
from utils.gemini_client import get_gemini_client

st.set_page_config(page_title="Gemini Generator", page_icon="🧠", layout="wide")
st.title("🧠 Gemini Generator — Turn Weather Data into Writing")

with st.expander("Setup (one-time)"):
    st.write("Make sure your deployment has GEMINI_API_KEY set in environment variables.")

lat = st.number_input("Latitude", value=33.7756)
lon = st.number_input("Longitude", value=-84.3963)
days = st.slider("Forecast Days", 1, 7, 3)
tone = st.selectbox("Tone", ["informative", "friendly", "funny", "formal"], index=1)
audience = st.text_input("Audience", "college students in Atlanta")

if st.button("Generate Write-Up"):
    try:
        df = fetch_weather(lat, lon, hourly="temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m", forecast_days=days)
        st.dataframe(df.head(24))

        # Condense recent slice for prompt
        use = df.dropna().head(48).to_dict(orient="list")
        model = get_gemini_client()

        prompt = f"""
        You are a meteorology explainer. Use the following hourly weather data (up to ~48 rows) to write a
        concise {tone} summary for {audience}. Include practical takeaways and 2-3 bullet tips at the end.

        DATA (python dict with parallel lists):
        {use}
        """

        resp = model.generate_content(prompt)
        st.subheader("Generated Summary")
        st.write(resp.text)

    except Exception as e:
        st.error(f"LLM generation failed safely: {e}")
