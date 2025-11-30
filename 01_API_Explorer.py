import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.api_client import fetch_weather

st.set_page_config(page_title="API Explorer", page_icon="📊", layout="wide")
st.title("📊 API Explorer — Open-Meteo")

st.caption("Live weather pulled from the Open-Meteo API (no key required).")

# ---- Inputs ---------------------------------------------------------------
col1, col2, col3 = st.columns([1,1,1])
with col1:
    lat = st.number_input("Latitude", value=33.7756, help="e.g., Atlanta ~ 33.7756")
with col2:
    lon = st.number_input("Longitude", value=-84.3963, help="e.g., Atlanta ~ -84.3963")
with col3:
    days = st.slider("Forecast Days", 1, 7, 3)

# Include precipitation & wind speed (10m)
metrics = st.multiselect(
    "Select hourly metrics",
    ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
    default=["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"]
)

# ---- Fetch & display ------------------------------------------------------
if st.button("Fetch Data"):
    try:
        df = fetch_weather(lat, lon, hourly=",".join(metrics), forecast_days=days)
        if df.empty:
            st.warning("No data returned. Try different coordinates/days.")
            st.stop()

        # ---- Derived/US-friendly units (only if source columns exist) ----
        if "temperature_2m" in df.columns:
            df["temp_f"] = df["temperature_2m"] * 9/5 + 32
        if "wind_speed_10m" in df.columns:
            df["wind_mph"] = df["wind_speed_10m"] * 2.23694   # m/s -> mph
        if "precipitation" in df.columns:
            df["precip_in"] = df["precipitation"] / 25.4      # mm -> inches

        st.success("Fetched data successfully!")
        show_cols = ["time"] + [c for c in [
            "temperature_2m","temp_f",
            "relative_humidity_2m",
            "precipitation","precip_in",
            "wind_speed_10m","wind_mph"
        ] if c in df.columns]
        st.dataframe(df[show_cols].head(30))

        # ---- Dynamic chart ------------------------------------------------
        numeric_cols = [c for c in df.columns if c != "time" and pd.api.types.is_numeric_dtype(df[c])]
        series = st.selectbox("Choose a series to chart", numeric_cols)
        if "time" in df.columns and series in df.columns:
            st.subheader(f"{series.replace('_',' ').title()} over Time")
            fig = plt.figure()
            plt.plot(df["time"], df[series])
            plt.xlabel("Time")
            plt.ylabel(series.replace("_"," ").title())
            st.pyplot(fig)

        # ---- Summary stats ------------------------------------------------
        st.subheader("Summary Stats")
        num_cols = [c for c in numeric_cols]
        st.write(df[num_cols].describe())

    except Exception as e:
        st.error(f"Error fetching data: {e}")

