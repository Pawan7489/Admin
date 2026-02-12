# File: terminal_backend.py
# Description: Universal Admin Panel (Unlimited Engines + Storage)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

# --- MODULE AUTO-LOADER ---
modules = {}

# 1. Engine Manager (NEW)
try:
    import engine_manager
    modules['engine'] = engine_manager.EngineRegistry()
except ImportError:
    modules['engine'] = None

# 2. Storage Manager
try:
    import storage_manager
    modules['storage'] = storage_manager.StorageRegistry()
except ImportError:
    modules['storage'] = None

# 3. Meta (FB/Insta/WA)
try:
    import facebook_manager
    modules['fb'] = facebook_manager.FacebookBot()
    import instagram_manager
    modules['insta'] = instagram_manager.InstaBot()
    import whatsapp_manager
    modules['wa'] = whatsapp_manager.WhatsAppBot()
except ImportError:
    pass

# 4. Other Tools (Cloud, TG, etc.)
try:
    import cloudflare_manager
    modules['cloud'] = cloudflare_manager.CloudflareTunnel()
    import telegram_manager
    modules['tg'] = telegram_manager.TelegramBot()
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

    # --- 1. ENGINE COMMANDS (Start/Stop/Add) ---
    if cmd_start == "engine":
        if not modules['engine']:
            emit('terminal_output', {'output': "❌ Error: 'engine_manager.py' missing."})
            return

        # engine add <Name> <Type> <Path>
        if parts[1] == "add":
            if len(parts) < 5:
                emit('terminal_output', {'output': "Usage: engine add <Name> <Type> <Path/Key>"})
            else:
                name = parts[2]
                etype = parts[3]
                path = " ".join(parts[4:])
                emit('terminal_output', {'output': modules['engine'].add_engine(name, etype, path)})
            return

        # engine start <Name>
        if parts[1] == "start" or parts[1] == "on":
            emit('terminal_output', {'output': modules['engine'].start_engine(parts[2])})
            return

        # engine stop <Name>
        if parts[1] == "stop" or parts[1] == "off":
            emit('terminal_output', {'output': modules['engine'].stop_engine(parts[2])})
            return

        # engine list
        if parts[1] == "list":
            emit('terminal_output', {'output': modules['engine'].list_engines()})
            return

        # engine remove <Name>
        if parts[1] == "remove":
            emit('terminal_output', {'output': modules['engine'].remove_engine(parts[2])})
            return

    # --- 2. STORAGE COMMANDS ---
    if cmd_start == "storage" and modules.get('storage'):
        if parts[1] == "add":
            emit('terminal_output', {'output': modules['storage'].add_storage(parts[2], parts[3], " ".join(parts[4:]))})
        elif parts[1] == "list":
            emit('terminal_output', {'output': modules['storage'].list_storage()})
        return

    # --- 3. META & SYSTEM COMMANDS ---
    if cmd_start == "fb" and modules.get('fb'):
        if parts[1] == "post": emit('terminal_output', {'output': modules['fb'].post_status(" ".join(parts[2:]))})
        return
        
    if cmd_start == "cloud" and modules.get('cloud'):
        if parts[1] == "public": emit('terminal_output', {'output': modules['cloud'].start_tunnel()})
        return

    # Fallback Shell
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: Unlimited Engine & Storage Box Active ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
