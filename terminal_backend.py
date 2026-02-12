# File: terminal_backend.py
# Description: Universal Admin Panel (Telegram + All Modules)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

# --- MODULE AUTO-LOADER ---
modules = {}

# 1. Telegram (NEW)
try:
    import telegram_manager
    modules['tg'] = telegram_manager.TelegramBot()
except ImportError:
    modules['tg'] = None

# 2. Cloudflare
try:
    import cloudflare_manager
    modules['cloud'] = cloudflare_manager.CloudflareTunnel()
except ImportError:
    modules['cloud'] = None

# 3. DNS Manager
try:
    import dns_manager
    modules['dns'] = dns_manager.DNSController()
except ImportError:
    modules['dns'] = None

# 4. WordPress & Blogger
try:
    import wordpress_manager
    modules['wp'] = wordpress_manager.WordPressBot()
    import blogger_manager
    modules['blogger'] = blogger_manager.BloggerBot()
except ImportError:
    pass

# 5. Git, Health, Colab, Kaggle
try:
    import git_ops
    modules['git'] = git_ops.GitManager()
    import system_health
    modules['health'] = system_health.SystemDoctor()
    import colab_bridge
    modules['colab'] = colab_bridge.ColabConnector()
    import kaggle_manager
    modules['kaggle'] = kaggle_manager.KaggleBot()
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

    # --- 1. TELEGRAM COMMANDS (NEW) ---
    if cmd_start == "telegram" or cmd_start == "tg":
        if not modules['tg']:
            emit('terminal_output', {'output': "❌ Error: Telegram module missing."})
            return

        # Setup: telegram setup <token> <chat_id>
        if parts[1] == "setup" and len(parts) == 4:
            emit('terminal_output', {'output': modules['tg'].setup(parts[2], parts[3])})
            return

        # Message: telegram send Hello World
        if parts[1] == "send" or parts[1] == "msg":
            message = " ".join(parts[2:])
            emit('terminal_output', {'output': modules['tg'].send_message(message)})
            return

        # File: telegram file my_data.txt
        if parts[1] == "file" or parts[1] == "upload":
            emit('terminal_output', {'output': modules['tg'].send_file(parts[2])})
            return
            
        # Test
        if parts[1] == "test":
            emit('terminal_output', {'output': modules['tg'].send_message("🔔 System Online! Admin Panel is connected to Telegram.")})
            return

    # --- 2. EXISTING COMMANDS (Quick Links) ---
    
    # Cloudflare
    if cmd_start == "cloud" and modules['cloud']:
        if parts[1] == "public": emit('terminal_output', {'output': modules['cloud'].start_tunnel()})
        elif parts[1] == "stop": emit('terminal_output', {'output': modules['cloud'].stop_tunnel()})
        return

    # DNS
    if cmd_start == "dns" and modules['dns']:
        if parts[1] == "check": emit('terminal_output', {'output': modules['dns'].check_domain_availability(parts[2])})
        return

    # System Health
    if raw_command == "system status" and modules.get('health'):
        emit('terminal_output', {'output': modules['health'].diagnose()})
        return
        
    # Git
    if cmd_start == "git" and modules['git']:
        emit('terminal_output', {'output': modules['git'].execute_git(parts[1:])})
        return

    # Fallback Shell
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: Telegram Active ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
