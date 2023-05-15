from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

BASE_HOST_NAME = "localhost:8000"
BASE_URL = "http://" + BASE_HOST_NAME

ALLOWED_HOSTS = [BASE_HOST_NAME, "localhost", "127.0.0.1", "[::1]"]

CORS_ALLOWED_ORIGINS = [
    "*"
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

KEYCLOAK_BASE_URL = "https://test-auth.gdfenhancer.com"
KEYCLOAK_WEB_CLIENT_ID = ""
KEYCLOAK_REALM_NAME = ""
KEYCLOAK_WEB_CLIENT_SECRET = ""
KEYCLOAK_ADMIN_NAME = ""
KEYCLOAK_ADMIN_PASSWORD = ""
KEYCLOAK_ADMIN_SECRET = ""

# 로깅설정
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(pathname)s: %(lineno)d: %(funcName)s: %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / f"logs/mysite.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}