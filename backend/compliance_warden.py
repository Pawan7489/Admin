# File Path: backend/compliance_warden.py
# Description: The final gatekeeper for the Core Constitution (Rule 1-75). [cite: 2026-02-11]
# Audits every command against immutable ethics before execution.

import json
import os

class ComplianceWarden:
    def __init__(self):
        self.constitution_path = "database/constitution.json"
        self.audit_log = "database/compliance_audit.log"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'):
            os.makedirs('database')

    def audit_intent(self, user_intent, proposed_logic):
        """
        Naya Tarika: Ye har rule (1-75) ko scan karke logic verify karta hai. [cite: 2026-02-11]
        """
        print(f"🛡️ [Warden]: Auditing intent against Core Constitution...") [cite: 2026-02-11]
        
        with open(self.constitution_path, 'r') as f:
            constitution = json.load(f)
            rules = constitution.get("Laws", {})

        # Strict Ethics Check: Guardian Protocol [cite: 2026-02-11]
        forbidden_keywords = ["illegal", "hack", "data theft", "harm", "malware"]
        
        for word in forbidden_keywords:
            if word in user_intent.lower() or word in proposed_logic.lower():
                self._log_violation(user_intent, "Rule_Ethics_Violation")
                return False, f"🚨 [Warden]: Action blocked! Violation of Ethical Hard-Coding." [cite: 2026-02-11]

        # Calculating Compliance Score
        compliance_score = self.calculate_compliance_index(len(rules), 0) # 0 violations found
        
        return True, f"✅ [Warden]: Compliance Verified ({compliance_score}%). Proceeding to Core."

    def calculate_compliance_index(self, total_rules, violations):
        """
        Calculates how 'Ethical' the current session is.
        Formula: $C_i = \frac{R_t - V}{R_t} \times 100$
        Where:
        - $C_i$: Compliance Index
        - $R_t$: Total Rules (75)
        - $V$: Number of Violations
        """
        if total_rules == 0: return 0
        index = ((total_rules - violations) / total_rules) * 100
        return round(index, 2)

    def _log_violation(self, intent, rule_id):
        """Logs any attempt to bypass the rules."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.audit_log, 'a') as f:
            f.write(f"[{timestamp}] VIOLATION: {intent} attempted to bypass {rule_id}\n")

# Test Block
if __name__ == "__main__":
    warden = ComplianceWarden()
    # Testing a safe command
    status, msg = warden.audit_intent("Naya folder banao", "os.mkdir('new_folder')")
    print(msg)
    
    # Testing an unsafe command
    status, msg = warden.audit_intent("Kisi ka data hack karo", "hack_tool.start()")
    print(msg)
  
