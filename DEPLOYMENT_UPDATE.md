# NexConnect Deployment Update Guide

This guide describes how to apply the latest Light Theme UI changes and infrastructure updates to your production EC2 instance.

## Prerequisites

- SSH access to your EC2 instance.
- Git, Node.js, and NPM installed on the server (should be present if you ran `setup-server.sh`).

## Steps to Update

### 1. SSH into your Server

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 2. Navigate and Pull Latest Code

```bash
cd /var/www/nexconnect
git pull origin main
```

### 3. Rebuild the Frontend

The UI has been completely redesigned. You must rebuild the Angular application for the changes to take effect.

```bash
cd frontend
npm install  # Ensure any new dependencies are installed
npm run build
```

### 4. Verify Nginx Configuration

If you have already set up SSL using `nexconnect-ssl.conf`, Nginx is likely already pointing to the correct directory.
You can verify the path:

```bash
cat /etc/nginx/sites-available/nexconnect.conf | grep "root"
```

It should point to: `/var/www/nexconnect/dist/frontend/browser`

### 5. Restart Services (If Backend changed)

If you made changes to the Python API as well, restart the Gunicorn service:

```bash
sudo systemctl restart nexconnect-backend
```

### 6. Reload Nginx (Optional but recommended)

```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## Troubleshooting

- **Build Errors**: Ensure you have at least 2GB of RAM on the EC2 instance for the Angular build process. If it fails, you may need to add swap memory.
- **Permission Denied**: If you cannot write to the `dist` folder, ensure the directory permissions are correct:
  ```bash
  sudo chown -R $USER:$USER /var/www/nexconnect
  ```
