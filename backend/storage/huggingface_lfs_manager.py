# File: backend/storage/huggingface_lfs_manager.py
# Purpose: Manages Active AI Models & Datasets on Hugging Face Hub using LFS.
# Strategy: Acts as an 'Active Repository' for version-controlled model storage.

import os
from huggingface_hub import HfApi, login, snapshot_download

class HuggingFaceLFSManager:
    def __init__(self, hf_token):
        """
        Initialize connection with Hugging Face.
        hf_token: Aapka 'Write' permission wala Access Token.
        """
        self.api = HfApi()
        self.token = hf_token
        # Auto-login to the Hub
        login(token=self.token, add_to_git_credential=True)
        print("🤗 [HF Manager]: Connected to Hugging Face Hub.")

    def create_repository(self, repo_name, repo_type="model", private=True):
        """
        Hub par naya repository banata hai agar wo exist nahi karta.
        repo_type options: 'model', 'dataset', 'space'
        """
        try:
            user = self.api.whoami(token=self.token)["name"]
            repo_id = f"{user}/{repo_name}"
            
            self.api.create_repo(repo_id=repo_id, repo_type=repo_type, private=private, exist_ok=True)
            print(f"✅ [HF Manager]: Repository '{repo_id}' is ready.")
            return repo_id
        except Exception as e:
            print(f"❌ [Error]: Could not create repo. {str(e)}")
            return None

    def push_model_to_hub(self, local_folder, repo_name, commit_message="Update model"):
        """
        Active Model Folder ko Cloud par upload (Push) karta hai via LFS.
        Yeh heavy files (.bin, .safetensors) ko automatically handle karta hai.
        """
        repo_id = self.create_repository(repo_name, repo_type="model")
        
        if repo_id:
            print(f"⬆️ [LFS Upload]: Pushing '{local_folder}' to {repo_id}...")
            try:
                self.api.upload_folder(
                    folder_path=local_folder,
                    repo_id=repo_id,
                    repo_type="model",
                    commit_message=commit_message
                )
                print(f"🎉 [Success]: Model is live at https://huggingface.co/{repo_id}")
                return True
            except Exception as e:
                print(f"❌ [Error]: Upload failed. {str(e)}")
                return False

    def pull_model_from_hub(self, repo_id, local_dir):
        """
        Cloud se Model ko wapas Local System par 'Pull' karta hai use karne ke liye.
        """
        print(f"⬇️ [LFS Download]: Fetching {repo_id} to {local_dir}...")
        try:
            snapshot_download(repo_id=repo_id, local_dir=local_dir, repo_type="model")
            print(f"✅ [Success]: Model downloaded and ready for Inference.")
            return True
        except Exception as e:
            print(f"❌ [Error]: Download failed. {str(e)}")
            return False

# --- Master Execution Block ---
if __name__ == "__main__":
    # 1. Apna Write Token yahan dalein (Settings -> Access Tokens se milega)
    MY_HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
    
    hf_manager = HuggingFaceLFSManager(MY_HF_TOKEN)

    # --- Scenario 1: Uploading a New Custom Model ---
    # Maan lijiye aapne Llama-3 ko fine-tune kiya hai 'my_custom_llama' folder mein
    local_model_path = "./my_custom_llama" 
    
    # Agar folder exist karta hai toh upload karein
    if os.path.exists(local_model_path):
        hf_manager.push_model_to_hub(
            local_folder=local_model_path,
            repo_name="A1-OS-Custom-Llama3",
            commit_message="Initial upload of fine-tuned model"
        )
    
    # --- Scenario 2: Downloading it back (on a different machine) ---
    # hf_manager.pull_model_from_hub(
    #     repo_id="username/A1-OS-Custom-Llama3", 
    #     local_dir="./downloaded_models/llama3"
    # )
  
