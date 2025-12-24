import json
from pathlib import Path
from langchain.tools import Tool

DATA_DIR = Path(__file__).parent.parent / "data"

with open(DATA_DIR / "flights.json", "r", encoding="utf-8") as f:
    flights_data = json.load(f)

def search_flights(source: str, destination: str):
    """Find cheapest flights between source and destination"""

    matches = [
        f for f in flights_data
        if f["from"] == source and f["to"] == destination
    ]

    if not matches:
        return []

    matches = sorted(matches, key=lambda x: x["price"])
    return matches[:3]

flight_search_tool = Tool(
    name="Flight Search Tool",
    description="Finds cheapest and best flights using flight dataset",
    func=search_flights
)
