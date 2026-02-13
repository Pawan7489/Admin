# File Path: backend/relevance_engine.py
# Description: Implements 'Relevance Score' and 'Musk Rule' for DB Optimization.
# Automatically archives or deletes low-priority data to maintain system speed.

import json
import os
import time
from datetime import datetime

class RelevanceEngine:
    def __init__(self):
        self.memory_file = "database/rlhf_memory_vector.json"
        self.archive_file = "database/memory_archive.json"
        self.decay_constant = 0.1 # Logic decay rate
        self._ensure_files()

    def _ensure_files(self):
        """Ensures the existence of memory and archive files."""
        if not os.path.exists('database'):
            os.makedirs('database')
        for f_path in [self.memory_file, self.archive_file]:
            if not os.path.exists(f_path):
                with open(f_path, 'w') as f:
                    json.dump({}, f)

    def calculate_score(self, frequency, last_access_time):
        """
        Calculates the Relevance Score using a time-decay formula.
        Formula: $R = F \cdot e^{-\lambda t}$
        Where:
        - $R$: Relevance Score
        - $F$: Frequency of access
        - $\lambda$: Decay constant
        - $t$: Days since last access
        """
        current_time = time.time()
        seconds_since_access = current_time - last_access_time
        days_since_access = seconds_since_access / (60 * 60 * 24)
        
        import math
        relevance_score = frequency * math.exp(-self.decay_constant * days_since_access)
        return round(relevance_score, 4)

    def optimize_memory(self, threshold=0.5):
        """
        Applies the 'Musk Rule' to remove non-essential data.
        Data below the threshold is moved to the archive.
        """
        print("🧹 [Relevance]: Starting Memory Optimization & Sync...")
        
        with open(self.memory_file, 'r') as f:
            memory = json.load(f)
        
        with open(self.archive_file, 'r') as f:
            archive = json.load(f)

        optimized_memory = {}
        archived_items = 0

        for key, data in memory.items():
            freq = data.get("access_count", 1)
            last_ts = data.get("last_access_timestamp", time.time())
            
            score = self.calculate_score(freq, last_ts)
            data["relevance_score"] = score

            if score >= threshold:
                optimized_memory[key] = data
            else:
                # Archiving low-priority data
                archive[key] = data
                archived_items += 1

        # Save optimized files to maintain infinite context without lag
        with open(self.memory_file, 'w') as f:
            json.dump(optimized_memory, f, indent=4)
        
        with open(self.archive_file, 'w') as f:
            json.dump(archive, f, indent=4)

        return {
            "status": "Optimization Complete",
            "archived_count": archived_items,
            "current_memory_size": len(optimized_memory)
        }

    def update_access(self, key):
        """Updates frequency and timestamp when data is accessed."""
        with open(self.memory_file, 'r') as f:
            memory = json.load(f)
        
        if key in memory:
            memory[key]["access_count"] = memory[key].get("access_count", 0) + 1
            memory[key]["last_access_timestamp"] = time.time()
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory, f, indent=4)
            return True
        return False

# Test Block
if __name__ == "__main__":
    re = RelevanceEngine()
    # Simulating optimization
    result = re.optimize_memory(threshold=0.5)
    print(f"✅ {result['status']}: Archived {result['archived_count']} low-priority items.")
          
