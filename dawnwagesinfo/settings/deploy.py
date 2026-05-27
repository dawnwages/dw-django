from socket import gethostname, gethostbyname
from dotenv import load_dotenv
from .base import *
import boto3
from botocore.config import Config
from dawnwagesinfo import custom_backends

load_dotenv()

DEBUG = os.environ.get('DEBUG')
ENVIRONMENT = os.environ.get('ENVIRONMENT')
HOST = os.environ.get('HOST')
TEMPLATE_DEBUG = DEBUG
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# S3 Configuration
USE_S3 = os.getenv('USE_S3') == 'TRUE'

# Dynamically request token

# try:
#     # Uses your machine's/server's default AWS credentials
#     rds_client = boto3.client('rds', region_name=os.getenv('AWS_DEFAULT_REGION'))
#     db_token = rds_client.generate_db_auth_token(
#         DBHostname=os.getenv('HOST'),
#         Port=os.getenv('PORT'),
#         DBUsername=os.getenv('DB_USER')
#     )
#     print("Successfully generated AWS IAM token for database connection.")
# except Exception as e:
#     # Fallback to env password if boto3 fails locally
#     print(f"AWS IAM Token generation failed: {e}")
#     db_token = os.getenv('DB_PASSWORD')

DB_HOST = os.getenv('HOST')
DB_NAME = os.getenv('NAME')
DB_USER = os.getenv('DB_USER')

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  # Standard backend
#         'NAME': 'dummy_db',
#         'USER': 'dummy_user', 
#         'PASSWORD': 'dummy_pass',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'dawnwagesinfo.custom_backends',  # Use our custom backend
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': '',  # Use the dynamically generated token
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    },
}



# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# DEBUG_PROPAGATE_EXCEPTIONS = True
# COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)
# # Logging with LogDNA

# LOGGING = {
#     # Other logging settings...
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'logdna': {
#             'level': logging.DEBUG,
#             'class': 'logging.handlers.LogDNAHandler',
#             'key': os.environ.get('LOGDNA_KEY'),
#             'options': {
#                 'app': 'dawnwagesinfo',
#                 'env': 'production',
#                 'index_meta': True,
#             },
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['logdna'],
#             'level': logging.DEBUG
#         },
#     },
# }
