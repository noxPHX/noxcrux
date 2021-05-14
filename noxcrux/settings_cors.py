import os


def get_bool_env(env_var, default='False'):
    return os.getenv(env_var, default).lower() in ('true', '1', 't')


CORS_ALLOW_ALL_ORIGINS = get_bool_env("CORS_ALLOW_ALL_ORIGINS")

if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost").split(",")

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
]
