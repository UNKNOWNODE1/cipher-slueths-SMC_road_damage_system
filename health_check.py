"""
Quick Application Health Check Script
Tests basic functionality of the SMC Road Damage Management Platform
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from reports.models import Report
from departments.models import Department
from django.db import connection

User = get_user_model()

def test_database_connection():
    """Test database connectivity"""
    try:
        connection.ensure_connection()
        print("[OK] Database connection: OK")
        return True
    except Exception as e:
        print(f"[FAIL] Database connection: FAILED - {e}")
        return False

def test_models():
    """Test model queries"""
    try:
        user_count = User.objects.count()
        report_count = Report.objects.count()
        dept_count = Department.objects.count()
        
        print(f"[OK] Models working:")
        print(f"   - Users: {user_count}")
        print(f"   - Reports: {report_count}")
        print(f"   - Departments: {dept_count}")
        return True
    except Exception as e:
        print(f"[FAIL] Models: FAILED - {e}")
        return False

def test_admin_user():
    """Check if admin user exists"""
    try:
        admin = User.objects.filter(username='admin').first()
        if admin:
            print(f"[OK] Admin user exists: {admin.username} ({admin.user_type})")
            return True
        else:
            print("[WARN] Admin user not found - run create_demo_users.py")
            return False
    except Exception as e:
        print(f"[FAIL] Admin user check: FAILED - {e}")
        return False

def test_redis_connection():
    """Test Redis connectivity (optional)"""
    try:
        import redis
        from django.conf import settings
        
        # Extract Redis URL
        broker_url = settings.CELERY_BROKER_URL
        r = redis.from_url(broker_url, socket_connect_timeout=2)
        r.ping()
        print("[OK] Redis connection: OK")
        return True
    except ImportError:
        print("[WARN] Redis library not installed (optional)")
        return False
    except Exception as e:
        print(f"[WARN] Redis connection: UNAVAILABLE - {e}")
        print("   Note: Application will work without Redis, but real-time features disabled")
        return False

def main():
    """Run all health checks"""
    print("=" * 60)
    print("SMC Road Damage Management Platform - Health Check")
    print("=" * 60)
    print()
    
    results = []
    
    # Critical tests
    results.append(("Database", test_database_connection()))
    results.append(("Models", test_models()))
    results.append(("Admin User", test_admin_user()))
    
    # Optional tests
    results.append(("Redis", test_redis_connection()))
    
    print()
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    
    critical_passed = all([r[1] for r in results[:3]])
    
    if critical_passed:
        print("[OK] Application is ready to run!")
        print()
        print("Start the server with:")
        print("  python manage.py runserver")
        print()
        print("Or use the startup script:")
        print("  start_server.bat")
        print()
        print("Access at: http://127.0.0.1:8000/")
    else:
        print("[FAIL] Some critical checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

