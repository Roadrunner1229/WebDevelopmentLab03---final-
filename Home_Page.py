import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="Web Development Lab03", page_icon="🌐", layout="wide")

# --- Title of App ---
st.title("Web Development Lab03")

# --- Assignment Data ---
st.header("CS 1301 Web Development Lab03")
st.subheader("Team 71 — Web Development")
st.subheader("Team Members: Nishan Watson (Section A, 8:25AM), Sriyash Tantia (Section B, 12:30PM)")

# --- 📸 Image Banner ---
# Make sure our images are saved inside the "Images" folder
st.image("Images/test_image.png", use_container_width=True, caption="Our Lab03 Project Banner")

# --- Introduction and Page Descriptions ---
st.write("""
Welcome to our **Streamlit Web Development Lab03** app!  
Use the **sidebar** or the **page links below** to explore each section of our project.  

### 📑 Page Overview
1. **Home Page** — Project introduction, team information, and page descriptions.  
2. **API Explorer** — Pulls and visualizes live weather data using the Open-Meteo API.  
   Includes user inputs for latitude, longitude, and forecast days, plus a dynamic chart.  
3. **Gemini Generator** — Uses the same API data to create a human-readable forecast
   summary using Google Gemini, with controls for tone and use case.  
4. **Gemini Chatbot** — An AI chatbot with conversation memory that answers questions
   about the fetched forecast, wrapped safely with try/except to avoid crashes.  
""")

# --- Footer ---
st.markdown(
    """
    <hr style="border:1px solid #444; margin-top:2em; margin-bottom:0.5em;">
    <p style="text-align:center; color:gray;">
        Made with 🫶🏾 and <a href="https://streamlit.io" target="_blank" style="color:#7aa2f7; text-decoration:none;">Streamlit</a>
    </p>
    """,
    unsafe_allow_html=True
)
