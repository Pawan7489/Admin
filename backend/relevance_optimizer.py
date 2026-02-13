# File Path: backend/relevance_optimizer.py
# Description: Implements the 'Relevance Score' logic to keep the AI's mind sharp.
# Automatically archives or deletes low-priority data based on access frequency and age.

import os
import json
import time
import math
from datetime import datetime

class RelevanceOptimizer:
    def __init__(self):
        self.vector_db_path = "database/rlhf_memory_vector.json"
        self.archive_path = "database/memory_archive.json"
        self.decay_constant = 0.05  # Lambda: Rate at which information is forgotten
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'):
            os.makedirs('database')
        for f in [self.vector_db_path, self.archive_path]:
            if not os.path.exists(f):
                with open(f, 'w') as file:
                    json.dump({}, file)

    def calculate_relevance(self, frequency, last_access_time):
        """
        Calculates the relevance score using an Exponential Decay model.
        Formula: $R(t) = F \cdot e^{-\lambda t}$
        """
        current_time = time.time()
        # Time elapsed in days
        t = (current_time - last_access_time) / (60 * 60 * 24)
        
        relevance_score = frequency * math.exp(-self.decay_constant * t)
        return round(relevance_score, 4)

    def deep_clean_protocol(self, threshold=0.1):
        """
        Scans the Vector DB and moves low-relevance data to the archive.
        """
        print("🧹 [Optimizer]: Starting Deep Clean Protocol...")
        
        with open(self.vector_db_path, 'r') as f:
            db = json.load(f)
        
        with open(self.archive_path, 'r') as f:
            archive = json.load(f)

        new_db = {}
        cleaned_count = 0

        for key, data in db.items():
            freq = data.get('access_count', 1)
            last_ts = data.get('last_access_timestamp', time.time())
            
            score = self.calculate_relevance(freq, last_ts)
            
            if score >= threshold:
                data['relevance_score'] = score
                new_db[key] = data
            else:
                # Move to archive instead of permanent deletion for safety
                archive[key] = data
                cleaned_count += 1

        # Save the optimized DB
        with open(self.vector_db_path, 'w') as f:
            json.dump(new_db, f, indent=4)
        
        with open(self.archive_path, 'w') as f:
            json.dump(archive, f, indent=4)

        return f"✅ [Clean Complete]: {cleaned_count} low-priority items moved to archive. System speed optimized."

    def track_access(self, entry_id):
        """Updates frequency and timestamp whenever a memory is accessed."""
        with open(self.vector_db_path, 'r') as f:
            db = json.load(f)
        
        if entry_id in db:
            db[entry_id]['access_count'] = db[entry_id].get('access_count', 0) + 1
            db[entry_id]['last_access_timestamp'] = time.time()
            
            with open(self.vector_db_path, 'w') as f:
                json.dump(db, f, indent=4)

# Test Block
if __name__ == "__main__":
    optimizer = RelevanceOptimizer()
    # Simulating a deep clean
    print(optimizer.deep_clean_protocol(threshold=0.2))
  
