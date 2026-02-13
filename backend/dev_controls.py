# File Path: backend/dev_controls.py
# Description: Advanced Dev Controls (Script Execution Sandbox & Visual Logic Builder)

import os
import json
import sys
import subprocess
import io
from contextlib import redirect_stdout
from datetime import datetime

class DevEnvironment:
    def __init__(self):
        self.logic_db_file = "database/visual_logic_nodes.json"
        self.script_logs = "database/script_execution_logs.json"
        self._ensure_directories()
        self.load_logic_nodes()

    def _ensure_directories(self):
        """Database folder check/create karta hai"""
        if not os.path.exists('database'):
            os.makedirs('database')
            
        # Creating empty JSON files if they don't exist
        for db_file in [self.logic_db_file, self.script_logs]:
            if not os.path.exists(db_file):
                with open(db_file, 'w') as f:
                    json.dump({}, f)

    def load_logic_nodes(self):
        with open(self.logic_db_file, 'r') as f:
            try:
                self.nodes = json.load(f)
            except:
                self.nodes = {}

    def save_logic_nodes(self):
        with open(self.logic_db_file, 'w') as f:
            json.dump(self.nodes, f, indent=4)

    # --- SCRIPT EXECUTION ENGINE (SANDBOX MODE) ---
    def execute_python(self, code_snippet):
        """
        Runs Python code directly from the UI.
        Uses Context Manager to catch standard output (print statements).
        """
        print("⚙️ [Sandbox]: Initializing Python Execution Environment...")
        
        # Catching the output
        output_buffer = io.StringIO()
        try:
            # Running the code safely and redirecting output to our buffer
            with redirect_stdout(output_buffer):
                # exec() runs dynamic python code. 
                # In a production server, this should be heavily sandboxed!
                exec(code_snippet, {"__builtins__": __builtins__}, {})
            
            result = output_buffer.getvalue()
            if not result.strip():
                result = "[Executed successfully with no print output]"
                
            self._log_execution("Python", code_snippet, "Success")
            return f"✅ Python Sandbox Result:\n{result}"
            
        except Exception as e:
            error_msg = str(e)
            self._log_execution("Python", code_snippet, f"Failed: {error_msg}")
            return f"❌ Python Execution Error:\n{error_msg}"

    def execute_js(self, code_snippet):
        """
        Runs Node.js code via Subprocess (Requires Node.js installed on host).
        """
        print("⚙️ [Sandbox]: Initializing JavaScript Execution Environment...")
        temp_file = "database/temp_script.js"
        
        try:
            # Write JS code to a temporary file
            with open(temp_file, "w") as f:
                f.write(code_snippet)
                
            # Execute via Node.js (Standard way to run JS in backend)
            # Assuming 'node' is in the system PATH
            process = subprocess.Popen(["node", temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            
            # Clean up temp file
            os.remove(temp_file)
            
            if process.returncode == 0:
                self._log_execution("JavaScript", code_snippet, "Success")
                return f"✅ JS Sandbox Result:\n{out.decode()}"
            else:
                self._log_execution("JavaScript", code_snippet, "Failed")
                return f"❌ JS Execution Error:\n{err.decode()}"
                
        except FileNotFoundError:
            return "⚠️ Notice: Node.js is not installed on this server. Cannot execute backend JS."
        except Exception as e:
            return f"❌ System Error: {str(e)}"

    def _log_execution(self, lang, code, status):
        """Maintains a history of all executed scripts"""
        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        log_entry = {
            "language": lang,
            "code": code[:100] + "..." if len(code) > 100 else code, # Save snippet
            "status": status
        }
        
        try:
            with open(self.script_logs, 'r') as f:
                logs = json.load(f)
        except:
            logs = {}
            
        logs[timestamp] = log_entry
        
        with open(self.script_logs, 'w') as f:
            json.dump(logs, f, indent=4)

    # --- VISUAL LOGIC BUILDER CORE ---
    def connect_nodes(self, source_node, target_node, action_type="trigger"):
        """
        Backend logic for the Drag-and-Drop builder.
        Example: connect_nodes("GitHub_Push", "Render_Deploy", "trigger")
        """
        connection_id = f"{source_node}_to_{target_node}"
        
        if connection_id in self.nodes:
            return f"⚠️ Logic Link '{connection_id}' already exists."

        self.nodes[connection_id] = {
            "source": source_node,
            "target": target_node,
            "action": action_type,
            "created_on": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "active": True
        }
        self.save_logic_nodes()
        
        return f"🔗 LOGIC LINKED: [{source_node}] will now {action_type} [{target_node}]."

    def list_active_logic(self):
        if not self.nodes:
            return "📭 Visual Logic Canvas is empty. Draw some connections!"
            
        output = "\n🕸️ --- A1 ACTIVE LOGIC MESH --- 🕸️\n"
        output += f"{'SOURCE':<20} | {'ACTION':<10} | {'TARGET':<20}\n"
        output += "-" * 55 + "\n"
        
        for conn_id, data in self.nodes.items():
            if data['active']:
                output += f"{data['source']:<20} | {data['action']:<10} | {data['target']:<20}\n"
                
        output += "-" * 55 + "\n"
        return output

# Testing Block (Will be ignored by server.py auto-loader)
if __name__ == "__main__":
    dev = DevEnvironment()
    print(dev.execute_python("print('Hello from A1 Sandbox!')"))
    print(dev.connect_nodes("WhatsApp_API", "Database_Save", "trigger"))
  
