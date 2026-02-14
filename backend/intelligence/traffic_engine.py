# File: backend/intelligence/traffic_engine.py
# Purpose: Real-time Traffic & Commute Optimization.
# Free Tier: 2,500 Transactions per day (TomTom).
# Strategy: Use for precise routing and "Estimated Time of Arrival" (ETA).

import requests

class TrafficEngine:
    def __init__(self, api_key):
        """
        API Key: developer.tomtom.com se lein.
        """
        self.key = api_key
        self.base_url = "https://api.tomtom.com/routing/1/calculateRoute"

    def get_commute_details(self, start_coords, end_coords):
        """
        Indore se Bhopal ka sabse tez rasta aur traffic delay nikaalta hai.
        start_coords: 'lat,lng'
        """
        print(f"🚦 [TomTom]: Calculating best route with live traffic...")
        
        # Route calculation with traffic awareness
        endpoint = f"{self.base_url}/{start_coords}:{end_coords}/json"
        params = {
            'key': self.key,
            'traffic': 'true',
            'travelMode': 'car'
        }

        try:
            response = requests.get(endpoint, params=params).json()
            route = response['routes'][0]['summary']
            
            # Data extraction
            travel_time_sec = route['travelTimeInSeconds']
            traffic_delay_sec = route['trafficDelayInSeconds']
            distance_km = route['lengthInMeters'] / 1000
            
            return {
                "eta_minutes": round(travel_time_sec / 60),
                "delay_minutes": round(traffic_delay_sec / 60),
                "distance": round(distance_km, 2)
            }
        except Exception as e:
            print(f"❌ [Error]: TomTom Routing failed. {e}")
            return None

# --- Logic: The "Commute Guardian" ---
# if time == "08:00 AM":
#     data = traffic_engine.get_commute_details("22.7196,75.8577", "23.2599,77.4126")
#     if data['delay_minutes'] > 15:
#         ai_voice.speak(f"Bhai, aaj bypass par jam hai, 15 minute late ho sakte ho.")
