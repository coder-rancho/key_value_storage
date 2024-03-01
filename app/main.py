from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.huey_tasks import *


app = FastAPI()

class Item(BaseModel):
    key: str
    value: str



def get_task_state(task_id: str):
  """Retrieves the state of a task using its ID.

  Args:
      task_id (str): The ID of the task to get the state for.

  Returns:
      str: The state of the task (e.g., PENDING, STARTED, FINISHED, FAILED).
  """
  all_tasks = huey.pending()
  for task in all_tasks:
      if (task.id == task_id):
          print(dir(task))
          return task
  return "Task not found"
    




@app.get("/")
async def ping():
    res = hello()
    msg = res()
    return {"res": msg}


@app.get("/get/{key}")
async def read_key(key: str):
    res = async_get_key(key)
    value = res(blocking=True)
    # value = key_value_store.get(key)

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