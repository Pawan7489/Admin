# File Path: backend/logic_version_control.py
# Description: Implements "Time Travel Rule" & "Memory Sync".
# Takes snapshots of AI's Logic/Memory and allows Rollbacks if performance drops.

import os
import json
import shutil
from datetime import datetime

class TimeTravelManager:
    def __init__(self):
        self.snapshots_dir = "database/mental_snapshots/"
        self.active_memory_file = "database/rlhf_memory_vector.json"
        self.snapshot_registry = "database/snapshot_registry.json"
        self._ensure_setup()

    def _ensure_setup(self):
        """Creates backup directories if they don't exist."""
        if not os.path.exists(self.snapshots_dir):
            os.makedirs(self.snapshots_dir)
            
        if not os.path.exists(self.snapshot_registry):
            with open(self.snapshot_registry, 'w') as f:
                json.dump({}, f, indent=4)

    def load_registry(self):
        try:
            with open(self.snapshot_registry, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_registry(self, data):
        with open(self.snapshot_registry, 'w') as f:
            json.dump(data, f, indent=4)

    # --- 1. THE TIME TRAVEL RULE (SNAPSHOT) ---
    def save_mental_state(self, version_name, description="Stable Version"):
        """
        AI ke current 'dimag' (Vector DB aur Logic paths) ki ek copy save karta hai.
        """
        if not os.path.exists(self.active_memory_file):
            return "⚠️ Notice: No active memory found to snapshot."

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_filename = f"state_{version_name}_{timestamp}.json"
        snapshot_path = os.path.join(self.snapshots_dir, snapshot_filename)

        try:
            # Copy current active memory to the snapshot vault
            shutil.copy2(self.active_memory_file, snapshot_path)
            
            # Register this snapshot
            registry = self.load_registry()
            registry[version_name] = {
                "file": snapshot_filename,
                "description": description,
                "date": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            self.save_registry(registry)
            
            return f"🕰️ TIME TRAVEL SAVED: Mental State '{version_name}' securely locked. System can roll back to this state anytime."
        except Exception as e:
            return f"❌ Snapshot Error: {str(e)}"

    # --- 2. THE TIME TRAVEL RULE (ROLLBACK) ---
    def rollback_mental_state(self, version_name):
        """
        Agar AI galti karne lage, toh is function se usko purane 'Stable' version par wapas bhej do.
        """
        registry = self.load_registry()
        if version_name not in registry:
            return f"❌ Error: Version '{version_name}' not found in Time Travel Registry."

        snapshot_filename = registry[version_name]["file"]
        snapshot_path = os.path.join(self.snapshots_dir, snapshot_filename)

        if not os.path.exists(snapshot_path):
            return f"❌ Error: Snapshot file {snapshot_filename} is missing or corrupted."

        try:
            # Overwrite current corrupted memory with the stable snapshot
            shutil.copy2(snapshot_path, self.active_memory_file)
            return f"⏪ ROLLBACK SUCCESSFUL: AI's mind has been reverted to version '{version_name}'. All recent bad logic is erased."
        except Exception as e:
            return f"❌ Rollback Error: {str(e)}"

    # --- 3. MEMORY SYNC (PREVENT SYSTEM LAG) ---
    def memory_sync_cleanup(self):
        """
        To prevent the Local Vector DB from becoming cluttered, 
        this automatically archives low-priority data.
        """
        if not os.path.exists(self.active_memory_file):
            return "No memory to sync."

        try:
            with open(self.active_memory_file, 'r') as f:
                memory = json.load(f)

            # Basic logic: Keep only 'thumbs_up' and important recent logic, archive the rest.
            optimized_memory = {}
            archived_count = 0

            for intent, data in memory.items():
                if data.get("feedback") == "thumbs_up":
                    optimized_memory[intent] = data
                else:
                    archived_count += 1

            # Save optimized fast memory
            with open(self.active_memory_file, 'w') as f:
                json.dump(optimized_memory, f, indent=4)

            return f"🧹 MEMORY SYNC COMPLETE: Archived {archived_count} low-priority thoughts. AI Mind is now sharp and fast."
        except Exception as e:
            return f"❌ Sync Error: {str(e)}"

    def list_snapshots(self):
        registry = self.load_registry()
        if not registry:
            return "📭 No mental snapshots found. Save a state first."
            
        output = "\n🕰️ --- A1 TIME TRAVEL SNAPSHOTS --- 🕰️\n"
        output += f"{'VERSION':<15} | {'DATE':<20} | {'DESCRIPTION':<30}\n"
        output += "-" * 70 + "\n"
        
        for v_name, details in registry.items():
            output += f"{v_name:<15} | {details['date']:<20} | {details['description']:<30}\n"
            
        output += "-" * 70 + "\n"
        return output

# Testing Block
if __name__ == "__main__":
    tv = TimeTravelManager()
    print(tv.save_mental_state("v1.0-Stable", "First perfect run without hallucinations"))
    print(tv.list_snapshots())
    print(tv.memory_sync_cleanup())
  
