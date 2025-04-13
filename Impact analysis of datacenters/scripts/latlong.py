from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="my_app")

# Single address geocoding
address = "1600 Amphitheatre Parkway, Mountain View, CA"
location = geolocator.geocode(address)

if location:
    print(f"Latitude: {location.latitude}")
    print(f"Longitude: {location.longitude}")

