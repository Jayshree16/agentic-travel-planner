import requests

def get_weather(latitude, longitude):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&daily=temperature_2m_max"
        "&timezone=auto"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    goa_lat = 15.2993
    goa_lon = 74.1240

    weather = get_weather(goa_lat, goa_lon)
    print(weather["daily"]["temperature_2m_max"][:3])
