# File: dns_manager.py
# Description: Manages Domains, WHOIS Lookups, and DNS Records

import socket
try:
    import whois # Library: python-whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

class DNSController:
    def __init__(self):
        self.simulated_records = [] # Testing ke liye memory database

    def check_domain_availability(self, domain):
        """
        Real WHOIS check karta hai ki domain khali hai ya nahi.
        """
        if not WHOIS_AVAILABLE:
            return "❌ Error: 'python-whois' library missing. Install via: pip install python-whois"

        try:
            w = whois.whois(domain)
            if w.domain_name:
                # Agar domain name wapas aya, matlab already registered hai
                return f"⚠️ Domain Taken: {domain}\n📅 Expiry: {w.expiration_date}\n🏢 Registrar: {w.registrar}"
            else:
                return f"✅ Available! Domain '{domain}' khali hai."
        except Exception:
            # Aksar agar domain nahi milta to error aata hai, matlab available hai
            return f"✅ Available! Domain '{domain}' register kiya ja sakta hai."

    def get_ip(self, domain):
        """Domain ka current IP address nikalta hai"""
        try:
            ip = socket.gethostbyname(domain)
            return f"🌐 {domain} points to IP: {ip}"
        except Exception as e:
            return f"❌ Error resolving IP: {str(e)}"

    def add_record(self, domain, record_type, name, value):
        """
        Simulates adding a DNS Record (A, CNAME, MX).
        Real API (GoDaddy/Cloudflare) connect karne ke liye API Key chahiye hogi.
        Abhi ye Simulation Mode me hai.
        """
        record = f"[{record_type}] {name}.{domain} -> {value}"
        self.simulated_records.append(record)
        return f"✅ DNS Record Added: {record} (Simulation Mode)"

    def list_records(self):
        """Shows current simulated records"""
        if not self.simulated_records:
            return "📭 No records found in session."
        return "\n".join(self.simulated_records)
      
