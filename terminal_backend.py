# File: terminal_backend.py
# Description: Universal Admin Panel (All Modules + Kaggle Integrated)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

# --- MODULE AUTO-LOADER (Plug & Play) ---

# 1. Kaggle Module (NEW)
try:
    import kaggle_manager
    kaggle_available = True
    kaggle_bot = kaggle_manager.KaggleBot()
except ImportError:
    kaggle_available = False
    print("⚠️ Warning: 'kaggle_manager.py' missing or 'kaggle' library not installed.")

# 2. Git Module
try:
    import git_ops
    git_available = True
    git_brain = git_ops.GitManager()
except ImportError:
    git_available = False

# 3. Hugging Face Module
try:
    import huggingface_manager
    hf_available = True
    hf_brain = huggingface_manager.ModelManager()
except ImportError:
    hf_available = False

# 4. System Health
try:
    import system_health
    health_available = True
    sys_doc = system_health.SystemDoctor()
except ImportError:
    health_available = False

# 5. Google Colab Bridge
try:
    import colab_bridge
    colab_available = True
    colab_link = colab_bridge.ColabConnector()
except ImportError:
    colab_available = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)

current_dir = os.getcwd()
os_type = platform.system()

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    if not raw_command: return

    # --- 1. KAGGLE COMMANDS (NEW) ---
    if raw_command.startswith("kaggle "):
        if not kaggle_available:
            emit('terminal_output', {'output': "❌ Error: Kaggle module missing. Install library: 'pip install kaggle'"})
            return

        parts = raw_command.split()
        
        # Command: kaggle setup <username> <key>
        if parts[1] == "setup" and len(parts) == 4:
            username = parts[2]
            key = parts[3]
            emit('terminal_output', {'output': kaggle_bot.setup_auth(username, key)})
            return
            
        # Command: kaggle search <query>
        if parts[1] == "search" and len(parts) > 2:
            query = parts[2]
            emit('terminal_output', {'output': kaggle_bot.search_data(query)})
            return

        # Command: kaggle download <dataset>
        if parts[1] == "download" and len(parts) > 2:
            dataset = parts[2]
            emit('terminal_output', {'output': "⏳ Downloading dataset... Please wait."})
            emit('terminal_output', {'output': kaggle_bot.download_dataset(dataset)})
            return

    # --- 2. COLAB COMMANDS ---
    if raw_command.lower() in ["connect colab", "colab setup"]:
        if colab_available:
            emit('terminal_output', {'output': "👇 Code for Colab:"})
            emit('terminal_output', {'output': colab_link.get_setup_script()})
        return

    # --- 3. HEALTH & GIT & HF (Existing) ---
    if raw_command.lower() in ["health check", "system status"]:
        if health_available: emit('terminal_output', {'output': sys_doc.diagnose()})
        return

    if raw_command.startswith("hf ") and hf_available:
        parts = raw_command.split()
        if parts[1] == "login": emit('terminal_output', {'output': hf_brain.login_hf(parts[2])})
        elif parts[1] == "download": emit('terminal_output', {'output': hf_brain.download_model(parts[2])})
        return

    if raw_command.startswith("git ") and git_available:
        emit('terminal_output', {'output': git_brain.execute_git(raw_command.split()[1:])})
        return

    # --- 4. FALLBACK SHELL ---
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode('utf-8', errors='ignore') + err.decode('utf-8', errors='ignore')})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: Kaggle Integrated ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
            
