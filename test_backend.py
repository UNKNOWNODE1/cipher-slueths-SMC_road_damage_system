"""
Backend Functionality Test
Tests models, views, serializers, and business logic
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from reports.models import Report, ReportImage
from departments.models import Department
from django.db import connection
from django.core.exceptions import ValidationError

User = get_user_model()

def test_database_connection():
    """Test database connection"""
    print("\n[TEST] Database Connection")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        print("  [OK] Database connection working")
        return True
    except Exception as e:
        print(f"  [FAIL] Database connection failed: {e}")
        return False

def test_user_model():
    """Test User model"""
    print("\n[TEST] User Model")
    try:
        # Test user creation
        user_count = User.objects.count()
        print(f"  [OK] User count: {user_count}")
        
        # Test user types
        admin_count = User.objects.filter(user_type='admin').count()
        official_count = User.objects.filter(user_type='official').count()
        citizen_count = User.objects.filter(user_type='citizen').count()
        print(f"  [OK] Admins: {admin_count}, Officials: {official_count}, Citizens: {citizen_count}")
        
        # Test admin user
        admin = User.objects.filter(username='admin').first()
        if admin:
            print(f"  [OK] Admin user exists: {admin.username}")
            if admin.check_password('admin123'):
                print(f"  [OK] Admin password correct")
            else:
                print(f"  [FAIL] Admin password incorrect")
                return False
        else:
            print(f"  [FAIL] Admin user not found")
            return False
            
        return True
    except Exception as e:
        print(f"  [FAIL] User model test failed: {e}")
        return False

def test_report_model():
    """Test Report model"""
    print("\n[TEST] Report Model")
    try:
        report_count = Report.objects.count()
        print(f"  [OK] Report count: {report_count}")
        
        # Test report statuses
        pending = Report.objects.filter(status='pending').count()
        verified = Report.objects.filter(status='verified').count()
        in_progress = Report.objects.filter(status='in_progress').count()
        resolved = Report.objects.filter(status='resolved').count()
        print(f"  [OK] Status breakdown - Pending: {pending}, Verified: {verified}, In Progress: {in_progress}, Resolved: {resolved}")
        
        # Test report with relations
        if report_count > 0:
            report = Report.objects.select_related('reporter', 'assigned_department').first()
            print(f"  [OK] Report relations working - Reporter: {report.reporter}, Dept: {report.assigned_department}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Report model test failed: {e}")
        return False

def test_department_model():
    """Test Department model"""
    print("\n[TEST] Department Model")
    try:
        dept_count = Department.objects.count()
        print(f"  [OK] Department count: {dept_count}")
        
        if dept_count > 0:
            dept = Department.objects.first()
            print(f"  [OK] Sample department: {dept.name}")
            
            # Test department reports
            dept_reports = Report.objects.filter(assigned_department=dept).count()
            print(f"  [OK] Reports in {dept.name}: {dept_reports}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Department model test failed: {e}")
        return False

def test_model_methods():
    """Test model methods and properties"""
    print("\n[TEST] Model Methods")
    try:
        # Test Report model methods
        if Report.objects.exists():
            report = Report.objects.first()
            
            # Test get_status_display
            status_display = report.get_status_display()
            print(f"  [OK] get_status_display() works: {status_display}")
            
            # Test get_damage_type_display
            damage_display = report.get_damage_type_display()
            print(f"  [OK] get_damage_type_display() works: {damage_display}")
            
            # Test get_severity_display
            severity_display = report.get_severity_display()
            print(f"  [OK] get_severity_display() works: {severity_display}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Model methods test failed: {e}")
        return False

def test_querysets():
    """Test complex querysets"""
    print("\n[TEST] QuerySets")
    try:
        # Test filtering
        pending_reports = Report.objects.filter(status='pending')
        print(f"  [OK] Filter query works: {pending_reports.count()} pending reports")
        
        # Test ordering
        recent_reports = Report.objects.order_by('-reported_at')[:5]
        print(f"  [OK] Ordering query works: {recent_reports.count()} recent reports")
        
        # Test aggregation
        from django.db.models import Count
        dept_stats = Department.objects.annotate(report_count=Count('assigned_reports'))
        print(f"  [OK] Aggregation query works: {dept_stats.count()} departments with counts")
        
        # Test select_related
        reports_with_relations = Report.objects.select_related('reporter', 'assigned_department')[:5]
        print(f"  [OK] select_related works: {reports_with_relations.count()} reports with relations")
        
        return True
    except Exception as e:
        print(f"  [FAIL] QuerySet test failed: {e}")
        return False

def test_api_serializers():
    """Test API serializers"""
    print("\n[TEST] API Serializers")
    try:
        from api.serializers import ReportSerializer, UserSerializer
        
        # Test ReportSerializer
        if Report.objects.exists():
            report = Report.objects.first()
            serializer = ReportSerializer(report)
            data = serializer.data
            print(f"  [OK] ReportSerializer works: {len(data)} fields")
        
        # Test UserSerializer
        if User.objects.exists():
            user = User.objects.first()
            serializer = UserSerializer(user)
            data = serializer.data
            print(f"  [OK] UserSerializer works: {len(data)} fields")
        
        return True
    except Exception as e:
        print(f"  [FAIL] API serializers test failed: {e}")
        return False

def test_views():
    """Test view functions exist and are importable"""
    print("\n[TEST] Views")
    try:
        from dashboard.views import dashboard_home, department_dashboard, admin_analytics
        print(f"  [OK] Dashboard views importable")
        
        from reports.views import report_list, report_create, report_detail
        print(f"  [OK] Report views importable")
        
        from accounts.views import login_view, register_view, profile_view
        print(f"  [OK] Account views importable")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Views test failed: {e}")
        return False

def test_url_patterns():
    """Test URL patterns are configured"""
    print("\n[TEST] URL Patterns")
    try:
        from django.urls import resolve
        
        # Test main URLs
        resolve('/')
        print(f"  [OK] Home URL configured")
        
        resolve('/accounts/login/')
        print(f"  [OK] Login URL configured")
        
        resolve('/dashboard/')
        print(f"  [OK] Dashboard URL configured")
        
        resolve('/reports/')
        print(f"  [OK] Reports URL configured")
        
        return True
    except Exception as e:
        print(f"  [FAIL] URL patterns test failed: {e}")
        return False

def main():
    """Run all backend tests"""
    print("=" * 60)
    print("Backend Functionality Test")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Database Connection", test_database_connection()))
    results.append(("User Model", test_user_model()))
    results.append(("Report Model", test_report_model()))
    results.append(("Department Model", test_department_model()))
    results.append(("Model Methods", test_model_methods()))
    results.append(("QuerySets", test_querysets()))
    results.append(("API Serializers", test_api_serializers()))
    results.append(("Views", test_views()))
    results.append(("URL Patterns", test_url_patterns()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Backend Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    
    print(f"Passed: {passed}/{len(results)}")
    print(f"Failed: {failed}/{len(results)}")
    
    if failed > 0:
        print("\nFailed Tests:")
        for test_name, result in results:
            if not result:
                print(f"  - {test_name}")
        print("\n[FAIL] Backend has issues that need to be fixed")
        return False
    else:
        print("\n[SUCCESS] All backend tests passed!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
