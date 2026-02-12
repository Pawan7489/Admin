# File: terminal_backend.py
# Description: Universal Admin Panel (Auto-detects Modules)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import importlib

# --- MODULES IMPORT ---
# Yahan hum check karenge ki kaunsi files maujood hain
try:
    import git_ops
    git_available = True
except ImportError:
    git_available = False

try:
    import huggingface_manager
    hf_available = True
    hf_brain = huggingface_manager.ModelManager()
except ImportError:
    hf_available = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(raw_command):
    raw_command = raw_command.strip()
    if not raw_command: return

    # --- ROUTER LOGIC (Traffic Police) ---
    
    # 1. Hugging Face Commands
    if raw_command.startswith("hf login "):
        token = raw_command.split()[2]
        if hf_available:
            emit('terminal_output', {'output': hf_brain.login_hf(token)})
        else:
            emit('terminal_output', {'output': "❌ Hugging Face module missing."})
        return

    if raw_command.startswith("hf download "):
        model_name = raw_command.split()[2]
        if hf_available:
            emit('terminal_output', {'output': hf_brain.download_model(model_name)})
        else:
            emit('terminal_output', {'output': "❌ Hugging Face module missing."})
        return

    # 2. Git Commands
    if raw_command.startswith("git ") and git_available:
        git_brain = git_ops.GitManager()
        emit('terminal_output', {'output': git_brain.execute_git(raw_command.split()[1:])})
        return

    # 3. System Commands (Fallback)
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
