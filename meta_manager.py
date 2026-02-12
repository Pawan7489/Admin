# File: meta_manager.py
# Description: Unified Controller for Facebook, Instagram, and WhatsApp

import requests
import json
import os

class MetaController:
    def __init__(self):
        self.config_file = "meta_config.json"
        self.access_token = None
        self.fb_page_id = None
        self.insta_account_id = None
        self.wa_phone_id = None
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.access_token = data.get("access_token")
                self.fb_page_id = data.get("fb_page_id")
                self.insta_account_id = data.get("insta_account_id")
                self.wa_phone_id = data.get("wa_phone_id")

    def setup(self, token, fb_id, insta_id, wa_id):
        """
        Configuration save karta hai.
        Data 'Meta for Developers' portal se milta hai.
        """
        data = {
            "access_token": token,
            "fb_page_id": fb_id,
            "insta_account_id": insta_id,
            "wa_phone_id": wa_id
        }
        with open(self.config_file, "w") as f:
            json.dump(data, f)
        self.load_config()
        return "✅ Meta Configuration Saved!"

    # --- FACEBOOK ---
    def post_facebook(self, message):
        if not self.access_token or not self.fb_page_id: return "❌ Config Missing."
        
        url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/feed"
        payload = {"message": message, "access_token": self.access_token}
        
        try:
            r = requests.post(url, data=payload)
            if r.status_code == 200:
                return f"✅ Posted to Facebook! ID: {r.json()['id']}"
            else:
                return f"❌ FB Error: {r.text}"
        except Exception as e: return str(e)

    # --- INSTAGRAM (Photo Only) ---
    def post_instagram(self, image_url, caption):
        """
        Instagram requires Image URL (Not local file).
        Step 1: Create Container. Step 2: Publish.
        """
        if not self.access_token or not self.insta_account_id: return "❌ Config Missing."

        # Step 1: Create Container
        url_create = f"https://graph.facebook.com/v18.0/{self.insta_account_id}/media"
        payload_create = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        r1 = requests.post(url_create, data=payload_create)
        if r1.status_code != 200: return f"❌ Insta Step 1 Failed: {r1.text}"
        
        container_id = r1.json()['id']

        # Step 2: Publish Container
        url_publish = f"https://graph.facebook.com/v18.0/{self.insta_account_id}/media_publish"
        payload_publish = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        r2 = requests.post(url_publish, data=payload_publish)
        
        if r2.status_code == 200:
            return f"✅ Posted to Instagram! ID: {r2.json()['id']}"
        else:
            return f"❌ Insta Step 2 Failed: {r2.text}"

    # --- WHATSAPP ---
    def send_whatsapp(self, to_number, message):
        if not self.access_token or not self.wa_phone_id: return "❌ Config Missing."
        
        url = f"https://graph.facebook.com/v18.0/{self.wa_phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            r = requests.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                return "✅ WhatsApp Message Sent!"
            else:
                return f"❌ WA Error: {r.text}"
        except Exception as e: return str(e)
      
