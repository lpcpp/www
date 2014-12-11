"""
Django settings for www project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^@+%p3=d*0fiwxo+i5sw+orqmfqm!*ubj&jwjt%9s((qd651%x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'blog',
    'gallery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'www.urls'

WSGI_APPLICATION = 'www.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
#        'NAME': os.path.join(BASE_DIR, 'blogdb'),
        'NAME': 'blogdb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR + '/gallery/media/' 
MEDIA_URL = '/gallery/media/' 
STATIC_ROOT = ''


INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_DIRS = ('/Library/Python/2.7/site-packages/debug_toolbar/templates',
                 '/Users/luopeng/project/www/blog/templates',
                 '/Users/luopeng/project/www/gallery/templates',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters':{
        'standard':{
            'format': '%(asctime)s[%(threadName)s:%(thread)d][%(name)s:%(lineno)d][%(levelname)s]-%(message)s'
        },
    },
    'filters':{
     },
    'handlers':{
         'default':{
              'level': 'DEBUG',
              'class': 'logging.StreamHandler',
              'formatter': 'standard',
          },
    },
    'loggers':{
        'runlog':{
            'handlers':['default',],
            'propagate': False
        },
    },
}
