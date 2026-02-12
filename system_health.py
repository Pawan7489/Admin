# File: system_health.py
# Description: Self-Diagnosis Module (Checks Internet, CPU, RAM, Disk)

import psutil  # System info ke liye
import socket  # Internet check ke liye
import shutil  # Disk space ke liye

class SystemDoctor:
    def __init__(self):
        self.status = "Green"

    def check_internet(self):
        """Google ko ping karke internet check karega"""
        try:
            # 8.8.8.8 is Google's DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def diagnose(self):
        """Full Body Checkup run karta hai"""
        report = []
        is_healthy = True
        
        # 1. Check Internet
        if self.check_internet():
            report.append("✅ Internet: CONNECTED")
        else:
            report.append("❌ Internet: DISCONNECTED (Offline Mode)")
            # Note: Offline hone par AI band nahi hoga, bas online features rok dega.

        # 2. Check CPU Usage
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 85:
            report.append(f"⚠️ CPU Warning: High Load ({cpu_usage}%)")
            is_healthy = False
        else:
            report.append(f"✅ CPU: Stable ({cpu_usage}%)")

        # 3. Check RAM
        ram = psutil.virtual_memory()
        if ram.percent > 90:
            report.append(f"⚠️ Memory Warning: RAM Full ({ram.percent}%)")
            is_healthy = False
        else:
            report.append(f"✅ RAM: {ram.percent}% Used ({ram.available // (1024*1024)} MB Free)")

        # 4. Check Disk Space
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        if free_gb < 5:
            report.append(f"⚠️ Storage Warning: Only {free_gb}GB left!")
            is_healthy = False
        else:
            report.append(f"✅ Storage: {free_gb}GB Free")

        # Final Verdict
        if is_healthy:
            report.append("\n🟢 SYSTEM STATUS: ONLINE & READY")
        else:
            report.append("\n🔴 SYSTEM STATUS: UNSTABLE (Check Warnings)")

        return "\n".join(report)

# Testing block
if __name__ == "__main__":
    doc = SystemDoctor()
    print(doc.diagnose())
  
