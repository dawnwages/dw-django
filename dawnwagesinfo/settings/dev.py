import os
from .base import *

# Local development settings. manage.py uses these by default; production
# (the Docker image) sets DJANGO_SETTINGS_MODULE to dawnwagesinfo.settings.deploy.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Local SQLite database (db.sqlite3 is gitignored). Production uses Aurora
# PostgreSQL, configured in deploy.py.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DOMAIN = "http://0.0.0.0:8000"


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

MAILERS = {"default": {"BACKEND": "django.core.mail.backends.console.EmailBackend"}}

