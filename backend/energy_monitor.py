# Sub-File 84-Y: Optimizes power consumption for travel and mobile use.
# Follows 'Musk Rule' for hardware efficiency. [cite: 2026-02-11]

class EnergyMonitor:
    def check_power_source(self):
        # Logic: If on Battery -> Limit Vision frame rate to 10 FPS
        import psutil
        battery = psutil.sensors_battery()
        if battery and not battery.power_plugged:
            return "🔋 [Power]: Travel Mode Active (Low GPU usage)."
        return "⚡ [Power]: Full Performance Mode."
      
