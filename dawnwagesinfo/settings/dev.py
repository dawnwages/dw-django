from .base import *

ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DOMAIN = "http://0.0.0.0:8000"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&%&+6u9=a50dsix7=0_5o=$kmi3bn=a^yqw7d5arn#ni90)+&t'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
