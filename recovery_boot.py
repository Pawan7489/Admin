# Sub-File 85-M: Standalone Emergency Bootloader for fatal system crashes.
# The Ultimate Kill-Switch Recovery. [cite: 2026-02-11]

import os
import zipfile

def emergency_system_restore():
    """Bina OS start kiye, pure folder ko pichle snapshot se overwrite karta hai."""
    print("🚨 [FATAL RECOVERY]: Main OS failed to boot. Initiating Failsafe...")
    
    snapshot_dir = "database/snapshots/"
    if not os.path.exists(snapshot_dir) or not os.listdir(snapshot_dir):
        print("❌ [Error]: No Time Capsules found. Manual intervention required.")
        return
        
    # Get the latest zip file
    latest_zip = max([os.path.join(snapshot_dir, f) for f in os.listdir(snapshot_dir) if f.endswith('.zip')], key=os.path.getctime)
    
    print(f"🛠️ [Bootloader]: Extracting {latest_zip}...")
    with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
        zip_ref.extractall(".")
        
    print("✅ [Resurrected]: System Core Repaired. You can now run 'run_a1.py'.")

if __name__ == "__main__":
    emergency_system_restore()
  
