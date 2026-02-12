# File: whatsapp_manager.py
# Description: Specialized Module for WhatsApp Cloud API

import requests
import json
import os

class WhatsAppBot:
    def __init__(self):
        self.config_file = "wa_config.json"
        self.access_token = None
        self.phone_id = None
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.access_token = data.get("token")
                self.phone_id = data.get("phone_id")

    def setup(self, token, phone_id):
        data = {"token": token, "phone_id": phone_id}
        with open(self.config_file, "w") as f:
            json.dump(data, f)
        self.load_config()
        return "✅ WhatsApp Configured Successfully!"

    def send_msg(self, to_number, message_text):
        if not self.access_token or not self.phone_id:
            return "❌ Error: Run 'wa setup <token> <phone_id>'"

        url = f"https://graph.facebook.com/v18.0/{self.phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": message_text}
        }

        try:
            r = requests.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                return "✅ WhatsApp Message Sent!"
            else:
                return f"❌ WA Error: {r.text}"
        except Exception as e:
            return f"System Error: {str(e)}"
          
