import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# ---------------- FLIGHTS ----------------
def search_flight(source, destination):
    with open(DATA_DIR / "flights.json") as f:
        flights = json.load(f)

    matches = [
        f for f in flights
        if f["from"].lower() == source.lower()
        and f["to"].lower() == destination.lower()
    ]

    if not matches:
        return None

    return min(matches, key=lambda x: x["price"])


# ---------------- HOTELS ----------------
def recommend_hotel(city, min_rating, days):
    with open(DATA_DIR / "hotels.json") as f:
        hotels = json.load(f)

    matches = [
        h for h in hotels
        if h["city"].lower() == city.lower()
        and h["stars"] >= min_rating
    ]

    if not matches:
        return None

    hotel = min(matches, key=lambda x: x["price_per_night"])
    hotel["total_cost"] = hotel["price_per_night"] * days
    return hotel


# ---------------- PLACES ----------------
def get_itinerary(city, days):
    with open(DATA_DIR / "places.json") as f:
        places = json.load(f)

    city_places = [p for p in places if p["city"].lower() == city.lower()]
    city_places.sort(key=lambda x: x["rating"], reverse=True)

    itinerary = []
    idx = 0

    for day in range(1, days + 1):
        day_places = city_places[idx:idx + 2]
        itinerary.append({
            "day": f"Day {day}",
            "activities": [p["name"] for p in day_places]
        })
        idx += 2

    return itinerary


# ---------------- WEATHER (REAL API) ----------------
def get_weather(lat, lon, days):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,weathercode"
        f"&timezone=auto"
    )

    res = requests.get(url).json()

    weather = []
    for i in range(days):
        temp = res["daily"]["temperature_2m_max"][i]
        code = res["daily"]["weathercode"][i]

        weather.append({
            "day": f"Day {i+1}",
            "description": map_weather(code, temp)
        })

    return weather


def map_weather(code, temp):
    if code in [0, 1]:
        return f"Sunny ({temp}°C)"
    elif code in [2, 3]:
        return f"Partly Cloudy ({temp}°C)"
    elif code in [45, 48]:
        return f"Foggy ({temp}°C)"
    elif code in [51, 61, 80]:
        return f"Rainy ({temp}°C)"
    else:
        return f"Pleasant ({temp}°C)"
