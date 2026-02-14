# File: backend/intelligence/geo_engine.py
# Purpose: Location-aware intelligence for A1 OS.
# Free Tier: ~50k-100k map loads per month (Mapbox).
# Strategy: "Musk Rule" - High precision, minimalist design, zero cost.

import requests

class GeoEngine:
    def __init__(self, access_token):
        """
        Access Token: mapbox.com dashboard se lein.
        """
        self.token = access_token
        self.geocoding_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"

    def get_coords(self, place_name):
        """
        Address ya jagah ke naam ko Latitude/Longitude mein badalta hai.
        Example: 'Bansal College Bhopal' -> [77.41, 23.25]
        """
        print(f"🗺️ [Geo]: Searching coordinates for: {place_name}...")
        url = f"{self.geocoding_url}/{place_name}.json?access_token={self.token}&limit=1"
        
        try:
            response = requests.get(url).json()
            if response['features']:
                coords = response['features'][0]['center'] # [longitude, latitude]
                return {"lng": coords[0], "lat": coords[1]}
            return None
        except Exception as e:
            print(f"❌ [Error]: Geocoding failed. {e}")
            return None

    def get_static_map_url(self, lat, lng, zoom=12):
        """
        Premium Static Map link generate karta hai (Apple-style Dark Theme).
        """
        # "dark-v11" style ekdum futuristic lagta hai dashboard par.
        style_id = "dark-v11"
        width, height = 600, 300
        return f"https://api.mapbox.com/styles/v1/mapbox/{style_id}/static/{lng},{lat},{zoom},0/{width}x{height}?access_token={self.token}"

# --- Usage Strategy ---
# if intent == "find_location":
#     pos = geo_engine.get_coords("Indore, MP")
#     map_img = geo_engine.get_static_map_url(pos['lat'], pos['lng'])
#     display_on_dashboard(map_img)
