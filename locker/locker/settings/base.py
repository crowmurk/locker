import os

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Build paths inside the project

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Loading secret key

SECRET_KEY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'secret.key',
)

SECRET_KEY = open(SECRET_KEY_FILE).read().strip()

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_tables2',
    'django_extensions',
    'django_filters',
    'import_export',
    'crispy_forms',
    'widget_tweaks',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
    'employee.apps.EmployeeConfig',
    'client.apps.ClientConfig',
    'calc.apps.CalcConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware to use

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'global_login_required.GlobalLoginRequiredMiddleware',
]

# Database

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# URLs
ROOT_URLCONF = 'locker.urls'

# Template engines

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'locker.wsgi.application'

# Password validation

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

# Login
LOGIN_REDIRECT_URL = '/'

# All but this views are login requred
PUBLIC_VIEWS = [
    'django.contrib.auth.views.LoginView',
]

# All but this paths are login requred
PUBLIC_PATHS = [
    r'^/i18n/setlang',
]

# Internationalization

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Bootstrap 4 support

CRISPY_TEMPLATE_PACK = 'bootstrap4'
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Admin config

ADMIN_SITE_HEADER = _("Industry-Spectrum administration")

ADMIN_SITE_TITLE = _("Industry-Spectrum site admin")

ADMIN_INDEX_TITLE = _('Site administration')
