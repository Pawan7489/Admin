# File: terminal_backend.py
# Description: Universal Admin Panel (All Modules + Cloudflare Tunnel)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

# --- MODULE AUTO-LOADER ---
modules = {}

# 1. Cloudflare (NEW)
try:
    import cloudflare_manager
    modules['cloud'] = cloudflare_manager.CloudflareTunnel()
except ImportError:
    modules['cloud'] = None

# 2. WordPress
try:
    import wordpress_manager
    modules['wp'] = wordpress_manager.WordPressBot()
except ImportError:
    modules['wp'] = None

# 3. Blogger
try:
    import blogger_manager
    modules['blogger'] = blogger_manager.BloggerBot()
except ImportError:
    modules['blogger'] = None

# 4. Git
try:
    import git_ops
    modules['git'] = git_ops.GitManager()
except ImportError:
    modules['git'] = None

# 5. Hugging Face
try:
    import huggingface_manager
    modules['hf'] = huggingface_manager.ModelManager()
except ImportError:
    modules['hf'] = None

# 6. System Health
try:
    import system_health
    modules['health'] = system_health.SystemDoctor()
except ImportError:
    modules['health'] = None

# 7. Colab Bridge
try:
    import colab_bridge
    modules['colab'] = colab_bridge.ColabConnector()
except ImportError:
    modules['colab'] = None
    
# 8. Kaggle
try:
    import kaggle_manager
    modules['kaggle'] = kaggle_manager.KaggleBot()
except ImportError:
    modules['kaggle'] = None


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

    # --- 1. CLOUDFLARE COMMANDS (NEW) ---
    if cmd_start == "cloud":
        if not modules['cloud']:
            emit('terminal_output', {'output': "❌ Error: Cloudflare module missing."})
            return
        
        # Command: cloud public (Make site online)
        if parts[1] == "public" or parts[1] == "start":
            emit('terminal_output', {'output': "🚀 Initializing Cloudflare Tunnel... Wait logic..."})
            emit('terminal_output', {'output': modules['cloud'].start_tunnel()})
            return

        # Command: cloud stop (Make site offline)
        if parts[1] == "stop":
            emit('terminal_output', {'output': modules['cloud'].stop_tunnel()})
            return
            
    # --- 2. EXISTING COMMANDS (Quick Logic) ---
    
    # CMS (WP/Blogger)
    if cmd_start == "wp" and modules['wp']:
        if parts[1] == "post": emit('terminal_output', {'output': modules['wp'].create_post(parts[2], " ".join(parts[3:]))})
        return
    if cmd_start == "blogger" and modules['blogger']:
        if parts[1] == "post": emit('terminal_output', {'output': modules['blogger'].create_post(parts[2], " ".join(parts[3:]))})
        return

    # Tools (Health, Git, Colab)
    if raw_command.lower() == "system status" and modules['health']:
        emit('terminal_output', {'output': modules['health'].diagnose()})
        return
    if raw_command.lower() == "connect colab" and modules['colab']:
        emit('terminal_output', {'output': modules['colab'].get_setup_script()})
        return
    if cmd_start == "git" and modules['git']:
        emit('terminal_output', {'output': modules['git'].execute_git(parts[1:])})
        return

    # Fallback System Command
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: Cloudflare Integrated ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
