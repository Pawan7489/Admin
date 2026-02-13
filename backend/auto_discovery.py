# File Path: backend/auto_discovery.py
# Description: Automatically scans and registers new AI engines from local drives. [cite: 2026-02-11]
# Ensures 'Unlimited Engine' scalability without manual configuration.

import os
import json
from backend.engine_aggregator import EngineAggregator

class AutoDiscoveryEngine:
    def __init__(self, aggregator):
        self.aggregator = aggregator
        self.search_paths = ["models/", "D:/A1_Models/", "E:/AI_Engines/"]
        self.discovered_log = "database/discovered_engines.json"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'): os.makedirs('database')
        if not os.path.exists(self.discovered_log):
            with open(self.discovered_log, 'w') as f: json.dump([], f)

    def scan_for_engines(self):
        """
        Drives aur folders ko scan karke naye engines dhoondta hai. [cite: 2026-02-11]
        """
        print("🔍 [Scout]: Scanning for new engines in distributed paths...") [cite: 2026-02-11]
        new_finds = 0
        
        for path in self.search_paths:
            if os.path.exists(path):
                # Scanning sub-folders for GGUF/Zip models [cite: 2026-02-10]
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith((".gguf", ".bin", ".zip")):
                            engine_id = f"Auto_{file.split('.')[0]}"
                            if engine_id not in self.aggregator.engines:
                                self.aggregator.register_new_engine(
                                    engine_id=engine_id,
                                    connection_type="Local_File",
                                    endpoint=os.path.join(root, file)
                                )
                                new_finds += 1
                                print(f"✨ [Scout]: New engine found and registered: {engine_id}")

        return self.calculate_discovery_saturation(new_finds)

    def calculate_discovery_saturation(self, new_finds):
        """
        Calculates how much the 'Wisdom Pool' has expanded.
        Formula: $S_{disc} = \frac{N_{new}}{N_{existing} + 1}$
        """
        existing = len(self.aggregator.engines)
        saturation = new_finds / (existing if existing > 0 else 1)
        return f"📈 Discovery Saturation: +{round(saturation * 100, 2)}% logic expansion."

    def add_search_path(self, new_path):
        """Admin panel se naya rasta jorne ke liye."""
        if os.path.exists(new_path) and new_path not in self.search_paths:
            self.search_paths.append(new_path)
            return True
        return False

# Test Block
if __name__ == "__main__":
    # Integration with File 58
    from backend.engine_aggregator import EngineAggregator
    mock_agg = EngineAggregator(None)
    scout = AutoDiscoveryEngine(mock_agg)
    print(scout.scan_for_engines())
      
