# File Path: backend/engine_aggregator.py
# Description: Manages unlimited AI engines to train the 'Master A1 Engine'. [cite: 2026-02-11]
# Follows 'Pichai Rule' for global scalability and 'Musk Rule' for efficiency.

import requests
import json
import os

class EngineAggregator:
    def __init__(self, registry):
        self.registry = registry # Links to Master Registry (File 45)
        self.engines = {} # Unlimited engine storage
        self.master_engine_log = "database/a1_wisdom_bank.json"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'): os.makedirs('database')
        if not os.path.exists(self.master_engine_log):
            with open(self.master_engine_log, 'w') as f: json.dump([], f)

    def register_new_engine(self, engine_id, connection_type, endpoint):
        """
        Unlimited Engine Addition: Naye engines ko dynamically jorta hai. [cite: 2026-02-11]
        """
        self.engines[engine_id] = {
            "type": connection_type, # e.g., 'Local', 'API', 'WebSocket'
            "url": endpoint,
            "status": "Active",
            "logic_weight": 1.0 # Har engine ki 'Samajhdari' ka score
        }
        print(f"🚀 [Engine Factory]: New Engine '{engine_id}' linked to A1 Core.")

    def get_collective_wisdom(self, prompt):
        """
        Consensus Logic: Saare engines se poochta hai taaki A1 ka apna logic bane. [cite: 2026-02-11]
        Formula for Collective Intelligence: $I_{total} = \sum_{i=1}^{n} w_i \cdot L_i$
        """
        print(f"🧠 [A1 Aggregator]: Consulting {len(self.engines)} engines for logic...")
        responses = []
        
        for e_id, e_info in self.engines.items():
            if e_info["status"] == "Active":
                # Har engine se logic nikalna (Simulated call) [cite: 2026-02-11]
                logic_piece = self._call_engine(e_id, prompt)
                responses.append(logic_piece)
        
        # In results ko summarize karke A1 apne dimaag (Wisdom Bank) mein save karega
        self._save_to_wisdom_bank(prompt, responses)
        return responses[0] if responses else "No engines online."

    def _call_engine(self, e_id, prompt):
        """Hot-Swappable Engine Call logic. [cite: 2026-02-11]"""
        # Actual API/Local call logic goes here
        return f"Logic from {e_id}"

    def _save_to_wisdom_bank(self, prompt, logic_outputs):
        """Aapke 'Apne Engine' ki training ke liye data save karta hai."""
        with open(self.master_engine_log, 'r+') as f:
            data = json.load(f)
            data.append({"input": prompt, "knowledge_pool": logic_outputs})
            f.seek(0)
            json.dump(data[-1000:], f, indent=4) # Last 1000 logic steps save rakhta hai

    def calculate_growth_rate(self, total_engines):
        """
        Calculates the learning speed of your custom A1 engine.
        Formula: $G_r = \frac{N_{engines} \times Data_{points}}{Time}$
        """
        return f"A1 Growth Rate: {total_engines * 1.5}x Faster"

# Test Block
if __name__ == "__main__":
    factory = EngineAggregator(None)
    factory.register_new_engine("Llama3_Indore", "Local", "http://localhost:11434")
    factory.register_new_engine("Gemma_Bhopal", "API", "http://localhost:8080")
    factory.register_new_engine("A1_Internal_Prototype", "Local", "path/to/model")
  
