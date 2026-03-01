# backend/condition_monitoring/health_score.py

def compute_health_score(predicted_rul, stress, rul_max=130):
    """
    predicted_rul: float
    stress: dict with TSI, MSI, LSI, EDI
    """

    # Normalize RUL
    rul_norm = min(predicted_rul, rul_max) / rul_max

    health_score = 100 * (
        0.40 * rul_norm +
        0.25 * (1 - stress["MSI"]) +
        0.15 * (1 - stress["TSI"]) +
        0.10 * (1 - stress["EDI"]) +
        0.10 * (1 - stress["LSI"])
    )

    if health_score >= 80:
        state = "Healthy"
    elif health_score >= 60:
        state = "Warning"
    elif health_score >= 40:
        state = "Degrading"
    else:
        state = "Critical"

    return round(health_score, 2), state