from tools.hotel_tool import recommend_hotel

result = recommend_hotel.invoke({
    "city": "Goa",
    "min_stars": 4,
    "max_price": 3000
})

print(result)
