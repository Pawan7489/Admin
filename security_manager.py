# File: security_manager.py
# Description: Handles Login Security (Digital Lock)

import hashlib
import json
import os

class SecurityGuard:
    def __init__(self):
        self.config_file = "security_config.json"
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            # Default Setup (Pehli baar ke liye)
            # Default Password: 'admin' (Change this immediately!)
            default_pass = "admin"
            self.credentials = {
                "username": "admin",
                "password_hash": self.hash_password(default_pass)
            }
            self.save_config()
        else:
            with open(self.config_file, "r") as f:
                self.credentials = json.load(f)

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.credentials, f)

    def hash_password(self, password):
        """Password ko code me convert karta hai taaki koi padh na sake"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_login(self, username, password):
        """Login check karta hai"""
        if username == self.credentials['username']:
            if self.hash_password(password) == self.credentials['password_hash']:
                return True
        return False

    def change_password(self, new_password):
        """Naya password set karta hai"""
        self.credentials['password_hash'] = self.hash_password(new_password)
        self.save_config()
        return "✅ Password Updated Successfully!"
      
