from .base import *

from local_settings import *
from secret_settings import *

# Fix Email Settings
SERVER_EMAIL = "server@crate.io"
DEFAULT_FROM_EMAIL = "donald@crate.io"

DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql_psycopg2"

# Configure Celery
BROKER_TRANSPORT = "redis"
BROKER_HOST = GONDOR_REDIS_HOST
BROKER_PORT = GONDOR_REDIS_PORT
BROKER_VHOST = "0"
BROKER_PASSWORD = GONDOR_REDIS_PASSWORD
BROKER_POOL_LIMIT = 10

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = GONDOR_REDIS_HOST
CELERY_REDIS_PORT = GONDOR_REDIS_PORT
CELERY_REDIS_PASSWORD = GONDOR_REDIS_PASSWORD
