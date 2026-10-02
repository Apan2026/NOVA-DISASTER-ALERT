from flask import Flask, request, render_template_string

from weather import get_weather
from earthquake import get_earthquakes
from ai_analysis import (
    analyze_weather,
    analyze_earthquake,
    get_overall_risk
)


app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html>

<head>

    <title>NOVA Disaster Alert</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #08111f;
            color: white;
        }

        header {
            background: #0f1d32;
            padding: 25px;
            text-align: center;
            border-bottom: 1px solid #24344d;
        }

        header h1 {
            margin: 0;
            color: #38bdf8;
            font-size: 32px;
        }

        header p {
            color: #94a3b8;
            margin-bottom: 0;
        }

        .container {
            max-width: 1200px;
            margin: auto;
            padding: 25px;
        }

        .search {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }

        input {
            flex: 1;
            padding: 14px;
            border-radius: 8px;
            border: 1px solid #334155;
            background: #111d30;
            color: white;
            font-size: 16px;
        }

        button {
            padding: 14px 22px;
            border: none;
            border-radius: 8px;
            background: #0284c7;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #0369a1;
        }

        .cards {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-top: 25px;
        }

        .card {
            background: #111d30;
            border: 1px solid #26364f;
            border-radius: 12px;
            padding: 22px;
        }

        .card h3 {
            color: #94a3b8;
            margin-top: 0;
        }

        .value {
            font-size: 28px;
            font-weight: bold;
        }

        .section {
            margin-top: 25px;
        }

        .earthquake {
            background: #0b1729;
            border: 1px solid #26364f;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }

        .risk {
            color: #facc15;
        }

        .error {
            background: #451a1a;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .search-title {
            color: #cbd5e1;
            margin-top: 25px;
            margin-bottom: 8px;
        }

        .location-info {
            color: #94a3b8;
            margin-top: 8px;
        }

        footer {
            text-align: center;
            color: #64748b;
            padding: 30px;
        }

        @media (max-width: 650px) {

            .search {
                flex-direction: column;
            }

            button {
                width: 100%;
            }

            header h1 {
                font-size: 26px;
            }

            .container {
                padding: 15px;
            }

        }

    </style>

</head>


<body>


<header>

    <h1>NOVA</h1>

    <p>
        DISASTER ALERT SYSTEM
    </p>

</header>


<div class="container">


    <!-- WEATHER SEARCH -->

    <div class="search-title">
        Weather Location
    </div>

    <form class="search" method="get">

        <input
            type="text"
            name="city"
            value="{{ city }}"
            placeholder="Enter city"
        >

        <input
            type="hidden"
            name="country"
            value="{{ country }}"
        >

        <button type="submit">
            WEATHER
        </button>

    </form>


    <!-- EARTHQUAKE SEARCH -->

    <div class="search-title">
        Earthquake Country / Location Search
    </div>

    <form class="search" method="get">

        <input
            type="text"
            name="country"
            value="{{ country }}"
            placeholder="Example: Japan, Indonesia, Philippines"
        >

        <input
            type="hidden"
            name="city"
            value="{{ city }}"
        >

        <button type="submit">
            SEARCH EARTHQUAKE
        </button>

    </form>


    {% if error %}

        <div class="error">
            Weather Error: {{ error }}
        </div>

    {% else %}


        <!-- WEATHER CARDS -->

        <div class="cards">


            <div class="card">

                <h3>
                    TEMPERATURE
                </h3>

                <div class="value">
                    {{ weather.temperature }} °C
                </div>

            </div>


            <div class="card">

                <h3>
                    CONDITION
                </h3>

                <div class="value">
                    {{ weather.condition }}
                </div>

            </div>


            <div class="card">

                <h3>
                    HUMIDITY
                </h3>

                <div class="value">
                    {{ weather.humidity }}%
                </div>

            </div>


            <div class="card">

                <h3>
                    WIND
                </h3>

                <div class="value">
                    {{ weather.wind_speed }}
                    km/h
                </div>

            </div>


        </div>


        <!-- WEATHER DETAILS -->

        <div class="section">

            <div class="card">

                <h2>
                    Weather Details
                </h2>

                <p>
                    City:
                    <b>{{ city }}</b>
                </p>

                <p>
                    Feels Like:
                    {{ weather.feels_like }} °C
                </p>

                <p>
                    Wind Direction:
                    {{ weather.wind_direction }}
                </p>

                <p>
                    Visibility:
                    {{ weather.visibility }} km
                </p>

                <p>
                    Pressure:
                    {{ weather.pressure }} hPa
                </p>

            </div>

        </div>


        <!-- WEATHER RISK -->

        <div class="section">

            <div class="card">

                <h2>
                    Weather Risk
                </h2>

                <div class="value risk">
                    {{ weather_result.level }}
                </div>

                <p>
                    {{ weather_result.message }}
                </p>

                {% if weather_result.reasons %}

                    {% for reason in weather_result.reasons %}

                        <p>
                            • {{ reason }}
                        </p>

                    {% endfor %}

                {% endif %}

            </div>

        </div>


        <!-- EARTHQUAKES -->

        <div class="section">

            <div class="card">

                <h2>
                    Latest Earthquakes
                </h2>


                {% if country %}

                    <p class="location-info">
                        Search:
                        <b>{{ country }}</b>
                    </p>

                {% endif %}


                {% if earthquakes %}


                    {% for earthquake in earthquakes %}

                        <div class="earthquake">

                            <b>
                                Magnitude:
                                M {{ earthquake.magnitude }}
                            </b>

                            <br><br>

                            Location:
                            {{ earthquake.place }}

                            <br>

                            Depth:
                            {{ earthquake.depth }} km

                            <br>

                            Distance from Dhaka:
                            {{
                                "%.1f"|format(
                                    earthquake.distance_from_dhaka
                                )
                            }}
                            km

                            <br>

                            Coordinates:
                            {{ earthquake.latitude }},
                            {{ earthquake.longitude }}

                            <br>

                            Time:
                            {{ earthquake.time }}

                        </div>

                    {% endfor %}


                {% else %}

                    <p>
                        No matching earthquake data found.
                    </p>

                {% endif %}


            </div>

        </div>


        <!-- EARTHQUAKE RISK -->

        {% if earthquake_result %}

            <div class="section">

                <div class="card">

                    <h2>
                        Earthquake Risk
                    </h2>

                    <div class="value risk">
                        {{ earthquake_result.level }}
                    </div>

                    <p>
                        {{ earthquake_result.message }}
                    </p>

                </div>

            </div>

        {% endif %}


        <!-- OVERALL RISK -->

        <div class="section">

            <div class="card">

                <h2>
                    Overall Risk
                </h2>

                <div class="value risk">
                    {{ overall.level }}
                </div>

                <p>
                    {{ overall.message }}
                </p>

            </div>

        </div>


    {% endif %}


</div>


<footer>

    NOVA Disaster Alert © 2026

</footer>


</body>

</html>
"""


@app.route("/")
def home():

    city = request.args.get(
        "city",
        "Dhaka"
    ).strip()


    country = request.args.get(
        "country",
        ""
    ).strip()


    # -----------------------------
    # WEATHER
    # -----------------------------

    weather = get_weather(
        city
    )


    if "error" in weather:

        return render_template_string(
            HTML,

            city=city,

            country=country,

            weather=None,

            weather_result=None,

            earthquakes=[],

            earthquake_result=None,

            overall=None,

            error=weather["error"]
        )


    weather_result = analyze_weather(
        weather
    )


    # -----------------------------
    # EARTHQUAKES
    # -----------------------------

    earthquake_data = get_earthquakes()

    earthquake_result = None


    if isinstance(
        earthquake_data,
        list
    ):

        valid = [

            earthquake

            for earthquake in earthquake_data

            if earthquake["magnitude"] is not None

        ]


        # Country / location search

        if country:

            search_text = country.lower()

            valid = [

                earthquake

                for earthquake in valid

                if search_text
                in earthquake["place"].lower()

            ]


        # Strongest earthquake

        if valid:

            strongest = max(

                valid,

                key=lambda earthquake:
                earthquake["magnitude"]

            )


            earthquake_result = analyze_earthquake(

                strongest["magnitude"]

            )


        earthquakes = valid[:10]


    else:

        earthquakes = []


    # -----------------------------
    # OVERALL RISK
    # -----------------------------

    overall = get_overall_risk(

        weather_result,

        earthquake_result

    )


    # -----------------------------
    # WEBSITE
    # -----------------------------

    return render_template_string(

        HTML,

        city=city,

        country=country,

        weather=weather,

        weather_result=weather_result,

        earthquakes=earthquakes,

        earthquake_result=earthquake_result,

        overall=overall,

        error=None

    )


if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
    