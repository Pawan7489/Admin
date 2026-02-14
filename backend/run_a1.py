# File Path: run_a1.py
# Description: The 'One-Click' entry point to launch the entire A1 OS.
# Rule: Runs a 5-second Self-Diagnosis before accepting commands. [cite: 2026-02-11]

import os
import sys
import subprocess
import time
from backend.master_bridge import a1_bridge

def launch_sequence():
    print("🚀 [Ignition]: Starting A1 Super Genius OS...")
    
    # Step 1: 5-Second Self-Diagnosis [cite: 2026-02-11]
    print("🛡️ [Diagnosis]: Checking Internet, GPU, Memory, and Drives...")
    time.sleep(5) 
    
    if not a1_bridge.boot_sequence():
        print("🛑 [Fatal]: Self-Diagnosis failed. System frozen for safety.")
        sys.exit(1)

    # Step 2: Launching the Web UI (Streamlit) on localhost:7860 [cite: 2026-02-11]
    print("🌐 [UI]: Launching Dashboard at http://localhost:7860")
    
    try:
        # Command to run Streamlit in the background
        # Note: 'frontend/dashboard.py' is the main UI file
        subprocess.Popen(["streamlit", "run", "frontend/dashboard.py", "--server.port", "7860"])
        
        print("\n✅ [A1 OS]: System is now LIVE. Welcome, Admin.")
        print("💡 [Hint]: Use Hinglish commands like 'Ek naya folder banao'.")
        
    except Exception as e:
        print(f"❌ [Error]: Failed to launch UI: {str(e)}")

def calculate_startup_probability(diag_score):
    """
    Calculates Success Probability ($P_s$).
    Formula: $P_s = \prod_{i=1}^{n} S_i$
    Where $S_i$ is the success factor of each hardware component.
    """
    return f"Startup Success Probability: {diag_score * 100}%"

if __name__ == "__main__":
    launch_sequence()
  
