from django.conf import settings

AXES_VERBOSE = False
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = 'lockout.html'

if settings.DEBUG:
    AXES_NEVER_LOCKOUT_WHITELIST = True
    AXES_IP_WHITELIST = ['127.0.0.1', '0.0.0.0']

if not settings.DEBUG:
    # When behind nginx
    AXES_PROXY_COUNT = 1
    AXES_META_PRECEDENCE_ORDER = [
        'HTTP_X_FORWARDED_FOR',
        'REMOTE_ADDR',
    ]
