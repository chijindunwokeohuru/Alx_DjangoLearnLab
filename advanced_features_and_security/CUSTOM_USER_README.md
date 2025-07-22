# Custom User Model Implementation

This project implements a custom user model in Django as part of the Advanced Features and Security task.

## Implementation Overview

### 1. Custom User Model (`LibraryProject/bookshelf/models.py`)

Created a `CustomUser` model that extends Django's `AbstractUser`:

```python
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    date_of_birth = DateField(null=True, blank=True, help_text="User's date of birth")
    profile_photo = ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True, 
        help_text="User's profile photo"
    )
```

### 2. Custom User Manager (`LibraryProject/bookshelf/models.py`)

Implemented a `CustomUserManager` to handle user creation:

```python
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        # Creates and saves a regular user
        
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # Creates and saves a superuser
```

### 3. Settings Configuration (`LibraryProject/LibraryProject/settings.py`)

Updated Django settings to use the custom user model:

```python
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 4. Admin Configuration (`LibraryProject/bookshelf/admin.py`)

Created a custom admin interface for the user model:

```python
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth']
```

### 5. URL Configuration (`LibraryProject/LibraryProject/urls.py`)

Added media file serving for development:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Features Implemented

1. **Extended User Fields**:
   - `date_of_birth`: DateField for storing user's birth date
   - `profile_photo`: ImageField for user profile pictures

2. **Custom User Management**:
   - Custom user creation logic
   - Superuser creation with proper field handling

3. **Admin Interface**:
   - Custom admin form with additional fields
   - Enhanced list display and filtering
   - Proper field grouping in admin forms

4. **File Upload Support**:
   - Profile photo upload functionality
   - Media files properly configured
   - Upload directory structure created

## Dependencies

- **Pillow**: Required for ImageField support
  ```bash
  pip install Pillow
  ```

## Database Setup

1. **Fresh Migrations**: Since changing `AUTH_USER_MODEL` requires a fresh database:
   ```bash
   # Remove old database and migrations
   rm db.sqlite3
   rm relationship_app/migrations/000*.py
   
   # Create new migrations
   python manage.py makemigrations relationship_app
   python manage.py migrate
   ```

2. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

## Directory Structure

```
advanced_features_and_security/
├── media/
│   └── profile_photos/          # Upload directory for profile photos
├── LibraryProject/
│   ├── bookshelf/
│   │   ├── models.py           # CustomUser and CustomUserManager
│   │   ├── admin.py            # CustomUserAdmin configuration
│   │   └── migrations/         # Database migrations
│   └── LibraryProject/
│       ├── settings.py         # AUTH_USER_MODEL configuration
│       └── urls.py             # Media files URL handling
└── manage.py
```

## Testing

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the admin interface at `http://127.0.0.1:8000/admin/`

3. Verify that:
   - Custom user fields appear in the admin interface
   - User creation works with additional fields
   - Profile photo upload functionality works
   - User list displays custom fields

## Key Benefits

1. **Extensibility**: Easy to add more custom fields in the future
2. **Admin Integration**: Seamless integration with Django admin
3. **File Handling**: Built-in support for user profile photos
4. **Security**: Maintains Django's built-in authentication security
5. **Compatibility**: Works with Django's permission and group system

## Future Enhancements

- Add validation for date_of_birth (e.g., minimum age requirements)
- Implement image resizing for profile photos
- Add custom user profile views and forms
- Implement user profile editing functionality
