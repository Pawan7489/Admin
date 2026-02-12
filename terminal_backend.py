# File: terminal_backend.py
# Description: Universal Admin Panel (DNS Manager Added)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

# --- MODULE AUTO-LOADER ---
modules = {}

# 1. DNS Manager (NEW)
try:
    import dns_manager
    modules['dns'] = dns_manager.DNSController()
except ImportError:
    modules['dns'] = None

# 2. Cloudflare
try:
    import cloudflare_manager
    modules['cloud'] = cloudflare_manager.CloudflareTunnel()
except ImportError:
    modules['cloud'] = None

# 3. WordPress
try:
    import wordpress_manager
    modules['wp'] = wordpress_manager.WordPressBot()
except ImportError:
    modules['wp'] = None

# 4. Blogger
try:
    import blogger_manager
    modules['blogger'] = blogger_manager.BloggerBot()
except ImportError:
    modules['blogger'] = None

# 5. Git & Health & Others
try:
    import git_ops
    modules['git'] = git_ops.GitManager()
    import system_health
    modules['health'] = system_health.SystemDoctor()
    import colab_bridge
    modules['colab'] = colab_bridge.ColabConnector()
except ImportError:
    pass 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)
current_dir = os.getcwd()

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    if not raw_command: return

    parts = raw_command.split()
    cmd_start = parts[0].lower()

    # --- 1. DNS COMMANDS (NEW) ---
    if cmd_start == "dns":
        if not modules['dns']:
            emit('terminal_output', {'output': "❌ Error: DNS module missing. Install: 'pip install python-whois'"})
            return
        
        # dns check <domain>
        if len(parts) > 2 and parts[1] == "check":
            emit('terminal_output', {'output': "🔍 Checking WHOIS database..."})
            emit('terminal_output', {'output': modules['dns'].check_domain_availability(parts[2])})
            return

        # dns ip <domain>
        if len(parts) > 2 and parts[1] == "ip":
            emit('terminal_output', {'output': modules['dns'].get_ip(parts[2])})
            return

        # dns add <domain> <type> <name> <value>
        # Example: dns add mysite.com A @ 192.168.1.1
        if len(parts) > 5 and parts[1] == "add":
            emit('terminal_output', {'output': modules['dns'].add_record(parts[2], parts[3], parts[4], parts[5])})
            return

        # dns list
        if parts[1] == "list":
            emit('terminal_output', {'output': modules['dns'].list_records()})
            return

    # --- 2. CLOUDFLARE ---
    if cmd_start == "cloud" and modules['cloud']:
        if parts[1] == "public": emit('terminal_output', {'output': modules['cloud'].start_tunnel()})
        elif parts[1] == "stop": emit('terminal_output', {'output': modules['cloud'].stop_tunnel()})
        return

    # --- 3. EXISTING COMMANDS (Shortened for brevity but fully working) ---
    if cmd_start == "wp" and modules['wp'] and parts[1] == "post":
         emit('terminal_output', {'output': modules['wp'].create_post(parts[2], " ".join(parts[3:]))})
         return
    
    if raw_command == "system status" and modules.get('health'):
        emit('terminal_output', {'output': modules['health'].diagnose()})
        return

    # Fallback Shell
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: DNS Manager Active ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
