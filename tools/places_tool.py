import json
from pathlib import Path
from langchain.tools import Tool

DATA_DIR = Path(__file__).parent.parent / "data"

with open(DATA_DIR / "places.json", "r", encoding="utf-8") as f:
    places_data = json.load(f)

def discover_places(city: str):
    """Discover top-rated tourist places"""

    matches = [
        p for p in places_data
        if p["city"].lower() == city.lower()
    ]

    matches = sorted(matches, key=lambda x: x["rating"], reverse=True)
    return matches[:6]

places_tool = Tool(
    name="Places Discovery Tool",
    description="Finds top attractions and tourist places in a city",
    func=discover_places
)
