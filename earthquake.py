# NOVA Disaster Alert
# STEP 12 - Fast Worldwide Earthquake Monitor

import requests
import math
from datetime import datetime, timezone


USGS_URL = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query"
    "?format=geojson"
    "&orderby=time"
    "&limit=50"
)


DHAKA_LAT = 23.8103
DHAKA_LON = 90.4125


def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    radius = 6371.0

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = math.radians(
        lat2 - lat1
    )

    dlon = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return radius * c


def get_earthquakes():

    try:

        response = requests.get(
            USGS_URL,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        earthquakes = []

        for event in data.get(
            "features",
            []
        ):

            properties = event.get(
                "properties",
                {}
            )

            geometry = event.get(
                "geometry",
                {}
            )

            coordinates = geometry.get(
                "coordinates",
                []
            )

            if len(coordinates) < 3:
                continue

            longitude = coordinates[0]
            latitude = coordinates[1]
            depth = coordinates[2]

            magnitude = properties.get(
                "mag"
            )

            place = properties.get(
                "place",
                "Unknown"
            )

            timestamp = properties.get(
                "time"
            )

            # ------------------------------
            # Distance from Dhaka
            # ------------------------------

            distance = calculate_distance(
                DHAKA_LAT,
                DHAKA_LON,
                latitude,
                longitude
            )

            # ------------------------------
            # Time
            # ------------------------------

            if timestamp:

                event_time = datetime.fromtimestamp(
                    timestamp / 1000,
                    tz=timezone.utc
                )

                formatted_time = event_time.strftime(
                    "%Y-%m-%d %H:%M:%S UTC"
                )

            else:

                formatted_time = "Unknown"

            # ------------------------------
            # Earthquake data
            # ------------------------------

            earthquakes.append({

                "country": "Not determined",

                "place": place,

                "magnitude": magnitude,

                "latitude": latitude,

                "longitude": longitude,

                "depth": depth,

                "distance_from_dhaka": distance,

                "time": formatted_time

            })

        return earthquakes

    except Exception as error:

        return {
            "error": str(error)
        }


def show_earthquakes():

    result = get_earthquakes()

    if isinstance(
        result,
        dict
    ):

        print(
            "Earthquake Error:",
            result["error"]
        )

        return

    print()
    print("=" * 70)
    print(
        "       NOVA WORLDWIDE EARTHQUAKE MONITOR"
    )
    print("=" * 70)

    print(
        f"Showing latest {len(result)} "
        "worldwide earthquakes."
    )

    for number, earthquake in enumerate(
        result,
        start=1
    ):

        print()
        print(
            f"EARTHQUAKE #{number}"
        )

        print("-" * 70)

        print(
            "Location:",
            earthquake["place"]
        )

        print(
            "Magnitude:",
            earthquake["magnitude"]
        )

        print(
            "Depth:",
            earthquake["depth"],
            "km"
        )

        print(
            "Distance from Dhaka:",
            round(
                earthquake[
                    "distance_from_dhaka"
                ],
                1
            ),
            "km"
        )

        print(
            "Coordinates:",
            earthquake["latitude"],
            earthquake["longitude"]
        )

        print(
            "Time:",
            earthquake["time"]
        )

    print()
    print("=" * 70)


if __name__ == "__main__":

    show_earthquakes()
    