from langchain_groq import ChatGroq

from agent.tools import (
    search_flight,
    recommend_hotel,
    get_itinerary,
    get_weather
)

CITY_COORDS = {
    "delhi": (28.61, 77.23),
    "mumbai": (19.07, 72.87),
    "goa": (15.29, 74.12),
    "bangalore": (12.97, 77.59),
    "chennai": (13.08, 80.27),
    "hyderabad": (17.38, 78.48),
    "kolkata": (22.57, 88.36),
    "jaipur": (26.91, 75.78),
}

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

def create_travel_agent():

    def agent(inputs):
        source = inputs["source"]
        destination = inputs["destination"]
        days = inputs["days"]
        rating = inputs["hotel_rating"]

        flight = search_flight(source, destination)
        if not flight:
            return {"error": f"No flights found from {source} to {destination}"}

        hotel = recommend_hotel(destination, rating, days)
        if not hotel:
            return {"error": f"No hotels found in {destination}"}

        itinerary = get_itinerary(destination, days)

        lat, lon = CITY_COORDS[destination.lower()]
        weather = get_weather(lat, lon, days)

        total = flight["price"] + hotel["total_cost"]

        # 🔹 LLM-based reasoning (AGENTIC PART)
        reasoning_prompt = f"""
        Explain why this flight and hotel were selected for a {days}-day trip
        from {source} to {destination}.
        Flight price: {flight['price']}
        Hotel price per night: {hotel['price_per_night']}
        """

        reasoning_text = llm.invoke(reasoning_prompt).content

        return {
            "flight": flight,
            "hotel": hotel,
            "itinerary": itinerary,
            "weather": weather,
            "budget": {
                "flight": flight["price"],
                "hotel": hotel["total_cost"],
                "total": total
            },
            "reasoning": {
                "llm_explanation": reasoning_text
            }
        }

    return agent
