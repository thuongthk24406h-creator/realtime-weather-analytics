

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Real-Time Weather",
    page_icon="🌦️",
    layout="wide"
)

# ==================================================
# CẤU HÌNH
# ==================================================

LATITUDE = 10.8231
LONGITUDE = 106.6297

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
    "&timezone=Asia/Ho_Chi_Minh"
)


# ==================================================
# LẤY DỮ LIỆU
# ==================================================

def get_weather():

    response = requests.get(
        API_URL,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ==================================================
# TIÊU ĐỀ
# ==================================================

st.title("🌦️ Real-Time Weather Monitoring")

st.write(
    "Theo dõi dữ liệu thời tiết hiện tại "
    "và cập nhật tự động."
)

st.divider()


# ==================================================
# REAL-TIME DASHBOARD
# ==================================================

@st.fragment(run_every=10)
def realtime_dashboard():

    try:

        data = get_weather()

        current = data["current"]


        # ==========================================
        # DỮ LIỆU HIỆN TẠI
        # ==========================================

        temperature = current["temperature_2m"]

        humidity = current["relative_humidity_2m"]

        apparent = current["apparent_temperature"]

        precipitation = current["precipitation"]

        wind = current["wind_speed_10m"]

        pressure = current["surface_pressure"]

        data_time = current["time"]


        # ==========================================
        # THÔNG TIN HIỆN TẠI
        # ==========================================

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
            "💨 Wind Speed",
            f"{wind:.1f} km/h"
        )


        col4, col5, col6 = st.columns(3)

        col4.metric(
            "🌡️ Feels Like",
            f"{apparent:.1f} °C"
        )

        col5.metric(
            "🌧️ Precipitation",
            f"{precipitation:.1f} mm"
        )

        col6.metric(
            "Pressure",
            f"{pressure:.1f} hPa"
        )


        st.divider()


        # ==========================================
        # TRẠNG THÁI REALTIME
        # ==========================================

        st.subheader("🔄 Real-Time Status")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Current Temperature",
            f"{temperature:.1f} °C"
        )

        c2.metric(
            "Data Time",
            data_time
        )

        c3.metric(
            "System Check",
            datetime.now().strftime("%H:%M:%S")
        )


        st.success(
            "🟢 LIVE — Hệ thống đang tự động "
            "kiểm tra dữ liệu mới mỗi 10 giây."
        )


        # ==========================================
        # BIỂU ĐỒ CHỈ HIỆN DỮ LIỆU ĐÃ QUA
        # ==========================================

        st.subheader(
            "📈 Temperature History"
        )

        # Lấy dữ liệu theo giờ của 1 ngày trước
        history_url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=10.8231"
            "&longitude=106.6297"
            "&hourly=temperature_2m"
            "&past_days=1"
            "&forecast_days=0"
            "&timezone=Asia/Ho_Chi_Minh"
        )

        history_response = requests.get(
            history_url,
            timeout=10
        )

        history_data = history_response.json()

        history = pd.DataFrame({

            "Time": pd.to_datetime(
                history_data["hourly"]["time"]
            ),

            "Temperature": history_data[
                "hourly"
            ]["temperature_2m"]

        })


        # Chỉ lấy tới thời điểm hiện tại
        now = pd.Timestamp.now(
            tz="Asia/Ho_Chi_Minh"
        ).tz_localize(None)

        history = history[
            history["Time"] <= now
        ]


        history = history.set_index("Time")


        st.line_chart(
            history["Temperature"]
        )


        # ==========================================
        # SOURCE
        # ==========================================

        st.divider()

        st.subheader("🌐 Data Source")

        st.write(
            "Open-Meteo API"
        )

        st.code(
            API_URL
        )


    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )


# ==================================================
# CHẠY APP
# ==================================================

realtime_dashboard()
