# File: terminal_backend.py
# Description: Admin Panel Core + GitHub Module Integration

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import git_ops  # <--- NEW: Import Git Module

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)

# Initialize Git Manager
git_brain = git_ops.GitManager()

current_dir = os.getcwd()

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    
    if not raw_command:
        return

    # --- GITHUB SPECIAL COMMANDS ---
    # Agar user "git" se start hone wala command likhe
    if raw_command.lower().startswith("git "):
        parts = raw_command.split()[1:] # "git" ko hata kar baaki hissa lo
        
        # Special feedback message
        emit('terminal_output', {'output': "🔄 Connecting to GitHub..."})
        
        # Git Manager ko kaam do
        response = git_brain.execute_git(parts)
        emit('terminal_output', {'output': response})
        return
    
    # --- GitHub Shortcuts (Hinglish/Smart) ---
    if raw_command.lower() == "update system" or raw_command.lower() == "code update karo":
        emit('terminal_output', {'output': "🔄 Pulling latest code from GitHub..."})
        response = git_brain.pull_updates()
        emit('terminal_output', {'output': response})
        return

    if raw_command.lower() == "status dikhao" or raw_command.lower() == "check changes":
        response = git_brain.get_status()
        emit('terminal_output', {'output': response})
        return

    # --- NORMAL COMMANDS (Old Logic) ---
    try:
        process = subprocess.Popen(
            raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir
        )
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')
        if not output: output = "Done."
        emit('terminal_output', {'output': output})
    except Exception as e:
        emit('terminal_output', {'output': f"Error: {str(e)}"})

if __name__ == '__main__':
    print("--- Admin Panel with GitHub Integration Active ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
