# 🚀 AWS Deployment Guide — Amazon Linux 2023

## What You Need
- AWS Account (free tier works)
- Your project pushed to GitHub

---

## Step 1: Launch EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Name: `multivendor-app`
3. AMI: **Amazon Linux 2023 AMI** (free tier eligible)
4. Instance type: **t2.micro** (free tier)
5. Key pair: Create new → download `.pem` file (keep it safe!)
6. Security Group → Add these rules:

| Type  | Port | Source   |
|-------|------|----------|
| SSH   | 22   | My IP    |
| HTTP  | 80   | Anywhere |
| HTTPS | 443  | Anywhere |

7. Click **Launch Instance**

---

## Step 2: Create RDS MySQL Database

1. **AWS Console → RDS → Create database**
2. Engine: **MySQL 8.0**
3. Template: **Free tier**
4. DB instance identifier: `multivendor-db`
5. Master username: `admin`
6. Master password: (save this!)
7. VPC: **Same VPC as EC2**
8. Public access: **No**
9. Security Group: allow port **3306** from EC2's security group
10. Click **Create database**

After creation, copy the **Endpoint URL** — this becomes your `DB_HOST` in `.env`

---

## Step 3: Connect to EC2

```bash
# On your local machine (Mac/Linux):
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@YOUR-EC2-PUBLIC-IP
```

> ⚠️ Amazon Linux 2023 default user is **`ec2-user`**, not `ubuntu`

---

## Step 4: Install System Dependencies

```bash
# Update packages
sudo dnf update -y

# Install Python 3.11 and pip
sudo dnf install python3.11 python3.11-pip -y

# Install MySQL client + dev libraries (needed for mysqlclient pip package)
sudo dnf install mysql mysql-devel -y

# Install Python dev headers and gcc (needed to compile mysqlclient)
sudo dnf install python3.11-devel gcc -y

# Install Nginx
sudo dnf install nginx -y

# Verify Python installed
python3.11 --version
```

---

## Step 5: Deploy Your App

```bash
# Create app directory
mkdir ~/app && cd ~/app

# Clone from GitHub (replace with your actual repo URL)
git clone https://github.com/your-username/django_multivendor_ecommerce_app.git .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## Step 6: Configure Environment Variables

```bash
nano ~/app/.env
```

Paste and fill these values:
```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=YOUR-EC2-PUBLIC-IP

DB_NAME=multivendor_ecommerce_django
DB_USER=admin
DB_PASSWORD=YOUR-RDS-PASSWORD
DB_HOST=YOUR-RDS-ENDPOINT.ap-south-1.rds.amazonaws.com
DB_PORT=3306

DEFAULT_FROM_EMAIL=rahulpanchal1872@gmail.com
EMAIL_USER=rahulpanchal1872@gmail.com
EMAIL_PASS=YOUR-GMAIL-APP-PASSWORD

CORS_ALLOWED_ORIGINS=http://YOUR-EC2-PUBLIC-IP
USE_S3=False
```
Save: `Ctrl+X` → `Y` → Enter

---

## Step 7: Create the Database on RDS

```bash
# Connect to RDS from EC2
mysql -h YOUR-RDS-ENDPOINT -u admin -p

# Inside MySQL shell:
CREATE DATABASE multivendor_ecommerce_django CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

## Step 8: Run Django Setup

```bash
cd ~/app
source venv/bin/activate

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser   # optional
```

---

## Step 9: Configure Gunicorn as a Service

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Paste this:
```ini
[Unit]
Description=Gunicorn daemon for Multivendor Django App
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/app
EnvironmentFile=/home/ec2-user/app/.env
ExecStart=/home/ec2-user/app/venv/bin/gunicorn \
          --config /home/ec2-user/app/gunicorn.conf.py \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn    # Should say: active (running)
```

---

## Step 10: Configure Nginx

```bash
sudo nano /etc/nginx/conf.d/multivendor.conf
```

> ⚠️ Amazon Linux 2023 uses `/etc/nginx/conf.d/` — NOT `sites-available` like Ubuntu

Paste this (replace YOUR-EC2-PUBLIC-IP):
```nginx
server {
    listen 80;
    server_name YOUR-EC2-PUBLIC-IP;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ec2-user/app/staticfiles/;
    }

    location /media/ {
        alias /home/ec2-user/app/media/;
    }

    location / {
        proxy_pass http://unix:/home/ec2-user/app/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }
}
```

```bash
# Test nginx config
sudo nginx -t                  # Should say: ok

# Start and enable nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

---

## ✅ Your App is Live!

- API: `http://YOUR-EC2-PUBLIC-IP/api/`
- Admin: `http://YOUR-EC2-PUBLIC-IP/admin/`

---

## Future Updates (after git push)

```bash
ssh -i your-key.pem ec2-user@YOUR-EC2-PUBLIC-IP
cd ~/app
git pull origin main
bash deploy.sh
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 502 Bad Gateway | `sudo systemctl status gunicorn` — check logs |
| Static CSS not loading | Re-run `python manage.py collectstatic --no-input` |
| DB connection refused | Check RDS security group allows EC2 on port 3306 |
| `ALLOWED_HOSTS` error | Add EC2 IP to `ALLOWED_HOSTS` in `.env` |
| Email not working | Use Gmail App Password, not normal Gmail password |
| `mysqlclient` install fails | Make sure `mysql-devel` and `gcc` are installed (Step 4) |
| Nginx 403 on static files | `chmod 755 /home/ec2-user` then restart nginx |
