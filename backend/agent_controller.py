# File Path: backend/agent_controller.py
# Description: Manages the internal discussion between specialized agents. [cite: 2026-02-11]
# Ensures a balanced solution through consensus before showing output.

import json
import time

class AgentDialogueController:
    def __init__(self):
        self.agents = {
            "Coder": {"priority": 1, "focus": "Efficiency & Syntax"},
            "Security": {"priority": 1, "focus": "Vulnerabilities & Ethics"},
            "Strategist": {"priority": 2, "focus": "Scalability & Value"}
        }
        self.dialogue_history = []

    def initiate_discussion(self, task_description):
        """
        Agents ke beech discussion start karta hai. [cite: 2026-02-11]
        """
        print(f"🗨️ [Controller]: Starting Expert Dialogue for Task: '{task_description}'")
        
        round_1_results = {}
        for agent_name, profile in self.agents.items():
            # Simulating agent's internal thought process [cite: 2026-02-11]
            opinion = self._generate_agent_opinion(agent_name, task_description)
            round_1_results[agent_name] = opinion
            print(f"👤 [{agent_name}]: {opinion['summary']}")

        # Reaching Consensus
        final_verdict = self._reach_consensus(round_1_results)
        return final_verdict

    def _generate_agent_opinion(self, agent, task):
        """Har agent apne focus area ke hisaab se logic check karta hai."""
        # Simulated logic paths [cite: 2026-02-11]
        if agent == "Security":
            return {"summary": "No vulnerabilities found in the proposed logic.", "confidence": 0.98}
        elif agent == "Coder":
            return {"summary": "Code follows First Principles. Optimized for CPU.", "confidence": 0.95}
        else:
            return {"summary": "Solution is scalable for millions of users.", "confidence": 0.92}

    def _reach_consensus(self, results):
        """
        Consensus Logic: Calculates the Weighted Agreement Score ($A_w$).
        Formula: $A_w = \frac{\sum (Confidence_i \times Priority_i)}{\sum Priority_i}$
        """
        total_weighted_confidence = sum(r['confidence'] * self.agents[name]['priority'] for name, r in results.items())
        total_priority = sum(a['priority'] for a in self.agents.values())
        
        agreement_score = total_weighted_confidence / total_priority
        
        return {
            "agreement_index": round(agreement_score * 100, 2),
            "status": "APPROVED" if agreement_score > 0.90 else "NEEDS_REFINEMENT",
            "reasoning_path": results
        }

    def get_hidden_reasoning(self, verdict):
        """User ko dikhane se pehle internal logic verify karta hai. [cite: 2026-02-11]"""
        return f"Verified via {len(self.agents)} agents. Final Confidence: {verdict['agreement_index']}%"

# Test Block
if __name__ == "__main__":
    controller = AgentDialogueController()
    verdict = controller.initiate_discussion("Deploying a new sub-brain on Drive D.")
    print(f"\n🏆 Final Decision: {verdict['status']} ({verdict['agreement_index']}%)")
      
