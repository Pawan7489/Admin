# Sub-File 86-C: A native browsing environment within the C-Panel.
# Prevents context-switching and keeps the user inside the 'World Hub'.

import requests

class InnerBrowserCore:
    def surf_internal(self, target_url):
        """Panel ke andar hi external website ya API ka data load karta hai."""
        print(f"🌍 [Inner Internet]: Fetching data from {target_url}...")
        # Securely fetching data without leaving the A1 OS environment
        try:
            response = requests.get(target_url, timeout=5)
            return f"✅ [Browser]: Successfully loaded {len(response.content)} bytes."
        except Exception as e:
            return f"❌ [Browser Error]: {str(e)}"
          
