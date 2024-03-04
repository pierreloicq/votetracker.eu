"""
Django settings for yvm_site project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if config('MODE') == 'PROD':
    DEBUG = False
    STATIC_ROOT = config('STATIC_ROOT')
    STATIC_URL  = config('STATIC_URL')
elif config('MODE') == 'DEV':
    DEBUG = True
    STATIC_URL = 'static/'


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# added for prod
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True


### for django to find the .mo files 
LOCALE_PATHS = [BASE_DIR / "locale"]


# Application definition
INSTALLED_APPS = [
    'yvm.apps.YvmConfig',
    # 'django.contrib.admin',
    'django.contrib.admin.apps.SimpleAdminConfig',
    # #https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#customizing-
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#overriding-the-default-admin-site
    # "yvm.apps.MyAdminConfig",  # replaces 'django.contrib.admin' 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yvm_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yvm_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': f"django.db.backends.{config('DB_ENGINE')}",
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PORT': config('DATABASE_PORT', cast=int),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1', # An empty string means localhost
    }
}

if config('DB_ENGINE') == 'mysql':
    DATABASES['default']['OPTIONS'] = {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'fr-fr'

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
    ('nl', 'Dutch'),
]


TIME_ZONE = 'CET'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL = 'yvm.MepUser' # was not working finally


EMAIL_BACKEND = config('EMAIL_BACKEND')

if EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
    print(f"{EMAIL_BACKEND=}")
elif EMAIL_BACKEND == "django.core.mail.backends.filebased.EmailBackend":
    EMAIL_FILE_PATH = config('EMAIL_FILE_PATH')
    with open(f"{EMAIL_FILE_PATH}/backend.txt", 'w') as file:
        file.write(f"{EMAIL_BACKEND=}")

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

LOGIN_URL = '/comment_my_stances/'