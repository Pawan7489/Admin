# File: terminal_backend.py
# Description: Core Logic for Web-based Admin Terminal
# Author: AI Project Architect

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_admin_key_123'
socketio = SocketIO(app)

# Current working directory (shuruaat mein project folder)
current_dir = os.getcwd()

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(command):
    global current_dir
    
    # Command ko clean karna
    command = command.strip()
    
    if not command:
        return

    # Special Command: Directory Change (cd)
    if command.startswith('cd '):
        try:
            target_dir = command[3:].strip()
            os.chdir(target_dir)
            current_dir = os.getcwd()
            emit('terminal_output', {'output': f"Directory changed to: {current_dir}"})
        except FileNotFoundError:
            emit('terminal_output', {'output': f"Error: Directory not found: {target_dir}"})
        except Exception as e:
            emit('terminal_output', {'output': f"Error: {str(e)}"})
    
    # System Commands (Windows/Linux support)
    else:
        try:
            # Subprocess se command run karna
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                stdin=subprocess.PIPE,
                cwd=current_dir
            )
            stdout, stderr = process.communicate()
            
            # Output ko decode karke wapas bhejna
            output = stdout.decode('utf-8') + stderr.decode('utf-8')
            
            # Agar output khali hai toh message do
            if not output:
                output = "Command executed successfully (No output)."
                
            emit('terminal_output', {'output': output})
            
        except Exception as e:
            emit('terminal_output', {'output': f"Execution Error: {str(e)}"})

if __name__ == '__main__':
    print("--- Admin Terminal Starting on Localhost:5000 ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
  
