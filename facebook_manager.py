# File: facebook_manager.py
# Description: Specialized Module for Facebook Page Management

import requests
import json
import os

class FacebookBot:
    def __init__(self):
        self.config_file = "fb_config.json"
        self.access_token = None
        self.page_id = None
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.access_token = data.get("token")
                self.page_id = data.get("page_id")

    def setup(self, token, page_id):
        """Facebook Credentials Save karega"""
        data = {"token": token, "page_id": page_id}
        with open(self.config_file, "w") as f:
            json.dump(data, f)
        self.load_config()
        return "✅ Facebook Configured Successfully!"

    def post_status(self, message):
        """Seedha Page par text post karega"""
        if not self.access_token or not self.page_id:
            return "❌ Error: Setup incomplete. Run: 'fb setup <token> <page_id>'"

        url = f"https://graph.facebook.com/v18.0/{self.page_id}/feed"
        payload = {"message": message, "access_token": self.access_token}

        try:
            r = requests.post(url, data=payload)
            if r.status_code == 200:
                return f"✅ Facebook Post Live! ID: {r.json()['id']}"
            else:
                return f"❌ FB Error: {r.text}"
        except Exception as e:
            return f"System Error: {str(e)}"
          
