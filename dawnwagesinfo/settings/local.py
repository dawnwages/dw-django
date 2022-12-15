from .dev import *
from django.core.management.utils import get_random_secret_key
import os
from dotenv import load_dotenv

load_dotenv()

USE_LOCAL_STORAGE = True

SECRET_KEY = get_random_secret_key()

MAILINGS = [""]
MAILING_FILES_PATH = os.path.join(PROJECT_PATH, '..', 'data')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CALENDAR_DOMAIN = '0.0.0.0:8000'
if os.getenv('EVNVIRONMENT') == 'local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'dawnwagesinfo',                      # Or path to database file if using sqlite3.
            'USER': 'dawnwagesinfo_user',                      # Not used with sqlite3.
            'PASSWORD': 4,                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': 5432,                      # Set to empty string for default. Not used with sqlite3.
        },
    }

UPLOAD_ROOT = os.path.abspath(os.path.join(BASE_DIR, "uploads"))

APACHE_X_SENDFILE = False

RELEVANT_EMAIL_DOMAINS = [
    '@mandrill.unstable.dawnwages.info',
    '@dawnwages.info'
]