# File Path: security/intrusion_detector.py
# Description: Monitors system access and network traffic for unauthorized entry.
# Rule: Trigger 'Kill Switch' if multiple failed login attempts occur. [cite: 2026-02-11]

import os
import time
import psutil

class IntrusionDetector:
    def __init__(self):
        self.authorized_ips = ["127.0.0.1", "localhost"] # Local and Trusted
        self.failed_attempts = 0
        self.max_attempts = 3

    def monitor_connections(self):
        """Active network connections ko scan karta hai."""
        print("🛡️ [IDS]: Monitoring active network bridge...")
        connections = psutil.net_connections()
        
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                remote_ip = conn.raddr.ip if conn.raddr else None
                if remote_ip and remote_ip not in self.authorized_ips:
                    self._handle_unauthorized(remote_ip)

    def _handle_unauthorized(self, ip):
        """Unauthorized access par action leta hai."""
        print(f"🚨 [ALERT]: Unauthorized access detected from IP: {ip}")
        self.failed_attempts += 1
        
        if self.failed_attempts >= self.max_attempts:
            self._trigger_emergency_freeze()

    def _trigger_emergency_freeze(self):
        """Master Override Command: System Freeze Protocol. [cite: 2026-02-11]"""
        print("🔥 [CRITICAL]: Security Breach. Triggering Master Kill Switch (Ctrl+Alt+K)...")
        # Actual command to cut internet and lock files
        # os.system("nmcli networking off") # Example for Linux/Mac
        return "SYSTEM_FROZEN"

    def calculate_threat_level(self, failed_cnt):
        """
        Calculates Threat Probability ($P_t$).
        Formula: $P_t = \frac{A_{failed}}{A_{max}} \times 100$
        """
        return round((failed_cnt / self.max_attempts) * 100, 2)

# Test Block
if __name__ == "__main__":
    ids = IntrusionDetector()
    ids.monitor_connections()
      
