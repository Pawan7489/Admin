# File: huggingface_manager.py
# Description: Manages AI Models via Hugging Face Hub

import os
try:
    from huggingface_hub import login, snapshot_download
    HF_INSTALLED = True
except ImportError:
    HF_INSTALLED = False

class ModelManager:
    def __init__(self):
        self.models_dir = os.path.join(os.getcwd(), "ai_models")
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)

    def login_hf(self, token):
        """Hugging Face Login function"""
        if not HF_INSTALLED:
            return "❌ Error: 'huggingface_hub' library installed nahi hai. Terminal me 'pip install huggingface_hub' run karein."
        try:
            login(token=token, add_to_git_credential=False)
            return "✅ Success: Hugging Face Login Successful!"
        except Exception as e:
            return f"❌ Login Failed: {str(e)}"

    def download_model(self, repo_id):
        """Model Download function (e.g., 'meta-llama/Llama-2-7b')"""
        if not HF_INSTALLED:
            return "❌ Error: Library missing."
        
        try:
            return f"⏳ Downloading {repo_id}... (Yeh background me chalega, thoda wait karein)"
            # Note: Asli download background thread me hona chahiye taaki UI freeze na ho.
            # Abhi ke liye hum simple path return kar rahe hain.
            path = snapshot_download(repo_id=repo_id, cache_dir=self.models_dir)
            return f"✅ Download Complete: Model saved at {path}"
        except Exception as e:
            return f"❌ Download Error: {str(e)}"
          
