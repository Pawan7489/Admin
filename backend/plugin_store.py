# File: plugin_store.py
# Description: Universal Plugin Store (Search & Download WordPress/Custom Plugins)

import requests
import os
import json
import urllib.request

class PluginMarketplace:
    def __init__(self):
        self.download_folder = os.path.join(os.getcwd(), "downloaded_plugins")
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        
        # WordPress API Endpoint
        self.wp_api_url = "https://api.wordpress.org/plugins/info/1.2/"

    def search_wordpress(self, query):
        """
        WordPress.org ki Official Directory mein plugins search karta hai.
        """
        try:
            params = {
                "action": "query_plugins",
                "request[search]": query,
                "request[per_page]": 5  # Top 5 results layega
            }
            
            response = requests.get(self.wp_api_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                plugins = data.get('plugins', [])
                
                if not plugins:
                    return "❌ No plugins found."

                output = f"\n📦 --- WORDPRESS PLUGIN RESULTS: '{query}' --- 📦\n"
                for p in plugins:
                    output += f"🔹 Name: {p['name']}\n"
                    output += f"   Slug: {p['slug']} (Use this to download)\n"
                    output += f"   Rating: {p['rating']}/100 | Downloads: {p['downloaded']}\n"
                    output += f"   Description: {p['short_description'][:100]}...\n"
                    output += "-" * 50 + "\n"
                return output
            else:
                return f"❌ API Error: {response.status_code}"
                
        except Exception as e:
            return f"Search Error: {str(e)}"

    def download_wp_plugin(self, plugin_slug):
        """
        Plugin ke 'slug' (e.g., 'elementor', 'woocommerce') se 
        direct .zip file download karta hai.
        """
        download_url = f"https://downloads.wordpress.org/plugin/{plugin_slug}.zip"
        save_path = os.path.join(self.download_folder, f"{plugin_slug}.zip")
        
        try:
            print(f"⏳ Downloading {plugin_slug}...")
            # Downloading file
            urllib.request.urlretrieve(download_url, save_path)
            
            if os.path.exists(save_path):
                file_size = os.path.getsize(save_path) / (1024 * 1024) # MB conversion
                return f"✅ SUCCESS: Plugin saved at: {save_path} ({file_size:.2f} MB)\nAb aap ise kisi bhi WP site par upload kar sakte hain."
            else:
                return "❌ Download Failed."
                
        except Exception as e:
            return f"❌ Error Downloading: {str(e)}"

    def list_local_plugins(self):
        """Check karta hai ki humne abhi tak kaunse plugins download karke rakhe hain"""
        files = os.listdir(self.download_folder)
        if not files:
            return "📭 Local Store Khali Hai."
            
        output = "\n📂 --- DOWNLOADED PLUGINS (Ready to Install) ---\n"
        for f in files:
            if f.endswith(".zip"):
                output += f"💾 {f}\n"
        return output

# --- CUSTOM/PREMIUM PLUGIN REGISTRY ---
# Agar aapke paas koi paid plugin (jaise Elementor Pro) ki zip file hai,
# toh use system mein manually register karne ke liye.
    def register_custom_plugin(self, name, path):
        inventory_file = "custom_plugins.json"
        
        if os.path.exists(inventory_file):
            with open(inventory_file, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        data[name] = path
        
        with open(inventory_file, 'w') as f:
            json.dump(data, f)
            
        return f"✅ Custom Plugin '{name}' registered from {path}"

# Testing Block (Jab aap file run karenge to ye check karega)
if __name__ == "__main__":
    store = PluginMarketplace()
    print(store.search_wordpress("seo"))
      
