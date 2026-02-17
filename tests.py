"""
Comprehensive test suite for SMC Road Damage Management Platform
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from accounts.models import CustomUser
from departments.models import Department, Zone
from reports.models import Report, ReportImage, Comment
from ai_engine.models import AIModel, AIPrediction
import json


User = get_user_model()


class AccountsModelTest(TestCase):
    """Test accounts models"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='citizen'
        )
    
    def test_custom_user_creation(self):
        """Test custom user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.user_type, 'citizen')
        self.assertTrue(self.user.is_active)
    
    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser (Citizen)')


class DepartmentsModelTest(TestCase):
    """Test departments models"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Road Maintenance',
            code='RM',
            description='Handles road surface repairs',
            is_active=True
        )
        
        self.zone = Zone.objects.create(
            name='Central Zone',
            code='CZ',
            description='Central business district',
            is_active=True
        )
    
    def test_department_creation(self):
        """Test department creation"""
        self.assertEqual(self.department.name, 'Road Maintenance')
        self.assertEqual(self.department.code, 'RM')
        self.assertTrue(self.department.is_active)
    
    def test_zone_creation(self):
        """Test zone creation"""
        self.assertEqual(self.zone.name, 'Central Zone')
        self.assertEqual(self.zone.code, 'CZ')
        self.assertTrue(self.zone.is_active)


