# Sub-File 85-X: Prevents heavy snapshot creation during low battery states.
# Hardware protection protocol. [cite: 2026-02-11]

import psutil

class BatterySafeBackup:
    def is_safe_to_backup(self):
        """Battery aur power status check karta hai."""
        battery = psutil.sensors_battery()
        if battery and not battery.power_plugged and battery.percent < 15:
            print(f"🔋 [Battery Guard]: Power at {battery.percent}%. Pausing snapshot to save energy.")
            return False
        return True
      
