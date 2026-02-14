# File: backend/database/mongodb_atlas_manager.py
# Purpose: Manages the Master List of 10,000+ AI Engines & Services.
# Logic: Cloud Sync ensures data is available in Indore & Bhopal instantly.

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime

class MongoDBAtlasManager:
    def __init__(self, connection_string):
        """
        connection_string: MongoDB Atlas se mila hua URI (mongodb+srv://...).
        """
        self.uri = connection_string
        self.client = None
        self.db = None
        self.engine_collection = None
        self._connect_to_cloud()

    def _connect_to_cloud(self):
        """Cloud Database se secure connection banata hai."""
        print("☁️ [MongoDB]: Connecting to Atlas Cloud...")
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Check connection
            self.client.admin.command('ping')
            
            self.db = self.client['A1_God_Mode_DB']
            self.engine_collection = self.db['AI_Engines_Registry']
            
            print("✅ [MongoDB]: Connection Successful! Data is synced globally.")
            return True
        except ConnectionFailure:
            print("❌ [Error]: Could not connect to Atlas. Check Internet or URI.")
            return False

    def register_new_engine(self, engine_name, engine_type, source_path, status="Active"):
        """
        Naye AI Model (e.g., Llama-3, Gemma) ko database mein add karta hai.
        """
        engine_metadata = {
            "name": engine_name,          # e.g., "Llama-3-8B"
            "type": engine_type,          # e.g., "LLM", "Voice", "Vision"
            "source": source_path,        # e.g., "HuggingFace/meta-llama" or Local Path
            "status": status,             # "Active", "Training", "Offline"
            "last_updated": datetime.utcnow()
        }
        
        try:
            # Duplicate check
            if self.engine_collection.count_documents({"name": engine_name}) == 0:
                result = self.engine_collection.insert_one(engine_metadata)
                print(f"📝 [Registry]: Registered '{engine_name}' with ID: {result.inserted_id}")
                return str(result.inserted_id)
            else:
                print(f"⚠️ [Registry]: Engine '{engine_name}' already exists.")
                return None
        except Exception as e:
            print(f"❌ [Error]: Failed to register engine. {str(e)}")
            return None

    def get_active_engines(self):
        """
        Sirf wo engines return karta hai jo 'Active' hain (Attendance Sheet).
        """
        print("🔍 [MongoDB]: Fetching active AI fleet...")
        engines = self.engine_collection.find({"status": "Active"})
        
        active_list = []
        for eng in engines:
            active_list.append(f"{eng['name']} ({eng['type']})")
            
        return active_list

    def update_engine_status(self, engine_name, new_status):
        """
        Kisi engine ko 'Maintenance' ya 'Offline' mark karne ke liye.
        """
        self.engine_collection.update_one(
            {"name": engine_name},
            {"$set": {"status": new_status, "last_updated": datetime.utcnow()}}
        )
        print(f"🔄 [Status]: '{engine_name}' is now '{new_status}'.")

# --- Master Execution Block ---
if __name__ == "__main__":
    # Apna MongoDB Atlas Connection String yahan dalein
    # (Security ke liye ise .env file mein rakhna behtar hai)
    ATLAS_URI = "mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority"
    
    db_manager = MongoDBAtlasManager(ATLAS_URI)
    
    # 1. Naya Engine Register karein
    db_manager.register_new_engine(
        engine_name="Mistral-7B-v0.3",
        engine_type="LLM",
        source_path="HuggingFace/mistralai/Mistral-7B-v0.3"
    )
    
    # 2. List check karein
    active_fleet = db_manager.get_active_engines()
    print("🚀 Active Fleet:", active_fleet)
          
