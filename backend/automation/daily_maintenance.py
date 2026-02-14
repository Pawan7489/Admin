# File: backend/automation/daily_maintenance.py
# Purpose: The "Janitor" script hosted on PythonAnywhere.
# Trigger: Runs automatically once a day via Scheduled Tasks.
# Task: Cleans old logs from MongoDB and summarizes system health.

import os
import datetime
from pymongo import MongoClient

class SystemJanitor:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client['A1_God_Mode_DB']
        self.logs = self.db['system_logs']
        self.stats = self.db['daily_stats']

    def clean_old_logs(self, days=7):
        """
        7 din se purane logs delete karta hai taaki DB bhare nahi.
        """
        print("🧹 [Janitor]: Checking for old trash logs...")
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        
        result = self.logs.delete_many({"timestamp": {"$lt": cutoff_date}})
        print(f"🗑️ [Janitor]: Deleted {result.deleted_count} old log entries.")
        return result.deleted_count

    def generate_daily_report(self):
        """
        Aaj ka hisaab-kitaab (Summary) banata hai.
        """
        today = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Count total active engines
        active_engines = self.db['AI_Engines_Registry'].count_documents({"status": "Active"})
        
        # Save daily stat
        report = {
            "date": today,
            "active_engines": active_engines,
            "maintenance_done": True,
            "platform": "PythonAnywhere"
        }
        
        self.stats.insert_one(report)
        print(f"✅ [Janitor]: Daily Report Saved: {report}")

# --- Execution Block ---
if __name__ == "__main__":
    # PythonAnywhere environment variables set karne padte hain
    # Ya direct string use karein (Secure nahi hai par free tier limit hai)
    MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/..."
    
    janitor = SystemJanitor(MONGO_URI)
    
    # 1. Safai karo
    janitor.clean_old_logs(days=7)
    
    # 2. Report banao
    janitor.generate_daily_report()
  
