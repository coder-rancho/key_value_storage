import os

REDIS_SERVICE_NAME = os.getenv("REDIS_SERVICE_NAME") or 'localhost'
REDIS_PORT = os.getenv("REDIS_PORT") or 6379    # default port
REDIS_STORAGE_DB = 0
REDIS_HUEY_DB = 1