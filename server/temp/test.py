import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Set API Key for OpenWeatherMap
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": "Phoenix, AZ",  # e.g., "41.3851,2.1734" for Barcelona
    "radius": "1000",
    "type": "restaurant",
    "key": GOOGLE_MAPS_API_KEY
}
response = requests.get(url, params=params)

# Parse the JSON string into a Python dictionary
data = json.loads(response.text)

# Iterate over each result and extract the desired information
places_info = []
for result in data.get("results", []):
    name = result.get("name", "N/A")
    rating = result.get("rating", "N/A")
    vicinity = result.get("vicinity", "N/A")
    places_info.append({"name": name, "rating": rating, "vicinity": vicinity})

print(places_info)