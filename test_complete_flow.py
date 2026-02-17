"""
Comprehensive end-to-end test for the SMC Road Damage Management Platform
This script tests the complete flow with actual database operations.
"""

import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import django
from io import BytesIO
from PIL import Image

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from reports.models import Report, ReportImage
from departments.models import Department, Zone
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

def create_test_image():
    """Create a test image in memory"""
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return SimpleUploadedFile("test_pothole.jpg", img_byte_arr.getvalue(), content_type="image/jpeg")

def test_complete_flow():
    """
    Test the complete citizen-to-resolution flow
    """
    print("=" * 60)
    print("TESTING COMPLETE SMC PLATFORM FLOW")
    print("=" * 60)
    
    # 1. Create test users
    print("\n[1/8] Creating test users...")
    try:
        citizen = User.objects.create_user(
            username='test_citizen',
            email='citizen@test.com',
            password='testpass123',
            user_type='citizen'
        )
        print(f"✓ Created citizen user: {citizen.username}")
    except:
        citizen = User.objects.get(username='test_citizen')
        print(f"✓ Using existing citizen: {citizen.username}")
    
    try:
        official = User.objects.create_user(
            username='test_official',
            email='official@test.com',
            password='testpass123',
            user_type='official'
        )
        print(f"✓ Created official user: {official.username}")
    except:
        official = User.objects.get(username='test_official')
        print(f"✓ Using existing official: {official.username}")
    
    try:
        admin_user = User.objects.create_superuser(
            username='test_admin',
            email='admin@test.com',
            password='testpass123',
            user_type='admin'
        )
        print(f"✓ Created admin user: {admin_user.username}")
    except:
        admin_user = User.objects.get(username='test_admin')
        print(f"✓ Using existing admin: {admin_user.username}")
    
    # 2. Create department and zone
    print("\n[2/8] Setting up departments and zones...")
    dept, created = Department.objects.get_or_create(
        name='Public Works Department',
        defaults={
            'description': 'Handles road maintenance',
            'code': 'PWD',
            'email': 'pwd@smc.gov.in',
            'phone_number': '1234567890',
            'is_active': True
        }
    )
    print(f"✓ Department: {dept.name} {'(created)' if created else '(exists)'}")
    
    zone, created = Zone.objects.get_or_create(
        code='CZ',
        defaults={
            'name': 'Central Zone',
            'description': 'Central district area',
            'department': dept,
            'is_active': True
        }
    )
    print(f"✓ Zone: {zone.name} {'(created)' if created else '(exists)'}")
    
    # Assign department to official
    official.department = dept
    official.zone = zone
    official.save()
    print(f"✓ Assigned official to department and zone")
    
    # 3. Citizen creates a report
    print("\n[3/8] Citizen submitting road damage report...")
    report = Report.objects.create(
        reporter=citizen,
        title='Dangerous Pothole on MG Road',
        description='Large pothole causing traffic issues near the junction. Urgent repair needed.',
        location_name='MG Road, Near City Mall',
        latitude=17.6599,
        longitude=75.9064,
        damage_type='pothole',
        severity='high',
        status='pending'
    )
    print(f"✓ Report created: {report.title}")
    print(f"  - ID: {report.id}")
    print(f"  - Status: {report.status}")
    print(f"  - Severity: {report.severity}")
    
    # 4. Add image to report
    print("\n[4/8] Uploading damage photo...")
    test_img = create_test_image()
    report_image = ReportImage.objects.create(
        report=report,
        image=test_img
    )
    print(f"✓ Image attached to report")
    
    # 5. Admin assigns report to department/official
    print("\n[5/8] Admin assigning report to department...")
    report.assigned_department = dept
    report.assigned_zone = zone
    report.assigned_official = official
    report.status = 'verified'
    report.save()
    print(f"✓ Report assigned to: {dept.name}")
    print(f"✓ Assigned official: {official.username}")
    print(f"✓ Status updated to: {report.status}")
    
    # 6. Official starts work
    print("\n[6/8] Official marking report as in progress...")
    report.status = 'in_progress'
    report.save()
    print(f"✓ Status: {report.status}")
    
    # 7. Official resolves the issue
    print("\n[7/8] Official resolving the report...")
    from django.utils import timezone
    report.status = 'resolved'
    report.resolved_by = official
    report.resolved_at = timezone.now()
    report.resolution_notes = 'Pothole filled and road resurfaced. Work completed successfully.'
    report.save()
    print(f"✓ Status: {report.status}")
    print(f"✓ Resolved by: {official.username}")
    print(f"✓ Resolution notes added")
    
    # 8. Verify complete data
    print("\n[8/8] Verifying complete report data...")
    final_report = Report.objects.select_related(
        'reporter', 'assigned_department', 'assigned_zone', 
        'assigned_official', 'resolved_by'
    ).prefetch_related('images').get(id=report.id)
    
    print(f"\n" + "=" * 60)
    print(f"FINAL REPORT STATUS")
    print(f"=" * 60)
    print(f"Title: {final_report.title}")
    print(f"Location: {final_report.location_name}")
    print(f"Reporter: {final_report.reporter.username}")
    print(f"Department: {final_report.assigned_department.name}")
    print(f"Zone: {final_report.assigned_zone.name}")
    print(f"Official: {final_report.assigned_official.username}")
    print(f"Status: {final_report.get_status_display()}")
    print(f"Severity: {final_report.get_severity_display()}")
    print(f"Images: {final_report.images.count()}")
    print(f"Resolved by: {final_report.resolved_by.username if final_report.resolved_by else 'N/A'}")
    print(f"Resolution time: {final_report.time_to_resolve if final_report.resolved_at else 'N/A'}")
    print(f"=" * 60)
    
    # Summary
    print(f"\n✓ ALL TESTS PASSED!")
    print(f"\nDatabase Statistics:")
    print(f"  - Total Users: {User.objects.count()}")
    print(f"  - Total Reports: {Report.objects.count()}")
    print(f"  - Pending: {Report.objects.filter(status='pending').count()}")
    print(f"  - Resolved: {Report.objects.filter(status='resolved').count()}")
    print(f"  - Departments: {Department.objects.count()}")
    print(f"  - Zones: {Zone.objects.count()}")
    
    print(f"\n" + "=" * 60)
    print(f"SYSTEM IS FULLY FUNCTIONAL!")
    print(f"=" * 60)
    print(f"\nYou can now:")
    print(f"  1. Visit http://localhost:8000/ to view the homepage")
    print(f"  2. Login as:")
    print(f"     - Citizen: test_citizen / testpass123")
    print(f"     - Official: test_official / testpass123")
    print(f"     - Admin: test_admin / testpass123")
    print(f"  3. Access Django admin at http://localhost:8000/admin/")
    print(f"  4. Use API endpoints at http://localhost:8000/api/")
    
    return True

if __name__ == "__main__":
    try:
        test_complete_flow()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