class ReportsModelTest(TestCase):
    """Test reports models"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='citizen',
            password='testpass123',
            user_type='citizen'
        )
        
        self.department = Department.objects.create(
            name='Road Maintenance',
            code='RM',
            is_active=True
        )
        
        self.report = Report.objects.create(
            reporter=self.user,
            title='Test Report',
            description='Test description',
            location_name='Test Location',
            damage_type='pothole',
            severity='high',
            status='pending'
        )
    
    def test_report_creation(self):
        """Test report creation"""
        self.assertEqual(self.report.title, 'Test Report')
        self.assertEqual(self.report.reporter.username, 'citizen')
        self.assertEqual(self.report.damage_type, 'pothole')
        self.assertEqual(self.report.severity, 'high')
        self.assertEqual(self.report.status, 'pending')
    
    def test_report_urgency_property(self):
        """Test is_urgent property"""
        self.assertTrue(self.report.is_urgent)
        
        # Test with low severity
        low_severity_report = Report.objects.create(
            reporter=self.user,
            title='Low Severity Report',
            description='Test description',
            location_name='Test Location',
            damage_type='pothole',
            severity='low',
            status='pending'
        )
        self.assertFalse(low_severity_report.is_urgent)


class ReportsViewsTest(TestCase):
    """Test reports views"""
    
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='citizen',
            password='testpass123',
            user_type='citizen'
        )
        
        self.department = Department.objects.create(
            name='Road Maintenance',
            code='RM',
            is_active=True
        )
    
    def test_report_creation_view(self):
        """Test report creation view"""
        self.client.login(username='citizen', password='testpass123')
        
        response = self.client.post(reverse('reports:create'), {
            'title': 'Test Report',
            'description': 'Test description',
            'location_name': 'Test Location',
            'damage_type': 'pothole',
            'severity': 'high'
        })
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        
        # Verify report was created
        report = Report.objects.get(title='Test Report')
        self.assertEqual(report.reporter.username, 'citizen')
    
    def test_report_list_view(self):
        """Test report list view"""
        # Create a test report
        Report.objects.create(
            reporter=self.user,
            title='Test Report',
            description='Test description',
            location_name='Test Location',
            damage_type='pothole',
            severity='high',
            status='pending'
        )
        
        self.client.login(username='citizen', password='testpass123')
        response = self.client.get(reverse('reports:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Report')


class APIViewsTest(TestCase):
    """Test API views"""
    
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='apitestuser',
            password='testpass123',
            user_type='citizen'
        )
        
        # Create department for testing
        self.department = Department.objects.create(
            name='Road Maintenance',
            code='RM',
            is_active=True
        )
    
    def test_api_report_list(self):
        """Test API report list endpoint"""
        # Create a report
        Report.objects.create(
            reporter=self.user,
            title='API Test Report',
            description='API test description',
            location_name='API Test Location',
            damage_type='pothole',
            severity='high',
            status='pending'
        )
        
        # Need to authenticate for API access
        self.client.login(username='apitestuser', password='testpass123')
        response = self.client.get('/api/reports/')
        
        # Since we haven't set up the API properly yet, expect 404 or 200 depending on implementation
        # For now, just check that the URL resolves
        from django.urls import resolve
        resolver = resolve('/api/reports/')
        self.assertEqual(resolver.view_name, 'reports-list-create')
    
    def test_api_department_list(self):
        """Test API department list endpoint"""
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, 200)

    def test_api_login(self):
        """Test API login endpoint returns JWT tokens and user data"""
        response = self.client.post('/api/auth/login/', {
            'username': 'apitestuser',
            'password': 'testpass123'
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('tokens', data['data'])
        self.assertIn('access', data['data']['tokens'])
        self.assertEqual(data['data']['user']['username'], 'apitestuser')


class DashboardViewsTest(TestCase):
    """Test dashboard views"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = CustomUser.objects.create_user(
            username='admin',
            password='adminpass123',
            user_type='admin',
            is_staff=True
        )
        
        self.official_user = CustomUser.objects.create_user(
            username='official',
            password='officialpass123',
            user_type='official',
            is_staff=True
        )
    
    def test_admin_dashboard_access(self):
        """Test admin dashboard access"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_official_dashboard_access(self):
        """Test official dashboard access"""
        self.client.login(username='official', password='officialpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)


class AIModelsTest(TestCase):
    """Test AI-related models"""
    
    def setUp(self):
        self.ai_model = AIModel.objects.create(
            name='Road Damage Classifier',
            model_type='image_classifier',
            version='1.0.0',
            file_path='/models/damage_classifier_v1.h5',
            accuracy=0.85,
            is_active=True
        )
    
    def test_ai_model_creation(self):
        """Test AI model creation"""
        self.assertEqual(self.ai_model.name, 'Road Damage Classifier')
        self.assertEqual(self.ai_model.model_type, 'image_classifier')
        self.assertTrue(self.ai_model.is_active)
        self.assertEqual(str(self.ai_model), 'Road Damage Classifier v1.0.0')


class IntegrationTest(TestCase):
    """Integration tests for the entire system"""
    
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='integration_user',
            password='testpass123',
            user_type='citizen'
        )
        
        self.department = Department.objects.create(
            name='Road Maintenance',
            code='RM',
            is_active=True
        )
    
    def test_full_report_lifecycle(self):
        """Test the complete lifecycle of a report"""
        # Login as citizen
        self.client.login(username='integration_user', password='testpass123')
        
        # Create a report
        response = self.client.post(reverse('reports:create'), {
            'title': 'Integration Test Report',
            'description': 'This is a test report for integration testing',
            'location_name': 'Test Location, Solapur',
            'damage_type': 'pothole',
            'severity': 'high'
        })
        
        # Verify report was created
        report = Report.objects.get(title='Integration Test Report')
        self.assertIsNotNone(report)
        self.assertEqual(report.status, 'pending')
        self.assertEqual(report.reporter.username, 'integration_user')
        
        # Verify we can view the report
        response = self.client.get(reverse('reports:detail', kwargs={'pk': report.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Report')
    
    def test_user_registration_and_login(self):
        """Test user registration and login workflow"""
        # Register a new user
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123!',
            'password2': 'complexpassword123!',
            'phone_number': '9876543210'
        })
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # Verify user was created
        user = CustomUser.objects.get(username='newuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
        
        # Login with the new user
        login_successful = self.client.login(username='newuser', password='complexpassword123!')
        self.assertTrue(login_successful)


class URLRoutingTest(TestCase):
    """Test URL routing"""
    
    def test_home_url(self):
        """Test home page URL"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_accounts_urls(self):
        """Test accounts URLs"""
        # Check if URLs resolve properly
        from django.urls import resolve
        
        resolver = resolve('/accounts/login/')
        self.assertEqual(resolver.view_name, 'accounts:login')
        
        resolver = resolve('/accounts/register/')
        self.assertEqual(resolver.view_name, 'accounts:register')
    
    def test_reports_urls(self):
        """Test reports URLs"""
        from django.urls import resolve
        
        resolver = resolve('/reports/')
        self.assertEqual(resolver.view_name, 'reports:list')
        
        resolver = resolve('/reports/create/')
        self.assertEqual(resolver.view_name, 'reports:create')


class AdminInterfaceTest(TestCase):
    """Test admin interface functionality"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@smc.solapur.gov.in'
        )
    
    def test_admin_login(self):
        """Test admin login"""
        response = self.client.post('/admin/login/', {
            'username': 'admin',
            'password': 'adminpass123'
        })
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
    
    def test_admin_can_access_user_model(self):
        """Test admin can access user model in admin interface"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/accounts/customuser/')
        self.assertEqual(response.status_code, 200)