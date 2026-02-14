# File: backend/admin_panel/app.py
# Purpose: The Main Admin Dashboard hosted on Render.
# Connects to MongoDB Atlas to show real-time status of A1 OS.

import os
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# --- Configuration ---
# Render par Environment Variable set karein: MONGO_URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://...") # Local testing ke liye default
client = MongoClient(MONGO_URI)
db = client['A1_God_Mode_DB']
collection = db['AI_Engines_Registry']

@app.route('/')
def dashboard():
    """
    Main God Mode Dashboard.
    Database se saare Active Engines fetch karke HTML mein dikhata hai.
    """
    # Fetch only active engines
    active_engines = list(collection.find({"status": "Active"}))
    total_count = collection.count_documents({})
    
    return render_template('dashboard.html', engines=active_engines, count=total_count)

@app.route('/api/status', methods=['GET'])
def system_health():
    """Render Health Check endpoint."""
    return jsonify({"status": "Online", "location": "Render Cloud", "db": "Connected"})

@app.route('/api/add_engine', methods=['POST'])
def add_engine():
    """
    Naya AI Model register karne ke liye API endpoint.
    Admin Panel ke button se call hoga.
    """
    data = request.json
    new_engine = {
        "name": data.get("name"),
        "type": data.get("type"),
        "status": "Active"
    }
    collection.insert_one(new_engine)
    return jsonify({"message": "Engine Registered Successfully!"})

if __name__ == "__main__":
    # Gunicorn production mein ise handle karega
    app.run(host='0.0.0.0', port=5000)
  
