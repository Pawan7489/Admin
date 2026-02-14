# File: backend/intelligence/geo_engine.py
# Purpose: Location-aware AI features (Maps/Routes).
# Free Tier: 100k monthly map loads (Mapbox).
# Strategy: "Musk Rule" - High precision with zero cost.

import requests

class GeoIntelligence:
    def __init__(self, access_token):
        self.token = access_token
        self.base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"

    def get_coordinates(self, location_name):
        """
        Address ko Latitude/Longitude mein badalta hai.
        """
        print(f"🗺️ [Geo]: Finding coordinates for '{location_name}'...")
        url = f"{self.base_url}/{location_name}.json?access_token={self.token}"
        
        try:
            response = requests.get(url).json()
            coords = response['features'][0]['center'] # [longitude, latitude]
            return {"lng": coords[0], "lat": coords[1]}
        except Exception as e:
            print(f"❌ [Geo Error]: Location not found. {e}")
            return None

    def get_static_map(self, lat, lng):
        """
        Premium Static Map URL generate karta hai UI mein dikhane ke liye.
        """
        # Apple-style Dark Theme map
        style_id = "dark-v11" 
        return f"https://api.mapbox.com/styles/v1/mapbox/{style_id}/static/{lng},{lat},12,0/500x300?access_token={self.token}"

# --- Usage Example ---
# geo = GeoIntelligence("mapbox_token")
# pos = geo.get_coordinates("Bhopal, India")
# map_url = geo.get_static_map(pos['lat'], pos['lng'])
