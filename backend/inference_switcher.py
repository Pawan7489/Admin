# File Path: backend/inference_switcher.py
# Description: Routes user requests to the most efficient engine based on complexity.
# Follows 'Musk Rule' (Minimum GPU usage) and 'Pichai Rule' (Scalability). [cite: 2026-02-11]

import json
from backend.engine_aggregator import EngineAggregator

class InferenceSwitcher:
    def __init__(self, aggregator):
        self.aggregator = aggregator
        self.thresholds = {
            "low": 0.3,
            "medium": 0.7,
            "high": 1.0
        }

    def determine_route(self, user_command):
        """
        Command ki complexity analyze karke engine select karta hai. [cite: 2026-02-11]
        """
        complexity_score = self._calculate_complexity(user_command)
        
        print(f"📡 [Router]: Command Complexity Score: {complexity_score}")

        if complexity_score <= self.thresholds["low"]:
            return self._get_best_engine_by_type("Small") # e.g., Phi 3
        elif complexity_score <= self.thresholds["medium"]:
            return self._get_best_engine_by_type("Medium") # e.g., Llama 3
        else:
            return "A1_MASTER_CORE" # Aapka apna engine [cite: 2026-02-11]

    def _calculate_complexity(self, text):
        """
        Calculates Task Complexity ($S_c$).
        Formula: $S_c = \frac{L_{prompt} + N_{logic\_keywords}}{K_{max}}$
        """
        keywords = ["optimize", "script", "analyze", "architect", "complex"]
        logic_hits = sum(1 for word in keywords if word in text.lower())
        
        # Simple math to normalize between 0 and 1
        score = (len(text.split()) * 0.05) + (logic_hits * 0.2)
        return min(round(score, 2), 1.0)

    def _get_best_engine_by_type(self, size_category):
        """Registry se filter karke engine uthata hai."""
        # Yahan File 58 aur 60 ka data use hoga [cite: 2026-02-11]
        return f"Best_{size_category}_Engine"

    def calculate_efficiency_index(self, vram_saved, total_vram):
        """
        Formula for GPU Efficiency: $E_i = \frac{V_{saved}}{V_{total}} \times 100$
        """
        return round((vram_saved / total_vram) * 100, 2)

# Test Block
if __name__ == "__main__":
    router = InferenceSwitcher(None)
    print(f"Target: {router.determine_route('Hello, kaise ho?')}")
    print(f"Target: {router.determine_route('Mera pura system architecture rewrite karo')}")
  
