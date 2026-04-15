import os
from pathlib import Path

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.dev"),
)

django_asgi_app = get_asgi_application()

from config.routing import websocket_application


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": websocket_application,
    }
)
