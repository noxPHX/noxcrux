from django.contrib.messages import constants as messages
from split_settings.tools import include
from pathlib import Path
import os

include('settings_drf.py')
include('settings_cors.py')
include('settings_csp.py')
include('settings_axes.py')


def get_bool_env(env_var, default='False'):
    return os.getenv(env_var, default).lower() in ('true', '1', 't')


NOXCRUX_VERSION = "v1.13.0"

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / 'secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG = get_bool_env("DEBUG", 'True')

if not DEBUG:
    include('settings_security.py')

SECURE_REFERRER_POLICY = "no-referrer"

REGISTRATION_OPEN = get_bool_env("REGISTRATION_OPEN", 'True')
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

ROOT_URLCONF = 'noxcrux.urls'
WSGI_APPLICATION = 'noxcrux.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/web/login/'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'qr_code',
    'noxcrux_api.apps.NoxcruxAPIConfig',
    'noxcrux_server.apps.NoxcruxServerConfig',
    'noxcrux_server.templatetags',
    'drf_spectacular',
    'axes'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'noxcrux_server/templates']
        ,
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

try:
    with open('/run/secrets/noxcrux_db_passwd') as f:
        DB_PASSWORD = f.read().strip()
except FileNotFoundError:
    DB_PASSWORD = os.getenv("DB_PASSWORD", "noxcrux_db_passwd")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME", "noxcrux"),
        'USER': os.getenv("DB_USER", "noxcrux"),
        'PASSWORD': DB_PASSWORD,
        'HOST': os.getenv("DB_HOST", "172.26.0.74"),
        'PORT': os.getenv("DB_PORT", "5432"),
    }
}

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

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
