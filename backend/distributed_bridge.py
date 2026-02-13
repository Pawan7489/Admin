# File Path: backend/distributed_bridge.py
# Description: Implements 'The Bridge' Rule for Distributed Execution.
# Links scattered files across Drive D, E, and Secure Clouds into one unit.

import os
import sys
import json
import socket
import requests
from datetime import datetime

class DistributedBridge:
    def __init__(self):
        self.bridge_config = "database/bridge_links.json"
        self._ensure_bridge_setup()

    def _ensure_bridge_setup(self):
        """Bridge configuration ki database check karta hai."""
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.bridge_config):
            # Default placeholders for distributed drives
            default_links = {
                "Drive_D_Node": {"path": "D:/A1_OS_Node/", "status": "Inactive"},
                "Drive_E_Node": {"path": "E:/A1_Brain_Part/", "status": "Inactive"},
                "Cloud_Secure_Unit": {"url": "https://secure-api.a1-os.cloud", "status": "Inactive"}
            }
            with open(self.bridge_config, 'w') as f:
                json.dump(default_links, f, indent=4)

    def link_remote_node(self, node_id, local_path_or_url):
        """
        Naye drive ya cloud node ko system se jorta hai.
        Bridge Rule: Instantly locates and links scattered files.
        """
        with open(self.bridge_config, 'r') as f:
            links = json.load(f)

        links[node_id] = {
            "path": local_path_or_url,
            "status": "Active",
            "linked_at": str(datetime.now())
        }

        # Adding to Python path so AI can import files from other drives
        if os.path.exists(local_path_or_url):
            sys.path.append(local_path_or_url)

        with open(self.bridge_config, 'w') as f:
            json.dump(links, f, indent=4)
        
        return f"🌉 [Bridge]: Node '{node_id}' successfully linked to the Master Brain."

    def execute_distributed_task(self, module_name, function_name, *args):
        """
        Distributed Execution: Files on Drive D or E act as one unit.
        """
        print(f"🚀 [Bridge]: Locating module '{module_name}' across mesh...")
        
        # Solo Mode Compliance: Check if module exists before calling
        try:
            # Dynamic import logic that searches all linked paths
            module = __import__(module_name)
            func = getattr(module, function_name)
            result = func(*args)
            return {"status": "Success", "output": result}
        except ImportError:
            # Solo Mode: Do not crash if a part is missing
            return {"status": "Skipped", "message": f"'{module_name}' not detected, skipping..."}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def sync_mesh_state(self):
        """Mesh ki health check karta hai (Drive connections check)."""
        with open(self.bridge_config, 'r') as f:
            links = json.load(f)
            
        report = {}
        for node, data in links.items():
            path = data.get("path", "")
            if path and os.path.exists(path):
                data["status"] = "Active"
            else:
                data["status"] = "Offline"
            report[node] = data["status"]
            
        with open(self.bridge_config, 'w') as f:
            json.dump(links, f, indent=4)
        return report

# Test Block
if __name__ == "__main__":
    bridge = DistributedBridge()
    # Simulating linking a drive
    print(bridge.link_remote_node("D_Drive_AI", "D:/A1_Modules/"))
    print(bridge.sync_mesh_state())
  
