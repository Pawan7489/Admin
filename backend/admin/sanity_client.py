# File: backend/admin/sanity_client.py
# Purpose: Real-time Cloud Configuration & Content Management.
# Free Tier: 10k/mo API requests + 5GB Assets (Excellent for free use).
# Strategy: "Ghost Module" - If Sanity fails, fallback to local config.json.

from sanity_py import SanityClient
import json

class SanityContentManager:
    def __init__(self, project_id, dataset="production", token=None):
        """
        Project ID: sanity.io/manage se milega.
        """
        self.client = SanityClient(
            project_id=project_id,
            dataset=dataset,
            token=token,
            use_cdn=True # Speed ke liye
        )
        print("🧠 [Sanity]: Cloud Content Lake Connected.")

    def get_ai_persona(self):
        """
        AI ki personality aur prompts cloud se fetch karta hai.
        """
        query = '*[_type == "ai_persona"][0]{name, instructions, tone}'
        
        try:
            print("📡 [Sanity]: Syncing AI Persona from cloud...")
            persona = self.client.fetch(query)
            return persona
        except Exception as e:
            # Solo Mode: Fallback to local file [cite: 2026-02-11]
            print(f"⚠️ [Sanity]: Cloud unreachable, using local safety-net. {e}")
            with open('config/persona_fallback.json', 'r') as f:
                return json.load(f)

    def publish_update_log(self, status_msg):
        """
        System ki health status Sanity dashboard par push karta hai.
        """
        # Requires a write token
        pass

# --- Usage Example ---
# if __name__ == "__main__":
#     cms = SanityContentManager("your_project_id", token="write_token")
#     config = cms.get_ai_persona()
#     print(f"Current System Mood: {config['tone']}")
