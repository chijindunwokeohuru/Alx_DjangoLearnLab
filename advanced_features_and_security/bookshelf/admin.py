from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import Book, CustomUser


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    """Custom admin for CustomUser model"""
    model = CustomUser
    
    # Add the custom fields to the admin interface
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Add custom fields to the add form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Display custom fields in the list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth']


# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for the Book model."""
    
    # Display fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Enable search functionality
    search_fields = ('title', 'author')
    
    # Add filters for better data management
    list_filter = ('publication_year', 'author')
    
    # Enable ordering by clicking on column headers
    ordering = ('title',)
    
    # Number of items per page in the admin list view
    list_per_page = 20
    
    # Enable date hierarchy (if we had a date field)
    # date_hierarchy = 'publication_year'
    
    # Customize the fieldsets for the detail view
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
    )
    
    # Add actions for bulk operations
    actions = ['mark_as_classic']
    
    def mark_as_classic(self, request, queryset):
        """Custom action to mark books as classics (example)."""
        updated = queryset.update(title=models.F('title') + ' (Classic)')
        self.message_user(request, f'{updated} book(s) marked as classic.')
    mark_as_classic.short_description = "Mark selected books as classics"
