# Django Environment Configuration Guide

This guide explains how to manage different Django environments (development, staging, production) with proper HTTPS configuration.

## 🔧 Environment Structure

```
LibraryProject/
├── LibraryProject/
│   ├── settings.py          # Default settings (not recommended for production)
│   ├── base.py             # Base settings shared across environments
│   ├── settings_dev.py     # Development settings (HTTP allowed)
│   ├── settings_prod.py    # Production settings (HTTPS enforced)
│   └── settings_staging.py # Staging settings (optional)
├── manage_environment.py   # Environment management script
├── .env                   # Environment variables (create from .env.example)
└── manage.py
```

## 🚀 Quick Start

### 1. Initialize Environment Configuration
```bash
python manage_environment.py init
```

This creates a `.env` file template. Edit it with your configuration:

```bash
# Example .env configuration
DJANGO_ENVIRONMENT=dev
SECRET_KEY=your-super-secret-key-here
DEBUG=True
DB_PASSWORD=your-database-password
EMAIL_HOST_PASSWORD=your-email-password
```

### 2. List Available Environments
```bash
python manage_environment.py list
```

### 3. Switch Between Environments
```bash
# Switch to development (HTTP allowed)
python manage_environment.py switch --env dev

# Switch to production (HTTPS enforced)
python manage_environment.py switch --env prod
```

### 4. Validate Environment Configuration
```bash
python manage_environment.py validate --env dev
python manage_environment.py validate --env prod
```

## 🛠️ Development Environment (HTTP)

**File:** `settings_dev.py`

**Features:**
- ✅ DEBUG mode enabled
- ✅ HTTP connections allowed (`SECURE_SSL_REDIRECT = False`)
- ✅ Relaxed security settings for development
- ✅ SQLite database
- ✅ Console email backend
- ✅ Detailed logging to console and files

**Usage:**
```bash
# Set environment
export DJANGO_SETTINGS_MODULE=LibraryProject.settings_dev

# Or use the management script
python manage_environment.py switch --env dev

# Run development server
python manage.py runserver
```

**Security Notes:**
- 🔓 HTTPS not enforced (suitable for localhost)
- 🔓 Secure cookies disabled
- 🔓 Relaxed Content Security Policy
- ⚠️ **Never use in production!**

## 🔒 Production Environment (HTTPS)

**File:** `settings_prod.py`

**Features:**
- ✅ DEBUG mode disabled
- ✅ HTTPS enforced (`SECURE_SSL_REDIRECT = True`)
- ✅ HSTS enabled (1 year)
- ✅ Secure cookies required
- ✅ PostgreSQL database with SSL
- ✅ Strict Content Security Policy
- ✅ Production logging with rotation

**Usage:**
```bash
# Set environment
export DJANGO_SETTINGS_MODULE=LibraryProject.settings_prod

# Or use the management script
python manage_environment.py switch --env prod

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn (recommended)
gunicorn LibraryProject.wsgi:application --bind 0.0.0.0:8000
```

**Requirements:**
- 🔐 SSL certificate installed
- 🔐 HTTPS-enabled web server (Nginx/Apache)
- 🔐 PostgreSQL with SSL
- 🔐 Redis for caching
- 🔐 Proper domain configuration

## 📊 Environment Comparison

| Feature | Development | Production |
|---------|-------------|------------|
| HTTPS Required | ❌ No | ✅ Yes |
| HSTS | ❌ Disabled | ✅ 1 Year |
| Secure Cookies | ❌ No | ✅ Yes |
| DEBUG Mode | ✅ On | ❌ Off |
| Database | SQLite | PostgreSQL |
| Cache | Dummy | Redis |
| CSP | Relaxed | Strict |
| Logging | Console | Files + Rotation |

## 🔄 Environment Switching Commands

### Using Environment Manager Script

```bash
# List all available environments
python manage_environment.py list

# Switch to development
python manage_environment.py switch --env dev

# Switch to production  
python manage_environment.py switch --env prod

# Validate environment configuration
python manage_environment.py validate --env prod

# Run management commands with specific environment
python manage_environment.py run --env prod --command "collectstatic --noinput"
python manage_environment.py run --env dev --command "runserver"
```

### Using Django Settings Module

```bash
# Development
export DJANGO_SETTINGS_MODULE=LibraryProject.settings_dev
python manage.py runserver

# Production
export DJANGO_SETTINGS_MODULE=LibraryProject.settings_prod
python manage.py migrate
python manage.py collectstatic --noinput
```

### Using PowerShell (Windows)

```powershell
# Development
$env:DJANGO_SETTINGS_MODULE="LibraryProject.settings_dev"
python manage.py runserver

# Production
$env:DJANGO_SETTINGS_MODULE="LibraryProject.settings_prod"
python manage.py collectstatic --noinput
```

## 🔐 Security Checklist

### Development Environment ✅
- [x] Debug mode enabled for development
- [x] HTTP allowed for localhost testing
- [x] Basic security headers enabled
- [x] CSRF protection active
- [x] XSS filtering enabled

### Production Environment ✅
- [x] Debug mode disabled
- [x] HTTPS enforced with redirects
- [x] HSTS enabled (1 year policy)
- [x] Secure cookies enabled
- [x] Strong password validation
- [x] Strict Content Security Policy
- [x] Database connections use SSL
- [x] Static files served securely
- [x] Comprehensive security logging
- [x] Session security hardened

## 🚀 Deployment Workflow

### 1. Development Phase
```bash
# Work in development environment
python manage_environment.py switch --env dev
python manage.py runserver
```

### 2. Testing Phase
```bash
# Validate production settings locally
python manage_environment.py validate --env prod
```

### 3. Production Deployment
```bash
# Switch to production
python manage_environment.py switch --env prod

# Run deployment commands
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy

# Start production server
gunicorn LibraryProject.wsgi:application
```

## 🛡️ Security Best Practices

### Environment Variables
- Use `.env` files for sensitive configuration
- Never commit secrets to version control
- Use different secrets for each environment
- Rotate secrets regularly

### Database Security
- Use SSL/TLS for database connections
- Implement proper database user permissions
- Regular database backups
- Monitor database access logs

### HTTPS Configuration
- Use strong SSL/TLS certificates
- Enable HSTS with long duration
- Implement proper certificate monitoring
- Regular security header testing

## 📝 Environment Configuration Files

### `.env` Template
```bash
# Django Environment Configuration
DJANGO_ENVIRONMENT=dev
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DB_NAME=libraryproject
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password

# Domain
PRODUCTION_DOMAIN=yourdomain.com
```

### Django Settings Module
```python
# In your activation script or environment setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings_dev')
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Check Python path and virtual environment
   python manage_environment.py validate --env dev
   ```

2. **HTTPS Redirect Loops**
   ```bash
   # Check proxy headers and web server configuration
   # Ensure SECURE_PROXY_SSL_HEADER is correctly configured
   ```

3. **Static Files Not Loading**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Check STATIC_ROOT and web server configuration
   ```

4. **Database Connection Issues**
   ```bash
   # Check database credentials and SSL configuration
   python manage.py dbshell
   ```

This environment management system provides a robust foundation for secure Django application deployment across different environments while maintaining proper HTTPS security in production.
