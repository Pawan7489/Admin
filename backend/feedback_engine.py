# File Path: backend/feedback_engine.py
# Description: Implements Human-in-the-Loop Learning (RLHF). [cite: 2026-02-11]
# Saves user feedback to Vector DB to refine future logic paths. [cite: 2026-02-11]

import json
import os
from datetime import datetime

class FeedbackEngine:
    def __init__(self):
        self.vector_db_file = "database/rlhf_memory_vector.json"
        self._ensure_db_setup()

    def _ensure_db_setup(self):
        """Ensures the Vector DB exists for storing feedback."""
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.vector_db_file):
            with open(self.vector_db_file, 'w') as f:
                json.dump({}, f)

    def save_task_feedback(self, task_id, intent, logic_path, rating):
        """
        Saves Thumbs Up/Down or 1-5 Rating to the Vector DB. [cite: 2026-02-11]
        rating: 'thumbs_up', 'thumbs_down', or numeric 1-5.
        """
        print(f"📝 [RLHF]: Processing feedback for Task '{intent}'...") [cite: 2026-02-11]
        
        with open(self.vector_db_file, 'r') as f:
            memory = json.load(f)

        # Logic to remember or avoid paths based on feedback [cite: 2026-02-11]
        memory[task_id] = {
            "intent": intent,
            "logic_path": logic_path,
            "feedback_rating": rating,
            "timestamp": str(datetime.now()),
            "priority": 1.0 if rating == 'thumbs_up' else 0.0
        }

        with open(self.vector_db_file, 'w') as f:
            json.dump(memory, f, indent=4)

        if rating == 'thumbs_up':
            return "🌟 [Good Job]: This method has been prioritized in the AI's memory." [cite: 2026-02-11]
        else:
            return "⚠️ [Bad]: This logic path will be avoided in the future." [cite: 2026-02-11]

    def get_preferred_logic(self, intent):
        """
        Searches the DB to find if a successful logic path already exists for this intent. [cite: 2026-02-11]
        """
        with open(self.vector_db_file, 'r') as f:
            memory = json.load(f)

        # Basic semantic search simulation
        for task_id, data in memory.items():
            if data["intent"] == intent and data["feedback_rating"] == 'thumbs_up':
                return data["logic_path"]
        
        return None

# Test Block (Simulation)
if __name__ == "__main__":
    fe = FeedbackEngine()
    # Simulating a "Good Job" feedback [cite: 2026-02-11]
    print(fe.save_task_feedback("T-101", "Create Folder", "os.mkdir('images')", "thumbs_up"))
    # Checking if AI remembers [cite: 2026-02-11]
    print(f"Memory Check: {fe.get_preferred_logic('Create Folder')}")
  
