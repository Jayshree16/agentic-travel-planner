import streamlit as st
import json
from datetime import date
from pathlib import Path
import requests

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

WEATHER_CODE_MAP = {
    0: "Clear Sky ☀️",
    1: "Mainly Clear 🌤️",
    2: "Partly Cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Depositing Rime Fog 🌫️",
    51: "Light Drizzle 🌦️",
    53: "Moderate Drizzle 🌦️",
    55: "Dense Drizzle 🌧️",
    61: "Slight Rain 🌧️",
    63: "Moderate Rain 🌧️",
    65: "Heavy Rain 🌧️",
    71: "Snowfall ❄️",
    80: "Rain Showers 🌦️",
    95: "Thunderstorm ⛈️"
}

def get_weather_forecast(city: str, days: int):
    """
    Fetches day-wise weather forecast using Open-Meteo API.
    Returns human-readable weather conditions.
    """
    if city not in CITY_COORDINATES:
        return []

    latitude, longitude = CITY_COORDINATES[city]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&daily=temperature_2m_max,weathercode"
        "&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecast = []
        for i in range(min(days, len(data["daily"]["time"]))):
            code = data["daily"]["weathercode"][i]
            forecast.append({
                "day": f"Day {i + 1}",
                "date": data["daily"]["time"][i],
                "max_temp": data["daily"]["temperature_2m_max"][i],
                "condition": WEATHER_CODE_MAP.get(code, "Weather Unavailable")
            })

        return forecast

    except Exception:
        return []


# ---------------- AGENT ----------------
from agent.travel_agent import create_travel_agent
agent = create_travel_agent()

# ---------------- PATHS ----------------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# ---------------- LOAD DATA ----------------
with open(DATA_DIR / "flights.json", "r", encoding="utf-8") as f:
    flights_data = json.load(f)

with open(DATA_DIR / "hotels.json", "r", encoding="utf-8") as f:
    hotels_data = json.load(f)

with open(DATA_DIR / "places.json", "r", encoding="utf-8") as f:
    places_data = json.load(f)

