# File Path: backend/registry.py
# Description: Acts as an attendance sheet for all active modules and drives. [cite: 2026-02-11]
# Scans Config on startup to register available 'Powers'.

import os
import json
import requests
from datetime import datetime

class MasterRegistry:
    def __init__(self, config_path="database/settings.json"):
        self.config_path = config_path
        self.active_registry = {}
        self.startup_time = datetime.now()

    def perform_morning_roll_call(self):
        """
        Startup scan: Drives, Folders aur APIs ki attendance leta hai. [cite: 2026-02-11]
        """
        print(f"📋 [Registry]: Starting Morning Roll Call at {self.startup_time}...")
        
        if not os.path.exists(self.config_path):
            return "❌ [Error]: Config file missing. Cannot register modules."

        with open(self.config_path, 'r') as f:
            config = json.load(f)

        # 1. Scanning Local & Distributed Drives [cite: 2026-02-11]
        for drive_name, path in config.get("DRIVE_PATHS", {}).items():
            if os.path.exists(path):
                self.active_registry[drive_name] = {"status": "Active", "type": "Storage"}
                print(f"✅ [Registry]: {drive_name} is PRESENT at {path}")
            else:
                print(f"❌ [Registry]: {drive_name} is ABSENT. Skipping...")

        # 2. Scanning API Slots (Skeleton Keys) [cite: 2026-02-11]
        for api_name, url in config.get("SKELETON_KEYS", {}).items():
            if url and url != "SKIP":
                self.active_registry[api_name] = {"status": "Active", "type": "API"}
                print(f"📡 [Registry]: API {api_name} is REGISTERED.")
            else:
                self.active_registry[api_name] = {"status": "Ghost", "type": "Placeholder"}

        self._save_active_manifest()
        return self.calculate_availability_ratio()

    def calculate_availability_ratio(self):
        """
        Calculates the percentage of available modules.
        Formula: $A_r = \frac{M_{active}}{M_{total}} \times 100$
        """
        total = len(self.active_registry)
        active = sum(1 for m in self.active_registry.values() if m["status"] == "Active")
        ratio = (active / total) * 100 if total > 0 else 0
        return f"📊 System Readiness: {round(ratio, 2)}%"

    def _save_active_manifest(self):
        """Active members ki list save karta hai."""
        with open("database/active_manifest.json", "w") as f:
            json.dump(self.active_registry, f, indent=4)

# Test Block
if __name__ == "__main__":
    # Mocking a settings file for test
    if not os.path.exists('database'): os.makedirs('database')
    mock_settings = {
        "DRIVE_PATHS": {"DRIVE_D": "D:/", "DRIVE_E": "E:/"},
        "SKELETON_KEYS": {"VOICE_API": "SKIP", "VISION_API": "http://localhost:8000"}
    }
    with open("database/settings.json", "w") as f: json.dump(mock_settings, f)
    
    registry = MasterRegistry()
    print(registry.perform_morning_roll_call())
  
