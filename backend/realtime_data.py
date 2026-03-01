import pandas as pd
import numpy as np
import time

# -------------------------------------------------
# LOAD FD002 DATA (FOR STATISTICS ONLY)
# -------------------------------------------------
df = pd.read_csv(r"C:\Digital twin\backend\FD002_full.csv")

FEATURE_COLUMNS = [
    "op1", "op2", "op3",
    "s2", "s3", "s4", "s7",
    "s8", "s11", "s12", "s15"
]

# -------------------------------------------------
# SENSOR STATISTICS
# -------------------------------------------------
sensor_stats = {}
for col in FEATURE_COLUMNS:
    sensor_stats[col] = {
        "mean": df[col].mean(),
        "std": df[col].std(),
        "min": df[col].min(),
        "max": df[col].max(),
    }

# -------------------------------------------------
# SENSOR DEGRADATION DIRECTION
# -------------------------------------------------
sensor_trend = {}
for col in FEATURE_COLUMNS:
    corr = df[[col, "RUL"]].corr().iloc[0, 1]
    sensor_trend[col] = np.sign(corr) if corr != 0 else 1.0

# -------------------------------------------------
# INITIAL ENGINE STATE
# -------------------------------------------------
SIM_UNIT_ID = "ESC_01"
cycle = 0

current_state = {
    col: sensor_stats[col]["mean"]
    for col in FEATURE_COLUMNS
}

# -------------------------------------------------
# LIVE STREAM GENERATOR
# -------------------------------------------------
def stream_data_every_60s():
    global cycle, current_state

    while True:
        cycle += 1
        packet = {"unit_id": SIM_UNIT_ID}

        degradation_factor = min(1.0, cycle / 40)

        for col in FEATURE_COLUMNS:
            stats = sensor_stats[col]
            sigma = stats["std"]

            # Directional degradation
            drift = sensor_trend[col] * degradation_factor * 0.4 * sigma
            noise = np.random.normal(0, 0.01 * sigma)

            value = current_state[col] + drift + noise

            # 🔥 SOFT BOUNDING (NO FREEZE)
            if value < stats["min"]:
                value = stats["min"] + abs(np.random.normal(0, 0.01 * sigma))
            elif value > stats["max"]:
                value = stats["max"] - abs(np.random.normal(0, 0.01 * sigma))

            current_state[col] = value
            packet[col] = float(value)

        yield packet
        time.sleep(1)  # 1 sec for testing (60 sec in production)