# File: backend/admin/strapi_client.py
# Purpose: Fetches dynamic configurations from Strapi Admin Panel.
# Strategy: "Pichai Rule" - Scalable config management.

import requests

class StrapiManager:
    def __init__(self, base_url, api_token):
        self.base_url = f"{base_url}/api"
        self.headers = {"Authorization": f"Bearer {api_token}"}
        print("📑 [Strapi]: Admin Interface Linked.")

    def get_system_config(self):
        """
        AI ki current settings Strapi se load karta hai.
        """
        try:
            response = requests.get(f"{self.base_url}/system-configs", headers=self.headers)
            if response.status_code == 200:
                config = response.json()['data']
                print("✅ [Strapi]: Latest System Config loaded.")
                return config
            return None
        except Exception as e:
            print(f"❌ [Error]: Strapi unreachable. {e}")
            return None

# --- Usage Strategy ---
# if __name__ == "__main__":
#     admin = StrapiManager("http://your-oracle-ip:1337", "token")
#     config = admin.get_system_config()
#     # Ab AI wahi settings use karega jo aapne Admin Panel mein set ki hain.
