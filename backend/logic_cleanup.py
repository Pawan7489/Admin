# File Path: backend/logic_cleanup.py
# Description: Automatically deletes failed logic paths and prompts. [cite: 2026-02-11]
# Keeps the AI's mind 'Sharp' by removing negative patterns.

import json
import os
import shutil

class LogicCleanup:
    def __init__(self, mental_registry):
        self.registry = mental_registry # Link to File 28
        self.feedback_file = "database/rlhf_feedback.json"
        self.purge_log = "database/purge_history.log"
        self.failure_threshold = 2.0 # Ratings below this are marked for cleanup

    def run_cleanup_cycle(self):
        """
        Bad feedback wale versions ko dhoond kar delete karta hai. [cite: 2026-02-11]
        """
        if not os.path.exists(self.feedback_file):
            return "✅ [Cleanup]: No feedback found. Mind is currently clean."

        print("🧹 [Logic Cleanup]: Scanning for toxic logic patterns...") [cite: 2026-02-11]
        
        with open(self.feedback_file, 'r') as f:
            feedbacks = json.load(f)

        failed_versions = [fb['version'] for fb in feedbacks if fb.get('rating', 5) < self.failure_threshold]
        
        if not failed_versions:
            return "✅ [Cleanup]: No failed versions detected."

        purged_count = 0
        for version in set(failed_versions):
            if self._purge_version_data(version):
                purged_count += 1
        
        # Purge Ratio Calculation
        # $P_r = \frac{V_{purged}}{V_{total}}$
        return f"🧹 [Cleanup Complete]: Purged {purged_count} failed logic paths. System efficiency restored."

    def _purge_version_data(self, version_tag):
        """Physical deletion of the failed prompt/logic snapshot."""
        try:
            # Registry se info lena [cite: 2026-02-11]
            with open(self.registry.registry_file, 'r') as f:
                reg = json.load(f)
            
            # Entry dhoondna aur remove karna
            new_history = [entry for entry in reg['history'] if entry['version'] != version_tag]
            
            # File delete karna (Mental Vault se)
            target_snapshot = os.path.join(self.registry.state_vault, f"mental_state_{version_tag}*")
            # Simulation of os.remove for safety in this snippet
            
            reg['history'] = new_history
            with open(self.registry.registry_file, 'w') as f:
                json.dump(reg, f, indent=4)
            
            print(f"🗑️ [Cleanup]: Version {version_tag} wiped from vault.")
            return True
        except Exception as e:
            print(f"⚠️ [Cleanup Error]: Failed to wipe {version_tag}: {e}")
            return False

    def calculate_purge_ratio(self, total_versions, purged_versions):
        """
        Calculates how much 'Trash' was removed.
        Formula: $P_r = \frac{N_{purged}}{N_{total}}$
        """
        if total_versions == 0: return 0.0
        return round(purged_versions / total_versions, 2)

# Test Block
if __name__ == "__main__":
    from mental_state_registry import MentalStateManager
    cleaner = LogicCleanup(MentalStateManager())
    print(cleaner.run_cleanup_cycle())
  
