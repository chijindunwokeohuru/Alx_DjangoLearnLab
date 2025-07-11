# LibraryProject

A Django-based library management system developed for the COMP11124 Object-Oriented Programming course. This project demonstrates Django fundamentals including models, CRUD operations, ORM usage, and admin interface customization.

## Features

- **Book Management**: Add, view, update, and delete books
- **Django ORM**: Database operations using Django's Object-Relational Mapping
- **Admin Interface**: Customized Django admin panel for easy management
- **RESTful Design**: Clean URL structure and views

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd LibraryProject

# Or download and extract, then navigate to the project folder
```

### 2. Create and Activate Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv django_env

# Activate virtual environment
# On Windows:
django_env\Scripts\activate
# On macOS/Linux:
source django_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install django
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

- **Main Application**: <http://127.0.0.1:8000/>
- **Admin Panel**: <http://127.0.0.1:8000/admin/> (if superuser created)

## Project Structure

```text
LibraryProject/
├── manage.py                   # Django management script
├── db.sqlite3                  # SQLite database file
├── README.md                   # This file
├── LibraryProject/             # Main project package
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # URL routing configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
└── bookshelf/                  # Django app (if exists)
    ├── models.py               # Book model definition
    ├── views.py                # View functions
    ├── admin.py                # Admin configuration
    └── ...
```

## Usage

1. **Adding Books**: Use the Django admin interface to add books to the library
2. **Viewing Books**: Navigate to the main page to see all books
3. **Managing Data**: Use the admin panel for full CRUD operations

## Development

To modify the project:

1. Make sure your virtual environment is activated
2. Edit the relevant files in the `bookshelf/` app
3. Run migrations if you change models: `python manage.py makemigrations && python manage.py migrate`
4. Test your changes with `python manage.py runserver`

## Technologies Used

- **Django 5.2.4**: Web framework
- **Python 3.12**: Programming language
- **SQLite**: Database (default)
- **Django ORM**: Database abstraction layer

## Course Information

- **Course**: COMP11124 Object-Oriented Programming
- **Project Type**: Library Management System
- **Focus**: Django fundamentals and OOP concepts
