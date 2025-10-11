# Social Media API (Django + DRF) — initial auth & user model

## Setup
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
   (requirements: django, djangorestframework, djangorestframework-authtoken, pillow)
4. Set AUTH_USER_MODEL = 'accounts.User' in settings.py
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py createsuperuser
8. python manage.py runserver

## Endpoints
- POST /api/auth/register/  — register, returns token
- POST /api/auth/login/     — login, returns token
- GET/PATCH /api/auth/profile/ — user profile (auth required)

## Authentication
Use token authentication. Include header:
Authorization: Token <your_token>

## Notes
- profile_picture stored in MEDIA_ROOT (configure in settings.py)
- Use multipart/form-data when uploading images


POST /api/posts/<id>/like/        -> like post (auth required)
POST /api/posts/<id>/unlike/      -> unlike post (auth required)
GET  /api/notifications/           -> list notifications (auth required)
GET  /api/notifications/unread/    -> list unread notifications
POST /api/notifications/<id>/read/ -> mark notification read
POST /api/notifications/mark-all-read/ -> mark all notifications read
