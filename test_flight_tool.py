from tools.flight_tool import search_flights

result = search_flights.invoke({
    "source": "Hyderabad",
    "destination": "Delhi",
    "preference": "cheapest"
})

print(result)
