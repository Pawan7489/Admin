# File: backend/deployment/koyeb_failover.py
# Purpose: Activates Koyeb (Backup Server) if Render (Primary) fails.
# Free Tier Benefit: Uses $5.50 monthly credit for emergency hosting.

import requests
import time

class KoyebFailoverManager:
    def __init__(self, koyeb_token, app_id, service_id, render_url):
        """
        koyeb_token: Koyeb Account Settings se milega.
        service_id: Koyeb Service ka unique ID.
        render_url: Aapka primary Render URL.
        """
        self.headers = {
            "Authorization": f"Bearer {koyeb_token}",
            "Content-Type": "application/json"
        }
        # Koyeb API Endpoint to redeploy/resume a service
        self.koyeb_api = f"https://app.koyeb.com/v1/services/{service_id}/redeploy"
        self.render_url = render_url

    def check_primary_health(self):
        """Render URL ko ping karta hai."""
        try:
            response = requests.get(self.render_url, timeout=5)
            if response.status_code == 200:
                print("✅ [Health]: Render is Active.")
                return True
            else:
                print(f"⚠️ [Health]: Render returned {response.status_code}.")
                return False
        except Exception:
            print("❌ [Health]: Render is DOWN!")
            return False

    def activate_backup(self):
        """Agar Render down hai, toh Koyeb ko jaga do."""
        print("🚨 [Failover]: Initiating Koyeb Backup Protocol...")
        
        try:
            # Koyeb API ko trigger karna
            response = requests.post(self.koyeb_api, headers=self.headers, json={})
            
            if response.status_code == 200:
                print("🚀 [Koyeb]: Backup Service Redeployed & Active!")
                return "Backup Online"
            else:
                print(f"❌ [Koyeb]: Failed to activate. Error: {response.text}")
                return "Failover Failed"
        except Exception as e:
            print(f"❌ [Error]: API Connection failed. {str(e)}")
            return "Connection Error"

# --- Master Execution Logic ---
if __name__ == "__main__":
    # Credentials (Vault se aayenge)
    KOYEB_TOKEN = "kyb_xxxxxxxxxxxxxxx"
    SERVICE_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    RENDER_URL = "https://a1-os-admin.onrender.com/health"
    
    manager = KoyebFailoverManager(KOYEB_TOKEN, SERVICE_ID, RENDER_URL)
    
    # Check Logic (Loop mein chalega ya Cron Job se)
    if not manager.check_primary_health():
        # Double check after 10 seconds (False Positive bachane ke liye)
        time.sleep(10)
        if not manager.check_primary_health():
            manager.activate_backup()
          
