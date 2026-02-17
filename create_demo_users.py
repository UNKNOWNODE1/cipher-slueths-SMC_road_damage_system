import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from departments.models import Department
from accounts.models import CustomUser

User = get_user_model()

def create_users():
    print("Creating demo users...")

    # 1. Ensure Department exists
    dept, created = Department.objects.get_or_create(
        name="Road Maintenance",
        defaults={'description': 'Handles road repairs and maintenance'}
    )
    if created:
        print(f"Created department: {dept.name}")
    else:
        print(f"Using existing department: {dept.name}")

    # 2. Admin User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass', user_type='admin')
        print("Created Admin user: admin / adminpass")
    else:
        print("Admin user already exists (password unchanged)")

    # 3. Official User
    if not User.objects.filter(username='official').exists():
        User.objects.create_user('official', 'official@example.com', 'officialpass', user_type='official', department=dept)
        print("Created Official user: official / officialpass")
    else:
        print("Official user already exists (password unchanged)")

    # 4. Citizen User
    if not User.objects.filter(username='citizen').exists():
        User.objects.create_user('citizen', 'citizen@example.com', 'citizenpass', user_type='citizen')
        print("Created Citizen user: citizen / citizenpass")
    else:
        print("Citizen user already exists (password unchanged)")

    print("\nDone! You can now use these credentials for the walkthrough.")

if __name__ == '__main__':
    create_users()
