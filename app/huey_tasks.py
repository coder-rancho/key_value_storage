"""
Huey Background Tasks Module

This module defines background tasks using Huey for key-value storage operations.
"""

import redis
from huey import RedisHuey
from config import REDIS_HUEY_DB, REDIS_PORT, REDIS_STORAGE_DB, REDIS_SERVICE_NAME


################################################
# Configurations
################################################

# Configure Redis store
key_value_store = redis.StrictRedis(host=REDIS_SERVICE_NAME, port=REDIS_PORT, db=REDIS_STORAGE_DB)

# Configure Huey with Redis as the message store
huey = RedisHuey(name='task-queue', store_none=True, url=f"redis://{REDIS_SERVICE_NAME}:{REDIS_PORT}/{REDIS_HUEY_DB}")


################################################
# TASKS
################################################

@huey.task()
def hello():
    """
    Background task to print a greeting message.

    Returns:
        str: Greeting message.
    """
    print("task executing...")
    return "Hello world"

@huey.task()
def async_get_key(key: str):
    """
    Background task to asynchronously retrieve the value associated with a key.

    Args:
        key (str): The key to retrieve.

    Returns:
        bytes: The value associated with the key.
    """
    value = key_value_store.get(key)
    return value

@huey.task()
def async_create_key(key: str, value: str):
    """
    Background task to asynchronously create a new key-value pair.

    Args:
        key (str): The key to create.
        value (str): The value associated with the key.

    Returns:
        int: Status code indicating the success of the operation.
    """
    return key_value_store.set(key, value)

@huey.task()
def async_delete_key(key: str):
    """
    Background task to asynchronously delete a key.

    Args:
        key (str): The key to delete.

    Returns:
        int: Status code indicating the success of the operation.
    """
    return key_value_store.delete(key) > 0


###############################################
# Utilities
###############################################

def get_task_state(task_id: str):
    """
    Retrieves the state of a task using its ID.

    Args:
        task_id (str): The ID of the task to get the state for.

    Returns:
        str: The state of the task (e.g., PENDING, STARTED, FINISHED, FAILED).
    """
    all_tasks = huey.pending()
    for task in all_tasks:
        if task.id == task_id:
            return task
    return "Task not found"
