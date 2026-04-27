# AI Emergency System Backend

Starter backend scaffold for a multi-actor emergency coordination platform built with Django, DRF, Channels, Redis, PostgreSQL, and GeoDjango.

## Apps

- `accounts`: custom users, roles, email OTP authentication, JWT entry points
- `emergencies`: emergency lifecycle scaffolding
- `hospitals`: hospital availability and capacity
- `ambulances`: ambulance registry and driver assignment
- `tracking`: geospatial tracking and WebSocket transport
- `ai`: AI messaging and RAG placeholders

## Quick start

1. Copy `.env.example` to `.env`.
2. Build and start services: `docker compose up --build`
3. Run migrations: `python manage.py migrate`
4. Create an admin user: `python manage.py createsuperuser`

## Email OTP Demo

This branch supports email-only OTP auth.

1. Start the server from this repo folder:
```powershell
cd C:\Users\Admin\Desktop\hackathon\Backend-Django-v1-email-otp
$env:POSTGRES_ENGINE='django.db.backends.sqlite3'
$env:SQLITE_NAME='C:\Users\Admin\Desktop\hackathon\Backend-Django-v1-email-otp\db.sqlite3'
C:\Users\Admin\Desktop\hackathon\.venv\Scripts\python.exe manage.py runserver
```
2. Open [http://127.0.0.1:8000/api/v1/auth/otp/request/](http://127.0.0.1:8000/api/v1/auth/otp/request/).
3. Submit:
```json
{"email":"test@gmail.com"}
```
4. Check the recipient inbox for the OTP email.
6. Open [http://127.0.0.1:8000/api/v1/auth/otp/verify/](http://127.0.0.1:8000/api/v1/auth/otp/verify/) and submit:
```json
{"email":"test@gmail.com","code":"123456"}
```
7. Replace `123456` with the real OTP from the email.

Before running the server, configure real SMTP credentials in `.env`:

```env
OTP_DELIVERY_BACKEND=email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

For Gmail, `EMAIL_HOST_PASSWORD` should be a Google App Password, not your normal account password.

## Verify From VS Code

After submitting the request, confirm the user and OTP were created:

```powershell
cd C:\Users\Admin\Desktop\hackathon\Backend-Django-v1-email-otp
$env:POSTGRES_ENGINE='django.db.backends.sqlite3'
$env:SQLITE_NAME='C:\Users\Admin\Desktop\hackathon\Backend-Django-v1-email-otp\db.sqlite3'
C:\Users\Admin\Desktop\hackathon\.venv\Scripts\python.exe manage.py shell -c "from accounts.models import User, OTPCode; u=User.objects.filter(email='test@gmail.com').first(); print({'user_exists': bool(u), 'otp_count': OTPCode.objects.filter(user=u).count() if u else 0, 'phone_number': getattr(u,'phone_number',None) if u else None})"
```

Expected result:

```python
{'user_exists': True, 'otp_count': 1, 'phone_number': None}
```

After OTP verification, confirm the user is marked verified:

```powershell
C:\Users\Admin\Desktop\hackathon\.venv\Scripts\python.exe manage.py shell -c "from accounts.models import User; u=User.objects.filter(email='test@gmail.com').first(); print({'is_verified': u.is_verified if u else None})"
```

## Troubleshooting

If you see:

```python
{'user_exists': False, 'otp_count': 0, 'phone_number': None}
```

check these:

1. Make sure `runserver` was started from `Backend-Django-v1-email-otp`, not another repo copy.
2. Make sure the server terminal and the `manage.py shell` command use the same SQLite env vars.
3. Check the server terminal for the real API result. You should see `202 Accepted` for `POST /api/v1/auth/otp/request/`.
4. If you do not see `202`, inspect the POST response directly:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/auth/otp/request/" `
  -ContentType "application/json" `
  -Body '{"email":"test@gmail.com"}'
```
