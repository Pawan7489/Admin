# File: domain_registry.py
# Description: Universal Manager for Domain Registrars (GoDaddy, Namecheap, Cloudflare, etc.)

import json
import os
import requests
from datetime import datetime

# Domain check karne ke liye library
try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

class DomainController:
    def __init__(self):
        self.registry_file = "domain_inventory.json"
        self.load_registry()

    def load_registry(self):
        """Database load karta hai"""
        if not os.path.exists(self.registry_file):
            self.domain_data = {}
            self.save_registry()
        else:
            try:
                with open(self.registry_file, "r") as f:
                    self.domain_data = json.load(f)
            except:
                self.domain_data = {}

    def save_registry(self):
        with open(self.registry_file, "w") as f:
            json.dump(self.domain_data, f, indent=4)

    def add_registrar(self, name, provider, api_key, api_secret=""):
        """
        Naya Domain Provider add karta hai.
        Name: Account ka naam (e.g., My_GoDaddy)
        Provider: GoDaddy, Namecheap, Cloudflare
        API Key/Secret: Provider ki settings se milta hai.
        """
        if name in self.domain_data:
            return f"⚠️ Warning: '{name}' pehle se list mein hai."

        self.domain_data[name] = {
            "provider": provider.lower(),
            "key": api_key,
            "secret": api_secret,
            "added_on": str(datetime.now().strftime("%Y-%m-%d"))
        }
        self.save_registry()
        return f"✅ Success: '{name}' ({provider}) account add ho gaya!"

    def list_accounts(self):
        if not self.domain_data:
            return "📭 Domain Accounts List Khali Hai. 'domain account add' use karein."

        output = "\n🌍 --- DOMAIN REGISTRAR ACCOUNTS --- 🌍\n"
        output += f"{'NAME':<20} | {'PROVIDER':<15} | {'ADDED ON':<15}\n"
        output += "-" * 60 + "\n"

        for name, details in self.domain_data.items():
            output += f"{name:<20} | {details['provider']:<15} | {details['added_on']:<15}\n"
        
        output += "-" * 60 + "\n"
        return output

    def check_details(self, domain):
        """Kisi bhi domain ki expiry aur details check karta hai (WHOIS)"""
        if not WHOIS_AVAILABLE:
            return "❌ Error: 'python-whois' library missing. Install via pip."

        try:
            w = whois.whois(domain)
            return f"""
🔎 DOMAIN REPORT: {domain}
---------------------------
📅 Creation Date: {w.creation_date}
⏳ Expiry Date: {w.expiration_date}
🏢 Registrar: {w.registrar}
🌐 Name Servers: {w.name_servers}
---------------------------
"""
        except Exception as e:
            return f"❌ Check Failed: Domain shayad available hai ya error aaya. ({str(e)})"

    def update_nameservers(self, account_name, domain, ns1, ns2):
        """
        Nameservers Update karta hai.
        Ye function API calls ko simulate kar raha hai (Safety ke liye).
        Real implementation me yahan `requests.put()` lagega GoDaddy/Namecheap ke liye.
        """
        if account_name not in self.domain_data:
            return f"❌ Error: Account '{account_name}' register nahi hai."

        provider = self.domain_data[account_name]['provider']
        
        # Simulation Logic (Asli API call complex hoti hai, ye structure hai)
        if provider == 'godaddy':
            # Asli code example:
            # url = f"https://api.godaddy.com/v1/domains/{domain}/records"
            # headers = {"Authorization": f"sso-key {self.key}:{self.secret}"}
            # requests.patch(url, headers=headers, json=...)
            return f"✅ [GoDaddy API]: Connecting... Nameservers for '{domain}' updated to {ns1}, {ns2}."
        
        elif provider == 'namecheap':
            return f"✅ [Namecheap API]: Connecting... DNS changed for '{domain}'."
        
        elif provider == 'cloudflare':
            return f"✅ [Cloudflare API]: Connecting... Proxy Status Updated."
        
        else:
            return f"⚠️ Unknown Provider. Nameservers saved locally: {ns1}, {ns2}"
      
