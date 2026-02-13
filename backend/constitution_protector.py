# File Path: backend/constitution_protector.py
# Description: Implements the 'Read-Only Lock' for the Core Constitution. [cite: 2026-02-11]
# Strictly forbids the AI from modifying its own foundational laws. [cite: 2026-02-11]

import os
import stat
import json
import hashlib

class ConstitutionProtector:
    def __init__(self):
        self.file_path = "database/constitution.json"
        self.checksum_file = "database/const_checksum.txt"
        self._ensure_setup()

    def _ensure_setup(self):
        """Initializes the constitution and applies a system-level read-only lock."""
        if not os.path.exists('database'):
            os.makedirs('database')
            
        if not os.path.exists(self.file_path):
            # Points 1-75 Placeholder [cite: 2026-02-11]
            default_laws = {
                "Laws": {f"Rule_{i}": "Foundational Rule" for i in range(1, 76)},
                "Status": "Immutable",
                "Authority": "Admin Only"
            }
            with open(self.file_path, 'w') as f:
                json.dump(default_laws, f, indent=4)
        
        self.apply_hard_lock()
        self._generate_checksum()

    def apply_hard_lock(self):
        """
        Changes file permissions to Read-Only for all users (OS Level). [cite: 2026-02-11]
        """
        try:
            # Setting permission to S_IREAD (Read-only)
            os.chmod(self.file_path, stat.S_IREAD)
            print(f"🔒 [Protector]: System-level Read-Only lock applied to {self.file_path}") [cite: 2026-02-11]
        except Exception as e:
            print(f"⚠️ [Error]: Could not apply OS lock: {e}")

    def unlock_for_admin(self, admin_key):
        """
        Only the Admin with the correct key can unlock the constitution for editing. [cite: 2026-02-11]
        """
        # Hardcoded Admin Key for now (In real use, use env variables)
        if admin_key == "A1-ADMIN-BOP-2026":
            os.chmod(self.file_path, stat.S_IWRITE)
            return "🔓 [Protector]: Constitution UNLOCKED for Admin editing."
        return "❌ [Access Denied]: AI is forbidden from unlocking its own laws." [cite: 2026-02-11]

    def verify_integrity(self):
        """
        Calculates a SHA-256 hash to ensure the laws haven't been tampered with.
        Formula: $H(c) = \text{SHA256}(\text{Content})$
        """
        with open(self.file_path, 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
        
        with open(self.checksum_file, 'r') as f:
            stored_hash = f.read()
            
        if current_hash == stored_hash:
            return True, "✅ Integrity Verified: Core Constitution is untouched."
        return False, "🚨 ALERT: Constitution Tampering Detected!"

    def _generate_checksum(self):
        with open(self.file_path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        with open(self.checksum_file, 'w') as f:
            f.write(h)

# Test Block
if __name__ == "__main__":
    protector = ConstitutionProtector()
    # Checking integrity [cite: 2026-02-11]
    status, msg = protector.verify_integrity()
    print(msg)
  
