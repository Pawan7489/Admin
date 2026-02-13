# File Path: backend/system_optimizer.py
# Description: Automates system cleanup and optimizes local database storage.
# Follows 'Musk Rule' (Maximum Efficiency, Minimum Junk). [cite: 2026-02-11]

import os
import time
import shutil
import json

class SystemOptimizer:
    def __init__(self):
        self.junk_folders = ["logs/", "database/renders/vision_captures/"]
        self.temp_files = ["temp_audio.wav", "temp_frame.jpg"]
        self.relevance_threshold = 0.4 # 40% se neeche ka data archive hoga

    def run_deep_clean(self):
        """Useless files ko delete aur storage ko optimize karta hai."""
        print("🧹 [Optimizer]: Starting Deep Space Cleanup...")
        initial_size = self._get_system_size()
        
        # 1. Clear Temp Files [cite: 2026-02-11]
        for f in self.temp_files:
            if os.path.exists(f):
                os.remove(f)
                print(f"🗑️ Deleted temp file: {f}")

        # 2. Log Rotation (Purane logs delete karna)
        for folder in self.junk_folders:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    file_path = os.path.join(folder, f)
                    # 7 din se purani files delete karo
                    if os.path.getmtime(file_path) < time.time() - (7 * 86400):
                        os.remove(file_path)

        final_size = self._get_system_size()
        space_saved = initial_size - final_size
        return self._generate_report(space_saved)

    def _get_system_size(self):
        """Poore project folder ka size calculate karta hai."""
        total_size = 0
        for start_path in ['.']:
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        return total_size / (1024 * 1024) # Size in MB

    def calculate_efficiency_index(self, saved, total):
        """
        Calculates Space Optimization Index ($E_i$).
        Formula: $E_i = \frac{S_{saved}}{S_{total}} \times 100$
        """
        if total == 0: return 0.0
        return round((saved / total) * 100, 2)

    def _generate_report(self, saved):
        return f"🚀 [Optimizer]: Efficiency Boosted! Saved {round(saved, 2)} MB of space."

# Test Block
if __name__ == "__main__":
    opt = SystemOptimizer()
    print(opt.run_deep_clean())
  
