# File: git_ops.py
# Description: GitHub Operations Module for Admin Panel

import subprocess
import os

class GitManager:
    def __init__(self):
        # Check karein ki GIT installed hai ya nahi
        try:
            subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.git_available = True
        except FileNotFoundError:
            self.git_available = False

    def execute_git(self, command_parts):
        """
        Git commands ko run karta hai aur output safai se deta hai.
        """
        if not self.git_available:
            return "❌ Error: Git aapke system me install nahi hai. Kripya pehle Git install karein."

        try:
            # Command construct karein (e.g., git status)
            full_command = ["git"] + command_parts
            
            result = subprocess.run(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd() # Current Project Folder
            )
            
            if result.returncode == 0:
                return f"✅ GitHub Output:\n{result.stdout}"
            else:
                return f"⚠️ GitHub Error:\n{result.stderr}"
                
        except Exception as e:
            return f"Critical Error: {str(e)}"

    def get_status(self):
        return self.execute_git(["status"])

    def pull_updates(self):
        return self.execute_git(["pull"])
      
