# File: backend/nervous_system/ngrok_tunnel.py
# Purpose: Exposes Local Server (Bhopal/Indore) to the Internet securely.
# Strategy: "The Tunnel" - No Static IP needed.

import os
from pyngrok import ngrok

class NgrokTunnelManager:
    def __init__(self, auth_token, port=5000):
        """
        auth_token: Ngrok dashboard se mila hua token.
        port: Wo local port jahan aapka server chal raha hai.
        """
        self.auth_token = auth_token
        self.port = port
        self.public_url = None

    def start_tunnel(self):
        """
        Secure tunnel start karta hai aur Public URL return karta hai.
        """
        print(f"🚇 [Ngrok]: Authenticating tunnel...")
        ngrok.set_auth_token(self.auth_token)
        
        # Open a HTTP tunnel on the default port 5000
        try:
            self.public_url = ngrok.connect(self.port).public_url
            print(f"🌍 [Ngrok]: Tunnel Active! Public URL: {self.public_url}")
            print("   -> Ab aap is URL se duniya mein kahin se bhi apne local server ko access kar sakte hain.")
            return self.public_url
        except Exception as e:
            print(f"❌ [Error]: Ngrok Connection Failed. {str(e)}")
            return None

    def close_tunnel(self):
        """Tunnel band karta hai."""
        ngrok.kill()
        print("🛑 [Ngrok]: Tunnel Closed.")

# --- Usage ---
# manager = NgrokTunnelManager("your_ngrok_auth_token")
# url = manager.start_tunnel()
# Keep the script running...
