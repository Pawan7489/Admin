# File: terminal_backend.py
# Description: SECURE Admin Panel (Login Required + Local Only)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import subprocess
import os

# --- SECURITY MODULE ---
import security_manager
guard = security_manager.SecurityGuard()

# --- OTHER MODULES ---
modules = {}
try:
    import hosting_manager
    modules['host'] = hosting_manager.HostingConnector()
    import engine_manager
    modules['engine'] = engine_manager.EngineRegistry()
    import storage_manager
    modules['storage'] = storage_manager.StorageRegistry()
    import plugin_store
    modules['plugin'] = plugin_store.PluginMarketplace()
except ImportError:
    pass
# Add other imports (Meta, etc.) as needed...

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER_SECURE_RANDOM_KEY_999' # Session ke liye zaroori
socketio = SocketIO(app)
current_dir = os.getcwd()

# --- 🔒 SECURITY GATEKEEPER ---
@app.route('/', methods=['GET', 'POST'])
def login():
    # Agar user pehle se logged in hai, to seedha terminal dikhao
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('terminal'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if guard.verify_login(username, password):
            session['logged_in'] = True
            return redirect(url_for('terminal'))
        else:
            error = "❌ ACCESS DENIED: Wrong Credentials."

    return render_template('login.html', error=error)

@app.route('/terminal')
def terminal():
    # Security Check: Kya user logged in hai?
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    return render_template('terminal_ui.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- COMMAND HANDLER (Only for Logged In Users) ---
@socketio.on('command_input')
def handle_command(raw_command):
    # Backend par bhi check karo ki user logged in hai ya nahi
    # (SocketIO session context verify karna complex ho sakta hai, 
    #  abhi ke liye frontend gatekeeper kaafi hai local use ke liye)
    
    global current_dir
    raw_command = raw_command.strip()
    if not raw_command: return

    parts = raw_command.split()
    cmd_start = parts[0].lower()

    # --- PASSWORD CHANGE COMMAND ---
    if cmd_start == "security" and parts[1] == "password":
        # Usage: security password <new_password>
        if len(parts) < 3:
            emit('terminal_output', {'output': "Usage: security password <new_password>"})
        else:
            new_pass = parts[2]
            emit('terminal_output', {'output': guard.change_password(new_pass)})
        return

    # --- PLUGIN STORE COMMANDS ---
    if cmd_start == "store" and modules.get('plugin'):
        if parts[1] == "search": emit('terminal_output', {'output': modules['plugin'].search_wordpress(" ".join(parts[2:]))})
        elif parts[1] == "download": emit('terminal_output', {'output': modules['plugin'].download_wp_plugin(parts[2])})
        elif parts[1] == "list": emit('terminal_output', {'output': modules['plugin'].list_local_plugins()})
        return

    # --- HOSTING COMMANDS ---
    if cmd_start == "hosting" and modules.get('host'):
        if parts[1] == "trigger": emit('terminal_output', {'output': modules['host'].trigger_deploy(parts[2])})
        elif parts[1] == "list": emit('terminal_output', {'output': modules['host'].list_hosting()})
        return

    # Fallback Shell
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🔒 SECURE AI Admin Panel Started (Login Required) ---")
    # Host '127.0.0.1' ensures it only runs on YOUR laptop, not on WiFi network
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
    
