import logging
import requests
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

class BaseSMSProvider(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> None:
        raise NotImplementedError

class ConsoleSMSProvider(BaseSMSProvider):
    def send_sms(self, phone_number: str, message: str) -> None:
        logger.info("SMS to %s: %s", phone_number, message)
        print(f"DEBUG SMS to {phone_number}: {message}")

# --- ADD THIS CLASS ---
class AfroMessageSMSProvider(BaseSMSProvider):
    def __init__(self, api_key: str, sender_id: str = ""):
        self.api_key = api_key
        self.sender_id = sender_id
        self.url = "https://api.afromessage.com/api/send"

        if not self.api_key:
            raise ImproperlyConfigured("AfroMessage requires AFROMESSAGE_API_KEY.")

    def send_sms(self, phone_number: str, message: str) -> None:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": phone_number,
            "message": message,
        }
        if self.sender_id:
            payload["from"] = self.sender_id

        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("acknowledge") != "success":
                errors = data.get("response", {}).get("errors", ["AfroMessage rejected the SMS request."])
                error_message = "; ".join(errors)
                logger.error("AfroMessage rejected SMS to %s: %s", phone_number, error_message)
                raise ImproperlyConfigured(error_message)
        except requests.exceptions.RequestException as e:
            logger.error(f"AfroMessage failed: {e}")
            # In a hackathon, you might want to print this to the console too
            print(f"AfroMessage Error: {e}")

# (Keep your Twilio and AfricasTalking classes here if you want to keep them)

class TwilioSMSProvider(BaseSMSProvider):
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        if not (self.account_sid and self.auth_token and self.from_number):
            raise ImproperlyConfigured(
                "Twilio requires TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER."
            )

    def send_sms(self, phone_number: str, message: str) -> None:
        logger.info("Twilio SMS to %s: %s", phone_number, message)
        print(f"DEBUG Twilio SMS to {phone_number}: {message}")

def get_sms_provider() -> BaseSMSProvider:
    provider_name = getattr(settings, "SMS_PROVIDER", "")

    if provider_name == "console":
        return ConsoleSMSProvider()
    
    # --- ADD THIS LOGIC ---
    if provider_name == "afromessage":
        return AfroMessageSMSProvider(
            api_key=settings.AFROMESSAGE_API_KEY,
            sender_id=getattr(settings, "AFROMESSAGE_SENDER_ID", "")
        )

    if provider_name == "twilio":
        return TwilioSMSProvider(
            account_sid=settings.TWILIO_ACCOUNT_SID,
            auth_token=settings.TWILIO_AUTH_TOKEN,
            from_number=settings.TWILIO_FROM_NUMBER,
        )

    if not provider_name:
        if settings.DEBUG:
            return ConsoleSMSProvider()
        raise ImproperlyConfigured("SMS_PROVIDER must be configured.")

    raise ImproperlyConfigured(f"Unsupported SMS provider: {provider_name}")

def send_sms(phone_number: str, message: str) -> None:
    provider = get_sms_provider()
    provider.send_sms(phone_number=phone_number, message=message)
