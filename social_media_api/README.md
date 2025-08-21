# Social Media API

This project is a Django REST Framework-based API for a social media platform. It includes user registration, authentication, and profile management.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install django djangorestframework
   ```
2. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## User Authentication

- **Registration:**
  - Endpoint: `POST /api/accounts/register/`
  - Fields: `username`, `email`, `password`, `password2`, `bio` (optional), `profile_picture` (optional)
  - Returns: User data and authentication token

- **Login:**
  - Endpoint: `POST /api/accounts/login/`
  - Fields: `username`, `password`
  - Returns: User data and authentication token

- **Profile:**
  - Endpoint: `GET/PUT /api/accounts/profile/`
  - Requires authentication (Token in `Authorization` header)
  - Returns: User profile data

## User Model Overview

The custom user model extends Django's `AbstractUser` and includes:
- `bio`: Text field for user bio
- `profile_picture`: Image field for profile picture
- `followers`: Many-to-many relationship for user followers

## Notes
- Use tools like Postman to test registration and login endpoints.
- Tokens are returned on successful registration and login.
- Add more features (posts, comments, follows, notifications) as you progress.
