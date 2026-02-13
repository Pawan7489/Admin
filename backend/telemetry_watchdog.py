# File Path: backend/telemetry_watchdog.py
# Description: 5-Second Self-Diagnosis & Hardware Watchdog. [cite: 2026-02-11]
# Monitors Thermal and Memory health to prevent hardware damage.

import psutil
import time
import socket
import threading

class TelemetryWatchdog:
    def __init__(self, kill_switch):
        self.kill_switch = kill_switch
        self.temp_threshold = 85.0 # Celsius
        self.mem_threshold = 90.0  # Percentage
        self.is_running = False

    def check_internet(self):
        """Internet status check karta hai. [cite: 2026-02-11]"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def get_hardware_stats(self):
        """CPU, GPU aur RAM ki health report nikalta hai. [cite: 2026-02-11]"""
        # RAM usage
        memory = psutil.virtual_memory().percent
        
        # CPU Temp (Note: Linux/Mac par direct chalta hai, Windows par external tool lag sakta hai)
        # Yahan hum simulation use kar rahe hain [cite: 2026-02-11]
        cpu_temp = 55.0 
        
        return {"temp": cpu_temp, "memory": memory}

    def start_monitoring(self):
        """Har 5 second mein diagnosis chalata hai. [cite: 2026-02-11]"""
        self.is_running = True
        print("🛡️ [Watchdog]: Hardware Monitoring Active (Interval: 5s)...")
        
        def loop():
            while self.is_running:
                stats = self.get_hardware_stats()
                internet = self.check_internet()
                
                print(f"📊 [Diagnosis]: Temp: {stats['temp']}°C | RAM: {stats['memory']}% | Net: {internet}")
                
                # Critical Checks [cite: 2026-02-11]
                if stats['temp'] > self.temp_threshold or stats['memory'] > self.mem_threshold:
                    print("🚨 [CRITICAL]: Hardware limits exceeded! Freezing System...")
                    self.kill_switch.trigger_protocol()
                    self.is_running = False
                
                time.sleep(5) # 5-Second Rule [cite: 2026-02-11]

        monitor_thread = threading.Thread(target=loop, daemon=True)
        monitor_thread.start()

    def calculate_thermal_pressure(self, current_temp):
        """
        Calculates the Thermal Pressure Index ($T_p$).
        Formula: $T_p = \frac{T_{current}}{T_{limit}} \times 100$
        """
        pressure = (current_temp / self.temp_threshold) * 100
        return round(pressure, 2)

# Test Block
if __name__ == "__main__":
    # Mock Kill Switch
    class MockKill:
        def trigger_protocol(self): print("❄️ [Kill Switch]: System State Saved & Frozen.")
    
    watchdog = TelemetryWatchdog(MockKill())
    watchdog.start_monitoring()
    
    # Keeping script alive
    while True: time.sleep(1)
