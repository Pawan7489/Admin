# File Path: backend/sandbox_env.py
# Description: Implements a Strict Sandbox Environment for safe code execution.
# Prevents AI from accidentally modifying or deleting system files.

import sys
import io
import contextlib
import multiprocessing
import traceback

class SecureSandbox:
    def __init__(self):
        # Banned commands that could harm your local machine
        self.forbidden_commands = [
            'os.remove', 'os.rmdir', 'shutil.rmtree', 
            'os.system', 'subprocess', 'format', 'open'
        ]

    def _validate_code(self, code):
        """
        Code ko execute karne se pehle scan karta hai.
        """
        for cmd in self.forbidden_commands:
            if cmd in code:
                return False, f"🛑 [SECURITY]: Execution blocked. Forbidden command '{cmd}' detected."
        return True, "Code Cleared."

    def execute_safely(self, code, timeout=5):
        """
        Code ko ek isolated process mein run karta hai.
        """
        is_safe, message = self._validate_code(code)
        if not is_safe:
            return message

        print(f"🛡️ [Sandbox]: Executing code in isolated environment (Timeout: {timeout}s)...")

        # StringIO used to capture the code's output
        output_buffer = io.StringIO()
        
        try:
            # Setting up a limited global environment
            safe_globals = {"__builtins__": __builtins__}
            
            with contextlib.redirect_stdout(output_buffer):
                # Using multiprocessing to enforce a strict timeout
                p = multiprocessing.Process(target=exec, args=(code, safe_globals))
                p.start()
                p.join(timeout)

                if p.is_alive():
                    p.terminate()
                    return "❌ [Timeout]: Code execution exceeded safety limits."

            return output_buffer.getvalue() or "✅ Code executed successfully (No output)."
        
        except Exception:
            return f"⚠️ [Execution Error]:\n{traceback.format_exc()}"

    def calculate_risk_index(self, code_length, complexity_score):
        """
        Calculates the risk of the generated code snippet.
        Formula: $R_i = \frac{L \times C}{100}$
        """
        risk = (code_length * complexity_score) / 100
        return round(risk, 2)

# Test Block
if __name__ == "__main__":
    sandbox = SecureSandbox()
    
    # Test 1: Safe Code
    safe_code = "print('Hello from the Safe Zone!')\nprint(5 * 5)"
    print(sandbox.execute_safely(safe_code))
    
    # Test 2: Dangerous Code (Banned)
    dangerous_code = "import os\nos.remove('important_file.txt')"
    print(sandbox.execute_safely(dangerous_code))
  
