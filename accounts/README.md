# Accounts Module

This module handles email-only OTP authentication, JWT issuance, and profile management.

## OTP Delivery

The branch defaults to real email delivery over SMTP.

Set:
- `OTP_DELIVERY_BACKEND=email`
- `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS` or `EMAIL_USE_SSL`
- `DEFAULT_FROM_EMAIL`

For Gmail:
- `EMAIL_HOST=smtp.gmail.com`
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=True`
- `EMAIL_HOST_PASSWORD` should be a Google App Password

## OTP Endpoints

- `GET /api/v1/auth/`
- `POST /api/v1/auth/otp/request/`
- `POST /api/v1/auth/otp/verify/`
- `POST /api/v1/auth/token/refresh/`
- `GET/PATCH /api/v1/auth/profile/`

## Browser Test Flow

1. Install dependencies with `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env`.
3. Put your real sender email and app password into `.env`.
4. Run `python manage.py migrate`.
5. Start the server with:
```powershell
cd C:\Users\Admin\Desktop\hackathon\Backend-Django-v1-email-otp
$env:POSTGRES_ENGINE='django.db.backends.sqlite3'
$env:SQLITE_NAME='C:\Users\Admin\Desktop\hackathon\Backend-Django-v1-email-otp\db.sqlite3'
C:\Users\Admin\Desktop\hackathon\.venv\Scripts\python.exe manage.py runserver
```
6. Open `/api/v1/auth/otp/request/` and submit:
```json
{"email":"test@gmail.com"}
```
7. Check the target inbox for the OTP email.
8. Open `/api/v1/auth/otp/verify/` and submit:
```json
{"email":"test@gmail.com","code":"123456"}
```
9. Replace `123456` with the real code from the email.

## Confirm It Worked In VS Code

Use this command after requesting the OTP:

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

If it instead shows:

```python
{'user_exists': False, 'otp_count': 0, 'phone_number': None}
```

then usually one of these is true:

1. The request failed before user creation.
2. The server is running from a different folder than the one you checked.
3. The server and shell are using different databases.

To inspect the request result directly:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/auth/otp/request/" `
  -ContentType "application/json" `
  -Body '{"email":"test@gmail.com"}'
```

## Notes

- OTPs are hashed before storage.
- OTPs expire after 5 minutes.
- Unused older OTPs are invalidated when a new one is issued.
- The phone number is optional and no longer required for OTP auth.
