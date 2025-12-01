from django.core.management.base import BaseCommand
from library.models import Admin

class Command(BaseCommand):
    help = 'Create default admin account'

    def handle(self, *args, **kwargs):
        # Check if admin exists
        if not Admin.objects.filter(username='admin').exists():
            admin = Admin.objects.create(
                username='admin',
                full_name='System Administrator',
                email='admin@library.edu',
                is_active=True
            )
            admin.set_password('admin123')  # Set default password
            self.stdout.write(self.style.SUCCESS(f'Admin created successfully!'))
            self.stdout.write(self.style.SUCCESS(f'Username: admin'))
            self.stdout.write(self.style.SUCCESS(f'Password: admin123'))
        else:
            self.stdout.write(self.style.WARNING('Admin already exists!'))