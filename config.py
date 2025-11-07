"""Flask Configuration"""

import os
from datetime import timedelta

# Environment
ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG = ENV == 'development'

# Secret key for session management
SECRET_KEY = os.environ.get('SECRET_KEY', 'algorithm-battlefield-arena-secret-key-2024-dev')

# Session configuration
PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
SESSION_PERMANENT = True
SESSION_TYPE = 'filesystem'
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Flask settings
JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR = False

# Max content length (for file uploads, etc.)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Timeout for algorithm execution (in seconds)
ALGORITHM_TIMEOUT = 30

# Default algorithm input size
DEFAULT_INPUT_SIZE = 50

# Maximum algorithm input size
MAX_INPUT_SIZE = 500

# Algorithm configuration
ALGORITHM_CONFIG = {
    'sorting': {
        'input_type': 'array',
        'default_size': 50,
        'max_size': 500
    },
    'searching': {
        'input_type': 'array',
        'default_size': 50,
        'max_size': 500
    },
    'shortest path': {
        'input_type': 'graph',
        'default_size': 20,
        'max_size': 100
    },
    'mst': {
        'input_type': 'edges',
        'default_size': 20,
        'max_size': 100
    },
    'graph': {
        'input_type': 'graph',
        'default_size': 20,
        'max_size': 100
    },
    'string matching': {
        'input_type': 'text',
        'default_size': 100,
        'max_size': 10000
    },
    'subset generation': {
        'input_type': 'array',
        'default_size': 15,
        'max_size': 25
    },
    '0/1 knapsack': {
        'input_type': 'knapsack',
        'default_size': 15,
        'max_size': 20
    }
}

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
