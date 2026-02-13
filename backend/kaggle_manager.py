# File: kaggle_manager.py
# Description: Manages Kaggle Datasets and API Authentication

import os
import json
import subprocess

class KaggleBot:
    def __init__(self):
        self.download_path = os.path.join(os.getcwd(), "kaggle_downloads")
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def setup_auth(self, username, key):
        """
        Kaggle API setup karta hai. 
        Ye function automatic 'kaggle.json' file create kar dega.
        """
        try:
            # 1. Determine Kaggle config path (usually ~/.kaggle/)
            home = os.path.expanduser("~")
            kaggle_dir = os.path.join(home, ".kaggle")
            
            if not os.path.exists(kaggle_dir):
                os.makedirs(kaggle_dir)
            
            # 2. Create kaggle.json
            config_file = os.path.join(kaggle_dir, "kaggle.json")
            data = {"username": username, "key": key}
            
            with open(config_file, "w") as f:
                json.dump(data, f)
            
            # 3. Security permission (Linux/Mac only, Windows ignores)
            try:
                os.chmod(config_file, 0o600)
            except:
                pass

            return "✅ Success: Kaggle API Configured! Ab aap download kar sakte hain."
        except Exception as e:
            return f"❌ Setup Error: {str(e)}"

    def download_dataset(self, dataset_name):
        """
        Example: download_dataset('heptapod/titanic')
        """
        try:
            # Command: kaggle datasets download -d <name> -p <path> --unzip
            cmd = f"kaggle datasets download -d {dataset_name} -p {self.download_path} --unzip"
            
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            
            if process.returncode == 0:
                return f"✅ Dataset Downloaded in 'kaggle_downloads' folder.\n{out.decode()}"
            else:
                return f"❌ Download Error: {err.decode()}"
        except Exception as e:
            return f"Critical Error: {str(e)}"

    def search_data(self, query):
        """
        Kaggle par datasets search karega
        """
        try:
            cmd = f"kaggle datasets list -s {query}"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            return f"🔍 Search Results:\n{out.decode()}"
        except Exception as e:
            return str(e)
