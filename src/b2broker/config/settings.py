import os
from pathlib import Path
from environ import Env
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT = BASE_DIR.parent.parent


# from Environment
env = Env(ALLOWED_HOSTS=(list, []))
Env.read_env(env_file=str(ROOT / ".env"))


SECRET_KEY = env("SECRET_KEY")

DJANGO_IS_DEBUG = env.bool("DJANGO_IS_DEBUG")
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

ROOT_URLCONF = env("ROOT_URLCONF")

WSGI_APPLICATION = env("WSGI_APPLICATION")

LANGUAGE_CODE = env("LANGUAGE_CODE")

TIME_ZONE = env("TIMEZONE")

USE_I18N = env.bool("USE_I18N")

USE_TZ = env.bool("USE_TZ")

STATIC_URL = env("STATIC_URL")

DEFAULT_AUTO_FIELD = env("DEFAULT_AUTO_FIELD")

APPEND_SLASH = env.bool("APPEND_SLASH")

CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS")

# Hardcode

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

SIDE_APPS = [
    "rest_framework",
    "rest_framework_json_api",
    "django_filters",
    "drf_spectacular",
]
PROJECT_APPS = ["app.core.apps.CoreConfig"]


INSTALLED_APPS = DJANGO_APPS + SIDE_APPS + PROJECT_APPS

STATICFILES_DIRS = [ROOT / "static"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "config.middlewares.LoggingMiddleware",
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
        "ENGINE": "django.db.backends.postgresql",
        "ATOMIC_REQUESTS": True,
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": (
            env("POSTGRES_LOCAL_HOST")
            if not os.path.exists("/.dockerenv")
            else env("POSTGRES_CONTAINER_HOST")
        ),
        "PORT": env("POSTGRES_PORT"),
        # "OPTIONS": {
        #     "default_transaction_isolation": "read committed"
        #     "pool": True,
        # },
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

REST_FRAMEWORK = {
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework_json_api.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular_jsonapi.schemas.openapi.JsonApiAutoSchema",
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
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
            "maxBytes": 25 * 1024 * 1024,
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
