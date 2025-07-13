# LibraryProject - Django Development Environment Setup

## Overview
This is a Django project created as part of the Django development environment setup task. The LibraryProject serves as the foundation for developing Django applications and demonstrates the basic Django project structure.

## Project Setup

### Prerequisites
- Python 3.x installed on your system
- pip package manager

### Installation Steps

1. **Install Django**
   ```bash
   pip install django
   ```

2. **Create Django Project**
   ```bash
   django-admin startproject LibraryProject
   ```

3. **Navigate to Project Directory**
   ```bash
   cd LibraryProject
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**
   Open your web browser and go to: http://127.0.0.1:8000/

## Project Structure

The Django project structure includes the following key components:

```
LibraryProject/
├── LibraryProject/ 
│   ├── __init__.py
│   ├── settings.py      # Configuration for the Django project
│   ├── urls.py          # URL declarations - "table of contents" of the site
│   ├── wsgi.py          # WSGI configuration for deployment
│   └── asgi.py          # ASGI configuration for async support
├── manage.py            # Command-line utility for Django project interaction
└── README.md           # Project documentation
```

### Key Files Description

- **settings.py**: Contains all configuration settings for the Django project including database settings, installed apps, middleware, and other project-specific configurations.

- **urls.py**: The URL dispatcher that maps URL patterns to views. Acts as a "table of contents" for your Django-powered site.

- **manage.py**: A command-line utility that provides various Django commands for:
  - Running the development server
  - Creating database migrations
  - Running tests
  - Creating superuser accounts
  - And many other administrative tasks

## Getting Started

1. Ensure you have completed the installation steps above
2. The development server should be running on http://127.0.0.1:8000/
3. You should see the Django welcome page confirming successful setup

## Next Steps

This project structure is now ready for:
- Creating Django applications
- Setting up models and databases
- Building views and templates
- Implementing URL routing

## Development Environment

- **Django Version**: Latest stable version
- **Python Version**: 3.x
- **Database**: SQLite (default for development)

## Notes

This project was created as part of the Django development environment setup task to:
- Gain familiarity with Django
- Understand Django project workflow
- Explore the default project structure
- Practice running the Django development server