"""
Django settings for planimbly project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from pathlib import Path

import django.conf.global_settings
from environs import Env
from huey import RedisHuey
from redis import ConnectionPool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environmental variables
env = Env()
env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default='7^j)k2u*-6-omh)u2f#n@yldbnd=82@vvg5&o-td^4eo_96=#9')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'planimbly.herokuapp.com']
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Internal
    'apps.accounts',
    'apps.organizations',
    'apps.schedules',

    # External
    'crispy_forms',
    'widget_tweaks',
    'rest_framework',
    'django_extensions',
    'huey.contrib.djhuey',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'planimbly.middleware.DenyAccesHueyMiddleware',
]

ROOT_URLCONF = 'planimbly.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'planimbly.context_processors.organization_data'
            ],
        },
    },
]

WSGI_APPLICATION = 'planimbly.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3")
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Authorization
AUTH_USER_MODEL = 'accounts.Employee'
LOGIN_REDIRECT_URL = "employees_manage"

# SSL
if env.bool("ENABLE_SSL", default=True):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# SSL when using reverse proxy
if env.bool("ENABLE_PROXY_SSL", default=False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Date input
DATE_INPUT_FORMATS = [
    *django.conf.global_settings.DATE_INPUT_FORMATS,
]

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Crispy config
CRISPY_TEMPLATE_PACK = 'bootstrap'

VUE2_CDN = 'https://cdn.jsdelivr.net/npm/vue/dist/vue.min.js'
VUE3_CDN = 'https://unpkg.com/vue@3.2.37/dist/vue.global.prod.js'
ENV_STAGE = env.str("ENV_STAGE", default='').upper()

# Static browser handling & Vue cdn paths for development
if DEBUG:
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)
    VUE2_CDN = 'https://cdn.jsdelivr.net/npm/vue/dist/vue.js'
    VUE3_CDN = 'https://unpkg.com/vue@3'

# HUEY config
USE_HUEY = env.bool("USE_HUEY", default=False)
pool = ConnectionPool(host='localhost', port=6379, max_connections=20)
HUEY = RedisHuey('planimbly', connection_pool=pool)

# Log 500 Error
DEBUG_PROPAGATE_EXCEPTIONS = True
