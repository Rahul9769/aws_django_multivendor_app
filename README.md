# Django Multivendor Ecommerce App

A multivendor ecommerce REST API built with Django DRF and JWT authentication.

## Features
- Custom User model with Vendor / Customer roles
- JWT-based authentication (register, login, refresh token)
- Product & Category management (vendor only)
- Cart and Checkout system
- Order management
- Django Admin panel

## Tech Stack
- Django 5.2.9 + DRF 3.16.1
- MySQL (local dev) / AWS RDS MySQL (production)
- JWT via `djangorestframework-simplejwt`
- Gunicorn + Nginx on AWS EC2
- WhiteNoise for static files

---

## Local Development Setup

### 1. Clone & create virtual environment
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create .env file
```bash
cp .env.example .env
```
Edit `.env` and set:
- `SECRET_KEY` — generate a new one (see .env.example)
- `DEBUG=True`
- `DB_PASSWORD` — your local MySQL root password
- `EMAIL_USER`, `EMAIL_PASS` — Gmail + App Password

### 3. Create MySQL database
```sql
CREATE DATABASE multivendor_ecommerce_django CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Run migrations & start server
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API available at: `http://localhost:8000/api/`  
Admin panel: `http://localhost:8000/admin/`

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register/` | No | Register new user |
| POST | `/api/auth/login/` | No | Login, get JWT tokens |
| POST | `/api/auth/refresh/` | No | Refresh access token |
| GET/POST | `/api/categories/` | Vendor | List / Create categories |
| GET/PUT/DELETE | `/api/categories/<id>/` | Vendor | Category detail |
| GET/POST | `/api/products/` | Vendor | List / Create products |
| GET/PUT/DELETE | `/api/products/<id>/` | Vendor | Product detail |
| GET | `/api/cart/` | Customer | View cart |
| POST | `/api/cart/add/<product_id>/` | Customer | Add to cart |
| DELETE | `/api/cart/remove/<product_id>/` | Customer | Remove from cart |
| POST | `/api/cart/checkout/` | Customer | Place order |

---

## AWS Deployment

See full step-by-step guide: [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)

Quick summary:
1. Launch EC2 (Ubuntu 22.04) + RDS MySQL
2. SSH into EC2, clone repo, set up venv
3. Copy `.env.example` → `.env`, fill AWS/RDS values
4. Run `bash deploy.sh`
5. Configure Gunicorn systemd service + Nginx
