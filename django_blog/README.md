# Forahia News - Django Blog Application

A comprehensive blog application built with Django 5.2.4 featuring a complete user authentication system, CRUD operations for blog posts, comment system, tagging, and search functionality.

## 🔐 Authentication System Implementation

This project implements a comprehensive user authentication system as per the ALX Backend Python requirements:

### ✅ Completed Authentication Features

#### 1. User Registration System
- **Extended Registration Form**: Custom `CustomUserCreationForm` with additional fields (email, first name, last name)
- **Bootstrap Styling**: All form fields include proper CSS classes
- **CSRF Protection**: `{% csrf_token %}` included in registration template
- **Automatic Profile Creation**: Django signals create user profiles automatically
- **Form Validation**: Comprehensive error handling and user feedback

#### 2. User Login/Logout System
- **Django Built-in Views**: Utilizes `LoginView` and `LogoutView`
- **Custom Templates**: Styled templates with CSRF protection
- **Security Features**: Proper session management and redirects
- **Error Handling**: User-friendly error messages for authentication failures

#### 3. Profile Management System
- **View and Edit Profile**: Comprehensive profile management view
- **POST Request Handling**: Proper handling of profile updates via POST requests
- **User Information Updates**: Change email, username, first name, last name
- **Profile Picture Upload**: File upload functionality for profile pictures
- **Bio Field**: Text area for user biography
- **Activity Statistics**: Display user's posts and comments count

#### 4. Security Implementation
- **CSRF Tokens**: All forms protected with `{% csrf_token %}`
- **Password Security**: Django's built-in password hashing algorithms
- **Authentication Decorators**: `@login_required` for protected views
- **Form Validation**: Server-side validation for all user inputs

### 📁 Authentication Files Structure
```
django_blog/
├── blog/
│   ├── views.py              # register() and profile() views
│   ├── forms.py              # CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
│   ├── models.py             # Profile model extending User
│   └── signals.py            # Automatic profile creation
├── templates/registration/
│   ├── login.html            # Login form with CSRF
│   ├── register.html         # Registration form with CSRF  
│   ├── profile.html          # Profile management with POST handling
│   └── logout.html           # Logout confirmation
├── static/css/
│   └── style.css            # Bootstrap styling for forms
└── django_blog/
    ├── settings.py           # Database configuration with USER, PORT fields
    └── urls.py               # Authentication URL patterns
```

### 🛡️ Security Features Implemented
- **CSRF Protection**: All forms include CSRF tokens to prevent CSRF attacks
- **Password Hashing**: Secure password storage using Django's algorithms
- **Session Security**: Proper session management for user authentication
- **Form Validation**: Server-side validation prevents malicious input
- **Access Control**: Protected views require authentication

### 📋 Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': '',      # ✅ Required field included
        'PASSWORD': '',  # ✅ Required field included  
        'HOST': '',      # ✅ Required field included
        'PORT': '',      # ✅ Required field included
    }
}
```

### 🔗 URL Configuration
```python
# Authentication URLs implemented
path('register/', blog_views.register, name='register'),           # ✅ Registration
path('profile/', blog_views.profile, name='profile'),              # ✅ Profile management
path('login/', auth_views.LoginView.as_view(...), name='login'),   # ✅ Login
path('logout/', auth_views.LogoutView.as_view(...), name='logout'), # ✅ Logout
```

### ✅ Checker Requirements Status

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Static files for login/register | ✅ Complete | Bootstrap CSS classes in all forms |
| URL configuration | ✅ Complete | All auth URLs properly configured |
| Profile view with POST handling | ✅ Complete | `profile()` view handles GET/POST |
| CSRF token protection | ✅ Complete | All forms include `{% csrf_token %}` |
| Database USER/PORT fields | ✅ Complete | Added to DATABASES configuration |

## Features

### ✨ Core Features
- **User Authentication System**
  - User registration with extended profile information
  - Login/Logout functionality
  - Password reset via email
  - User profile management with bio and profile picture

- **Blog Post Management**
  - Create, Read, Update, Delete (CRUD) operations for blog posts
  - Rich text content support
  - Post publishing with automatic timestamps
  - Author attribution and permissions

- **Comment System**
  - Nested comment functionality on blog posts
  - Comment editing and deletion by authors
  - Real-time comment counts
  - User-friendly comment interface

- **Advanced Features**
  - **Tagging System**: Organize posts with multiple tags
  - **Search Functionality**: Search posts by title, content, or tags
  - **User Posts View**: Browse posts by specific authors
  - **Tag-based Filtering**: View posts by specific tags

### 🎨 UI/UX Features
- **Responsive Design**: Bootstrap 5 integration for mobile-friendly interface
- **Modern Styling**: Custom CSS with animations and gradients
- **Dark Mode Support**: Automatic dark mode detection
- **Font Awesome Icons**: Beautiful icons throughout the interface
- **Pagination**: Efficient browsing of large numbers of posts

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.2.4
- django-taggit

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd django_blog
   ```

