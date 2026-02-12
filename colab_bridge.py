# File: colab_bridge.py
# Description: Generates connection scripts to link Google Colab with this Project

class ColabConnector:
    def __init__(self):
        self.project_name = "AI_Super_Genius"

    def get_setup_script(self):
        """
        Ye function ek Python script generate karta hai jo user ko 
        Google Colab me paste karna hoga connection ke liye.
        """
        script = f"""
# --- 🚀 STARTING BRIDGE TO LOCAL ADMIN PANEL ---
# Is code ko Colab cell me run karein

import os
from google.colab import drive

print("🔄 Connecting to Google Drive Bridge...")
drive.mount('/content/drive')

# Project Folder Setup
PROJECT_PATH = '/content/drive/MyDrive/{self.project_name}'

if not os.path.exists(PROJECT_PATH):
    print(f"⚠️ Project folder nahi mila. Creating new: {{PROJECT_PATH}}")
    os.makedirs(PROJECT_PATH)
else:
    print(f"✅ Project Found: {{PROJECT_PATH}}")

# Navigate to Project
os.chdir(PROJECT_PATH)
print(f"📂 Current Working Directory: {{os.getcwd()}}")

# Install Dependencies
print("⬇️ Installing Project Libraries...")
# Agar requirements.txt hai to install karo, nahi to basic tools
if os.path.exists('requirements.txt'):
    os.system('pip install -r requirements.txt')
else:
    os.system('pip install flask flask-socketio huggingface_hub')

print("\\n✅ BRIDGE ESTABLISHED! Aapka Colab ab Admin Panel files ke sath sync hai.")
print("Ab aap yahan se 'python terminal_backend.py' run kar sakte hain.")
"""
        return script

    def get_status(self):
        return "✅ Colab Bridge Module is Active. Type 'connect colab' to get the key."
      
