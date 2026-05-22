import os
from .base import *

DEBUG = False
# SECURITY WARNING: don't run with debug turned on in production!
TEMPLATE_DEBUG = DEBUG

DOMAIN = "http://0.0.0.0:8000"


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
