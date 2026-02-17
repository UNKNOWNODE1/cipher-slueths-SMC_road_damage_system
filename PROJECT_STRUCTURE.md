# SMC Road Damage Management Platform – Project Structure

## Overview

Django monorepo: backend (Django + DRF + Celery) and frontend (Django templates + Bootstrap). No separate frontend app; templates and static files live under the project root.

## Directory Layout

```
road damage system/
├── smc_platform/           # Backend: Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── api/                    # Backend: REST API (DRF)
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── accounts/               # Backend: auth & user management
│   ├── models.py           # CustomUser, UserActivity, OTP
│   ├── views.py
│   └── urls.py
├── departments/            # Backend: departments & zones
│   ├── models.py
│   └── admin.py
├── reports/                # Backend: reports, images, comments
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── dashboard/              # Backend: dashboard & analytics
│   ├── views.py
│   ├── analytics.py
│   └── urls.py
├── ai_engine/              # Backend: AI/ML (classification, duplicate detection)
│   ├── classifier.py
│   ├── duplicate.py
│   ├── tasks.py            # Celery tasks
│   └── models.py
├── templates/              # Frontend: HTML (Django templates)
│   ├── base.html
│   ├── base/
│   │   └── home.html
│   ├── registration/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── reports/
│   │   ├── create.html
│   │   ├── detail.html
│   │   ├── list.html
│   │   └── assign.html
│   └── dashboard/
│       ├── admin.html
│       ├── official.html
│       ├── base.html
│       └── analytics.html
├── static/                 # Frontend: CSS, JS, images (optional)
├── media/                  # User uploads (report images)
├── manage.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Backend vs Frontend

- **Backend**: Django apps (`smc_platform`, `api`, `accounts`, `departments`, `reports`, `dashboard`, `ai_engine`), REST API under `/api/`, Celery workers, DB (PostgreSQL or SQLite for dev).
- **Frontend**: Django templates in `templates/`, Bootstrap 5 + Font Awesome + Leaflet, optional assets in `static/`.

## Running the Project

1. **Environment**: Copy `.env.example` to `.env`. For local dev without PostgreSQL set `USE_SQLITE=true` in `.env`.
2. **Install**: `pip install -r requirements.txt`
3. **Database**: `python manage.py migrate`
4. **Run server**: `python manage.py runserver`
5. **Celery** (optional): `celery -A smc_platform worker -l info` (requires Redis).

## Key URLs

- Home: `/`
- Login/Register: `/accounts/login/`, `/accounts/register/`
- Reports: `/reports/create/`, `/reports/`, `/reports/<uuid>/`
- Dashboard: `/dashboard/`, `/dashboard/analytics/`
- REST API: `/api/` (auth, departments, zones, reports, etc.)
- Admin: `/admin/`
