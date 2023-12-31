from os import environ, getenv
from pathlib import Path


APPEND_SLASH = False
ASGI_APPLICATION = 'fantasta.asgi.application'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]
BASE_DIR = Path(__file__).resolve().parent.parent
CRISPY_ALLOWED_TEMPLATE_PACKS = CRISPY_TEMPLATE_PACK = 'bootstrap5'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DEFAULT_FROM_EMAIL = 'ruggero.fabbiano@gmail.com'
ENV = getenv('ENVIRONMENT', 'dev')
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_bootstrap5',
    'crispy_forms',
    'import_export',
    'auction'
]
LANGUAGE_CODE = 'it-it'
LOGIN_REDIRECT_URL = 'rules'
LOGIN_URL = 'log-in'
LOGOUT_REDIRECT_URL = '/'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]
ROOT_URLCONF = 'fantasta.urls'
SECRET_KEY = getenv(
    'DJANGO_KEY',
    'django-insecure-6e3bzkjtu(9*#20y@du$(*e-kj57jh)jzoabzk!dn793wn9x=#'
)
STATICFILES_DIRS = [
    BASE_DIR / 'fantasta' / 'static',
    BASE_DIR / 'admin' / 'static'
]
STATIC_ROOT = '/static/'
STATIC_URL = 'static/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'fantasta' / 'templates',
            BASE_DIR / 'admin' / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        }
    }
]
TIME_ZONE = 'Europe/Rome'
WSGI_APPLICATION = 'fantasta.wsgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1' if ENV == 'dev' else 'redis', 6379)]
        }
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    } if ENV == 'dev' else {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ProdDB',
        'HOST': 'mysql8',
        'PORT': '3306',
        'USER': 'DjangoDB',
        'PASSWORD': environ['MYSQL_PASSWORD']
    }
}
DEBUG = ENV == 'dev'

if ENV == 'dev':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    ADMINS = [('Ruggero Fabbiano', 'ruggero_fabbiano@outlook.com')]
    ALLOWED_HOSTS = ['fantasta.net']
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ['https://fantasta.net']
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_PASSWORD = environ['EMAIL_PASSWORD']
    EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
    EMAIL_PORT = 587
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SERVER_EMAIL = 'ruggero_fabbiano@outlook.com'
    SESSION_COOKIE_SECURE = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True