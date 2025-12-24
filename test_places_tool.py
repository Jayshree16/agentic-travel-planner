from tools.places_tool import discover_places

result = discover_places.invoke({
    "city": "Goa",
    "top_n": 3
})

print(result)
