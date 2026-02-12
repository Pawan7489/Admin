# File: terminal_backend.py
# Description: Universal Admin Panel (Unlimited Storage Boxes Added)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

# --- MODULE AUTO-LOADER ---
modules = {}

# 1. Storage Manager (NEW)
try:
    import storage_manager
    modules['storage'] = storage_manager.StorageRegistry()
except ImportError:
    modules['storage'] = None

# 2. Meta (FB/Insta/WA)
try:
    import facebook_manager
    modules['fb'] = facebook_manager.FacebookBot()
    import instagram_manager
    modules['insta'] = instagram_manager.InstaBot()
    import whatsapp_manager
    modules['wa'] = whatsapp_manager.WhatsAppBot()
except ImportError:
    pass

# 3. Other Tools
try:
    import cloudflare_manager
    modules['cloud'] = cloudflare_manager.CloudflareTunnel()
    import dns_manager
    modules['dns'] = dns_manager.DNSController()
    import telegram_manager
    modules['tg'] = telegram_manager.TelegramBot()
    import git_ops
    modules['git'] = git_ops.GitManager()
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

    # --- 1. STORAGE COMMANDS (Unlimited Boxes) ---
    if cmd_start == "storage":
        if not modules['storage']:
            emit('terminal_output', {'output': "❌ Error: 'storage_manager.py' missing."})
            return

        # Command: storage add <Name> <Provider> <URL/API>
        # Example: storage add MyDrive Google https://api.google.com/xyz
        if parts[1] == "add":
            if len(parts) < 5:
                emit('terminal_output', {'output': "Usage: storage add <UniqueName> <Provider> <API_Key_or_URL>"})
            else:
                name = parts[2]
                provider = parts[3]
                cred = " ".join(parts[4:]) # URL/Key me spaces ho sakte hain
                emit('terminal_output', {'output': modules['storage'].add_storage(name, provider, cred)})
            return

        # Command: storage list
        if parts[1] == "list":
            emit('terminal_output', {'output': modules['storage'].list_storage()})
            return

        # Command: storage remove <Name>
        if parts[1] == "remove" or parts[1] == "delete":
            emit('terminal_output', {'output': modules['storage'].remove_storage(parts[2])})
            return

    # --- 2. META COMMANDS ---
    if cmd_start == "fb" and modules.get('fb'):
        if parts[1] == "post": emit('terminal_output', {'output': modules['fb'].post_status(" ".join(parts[2:]))})
        return
    if cmd_start == "wa" and modules.get('wa'):
        if parts[1] == "send": emit('terminal_output', {'output': modules['wa'].send_msg(parts[2], " ".join(parts[3:]))})
        return

    # --- 3. SYSTEM COMMANDS ---
    if cmd_start == "cloud" and modules.get('cloud'):
        if parts[1] == "public": emit('terminal_output', {'output': modules['cloud'].start_tunnel()})
        return

    if cmd_start == "telegram" and modules.get('tg'):
        if parts[1] == "send": emit('terminal_output', {'output': modules['tg'].send_message(" ".join(parts[2:]))})
        return

    # Fallback Shell
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: Unlimited Storage System Active ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
