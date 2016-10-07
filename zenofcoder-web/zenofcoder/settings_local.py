# encoding: utf-8
# encoding: utf-8
from os import path
import dotenv

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
dotenv_path = path.join(path.dirname(__file__), '..', '.env_local')
dotenv.load_dotenv(dotenv_path)
from .settings import *

SECRET_KEY = 'jh^r@e8q&i#p^(u2#dyxn-n2+!2%u8zuv_5wkovbzg9ftqy9a$'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LOGS_DIR = '/home/kuba/temp/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'clear': {
            'format': '%(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'error_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR + 'django-errors.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'debug_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR + 'django-debugmess.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'standard'
        }
    },
    'loggers': {
        'debugmess': {
            'handlers': ['debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.requests': {
            'handlers': ['error_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['error_log'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')
