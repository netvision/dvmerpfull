#!/usr/bin/env bash
# deploy/setup.sh
# ONE-TIME server setup script. Run as user 'dev' on the VPS.
# Prerequisites: git, python3, pip, nginx, postgresql already installed.
set -euo pipefail

APP_DIR="/home/dev/dvmerpfull"
BACKEND="$APP_DIR/backend"
DB_NAME="dvmdb"
DB_USER="dvmuser"

echo "==> Cloning repository..."
git clone https://github.com/YOUR_GITHUB_USERNAME/dvmerpfull.git "$APP_DIR"

echo "==> Creating Python virtual environment..."
python3 -m venv "$BACKEND/venv"
"$BACKEND/venv/bin/pip" install --upgrade pip
"$BACKEND/venv/bin/pip" install -r "$BACKEND/requirements.txt"

echo "==> Creating uploads directory..."
mkdir -p "$BACKEND/uploads"

echo ""
echo "==> Setting up PostgreSQL database..."
echo "    Run the following as postgres user (sudo -u postgres psql):"
echo ""
echo "    CREATE USER $DB_USER WITH PASSWORD 'CHOOSE_A_STRONG_PASSWORD';"
echo "    CREATE DATABASE $DB_NAME OWNER $DB_USER;"
echo "    \\q"
echo ""

echo "==> Creating .env file..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
cat > "$BACKEND/.env" <<EOF
SECRET_KEY=$SECRET_KEY
DATABASE_URL=postgresql://$DB_USER:REPLACE_WITH_PASSWORD@localhost/$DB_NAME
ALLOWED_ORIGINS=https://YOUR_NETLIFY_URL.netlify.app,https://dvmchirawa.ac.in
EOF
echo "    .env created at $BACKEND/.env — edit it to fill in DB password and ALLOWED_ORIGINS."

echo "==> Running Alembic migrations..."
cd "$BACKEND"
"$BACKEND/venv/bin/alembic" upgrade head

echo "==> Running database seed (creates admin user)..."
"$BACKEND/venv/bin/python" seed.py

echo "==> Installing systemd service..."
sudo cp "$APP_DIR/deploy/dvmapi.service" /etc/systemd/system/dvmapi.service
sudo systemctl daemon-reload
sudo systemctl enable dvmapi
sudo systemctl start dvmapi

echo "==> Installing Nginx config..."
sudo cp "$APP_DIR/deploy/api.dvmchirawa.ac.in.conf" /etc/nginx/sites-available/api.dvmchirawa.ac.in
sudo ln -sf /etc/nginx/sites-available/api.dvmchirawa.ac.in /etc/nginx/sites-enabled/api.dvmchirawa.ac.in
sudo nginx -t
sudo systemctl reload nginx

echo ""
echo "==> Setup complete! Next steps:"
echo "    1. Edit $BACKEND/.env with the correct DB password and ALLOWED_ORIGINS"
echo "    2. Run: sudo certbot --nginx -d api.dvmchirawa.ac.in"
echo "    3. Deploy frontend to Netlify (see deploy/NETLIFY.md)"
