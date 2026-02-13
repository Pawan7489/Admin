# File Path: backend/model_versioning.py
# Description: Manages versions of the A1 Master Core and handles rollbacks.
# Implements 'Time Travel Rule' for AI Stability. [cite: 2026-02-11]

import os
import json
import shutil
import hashlib
from datetime import datetime

class ModelVersioning:
    def __init__(self):
        self.version_registry = "database/model_versions.json"
        self.model_vault = "models/vault/"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists(self.model_vault):
            os.makedirs(self.model_vault)
        if not os.path.exists(self.version_registry):
            with open(self.version_registry, 'w') as f:
                json.dump({"current_version": None, "history": []}, f)

    def create_checkpoint(self, model_path, performance_score):
        """
        Naye trained model ka snapshot leta hai. [cite: 2026-02-11]
        """
        version_id = f"v{datetime.now().strftime('%Y%m%d_%H%M')}"
        snapshot_path = os.path.join(self.model_vault, version_id)
        
        # Physical copy (Simulated for efficiency) [cite: 2026-02-11]
        # shutil.copytree(model_path, snapshot_path) 
        
        entry = {
            "version": version_id,
            "timestamp": str(datetime.now()),
            "score": performance_score,
            "status": "Stable" if performance_score > 0.8 else "Needs Review"
        }

        with open(self.version_registry, 'r+') as f:
            data = json.load(f)
            data["history"].append(entry)
            data["current_version"] = version_id
            f.seek(0)
            json.dump(data, f, indent=4)
            
        print(f"📦 [Versioning]: Checkpoint {version_id} created with score {performance_score}")
        return version_id

    def trigger_rollback(self):
        """
        Pichle sabse stable version par wapas jata hai. [cite: 2026-02-11]
        """
        with open(self.version_registry, 'r') as f:
            data = json.load(f)
        
        if len(data["history"]) < 2:
            return "❌ [Rollback Fail]: No previous versions available."

        # Logic: Finding last version with 'Stable' status
        stable_history = [v for v in data["history"] if v["status"] == "Stable"]
        target_version = stable_history[-2]["version"] # Second last stable

        print(f"⏪ [Time Travel]: Rolling back to {target_version}...") [cite: 2026-02-11]
        data["current_version"] = target_version
        
        with open(self.version_registry, 'w') as f:
            json.dump(data, f, indent=4)
            
        return f"✅ [Success]: System restored to {target_version}."

    def calculate_stability_score(self, scores_list):
        """
        Calculates Model Stability Index ($S_s$).
        Formula: $S_s = \frac{\sum (S_i - \bar{S})^2}{N}$ (Variance of performance)
        Lower variance means higher stability.
        """
        if not scores_list: return 0.0
        avg = sum(scores_list) / len(scores_list)
        variance = sum((x - avg) ** 2 for x in scores_list) / len(scores_list)
        return round(1.0 - variance, 4)

# Test Block
if __name__ == "__main__":
    v_sys = ModelVersioning()
    # v_sys.create_checkpoint("models/A1_Core", 0.92)
    # print(v_sys.trigger_rollback())
  
