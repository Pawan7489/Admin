# File: wordpress_manager.py
# Description: Manages WordPress Posts via REST API

import requests
import base64
import json
import os

class WordPressBot:
    def __init__(self):
        self.config_file = "wp_config.json"
        self.base_url = ""
        self.auth_header = None
        self.load_config()

    def load_config(self):
        """Saved login details load karta hai"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.base_url = data.get("url")
                user = data.get("user")
                pwd = data.get("password")
                # Create Auth Header
                credentials = f"{user}:{pwd}"
                token = base64.b64encode(credentials.encode()).decode()
                self.auth_header = {'Authorization': f'Basic {token}'}

    def setup(self, url, username, app_password):
        """
        Login details save karta hai.
        Note: WordPress Admin panel me 'Application Password' generate karein.
        """
        if not url.endswith("/"): url += "/"
        # API endpoint add karte hain
        api_url = url + "wp-json/wp/v2/"
        
        data = {"url": api_url, "user": username, "password": app_password}
        with open(self.config_file, "w") as f:
            json.dump(data, f)
        
        self.load_config()
        return f"✅ WordPress Configured for: {url}"

    def create_post(self, title, content, status="draft"):
        """
        Post create karta hai. 
        Status options: 'publish', 'draft'
        """
        if not self.auth_header:
            return "❌ Error: Pehle 'wp setup' run karein."

        post_url = self.base_url + "posts"
        post_data = {
            "title": title,
            "content": content,
            "status": status
        }

        try:
            response = requests.post(post_url, headers=self.auth_header, json=post_data)
            if response.status_code == 201:
                return f"✅ Post Created Successfully! ID: {response.json()['id']}"
            else:
                return f"❌ Failed: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"
          
