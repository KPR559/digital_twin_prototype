from fastapi import FastAPI,WebSocket
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import joblib
import tensorflow as tf
from realtime_data import stream_data_every_60s
from preprocess import preprocess_live_sample
from sequence_buffer import SequenceBuffer
from stress_indices import compute_stress_indices
from health_score import compute_health_score
from maintance_prediction import get_maintenance_recommendation

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------- CONFIG ----------------
SEQUENCE_LENGTH = 30
RUL_MAX = 130

FEATURE_COLUMNS = [
    "op1", "op2", "op3",
    "s2", "s3", "s4", "s7",
    "s8", "s11", "s12", "s15"
]

# ---------------- GLOBAL STATE ----------------
anomaly_model = None
lstm_model = None
buffer = SequenceBuffer(SEQUENCE_LENGTH)
last_rul = None


# ---------------- STARTUP ----------------
@app.on_event("startup")
def load_models():
    global anomaly_model, lstm_model

    anomaly_model = joblib.load(r"C:\Users\karet\Downloads\backend\model_train\models\anomaly_model.pkl")
    lstm_model = tf.keras.models.load_model(
        r"C:\Users\karet\Downloads\backend\model_train\models\lstm_model.h5",
        compile=False
    )

    print("✅ Models loaded")


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {"message": "AI Digital Twin Backend Running"}


# ---------------- INFERENCE LOGIC ----------------
def run_inference(packet):
    global last_rul

    # 1. Preprocess
    X_scaled = preprocess_live_sample(packet)

    # 2. Anomaly detection
    anomaly_score = anomaly_model.decision_function(X_scaled)[0]
    anomaly_flag = anomaly_model.predict(X_scaled)[0] == -1

    # 3. Add to buffer
    buffer.add(X_scaled[0])
    stress = compute_stress_indices(
        X_scaled[0],
        FEATURE_COLUMNS
    )
    if not buffer.is_ready():
        return {
            "status": "collecting_data",
            "buffer_size": len(buffer.buffer),
            "stress_indices": {k: float(v) for k, v in stress.items()}
        }

    # 4. LSTM RUL prediction
    X_seq = buffer.get_sequence()

    lstm_rul = float(lstm_model.predict(X_seq, verbose=0)[0][0])
    lstm_rul = max(0.0, min(RUL_MAX, lstm_rul))

    # 5. Adaptive decay
    decay = max(1.0, abs(anomaly_score) * 80) if anomaly_flag else 0.5

    if last_rul is None:
        last_rul = lstm_rul

    predicted_rul = min(last_rul - decay, lstm_rul)
    predicted_rul = int(max(0, round(predicted_rul)))

    if predicted_rul == 0:
        return {
            "unit_id": str(packet["unit_id"]),
            "anomaly_score": None,
            "anomaly_detected": True,
            "predicted_rul": 0,
            "stress_indices": {"TSI": None, "MSI": None, "LSI": None, "EDI": None},
            "health_score": 0.0,
            "health_state": "Critical",
            "maintenance_schedule": "Immediate",
            "maintenance_priority": "High",
            "maintenance_action": "Asset Failed - Shut Down"
        }

    last_rul = predicted_rul

    # 6. Stress + health score
    stress = compute_stress_indices(
        X_scaled[0],
        FEATURE_COLUMNS
    )

    health_score, health_state = compute_health_score(
        predicted_rul,
        stress
    )

    # 7. Maintenance recommendation
    maintenance = get_maintenance_recommendation(health_score, anomaly_flag)

    return {
        "unit_id": str(packet["unit_id"]),
        "anomaly_score": float(round(float(anomaly_score), 4)),
        "anomaly_detected": bool(anomaly_flag),
        "predicted_rul": int(predicted_rul),
        "stress_indices": {
            k: float(v) for k, v in stress.items()
        },
        "health_score": float(health_score),
        "health_state": str(health_state),
        "maintenance_schedule": str(maintenance["schedule"]),
        "maintenance_priority": str(maintenance["priority"]),
        "maintenance_action": str(maintenance["action"])
    }


# ---------------- WEBSOCKET (REAL-TIME STREAM) ----------------
@app.websocket("/ws")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()

    print("🔌 Client connected")

    try:
        for packet in stream_data_every_60s():
            result = run_inference(packet)
            await websocket.send_json(result)

            await asyncio.sleep(2)  # small delay

    except Exception as e:
        print("Client disconnected:", e)


# ---------------- REST ENDPOINT (OPTIONAL) ----------------
@app.get("/predict-once")
def predict_once():
    packet = next(stream_data_every_60s())
    return run_inference(packet)