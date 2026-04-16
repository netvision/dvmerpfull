#!/usr/bin/env bash
# deploy/deploy.sh
# Run this on the VPS as user 'dev' to deploy updates.
# First-time setup: run deploy/setup.sh
set -euo pipefail

APP_DIR="/home/dev/dvmerpfull"
BACKEND="$APP_DIR/backend"

echo "==> Pulling latest code..."
cd "$APP_DIR"
git pull origin main

echo "==> Installing/updating Python dependencies..."
"$BACKEND/venv/bin/pip" install -q -r "$BACKEND/requirements.txt"

echo "==> Running Alembic migrations..."
cd "$BACKEND"
"$BACKEND/venv/bin/alembic" upgrade head

echo "==> Restarting API service..."
sudo systemctl restart dvmapi

echo "==> Done. API is live at https://fastapi.dvmchirawa.ac.in"
