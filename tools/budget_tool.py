import json
from pathlib import Path
from langchain.tools import Tool


def estimate_budget(flight_price: int, hotel_price: int, days: int):
    """Estimate total trip budget"""

    food_and_local = days * 800  # approx per day
    hotel_total = hotel_price * days

    return {
        "flight": flight_price,
        "hotel": hotel_total,
        "food_and_travel": food_and_local,
        "total": flight_price + hotel_total + food_and_local
    }

budget_tool = Tool(
    name="Budget Estimation Tool",
    description="Calculates total trip cost including flights, hotels, and daily expenses",
    func=estimate_budget
)
