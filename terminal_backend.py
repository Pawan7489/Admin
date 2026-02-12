# File: terminal_backend.py
# Description: Universal Admin Panel (Separated Meta Modules)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

# --- MODULE AUTO-LOADER ---
modules = {}

# 1. Facebook Manager
try:
    import facebook_manager
    modules['fb'] = facebook_manager.FacebookBot()
except ImportError:
    modules['fb'] = None

# 2. Instagram Manager
try:
    import instagram_manager
    modules['insta'] = instagram_manager.InstaBot()
except ImportError:
    modules['insta'] = None

# 3. WhatsApp Manager
try:
    import whatsapp_manager
    modules['wa'] = whatsapp_manager.WhatsAppBot()
except ImportError:
    modules['wa'] = None

# 4. Telegram & Others (Existing)
try:
    import telegram_manager
    modules['tg'] = telegram_manager.TelegramBot()
    import cloudflare_manager
    modules['cloud'] = cloudflare_manager.CloudflareTunnel()
    import dns_manager
    modules['dns'] = dns_manager.DNSController()
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

    # --- 1. FACEBOOK COMMANDS ---
    if cmd_start == "fb":
        if not modules['fb']:
            emit('terminal_output', {'output': "❌ Error: 'facebook_manager.py' missing."})
            return
        
        # fb setup <token> <page_id>
        if parts[1] == "setup" and len(parts) == 4:
            emit('terminal_output', {'output': modules['fb'].setup(parts[2], parts[3])})
            return
        
        # fb post Hello World
        if parts[1] == "post":
            emit('terminal_output', {'output': modules['fb'].post_status(" ".join(parts[2:]))})
            return

    # --- 2. INSTAGRAM COMMANDS ---
    if cmd_start == "insta":
        if not modules['insta']:
            emit('terminal_output', {'output': "❌ Error: 'instagram_manager.py' missing."})
            return

        # insta setup <token> <account_id>
        if parts[1] == "setup" and len(parts) == 4:
            emit('terminal_output', {'output': modules['insta'].setup(parts[2], parts[3])})
            return

        # insta upload <url> <caption>
        if parts[1] == "upload":
            if len(parts) < 4:
                emit('terminal_output', {'output': "Usage: insta upload <ImageURL> <Caption>"})
            else:
                emit('terminal_output', {'output': modules['insta'].upload_photo(parts[2], " ".join(parts[3:]))})
            return

    # --- 3. WHATSAPP COMMANDS ---
    if cmd_start == "wa":
        if not modules['wa']:
            emit('terminal_output', {'output': "❌ Error: 'whatsapp_manager.py' missing."})
            return

        # wa setup <token> <phone_id>
        if parts[1] == "setup" and len(parts) == 4:
            emit('terminal_output', {'output': modules['wa'].setup(parts[2], parts[3])})
            return

        # wa send <number> <message>
        if parts[1] == "send":
            if len(parts) < 4:
                emit('terminal_output', {'output': "Usage: wa send <Number> <Message>"})
            else:
                emit('terminal_output', {'output': modules['wa'].send_msg(parts[2], " ".join(parts[3:]))})
            return

    # --- 4. TELEGRAM & SYSTEM COMMANDS (Existing) ---
    if cmd_start == "telegram" and modules.get('tg'):
        if parts[1] == "send": emit('terminal_output', {'output': modules['tg'].send_message(" ".join(parts[2:]))})
        return

    if cmd_start == "cloud" and modules.get('cloud'):
        if parts[1] == "public": emit('terminal_output', {'output': modules['cloud'].start_tunnel()})
        elif parts[1] == "stop": emit('terminal_output', {'output': modules['cloud'].stop_tunnel()})
        return

    # Fallback Shell
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: FB, Insta, WA separated ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
