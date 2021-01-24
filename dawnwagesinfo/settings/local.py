from .dev import *

USE_LOCAL_STORAGE = True

MAILINGS = [""]
MAILING_FILES_PATH = os.path.join(PROJECT_PATH, '..', 'data')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CALENDAR_DOMAIN = '0.0.0.0:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dawnwagesinfo',                      # Or path to database file if using sqlite3.
        'USER': 'dawn',                      # Not used with sqlite3.
        'PASSWORD': '4',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

UPLOAD_ROOT = os.path.abspath(os.path.join(BASE_DIR, "uploads"))

APACHE_X_SENDFILE = False

RELEVANT_EMAIL_DOMAINS = [
    '@mandrill.unstable.dawnwages.info',
    '@dawnwages.info'
]

ENVIRONMENT = 'local'