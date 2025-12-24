from data_loader import load_flights, load_hotels, load_places

flights = load_flights()
hotels = load_hotels()
places = load_places()

print(f"Flights loaded: {len(flights)}")
print(f"Hotels loaded: {len(hotels)}")
print(f"Places loaded: {len(places)}")

print("\nSample Flight:", flights[0])
print("\nSample Hotel:", hotels[0])
print("\nSample Place:", places[0])
