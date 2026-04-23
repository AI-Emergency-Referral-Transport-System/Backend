import os
import logging
import requests
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


def _setting(name: str, default: str = "") -> str:
    value = getattr(settings, name, None)
    if value in (None, ""):
        value = os.getenv(name, default)
    return value


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

class AfroMessageSMSProvider(BaseSMSProvider):
    def __init__(
        self,
        token: str,
        from_name: str = "",
        sender_id: str = "",
        callback_url: str = "",
    ):
        self.token = token
        self.from_name = from_name
        self.sender_id = sender_id
        self.callback_url = callback_url

        if not self.token:
            raise ImproperlyConfigured("AfroMessage requires AFROMESSAGE_TOKEN.")

    def send_sms(self, phone_number: str, message: str) -> None:
        try:
            from afromessage import AfroMessage
            from afromessage.models.sms_models import SendSMSRequest
        except ImportError as exc:
            raise ImproperlyConfigured(
                "AfroMessage support requires the 'afromessage' package to be installed."
            ) from exc

        client = AfroMessage(token=self.token)
        payload = {
            "to": phone_number,
            "message": message,
        }
        if self.from_name:
            payload["from_"] = self.from_name
        if self.sender_id:
            payload["sender"] = self.sender_id
        if self.callback_url:
            payload["callback"] = self.callback_url

        request = SendSMSRequest(**payload)
        client.sms.send(request)


def get_sms_provider() -> BaseSMSProvider:
    provider_name = _setting("SMS_PROVIDER", "").strip().lower()

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
            messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_SID,
        )
    if provider_name in {"africas_talking", "africastalking"}:
        return AfricasTalkingSMSProvider(
            username=_setting("AFRICASTALKING_USERNAME"),
            api_key=_setting("AFRICASTALKING_API_KEY") or _setting("SMS_API_KEY"),
            sender_id=_setting("AFRICASTALKING_SENDER_ID") or _setting("SMS_SENDER_ID"),
        )
    if provider_name in {"afromessage", "afro_message"}:
        return AfroMessageSMSProvider(
            token=_setting("AFROMESSAGE_TOKEN"),
            from_name=_setting("AFROMESSAGE_FROM"),
            sender_id=_setting("AFROMESSAGE_SENDER_ID") or _setting("SMS_SENDER_ID"),
            callback_url=_setting("AFROMESSAGE_CALLBACK_URL"),
        )

    if not provider_name:
        if settings.DEBUG:
            return ConsoleSMSProvider()
        raise ImproperlyConfigured("SMS_PROVIDER must be configured.")

    raise ImproperlyConfigured(f"Unsupported SMS provider: {provider_name}")

def send_sms(phone_number: str, message: str) -> None:
    provider = get_sms_provider()
    provider.send_sms(phone_number=phone_number, message=message)
