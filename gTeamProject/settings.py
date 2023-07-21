from pathlib import Path

from aws import AWSManager

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
SECRET_KEY = AWSManager.get_secret("django")["SECRET_KEY"]


DEBUG = True  # Set False when production!!

ALLOWED_HOSTS = ["*"]  # 검토 필요

AUTH_USER_MODEL = "accounts.User"

# Django의 인증 시스템에서 사용자를 자연키로 검색하기 위한 설정
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# 세션 관리를 위한 쿠키 설정
SESSION_COOKIE_HTTPONLY = True  # JavaScript에서 접근 불가능하도록 설정
SESSION_COOKIE_SECURE = False  # HTTPS에서만 쿠키 전송
SESSION_COOKIE_SAMESITE = "Lax"  # SameSite 설정
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2주(초단위)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "rest_framework",
    "question",
    "character",
    "drf_yasg",
    "corsheaders",
    "django_celery_results",
    "django_redis",
]

# Gunicorn 설정
INSTALLED_APPS += ["gunicorn"]
# Gunicorn을 웹 서버로 사용하기 위해 WSGI_APPLICATION 설정
WSGI_APPLICATION = "gTeamProject.wsgi.application"
# Gunicorn이 사용할 워커 프로세스 수 설정
# 예시: 워커 프로세스를 4개로 설정
# NUM_WORKERS = 4 # 별도로 설정 안해도 됨, Gunicorn에서 설정해줌
# Gunicorn 실행 명령어
# CMD = "gunicorn gTeamProject.wsgi:application --bind 0.0.0.0:8000"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "gTeamProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gTeamProject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

db_secret = AWSManager.get_secret("teacheer-db")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": db_secret["dbname"],
        "USER": db_secret["username"],
        "PASSWORD": db_secret["password"],
        "HOST": db_secret["host"],
        "PORT": db_secret["port"],
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True  # 검토 필요

# CELERY SETTINGS
CELERY_TIMEZONE = "Asia/Seoul"
CELERY_BROKER_URL = "amqp://rabbitmq:5672"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
    }
}
