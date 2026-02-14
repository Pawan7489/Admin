# File: setup_master_brain.sh
# Purpose: Transform Oracle ARM Instance into A1 OS Master Brain.
# Strategy: Docker-based isolation for "Solo Mode" safety. [cite: 2026-02-11]

echo "🚀 [A1 OS]: Initializing Master Brain Deployment..."

# 1. Update System
sudo apt update && sudo apt upgrade -y

# 2. Install Docker & Docker Compose (The Nervous System)
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker

# 3. Setup Master Registry & Config Slots [cite: 2026-02-11]
mkdir -p ~/a1-os/{config,data,logs,engines}
touch ~/a1-os/config/settings.json
touch ~/a1-os/config/constitution.json

# 4. Open Essential Ports (Oracle Security Lists mein bhi open karein)
# 80/443: Web | 7860: Gradio UI | 1337: Strapi | 5678: n8n
sudo ufw allow 80,443,7860,1337,5678/tcp

echo "✅ [Oracle]: Master Brain is now Docker-ready."
