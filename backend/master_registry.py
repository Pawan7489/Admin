# File Path: backend/master_registry.py
# Description: Implements 'Master Blueprint' & 'Empty Slot' Configuration.
# Scans all distributed drives and modules to register active members.

import os
import json
import socket
from datetime import datetime

class MasterBlueprint:
    def __init__(self):
        self.config_file = "database/settings.json" # Skeleton Keys file
        self.registry_log = "database/active_registry.json"
        self._initialize_skeleton_keys()

    def _initialize_skeleton_keys(self):
        """Generates empty slots for future tools (Skeleton Keys)."""
        if not os.path.exists('database'):
            os.makedirs('database')

        if not os.path.exists(self.config_file):
            # Pre-defined but empty slots for future integration
            skeleton_keys = {
                "VOICE_API_URL": "",
                "IMAGE_MODEL_PATH": "",
                "CLOUD_SECURE_BRIDGE": "",
                "GPU_ACCELERATOR_NODE": "",
                "EXTERNAL_DRIVE_PATH": "D:/A1_Storage"
            }
            with open(self.config_file, 'w') as f:
                json.dump(skeleton_keys, f, indent=4)

    def scan_distributed_units(self):
        """
        The 'Bridge' Rule: Instantly locates and links scattered files across drives.
        Checks for Solo Mode compliance to prevent system crashes.
        """
        active_members = {}
        print("🔍 [Master Registry]: Scanning Distributed Mesh...")

        # 1. Scanning Core Backend Modules
        core_path = os.path.dirname(__file__)
        for file in os.listdir(core_path):
            if file.endswith("_manager.py") or file.endswith("_hub.py"):
                module_name = file.replace(".py", "")
                active_members[module_name] = {"status": "Active", "location": "Local/Backend"}

        # 2. Scanning Skeleton Key Slots (Empty Slot Rule)
        with open(self.config_file, 'r') as f:
            keys = json.load(f)
            for key, path in keys.items():
                if path and os.path.exists(path):
                    active_members[key] = {"status": "Linked", "location": path}
                else:
                    # Solo Mode: Simply log as missing instead of crashing
                    active_members[key] = {"status": "Offline/Missing", "location": "N/A"}

        # 3. Network Identity Check
        active_members["System_Node"] = {
            "hostname": socket.gethostname(),
            "ip": socket.gethostbyname(socket.gethostname()),
            "timestamp": str(datetime.now())
        }

        self._save_active_registry(active_members)
        return active_members

    def _save_active_registry(self, data):
        """Maintains the attendance sheet for the AI."""
        with open(self.registry_log, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"📋 [Master Registry]: Attendance sheet updated with {len(data)} nodes.")

    def check_power_availability(self, tool_name):
        """Allows the AI to 'know' instantly what powers it has available right now."""
        with open(self.registry_log, 'r') as f:
            registry = json.load(f)
            status = registry.get(tool_name, {}).get("status", "Unknown")
            
            if status == "Offline/Missing":
                return False, f"⚠️ {tool_name} not detected, skipping..." # Solo Mode message
            return True, f"✅ {tool_name} is active."

# Start-up Auto-Scan
if __name__ == "__main__":
    blueprint = MasterBlueprint()
    blueprint.scan_distributed_units()
    print(blueprint.check_power_availability("VOICE_API_URL"))
                  
