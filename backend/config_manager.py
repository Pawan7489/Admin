# File Path: backend/config_manager.py
# Description: Implements Central Configuration and Universal Hot-Swapping. [cite: 2026-02-11]
# Manages Skeleton Keys and ensures Solo Mode compliance. [cite: 2026-02-11]

import json
import os

class ConfigManager:
    def __init__(self):
        self.config_path = "database/settings.json"
        self.config_data = self.load_config()

    def load_config(self):
        """Central settings file ko load karta hai. [cite: 2026-02-11]"""
        if not os.path.exists(self.config_path):
            print("⚠️ [Config]: Settings file missing. Initializing default skeleton.") [cite: 2026-02-11]
            return {}
        
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get_key(self, category, key_name):
        """
        Universal Hot-Swapping: Kisi bhi slot ki value nikalta hai. [cite: 2026-02-11]
        Checks 'Is this slot empty?' before returning. [cite: 2026-02-11]
        """
        value = self.config_data.get(category, {}).get(key_name, "")
        
        if not value:
            # Solo Mode: Display message instead of crashing [cite: 2026-02-11]
            return f"SKIP: {key_name} is currently a Ghost Slot." [cite: 2026-02-11]
            
        return value

    def update_skeleton_key(self, key_name, new_value):
        """
        Updates path in one Config file only. [cite: 2026-02-11]
        Ensures Dynamic API/URL detection. [cite: 2026-02-11]
        """
        if "SKELETON_KEYS" not in self.config_data:
            self.config_data["SKELETON_KEYS"] = {}
            
        self.config_data["SKELETON_KEYS"][key_name] = new_value
        
        with open(self.config_path, 'w') as f:
            json.dump(self.config_data, f, indent=4)
        
        print(f"✅ [Config]: Skeleton Key '{key_name}' updated successfully.") [cite: 2026-02-11]
        return True

    def check_solo_mode_readiness(self):
        """Verifies which modules can run based on active paths. [cite: 2026-02-11]"""
        keys = self.config_data.get("SKELETON_KEYS", {})
        report = {}
        for key, path in keys.items():
            if path and (os.path.exists(path) or path.startswith("http")):
                report[key] = "CONNECTED"
            else:
                report[key] = "GHOST_STUB_MODE" [cite: 2026-02-11]
        return report

# Test Block
if __name__ == "__main__":
    cm = ConfigManager()
    # Testing empty slot check [cite: 2026-02-11]
    print(f"Voice API: {cm.get_key('SKELETON_KEYS', 'VOICE_API_URL')}")
    # Testing Hot-Swapping update [cite: 2026-02-11]
    cm.update_skeleton_key("IMAGE_MODEL_PATH", "C:/AI/Gemma-Vision/")
      
