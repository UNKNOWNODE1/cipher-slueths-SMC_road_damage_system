import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = 'sarangshukla'
    password = '123456'
    email = 'sarang@example.com'
    
    user, created = User.objects.get_or_create(username=username, defaults={
        'email': email,
        'user_type': 'admin',
        'is_staff': True,
        'is_superuser': True
    })
    
    if created:
        user.set_password(password)
        user.save()
        print(f"Created Admin user: {username}")
    else:
        user.set_password(password)
        user.user_type = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"Updated Admin user: {username} (Password set to 123456)")

if __name__ == '__main__':
    create_admin()
