import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

root = environ.Path(__file__) - 2
env = environ.Env(
    DEBUG=(bool, False),
    SENTRY_DSN=(str, None),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"])
)

environ.Env.read_env()

BASE_DIR = root()
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
SENTRY_DSN = env("SENTRY_DSN")

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'main',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'avstat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'avstat.wsgi.application'

DATABASES = {
    "default": env.db()
}

AUTH_PASSWORD_VALIDATORS = [
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True

if SENTRY_DSN and not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        'rest_framework.renderers.JSONRenderer',
    ],
    "UNAUTHENTICATED_USER": None,
    "PAGE_SIZE": 100,
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.LimitOffsetPagination',
}
