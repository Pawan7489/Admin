# File: backend/storage/infinite_storage_router.py
# Purpose: "Sundar Pichai Style" - Routes data to the best FREE storage provider.
# Logic: Central Controller for HF, Mongo, Drive, and Cloudinary.

import os
from .huggingface_lfs_manager import HuggingFaceLFSManager
from .mongodb_atlas_manager import MongoDBAtlasManager
from .cloudinary_manager import CloudinaryManager
# from .zero_cost_model_vault import ZeroCostModelVault (Google Drive)

class InfiniteStorageRouter:
    def __init__(self, config):
        self.hf = HuggingFaceLFSManager(config['HF_TOKEN'])
        self.mongo = MongoDBAtlasManager(config['MONGO_URI'])
        self.cloudinary = CloudinaryManager(
            config['CLD_NAME'], config['CLD_KEY'], config['CLD_SECRET']
        )
        # self.gdrive = ZeroCostModelVault(config['GDRIVE_CREDS'])

    def save_asset(self, asset_path, asset_type, asset_name):
        """
        Master Function: Decide karta hai kahan store karna hai.
        asset_type: 'model', 'image', 'metadata', 'backup'
        """
        print(f"🚦 [Router]: Routing '{asset_name}' ({asset_type})...")

        if asset_type == "model":
            # Models go to Hugging Face (Unlimited LFS)
            return self.hf.push_model_to_hub(asset_path, repo_name=asset_name)

        elif asset_type == "image":
            # Images go to Cloudinary (Media Optimization)
            return self.cloudinary.upload_image(asset_path)

        elif asset_type == "metadata":
            # Engine Lists go to MongoDB (Fast Text Search)
            return self.mongo.register_new_engine(asset_name, "Generic", "System")

        # elif asset_type == "backup":
            # Personal Backups go to Google Drive
            # return self.gdrive.process_and_backup(asset_path)

        else:
            print("⚠️ [Router]: Unknown Asset Type.")
            return None

# --- Execution Example ---
if __name__ == "__main__":
    # Load Environment Variables (Secure Vault)
    # Aapke Admin Panel mein ye hidden rahenge
    CONFIG = {
        'HF_TOKEN': "hf_xxx",
        'MONGO_URI': "mongodb+srv://xxx",
        'CLD_NAME': "xxx", 'CLD_KEY': "xxx", 'CLD_SECRET': "xxx",
        'GDRIVE_CREDS': "credentials.json"
    }

    router = InfiniteStorageRouter(CONFIG)

    # Scenario: AI ne ek image banayi
    router.save_asset("./temp/output.png", "image", "Futuristic_City")
    
    # Scenario: Naya Model Train hua
    router.save_asset("./models/Llama-3-FineTuned", "model", "A1-Llama-3")
  
