"""
FastAPI Application for Key-Value Storage

This FastAPI application provides endpoints for managing key-value pairs using background tasks.

Endpoints:
- `/`: Ping endpoint that enqueues a background task.
- `/get/{key}`: Retrieve the value for a given key.
- `/put`: Create a new key-value pair.
- `/delete/{key}`: Delete a key-value pair.
- `/task-state-info/{id}`: Retrieve the state information for a background task.

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.huey_tasks import *

app = FastAPI()

class Item(BaseModel):
    key: str
    value: str

@app.get("/")
async def ping():
    """
    Ping endpoint that enqueues a background task.

    Returns:
        dict: A message indicating the success of the task enqueuing.
    """
    res = hello()
    msg = res(blocking=True)
    return {"res": msg}

@app.get("/get/{key}")
async def read_key(key: str):
    """
    Retrieve the value for a given key.

    Args:
        key (str): The key for which to retrieve the value.

    Returns:
        dict: The key-value pair.
    """
    res = async_get_key(key)
    value = res(blocking=True)

    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    
    return {"key": key, "value": value}

@app.put("/put")
async def create_key(item: Item):
    """
    Create a new key-value pair.

    Args:
        item (Item): The item containing the key-value pair to be created.

    Returns:
        dict: A message indicating the success of the task enqueuing.
    """
    async_task = async_create_key(item.key, item.value)
    return {"message": "Key creation task enqueued", "task_id": async_task.id}

@app.delete("/delete/{key}")
async def delete_key(key: str):
    """
    Delete a key-value pair.

    Args:
        key (str): The key to be deleted.

    Returns:
        dict: A message indicating the success of the task enqueuing.
    """
    async_task = async_delete_key(key)
    return {"message": "Key deletion task enqueued", "task_id": async_task.id}

@app.get("/task-state-info/{id}")
async def get_task_state_info(id: str):
    """
    Retrieve the state information for a background task.

    Args:
        id (str): The ID of the task.

    Returns:
        dict: The state information of the task.
    """
    return {"state": get_task_state(id)}