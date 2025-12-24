from tools.weather_tool import get_weather_forecast

# Goa coordinates
result = get_weather_forecast.invoke({
    "latitude": 15.2993,
    "longitude": 74.1240,
    "days": 3
})

print(result)
