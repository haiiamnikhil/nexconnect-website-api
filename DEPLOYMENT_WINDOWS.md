# NexConnect – EC2 Windows Server Deployment Guide

Deploy the Angular frontend and FastAPI backend natively on an **AWS EC2 Windows Server 2022** instance using **Nginx, NSSM, Uvicorn, and PowerShell**.

**Domain:** `nex-connect.in`  
**Server:** AWS EC2 Windows Server 2022 Base  
**Ports required:** `3389` (RDP), `80` (HTTP), `443` (HTTPS)

---

## Step 1 – Server Setup via RDP

1. Launch an EC2 Windows Server 2022 instance (t2.small or t2.medium recommended).
2. Connect to the instance via **RDP**.
3. Open **Windows PowerShell as Administrator**.
4. Clone the repository into `C:\Users\Administrator`:

```powershell
Set-Location C:\Users\Administrator
git clone https://github.com/haiiamnikhil/nexconnect-website-api.git nexconnect-api
Set-Location nexconnect-api
```

5. Run the setup script:

```powershell
.\deployment\windows\setup-server.ps1
```

> **IMPORTANT:** Once the script finishes, you **must close** the PowerShell window and open a **new** Administrator PowerShell window. This is required for Windows to reload the updated `PATH` environment variables (Node, Python, Nginx).

---

## Step 2 – Configure the Backend

In your _new_ Administrator PowerShell window:

```powershell
Set-Location C:\Users\Administrator\nexconnect-api\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Create the `.env` file:**
Create a `.env` file in `C:\Users\Administrator\nexconnect-api\backend\` using Notepad:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YourSecurePassword!
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nexconnect_db
JWT_SECRET=paste-your-generated-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOWED_ORIGINS=https://nex-connect.in,https://www.nex-connect.in
```

**Initialize Database:**
Ensure PostgreSQL is running, then create the `nexconnect_db` via pgAdmin.
Then initialize tables:

```powershell
python init_db.py
python setup_admin.py
```

Deactivate the virtual environment:

```powershell
deactivate
```

---

## Step 3 – Build the Frontend

```powershell
Set-Location C:\Users\Administrator
git clone https://github.com/haiiamnikhil/nexconnect-website-ui.git nexconnect-ui

Set-Location nexconnect-ui
npm ci
npm run build -- --configuration production
```

---

## Step 4 – Configure Nginx

Copy the custom Nginx configuration into the Chocolatey Nginx installation path:

```powershell
Copy-Item C:\Users\Administrator\nexconnect-api\deployment\windows\nginx\nexconnect-windows.conf C:\tools\nginx\conf\nginx.conf -Force
```

---

## Step 5 – Install Windows Services

We use **NSSM** (Non-Sucking Service Manager) to run FastAPI and Nginx as background Windows Services.

```powershell
Set-Location C:\Users\Administrator\nexconnect-api
.\deployment\windows\install-services.ps1
```

**Verify Services are running:**

```powershell
Get-Service NexConnect-FastAPI
Get-Service NexConnect-Nginx
```

_(Both should report `Running` status)._

**Sanity Check:**
Open Edge / Chrome on the server and navigate to `http://localhost`. The Angular site should appear!

---

## Step 6 – Enable HTTPS (Let's Encrypt for Windows)

1. Ensure your domain `nex-connect.in` points to the EC2 Public IP via an A-Record.
2. Download and install **Certbot for Windows** from [certbot.eff.org](https://certbot.eff.org/).
3. Open a new Admin PowerShell and run:

```powershell
certbot certonly --standalone -d nex-connect.in -d www.nex-connect.in
```

4. Replace the Nginx config with the SSL version:

```powershell
Copy-Item C:\Users\Administrator\nexconnect-api\deployment\windows\nginx\nexconnect-ssl-windows.conf C:\tools\nginx\conf\nginx.conf -Force
Restart-Service NexConnect-Nginx
```

---

## Future Updates

Every time you push new code to GitHub, simply run the update script as Administrator:

```powershell
C:\Users\Administrator\nexconnect-api\deployment\windows\update.ps1
```

---

## Troubleshooting

- **Check Nginx Logs:** `C:\tools\nginx\logs\error.log`
- **Check Backend Logs:** Open `Event Viewer` → Windows Logs → Application. Look for events from `nssm`.
- **Can't access site externally?** Ensure **Windows Defender Firewall** has an inbound rule allowing Ports 80 and 443. (AWS Security Group alone isn't enough on Windows).

```powershell
# Open Windows Firewall ports via PowerShell
New-NetFirewallRule -DisplayName "Allow HTTP/HTTPS" -Direction Inbound -LocalPort 80,443 -Protocol TCP -Action Allow
```
