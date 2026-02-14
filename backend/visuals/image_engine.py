# File: backend/visuals/image_engine.py
# Purpose: Fetches high-quality, relevant images for the UI.
# Free Tier: Unsplash API (5,000 requests/hour - Huge!).
# Strategy: "Pichai Rule" - Global standard scalability.

import requests

class VisualAssetManager:
    def __init__(self, access_key):
        """
        Access Key: unsplash.com/developers se lein.
        """
        self.access_key = access_key
        self.base_url = "https://api.unsplash.com/search/photos"

    def get_relevant_image(self, query):
        """
        Query ke basis par sabse best high-quality image nikaalta hai.
        """
        print(f"🖼️ [Unsplash]: Searching for high-quality '{query}' visuals...")
        
        params = {
            "query": query,
            "client_id": self.access_key,
            "per_page": 1,
            "orientation": "landscape" # Premium look ke liye hamesha landscape
        }

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data['results']:
                img_url = data['results'][0]['urls']['regular']
                photographer = data['results'][0]['user']['name']
                print(f"✅ [Success]: Found image by {photographer}.")
                return img_url
            return None
            
        except Exception as e:
            print(f"❌ [Error]: Visual fetch failed. {e}")
            return "https://images.unsplash.com/photo-1518770660439-4636190af475" # Fallback Tech Image

# --- Master Logic: Linking Intent to Visuals ---
# if intent == "show_image":
#     topic = entities.get('topic')
#     url = visual_manager.get_relevant_image(topic)
#     display_in_ui(url)
