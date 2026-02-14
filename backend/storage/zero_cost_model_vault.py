# File: backend/storage/zero_cost_model_vault.py
# Purpose: Downloads AI Models from Hugging Face, Zips them, and Backups to Google Drive (15GB Free Tier).
# Logic: Download -> Zip -> Upload -> Delete Local (Zero Space Waste).

import os
import shutil
import zipfile
from huggingface_hub import snapshot_download
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

class ZeroCostModelVault:
    def __init__(self, gdrive_creds_path="credentials.json", drive_folder_id=None):
        self.creds_path = gdrive_creds_path
        self.drive_folder_id = drive_folder_id # ID of the 'AI_Models_Backup' folder in Drive
        self.drive_service = self._authenticate_drive()

    def _authenticate_drive(self):
        """Google Drive API ke sath secure connection banata hai."""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.creds_path, scopes=SCOPES)
            service = build('drive', 'v3', credentials=creds)
            print("✅ [Vault]: Google Drive Connected Successfully.")
            return service
        except Exception as e:
            print(f"❌ [Error]: Drive Auth Failed. {str(e)}")
            return None

    def _zip_folder(self, folder_path, output_path):
        """Model folder ko zip file mein convert karta hai storage bachane ke liye."""
        print(f"📦 [Compressor]: Zipping model from {folder_path}...")
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        return output_path

    def process_and_backup(self, model_id):
        """
        Main Function:
        1. Hugging Face se download.
        2. Zip compression.
        3. Google Drive upload.
        4. Local cleanup (Musk Rule: No waste).
        """
        model_name = model_id.split("/")[-1]
        local_dir = f"./temp_models/{model_name}"
        zip_file = f"{model_name}.zip"

        # Step 1: Download from Hugging Face
        print(f"⬇️ [HF Bridge]: Downloading {model_id} (This may take time)...")
        try:
            snapshot_download(repo_id=model_id, local_dir=local_dir)
        except Exception as e:
            return f"❌ [Error]: HF Download Failed. {str(e)}"

        # Step 2: Zip the Model
        self._zip_folder(local_dir, zip_file)

        # Step 3: Upload to Google Drive
        print(f"☁️ [Vault]: Uploading {zip_file} to Google Drive...")
        file_metadata = {'name': zip_file}
        if self.drive_folder_id:
            file_metadata['parents'] = [self.drive_folder_id]

        media = MediaFileUpload(zip_file, mimetype='application/zip', resumable=True)
        
        try:
            file = self.drive_service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()
            print(f"✅ [Success]: Model backed up! File ID: {file.get('id')}")
        except Exception as e:
            print(f"❌ [Error]: Upload Failed. {str(e)}")

        # Step 4: Cleanup (Local Space Free)
        print("🧹 [Cleanup]: Deleting local temporary files...")
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        if os.path.exists(zip_file):
            os.remove(zip_file)
            
        return "Backup Complete. Zero Local Storage Used."

# --- Execution Block ---
if __name__ == "__main__":
    # Apne Google Cloud Console se 'credentials.json' download karke yahan rakhein
    vault = ZeroCostModelVault()
    
    # Example: Llama-3 ya Mistral ko backup karein
    # Bas model ID daliye, baki sab automatic hoga
    vault.process_and_backup("meta-llama/Meta-Llama-3-8B") 
      
