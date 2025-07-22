from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Test Django permissions system'
    
    def handle(self, *args, **options):
        self.stdout.write("="*60)
        self.stdout.write("DJANGO PERMISSIONS TESTING")
        self.stdout.write("="*60)
        
        # Create test users and assign to groups
        test_users = [
            ('test_viewer', 'Viewers'),
            ('test_editor', 'Editors'), 
            ('test_admin', 'Admins')
        ]
        
        for username, group_name in test_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@test.com'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f"✅ Created {username}")
            
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                self.stdout.write(f"✅ Added {username} to {group_name}")
            except Group.DoesNotExist:
                self.stdout.write(f"❌ Group {group_name} not found")
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write("PERMISSION TEST RESULTS")
        self.stdout.write("="*60)
        
        permissions = ['bookshelf.can_view', 'bookshelf.can_create', 'bookshelf.can_edit', 'bookshelf.can_delete']
        
        for username, group_name in test_users:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(f"\n{username} ({group_name}):")
                for perm in permissions:
                    has_perm = user.has_perm(perm)
                    status = "✅ HAS" if has_perm else "❌ NO"
                    self.stdout.write(f"  {status} {perm}")
            except User.DoesNotExist:
                self.stdout.write(f"❌ User {username} not found")
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write("TEST COMPLETE - Visit /bookshelf/ to test in browser!")
        self.stdout.write("="*60)
