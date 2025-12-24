with open(DATA_DIR / "hotels.json", "r", encoding="utf-8") as f:
    hotels_data = json.load(f)

def recommend_hotels(city: str, min_stars: int):
    """Recommend hotels by city and rating"""

    matches = [
        h for h in hotels_data
        if h["city"] == city and h["stars"] >= min_stars
    ]

    matches = sorted(matches, key=lambda x: x["price_per_night"])
    return matches[:3]

hotel_tool = Tool(
    name="Hotel Recommendation Tool",
    description="Recommends hotels based on city, rating and price",
    func=recommend_hotels
)
