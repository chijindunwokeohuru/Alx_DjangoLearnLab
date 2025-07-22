# LibraryProject - Django Permissions and Groups Management System

This Django project demonstrates advanced user authentication, custom user models, and comprehensive permissions and groups management for controlling access to different parts of the application.

## Project Overview

The LibraryProject implements:
- **Custom User Model** with extended fields (date_of_birth, profile_photo)
- **Role-Based Access Control** using Django groups and permissions
- **Permission-Protected Views** for book management operations
- **Granular Permissions** for viewing, creating, editing, and deleting books

## Features Implemented

### 1. Custom User Authentication
- Extended AbstractUser with additional fields
- Custom user manager for user creation
- Profile photo upload functionality
- Admin interface integration

### 2. Permissions and Groups System
- Custom model permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
- Three user groups with different access levels:
  - **Viewers**: Read-only access to books
  - **Editors**: Can view, create, and edit books
  - **Admins**: Full access to all operations

### 3. Security Implementation
- View-level permission enforcement using decorators
- Template-level permission checks for UI elements
- Automatic 403 Forbidden responses for unauthorized access
- User authentication required for all operations

## Directory Structure

```
LibraryProject/
├── LibraryProject/           # Main project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── bookshelf/               # Book management app
│   ├── models.py            # CustomUser and Book models with permissions
│   ├── views.py             # Permission-protected views
│   ├── admin.py             # Django admin configuration
│   ├── urls.py              # App URL patterns
│   ├── templates/           # HTML templates with permission checks
│   └── management/          # Custom management commands
│       └── commands/
│           ├── setup_groups.py     # Automated group setup
│           └── test_permissions.py # Permission testing
├── relationship_app/        # User profile and relationship management
├── media/                   # User uploaded files
└── manage.py               # Django management script
```

## Installation and Setup

### 1. Install Dependencies

```bash
pip install Django Pillow
```

### 2. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Setup Groups and Permissions

```bash
python manage.py setup_groups
```

### 5. Create Test Users

```bash
python manage.py test_permissions
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## Usage Guide

### Accessing the Application

1. **Admin Interface**: `http://127.0.0.1:8000/admin/`
   - Manage users, groups, and permissions
   - Assign users to groups
   - Configure book data

2. **Book Management**: `http://127.0.0.1:8000/bookshelf/`
   - View books (requires `can_view` permission)
   - Create new books (requires `can_create` permission)
   - Edit books (requires `can_edit` permission)
   - Delete books (requires `can_delete` permission)

### User Roles and Permissions

| Role | Permissions | Description |
|------|-------------|-------------|
| **Viewers** | `can_view` | Can only view books and book details |
| **Editors** | `can_view`, `can_create`, `can_edit` | Can manage books but cannot delete |
| **Admins** | `can_view`, `can_create`, `can_edit`, `can_delete` | Full access to all operations |

### Test Users

The system includes pre-created test users for demonstration:

- **test_viewer** (password: testpass123) - Viewers group
- **test_editor** (password: testpass123) - Editors group  
- **test_admin** (password: testpass123) - Admins group

## Custom Management Commands

### setup_groups
Creates user groups and assigns appropriate permissions.

```bash
python manage.py setup_groups
```

**Features:**
- Creates Viewers, Editors, and Admins groups
- Assigns specific permissions to each group
- Provides detailed output and summary
- Safe to run multiple times (idempotent)

### test_permissions
Creates test users and verifies permission assignments.

```bash
python manage.py test_permissions
```

**Features:**
- Creates test users with different roles
- Assigns users to appropriate groups
- Tests permission enforcement
- Displays comprehensive permission matrix

## Security Features

### View Protection
All views are protected with permission decorators:

```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View implementation
```

### Template Security
UI elements are conditionally displayed based on permissions:

```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Add New Book</a>
{% endif %}
```

### Error Handling
- **Unauthenticated users**: Redirected to login page
- **Unauthorized users**: Receive 403 Forbidden response
- **Missing permissions**: UI elements hidden automatically

## Model Definitions

### CustomUser Model
Extends Django's AbstractUser with additional fields:

```python
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
```

### Book Model with Custom Permissions
Defines granular permissions for book operations:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

## API Endpoints

| URL Pattern | View | Permission Required | Description |
|-------------|------|---------------------|-------------|
| `/bookshelf/` | book_list | `can_view` | List all books |
| `/bookshelf/book/<id>/` | book_detail | `can_view` | View book details |
| `/bookshelf/book/create/` | book_create | `can_create` | Create new book |
| `/bookshelf/book/<id>/edit/` | book_edit | `can_edit` | Edit existing book |
| `/bookshelf/book/<id>/delete/` | book_delete | `can_delete` | Delete book |

## Testing

### Manual Testing Steps

1. **Setup Test Environment**:
   ```bash
   python manage.py setup_groups
   python manage.py test_permissions
   ```

2. **Test Different User Roles**:
   - Login as `test_viewer` - should only see books
   - Login as `test_editor` - should see create/edit options
   - Login as `test_admin` - should see all options including delete

3. **Verify Permission Enforcement**:
   - Try accessing URLs directly without permissions
   - Verify 403 errors are returned appropriately
   - Check that UI elements are hidden based on permissions

### Automated Testing

The project includes management commands for automated testing:

```bash
# Test permission assignments
python manage.py test_permissions

# Verify group setup
python manage.py setup_groups
```

## Configuration

### Settings Configuration

Key settings for the permissions system:

```python
# Custom user model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Media files for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Installed apps
INSTALLED_APPS = [
    # ... default apps
    'bookshelf',
    'relationship_app',
]
```

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**:
   - Ensure user is assigned to appropriate group
   - Verify group has required permissions
   - Check that permissions were created during migration

2. **Template Not Found**:
   - Verify template directory structure
   - Check INSTALLED_APPS includes bookshelf
   - Ensure template files are in correct locations

3. **Media Files Not Loading**:
   - Verify MEDIA_URL and MEDIA_ROOT settings
   - Check URL configuration includes media serving
   - Ensure media directories exist

### Debug Commands

```bash
# Check user permissions
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='test_viewer'); print([p.codename for p in user.get_all_permissions()])"

# List all groups and permissions
python manage.py shell -c "from django.contrib.auth.models import Group; [print(f'{g.name}: {[p.codename for p in g.permissions.all()]}') for g in Group.objects.all()]"
```

## Contributing

This project demonstrates Django best practices for:
- Custom user model implementation
- Permission and group management
- Security-first development
- Comprehensive testing strategies

## License

This project is for educational purposes as part of the ALX Backend Python curriculum.

---

**Note**: This implementation serves as a foundation for role-based access control in Django applications and can be extended for more complex permission scenarios.
