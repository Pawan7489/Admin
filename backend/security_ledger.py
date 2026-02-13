# File Path: backend/security_ledger.py
# Description: Digital mirror of the Admin's handwritten security logic.
# Logs all high-level commands with a unique cryptographic signature.

import os
import json
import hashlib
from datetime import datetime

class SecurityLedger:
    def __init__(self):
        self.ledger_file = "database/admin_ledger.log"
        self.signature_vault = "database/admin_signatures.json"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.signature_vault):
            with open(self.signature_vault, 'w') as f:
                json.dump({"active_signatures": []}, f)

    def log_action(self, admin_key, command_type, details):
        """
        Admin action ko log karta hai aur ek unique signature generate karta hai.
        Formula for Command Signature: $S_c = \text{SHA256}(Key + Cmd + Time)$
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generating a unique signature for this specific command
        raw_string = f"{admin_key}{command_type}{timestamp}"
        signature = hashlib.sha256(raw_string.encode()).hexdigest()

        log_entry = (
            f"--- [ADMIN LEDGER ENTRY] ---\n"
            f"Timestamp: {timestamp}\n"
            f"Command: {command_type}\n"
            f"Details: {details}\n"
            f"Signature: {signature}\n"
            f"---------------------------\n\n"
        )

        # Saving to the log file (Handwritten mirror)
        with open(self.ledger_file, 'a') as f:
            f.write(log_entry)
            
        self._archive_signature(signature)
        print(f"📒 [Ledger]: Action signed and recorded. Signature: {signature[:12]}...")

    def _archive_signature(self, signature):
        with open(self.signature_vault, 'r') as f:
            data = json.load(f)
        
        data["active_signatures"].append({
            "sig": signature,
            "timestamp": str(datetime.now())
        })
        
        with open(self.signature_vault, 'w') as f:
            json.dump(data, f, indent=4)

    def verify_command_integrity(self, signature_to_check):
        """
        Check karta hai ki koi command tampering toh nahi hui.
        """
        with open(self.signature_vault, 'r') as f:
            data = json.load(f)
        
        for entry in data["active_signatures"]:
            if entry["sig"] == signature_to_check:
                return True
        return False

# Test Block
if __name__ == "__main__":
    ledger = SecurityLedger()
    # Simulating a high-level admin command
    ledger.log_action("A1-BOP-2026", "CORE_UPDATE", "Updating Logic Version to v2.1")
  
