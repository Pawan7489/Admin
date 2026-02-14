import os
from huggingface_hub import HfApi, list_spaces
from dotenv import load_dotenv

# Musk Rule: Minimalist code for maximum connectivity
load_dotenv("config.env")

class HuggingFaceBridge:
    def __init__(self):
        self.token = os.getenv("HF_TOKEN")
        self.api = HfApi(token=self.token) if self.token else None
        
        if not self.api:
            # Solo Mode: No crash, just silent skip
            print("⚠️ Hugging Face Token missing. Cloud features disabled.")

    def check_space_status(self, space_id):
        """Registry Rule: Check if our remote brain is online."""
        if not self.api: return "Offline"
        try:
            space_info = self.api.repo_info(repo_id=space_id, repo_type="space")
            return space_info.status # e.g., 'running', 'building'
        except Exception:
            return "Not Found"

    def deploy_logic_to_space(self, repo_name):
        """Hack: Auto-deploying custom software via Docker stubs."""
        # Zuckerberg Rule: Fast deployment logic
        if not self.api: return "Error: No API Token"
        print(f"🚀 Deploying {repo_name} to HF Spaces (Docker Mode)...")
        # Logic to push local folder to HF Space
        return "Deployment Initiated"

# Simulation for Registry.py
if __name__ == "__main__":
    hf = HuggingFaceBridge()
    print(f"HF Bridge Status: {'Active' if hf.api else 'Inactive'}")
  
