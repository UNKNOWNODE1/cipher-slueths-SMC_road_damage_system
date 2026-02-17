# cipher-slueths-SMC_road_damage_system
# SMC Road Damage Management Platform

> **AI-Assisted, Human-Controlled** Civic Infrastructure System for Solapur Municipal Corporation

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Overview

The SMC Road Damage Management Platform is a **web-first, production-ready** civic infrastructure system designed for immediate deployment in Solapur Municipal Corporation. It enables citizens to report road damage issues while providing municipal officials with AI-assisted tools for verification, routing, and resolution—all with **complete human oversight**.

### 🎯 Key Principles

1. **Human Control First**: AI assists, humans decide
2. **Transparency**: Every action is logged and auditable
3. **Simplicity**: Works with existing infrastructure
4. **Scalability**: JWT-based API for mobile app integration
5. **Modern Stack**: Works with Python 3.14+ (including alpha releases)
6. **Accountability**: Complete audit trails

## ✨ Features

### For Citizens
- ✅ **Simple Reporting**: Web-based form with GPS/manual location
- ✅ **Image Upload**: Multiple photos of road damage
- ✅ **Anonymous Option**: Report without revealing identity
- ✅ **Real-time Tracking**: Track report status 24/7
- ✅ **Notifications**: SMS/Email updates on progress

### For Officials
- ✅ **Smart Dashboard**: AI-filtered queue of pending reports
- ✅ **Verification Tools**: Quick approve/reject with override capability
- ✅ **Auto-Routing**: Intelligent department assignment (with manual control)
- ✅ **Workload Management**: See department capacity at a glance
- ✅ **Complete Audit Trail**: Every action logged

### AI Features (All with Human Override)
- ✅ **Image Verification**: "Is this actually road damage?"
- ✅ **Damage Classification**: Pothole, crack, waterlogging, etc.
- ✅ **Severity Assessment**: Low/Medium/High/Critical
- ✅ **Duplicate Detection**: Prevent duplicate reports
- ✅ **Fraud Flagging**: Identify suspicious patterns
- ✅ **Priority Scoring**: Suggest urgent cases

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/smc-platform.git
cd smc-platform

# 2. Copy environment file
cp .env.example .env
# Edit .env with your settings

# 3. Start all services
docker-compose up --build

# 4. Run migrations in another terminal
docker-compose exec web python manage.py migrate

# 5. Create superuser
docker-compose exec web python manage.py createsuperuser

# 6. Access the application
open http://localhost:8000
```

### Manual Setup

```bash
# 1. Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 4. Setup database
sudo -u postgres createdb smc_platform

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver

# 8. In another terminal, start Celery
celery -A smc_platform worker -l info
```

## 🏗️ Architecture

### Technology Stack

**Backend**
- Django 5.0 (Python web framework)
- Django REST Framework (API with JWT auth)
- PostgreSQL 15 (Database, SQLite supported for dev)
- Redis (Caching & task queue)
- Celery (Background tasks)
- Django Channels (Real-time WebSocket updates)
- WhiteNoise (Efficient static file serving)

**Frontend**
- Django Templates + Bootstrap 5
- Alpine.js (Interactive components)
- Leaflet.js (Maps with OpenStreetMap)
- Chart.js (Visualizations)

**AI/ML**
- TensorFlow/PyTorch (Image classification)
- Pre-trained models fine-tuned for Indian roads
- OpenCV (Image processing)
- scikit-learn (ML utilities)

## 📂 Project Structure

```
smc-platform/
├── accounts/               # User management
│   ├── models.py          # User, OTP, Activity models
│   ├── views.py           # Authentication views
│   └── serializers.py     # API serializers
├── departments/           # Department management
│   ├── models.py          # Department, Zone models
│   └── views.py           # Department views
├── reports/               # Core reporting functionality
│   ├── models.py          # Report, Image, ActionLog, Comment
│   ├── views.py           # Citizen & official views
│   └── forms.py           # Report forms
├── ai_engine/            # AI components
│   ├── models.py          # AI models tracking
│   ├── classifier.py      # Image classification
│   ├── duplicate.py       # Duplicate detection
│   └── tasks.py           # Celery tasks
├── dashboard/            # Official dashboard
│   ├── views.py           # Dashboard views
│   └── analytics.py       # Performance analytics
├── api/                  # REST API
│   ├── urls.py            # API routes
│   ├── views.py           # API views
│   └── serializers.py     # Data serializers
├── templates/            # HTML templates
├── static/               # Static assets
├── media/                # User uploads
├── smc_platform/         # Django project settings
├── docker-compose.yml    # Docker configuration
├── Dockerfile
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```



