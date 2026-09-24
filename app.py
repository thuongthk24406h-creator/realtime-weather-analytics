
import streamlit as st
import requests
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Real-Time Weather Analytics",
    page_icon="🌦️",
    layout="wide"
)

# =========================
# API
# =========================

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=10.8231"
    "&longitude=106.6297"
    "&current="
    "temperature_2m,"
    "relative_humidity_2m,"
    "apparent_temperature,"
    "precipitation,"
    "wind_speed_10m,"
    "surface_pressure"
    "&hourly="
    "temperature_2m,"
    "relative_humidity_2m,"
    "wind_speed_10m"
    "&timezone=Asia/Ho_Chi_Minh"
)


# =========================
# GET DATA
# =========================

def get_weather():

    response = requests.get(
        API_URL,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# =========================
# TITLE
# =========================

st.title("🌦️ Real-Time Weather Analytics")

st.write(
    "Dashboard phân tích dữ liệu thời tiết "
    "với Real-Time Updates."
)

st.divider()


# =========================
# REALTIME UPDATE
# =========================

@st.fragment(run_every=10)
def realtime_dashboard():

    try:

        data = get_weather()

        current = data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        apparent = current["apparent_temperature"]
        precipitation = current["precipitation"]
        wind = current["wind_speed_10m"]
        pressure = current["surface_pressure"]
        update_time = current["time"]


        # =========================
        # CURRENT METRICS
        # =========================

        st.subheader("🔴 Current Weather")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🌡️ Temperature",
            f"{temperature:.1f} °C"
        )

        col2.metric(
            "💧 Humidity",
            f"{humidity:.0f} %"
        )

        col3.metric(
            "💨 Wind",
            f"{wind:.1f} km/h"
        )


        col4, col5, col6 = st.columns(3)

        col4.metric(
            "🌡️ Feels Like",
            f"{apparent:.1f} °C"
        )

        col5.metric(
            "🌧️ Rain",
            f"{precipitation:.1f} mm"
        )

        col6.metric(
            "Pressure",
            f"{pressure:.1f} hPa"
        )


        st.divider()


        # =========================
        # HOURLY DATA
        # =========================

        hourly = data["hourly"]

        df = pd.DataFrame({

            "Time": pd.to_datetime(
                hourly["time"]
            ),

            "Temperature": hourly[
                "temperature_2m"
            ],

            "Humidity": hourly[
                "relative_humidity_2m"
            ],

            "Wind Speed": hourly[
                "wind_speed_10m"
            ]

        })


        # =========================
        # MOVING AVERAGE
        # =========================

        df["Moving Average"] = (
            df["Temperature"]
            .rolling(3)
            .mean()
        )


        # =========================
        # STATISTICS
        # =========================

        mean_temp = df["Temperature"].mean()
        max_temp = df["Temperature"].max()
        min_temp = df["Temperature"].min()
        std_temp = df["Temperature"].std()


        st.subheader("📊 Statistical Analysis")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Mean",
            f"{mean_temp:.2f} °C"
        )

        c2.metric(
            "Maximum",
            f"{max_temp:.2f} °C"
        )

        c3.metric(
            "Minimum",
            f"{min_temp:.2f} °C"
        )

        c4.metric(
            "Std Dev",
            f"{std_temp:.2f}"
        )


        # =========================
        # TEMPERATURE
        # =========================

        st.subheader("🌡️ Temperature")

        temperature_chart = df.set_index("Time")[
            [
                "Temperature",
                "Moving Average"
            ]
        ]

        st.line_chart(
            temperature_chart
        )


        # =========================
        # HUMIDITY
        # =========================

        st.subheader("💧 Humidity")

        humidity_chart = df.set_index(
            "Time"
        )[["Humidity"]]

        st.line_chart(
            humidity_chart
        )


        # =========================
        # WIND
        # =========================

        st.subheader("💨 Wind Speed")

        wind_chart = df.set_index(
            "Time"
        )[["Wind Speed"]]

        st.line_chart(
            wind_chart
        )


        # =========================
        # UPDATE INFO
        # =========================

        st.success(
            f"🟢 LIVE UPDATE | "
            f"Last data: {update_time}"
        )

        st.caption(
            "🔄 Dashboard tự động cập nhật mỗi 10 giây."
        )

        st.caption(
            "🌐 Data source: Open-Meteo API"
        )

        st.caption(API_URL)


    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )


realtime_dashboard()
