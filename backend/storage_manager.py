# File: storage_manager.py
# Description: Manages Unlimited Cloud/Drive Storage Connections

import json
import os
from datetime import datetime

class StorageRegistry:
    def __init__(self):
        self.registry_file = "storage_inventory.json"
        self.load_registry()

    def load_registry(self):
        """Database load karta hai (agar nahi hai to naya banata hai)"""
        if not os.path.exists(self.registry_file):
            self.storage_data = {}
            self.save_registry()
        else:
            try:
                with open(self.registry_file, "r") as f:
                    self.storage_data = json.load(f)
            except:
                self.storage_data = {}

    def save_registry(self):
        """Database save karta hai"""
        with open(self.registry_file, "w") as f:
            json.dump(self.storage_data, f, indent=4)

    def add_storage(self, name, provider, credentials):
        """
        Naya Storage Box add karta hai.
        Name: User ka diya hua naam (e.g., Personal_Drive, Office_Cloud)
        Provider: Service name (Google, AWS, Dropbox, FTP)
        Credentials: URL ya API Key
        """
        if name in self.storage_data:
            return f"⚠️ Warning: '{name}' naam pehle se maujood hai. Alag naam use karein."

        self.storage_data[name] = {
            "provider": provider,
            "credentials": credentials, # Note: Production me ise encrypt karna chahiye
            "added_on": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "status": "Active"
        }
        self.save_registry()
        return f"✅ Success: '{name}' ({provider}) list mein add ho gaya!"

    def remove_storage(self, name):
        """Storage hatata hai"""
        if name in self.storage_data:
            del self.storage_data[name]
            self.save_registry()
            return f"🗑️ Deleted: '{name}' ko list se hata diya gaya."
        else:
            return f"❌ Error: '{name}' naam ka koi storage nahi mila."

    def list_storage(self):
        """Sabhi connected drives ki list dikhata hai"""
        if not self.storage_data:
            return "📭 Storage List Khali Hai. 'storage add' command use karein."

        output = "\n📂 --- CONNECTED STORAGE INVENTORY --- 📂\n"
        output += f"{'NAME':<20} | {'PROVIDER':<15} | {'ADDED ON':<20}\n"
        output += "-" * 60 + "\n"

        for name, details in self.storage_data.items():
            output += f"{name:<20} | {details['provider']:<15} | {details['added_on']:<20}\n"
        
        output += "-" * 60 + "\n"
        output += f"Total Connections: {len(self.storage_data)}"
        return output

    def get_credential(self, name):
        """Kisi specific drive ki API/URL nikalta hai use karne ke liye"""
        if name in self.storage_data:
            return self.storage_data[name]['credentials']
        return None
      
