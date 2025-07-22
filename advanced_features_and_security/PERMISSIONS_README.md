# Django Permissions and Groups Management System

This document explains the implementation of Django's permission and group system for controlling access to the bookshelf application.

## Overview

The system implements role-based access control using Django's built-in permissions and groups functionality to restrict access to book management operations.

## Custom Permissions Implementation

### 1. Model-Level Permissions

In `bookshelf/models.py`, the `Book` model defines custom permissions:

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

**Custom Permissions:**
- `can_view`: Allows viewing book list and details
- `can_create`: Allows creating new books
- `can_edit`: Allows editing existing books
- `can_delete`: Allows deleting books

### 2. View-Level Permission Enforcement

In `bookshelf/views.py`, each view is protected with permission decorators:

```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View to display all books - requires can_view permission."""
    
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View to create a new book - requires can_create permission."""
    
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """View to edit an existing book - requires can_edit permission."""
    
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """View to delete a book - requires can_delete permission."""
```

**Permission Enforcement:**
- `@permission_required()` decorator checks if user has specific permission
- `raise_exception=True` returns 403 Forbidden if permission denied
- Users without login are redirected to login page

## Groups and Role-Based Access Control

### 3. Predefined Groups

Three user groups are automatically created with different permission levels:

| Group | Permissions | Access Level |
|-------|-------------|--------------|
| **Viewers** | `can_view` | Read-only access to books |
| **Editors** | `can_view`, `can_create`, `can_edit` | Can view, create, and edit books |
| **Admins** | `can_view`, `can_create`, `can_edit`, `can_delete` | Full access to all operations |

### 4. Automatic Group Setup

The `setup_groups` management command creates groups and assigns permissions:

```bash
python manage.py setup_groups
```

**What it does:**
- Creates the three groups (Viewers, Editors, Admins)
- Assigns appropriate permissions to each group
- Displays a summary of the setup

### 5. Template-Level Permission Checks

In templates, permissions are checked before showing action buttons:

```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}" class="btn btn-success">Add New Book</a>
{% endif %}

{% if perms.bookshelf.can_edit %}
    <a href="{% url 'book_edit' book.pk %}" class="btn btn-warning">Edit</a>
{% endif %}

{% if perms.bookshelf.can_delete %}
    <a href="{% url 'book_delete' book.pk %}" class="btn btn-danger">Delete</a>
{% endif %}
```

## Testing the Permission System

### Step 1: Create Test Users

1. Access Django Admin at `/admin/`
2. Go to **Users** section
3. Create test users:
   - `viewer_user` (password: testpass123)
   - `editor_user` (password: testpass123)  
   - `admin_user` (password: testpass123)

### Step 2: Assign Users to Groups

1. In Django Admin, edit each user
2. In the **Groups** section, assign:
   - `viewer_user` → `Viewers` group
   - `editor_user` → `Editors` group
   - `admin_user` → `Admins` group

### Step 3: Test Permissions

Visit `/bookshelf/` and test with different users:

**As viewer_user:**
- ✅ Can see book list
- ✅ Can view book details
- ❌ Cannot see "Add New Book" button
- ❌ Cannot see "Edit" buttons
- ❌ Cannot see "Delete" buttons

**As editor_user:**
- ✅ Can see book list
- ✅ Can view book details
- ✅ Can see "Add New Book" button
- ✅ Can see "Edit" buttons
- ❌ Cannot see "Delete" buttons

**As admin_user:**
- ✅ Can see book list
- ✅ Can view book details
- ✅ Can see "Add New Book" button
- ✅ Can see "Edit" buttons
- ✅ Can see "Delete" buttons

## URL Configuration

The bookshelf URLs are configured in `bookshelf/urls.py`:

```python
urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
]
```

Main project URLs include bookshelf at `/bookshelf/` endpoint.

## Error Handling

### Permission Denied Scenarios

- **Unauthenticated users**: Redirected to login page
- **Authenticated users without permission**: See 403 Forbidden error
- **Template elements**: Hidden if user lacks permission

### Security Features

1. **View-level protection**: All sensitive operations protected by decorators
2. **Template-level hiding**: UI elements hidden based on permissions
3. **Database-level integrity**: Custom permissions stored in Django's permission system
4. **Group-based management**: Easy assignment of permissions via groups

## Management Commands

### setup_groups Command

**Purpose**: Automate the creation of groups and permission assignments

**Usage**:
```bash
python manage.py setup_groups
```

**Features**:
- Creates Viewers, Editors, and Admins groups
- Assigns appropriate permissions to each group
- Provides detailed output and summary
- Idempotent (safe to run multiple times)

## File Structure

```
bookshelf/
├── models.py                 # Book model with custom permissions
├── views.py                  # Permission-protected views
├── urls.py                   # URL routing configuration
├── admin.py                  # Django admin configuration
├── templates/bookshelf/      # HTML templates with permission checks
├── management/
│   └── commands/
│       └── setup_groups.py   # Custom management command
└── migrations/               # Database migrations including permissions
```

## Benefits of This Implementation

1. **Granular Control**: Specific permissions for different operations
2. **Role-Based Access**: Easy management through groups
3. **Security by Default**: All operations require explicit permissions
4. **User Experience**: UI adapts based on user permissions
5. **Maintainability**: Centralized permission management
6. **Scalability**: Easy to add new permissions and groups

## Future Enhancements

1. **Object-level permissions**: Row-level access control
2. **Dynamic role assignment**: API for role management
3. **Audit logging**: Track permission-based actions
4. **Custom permission backends**: Advanced permission logic
5. **API permissions**: REST API integration with DRF permissions
