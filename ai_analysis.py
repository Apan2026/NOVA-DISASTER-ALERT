# NOVA Disaster Alert - Data Based Risk Analysis

from datetime import datetime, timezone


RISK_SCORE = {
    "INFO": 0,
    "LOW": 1,
    "MODERATE": 2,
    "HIGH": 3,
    "EXTREME": 4,
    "UNKNOWN": -1
}


def make_result(level, message, reasons=None):
    """Create a standard risk result."""

    return {
        "level": level,
        "message": message,
        "reasons": reasons or []
    }


# ==========================================
# WEATHER RISK
# ==========================================

def analyze_weather(weather):
    """
    Analyze actual weather data.

    No data = UNKNOWN.
    The function does not guess missing information.
    """

    if not weather:
        return make_result(
            "UNKNOWN",
            "No weather data available."
        )

    if "error" in weather:
        return make_result(
            "UNKNOWN",
            "Weather data could not be verified."
        )

    required_fields = [
        "temperature",
        "wind_speed",
        "condition"
    ]

    for field in required_fields:

        if field not in weather:
            return make_result(
                "UNKNOWN",
                f"Missing weather data: {field}"
            )

    try:
        temperature = float(weather["temperature"])
        wind_speed = float(weather["wind_speed"])
        condition = str(
            weather["condition"]
        ).lower()

    except (ValueError, TypeError):

        return make_result(
            "UNKNOWN",
            "Invalid weather data."
        )

    risks = []
    reasons = []

    # --------------------------------------
    # Wind
    # --------------------------------------

    if wind_speed >= 80:

        risks.append("EXTREME")
        reasons.append(
            f"Very strong wind: {wind_speed} km/h"
        )

    elif wind_speed >= 60:

        risks.append("HIGH")
        reasons.append(
            f"Strong wind: {wind_speed} km/h"
        )

    elif wind_speed >= 40:

        risks.append("MODERATE")
        reasons.append(
            f"Elevated wind: {wind_speed} km/h"
        )

    # --------------------------------------
    # Weather condition
    # --------------------------------------

    if "thunderstorm" in condition:

        risks.append("HIGH")
        reasons.append(
            "Thunderstorm reported by weather source."
        )

    elif "heavy rain" in condition:

        risks.append("HIGH")
        reasons.append(
            "Heavy rain reported by weather source."
        )

    elif "rain" in condition:

        risks.append("MODERATE")
        reasons.append(
            "Rain reported by weather source."
        )

    # --------------------------------------
    # Temperature
    # --------------------------------------

    if temperature >= 40:

        risks.append("HIGH")
        reasons.append(
            f"Very high temperature: {temperature} °C"
        )

    elif temperature <= 5:

        risks.append("HIGH")
        reasons.append(
            f"Very low temperature: {temperature} °C"
        )

    # --------------------------------------
    # Final weather risk
    # --------------------------------------

    if not risks:

        return make_result(
            "LOW",
            "No configured severe weather condition detected.",
            ["Current weather data does not meet alert thresholds."]
        )

    highest_risk = max(
        risks,
        key=lambda x: RISK_SCORE[x]
    )

    return make_result(
        highest_risk,
        "Risk based on current weather data.",
        reasons
    )


# ==========================================
# EARTHQUAKE RISK
# ==========================================

def analyze_earthquake(magnitude):
    """
    Analyze an already detected earthquake.

    This does NOT predict earthquakes.
    """

    if magnitude is None:

        return make_result(
            "UNKNOWN",
            "Earthquake magnitude is unavailable."
        )

    try:
        magnitude = float(magnitude)

    except (ValueError, TypeError):

        return make_result(
            "UNKNOWN",
            "Invalid earthquake magnitude."
        )

    if magnitude >= 7.0:

        return make_result(
            "EXTREME",
            "Very large earthquake detected.",
            [f"Magnitude: {magnitude}"]
        )

    elif magnitude >= 6.0:

        return make_result(
            "HIGH",
            "Large earthquake detected.",
            [f"Magnitude: {magnitude}"]
        )

    elif magnitude >= 5.0:

        return make_result(
            "MODERATE",
            "Moderate earthquake detected.",
            [f"Magnitude: {magnitude}"]
        )

    elif magnitude >= 4.0:

        return make_result(
            "LOW",
            "Small earthquake detected.",
            [f"Magnitude: {magnitude}"]
        )

    else:

        return make_result(
            "INFO",
            "Small earthquake detected.",
            [f"Magnitude: {magnitude}"]
        )


# ==========================================
# OVERALL RISK
# ==========================================

def get_overall_risk(
    weather_result,
    earthquake_result
):
    """
    Combine verified weather and earthquake results.
    """

    levels = []

    if weather_result:
        levels.append(
            weather_result.get(
                "level",
                "UNKNOWN"
            )
        )

    if earthquake_result:
        levels.append(
            earthquake_result.get(
                "level",
                "UNKNOWN"
            )
        )

    valid_levels = [
        level
        for level in levels
        if level in RISK_SCORE
        and level != "UNKNOWN"
    ]

    # No verified information
    if not valid_levels:

        return make_result(
            "UNKNOWN",
            "There is not enough verified data to calculate overall risk."
        )

    highest = max(
        valid_levels,
        key=lambda x: RISK_SCORE[x]
    )

    return make_result(
        highest,
        "Overall risk based on available verified data.",
        valid_levels
    )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_weather = {
        "temperature": 31,
        "wind_speed": 12,
        "condition": "Clear"
    }

    weather_result = analyze_weather(
        test_weather
    )

    print("\nNOVA WEATHER RISK")
    print("----------------------")
    print(
        "Level:",
        weather_result["level"]
    )
    print(
        "Message:",
        weather_result["message"]
    )

    for reason in weather_result["reasons"]:
        print("-", reason)


    earthquake_result = analyze_earthquake(
        3.2
    )

    print("\nNOVA EARTHQUAKE RISK")
    print("----------------------")
    print(
        "Level:",
        earthquake_result["level"]
    )
    print(
        "Message:",
        earthquake_result["message"]
    )

    for reason in earthquake_result["reasons"]:
        print("-", reason)


    overall = get_overall_risk(
        weather_result,
        earthquake_result
    )

    print("\nNOVA OVERALL RISK")
    print("----------------------")
    print(
        "Level:",
        overall["level"]
    )
    print(
        "Message:",
        overall["message"]
    )
    