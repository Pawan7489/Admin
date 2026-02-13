# File Path: backend/mental_state_registry.py
# Description: Implements 'Semantic Versioning for Logic'. [cite: 2026-02-11]
# Versions AI Thinking Paths, Prompts, and successful Mental States for Roll-back.

import os
import json
import shutil
from datetime import datetime

class MentalStateManager:
    def __init__(self):
        self.registry_file = "database/mental_version_registry.json"
        self.prompt_dir = "backend/prompts/templates/"
        self.state_vault = "database/mental_vault/"
        self._ensure_setup()

    def _ensure_setup(self):
        """Directories aur registry file initialize karta hai."""
        for path in [self.state_vault, self.prompt_dir, "database"]:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
        if not os.path.exists(self.registry_file):
            with open(self.registry_file, 'w') as f:
                json.dump({"current_version": "1.0.0", "history": []}, f)

    def commit_mental_state(self, version_tag, logic_description):
        """
        AI ki current 'Soch' (Prompts + Logic Tree) ka snapshot leta hai. [cite: 2026-02-11]
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"mental_state_{version_tag}_{timestamp}"
        snapshot_path = os.path.join(self.state_vault, snapshot_name)
        
        # Archiving current prompt templates
        shutil.make_archive(snapshot_path, 'zip', self.prompt_dir)
        
        # Updating Registry
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)
            
        entry = {
            "version": version_tag,
            "timestamp": str(datetime.now()),
            "description": logic_description,
            "snapshot_file": f"{snapshot_name}.zip",
            "status": "Stable"
        }
        registry["history"].append(entry)
        registry["current_version"] = version_tag
        
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=4)
            
        return f"🕰️ [Time Travel]: Mental State '{version_tag}' committed to vault." [cite: 2026-02-11]

    def rollback_to_version(self, target_version):
        """
        AI ko pichle successful mental state par wapas le jata hai. [cite: 2026-02-11]
        """
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)
            
        target_entry = next((item for item in registry["history"] if item["version"] == target_version), None)
        
        if not target_entry:
            return f"❌ [Error]: Version {target_version} not found in Time Travel vault."

        # Extracting the old logic/prompts
        snapshot_path = os.path.join(self.state_vault, target_entry["snapshot_file"])
        shutil.unpack_archive(snapshot_path, self.prompt_dir, 'zip')
        
        registry["current_version"] = target_version
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=4)
            
        return f"⏪ [Roll-Back]: System has traveled back to Mental State '{target_version}'." [cite: 2026-02-11]

    def calculate_logic_stability(self, success_rate, iteration_count):
        """
        Calculates if the current logic version is 'Stable' enough to commit.
        Formula: $S = \frac{\sum_{i=1}^{n} Success_i}{n} \times 100$
        """
        stability_score = (success_rate / iteration_count) * 100
        return round(stability_score, 2)

# Test Block
if __name__ == "__main__":
    ms = MentalStateManager()
    # Simulating a commit of version 1.0.5 [cite: 2026-02-11]
    print(ms.commit_mental_state("v1.0.5", "Fixed WordPress injection logic for subdomains."))
  
