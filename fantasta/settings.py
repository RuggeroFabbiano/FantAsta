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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = 'ruggero_fabbiano@outlook.com'
DJANGO_EASY_HEALTH_CHECK = {'PATH': "/health-check"}
DOMAIN = 'fantasta.net'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ENV = getenv('ENVIRONMENT', 'dev')
INSTALLED_APPS = [
    # 'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_bootstrap5',
    'crispy_forms',
    'import_export',
]
LANGUAGE_CODE = 'it-it'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true']
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false']
        },
        'null': {'class': 'logging.NullHandler'}
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'], 'propagate': False
        },
        'fantasta': {'handlers': ['console'], 'level': 'DEBUG'}
    }
}
LOGIN_REDIRECT_URL = 'waiting_room'
LOGIN_URL = 'log-in'
LOGOUT_REDIRECT_URL = '/'
MIDDLEWARE = [
    'easy_health_check.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
ROOT_URLCONF = 'fantasta.urls'
SECRET_KEY = getenv(
    'DJANGO_KEY',
    'django-insecure-6e3bzkjtu(9*#20y@du$(*e-kj57jh)jzoabzk!dn793wn9x=#'
)
STATICFILES_DIRS = [BASE_DIR / 'fantasta' / 'static']
STATIC_ROOT = 'static'
STATIC_URL = 'static/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'fantasta' / 'templates'],
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
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1" if ENV == 'dev' else DOMAIN, 6379)]
        }
    }
}
DEBUG = ENV == 'dev'


if ENV == 'prod':
    ADMINS = [('Ruggero Fabbiano', 'ruggero_fabbiano@outlook.com')]
    ALLOWED_HOSTS = [DOMAIN, 'fantasta.eu-west-3.elasticbeanstalk.com']
    CSRF_COOKIE_SECURE = True
    # LOGGING['formatters'] = {
    #     'custom': {
    #         'style': '{',
    #         'format': '{levelname} {asctime} {message}'
    #     }
    # }
    # LOGGING['handlers']['fantasta'] = {
    #     'class': 'logging.FileHandler',
    #     'filename': F'/var/log/fantasta.log',
    #     'level': 'DEBUG',
    #     'formatter': 'custom'
    # }
    # LOGGING['loggers']['fantasta']['handlers'].append('fantasta')
    # LOGGING['loggers']['django'] = {
    #     'handlers': ['fantasta'], 'level': 'INFO', 'propagate': False
    # }
    # LOGGING['loggers']['django.request'] = {
    #     'handlers': ['mail_admins'], 'level': 'ERROR', 'propagate': False
    # }
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    # SECURE_HSTS_SECONDS = 31536000 # 1 year
    # SECURE_REDIRECT_EXEMPT = ['/health-check']
    # SECURE_SSL_REDIRECT = True
    # SERVER_EMAIL = 'ruggero_fabbiano@outlook.com'
    # SESSION_COOKIE_SECURE = True
    # SESSION_EXPIRE_AT_BROWSER_CLOSE = True