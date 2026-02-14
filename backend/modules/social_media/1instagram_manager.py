# File: instagram_manager.py
# Description: Specialized Module for Instagram Publishing

import requests
import json
import os

class InstaBot:
    def __init__(self):
        self.config_file = "insta_config.json"
        self.access_token = None
        self.account_id = None
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.access_token = data.get("token")
                self.account_id = data.get("account_id")

    def setup(self, token, account_id):
        data = {"token": token, "account_id": account_id}
        with open(self.config_file, "w") as f:
            json.dump(data, f)
        self.load_config()
        return "✅ Instagram Configured Successfully!"

    def upload_photo(self, image_url, caption):
        """
        Instagram par post karne ke 2 steps hote hain:
        1. Container Create karna
        2. Publish karna
        """
        if not self.access_token or not self.account_id:
            return "❌ Error: Run 'insta setup <token> <account_id>'"

        # Step 1: Create Container
        url_create = f"https://graph.facebook.com/v18.0/{self.account_id}/media"
        payload_create = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        
        try:
            r1 = requests.post(url_create, data=payload_create)
            if r1.status_code != 200: return f"❌ Step 1 Failed: {r1.text}"
            
            container_id = r1.json()['id']

            # Step 2: Publish
            url_publish = f"https://graph.facebook.com/v18.0/{self.account_id}/media_publish"
            payload_publish = {
                "creation_id": container_id,
                "access_token": self.access_token
            }
            r2 = requests.post(url_publish, data=payload_publish)
            
            if r2.status_code == 200:
                return f"✅ Instagram Post Live! ID: {r2.json()['id']}"
            else:
                return f"❌ Step 2 Failed: {r2.text}"
        except Exception as e:
            return f"System Error: {str(e)}"
          
