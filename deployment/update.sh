#!/bin/bash
set -e

# NexConnect Update Script (Two-Repo Layout)
# Run from the API repo root: ./deployment/update.sh
#
# Expected EC2 directory layout:
#   ~/nexconnect-api/   ← this repo (backend + deployment)
#   ~/nexconnect-ui/    ← frontend repo

API_DIR="/home/ubuntu/nexconnect-api"
UI_DIR="/home/ubuntu/nexconnect-ui"
WEB_ROOT="/var/www/nexconnect/dist/frontend/browser"

echo "======================================"
echo "    NexConnect Update Script          "
echo "======================================"

# 1. Pull latest code
echo "-> Pulling latest API (backend)..."
cd "$API_DIR" && git pull origin main

echo "-> Pulling latest UI (frontend)..."
cd "$UI_DIR" && git pull origin main

# 2. Update backend dependencies
echo "-> Updating backend dependencies..."
source "$API_DIR/backend/venv/bin/activate"
pip install -r "$API_DIR/backend/requirements.txt"
deactivate

# 3. Build Angular frontend
echo "-> Building Angular frontend..."
cd "$UI_DIR"
npm ci
npm run build -- --configuration production

# 4. Deploy frontend to Nginx web root
echo "-> Deploying frontend..."
sudo rm -rf "$WEB_ROOT"
sudo mkdir -p "$WEB_ROOT"
sudo cp -r "$UI_DIR/dist/frontend/browser/"* "$WEB_ROOT/"
sudo chown -R www-data:www-data /var/www/nexconnect

# 5. Restart services
echo "-> Restarting services..."
sudo systemctl restart nexconnect-backend
sudo systemctl reload nginx

echo "======================================"
echo "    Update complete!"
echo "======================================"
