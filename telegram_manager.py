# File: telegram_manager.py
# Description: Telegram Bot Integration (Send Messages & Files)

import requests
import json
import os

class TelegramBot:
    def __init__(self):
        self.config_file = "telegram_config.json"
        self.base_url = "https://api.telegram.org/bot"
        self.token = None
        self.chat_id = None
        self.load_config()

    def load_config(self):
        """Saved Token aur Chat ID load karta hai"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.token = data.get("token")
                self.chat_id = data.get("chat_id")

    def setup(self, token, chat_id):
        """
        Setup function.
        Token: BotFather se milega.
        Chat ID: 'userinfobot' se milega.
        """
        data = {"token": token, "chat_id": chat_id}
        with open(self.config_file, "w") as f:
            json.dump(data, f)
        
        self.load_config()
        return "✅ Telegram Configured! Test message bhejne ke liye 'telegram test' try karein."

    def send_message(self, message):
        """Simple text message bhejta hai"""
        if not self.token or not self.chat_id:
            return "❌ Error: Setup incomplete. Run: telegram setup <token> <chat_id>"

        url = f"{self.base_url}{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message}
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return "✅ Message Sent!"
            else:
                return f"❌ Failed: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def send_file(self, file_path):
        """
        Server se koi bhi file (Photo/PDF/Zip) Telegram par bhejta hai.
        """
        if not self.token or not self.chat_id:
            return "❌ Error: Config missing."
        
        if not os.path.exists(file_path):
            return f"❌ Error: File '{file_path}' nahi mili."

        url = f"{self.base_url}{self.token}/sendDocument"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': self.chat_id}
                response = requests.post(url, data=data, files=files)
                
            if response.status_code == 200:
                return f"✅ File '{file_path}' sent successfully!"
            else:
                return f"❌ Failed: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"
          
