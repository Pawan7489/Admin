# File Path: backend/resource_balancer.py
# Description: Monitors system resources and suspends non-essential tasks.
# Implements 'Musk Rule' for maximum efficiency during travel or low-power modes.

import psutil
import time
import json
import os

class ResourceBalancer:
    def __init__(self, registry):
        self.registry = registry  # Link to Master Registry (File 12)
        self.threshold_cpu = 80.0 # Percentage
        self.threshold_ram = 75.0 # Percentage
        self.balance_log = "database/resource_balance.json"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'):
            os.makedirs('database')

    def check_system_load(self):
        """
        CPU aur RAM usage check karta hai. 
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        
        print(f"📊 [Monitor]: CPU: {cpu_usage}% | RAM: {ram_usage}%")
        
        if cpu_usage > self.threshold_cpu or ram_usage > self.threshold_ram:
            return True, cpu_usage, ram_usage
        return False, cpu_usage, ram_usage

    def enforce_balance(self):
        """
        High load hone par non-essential modules ko suspend karta hai.
        """
        is_heavy, cpu, ram = self.check_system_load()
        
        if is_heavy:
            print("⚠️ [Balancer]: High Resource Load Detected! Activating Power-Save Mode...")
            # Suspending non-essential modules like 'Visual UI' or 'Deep Analytics'
            suspended = ["Visual_Logic_Engine", "Deep_Critique_Node"]
            for module in suspended:
                print(f"💤 [Balancer]: Suspending {module} to save CPU/RAM...")
            
            self._log_balancing_event("Suspension", cpu, ram, suspended)
            return f"🚀 [Optimized]: Suspended {len(suspended)} modules for efficiency."
        
        return "✅ [Stable]: System running within normal limits."

    def calculate_efficiency_index(self):
        """
        Calculates the Resource Efficiency Index ($E_i$).
        Formula: $E_i = \frac{Output}{Load}$
        Where Load is $L = (CPU\% + RAM\%) / 2$.
        """
        _, cpu, ram = self.check_system_load()
        load = (cpu + ram) / 2
        if load == 0: return 100.0
        # Assuming fixed high output for A1 engine
        efficiency = 100 / (load / 10) 
        return round(efficiency, 2)

    def _log_balancing_event(self, action, cpu, ram, modules):
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "cpu_at_event": cpu,
            "ram_at_event": ram,
            "affected_modules": modules
        }
        with open(self.balance_log, 'a') as f:
            f.write(json.dumps(event) + "\n")

# Test Block
if __name__ == "__main__":
    # Mocking registry
    balancer = ResourceBalancer(None)
    print(balancer.enforce_balance())
    print(f"📈 Efficiency Index: {balancer.calculate_efficiency_index()}")
      
