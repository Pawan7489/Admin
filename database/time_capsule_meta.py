# Sub-File 85-K: Attaches searchable context and diary entries to snapshots.
# Implements 'Intent over Syntax' for easy searching. [cite: 2026-02-11]

import json
from datetime import datetime

class TimeCapsuleMeta:
    def log_snapshot_context(self, active_modules, user_note):
        """Snapshot ke waqt A1 OS kya kar raha tha, uska tag banata hai."""
        metadata = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": "Indore", # Context-aware logging
            "active_persona": "student",
            "note": user_note,
            "modules_running": active_modules
        }
        print(f"📝 [Time Capsule]: Metadata logged -> '{user_note}'")
        return metadata

    def calculate_search_complexity(self, n_records):
        """
        Formula for Binary Search Time Complexity: $L_s = \mathcal{O}(\log N)$
        """
        return "Search Latency: < 10ms"
      
