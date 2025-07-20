import os
from pathlib import Path
from environ import Env


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
)
ROOT = BASE_DIR.parent.parent


# from Environment
env = Env(ALLOWED_HOSTS=(list, []))
Env.read_env(
    env_file=str(ROOT / ".env")
)


SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

ROOT_URLCONF = env("ROOT_URLCONF")

WSGI_APPLICATION = env(
    "WSGI_APPLICATION"
)

LANGUAGE_CODE = env("LANGUAGE_CODE")

TIME_ZONE = env("TIMEZONE")

USE_I18N = env("USE_I18N")

USE_TZ = env("USE_TZ")

STATIC_URL = env("STATIC_URL")

DEFAULT_AUTO_FIELD = env(
    "DEFAULT_AUTO_FIELD"
)

APPEND_SLASH = env("APPEND_SLASH")

# Hardcode
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

STATICFILES_DIRS = [ROOT / "static"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LOGGING = {
    "formatters": {
        "standard": {
            "format": "[%(levelname)s] %(asctime)s %(name)s: %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(
                ROOT
                / env("LOG_ROOT_PATH")
                / env("LOG_FILENAME")
            ),
            "maxBytes": 25
            * 1024
            * 1024,
            "backupCount": 10,
            "encoding": "utf8",
        },
    },
    "root": {
        "handlers": [
            "console",
            "file",
        ],
        "level": "DEBUG",
    },
}
