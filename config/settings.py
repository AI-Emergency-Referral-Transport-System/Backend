import glob
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-fw@*-olpidf^0ooir34+lbq^hdn-w%q$00-!*)5o5r+lpkd63#')
DEBUG = True
ALLOWED_HOSTS = ['*']

# --- 1. GIS / GEODJANGO CONFIG ---
OSGEO4W_BIN = Path(os.environ.get("OSGEO4W_BIN", r"C:\OSGeo4W\bin"))
gdal_files = glob.glob(str(OSGEO4W_BIN / "gdal*.dll")) if OSGEO4W_BIN.exists() else []
GIS_ENABLED = bool(gdal_files)

if GIS_ENABLED:
    os.environ["PATH"] = str(OSGEO4W_BIN) + os.pathsep + os.environ["PATH"]
    GDAL_LIBRARY_PATH = gdal_files[0]
    geos_library = OSGEO4W_BIN / "geos_c.dll"
    if geos_library.exists():
        GEOS_LIBRARY_PATH = str(geos_library)
else:
    print(r"WARNING: GIS features are disabled because GDAL was not found.")

# --- 2. INSTALLED APPS ---
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party Apps
    'rest_framework',
    'rest_framework_simplejwt', 
    'channels',
    
    # Your Project Apps
    'accounts',
    'common',
]

if GIS_ENABLED:
    INSTALLED_APPS += [
        'tracking',
        'emergencies',
        'hospitals',
        'ambulances',
        'ai',
    ]

# --- 3. AUTH & USER CONFIG ---
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# --- 4. DATABASE CONFIG ---
USE_POSTGRES = os.environ.get("USE_POSTGRES", "").lower() in {"1", "true", "yes", "on"}

if USE_POSTGRES:
    default_engine = "django.contrib.gis.db.backends.postgis" if GIS_ENABLED else "django.db.backends.postgresql"
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("POSTGRES_ENGINE", default_engine),
            "NAME": os.environ.get("POSTGRES_DB", "herd_db"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- 5. CHANNELS / ASGI ---
ASGI_APPLICATION = 'config.asgi.application'
WSGI_APPLICATION = 'config.wsgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# --- 6. OTP DELIVERY CONFIG ---
SMS_PROVIDER = os.environ.get("SMS_PROVIDER", "console")
AFROMESSAGE_API_KEY = os.environ.get("AFROMESSAGE_API_KEY", "")
AFROMESSAGE_SENDER_ID = os.environ.get("AFROMESSAGE_SENDER_ID", "")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER", "")
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "no-reply@ai-emergency.local")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "").lower() in {"1", "true", "yes", "on"}
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "").lower() in {"1", "true", "yes", "on"}

# --- 7. MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

