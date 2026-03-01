import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import time

st.set_page_config(page_title="Digital Twin Dashboard", layout="wide")

st.title("🏗️ Escalator Digital Twin Monitor")

# ------------------ DIGITAL TWIN VIEW ------------------
st.subheader("3D Digital Twin View")

components.iframe(
    "http://127.0.0.1:8080",  
    height=500,
    scrolling=False
)

# Auto refresh
refresh_rate = 1 # seconds

# Create session state to store history
if "data_history" not in st.session_state:
    st.session_state.data_history = pd.DataFrame(
        columns=["temperature", "vibration", "health"]
    )

while True:

    try:
        # Get data from FastAPI backend
        response = requests.get("http://127.0.0.1:8000/predict-once")
        data = response.json()

        # If buffer not ready yet
        if "status" in data and data["status"] == "collecting_data":
            st.warning(f"Collecting data... Please wait.")
            time.sleep(refresh_rate)
            st.rerun()

        # Store new values
        new_row = {
            "temperature": data["stress_indices"]["TSI"],
            "vibration": data["stress_indices"]["MSI"],
            "health": data["health_score"]
        }

        st.session_state.data_history.loc[
            len(st.session_state.data_history)
        ] = new_row

        # Limit history to last 50 values
        st.session_state.data_history = st.session_state.data_history.tail(50)


        st.subheader("Asset Information")
        col1, col2, col3 = st.columns(3)
        col1.metric("Health Score", data["health_score"])
        col2.metric("Health State", data["health_state"])
        col3.metric("Predicted RUL", data["predicted_rul"])

        st.subheader("AI Prediction")
        col1, col2 = st.columns(2)
        if data["anomaly_score"] is None:
            anomaly_display = "N/A"
        else:
            anomaly_display = data["anomaly_score"]
    
        col1.metric("Anomaly Score", anomaly_display)
        col2.metric("Anomaly Detected", data["anomaly_detected"])

        st.subheader("Stress Indices")
        col1, col2, col3 = st.columns(3)
        if data["stress_indices"]["TSI"] is None:
            tsi_display = "N/A"
        else:
            tsi_display = round(data["stress_indices"]["TSI"], 4)
        col1.metric("Thermal Stress (TSI)", tsi_display)

        if data["stress_indices"]["MSI"] is None:
            msi_display = "N/A"
        else:
            msi_display = round(data["stress_indices"]["MSI"], 4)
        col2.metric("Mechanical Stress (MSI)", msi_display)

        if data["stress_indices"]["LSI"] is None:
            lsi_display = "N/A"
        else:
            lsi_display = round(data["stress_indices"]["LSI"], 4)
        col3.metric("Load Stress (LSI)", lsi_display)

        if data["stress_indices"]["EDI"] is None:
            edi_display = "N/A"
        else:
            edi_display = round(data["stress_indices"]["EDI"], 4)
        col1.metric("Efficiency Degradation (EDI)", edi_display)

        st.subheader("Maintenance Recommendation")
        col1, col2, col3 = st.columns(3)
        col1.metric("Maintenance Schedule", data["maintenance_schedule"])
        col2.metric("Maintenance Priority", data["maintenance_priority"])
        col3.metric("Maintenance Action", data["maintenance_action"])

        st.subheader("Real-Time Trends")
        st.subheader("Temperature")
        st.line_chart(st.session_state.data_history["temperature"])
        st.subheader("Vibration")
        st.line_chart(st.session_state.data_history["vibration"])
        st.subheader("Health")
        st.line_chart(st.session_state.data_history["health"])        

    except Exception as e:
        st.error(f"Backend not running: {e}")

    time.sleep(refresh_rate)
    st.rerun()