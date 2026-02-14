# File: backend/automation/activepieces_connector.py
# Purpose: Triggers Activepieces flows for lightweight automations.
# Logic: Ghost Module Protocol - If Activepieces is down, skip and log.

import requests
import json

class ActivepiecesManager:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        print("🔗 [Activepieces]: Ninja Automation Linked.")

    def run_flow(self, payload):
        """
        Flow ko trigger karta hai. 
        Example payload: {"action": "send_alert", "msg": "GPU Overheating!"}
        """
        print("⚡ [Activepieces]: Sending signal to flow...")
        
        try:
            # First Principles: Keep it simple
            response = requests.post(
                self.webhook_url, 
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ [Activepieces]: Flow executed.")
                return True
            return False
            
        except Exception as e:
            # Solo Mode logic: Don't crash if automation fails [cite: 2026-02-11]
            print(f"⚠️ [Automation]: Activepieces unreachable, skipping... {e}")
            return False

# --- Usage Example ---
# ap = ActivepiecesManager("http://your-ip:8080/api/v1/webhooks/...")
# ap.run_flow({"event": "new_user", "name": "Rahul", "college": "Bansal"})
