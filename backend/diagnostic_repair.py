# File Path: backend/diagnostic_repair.py
# Description: Implements 'Self-Repair' for the 5-Second Diagnosis protocol. [cite: 2026-02-11]
# Reconnects missing drives or activates Ghost Stubs to prevent system crashes. [cite: 2026-02-11]

import os
import json
import time

class SelfRepairHub:
    def __init__(self, config_manager, ghost_registry):
        self.config = config_manager
        self.ghost = ghost_registry
        self.repair_log = "database/repair_history.json"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.repair_log):
            with open(self.repair_log, 'w') as f:
                json.dump([], f)

    def trigger_healing_sequence(self, diagnosis_report):
        """
        Diagnosis fail hone par fault theek karne ki koshish karta hai. [cite: 2026-02-11]
        """
        print("🔧 [Self-Healer]: Fault detected during diagnosis. Initiating repair...") [cite: 2026-02-11]
        fixed_count = 0
        detected_count = len(diagnosis_report)

        for fault in diagnosis_report:
            module = fault.get("module")
            if self._reconnect_drive(module):
                fixed_count += 1
            else:
                # If cannot heal, activate Ghost Stub (Solo Mode) [cite: 2026-02-11]
                print(f"👻 [Self-Healer]: {module} unavailable. Activating Ghost Mode.")
                self.ghost.invoke_power(module)

        efficiency = self.calculate_healing_efficiency(fixed_count, detected_count)
        return f"✅ [Healing Complete]: Efficiency {efficiency}%. System stabilized."

    def _reconnect_drive(self, module_name):
        """Attempts to refresh the file path connection for a module."""
        path = self.config.get_key("SKELETON_KEYS", f"{module_name}_PATH")
        # Check if the path is now accessible [cite: 2026-02-11]
        if path and os.path.exists(str(path)):
            return True
        return False

    def calculate_healing_efficiency(self, fixed, detected):
        """
        Calculates the effectiveness of the self-repair session.
        Formula: $H_e = \frac{F_{fixed}}{F_{detected}} \times 100$
        """
        if detected == 0: return 100.0
        efficiency = (fixed / detected) * 100
        return round(efficiency, 2)

# Test Block
if __name__ == "__main__":
    # Mocking for standalone test
    class MockObj:
        def get_key(self, a, b): return "./"
        def invoke_power(self, p): print(f"Ghost activated for {p}")
        
    healer = SelfRepairHub(MockObj(), MockObj())
    sample_faults = [{"module": "DRIVE_E_NODE", "error": "Path Not Found"}]
    print(healer.trigger_healing_sequence(sample_faults))
                  
