from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY -> 임의로 만들어져 있는 키
SECRET_KEY = "django-insecure-h%hj*4^5(1r84@v!=v=0)=^2@k_q50$c=eh61kpr=&p0idlwkn"


# Local에서 개발할 경우 1, 그렇지 않은 경우 0
DEBUG = True

# EC2의 주소
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.User'

# Django의 인증 시스템에서 사용자를 자연키로 검색하기 위한 설정
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


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
]

# Gunicorn 설정
INSTALLED_APPS += ['gunicorn']
# Gunicorn을 웹 서버로 사용하기 위해 WSGI_APPLICATION 설정
WSGI_APPLICATION = 'gTeamProject.wsgi.application'
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "teacheer",
        "USER": "admin",
        "PASSWORD": "teamgbe13579",
        "HOST": "teacheer-db.cz3svk2xsnsk.ap-northeast-2.rds.amazonaws.com",
        "PORT": "3306",
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
