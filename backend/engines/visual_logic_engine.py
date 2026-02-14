# File Path: backend/visual_logic_engine.py
# Description: Implements 'Visual Logic Builder' and 'Ghost Module' Protocol.
# Handles Universal Hot-Swapping for distributed modules.

import os
import json
import importlib.util
from datetime import datetime

class VisualLogicEngine:
    def __init__(self):
        self.node_registry = "database/node_registry.json"
        self.connection_map = "database/logic_connections.json"
        self._ensure_setup()

    def _ensure_setup(self):
        """Initializes registry files for nodes and their links."""
        if not os.path.exists('database'):
            os.makedirs('database')
        for f_path in [self.node_registry, self.connection_map]:
            if not os.path.exists(f_path):
                with open(f_path, 'w') as f:
                    json.dump({}, f)

    # --- 1. GHOST MODULE PROTOCOL ---
    def execute_ghost_stub(self, module_name):
        """
        Placeholder function for future features.
        Ensures the system 'fills the ghost body' without breaking the main code.
        """
        print(f"👻 [Ghost]: '{module_name}' is not yet ready. Skipping execution to prevent crash...")
        return f"Ghost Stub Active: {module_name} is in standby mode."

    # --- 2. UNIVERSAL HOT-SWAPPING ---
    def detect_connection_type(self, path_or_url):
        """
        Automatically detects if a module is linked via File Path, URL, or API.
        """
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return "Local_URL/API"
        elif os.path.exists(path_or_url):
            return "File_Path"
        elif len(path_or_url) > 20: # Heuristic for API keys
            return "API_Key"
        else:
            return "Unknown/Ghost"

    # --- 3. NODE-TO-NODE CONNECTIVITY ---
    def register_node(self, node_id, source_type, connection_string):
        """
        Registers a new functional node in the visual logic builder.
        """
        conn_type = self.detect_connection_type(connection_string)
        
        node_data = {
            "id": node_id,
            "type": source_type,
            "connection": connection_string,
            "detected_as": conn_type,
            "status": "Registered",
            "timestamp": str(datetime.now())
        }

        with open(self.node_registry, 'r') as f:
            nodes = json.load(f)
        
        nodes[node_id] = node_data
        
        with open(self.node_registry, 'w') as f:
            json.dump(nodes, f, indent=4)
        
        return f"✅ Node '{node_id}' registered as {conn_type}."

    def link_logic(self, source_node, target_node):
        """
        Connects two nodes, e.g., dragging a Hosting node to a Domain node.
        """
        with open(self.connection_map, 'r') as f:
            links = json.load(f)

        link_id = f"{source_node}_TO_{target_node}"
        links[link_id] = {
            "from": source_node,
            "to": target_node,
            "active": True
        }

        with open(self.connection_map, 'w') as f:
            json.dump(links, f, indent=4)
        
        return f"🔗 Logic Link Established: {source_node} ---> {target_node}"

# Test Block
if __name__ == "__main__":
    vle = VisualLogicEngine()
    # Registering a local file node
    print(vle.register_node("WP_Installer", "Hosting", "backend/web_injector.py"))
    # Registering an API node (Ghost/Placeholder)
    print(vle.register_node("Voice_AI", "Voice", "https://api.voice-gen.local"))
    # Linking them
    print(vle.link_logic("WP_Installer", "Voice_AI"))
  
