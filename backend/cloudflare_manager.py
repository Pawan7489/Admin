# File: cloudflare_manager.py
# Description: Manages Cloudflare Tunnels to expose Localhost to the World

import os
import platform
import subprocess
import requests
import time
import threading

class CloudflareTunnel:
    def __init__(self):
        self.system = platform.system()
        self.binary_name = "cloudflared.exe" if self.system == "Windows" else "cloudflared"
        self.tunnel_process = None
        self.public_url = None

    def check_install(self):
        """Checks if cloudflared tool exists, else downloads it."""
        if os.path.exists(self.binary_name):
            return True
        
        print("⬇️ Cloudflare tool missing. Downloading automatically...")
        try:
            if self.system == "Windows":
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
            elif self.system == "Linux":
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
            else:
                return False # Mac logic add kar sakte hain baad me

            # Download Logic
            r = requests.get(url, stream=True)
            with open(self.binary_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: f.write(chunk)
            
            # Permissions set karo (Linux ke liye)
            if self.system != "Windows":
                os.chmod(self.binary_name, 0o777)
                
            return True
        except Exception as e:
            print(f"Download Error: {e}")
            return False

    def start_tunnel(self, port=5000):
        """Starts the tunnel on the given port."""
        if self.tunnel_process:
            return f"⚠️ Tunnel already running at: {self.public_url}"

        if not self.check_install():
            return "❌ Error: Could not install Cloudflare tool."

        # Command run karo background me
        cmd = [f"./{self.binary_name}" if self.system != "Windows" else self.binary_name, "tunnel", "--url", f"localhost:{port}"]
        
        try:
            # Output capture karne ke liye process start
            self.tunnel_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            
            # URL dhundhne ke liye thread (Kyunki Cloudflare URL thodi der baad deta hai)
            def find_url():
                for line in iter(self.tunnel_process.stderr.readline, ''):
                    if "trycloudflare.com" in line:
                        # URL extract logic
                        import re
                        url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                        if url_match:
                            self.public_url = url_match.group(0)
                            break
            
            t = threading.Thread(target=find_url)
            t.daemon = True
            t.start()
            
            # Thoda wait karo URL aane ka
            time.sleep(5)
            
            if self.public_url:
                return f"✅ ONLINE! Public URL: {self.public_url}"
            else:
                return "⏳ Tunnel starting... Check logs in 10 seconds."

        except Exception as e:
            return f"Error starting tunnel: {str(e)}"

    def stop_tunnel(self):
        """Stops the tunnel."""
        if self.tunnel_process:
            self.tunnel_process.terminate()
            self.tunnel_process = None
            self.public_url = None
            return "🛑 Tunnel Stopped. Site is now Offline."
        else:
            return "⚠️ No active tunnel found."
          
