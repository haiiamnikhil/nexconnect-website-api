# NexConnect – EC2 Ubuntu Deployment Guide (No Docker)

Deploy the Angular frontend and FastAPI backend directly on an EC2 Ubuntu 22.04/24.04 instance using Nginx + Gunicorn + systemd.

**Domain:** `nex-connect.in`  
**Server:** AWS EC2 Ubuntu 22.04 or 24.04  
**Ports required:** `22` (SSH), `80` (HTTP), `443` (HTTPS)

---

## Step 1 – Server Setup

SSH into your EC2 instance, then run the setup script (one-time):

```bash
ssh -i /path/to/key.pem ubuntu@<EC2-PUBLIC-IP>
git clone https://github.com/your-username/nexconnect-website.git ~/NexConnect/Website
cd ~/NexConnect/Website
chmod +x deployment/setup-server.sh
./deployment/setup-server.sh
```

This installs: Nginx, PostgreSQL, Python 3.11, Node.js 20, and Certbot.

---

## Step 2 – Configure the Backend

```bash
cd ~/NexConnect/Website/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**Create the `.env` file** (copy from the template and fill in real values):

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

| Variable                      | Description                                                      |
| ----------------------------- | ---------------------------------------------------------------- |
| `POSTGRES_USER`               | `nexconnect_admin`                                               |
| `POSTGRES_PASSWORD`           | Password set in setup-server.sh                                  |
| `POSTGRES_SERVER`             | `localhost`                                                      |
| `POSTGRES_PORT`               | `5432`                                                           |
| `POSTGRES_DB`                 | `nexconnect_db`                                                  |
| `JWT_SECRET`                  | Run: `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60`                                                             |
| `ALLOWED_ORIGINS`             | `https://nex-connect.in,https://www.nex-connect.in`              |

**Initialize the database:**

```bash
cd ~/NexConnect/Website/backend
source venv/bin/activate
python init_db.py
python setup_admin.py   # Follow prompts to create the admin user
deactivate
```

---

## Step 3 – Build the Frontend

```bash
cd ~/NexConnect/Website/frontend
npm ci
npm run build -- --configuration production
```

---

## Step 4 – Deploy systemd Service (Backend)

```bash
sudo cp ~/NexConnect/Website/deployment/systemd/nexconnect-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start nexconnect-backend
sudo systemctl enable nexconnect-backend
sudo systemctl status nexconnect-backend   # Should show: active (running)
```

---

## Step 5 – Deploy Nginx (Frontend + Reverse Proxy)

```bash
# Copy frontend build to web root
sudo mkdir -p /var/www/nexconnect/frontend/dist/frontend/browser
sudo cp -r ~/NexConnect/Website/frontend/dist/frontend/browser/* \
    /var/www/nexconnect/frontend/dist/frontend/browser/
sudo chown -R www-data:www-data /var/www/nexconnect

# Install Nginx config
sudo cp ~/NexConnect/Website/deployment/nginx/nexconnect.conf \
    /etc/nginx/sites-available/nexconnect.conf
sudo ln -s /etc/nginx/sites-available/nexconnect.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 6 – Enable HTTPS (Let's Encrypt)

Point your DNS A record for `nex-connect.in` → EC2 public IP, then:

```bash
sudo certbot --nginx -d nex-connect.in -d www.nex-connect.in
```

Certbot will automatically modify the nginx config to handle HTTPS. Alternatively, replace `nexconnect.conf` with `nexconnect-ssl.conf` (manual cert path method).

**Verify auto-renewal:**

```bash
sudo certbot renew --dry-run
```

---

## Step 7 – Verification

| Check                 | Command                                    |
| --------------------- | ------------------------------------------ |
| Backend is running    | `sudo systemctl status nexconnect-backend` |
| Backend API responds  | `curl http://localhost:8000/`              |
| Nginx config is valid | `sudo nginx -t`                            |
| View backend logs     | `journalctl -u nexconnect-backend -f`      |
| Site loads in browser | Visit `https://nex-connect.in`             |
| Swagger UI            | Visit `https://nex-connect.in/api/docs`    |

---

## Updating the App

```bash
cd ~/NexConnect/Website
chmod +x deployment/update.sh
./deployment/update.sh
```

---

## Troubleshooting

**Backend won't start:**

```bash
journalctl -u nexconnect-backend -n 50 --no-pager
```

Most common cause: missing or wrong `.env` values (especially `JWT_SECRET` or DB credentials).

**Nginx 502 Bad Gateway:**
The backend is not running. Check: `sudo systemctl status nexconnect-backend`.

**PostgreSQL connection refused:**

```bash
sudo -u postgres psql -c "\l"   # List databases
sudo systemctl status postgresql
```

**Permission denied on `/var/www/nexconnect`:**

```bash
sudo chown -R www-data:www-data /var/www/nexconnect
```
