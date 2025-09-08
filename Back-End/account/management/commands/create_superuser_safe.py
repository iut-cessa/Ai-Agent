"""
Django management command to create or update superuser.
This follows Django best practices for custom management commands.

Usage:
    python manage.py create_superuser_safe
    python manage.py create_superuser_safe --interactive
    python manage.py create_superuser_safe --email admin@example.com --username admin --password secret123
"""

import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Create a superuser if one does not exist, or update existing superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Superuser email address',
        )
        parser.add_argument(
            '--username', 
            type=str,
            help='Superuser username',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Superuser password',
        )
        parser.add_argument(
            '--interactive',
            action='store_true',
            help='Prompt for missing values interactively',
        )
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Update existing superuser if found',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from options, environment, or defaults
        email = (
            options.get('email') or 
            os.environ.get('DJANGO_SUPERUSER_EMAIL') or 
            'admin@admin.com'
        )
        username = (
            options.get('username') or 
            os.environ.get('DJANGO_SUPERUSER_USERNAME') or 
            'admin'
        )
        password = (
            options.get('password') or 
            os.environ.get('DJANGO_SUPERUSER_PASSWORD') or 
            'admin123'
        )
        
        # Interactive mode
        if options.get('interactive'):
            email = input(f"Email ({email}): ").strip() or email
            username = input(f"Username ({username}): ").strip() or username
            
            import getpass
            new_password = getpass.getpass(f"Password (current: {'*' * len(password)}): ")
            if new_password:
                password = new_password

        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("🚀 Superuser Management Command"))
        self.stdout.write("=" * 60)

        try:
            # Check if user exists by email
            existing_user = None
            try:
                existing_user = User.objects.get(email=email)
                self.stdout.write(
                    self.style.WARNING(f"✅ User with email '{email}' already exists")
                )
            except User.DoesNotExist:
                pass

            # Check if user exists by username
            if not existing_user:
                try:
                    existing_user = User.objects.get(username=username)
                    self.stdout.write(
                        self.style.WARNING(f"✅ User with username '{username}' already exists")
                    )
                except User.DoesNotExist:
                    pass

            if existing_user:
                if options.get('force_update'):
                    # Update existing user
                    existing_user.email = email
                    existing_user.username = username
                    existing_user.set_password(password)
                    existing_user.is_staff = True
                    existing_user.is_superuser = True
                    existing_user.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f"🔄 Updated existing superuser:")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"📋 Existing superuser details:")
                    )
                
                self._display_user_info(existing_user)
                
            else:
                # Create new superuser
                self.stdout.write(f"📝 Creating new superuser...")
                self.stdout.write(f"   Email: {email}")
                self.stdout.write(f"   Username: {username}")
                
                user = User.objects.create_superuser(
                    email=email,
                    username=username,
                    password=password
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f"🎉 Superuser created successfully!")
                )
                self._display_user_info(user)

            self.stdout.write("=" * 60)
            self.stdout.write(
                self.style.SUCCESS("✅ Superuser management completed!")
            )
            self.stdout.write("")
            self.stdout.write("💡 Access points:")
            self.stdout.write("   - Django Admin: http://localhost/admin/")
            self.stdout.write("   - API Docs: http://localhost/swagger/")
            self.stdout.write("   - API Redoc: http://localhost/redoc/")

        except ValidationError as e:
            raise CommandError(f"Validation error: {e}")
        except Exception as e:
            raise CommandError(f"Error managing superuser: {e}")

    def _display_user_info(self, user):
        """Display user information in a formatted way."""
        self.stdout.write(f"   ID: {user.id}")
        self.stdout.write(f"   Username: {user.username}")
        self.stdout.write(f"   Email: {user.email}")
        self.stdout.write(f"   Is Staff: {user.is_staff}")
        self.stdout.write(f"   Is Superuser: {user.is_superuser}")
        self.stdout.write(f"   Date Joined: {user.date_joined}")
        self.stdout.write(f"   Last Login: {user.last_login or 'Never'}")
