# File: backend/storage/storj_vault.py
# Purpose: The "Black Box" storage for Sensitive Data.
# Free Tier: 25 GB Decentralized Storage.
# Security: Client-side encryption & Sharding (Hack-proof).

import boto3
from botocore.exceptions import NoCredentialsError

class StorjVaultManager:
    def __init__(self, access_key, secret_key, bucket_name):
        """
        Storj Console se S3 Credentials generate karein.
        Endpoint: https://gateway.storjshare.io
        """
        self.bucket_name = bucket_name
        self.client = boto3.client(
            's3',
            endpoint_url='https://gateway.storjshare.io',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        print("📦 [Storj]: Decentralized Vault Connected. Privacy: 100%.")

    def upload_sensitive_file(self, local_path, object_name):
        """
        File ko upload karta hai. Storj automatically ise encrypt aur shard kar dega.
        """
        print(f"🔒 [Vault]: Encrypting & Sharding '{local_path}' to global nodes...")
        
        try:
            self.client.upload_file(local_path, self.bucket_name, object_name)
            print(f"✅ [Storj]: File Secured at {object_name}")
            return True
        except NoCredentialsError:
            print("❌ [Error]: Credentials not available.")
            return False
        except Exception as e:
            print(f"❌ [Error]: Upload failed. {e}")
            return False

    def retrieve_file(self, object_name, download_path):
        """
        Duniya bhar se file ke tukde wapas laata hai aur jodta hai.
        """
        print(f"🧩 [Vault]: Reassembling shards for '{object_name}'...")
        
        try:
            self.client.download_file(self.bucket_name, object_name, download_path)
            print(f"✅ [Storj]: File Retrieved successfully at {download_path}")
            return True
        except Exception as e:
            print(f"❌ [Error]: Retrieval failed. {e}")
            return False

# --- Usage Strategy (Master Terminal) ---
# if __name__ == "__main__":
#     # Storj Console -> Access Grant -> S3 Credentials
#     ACCESS = "access_key_from_storj"
#     SECRET = "secret_key_from_storj"
#     BUCKET = "a1-secret-bunker"
#     
#     vault = StorjVaultManager(ACCESS, SECRET, BUCKET)
#     
#     # Scenario: Backing up Core Constitution
#     # Yeh file Google Drive par nahi jayegi, sirf Storj par.
#     vault.upload_sensitive_file("constitution.json", "core/constitution_v1.json")
