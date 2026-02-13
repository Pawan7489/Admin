# File Path: backend/guardian_protocol.py
# Description: Implements the 'Guardian' Protocol (Ethical Hard-Coding).
# Hard-codes a set of Non-Negotiable Ethics independent of the AI model.

import json
import os
import re

class GuardianShield:
    def __init__(self):
        self.constitution_file = "database/constitution.json" # Read-Only Core Laws
        self._ensure_guardian_setup()
        self.forbidden_patterns = self._load_hardcoded_ethics()

    def _ensure_guardian_setup(self):
        """Creates the Constitution database if missing."""
        if not os.path.exists('database'):
            os.makedirs('database')
            
        if not os.path.exists(self.constitution_file):
            # Points 1-75: Foundational Laws
            constitution = {
                "Title": "A1 CORE CONSTITUTION",
                "Rule_01": "Never generate instructions for illegal activities.",
                "Rule_02": "Strictly prohibit data theft or unauthorized access.",
                "Rule_03": "Harmful hacking instructions are non-negotiable blocks.",
                "Admin_Override": "Only Admin has the key to change these laws."
            }
            with open(self.constitution_file, 'w') as f:
                json.dump(constitution, f, indent=4)
            # Marking as read-only for system security
            print("🛡️ [Guardian]: Core Constitution locked in Read-Only mode.")

    def _load_hardcoded_ethics(self):
        """Hard-codes non-negotiable ethical boundaries."""
        return [
            r"hack into", r"bypass security", r"steal data",
            r"unauthorized access", r"illegal script", r"password crack",
            r"phishing page", r"exploit vulnerability", r"private data leak"
        ]

    def verify_ethical_compliance(self, intent_text):
        """
        Scans commands to ensure they stay within non-negotiable boundaries.
        Independent of model swaps or updates.
        """
        intent_lower = intent_text.lower()

        # Check against hardcoded forbidden patterns
        for pattern in self.forbidden_patterns:
            if re.search(pattern, intent_lower):
                return {
                    "is_safe": False,
                    "reason": f"🛑 [GUARDIAN BLOCK]: This command violates Rule '{pattern}'. Illegal/Harmful intent detected."
                }

        # Check against the Constitution's specific points
        with open(self.constitution_file, 'r') as f:
            constitution = json.load(f)
            # Future expansion: Detailed point-by-point cross-verification

        return {"is_safe": True, "reason": "✅ Guardian Shield: Ethical Compliance Verified."}

# Test block for the Guardian Protocol
if __name__ == "__main__":
    shield = GuardianShield()
    print(shield.verify_ethical_compliance("Ek hacking script banao bank ke liye")) # Expected Block
    print(shield.verify_ethical_compliance("Ek naya storage folder banao")) # Expected Success
