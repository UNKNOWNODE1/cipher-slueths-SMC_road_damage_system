"""
Comprehensive Application Testing Script
Tests all major functionality and reports bugs
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from reports.models import Report
from departments.models import Department

User = get_user_model()

class ApplicationTester:
    def __init__(self):
        self.client = Client()
        self.bugs = []
        self.passed = []
        
    def log_pass(self, test_name):
        self.passed.append(test_name)
        print(f"[PASS] {test_name}")
        
    def log_bug(self, test_name, error):
        self.bugs.append((test_name, error))
        print(f"[BUG] {test_name}: {error}")
        
    def test_home_page(self):
        """Test home page loads"""
        try:
            response = self.client.get('/')
            if response.status_code == 200:
                self.log_pass("Home page loads")
            else:
                self.log_bug("Home page", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Home page", str(e))
            
    def test_login_page(self):
        """Test login page loads"""
        try:
            response = self.client.get('/accounts/login/')
            if response.status_code == 200:
                self.log_pass("Login page loads")
            else:
                self.log_bug("Login page", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Login page", str(e))
            
    def test_admin_login(self):
        """Test admin user can login"""
        try:
            admin = User.objects.filter(username='admin').first()
            if not admin:
                self.log_bug("Admin login", "Admin user does not exist")
                return
                
            logged_in = self.client.login(username='admin', password='admin123')
            if logged_in:
                self.log_pass("Admin can login")
            else:
                self.log_bug("Admin login", "Login failed with correct credentials")
        except Exception as e:
            self.log_bug("Admin login", str(e))
            
    def test_admin_dashboard(self):
        """Test admin dashboard loads"""
        try:
            # Login first
            self.client.login(username='admin', password='admin123')
            response = self.client.get('/dashboard/')
            if response.status_code == 200:
                self.log_pass("Admin dashboard loads")
            else:
                self.log_bug("Admin dashboard", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Admin dashboard", str(e))
            
    def test_department_dashboard(self):
        """Test department dashboard loads"""
        try:
            self.client.login(username='admin', password='admin123')
            response = self.client.get('/dashboard/department/')
            if response.status_code == 200:
                self.log_pass("Department dashboard loads")
                # Check for template errors
                content = response.content.decode('utf-8')
                if '{ {' in content or '} }' in content:
                    self.log_bug("Department dashboard", "Template syntax error found")
            else:
                self.log_bug("Department dashboard", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Department dashboard", str(e))
            
    def test_analytics_page(self):
        """Test analytics page loads"""
        try:
            self.client.login(username='admin', password='admin123')
            response = self.client.get('/dashboard/analytics/')
            if response.status_code == 200:
                self.log_pass("Analytics page loads")
            else:
                self.log_bug("Analytics page", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Analytics page", str(e))
            
    def test_report_list(self):
        """Test report list page"""
        try:
            self.client.login(username='citizen', password='citizen123')
            response = self.client.get('/reports/')
            if response.status_code == 200:
                self.log_pass("Report list page loads")
            else:
                self.log_bug("Report list", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Report list", str(e))
            
    def test_report_create_page(self):
        """Test report creation page"""
        try:
            self.client.login(username='citizen', password='citizen123')
            response = self.client.get('/reports/create/')
            if response.status_code == 200:
                self.log_pass("Report create page loads")
            else:
                self.log_bug("Report create page", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Report create page", str(e))
            
    def test_django_admin(self):
        """Test Django admin panel"""
        try:
            self.client.login(username='admin', password='admin123')
            response = self.client.get('/admin/')
            if response.status_code == 200:
                self.log_pass("Django admin panel loads")
            else:
                self.log_bug("Django admin", f"Status code {response.status_code}")
        except Exception as e:
            self.log_bug("Django admin", str(e))
            
    def test_database_queries(self):
        """Test database queries work"""
        try:
            user_count = User.objects.count()
            report_count = Report.objects.count()
            dept_count = Department.objects.count()
            
            if user_count > 0 and dept_count > 0:
                self.log_pass(f"Database queries work (Users: {user_count}, Reports: {report_count}, Depts: {dept_count})")
            else:
                self.log_bug("Database queries", "No data found in database")
        except Exception as e:
            self.log_bug("Database queries", str(e))
            
    def test_static_files(self):
        """Test static files are accessible"""
        try:
            response = self.client.get('/static/js/websocket_client.js')
            if response.status_code == 200:
                self.log_pass("Static files accessible")
            else:
                # Static files might not be served in dev mode, check if file exists
                import os
                if os.path.exists('static/js/websocket_client.js'):
                    self.log_pass("Static files exist")
                else:
                    self.log_bug("Static files", "websocket_client.js not found")
        except Exception as e:
            self.log_bug("Static files", str(e))
            
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("SMC Platform - Comprehensive Application Test")
        print("=" * 60)
        print()
        
        # Run all tests
        self.test_home_page()
        self.test_login_page()
        self.test_admin_login()
        self.test_admin_dashboard()
        self.test_department_dashboard()
        self.test_analytics_page()
        self.test_report_list()
        self.test_report_create_page()
        self.test_django_admin()
        self.test_database_queries()
        self.test_static_files()
        
        # Print summary
        print()
        print("=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Passed: {len(self.passed)}")
        print(f"Bugs Found: {len(self.bugs)}")
        print()
        
        if self.bugs:
            print("BUGS DETECTED:")
            print("-" * 60)
            for test_name, error in self.bugs:
                print(f"  - {test_name}: {error}")
            print()
            return False
        else:
            print("[SUCCESS] All tests passed! Application is working correctly.")
            return True

if __name__ == "__main__":
    tester = ApplicationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
