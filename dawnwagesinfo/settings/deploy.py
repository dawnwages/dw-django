from socket import gethostname, gethostbyname
from .base import *
import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

DEBUG = False
TEMPLATE_DEBUG = DEBUG


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True