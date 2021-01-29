from socket import gethostname, gethostbyname
from .base import *

#: deploy environment - e.g. "staging" or "production"
ENVIRONMENT = os.environ["ENVIRONMENT"]
os.environ.setdefault("BROKER_HOST", "127.0.0.1:5672")

DEBUG = False
TEMPLATE_DEBUG = DEBUG
if ENVIRONMENT == "production":
    TWILIO_DEBUG_MODE = False
    DOMAIN = "https://www.dawnwages.info"

ALLOWED_HOSTS = [
    "dawnwages.info",
    "localhost",
    "127.0.0.1",
    "http://161.35.190.151/",
    gethostname(),
    gethostbyname(gethostname()),
    os.environ["DOMAIN"],
]

try:
    from .local import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django',                      # Or path to database file if using sqlite3.
        'USER': 'django',                      # Not used with sqlite3.
        'PASSWORD': '2706e1f5e33a8a797895993d8b82fa4c',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True