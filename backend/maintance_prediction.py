# Generate maintenance recommendation
def get_maintenance_recommendation(health_score, failure_risk):

    if failure_risk == "True" or health_score < 40:
        return {
            "priority": "High",
            "action": "Immediate maintenance required",
            "schedule": "Within 24 hours"
        }

    elif health_score < 70:
        return {
            "priority": "Medium",
            "action": "Schedule maintenance",
            "schedule": "Within 7 days"
        }

    else:
        return {
            "priority": "Low",
            "action": "Routine inspection",
            "schedule": "Next monthly check"
        }