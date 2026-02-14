# File: backend/storage/pinata_ipfs.py
# Purpose: The "Immortal Storage" for unchangeable files.
# Free Tier: 1GB Storage + 100 Files.
# Logic: Uploads to IPFS via Pinata and returns a permanent CID (Content ID).

import requests
import os

class PinataIPFSManager:
    def __init__(self, api_key, secret_api_key):
        """
        Pinata Dashboard se API Keys lein.
        """
        self.headers = {
            "pinata_api_key": api_key,
            "pinata_secret_api_key": secret_api_key
        }
        self.pin_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        self.test_url = "https://api.pinata.cloud/data/testAuthentication"

    def check_connection(self):
        """Check karta hai ki keys sahi hain ya nahi."""
        try:
            response = requests.get(self.test_url, headers=self.headers)
            if response.status_code == 200:
                print("🌌 [Pinata]: Connected to IPFS Network.")
                return True
            else:
                print("❌ [Error]: Pinata Auth Failed.")
                return False
        except Exception as e:
            print(f"❌ [Error]: Connection Error. {e}")
            return False

    def upload_immutable_file(self, file_path):
        """
        File ko IPFS par upload karta hai.
        Result: Ek CID (e.g., QmXoyp...) milta hai jo file ka permanent address hai.
        """
        if not os.path.exists(file_path):
            print("⚠️ [Pinata]: File not found.")
            return None

        print(f"🚀 [Pinata]: Uploading '{file_path}' to the InterPlanetary System...")
        
        file_name = file_path.split("/")[-1]
        
        # Multipart upload request
        files = {
            'file': (file_name, open(file_path, 'rb'))
        }
        
        try:
            response = requests.post(self.pin_url, files=files, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                cid = data['IpfsHash']
                public_link = f"https://gateway.pinata.cloud/ipfs/{cid}"
                
                print(f"✅ [Success]: File Immortalized!")
                print(f"🔗 CID: {cid}")
                print(f"🌍 Public Link: {public_link}")
                return public_link
            else:
                print(f"❌ [Error]: Upload failed. {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ [Error]: API Request failed. {e}")
            return None

# --- Usage Strategy (Master Terminal) ---
if __name__ == "__main__":
    # Pinata Console se Keys lein
    API_KEY = "your_pinata_api_key"
    SECRET_KEY = "your_pinata_secret_key"
    
    ipfs = PinataIPFSManager(API_KEY, SECRET_KEY)
    
    if ipfs.check_connection():
        # Scenario: Core Constitution ko upload karna
        # Yeh file ab internet se tab tak delete nahi hogi jab tak Pinata account active hai
        ipfs.upload_immutable_file("constitution.json")
      
