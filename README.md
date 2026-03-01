# 🏗️ Digital Twin of an Asset -- AI-Based Predictive Maintenance System

## 📌 Overview

The **Asset Digital Twin (Prototype Demonstrated Using an Escalator Asset)** 
is an AI-powered virtual replica of an escalator that monitors asset health, 
detects anomalies, predicts Remaining Useful Life (RUL), and provides maintenance 
recommendations in real time.

This project demonstrates how AI + Digital Twin technology can enable 
**predictive maintenance** instead of reactive maintenance.

------------------------------------------------------------------------

## 🎯 Key Features

-   Real-time sensor data simulation
-   Anomaly detection using Machine Learning
-   LSTM-based Remaining Useful Life (RUL) prediction
-   Stress index computation (TSI, MSI, LSI, EDI)
-   Health score calculation
-   Maintenance recommendation engine
-   3D Digital Twin visualization (Three.js)
-   Real-time monitoring dashboard (Streamlit)
-   Automatic failure shutdown logic

------------------------------------------------------------------------

## 🏗️ System Architecture

The system consists of three major components:

### 1️⃣ AI Backend (FastAPI)

-   Simulates real-time sensor data
-   Runs Isolation Forest (Anomaly Detection)
-   Runs LSTM Model (RUL Prediction)
-   Computes Stress Indices and Health Score
-   Generates maintenance recommendations

### 2️⃣ 3D Digital Twin (Three.js)

-   Real-time 3D asset model
-   Color changes based on health:
    -   🟢 Healthy
    -   🟡 Warning
    -   🟠 Degrading
    -   🔴 Critical
-   Stops animation automatically when RUL = 0

### 3️⃣ Monitoring Dashboard (Streamlit)

Displays:

-   Health Score
-   Predicted RUL
-   Anomaly Score
-   Stress Indices
-   Maintenance Recommendations
-   Real-Time Trend Graphs

------------------------------------------------------------------------

## 🧠 AI Workflow

1.  Sensor data simulation
2.  Data preprocessing
3.  Anomaly detection
4.  Sequence buffering
5.  LSTM-based RUL prediction
6.  Stress index computation
7.  Health scoring
8.  Maintenance recommendation
9.  Digital twin visualization update

------------------------------------------------------------------------

## 🛠️ Technology Stack

### Backend

-   Python
-   FastAPI
-   TensorFlow / Keras
-   Scikit-learn
-   Joblib

### Dashboard

-   Streamlit
-   Pandas

### 3D Visualization

-   Three.js
-   GLTFLoader
-   OrbitControls

------------------------------------------------------------------------

## 📂 Project Structure

    Escalator-Digital-Twin/
    │
    ├── backend/
    │   ├── main.py
    │   ├── realtime_data.py
    │   ├── preprocess.py
    │   ├── sequence_buffer.py
    │   ├── stress_indices.py
    │   ├── health_score.py
    │   ├── maintance_prediction.py
    │   └── models/
    │       ├── anomaly_model.pkl
    │       └── lstm_model.h5
    │
    ├── frontend/
    │   ├── dashboard.py
    │   └── 3d_viewer/
    │       ├── index.html
    │       └── escalator.glb
    │
    └── README.md

------------------------------------------------------------------------

## 🚀 How to Run the Project

### Step 1: Start Backend

``` bash
cd backend
uvicorn main:app --reload
```

Backend runs at: http://127.0.0.1:8000

------------------------------------------------------------------------

### Step 2: Start 3D Viewer

``` bash
live-server
```

Runs at: http://127.0.0.1:8080

------------------------------------------------------------------------

### Step 3: Start Dashboard

``` bash
cd frontend
streamlit run dashboard.py
```

Runs at: http://localhost:8501

------------------------------------------------------------------------

## ⚠️ Failure Behavior

When predicted RUL reaches 0:

-   Health score becomes 0
-   Health state becomes "Critical"
-   3D asset stops
-   Maintenance priority becomes "High"
-   Monitoring halts automatically

------------------------------------------------------------------------

## 🔮 Future Enhancements

-   IoT sensor integration
-   Database storage
-   Multi-asset support
-   Cloud deployment
-   Email/SMS alerts
-   Historical analytics dashboard

------------------------------------------------------------------------

## 📌 Applications

-   Elevators
-   Pumps
-   Turbines
-   Motors
-   Smart infrastructure systems
-   Manufacturing equipment

------------------------------------------------------------------------

