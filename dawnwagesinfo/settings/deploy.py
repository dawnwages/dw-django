from socket import gethostname, gethostbyname
from .base import *

#: deploy environment - e.g. "staging" or "production"
ENVIRONMENT = os.environ.get("ENVIRONMENT")
os.environ.setdefault("BROKER_HOST", "127.0.0.1:5672")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "&%&+6u9=a50dsix7=0_5o=$kmi3bn=a^yqw7d5arn#ni90)+&t")


DEBUG = os.environ.get('DJANGO_DEBUG', 'False')
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
        'NAME': 'dawnwagesinfo',                      # Or path to database file if using sqlite3.
        'USER': 'dawnwagesinfo_user',                      # Not used with sqlite3.
        'PASSWORD': 'ohSh111t',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True