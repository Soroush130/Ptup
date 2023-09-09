from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/dist/js', 'serviceworker.js')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^@7s--za+z%%d8^i*&z#gjewhvlw!(-euz#o16$^c&2&ize!q_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

DJANGO_DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_render_partial',
    'django.contrib.humanize',
    'django_quill',
    'pwa',
]

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'customers.apps.CustomersConfig',
    'doctors.apps.DoctorsConfig',
    'ptup_messages.apps.PtupMessagesConfig',
    'ptup_utilities.apps.PtupUtilitiesConfig',
    'illness.apps.IllnessConfig',
    'healing_content.apps.HealingContentConfig',
    'foundation_course.apps.FoundationCourseConfig',
    'followup.apps.FollowupConfig',
]

INSTALLED_APPS = DJANGO_DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Ptup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ptup.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',

        ### Postgres
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ptup',
        'USER': 'postgres',
        'PASSWORD': 'ptup',
        'HOST': '127.0.0.1',
        'PORT': '5430',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets")
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media_root")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Messages
# MESSAGE_TAGS = {
#     messages.DEBUG: 'debug',
#     messages.INFO: 'info',
#     messages.SUCCESS: 'success',
#     messages.WARNING: 'warning',
#     messages.ERROR: 'error',
# }

# Setting Session App
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 86400

# Setting Kavenegar
KAVENEGAR_API_KEY = '2F776B494544336F2F516C456C704F52737659384D577855566B46617031334F4A796C767A564E494476343D'

# PWA
PWA_APP_NAME = 'PTUP'
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': 'static/dist/img/logo_ptup.png',
        'sizes': '512x512'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/dist/img/logo_ptup.png',
        'sizes': '512x512'
    }
]
PWA_APP_DIR = 'rtl'
PWA_APP_LANG = 'en-US'











