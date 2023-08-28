from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-6e3bzkjtu(9*#20y@du$(*e-kj57jh)jzoabzk!dn793wn9x=#'
DEBUG = True

ALLOWED_HOSTS = []

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
    'account',
    'auction'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'fantasta.urls'

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

ASGI_APPLICATION = 'fantasta.asgi.application'
WSGI_APPLICATION = 'fantasta.wsgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)]
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]


LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'


STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'fantasta' / 'static']


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'ruggero.fabbiano@gmail.com'


CRISPY_ALLOWED_TEMPLATE_PACKS = CRISPY_TEMPLATE_PACK = 'bootstrap5'


LOGIN_URL = 'log-in'
LOGIN_REDIRECT_URL = 'waiting_room'
LOGOUT_REDIRECT_URL = '/'