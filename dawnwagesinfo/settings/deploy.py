from socket import gethostname, gethostbyname
from .base import *
import os
import dj_database_url
import django_heroku
import logging
from logdna import LogDNAHandler

DEBUG = False
TEMPLATE_DEBUG = DEBUG


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Activate Django-Heroku.
django_heroku.settings(locals())

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    gethostname(),
    gethostbyname(gethostname()),
    'logs.dna.com',
    'dawn-wages-info.herokuapp.com'
]

DEBUG_PROPAGATE_EXCEPTIONS = True
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)
# Logging with LogDNA

LOGGING = {
    # Other logging settings...
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logdna': {
            'level': logging.DEBUG,
            'class': 'logging.handlers.LogDNAHandler',
            'key': os.environ.get('LOGDNA_KEY'),
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
