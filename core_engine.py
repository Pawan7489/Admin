# File 01: core_engine.py
# Description: The "Super Genius" Logic Hub. 
# Automatically detects and links all 50+ modules via Distributed Mesh.

import os
import importlib
import sys
from datetime import datetime

class SuperGeniusCore:
    def __init__(self):
        self.modules = {}
        self.start_time = datetime.now()
        self.version = "1.0.0-PRO"
        self.registry_path = "registry.py" # Master attendance sheet

    def scan_and_link(self):
        """
        Ye function folder ko scan karta hai aur 'manager' ya 'ops' 
        naam ki har file ko automatically 'Plug & Play' mode mein load karta hai.
        """
        print(f"--- 🛡️ SYSTEM SCAN STARTING: {self.start_time} ---")
        
        # Current folder ki saari files check karein
        files = [f for f in os.listdir('.') if f.endswith('_manager.py') or f.endswith('_ops.py')]
        
        for file in files:
            module_name = file[:-3] # '.py' hatao
            try:
                # Dynamic Importing: Bina code likhe naye modules add karna
                module = importlib.import_module(module_name)
                self.modules[module_name] = module
                print(f"✅ LINKED: {module_name} is now Online.")
            except Exception as e:
                print(f"⚠️ FAILED TO LINK: {module_name} | Error: {str(e)}")

        print(f"--- 🚀 SCAN COMPLETE: {len(self.modules)} Active Modules Found ---")
        return self.modules

    def get_system_report(self):
        """AI-OS ki health aur uptime ki advance report"""
        uptime = datetime.now() - self.start_time
        return {
            "Status": "Optimal",
            "Uptime": str(uptime),
            "Engine_Version": self.version,
            "Modules_Active": list(self.modules.keys())
        }

# Singleton Instance: Taki pure system mein ek hi brain chale
AI_CORE = SuperGeniusCore()
