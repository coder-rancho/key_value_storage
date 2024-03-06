"""
Configuration Module

This module defines configuration settings for the key-value storage application.
"""

import os

# Redis configuration
REDIS_SERVICE_NAME = os.getenv("REDIS_SERVICE_NAME") or 'localhost'
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))  # Default port if not specified
REDIS_STORAGE_DB = 0
REDIS_HUEY_DB = 1
