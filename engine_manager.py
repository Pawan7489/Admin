# File: engine_manager.py
# Description: Manages Unlimited AI Engines (Start/Stop/Add/Remove)

import json
import os
from datetime import datetime

class EngineRegistry:
    def __init__(self):
        self.registry_file = "engine_inventory.json"
        self.load_registry()

    def load_registry(self):
        """Database load karta hai"""
        if not os.path.exists(self.registry_file):
            self.engine_data = {}
            self.save_registry()
        else:
            try:
                with open(self.registry_file, "r") as f:
                    self.engine_data = json.load(f)
            except:
                self.engine_data = {}

    def save_registry(self):
        """Database save karta hai"""
        with open(self.registry_file, "w") as f:
            json.dump(self.engine_data, f, indent=4)

    def add_engine(self, name, engine_type, path_or_key):
        """
        Naya Engine Register karta hai.
        Name: User ka diya hua naam (e.g., Jarvis_Brain, Coding_Model)
        Type: Llama, GPT, Mistral, HuggingFace
        Path: Local path ya API Key
        """
        if name in self.engine_data:
            return f"⚠️ Warning: '{name}' pehle se list mein hai."

        self.engine_data[name] = {
            "type": engine_type,
            "source": path_or_key,
            "status": "STOPPED 🔴",  # Default state off rahegi
            "added_on": str(datetime.now().strftime("%Y-%m-%d"))
        }
        self.save_registry()
        return f"✅ Success: Engine '{name}' add ho gaya (Status: STOPPED)."

    def remove_engine(self, name):
        """Engine ko list se hatata hai"""
        if name in self.engine_data:
            del self.engine_data[name]
            self.save_registry()
            return f"🗑️ Engine '{name}' deleted successfully."
        else:
            return f"❌ Error: '{name}' nahi mila."

    def start_engine(self, name):
        """Engine ko ON karta hai"""
        if name not in self.engine_data:
            return f"❌ Error: '{name}' register nahi hai."
        
        # Check if already running
        if self.engine_data[name]['status'] == "RUNNING 🟢":
            return f"⚠️ '{name}' pehle se chal raha hai!"

        # Logic to actually load model would go here (Simulation for now)
        self.engine_data[name]['status'] = "RUNNING 🟢"
        self.save_registry()
        return f"🚀 ENGINE STARTED: '{name}' ab active hai aur kaam ke liye taiyar hai."

    def stop_engine(self, name):
        """Engine ko OFF karta hai"""
        if name not in self.engine_data:
            return f"❌ Error: '{name}' register nahi hai."

        if self.engine_data[name]['status'] == "STOPPED 🔴":
            return f"⚠️ '{name}' pehle se band hai."

        # Logic to unload model (free RAM)
        self.engine_data[name]['status'] = "STOPPED 🔴"
        self.save_registry()
        return f"🛑 ENGINE STOPPED: '{name}' ko band kar diya gaya hai."

    def list_engines(self):
        """Sabhi Engines aur unka Status dikhata hai"""
        if not self.engine_data:
            return "📭 Engine Room Khali Hai. 'engine add' command use karein."

        output = "\n⚙️ --- AI ENGINE CONTROL ROOM --- ⚙️\n"
        output += f"{'NAME':<20} | {'TYPE':<15} | {'STATUS':<15}\n"
        output += "-" * 60 + "\n"

        for name, details in self.engine_data.items():
            output += f"{name:<20} | {details['type']:<15} | {details['status']:<15}\n"
        
        output += "-" * 60 + "\n"
        return output
      
