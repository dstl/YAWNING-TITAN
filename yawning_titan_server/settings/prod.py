"""Django settings for a development environment"""

from yawning_titan_server.settings.base import *

# DEBUG CONFIGURATION
DEBUG = True
# END DEBUG CONFIGURATION

# Stop spamming the console with irrelevant logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    "root": {
        "level": "WARNING",
        "handlers": ["null"],
        "propagate": True,
    },
    "loggers": {
        'django.server': {
            'handlers': ['null'],
            'level': 'WARNING',
            'propagate': False,
        }
    },
}
