# BookStore - Django E-Commerce App

A full-stack bookstore application built with **Django**, featuring full user auth, shopping cart functionality, payment integration, and a clean templating system for dynamic page rendering.

---

## Live Demo (optional)

**Frontend + Backend (Django):** [Heroku URL here]

---

## Features

- **Browse Books** – View book listings, details, and genres dynamically
-  **Shopping Cart** – Add/remove books, adjust quantities, view total costs
-  **User Authentication** – Sign up, log in, manage profile, and track orders
-  **Payments Integration** – Fully functioning checkout flow (Stripe or PayPal)
-  **Modular App Design** – Books, users, cart, and payments are separate Django apps
-  **Media Support** – Book covers and other uploaded assets served dynamically
-  **Admin Panel** – Full Django admin for managing books, users, and orders

---

## Tech Stack

- Python 3 + Django
- SQLite (default dev DB, easily upgradable to PostgreSQL)
- HTML5 + Django Templating
- Bootstrap / CSS for styling
- Gunicorn + Heroku-ready (`Procfile` included)
- Pipenv / virtualenv compatible (`requirements.txt` provided)

---

## Running Locally

### Clone the repo:
```bash
git clone https://github.com/Butler839/BookStore
cd BookStore
```

### Set up the environment:
```bash
python -m venv env
source env/bin/activate  # on Windows: env\Scripts\activate
pip install -r requirements.txt
```

### Run the server:
```bash
python manage.py migrate
python manage.py runserver
```

---

## Deployment Notes
- Use `Procfile` and `gunicorn` for Heroku deployment
- Set up `ALLOWED_HOSTS` and `DEBUG` properly for production
- Configure `STATIC_ROOT` and `MEDIA_ROOT` for assets on cloud

---
