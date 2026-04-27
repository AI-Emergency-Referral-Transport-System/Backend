import glob
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-fw@*-olpidf^0ooir34+lbq^hdn-w%q$00-!*)5o5r+lpkd63#',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True').strip().lower() == 'true'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')
    if host.strip()
]

AUTH_USER_MODEL = 'accounts.User'

OSGEO4W_BIN = Path(os.getenv("OSGEO4W_BIN", r"C:\OSGeo4W\bin"))
gdal_files = glob.glob(str(OSGEO4W_BIN / "gdal*.dll")) if OSGEO4W_BIN.exists() else []
GIS_ENABLED = bool(gdal_files)

if GIS_ENABLED:
    os.environ["PATH"] = str(OSGEO4W_BIN) + os.pathsep + os.environ["PATH"]
    GDAL_LIBRARY_PATH = gdal_files[0]
    geos_library = OSGEO4W_BIN / "geos_c.dll"
    if geos_library.exists():
        GEOS_LIBRARY_PATH = str(geos_library)

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'channels',
    'accounts',
    'common',
]

if GIS_ENABLED:
    INSTALLED_APPS += [
        'django.contrib.gis',
        'tracking',
        'emergencies',
        'hospitals',
        'ambulances',
        'ai',
    ]

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

WSGI_APPLICATION = 'config.wsgi.application'

# Tell Django where your ASGI application is located
ASGI_APPLICATION = 'config.asgi.application'

# Configure the Channel Layer (uses Redis to pass messages between users)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

default_engine = 'django.contrib.gis.db.backends.postgis' if GIS_ENABLED else 'django.db.backends.sqlite3'
DATABASES = {
    'default': {
        'ENGINE': os.getenv('POSTGRES_ENGINE', default_engine),
        'NAME': os.getenv('POSTGRES_DB', 'herd_db'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'test'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('SQLITE_NAME', str(BASE_DIR / 'db.sqlite3')),
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OTP_DELIVERY_BACKEND = os.getenv('OTP_DELIVERY_BACKEND', 'email').strip().lower()
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@ai-emergency.local')
EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend',
)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '25'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False').strip().lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').strip().lower() == 'true'

if os.name == "nt" and not GIS_ENABLED:
    pass
elif os.name == "nt":
    gdal_library_path = os.getenv("GDAL_LIBRARY_PATH")
    geos_library_path = os.getenv("GEOS_LIBRARY_PATH")

    default_gdal_path = Path(r"C:\OSGeo4W\bin\gdal312.dll")
    default_geos_path = Path(r"C:\OSGeo4W\bin\geos_c.dll")

    if not gdal_library_path and default_gdal_path.exists():
        gdal_library_path = str(default_gdal_path)
    if not geos_library_path and default_geos_path.exists():
        geos_library_path = str(default_geos_path)

    if gdal_library_path:
        GDAL_LIBRARY_PATH = gdal_library_path
    if geos_library_path:
        GEOS_LIBRARY_PATH = geos_library_path

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
