# Deployment HTTPS Configuration (Nginx Example)

## 1. Install Certbot (Let’s Encrypt)
Ubuntu/Debian:
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx

## 2. Obtain SSL/TLS Certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

Certbot automatically updates Nginx config and installs certificates.

## 3. Force HTTPS Redirect (Nginx)
Example Nginx server blocks:

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

# HTTPS server
server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

## 4. Renew Certificates
sudo certbot renew --dry-run
