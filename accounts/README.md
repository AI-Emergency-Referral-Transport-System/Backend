# Accounts Module

This module handles phone-number authentication, OTP delivery, JWT issuance, and profile management.

## SMS Providers

Supported providers:

- `console`
- `twilio`
- `africas_talking`

### Twilio

Set:

- `SMS_PROVIDER=twilio`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER` or `TWILIO_MESSAGING_SERVICE_SID`

### Africa's Talking

Set:

- `SMS_PROVIDER=africas_talking`
- `AFRICASTALKING_USERNAME`
- `AFRICASTALKING_API_KEY`
- `AFRICASTALKING_SENDER_ID` if your account uses one

## OTP Endpoints

- `POST /api/v1/auth/otp/request/`
- `POST /api/v1/auth/otp/verify/`
- `POST /api/v1/auth/token/refresh/`
- `GET/PATCH /api/v1/auth/profile/`

## Real SMS Test Flow

1. Install dependencies with `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env`.
3. Set `SMS_PROVIDER` and the matching provider credentials.
4. Run `python manage.py migrate`.
5. Start the server with `python manage.py runserver`.
6. Request an OTP with `POST /api/v1/auth/otp/request/`.
7. Check the real phone for the OTP.
8. Verify it with `POST /api/v1/auth/otp/verify/`.

## Notes

- OTPs are hashed before storage.
- OTPs expire after 5 minutes.
- Unused older OTPs are invalidated when a new one is issued.
- Console delivery is only allowed when `DEBUG=True`.
