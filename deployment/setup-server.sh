#!/bin/bash
set -e

# NexConnect Server Setup Script
# Run ONCE on a fresh EC2 Ubuntu 22.04 / 24.04 instance.
# Usage: chmod +x deployment/setup-server.sh && ./deployment/setup-server.sh

echo "======================================"
echo "    NexConnect Server Setup Script    "
echo "======================================"

# 1. System dependencies
echo "-> Installing system dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y nginx postgresql postgresql-contrib git curl

# 2. Node.js v20
echo "-> Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 3. Certbot (for HTTPS / Let's Encrypt)
echo "-> Installing Certbot..."
sudo apt install -y certbot python3-certbot-nginx

# 4. PostgreSQL Database Setup
echo "-> Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE nexconnect_db;" || echo "Database already exists."
sudo -u postgres psql -c "CREATE USER nexconnect_admin WITH PASSWORD 'YourSecurePassword!';" || echo "User already exists."
sudo -u postgres psql -c "ALTER ROLE nexconnect_admin SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE nexconnect_admin SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE nexconnect_admin SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE nexconnect_db TO nexconnect_admin;"
# Required on PostgreSQL 15+ (Ubuntu 24.04)
sudo -u postgres psql -d nexconnect_db -c "GRANT ALL ON SCHEMA public TO nexconnect_admin;"

echo "================================================================"
echo "Setup complete! Next: clone your repo and follow DEPLOYMENT.md."
echo "  cd ~"
echo "  git clone <your-repo-url> NexConnect/Website"
echo "================================================================"
