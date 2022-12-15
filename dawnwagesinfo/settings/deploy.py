from socket import gethostname, gethostbyname
from .base import *
import os
import dj_database_url
import django_heroku
import logging
from logdna import LogDNAHandler
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG')
TEMPLATE_DEBUG = DEBUG

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Activate Django-Heroku.
django_heroku.settings(locals())
if os.getenv('EVNVIRONMENT') == 'deploy':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'dawnwagesinfo',                      # Or path to database file if using sqlite3.
            'USER': os.environ['USER'],                      # Not used with sqlite3.
            'PASSWORD': os.environ['PASSWORD'],                  # Not used with sqlite3.
            'HOST': os.environ['HOST'],                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require'
            },                      # Set to empty string for default. Not used with sqlite3.
        },
    }

# S3 Configuration
USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'dawnwagesinfo.settings.storage.PublicMediaStorage'
    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'dawnwagesinfo.settings.storage.PrivateMediaStorage'
else:
    MEDIA_URL = '/mediafiles/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DEBUG_PROPAGATE_EXCEPTIONS = True
COMPRESS_ENABLED = os.getenv('COMPRESS_ENABLED', False)
# Logging with LogDNA

LOGGING = {
    # Other logging settings...
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logdna': {
            'level': logging.DEBUG,
            'class': 'logging.handlers.LogDNAHandler',
            'key': os.getenv('LOGDNA_KEY'),
            'options': {
                'app': 'dawnwagesinfo',
                'env': 'production',
                'index_meta': True,
            },
        },
    },
    'loggers': {
        '': {
            'handlers': ['logdna'],
            'level': logging.DEBUG
        },
    },
}
