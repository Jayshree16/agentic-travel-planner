from tools.budget_tool import estimate_budget

result = estimate_budget.invoke({
    "flight_price": 4800,
    "hotel_price_per_night": 3200,
    "days": 3,
    "daily_food_travel_cost": 800
})

print(result)
