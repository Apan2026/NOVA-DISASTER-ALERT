# NOVA Disaster Alert - Weather Module

import requests


def get_weather(city):
    """
    Gets basic current weather information for a city.
    """

    url = "https://wttr.in/"

    try:
        response = requests.get(
            f"{url}{city}?format=j1",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        current = data["current_condition"][0]

        weather = {
            "city": city,
            "temperature": current["temp_C"],
            "feels_like": current["FeelsLikeC"],
            "humidity": current["humidity"],
            "wind_speed": current["windspeedKmph"],
            "wind_direction": current["winddir16Point"],
            "condition": current["weatherDesc"][0]["value"],
            "visibility": current["visibility"],
            "pressure": current["pressure"],
        }

        return weather

    except Exception as error:
        return {
            "error": str(error)
        }


if __name__ == "__main__":
    result = get_weather("Dhaka")

    if "error" in result:
        print("Weather Error:", result["error"])
    else:
        print("Weather information:")
        print("---------------------")
        print("City:", result["city"])
        print("Temperature:", result["temperature"], "°C")
        print("Feels Like:", result["feels_like"], "°C")
        print("Humidity:", result["humidity"], "%")
        print("Wind:", result["wind_speed"], "km/h")
        print("Direction:", result["wind_direction"])
        print("Condition:", result["condition"])
        print("Visibility:", result["visibility"], "km")
        print("Pressure:", result["pressure"], "hPa")
        