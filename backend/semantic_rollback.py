# File Path: backend/semantic_rollback.py
# Description: Implements Logic Rollback based on Human-in-the-Loop Feedback. [cite: 2026-02-11]
# Connects Feedback Engine (File 21) with Mental State Registry (File 28).

import json
import os
from mental_state_registry import MentalStateManager

class SemanticRollback:
    def __init__(self):
        self.registry = MentalStateManager()
        self.feedback_file = "database/rlhf_feedback.json"
        self.rollback_threshold = 3 # Rollback if 3 consecutive 'Bad' ratings occur

    def analyze_feedback_and_trigger(self):
        """
        Feedback scan karta hai aur agar 'Bad' ratings zyada hain toh rollback trigger karta hai. [cite: 2026-02-11]
        """
        if not os.path.exists(self.feedback_file):
            return "✅ [Rollback]: No feedback data yet."

        with open(self.feedback_file, 'r') as f:
            feedback_data = json.load(f)

        # Checking the last N feedbacks
        recent_feedback = feedback_data[-self.rollback_threshold:]
        bad_count = sum(1 for fb in recent_feedback if fb.get("rating") <= 2 or fb.get("status") == "Bad")

        if bad_count >= self.rollback_threshold:
            print(f"⚠️ [Rollback]: {bad_count} consecutive bad feedbacks detected. Initiating Time Travel...") [cite: 2026-02-11]
            return self._execute_rewind()
        
        return "✅ [Rollback]: System logic is within acceptable performance limits."

    def _execute_rewind(self):
        """
        Mental State Vault se pichla stable version uthakar restore karta hai. [cite: 2026-02-11]
        """
        with open(self.registry.registry_file, 'r') as f:
            reg_data = json.load(f)
        
        history = reg_data.get("history", [])
        if len(history) < 2:
            return "❌ [Error]: No previous stable mental state found to rollback."

        # Finding the second to last stable version
        previous_stable = history[-2]["version"]
        result = self.registry.rollback_to_version(previous_stable)
        
        # Calculating Recovery Stability Ratio
        # $R_s = \frac{V_{prev}}{V_{current}} \times 100$
        return f"⏪ [Time Travel Success]: {result}. AI has forgotten the 'Bad' logic path." [cite: 2026-02-11]

    def calculate_error_velocity(self, error_count, time_window):
        """
        Calculates how fast errors are accumulating.
        Formula: $V_e = \frac{\Delta E}{\Delta t}$
        """
        velocity = error_count / time_window
        return round(velocity, 2)

# Test Block
if __name__ == "__main__":
    rewinder = SemanticRollback()
    # Simulating a check
    print(rewinder.analyze_feedback_and_trigger())
  
