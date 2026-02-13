# File Path: backend/sync_engine.py
# Description: Synchronizes files across distributed drives (D, E, Cloud).
# Implements the 'Bridge Rule' for mesh connectivity. [cite: 2026-02-11]

import os
import hashlib
import shutil
from datetime import datetime

class AutoSyncEngine:
    def __init__(self, master_config):
        self.config = master_config # Drive paths from File 55
        self.sync_log = "database/sync_history.json"
        self.sync_active = True

    def perform_mesh_sync(self):
        """Indore aur Bhopal ke bikhre huye data ko merge karta hai."""
        print("🌉 [Bridge]: Initiating Distributed Mesh Sync...")
        
        source = self.config.get("DRIVE_D", "D:/A1_Data/")
        target = self.config.get("DRIVE_E", "E:/A1_Mirror/")
        
        if not os.path.exists(source) or not os.path.exists(target):
            print("⚠️ [Bridge]: One or more drives offline. Entering 'Solo Sync' mode.")
            return False

        files_synced = 0
        for root, dirs, files in os.walk(source):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), source)
                dest_path = os.path.join(target, rel_path)
                
                # Zuckerberg Speed Rule: Sirf badli hui files sync karo
                if self._needs_update(os.path.join(root, file), dest_path):
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(os.path.join(root, file), dest_path)
                    files_synced += 1
        
        print(f"✅ [Sync]: Mesh updated. {files_synced} files synchronized.")
        return True

    def _needs_update(self, src, dst):
        """Checksum se check karta hai ki file update ki zarurat hai ya nahi."""
        if not os.path.exists(dst): return True
        
        src_hash = self._get_hash(src)
        dst_hash = self._get_hash(dst)
        return src_hash != dst_hash

    def _get_hash(self, path):
        """File integrity check using MD5."""
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def calculate_sync_integrity(self, total_files, synced_files):
        """
        Calculates the Sync Integrity Index ($I_s$).
        Formula: $I_s = \frac{N_{synced}}{N_{total}} \times 100$
        Target: 100% for full distributed mesh.
        """
        if total_files == 0: return 100.0
        return round((synced_files / total_files) * 100, 2)

# Integration Logic
if __name__ == "__main__":
    # Mock Config for Testing
    config = {"DRIVE_D": "./test_d", "DRIVE_E": "./test_e"}
    engine = AutoSyncEngine(config)
    # engine.perform_mesh_sync()
  
