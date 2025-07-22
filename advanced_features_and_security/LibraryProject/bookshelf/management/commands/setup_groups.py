from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    """
    Management command to create groups and assign permissions for the bookshelf app.
    
    Usage: python manage.py setup_groups
    """
    help = 'Create groups and assign permissions for bookshelf app'
    
    def handle(self, *args, **options):
        # Get the content type for Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create permissions
        permissions = {}
        permission_codenames = ['can_view', 'can_create', 'can_edit', 'can_delete']
        
        for codename in permission_codenames:
            try:
                permission = Permission.objects.get(
                    codename=codename,
                    content_type=book_content_type
                )
                permissions[codename] = permission
                self.stdout.write(f"Found permission: {codename}")
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Permission {codename} not found. Run migrations first.")
                )
                return
        
        # Create groups with specific permissions
        groups_config = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }
        
        for group_name, permission_codes in groups_config.items():
            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created group: {group_name}")
                )
            else:
                self.stdout.write(f"Group already exists: {group_name}")
            
            # Clear existing permissions and add new ones
            group.permissions.clear()
            
            for perm_code in permission_codes:
                if perm_code in permissions:
                    group.permissions.add(permissions[perm_code])
                    self.stdout.write(f"  Added permission {perm_code} to {group_name}")
            
            group.save()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up groups and permissions!')
        )
        
        # Print summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write("GROUPS AND PERMISSIONS SUMMARY:")
        self.stdout.write("="*50)
        
        for group_name, permission_codes in groups_config.items():
            self.stdout.write(f"\n{group_name}:")
            for perm_code in permission_codes:
                self.stdout.write(f"  - {perm_code}")
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write("NEXT STEPS:")
        self.stdout.write("1. Go to Django Admin (/admin/)")
        self.stdout.write("2. Create test users")
        self.stdout.write("3. Assign users to groups")
        self.stdout.write("4. Test permissions at /bookshelf/")
        self.stdout.write("="*50)
