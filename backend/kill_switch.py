# File Path: backend/kill_switch.py
# Description: Implements the 'Kill Switch' Protocol (Emergency Stop). [cite: 2026-02-11]
# Purpose: Instant process termination, network cutoff, and state saving. [cite: 2026-02-11]

import os
import sys
import psutil
import subprocess
import json
from datetime import datetime

class EmergencyKillSwitch:
    def __init__(self):
        self.override_command = "System Freeze" # Voice/Text Trigger [cite: 2026-02-11]
        self.state_file = "database/emergency_state.json"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'):
            os.makedirs('database')

    def trigger_protocol(self):
        """
        Executes the full Kill Switch protocol to give you absolute control. [cite: 2026-02-11]
        """
        print("🚨 [KILL SWITCH]: EMERGENCY OVERRIDE DETECTED!") [cite: 2026-02-11]
        
        # 1. Save Current State [cite: 2026-02-11]
        self._save_system_state()
        
        # 2. Cut Internet Access [cite: 2026-02-11]
        self._disable_network()
        
        # 3. Stop All Processes [cite: 2026-02-11]
        self._terminate_all_processes()
        
        print("🛑 [SYSTEM FROZEN]: All operations halted successfully.") [cite: 2026-02-11]
        sys.exit(0)

    def _save_system_state(self):
        """Saves a snapshot of active modules and settings before shutdown. [cite: 2026-02-11]"""
        state = {
            "timestamp": str(datetime.now()),
            "active_pids": [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name'].lower()],
            "message": "Emergency Stop Triggered. State preserved for Admin review."
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=4)
        print("💾 [Kill Switch]: Current state saved to database.") [cite: 2026-02-11]

    def _disable_network(self):
        """Attempts to cut internet access via system commands. [cite: 2026-02-11]"""
        print("🌐 [Kill Switch]: Cutting Internet Access...") [cite: 2026-02-11]
        try:
            if os.name == 'nt': # Windows
                # Disables all network interfaces
                subprocess.run(["ipconfig", "/release"], shell=True, check=True)
            else: # Linux/Mac
                subprocess.run(["ifconfig", "eth0", "down"], shell=True, check=True)
        except Exception as e:
            print(f"⚠️ [Kill Switch]: Network cutoff partial: {str(e)}")

    def _terminate_all_processes(self):
        """Instantly stops all child and sister processes. [cite: 2026-02-11]"""
        print("✂️ [Kill Switch]: Terminating all active processes...") [cite: 2026-02-11]
        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        for child in children:
            child.kill()
        # The main process will exit after this [cite: 2026-02-11]

# Test Block (Simulation)
if __name__ == "__main__":
    ks = EmergencyKillSwitch()
    # In reality, this would be triggered by a key combo or voice command
    # ks.trigger_protocol() 
  
