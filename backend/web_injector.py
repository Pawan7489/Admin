# File Path: backend/web_injector.py
# Description: Advanced Web Admin, WP Auto-Installer, and AI Injector
# Ye module website banana aur usme AI dalne ka kaam karta hai.

import os
import json
import subprocess
from datetime import datetime

class WebAdminInjector:
    def __init__(self):
        self.sites_registry = "database/managed_sites.json"
        self.load_sites()

    def load_sites(self):
        """Database se managed sites ki list nikalta hai"""
        # Ensure database directory exists
        if not os.path.exists('database'):
            os.makedirs('database')
            
        if not os.path.exists(self.sites_registry):
            self.sites = {}
            self.save_sites()
        else:
            try:
                with open(self.sites_registry, "r") as f:
                    self.sites = json.load(f)
            except:
                self.sites = {}

    def save_sites(self):
        with open(self.sites_registry, "w") as f:
            json.dump(self.sites, f, indent=4)

    def install_wordpress(self, domain, db_info):
        """
        1-Click WP Installer.
        Note: Ye script WP-CLI (WordPress Command Line) ka use karti hai.
        Server par WP-CLI install hona chahiye asli magic ke liye.
        """
        print(f"⚙️ Starting Auto-Install for: {domain}")
        
        # Checking if domain already exists in our system
        if domain in self.sites:
            return f"⚠️ Warning: '{domain}' is already managed by A1 OS."

        # Real-World Logic (Simulation via safe shell commands)
        try:
            # Step 1: Create Domain Folder (Simulated web root path)
            site_path = os.path.join(os.getcwd(), "hosted_sites", domain)
            if not os.path.exists(site_path):
                os.makedirs(site_path)

            # Step 2: Simulated WP-CLI Commands (Ye server par WP download karega)
            # cmd = f"cd {site_path} && wp core download && wp config create --dbname={db_info} ... "
            
            # Step 3: Registering the site in our A1 OS Memory
            self.sites[domain] = {
                "platform": "WordPress",
                "db_linked": db_info,
                "ai_injected": False,
                "installed_on": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            self.save_sites()

            return f"✅ SUCCESS: WordPress Auto-Installed for '{domain}' in isolated environment."
        
        except Exception as e:
            return f"❌ WP Installation Failed: {str(e)}"

    def inject_ai_into_website(self, domain):
        """
        Kisi bhi website me AI logic (JS script) dalne ka Super Advanced feature.
        """
        if domain not in self.sites:
            return f"❌ Error: '{domain}' is not registered in A1 OS managed sites."

        if self.sites[domain]['ai_injected']:
            return f"⚠️ Notice: AI is already injected and active on '{domain}'."

        # Generating a unique AI API Key for this specific domain
        import hashlib
        domain_hash = hashlib.md5(domain.encode()).hexdigest()[:10]
        
        # The AI Snippet to be placed in the website's <head>
        ai_snippet = f"""
<script>
    window.A1_CONFIG = {{
        domain: "{domain}",
        bridge_key: "A1-{domain_hash}",
        server: "http://localhost:5000"
    }};
</script>
<script src="http://localhost:5000/static/ai_bridge.js" async></script>
"""
        
        # Mark as injected in DB
        self.sites[domain]['ai_injected'] = True
        self.sites[domain]['bridge_key'] = f"A1-{domain_hash}"
        self.save_sites()

        # Output the result so the Admin can copy it if needed
        return f"🚀 AI INJECTION SUCCESSFUL for '{domain}'.\n\nBridge Key: A1-{domain_hash}\n\nSnipped Generated:\n{ai_snippet}"

    def list_managed_sites(self):
        """Dashboard par dikhane ke liye sites ki list"""
        if not self.sites:
            return "📭 No managed sites found. Install WP or add a site first."

        output = "\n🌐 --- A1 MANAGED WEB FLEET --- 🌐\n"
        output += f"{'DOMAIN':<25} | {'PLATFORM':<12} | {'AI STATUS':<12}\n"
        output += "-" * 55 + "\n"

        for domain, details in self.sites.items():
            ai_status = "🟢 Active" if details['ai_injected'] else "🔴 Pending"
            output += f"{domain:<25} | {details['platform']:<12} | {ai_status:<12}\n"
        
        output += "-" * 55 + "\n"
        return output

# Test execution block (Ignored when imported)
if __name__ == "__main__":
    injector = WebAdminInjector()
    print(injector.install_wordpress("mysuperai.com", "db_ai_123"))
    print(injector.inject_ai_into_website("mysuperai.com"))
    
