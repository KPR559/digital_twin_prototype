import numpy as np
import joblib

FEATURE_COLUMNS = [
    "op1", "op2", "op3",
    "s2", "s3", "s4", "s7",
    "s8", "s11", "s12", "s15"
]

scaler = joblib.load(
    r"C:\Digital twin\backend\scaler.pkl"
)

def preprocess_live_sample(packet):
    X = np.array([[packet[col] for col in FEATURE_COLUMNS]])
    X_scaled = scaler.transform(X)
    return X_scaled