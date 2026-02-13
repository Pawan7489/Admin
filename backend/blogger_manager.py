# File: blogger_manager.py
# Description: Manages Blogger Posts via Google API

import os
import json

# Note: Asli Blogger automation ke liye 'google-api-python-client' chahiye
try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

class BloggerBot:
    def __init__(self):
        self.service = None
        self.blog_id = None # Blog ID yahan save hogi

    def setup(self, credentials_file, blog_id):
        """
        Google Cloud Console se JSON key file chahiye hoti hai.
        """
        if not GOOGLE_API_AVAILABLE:
            return "❌ Error: Google Libraries missing. Install: 'pip install google-api-python-client'"

        if not os.path.exists(credentials_file):
            return f"❌ Error: File '{credentials_file}' nahi mili."

        try:
            # Service Account method (Simplest for servers)
            creds = service_account.Credentials.from_service_account_file(
                credentials_file, scopes=['https://www.googleapis.com/auth/blogger'])
            
            self.service = build('blogger', 'v3', credentials=creds)
            self.blog_id = blog_id
            return "✅ Blogger Connected Successfully!"
        except Exception as e:
            return f"❌ Connection Failed: {str(e)}"

    def create_post(self, title, content):
        if not self.service:
            return "❌ Error: Pehle 'blogger setup' run karein."

        body = {
            "kind": "blogger#post",
            "blog": {"id": self.blog_id},
            "title": title,
            "content": content
        }

        try:
            posts = self.service.posts()
            result = posts.insert(blogId=self.blog_id, body=body).execute()
            return f"✅ Blog Published! URL: {result['url']}"
        except Exception as e:
            return f"Error: {str(e)}"
          
