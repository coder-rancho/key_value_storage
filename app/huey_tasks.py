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
    print("task executing...")
    return "Hello world"


@huey.task()
def async_get_key(key: str):
    value = key_value_store.get(key)
    return value
     

@huey.task()
def async_create_key(key: str, value: str):
    return key_value_store.set(key, value)

@huey.task()
def async_delete_key(key: str):
    return key_value_store.delete(key) > 0