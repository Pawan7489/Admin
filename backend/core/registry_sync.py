# File: backend/core/registry_sync.py
# Purpose: Scans active drives and APIs on the Master Server.
# Strategy: "Master Blueprint" Registry - AI knows its powers instantly.

import os
import json

class A1Registry:
    def __init__(self):
        self.config_path = "~/a1-os/config/settings.json"
        print("📁 [Registry]: Scanning Master Brain resources...")

    def sync_powers(self):
        """
        [cite: 2026-02-11] Checks which 'Skeleton Keys' are filled.
        """
        with open(os.path.expanduser(self.config_path), 'r') as f:
            settings = json.load(f)
            
        active_tools = []
        for key, value in settings.items():
            if value: # Agar slot khali nahi hai
                active_tools.append(key)
        
        print(f"⚡ [Status]: AI current powers: {active_tools}")
        return active_tools

# Logic: Agar 'STRIPE_KEY' hai toh 'Finance' module unlock hoga.
# Agar 'MAPBOX_KEY' hai toh 'Geo-Intelligence' unlock hoga.
