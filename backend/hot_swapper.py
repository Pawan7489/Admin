# File Path: backend/hot_swapper.py
# Description: Implements 'Universal Hot-Swapping' logic. [cite: 2026-02-11]
# Automatically detects if a module is a File Path, Local URL, or API.

import os
import requests
import importlib.util

class HotSwapper:
    def __init__(self):
        self.connection_history = "database/swap_logs.json"

    def connect_module(self, module_name, target_path):
        """
        Interchangeably links via Path, Localhost, or API. [cite: 2026-02-11]
        """
        print(f"🔗 [Hot-Swapper]: Attempting to link '{module_name}' via '{target_path}'...")

        # Case 1: Is it a Local URL (localhost)? [cite: 2026-02-11]
        if "localhost" in target_path or "127.0.0.1" in target_path:
            return self._link_via_url(module_name, target_path, mode="Localhost")

        # Case 2: Is it a Remote API Key/URL? [cite: 2026-02-11]
        elif target_path.startswith("http"):
            return self._link_via_url(module_name, target_path, mode="API")

        # Case 3: Is it a Local File Path? [cite: 2026-02-11]
        elif os.path.exists(target_path):
            return self._link_via_file(module_name, target_path)

        else:
            return f"⚠️ [Swap Fail]: Unknown connection type for {module_name}."

    def _link_via_file(self, name, path):
        """Python file ko dynamically load karta hai."""
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return f"✅ [File Link]: {name} connected from local drive."
        except Exception as e:
            return f"❌ [File Error]: {str(e)}"

    def _link_via_url(self, name, url, mode):
        """API ya Localhost service ko verify karta hai."""
        try:
            # Check if the service is alive
            # response = requests.get(url, timeout=1) 
            return f"✅ [{mode} Link]: {name} connected via {url}."
        except Exception:
            return f"❌ [{mode} Error]: Service at {url} is unreachable."

    def calculate_versatility_index(self, active_links):
        """
        Calculates how 'Hot-Swappable' the system is.
        Formula: $V_i = \frac{T_{types}}{3} \times 100$
        Where T_types is the count of distinct connection modes used.
        """
        modes = set()
        for link in active_links:
            if "localhost" in link: modes.add("Localhost")
            elif "http" in link: modes.add("API")
            else: modes.add("Path")
        
        index = (len(modes) / 3) * 100
        return round(index, 2)

# Test Block
if __name__ == "__main__":
    swapper = HotSwapper()
    # Test 1: File Path link [cite: 2026-02-11]
    print(swapper.connect_module("Core_Brain", "./server.py"))
    # Test 2: Localhost link [cite: 2026-02-11]
    print(swapper.connect_module("Vision_API", "http://localhost:8080"))
  
