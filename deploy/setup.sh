#!/usr/bin/env bash
# deploy/setup.sh
# ONE-TIME app setup script. Run as user 'dev' on the VPS.
# Use deploy/bootstrap_fresh_ubuntu.sh first on a brand-new Ubuntu server.
set -euo pipefail

APP_DIR="/home/dev/dvmerpfull"
BACKEND="$APP_DIR/backend"
REPO_URL="https://github.com/netvision/dvmerpfull.git"
DB_NAME="dvmdb"
DB_USER="dvmuser"
DB_PASSWORD="${DB_PASSWORD:-}"
FRONTEND_ORIGIN="${FRONTEND_ORIGIN:-https://YOUR_NETLIFY_URL.netlify.app}"

if [ -z "$DB_PASSWORD" ]; then
	echo "ERROR: DB_PASSWORD is required."
	echo "Example: DB_PASSWORD='strongpass' FRONTEND_ORIGIN='https://your-site.netlify.app' bash deploy/setup.sh"
	exit 1
fi

echo "==> Cloning or updating repository..."
if [ -d "$APP_DIR/.git" ]; then
	cd "$APP_DIR"
	git fetch origin
	git checkout main
	git pull origin main
else
	git clone "$REPO_URL" "$APP_DIR"
fi

echo "==> Creating Python virtual environment..."
python3 -m venv "$BACKEND/venv"
"$BACKEND/venv/bin/pip" install --upgrade pip
"$BACKEND/venv/bin/pip" install -r "$BACKEND/requirements.txt"

echo "==> Creating uploads directory..."
mkdir -p "$BACKEND/uploads"

echo ""
echo "==> Setting up PostgreSQL database..."
sudo -u postgres psql -v ON_ERROR_STOP=1 <<SQL
DO
\$\$
BEGIN
	IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
		CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASSWORD';
	ELSE
		ALTER ROLE $DB_USER WITH PASSWORD '$DB_PASSWORD';
	END IF;
END
\$\$;
SQL

if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
	 sudo -u postgres createdb -O "$DB_USER" "$DB_NAME"
fi

echo "==> Creating .env file..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
cat > "$BACKEND/.env" <<EOF
SECRET_KEY=$SECRET_KEY
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME
ALLOWED_ORIGINS=$FRONTEND_ORIGIN,https://dvmchirawa.ac.in
EOF
chmod 600 "$BACKEND/.env"
echo "    .env created at $BACKEND/.env"

echo "==> Running Alembic migrations..."
cd "$BACKEND"
if ! "$BACKEND/venv/bin/alembic" upgrade head; then
	echo "==> Alembic upgrade failed. Checking for empty database bootstrap case..."
	if "$BACKEND/venv/bin/python" - <<'PY'
from sqlalchemy import inspect
from database import engine, Base
import models  # noqa: F401

tables = inspect(engine).get_table_names()
if tables:
	raise SystemExit(1)

Base.metadata.create_all(bind=engine)
print("Created base schema from SQLAlchemy models on empty database.")
PY
	then
		"$BACKEND/venv/bin/alembic" stamp head
		echo "==> Alembic stamped to head after base schema bootstrap."
	else
		echo "ERROR: Migration failed and database is not empty. Manual intervention required."
		exit 1
	fi
fi

echo "==> Running database seed (creates admin user)..."
"$BACKEND/venv/bin/python" seed.py

echo "==> Installing systemd service..."
sudo cp "$APP_DIR/deploy/dvmapi.service" /etc/systemd/system/dvmapi.service
sudo systemctl daemon-reload
sudo systemctl enable dvmapi
sudo systemctl start dvmapi

echo "==> Installing Nginx config..."
sudo cp "$APP_DIR/deploy/fastapi.dvmchirawa.ac.in.conf" /etc/nginx/sites-available/fastapi.dvmchirawa.ac.in
sudo ln -sf /etc/nginx/sites-available/fastapi.dvmchirawa.ac.in /etc/nginx/sites-enabled/fastapi.dvmchirawa.ac.in
sudo nginx -t
sudo systemctl reload nginx

echo ""
echo "==> Setup complete! Next steps:"
echo "    1. Run: sudo certbot --nginx -d fastapi.dvmchirawa.ac.in"
echo "    2. Check API: https://fastapi.dvmchirawa.ac.in/"
echo "    3. Deploy frontend to Netlify and set VITE_API_BASE_URL=https://fastapi.dvmchirawa.ac.in"
