from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Connect to MongoDB Atlas
MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

# Database
db = client["task_manager"]

# Collection
tasks_collection = db["tasks"]


app = FastAPI()


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Structure of incoming task
class Task(BaseModel):
    name: str


# Convert MongoDB document into normal JSON
def task_helper(task):

    return {
        "id": str(task["_id"]),
        "name": task["name"],
        "completed": task["completed"]
    }


# HOME
@app.get("/")
def home():

    return {
        "message": "Task Manager Backend with MongoDB is Working"
    }


# READ ALL TASKS
@app.get("/tasks")
def get_tasks():

    tasks = []

    for task in tasks_collection.find():
        tasks.append(task_helper(task))

    return tasks


# CREATE TASK
@app.post("/tasks")
def add_task(task: Task):

    new_task = {
        "name": task.name,
        "completed": False
    }

    result = tasks_collection.insert_one(new_task)

    created_task = tasks_collection.find_one({
        "_id": result.inserted_id
    })

    return task_helper(created_task)


# COMPLETE / UNDO TASK
@app.put("/tasks/{task_id}")
def complete_task(task_id: str):

    task = tasks_collection.find_one({
        "_id": ObjectId(task_id)
    })

    if not task:
        return {"error": "Task not found"}

    new_status = not task["completed"]

    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"completed": new_status}}
    )

    updated_task = tasks_collection.find_one({
        "_id": ObjectId(task_id)
    })

    return task_helper(updated_task)


# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):

    result = tasks_collection.delete_one({
        "_id": ObjectId(task_id)
    })

    if result.deleted_count == 0:
        return {"error": "Task not found"}

    return {
        "message": "Task deleted"
    }