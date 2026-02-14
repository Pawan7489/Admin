# File: backend/automation/n8n_connector.py
# Purpose: Triggers automated workflows in n8n.
# Strategy: "Decoupled Execution" - AI triggers it and moves on.

import requests
import json

class N8NWorkflowManager:
    def __init__(self, webhook_base_url):
        self.base_url = webhook_base_url
        print("🔗 [n8n]: Automation Web Connected.")

    def trigger_workflow(self, workflow_id, data):
        """
        Specific workflow ko data ke saath trigger karta hai.
        """
        url = f"{self.base_url}/{workflow_id}"
        print(f"⚡ [n8n]: Triggering workflow '{workflow_id}'...")
        
        try:
            # We use 'json' to send complex data like list of images/emails
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                print("✅ [n8n]: Workflow executed successfully.")
                return response.json()
            else:
                print(f"⚠️ [n8n]: Workflow returned status {response.status_code}.")
                return None
        except Exception as e:
            print(f"❌ [Error]: Could not reach n8n. {e}")
            return None

# --- Usage Strategy ---
# if intent == "schedule_meeting":
#     n8n.trigger_workflow("meeting-bot", {"email": "user@test.com", "time": "10am"})
