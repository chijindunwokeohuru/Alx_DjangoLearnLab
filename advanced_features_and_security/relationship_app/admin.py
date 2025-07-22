from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, Author, Library, Librarian, UserProfile

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

# Register other models
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['author']
    search_fields = ['title', 'author__name']


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['books']


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['name', 'library']
    list_filter = ['library']
    search_fields = ['name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']
