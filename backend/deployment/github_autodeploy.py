# File: backend/deployment/github_autodeploy.py
# Purpose: Pushes Core Python Code & Logic to GitHub.
# Trigger: Automatically triggers CD pipelines on Render/HF Spaces/Heroku.

import os
from git import Repo, Actor

class GitHubAutoDeployer:
    def __init__(self, local_repo_path, remote_repo_url, github_token):
        """
        local_repo_path: Aapke project ka local folder.
        remote_repo_url: GitHub repo link (e.g., https://github.com/User/A1-OS.git).
        github_token: Personal Access Token (Settings -> Developer Settings -> Tokens).
        """
        self.repo_path = local_repo_path
        self.token = github_token
        # Token ko URL mein embed karna secure auth ke liye
        self.auth_url = remote_repo_url.replace("https://", f"https://{self.token}@")
        
        self.repo = self._init_or_load_repo()

    def _init_or_load_repo(self):
        """Repo load karta hai ya naya initialize karta hai."""
        if os.path.exists(os.path.join(self.repo_path, ".git")):
            print("📂 [Git]: Existing repository loaded.")
            return Repo(self.repo_path)
        else:
            print("✨ [Git]: Initializing new repository...")
            repo = Repo.init(self.repo_path)
            # Default branch 'main' set karna
            if 'main' not in repo.heads:
                repo.git.checkout(b='main')
            return repo

    def push_code_update(self, commit_message="Auto-update from A1 OS"):
        """
        Core function jo code ko Stage -> Commit -> Push karta hai.
        Yahi 'Auto-Deploy' ka trigger hai.
        """
        try:
            # 1. Add all files (Stage)
            print("➕ [Git]: Staging all new logic and files...")
            self.repo.git.add(A=True) # 'git add .' equivalent

            # Check if there are changes to commit
            if not self.repo.is_dirty(untracked_files=True):
                print("⚠️ [Git]: No changes detected. Nothing to deploy.")
                return "No Changes"

            # 2. Commit
            print(f"📝 [Git]: Committing changes: '{commit_message}'...")
            author = Actor("A1 Admin", "admin@a1-os.com")
            self.repo.index.commit(commit_message, author=author, committer=author)

            # 3. Set Remote (if not exists)
            if 'origin' not in self.repo.remotes:
                self.repo.create_remote('origin', self.auth_url)
            else:
                # Update URL just in case token changed
                self.repo.remotes.origin.set_url(self.auth_url)

            # 4. Push to GitHub
            print("🚀 [Git]: Pushing code to GitHub Main Branch...")
            origin = self.repo.remotes.origin
            origin.push(refspec='main:main')
            
            print("✅ [Success]: Code Pushed! Auto-Deploy sequence started on Render/HF.")
            return "Deployed"

        except Exception as e:
            print(f"❌ [Error]: Git Operation Failed. {str(e)}")
            return "Failed"

# --- Master Execution Block ---
if __name__ == "__main__":
    # Project Folder Path
    PROJECT_DIR = "./" 
    
    # Aapka GitHub Repo URL aur Token
    MY_REPO_URL = "https://github.com/username/A1-OS-Core.git"
    MY_GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx" # GitHub se generate karein
    
    deployer = GitHubAutoDeployer(PROJECT_DIR, MY_REPO_URL, MY_GITHUB_TOKEN)
    
    # Jab bhi aap naya logic likhein, bas ye function call karein
    deployer.push_code_update(commit_message="Added new Swarm Logic Module 87-X")
  