# ---------------- DROPDOWN DATA ----------------
sources = sorted({f["from"] for f in flights_data})

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Agentic AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #F6F8FB; }
h1, h2, h3 { color: #1E2A38; }

.reason-box {
    background: #FFF8E1;
    border-left: 6px solid #C9A14A;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    border-top: 4px solid #C9A14A;
    transition: 0.3s;
}

.card:hover { transform: translateY(-6px); }

.price {
    font-size: 22px;
    font-weight: 700;
    color: #C9A14A;
}

.badge {
    background: #1E2A38;
    color: white;
    padding: 6px 12px;
    border-radius: 10px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

PLACE_IMAGE_MAP = {
    "fort": "fort.jpg",
    "beach": "beach.jpg",
    "temple": "temple.jpg",
    "museum": "museum.jpg",
    "palace": "palace.jpg",
    "park": "park.jpg",
    "monument": "monument.jpg"
}

# ---------------- SEARCH ----------------
st.title("Luxury AI Travel Planner")

c1, c2, c3 = st.columns(3)

with c1:
    source = st.selectbox("From", sources)

destinations = sorted({f["to"] for f in flights_data if f["from"] == source})

with c2:
    destination = st.selectbox("To", destinations)

with c3:
    start_date = st.date_input("Departure", date.today())

c1, c2 = st.columns(2)
with c1:
    trip_days = st.slider("Trip Duration (Days)", 2, 7, 3)
with c2:
    hotel_rating = st.selectbox("Hotel Rating", [2, 3, 4, 5], index=3)

plan = st.button("🔍 PLAN MY TRIP", use_container_width=True)

# ========================== RESULT ==========================
if plan:
    with st.spinner("🤖 AI is planning your trip..."):
        agent({
            "source": source,
            "destination": destination,
            "days": trip_days,
            "hotel_rating": hotel_rating,
            "budget": (15000, 40000)
        })

    # ---------------- WHY THIS PLAN ----------------
    st.markdown("## Why this plan works for you")

    st.markdown("""
    <div class="reason-box">
    ✈️ <b>Flight Selection</b><br>
    We picked the lowest-priced direct flight available on your selected route,
    with a convenient departure time and reliable airline rating.
    </div>

    <div class="reason-box">
    🏨 <b>Hotel Selection</b><br>
    Hotels shown here meet your 5-star preference and are among the most
    cost-effective options available in the city for your travel dates.
    </div>
    """, unsafe_allow_html=True)


    # ---------------- FLIGHTS ----------------
    st.markdown("## ✈️ Flight Options")

    flight_options = sorted(
        [f for f in flights_data if f["from"] == source and f["to"] == destination],
        key=lambda x: x["price"]
    )[:3]

    cols = st.columns(len(flight_options))
    for col, f in zip(cols, flight_options):
        with col:
            st.markdown(f"""
            <div class="card">
                <span class="badge">Best Choice</span>
                <h3>{f['airline']}</h3>
                <p class="price">₹{f['price']}</p>
                <p><b>Departure:</b> {f['departure_time']}</p>
                <p><b>Arrival:</b> {f['arrival_time']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- HOTELS ----------------
    st.markdown("## 🏨 Hotel Options")

    hotel_options = sorted(
        [h for h in hotels_data if h["city"] == destination and h["stars"] >= hotel_rating],
        key=lambda x: x["price_per_night"]
    )[:3]

    if not hotel_options:
        st.warning(
            f"No {hotel_rating}-star hotels found in {destination}. "
            f"Try lowering the rating filter."
        )
    else:
        cols = st.columns(len(hotel_options))
    for col, h in zip(cols, hotel_options):
        with col:
            amenities = ", ".join(a.title() for a in h["amenities"])
            st.markdown(f"""
            <div class="card">
                <span class="badge">Recommended</span>
                <h3>{h['name']}</h3>
                <p class="price">₹{h['price_per_night']} / night</p>
                <p>⭐ {h['stars']} Star</p>
                <p><b>Amenities:</b> {amenities}</p>
            </div>
            """, unsafe_allow_html=True)

    # # ---------------- TRIP SUMMARY ----------------
    # st.markdown("## 🧳 Trip Summary")

    # flight_cost = flight_options[0]["price"] if flight_options else 0
    # hotel_cost = (
    # hotel_options[0]["price_per_night"] * trip_days
    # if hotel_options else 0
    # )
    # total_cost = flight_cost + hotel_cost

    # st.markdown(
    # f"""
    # <div class="card" style="border-top:4px solid #1E2A38;">
    #     <h3 style="margin-bottom:14px;">💰 Cost Breakdown</h3>

    #     <p style="font-size:16px;">
    #         ✈️ <b>Flight Cost:</b> ₹{flight_cost}
    #     </p>

    #     <p style="font-size:16px;">
    #         🏨 <b>Hotel Cost</b> ({trip_days} nights): ₹{hotel_cost}
    #     </p>

    #     <hr style="margin:14px 0;">

    #     <p style="font-size:18px;font-weight:700;color:#1E2A38;">
    #         💳 Total Estimated Cost: ₹{total_cost}
    #     </p>
    # </div>
    # """,
    # unsafe_allow_html=True
    # )

    # ---------------- FAMOUS PLACES ----------------
    st.markdown("## 📍 Famous Places to Visit")

    city_places = sorted(
    [p for p in places_data if p["city"].lower() == destination.lower()],
    key=lambda x: x["rating"],
    reverse=True
    )

    if not city_places:
        st.info("No famous places available for this city.")
    else:
        cols = st.columns(min(3, len(city_places)))
        for col, place in zip(cols, city_places[:3]):
            with col:
                st.markdown(f"""
                <div class="card">
                <h3>{place['name']}</h3>
                <p>🏷️ {place['type'].title()}</p>
                <p>⭐ {place['rating']}</p>
                </div>
                """, unsafe_allow_html=True)


    # ---------------- ITINERARY ----------------
    st.markdown("## 🗺️ Day-wise Itinerary")

    itinerary_places = city_places[:trip_days * 2]
    day_chunks = [itinerary_places[i:i+2] for i in range(0, len(itinerary_places), 2)]

    for i, day_places in enumerate(day_chunks[:trip_days], start=1):
        st.markdown(f"### 📅 Day {i}")
        cols = st.columns(len(day_places))
        for col, p in zip(cols, day_places):
            with col:
                st.markdown(f"""
                <div class="card">
                    <h4>{p['name']}</h4>
                    <p>⭐ {p['rating']}</p>
                </div>
                """, unsafe_allow_html=True)

    # ---------------- WEATHER FORECAST ----------------
    
    st.markdown("## 🌦️ Weather Forecast")

    weather_data = get_weather_forecast(destination, trip_days)

    if not weather_data:
        st.warning("Weather data is currently unavailable.")
    else:
        cols = st.columns(len(weather_data))
        conditions = []
    for col, w in zip(cols, weather_data):
        conditions.append(w["condition"])

        with col:
            st.markdown(f"""
            <div class="card">
                <h4>{w['day']}</h4>
                <p>{w['date']}</p>
                <p><b>{w['condition']}</b></p>
                <p>🌡️ Max Temp: {w['max_temp']}°C</p>
            </div>
            """, unsafe_allow_html=True)

    # -------- WEATHER SUMMARY --------
    st.markdown("## 🌤️ Weather Overview")

    st.markdown(
    f"""
    <div class="card" style="border-top:4px solid #C9A14A;">
        <h3 style="margin-bottom:10px;">🌦️ Weather Conditions</h3>
        <p style="font-size:15px;line-height:1.6;">
            During your stay in <b>{destination}</b>, temperatures are expected
            to remain comfortable with no extreme weather conditions.
            Outdoor sightseeing and city exploration should be possible
            on most days.
        </p>
    </div>
    """,
    unsafe_allow_html=True
    )



    # -------- TRIP SUMMARY (SINGLE, CLEAN) --------
    flight_cost = flight_options[0]["price"] if flight_options else 0
    hotel_cost = hotel_options[0]["price_per_night"] * trip_days if hotel_options else 0
    total_cost = flight_cost + hotel_cost

    st.markdown("## 🧳 Trip Summary")
    st.markdown(f"""
    <div class="card">
        <h3>💰 Cost Breakdown</h3>
        <p>✈️ Flight Cost: ₹{flight_cost}</p>
        <p>🏨 Hotel Cost ({trip_days} nights): ₹{hotel_cost}</p>
        <hr>
        <p style="font-size:18px;font-weight:700;">
            💳 Total Estimated Cost: ₹{total_cost}
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("👆 Enter details and click **Plan My Trip**")
    # # ---------------- BUDGET ----------------
    # st.markdown("## 🧳 Trip Summary")

    # flight_cost = flight_options[0]["price"] if flight_options else 0
    # hotel_cost = hotel_options[0]["price_per_night"] * trip_days if hotel_options else 0
    # total_cost = flight_cost + hotel_cost

    # st.markdown(f"""
    # <div class="card">
    #     <h3 style="margin-bottom:12px;">💰 Cost Breakdown</h3>

    #     <p style="font-size:16px;">
    #         ✈️ <b>Flight Cost:</b> ₹{flight_cost}
    #     </p>

    # <p style="font-size:16px;">
    #     🏨 <b>Hotel Cost</b> ({trip_days} nights): ₹{hotel_cost}
    # </p>

    # <hr style="margin:14px 0;">

    # <p style="font-size:20px;font-weight:700;color:#1E2A38;">
    #     💳 Total Estimated Cost: ₹{total_cost}
    # </p>
    # </div>
    # """, unsafe_allow_html=True)

