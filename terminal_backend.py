# File: terminal_backend.py
# Description: Admin Terminal with Basic Hinglish Intelligence (Rule-Based v1)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)

# Current working directory tracker
current_dir = os.getcwd()
os_type = platform.system()  # Windows ya Linux detect karega

def translate_hinglish(command):
    """
    Basic Rule-Based Translator.
    Future me yahan bada LLM model connect hoga.
    Abhi ke liye hum common patterns pakdenge.
    """
    cmd_lower = command.lower()
    
    # Logic 1: Folder Banane ka command
    # User: "Ek naya folder banao Images naam ka"
    if "folder" in cmd_lower and ("banao" in cmd_lower or "create" in cmd_lower):
        parts = command.split()
        # Simple logic: Last word ko folder name maan lete hain
        folder_name = parts[-1] 
        return f"mkdir {folder_name}"

    # Logic 2: Files dekhne ka command
    # User: "Yahan kya hai" ya "List dikhao"
    if "kya hai" in cmd_lower or "list dikhao" in cmd_lower or "files dikhao" in cmd_lower:
        if os_type == "Windows":
            return "dir"
        else:
            return "ls -la"

    # Logic 3: Delete karne ka command
    # User: "Images folder uda do" or "delete folder Images"
    if "delete" in cmd_lower or "uda do" in cmd_lower:
        target = parts[-1]
        if os_type == "Windows":
            return f"rmdir /s /q {target}" # Dangerous command, use carefully
        else:
            return f"rm -rf {target}"

    # Agar koi Hinglish pattern match nahi hua, toh original command wapas karo
    return command

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    
    raw_command = raw_command.strip()
    if not raw_command:
        return

    # STEP 1: AI Translation Layer
    # Pehle hum Hinglish check karenge
    final_command = translate_hinglish(raw_command)

    # User ko dikhao ki AI ne kya samjha (Feedback Loop)
    if final_command != raw_command:
        emit('terminal_output', {'output': f"🤖 AI Logic: Translating '{raw_command}' -> '{final_command}'..."})

    # STEP 2: Execution Layer
    # Directory Change (Special Case)
    if final_command.startswith('cd '):
        try:
            target_dir = final_command[3:].strip()
            os.chdir(target_dir)
            current_dir = os.getcwd()
            emit('terminal_output', {'output': f"Directory changed to: {current_dir}"})
        except Exception as e:
            emit('terminal_output', {'output': f"Error: {str(e)}"})
            
    # System Command Execution
    else:
        try:
            process = subprocess.Popen(
                final_command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                stdin=subprocess.PIPE,
                cwd=current_dir
            )
            stdout, stderr = process.communicate()
            output = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')
            
            if not output:
                output = "Done."
                
            emit('terminal_output', {'output': output})
            
        except Exception as e:
            emit('terminal_output', {'output': f"Execution Error: {str(e)}"})

if __name__ == '__main__':
    print(f"--- AI Admin Terminal Active on {os_type} ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
