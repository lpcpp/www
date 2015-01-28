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

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = True


ADMINS = (
    ('django', 'lp_cpp@163.com'),
)

EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'lp_cpp@163.com'
EMAIL_HOST_PASSWORD = 'Fe9viu7g'
EMAIL_USER_TLS = True

EMAIL_USER_TO = '517145673@qq.com'

# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'debug_toolbar',
    'blog',
    'gallery',
  #  'ckeditor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
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

MEDIA_ROOT = os.path.join(BASE_DIR, 'gallery/media') 

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 

STATICFILES_DIR = (
    os.path.join(BASE_DIR, 'blog/static'),
    os.path.join(BASE_DIR, 'gallery/static'),
)

VERIFY_CODE_TTF = BASE_DIR + '/static/fonts/LucidaSansRegular.ttf'

#CKEDITOR_UPLOAD_PATH = MEDIA_ROOT
#CKEDITOR_MEDIA_PREFIX = BASE_DIR + '/static/ckeditor'

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_DIRS = ('/Library/Python/2.7/site-packages/debug_toolbar/templates',
                 BASE_DIR + '/blog/templates',
                 BASE_DIR + '/gallery/templates',
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
         'server_log':{
              'level': 'INFO',
              'class': 'logging.handlers.RotatingFileHandler',
              'filename': os.path.join(BASE_DIR + '/www/' +
'logs/', 'log'),
              'formatter': 'standard',
          },
    },
    'loggers':{
        'runlog':{
            'handlers':['default', 'server_log'],
            'propagate': False
        },
    },
}
