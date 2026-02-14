# File: backend/storage/cloudinary_manager.py
# Purpose: Stores AI-generated images on Cloudinary (Free Tier).
# Benefit: Saves local disk space and provides fast CDN links.

import cloudinary
import cloudinary.uploader
import cloudinary.api

class CloudinaryManager:
    def __init__(self, cloud_name, api_key, api_secret):
        """
        Cloudinary connection initialize karta hai.
        Credentials dashboard se milenge.
        """
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        print("☁️ [Cloudinary]: Media Storage Connected.")

    def upload_image(self, file_path, folder_name="A1_OS_Images"):
        """
        Local image ko Cloud par upload karta hai aur URL return karta hai.
        """
        print(f"🖼️ [Media]: Uploading {file_path} to Cloudinary...")
        try:
            response = cloudinary.uploader.upload(
                file_path,
                folder=folder_name,
                resource_type="image"
            )
            # Public URL jo hum user ko dikhayenge
            image_url = response['secure_url']
            print(f"✅ [Success]: Image Hosted at {image_url}")
            return image_url
        except Exception as e:
            print(f"❌ [Error]: Image Upload Failed. {e}")
            return None

# --- Usage ---
# cld = CloudinaryManager("my_cloud", "key", "secret")
# url = cld.upload_image("generated_cat.png")
