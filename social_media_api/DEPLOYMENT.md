# Deployment Instructions for Heroku

## Prerequisites
- Heroku CLI installed
- GitHub repository for your project

## 1. Prepare your Django project
- Ensure you have a `Procfile` with:
  ```
  web: gunicorn social_media_api.wsgi
  ```
- Add `gunicorn`, `whitenoise`, and `psycopg2-binary` to your `requirements.txt`:
  ```
  pip install gunicorn whitenoise psycopg2-binary
  pip freeze > requirements.txt
  ```
- In `settings.py`:
  - Set `DEBUG = False`
  - Set `ALLOWED_HOSTS = ['*']` (or your Heroku app domain)
  - Add:
    ```python
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    ```

## 2. Deploy to Heroku
- Login to Heroku:
  ```
  heroku login
  ```
- Create Heroku app:
  ```
  heroku create your-app-name
  ```
- Add Heroku Postgres:
  ```
  heroku addons:create heroku-postgresql:hobby-dev
  ```
- Set environment variables:
  ```
  heroku config:set SECRET_KEY='your-secret-key'
  heroku config:set DEBUG=False
  ```
- Push code to Heroku:
  ```
  git push heroku main
  ```
- Run migrations and collectstatic:
  ```
  heroku run python manage.py migrate
  heroku run python manage.py collectstatic --noinput
  ```
- Open your app:
  ```
  heroku open
  ```

## 3. Maintenance
- Monitor logs:
  ```
  heroku logs --tail
  ```
- Update dependencies regularly.

## 4. Notes
- For custom domains, configure in Heroku dashboard.
- For media files, consider AWS S3 or similar.
