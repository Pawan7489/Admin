# File: hosting_manager.py
# Description: Universal Connector for Free Hosting Providers (Vercel, Netlify, Render, etc.)

import json
import os
import requests
import subprocess
from datetime import datetime

class HostingConnector:
    def __init__(self):
        self.registry_file = "hosting_inventory.json"
        self.load_registry()

    def load_registry(self):
        """Database load karta hai"""
        if not os.path.exists(self.registry_file):
            self.hosting_data = {}
            self.save_registry()
        else:
            try:
                with open(self.registry_file, "r") as f:
                    self.hosting_data = json.load(f)
            except:
                self.hosting_data = {}

    def save_registry(self):
        with open(self.registry_file, "w") as f:
            json.dump(self.hosting_data, f, indent=4)

    def add_hosting(self, name, provider, key_or_url):
        """
        Naya Hosting Account add karta hai.
        Provider Options: 'render', 'netlify', 'vercel', 'custom'
        Key_or_URL: 
           - Render/Netlify ke liye: 'Deploy Hook URL' (Settings se milta hai)
           - Vercel ke liye: 'API Token'
        """
        if name in self.hosting_data:
            return f"⚠️ Warning: '{name}' pehle se list mein hai."

        self.hosting_data[name] = {
            "provider": provider.lower(),
            "credential": key_or_url,
            "last_deploy": "Never",
            "added_on": str(datetime.now().strftime("%Y-%m-%d"))
        }
        self.save_registry()
        return f"✅ Success: '{name}' ({provider}) hosting list mein add ho gaya!"

    def remove_hosting(self, name):
        if name in self.hosting_data:
            del self.hosting_data[name]
            self.save_registry()
            return f"🗑️ Hosting '{name}' removed."
        else:
            return f"❌ Error: '{name}' nahi mila."

    def list_hosting(self):
        if not self.hosting_data:
            return "📭 Hosting List Khali Hai. 'hosting add' command use karein."

        output = "\n🌐 --- UNIVERSAL HOSTING CONNECTOR --- 🌐\n"
        output += f"{'NAME':<20} | {'PROVIDER':<15} | {'LAST DEPLOY':<20}\n"
        output += "-" * 60 + "\n"

        for name, details in self.hosting_data.items():
            output += f"{name:<20} | {details['provider']:<15} | {details['last_deploy']:<20}\n"
        
        output += "-" * 60 + "\n"
        return output

    def trigger_deploy(self, name):
        """
        Asli Jaadu: Website ko Deploy/Update karta hai.
        """
        if name not in self.hosting_data:
            return f"❌ Error: '{name}' register nahi hai."

        data = self.hosting_data[name]
        provider = data['provider']
        cred = data['credential']

        # LOGIC 1: Deploy Hooks (Render, Netlify, Custom)
        # Ye sabse fast hai, bas ek URL hit karna hota hai.
        if provider in ['render', 'netlify_hook', 'custom']:
            try:
                if not cred.startswith("http"):
                    return "❌ Error: Invalid URL. Deploy Hook http se shuru hona chahiye."
                
                response = requests.get(cred) if provider == 'render' else requests.post(cred)
                
                if response.status_code in [200, 201]:
                    self.hosting_data[name]['last_deploy'] = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
                    self.save_registry()
                    return f"🚀 DEPLOY TRIGGERED: '{name}' update ho raha hai! (Check live site in 1-2 mins)"
                else:
                    return f"❌ Failed: Server returned {response.status_code}"
            except Exception as e:
                return f"Connection Error: {str(e)}"

        # LOGIC 2: Vercel CLI (Token based)
        elif provider == 'vercel':
            try:
                # Vercel CLI install hona chahiye (npm i -g vercel)
                # Command: vercel --prod --token <TOKEN>
                cmd = f"vercel --prod --token {cred} --yes"
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                
                self.hosting_data[name]['last_deploy'] = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
                self.save_registry()
                return f"🚀 Vercel Deployment Started!\n{out.decode()}"
            except Exception as e:
                return f"CLI Error: {str(e)}"

        else:
            return "❌ Unknown Provider type."
      
