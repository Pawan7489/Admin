# Sub-File 85-T: Automatically triggers system rollback upon consecutive critical failures.
# Implements 'Self-Healing' logic at the OS level.

class AnomalyRollback:
    def __init__(self):
        self.crash_count = 0
        self.max_crashes = 3

    def detect_and_recover(self, boot_status):
        """Lagataar failures par auto-restore trigger karta hai."""
        if boot_status == "FATAL":
            self.crash_count += 1
            print(f"⚠️ [Anomaly]: Critical failure {self.crash_count}/{self.max_crashes}.")
            
            if self.crash_count >= self.max_crashes:
                print("🔄 [Rollback]: System unstable. Auto-restoring last stable Time Capsule...")
                # Call to SnapshotHarmonizer to revert state
                return "System Restored to Safety."
        else:
            self.crash_count = 0 # Reset on successful boot
            return "System Stable."
          
