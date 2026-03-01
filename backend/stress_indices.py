# backend/condition_monitoring/stress_indices.py

def compute_stress_indices(packet_scaled, feature_columns):
    """
    packet_scaled: 1D numpy array (scaled sensor values)
    feature_columns: list of feature names in correct order
    """

    data = dict(zip(feature_columns, packet_scaled))

    # Stress indices (0 = healthy, 1 = stressed)
    stress = {
        "TSI": data["s2"],  # thermal stress
        "MSI": (data["s7"] + data["s15"] + data["s3"]) / 3,  # mechanical
        "LSI": (data["s8"] + data["op1"] + data["op2"]) / 3, # load
        "EDI": (data["s11"] + data["s12"]) / 2              # efficiency
    }

    return stress