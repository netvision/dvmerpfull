#!/usr/bin/env bash
# deploy/bootstrap_fresh_ubuntu.sh
# Run on a fresh Ubuntu Linode as a sudo-capable user (for you: dev).
# Installs all server prerequisites, hardens basic access, then runs app setup.
set -euo pipefail

APP_DIR="/home/dev/dvmerpfull"

echo "==> Updating system packages..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y upgrade

echo "==> Installing required packages..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git \
  curl \
  unzip \
  nginx \
  postgresql \
  postgresql-contrib \
  python3 \
  python3-venv \
  python3-pip \
  python3-certbot-nginx \
  ufw \
  fail2ban

echo "==> Enabling and starting core services..."
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

echo "==> Configuring firewall (UFW)..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

echo ""
echo "==> Prerequisites complete. Running app setup next..."
echo "    Provide DB_PASSWORD and FRONTEND_ORIGIN as environment variables."

test -d "$APP_DIR" || mkdir -p "$APP_DIR"
cd "$APP_DIR"

if [ ! -f "$APP_DIR/deploy/setup.sh" ]; then
  git clone https://github.com/netvision/dvmerpfull.git "$APP_DIR"
fi

DB_PASSWORD="${DB_PASSWORD:-}" FRONTEND_ORIGIN="${FRONTEND_ORIGIN:-https://YOUR_NETLIFY_URL.netlify.app}" bash "$APP_DIR/deploy/setup.sh"

echo ""
echo "==> Bootstrap complete. Next step:"
echo "    sudo certbot --nginx -d api.dvmchirawa.ac.in"
