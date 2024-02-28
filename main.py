from fastapi import FastAPI, HTTPException
from huey import RedisHuey
from pydantic import BaseModel
import redis

# Constants
REDIS_PORT = 6379
REDIS_STORAGE_DB = 0
REDIS_HUEY_DB = 1




app = FastAPI()

key_value_store = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=REDIS_STORAGE_DB)

# Configure Huey with Redis as the message store
huey = RedisHuey(url=f"redis://localhost:{REDIS_PORT}/{REDIS_HUEY_DB}")




class Item(BaseModel):
    key: str
    value: str





@huey.task()
def async_get_key(key: str):
    value = key_value_store.get(key)

    if value is None:
        return False
    else:
        return value
     

@huey.task()
def async_create_key(key: str, value: str):
    return key_value_store.set(key, value)

@huey.task()
def async_delete_key(key: str):
    return key_value_store.delete(key) > 0


def get_task_state(task_id: str):
  """Retrieves the state of a task using its ID.

  Args:
      task_id (str): The ID of the task to get the state for.

  Returns:
      str: The state of the task (e.g., PENDING, STARTED, FINISHED, FAILED).
  """
  all_tasks = huey.pending()
  task_info = all_tasks.get(task_id)
  if task_info:
    return task_info['state']
  else:
    # Task not found
    return "Task not found"




@app.get("/")
async def ping():
    return {"res": "pong"}


@app.get("/get/{key}")
async def read_key(key: str):
    res = async_get_key(key)
    value = res()

    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    
    return {"key": key, "value": value}


@app.put("/put")
async def create_key(item: Item):
    # Enqueue the task for background execution
    async_task = async_create_key(item.key, item.value)
    return {"message": "Key creation task enqueued", "task_id": async_task.id}

@app.delete("/delete/{key}")
async def delete_key(key: str):
    # Enqueue the task for background execution
    async_task = async_delete_key(key)
    return {"message": "Key deletion task enqueued", "task_id": async_task.id}

@app.get("/task-state-info/{id}")
async def get_task_state_info(id: str):
    return {"state": get_task_state(id)}