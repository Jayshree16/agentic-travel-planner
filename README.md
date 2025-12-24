# ✈️ Agentic AI-Based Travel Planning Assistant (LangChain + Streamlit)

An intelligent, agentic AI travel planning system that automatically generates optimized travel itineraries by combining structured datasets (flights, hotels, places) with real-time weather data.  
The system reasons like a travel expert and presents results through a clean, interactive Streamlit interface.

---

## 🚀 Features

- 🔍 Intelligent flight selection from structured JSON data
- 🏨 Hotel recommendations based on rating and price
- 📍 Famous places & attractions discovery
- 🗺️ Day-wise itinerary generation
- 🌦️ Real-time weather forecast (Open-Meteo API)
- 💰 Budget estimation (flight + hotel)
- 🤖 Agentic workflow using LangChain-style tools
- 🎨 Professional Streamlit UI (non AI-looking)

---

## 🧠 Agentic AI Architecture

This project follows an **Agent + Tools** design pattern.

### Agent Responsibilities:
- Understand user travel intent
- Decide which tools to invoke
- Combine results logically
- Generate structured output:
  - Flight
  - Hotel
  - Places
  - Weather
  - Budget
  - Reasoning

---

## 🧩 Project Structure

AGENTIC-TRAVEL-PLANNER/
│
├── agent/
│ ├── init.py
│ ├── agent_prompt.py
│ ├── tools.py
│ └── travel_agent.py
│
├── assets/
│ ├── icons/
│ ├── images/
│ └── places/
│ ├── beach.jpg
│ ├── fort.jpg
│ ├── monument.jpg
│ ├── museum.jpg
│ ├── palace.jpg
│ ├── park.jpg
│ └── temple.jpg
│
├── components/
│ ├── budget_card.py
│ ├── flight_card.py
│ ├── hotel_card.py
│ └── itinerary_card.py
│
├── data/
│ ├── flights.json
│ ├── hotels.json
│ └── places.json
│
├── tools/
│ ├── budget_tool.py
│ ├── flight_tool.py
│ ├── hotel_tool.py
│ ├── places_tool.py
│ └── weather_tool.py
│
├── streamlit.py
├── test_agent.py
├── test_budget_tool.py
├── test_flight_tool.py
├── test_hotel_tool.py
├── test_places_tool.py
├── test_weather_tool.py
│
├── requirements.txt
└── README.md


---

## 📊 Data Sources

### Static Datasets
- `flights.json` – Flight routes, prices, timings
- `hotels.json` – Hotels, city, stars, pricing
- `places.json` – Attractions, type, rating

### Live API
- **Weather**: Open-Meteo (No API key required)

---

## 🔧 Tools Implemented

| Tool | Description |
|----|----|
| Flight Tool | Filters cheapest flight by route |
| Hotel Tool | Recommends hotels by rating & price |
| Places Tool | Selects top-rated attractions |
| Weather Tool | Fetches real-time forecast |
| Budget Tool | Calculates total trip cost |

---

## 🖥️ Streamlit UI Highlights

- Dropdown-based source & destination selection
- Trip duration & hotel rating filters
- 3 flight & 3 hotel options
- Clean card-based layout
- Human-readable weather summary
- Professional cost breakdown UI

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/agentic-travel-planner.git
cd agentic-travel-planner

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the App
streamlit run streamlit.py

🧪 Testing

Individual tools and agent logic are unit-tested:

python test_agent.py
python test_flight_tool.py
python test_weather_tool.py