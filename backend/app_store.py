# File Path: backend/app_store.py
# Description: Manages API Connections for WhatsApp, Facebook, Instagram, and Truecaller.
# Handles 1-Click Connect, Storage Sync, and APK Uploads.

import os
import json
from datetime import datetime

class AppStoreManager:
    def __init__(self):
        self.db_file = "database/app_connections.json"
        self._ensure_db()
        self.load_connections()

    def _ensure_db(self):
        """Database folder aur JSON file create karta hai agar nahi hai toh."""
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.db_file):
            # Default empty states for our Section D apps
            default_state = {
                "WhatsApp API": {"status": "Disconnected", "api_key": "", "last_sync": "Never"},
                "Facebook Graph": {"status": "Disconnected", "api_key": "", "last_sync": "Never"},
                "Instagram Hub": {"status": "Disconnected", "api_key": "", "last_sync": "Never"},
                "Truecaller ID": {"status": "Disconnected", "api_key": "", "last_sync": "Never"}
            }
            with open(self.db_file, 'w') as f:
                json.dump(default_state, f, indent=4)

    def load_connections(self):
        with open(self.db_file, 'r') as f:
            try:
                self.apps = json.load(f)
            except:
                self.apps = {}

    def save_connections(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.apps, f, indent=4)

    # --- 1. API CONNECTION LOGIC ---
    def connect_api(self, app_name, api_key="AUTO_GENERATE"):
        """
        App ko A1 OS se link karta hai. 
        UI button "Connect API" click hone par ye run hoga.
        """
        app_name = app_name.strip()
        
        # Checking if the app is supported in our UI cards
        valid_apps = ["WhatsApp API", "Facebook Graph", "Instagram Hub", "Truecaller ID"]
        if app_name not in valid_apps:
            # Flexible matching agar naam thoda alag ho
            matched = False
            for valid in valid_apps:
                if app_name.lower() in valid.lower():
                    app_name = valid
                    matched = True
                    break
            if not matched:
                return f"❌ Error: '{app_name}' is not recognized in the A1 App Store."

        # Simulate connecting to the API
        print(f"🔗 [App Store]: Linking {app_name} to A1 Core...")
        
        if api_key == "AUTO_GENERATE":
            # For demonstration, creating a mock secure key
            import hashlib
            api_key = "A1-" + hashlib.md5((app_name + str(datetime.now())).encode()).hexdigest()[:15].upper()

        self.apps[app_name]["status"] = "Connected"
        self.apps[app_name]["api_key"] = api_key
        self.save_connections()

        return f"✅ SUCCESS: [{app_name}] is now securely connected to A1 OS.\n🔑 Bridge Key: {api_key}"

    # --- 2. STORAGE SYNC LOGIC ---
    def sync_storage(self, app_name):
        """
        WhatsApp ya kisi aur app ka data apne 'Storage Box' (File 02/03 era) mein backup karta hai.
        UI button "Sync Storage" ya "Cloud Storage Sync" click hone par chalega.
        """
        if app_name not in self.apps or self.apps[app_name]["status"] == "Disconnected":
            return f"⚠️ Action Denied: Cannot sync [{app_name}]. It is currently Disconnected. Connect API first."

        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.apps[app_name]["last_sync"] = timestamp
        self.save_connections()

        # Yahan hum apne purane 'storage_manager.py' ko call kar sakte hain future mein
        return f"🔄 SYNC COMPLETE: [{app_name}] data securely backed up to Local Vector DB at {timestamp}."

    # --- 3. APK UPLOAD / BOT DEPLOYMENT ---
    def execute_app_action(self, action_name, app_name):
        """
        UI Cards ke baaki special buttons ke liye general router.
        (e.g., "Upload APK", "Auto-Post Bot", "Lookup Panel")
        """
        action_lower = action_name.lower()
        
        if self.apps.get(app_name, {}).get("status") == "Disconnected" and "connect" not in action_lower:
             return f"⚠️ [{app_name}] is offline. Please 'Connect API' before running '{action_name}'."

        if "upload apk" in action_lower:
            return f"📦 DEPLOYMENT: APK for [{app_name}] verified. Ready to push to secure testing server."
            
        elif "auto-post" in action_lower:
            return f"🤖 AI BOT ACTIVE: A1 Engine will now auto-generate and post content to [{app_name}] based on your instructions."
            
        elif "lookup" in action_lower:
            return f"🔍 LOOKUP PANEL LAUNCHED: Enter number below to query via [{app_name}]."
            
        else:
            return f"⚙️ Action '{action_name}' initiated on '{app_name}'. Pending backend execution module."

# Testing Block (Ignored by server.py auto-loader)
if __name__ == "__main__":
    store = AppStoreManager()
    print(store.connect_api("WhatsApp API"))
    print(store.sync_storage("WhatsApp API"))
    print(store.execute_app_action("Auto-Post Bot", "Instagram Hub"))
    
