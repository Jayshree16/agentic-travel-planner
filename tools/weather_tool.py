# agent/tools.py
import requests
from langchain.tools import Tool

# City → Coordinates (REQUIRED for Open-Meteo)
CITY_COORDINATES = {
    "Goa": (15.2993, 74.1240),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Jaipur": (26.9124, 75.7873)
}

# Weather code mapping → Human readable
WEATHER_CODE_MAP = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Depositing rime fog 🌫️",
    51: "Light drizzle 🌦️",
    61: "Light rain 🌧️",
    63: "Moderate rain 🌧️",
    80: "Rain showers 🌧️",
    95: "Thunderstorm ⛈️"
}

def get_weather_forecast(city: str, days: int):
    """Fetch real-time weather forecast using Open-Meteo API"""

    if city not in CITY_COORDINATES:
        return {"error": "Weather not available for this city"}

    latitude, longitude = CITY_COORDINATES[city]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&daily=temperature_2m_max,weathercode"
        "&timezone=auto"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    forecasts = []
    codes = data["daily"]["weathercode"]
    temps = data["daily"]["temperature_2m_max"]

    for i in range(min(days, len(temps))):
        forecasts.append({
            "day": f"Day {i+1}",
            "max_temp": f"{temps[i]}°C",
            "condition": WEATHER_CODE_MAP.get(codes[i], "Unknown")
        })

    # Human-readable summary
    summary = "Mostly pleasant weather, suitable for sightseeing and outdoor activities."

    return {
        "city": city,
        "summary": summary,
        "forecast": forecasts
    }

weather_tool = Tool(
    name="Weather Lookup Tool",
    description="Fetches real-time weather forecast with readable conditions for a city",
    func=get_weather_forecast
)
