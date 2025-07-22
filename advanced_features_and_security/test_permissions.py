#!/usr/bin/env python
"""
Django Permission Testing Script

This script demonstrates how to test Django permissions programmatically.
Run with: python manage.py shell < test_permissions.py
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

User = get_user_model()

def test_permissions():
    print("="*60)
    print("DJANGO PERMISSIONS TESTING")
    print("="*60)
    
    # Get or create test users
    viewer_user, created = User.objects.get_or_create(
        username='test_viewer',
        defaults={'email': 'viewer@test.com'}
    )
    if created:
        viewer_user.set_password('testpass123')
        viewer_user.save()
        print("✅ Created test_viewer user")
    
    editor_user, created = User.objects.get_or_create(
        username='test_editor',
        defaults={'email': 'editor@test.com'}
    )
    if created:
        editor_user.set_password('testpass123')
        editor_user.save()
        print("✅ Created test_editor user")
    
    admin_user, created = User.objects.get_or_create(
        username='test_admin',
        defaults={'email': 'admin@test.com'}
    )
    if created:
        admin_user.set_password('testpass123')
        admin_user.save()
        print("✅ Created test_admin user")
    
    # Assign users to groups
    try:
        viewers_group = Group.objects.get(name='Viewers')
        editors_group = Group.objects.get(name='Editors')
        admins_group = Group.objects.get(name='Admins')
        
        viewer_user.groups.add(viewers_group)
        editor_user.groups.add(editors_group)
        admin_user.groups.add(admins_group)
        
        print("✅ Assigned users to groups")
    except Group.DoesNotExist:
        print("❌ Groups not found. Run: python manage.py setup_groups")
        return
    
    # Test permissions
    print("\n" + "="*60)
    print("PERMISSION TESTING RESULTS")
    print("="*60)
    
    permissions_to_test = [
        'bookshelf.can_view',
        'bookshelf.can_create', 
        'bookshelf.can_edit',
        'bookshelf.can_delete'
    ]
    
    users_to_test = [
        ('Viewer User', viewer_user),
        ('Editor User', editor_user),
        ('Admin User', admin_user)
    ]
    
    for user_label, user in users_to_test:
        print(f"\n{user_label} ({user.username}) permissions:")
        for perm in permissions_to_test:
            has_perm = user.has_perm(perm)
            status = "✅ HAS" if has_perm else "❌ NO"
            print(f"  {status} {perm}")
    
    # Display summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print("Test users created with following group assignments:")
    print("• test_viewer → Viewers group (can_view only)")
    print("• test_editor → Editors group (can_view, can_create, can_edit)")  
    print("• test_admin → Admins group (all permissions)")
    print("\nTo test in browser:")
    print("1. Go to /admin/ and login as superuser")
    print("2. Visit /bookshelf/ to see the book list")
    print("3. Login as different test users to verify permissions")
    print("="*60)

if __name__ == "__main__":
    test_permissions()