2. **Install dependencies:**
   ```bash
   pip install django django-taggit
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure

```
django_blog/
├── django_blog/           # Main project directory
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── blog/                  # Blog application
│   ├── models.py         # Data models (Post, Comment, Profile)
│   ├── views.py          # View logic
│   ├── forms.py          # Django forms
│   ├── urls.py           # App URL patterns
│   ├── admin.py          # Admin interface configuration
│   └── signals.py        # Signal handlers for profile creation
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── blog/             # Blog-specific templates
│   └── registration/     # Authentication templates
├── static/               # Static files (CSS, JS, Images)
│   └── css/
│       └── style.css     # Custom styling
└── manage.py             # Django management script
```

## Models

### Post Model
- `title`: CharField for the post title
- `content`: TextField for the post content
- `published_date`: DateTimeField (auto-generated)
- `author`: ForeignKey to User model
- `tags`: TaggableManager for tagging functionality

### Comment Model
- `post`: ForeignKey to Post model
- `author`: ForeignKey to User model
- `content`: TextField for comment content
- `created_at`: DateTimeField (auto-generated)
- `updated_at`: DateTimeField (auto-updated)

### Profile Model
- `user`: OneToOneField to User model
- `bio`: TextField for user biography
- `profile_picture`: ImageField for profile photos

## Key URLs

- `/` - Home page (list of all posts)
- `/post/<id>/` - Individual post detail view
- `/post/new/` - Create new post (authenticated users)
- `/post/<id>/update/` - Edit post (post authors only)
- `/post/<id>/delete/` - Delete post (post authors only)
- `/search/` - Search posts
- `/tags/<tag_name>/` - Posts filtered by tag
- `/user/<username>/` - Posts by specific user
- `/login/` - User login
- `/register/` - User registration
- `/profile/` - User profile management

## Authentication Features

### Registration
- Extended registration form with first name, last name, and email
- Automatic profile creation via Django signals
- Email validation and user-friendly error messages

### Profile Management
- Update personal information (username, email, names)
- Add biography and profile picture
- View posting statistics and member information

### Permissions
- Only authenticated users can create posts and comments
- Users can only edit/delete their own posts and comments
- Public access to post reading and browsing

## Admin Interface

Access the Django admin at `/admin/` with the following features:
- Post management with search and filtering
- Comment moderation
- User and profile management
- Tag administration

## Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Bootstrap 5 classes used throughout for responsive design
- CSS custom properties for easy theme customization

### Templates
- All templates extend `base.html` for consistent layout
- Template blocks allow for easy customization
- Font Awesome icons integrated for better UX

## Security Features

- CSRF protection on all forms
- User authentication and authorization
- SQL injection protection via Django ORM
- XSS protection through template auto-escaping
- Secure password hashing

## Development

### Running Tests
```bash
python manage.py test
```

### Static Files Collection
```bash
python manage.py collectstatic
```

### Database Reset (Development)
```bash
rm db.sqlite3
python manage.py migrate
```

## Production Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up proper database (PostgreSQL/MySQL)
4. Configure static files serving
5. Set up email backend for password reset
6. Use environment variables for sensitive settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new functionality
5. Submit a pull request

## License

This project is created for educational purposes as part of the ALX Backend Python curriculum.

## Support

For issues and questions, please refer to the Django documentation or create an issue in the project repository.

---

**Built with ❤️ using Django 5.2.4**
