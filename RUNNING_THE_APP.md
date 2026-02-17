# Running the SMC Road Damage Management Platform

## Quick Start (Recommended)

### Option 1: Using the Startup Script (Windows)
```cmd
start_server.bat
```

This will:
1. Check for virtual environment
2. Apply pending migrations
3. Start Celery worker (AI Engine)
4. Start Django development server

**Access the application at:** http://127.0.0.1:8000/

---

## Prerequisites

### Required Services

#### 1. **Redis Server** (for Celery & WebSockets)

**Windows:**
- Download Redis for Windows from: https://github.com/microsoftarchive/redis/releases
- Or use WSL2 with Redis
- Or use Docker: `docker run -d -p 6379:6379 redis:alpine`

**Check if Redis is running:**
```cmd
redis-cli ping
```
Should return: `PONG`

**If Redis is not installed:**
The application will still run, but:
- ✅ Web interface will work
- ✅ Dashboard will work
- ❌ Real-time updates (WebSockets) won't work
- ❌ AI processing (Celery tasks) won't work

---

## Running Without Redis (Development Mode)

If you don't have Redis installed, you can still run the application:

### Step 1: Start Django Server Only
```cmd
venv\Scripts\activate
python manage.py runserver
```

### Step 2: Access the Application
Open your browser to: http://127.0.0.1:8000/

**What works:**
- ✅ User authentication
- ✅ Report creation (manual)
- ✅ Dashboard viewing
- ✅ Admin panel
- ✅ All CRUD operations

**What doesn't work:**
- ❌ Real-time dashboard updates
- ❌ Automatic AI analysis of images
- ❌ Background task processing

---

## Running With Redis (Full Features)

### Step 1: Start Redis
```cmd
# If using Docker
docker run -d -p 6379:6379 redis:alpine

# Or if Redis is installed locally
redis-server
```

### Step 2: Start Celery Worker
```cmd
venv\Scripts\activate
celery -A smc_platform worker --loglevel=info -P solo
```

### Step 3: Start Django Server
```cmd
venv\Scripts\activate
python manage.py runserver
```

### Step 4: Access the Application
Open your browser to: http://127.0.0.1:8000/

---

## Default Login Credentials

### Admin User
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full system access, analytics, all dashboards

### Official User
- **Username:** `official`
- **Password:** `official123`
- **Access:** Department dashboard, assigned reports

### Citizen User
- **Username:** `citizen`
- **Password:** `citizen123`
- **Access:** Report creation, view own reports

---

## Application URLs

| Page | URL | Access |
|------|-----|--------|
| Home | http://127.0.0.1:8000/ | Public |
| Login | http://127.0.0.1:8000/accounts/login/ | Public |
| Register | http://127.0.0.1:8000/accounts/register/ | Public |
| Admin Dashboard | http://127.0.0.1:8000/dashboard/ | Admin only |
| Department Dashboard | http://127.0.0.1:8000/dashboard/department/ | Admin/Official |
| Analytics | http://127.0.0.1:8000/dashboard/analytics/ | Admin only |
| Create Report | http://127.0.0.1:8000/reports/create/ | Citizen |
| My Reports | http://127.0.0.1:8000/reports/ | Citizen |
| Django Admin | http://127.0.0.1:8000/admin/ | Admin only |

---

## Troubleshooting

### Issue: "Port 8000 already in use"
```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

### Issue: "Cannot connect to Redis"
**Solution 1:** Install and start Redis (see Prerequisites above)

**Solution 2:** Run without Redis (limited features)
- Just start Django server: `python manage.py runserver`
- Skip Celery worker

### Issue: "No module named 'gevent'"
**Solution:** Use `-P solo` instead of `-P gevent` for Celery on Windows
```cmd
celery -A smc_platform worker --loglevel=info -P solo
```

### Issue: "Template rendering error"
**Solution:** Ensure all migrations are applied
```cmd
python manage.py migrate
```

### Issue: "Static files not loading"
**Solution:** Collect static files
```cmd
python manage.py collectstatic --no-input
```

---

## Creating Test Data

### Create Demo Users
```cmd
python create_demo_users.py
```

### Add Sample Reports
```cmd
python manage.py add_report
```

---

## Stopping the Application

1. Press `Ctrl+C` in the Django server terminal
2. Press `Ctrl+C` in the Celery worker terminal (if running)
3. Stop Redis (if using Docker): `docker stop <container_id>`

---

## Production Deployment

For production deployment, please refer to:
- `DEPLOYMENT_STATUS.md` - Current deployment status
- `SETUP_GUIDE.md` - Comprehensive setup guide
- `docker-compose.yml` - Docker deployment configuration

---

## Need Help?

- Check `DIAGNOSTIC_REPORT.md` for system diagnostics
- Check `TEST_REPORT.md` for test results
- Check `TROUBLESHOOTING.md` for common issues
- Review Django logs in the console output

---

**🎉 Happy Testing!**
