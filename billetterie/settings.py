"""
Django settings for billetterie project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '^&2upg8b26db6l#3o&2jsfta2@mkek^pan^a-h29v1gi&l%57!')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ENV', 'development') != 'production'

ALLOWED_HOSTS = os.environ.get('HOST', 'localhost').split(',')

CORS_ORIGIN_WHITELIST = [
    'billetterie.bde-insa-lyon.fr',
    'localhost:4200',
    '127.0.0.1:4200',
    '127.0.0.1:8000',
    'localhost:8000'
] + os.environ.get('DOMAINS', '').split(',')

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    'billetterie.bde-insa-lyon.fr',
    'localhost:4200',
    '127.0.0.1:4200',
] + os.environ.get('DOMAINS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "anymail",
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'api.apps.ApiConfig',
    'mercanet'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'billetterie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'billetterie.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.IsAuthenticatedAndReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7)
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3'), conn_max_age=600)
}

ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY', ''),
    "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_DOMAIN', 'demo'),  # your Mailgun domain, if needed
}

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'billetterie@gala.bde-insa-lyon.fr')

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    #  No conditions on password for development phase
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

BILLEVENT = {
    'FRONTEND_URL': os.environ.get('FRONTEND_URL', 'http://localhost:4200'),
    'MERCANET': {
        'INTERFACE_VERSION': os.environ.get('MERCANET_INTERFACE_VERSION', 'IR_WS_2.18'),
        'KEY_VERSION': os.environ.get('MERCANET_KEY_VERSION', '1'),
        'MERCHANT_ID': os.environ.get('MERCANET_MERCHANT_ID', '211000021310001'),
        'URL': os.environ.get('MERCANET_URL', 'https://payment-webinit-mercanet.test.sips-atos.com/rs-services/v2/paymentInit'),
        'SECRET_KEY': os.environ.get('MERCANET_SECRET_KEY', 'S9i8qClCnb2CZU3y3Vn0toIOgz3z_aBi79akR30vM9o'),
        'REPONSE_AUTO_URL': os.environ.get('MERCANET_REPONSE_AUTO_URL', 'http://mercanet.pvienne.ultrahook.com/pay/auto/'),
    }
}
