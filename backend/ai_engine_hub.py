# File Path: backend/ai_engine_hub.py
# Description: Advanced Hot-Swap Manager for Local AI Models, APIs, and Ghost Stubs.
# Supports 1-Click Inject and Empty Slot configuration.

import os
import json
from datetime import datetime

class AIEngineManager:
    def __init__(self):
        self.registry_file = "database/engine_registry.json"
        self.local_models_dir = "ai_models/" # Default folder for downloaded model zips
        self._ensure_setup()
        self.load_engines()

    def _ensure_setup(self):
        """Creates the database and models directory if they don't exist."""
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.local_models_dir):
            os.makedirs(self.local_models_dir)
            
        if not os.path.exists(self.registry_file):
            # The "Empty Slot" & Local Model Architecture
            default_engines = {
                "Llama-3-Local": {"type": "Local Path", "status": "Offline", "path": f"{self.local_models_dir}llama3/"},
                "Gemma-Local": {"type": "Local Path", "status": "Offline", "path": f"{self.local_models_dir}gemma/"},
                "Phi-3-Mini-Local": {"type": "Local Path", "status": "Offline", "path": f"{self.local_models_dir}phi3/"},
                "Mistral-7B-Local": {"type": "Local Path", "status": "Offline", "path": f"{self.local_models_dir}mistral7b/"},
                "Qwen-2.5-Local": {"type": "Local Path", "status": "Offline", "path": f"{self.local_models_dir}qwen2.5/"},
                "GPT-4-API": {"type": "API Key", "status": "Empty Slot", "key": ""},
                "Claude-3-API": {"type": "API Key", "status": "Empty Slot", "key": ""},
                "Voice_Module": {"type": "Ghost Stub", "status": "Placeholder", "path": ""}
            }
            with open(self.registry_file, 'w') as f:
                json.dump(default_engines, f, indent=4)

    def load_engines(self):
        with open(self.registry_file, 'r') as f:
            try:
                self.engines = json.load(f)
            except:
                self.engines = {}

    def save_engines(self):
        with open(self.registry_file, 'w') as f:
            json.dump(self.engines, f, indent=4)

    # --- 1-CLICK INJECT LOGIC ---
    def inject_engine(self, engine_name):
        """
        UI ke '1-Click Inject' button se call hota hai.
        Checks if it's a Local model, API, or Ghost Stub and processes accordingly.
        """
        if engine_name not in self.engines:
            return f"❌ Error: Engine '{engine_name}' not found in A1 Registry."

        engine_data = self.engines[engine_name]
        engine_type = engine_data["type"]

        # 1. Handling Ghost Stubs (Placeholder Logic)
        if engine_type == "Ghost Stub":
            return f"👻 GHOST PROTOCOL: '{engine_name}' is a placeholder. Main code continues to run without crashing. Waiting for future module update."

        # 2. Handling Empty API Slots
        if engine_type == "API Key" and engine_data["status"] == "Empty Slot":
            if not engine_data.get("key"):
                return f"⚠️ EMPTY SLOT: '{engine_name}' has no API Key configured. Please add the key via Settings to inject."
            
        # 3. Handling Local Models
        if engine_type == "Local Path":
            model_path = engine_data["path"]
            # Just simulating the boot-up sequence
            print(f"🧠 [Engine Hub]: Loading weights from {model_path}...")
            
            # Switch off all other local models to save RAM (Solo Mode Rule)
            for name, data in self.engines.items():
                if data["type"] == "Local Path" and data["status"] == "Connected":
                    self.engines[name]["status"] = "Offline"
                    print(f"💤 [Engine Hub]: Unloaded {name} to free up memory.")

        # Activate the requested engine
        self.engines[engine_name]["status"] = "Connected"
        self.engines[engine_name]["last_injected"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.save_engines()

        return f"🚀 INJECTION SUCCESS: [{engine_name}] is now the Active Engine."

    def get_engine_status(self):
        """Returns the current grid status for the UI Dashboard"""
        if not self.engines:
            return "📭 Engine Hub is empty."
            
        output = "\n🧠 --- A1 ENGINE HUB STATUS --- 🧠\n"
        output += f"{'NAME':<20} | {'TYPE':<15} | {'STATUS':<15}\n"
        output += "-" * 55 + "\n"
        
        for name, data in self.engines.items():
            status_color = "🟢 " if data['status'] == "Connected" else ("🟡 " if data['status'] == "Empty Slot" else "🔴 ")
            output += f"{name:<20} | {data['type']:<15} | {status_color + data['status']:<15}\n"
                
        output += "-" * 55 + "\n"
        return output

# Test Execution (Ignored by Master Server)
if __name__ == "__main__":
    hub = AIEngineManager()
    print(hub.inject_engine("Llama-3-Local"))
    print(hub.inject_engine("Voice_Module"))
    print(hub.get_engine_status())
      
