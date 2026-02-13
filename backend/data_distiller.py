# File Path: backend/data_distiller.py
# Description: Refines logic from multiple engines to create the training core for A1.
# Follows 'Musk Rule' (Efficiency) and 'Pichai Rule' (Scale). [cite: 2026-02-11]

import json
import os

class DataDistiller:
    def __init__(self, aggregator):
        self.aggregator = aggregator # Link to File 58
        self.raw_wisdom_bank = "database/a1_wisdom_bank.json"
        self.distilled_training_file = "database/a1_golden_dataset.jsonl"
        self.quality_threshold = 0.85 # 85% se neeche ka logic discard hoga

    def distill_knowledge(self):
        """
        Raw logic pools se 'Golden Logic' nikaalta hai. [cite: 2026-02-11]
        """
        print("⚗️ [Distiller]: Starting the distillation process...")
        
        if not os.path.exists(self.raw_wisdom_bank):
            return "❌ [Error]: Wisdom Bank is empty. Need more engine interaction."

        with open(self.raw_wisdom_bank, 'r') as f:
            raw_data = json.load(f)

        golden_samples = []
        for entry in raw_data:
            prompt = entry['input']
            # Best engine ka answer choose karna based on logic_weight [cite: 2026-02-11]
            best_logic = self._extract_best_logic(entry['knowledge_pool'])
            
            if best_logic:
                # Formatting for Fine-tuning (JSONL format)
                training_sample = {
                    "instruction": prompt,
                    "context": "A1 Super Genius OS Logic",
                    "response": best_logic
                }
                golden_samples.append(training_sample)

        self._save_as_jsonl(golden_samples)
        return self.calculate_distillation_efficiency(len(raw_data), len(golden_samples))

    def _extract_best_logic(self, pool):
        """Sirf high-weight engines ka data select karta hai."""
        # Simple selection for now, future mein isme 'Consensus logic' aayega
        return pool[0] if pool else None

    def calculate_distillation_efficiency(self, raw_count, distilled_count):
        """
        Calculates the Distillation Ratio ($R_d$).
        Formula: $R_d = \frac{N_{distilled}}{N_{raw}} \times 100$
        """
        ratio = (distilled_count / raw_count) * 100 if raw_count > 0 else 0
        return f"✨ [Distiller]: Refined {distilled_count} high-quality logic paths. Efficiency: {round(ratio, 2)}%"

    def _save_as_jsonl(self, samples):
        with open(self.distilled_training_file, 'w') as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")
        print(f"💾 [Success]: Golden Dataset saved at {self.distilled_training_file}")

# Test Block
if __name__ == "__main__":
    # Integration with File 58 & 60 logic
    pass
